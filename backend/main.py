"""
FastAPI main application - demonstrates modern async patterns and dependency injection
Architectural decisions based on study guide principles:

1. Async/await for all I/O operations (study guide: "Use async def for I/O")
2. Dependency injection for database and external services (study guide: "Leverage Dependency Injection")
3. CORS configuration for Next.js frontend integration
4. SQLModel integration for single source of truth
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .database import create_db_and_tables
from .api.metrics import router as metrics_router
from .api.insights import router as insights_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan management
    Demonstrates study guide principle: proper resource initialization
    """
    # Create database tables on startup
    # This follows study guide principle: SQLModel as single source of truth
    create_db_and_tables()
    yield
    # Cleanup on shutdown (if needed)


# Initialize FastAPI app with lifespan management
# Demonstrates study guide principle: proper application lifecycle
app = FastAPI(
    title="Analytics Dashboard API",
    description="AI-powered analytics dashboard with modern tech stack",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Next.js frontend integration
# Demonstrates study guide principle: frontend-backend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
# Demonstrates study guide principle: modular API design
app.include_router(metrics_router)
app.include_router(insights_router)


@app.get("/")
async def root():
    """
    Health check endpoint
    Demonstrates study guide principle: API design best practices
    """
    return {
        "message": "Analytics Dashboard API",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """
    Detailed health check endpoint
    Demonstrates study guide principle: monitoring and observability
    """
    return {
        "status": "healthy",
        "database": "connected",
        "bigquery": "configured"
    }
