from pydantic import BaseModel, EmailStr, Field
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
        orm_mode = True

class PaymentCreate(BaseModel):
    amount: decimal
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
        orm_mode = True

class WebhookIn(BaseModel):
    payment_id: int
    score: int
    amount: decimal
    status: str
    
   
    
