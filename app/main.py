from fastapi import FastAPI, Depends, HTTPException
from db import get_db
from schemas import UserCreate, UserResponse
from models import User
from services import hash_password
from sqlalchemy.orm import query
import uvicorn 

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)

