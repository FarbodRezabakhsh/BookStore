from fastapi import HTTPException
from app.models import Customer

MEMBERSHIP_LIMITS = {
    "free": {"max_days": 0, "max_books": 0, "price_per_day": None},
    "plus": {"max_days": 7, "max_books": 5, "price_per_day": 1000},
    "premium": {"max_days": 14, "max_books": 10, "price_per_day": 1000},
}

def check_membership_permissions(customer):
    print(f"DEBUG: Customer {customer.user_id} has membership: {customer.subscription_model}")  # Debugging line
    allowed_levels = ["plus", "premium"]
    if customer.subscription_model.lower() not in allowed_levels:
        raise HTTPException(status_code=403, detail="Invalid membership type.")

def check_membership_level(customer: Customer):
    """
    Ensures that only Plus and Premium users can make reservations.
    """
    if customer.subscription_model == "free":
        raise HTTPException(
            status_code=403, detail="Free users cannot reserve books."
        )
