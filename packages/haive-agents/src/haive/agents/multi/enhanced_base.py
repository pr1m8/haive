"""Enhanced Multi-Agent Base for flexible agent orchestration.

This module provides an improved multi-agent base that leverages the advanced
conditional edges functionality from base_graph2.py while keeping the API simple
and similar to how it works in simple agents.

The MultiAgentBase class enables sophisticated agent orchestration patterns including:

- **Sequential Execution**: Simple chain of agents in order
- **Conditional Branching**: Dynamic routing based on state conditions
- **Plan-Execute-Replan**: Complex workflows with feedback loops
- **Parallel Schema Composition**: Isolated namespaces for agent fields

The system uses Pydantic fields for configuration and supports both simple
edge definitions and complex conditional routing with proper error handling
and state management.

Example:
    Sequential multi-agent system::

        agents = [planner, executor, validator]
        multi_agent = MultiAgentBase(
            agents=agents,
            name="sequential_pipeline"
        )

    Conditional branching system::

        def route_condition(state) -> str:
            return "success" if state.validation_passed else "retry"

        multi_agent = MultiAgentBase(
            agents=[processor, validator, retrier],
            branches=[
                (validator, route_condition, {
                    "success": "END",
                    "retry": retrier
                })
            ]
        )

See Also:
    :class:`haive.agents.planning.plan_and_execute.PlanAndExecuteAgent`: Complete Plan and Execute implementation
    :class:`haive.core.graph.state_graph.base_graph2.BaseGraph`: Underlying graph implementation
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union

from haive.core.graph.node.agent_node import AgentNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode
from haive.core.schema.state_schema import StateSchema
from langgraph.graph import END, START
from pydantic import BaseModel, Field, field_validator, validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class AgentList(list):
    """List of agents with dict-like access by name."""

    def __getitem__(self, key):
        """Get agent by index (int) or name (str)."""
        if isinstance(key, str):
            # Dict-like access by name
            for agent in self:
                if agent.name == key:
                    return agent
            raise KeyError(f"Agent '{key}' not found")
        # Normal list access by index
        return super().__getitem__(key)

    def __contains__(self, key):
        """Check if agent exists by name (str) or object (Agent)."""
        if isinstance(key, str):
            return any(agent.name == key for agent in self)
        return super().__contains__(key)

    def get(self, key: str, default=None):
        """Get agent by name with optional default."""
        try:
            return self[key]
        except KeyError:
            return default


class MultiAgentBase(Agent):
    """Multi-agent base with simple API for advanced orchestration.

    This class provides a flexible foundation for building complex multi-agent systems
    with conditional routing, parallel schema composition, and sophisticated workflow
    management. It extends the base Agent class while orchestrating multiple sub-agents.

    The system supports various orchestration patterns:

    - **Sequential**: Agents execute in order (default behavior)
    - **Conditional**: Dynamic routing based on state conditions
    - **Parallel Schema**: Isolated field namespaces for complex state management
    - **Custom Workflows**: User-defined workflow nodes for state processing

    Attributes:
        agents (List[Agent]): List of agents to orchestrate
        branches (Optional[List[tuple]]): Conditional routing branches
        state_schema_override (Optional[Type[StateSchema]]): Override for state schema
        schema_build_mode (BuildMode): Schema composition mode (SEQUENCE/PARALLEL)
        schema_separation (str): Field separation strategy for schemas
        include_meta (bool): Include meta state for coordination
        entry_points (Optional[List[Union[str, Agent]]]): Entry points for execution
        finish_points (Optional[List[Union[str, Agent]]]): Finish points for execution
        workflow_nodes (Optional[Dict[str, Callable]]): Custom workflow nodes
        create_missing_nodes (bool): Auto-create missing destination nodes

    Example:
        Sequential execution (default)::

            multi_agent = MultiAgentBase(
                agents=[agent1, agent2, agent3],
                name="sequential_pipeline"
            )

        Conditional branching::

            def route_condition(state) -> str:
                return "success" if state.is_valid else "retry"

            multi_agent = MultiAgentBase(
                agents=[processor, validator, retrier],
                branches=[
                    (validator, route_condition, {
                        "success": "END",
                        "retry": retrier
                    })
                ]
            )

        Parallel schema composition::

            multi_agent = MultiAgentBase(
                agents=[planner, executor, replanner],
                schema_build_mode=BuildMode.PARALLEL,
                branches=[
                    (executor, route_after_execution, {
                        "continue": executor,
                        "replan": replanner
                    })
                ]
            )

    Note:
        The class automatically handles schema composition, node creation, and edge
        routing based on the provided configuration. Custom workflow nodes can be
        added for complex state processing between agent executions.
    """

    # Core configuration
    agents: AgentList = Field(
        default_factory=AgentList, description="List of agents to orchestrate"
    )
    branches: list[tuple] | None = Field(
        default=None, description="Conditional routing branches"
    )
    state_schema_override: type[StateSchema] | None = Field(
        default=None, description="Optional state schema override"
    )
    schema_build_mode: BuildMode = Field(
        default=BuildMode.SEQUENCE, description="Schema composition build mode"
    )
    schema_separation: str = Field(
        default="smart", description="Schema field separation strategy"
    )
    include_meta: bool = Field(
        default=True, description="Include meta state for coordination"
    )
    entry_points: list[str | Agent] | None = Field(
        default=None, description="Entry points for the multi-agent system"
    )
    finish_points: list[str | Agent] | None = Field(
        default=None, description="Finish points for the multi-agent system"
    )
    workflow_nodes: dict[str, Callable] | None = Field(
        default_factory=dict, description="Custom workflow nodes"
    )
    create_missing_nodes: bool = Field(
        default=False, description="Auto-create missing destination nodes"
    )

    # State tracking
    agent_node_mapping: dict[str, str] = Field(default_factory=dict)
    conditional_edges: list[dict[str, Any]] = Field(default_factory=list)

    @field_validator("agents", mode="before")
    @classmethod
    def convert_to_agent_list(cls, v):
        """Convert regular list to AgentList."""
        if isinstance(v, list) and not isinstance(v, AgentList):
            return AgentList(v)
        return v

    def _auto_detect_agents(self) -> AgentList:
        """Auto-detect agents from individual agent fields."""
        detected_agents = AgentList()

        # Get all fields that are Agent instances
        for _field_name, field_value in self.__dict__.items():
            if isinstance(field_value, Agent):
                detected_agents.append(field_value)

        return detected_agents

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)

        # Auto-compose agents from individual agent fields if not provided
        if not self.agents:
            self.agents = self._auto_detect_agents()

        # Validate agents
        if not self.agents:
            raise ValueError("MultiAgentBase requires at least one agent")

        # Set up state schema
        if self.state_schema_override:
            self.state_schema = self.state_schema_override
        else:
            self.state_schema = AgentSchemaComposer.from_agents(
                agents=self.agents,
                name=f"{self.__class__.__name__}State",
                include_meta=self.include_meta,
                separation=self.schema_separation,
                build_mode=self.schema_build_mode,
            )

        # Set input/output schemas
        if self.state_schema:
            self.input_schema = self.state_schema.derive_input_schema()
            self.output_schema = self.state_schema.derive_output_schema()

        # Auto-detect entry points if not specified
        if not self.entry_points and self.agents:
            self.entry_points = [self.agents[0]]  # Default to first agent

        # Auto-detect finish points if not specified (for sequential flow)
        if not self.finish_points and not self.branches and len(self.agents) > 0:
            self.finish_points = [
                self.agents[-1]
            ]  # Default to last agent for sequential

        # Process branches if provided
        if self.branches:
            for branch in self.branches:
                if len(branch) == 3:
                    source_agent, condition, destinations = branch
                    self.add_conditional_edges(source_agent, condition, destinations)
                elif len(branch) == 4:
                    source_agent, condition, destinations, default = branch
                    self.add_conditional_edges(
                        source_agent, condition, destinations, default
                    )

    def add_conditional_edges(
        self,
        source_agent: str | Agent,
        condition: Callable[[Any], Any],
        destinations: str | list[str] | dict[Any, str | Agent],
        default: str | Agent | None = END,
    ) -> None:
        """Add conditional edges between agents with simple API.

        This method provides a simple interface for adding conditional routing between
        agents, similar to the API used in simple agents. The conditional edges are
        stored and processed during graph building to create the actual routing logic.

        Args:
            source_agent: Source agent (name or Agent object) from which to route
            condition: Function that takes state and returns routing key for destinations
            destinations: Target destinations based on condition result. Can be:
                - str: Single destination
                - List[str]: Multiple destinations (condition returns index)
                - Dict[Any, Union[str, Agent]]: Mapping of condition results to destinations
            default: Default destination if no condition matches (defaults to END)

        Example:
            Simple conditional routing::

                def route_condition(state):
                    return "success" if state.is_valid else "retry"

                multi_agent.add_conditional_edges(
                    source_agent=validator,
                    condition=route_condition,
                    destinations={
                        "success": "END",
                        "retry": processor
                    }
                )

        Note:
            The conditional edges are stored and processed during graph building.
            The actual routing logic is implemented using the underlying BaseGraph
            conditional edges functionality.
        """
        # Store for later use in build_graph
        self.conditional_edges.append(
            {
                "source_agent": source_agent,
                "condition": condition,
                "destinations": destinations,
                "default": default,
            }
        )

    def add_edge(self, source_agent: str | Agent, target_agent: str | Agent) -> None:
        """Add a simple edge between agents.

        Args:
            source_agent: Source agent
            target_agent: Target agent
        """
        self.conditional_edges.append(
            {
                "source_agent": source_agent,
                "condition": None,  # No condition = direct edge
                "destinations": target_agent,
                "default": None,
            }
        )

    def _get_agent_node_name(self, agent: str | Agent) -> str:
        """Get the node name for an agent."""
        if isinstance(agent, str):
            if agent in [START, END, "START", "END"]:
                return agent

            # Find agent by name
            for a in self.agents:
                if getattr(a, "name", None) == agent:
                    return self._get_unique_node_name(agent)
            return agent  # Assume it's already a node name

        if isinstance(agent, Agent):
            agent_name = getattr(agent, "name", agent.__class__.__name__)
            return self._get_unique_node_name(agent_name)

        return str(agent)

    def _get_unique_node_name(self, base_name: str) -> str:
        """Ensure unique node names."""
        if base_name not in self.agent_node_mapping:
            node_name = base_name
            counter = 1
            while node_name in self.agent_node_mapping.values():
                node_name = f"{base_name}_{counter}"
                counter += 1
            self.agent_node_mapping[base_name] = node_name

        return self.agent_node_mapping[base_name]

    def _normalize_destination(self, dest: str | Agent) -> str:
        """Normalize destination to node name."""
        if dest in (END, "END"):
            return END
        if dest in (START, "START"):
            return START
        return self._get_agent_node_name(dest)

    def _serialize_engine_for_state(self, engine: Any) -> dict[str, Any]:
        """Serialize an engine to a dict that can be stored in state and serialized by msgpack.

        The agent node can model validate this dict back to an engine if needed.
        """
        if not hasattr(engine, "model_dump"):
            # Not a Pydantic model, try to convert to dict
            return {"name": str(engine), "type": "unknown"}

        try:
            # Get base serialization with mode='json' to handle SecretStr and other special types
            engine_dict = engine.model_dump(
                mode="json",  # This converts SecretStr and other non-JSON types
                exclude={"input_schema", "output_schema"},  # These are already excluded
                exclude_none=True,
                exclude_unset=True,  # Don't include unset fields
            )

            # Handle fields that contain Pydantic classes or other non-serializable objects
            # These fields typically contain ModelMetaclass objects
            fields_to_clean = [
                "tools",
                "schemas",
                "pydantic_tools",
                "structured_output_model",
            ]

            for field in fields_to_clean:
                if field in engine_dict:
                    value = engine_dict[field]
                    if value is None:
                        continue
                    if field == "structured_output_model":
                        # Convert Pydantic model class to string representation
                        if hasattr(value, "__name__"):
                            engine_dict[field] = f"<PydanticModel:{value.__name__}>"
                        else:
                            engine_dict[field] = None
                    elif isinstance(value, list):
                        # Convert list of Pydantic classes to string representations
                        cleaned_list = []
                        for item in value:
                            if hasattr(item, "__name__"):
                                cleaned_list.append(f"<PydanticModel:{item.__name__}>")
                            elif hasattr(item, "name"):
                                cleaned_list.append({"name": item.name, "type": "tool"})
                            else:
                                # Skip non-serializable items
                                continue
                        engine_dict[field] = cleaned_list
                    else:
                        # For other types, remove them
                        engine_dict[field] = None

            return engine_dict

        except Exception as e:
            logger.warning(
                f"Failed to serialize engine {getattr(engine, 'name', 'unknown')}: {e}"
            )
            # Return minimal engine info
            return {
                "id": getattr(engine, "id", str(id(engine))),
                "name": getattr(engine, "name", "unknown"),
                "engine_type": str(getattr(engine, "engine_type", "unknown")),
            }

    def _prepare_input(self, input_data: Any) -> Any:
        """Prepare input data for the multi-agent system.

        For PARALLEL mode, we don't pass engines through state to avoid
        serialization issues. Each agent will use its own engines.
        """
        # Call parent's _prepare_input first
        prepared = super()._prepare_input(input_data)

        # Ensure prepared is a dict
        if hasattr(prepared, "model_dump"):
            prepared_dict = prepared.model_dump()
        elif isinstance(prepared, dict):
            prepared_dict = prepared
        else:
            prepared_dict = {"messages": []}

        # For PARALLEL mode, explicitly remove engine and engines fields
        # to avoid abstract class instantiation issues
        if self.schema_build_mode == BuildMode.PARALLEL:
            # Remove engine fields that would cause deserialization issues
            prepared_dict.pop("engine", None)
            prepared_dict.pop("engines", None)
            logger.debug(
                "Removed engine fields from state for PARALLEL mode to avoid serialization issues"
            )

        # Convert back to state schema if needed
        if self.state_schema and not isinstance(prepared, self.state_schema):
            try:
                return self.state_schema(**prepared_dict)
            except Exception as e:
                logger.warning(f"Could not convert to state schema: {e}")
                return prepared_dict

        return prepared

    def build_graph(self) -> BaseGraph:
        """Build the execution graph using the configured agents and routing logic.

        This method creates the complete execution graph by:

        1. Adding all agents as nodes with proper configuration
        2. Adding custom workflow nodes for state processing
        3. Setting up entry points for execution flow
        4. Processing conditional edges for dynamic routing
        5. Creating sequential flow if no explicit routing is defined
        6. Configuring finish points for completion

        The graph building process handles both simple sequential execution and
        complex conditional routing patterns, automatically normalizing destinations
        and creating the appropriate edge types.

        Returns:
            BaseGraph: Compiled graph ready for execution with all nodes, edges,
                and routing logic properly configured

        Note:
            This method is called automatically during agent execution setup.
            The resulting graph uses the advanced BaseGraph functionality for
            conditional edges and state management.
        """
        graph = BaseGraph(name=self.name)

        # Add all agents as nodes
        for agent in self.agents:
            node_name = self._get_agent_node_name(agent)
            graph.add_node(node_name, AgentNodeConfig(name=node_name, agent=agent))

        # Add workflow nodes
        for node_name, function in self.workflow_nodes.items():
            graph.add_node(node_name, function)

        # Set up entry points
        for entry_agent in self.entry_points:
            entry_node = self._get_agent_node_name(entry_agent)
            graph.add_edge(START, entry_node)

        # Add edges based on stored conditional edges
        for edge_config in self.conditional_edges:
            source_node = self._get_agent_node_name(edge_config["source_agent"])

            if edge_config["condition"] is None:
                # Direct edge
                target_node = self._normalize_destination(edge_config["destinations"])
                graph.add_edge(source_node, target_node)
            else:
                # Conditional edge - use base_graph2's advanced functionality
                destinations = edge_config["destinations"]

                # Normalize destinations based on type
                if isinstance(destinations, dict):
                    normalized_destinations = {}
                    for key, dest in destinations.items():
                        normalized_destinations[key] = self._normalize_destination(dest)
                elif isinstance(destinations, list):
                    normalized_destinations = [
                        self._normalize_destination(dest) for dest in destinations
                    ]
                else:
                    normalized_destinations = self._normalize_destination(destinations)

                # Normalize default
                default_dest = None
                if edge_config["default"]:
                    default_dest = self._normalize_destination(edge_config["default"])

                # Use base_graph2's add_conditional_edges
                graph.add_conditional_edges(
                    source_node=source_node,
                    condition=edge_config["condition"],
                    destinations=normalized_destinations,
                    default=default_dest,
                    create_missing_nodes=self.create_missing_nodes,
                )

        # Create sequential flow for agents without explicit branches
        if len(self.agents) > 1:
            # Track which agents have explicit outgoing edges
            agents_with_edges = set()
            for edge_config in self.conditional_edges:
                agents_with_edges.add(
                    self._get_agent_node_name(edge_config["source_agent"])
                )

            # Add sequential edges for agents without explicit routing
            for i in range(len(self.agents) - 1):
                current_node = self._get_agent_node_name(self.agents[i])
                next_node = self._get_agent_node_name(self.agents[i + 1])

                # Only add sequential edge if no explicit edge exists
                if current_node not in agents_with_edges:
                    graph.add_edge(current_node, next_node)

        # Set up finish points
        if self.finish_points:
            for finish_agent in self.finish_points:
                finish_node = self._get_agent_node_name(finish_agent)
                graph.add_edge(finish_node, END)

        return graph


# Convenience functions for common patterns


def create_sequential_multi_agent(
    agents: list[Agent],
    name: str = "Sequential Multi-Agent",
    state_schema: type[StateSchema] | None = None,
    **kwargs,
) -> MultiAgentBase:
    """Create a simple sequential multi-agent system.

    This convenience function creates a MultiAgentBase configured for sequential
    execution where agents run in the order provided. The system uses SEQUENCE
    schema build mode for unified state management.

    Args:
        agents: List of agents to execute in sequence
        name: Name for the multi-agent system
        state_schema: Optional state schema override
        **kwargs: Additional configuration options for MultiAgentBase

    Returns:
        MultiAgentBase: Configured sequential multi-agent system

    Example:
        Create a simple pipeline::

            agents = [preprocessor, analyzer, summarizer]
            pipeline = create_sequential_multi_agent(
                agents=agents,
                name="analysis_pipeline"
            )
    """
    return MultiAgentBase(
        agents=agents,
        name=name,
        state_schema_override=state_schema,
        schema_build_mode=BuildMode.SEQUENCE,
        **kwargs,
    )


def create_branching_multi_agent(
    agents: list[Agent],
    branches: list[tuple],
    name: str = "Branching Multi-Agent",
    state_schema: type[StateSchema] | None = None,
    **kwargs,
) -> MultiAgentBase:
    """Create a multi-agent system with conditional branching.

    This convenience function creates a MultiAgentBase configured for conditional
    execution with branching logic. The system uses SEQUENCE schema build mode
    by default for unified state management.

    Args:
        agents: List of agents involved in the branching system
        branches: List of branch tuples defining conditional routing
        name: Name for the multi-agent system
        state_schema: Optional state schema override
        **kwargs: Additional configuration options for MultiAgentBase

    Returns:
        MultiAgentBase: Configured branching multi-agent system

    Example:
        Create a system with conditional routing::

            def route_condition(state):
                return "success" if state.is_valid else "retry"

            branches = [
                (validator, route_condition, {
                    "success": "END",
                    "retry": processor
                })
            ]

            system = create_branching_multi_agent(
                agents=[processor, validator],
                branches=branches,
                name="validation_system"
            )
    """
    return MultiAgentBase(
        agents=agents,
        branches=branches,
        name=name,
        state_schema_override=state_schema,
        schema_build_mode=BuildMode.SEQUENCE,
        **kwargs,
    )


def create_plan_execute_multi_agent(
    planner_agent: Agent,
    executor_agent: Agent,
    replanner_agent: Agent,
    name: str = "Plan and Execute System",
    state_schema: type[StateSchema] | None = None,
    schema_build_mode: BuildMode = BuildMode.PARALLEL,
    **kwargs,
) -> MultiAgentBase:
    """Create a Plan and Execute multi-agent system with proper routing."""
    # Import PlanExecuteState here to avoid circular imports
    from haive.agents.planning.p_and_e.state import PlanExecuteState

    # Default to PlanExecuteState if no schema provided
    if state_schema is None:
        state_schema = PlanExecuteState

    def route_after_execution(state) -> str:
        """Route after execution based on plan status."""
        if hasattr(state, "plan") and state.plan:
            if state.plan.is_complete:
                return "replanner"
            return "executor"
        return "replanner"

    def route_after_replan(state) -> str:
        """Route after replanning decision."""
        if hasattr(state, "final_answer") and state.final_answer:
            return END
        if hasattr(state, "plan") and state.plan:
            return "executor"
        return END

    # Define branches for the plan and execute pattern
    branches = [
        (
            executor_agent,
            route_after_execution,
            {"executor": executor_agent, "replanner": replanner_agent},
        ),
        (replanner_agent, route_after_replan, {"executor": executor_agent, END: END}),
    ]

    # Create the system with branches
    return MultiAgentBase(
        agents=[planner_agent, executor_agent, replanner_agent],
        branches=branches,
        name=name,
        state_schema_override=state_schema,
        schema_build_mode=schema_build_mode,
        **kwargs,
    )
