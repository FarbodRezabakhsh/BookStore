from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.models import Reservation, Customer
from fastapi import HTTPException

def check_membership_permissions(customer: Customer, db: Session):
    """
    Validates if a customer is allowed to reserve books based on their membership level.
    Checks for discount eligibility for Plus users.
    """
    # Free users cannot reserve books
    if customer.subscription_model == "free":
        raise HTTPException(status_code=403, detail="Free users cannot reserve books.")

    # Get current date
    today = datetime.utcnow()

    # Define reservation limits
    if customer.subscription_model == "plus":
        max_days = 7  # Plus users can reserve for at most 7 days
        max_books = 5  # Plus users can have 5 active reservations
    elif customer.subscription_model == "premium":
        max_days = 14  # Premium users can reserve for 14 days
        max_books = 10  # Premium users can have 10 active reservations
    else:
        raise HTTPException(status_code=400, detail="Invalid membership type.")

    # Apply discounts for Plus users
    discount = 0

    # Check if the user has read 3+ different books in the last 30 days
    thirty_days_ago = today - timedelta(days=30)
    books_read = (
        db.query(Reservation)
        .filter(Reservation.customer_id == customer.id)
        .filter(Reservation.start_date >= thirty_days_ago)
        .distinct(Reservation.book_id)
        .count()
    )

    if books_read >= 3:
        discount = 30  # Apply 30% discount

    # Check if the user has spent 300,000+ Toman in the last 60 days
    sixty_days_ago = today - timedelta(days=60)
    total_spent = (
        db.query(Reservation)
        .filter(Reservation.customer_id == customer.id)
        .filter(Reservation.start_date >= sixty_days_ago)
        .with_entities(Reservation.price)
    )

    total_spent_amount = sum([r.price for r in total_spent])

    if total_spent_amount >= 300000:
        discount = 100  # Apply 100% discount

    return {
        "max_days": max_days,
        "max_books": max_books,
        "discount": discount,  # Discount for Plus users
    }
