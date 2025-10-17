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
from ..agents.analytics_agent import analytics_agent

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
    Generate AI insights for a specific metric using LangGraph agent
    Demonstrates study guide principle: AI agent integration with real LLM
    
    This endpoint integrates the LangGraph analytics agent to generate
    intelligent business insights from metric data.
    """
    # Verify metric exists
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    try:
        # Get all metrics for context (agent works better with multiple data points)
        # Demonstrates study guide principle: providing context to AI agents
        statement = select(Metric).where(Metric.category == metric.category)
        related_metrics = session.exec(statement).all()
        
        # Convert to format expected by agent
        # Demonstrates study guide principle: data preparation for AI
        metrics_data = [
            {
                "name": m.name,
                "value": m.value,
                "category": m.category,
                "description": m.description
            }
            for m in related_metrics
        ]
        
        # Generate insights using LangGraph agent
        # Demonstrates study guide principle: stateful AI agent execution
        agent_result = await analytics_agent.generate_insights(metrics_data)
        
        # Store insights in database
        # Demonstrates study guide principle: SQLModel integration with AI results
        created_insights = []
        for insight_data in agent_result["insights"]:
            db_insight = Insight(
                insight_text=insight_data["text"],
                confidence_score=insight_data["confidence"],
                insight_type=insight_data["type"],
                metric_id=metric_id
            )
            session.add(db_insight)
            created_insights.append(db_insight)
        
        session.commit()
        
        # Refresh to get IDs
        for insight in created_insights:
            session.refresh(insight)
        
        return {
            "message": "AI insights generated successfully",
            "insights_count": len(created_insights),
            "confidence_score": agent_result["confidence_score"],
            "insight_ids": [insight.id for insight in created_insights],
            "analysis": agent_result["analysis"]
        }
        
    except Exception as e:
        # Handle AI agent errors gracefully
        # Demonstrates study guide principle: error handling in AI integration
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI insights: {str(e)}"
        )


@router.post("/generate/all")
async def generate_insights_for_all_metrics(session: Session = Depends(get_session)):
    """
    Generate AI insights for all metrics using LangGraph agent
    Demonstrates study guide principle: batch AI processing
    
    This endpoint processes all available metrics to generate comprehensive
    business insights using the LangGraph analytics agent.
    """
    try:
        # Get all metrics
        # Demonstrates study guide principle: comprehensive data analysis
        statement = select(Metric).order_by(Metric.created_at.desc())
        all_metrics = session.exec(statement).all()
        
        if not all_metrics:
            raise HTTPException(status_code=404, detail="No metrics found")
        
        # Convert to format expected by agent
        metrics_data = [
            {
                "name": m.name,
                "value": m.value,
                "category": m.category,
                "description": m.description
            }
            for m in all_metrics
        ]
        
        # Generate insights using LangGraph agent
        # Demonstrates study guide principle: comprehensive AI analysis
        agent_result = await analytics_agent.generate_insights(metrics_data)
        
        # Store insights in database (associate with first metric for simplicity)
        # In a real application, you might create a separate "global insights" table
        created_insights = []
        for insight_data in agent_result["insights"]:
            db_insight = Insight(
                insight_text=insight_data["text"],
                confidence_score=insight_data["confidence"],
                insight_type=insight_data["type"],
                metric_id=all_metrics[0].id  # Associate with first metric
            )
            session.add(db_insight)
            created_insights.append(db_insight)
        
        session.commit()
        
        # Refresh to get IDs
        for insight in created_insights:
            session.refresh(insight)
        
        return {
            "message": "Comprehensive AI insights generated successfully",
            "insights_count": len(created_insights),
            "confidence_score": agent_result["confidence_score"],
            "insight_ids": [insight.id for insight in created_insights],
            "analysis": agent_result["analysis"],
            "processed_metrics": len(all_metrics)
        }
        
    except Exception as e:
        # Handle AI agent errors gracefully
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate comprehensive AI insights: {str(e)}"
        )


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
