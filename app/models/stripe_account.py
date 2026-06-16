
# ============================================================
# app/models/stripe_account.py
# ============================================================
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.base import Base
 
 
class StripeAccount(Base):
    __tablename__ = "stripe_accounts"
 
    id = Column(Integer, primary_key=True, index=True)
    cafe_id = Column(Integer, ForeignKey("cafes.id"), unique=True, nullable=False)
    stripe_account_id = Column(String, unique=True, nullable=False)  # acct_xxx
    is_onboarded = Column(Boolean, default=False)   # завершил ли кафе onboarding
    charges_enabled = Column(Boolean, default=False)
    payouts_enabled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
 
    cafe = relationship("Cafe", back_populates="stripe_account")
 