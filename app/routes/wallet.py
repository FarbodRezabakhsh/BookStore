from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User, Customer
from app.core.auth import get_current_user,get_current_customer
from app.services.wallet import add_money_to_wallet

router = APIRouter()

@router.post("/add-money")
def add_money_route(
    amount: float,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    API for customers to add money to their wallet.
    """
    # Check if the current user is a customer
    customer = db.query(Customer).filter(Customer.user_id == current_user.id).first()
    if not customer:
        raise HTTPException(status_code=400, detail="Only customers can add money to their wallet")

    updated_customer = add_money_to_wallet(db, customer.id, amount)

    return {
        "message": "Money added successfully",
        "new_balance": updated_customer.wallet_money_amount
    }
