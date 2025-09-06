# ⚠️ IMPORTANT: Rewrite this README in your own words before submission. This is an AI draft.

# Webknot Campus Event Management System

A comprehensive event management system for campus events built with FastAPI and React.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Load sample data:**
   ```bash
   python -m app.fixtures.load_sample_data
   ```

4. **Start the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 🧪 Running Tests

```bash
cd backend
pytest app/tests/test_reports.py -v
```

## 📡 API Endpoints

### Events
- `POST /events` - Create event
- `GET /events` - List events (with filters: college_id, event_type)
- `GET /events/{id}` - Get specific event

### Registrations
- `POST /events/{id}/register` - Register for event (returns 409 if already registered)
- `POST /events/{id}/attendance` - Mark attendance
- `POST /events/{id}/feedback` - Submit feedback (rating 1-5)

### Reports
- `GET /reports/event-popularity` - Events sorted by registrations
- `GET /reports/student-participation` - Students by events attended
- `GET /reports/top-active-students?limit=N` - Top active students

## 📋 Example API Calls

### 1. Create Event
```bash
curl -X POST "http://localhost:8000/events" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Python Workshop",
    "description": "Learn Python fundamentals",
    "event_type": "workshop",
    "date": "2024-02-15T10:00:00",
    "location": "Computer Lab A",
    "max_participants": 30
  }'
```

### 2. Register for Event
```bash
curl -X POST "http://localhost:8000/events/1/register" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1
  }'
```

### 3. Mark Attendance
```bash
curl -X POST "http://localhost:8000/events/1/attendance" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1
  }'
```

### 4. Submit Feedback
```bash
curl -X POST "http://localhost:8000/events/1/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "rating": 5,
    "comment": "Excellent workshop!"
  }'
```

### 5. Get Event Popularity Report
```bash
curl "http://localhost:8000/reports/event-popularity"
```

### 6. Get Top Active Students
```bash
curl "http://localhost:8000/reports/top-active-students?limit=3"
```

## 🎯 Demo Script

1. **Start both servers** (backend and frontend)
2. **Load sample data:** `python -m app.fixtures.load_sample_data`
3. **Visit frontend:** `http://localhost:5173`
4. **Browse events** on the home page
5. **Register for an event** using the registration form
6. **View reports** in the admin reports section

## 🏗️ Architecture

### Backend (FastAPI + SQLModel)
- **Models:** Event, Student, Registration, Attendance, Feedback, College
- **Database:** SQLite (dev) / PostgreSQL (prod via DATABASE_URL)
- **API:** RESTful endpoints with automatic OpenAPI documentation
- **Testing:** pytest with in-memory SQLite

### Frontend (React + Vite + Tailwind)
- **Pages:** Events List, Registration, Admin Reports
- **Components:** Event Cards, Forms, Data Tables
- **Styling:** Tailwind CSS with responsive design
- **Navigation:** React Router for SPA routing

## 📊 Features

- ✅ Event creation and management
- ✅ Student registration with duplicate prevention
- ✅ Attendance tracking
- ✅ Feedback system (1-5 star ratings)
- ✅ Event popularity analytics
- ✅ Student participation reports
- ✅ Top active students ranking
- ✅ Responsive web interface
- ✅ API documentation (FastAPI auto-generated)
- ✅ Comprehensive test coverage

## 🔧 Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string (defaults to SQLite)
- Backend runs on port 8000
- Frontend runs on port 5173

### Database Schema
The system uses 6 main tables:
- **Colleges:** University/college information
- **Students:** Student profiles with college association
- **Events:** Event details with college association
- **Registrations:** Student event registrations
- **Attendance:** Event attendance tracking
- **Feedback:** Event ratings and comments

## 🚀 Production Deployment

For production deployment:
1. Set `DATABASE_URL` environment variable to PostgreSQL
2. Run `npm run build` in frontend directory
3. Serve frontend build files with a web server
4. Use a production ASGI server like Gunicorn for backend

---

**Note:** This is a prototype built for demonstration purposes. For production use, additional features like authentication, authorization, data validation, and error handling would be needed.
