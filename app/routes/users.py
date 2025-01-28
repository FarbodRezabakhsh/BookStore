from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import get_user_id, get_all_users, create_user, update_user, delete_user
from app.models import User
from app.core.auth import get_current_user,check_user_role

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    check_user_role(current_user, allowed_roles=['ADMIN'])
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db),current_user: User = Depends(get_current_user),):
    # Admin can fetch any user data and user are able to access their own data
    user = get_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.user_role != "ADMIN" and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return user

@router.get("/", response_model=list[UserResponse])
def get_all_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Only ADMIN can view all users
    check_user_role(current_user, allowed_roles=["ADMIN"])
    return get_all_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, updates: dict, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    # Allow both ADMIN and the user themselves to update their data
    user = get_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if current_user.user_role != "ADMIN" and current_user.id != user.id:
        raise HTTPException(status_code=403, detail="Permission denied")
    return update_user(db, user_id, updates)

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Check if the user exists
    user = get_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Allow ADMIN to delete any user, or allow users to delete their own account
    if current_user.user_role != "ADMIN" and current_user.id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this user.",
        )
    # Proceed with deletion
    delete_user(db, user_id)
    return user