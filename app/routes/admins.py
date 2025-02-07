from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Reservation,Book , ReservationQueue
from app.core.auth import get_current_user, revoked_tokens
from app.core.auth import check_user_role
from datetime import datetime

router = APIRouter()

@router.delete("/revoke-token/{user_id}")
def revoke_user_token(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admins can revoke a user's access token except for other admins.
    """
    check_user_role(current_user, allowed_roles=["admin"])  # Ensure only admins can revoke tokens

    # Fetch the user to be revoked
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ensure admins cannot revoke other admins' tokens
    if user.user_role.lower() == "admin":
        raise HTTPException(status_code=403, detail="Cannot revoke another admin’s token.")

    # Convert user_id to an integer before adding to revoked_tokens
    revoked_tokens.add(int(user_id))

    return {"message": f"Token for user {user.username} has been revoked."}

# Admins can end reservation's anytime they want
@router.put("/reservations/{reservation_id}/end")
def end_reservation_early(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Admins can forcefully end a user's reservation before its scheduled end time.
    """
    check_user_role(current_user, allowed_roles=["admin"])

    # Fetch reservation
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")

    # Update reservation to end immediately
    reservation.end_date = datetime.utcnow()
    db.commit()
    return {"message": f"Reservation {reservation_id} has been ended early."}

# Admin can view book reservations queue

@router.get('/books/{book_id}/reservations')
def get_book_reservations(
        book_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
        Admins can view a book's current holders and scheduled reservers in queue.
        """
    check_user_role(current_user, allowed_roles=["admin"])

    # Get the book
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Get active reservations
    active_reservations = (
        db.query(Reservation)
        .filter(Reservation.book_id == book_id)
        .all()
    )

    # Get users in queue
    queue_users = (
        db.query(ReservationQueue)
        .filter(ReservationQueue.book_id == book_id)
        .all()
    )

    return {
        "active_reservations": [
            {"user_id": res.customer_id, "start_date": res.start_date, "end_date": res.end_date}
            for res in active_reservations
        ],
        "queue_users": [
            {"user_id": queue.customer_id, "queued_at": queue.created_at}
            for queue in queue_users
        ],
    }

@router.delete("/books/{book_id}/remove-user/{user_id}")
def remove_user_from_reservation_or_queue(
    book_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Admins can remove a user from a reservation or waiting queue.
    """
    check_user_role(current_user, allowed_roles=["admin"])

    # Check if user has an active reservation
    reservation = (
        db.query(Reservation)
        .filter(Reservation.book_id == book_id,Reservation.customer_id == user_id)
        .first()
    )
    if reservation:
        db.delete(reservation)
        db.commit()
        return {"message": f"User:{user_id} removed from active reservation for book:{book_id}"}

    # Check if user is in queue
    queue_entry = (
        db.query(ReservationQueue)
        .filter(ReservationQueue.book_id == book_id, ReservationQueue.customer_id == user_id)
        .first()
    )
    if queue_entry:
        db.delete(queue_entry)
        db.commit()
        return {"message": f"User {user_id} removed from reservation queue for book {book_id}"}

    raise HTTPException(status_code=404, detail="User not found in reservations or queue")
