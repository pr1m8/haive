from __future__ import annotations

"""Agent Node V3 - Hierarchical state projection for multi-agent systems.

This module provides AgentNodeV3 which enables sophisticated multi-agent workflows
by properly handling state projection between container states (like MultiAgentState)
and individual agent states, maintaining type safety and hierarchical access patterns.

Key Features:
    - **Hierarchical State Management**: Projects container states to agent-specific schemas
    - **Direct Field Updates**: Agents with output_schema update state fields directly
    - **Type Safety**: Maintains schema validation throughout execution
    - **Backward Compatibility**: Supports both structured and message-based agents
    - **Dynamic Agent Lookup**: Resolves agents from state at runtime
    - **Recompilation Tracking**: Monitors when agents need graph rebuilding

Architecture:
    The AgentNodeV3 follows a projection-based approach where:

    1. **Container State**: MultiAgentState holds all agents and shared data
    2. **State Projection**: Each agent gets exactly what it expects
    3. **Output Processing**: Structured outputs update fields directly
    4. **State Synchronization**: Changes propagate back to container

Usage Patterns:
    - **Self-Discover Workflows**: Sequential agents building on each other's outputs
    - **Multi-Agent Coordination**: Parallel agents sharing common state
    - **Hierarchical Processing**: Nested agent structures with state isolation

Examples:
    Basic agent node creation::

        from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
        from haive.agents.simple import SimpleAgent

        # Create agent with structured output
        agent = SimpleAgent(
            name="analyzer",
            engine=AugLLMConfig(),
            structured_output_model=AnalysisResult
        )

        # Create node that updates fields directly
        node = create_agent_node_v3(
            agent_name="analyzer",
            agent=agent
        )

    Multi-agent workflow::

        # Sequential execution where agents read each other's outputs
        state = MultiAgentState()
        state.agents["planner"] = planner_agent
        state.agents["executor"] = executor_agent

        # Step 1: Planner outputs planning_result field
        planner_node = create_agent_node_v3("planner")
        result1 = planner_node(state, config)

        # Step 2: Executor reads planning_result directly from state
        executor_node = create_agent_node_v3("executor")
        result2 = executor_node(state, config)

See Also:
    - :class:`haive.core.schema.prebuilt.multi_agent_state.MultiAgentState`: Container state
    - :class:`haive.agents.base.Agent`: Base agent class
    - :mod:`haive.core.graph.node.base_node_config`: Base node configuration
"""


import contextlib
import logging
from typing import TYPE_CHECKING, Any, Self, TypeVar

from langchain_core.messages import BaseMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator
from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

# Handle Agent import - use TYPE_CHECKING to avoid circular import
if TYPE_CHECKING:
    from haive.agents.base.agent import Agent
else:
    # For runtime Pydantic validation
    try:
        from haive.agents.base.agent import Agent
    except ImportError:
        # If circular import, use Any
        from typing import Any as Agent

logger = logging.getLogger(__name__)
console = Console()

