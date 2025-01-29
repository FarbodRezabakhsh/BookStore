from fastapi import HTTPException
from app.models import Customer


def check_membership_level(customer: Customer):
    """
    Ensures that only Plus and Premium users can make reservations.
    """
    if customer.subscription_model == "free":
        raise HTTPException(
            status_code=403, detail="Free users cannot reserve books."
        )
