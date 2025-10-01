from db import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, func
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")

class Payments(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    status = Column(String, server_default='PENDING')
    created_at = Column(String, nullable=False, server_default=func.now())
    updated_at = Column(String, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")

class Transaction_Logs(Base):
    __tablename__ = 'transaction_logs'

    id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey('payments.id'))
    status = Column(String, nullable=False)
    timestamp = Column(String, nullable=False)
    payment = relationship("Payment")
