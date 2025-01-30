from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Customer

def add_money_to_wallet(db: Session, customer_id: int, amount: float):
    """
    Add money to the customer's wallet.
    """
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Invalid amount. Must be greater than zero.")

    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    customer.wallet_money_amount += amount
    db.commit()
    db.refresh(customer)

    return customer
