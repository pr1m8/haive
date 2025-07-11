#!/usr/bin/env python3
"""Test Plan-and-Execute to identify multi-agent state issues.

This test demonstrates:
1. Current state management problems
2. Type safety issues
3. Proposed solutions
"""

import sys

sys.path.insert(0, "/home/will/Projects/haive/backend/haive")

from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import Field

from haive.agents.base.agent import Agent

# Import the models and state
from haive.agents.planning.p_and_e.models import Act, Plan, PlanStep, Response, StepType
from haive.agents.planning.p_and_e.state import PlanExecuteState

# Import agents
from haive.agents.simple.agent import SimpleAgent

# Skip LLM for now, focus on state issues


def test_current_plan_execute_state():
    """Test the current PlanExecuteState approach."""
    # Create state
    state = PlanExecuteState(
        messages=[HumanMessage(content="Build a web scraper")],
        context="Need to scrape product data from e-commerce sites",
    )

    # Create a plan
    plan = Plan(
        objective="Build a web scraper",
        steps=[
            PlanStep(
                step_id=1,
                description="Research web scraping libraries",
                step_type=StepType.RESEARCH,
                expected_output="List of suitable libraries",
            ),
            PlanStep(
                step_id=2,
                description="Design scraper architecture",
                step_type=StepType.ANALYSIS,
                expected_output="Architecture diagram",
                dependencies=[1],
            ),
            PlanStep(
                step_id=3,
                description="Implement the scraper",
                step_type=StepType.ACTION,
                expected_output="Working scraper code",
                dependencies=[1, 2],
            ),
        ],
        total_steps=3,
    )

    state.plan = plan

    return state


def test_agent_state_mismatch():
    """Test the state mismatch issue with individual agents."""
    # Skip creating actual LLM for this demo
    llm = None  # Would be actual engine

    # Issue 1: Planner agent expects different state

    # Planner might expect a simpler state
    planner = SimpleAgent(
        name="planner",
        engine=llm,
        instructions="Create a plan for the given objective",
        # The agent might have its own internal state schema
    )

    # Problem: PlanExecuteState has many fields the planner doesn't need
    state = PlanExecuteState(messages=[HumanMessage(content="Build a web app")])

    # Issue 2: Executor agent expects different fields

    SimpleAgent(
        name="executor", engine=llm, instructions="Execute the current step of the plan"
    )

    # Executor needs: current_step, previous_results
    # But gets entire PlanExecuteState

    # Issue 3: Type safety lost

    # Each agent might have specific output schemas
    planner.output_schema = Act  # Planner outputs Act (Plan or Response)

    # But multi-agent flattens everything

    return state


def demonstrate_proposed_solution():
    """Demonstrate the proposed solution with proper state management."""
    # Solution: Create an agent-aware state that manages projections

    class AgentAwarePlanExecuteState(PlanExecuteState):
        """Enhanced state that can project views for specific agents."""

        # Track agent-specific data separately
        agent_data: dict[str, dict[str, Any]] = Field(default_factory=dict)

        def get_planner_view(self) -> dict[str, Any]:
            """Get state view for planner agent."""
            return {
                "messages": self.messages,
                "objective": self.objective,
                "context": self.context,
                # Planner doesn't need execution details
            }

        def get_executor_view(self) -> dict[str, Any]:
            """Get state view for executor agent."""
            return {
                "current_step": self.current_step,
                "previous_results": self.previous_results,
                "plan_status": self.plan_status,
                # Executor doesn't need replanning history
            }

        def get_replanner_view(self) -> dict[str, Any]:
            """Get state view for replanner agent."""
            return {
                "messages": self.messages,
                "plan": self.plan,
                "execution_results": self.execution_results,
                "errors": self.errors,
                # Replanner needs full context
            }

        def update_from_agent(self, agent_name: str, result: Any) -> None:
            """Update state from agent result."""
            # Store agent-specific results
            self.agent_data[agent_name] = result

            # Update main state based on agent type
            if agent_name == "planner" and isinstance(result, dict):
                if "action" in result:
                    act = result["action"]
                    if isinstance(act, dict) and "plan" in act:
                        self.plan = Plan(**act["plan"])

            elif agent_name == "executor" and isinstance(result, dict):
                if "result" in result:
                    self.execution_results.append(result["result"])

    # Test the enhanced state
    state = AgentAwarePlanExecuteState(
        messages=[HumanMessage(content="Build a web app")]
    )

    # Each agent gets only what it needs
    state.get_planner_view()

    state.get_executor_view()

    state.get_replanner_view()

    return state


def show_improved_multi_agent_pattern():
    """Show how multi-agent should work with proper state handling."""


if __name__ == "__main__":

    # Test current approach
    current_state = test_current_plan_execute_state()

    # Show the issues
    mismatch_demo = test_agent_state_mismatch()

    # Demonstrate solution
    solution_demo = demonstrate_proposed_solution()

    # Show improved pattern
    show_improved_multi_agent_pattern()
