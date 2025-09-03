#!/usr/bin/env python3
"""Proof of Concept: Meta Agent State Pattern.

This explores a state that contains agents and itself, with proper type safety
and state projection capabilities.
"""
from __future__ import annotations
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage, HumanMessage
from haive.core.schema.state_schema import StateSchema
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar
from abc import ABC, abstractmethod

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")


# Type variable for agent state schemas
TAgentState = TypeVar("TAgentState", bound=StateSchema)


class AgentStateView(BaseModel, Generic[TAgentState]):
    """A view into the meta state for a specific agent."""

    # Shared fields that all agents can see
    messages: list[BaseMessage]
    shared_context: dict[str, Any]

    # Agent-specific state
    agent_state: TAgentState

    # Meta information
    agent_name: str
    execution_count: int


class MetaAgentState(StateSchema):
    """Meta state that contains agents and manages their states.

    This state:
    - Contains agent instances
    - Manages agent-specific states
    - Provides type-safe projections
    - Tracks execution flow
    """

    # Shared communication channel
    messages: list[BaseMessage] = Field(default_factory=list)

    # Shared context accessible by all agents
    shared_context: dict[str, Any] = Field(
        default_factory=dict, description="Context shared across all agents"
    )

    # Agent registry - agent name to state schema type
    agent_schemas: dict[str, type[StateSchema]] = Field(
        default_factory=dict, exclude=True  # Don't serialize schema types
    )

    # Agent states - agent name to state instance
    agent_states: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Serialized agent states"
    )

    # Execution control
    current_agent: str | None = None
    execution_history: list[dict[str, Any]] = Field(default_factory=list)
    execution_counts: dict[str, int] = Field(default_factory=dict)

    # Meta information about the state itself
    meta: dict[str, Any] = Field(
        default_factory=lambda: {
            "version": "1.0",
            "created_at": None,
            "last_updated": None,
        }
    )

    def register_agent(self, agent_name: str, state_schema: type[StateSchema]) -> None:
        """Register an agent with its state schema."""
        self.agent_schemas[agent_name] = state_schema

        # Initialize agent state if not exists
        if agent_name not in self.agent_states:
            # Create default instance of agent's state
            default_state = state_schema()
            self.agent_states[agent_name] = default_state.model_dump()
            self.execution_counts[agent_name] = 0

    def get_agent_view(self, agent_name: str) -> AgentStateView:
        """Get a type-safe view of the state for a specific agent.

        This method:
        1. Retrieves the agent's specific state
        2. Combines it with shared fields
        3. Returns a typed view
        """
        if agent_name not in self.agent_schemas:
            raise ValueError(f"Agent '{agent_name}' not registered")

        # Get agent's schema type
        schema_type = self.agent_schemas[agent_name]

        # Deserialize agent's state
        agent_state_data = self.agent_states.get(agent_name, {})
        agent_state = schema_type(**agent_state_data)

        # Create view with shared + agent-specific state
        return AgentStateView(
            messages=self.messages,
            shared_context=self.shared_context,
            agent_state=agent_state,
            agent_name=agent_name,
            execution_count=self.execution_counts.get(agent_name, 0),
        )

    def update_from_agent(
        self,
        agent_name: str,
        updated_state: StateSchema,
        updated_messages: List[BaseMessage] | None = None,
    ) -> None:
        """Update meta state from agent execution result.

        This method:
        1. Updates agent-specific state
        2. Optionally updates shared messages
        3. Tracks execution history
        """
        if agent_name not in self.agent_schemas:
            raise ValueError(f"Agent '{agent_name}' not registered")

        # Update agent's state
        self.agent_states[agent_name] = updated_state.model_dump()

        # Update shared messages if provided
        if updated_messages is not None:
            self.messages = updated_messages

        # Update execution tracking
        self.execution_counts[agent_name] = self.execution_counts.get(agent_name, 0) + 1
        self.execution_history.append(
            {
                "agent": agent_name,
                "timestamp": None,  # Would use real timestamp
                "state_size": len(str(updated_state.model_dump())),
            }
        )

        # Update current agent
        self.current_agent = agent_name

    def get_next_agent(self, current_agent: str) -> str | None:
        """Determine next agent in execution flow."""
        # This is where routing logic would go
        # For now, simple sequential execution
        agents = list(self.agent_schemas.keys())
        if current_agent in agents:
            idx = agents.index(current_agent)
            if idx < len(agents) - 1:
                return agents[idx + 1]
        return None


