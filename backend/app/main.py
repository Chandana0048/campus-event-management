"""
Webknot Campus Event Management System - Main FastAPI Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.db import init_db
from app.routers import events, registrations, reports, students


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database on startup"""
    await init_db()
    yield


app = FastAPI(
    title="Webknot Campus Event Management System",
    description="A comprehensive event management system for campus events",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(registrations.router, prefix="/events", tags=["registrations"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])
app.include_router(students.router, prefix="/students", tags=["students"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Webknot Campus Event Management System API", "status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
