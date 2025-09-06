"""
Pydantic schemas for request/response models
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr


# College schemas
class CollegeCreate(BaseModel):
    name: str
    location: str


class CollegeResponse(CollegeCreate):
    id: int
    created_at: datetime


# Student schemas
class StudentCreate(BaseModel):
    name: str
    email: EmailStr
    student_id: str
    college_id: Optional[int] = None


class StudentResponse(StudentCreate):
    id: int
    created_at: datetime


# Event schemas
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str
    date: datetime
    location: str
    max_participants: Optional[int] = None
    college_id: Optional[int] = None


class EventResponse(EventCreate):
    id: int
    created_at: datetime


class EventListResponse(EventResponse):
    registration_count: Optional[int] = 0
    attendance_count: Optional[int] = 0
    avg_rating: Optional[float] = None


# Registration schemas
class RegistrationCreate(BaseModel):
    student_id: int


class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    student_id: int
    registered_at: datetime


# Attendance schemas
class AttendanceCreate(BaseModel):
    student_id: int


class AttendanceResponse(BaseModel):
    id: int
    event_id: int
    student_id: int
    attended_at: datetime


# Feedback schemas
class FeedbackCreate(BaseModel):
    student_id: int
    rating: int  # 1-5
    comment: Optional[str] = None


class FeedbackResponse(BaseModel):
    id: int
    event_id: int
    student_id: int
    rating: int
    comment: Optional[str] = None
    submitted_at: datetime


# Report schemas
class EventPopularityReport(BaseModel):
    event_id: int
    title: str
    event_type: str
    registration_count: int
    attendance_count: int
    avg_rating: Optional[float] = None


class StudentParticipationReport(BaseModel):
    student_id: int
    name: str
    email: str
    events_attended: int
    total_registrations: int


class TopActiveStudentsReport(BaseModel):
    student_id: int
    name: str
    email: str
    events_attended: int
    avg_rating_given: Optional[float] = None
