"""
Insight model - demonstrates SQLModel relationships and AI-generated content
"""
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class InsightBase(SQLModel):
    """Base insight model with common fields"""
    insight_text: str = Field(description="AI-generated insight text")
    confidence_score: float = Field(ge=0.0, le=1.0, description="AI confidence score (0-1)")
    insight_type: str = Field(index=True, description="Type of insight (trend, anomaly, prediction)")
    metric_id: int = Field(foreign_key="metrics.id", description="Related metric ID")


class Insight(InsightBase, table=True):
    """
    Insight model - demonstrates SQLModel relationships
    Links AI-generated insights to metrics
    """
    __tablename__ = "insights"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)
    
    # Relationship to Metric (many-to-one)
    metric: Optional["Metric"] = Relationship(back_populates="insights")


class InsightCreate(InsightBase):
    """Pydantic model for creating insights"""
    pass


class InsightRead(InsightBase):
    """Pydantic model for reading insights"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class InsightUpdate(SQLModel):
    """Pydantic model for updating insights"""
    insight_text: Optional[str] = None
    confidence_score: Optional[float] = Field(default=None, ge=0.0, le=1.0)
    insight_type: Optional[str] = None