# Type variables for schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class AgentNodeV3Config(BaseNodeConfig[TInput, TOutput]):
    """Agent node configuration with hierarchical state projection support.

    This node configuration enables sophisticated multi-agent workflows by handling
    execution of agents within container states (like MultiAgentState) with proper
    state projection, output processing, and hierarchy maintenance.

    The AgentNodeV3Config is designed to work seamlessly with structured output agents,
    enabling direct field updates (like engine nodes) while maintaining backward
    compatibility with message-based agents.

    Key Features:
        - **Hierarchical State Management**: Projects container states to agent schemas
        - **Direct Field Updates**: Agents with output_schema update state fields directly
        - **Type Safety**: Maintains schema validation throughout execution
        - **Dynamic Agent Resolution**: Resolves agents from state at runtime
        - **Recompilation Tracking**: Monitors when agents need graph rebuilding
        - **Flexible Output Modes**: Supports merge, replace, and isolate patterns

    Architecture:
        The node follows a three-phase execution pattern:

        1. **State Projection**: Container state → Agent-specific schema
        2. **Agent Execution**: Agent processes projected state
        3. **Output Integration**: Results → Container state updates

    Key Improvements Over V2:
        - Works with MultiAgentState and similar container patterns
        - Projects state to exact agent schema (no flattening)
        - Maintains type safety throughout execution
        - Supports dynamic agent lookup from state
        - Enables Self-Discover style workflows

    Attributes:
        agent_name (str): Name of agent to execute (key in container's agents dict)
        agent (Optional[Agent]): Agent instance (extracted from state if not provided)
        agent_state_field (str): Field in container holding agent states (default: "agent_states")
        agents_field (str): Field in container holding agent instances (default: "agents")
        project_state (bool): Whether to project state to agent's expected schema (default: True)
        shared_fields (List[str]): Fields to share from container to agent (default: ["messages"])
        output_mode (str): How to handle outputs: 'merge', 'replace', or 'isolate' (default: "merge")
        update_container_state (bool): Whether to update the container's agent_states (default: True)
        track_recompilation (bool): Whether to track agent recompilation needs (default: True)

    Examples:
        Basic configuration::

            from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
            from haive.agents.simple import SimpleAgent

            # Create agent with structured output
            agent = SimpleAgent(
                name="analyzer",
                engine=AugLLMConfig(),
                structured_output_model=AnalysisResult
            )

            # Create node configuration
            config = AgentNodeV3Config(
                name="analysis_node",
                agent_name="analyzer",
                agent=agent
            )

        Custom state projection::

            # Custom shared fields and output mode
            config = AgentNodeV3Config(
                name="custom_node",
                agent_name="custom_agent",
                shared_fields=["messages", "context", "metadata"],
                output_mode="replace",
                project_state=True
            )

        Multi-agent workflow::

            # Sequential agents with direct field access
            planner_config = AgentNodeV3Config(
                name="planner_node",
                agent_name="planner"
            )

            executor_config = AgentNodeV3Config(
                name="executor_node",
                agent_name="executor"
            )

            # Execute in sequence
            state = MultiAgentState()
            result1 = planner_config(state, config)  # Updates planning fields
            result2 = executor_config(state, config)  # Reads planning fields directly

    Raises:
        ValueError: If neither agent_name nor agent is provided
        ValueError: If agent_name not found in state's agents dict
        AgentExecutionError: If agent execution fails

    Note:
        For agents with structured output schemas, the node will update state fields
        directly (like engine nodes). For message-based agents, it uses the traditional
        agent_outputs pattern for backward compatibility.

    See Also:
        - :func:`create_agent_node_v3`: Convenience factory function
        - :class:`haive.core.schema.prebuilt.multi_agent_state.MultiAgentState`: Container state
        - :class:`haive.agents.base.Agent`: Base agent class
        - :class:`haive.core.graph.node.base_node_config.BaseNodeConfig`: Base configuration
    """

    node_type: NodeType = Field(
        default=NodeType.AGENT, description="Node type for agent execution"
    )

    # Agent configuration
    agent_name: str = Field(
        description="Name of agent to execute (key in container's agents dict)"
    )

    agent: Agent | None = Field(
        default=None,
        description="Agent instance (extracted from state if not provided)",
    )

    agent_state_field: str = Field(
        default="agent_states", description="Field in container holding agent states"
    )

    agents_field: str = Field(
        default="agents", description="Field in container holding agent instances"
    )

    # State projection
    project_state: bool = Field(
        default=True, description="Whether to project state to agent's expected schema"
    )

    shared_fields: list[str] = Field(
        default_factory=lambda: ["messages"],
        description="Fields to share from container to agent",
    )

    # Output handling
    output_mode: str = Field(
        default="merge",
        description="How to handle outputs: 'merge', 'replace', or 'isolate'",
    )

    update_container_state: bool = Field(
        default=True, description="Whether to update the container's agent_states"
    )

    # Recompilation tracking
    track_recompilation: bool = Field(
        default=True, description="Whether to track agent recompilation needs"
    )

    @model_validator(mode="after")
    def validate_agent_config(self) -> Self:
        """Validate configuration."""
        if not self.agent_name and not self.agent:
            raise ValueError("Either agent_name or agent must be provided")

        # If agent is provided directly, we should use it regardless of extract_from_container
        # The runtime logic in _get_agent already handles this correctly

        return self

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get input fields based on container expectations."""
        fields = []

        # Always need messages
        fields.append(StandardFields.messages(use_enhanced=True))

        # Need agent states field
        fields.append(
            FieldDefinition(
                name=self.agent_state_field,
                field_type=dict[str, dict[str, Any]],
                default_factory=dict,
                description="Agent states container",
            )
        )

        # Always need agents field for state pattern (like engines field)
        fields.append(
            FieldDefinition(
                name=self.agents_field,
                field_type=dict[str, "Agent"],
                default_factory=dict,
                description="Agent instances",
            )
        )

        return fields

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get output fields."""
        fields = []

        # Messages are always output
        fields.append(StandardFields.messages(use_enhanced=True))

        # Agent states if updating container
        if self.update_container_state:
            fields.append(
                FieldDefinition(
                    name=self.agent_state_field,
                    field_type=dict[str, dict[str, Any]],
                    default_factory=dict,
                    description="Updated agent states",
                )
            )

        # Agent outputs
        fields.append(
            FieldDefinition(
                name="agent_outputs",
                field_type=dict[str, Any],
                default_factory=dict,
                description="Agent execution outputs",
            )
        )

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute agent with hierarchical state projection.

        This is the main execution method that orchestrates the complete agent
        execution workflow within a multi-agent system. It handles state projection,
        agent execution, output processing, and state updates.

        The method follows a three-phase execution pattern:
        1. **State Projection**: Projects container state to agent-specific schema
        2. **Agent Execution**: Executes agent with projected state
        3. **Output Integration**: Processes results and updates container state

        Args:
            state (StateLike): Container state (e.g., MultiAgentState) containing
                agents and shared data. Must have agents dict and agent_states dict.
            config (Optional[ConfigLike]): Optional configuration for execution.
                Can include debug flags, execution parameters, and runtime settings.

        Returns:
            Command: LangGraph command containing state updates and optional goto.
                For agents with structured output, updates contain direct field updates.
                For message-based agents, updates contain agent_outputs and messages.

        Raises:
            ValueError: If agent_name not found in state's agents dict
            AgentExecutionError: If agent execution fails
            ValidationError: If state projection or output processing fails

        Examples:
            Basic execution::

                from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
                from haive.agents.simple import SimpleAgent

                # Setup state with agent
                state = MultiAgentState()
                state.agents["analyzer"] = SimpleAgent(
                    name="analyzer",
                    engine=AugLLMConfig(),
                    structured_output_model=AnalysisResult
                )

                # Create and execute node
                node = create_agent_node_v3("analyzef")
                result = node(state, {"debug": True})

                # Result contains direct field updates
                print(result.update.keys())  # ['analysis_result', 'confidence', 'agent_states']

            Sequential multi-agent execution::

                # Sequential agents reading each other's outputs
                state = MultiAgentState()
                state.agents["planner"] = planner_agent
                state.agents["executor"] = executor_agent

                # Execute planner - outputs planning_result
                planner_node = create_agent_node_v3("planner")
                result1 = planner_node(state, config)

                # Apply updates
                for key, value in result1.update.items():
                    setattr(state, key, value)

                # Execute executor - reads planning_result directly
                executor_node = create_agent_node_v3("executor")
                result2 = executor_node(state, config)

        Note:
            The method automatically detects whether an agent has structured output
            and adjusts the output processing accordingly. Agents with output_schema
            will have their outputs used for direct field updates, while message-based
            agents will use the traditional agent_outputs pattern.

        See Also:
            - :meth:`_project_state_for_agent`: State projection logic
            - :meth:`_process_agent_output`: Output processing logic
            - :class:`haive.core.schema.prebuilt.multi_agent_state.MultiAgentState`: Container state
        """
        # Check if debug mode is enabled
        debug_mode = (
            (config and config.get("debug", False))
            or (hasattr(state, "debug") and getattr(state, "debug", False))
            or False
        )

        if debug_mode:
            self._display_debug_info(state, "BEFORE_EXECUTION")

        logger.info(f"{'=' * 60}")
        logger.info(f"AGENT NODE V3: {self.name}")
        logger.info(f"Agent: {self.agent_name}")
        logger.info(f"{'=' * 60}")

        try:
            # Get agent instance
            agent = self._get_agent(state)
            if not agent:
                raise ValueError(f"Agent '{self.agent_name}' not found")

            # Set active agent if container supports it
            self._set_active_agent(state)

            # Project state for agent
            agent_input = self._project_state_for_agent(state, agent)

            if debug_mode:
                self._display_agent_input(agent_input, agent)

            logger.info(f"Executing agent with {len(agent_input)} fields")
            logger.debug(f"Fields: {list(agent_input.keys())}")

            # Execute agent
            if hasattr(agent, "_app") and agent._app:
                logger.debug("Using agent's compiled graph")
                result = agent._app.invoke(agent_input, config)
            else:
                logger.debug("Using agent's invoke method")
                result = agent.invoke(agent_input, config)

            # Process output
            state_update = self._process_agent_output(result, state, agent)

            if debug_mode:
                self._display_agent_output(result, state_update)

            # Track recompilation if needed
            if self.track_recompilation:
                self._check_recompilation(state, agent)

            logger.info(
                f"✅ Agent completed with {
                    len(state_update)} field updates"
            )

            if debug_mode:
                self._display_debug_info(state, "AFTER_EXECUTION", state_update)

            return Command(update=state_update, goto=self._get_goto_node())

        except Exception as e:
            logger.exception(f"❌ Agent execution failed: {e}")

            # Record error
            error_update = {
                "agent_outputs": {
                    self.agent_name: {"error": str(e), "error_type": type(e).__name__}
                }
            }

            # Preserve existing outputs
            if hasattr(state, "agent_outputs"):
                current_outputs = getattr(state, "agent_outputs", {})
                error_update["agent_outputs"] = {
                    **current_outputs,
                    **error_update["agent_outputs"],
                }

            return Command(update=error_update, goto=self._get_goto_node())

    def _get_agent(self, state: StateLike) -> Agent | None:
        """Get agent from direct reference or state's agents dict."""
        # Priority 1: Direct agent reference
        if self.agent:
            return self.agent

        # Priority 2: Get from state's agents dict using agent_name
        if self.agent_name and state:
            # Try to get from agents dict in state
            if hasattr(state, self.agents_field):
                agents_dict = getattr(state, self.agents_field, {})
                if isinstance(agents_dict, dict):
                    return agents_dict.get(self.agent_name)

        return None

    def _set_active_agent(self, state: StateLike) -> None:
        """Set active agent if container supports it."""
        # Only try to set active agent if the state supports it
        # and we're not using a direct agent reference
        if hasattr(state, "set_active_agent") and not self.agent:
            # Only validate if we're relying on state's agents dict
            state.set_active_agent(self.agent_name)
        elif hasattr(state, "active_agent"):
            # Direct assignment doesn't validate
            state.active_agent = self.agent_name

    def _project_state_for_agent(
        self, state: StateLike, agent: Agent
    ) -> dict[str, Any]:
        """Project container state to agent's expected schema.

        This is the key method that enables hierarchical state management in
        multi-agent systems. It projects a container state (like MultiAgentState)
        to the specific schema expected by an individual agent, ensuring type
        safety and proper data isolation.

        The projection process:
        1. Extracts agent's isolated state from agent_states field
        2. Adds shared fields from container (messages, context, etc.)
        3. Preserves agent-specific data while sharing common information
        4. Validates that all required inputs are available

        Args:
            state (StateLike): Container state containing all agents and shared data.
                Must have agent_states dict and shared fields.
            agent (Agent): Target agent instance that will receive the projected state.
                Used to determine expected schema and validation requirements.

        Returns:
            Dict[str, Any]: Projected state dictionary containing:
                - Agent's isolated state from agent_states[agent_name]
                - Shared fields from container (messages, context, etc.)
                - Properly formatted data matching agent's expected schema

        Examples:
            Basic state projection::

                # Container state with multiple agents
                state = MultiAgentState()
                state.messages = [HumanMessage("Hello")]
                state.agent_states = {
                    "analyzef": {"analysis_ready": True},
                    "executof": {"execution_ready": False}
                }

                # Project for specific agent
                projected = node._project_state_for_agent(state, analyzer_agent)

                # Result contains isolated state + shared fields
                print(projected)
                # {
                #     "analysis_ready": True,      # From agent_states["analyzer"]
                #     "messages": [HumanMessage("Hello")]  # Shared field
                # }

            Custom shared fields::

                # Configure custom shared fields
                config = AgentNodeV3Config(
                    agent_name="custom_agent",
                    shared_fields=["messages", "context", "metadata"]
                )

                # Projection includes all shared fields
                projected = config._project_state_for_agent(state, agent)
                # Contains: agent state + messages + context + metadata

        Note:
            The method ensures that each agent receives exactly what it expects,
            maintaining type safety and preventing agents from accessing data
            they shouldn't see. This enables true hierarchical state management
            in complex multi-agent workflows.

        See Also:
            - :attr:`shared_fields`: Fields shared from container to agent
            - :attr:`agent_state_field`: Container field holding agent states
            - :meth:`_extract_message_objects`: Message extraction helper
        """
        # DEBUG: Print state projection debug info

        # Start with agent's isolated state
        agent_states = getattr(state, self.agent_state_field, {})
        agent_state = agent_states.get(self.agent_name, {})
        projected = agent_state.copy()

        # DEBUG: Show agent outputs
        if hasattr(state, "agent_outputs"):
            agent_outputs = getattr(state, "agent_outputs", {})
            for agent_name, _output in agent_outputs.items():
                pass

        if not self.project_state:
            return projected

        # Add shared fields from container
        for field in self.shared_fields:
            if hasattr(state, field) and field not in projected:
                value = getattr(state, field)
                # Special handling for messages
                if field == "messages":
                    value = self._extract_message_objects(value)
                projected[field] = value
            elif hasattr(state, field):
                pass
            else:
                pass

        # DEBUG: Show projected state

        # DEBUG: Check if required inputs are available
        agent_name = self.agent_name
        if agent_name == "select_modules":
            required = ["reasoning_modules", "task_description"]
        elif agent_name == "adapt_modules":
            required = ["selected_modules", "task_description"]
        elif agent_name == "create_structure":
            required = ["adapted_modules", "task_description"]
        elif agent_name == "final_reasoning":
            required = ["reasoning_structure", "task_description"]
        else:
            required = []

        missing = [key for key in required if key not in projected]
        if missing:
            pass
        else:
            pass

        # Let the agent handle its own state schema validation
        # AgentNodeV3 just provides the projected data
        return projected

    def _extract_message_objects(self, messages: Any) -> list[BaseMessage]:
        """Extract BaseMessage objects from various containers."""
        if hasattr(messages, "root"):
            return messages.root
        if isinstance(messages, list | tuple):
            return list(messages)
        try:
            return list(messages)
        except BaseException:
            logger.warning(f"Cannot extract messages from {type(messages)}")
            return []

    def _process_agent_output(
        self, result: Any, state: StateLike, agent: Agent
    ) -> dict[str, Any]:
        """Process agent output and prepare state update.

        This method processes agent execution results and converts them into
        appropriate state updates for the container state. It handles both
        structured output agents (with output_schema) and traditional message-based
        agents, ensuring proper integration with multi-agent workflows.

        The processing follows different patterns based on agent type:
        - **Structured Output Agents**: Direct field updates (like engine nodes)
        - **Message-Based Agents**: Traditional agent_outputs pattern
        - **Hybrid Agents**: Combination of both patterns

        Processing Logic:
            1. Detects if agent has structured output schema
            2. For structured output: Extracts fields for direct state updates
            3. For messages: Preserves message-based workflow compatibility
            4. Updates agent_states for tracking and debugging
            5. Handles shared fields and cross-agent communication

        Args:
            result (Any): Raw result from agent execution. Can be:
                - BaseModel instance (structured output)
                - Dict with messages and/or structured fields
                - String or other primitive (fallback)
            state (StateLike): Container state to update. Must have agent_states
                and other container fields.
            agent (Agent): Agent instance that produced the result. Used to
                determine output schema and processing strategy.

        Returns:
            Dict[str, Any]: State update dictionary containing:
                - Direct field updates for structured output agents
                - agent_states updates for tracking
                - agent_outputs for message-based agents
                - messages for message-based workflows

        Examples:
            Structured output agent::

                # Agent with output_schema returns BaseModel
                class AnalysisResult(BaseModel):
                    analysis: str
                    confidence: float
                    recommendations: List[str]

                agent = SimpleAgent(
                    name="analyzer",
                    structured_output_model=AnalysisResult
                )

                result = AnalysisResult(
                    analysis="Market analysis complete",
                    confidence=0.95,
                    recommendations=["Invest in AI", "Expand globally"]
                )

                # Processing creates direct field updates
                update = node._process_agent_output(result, state, agent)
                print(update)
                # {
                #     "analysis": "Market analysis complete",
                #     "confidence": 0.95,
                #     "recommendations": ["Invest in AI", "Expand globally"],
                #     "agent_states": {
                #         "analyzef": {"executed": True, "has_schema": True}
                #     }
                # }

            Message-based agent::

                # Traditional agent returns messages
                result = {
                    "messages": [
                        AIMessage("I've completed the analysis.")
                    ]
                }

                # Processing preserves message workflow
                update = node._process_agent_output(result, state, agent)
                print(update)
                # {
                #     "messages": [AIMessage("I've completed the analysis.")],
                #     "agent_states": {
                #         "analyzef": {"executed": True, "message_count": 1}
                #     }
                # }

            Sequential workflow (Self-Discover pattern)::

                # Agent 1 outputs structured data
                planner_result = PlanningResult(
                    plan=["Step 1", "Step 2", "Step 3"],
                    priority="high"
                )

                # Creates direct field updates
                update1 = node._process_agent_output(planner_result, state, planner)
                # Updates: {"plan": [...], "priority": "high"}

                # Agent 2 can read these fields directly
                executor_input = node._project_state_for_agent(state, executor)
                # Contains: {"plan": [...], "priority": "high", "messages": [...]}

        Note:
            This method is the key to enabling Self-Discover style workflows where
            agents can read each other's outputs directly from state fields, rather
            than navigating complex nested structures like agent_outputs[agent_name][field].

        See Also:
            - :attr:`output_mode`: Controls how outputs are merged
            - :attr:`update_container_state`: Controls agent_states updates
            - :meth:`_project_state_for_agent`: State projection for next agents
        """
        state_update = {}

        # Check if agent has structured output
        has_output_schema = hasattr(agent, "output_schema") and agent.output_schema

        if has_output_schema:
            # STRUCTURED OUTPUT - Direct field updates
            if isinstance(result, BaseModel):
                # Agent returned a Pydantic model instance
                state_update = result.model_dump()

                # Special handling for messages if present
                if hasattr(result, "messages"):
                    messages = getattr(result, "messages", None)
                    if messages is not None:
                        state_update["messages"] = messages

            elif isinstance(result, dict):
                # Agent returned dict - use directly
                state_update = result
            else:
                # Fallback - shouldn't happen with structured output
                state_update = {"result": result}

            # Optional: Track in agent_states for history/debugging
            # But this is NOT the primary output mechanism
            if self.update_container_state:
                agent_states = getattr(state, self.agent_state_field, {})
                # Only store metadata, not duplicate all data
                agent_state_data = {
                    "executed": True,
                    "output_type": type(result).__name__,
                    "has_schema": True,
                }
                state_update[self.agent_state_field] = {
                    **agent_states,
                    self.agent_name: agent_state_data,
                }

        else:
            # NO STRUCTURED OUTPUT - Original behavior
            if isinstance(result, dict):
                result_dict = result
            elif isinstance(result, BaseModel):
                # Preserve messages
                messages = getattr(result, "messages", None)
                result_dict = result.model_dump()
                if messages is not None:
                    result_dict["messages"] = messages
            else:
                result_dict = {"result": result}

            # Check if this is message-based output
            if "messages" in result_dict:
                # Message-based - just pass through messages
                state_update["messages"] = result_dict["messages"]

                # Optional: Track in agent_states
                if self.update_container_state:
                    agent_states = getattr(state, self.agent_state_field, {})
                    state_update[self.agent_state_field] = {
                        **agent_states,
                        self.agent_name: {
                            "executed": True,
                            "message_count": len(result_dict["messages"]),
                        },
                    }
            else:
                # Unstructured output - use agent_outputs pattern
                if self.update_container_state:
                    agent_states = getattr(state, self.agent_state_field, {})
                    current_agent_state = agent_states.get(self.agent_name, {})

                    if self.output_mode == "merge":
                        updated_state = {**current_agent_state, **result_dict}
                    elif self.output_mode == "replace":
                        updated_state = result_dict
                    else:  # isolate
                        updated_state = current_agent_state

                    state_update[self.agent_state_field] = {
                        **agent_states,
                        self.agent_name: updated_state,
                    }

                # Update agent outputs
                current_outputs = getattr(state, "agent_outputs", {})
                state_update["agent_outputs"] = {
                    **current_outputs,
                    self.agent_name: result_dict,
                }

        # Check for shared fields (from agent state_schema if it has one)
        if hasattr(agent, "state_schema"):
            schema_shared = getattr(agent.state_schema, "__shared_fields__", set())
            # Only process shared fields if we haven't already updated them
            for field in schema_shared:
                if field not in state_update and field in result_dict:
                    state_update[field] = result_dict[field]

        return state_update

    def _check_recompilation(self, state: StateLike, agent: Agent) -> None:
        """Check and track recompilation needs."""
        if hasattr(agent, "graph") and hasattr(agent.graph, "needs_recompile"):
            if agent.graph.needs_recompile():
                # Mark for recompilation
                if hasattr(state, "mark_agent_for_recompile"):
                    state.mark_agent_for_recompile(
                        self.agent_name, "Graph needs recompilation"
                    )
                elif hasattr(state, "agents_needing_recompile"):
                    state.agents_needing_recompile.add(self.agent_name)

    def _get_goto_node(self) -> str | None:
        """Get next node to execute."""
        return self.command_goto

    def _display_debug_info(
        self,
        state: StateLike,
        phase: str,
        state_update: dict[str, Any] | None = None,
    ) -> None:
        """Display comprehensive debug information with rich visualization."""
        # Create main panel title
        panel_title = f"🔍 AgentNodeV3 Debug - {phase} - {self.agent_name}"

        # Create the main tree structure
        debug_tree = Tree(panel_title, style="bold blue")

        # 1. Global MultiAgentState
        global_branch = debug_tree.add("🌍 Global MultiAgentState", style="bold green")
        self._add_global_state_info(global_branch, state)

        # 2. Individual Agent State
        agent_branch = debug_tree.add(
            f"🤖 Agent '{self.agent_name}' State", style="bold yellow"
        )
        self._add_agent_state_info(agent_branch, state)

        # 3. Private/Engine State
        private_branch = debug_tree.add("🔒 Private/Engine State", style="bold red")
        self._add_private_state_info(private_branch, state)

        # 4. State Update (if provided)
        if state_update:
            update_branch = debug_tree.add("📝 State Updates", style="bold magenta")
            self._add_state_update_info(update_branch, state_update)

        # Display the tree in a panel
        console.print(Panel(debug_tree, border_style="blue", expand=False))
        console.print()  # Add spacing

    def _add_global_state_info(self, branch: Tree, state: StateLike) -> None:
        """Add global state information to the debug tree."""
        # Messages
        if hasattr(state, "messages"):
            messages = getattr(state, "messages", [])
            msg_branch = branch.add(f"💬 Messages ({len(messages)})")
            for i, msg in enumerate(messages[-3:]):  # Show last 3 messages
                content = (
                    getattr(msg, "content", str(msg))[:50] + "..."
                    if len(str(getattr(msg, "content", str(msg)))) > 50
                    else getattr(msg, "content", str(msg))
                )
                msg_type = getattr(msg, "type", type(msg).__name__)
                msg_branch.add(f"[{i}] {msg_type}: {content}")

        # Agent count and names
        if hasattr(state, "agents"):
            agents = getattr(state, "agents", {})
            agent_branch = branch.add(f"👥 Agents ({len(agents)})")
            for name, agent in agents.items():
                agent_type = type(agent).__name__
                agent_status = "✅ Active" if name == self.agent_name else "⏸️ Idle"
                agent_branch.add(f"{name} ({agent_type}) - {agent_status}")

        # Execution order
        if hasattr(state, "agent_execution_order"):
            order = getattr(state, "agent_execution_order", [])
            order_branch = branch.add(f"📋 Execution Order ({len(order)})")
            for i, agent_name in enumerate(order):
                order_branch.add(f"{i + 1}. {agent_name}")

        # Active agent
        if hasattr(state, "active_agent"):
            active = getattr(state, "active_agent", None)
            branch.add(f"⭐ Active Agent: {active or 'None'}")

    def _add_agent_state_info(self, branch: Tree, state: StateLike) -> None:
        """Add specific agent state information to the debug tree."""
        # Agent states container
        if hasattr(state, "agent_states"):
            agent_states = getattr(state, "agent_states", {})
            agent_state = agent_states.get(self.agent_name, {})

            state_branch = branch.add(f"📊 State Fields ({len(agent_state)})")
            for key, value in agent_state.items():
                if key == "messages":
                    state_branch.add(f"💬 {key}: {len(value)} messages")
                elif isinstance(value, list | tuple):
                    state_branch.add(f"📋 {key}: [{len(value)} items]")
                elif isinstance(value, dict):
                    state_branch.add(f"📁 {key}: {{{len(value)} keys}}")
                else:
                    value_str = (
                        str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                    )
                    state_branch.add(f"📝 {key}: {value_str}")

        # Agent outputs
        if hasattr(state, "agent_outputs"):
            outputs = getattr(state, "agent_outputs", {})
            agent_output = outputs.get(self.agent_name, {})

            output_branch = branch.add(f"📤 Outputs ({len(agent_output)})")
            for key, value in agent_output.items():
                if key == "error":
                    output_branch.add(f"❌ {key}: {value}")
                elif isinstance(value, list | tuple):
                    output_branch.add(f"📋 {key}: [{len(value)} items]")
                else:
                    value_str = (
                        str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                    )
                    output_branch.add(f"📝 {key}: {value_str}")

    def _add_private_state_info(self, branch: Tree, state: StateLike) -> None:
        """Add private/engine state information to the debug tree."""
        # Tool-related state
        tool_fields = ["tools", "tool_calls", "tool_results", "available_tools"]
        tool_branch = None
        for field in tool_fields:
            if hasattr(state, field):
                if tool_branch is None:
                    tool_branch = branch.add("🛠️ Tool State")
                value = getattr(state, field, None)
                if isinstance(value, list | tuple):
                    tool_branch.add(f"{field}: [{len(value)} items]")
                elif isinstance(value, dict):
                    tool_branch.add(f"{field}: {{{len(value)} keys}}")
                else:
                    tool_branch.add(f"{field}: {str(value)[:30]}...")

        # Engine-related state
        engine_fields = [
            "engine_name",
            "model",
            "temperature",
            "max_tokens",
            "token_usage",
        ]
        engine_branch = None
        for field in engine_fields:
            if hasattr(state, field):
                if engine_branch is None:
                    engine_branch = branch.add("⚙️ Engine State")
                value = getattr(state, field, None)
                engine_branch.add(f"{field}: {value}")

        # Meta state
        meta_fields = ["recompile_needed", "agents_needing_recompile", "meta"]
        meta_branch = None
        for field in meta_fields:
            if hasattr(state, field):
                if meta_branch is None:
                    meta_branch = branch.add("🎛️ Meta State")
                value = getattr(state, field, None)
                if isinstance(value, set):
                    meta_branch.add(f"{field}: {{{', '.join(value)}}}")
                else:
                    meta_branch.add(f"{field}: {value}")

    def _add_state_update_info(
        self, branch: Tree, state_update: dict[str, Any]
    ) -> None:
        """Add state update information to the debug tree."""
        for key, value in state_update.items():
            if key == "messages":
                branch.add(f"💬 {key}: Updated with new messages")
            elif key == "agent_states":
                agent_updates = (
                    value.get(self.agent_name, {}) if isinstance(value, dict) else {}
                )
                update_branch = branch.add(
                    f"📊 {key}: Agent '{
                        self.agent_name}' ({
                        len(agent_updates)} fields)"
                )
                for field, field_value in agent_updates.items():
                    if isinstance(field_value, list | tuple):
                        update_branch.add(f"  📋 {field}: [{len(field_value)} items]")
                    else:
                        value_str = (
                            str(field_value)[:30] + "..."
                            if len(str(field_value)) > 30
                            else str(field_value)
                        )
                        update_branch.add(f"  📝 {field}: {value_str}")
            elif key == "agent_outputs":
                agent_output = (
                    value.get(self.agent_name, {}) if isinstance(value, dict) else {}
                )
                output_branch = branch.add(
                    f"📤 {key}: Agent '{
                        self.agent_name}' ({
                        len(agent_output)} fields)"
                )
                for field, field_value in agent_output.items():
                    value_str = (
                        str(field_value)[:30] + "..."
                        if len(str(field_value)) > 30
                        else str(field_value)
                    )
                    output_branch.add(f"  📝 {field}: {value_str}")
            else:
                value_str = (
                    str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                )
                branch.add(f"📝 {key}: {value_str}")

    def _display_agent_input(self, agent_input: dict[str, Any], agent: Agent) -> None:
        """Display agent input projection with rich visualization."""
        input_tree = Tree(
            f"📥 Projected Input for '{self.agent_name}'", style="bold cyan"
        )

        # Add agent schema info
        schema_info = input_tree.add("📋 Schema Information")
        if hasattr(agent, "state_schema"):
            schema_name = getattr(
                agent.state_schema, "__name__", str(agent.state_schema)
            )
            schema_info.add(f"State Schema: {schema_name}")
        if hasattr(agent, "input_schema"):
            schema_name = getattr(
                agent.input_schema, "__name__", str(agent.input_schema)
            )
            schema_info.add(f"Input Schema: {schema_name}")

        # Add projected fields
        fields_branch = input_tree.add(f"📊 Projected Fields ({len(agent_input)})")
        for key, value in agent_input.items():
            if key == "messages":
                fields_branch.add(f"💬 {key}: {len(value)} messages")
            elif isinstance(value, list | tuple):
                fields_branch.add(f"📋 {key}: [{len(value)} items]")
            elif isinstance(value, dict):
                fields_branch.add(f"📁 {key}: {{{len(value)} keys}}")
            else:
                value_str = (
                    str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                )
                fields_branch.add(f"📝 {key}: {value_str}")

        console.print(Panel(input_tree, border_style="cyan", expand=False))
        console.print()

    def _display_agent_output(self, result: Any, state_update: dict[str, Any]) -> None:
        """Display agent output and state updates with rich visualization."""
        output_tree = Tree(
            f"📤 Agent '{
                self.agent_name}' Output",
            style="bold green",
        )

        # Add raw result info
        result_branch = output_tree.add("🎯 Raw Result")
        if isinstance(result, dict):
            result_branch.add(f"Type: Dictionary ({len(result)} fields)")
            for key, value in result.items():
                if isinstance(value, list | tuple):
                    result_branch.add(f"📋 {key}: [{len(value)} items]")
                else:
                    value_str = (
                        str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                    )
                    result_branch.add(f"📝 {key}: {value_str}")
        else:
            result_type = type(result).__name__
            result_branch.add(f"Type: {result_type}")
            if hasattr(result, "model_dump"):
                fields = result.model_dump()
                result_branch.add(f"Fields: {len(fields)}")

        # Add state update info
        if state_update:
            update_branch = output_tree.add(f"📝 State Updates ({len(state_update)})")
            self._add_state_update_info(update_branch, state_update)

        console.print(Panel(output_tree, border_style="green", expand=False))
        console.print()


