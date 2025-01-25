from sqlalchemy import Column, Integer, String, Enum
from app.database import Base
import enum

class UserRole(enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    AUTHOR = "author"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER)
