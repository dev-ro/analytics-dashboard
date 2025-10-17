"""
Insights API endpoints - demonstrates AI integration and LangGraph patterns
Architectural decisions based on study guide principles:

1. AI agent integration with FastAPI (study guide: "LangGraph with FastAPI")
2. Async patterns for AI operations (study guide: "async def for I/O")
3. Pydantic validation for AI responses (study guide: "Data Validation")
4. SQLModel relationships for insights storage
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.insight import Insight, InsightCreate, InsightRead
from ..models.metric import Metric

router = APIRouter(prefix="/api/insights", tags=["insights"])


@router.get("/", response_model=List[InsightRead])
async def get_insights(session: Session = Depends(get_session)):
    """
    Get all AI-generated insights
    Demonstrates study guide principle: async endpoints with dependency injection
    """
    # Use SQLModel select with relationships
    # Demonstrates study guide principle: SQLModel relationships
    statement = select(Insight).order_by(Insight.created_at.desc())
    insights = session.exec(statement).all()
    return insights


@router.get("/metric/{metric_id}", response_model=List[InsightRead])
async def get_insights_for_metric(metric_id: int, session: Session = Depends(get_session)):
    """
    Get insights for a specific metric
    Demonstrates study guide principle: relationship-based queries
    """
    # Verify metric exists
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    # Get insights for this metric
    # Demonstrates study guide principle: SQLModel relationships
    statement = select(Insight).where(Insight.metric_id == metric_id)
    insights = session.exec(statement).all()
    return insights


@router.post("/generate/{metric_id}")
async def generate_insights_for_metric(
    metric_id: int, 
    session: Session = Depends(get_session)
):
    """
    Generate AI insights for a specific metric
    Demonstrates study guide principle: AI agent integration
    
    Note: This endpoint will be enhanced in Phase 3 with actual LangGraph agent
    For now, it demonstrates the API structure and async patterns
    """
    # Verify metric exists
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    # TODO: In Phase 3, this will integrate with LangGraph agent
    # For now, create a placeholder insight
    # Demonstrates study guide principle: Pydantic model validation
    placeholder_insight = InsightCreate(
        insight_text=f"AI analysis for {metric.name}: This metric shows {metric.value} with category {metric.category}. Further analysis will be available when LangGraph agent is implemented.",
        confidence_score=0.7,
        insight_type="preliminary",
        metric_id=metric_id
    )
    
    # Store insight in database
    # Demonstrates study guide principle: SQLModel integration
    db_insight = Insight.model_validate(placeholder_insight)
    session.add(db_insight)
    session.commit()
    session.refresh(db_insight)
    
    return {
        "message": "Insight generated successfully",
        "insight_id": db_insight.id,
        "note": "This is a placeholder. Real AI insights will be available in Phase 3 with LangGraph integration."
    }


@router.delete("/{insight_id}")
async def delete_insight(insight_id: int, session: Session = Depends(get_session)):
    """
    Delete insight by ID
    Demonstrates study guide principle: CRUD operations with error handling
    """
    insight = session.get(Insight, insight_id)
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
    
    session.delete(insight)
    session.commit()
    return {"message": "Insight deleted successfully"}
