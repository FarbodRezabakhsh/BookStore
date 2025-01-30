from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from app.models import Book, Reservation, Customer, ReservationQueue
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
    - If the book is unavailable, queues the user.
    """

    book = db.query(Book).filter(Book.id == reservation_data.book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Enforce membership permissions
    check_membership_permissions(customer, db)

    # Fetch membership limits
    membership = customer.subscription_model.lower()
    membership_rules = MEMBERSHIP_LIMITS.get(membership)

    # Ensure the user does not exceed max reservations
    active_reservations = db.query(Reservation).filter(Reservation.customer_id == customer.id).count()
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

    # If the book has available units → Reserve immediately
    if book.units > 0:
        book.units -= 1  # Reduce available book units
        new_reservation = Reservation(
            customer_id=customer.id,  # FIXED: Correct Foreign Key Reference
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

    # If the book is unavailable → Add user to the queue
    new_queue_entry = ReservationQueue(
        customer_id=customer.id,  # FIXED: Correct Foreign Key Reference
        book_id=reservation_data.book_id,
        created_at=datetime.utcnow()
    )
    db.add(new_queue_entry)
    db.commit()
    return {"message": "Book is currently unavailable. You have been added to the waiting list."}

def process_reservation_queue(db: Session, book_id: int):
    """
    Assigns a reserved book to the first user in the queue.
    - Premium users get priority.
    - If two users have the same level, the oldest request gets priority.
    """

    next_in_queue = (
        db.query(ReservationQueue)
        .join(Customer, ReservationQueue.customer_id == Customer.id)
        .filter(ReservationQueue.book_id == book_id)
        .order_by(
            Customer.subscription_model.desc(),  # Premium users first
            ReservationQueue.created_at.asc()  # Older requests get priority
        )
        .first()
    )

    if next_in_queue:
        customer = db.query(Customer).filter(Customer.id == next_in_queue.customer_id).first()
        book = db.query(Book).filter(Book.id == book_id).first()

        price = MEMBERSHIP_LIMITS[customer.subscription_model]["price_per_day"] * 7
        if customer.wallet_money_amount < price:
            db.delete(next_in_queue)  # Remove from queue if the user cannot afford
            db.commit()
            return process_reservation_queue(db, book_id)  # Try the next person in line

        # Assign reservation
        book.units -= 1
        new_reservation = Reservation(
            customer_id=customer.id,  # FIXED: Correct Foreign Key Reference
            book_id=book_id,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=7),
            price=price
        )
        db.add(new_reservation)
        customer.wallet_money_amount -= price
        db.delete(next_in_queue)  # Remove from queue
        db.commit()
        db.refresh(new_reservation)

def return_book(db: Session, reservation_id: int):
    """
    Handles book return and assigns it to the next user in the queue if available.
    """
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found.")

    book = db.query(Book).filter(Book.id == reservation.book_id).first()
    book.units += 1  # Increase available book count
    db.delete(reservation)
    db.commit()

    # Check if someone is waiting in the queue
    process_reservation_queue(db, book.id)

def exit_reservation_queue(db: Session, customer: Customer, book_id: int):
    """
    Allows a user to exit the reservation queue for a specific book.
    """
    queue_entry = db.query(ReservationQueue).filter(
        ReservationQueue.customer_id == customer.id,
        ReservationQueue.book_id == book_id
    ).first()

    if not queue_entry:
        raise HTTPException(status_code=404, detail="You are not in the queue for this book.")
    db.delete(queue_entry)
    db.commit()
    return {"message": "You have successfully exited the reservation queue."}

