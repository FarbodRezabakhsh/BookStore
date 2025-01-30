from pydantic import BaseModel,EmailStr
from typing import Optional,List
from datetime import date

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

class GenreResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class CityResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class BookBase(BaseModel):
    title: str
    isbn: str
    price: float
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

class AuthorBase(BaseModel):
    user_id: int
    city_id: int
    goodreads_link: Optional[str] = None
    bank_account_number: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    city_id: Optional[int] = None
    goodreads_link: Optional[str] = None
    bank_account_number: Optional[str] = None

class AuthorResponse(AuthorBase):
    id: int
    books: Optional[List[int]] = []  # Book IDs authored by this author

    class Config:
        orm_mode = True

class ReservationBase(BaseModel):
    book_id: int
    start_date: date
    end_date: date
    price: float

class ReservationCreate(ReservationBase):
    pass

class ReservationUpdate(BaseModel):
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    price: Optional[float] = None

class ReservationResponse(ReservationBase):
    id: int

    class Config:
        orm_mode = True

# Customer schema
class CustomerBase(BaseModel):
    user_id: int
    subscription_model: str = "free"
    subscription_end_time: Optional[date] = None
    wallet_money_amount: float = 0.0

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModel):
    subscription_model: Optional[str] = None
    subscription_end_time: Optional[date] = None
    wallet_money_amount: Optional[float] = None

class CustomerResponse(CustomerBase):
    id: int

    class Config:
        orm_mode = True

# JWT schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class SignUp(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: Optional[str] = None
    user_role: Optional[str] = "CUSTOMER"

class Login(BaseModel):
    username: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "root",
                "password": "rootroot"
            }
        }

    def validate_login(self):
        if not self.username:
            raise ValueError("Username must be provided")

class OTPResponse(BaseModel):
    message: str

class VerifyOTPRequest(BaseModel):
    username: str
    otp: str