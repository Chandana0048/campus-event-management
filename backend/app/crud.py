"""
CRUD operations for the Campus Event Management System
"""

from typing import List, Optional
from sqlmodel import Session, select, func, and_
from sqlalchemy import desc

from app.models import (
    College, Student, Event, Registration, Attendance, Feedback
)
from app.schemas import (
    CollegeCreate, StudentCreate, EventCreate, RegistrationCreate,
    AttendanceCreate, FeedbackCreate
)


# College CRUD
def create_college(db: Session, college: CollegeCreate) -> College:
    """Create a new college"""
    db_college = College(**college.dict())
    db.add(db_college)
    db.commit()
    db.refresh(db_college)
    return db_college


def get_college(db: Session, college_id: int) -> Optional[College]:
    """Get college by ID"""
    return db.get(College, college_id)


# Student CRUD
def create_student(db: Session, student: StudentCreate) -> Student:
    """Create a new student"""
    db_student = Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: int) -> Optional[Student]:
    """Get student by ID"""
    return db.get(Student, student_id)


def get_student_by_email(db: Session, email: str) -> Optional[Student]:
    """Get student by email"""
    return db.exec(select(Student).where(Student.email == email)).first()


# Event CRUD
def create_event(db: Session, event: EventCreate) -> Event:
    """Create a new event"""
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event(db: Session, event_id: int) -> Optional[Event]:
    """Get event by ID"""
    return db.get(Event, event_id)


def get_events(db: Session, college_id: Optional[int] = None, event_type: Optional[str] = None) -> List[Event]:
    """Get events with optional filtering"""
    query = select(Event)
    
    if college_id:
        query = query.where(Event.college_id == college_id)
    if event_type:
        query = query.where(Event.event_type == event_type)
    
    return db.exec(query.order_by(desc(Event.date))).all()


# Registration CRUD
def create_registration(db: Session, event_id: int, registration: RegistrationCreate) -> Registration:
    """Create a new event registration"""
    # Check if student is already registered
    existing = db.exec(
        select(Registration).where(
            and_(Registration.event_id == event_id, Registration.student_id == registration.student_id)
        )
    ).first()
    
    if existing:
        raise ValueError("Student is already registered for this event")
    
    db_registration = Registration(event_id=event_id, **registration.dict())
    db.add(db_registration)
    db.commit()
    db.refresh(db_registration)
    return db_registration


def get_registrations_by_event(db: Session, event_id: int) -> List[Registration]:
    """Get all registrations for an event"""
    return db.exec(select(Registration).where(Registration.event_id == event_id)).all()


# Attendance CRUD
def create_attendance(db: Session, event_id: int, attendance: AttendanceCreate) -> Attendance:
    """Mark attendance for an event"""
    db_attendance = Attendance(event_id=event_id, **attendance.dict())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


def get_attendance_by_event(db: Session, event_id: int) -> List[Attendance]:
    """Get all attendance records for an event"""
    return db.exec(select(Attendance).where(Attendance.event_id == event_id)).all()


# Feedback CRUD
def create_feedback(db: Session, event_id: int, feedback: FeedbackCreate) -> Feedback:
    """Create feedback for an event"""
    db_feedback = Feedback(event_id=event_id, **feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback


def get_feedback_by_event(db: Session, event_id: int) -> List[Feedback]:
    """Get all feedback for an event"""
    return db.exec(select(Feedback).where(Feedback.event_id == event_id)).all()


# Report functions
def get_event_popularity_report(db: Session) -> List[dict]:
    """Get event popularity report sorted by registrations"""
    query = db.exec(
        select(
            Event.id,
            Event.title,
            Event.event_type,
            func.count(Registration.id).label("registration_count"),
            func.count(Attendance.id).label("attendance_count"),
            func.avg(Feedback.rating).label("avg_rating")
        )
        .outerjoin(Registration, Event.id == Registration.event_id)
        .outerjoin(Attendance, Event.id == Attendance.event_id)
        .outerjoin(Feedback, Event.id == Feedback.event_id)
        .group_by(Event.id, Event.title, Event.event_type)
        .order_by(desc("registration_count"))
    ).all()
    
    return [
        {
            "event_id": row.id,
            "title": row.title,
            "event_type": row.event_type,
            "registration_count": row.registration_count or 0,
            "attendance_count": row.attendance_count or 0,
            "avg_rating": float(row.avg_rating) if row.avg_rating else None
        }
        for row in query
    ]


def get_student_participation_report(db: Session) -> List[dict]:
    """Get student participation report"""
    query = db.exec(
        select(
            Student.id,
            Student.name,
            Student.email,
            func.count(Attendance.id).label("events_attended"),
            func.count(Registration.id).label("total_registrations")
        )
        .outerjoin(Registration, Student.id == Registration.student_id)
        .outerjoin(Attendance, Student.id == Attendance.student_id)
        .group_by(Student.id, Student.name, Student.email)
        .order_by(desc("events_attended"))
    ).all()
    
    return [
        {
            "student_id": row.id,
            "name": row.name,
            "email": row.email,
            "events_attended": row.events_attended or 0,
            "total_registrations": row.total_registrations or 0
        }
        for row in query
    ]


def get_top_active_students(db: Session, limit: int = 10) -> List[dict]:
    """Get top active students by attendance and feedback"""
    query = db.exec(
        select(
            Student.id,
            Student.name,
            Student.email,
            func.count(Attendance.id).label("events_attended"),
            func.avg(Feedback.rating).label("avg_rating_given")
        )
        .outerjoin(Attendance, Student.id == Attendance.student_id)
        .outerjoin(Feedback, Student.id == Feedback.student_id)
        .group_by(Student.id, Student.name, Student.email)
        .order_by(desc("events_attended"))
        .limit(limit)
    ).all()
    
    return [
        {
            "student_id": row.id,
            "name": row.name,
            "email": row.email,
            "events_attended": row.events_attended or 0,
            "avg_rating_given": float(row.avg_rating_given) if row.avg_rating_given else None
        }
        for row in query
    ]
