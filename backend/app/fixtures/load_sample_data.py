"""
Sample data loader for the Campus Event Management System
Run with: python -m app.fixtures.load_sample_data
"""

import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from sqlmodel import Session
from app.db import engine, create_db_and_tables
from app.models import College, Student, Event, Registration, Attendance, Feedback
from app.crud import create_college, create_student, create_event, create_registration, create_attendance, create_feedback
from app.schemas import CollegeCreate, StudentCreate, EventCreate, RegistrationCreate, AttendanceCreate, FeedbackCreate


def load_sample_data():
    """Load sample data into the database"""
    print("Creating database tables...")
    create_db_and_tables()
    
    with Session(engine) as db:
        print("Loading sample data...")
        
        # Create colleges
        print("Creating colleges...")
        colleges_data = [
            {"name": "Tech University", "location": "San Francisco, CA"},
            {"name": "State College", "location": "Austin, TX"},
            {"name": "Engineering Institute", "location": "Boston, MA"},
        ]
        
        colleges = []
        for college_data in colleges_data:
            college = create_college(db, CollegeCreate(**college_data))
            colleges.append(college)
            print(f"  Created college: {college.name}")
        
        # Create students
        print("Creating students...")
        students_data = [
            {"name": "Alice Johnson", "email": "alice@tech.edu", "student_id": "TU001", "college_id": colleges[0].id},
            {"name": "Bob Smith", "email": "bob@state.edu", "student_id": "SC001", "college_id": colleges[1].id},
            {"name": "Carol Davis", "email": "carol@eng.edu", "student_id": "EI001", "college_id": colleges[2].id},
            {"name": "David Wilson", "email": "david@tech.edu", "student_id": "TU002", "college_id": colleges[0].id},
            {"name": "Eva Brown", "email": "eva@state.edu", "student_id": "SC002", "college_id": colleges[1].id},
            {"name": "Frank Miller", "email": "frank@eng.edu", "student_id": "EI002", "college_id": colleges[2].id},
        ]
        
        students = []
        for student_data in students_data:
            student = create_student(db, StudentCreate(**student_data))
            students.append(student)
            print(f"  Created student: {student.name}")
        
        # Create events
        print("Creating events...")
        events_data = [
            {
                "title": "Python Workshop",
                "description": "Learn Python programming fundamentals",
                "event_type": "workshop",
                "date": datetime.now() + timedelta(days=7),
                "location": "Computer Lab A",
                "max_participants": 30,
                "college_id": colleges[0].id
            },
            {
                "title": "Data Science Seminar",
                "description": "Introduction to data science and machine learning",
                "event_type": "seminar",
                "date": datetime.now() + timedelta(days=14),
                "location": "Auditorium",
                "max_participants": 100,
                "college_id": colleges[1].id
            },
            {
                "title": "Hackathon 2024",
                "description": "24-hour coding competition",
                "event_type": "competition",
                "date": datetime.now() + timedelta(days=21),
                "location": "Conference Center",
                "max_participants": 50,
                "college_id": colleges[2].id
            },
            {
                "title": "Web Development Bootcamp",
                "description": "Full-stack web development intensive",
                "event_type": "workshop",
                "date": datetime.now() + timedelta(days=30),
                "location": "Tech Hub",
                "max_participants": 25,
                "college_id": colleges[0].id
            },
        ]
        
        events = []
        for event_data in events_data:
            event = create_event(db, EventCreate(**event_data))
            events.append(event)
            print(f"  Created event: {event.title}")
        
        # Create registrations
        print("Creating registrations...")
        registrations_data = [
            # Python Workshop registrations
            {"student_id": students[0].id},  # Alice
            {"student_id": students[3].id},  # David
            {"student_id": students[1].id},  # Bob
            # Data Science Seminar registrations
            {"student_id": students[1].id},  # Bob
            {"student_id": students[4].id},  # Eva
            {"student_id": students[2].id},  # Carol
            {"student_id": students[0].id},  # Alice
            # Hackathon registrations
            {"student_id": students[2].id},  # Carol
            {"student_id": students[5].id},  # Frank
            {"student_id": students[1].id},  # Bob
            # Web Development Bootcamp registrations
            {"student_id": students[0].id},  # Alice
            {"student_id": students[3].id},  # David
        ]
        
        event_registration_map = [
            (events[0].id, 3),  # Python Workshop: 3 registrations
            (events[1].id, 4),  # Data Science Seminar: 4 registrations
            (events[2].id, 3),  # Hackathon: 3 registrations
            (events[3].id, 2),  # Web Development Bootcamp: 2 registrations
        ]
        
        reg_index = 0
        for event_id, count in event_registration_map:
            for _ in range(count):
                try:
                    registration = create_registration(db, event_id, RegistrationCreate(**registrations_data[reg_index]))
                    print(f"  Registered student {registrations_data[reg_index]['student_id']} for event {event_id}")
                except ValueError as e:
                    print(f"  Registration failed: {e}")
                reg_index += 1
        
        # Create attendance (some students attended past events)
        print("Creating attendance records...")
        attendance_data = [
            # Python Workshop attendance
            {"student_id": students[0].id},  # Alice attended
            {"student_id": students[3].id},  # David attended
            # Data Science Seminar attendance
            {"student_id": students[1].id},  # Bob attended
            {"student_id": students[4].id},  # Eva attended
            {"student_id": students[2].id},  # Carol attended
            # Hackathon attendance
            {"student_id": students[2].id},  # Carol attended
            {"student_id": students[5].id},  # Frank attended
        ]
        
        event_attendance_map = [
            (events[0].id, 2),  # Python Workshop: 2 attended
            (events[1].id, 3),  # Data Science Seminar: 3 attended
            (events[2].id, 2),  # Hackathon: 2 attended
        ]
        
        att_index = 0
        for event_id, count in event_attendance_map:
            for _ in range(count):
                attendance = create_attendance(db, event_id, AttendanceCreate(**attendance_data[att_index]))
                print(f"  Marked attendance for student {attendance_data[att_index]['student_id']} at event {event_id}")
                att_index += 1
        
        # Create feedback
        print("Creating feedback...")
        feedback_data = [
            # Python Workshop feedback
            {"student_id": students[0].id, "rating": 5, "comment": "Excellent workshop! Very informative."},
            {"student_id": students[3].id, "rating": 4, "comment": "Good content, could use more hands-on practice."},
            # Data Science Seminar feedback
            {"student_id": students[1].id, "rating": 5, "comment": "Amazing seminar, learned a lot!"},
            {"student_id": students[4].id, "rating": 3, "comment": "Interesting but too theoretical."},
            {"student_id": students[2].id, "rating": 4, "comment": "Good overview of data science concepts."},
            # Hackathon feedback
            {"student_id": students[2].id, "rating": 5, "comment": "Challenging but fun! Great experience."},
            {"student_id": students[5].id, "rating": 4, "comment": "Well organized, good prizes."},
        ]
        
        event_feedback_map = [
            (events[0].id, 2),  # Python Workshop: 2 feedback
            (events[1].id, 3),  # Data Science Seminar: 3 feedback
            (events[2].id, 2),  # Hackathon: 2 feedback
        ]
        
        fb_index = 0
        for event_id, count in event_feedback_map:
            for _ in range(count):
                feedback = create_feedback(db, event_id, FeedbackCreate(**feedback_data[fb_index]))
                print(f"  Created feedback from student {feedback_data[fb_index]['student_id']} for event {event_id}")
                fb_index += 1
        
        print("\nSample data loaded successfully!")
        print(f"Created: {len(colleges)} colleges, {len(students)} students, {len(events)} events")
        print("Plus registrations, attendance records, and feedback")


if __name__ == "__main__":
    load_sample_data()
