from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
import jwt
from app.models.schemas import engine, User
from app.data_models.user import UserCreate
from datetime import datetime, timedelta
from decouple import config
from fastapi.security import OAuth2PasswordBearer


router = APIRouter()

SessionLocal = sessionmaker(bind=engine)

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("sub")

        db_user = db.query(User).filter(User.email == email).first() 
        return db_user
           
    except:
        raise HTTPException(status_code=400, detail="Invalid token")


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = User.get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password, username=user.username)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login/")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
