"""
Registration, attendance, and feedback endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db import get_session
from app.schemas import (
    RegistrationCreate, RegistrationResponse,
    AttendanceCreate, AttendanceResponse,
    FeedbackCreate, FeedbackResponse
)
from app import crud

router = APIRouter()


@router.post("/{event_id}/register", response_model=RegistrationResponse)
def register_for_event(
    event_id: int,
    registration: RegistrationCreate,
    db: Session = Depends(get_session)
):
    """Register a student for an event"""
    # Check if event exists
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if student exists
    student = crud.get_student(db=db, student_id=registration.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    try:
        return crud.create_registration(db=db, event_id=event_id, registration=registration)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/{event_id}/attendance", response_model=AttendanceResponse)
def mark_attendance(
    event_id: int,
    attendance: AttendanceCreate,
    db: Session = Depends(get_session)
):
    """Mark attendance for an event"""
    # Check if event exists
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if student exists
    student = crud.get_student(db=db, student_id=attendance.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return crud.create_attendance(db=db, event_id=event_id, attendance=attendance)


@router.post("/{event_id}/feedback", response_model=FeedbackResponse)
def submit_feedback(
    event_id: int,
    feedback: FeedbackCreate,
    db: Session = Depends(get_session)
):
    """Submit feedback for an event"""
    # Check if event exists
    event = crud.get_event(db=db, event_id=event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if student exists
    student = crud.get_student(db=db, student_id=feedback.student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate rating
    if not (1 <= feedback.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
    
    return crud.create_feedback(db=db, event_id=event_id, feedback=feedback)
