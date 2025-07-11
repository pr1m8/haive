# src/haive/agents/simple/agent.py

import logging
from typing import Any, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field, field_validator

from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


def has_tool_calls(state) -> bool:
    """Check if the last AI message has tool calls."""
    if not hasattr(state, "messages") or not state.messages:
        return False

    last_msg = state.messages[-1]

    if not isinstance(last_msg, AIMessage):
        return False

    tool_calls = getattr(last_msg, "tool_calls", None)
    return bool(tool_calls)


def placeholder_node(state):
    """Placeholder node that does nothing."""
    return Command(update={})


class SimpleAgent(Agent):
    """Simple agent that modifies its engine to include structured output schema.

    This agent provides a streamlined interface for creating agents with structured outputs
    by automatically modifying the underlying AugLLM engine to include the desired output
    schema. It's designed for straightforward LLM interactions with optional tool use.

    The SimpleAgent automatically:
        - Updates engine schemas to include structured output fields
        - Handles tool routing and execution
        - Manages conversation flow with tool calls
        - Provides validation and parsing capabilities

    Args:
        engine: The AugLLM engine configuration for this agent.
        tools: Optional list of tools available to the agent.
        tool_node_config: Configuration for tool execution node.
        parser_node_config: Configuration for output parsing node.
        validation_node_config: Configuration for validation node.
        structured_output_model: Pydantic model for structured outputs.
        output_parser: Custom output parser for response processing.

    Example:
        Creating a simple agent with structured output::

            from pydantic import BaseModel
            from haive.agents.simple import SimpleAgent
            from haive.core.engine.aug_llm import AugLLMConfig

            class TaskResult(BaseModel):
                completed: bool
                result: str
                confidence: float

            agent = SimpleAgent(
                engine=AugLLMConfig(
                    model="gpt-4",
                    temperature=0.7
                ),
                structured_output_model=TaskResult
            )

            result = agent.invoke({"query": "Analyze this data"})

    Note:
        The agent automatically modifies the engine schema to incorporate structured
        output fields, ensuring seamless integration between the LLM and output models.
    """

    # ========================================================================
    # CORE ENGINE
    # ========================================================================

    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="The AugLLM engine for this agent"
    )

    # ========================================================================
    # CONVENIENCE FIELDS
    # ========================================================================

    # LLM parameters
    temperature: float | None = Field(default=None, description="Temperature")
    max_tokens: int | None = Field(default=None, description="Max tokens")
    model_name: str | None = Field(default=None, description="Model name")

    # Tool configuration
    tools: list[Any] | None = Field(default=None, description="Tools")
    force_tool_use: bool | None = Field(default=None, description="Force tool use")

    # Structured output - THIS IS THE KEY FIELD
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model"
    )
    structured_output_version: int | str | None = Field(
        default=None, description="Structured output version"
    )

    # Prompting
    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None, description="Prompt template"
    )
    system_message: str | None = Field(default=None, description="System message")

    # LLM config
    llm_config: LLMConfig | None = Field(default=None, description="LLM config")

    # ========================================================================
    # NON-SYNCED FIELDS
    # ========================================================================

    output_parser: BaseOutputParser | None = Field(
        default=None, description="Output parser"
    )
    output_parser_field: str | None = Field(
        default=None, description="Output parser field name"
    )

    # ========================================================================
    # VALIDATION AND SETUP
    # ========================================================================

    @field_validator("engine")
    @classmethod
    def validate_engine_type(cls, v):
        """Ensure engine is AugLLMConfig."""
        if v is not None and not isinstance(v, AugLLMConfig):
            raise ValueError("SimpleAgent engine must be AugLLMConfig")
        return v

    def setup_agent(self):
        """Custom setup that modifies the engine and regenerates schemas.

        This is where we MODIFY THE ENGINE to include structured output
        and then force schema regeneration.
        """
        if self.engine:
            # Add engine to engines dict
            self.engines["main"] = self.engine

            # FIXED: Register engine in EngineRegistry so other nodes can find it
            self._register_engine_in_registry()

            # Sync fields to engine FIRST
            self._sync_fields_to_engine()

            # MODIFY ENGINE SCHEMA if we have structured output
            if self.structured_output_model:
                self._modify_engine_schema()

            # Force schema regeneration after engine modification
            self.set_schema = True

        # Don't call parent setup_agent() - we handle it ourselves

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
        if self.tools is not None and hasattr(self.engine, "tools"):
            self.engine.tools = self.tools
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
        """MODIFY the engine's output schema to include structured output fields.

        This is the KEY METHOD that updates the engine schema.
        """
        if not self.structured_output_model or not self.engine:
            return

        logger.info(
            f"Modifying engine schema to include {self.structured_output_model.__name__}"
        )

        # Get the engine's current output schema
        current_output_schema = self.engine.derive_output_schema()

        # Create a new schema composer to build enhanced schema
        composer = SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")

        # Add the enhanced messages field using StandardFields
        composer.add_standard_field("messages", use_enhanced=True)

        # Add existing fields from current schema (except messages which we just added)
        if hasattr(current_output_schema, "model_fields"):
            for field_name, field_info in current_output_schema.model_fields.items():
                if (
                    field_name != "messages"
                ):  # Skip messages since we added enhanced version
                    composer.add_field(
                        name=field_name,
                        field_type=field_info.annotation,
                        default=field_info.default,
                        default_factory=field_info.default_factory,
                        description=field_info.description,
                    )

        # Add the structured output field
        field_name = (
            self.structured_output_model.__name__.lower()
            .replace("response", "")
            .replace("result", "")
            .strip()
        )
        if not field_name:
            field_name = "structured_result"

        composer.add_field(
            name=field_name,
            field_type=Optional[self.structured_output_model],
            default=None,
            description=f"Structured output of type {self.structured_output_model.__name__}",
        )

        # Build the enhanced schema
        enhanced_schema = composer.build()

        # OVERRIDE the engine's output schema
        self.engine.output_schema = enhanced_schema

        # Clear any cached schemas in the engine
        if hasattr(self.engine, "_output_schema_instance"):
            self.engine._output_schema_instance = None
        if hasattr(self.engine, "_schema_cache"):
            self.engine._schema_cache.clear()

        logger.info(f"Engine schema modified successfully - added field '{field_name}'")

    # ========================================================================
    # FORCE SCHEMA REGENERATION AFTER ENGINE MODIFICATION
    # ========================================================================

    # ========================================================================
    # NODE DETECTION (unchanged)
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

        # Check for output parser
        has_output_parser = self.output_parser is not None

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
    # GRAPH BUILDING with proper state initialization
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the agent graph with proper state initialization."""
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
            # Store available nodes in graph metadata
            graph.metadata["available_nodes"] = available_nodes
            return graph

        # Add tool node if needed
        if needs_tool_node:
            # V2 tool node with better field handling
            tool_config = ToolNodeConfig(
                name="tool_node",
                engine_name=self.engine.name,
            )
            graph.add_node("tool_node", tool_config)
            graph.add_edge("tool_node", END)
            available_nodes.append("tool_node")

        # Add parser node if needed
        if needs_parser_node:
            # V2 parser node with better field handling
            parser_config = ParserNodeConfigV2(
                name="parse_output",
                engine_name=self.engine.name,
            )
            graph.add_node("parse_output", parser_config)
            graph.add_edge("parse_output", END)
            available_nodes.append("parse_output")

        # Create validation config with available nodes (v2)
        validation_config = ValidationNodeConfigV2(
            name="validation",
            engine_name=self.engine.name,
            tool_node="tool_node",
            parser_node="parse_output",
            available_nodes=available_nodes,
        )

        # Add validation node with proper config
        graph.add_node("validation", validation_config)
        available_nodes.append("validation")

        # Agent routing with conditional branching
        if has_force_tool_use:
            # Force tools - always go to validation
            graph.add_edge("agent_node", "validation")
        else:
            # Use conditional branching for tool calls
            graph.add_conditional_edges(
                "agent_node", has_tool_calls, {True: "validation", False: END}
            )

        # ValidationNodeConfigV2 returns Command, not conditional routing
        # Remove the conditional edges as V2 uses Send-based routing internally

        # Store available nodes and tool routes in graph metadata
        graph.metadata["available_nodes"] = available_nodes
        graph.metadata["tool_routes"] = self.get_tool_routes()

        return graph

    def create_runnable(self, runnable_config=None) -> Any:
        """Override to ensure state is properly initialized with tool routes and available nodes."""
        # Get the compiled graph
        compiled = super().create_runnable(runnable_config)

        # Ensure initial state has tool_routes, available_nodes, and engine
        if hasattr(self, "graph") and self.graph and hasattr(self.graph, "metadata"):
            # The state should be initialized with these values from graph metadata
            initial_values = {}

            # Initialize engine field with actual engine object
            if self.engine:
                initial_values["engine"] = self.engine

            if "tool_routes" in self.graph.metadata:
                initial_values["tool_routes"] = self.graph.metadata["tool_routes"]
            elif self.engine and hasattr(self.engine, "tool_routes"):
                initial_values["tool_routes"] = self.engine.tool_routes

            if "available_nodes" in self.graph.metadata:
                initial_values["available_nodes"] = self.graph.metadata[
                    "available_nodes"
                ]

            # Store in compiled graph's initial channel values if possible
            if initial_values and hasattr(compiled, "_channels"):
                for key, value in initial_values.items():
                    if key in compiled._channels:
                        # Set initial value in channel
                        compiled._channels[key].default_value = value

        return compiled

    # ========================================================================
    # CONVENIENCE CONSTRUCTORS
    # ========================================================================

    @classmethod
    def from_engine(cls, engine: AugLLMConfig, name: str | None = None, **kwargs):
        """Create SimpleAgent from engine."""
        return cls(name=name or "Simple Agent", engine=engine, **kwargs)

    @classmethod
    def create_with_tools(cls, tools: list[Any], name: str | None = None, **kwargs):
        """Create SimpleAgent with tools."""
        return cls(name=name or "Tool Agent", tools=tools, **kwargs)

    def __repr__(self) -> str:
        engine_info = f"model={getattr(self.engine, 'model', 'unknown')}"
        schema_info = f"structured_output={self.structured_output_model.__name__ if self.structured_output_model else 'None'}"
        return f"SimpleAgent(name='{self.name}', {engine_info}, {schema_info})"
