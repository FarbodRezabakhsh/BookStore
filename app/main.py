from fastapi import FastAPI
from app.database import Base,engine
from app import models
from app.routes import users,books,authors,reservations,customers,auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running with PostgreSQL"}

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(authors.router, prefix="/authors", tags=["Authors"])
app.include_router(reservations.router, prefix="/reservations", tags=["Reservations"])
app.include_router(customers.router, prefix="/customers", tags=["Customers"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")