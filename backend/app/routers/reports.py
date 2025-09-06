"""
Reports and analytics endpoints
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db import get_session
from app.schemas import (
    EventPopularityReport, StudentParticipationReport, TopActiveStudentsReport
)
from app import crud

router = APIRouter()


@router.get("/event-popularity", response_model=List[EventPopularityReport])
def get_event_popularity_report(
    db: Session = Depends(get_session)
):
    """Get event popularity report sorted by registrations"""
    return crud.get_event_popularity_report(db=db)


@router.get("/student-participation", response_model=List[StudentParticipationReport])
def get_student_participation_report(
    db: Session = Depends(get_session)
):
    """Get student participation report showing events attended count"""
    return crud.get_student_participation_report(db=db)


@router.get("/top-active-students", response_model=List[TopActiveStudentsReport])
def get_top_active_students(
    limit: int = Query(default=10, ge=1, le=100, description="Number of top students to return"),
    db: Session = Depends(get_session)
):
    """Get top active students by attendance count"""
    return crud.get_top_active_students(db=db, limit=limit)
