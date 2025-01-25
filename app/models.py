from sqlalchemy import Column, Integer, String, Enum , Float,ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship
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

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String)
    units = Column(Integer, nullable=False)
