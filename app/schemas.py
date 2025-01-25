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

class BookBase(BaseModel):
    title: str
    isbn: str
    price: float
    genre_id: int
    description: Optional[str] = None
    units: int

class BookCreate(BookBase):
    author_id: int

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    price: Optional[float] = None
    genre_id: Optional[int] = None
    description: Optional[str] = None
    units: Optional[int] = None

class BookResponse(BookBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True