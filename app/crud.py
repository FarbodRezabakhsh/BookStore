from sqlalchemy.orm import Session
from app.models import User,Book
from app.schemas import UserCreate,BookCreate,BookUpdate

def get_user_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_all_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(User).offset(skip).limit(limit).all() # These parameters enable pagination

def create_user(db: Session, user: UserCreate):
    db_user = User(
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        password=user.password,
        user_role=user.user_role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, updates: dict):
    db_user = get_user_id(db, user_id)
    if not db_user:
        return None
    for key, value in updates.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = get_user_id(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user

def create_book(db: Session, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_all_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Book).offset(skip).limit(limit).all()

def get_book_by_id(db: Session, book_id: int):
    return db.query(Book).filter(Book.id == book_id).first()

def update_book(db: Session, book_id: int, updates: BookUpdate):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = get_book_by_id(db, book_id)
    if not db_book:
        return None
    db.delete(db_book)
    db.commit()
    return db_book