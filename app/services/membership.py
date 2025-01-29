from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import User

# Membership pricing
MEMBERSHIP_PRICING = {
    "PLUS": 50000,       # 50,000 Toman
    "PREMIUM": 200000,   # 200,000 Toman
}

def upgrade_membership(db: Session, user: User, membership_type: str):
    """
    Upgrade users membership if they have enough balance in their wallet.
    """
    # Validate membership type
    if membership_type not in MEMBERSHIP_PRICING:
        raise HTTPException(status_code=400, detail="Invalid membership type")

    membership_price = MEMBERSHIP_PRICING[membership_type]

    # Check if user has enough balance
    if user.wallet_money_amount < membership_price:
        raise HTTPException(status_code=400, detail="Insufficient wallet balance")

    # Deduct the money from wallet
    user.wallet_money_amount -= membership_price

    # Set the membership type & expiration date (30 days from now)
    user.subscription_model = membership_type
    user.subscription_end_time = datetime.utcnow() + timedelta(days=30)

    db.commit()
    db.refresh(user)

    return user
