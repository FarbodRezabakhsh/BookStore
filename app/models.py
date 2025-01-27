from sqlalchemy import Column, Integer, String, Enum , Float,ForeignKey,Table,Date
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
    user_role = Column(String, default=UserRole.CUSTOMER.value,nullable=False)

    author_profile = relationship("Author", back_populates="user", uselist=False)
    customer_profile = relationship("Customer", back_populates="user", uselist=False)

class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("authors.id",ondelete='CASCADE'), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id",ondelete='CASCADE'), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id",ondelete="CASCADE"), nullable=False)
    description = Column(String)
    units = Column(Integer, nullable=False)

    authors = relationship("Author", secondary="author_book", back_populates="books")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id',ondelete="SET NULL"), nullable=False)
    goodreads_link = Column(String, nullable=True)
    bank_account_number = Column(String, nullable=True)

    user = relationship("User", back_populates="author_profile")
    city = relationship("City")
    books = relationship("Book", secondary="author_book", back_populates="authors") # many to many relationship

class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'), nullable=False)
    Subscription_model = Column(String, nullable=False)

class Reservation(Base):
    __tablename__ = "reservations"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    price = Column(Float, nullable=False)

    customer = relationship("User")
    book = relationship("Book")

class SubscriptionModel(enum.Enum):
    FREE = "free"
    PLUS = "plus"
    PREMIUM = "premium"

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True)
    subscription_model = Column(String, nullable=False, default=SubscriptionModel.FREE.value)
    subscription_end_time = Column(Date, nullable=True)
    wallet_money_amount = Column(Float, nullable=False, default=0.0)

    user = relationship("User", back_populates="customer_profile")
