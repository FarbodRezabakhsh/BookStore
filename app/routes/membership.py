from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Customer
from app.core.auth import get_current_user,get_current_customer
from app.services.membership import upgrade_membership  # from services folder

router = APIRouter()

@router.post("/upgrade-membership")
def upgrade_membership_route(membership_type: str, db: Session = Depends(get_db), current_customer=Depends(get_current_customer),):
    """
    API endpoint for customers to upgrade their membership to plus or premium.
    """
    # Get the customer's profile
    upgraded_customer = upgrade_membership(db, current_customer, membership_type)
    return {
        "message": f"Membership upgraded to {membership_type}",
        "new_balance": upgraded_customer.wallet_money_amount,
        "expires_at": upgraded_customer.subscription_end_time,
    }