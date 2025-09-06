"""
Student management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from app.db import get_session
from app.models import Student
from app.schemas import StudentCreate, StudentResponse
from app import crud

router = APIRouter()


@router.post("/", response_model=StudentResponse)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_session)
):
    """Create a new student"""
    # Check if student with email already exists
    existing_student = crud.get_student_by_email(db=db, email=student.email)
    if existing_student:
        raise HTTPException(status_code=409, detail="Student with this email already exists")
    
    return crud.create_student(db=db, student=student)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_session)
):
    """Get a specific student by ID"""
    student = crud.get_student(db=db, student_id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
