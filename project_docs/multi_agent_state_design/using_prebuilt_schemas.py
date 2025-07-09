#!/usr/bin/env python3
"""
Using the prebuilt state schemas for multi-agent systems.

This shows how to properly use MetaAgentState and MultiAgentState
from base_state_schemas.py
"""

import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive')

from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from haive.core.engine.base import Engine  # Import Engine first
from haive.core.schema.base_state_schemas import (
    MetaAgentState, 
    MultiAgentState,
    AgentState,
    MessagingState,
    HierarchicalAgentState
)
from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent


def test_meta_agent_state():
    """Test using the prebuilt MetaAgentState."""
    print("=" * 60)
    print("TESTING PREBUILT META AGENT STATE")
    print("=" * 60)
    
    # MetaAgentState is for agents that spawn other agents
    meta_state = MetaAgentState(
        messages=[HumanMessage(content="Build a web app")],
        agent_name="coordinator",
        agent_type="meta"
    )
    
    # Spawn sub-agents
    meta_state.spawn_sub_agent(
        name="planner",
        agent_type="llm",
        initial_state={"task": "Create project plan"}
    )
    
    meta_state.spawn_sub_agent(
        name="coder", 
        agent_type="llm",
        initial_state={"task": "Write code"}
    )
    
    print(f"Sub-agents: {list(meta_state.sub_agents.keys())}")
    print(f"Coordination strategy: {meta_state.coordination_strategy}")
    
    # Update results
    meta_state.update_sub_agent_result("planner", {"plan": "1. Design\n2. Code\n3. Test"})
    
    print(f"Sub-agent results: {meta_state.sub_agent_results}")
    
    return meta_state


def test_multi_agent_state():
    """Test using the prebuilt MultiAgentState."""
    print("\n" + "=" * 60)
    print("TESTING PREBUILT MULTI AGENT STATE")
    print("=" * 60)
    
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
    
    print(f"Agent states: {list(multi_state.agent_states.keys())}")
    
    # Broadcast shared data
    multi_state.broadcast_to_agents({"document_url": "https://example.com/doc.pdf"})
    print(f"Shared context: {multi_state.shared_context}")
    
    # Collect results
    results = multi_state.collect_agent_results()
    print(f"Collected results: {results}")
    
    return multi_state


def test_with_actual_agents():
    """Test how these states work with actual Agent instances."""
    print("\n" + "=" * 60)
    print("TESTING WITH ACTUAL AGENTS")
    print("=" * 60)
    
    # Create multi-agent state
    multi_state = MultiAgentState()
    
    # Problem: The Agent class expects its own state schema
    # but MultiAgentState.agent_states contains AgentState instances
    
    # This is the mismatch:
    # 1. SimpleAgent expects its state_schema (e.g., SimpleState)
    # 2. MultiAgentState provides AgentState instances
    # 3. No automatic mapping between them
    
    print("Issue identified:")
    print("- Agents have their own state schemas")
    print("- MultiAgentState provides generic AgentState")
    print("- Need projection/mapping layer")
    
    return multi_state


def test_hierarchical_state():
    """Test hierarchical agent state."""
    print("\n" + "=" * 60)
    print("TESTING HIERARCHICAL AGENT STATE")
    print("=" * 60)
    
    # Parent agent
    parent_state = HierarchicalAgentState(
        agent_name="supervisor",
        messages=[HumanMessage(content="Coordinate the analysis")]
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
    aggregated = parent_state.aggregate_child_results()
    print(f"Child agents: {parent_state.child_agents}")
    print(f"Aggregated results: {aggregated}")
    
    return parent_state


def analyze_prebuilt_patterns():
    """Analyze the patterns in prebuilt schemas."""
    print("\n" + "=" * 60)
    print("ANALYSIS OF PREBUILT PATTERNS")
    print("=" * 60)
    
    print("Key observations:")
    print("1. MetaAgentState - For agents that spawn other agents dynamically")
    print("2. MultiAgentState - For parallel/isolated agent execution")
    print("3. HierarchicalAgentState - For parent-child agent relationships")
    print("4. AgentState - Base state for individual agents")
    
    print("\nThe missing piece:")
    print("- These states don't know about actual Agent instances")
    print("- They store serialized states, not agent objects")
    print("- No automatic state projection for typed agents")
    
    print("\nPotential solutions:")
    print("1. Enhanced MultiAgentState that registers Agent instances")
    print("2. State projection layer in agent nodes")
    print("3. Agent-aware coordinator that handles mapping")


if __name__ == "__main__":
    # Test each pattern
    meta_state = test_meta_agent_state()
    multi_state = test_multi_agent_state()
    actual_agents = test_with_actual_agents()
    hierarchical = test_hierarchical_state()
    
    analyze_prebuilt_patterns()
    
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)
    print("1. Use MultiAgentState as base (it has proper isolation)")
    print("2. Extend it to register actual Agent instances")
    print("3. Add projection methods for type safety")
    print("4. Keep serialization separate from runtime state")