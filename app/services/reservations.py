from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models import Book, Reservation, Customer
from app.schemas import ReservationCreate
from app.core.membership_validation import check_membership_permissions

# Membership Reservation Limits
MEMBERSHIP_LIMITS = {
    "free": {"max_days": 0, "max_books": 0, "price_per_day": None},
    "plus": {"max_days": 7, "max_books": 5, "price_per_day": 1000},
    "premium": {"max_days": 14, "max_books": 10, "price_per_day": 1000},
}

def reserve_book(db: Session, customer: Customer, reservation_data: ReservationCreate):
    """
    Handles book reservations:
    - Enforces membership-based limits.
    - Deducts money from wallet.
    - Checks book availability.
    - If book is unavailable, queues the user.
    """

    # Fetch the book from DB
    book = db.query(Book).filter(Book.id == reservation_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Enforce membership permissions
    check_membership_permissions(customer,db)

    # Fetch membership limits
    membership = customer.subscription_model
    membership_rules = MEMBERSHIP_LIMITS.get(membership)

    # Ensure the user does not exceed max reservations
    active_reservations = db.query(Reservation).filter(Reservation.customer_id == customer.user_id).count()
    if active_reservations >= membership_rules["max_books"]:
        raise HTTPException(status_code=403, detail="You have reached your reservation limit.")

    # Calculate reservation duration
    max_days = membership_rules["max_days"]
    reservation_duration = (reservation_data.end_date - reservation_data.start_date).days

    if reservation_duration > max_days:
        raise HTTPException(status_code=400, detail=f"You can only reserve books for a maximum of {max_days} days.")

    # Calculate cost
    total_price = reservation_duration * membership_rules["price_per_day"]

    # Check wallet balance
    if customer.wallet_money_amount < total_price:
        raise HTTPException(status_code=400, detail="Insufficient funds. Please add money to your wallet.")

    # If book has available units → Reserve immediately
    if book.units > 0:
        book.units -= 1  # Reduce available book units
        new_reservation = Reservation(
            customer_id=customer.user_id,
            book_id=reservation_data.book_id,
            start_date=reservation_data.start_date,
            end_date=reservation_data.end_date,
            price=total_price
        )
        db.add(new_reservation)

        # Deduct money from wallet
        customer.wallet_money_amount -= total_price

        db.commit()
        db.refresh(new_reservation)
        return new_reservation

    # If book is unavailable, add to queue (Not yet implemented)
    raise HTTPException(status_code=400, detail="No available units. Queue system not implemented yet.")