# ============================================================================
# CONVENIENCE FACTORY FUNCTION
# ============================================================================


def create_agent_node_v3(
    agent_name: str,
    agent: Agent | None = None,
    name: str | None = None,
    **kwargs,
) -> AgentNodeV3Config:
    """Create an agent node V3 configuration.

    Convenience factory function for creating AgentNodeV3Config instances with
    sensible defaults. This function simplifies the creation of agent nodes for
    multi-agent workflows and handles common configuration patterns.

    The function automatically:
    - Generates a descriptive node name if not provided
    - Rebuilds the model to resolve forward references
    - Applies default configuration suitable for most use cases
    - Supports both direct agent provision and runtime resolution

    Args:
        agent_name (str): Name of agent to execute. This should match a key in
            the container state's agents dictionary. Used for dynamic agent
            resolution at runtime.
        agent (Optional[Agent]): Optional agent instance to use directly.
            If provided, the agent will be used regardless of what's in the
            container state. If None, agent will be resolved from state.agents[agent_name].
        name (Optional[str]): Optional node name for debugging and visualization.
            If not provided, will be auto-generated as "agent_{agent_name}".
        **kwargs: Additional configuration options passed to AgentNodeV3Config:
            - shared_fields: Fields to share from container (default: ["messages"])
            - output_mode: How to handle outputs ("merge", "replace", "isolate")
            - project_state: Whether to project state to agent schema (default: True)
            - track_recompilation: Whether to track recompilation needs (default: True)

    Returns:
        AgentNodeV3Config: Configured agent node ready for execution in graphs.
            The returned configuration can be used directly in LangGraph workflows.

    Examples:
        Basic agent node creation::

            from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
            from haive.agents.simple import SimpleAgent

            # Create agent with structured output
            agent = SimpleAgent(
                name="analyzer",
                engine=AugLLMConfig(),
                structured_output_model=AnalysisResult
            )

            # Create node - agent will be resolved from state
            node = create_agent_node_v3("analyzer")

            # Or provide agent directly
            node = create_agent_node_v3("analyzer", agent=agent)

        Custom configuration::

            # Advanced configuration with custom settings
            node = create_agent_node_v3(
                agent_name="custom_agent",
                name="custom_analysis_node",
                shared_fields=["messages", "context", "metadata"],
                output_mode="replace",
                project_state=True,
                track_recompilation=False
            )

        Multi-agent workflow::

            # Create nodes for sequential execution
            planner_node = create_agent_node_v3("planner")
            executor_node = create_agent_node_v3("executor")
            reviewer_node = create_agent_node_v3("reviewer")

            # Build graph
            from langgraph.graph import StateGraph
            graph = StateGraph(MultiAgentState)
            graph.add_node("plan", planner_node)
            graph.add_node("execute", executor_node)
            graph.add_node("review", reviewer_node)

            # Chain execution
            graph.add_edge("plan", "execute")
            graph.add_edge("execute", "review")

        Usage in LangGraph::

            # Direct usage in graph execution
            state = MultiAgentState()
            state.agents["analyzer"] = analyzer_agent

            # Execute node
            node = create_agent_node_v3("analyzef")
            result = node(state, {"debug": True})

            # Apply updates
            for key, value in result.update.items():
                if hasattr(state, key):
                    setattr(state, key, value)

    Raises:
        ValueError: If agent_name is empty or None
        ImportError: If Agent class cannot be imported for model rebuilding

    Note:
        The function automatically rebuilds the Pydantic model to resolve forward
        references to the Agent class. This ensures proper type validation and
        IDE support.

    See Also:
        - :class:`AgentNodeV3Config`: The main configuration class
        - :class:`haive.core.schema.prebuilt.multi_agent_state.MultiAgentState`: Container state
        - :class:`haive.agents.base.Agent`: Base agent class
        - :mod:`langgraph.graph`: LangGraph integration
    """
    # Ensure model is rebuilt if needed
    with contextlib.suppress(ImportError):

        AgentNodeV3Config.model_rebuild()

    if not name:
        name = f"agent_{agent_name}"

    return AgentNodeV3Config(name=name, agent_name=agent_name, agent=agent, **kwargs)


# Rebuild the model after Agent is available to resolve forward references
try:
    from haive.agents.base.agent import Agent

    AgentNodeV3Config.model_rebuild()
except ImportError:
    # Will rebuild when Agent becomes available
    pass
