from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import BookCreate, BookUpdate, BookResponse
from app.crud import create_book, get_all_books, get_book_by_id, update_book, delete_book

router = APIRouter()

@router.post("/", response_model=BookResponse)
def create_book_endpoint(book: BookCreate, db: Session = Depends(get_db)):
    return create_book(db, book)

@router.get("/", response_model=list[BookResponse])
def get_books_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_books(db, skip=skip, limit=limit)

@router.get("/{book_id}", response_model=BookResponse)
def get_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    book = get_book_by_id(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
def update_book_endpoint(book_id: int, updates: BookUpdate, db: Session = Depends(get_db)):
    book = update_book(db, book_id, updates)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.delete("/{book_id}", response_model=BookResponse)
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    book = delete_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
