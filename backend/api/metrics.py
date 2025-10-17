"""
Metrics API endpoints - demonstrates FastAPI async patterns and SQLModel integration
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ..database import get_session
from ..models.metric import Metric, MetricCreate, MetricRead, MetricUpdate
from ..services.bigquery_service import bigquery_service

router = APIRouter(prefix="/api/metrics", tags=["metrics"])


@router.get("/", response_model=List[MetricRead])
async def get_metrics(session: Session = Depends(get_session)):
    """
    Get all metrics from local database
    Demonstrates async endpoint with dependency injection
    """
    # Use SQLModel select statement - demonstrates ORM usage
    statement = select(Metric).order_by(Metric.created_at.desc())
    metrics = session.exec(statement).all()
    return metrics


@router.get("/{metric_id}", response_model=MetricRead)
async def get_metric(metric_id: int, session: Session = Depends(get_session)):
    """
    Get specific metric by ID
    Demonstrates path parameters and error handling
    """
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    return metric


@router.post("/", response_model=MetricRead)
async def create_metric(metric: MetricCreate, session: Session = Depends(get_session)):
    """
    Create new metric
    Demonstrates Pydantic model validation and SQLModel integration
    """
    # Convert Pydantic model to SQLModel instance
    db_metric = Metric.model_validate(metric)
    session.add(db_metric)
    session.commit()
    session.refresh(db_metric)
    return db_metric


@router.put("/{metric_id}", response_model=MetricRead)
async def update_metric(
    metric_id: int, 
    metric_update: MetricUpdate, 
    session: Session = Depends(get_session)
):
    """
    Update existing metric
    Demonstrates partial updates with Pydantic
    """
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    # Update only provided fields
    metric_data = metric_update.model_dump(exclude_unset=True)
    for field, value in metric_data.items():
        setattr(metric, field, value)
    
    session.add(metric)
    session.commit()
    session.refresh(metric)
    return metric


@router.post("/refresh")
async def refresh_metrics_from_bigquery(session: Session = Depends(get_session)):
    """
    Refresh metrics from BigQuery
    Demonstrates async I/O operations and external service integration
    """
    try:
        # Fetch fresh data from BigQuery
        # This demonstrates study guide principle: async def for I/O operations
        bigquery_metrics = await bigquery_service.get_business_metrics()
        
        # Store in local database
        created_count = 0
        for metric_data in bigquery_metrics:
            # Check if metric already exists
            statement = select(Metric).where(
                Metric.name == metric_data["name"],
                Metric.category == metric_data["category"]
            )
            existing_metric = session.exec(statement).first()
            
            if not existing_metric:
                # Create new metric
                db_metric = Metric.model_validate(metric_data)
                session.add(db_metric)
                created_count += 1
        
        session.commit()
        
        return {
            "message": f"Successfully refreshed metrics from BigQuery",
            "created_count": created_count,
            "total_fetched": len(bigquery_metrics)
        }
        
    except Exception as e:
        # Handle errors gracefully
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to refresh metrics from BigQuery: {str(e)}"
        )


@router.delete("/{metric_id}")
async def delete_metric(metric_id: int, session: Session = Depends(get_session)):
    """
    Delete metric by ID
    Demonstrates CRUD operations completion
    """
    metric = session.get(Metric, metric_id)
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    
    session.delete(metric)
    session.commit()
    return {"message": "Metric deleted successfully"}
