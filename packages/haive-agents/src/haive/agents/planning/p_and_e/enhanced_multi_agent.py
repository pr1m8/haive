"""
Enhanced Multi-Agent Base for Plan and Execute patterns.

This module provides an enhanced version of MultiAgent that allows for cleaner
configuration with agents, state schema, and branches passed directly.
"""

import logging
from abc import abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from pydantic import Field

from haive.agents.multi.base import ExecutionMode, MultiAgent

logger = logging.getLogger(__name__)


class EnhancedMultiAgent(MultiAgent):
    """Enhanced MultiAgent that accepts agents, state schema, and branches directly."""

    def __init__(
        self,
        agents: List[Any],
        state_schema: Optional[Type[StateSchema]] = None,
        branches: Optional[Dict[str, Dict[str, Any]]] = None,
        schema_composition_method: str = "smart",
        execution_mode: ExecutionMode = ExecutionMode.CONDITIONAL,
        **kwargs,
    ):
        """
        Initialize enhanced multi-agent with direct configuration.

        Args:
            agents: List of agents to orchestrate
            state_schema: Optional state schema override
            branches: Branch configuration for conditional routing
            schema_composition_method: How to compose schemas ("smart", "shared", "namespaced")
            execution_mode: Execution pattern
            **kwargs: Additional MultiAgent arguments
        """

        # Store schema override
        self._state_schema_override = state_schema

        # Set schema separation strategy
        kwargs["schema_separation"] = schema_composition_method

        # Set branches
        if branches:
            kwargs["branches"] = branches

        # Initialize with agents and execution mode
        super().__init__(agents=agents, execution_mode=execution_mode, **kwargs)

    def setup_multi_agent(self) -> "EnhancedMultiAgent":
        """Override to use state schema override if provided."""

        if self._state_schema_override:
            # Use provided state schema instead of composing
            self.state_schema = self._state_schema_override
            logger.info(f"Using provided state schema: {self.state_schema.__name__}")
        else:
            # Use parent's schema composition
            build_mode = self._get_build_mode()

            from haive.core.schema.agent_schema_composer import AgentSchemaComposer

            self.state_schema = AgentSchemaComposer.from_agents(
                agents=list(self.agents),
                name=f"{self.__class__.__name__}State",
                include_meta=self.include_meta,
                separation=self.schema_separation,
                build_mode=build_mode,
            )
            logger.info(f"Composed state schema: {self.state_schema.__name__}")

        # Store private schemas for each agent
        for agent in self.agents:
            agent_id = getattr(agent, "id", agent.name)
            if hasattr(agent, "state_schema") and agent.state_schema:
                self._agent_private_states[agent_id] = agent.state_schema

        # Set input/output schemas
        self._setup_io_schemas()

        return self


class PlanAndExecuteMultiAgent(EnhancedMultiAgent):
    """Plan and Execute multi-agent using enhanced base."""

    def __init__(
        self,
        agents: List[Any],
        state_schema: Optional[Type[StateSchema]] = None,
        **kwargs,
    ):
        """
        Initialize Plan and Execute multi-agent.

        Args:
            agents: List of [planner, executor, replanner] agents
            state_schema: Optional state schema (defaults to PlanExecuteState)
            **kwargs: Additional arguments
        """

        # Default state schema
        if state_schema is None:
            from haive.agents.planning.p_and_e.state import PlanExecuteState

            state_schema = PlanExecuteState

        # Define Plan & Execute branches
        branches = {
            "process_execution": {
                "condition": self._route_after_execution,
                "destinations": {
                    "continue": "prepare_execution",
                    "replan": "prepare_replan",
                    "complete": "END",
                },
            },
            "process_replan": {
                "condition": self._route_after_replan,
                "destinations": {
                    "continue": "prepare_execution",
                    "new_plan": self._get_agent_node_name(agents[0]),  # planner
                    "complete": "END",
                },
            },
        }

        # Initialize enhanced multi-agent
        super().__init__(
            agents=agents,
            state_schema=state_schema,
            branches=branches,
            execution_mode=ExecutionMode.CONDITIONAL,
            **kwargs,
        )

    def build_custom_graph(self, graph: BaseGraph) -> BaseGraph:
        """Build the Plan and Execute workflow graph."""

        # Ensure we have exactly 3 agents
        if len(self.agents) != 3:
            raise ValueError(
                "PlanAndExecuteMultiAgent requires exactly 3 agents: [planner, executor, replanner]"
            )

        # Get agent node names
        planner_node = self._get_agent_node_name(self.agents[0])
        executor_node = self._get_agent_node_name(self.agents[1])
        replanner_node = self._get_agent_node_name(self.agents[2])

        # Add agents as nodes
        from haive.core.graph.node.agent_node import AgentNodeConfig

        for agent in self.agents:
            node_name = self._get_agent_node_name(agent)
            graph.add_node(node_name, AgentNodeConfig(name=node_name, agent=agent))

        # Add workflow logic nodes
        graph.add_node("prepare_execution", self._prepare_execution_step)
        graph.add_node("process_execution", self._process_execution_result)
        graph.add_node("prepare_replan", self._prepare_replan_step)
        graph.add_node("process_replan", self._process_replan_decision)

        # Define the workflow
        from langgraph.graph import END, START

        graph.add_edge(START, planner_node)
        graph.add_edge(planner_node, "prepare_execution")
        graph.add_edge("prepare_execution", executor_node)
        graph.add_edge(executor_node, "process_execution")

        # Conditional routing after execution
        branch_config = self.branches["process_execution"]
        graph.add_conditional_edges(
            "process_execution",
            branch_config["condition"],
            branch_config["destinations"],
        )

        # Replan workflow
        graph.add_edge("prepare_replan", replanner_node)
        graph.add_edge(replanner_node, "process_replan")

        # Conditional routing after replanning
        branch_config = self.branches["process_replan"]
        graph.add_conditional_edges(
            "process_replan", branch_config["condition"], branch_config["destinations"]
        )

        return graph

    # Workflow logic methods - these would be implemented based on your Plan & Execute logic
    def _prepare_execution_step(self, state: Any):
        """Prepare the next execution step."""
        # Your implementation here
        pass

    def _process_execution_result(self, state: Any):
        """Process the execution result and update the plan."""
        # Your implementation here
        pass

    def _prepare_replan_step(self, state: Any):
        """Prepare for replanning."""
        # Your implementation here
        pass

    def _process_replan_decision(self, state: Any):
        """Process the replanning decision."""
        # Your implementation here
        pass

    def _route_after_execution(self, state: Any) -> str:
        """Route after execution based on plan status."""
        # Your routing logic here
        return "complete"

    def _route_after_replan(self, state: Any) -> str:
        """Route after replanning decision."""
        # Your routing logic here
        return "complete"
