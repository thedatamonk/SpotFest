from fastapi import APIRouter, Depends, HTTPException, Form
from pydantic import EmailStr
from sqlalchemy.orm import Session
from app.models.schemas import User
from app.api.deps import get_db, create_access_token

router = APIRouter()

@router.post("/signup/")
def signup(email: EmailStr = Form(...), password: str = Form(...), username: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = User.get_password_hash(password)
    new_user = User(email=email, hashed_password=hashed_password, username=username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login(username: EmailStr = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.email == username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail='Email address not found')
    if not db_user.verify_password(password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    token = create_access_token(data={"sub": username})
    return {"access_token": token, "token_type": "bearer"}



# TODO: Logout endpoint