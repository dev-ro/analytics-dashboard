"""
Database configuration and session management
Demonstrates SQLModel database setup and dependency injection
"""
import os
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator

# Database URL from environment or default to SQLite
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./analytics.db")

# Create engine - demonstrates SQLModel engine creation
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries for development
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)


def create_db_and_tables():
    """
    Create database tables from SQLModel definitions
    Demonstrates single source of truth - models define both schema and API
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency injection for database sessions
    Demonstrates FastAPI dependency injection pattern from study guide
    """
    with Session(engine) as session:
        yield session
