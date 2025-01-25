from pydantic import BaseModel,EmailStr
from typing import Optional

class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: Optional[str] = None
    password: Optional[str] = None

class UserCreate(UserBase):
    password: str
    user_role: Optional[str] = "CUSTOMER"

class UserResponse(UserBase):
    id: int
    user_role: str

    class Config:
        orm_mode = True