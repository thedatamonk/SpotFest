from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str
    username: str = None
    is_active: bool = True
