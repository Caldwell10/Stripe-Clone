from db import Base
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, DECIMAL, CheckConstraint
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True, index=True)
    password = Column(String, nullable=False)

    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(DECIMAL(12,2), nullable=False)
    currency = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    status = Column(String, server_default='INITIATED', nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="payments")

    __table_args__ = (
        CheckConstraint('amount > 0', name='check_amount_positive'),
        CheckConstraint("status IN ('INITIATED', 'COMPLETED', 'FAILED')", name='check_status_valid'),
    )

class Transaction_Logs(Base):
    __tablename__ = 'transaction_logs'

    id = Column(Integer, primary_key=True, index=True)
    direction = Column(String, nullable=False)  # INCOMING or OUTGOING
    url = Column(String, nullable=False) # URL of the third-party service
    payload = Column(String, nullable=False)
    status_code = Column(Integer, nullable=False)
