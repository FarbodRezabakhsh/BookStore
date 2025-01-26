from fastapi import FastAPI
from app.database import Base,engine
from app import models
from app.routes import users,books


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "FastAPI is running with PostgreSQL"}

app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(books.router, prefix="/books", tags=["Books"])

try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")