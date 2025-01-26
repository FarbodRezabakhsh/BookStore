from sqlalchemy.orm import Session
from app.models import User,Book,Author
from app.schemas import UserCreate,BookCreate,BookUpdate,AuthorCreate,AuthorUpdate

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


def create_author(db: Session, author: AuthorCreate):
    db_author = Author(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author

def get_all_authors(db: Session,skip:int=0,limit: int=10):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author_by_id(db:Session,author_id:int):
    return db.query(Author).filter(Author.id == author_id).first()

def update_author(db: Session, author_id:int, updates:AuthorUpdate):
    db_author = get_author_by_id(db, author_id)
    if not db_author:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_author, key, value)
    db.commit()
    db.refresh(db_author)
    return db_author

def delete_author(db: Session, author_id: int):
    db_author = get_author_by_id(db, author_id)
    if not db_author:
        return None
    db.delete(db_author)
    db.commit()
    return f'{db_author} deleted successfully'