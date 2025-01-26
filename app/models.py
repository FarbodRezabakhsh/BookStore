from sqlalchemy import Column, Integer, String, Enum , Float,ForeignKey,Table
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

    author_profile = relationship("Author", back_populates="user", uselist=False)

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
    Column("author_id", Integer, ForeignKey("authors.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("books.id"), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"), nullable=False)
    description = Column(String)
    units = Column(Integer, nullable=False)

    authors = relationship("Author", secondary="author_book", back_populates="books")

class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    city_id = Column(Integer, ForeignKey('cities.id'), nullable=False)
    goodreads_link = Column(String, nullable=True)
    bank_account_number = Column(String, nullable=True)

    user = relationship("User", back_populates="author_profile")
    city = relationship("City")
    books = relationship("Book", secondary="author_book", back_populates="authors") # many to many relationship
