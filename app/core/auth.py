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
from app.models import Customer,User
from sqlalchemy.orm import Session

load_dotenv()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# ----------------------------------------
# Password Handling Functions
# ----------------------------------------

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


# ----------------------------------------
# Token Handling Functions
# ----------------------------------------

def create_access_token(user: User, expires_delta: Optional[timedelta] = None):
    """
    Generates an access token with user ID instead of username.
    """
    to_encode = {"sub": str(user.id)}  # Store user ID instead of username
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


# ----------------------------------------
# User Authentication & Authorization
# ----------------------------------------

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    try:
        user_id = int(user_id)  # Convert to integer
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token format")

    # Check if token is revoked
    if user_id in revoked_tokens:
        raise HTTPException(status_code=401, detail="User access revoked. Please log in again.")

    # Retrieve the User object from the database
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def get_current_customer(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Retrieve the currently authenticated customer profile.
    """
    current_user = get_current_user(token, db)  # Fetch authenticated user

    # Check if the user has a customer profile
    customer = db.query(Customer).filter(Customer.user_id == current_user.id).first()

    if not customer:
        raise HTTPException(status_code=403, detail="Only customers can reserve books.")
    return customer


def check_user_role(current_user, allowed_roles: list[str]):
    user_role = current_user.user_role.lower()  # Convert user role to lowercase
    allowed_roles = [role.lower() for role in allowed_roles]  # Convert allowed roles to lowercase

    if user_role not in allowed_roles:  # Compare lowercase role names
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the required permissions to perform this action.",
        )


# ----------------------------------------
# OTP Handling
# ----------------------------------------

def generate_otp():
    return str(random.randint(100000,999999))

# OTP Storage
otp_store = {}

def save_otp(username: str, otp: str):
    otp_store[username] = otp

def get_saved_otp(username: str):
    otp = otp_store.get(username)
    return otp

def clear_otp(username: str):
    if username in otp_store:
        del otp_store[username]


# Token Revocation Storage (Consider storing in DB or Redis for persistence)
revoked_tokens = set()