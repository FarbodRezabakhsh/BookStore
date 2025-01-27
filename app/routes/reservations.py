from fastapi import APIRouter, Depends, HTTPException
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
def create_reservation_route(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return create_reservation(db, reservation)

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
