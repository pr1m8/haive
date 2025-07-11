# src/haive/agents/plan_and_execute/agents.py
"""Plan and Execute Agent implementation."""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.tools import BaseTool
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.planning.p_and_e.models import Act, Plan, Response
from haive.agents.planning.p_and_e.prompts import (
    executor_prompt,
    planner_prompt,
    replan_prompt,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState

logger = logging.getLogger(__name__)


def check_plan_complete(state: PlanExecuteState) -> str:
    """Check if plan execution is complete or needs more steps."""
    if not state.plan:
        return "create_plan"

    if state.plan.is_complete:
        return "evaluate_progress"

    if state.plan.has_failures and not state.plan.next_step:
        return "evaluate_progress"

    # Check if we should evaluate periodically
    completed_count = len(state.plan.completed_steps)
    if completed_count > 0 and completed_count % 3 == 0:
        return "evaluate_progress"

    return "execute_step"


def route_after_evaluation(state: PlanExecuteState) -> str:
    """Route based on evaluation decision."""
    # Check if we have a final answer
    if state.final_answer:
        return END

    # Check the last message for Act decision
    if state.messages:
        last_msg = state.messages[-1]
        if hasattr(last_msg, "parsed"):
            act = last_msg.parsed
            if isinstance(act, Act):
                if isinstance(act.action, Response):
                    # Update final answer
                    state.final_answer = act.action.response
                    state.completed_at = datetime.now()
                    return END
                if isinstance(act.action, Plan):
                    return "create_plan"

    # Default to continuing execution
    return "execute_step"


class PlanAndExecuteAgent(Agent):
    """Plan and Execute agent that orchestrates planning, execution, and replanning."""

    # Set schemas
    state_schema: type = Field(default=PlanExecuteState)
    use_prebuilt_base: bool = Field(
        default=True
    )  # Enable schema composition with prebuilt base

    # Tools available to the agent
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools available to this agent"
    )

    def setup_agent(self) -> None:
        """Set up the three engines required for plan-execute-replan workflow."""
        # Create planner engine
        self.engines["planner"] = AugLLMConfig(
            name="planner",
            structured_output_model=Plan,
            structured_output_version="v2",
            prompt_template=planner_prompt,
            partial_variables={"context": ""},
        )

        # Create executor engine with tools
        self.engines["executor"] = AugLLMConfig(
            name="executor",
            prompt_template=executor_prompt,
            tools=self.tools,  # Pass the actual tools to the executor
            partial_variables={
                "plan_status": "",
                "current_step": "",
                "previous_results": "",
            },
        )

        # Create replanner engine
        self.engines["replanner"] = AugLLMConfig(
            name="replanner",
            structured_output_model=Act,
            structured_output_version="v2",
            prompt_template=replan_prompt,
            partial_variables={
                "objective": "",
                "plan_progress": "",
                "execution_results": "",
            },
        )

    def build_graph(self) -> BaseGraph:
        """Build the plan-execute-replan graph."""
        graph = BaseGraph(name=self.name)

        # Add planner node
        planner_node = EngineNodeConfig(
            name="create_plan", engine=self.engines["planner"]
        )
        graph.add_node("create_plan", planner_node)
        graph.add_edge(START, "create_plan")

        # Add executor node
        executor_node = EngineNodeConfig(
            name="execute_step", engine=self.engines["executor"]
        )
        graph.add_node("execute_step", executor_node)

        # Add evaluation/replan node
        replan_node = EngineNodeConfig(
            name="evaluate_progress", engine=self.engines["replanner"]
        )
        graph.add_node("evaluate_progress", replan_node)

        # Add edges
        graph.add_edge("create_plan", "execute_step")

        # Conditional routing after execution
        graph.add_conditional_edges(
            "execute_step",
            check_plan_complete,
            {
                "execute_step": "execute_step",
                "evaluate_progress": "evaluate_progress",
                "create_plan": "create_plan",
            },
        )

        # Conditional routing after evaluation
        graph.add_conditional_edges(
            "evaluate_progress",
            route_after_evaluation,
            {"execute_step": "execute_step", "create_plan": "create_plan", END: END},
        )

        return graph
