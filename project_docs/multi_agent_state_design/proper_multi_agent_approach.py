#!/usr/bin/env python3
"""
Proper Multi-Agent Approach using MultiAgentStateSchema

This demonstrates the correct pattern for multi-agent systems in Haive.
"""

import sys
sys.path.insert(0, '/home/will/Projects/haive/backend/haive')

from typing import Dict, Any, List, Optional
from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import Field

# Import the proper multi-agent schema
from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema
from haive.core.schema.state_schema import StateSchema
from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent


# Define individual agent state schemas
class PlannerState(StateSchema):
    """State for planning agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    task: str = Field(default="")
    plan: Optional[str] = Field(default=None)
    plan_steps: List[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    plan: str = Field(default="")
    execution_result: Optional[str] = Field(default=None)
    completed_steps: List[str] = Field(default_factory=list)


class ReviewerState(StateSchema):
    """State for reviewer agent."""
    messages: List[BaseMessage] = Field(default_factory=list)
    execution_result: str = Field(default="")
    review_notes: List[str] = Field(default_factory=list)
    approval: bool = Field(default=False)


# Option 1: Create multi-agent state from existing schema
def test_from_existing_schema():
    """Test creating multi-agent schema from existing schema."""
    print("=" * 60)
    print("OPTION 1: From Existing Schema")
    print("=" * 60)
    
    # Create a base schema
    class TeamState(StateSchema):
        messages: List[BaseMessage] = Field(default_factory=list)
        project_goal: str = Field(default="")
        team_status: str = Field(default="initializing")
    
    # Convert to multi-agent schema
    MultiTeamState = MultiAgentStateSchema.from_state_schema(
        TeamState,
        name="MultiTeamState"
    )
    
    # Now we can instantiate with agents
    state = MultiTeamState(
        messages=[HumanMessage(content="Build a web app")],
        project_goal="Create an e-commerce platform",
        team_status="planning"
    )
    
    print(f"Created multi-agent state: {state.__class__.__name__}")
    print(f"Has engines field: {'engines' in state.model_fields}")
    print(f"Engines: {state.engines}")
    
    return state


# Option 2: Direct multi-agent state definition
class ProjectTeamState(MultiAgentStateSchema):
    """
    Multi-agent state for a project team.
    
    This automatically:
    - Has an engines field
    - Populates engines from agents
    - Makes engines accessible to nodes
    """
    
    # Shared state
    messages: List[BaseMessage] = Field(default_factory=list)
    project_name: str = Field(default="")
    current_phase: str = Field(default="planning")
    
    # Agent-specific states (these would be populated by agent nodes)
    planner_state: Optional[Dict[str, Any]] = Field(default=None)
    executor_state: Optional[Dict[str, Any]] = Field(default=None)
    reviewer_state: Optional[Dict[str, Any]] = Field(default=None)
    
    # Agents field that will be discovered by populate_engines_dict
    agents: Dict[str, Agent] = Field(default_factory=dict)


def test_direct_multi_agent_state():
    """Test direct multi-agent state definition."""
    print("\n" + "=" * 60)
    print("OPTION 2: Direct Multi-Agent State")
    print("=" * 60)
    
    # Create state
    state = ProjectTeamState(
        messages=[HumanMessage(content="Build the project")],
        project_name="E-commerce Platform",
        current_phase="planning"
    )
    
    # The populate_engines_dict validator will run automatically
    # and collect engines from the agents field
    
    print(f"State class: {state.__class__.__name__}")
    print(f"Engines field populated: {state.engines}")
    print(f"Current phase: {state.current_phase}")
    
    return state


# Option 3: Multi-agent state with actual agents
def test_with_agents():
    """Test multi-agent state with actual agent instances."""
    print("\n" + "=" * 60)
    print("OPTION 3: With Actual Agents")
    print("=" * 60)
    
    # Note: In real usage, agents would be created with engines
    # For this example, we'll show the pattern
    
    class TeamWithAgentsState(MultiAgentStateSchema):
        """State that includes agent instances."""
        messages: List[BaseMessage] = Field(default_factory=list)
        
        # This is the key - agents field that gets discovered
        agents: Dict[str, Agent] = Field(default_factory=dict)
        
        # Shared context
        shared_data: Dict[str, Any] = Field(default_factory=dict)
    
    # Create state
    state = TeamWithAgentsState(
        messages=[HumanMessage(content="Start project")]
    )
    
    # In practice, agents would be added by the multi-agent class
    # state.agents["planner"] = PlannerAgent(...)
    # state.agents["executor"] = ExecutorAgent(...)
    
    # The populate_engines_dict will:
    # 1. Find agents in state.agents
    # 2. Extract their engines
    # 3. Add with qualified names (e.g., "planner.llm")
    # 4. Make them accessible via state.engines
    
    print(f"State ready for agents: {state.__class__.__name__}")
    print(f"Engines will be auto-populated from agents")
    
    return state


# The key pattern: How agent nodes work with this
def explain_agent_node_pattern():
    """Explain how agent nodes work with MultiAgentStateSchema."""
    print("\n" + "=" * 60)
    print("HOW AGENT NODES USE THIS")
    print("=" * 60)
    
    print("""
The key insight is that EngineNodeConfig looks for engines in state.engines.
MultiAgentStateSchema ensures this field exists and is populated.

Pattern:
1. Multi-agent creates MultiAgentStateSchema
2. Agents are registered in state.agents
3. populate_engines_dict() runs automatically
4. Engines are collected with qualified names
5. EngineNodeConfig can find engines by name

Example engine names in state.engines:
- "planner.llm" (from planner agent's llm engine)
- "executor.tool_engine" (from executor's tool engine)
- "llm" (if unique, also available without prefix)

This solves the engine visibility problem in multi-agent systems!
""")


def show_best_practice():
    """Show the recommended pattern."""
    print("\n" + "=" * 60)
    print("RECOMMENDED PATTERN")
    print("=" * 60)
    
    print("""
Best Practice for Multi-Agent Systems:

1. Define your multi-agent state extending MultiAgentStateSchema:
   ```python
   class MyTeamState(MultiAgentStateSchema):
       messages: List[BaseMessage]
       shared_context: Dict[str, Any]
       agents: Dict[str, Agent]  # Important!
   ```

2. Register agents in the state:
   ```python
   state.agents["researcher"] = ResearchAgent(engine=llm)
   state.agents["writer"] = WriterAgent(engine=llm)
   ```

3. Engines are automatically available:
   - state.engines["researcher.llm"]
   - state.engines["writer.llm"]

4. EngineNodeConfig can find engines:
   ```python
   node = EngineNodeConfig(
       engine_name="researcher.llm",  # Qualified name
       # or just "llm" if unique
   )
   ```

This maintains type safety while solving engine visibility!
""")


if __name__ == "__main__":
    # Test each approach
    from_existing = test_from_existing_schema()
    direct_state = test_direct_multi_agent_state()
    with_agents = test_with_agents()
    
    explain_agent_node_pattern()
    show_best_practice()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("✅ Use MultiAgentStateSchema for multi-agent systems")
    print("✅ It automatically handles engine visibility")
    print("✅ Engines are accessible via qualified names")
    print("✅ Solves the EngineNodeConfig lookup problem")
    print("✅ Maintains backward compatibility")