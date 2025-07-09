"""ReWOO Agent following SimpleAgent pattern with ReWOO-specific routing."""

import logging
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field

from haive.agents.simple.agent import SimpleAgent
from haive.agents.planning.rewoo.state import ReWOOState
from haive.agents.planning.rewoo.models import ReWOOPlan, EvidenceStatus
from haive.agents.planning.rewoo.node_config import (
    create_rewoo_planning_node,
    create_rewoo_evidence_node,
    create_rewoo_reasoning_node
)

logger = logging.getLogger(__name__)


# Routing functions for ReWOO
def has_plan(state: ReWOOState) -> bool:
    """Check if state has a ReWOO plan."""
    return hasattr(state, 'plan') and state.plan is not None


def has_evidence_ready(state: ReWOOState) -> bool:
    """Check if evidence is ready to collect."""
    return len(state.ready_evidence) > 0


def is_evidence_complete(state: ReWOOState) -> bool:
    """Check if all evidence collection is complete."""
    return state.is_evidence_complete


def has_tool_calls(state: ReWOOState) -> bool:
    """Check if the last AI message has tool calls."""
    if not hasattr(state, "messages") or not state.messages:
        return False

    last_msg = state.messages[-1]
    if not isinstance(last_msg, AIMessage):
        return False

    tool_calls = getattr(last_msg, "tool_calls", None)
    return bool(tool_calls)


class ReWOOAgent(SimpleAgent):
    """ReWOO Agent that extends SimpleAgent with evidence-based planning.
    
    This agent follows the ReWOO pattern:
    1. Planning: Creates evidence-based plan
    2. Collection: Collects evidence systematically
    3. Reasoning: Uses evidence for final answer
    
    Uses SimpleAgent's infrastructure with ReWOO-specific routing.
    """
    
    def build_graph(self) -> BaseGraph:
        """Build ReWOO graph with conditional routing."""
        # For now, let's just use the base SimpleAgent graph to test the agent works
        # TODO: Add ReWOO-specific nodes and routing
        graph = super().build_graph()
        
        # Later we'll modify this to add ReWOO-specific nodes:
        # - Planning node for creating evidence-based plans
        # - Evidence collection node for gathering evidence
        # - Reasoning node for final answer synthesis
        
        return graph
    
    def process_tool_results_node(self, state: ReWOOState) -> Command:
        """Process tool results back into evidence."""
        logger.info("Processing tool results into evidence")
        
        # Get the messages
        messages = state.messages or []
        if len(messages) < 2:
            return Command(update={"messages": ["No tool results to process"]})
        
        # Get current evidence being collected
        current_evidence_id = getattr(state, 'current_evidence_id', None)
        if not current_evidence_id:
            return Command(update={"messages": ["No current evidence to update"]})
        
        # Find the latest ToolMessage
        from langchain_core.messages import ToolMessage
        tool_message = None
        for msg in reversed(messages):
            if isinstance(msg, ToolMessage):
                tool_message = msg
                break
        
        if not tool_message:
            # Tool execution failed
            state.update_evidence(
                current_evidence_id,
                status=EvidenceStatus.FAILED,
                error="No tool result found"
            )
            return Command(update={
                "messages": ["Tool execution failed - no result"]
            })
        
        try:
            # Update evidence with tool result
            state.update_evidence(
                current_evidence_id,
                status=EvidenceStatus.COLLECTED,
                content=tool_message.content
            )
            
            # Also track in tool_results
            state.add_tool_result(
                tool_message.name or "unknown", 
                tool_message.content
            )
            
            return Command(update={
                "messages": [f"Evidence {current_evidence_id} collected successfully"]
            })
            
        except Exception as e:
            state.update_evidence(
                current_evidence_id,
                status=EvidenceStatus.FAILED,
                error=str(e)
            )
            return Command(update={
                "messages": [f"Failed to update evidence: {str(e)}"]
            })


# Example usage
async def example_rewoo_agent():
    """Example of using ReWOO agent."""
    from haive.core.tools import tool
    
    # Define tools
    @tool
    def search_tool(query: str) -> str:
        """Search for information."""
        return f"Search results for: {query}"
    
    @tool
    def analyze_tool(data: str) -> str:
        """Analyze data."""
        return f"Analysis of: {data}"
    
    # Create agent
    agent = ReWOOAgent(
        name="rewoo_agent",
        engine=AugLLMConfig(
            model="gpt-4",
            temperature=0.7
        ),
        tools=[search_tool, analyze_tool]
    )
    
    # Run agent
    result = await agent.arun("What is the population of Tokyo?")
    
    print(f"Result: {result}")
    
    # Check evidence collected
    if hasattr(agent.state, 'evidence_summary'):
        print(f"Evidence: {agent.state.evidence_summary}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(example_rewoo_agent())