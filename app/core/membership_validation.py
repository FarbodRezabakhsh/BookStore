from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Reservation, Customer
from fastapi import HTTPException
from app.core.membership_permissions import MEMBERSHIP_LIMITS

def check_membership_permissions(customer: Customer, db: Session):
    """
    Validates if a customer is allowed to reserve books based on their membership level.
    Checks for discount eligibility for Plus users.
    """
    membership = customer.subscription_model.lower()  # Convert to lowercase
    # Free users cannot reserve books
    if membership == "free":
        raise HTTPException(status_code=403, detail="Free users cannot reserve books.")

    # Fetch membership rules
    membership_rules = MEMBERSHIP_LIMITS.get(membership, None)

    if membership_rules is None:
        raise HTTPException(status_code=400, detail=f"Invalid membership type: {membership}")

