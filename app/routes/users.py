from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse
from app.crud import get_user_id, get_all_users, create_user, update_user, delete_user

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
def get_all_users_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_users(db, skip=skip, limit=limit)

@router.put("/{user_id}", response_model=UserResponse)
def update_user_endpoint(user_id: int, updates: dict, db: Session = Depends(get_db)):
    user = update_user(db, user_id, updates)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}", response_model=UserResponse)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
