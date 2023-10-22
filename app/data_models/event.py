from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date_time: Optional[datetime] = None

class EventOut(EventCreate):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date_time: Optional[datetime] = None
