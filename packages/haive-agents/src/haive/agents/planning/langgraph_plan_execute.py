"""LangGraph Plan and Execute Implementation.

Following the official LangGraph tutorial pattern:
https://langchain-ai.github.io/langgraph/tutorials/plan-and-execute/plan-and-execute/
"""

from typing import List, Literal, Union

from haive.core.schema.prebuilt.messages.messages_state import MessagesState
from langchain_core.messages import BaseMessage
from langgraph.graph import END
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_base import BuildMode, MultiAgentBase
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# ============================================================================
# MODELS (following official LangGraph tutorial)
# ============================================================================


class Plan(BaseModel):
    """A plan to follow for solving a task."""

    steps: list[str] = Field(
        description="Different steps to follow, should be in sorted order"
    )


class Response(BaseModel):
    """Response to user."""

    response: str = Field(description="Response to the user")


class Act(BaseModel):
    """Action to perform - either respond or continue."""

    action: Response | Plan = Field(
        description="Action to perform. If you want to respond to user, use Response. "
        "If you need to further use tools to get the answer, use Plan."
    )


# ============================================================================
# STATE SCHEMA (following LangGraph pattern)
# ============================================================================


class PlanExecuteState(MessagesState):
    """State for the plan-and-execute agent."""

    plan: list[str] = Field(default_factory=list, description="The plan to follow")
    past_steps: list[str] = Field(
        default_factory=list, description="Steps that have been executed"
    )
    response: str = Field(default="", description="Final response")


# ============================================================================
# ROUTING FUNCTIONS (following LangGraph pattern)
# ============================================================================


def should_continue(state: PlanExecuteState) -> str:
    """Decide whether to continue executing the plan or finish."""
    if state.response:
        return END
    if state.plan:
        return "agent"
    return "replan"


def route_replan(state: PlanExecuteState) -> str:
    """Route after replanning."""
    if state.response:
        return END
    return "agent"


# ============================================================================
# PROMPT TEMPLATES (following LangGraph style)
# ============================================================================

PLANNER_PROMPT = """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps."""

EXECUTOR_PROMPT = """Execute the given task using the available tools. \
Return the result when you have completed the task."""

REPLANNER_PROMPT = """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan."""


# ============================================================================
# LANGGRAPH PLAN AND EXECUTE AGENT
# ============================================================================


def create_langgraph_plan_execute(
    name: str = "PlanExecute", model: str = "gpt-4o-mini", tools: list | None = None
) -> MultiAgentBase:
    """Create Plan and Execute agent following official LangGraph tutorial.

    Args:
        name: Name for the agent
        model: Model to use for all agents
        tools: Tools available to executor

    Returns:
        MultiAgentBase: Plan and Execute system following LangGraph pattern
    """
    if tools is None:
        tools = []

    # Create planner agent (generates initial plan)
    planner = SimpleAgent(
        name="planner",
        model=model,
        system_message=PLANNER_PROMPT,
        structured_output_model=Plan,
    )

    # Create executor agent (executes individual steps)
    executor = ReactAgent(
        name="agent", model=model, system_message=EXECUTOR_PROMPT, tools=tools
    )

    # Create replanner agent (updates plan or provides final answer)
    replanner = SimpleAgent(
        name="replan",
        model=model,
        system_message=REPLANNER_PROMPT,
        structured_output_model=Act,
    )

    # Define conditional branches following LangGraph pattern
    branches = [
        # After execution: continue, replan, or end
        (executor, should_continue, {"agent": executor, "replan": replanner, END: END}),
        # After replanning: continue or end
        (replanner, route_replan, {"agent": executor, END: END}),
    ]

    # Create MultiAgentBase following LangGraph flow
    return MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=branches,
        entry_points=[planner],  # Start with planning
        name=name,
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,
    )


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================


def create_plan_execute_agent(tools: list | None = None) -> MultiAgentBase:
    """Create a Plan and Execute agent with default settings."""
    return create_langgraph_plan_execute(name="PlanExecuteAgent", tools=tools or [])


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create agent following LangGraph tutorial
    agent = create_plan_execute_agent()

    # Test the pattern
    result = agent.run("What is the capital of France and what is its population?")