# Example Agent State Schemas
class PlannerState(StateSchema):
    """State for a planning agent."""

    task: str = Field(default="", description="Task to plan")
    plan: str | None = Field(default=None, description="Generated plan")
    plan_steps: list[str] = Field(default_factory=list)
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class ExecutorState(StateSchema):
    """State for an execution agent."""

    plan: str = Field(default="", description="Plan to execute")
    current_step: int = Field(default=0)
    completed_steps: list[str] = Field(default_factory=list)
    execution_result: str | None = Field(default=None)
    success: bool = Field(default=False)


class ReviewerState(StateSchema):
    """State for a review agent."""

    plan: str = Field(default="")
    execution_result: str = Field(default="")
    review_notes: list[str] = Field(default_factory=list)
    approval_status: str | None = Field(default=None)
    score: float = Field(default=0.0)


def test_meta_agent_state():
    """Test the meta agent state pattern."""

    # Create meta state
    meta_state = MetaAgentState(
        messages=[HumanMessage(content="Build a web application")],
        shared_context={"project": "web_app", "deadline": "2024-12-31"},
    )

    # Register agents with their schemas
    meta_state.register_agent("planner", PlannerState)
    meta_state.register_agent("executor", ExecutorState)
    meta_state.register_agent("reviewer", ReviewerState)

    # Test 1: Get planner view
    planner_view = meta_state.get_agent_view("planner")

    # Simulate planner execution
    planner_state = planner_view.agent_state
    planner_state.task = "Build a web application"
    planner_state.plan = "1. Design UI\n2. Build backend\n3. Deploy"
    planner_state.plan_steps = ["Design UI", "Build backend", "Deploy"]
    planner_state.confidence = 0.85

    # Update meta state
    meta_state.update_from_agent("planner", planner_state)

    # Test 2: Get executor view
    executor_view = meta_state.get_agent_view("executor")

    # Executor should be able to see the plan from shared context
    # or we can explicitly transfer it
    executor_state = executor_view.agent_state

    # Transfer plan from planner to executor
    planner_data = meta_state.agent_states["planner"]
    executor_state.plan = planner_data.get("plan", "")

    # Simulate execution
    executor_state.completed_steps = ["Design UI"]
    executor_state.current_step = 1
    executor_state.execution_result = "UI design completed successfully"
    executor_state.success = True

    meta_state.update_from_agent("executor", executor_state)

    # Test 3: State consistency

    # Verify type safety
    try:
        # This should work - correct type
        planner_view2 = meta_state.get_agent_view("planner")
        assert isinstance(planner_view2.agent_state, PlannerState)

        # The agent states maintain their specific types
        assert hasattr(planner_view2.agent_state, "plan_steps")
        assert hasattr(planner_view2.agent_state, "confidence")

    except Exception as e:
        pass")

    return meta_state


def test_state_transitions():
    """Test state transitions between agents."""

    # Create and setup meta state
    meta_state = MetaAgentState()
    meta_state.register_agent("planner", PlannerState)
    meta_state.register_agent("executor", ExecutorState)

    # Define state transfer rules
    def transfer_planner_to_executor(meta_state: MetaAgentState):
        """Transfer relevant fields from planner to executor."""
        planner_data = meta_state.agent_states["planner"]
        executor_view = meta_state.get_agent_view("executor")

        # Transfer plan
        executor_view.agent_state.plan = planner_data.get("plan", "")

        # Update executor state
        meta_state.update_from_agent("executor", executor_view.agent_state)

    # Test the transfer
    planner_view = meta_state.get_agent_view("planner")
    planner_view.agent_state.plan = "Test plan"
    planner_view.agent_state.plan_steps = ["Step 1", "Step 2"]
    meta_state.update_from_agent("planner", planner_view.agent_state)

    # Transfer state
    transfer_planner_to_executor(meta_state)

    # Verify transfer
    executor_view = meta_state.get_agent_view("executor")
    assert executor_view.agent_state.plan == "Test plan"

    return meta_state


if __name__ == "__main__":
    # Run tests
    meta_state1 = test_meta_agent_state()
    meta_state2 = test_state_transitions()
