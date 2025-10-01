from fastapi import FastAPI, Depends, HTTPException
from db import get_db
from schemas import UserCreate, UserResponse, PaymentResponse, PaymentCreate, WebhookIn
from models import User, Payment
from services import hash_password, save_transaction_log
from sqlalchemy.orm import query
import uvicorn 
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/create-user", response_model=UserResponse)
def create_user(user: UserCreate, db=Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    secure_password = hash_password(user.password)  
    new_user = User(
        name = user.name,
        email = user.email,
        phone_number = user.phone_number,
        password = secure_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/payments/{user_id}", response_model=PaymentResponse)
def create_payment(user_id:int, payment: PaymentCreate, db=Depends(get_db)):
    if not db.query(User).filter(User.id == user_id).first():
        raise HTTPException(status_code=404, detail="User not found")
    
    if db.query(Payment).filter(Payment.user_id == user_id, Payment.status == 'INITIATED').first():
        raise HTTPException(status_code=400, detail="User has an ongoing payment")
    
    new_payment = Payment(
        user_id = user_id,
        amount = payment.amount,
        currency = payment.currency
    )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)

    outgoing_payload = {
        "payment_id": new_payment.id,
        "amount": str(new_payment.amount),
        "status": new_payment.status,
        "user": {"name": new_payment.user.name, "email": new_payment.user.email},
        "callback_url": "http://localhost:8001/webhook/payment-status"
    }

    # Log the outgoing webhooka
    save_transaction_log(
        db,
        direction="OUTGOING",
        url="http://localhost:8001/webhook/payment-status",  
        payload=json.dumps(outgoing_payload, default=str),
        status_code=0  # Simulated status code
    )

    return new_payment

@app.post('/webhook/payment-status')
def payment_webhook(payload: WebhookIn, db=Depends(get_db)):
    payment = db.query(Payment).filter(Payment.id == payload.payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    # Update payment status based on webhook payload from third-party service
    payment.status = payload.status
    
    db.commit()
    db.refresh(payment)

    # Log the incoming webhook
    save_transaction_log(
        db,
        direction="INCOMING",
        url="http://localhost:8001/webhook/payment-status",  # Simulated URL
        payload=json.dumps(payload.dict(), default=str),
        status_code=200
    )

    return vars(payment)



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

