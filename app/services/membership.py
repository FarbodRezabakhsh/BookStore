from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Customer

# Membership pricing
# Membership pricing (Ensure keys are uppercase)
MEMBERSHIP_PRICING = {
    "PLUS": 50000,       # 50,000 Toman
    "PREMIUM": 200000,   # 200,000 Toman
}

def upgrade_membership(db: Session, customer: Customer, membership_type: str):
    """
    Upgrade customer's membership if they have enough balance in their wallet.
    """
    membership_type = membership_type.upper()  # Convert to uppercase to match dictionary keys

    # Validate membership type
    if membership_type not in MEMBERSHIP_PRICING:
        raise HTTPException(status_code=400, detail="Invalid membership type.")

    membership_price = MEMBERSHIP_PRICING[membership_type]  # Now it won't raise KeyError

    # Check if customer has enough balance
    if customer.wallet_money_amount < membership_price:
        raise HTTPException(status_code=400, detail="Not enough wallet balance.")

    # Deduct money from wallet
    customer.wallet_money_amount -= membership_price

    # Set the membership type & expiration date (30 days from now)
    customer.subscription_model = membership_type.lower()  # Store in lowercase
    customer.subscription_end_time = datetime.utcnow() + timedelta(days=30)

    db.commit()
    db.refresh(customer)

    return customer
