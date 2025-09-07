"""
Tests for the reports endpoints
"""

import pytest
import sys
import os
from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from app.main import app
from app.db import get_session
from app.models import Event, Student, College, Registration, Attendance, Feedback


# Create test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        # Load sample data for testing
        load_sample_data_for_test(session)
        yield session


def load_sample_data_for_test(session: Session):
    """Load minimal sample data for testing"""
    # Create test college
    college = College(name="Test University", location="Test City")
    session.add(college)
    session.commit()
    session.refresh(college)
    
    # Create test students
    students = [
        Student(name="Test Student 1", email="student1@test.edu", student_id="TS001", college_id=college.id),
        Student(name="Test Student 2", email="student2@test.edu", student_id="TS002", college_id=college.id),
        Student(name="Test Student 3", email="student3@test.edu", student_id="TS003", college_id=college.id),
    ]
    for student in students:
        session.add(student)
    session.commit()
    for student in students:
        session.refresh(student)
    
    # Create test events
    events = [
        Event(title="Test Event 1", description="Test event 1", event_type="workshop", 
              date=datetime(2024, 1, 15, 10, 0, 0), location="Test Location 1", college_id=college.id),
        Event(title="Test Event 2", description="Test event 2", event_type="seminar", 
              date=datetime(2024, 1, 20, 14, 0, 0), location="Test Location 2", college_id=college.id),
    ]
    for event in events:
        session.add(event)
    session.commit()
    for event in events:
        session.refresh(event)
    
    # Create registrations
    registrations = [
        Registration(event_id=events[0].id, student_id=students[0].id),
        Registration(event_id=events[0].id, student_id=students[1].id),
        Registration(event_id=events[1].id, student_id=students[0].id),
        Registration(event_id=events[1].id, student_id=students[2].id),
    ]
    for reg in registrations:
        session.add(reg)
    
    # Create attendance
    attendance = [
        Attendance(event_id=events[0].id, student_id=students[0].id),
        Attendance(event_id=events[1].id, student_id=students[0].id),
        Attendance(event_id=events[1].id, student_id=students[2].id),
    ]
    for att in attendance:
        session.add(att)
    
    # Create feedback
    feedback = [
        Feedback(event_id=events[0].id, student_id=students[0].id, rating=5, comment="Great event!"),
        Feedback(event_id=events[1].id, student_id=students[0].id, rating=4, comment="Good seminar"),
        Feedback(event_id=events[1].id, student_id=students[2].id, rating=3, comment="Average"),
    ]
    for fb in feedback:
        session.add(fb)
    
    session.commit()


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_event_popularity_report(client: TestClient):
    """Test event popularity report endpoint"""
    response = client.get("/reports/event-popularity")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    
    # Check that events are sorted by registration count
    assert data[0]["registration_count"] >= data[1]["registration_count"]
    
    # Verify event data structure
    for event in data:
        assert "event_id" in event
        assert "title" in event
        assert "event_type" in event
        assert "registration_count" in event
        assert "attendance_count" in event
        assert isinstance(event["registration_count"], int)
        assert isinstance(event["attendance_count"], int)


def test_student_participation_report(client: TestClient):
    """Test student participation report endpoint"""
    response = client.get("/reports/student-participation")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3  # 3 test students
    
    # Check that students are sorted by events attended
    assert data[0]["events_attended"] >= data[1]["events_attended"]
    
    # Verify student data structure
    for student in data:
        assert "student_id" in student
        assert "name" in student
        assert "email" in student
        assert "events_attended" in student
        assert "total_registrations" in student
        assert isinstance(student["events_attended"], int)
        assert isinstance(student["total_registrations"], int)


def test_top_active_students_report(client: TestClient):
    """Test top active students report endpoint"""
    response = client.get("/reports/top-active-students?limit=3")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    
    # Check that students are sorted by events attended
    assert data[0]["events_attended"] >= data[1]["events_attended"]
    assert data[1]["events_attended"] >= data[2]["events_attended"]
    
    # Verify student data structure
    for student in data:
        assert "student_id" in student
        assert "name" in student
        assert "email" in student
        assert "events_attended" in student
        assert "avg_rating_given" in student
        assert isinstance(student["events_attended"], int)


def test_top_active_students_default_limit(client: TestClient):
    """Test top active students with default limit"""
    response = client.get("/reports/top-active-students")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) <= 10  # Default limit is 10
