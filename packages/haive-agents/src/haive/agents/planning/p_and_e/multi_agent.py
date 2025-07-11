"""Plan and Execute Multi-Agent System using Configurable Base.

This module demonstrates how to use the configurable multi-agent base
for building Plan and Execute workflows with branches.
"""

import logging
from datetime import datetime
from typing import Any, List

from langgraph.graph import END
from langgraph.types import Command

from haive.agents.multi.configurable_base import (
    AgentBranch,
    ConfigurableMultiAgent,
    WorkflowStep,
)
from haive.agents.planning.p_and_e.models import Act, ExecutionResult, Plan, Response
from haive.agents.planning.p_and_e.state import PlanExecuteState

logger = logging.getLogger(__name__)


class PlanAndExecuteAgent(ConfigurableMultiAgent):
    """Plan and Execute multi-agent using the configurable base."""

    def __init__(
        self,
        agents: list[Any],  # [planner, executor, replanner]
        branches: list[AgentBranch] | None = None,
        state_schema=None,
        **kwargs
    ):
        """Initialize Plan and Execute multi-agent.

        Args:
            agents: List of [planner, executor, replanner] agents
            branches: Optional custom branches (defaults to Plan & Execute workflow)
            state_schema: Optional state schema override
            **kwargs: Additional arguments
        """
        if len(agents) != 3:
            raise ValueError(
                "PlanAndExecuteAgent requires exactly 3 agents: [planner, executor, replanner]"
            )

        planner, executor, replanner = agents

        # Use PlanExecuteState as default
        if state_schema is None:
            state_schema = PlanExecuteState

        # Define default Plan & Execute workflow steps if no custom branches
        if branches is None:
            workflow_steps = [
                WorkflowStep(
                    "prepare_execution",
                    self._prepare_execution_step,
                    inputs=[planner],
                    outputs=[executor],
                ),
                WorkflowStep(
                    "process_execution",
                    self._process_execution_result,
                    inputs=[executor],
                    outputs=[],  # Connects via branches
                ),
                WorkflowStep(
                    "prepare_replan",
                    self._prepare_replan_step,
                    inputs=[],
                    outputs=[replanner],
                ),
                WorkflowStep(
                    "process_replan",
                    self._process_replan_decision,
                    inputs=[replanner],
                    outputs=[],  # Connects via branches
                ),
            ]

            # Define default Plan & Execute branches
            branches = [
                # Branch after execution processing
                AgentBranch(
                    from_agent="process_execution",
                    condition=self._route_after_execution,
                    destinations={
                        "continue": "prepare_execution",
                        "replan": "prepare_replan",
                        "complete": END,
                    },
                ),
                # Branch after replan processing
                AgentBranch(
                    from_agent="process_replan",
                    condition=self._route_after_replan,
                    destinations={
                        "continue": "prepare_execution",
                        "new_plan": planner,
                        "complete": END,
                    },
                ),
            ]
        else:
            workflow_steps = []

        # Initialize with configuration
        super().__init__(
            agents=agents,
            branches=branches,
            workflow_steps=workflow_steps,
            state_schema_override=state_schema,
            start_agent=planner,
            **kwargs
        )

    # Workflow logic methods
    def _prepare_execution_step(self, state: PlanExecuteState) -> Command:
        """Prepare the next execution step."""
        if not state.plan:
            return Command(
                update={"errors": [*state.errors, "No plan available for execution"]}
            )

        next_step = state.plan.next_step
        if not next_step:
            return Command(update={"current_step_id": None})

        state.plan.update_step_status(next_step.step_id, "in_progress")

        return Command(
            update={"current_step_id": next_step.step_id, "plan": state.plan}
        )

    def _process_execution_result(self, state: PlanExecuteState) -> Command:
        """Process the execution result and update the plan."""
        if not state.current_step_id or not state.plan:
            return Command(update={})

        if not state.messages:
            return Command(
                update={"errors": [*state.errors, "No execution result received"]}
            )

        last_message = state.messages[-1]
        result_content = getattr(last_message, "content", "")

        execution_result = ExecutionResult(
            step_id=state.current_step_id,
            success=True,
            output=result_content,
            execution_time=1.0,
        )

        state.plan.update_step_status(
            state.current_step_id, "completed", result=result_content
        )

        return Command(
            update={
                "execution_results": [*state.execution_results, execution_result],
                "plan": state.plan,
                "current_step_id": None,
            }
        )

    def _prepare_replan_step(self, state: PlanExecuteState) -> Command:
        """Prepare for replanning."""
        return Command(update={})

    def _process_replan_decision(self, state: PlanExecuteState) -> Command:
        """Process the replanning decision."""
        if not state.messages:
            return Command(update={})

        last_message = state.messages[-1]

        if hasattr(last_message, "parsed") and isinstance(last_message.parsed, Act):
            act = last_message.parsed

            if isinstance(act.action, Response):
                return Command(
                    update={
                        "final_answer": act.action.response,
                        "completed_at": datetime.now(),
                    }
                )

            if isinstance(act.action, Plan):
                return Command(
                    update={
                        "plan": act.action,
                        "replan_count": state.replan_count + 1,
                        "replan_history": [
                            *state.replan_history,
                            {
                                "timestamp": datetime.now().isoformat(),
                                "reason": "New plan from replanner",
                                "old_plan_progress": (
                                    state.plan.progress_percentage if state.plan else 0
                                ),
                            },
                        ],
                    }
                )

        return Command(update={})

    # Routing logic methods
    def _route_after_execution(self, state: PlanExecuteState) -> str:
        """Route after execution based on plan status."""
        if not state.plan:
            return "complete"

        if state.plan.is_complete:
            return "complete"

        if state.should_replan:
            return "replan"

        return "continue"

    def _route_after_replan(self, state: PlanExecuteState) -> str:
        """Route after replanning decision."""
        if state.final_answer:
            return "complete"

        if state.plan and state.replan_count > 0:
            replan_history = state.replan_history or []
            if (
                replan_history
                and replan_history[-1].get("reason") == "New plan from replanner"
            ):
                return "new_plan"

        return "continue"


# Example usage patterns:


def create_plan_execute_system(planner_agent, executor_agent, replanner_agent):
    """Create Plan and Execute system with default workflow."""
    return PlanAndExecuteAgent(
        agents=[planner_agent, executor_agent, replanner_agent],
        name="Plan and Execute System",
    )


def create_custom_plan_execute_system(
    planner_agent, executor_agent, replanner_agent, custom_branches: list[AgentBranch]
):
    """Create Plan and Execute system with custom branches."""
    return PlanAndExecuteAgent(
        agents=[planner_agent, executor_agent, replanner_agent],
        branches=custom_branches,
        name="Custom Plan and Execute System",
    )


def create_simple_sequential_system(agents):
    """Create simple sequential multi-agent system."""
    from haive.agents.multi.configurable_base import create_sequential_multi_agent

    return create_sequential_multi_agent(agents=agents, name="Sequential Agent System")


def create_custom_branching_system(agents, branches):
    """Create custom branching multi-agent system."""
    from haive.agents.multi.configurable_base import create_branching_multi_agent

    return create_branching_multi_agent(
        agents=agents, branches=branches, name="Custom Branching System"
    )
