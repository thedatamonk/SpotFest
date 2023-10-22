from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    username: str = None

class UserCreate(UserBase):
    password: str
    is_active: bool = True


class UserOut(UserBase):
    pass