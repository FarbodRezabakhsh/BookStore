from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.auth import get_current_user
from app.services.membership import upgrade_membership  # from services folder

router = APIRouter()

@router.post("/upgrade-membership")
def upgrade_membership_route(
    membership_type: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    API endpoint for users to upgrade their membership (Plus/Premium).
    """
    upgraded_user = upgrade_membership(db, current_user, membership_type)
    return {
        "message": f"Membership upgraded to {membership_type}",
        "new_balance": upgraded_user.wallet_money_amount,
        "expires_at": upgraded_user.subscription_end_time,
    }
