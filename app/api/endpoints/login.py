from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.schemas import User
from app.data_models.user import UserLogin, UserSignup
from app.api.deps import get_db, create_access_token

router = APIRouter()

@router.post("/signup/")
def signup(request: UserSignup, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == request.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = User.get_password_hash(request.password)
    new_user = User(email=request.email, hashed_password=hashed_password, username=request.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login(request: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Email address not found')
    if not db_user.verify_password(request.password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token(data={"sub": request.email})
    return {"access_token": token, "token_type": "bearer"}



# TODO: Logout endpoint