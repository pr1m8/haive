"""Clean Plan and Execute Implementation following LangGraph patterns.

This implementation follows the standard LangGraph Plan and Execute pattern with:
- Simple models (not overcomplicated)
- MultiAgentBase for orchestration
- React agent for execution
- Simple agent for planning
- Clean routing logic
"""

from typing import List, Literal

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_base import BuildMode, MultiAgentBase
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# ============================================================================
# SIMPLE MODELS (following LangGraph pattern)
# ============================================================================


class Plan(BaseModel):
    """A simple plan with list of steps."""

    steps: list[str] = Field(description="List of steps to execute")


class Act(BaseModel):
    """Action to take - either respond or replan."""

    action: Literal["response", "continue"] = Field(
        description="Whether to respond with final answer or continue with plan"
    )
    response: str = Field(description="Response to user or next step to execute")


# ============================================================================
# CLEAN STATE SCHEMA
# ============================================================================


class PlanExecuteState(MessagesState):
    """Clean state schema for Plan and Execute."""

    plan: list[str] = Field(default_factory=list, description="Current plan steps")
    past_steps: list[str] = Field(default_factory=list, description="Completed steps")
    response: str = Field(default="", description="Final response")


# ============================================================================
# ROUTING FUNCTIONS
# ============================================================================


def should_continue(state: PlanExecuteState) -> str:
    """Decide whether to continue executing or move to replanning."""
    if state.response:
        return "END"
    if state.plan:
        return "agent"  # Execute next step
    return "replan"  # Need to replan


def route_after_replan(state: PlanExecuteState) -> str:
    """Route after replanning decision."""
    if state.response:
        return "END"
    return "agent"


# ============================================================================
# CLEAN PLAN AND EXECUTE AGENT
# ============================================================================


def create_clean_plan_execute_agent(
    name: str = "PlanExecute",
    planner_model: str = "gpt-4o-mini",
    executor_model: str = "gpt-4o-mini",
    tools: list | None = None,
) -> MultiAgentBase:
    """Create a clean Plan and Execute agent following LangGraph patterns.

    Args:
        name: Name for the agent
        planner_model: Model for planning
        executor_model: Model for execution
        tools: Tools available to executor

    Returns:
        MultiAgentBase: Clean Plan and Execute system
    """
    if tools is None:
        tools = []

    # Create planning agent (Simple agent for planning)
    planner = SimpleAgent(
        name="planner",
        model=planner_model,
        system_message="""For the given objective, come up with a simple step by step plan.
This plan should involve individual tasks, that if executed correctly will yield the correct answer.
Do not add any superfluous steps. The result of the final step should be the final answer.
Make sure that each step has all the information needed - do not skip steps.""",
        structured_output_model=Plan,
    )

    # Create execution agent (React agent for tool usage)
    executor = ReactAgent(
        name="agent",
        model=executor_model,
        system_message="""Execute the given step in the plan. Use tools as needed.
When you have completed the step, provide a clear result.""",
        tools=tools,
    )

    # Create replanning agent (Simple agent for decision making)
    replanner = SimpleAgent(
        name="replan",
        model=planner_model,
        system_message="""For the given objective, come up with a simple step by step plan.
This plan should involve individual tasks, that if executed correctly will yield the correct answer.
Do not add any superfluous steps. The result of the final step should be the final answer.
Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that.
Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.""",
        structured_output_model=Act,
    )

    # Define branches for routing
    branches = [
        # After execution, check if we should continue or replan
        (
            executor,
            should_continue,
            {"agent": executor, "replan": replanner, "END": "END"},
        ),
        # After replanning, decide next action
        (replanner, route_after_replan, {"agent": executor, "END": "END"}),
    ]

    # Create MultiAgentBase with clean configuration
    return MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=branches,
        entry_points=[planner],  # Start with planner
        name=name,
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,
    )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def create_simple_plan_execute(tools: list | None = None) -> MultiAgentBase:
    """Create a simple Plan and Execute agent with default settings."""
    return create_clean_plan_execute_agent(name="SimplePlanExecute", tools=tools or [])


# Example usage
if __name__ == "__main__":
    # Create a simple plan and execute agent
    agent = create_simple_plan_execute()

    # Test basic functionality
    result = agent.run("What is the capital of France?")
