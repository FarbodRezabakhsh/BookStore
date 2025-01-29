import os
from dotenv import load_dotenv
from datetime import datetime,timedelta
from jose import jwt,JWTError
from passlib.context import CryptContext
from typing import Optional
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import random
from app.database import get_db
from app.models import Customer
from sqlalchemy.orm import Session

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Validates the token and retrieves the current user's information.
    """
    try:
        # Decode the token to retrieve its payload
        payload = decode_access_token(token)
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

    # Ensure the payload contains the 'sub' field (typically the username)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
        )

    return payload["sub"]


def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve the currently authenticated customer profile.
    """
    current_user = get_current_user(token)  # Fetch authenticated user

    # Check if the user has a customer profile
    customer = db.query(Customer).filter(Customer.user_id == current_user.id).first()

    if not customer:
        raise HTTPException(status_code=403, detail="Only customers can upgrade membership")

    return customer


def check_user_role(current_user, allowed_roles: list[str]):
    if current_user.user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permissions to perform this action.",
        )

def generate_otp():
    return str(random.randint(100000,999999))

otp_store = {}

def save_otp(username: str, otp: str):
    otp_store[username] = otp

def get_saved_otp(username: str):
    otp = otp_store.get(username)
    return otp

def clear_otp(username: str):
    if username in otp_store:
        del otp_store[username]