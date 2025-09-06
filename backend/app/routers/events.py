"""
Event management endpoints
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.models import Event
from app.schemas import EventCreate, EventResponse, EventListResponse
from app import crud

router = APIRouter()


@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_session)
):
    """Create a new event"""
    return crud.create_event(db=db, event=event)


@router.get("/", response_model=List[EventListResponse])
def get_events(
    college_id: Optional[int] = None,
    event_type: Optional[str] = None,
    db: Session = Depends(get_session)
):
    """Get events with optional filtering by college and event type"""
    events = crud.get_events(db=db, college_id=college_id, event_type=event_type)
    
    # Enhance with statistics
    result = []
    for event in events:
        registrations = crud.get_registrations_by_event(db, event.id)
        attendance = crud.get_attendance_by_event(db, event.id)
        feedback = crud.get_feedback_by_event(db, event.id)
        
        # Calculate average rating
        avg_rating = None
        if feedback:
            avg_rating = sum(f.rating for f in feedback) / len(feedback)
        
        result.append(EventListResponse(
            **event.dict(),
            registration_count=len(registrations),
            attendance_count=len(attendance),
            avg_rating=avg_rating
        ))
    
    return result


@router.get("/{event_id}", response_model=EventResponse)
def get_event(
    event_id: int,
    db: Session = Depends(get_session)
):
    """Get a specific event by ID"""
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event
