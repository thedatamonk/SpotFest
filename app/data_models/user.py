from pydantic import BaseModel, EmailStr

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserSignup(BaseModel):
    email: EmailStr
    password: str
    username: str
    
class UserBase(BaseModel):
    email: EmailStr
    username: str = None

class UserCreate(UserBase):
    password: str
    is_active: bool = True

class UserUpdate(BaseModel):
    password: str = None
    username: str = None
    
class UserOut(UserBase):
    pass