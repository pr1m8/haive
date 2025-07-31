#!/usr/bin/env python3
"""Using the prebuilt state schemas for multi-agent systems.

This shows how to properly use MetaAgentState and MultiAgentState
from base_state_schemas.py
"""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")


from haive.core.schema.base_state_schemas import (
    HierarchicalAgentState,
    MetaAgentState,
    MultiAgentState,
)
from langchain_core.messages import HumanMessage


def test_meta_agent_state():
    """Test using the prebuilt MetaAgentState."""
    # MetaAgentState is for agents that spawn other agents
    meta_state = MetaAgentState(
        messages=[HumanMessage(content="Build a web app")],
        agent_name="coordinator",
        agent_type="meta",
    )

    # Spawn sub-agents
    meta_state.spawn_sub_agent(
        name="planner", agent_type="llm", initial_state={"task": "Create project plan"}
    )

    meta_state.spawn_sub_agent(
        name="coder", agent_type="llm", initial_state={"task": "Write code"}
    )

    # Update results
    meta_state.update_sub_agent_result(
        "planner", {"plan": "1. Design\n2. Code\n3. Test"}
    )

    return meta_state


def test_multi_agent_state():
    """Test using the prebuilt MultiAgentState."""
    # MultiAgentState provides isolation between agents
    multi_state = MultiAgentState(
        messages=[HumanMessage(content="Analyze this document")]
    )

    # Each agent gets its own state
    planner_state = multi_state.get_agent_state("planner")
    planner_state.agent_type = "llm"
    planner_state.tool_results = {"plan": "Analysis plan"}

    analyzer_state = multi_state.get_agent_state("analyzer")
    analyzer_state.agent_type = "tool_executor"
    analyzer_state.tool_results = {"analysis": "Document is about X"}

    # Broadcast shared data
    multi_state.broadcast_to_agents({"document_url": "https://example.com/doc.pdf"})

    # Collect results
    multi_state.collect_agent_results()

    return multi_state


def test_with_actual_agents():
    """Test how these states work with actual Agent instances."""
    # Create multi-agent state
    multi_state = MultiAgentState()

    # Problem: The Agent class expects its own state schema
    # but MultiAgentState.agent_states contains AgentState instances

    # This is the mismatch:
    # 1. SimpleAgent expects its state_schema (e.g., SimpleState)
    # 2. MultiAgentState provides AgentState instances
    # 3. No automatic mapping between them

    return multi_state


def test_hierarchical_state():
    """Test hierarchical agent state."""
    # Parent agent
    parent_state = HierarchicalAgentState(
        agent_name="supervisor",
        messages=[HumanMessage(content="Coordinate the analysis")],
    )

    # Add child agents
    parent_state.add_child_agent("researcher")
    parent_state.add_child_agent("writer")
    parent_state.add_child_agent("reviewer")

    # Update child results
    parent_state.agent_states["researcher"].tool_results = {"facts": ["fact1", "fact2"]}
    parent_state.agent_states["writer"].tool_results = {"draft": "Article draft..."}
    parent_state.agent_states["reviewer"].tool_results = {"score": 0.85}

    # Aggregate results
    parent_state.aggregate_child_results()

    return parent_state


def analyze_prebuilt_patterns():
    """Analyze the patterns in prebuilt schemas."""


if __name__ == "__main__":
    # Test each pattern
    meta_state = test_meta_agent_state()
    multi_state = test_multi_agent_state()
    actual_agents = test_with_actual_agents()
    hierarchical = test_hierarchical_state()

    analyze_prebuilt_patterns()
