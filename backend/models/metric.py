"""
Metric model - demonstrates SQLModel single source of truth principle
This model serves as both the database schema and API contract
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class MetricBase(SQLModel):
    """Base metric model with common fields"""
    name: str = Field(index=True, description="Metric name")
    value: float = Field(description="Metric value")
    category: str = Field(index=True, description="Metric category")
    description: Optional[str] = Field(default=None, description="Metric description")


class Metric(MetricBase, table=True):
    """
    Metric model - demonstrates SQLModel table definition
    This serves as both SQLAlchemy table and Pydantic model
    """
    __tablename__ = "metrics"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.utcnow, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationship to Insights (one-to-many)
    insights: List["Insight"] = Relationship(back_populates="metric")


class MetricCreate(MetricBase):
    """Pydantic model for creating metrics - no database fields"""
    pass


class MetricRead(MetricBase):
    """Pydantic model for reading metrics - includes all fields"""
    id: int
    timestamp: datetime
    created_at: datetime
    updated_at: Optional[datetime] = None


class MetricUpdate(SQLModel):
    """Pydantic model for updating metrics - all fields optional"""
    name: Optional[str] = None
    value: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
