"""
LangGraph Analytics Agent - demonstrates stateful AI agents for business insights
Architectural decisions based on study guide principles:

1. Stateful AI Agents: LangGraph enables cyclical, stateful agent behavior
2. Unified Data Modeling: Agent state uses same data structures as API
3. Modular Node Design: Single-responsibility nodes for different AI operations
4. Conditional Edges: Intelligent decision-making for agent workflow
5. LLM Integration: Real OpenAI/Anthropic API for production-quality insights

Study Guide Principles Demonstrated:
- "Define a Clear and Minimal State": TypedDict with essential information
- "Build Modular, Single-Responsibility Nodes": Separate nodes for analysis, generation, formatting
- "Use Conditional Edges for Control Flow": LLM-powered decision making
"""
import operator
from typing import Annotated, List, Dict, Any, TypedDict
from typing_extensions import TypedDict as TypedDictExt
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import os


class AgentState(TypedDictExt):
    """
    Agent state - demonstrates study guide principle: "Define a Clear and Minimal State"
    
    The state contains only essential information needed for the agent to function:
    - messages: Conversation history for context
    - metrics_data: Business metrics to analyze
    - insights: Generated insights
    - current_analysis: Intermediate analysis results
    """
    messages: Annotated[List[BaseMessage], operator.add]
    metrics_data: List[Dict[str, Any]]
    insights: Annotated[List[str], operator.add]
    current_analysis: Dict[str, Any]
    confidence_score: float


