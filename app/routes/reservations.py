from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud import (
    get_reservations,
    get_reservation,
    create_reservation,
    update_reservation,
    delete_reservation,
)
from app.schemas import ReservationCreate, ReservationUpdate, ReservationResponse
from app.core.auth import get_current_customer
from app.services.reservations import reserve_book,exit_reservation_queue

router = APIRouter()

@router.get("/", response_model=list[ReservationResponse])
def get_reservations_route(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reservations(db, skip=skip, limit=limit)

@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation_route(reservation_id: int, db: Session = Depends(get_db)):
    reservation = get_reservation(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

@router.post("/", response_model=ReservationResponse)
def create_reservation_route(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    """
    Handles reservation creation.
    - Enforces membership-based limits.
    - Deducts money from wallet.
    - If book is unavailable, queues the user.
    """
    reservation_or_queue = reserve_book(db, current_customer, reservation_data)

    if isinstance(reservation_or_queue, dict):  # If the function returns a queue message
        return JSONResponse(content=reservation_or_queue, status_code=200)

    return reservation_or_queue  # Otherwise, return the reservation as normal

@router.put("/{reservation_id}", response_model=ReservationResponse)
def update_reservation_route(reservation_id: int, reservation: ReservationUpdate, db: Session = Depends(get_db)):
    updated_reservation = update_reservation(db, reservation_id, reservation)
    if not updated_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return updated_reservation

@router.delete("/{reservation_id}", response_model=ReservationResponse)
def delete_reservation_route(reservation_id: int, db: Session = Depends(get_db)):
    deleted_reservation = delete_reservation(db, reservation_id)
    if not deleted_reservation:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return deleted_reservation

@router.delete("/queue/exit/{book_id}")
def exit_queue_route(
    book_id: int,
    db: Session = Depends(get_db),
    current_customer=Depends(get_current_customer),
):
    """
    Allows a user to remove themselves from the reservation queue.
    """
    return exit_reservation_queue(db, current_customer, book_id)
