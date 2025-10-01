from pydantic import BaseModel, EmailStr, Field, condecimal
from decimal import Decimal as decimal


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone_number: str = Field(min_length=8, max_length=15)
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone_number: str

    class Config:
        from_attributes = True

class PaymentCreate(BaseModel):
    user_id: int
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    currency: str

class PaymentResponse(BaseModel):
    id: int
    amount: decimal
    currency: str
    user_id: int
    status: str
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True

class WebhookIn(BaseModel):
    payment_id: int 
    score: int
    amount: decimal
    status: str
    
   
    
