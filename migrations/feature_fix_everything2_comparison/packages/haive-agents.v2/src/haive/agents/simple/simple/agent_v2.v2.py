"""SimpleAgent V2 - Uses V2 validation node + router system.

This version uses the V2 validation system that can properly:
1. Add ToolMessages to state for Pydantic model validation
2. Use separate validation node + router for proper state management
3. Handle both regular tools and Pydantic models correctly

Key improvements over V1:
- Uses ValidationNodeV2 for state updates
- Uses validation_router_v2 for routing decisions
- Proper ToolMessage creation for Pydantic models
- Better error handling and routing
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config import ParserNodeConfig
from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.node.validation_node_v2 import ValidationNodeV2
from haive.core.graph.node.validation_router_v2 import validation_router_v2
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.messages import AIMessage

# Import BaseOutputParser to ensure it's available for LangGraph type evaluation
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field, field_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


def has_tool_calls_v2(state: dict[str, Any]) -> bool:
    """Check if the last AI message has tool calls - V2 version."""
    if not hasattr(state, "messages") or not state.messages:
        return False

    last_msg = state.messages[-1]

    if not isinstance(last_msg, AIMessage):
        return False

    tool_calls = getattr(last_msg, "tool_calls", None)
    return bool(tool_calls)


class SimpleAgentV2(Agent):
    """V2 SimpleAgent with improved validation node + router system.

    This version addresses the key issues with tool message handling by using
    a two-step validation process:
    1. ValidationNodeV2: Updates state with ToolMessages
    2. validation_router_v2: Makes routing decisions based on updated state

    This allows proper ToolMessage creation for Pydantic models while
    maintaining clean separation between state updates and routing.
    """

    # ========================================================================
    # CORE ENGINE (same as V1)
    # ========================================================================

    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="The AugLLM engine for this agent"
    )

    # ========================================================================
    # CONVENIENCE FIELDS (same as V1)
    # ========================================================================

    # LLM parameters
    temperature: float | None = Field(default=None, description="Temperature")
    max_tokens: int | None = Field(default=None, description="Max tokens")
    model_name: str | None = Field(default=None, description="Model name")

    # Tool configuration
    # Note: tools field is inherited from ToolRouteMixin with default_factory=list
    force_tool_use: bool | None = Field(default=None, description="Force tool use")

    # Structured output - THIS IS THE KEY FIELD
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model"
    )
    structured_output_version: Literal["v1", "v2"] | None = Field(
        default=None, description="Structured output version"
    )

    # Prompting
    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None, description="Prompt template"
    )
    system_message: str | None = Field(default=None, description="System message")

    # LLM config
    llm_config: LLMConfig | None = Field(default=None, description="LLM config")

    # V2 Configuration options
    use_parser_safety_net: bool = Field(
        default=True, description="Use V2 parser with ToolMessage safety net"
    )
    parser_safety_net_mode: str = Field(
        default="create",
        description="Parser safety net mode: 'create', 'warn', 'ignore'",
    )

    # ========================================================================
    # NON-SYNCED FIELDS (same as V1)
    # ========================================================================

    # Note: In agent context, output parsing is handled by parser nodes,
    # not by storing parser instances. These fields track configuration only.
    output_parser_field: str | None = Field(
        default=None, description="Output parser field name", exclude=True
    )

    # ========================================================================
    # VALIDATION AND SETUP (same as V1)
    # ========================================================================

    @field_validator("engine")
    @classmethod
    def validate_engine_type(cls, v) -> Any:
        """Ensure engine is AugLLMConfig."""
        if v is not None and not isinstance(v, AugLLMConfig):
            raise ValueError("SimpleAgentV2 engine must be AugLLMConfig")
        return v

    def setup_agent(self) -> None:
        """Custom setup that modifies the engine and regenerates schemas."""
        if self.engine:
            # Add engine to engines dict
            self.engines["main"] = self.engine

            # Register engine in EngineRegistry
            self._register_engine_in_registry()

            # Sync fields to engine FIRST
            self._sync_fields_to_engine()

            # MODIFY ENGINE SCHEMA if we have structured output
            if self.structured_output_model:
                self._modify_engine_schema()

            # Force schema regeneration after engine modification
            self.set_schema = True

    def _register_engine_in_registry(self) -> None:
        """Register the engine in EngineRegistry so other nodes can find it by name."""
        if not self.engine:
            return

        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()

            # Check if engine is already registered
            if not registry.find(self.engine.name):
                registry.register(self.engine)
                logger.info(f"Registered engine '{self.engine.name}' in EngineRegistry")
            else:
                logger.debug(
                    f"Engine '{self.engine.name}' already registered in EngineRegistry"
                )

        except ImportError:
            logger.warning(
                "Could not import EngineRegistry - engine registration skipped"
            )
        except Exception as e:
            logger.warning(f"Failed to register engine in registry: {e}")

    def _sync_fields_to_engine(self) -> None:
        """Sync convenience fields to engine."""
        if not self.engine:
            return

        # Sync fields if they exist on engine
        if self.temperature is not None and hasattr(self.engine, "temperature"):
            self.engine.temperature = self.temperature
        if self.max_tokens is not None and hasattr(self.engine, "max_tokens"):
            self.engine.max_tokens = self.max_tokens
        if self.model_name is not None and hasattr(self.engine, "model"):
            self.engine.model = self.model_name
        # Tools are managed directly by the engine (via ToolRouteMixin)
        # No need to sync from agent to engine
        if self.force_tool_use is not None and hasattr(self.engine, "force_tool_use"):
            self.engine.force_tool_use = self.force_tool_use
        if self.structured_output_model is not None and hasattr(
            self.engine, "structured_output_model"
        ):
            self.engine.structured_output_model = self.structured_output_model
        if self.system_message is not None and hasattr(self.engine, "system_message"):
            self.engine.system_message = self.system_message
        if self.llm_config is not None and hasattr(self.engine, "llm_config"):
            self.engine.llm_config = self.llm_config

    def _modify_engine_schema(self) -> None:
        """MODIFY the engine's output schema to include structured output fields."""
        if not self.structured_output_model or not self.engine:
            return

        logger.info(
            f"Modifying engine schema to include {self.structured_output_model.__name__}"
        )

        # Get the engine's current output schema
        current_output_schema = self.engine.derive_output_schema()

        # Create a new schema composer to build enhanced schema
        SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")

        logger.info(
            f"Skipping engine schema modification for {self.structured_output_model.__name__} "
            f"- extraction handled by validation nodes"
        )

    # ========================================================================
    # NODE DETECTION (same as V1)
    # ========================================================================

    def _needs_tool_node(self) -> bool:
        """Check if we need a tool node for langchain tools."""
        if not self.engine:
            return False

        tool_routes = self.get_tool_routes()
        langchain_tools = [
            tool
            for tool, route in tool_routes.items()
            if route in ["langchain_tool", "function", "tool_node"]
        ]

        return len(langchain_tools) > 0

    def _needs_parser_node(self) -> bool:
        """Check if we need a parser node for pydantic models."""
        if not self.engine:
            return False

        # Check for structured output
        has_structured_output = bool(
            self.structured_output_model
            or getattr(self.engine, "structured_output_model", None)
        )

        # Check for output parser in engine (not in agent)
        has_output_parser = bool(
            getattr(self.engine, "output_parser", None) is not None
        )

        # Check for pydantic tools
        tool_routes = self.get_tool_routes()
        pydantic_tools = [
            tool for tool, route in tool_routes.items() if route == "pydantic_model"
        ]

        return has_structured_output or has_output_parser or len(pydantic_tools) > 0

    def _has_force_tool_use(self) -> bool:
        """Check if tool use is forced."""
        return bool(
            getattr(self.engine, "force_tool_use", False)
            or getattr(self.engine, "force_tool_choice", False)
            or (self.force_tool_use is not None and self.force_tool_use)
            or (self.structured_output_model is not None)
            or (getattr(self.engine, "structured_output_model", None) is not None)
        )

    def get_tool_routes(self) -> dict[str, str]:
        """Get tool routes from engine."""
        if self.engine and hasattr(self.engine, "tool_routes"):
            return getattr(self.engine, "tool_routes", {})
        return {}

    # ========================================================================
    # GRAPH BUILDING - V2 VERSION WITH VALIDATION NODE + ROUTER
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the agent graph with V2 validation node + router system."""
        graph = BaseGraph(name=self.name)

        # Track available nodes
        available_nodes = []

        # Add agent node
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")
        available_nodes.append("agent_node")

        # Check what nodes we need
        needs_tool_node = self._needs_tool_node()
        needs_parser_node = self._needs_parser_node()
        has_force_tool_use = self._has_force_tool_use()

        # Simple case - no tools
        if not needs_tool_node and not needs_parser_node:
            graph.add_edge("agent_node", END)
            graph.metadata["available_nodes"] = available_nodes
            return graph

        # Add V2 validation node (regular node that updates state)
        validation_node_v2 = ValidationNodeV2(
            name="validation_v2",
            engine_name=self.engine.name,
            router_node="validation_router",  # Goes to router after updating state
        )
        graph.add_node("validation_v2", validation_node_v2)
        available_nodes.append("validation_v2")

        # Add tool node if needed
        if needs_tool_node:
            tool_config = ToolNodeConfig(
                name="tool_node",
                engine_name=self.engine.name,
                allowed_routes=["langchain_tool", "function", "tool_node"],
            )
            graph.add_node("tool_node", tool_config)
            graph.add_edge("tool_node", END)
            available_nodes.append("tool_node")

        # Add parser node if needed
        if needs_parser_node:
            if self.use_parser_safety_net:
                # Use V2 parser with safety net
                parser_config = ParserNodeConfigV2(
                    name="parse_output",
                    engine_name=self.engine.name,
                    add_tool_message_safety_net=True,
                    safety_net_mode=self.parser_safety_net_mode,
                )
                logger.info(
                    f"Using V2 parser with safety net mode: {self.parser_safety_net_mode}"
                )
            else:
                # Use V1 parser (original behavior)
                parser_config = ParserNodeConfig(
                    name="parse_output",
                    engine_name=self.engine.name,
                )
                logger.info("Using V1 parser (no safety net)")

            graph.add_node("parse_output", parser_config)
            graph.add_edge("parse_output", END)
            available_nodes.append("parse_output")

        # Agent routing to validation
        if has_force_tool_use:
            # Force tools - always go to validation
            graph.add_edge("agent_node", "validation_v2")
        else:
            # Use conditional branching for tool calls
            graph.add_conditional_edges(
                "agent_node", has_tool_calls_v2, {True: "validation_v2", False: END}
            )

        # V2 Router: validation_v2 → validation_router_v2 → destinations
        routing_map = {"agent_node": "agent_node"}
        if needs_tool_node:
            routing_map["tool_node"] = "tool_node"
        if needs_parser_node:
            routing_map["parse_output"] = "parse_output"

        graph.add_conditional_edges("validation_v2", validation_router_v2, routing_map)

        # Store metadata
        graph.metadata["available_nodes"] = available_nodes
        graph.metadata["tool_routes"] = self.get_tool_routes()

        return graph

    def create_runnable(self, runnable_config: dict[str, Any] = None):
        """Override to ensure state includes required fields."""
        compiled = super().create_runnable(runnable_config)

        # Wrap to inject additional state fields (engine is now handled in _prepare_input)
        original_ainvoke = compiled.ainvoke

        async def wrapped_ainvoke(input_data, config=None):
            # Ensure additional state fields are available
            if isinstance(input_data, dict):
                if "engine_name" not in input_data and self.engine:
                    input_data["engine_name"] = self.engine.name
                if "tool_routes" not in input_data:
                    input_data["tool_routes"] = self.get_tool_routes()
                if "available_nodes" not in input_data and hasattr(self, "graph"):
                    input_data["available_nodes"] = self.graph.metadata.get(
                        "available_nodes", []
                    )

            return await original_ainvoke(input_data, config)

        compiled.ainvoke = wrapped_ainvoke
        return compiled

    # ========================================================================
    # DIRECT MANAGEMENT METHODS
    # ========================================================================

    def add_prompt_template(
        self, name: str, template: ChatPromptTemplate | PromptTemplate
    ) -> None:
        """Add a named prompt template to the engine.

        Args:
            name: Unique name for the template
            template: The prompt template to store
        """
        self.engine.add_prompt_template(name, template)
        logger.info(f"Added prompt template '{name}' to agent '{self.name}'")

    def use_prompt_template(self, name: str) -> None:
        """Switch to using a specific template.

        Args:
            name: Name of the template to activate

        Raises:
            ValueError: If template name not found
        """
        self.engine.use_prompt_template(name)
        logger.info(f"Agent '{self.name}' now using template '{name}'")

    def remove_prompt_template(self, name: str | None = None) -> None:
        """Remove a template or disable the active one.

        Args:
            name: Template name to remove. If None, disables active template.
        """
        self.engine.remove_prompt_template(name)
        action = f"removed template '{name}'" if name else "disabled active template"
        logger.info(f"Agent '{self.name}' {action}")

    def list_prompt_templates(self) -> list[str]:
        """List available template names."""
        return self.engine.list_prompt_templates()

    def get_active_template(self) -> str | None:
        """Get the name of the currently active template."""
        return self.engine.get_active_template()

    def add_tool(self, tool: Any) -> None:
        """Add a tool to the agent.

        Args:
            tool: Tool to add (LangChain tool, Pydantic model, or callable)
        """
        # Add to engine
        self.engine.add_tool(tool)

        # Engine handles the actual tools (via ToolRouteMixin)
        # No need to maintain a separate tools list on SimpleAgentV2

        tool_name = getattr(tool, "name", type(tool).__name__)
        logger.info(f"Added tool '{tool_name}' to agent '{self.name}'")

    def remove_tool(self, tool: Any) -> None:
        """Remove a tool from the agent.

        Args:
            tool: Tool instance to remove
        """
        # Remove from engine
        self.engine.remove_tool(tool)

        # Engine handles the actual tools (via ToolRouteMixin)
        # No need to maintain a separate tools list on SimpleAgentV2

        tool_name = getattr(tool, "name", type(tool).__name__)
        logger.info(f"Removed tool '{tool_name}' from agent '{self.name}'")

    def clear_tools(self) -> None:
        """Clear all tools from the agent."""
        self.engine.clear_tools()
        # Engine handles the actual tools (via ToolRouteMixin)
        logger.info(f"Cleared all tools from agent '{self.name}'")

    def set_structured_output(
        self,
        model: type[BaseModel],
        version: str = "v2",
        include_instructions: bool = True,
    ) -> None:
        """Set structured output model.

        Args:
            model: Pydantic model for structured output
            version: Version to use ("v1" or "v2")
            include_instructions: Whether to include format instructions
        """
        # Update engine with structured output
        self.engine = self.engine.with_structured_output(
            model=model, version=version, include_instructions=include_instructions
        )

        # Update convenience fields
        self.structured_output_model = model
        self.structured_output_version = version

        # Force schema regeneration
        self.set_schema = True

        logger.info(
            f"Set structured output to {model.__name__} (version {version}) for agent '{self.name}'"
        )

    def clear_structured_output(self) -> None:
        """Clear structured output configuration."""
        self.engine.structured_output_model = None
        self.engine.structured_output_version = None
        self.structured_output_model = None
        self.structured_output_version = None

        # Force schema regeneration
        self.set_schema = True

        logger.info(f"Cleared structured output for agent '{self.name}'")

    def get_structured_output_model(self) -> type[BaseModel] | None:
        """Get current structured output model."""
        return self.structured_output_model

    def add_system_message(self, message: str) -> None:
        """Add or update the system message.

        Args:
            message: System message content
        """
        self.engine.system_message = message
        self.system_message = message
        logger.info(f"Updated system message for agent '{self.name}'")

    def get_configuration_summary(self) -> dict[str, Any]:
        """Get a summary of current agent configuration."""
        return {
            "name": self.name,
            "active_template": self.get_active_template(),
            "available_templates": self.list_prompt_templates(),
            "tools_count": (
                len(self.engine.tools)
                if self.engine and hasattr(self.engine, "tools")
                else 0
            ),
            "structured_output": (
                self.get_structured_output_model().__name__
                if self.get_structured_output_model()
                else None
            ),
            "engine_model": getattr(self.engine, "model", None),
            "engine_temperature": getattr(self.engine, "temperature", None),
            "system_message": bool(self.system_message),
        }

    # ========================================================================
    # CONVENIENCE CONSTRUCTORS (same as V1)
    # ========================================================================

    @classmethod
    def from_engine(cls, engine: AugLLMConfig, name: str | None = None, **kwargs):
        """Create SimpleAgentV2 from engine."""
        return cls(name=name or "Simple Agent V2", engine=engine, **kwargs)

    @classmethod
    def create_with_tools(cls, tools: list[Any], name: str | None = None, **kwargs):
        """Create SimpleAgentV2 with tools."""
        return cls(name=name or "Tool Agent V2", tools=tools, **kwargs)

    def __repr__(self) -> str:
        engine_info = f"model={getattr(self.engine, 'model', 'unknown')}"
        schema_info = f"structured_output={self.structured_output_model.__name__ if self.structured_output_model else 'None'}"
        return f"SimpleAgentV2(name='{self.name}', {engine_info}, {schema_info})"
