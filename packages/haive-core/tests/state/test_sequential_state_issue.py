#!/usr/bin/env python3
"""
Test script to identify the core state management issues in multi-agent systems.

This script demonstrates the problems with:
1. Global state vs typed state schemas
2. Agent-specific input/output schema mismatches
3. State projection/mapping issues
"""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from typing import Any, Dict, List, Optional

from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import BaseMessage, HumanMessage
from pydantic import BaseModel, Field

from haive.core.engine.llm.factories.litellm_factory import LiteLLMFactory
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode

# Core imports
from haive.core.schema.state_schema import StateSchema


class PlannerState(StateSchema):
    """State schema for a planner agent."""

    messages: List[BaseMessage] = Field(default_factory=list)
    task: str = Field(default="")
    plan: Optional[str] = Field(default=None)
    plan_steps: List[str] = Field(default_factory=list)


class ExecutorState(StateSchema):
    """State schema for an executor agent."""

    messages: List[BaseMessage] = Field(default_factory=list)
    plan: str = Field(default="")
    execution_result: Optional[str] = Field(default=None)
    completed_steps: List[str] = Field(default_factory=list)


class GlobalMultiAgentState(StateSchema):
    """Global state that attempts to combine all agent states."""

    # Shared fields
    messages: List[BaseMessage] = Field(default_factory=list)

    # Planner fields
    task: str = Field(default="")
    plan: Optional[str] = Field(default=None)
    plan_steps: List[str] = Field(default_factory=list)

    # Executor fields
    execution_result: Optional[str] = Field(default=None)
    completed_steps: List[str] = Field(default_factory=list)

    # Coordination fields
    current_agent: str = Field(default="planner")
    agent_outputs: Dict[str, Any] = Field(default_factory=dict)


def test_schema_composition_issues():
    """Test the schema composition issues."""
    print("=" * 60)
    print("TESTING SCHEMA COMPOSITION ISSUES")
    print("=" * 60)

    # Create simple agents with different state schemas
    factory = LiteLLMFactory()
    llm = factory.create_engine(model="gpt-4o-mini")

    # Create planner agent
    planner = SimpleAgent(name="planner", engine=llm, state_schema=PlannerState)

    # Create executor agent
    executor = SimpleAgent(name="executor", engine=llm, state_schema=ExecutorState)

    agents = [planner, executor]

    print(f"Planner state schema: {PlannerState}")
    print(f"Executor state schema: {ExecutorState}")

    # Test AgentSchemaComposer
    composer = AgentSchemaComposer(agents)

    # Test SEQUENCE mode
    print("\n--- SEQUENCE MODE ---")
    try:
        sequence_schema = composer.build_schema(BuildMode.SEQUENCE)
        print(f"✅ Sequence schema created: {sequence_schema}")
        print(f"Schema fields: {list(sequence_schema.model_fields.keys())}")
    except Exception as e:
        print(f"❌ Sequence schema failed: {e}")

    # Test PARALLEL mode
    print("\n--- PARALLEL MODE ---")
    try:
        parallel_schema = composer.build_schema(BuildMode.PARALLEL)
        print(f"✅ Parallel schema created: {parallel_schema}")
        print(f"Schema fields: {list(parallel_schema.model_fields.keys())}")
    except Exception as e:
        print(f"❌ Parallel schema failed: {e}")


def test_state_projection_issues():
    """Test state projection and agent execution issues."""
    print("\n" + "=" * 60)
    print("TESTING STATE PROJECTION ISSUES")
    print("=" * 60)

    # Create a global state instance
    global_state = GlobalMultiAgentState(
        messages=[HumanMessage(content="Create a plan for building a web app")],
        task="Build a web app",
        current_agent="planner",
    )

    print(f"Global state: {global_state}")

    # Create agents
    factory = LiteLLMFactory()
    llm = factory.create_engine(model="gpt-4o-mini")

    planner = SimpleAgent(name="planner", engine=llm, state_schema=PlannerState)

    # Problem 1: Agent expects PlannerState but gets GlobalMultiAgentState
    print("\n--- ATTEMPTING TO RUN PLANNER ---")
    try:
        # This should fail because the agent expects PlannerState
        # but global_state is GlobalMultiAgentState
        planner_input = {"messages": global_state.messages, "task": global_state.task}

        print(f"Planner input: {planner_input}")
        print(f"Planner expected schema: {PlannerState}")

        # This will likely fail due to schema mismatch
        result = planner.invoke(planner_input)
        print(f"✅ Planner result: {result}")

    except Exception as e:
        print(f"❌ Planner execution failed: {e}")
        print(
            f"   This is the core issue - agent expects specific schema but gets different one"
        )


def test_proposed_solution():
    """Test a proposed solution with proper state projection."""
    print("\n" + "=" * 60)
    print("TESTING PROPOSED SOLUTION")
    print("=" * 60)

    # Solution: Create state projection functions
    def project_global_to_planner(global_state: GlobalMultiAgentState) -> PlannerState:
        """Project global state to planner state."""
        return PlannerState(
            messages=global_state.messages,
            task=global_state.task,
            plan=global_state.plan,
            plan_steps=global_state.plan_steps,
        )

    def merge_planner_to_global(
        planner_result: PlannerState, global_state: GlobalMultiAgentState
    ) -> GlobalMultiAgentState:
        """Merge planner result back to global state."""
        return GlobalMultiAgentState(
            messages=planner_result.messages,
            task=planner_result.task,
            plan=planner_result.plan,
            plan_steps=planner_result.plan_steps,
            # Preserve other fields
            execution_result=global_state.execution_result,
            completed_steps=global_state.completed_steps,
            current_agent="executor",  # Move to next agent
            agent_outputs={
                **global_state.agent_outputs,
                "planner": planner_result.model_dump(),
            },
        )

    # Test the projection approach
    global_state = GlobalMultiAgentState(
        messages=[HumanMessage(content="Create a plan for building a web app")],
        task="Build a web app",
        current_agent="planner",
    )

    # Create agent
    factory = LiteLLMFactory()
    llm = factory.create_engine(model="gpt-4o-mini")

    planner = SimpleAgent(name="planner", engine=llm, state_schema=PlannerState)

    try:
        # Step 1: Project global state to agent state
        planner_state = project_global_to_planner(global_state)
        print(f"✅ Projected state: {planner_state}")

        # Step 2: Execute agent with proper state
        planner_input = planner_state.model_dump()
        print(f"Planner input: {planner_input}")

        result = planner.invoke(planner_input)
        print(f"✅ Planner result: {result}")

        # Step 3: Merge result back to global state
        if isinstance(result, dict):
            planner_result = PlannerState(**result)
        else:
            planner_result = result

        updated_global = merge_planner_to_global(planner_result, global_state)
        print(f"✅ Updated global state: {updated_global}")

    except Exception as e:
        print(f"❌ Projection solution failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    print("🔍 TESTING MULTI-AGENT STATE MANAGEMENT ISSUES")
    print("=" * 60)

    test_schema_composition_issues()
    test_state_projection_issues()
    test_proposed_solution()

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("1. Schema composition creates mismatched schemas")
    print("2. Agents expect specific state types but get global state")
    print("3. State projection/mapping is needed for type safety")
    print("4. Agent node v2 needs proper projection logic")
    print("=" * 60)
