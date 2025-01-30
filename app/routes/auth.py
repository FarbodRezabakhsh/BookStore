from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import SignUp, Login, Token,OTPResponse,VerifyOTPRequest
from app.models import User,Customer
from app.core.auth import verify_password, get_password_hash, create_access_token,save_otp,generate_otp,clear_otp,get_saved_otp

router = APIRouter()


@router.post("/signup", response_model=Token)
def signup(user: SignUp, db: Session = Depends(get_db)):
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists",
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the new user
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone,
        user_role=user.user_role,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if new_user.user_role.lower() == "customer":
        new_customer = Customer(
            user_id=new_user.id,
            subscription_model="free",  # Default new customers to "free"
            subscription_end_time=None,
            wallet_money_amount=0.0,  # New customers start with 0 money
        )
        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

    # Generate an access token for the user
    access_token = create_access_token(data={"sub": new_user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=OTPResponse)
def login(user: Login, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        print("User not found.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    if not verify_password(user.password, db_user.password):
        print("Password mismatch.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username or password")

    otp = generate_otp()
    print(f"Generated OTP: {otp}")
    save_otp(user.username, otp)
    print(f"OTP saved for user: {user.username}")
    return {"message": "OTP sent. Please verify to complete login."}

    print(f"Error during login: {e}")
    raise HTTPException(status_code=500, detail="Internal Server Error")


# OTP implementation
@router.post("/request-otp")
def request_otp(username: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    otp = generate_otp()
    save_otp(username, otp)

    # Simulate sending OTP
    print(f"OTP for {username}: {otp}")
    return {"message": "OTP sent to your registered phone/email"}


@router.post("/verify-otp", response_model=Token)
def verify_otp(request: VerifyOTPRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Retrieve and verify OTP
    saved_otp = get_saved_otp(request.username)
    if not saved_otp or saved_otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    clear_otp(request.username)
    access_token = create_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

