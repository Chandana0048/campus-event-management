"""
Database configuration and session management
"""

import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import event
from sqlalchemy.engine import Engine

# Database URL - defaults to SQLite for development, can be overridden with DATABASE_URL env var
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./campus_events.db")

# Create engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL)

# Enable foreign key constraints for SQLite
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if "sqlite" in str(dbapi_connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(engine)


async def init_db():
    """Initialize database on startup"""
    create_db_and_tables()


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
