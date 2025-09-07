Campus Event Management System (Webknot Assignment)

This project is my prototype for the Webknot assignment. The goal was to design and implement a system that makes it easier to manage campus events — from event creation and registration to attendance and feedback collection. I wanted to build something simple but functional that reflects how such a platform could work in real life.

*Problem Statement

On most campuses, handling events is still a bit messy. Students often get event information late, registrations are done manually, and tracking attendance or collecting feedback isn’t smooth.
The problem asked me to come up with a solution that organizes these processes into one system, where:

Admins/organizers can create events,

Students can view and register,

Attendance and feedback can be tracked,

Reports can be generated to analyze participation.

*My Approach

I decided to split the project into backend and frontend for clarity:

Backend (FastAPI + SQLModel): Handles data storage, APIs for events, registrations, attendance, and reports.

Frontend (React + Tailwind): Provides a clean, responsive interface where users can interact with the system.

I used SQLite for quick development and kept PostgreSQL as an option for scaling. For the frontend, I wanted a simple yet modern look, so I went with React + Vite + Tailwind.

The main design decision was to make it modular: events, students, registrations, and feedback are all separate but connected tables. This keeps the system flexible for future features like authentication or notifications.

*Prototype Implementation
Backend Setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload


Runs at: http://localhost:8000

Frontend Setup
cd frontend
npm install
npm run dev


Runs at: http://localhost:5173

Sample Data

For quick testing:

python -m app.fixtures.load_sample_data

*Tech Stack

Backend: FastAPI, SQLModel, SQLite (with PostgreSQL option)

Frontend: React, Vite, Tailwind CSS, React Router

Testing: pytest (with in-memory SQLite for quick tests)

Other tools: Uvicorn (backend server), npm for frontend package management

*Key Features in This Prototype

Event creation and listing

Student registration (with duplicate prevention)

Attendance marking

Feedback with ratings (1–5)

Reports on event popularity & top active students

Simple responsive interface

*Testing

I added a few tests with pytest to check reports:

cd backend
pytest app/tests/test_reports.py -v

*Design Overview

Database: 6 main tables (Colleges, Students, Events, Registrations, Attendance, Feedback).

Frontend Pages: Event listing, registration form, and admin reports.

Architecture: REST API backend + React frontend with clean separation.

Styling: Tailwind CSS for quick, responsive design.

*Demo Flow

Start backend & frontend servers.

Load sample data.

Open the frontend at http://localhost:5173.

Browse events → register for one → view participation reports.

*Known Issues / Limitations

Since this is still a prototype, there are some gaps I couldn’t fully implement yet:

No proper login or authentication system (anyone can register right now).

Minimal error handling — the system may not respond gracefully to invalid inputs.

Reports are basic and text-based; no visual charts yet.

Notifications (emails/SMS) for event updates are not implemented.

Frontend design is functional but could be more polished.

*Reflection & Next Steps

This prototype covers the core requirements, but if I had more time, I’d add:

Authentication for admins and students.

Email/SMS notifications for events.

More advanced analytics and charts.

Better error handling and validation.

Still, I feel this version demonstrates the main idea clearly and shows how campus events can be digitized and managed effectively.

This is my completed prototype for the Webknot assignment, built step by step with focus on both functionality and design clarity.