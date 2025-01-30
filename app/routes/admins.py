from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.core.auth import get_current_user, revoked_tokens
from app.core.auth import check_user_role

router = APIRouter()

@router.delete("/revoke-token/{user_id}")
def revoke_user_token(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admins can revoke a user's access token except for other admins.
    """
    check_user_role(current_user, allowed_roles=["admin"])  # Ensure only admins can revoke tokens

    # Fetch the user to be revoked
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure admins cannot revoke other admins' tokens
    if user.user_role.lower() == "admin":
        raise HTTPException(status_code=403, detail="Cannot revoke another admin’s token.")

    # Convert user_id to an integer before adding to revoked_tokens
    revoked_tokens.add(int(user_id))

    return {"message": f"Token for user {user.username} has been revoked."}
