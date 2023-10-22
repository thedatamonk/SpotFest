from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.data_models.event import EventCreate, EventOut, EventUpdate
from app.data_models.user import UserOut

from app.api.deps import get_current_user, get_db

from app.models.schemas import Event, RSVP

from typing import List


router = APIRouter()

@router.post("/events/", response_model=EventOut)
def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    # Assuming the current_user object has the user's ID as 'id'
    db_event = Event(**event.model_dump(), host_id=current_user.id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events/{event_id}", response_model=EventOut)
def read_event(event_id: int, db: Session = Depends(get_db)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/events/{event_id}", response_model=EventOut)
def update_event(event_id: int, event: EventUpdate, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if current user is the host of the event
    if db_event.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this event")
    
    for key, value in event.model_dump().items():
        if value is not None:
            setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/events/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    db_event = db.query(Event).filter(Event.id == event_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    if db_event.host_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this event")
    db.delete(db_event)
    db.commit()
    return {"status": "Event deleted successfully"}


@router.get("/events/", response_model=List[EventOut])
def list_events(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    events = db.query(Event).offset(skip).limit(limit).all()
    return events

@router.post("/events/{event_id}/rsvp")
def create_rsvp(event_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    existing_rsvp = db.query(RSVP).filter(RSVP.user_id == current_user.id, RSVP.event_id == event_id).first()

    # If an RSVP already exists, raise an exception
    if existing_rsvp:
        raise HTTPException(status_code=400, detail="You have already RSVPed to this event")

    rsvp = RSVP(user_id=current_user.id, event_id=event_id)
    db.add(rsvp)
    db.commit()
    return {"message": "Event RSVPed successfully"}


@router.get("/events/{event_id}/rsvps")
def list_rsvps_for_event(event_id: int, db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).filter(RSVP.event_id == event_id).all()
    return rsvps

@router.delete("/events/{event_id}/rsvp")
def cancel_rsvp(event_id: int, db: Session = Depends(get_db), current_user: UserOut = Depends(get_current_user)):
    rsvp = db.query(RSVP).filter(RSVP.event_id == event_id, RSVP.user_id == current_user.id).first()
    if not rsvp:
        raise HTTPException(status_code=404, detail="RSVP not found")
    db.delete(rsvp)
    db.commit()
    return {"message": "RSVP cancelled successfully."}
