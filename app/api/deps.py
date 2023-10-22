from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from app.models.schemas import engine
from fastapi.security import OAuth2PasswordBearer
from decouple import config
import jwt
from datetime import datetime, timedelta
from app.models.schemas import User

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(config("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api_v1/login")


SessionLocal = sessionmaker(bind=engine)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        email = payload.get("sub")

        db_user = db.query(User).filter(User.email == email).first() 
        return db_user
           
    except:
        raise HTTPException(status_code=400, detail="Invalid token")
