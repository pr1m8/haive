"""Agent Node V3 - Hierarchical state projection for multi-agent systems.

This module provides AgentNodeV3 which properly handles state projection
between container states (like MultiAgentState) and individual agent states,
maintaining type safety and hierarchical access patterns.
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from langchain_core.messages import BaseMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

if TYPE_CHECKING:
    from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)
console = Console()

# Type variables for schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class AgentNodeV3Config(BaseNodeConfig[TInput, TOutput]):
    """Agent node configuration with hierarchical state projection support.

    This node configuration handles:
    - Execution of agents within container states (like MultiAgentState)
    - State projection from container to agent-specific schema
    - Updates back to the container maintaining hierarchy
    - Recompilation tracking for dynamic agent changes

    Key improvements over V2:
    - Works with MultiAgentState and similar container patterns
    - Projects state to exact agent schema (no flattening)
    - Maintains type safety throughout execution
    - Supports dynamic agent lookup from state
    """

    node_type: NodeType = Field(
        default=NodeType.AGENT, description="Node type for agent execution"
    )

    # Agent configuration
    agent_name: str = Field(
        description="Name of agent to execute (key in container's agents dict)"
    )

    agent: Optional["Agent"] = Field(
        default=None,
        description="Agent instance (extracted from state if not provided)",
        exclude=True,
    )

    # Container state handling
    extract_from_container: bool = Field(
        default=True, description="Whether to extract agent from container state"
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
    def validate_agent_config(self) -> "AgentNodeV3Config":
        """Validate configuration."""
        if not self.agent_name and not self.agent:
            raise ValueError("Either agent_name or agent must be provided")
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

        # Need agents field if extracting
        if self.extract_from_container:
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
        """Execute agent with hierarchical state projection."""
        # Check if debug mode is enabled
        debug_mode = (
            (config and config.get("debug", False))
            or (hasattr(state, "debug") and getattr(state, "debug", False))
            or False
        )

        if debug_mode:
            self._display_debug_info(state, "BEFORE_EXECUTION")

        logger.info(f"{'='*60}")
        logger.info(f"AGENT NODE V3: {self.name}")
        logger.info(f"Agent: {self.agent_name}")
        logger.info(f"{'='*60}")

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

            logger.info(f"✅ Agent completed with {len(state_update)} field updates")

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

    def _get_agent(self, state: StateLike) -> Optional["Agent"]:
        """Get agent from state or use provided agent."""
        if self.agent:
            return self.agent

        if self.extract_from_container:
            # Extract from container state
            agents = getattr(state, self.agents_field, {})
            if isinstance(agents, dict):
                return agents.get(self.agent_name)

        return None

    def _set_active_agent(self, state: StateLike) -> None:
        """Set active agent if container supports it."""
        if hasattr(state, "set_active_agent"):
            state.set_active_agent(self.agent_name)
        elif hasattr(state, "active_agent"):
            state.active_agent = self.agent_name

    def _project_state_for_agent(
        self, state: StateLike, agent: "Agent"
    ) -> dict[str, Any]:
        """Project container state to agent's expected schema.

        This is the key method that enables hierarchical state management.
        Each agent gets exactly what it expects, not a flattened global state.
        """
        # Start with agent's isolated state
        agent_states = getattr(state, self.agent_state_field, {})
        agent_state = agent_states.get(self.agent_name, {})
        projected = agent_state.copy()

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

        # Let the agent handle its own state schema validation
        # AgentNodeV3 just provides the projected data
        return projected

    def _extract_message_objects(self, messages: Any) -> list[BaseMessage]:
        """Extract BaseMessage objects from various containers."""
        if hasattr(messages, "root"):
            return messages.root
        if isinstance(messages, list | tuple):
            return list(messages)
        else:
            try:
                return list(messages)
            except:
                logger.warning(f"Cannot extract messages from {type(messages)}")
                return []

    def _process_agent_output(
        self, result: Any, state: StateLike, agent: "Agent"
    ) -> dict[str, Any]:
        """Process agent output and prepare state update."""
        state_update = {}

        # Convert result to dict
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

        # Update agent's isolated state
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

        # Update shared fields
        if hasattr(agent, "state_schema"):
            schema_shared = getattr(agent.state_schema, "__shared_fields__", set())
            for field in schema_shared:
                if field in result_dict:
                    state_update[field] = result_dict[field]

        # Always update messages if present
        if "messages" in result_dict:
            state_update["messages"] = result_dict["messages"]

        return state_update

    def _check_recompilation(self, state: StateLike, agent: "Agent") -> None:
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
        state_update: Dict[str, Any] | None = None,
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
                order_branch.add(f"{i+1}. {agent_name}")

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
                    f"📊 {key}: Agent '{self.agent_name}' ({len(agent_updates)} fields)"
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
                    f"📤 {key}: Agent '{self.agent_name}' ({len(agent_output)} fields)"
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

    def _display_agent_input(self, agent_input: dict[str, Any], agent: "Agent") -> None:
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
        output_tree = Tree(f"📤 Agent '{self.agent_name}' Output", style="bold green")

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
    agent: Optional["Agent"] = None,
    name: str | None = None,
    **kwargs,
) -> AgentNodeV3Config:
    """Create an agent node V3 configuration.

    Args:
        agent_name: Name of agent to execute (key in container)
        agent: Optional agent instance (extracted from state if not provided)
        name: Optional node name
        **kwargs: Additional configuration options

    Returns:
        AgentNodeV3Config instance
    """
    if not name:
        name = f"agent_{agent_name}"

    return AgentNodeV3Config(name=name, agent_name=agent_name, agent=agent, **kwargs)