class AnalyticsAgent:
    """
    LangGraph Analytics Agent for generating business insights
    
    Demonstrates study guide principles:
    - Stateful agent with cyclical behavior
    - Modular node design with single responsibilities
    - Conditional edges for intelligent decision-making
    - Integration with real LLM APIs
    """
    
    def __init__(self):
        """Initialize agent with LLM configuration"""
        # Initialize LLM with environment configuration
        # Demonstrates study guide principle: proper configuration management
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Build the agent graph
        # Demonstrates study guide principle: "Build Modular, Single-Responsibility Nodes"
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """
        Build LangGraph workflow with nodes and edges
        Demonstrates study guide principle: modular graph construction
        """
        # Create state graph with AgentState
        workflow = StateGraph(AgentState)
        
        # Add nodes - each with single responsibility
        # Demonstrates study guide principle: "Build Modular, Single-Responsibility Nodes"
        workflow.add_node("analyze_metrics", self._analyze_metrics_node)
        workflow.add_node("generate_insights", self._generate_insights_node)
        workflow.add_node("format_response", self._format_response_node)
        workflow.add_node("quality_check", self._quality_check_node)
        
        # Set entry point
        workflow.set_entry_point("analyze_metrics")
        
        # Add edges - demonstrates study guide principle: "Use Conditional Edges for Control Flow"
        workflow.add_edge("analyze_metrics", "generate_insights")
        workflow.add_edge("generate_insights", "quality_check")
        
        # Conditional edge for quality control
        workflow.add_conditional_edges(
            "quality_check",
            self._should_continue,
            {
                "continue": "format_response",
                "regenerate": "generate_insights",
                "end": END
            }
        )
        
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def _analyze_metrics_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Analyze metrics data - demonstrates study guide principle: single-responsibility node
        
        This node performs initial analysis of business metrics to understand patterns,
        trends, and anomalies that will inform insight generation.
        """
        metrics_data = state["metrics_data"]
        
        # Perform basic statistical analysis
        # Demonstrates study guide principle: data processing within agent
        analysis = {
            "total_metrics": len(metrics_data),
            "categories": list(set(metric.get("category", "unknown") for metric in metrics_data)),
            "value_ranges": {
                "min": min(metric.get("value", 0) for metric in metrics_data),
                "max": max(metric.get("value", 0) for metric in metrics_data),
                "avg": sum(metric.get("value", 0) for metric in metrics_data) / len(metrics_data)
            },
            "patterns": self._identify_patterns(metrics_data)
        }
        
        # Add analysis message to conversation
        analysis_message = HumanMessage(
            content=f"Analyzing {len(metrics_data)} business metrics. "
                   f"Found {len(analysis['categories'])} categories: {', '.join(analysis['categories'])}. "
                   f"Value range: {analysis['value_ranges']['min']:.2f} to {analysis['value_ranges']['max']:.2f}"
        )
        
        return {
            "current_analysis": analysis,
            "messages": [analysis_message]
        }
    
    def _generate_insights_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Generate AI insights - demonstrates study guide principle: LLM integration
        
        This node uses the LLM to generate intelligent business insights based on
        the analyzed metrics data and conversation context.
        """
        analysis = state["current_analysis"]
        metrics_data = state["metrics_data"]
        
        # Create prompt for LLM
        # Demonstrates study guide principle: structured prompting
        prompt = f"""
        As a business analyst AI, analyze the following metrics data and generate actionable insights:
        
        Metrics Summary:
        - Total metrics: {analysis['total_metrics']}
        - Categories: {', '.join(analysis['categories'])}
        - Value range: {analysis['value_ranges']['min']:.2f} to {analysis['value_ranges']['max']:.2f}
        - Average value: {analysis['value_ranges']['avg']:.2f}
        
        Patterns identified: {analysis['patterns']}
        
        Sample metrics:
        {self._format_metrics_for_llm(metrics_data[:5])}
        
        Generate 3-5 actionable business insights. Focus on:
        1. Trends and patterns
        2. Anomalies or outliers
        3. Business recommendations
        4. Risk indicators
        5. Growth opportunities
        
        Format each insight as a clear, actionable statement.
        """
        
        # Get LLM response
        # Demonstrates study guide principle: real LLM integration
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        # Extract insights from response
        insights = self._extract_insights_from_response(response.content)
        
        # Add to conversation
        ai_message = AIMessage(content=response.content)
        
        return {
            "insights": insights,
            "messages": [ai_message],
            "confidence_score": self._calculate_confidence(insights, analysis)
        }
    
    def _quality_check_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Quality check insights - demonstrates study guide principle: validation
        
        This node validates the quality and relevance of generated insights
        to ensure they meet business standards.
        """
        insights = state["insights"]
        confidence = state["confidence_score"]
        
        # Quality assessment
        quality_metrics = {
            "insight_count": len(insights),
            "avg_length": sum(len(insight) for insight in insights) / len(insights) if insights else 0,
            "confidence_score": confidence,
            "has_actionable_items": any("recommend" in insight.lower() or "should" in insight.lower() for insight in insights)
        }
        
        # Determine if insights meet quality threshold
        quality_acceptable = (
            quality_metrics["insight_count"] >= 3 and
            quality_metrics["confidence_score"] >= 0.6 and
            quality_metrics["has_actionable_items"]
        )
        
        return {
            "current_analysis": {**state["current_analysis"], "quality_metrics": quality_metrics},
            "quality_acceptable": quality_acceptable
        }
    
    def _format_response_node(self, state: AgentState) -> Dict[str, Any]:
        """
        Format final response - demonstrates study guide principle: output formatting
        
        This node formats the final insights for API consumption.
        """
        insights = state["insights"]
        analysis = state["current_analysis"]
        
        # Format insights for API response
        formatted_insights = []
        for i, insight in enumerate(insights, 1):
            formatted_insights.append({
                "id": i,
                "text": insight,
                "type": self._classify_insight_type(insight),
                "confidence": state["confidence_score"]
            })
        
        # Create final response
        final_message = AIMessage(
            content=f"Generated {len(insights)} business insights with {state['confidence_score']:.2f} confidence"
        )
        
        return {
            "messages": [final_message],
            "formatted_insights": formatted_insights
        }
    
    def _should_continue(self, state: AgentState) -> str:
        """
        Conditional edge logic - demonstrates study guide principle: intelligent decision-making
        
        Determines whether to continue processing, regenerate insights, or end the workflow.
        """
        quality_acceptable = state["current_analysis"].get("quality_acceptable", False)
        confidence = state["confidence_score"]
        
        if quality_acceptable and confidence >= 0.7:
            return "continue"
        elif confidence < 0.5:
            return "regenerate"
        else:
            return "end"
    
    def _identify_patterns(self, metrics_data: List[Dict[str, Any]]) -> List[str]:
        """Identify patterns in metrics data"""
        patterns = []
        
        # Check for trends
        values = [metric.get("value", 0) for metric in metrics_data]
        if len(values) > 1:
            if all(values[i] <= values[i+1] for i in range(len(values)-1)):
                patterns.append("increasing trend")
            elif all(values[i] >= values[i+1] for i in range(len(values)-1)):
                patterns.append("decreasing trend")
        
        # Check for categories
        categories = [metric.get("category", "unknown") for metric in metrics_data]
        unique_categories = set(categories)
        if len(unique_categories) == 1:
            patterns.append("single category focus")
        elif len(unique_categories) > 3:
            patterns.append("diverse categories")
        
        return patterns
    
    def _format_metrics_for_llm(self, metrics: List[Dict[str, Any]]) -> str:
        """Format metrics data for LLM consumption"""
        formatted = []
        for metric in metrics:
            formatted.append(f"- {metric.get('name', 'Unknown')}: {metric.get('value', 0)} ({metric.get('category', 'unknown')})")
        return "\n".join(formatted)
    
    def _extract_insights_from_response(self, response: str) -> List[str]:
        """Extract individual insights from LLM response"""
        # Simple extraction - in production, use more sophisticated parsing
        lines = response.split('\n')
        insights = []
        for line in lines:
            line = line.strip()
            if line and (line.startswith('-') or line.startswith('•') or line.startswith('1.') or line.startswith('2.') or line.startswith('3.')):
                # Clean up the insight
                insight = line.lstrip('-•123456789. ').strip()
                if len(insight) > 20:  # Only include substantial insights
                    insights.append(insight)
        return insights[:5]  # Limit to 5 insights
    
    def _calculate_confidence(self, insights: List[str], analysis: Dict[str, Any]) -> float:
        """Calculate confidence score for generated insights"""
        if not insights:
            return 0.0
        
        # Simple confidence calculation based on insight quality
        avg_length = sum(len(insight) for insight in insights) / len(insights)
        has_numbers = any(any(char.isdigit() for char in insight) for insight in insights)
        has_action_words = any(any(word in insight.lower() for word in ['recommend', 'should', 'consider', 'suggest']) for insight in insights)
        
        confidence = 0.5  # Base confidence
        if avg_length > 50:
            confidence += 0.2
        if has_numbers:
            confidence += 0.1
        if has_action_words:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _classify_insight_type(self, insight: str) -> str:
        """Classify insight type based on content"""
        insight_lower = insight.lower()
        if any(word in insight_lower for word in ['trend', 'increasing', 'decreasing', 'growth']):
            return "trend"
        elif any(word in insight_lower for word in ['risk', 'warning', 'concern', 'issue']):
            return "risk"
        elif any(word in insight_lower for word in ['opportunity', 'potential', 'growth', 'improve']):
            return "opportunity"
        elif any(word in insight_lower for word in ['recommend', 'should', 'consider', 'suggest']):
            return "recommendation"
        else:
            return "observation"
    
    async def generate_insights(self, metrics_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Main method to generate insights from metrics data
        Demonstrates study guide principle: agent invocation with real data
        """
        # Initialize agent state
        initial_state = {
            "messages": [],
            "metrics_data": metrics_data,
            "insights": [],
            "current_analysis": {},
            "confidence_score": 0.0
        }
        
        # Run the agent workflow
        # Demonstrates study guide principle: stateful agent execution
        final_state = await self.workflow.ainvoke(initial_state)
        
        return {
            "insights": final_state.get("formatted_insights", []),
            "confidence_score": final_state.get("confidence_score", 0.0),
            "analysis": final_state.get("current_analysis", {}),
            "messages": [msg.content for msg in final_state.get("messages", [])]
        }


# Global agent instance for dependency injection
analytics_agent = AnalyticsAgent()
