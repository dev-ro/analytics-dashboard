"""
BigQuery service - demonstrates async FastAPI with BigQuery integration
Follows study guide principles: query optimization, cost control, dependency injection
"""
import os
from typing import List, Dict, Any
from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPICallError
import asyncio
from concurrent.futures import ThreadPoolExecutor


class BigQueryService:
    """
    BigQuery service with optimized queries and cost controls
    Demonstrates study guide principles:
    - Query optimization (SELECT specific columns, WHERE filters, LIMIT)
    - Cost control (avoiding SELECT *, using WHERE clauses)
    - Async patterns for I/O operations
    """
    
    def __init__(self):
        """Initialize BigQuery client with Application Default Credentials"""
        self.client = bigquery.Client()
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        # Thread pool for running sync BigQuery operations in async context
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    async def get_business_metrics(self) -> List[Dict[str, Any]]:
        """
        Fetch business metrics from BigQuery public dataset
        Demonstrates query optimization principles from study guide
        """
        # Using public dataset: bigquery-public-data.usa_names.usa_1910_current
        # This demonstrates cost-effective querying of public data
        
        # Optimized query - demonstrates study guide principles:
        # 1. SELECT specific columns only (not SELECT *)
        # 2. Use WHERE clause to filter data early
        # 3. Use LIMIT to control result size
        # 4. Use aggregation functions for business metrics
        query = """
        SELECT 
            state,
            COUNT(*) as name_count,
            COUNT(DISTINCT name) as unique_names,
            AVG(number) as avg_occurrences
        FROM 
            `bigquery-public-data.usa_names.usa_1910_current`
        WHERE 
            year >= 2020  -- Filter to recent data
            AND state IN ('CA', 'NY', 'TX', 'FL', 'IL')  -- Focus on major states
        GROUP BY 
            state
        ORDER BY 
            name_count DESC
        LIMIT 10
        """
        
        try:
            # Run query in thread pool to avoid blocking async event loop
            # Demonstrates study guide principle: async def for I/O operations
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor, 
                self._execute_query, 
                query
            )
            
            # Transform results into business metrics format
            metrics = []
            for row in results:
                metrics.append({
                    "name": f"Names in {row.state}",
                    "value": row.name_count,
                    "category": "demographics",
                    "description": f"Total name occurrences in {row.state} since 2020"
                })
                
                metrics.append({
                    "name": f"Unique names in {row.state}",
                    "value": row.unique_names,
                    "category": "demographics", 
                    "description": f"Number of unique names in {row.state} since 2020"
                })
                
                metrics.append({
                    "name": f"Avg occurrences in {row.state}",
                    "value": round(row.avg_occurrences, 2),
                    "category": "demographics",
                    "description": f"Average name occurrences in {row.state} since 2020"
                })
            
            return metrics
            
        except GoogleAPICallError as e:
            # Handle BigQuery API errors gracefully
            print(f"BigQuery API error: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error in BigQuery service: {e}")
            return []
    
    def _execute_query(self, query: str) -> List[Any]:
        """
        Execute BigQuery query synchronously
        Called from thread pool to avoid blocking async event loop
        """
        query_job = self.client.query(query)
        return list(query_job.result())
    
    async def get_trend_analysis(self, metric_name: str) -> Dict[str, Any]:
        """
        Get trend analysis for a specific metric
        Demonstrates more complex analytical queries
        """
        # Example trend analysis query
        query = """
        SELECT 
            year,
            COUNT(*) as total_names,
            COUNT(DISTINCT name) as unique_names
        FROM 
            `bigquery-public-data.usa_names.usa_1910_current`
        WHERE 
            year >= 2015
        GROUP BY 
            year
        ORDER BY 
            year DESC
        LIMIT 10
        """
        
        try:
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                self._execute_query,
                query
            )
            
            # Calculate trend (simple linear trend)
            if len(results) >= 2:
                recent = results[0].total_names
                previous = results[1].total_names
                trend = ((recent - previous) / previous) * 100 if previous > 0 else 0
            else:
                trend = 0
            
            return {
                "metric_name": metric_name,
                "trend_percentage": round(trend, 2),
                "data_points": len(results),
                "latest_value": results[0].total_names if results else 0
            }
            
        except Exception as e:
            print(f"Error in trend analysis: {e}")
            return {
                "metric_name": metric_name,
                "trend_percentage": 0,
                "data_points": 0,
                "latest_value": 0
            }


# Global instance for dependency injection
bigquery_service = BigQueryService()
