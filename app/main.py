from fastapi import FastAPI
from app.database import Base,engine
from app import models


app = FastAPI()

print("Dropping and recreating tables...")
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
print("Tables recreated!")
@app.get("/")
def read_root():
    return {"message": "FastAPI is running with PostgreSQL"}


try:
    with engine.connect() as connection:
        print("Database connection successful!")
except Exception as e:
    print(f"Database connection failed: {e}")