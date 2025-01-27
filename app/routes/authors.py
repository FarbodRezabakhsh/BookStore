from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AuthorCreate, AuthorUpdate, AuthorResponse
from app.crud import create_author, get_all_authors, get_author_by_id, update_author, delete_author

router = APIRouter()

@router.get("/", response_model=list[AuthorResponse])
def get_authors_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_all_authors(db, skip=skip, limit=limit)

@router.get("/{author_id}", response_model=AuthorResponse)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    author = get_author_by_id(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.post("/", response_model=AuthorResponse)
def create_author_endpoint(author: AuthorCreate, db: Session = Depends(get_db)):
    return create_author(db, author)


@router.put("/{author_id}", response_model=AuthorResponse)
def update_author_endpoint(author_id: int, updates: AuthorUpdate, db: Session = Depends(get_db)):
    author = update_author(db, author_id, updates)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@router.delete("/{author_id}", response_model=AuthorResponse)
def delete_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    author = delete_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author
