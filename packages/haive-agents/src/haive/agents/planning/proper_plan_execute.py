"""Proper Plan & Execute Implementation using existing p_and_e components.

This implementation follows the LangGraph pattern using:
- SimpleAgent for planning
- ReactAgent for execution
- SimpleAgent for replanning with branching
- MultiAgentBase for orchestration
- Existing models, prompts, and state from p_and_e folder
"""

from typing import List

from langgraph.graph import END

from haive.agents.multi.enhanced_base import BuildMode, MultiAgentBase

# Import existing p_and_e components
from haive.agents.planning.p_and_e.models import Act, Plan, StepStatus
from haive.agents.planning.p_and_e.prompts import (
    EXECUTOR_SYSTEM_MESSAGE,
    PLANNER_SYSTEM_MESSAGE,
    REPLAN_SYSTEM_MESSAGE,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# ============================================================================
# ROUTING FUNCTIONS (LangGraph Pattern)
# ============================================================================


def should_continue(state: PlanExecuteState) -> str:
    """Route after execution: continue, replan, or end."""
    # If we have a final answer, we're done
    if state.final_answer:
        return "__end__"

    # If no plan, need to replan
    if not state.plan:
        return "replan"

    # If plan is complete, need to replan to decide if we're done
    if state.plan.is_complete:
        return "replan"

    # If there's a next step ready, continue execution
    if state.plan.next_step:
        return "agent"

    # Otherwise, need to replan
    return "replan"


def route_after_replan(state: PlanExecuteState) -> str:
    """Route after replanning: continue or end."""
    # If we have a final answer, we're done
    if state.final_answer:
        return "__end__"

    # If we have a plan with next steps, continue execution
    if state.plan and state.plan.next_step:
        return "agent"

    # Otherwise end
    return "__end__"


# ============================================================================
# AGENT PROCESSING FUNCTIONS
# ============================================================================


def process_planner_output(state: PlanExecuteState, planner_result) -> dict:
    """Process planner output and update state."""
    updates = {}

    # Extract Plan from structured output
    if hasattr(planner_result, "steps"):
        # Direct Plan object
        plan = planner_result
    elif hasattr(planner_result, "action") and hasattr(planner_result.action, "steps"):
        # Plan wrapped in Act
        plan = planner_result.action
    else:
        # Fallback - create simple plan from messages
        return {"plan": None}

    updates["plan"] = plan

    # Set current step if available
    if plan.next_step:
        updates["current_step_id"] = plan.next_step.step_id

    return updates


def process_executor_output(state: PlanExecuteState, executor_result) -> dict:
    """Process executor output and update state."""
    updates = {}

    # Update current step with result
    if state.plan and state.current_step_id:
        current_step = state.plan.get_step(state.current_step_id)
        if current_step:
            # Update step with result
            result_text = str(executor_result) if executor_result else "Step completed"
            state.plan.update_step_status(
                state.current_step_id, StepStatus.COMPLETED, result=result_text
            )

            # Add to execution results
            from haive.agents.planning.p_and_e.models import ExecutionResult

            exec_result = ExecutionResult(
                step_id=state.current_step_id, success=True, output=result_text
            )
            updates["execution_results"] = state.execution_results + [exec_result]

            # Set next step if available
            if state.plan.next_step:
                updates["current_step_id"] = state.plan.next_step.step_id
            else:
                updates["current_step_id"] = None

    return updates


def process_replanner_output(state: PlanExecuteState, replanner_result) -> dict:
    """Process replanner output and update state."""
    updates = {}

    # Check if this is an Act with Response (final answer)
    if hasattr(replanner_result, "action"):
        action = replanner_result.action

        if hasattr(action, "response"):
            # This is a Response - final answer
            updates["final_answer"] = action.response
        elif hasattr(action, "steps"):
            # This is a Plan - continue with new plan
            updates["plan"] = action
            if action.next_step:
                updates["current_step_id"] = action.next_step.step_id
            updates["replan_count"] = state.replan_count + 1

    return updates


# ============================================================================
# MAIN AGENT CREATION FUNCTION
# ============================================================================


def create_proper_plan_execute(
    name: str = "ProperPlanExecute",
    planner_model: str = "gpt-4o-mini",
    executor_model: str = "gpt-4o-mini",
    replanner_model: str = "gpt-4o-mini",
    tools: List = None,
) -> MultiAgentBase:
    """Create proper Plan & Execute agent using existing p_and_e components.

    Args:
        name: Name for the agent system
        planner_model: Model for planning agent
        executor_model: Model for execution agent
        replanner_model: Model for replanning agent
        tools: Tools available to executor

    Returns:
        MultiAgentBase: Complete Plan & Execute system
    """
    if tools is None:
        tools = []

    # Create planner agent using existing prompts and models
    planner = SimpleAgent(
        name="planner",
        model=planner_model,
        system_message=PLANNER_SYSTEM_MESSAGE,
        structured_output_model=Plan,
        post_process_func=process_planner_output,
    )

    # Create executor agent using existing prompts
    executor = ReactAgent(
        name="agent",
        model=executor_model,
        system_message=EXECUTOR_SYSTEM_MESSAGE,
        tools=tools,
        post_process_func=process_executor_output,
    )

    # Create replanner agent using existing prompts and models
    replanner = SimpleAgent(
        name="replan",
        model=replanner_model,
        system_message=REPLAN_SYSTEM_MESSAGE,
        structured_output_model=Act,
        post_process_func=process_replanner_output,
    )

    # Define branches following LangGraph pattern
    branches = [
        # After execution: continue, replan, or end
        (
            executor,
            should_continue,
            {"agent": executor, "replan": replanner, "__end__": "__end__"},
        ),
        # After replanning: continue or end
        (replanner, route_after_replan, {"agent": executor, "__end__": "__end__"}),
    ]

    # Create MultiAgentBase with existing state schema
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


def create_plan_execute_with_search(tools: List = None) -> MultiAgentBase:
    """Create Plan & Execute agent with search tools."""
    if tools is None:
        from haive.tools import duckduckgo_search_tool

        tools = [duckduckgo_search_tool]

    return create_proper_plan_execute(name="PlanExecuteWithSearch", tools=tools)


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Create proper plan execute agent
    agent = create_proper_plan_execute()

    # Test the implementation
    result = agent.run("Research the latest developments in AI and provide a summary")
    print(f"Result: {result}")
