#!/usr/bin/env python3
"""Proper Multi-Agent Approach using MultiAgentStateSchema.

This demonstrates the correct pattern for multi-agent systems in Haive.
"""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from typing import Any, Dict, List, Optional

from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

# Import the proper multi-agent schema
from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import Field


# Define individual agent state schemas
class PlannerState(StateSchema):
    """State for planning agent."""

    messages: list[BaseMessage] = Field(default_factory=list)
    task: str = Field(default="")
    plan: str | None = Field(default=None)
    plan_steps: list[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State for executor agent."""

    messages: list[BaseMessage] = Field(default_factory=list)
    plan: str = Field(default="")
    execution_result: str | None = Field(default=None)
    completed_steps: list[str] = Field(default_factory=list)


class ReviewerState(StateSchema):
    """State for reviewer agent."""

    messages: list[BaseMessage] = Field(default_factory=list)
    execution_result: str = Field(default="")
    review_notes: list[str] = Field(default_factory=list)
    approval: bool = Field(default=False)


# Option 1: Create multi-agent state from existing schema
def test_from_existing_schema():
    """Test creating multi-agent schema from existing schema."""

    # Create a base schema
    class TeamState(StateSchema):
        messages: list[BaseMessage] = Field(default_factory=list)
        project_goal: str = Field(default="")
        team_status: str = Field(default="initializing")

    # Convert to multi-agent schema
    MultiTeamState = MultiAgentStateSchema.from_state_schema(
        TeamState, name="MultiTeamState"
    )

    # Now we can instantiate with agents
    state = MultiTeamState(
        messages=[HumanMessage(content="Build a web app")],
        project_goal="Create an e-commerce platform",
        team_status="planning",
    )

    return state


# Option 2: Direct multi-agent state definition
class ProjectTeamState(MultiAgentStateSchema):
    """Multi-agent state for a project team.

    This automatically:
    - Has an engines field
    - Populates engines from agents
    - Makes engines accessible to nodes
    """

    # Shared state
    messages: list[BaseMessage] = Field(default_factory=list)
    project_name: str = Field(default="")
    current_phase: str = Field(default="planning")

    # Agent-specific states (these would be populated by agent nodes)
    planner_state: dict[str, Any] | None = Field(default=None)
    executor_state: dict[str, Any] | None = Field(default=None)
    reviewer_state: dict[str, Any] | None = Field(default=None)

    # Agents field that will be discovered by populate_engines_dict
    agents: dict[str, Agent] = Field(default_factory=dict)


def test_direct_multi_agent_state():
    """Test direct multi-agent state definition."""
    # Create state
    state = ProjectTeamState(
        messages=[HumanMessage(content="Build the project")],
        project_name="E-commerce Platform",
        current_phase="planning",
    )

    # The populate_engines_dict validator will run automatically
    # and collect engines from the agents field

    return state


# Option 3: Multi-agent state with actual agents
def test_with_agents():
    """Test multi-agent state with actual agent instances."""
    # Note: In real usage, agents would be created with engines
    # For this example, we'll show the pattern

    class TeamWithAgentsState(MultiAgentStateSchema):
        """State that includes agent instances."""

        messages: list[BaseMessage] = Field(default_factory=list)

        # This is the key - agents field that gets discovered
        agents: dict[str, Agent] = Field(default_factory=dict)

        # Shared context
        shared_data: dict[str, Any] = Field(default_factory=dict)

    # Create state
    state = TeamWithAgentsState(messages=[HumanMessage(content="Start project")])

    # In practice, agents would be added by the multi-agent class

    # The populate_engines_dict will:
    # 1. Find agents in state.agents
    # 2. Extract their engines
    # 3. Add with qualified names (e.g., "planner.llm")
    # 4. Make them accessible via state.engines

    return state


# The key pattern: How agent nodes work with this
def explain_agent_node_pattern():
    """Explain how agent nodes work with MultiAgentStateSchema."""


def show_best_practice():
    """Show the recommended pattern."""


if __name__ == "__main__":
    # Test each approach
    from_existing = test_from_existing_schema()
    direct_state = test_direct_multi_agent_state()
    with_agents = test_with_agents()

    explain_agent_node_pattern()
    show_best_practice()
