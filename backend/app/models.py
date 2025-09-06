"""
Database models for the Campus Event Management System
"""

from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class College(SQLModel, table=True):
    """College/University model"""
    __tablename__ = "colleges"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, max_length=200)
    location: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    students: List["Student"] = Relationship(back_populates="college")
    events: List["Event"] = Relationship(back_populates="college")


class Student(SQLModel, table=True):
    """Student model"""
    __tablename__ = "students"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    email: str = Field(index=True, max_length=200, unique=True)
    student_id: str = Field(index=True, max_length=50, unique=True)
    college_id: Optional[int] = Field(default=None, foreign_key="colleges.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    college: Optional[College] = Relationship(back_populates="students")
    registrations: List["Registration"] = Relationship(back_populates="student")
    attendance: List["Attendance"] = Relationship(back_populates="student")
    feedback: List["Feedback"] = Relationship(back_populates="student")


class Event(SQLModel, table=True):
    """Event model"""
    __tablename__ = "events"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    event_type: str = Field(max_length=100)  # workshop, seminar, competition, etc.
    date: datetime
    location: str = Field(max_length=200)
    max_participants: Optional[int] = Field(default=None)
    college_id: Optional[int] = Field(default=None, foreign_key="colleges.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    college: Optional[College] = Relationship(back_populates="events")
    registrations: List["Registration"] = Relationship(back_populates="event")
    attendance: List["Attendance"] = Relationship(back_populates="event")
    feedback: List["Feedback"] = Relationship(back_populates="event")


class Registration(SQLModel, table=True):
    """Event registration model"""
    __tablename__ = "registrations"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id")
    student_id: int = Field(foreign_key="students.id")
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    event: Event = Relationship(back_populates="registrations")
    student: Student = Relationship(back_populates="registrations")


class Attendance(SQLModel, table=True):
    """Event attendance model"""
    __tablename__ = "attendance"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id")
    student_id: int = Field(foreign_key="students.id")
    attended_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    event: Event = Relationship(back_populates="attendance")
    student: Student = Relationship(back_populates="attendance")


class Feedback(SQLModel, table=True):
    """Event feedback model"""
    __tablename__ = "feedback"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    event_id: int = Field(foreign_key="events.id")
    student_id: int = Field(foreign_key="students.id")
    rating: int = Field(ge=1, le=5)  # Rating between 1-5
    comment: Optional[str] = Field(default=None, max_length=500)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    event: Event = Relationship(back_populates="feedback")
    student: Student = Relationship(back_populates="feedback")
