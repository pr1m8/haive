# haive/agents/multi/agent.py

"""Advanced multi-agent class for the Haive framework.

This module provides a comprehensive implementation of multi-agent systems,
enabling seamless composition of multiple agents with various coordination patterns.
"""

import logging
from typing import Any, Literal

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.state_graph.components.node import Node
from haive.core.schema.agent_schema_composer import AgentSchemaComposer
from langgraph.graph import END
from langgraph.graph.graph import CompiledGraph
from langgraph.types import Command
from pydantic import Field, PrivateAttr, model_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


class MultiAgent(Agent):
    """Advanced multi-agent system with flexible coordination patterns.

    This class enables the seamless composition of multiple agents into
    coordinated systems with various execution patterns and state sharing
    capabilities. It leverages the AgentNode and AgentSchemaComposer to
    properly handle agent interactions and state management.

    Key features:
    - Multiple coordination modes (sequential, parallel, supervisor, custom)
    - Smart state schema composition with proper field handling
    - Automatic engine I/O mapping preservation
    - Agent transitions based on agent decisions
    - Meta-agent capabilities for self-modification

    Example:
        ```python
        # Create multi-agent with two component agents
        multi = MultiAgent(
            agents=[react_agent, simple_agent],
            coordination_mode="sequential"
        )

        # Run the multi-agent system
        result = multi.run({"messages": [HumanMessage(content="Hello")]})
        ```
    """

    # Multi-agent specific fields
    agents: dict[str, Agent] = Field(
        default_factory=dict,
        description="Dictionary of sub-agents in this multi-agent system",
    )

    coordination_mode: Literal[
        "sequential", "parallel", "supervisor", "swarm", "custom"
    ] = Field(default="sequential", description="Coordination mode for the agents")

    separation_strategy: Literal["namespaced", "smart", "shared"] = Field(
        default="smart", description="Schema field separation strategy"
    )

    enable_meta: bool = Field(
        default=False,
        description="Enable meta-agent capabilities (graph self-modification)",
    )

    # Agent execution configuration
    max_iterations: int = Field(
        default=10, description="Maximum iterations for iterative patterns"
    )

    allow_agent_communication: bool = Field(
        default=True, description="Allow agents to communicate directly"
    )

    share_message_history: bool = Field(
        default=True, description="Share message history between agents"
    )

    # Node configuration
    use_agent_nodes: bool = Field(
        default=True,
        description="Use AgentNode instead of EngineNode for better agent handling",
    )

    # Schema configuration
    use_engine_io_mappings: bool = Field(
        default=True, description="Use engine I/O mappings for smart field routing"
    )

    # Private tracking
    _agent_order: list[str] = PrivateAttr(default_factory=list)
    _coordinator_agent: str | None = PrivateAttr(default=None)
    _agent_nodes: dict[str, Node] = PrivateAttr(default_factory=dict)

    def __reduce__(self):
        """Make MultiAgent picklable."""
        state_dict = self.model_dump(
            exclude={
                "_state_instance",
                "graph",
                "_compiled_graph",
                "checkpointer",
                "store",
                "config",
                "_agent_order",
                "_coordinator_agent",
                "_agent_nodes",
            }
        )

        # Handle agent references
        if "agents" in state_dict:
            # Store agent names only for serialization
            state_dict["agent_names"] = list(state_dict["agents"].keys())
            state_dict.pop("agents")

        return (self.__class__, (), state_dict)

    @model_validator(mode="before")
    @classmethod
    def normalize_agents(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Normalize agents into engines dict."""
        # Handle list of agents - convert to dict
        if "agents" in values and isinstance(values["agents"], list):
            agent_dict = {}
            for i, agent in enumerate(values["agents"]):
                if hasattr(agent, "name"):
                    agent_dict[agent.name] = agent
                else:
                    agent_dict[f"agent_{i}"] = agent
            values["agents"] = agent_dict

        # Now handle the dict of agents
        if values.get("agents"):
            # Also add agents to engines dict for compatibility
            if "engines" not in values:
                values["engines"] = {}

            for name, agent in values["agents"].items():
                if isinstance(agent, Agent):
                    values["engines"][name] = agent

        return values

    def setup_agent(self) -> None:
        """Set up the multi-agent system."""
        # Validate we have agents
        if not self.agents:
            raise ValueError(f"{self.__class__.__name__} requires at least one agent")

        # Store agent order
        self._agent_order = list(self.agents.keys())

        # Set up coordinator if needed
        if self.coordination_mode == "supervisor":
            self._setup_supervisor()

        # Ensure schema generation
        self.set_schema = True

        # Initialize agent nodes dict
        self._agent_nodes = {}

    def _setup_schemas(self) -> None:
        """Generate schemas using AgentSchemaComposer."""
        # Don't regenerate if we already have schemas
        if self.state_schema:
            logger.debug(f"Using existing schema: {self.state_schema.__name__}")
            return

        # Get list of agents
        agent_list = list(self.agents.values())

        logger.info(
            f"Creating schema from {len(agent_list)} agents using {self.separation_strategy} strategy"
        )

        # Use AgentSchemaComposer
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agent_list,
            name=f"{self.__class__.__name__}State",
            separation=self.separation_strategy,
            include_meta=self.enable_meta,
        )

        # Log engine IO mappings
        if hasattr(self.state_schema, "__engine_io_mappings__"):
            mappings = getattr(self.state_schema, "__engine_io_mappings__", {})
            logger.debug(f"Schema created with {len(mappings)} engine I/O mappings")

            # Log a few mappings as examples
            for i, (engine_name, mapping) in enumerate(mappings.items()):
                if i < 3:  # Just show first few
                    logger.debug(f"Engine '{engine_name}':")
                    logger.debug(f"  Inputs: {mapping.get('inputs', [])}")
                    logger.debug(f"  Outputs: {mapping.get('outputs', [])}")

        # Let parent handle input/output schema derivation
        super()._auto_derive_io_schemas()

    def build_graph(self) -> BaseGraph:
        """Build the multi-agent graph based on coordination mode."""
        # Create the graph
        graph = BaseGraph(name=f"{self.name}Graph")

        # We'll add state_schema to the graph
        # It will be passed to to_langgraph in compile method

        # Build nodes for each agent
        for agent_name, agent in self.agents.items():
            node = self._create_agent_node(agent_name, agent)
            graph.add_node(node)
            self._agent_nodes[agent_name] = node

        # Connect nodes based on coordination mode
        if self.coordination_mode == "sequential":
            self._build_sequential_graph(graph)
        elif self.coordination_mode == "parallel":
            self._build_parallel_graph(graph)
        elif self.coordination_mode == "supervisor":
            self._build_supervisor_graph(graph)
        elif self.coordination_mode == "swarm":
            self._build_swarm_graph(graph)
        else:  # custom
            self._build_custom_graph(graph)

        return graph

    def _build_sequential_graph(self, graph: BaseGraph) -> None:
        """Build a sequential execution graph."""
        logger.info(f"Building sequential graph with {len(self._agent_order)} agents")

        # Connect agents in sequence
        for i in range(len(self._agent_order) - 1):
            current = self._agent_order[i]
            next_agent = self._agent_order[i + 1]

            graph.add_edge(f"{current}_node", f"{next_agent}_node")

        # Last agent goes to END
        if self._agent_order:
            last_agent = self._agent_order[-1]
            graph.add_edge(f"{last_agent}_node", END)

    def _build_parallel_graph(self, graph: BaseGraph) -> None:
        """Build a parallel execution graph with aggregation."""
        logger.info(f"Building parallel graph with {len(self._agent_order)} agents")

        # Create a special router node that decides which agent to execute
        router_node = Node(name="router", fn=self.route_to_agent, is_entry_point=True)
        graph.add_node(router_node)

        # Create aggregator node
        aggregator_node = Node(name="aggregator", fn=self.aggregate_results)
        graph.add_node(aggregator_node)

        # Connect router to all agents
        for agent_name in self._agent_order:
            # Conditional edge from router to agent
            graph.add_conditional_edge(
                "router", f"{agent_name}_node", self._should_route_to(agent_name)
            )

            # Agent to aggregator
            graph.add_edge(f"{agent_name}_node", "aggregator")

        # Aggregator has conditional edges to either END or back to router
        graph.add_conditional_edge("aggregator", END, self.is_complete)
        graph.add_conditional_edge("aggregator", "router", self.should_continue)

    def _build_supervisor_graph(self, graph: BaseGraph) -> None:
        """Build a supervisor-based execution graph."""
        logger.info(
            f"Building supervisor graph with coordinator: {self._coordinator_agent}"
        )

        if not self._coordinator_agent:
            logger.warning("No coordinator agent set, using first agent")
            self._coordinator_agent = (
                self._agent_order[0] if self._agent_order else None
            )

        if not self._coordinator_agent:
            raise ValueError(
                "Cannot build supervisor graph without a coordinator agent"
            )

        # Coordinator is the entry point and decides routing
        coordinator_node = f"{self._coordinator_agent}_node"
        graph.get_node(coordinator_node).is_entry_point = True

        # Connect coordinator to all other agents
        for agent_name in self._agent_order:
            if agent_name != self._coordinator_agent:
                # Conditional edge from coordinator to agent
                graph.add_conditional_edge(
                    coordinator_node,
                    f"{agent_name}_node",
                    self._should_route_to(agent_name),
                )

                # Agent back to coordinator
                graph.add_edge(f"{agent_name}_node", coordinator_node)

        # Coordinator can decide to end
        graph.add_conditional_edge(coordinator_node, END, self.is_complete)

        # Coordinator can loop to itself
        graph.add_conditional_edge(
            coordinator_node, coordinator_node, self._should_loop_coordinator
        )

    def _build_swarm_graph(self, graph: BaseGraph) -> None:
        """Build a swarm execution graph where any agent can call any other."""
        logger.info(f"Building swarm graph with {len(self._agent_order)} agents")

        # Every agent can potentially call any other agent
        for from_agent in self._agent_order:
            # First agent is entry point
            if from_agent == self._agent_order[0]:
                graph.get_node(f"{from_agent}_node").is_entry_point = True

            # Connect to every other agent
            for to_agent in self._agent_order:
                if from_agent != to_agent:
                    graph.add_conditional_edge(
                        f"{from_agent}_node",
                        f"{to_agent}_node",
                        self._should_route_from_to(from_agent, to_agent),
                    )

            # Every agent can potentially end
            graph.add_conditional_edge(f"{from_agent}_node", END, self.is_complete)

    def _build_custom_graph(self, graph: BaseGraph) -> None:
        """Build a custom graph defined by overriding this method."""
        logger.warning(
            "Using default custom graph implementation - subclasses should override this"
        )

        # Default to sequential as fallback
        self._build_sequential_graph(graph)

    def _create_agent_node(self, agent_name: str, agent: Agent) -> Node:
        """Create a node for an agent with proper configuration."""
        node_name = f"{agent_name}_node"

        # For now, always use standard Node with function wrapper
        # AgentNode is not supported by the current BaseGraph.to_langgraph
        node = Node(
            name=node_name,
            fn=self._create_agent_executor(agent_name, agent),
            is_entry_point=(
                (agent_name == self._agent_order[0]) if self._agent_order else False
            ),
        )

        return node

    def _create_agent_executor(self, agent_name: str, agent: Agent):
        """Create a function that executes an agent and handles state updates."""

        def _execute(state: Any) -> Any:
            # Extract relevant fields based on mapping
            input_data = self._extract_agent_input(agent_name, agent, state)

            # Run the agent
            logger.info(f"Executing agent: {agent_name}")
            result = agent.invoke(input_data)

            # Create state update
            update = self._create_agent_output(agent_name, agent, result, state)

            # Determine next node
            next_node = self._determine_next_node(agent_name, result, state)

            # Return command
            return Command(update=update, goto=next_node)

        return _execute

    def _extract_agent_input(self, agent_name: str, agent: Agent, state: Any) -> Any:
        """Extract input for an agent from the state."""
        # If using engine IO mappings and state schema has them
        if self.use_engine_io_mappings and hasattr(
            self.state_schema, "__engine_io_mappings__"
        ):
            # Get engine name with prefix
            prefixed_name = f"{agent_name.lower().replace(' ', '_')}_{agent.name}"
            mappings = getattr(self.state_schema, "__engine_io_mappings__", {})

            if prefixed_name in mappings:
                # Get input fields for this engine
                input_fields = mappings[prefixed_name].get("inputs", [])
                logger.debug(
                    f"Using engine IO mappings for {prefixed_name}: {input_fields}"
                )

                # Extract the fields
                input_data = {}
                for field in input_fields:
                    if hasattr(state, field):
                        input_data[field] = getattr(state, field)

                # Ensure messages are included if they exist
                if (
                    "messages" not in input_data
                    and hasattr(state, "messages")
                    and state.messages
                ):
                    input_data["messages"] = state.messages

                return input_data

        # Fall back to manual field mapping
        if self.separation_strategy == "namespaced":
            # Map namespaced fields
            input_data = {}

            # Check agent's state schema for expected fields
            if agent.state_schema and hasattr(agent.state_schema, "model_fields"):
                for field_name in agent.state_schema.model_fields:
                    # Try namespaced field first
                    namespaced = f"{agent_name}_{field_name}"
                    if hasattr(state, namespaced):
                        input_data[field_name] = getattr(state, namespaced)
                    # Fall back to direct field
                    elif hasattr(state, field_name):
                        input_data[field_name] = getattr(state, field_name)

            return input_data

        # For shared or smart, pass the state directly (let agent extract what it needs)
        return state

    def _create_agent_output(
        self, agent_name: str, agent: Agent, result: Any, state: Any
    ) -> dict[str, Any]:
        """Create state update from agent result."""
        update = {}

        # Track current and completed agents
        update["active_agent_id"] = agent.id or agent_name

        # If there's a completed_agents field, update it
        if hasattr(state, "completed_agents"):
            completed = list(getattr(state, "completed_agents", []))
            if agent_name not in completed:
                completed.append(agent_name)
            update["completed_agents"] = completed

        # Store agent result in agent_outputs
        if hasattr(state, "agent_outputs") or not hasattr(state, "__fields__"):
            # Either we have agent_outputs or state is a dict (no fields)
            agent_outputs = dict(getattr(state, "agent_outputs", {}))
            agent_outputs[agent_name] = result
            update["agent_outputs"] = agent_outputs

        # If using engine IO mappings and state schema has them
        if self.use_engine_io_mappings and hasattr(
            self.state_schema, "__engine_io_mappings__"
        ):
            # Get engine name with prefix
            prefixed_name = f"{agent_name.lower().replace(' ', '_')}_{agent.name}"
            mappings = getattr(self.state_schema, "__engine_io_mappings__", {})

            if prefixed_name in mappings:
                # Get output fields for this engine
                output_fields = mappings[prefixed_name].get("outputs", [])
                logger.debug(f"Using engine IO mappings for outputs: {output_fields}")

                # Extract the output fields from result
                if isinstance(result, dict):
                    for field in output_fields:
                        if field in result:
                            update[field] = result[field]
                # Special case for messages
                elif "messages" in output_fields and hasattr(result, "messages"):
                    update["messages"] = result.messages

        # For dict results, merge all fields
        elif isinstance(result, dict):
            for key, value in result.items():
                if self.separation_strategy == "namespaced":
                    # Map to namespaced fields
                    update[f"{agent_name}_{key}"] = value
                else:
                    # Direct mapping
                    update[key] = value

        return update

    def _determine_next_node(
        self, agent_name: str, result: Any, state: Any
    ) -> str | None:
        """Determine the next node based on agent result and coordination mode."""
        # Check if result explicitly specifies next_agent
        if isinstance(result, dict) and "next_agent" in result:
            next_agent = result["next_agent"]
            if next_agent in self.agents:
                return f"{next_agent}_node"
            if next_agent == "END":
                return END

        # Use coordination mode default behavior
        if self.coordination_mode == "sequential":
            # Find next agent in sequence
            try:
                idx = self._agent_order.index(agent_name)
                if idx < len(self._agent_order) - 1:
                    return f"{self._agent_order[idx + 1]}_node"
                return END
            except ValueError:
                return END

        # For other modes, routing is handled by conditional edges
        return None

    # Conditional routing functions for graph edges

    def route_to_agent(self, state: Any) -> str:
        """Route to the next agent based on state - used by router node."""
        # Check for explicit next_agent field
        if hasattr(state, "next_agent") and state.next_agent:
            if state.next_agent in self.agents:
                return f"{state.next_agent}_node"
            if state.next_agent == "END":
                return END

        # Check for active_agent_id
        if hasattr(state, "active_agent_id") and state.active_agent_id:
            for agent_name, agent in self.agents.items():
                if agent.id == state.active_agent_id:
                    return f"{agent_name}_node"

        # Default routing based on who hasn't run yet
        if hasattr(state, "completed_agents"):
            completed = getattr(state, "completed_agents", [])
            for agent_name in self._agent_order:
                if agent_name not in completed:
                    return f"{agent_name}_node"

        # No eligible agents left
        return END

    def _should_route_to(self, agent_name: str):
        """Create a condition function that checks if we should route to a specific agent."""

        def _condition(state: Any) -> bool:
            # Check for explicit next_agent
            if hasattr(state, "next_agent"):
                return state.next_agent == agent_name

            # Check if agent is in completed_agents
            if hasattr(state, "completed_agents"):
                return agent_name not in state.completed_agents

            return False

        return _condition

    def _should_route_from_to(self, from_agent: str, to_agent: str):
        """Create a condition function that checks if we should route from one agent to another."""

        def _condition(state: Any) -> bool:
            # Check for explicit next_agent
            if hasattr(state, "next_agent"):
                return state.next_agent == to_agent

            # Default behavior
            return False

        return _condition

    def _should_loop_coordinator(self, state: Any) -> bool:
        """Check if coordinator should loop back to itself."""
        # Check for explicit next_agent = self
        if hasattr(state, "next_agent"):
            return state.next_agent == self._coordinator_agent

        # Check if we have pending items but shouldn't end yet
        if hasattr(state, "is_complete"):
            return not state.is_complete

        return False

    def is_complete(self, state: Any) -> bool:
        """Check if execution is complete."""
        # Check for explicit is_complete flag
        if hasattr(state, "is_complete"):
            return state.is_complete

        # Check if all agents have been run
        if hasattr(state, "completed_agents") and self.agents:
            return len(state.completed_agents) >= len(self.agents)

        # Check max iterations
        if hasattr(state, "iterations"):
            return state.iterations >= self.max_iterations

        return False

    def should_continue(self, state: Any) -> bool:
        """Check if execution should continue."""
        return not self.is_complete(state)

    def aggregate_results(self, state: Any) -> Any:
        """Aggregate results from all agents - used by aggregator node."""
        # Create a Command with the required updates
        updates = {}

        # Increment iterations counter
        iterations = getattr(state, "iterations", 0) + 1
        updates["iterations"] = iterations

        # Check if we've reached max_iterations
        if iterations >= self.max_iterations:
            updates["is_complete"] = True

        # Check if all agents have run
        if hasattr(state, "completed_agents") and self.agents:
            if len(state.completed_agents) >= len(self.agents):
                updates["is_complete"] = True

        # Determine where to go next
        goto = None
        if updates.get("is_complete", False):
            goto = END

        return Command(update=updates, goto=goto)

    def _setup_supervisor(self) -> None:
        """Set up a supervisor agent if needed."""
        # Select coordinator agent - by default, use first agent
        if self._agent_order:
            self._coordinator_agent = self._agent_order[0]
            logger.info(f"Using {self._coordinator_agent} as coordinator agent")

    @classmethod
    def from_agents(
        cls,
        agents: list[Agent] | dict[str, Agent],
        name: str | None = None,
        coordination_mode: str = "sequential",
        **kwargs,
    ) -> "MultiAgent":
        """Create a multi-agent system from a list or dict of agents."""
        # Convert list to dict if needed
        if isinstance(agents, list):
            agent_dict = {}
            for i, agent in enumerate(agents):
                agent_name = getattr(agent, "name", f"agent_{i}")
                # Ensure unique names
                if agent_name in agent_dict:
                    agent_name = f"{agent_name}_{i}"
                agent_dict[agent_name] = agent
        else:
            agent_dict = agents

        logger.info(
            f"Creating {coordination_mode} multi-agent with {len(agent_dict)} agents"
        )

        return cls(
            name=name or f"{cls.__name__}",
            agents=agent_dict,
            coordination_mode=coordination_mode,
            **kwargs,
        )

    @classmethod
    def sequential(
        cls, agents: list[Agent], name: str | None = None, **kwargs
    ) -> "MultiAgent":
        """Create a sequential multi-agent system."""
        return cls.from_agents(
            agents=agents,
            name=name or "SequentialMultiAgent",
            coordination_mode="sequential",
            **kwargs,
        )

    @classmethod
    def parallel(
        cls, agents: list[Agent], name: str | None = None, **kwargs
    ) -> "MultiAgent":
        """Create a parallel multi-agent system."""
        return cls.from_agents(
            agents=agents,
            name=name or "ParallelMultiAgent",
            coordination_mode="parallel",
            **kwargs,
        )

    @classmethod
    def supervised(
        cls,
        agents: list[Agent],
        coordinator: Agent | None = None,
        name: str | None = None,
        **kwargs,
    ) -> "MultiAgent":
        """Create a supervised multi-agent system with a coordinator."""
        agent_list = list(agents)

        # Add coordinator as first agent if provided
        if coordinator and coordinator not in agent_list:
            agent_list.insert(0, coordinator)

        return cls.from_agents(
            agents=agent_list,
            name=name or "SupervisedMultiAgent",
            coordination_mode="supervisor",
            **kwargs,
        )

    def create_runnable(
        self, runnable_config: dict[str, Any] | None = None
    ) -> CompiledGraph:
        """Create and compile the runnable with proper schema kwargs.

        This overrides the base Agent implementation to handle our multi-agent
        state schema correctly.
        """
        if not self._setup_complete:
            raise RuntimeError("Agent setup not complete")

        if not self.graph:
            self._ensure_graph_built()

        if not self.graph:
            raise ValueError("Graph could not be built")

        # Ensure we have schemas - regenerate if needed
        if not self.state_schema:
            logger.warning(f"No state schema found for {self.name}, regenerating...")
            self._setup_schemas()

        # Build schema kwargs - only pass what StateGraph expects
        schema_kwargs = {}

        # CRITICAL: state_schema is required
        if self.state_schema:
            schema_kwargs["state_schema"] = self.state_schema
        else:
            raise ValueError(f"No state schema available for {self.name}")

        # Only add input/output if they exist
        if self.input_schema:
            schema_kwargs["input"] = self.input_schema

        if self.output_schema:
            schema_kwargs["output"] = self.output_schema

        if self.config_schema:
            schema_kwargs["config_schema"] = self.config_schema

        # Debug logging
        logger.debug(f"Schema kwargs for {self.name}: {list(schema_kwargs.keys())}")
        logger.debug(f"State schema: {self.state_schema.__name__}")
        logger.debug(f"Input schema: {getattr(self.input_schema, '__name__', 'None')}")
        logger.debug(
            f"Output schema: {getattr(self.output_schema, '__name__', 'None')}"
        )

        # Convert BaseGraph to LangGraph with schemas
        try:
            # Important: Make the state_schema directly accessible on the graph object
            # so BaseGraph.to_langgraph can access it properly
            self.graph.state_schema = self.state_schema

            langgraph = self.graph.to_langgraph(**schema_kwargs)
        except Exception as e:
            logger.error(f"Failed to convert graph to langgraph: {e}")
            logger.error(f"Schema kwargs were: {list(schema_kwargs.keys())}")
            logger.error(f"State schema type: {type(self.state_schema)}")
            raise

        # Now compile the LangGraph StateGraph with checkpointer and runtime config
        compile_kwargs = {}

        # Always add our checkpointer
        if self.checkpointer:
            compile_kwargs["checkpointer"] = self.checkpointer

        # Add store if available
        if self.store:
            compile_kwargs["store"] = self.store

        # Extract compilation-relevant parameters from runnable_config if provided
        if runnable_config:
            if "interrupt_before" in runnable_config:
                compile_kwargs["interrupt_before"] = runnable_config["interrupt_before"]
            if "interrupt_after" in runnable_config:
                compile_kwargs["interrupt_after"] = runnable_config["interrupt_after"]

        # Compile the LangGraph StateGraph
        return langgraph.compile(**compile_kwargs)
