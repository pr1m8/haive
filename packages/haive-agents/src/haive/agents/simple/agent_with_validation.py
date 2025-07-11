"""SimpleAgent with integrated StateUpdatingValidationNode implementation."""

import logging
from typing import Any, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config import ParserNodeConfig
from haive.core.graph.node.state_updating_validation_node import (
    StateUpdatingValidationNode,
    ValidationMode,
)
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command, Send
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


class SimpleAgentWithValidation(Agent):
    """SimpleAgent with integrated StateUpdatingValidationNode.

    This agent demonstrates how to properly integrate the StateUpdatingValidationNode
    with the existing agent architecture, replacing placeholder nodes with actual
    validation and routing functionality.

    Key improvements over SimpleAgent:
    - Uses StateUpdatingValidationNode instead of placeholder
    - Provides both state updating and routing capabilities
    - Integrates with state schema for validation persistence
    - Supports different validation modes (STRICT, PARTIAL, PERMISSIVE)
    """

    # Core engine (unchanged)
    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="The AugLLM engine for this agent"
    )

    # Convenience fields (unchanged from SimpleAgent)
    temperature: float | None = Field(default=None, description="Temperature")
    max_tokens: int | None = Field(default=None, description="Max tokens")
    model_name: str | None = Field(default=None, description="Model name")
    tools: list[Any] | None = Field(default=None, description="Tools")
    force_tool_use: bool | None = Field(default=None, description="Force tool use")
    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model"
    )
    structured_output_version: int | str | None = Field(
        default=None, description="Structured output version"
    )
    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None, description="Prompt template"
    )
    system_message: str | None = Field(default=None, description="System message")
    llm_config: LLMConfig | None = Field(default=None, description="LLM config")
    output_parser: BaseOutputParser | None = Field(
        default=None, description="Output parser"
    )
    output_parser_field: str | None = Field(
        default=None, description="Output parser field name"
    )

    # NEW: Validation configuration
    validation_mode: ValidationMode = Field(
        default=ValidationMode.PARTIAL,
        description="Validation mode: STRICT, PARTIAL, or PERMISSIVE",
    )
    update_validation_messages: bool = Field(
        default=True, description="Whether to add validation error messages to state"
    )
    track_error_tools: bool = Field(
        default=True, description="Whether to track error tool calls in state"
    )

    @field_validator("engine")
    @classmethod
    def validate_engine_type(cls, v):
        """Ensure engine is AugLLMConfig."""
        if v is not None and not isinstance(v, AugLLMConfig):
            raise ValueError("SimpleAgentWithValidation engine must be AugLLMConfig")
        return v

    def setup_agent(self):
        """Custom setup that modifies the engine and regenerates schemas."""
        if self.engine:
            # Add engine to engines dict
            self.engines["main"] = self.engine

            # Register engine in EngineRegistry so other nodes can find it
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

        # Sync fields if they exist on engine (same as SimpleAgent)
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
        """MODIFY the engine's output schema to include structured output fields."""
        if not self.structured_output_model or not self.engine:
            return

        logger.info(
            f"Modifying engine schema to include {self.structured_output_model.__name__}"
        )

        # Get the engine's current output schema
        current_output_schema = self.engine.derive_output_schema()

        # Create a new schema composer to build enhanced schema
        composer = SchemaComposer(name=f"Enhanced{current_output_schema.__name__}")

        # Add existing fields from current schema
        composer.add_fields_from_model(current_output_schema)

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

    # Node detection methods (unchanged from SimpleAgent)
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

    def _create_validation_node(self) -> StateUpdatingValidationNode:
        """Create the StateUpdatingValidationNode with proper configuration."""
        # Determine route to node mapping based on available nodes
        route_mapping = {}

        if self._needs_tool_node():
            route_mapping.update(
                {
                    "langchain_tool": "tool_node",
                    "function": "tool_node",
                    "tool_node": "tool_node",
                }
            )

        if self._needs_parser_node():
            route_mapping["pydantic_model"] = "parse_output"

        # Add default routes
        route_mapping.update(
            {
                "retriever": "retriever_node",
                "unknown": "tool_node" if self._needs_tool_node() else "agent_node",
            }
        )

        return StateUpdatingValidationNode(
            name="state_validator",
            engine_name=self.engine.name if self.engine else None,
            validation_mode=self.validation_mode,
            update_messages=self.update_validation_messages,
            track_error_tools=self.track_error_tools,
            add_validation_metadata=True,
            agent_node="agent_node",
            tool_node="tool_node",
            parser_node="parse_output",
            route_to_node_mapping=route_mapping,
        )

    def build_graph(self) -> BaseGraph:
        """Build the agent graph with StateUpdatingValidationNode integration."""
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

        # NEW: Create StateUpdatingValidationNode instead of placeholder
        validation_node = self._create_validation_node()

        # Get both functions from the validation node
        state_updater_func = validation_node.create_node_function()
        router_func = validation_node.create_router_function()

        # Add state updater node (updates state with validation results)
        graph.add_node("state_validator", state_updater_func)
        available_nodes.append("state_validator")

        # Add router node (routes based on validation state)
        graph.add_node("validation_router", router_func)
        available_nodes.append("validation_router")

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
            parser_config = ParserNodeConfig(
                name="parse_output",
                engine_name=self.engine.name,
            )
            graph.add_node("parse_output", parser_config)
            graph.add_edge("parse_output", END)
            available_nodes.append("parse_output")

        # NEW: Flow with dual validation approach
        if has_force_tool_use:
            # Force tools - always go to state validator
            graph.add_edge("agent_node", "state_validator")
        else:
            # Use conditional branching for tool calls
            graph.add_conditional_edges(
                "agent_node", has_tool_calls, {True: "state_validator", False: END}
            )

        # State validator always goes to router
        graph.add_edge("state_validator", "validation_router")

        # Router uses the router function to make dynamic routing decisions
        # The router function will return Send objects or node names
        # No explicit edges needed - Send objects handle routing

        # Store metadata
        graph.metadata["available_nodes"] = available_nodes
        graph.metadata["tool_routes"] = self.get_tool_routes()
        graph.metadata["validation_config"] = {
            "mode": self.validation_mode.value,
            "update_messages": self.update_validation_messages,
            "track_errors": self.track_error_tools,
        }

        return graph

    def create_runnable(self, runnable_config=None) -> Any:
        """Override to ensure state is properly initialized."""
        # Get the compiled graph
        compiled = super().create_runnable(runnable_config)

        # Ensure initial state has tool_routes and available_nodes
        if hasattr(self, "graph") and self.graph and hasattr(self.graph, "metadata"):
            initial_values = {}

            if "tool_routes" in self.graph.metadata:
                initial_values["tool_routes"] = self.graph.metadata["tool_routes"]
            elif self.engine and hasattr(self.engine, "tool_routes"):
                initial_values["tool_routes"] = self.engine.tool_routes

            if "available_nodes" in self.graph.metadata:
                initial_values["available_nodes"] = self.graph.metadata[
                    "available_nodes"
                ]

        return compiled

    # Convenience constructors
    @classmethod
    def from_engine(cls, engine: AugLLMConfig, name: str | None = None, **kwargs):
        """Create SimpleAgentWithValidation from engine."""
        return cls(name=name or "Simple Agent with Validation", engine=engine, **kwargs)

    @classmethod
    def create_with_tools(cls, tools: list[Any], name: str | None = None, **kwargs):
        """Create SimpleAgentWithValidation with tools."""
        return cls(name=name or "Tool Agent with Validation", tools=tools, **kwargs)

    @classmethod
    def create_strict_validation(
        cls, engine: AugLLMConfig, name: str | None = None, **kwargs
    ):
        """Create agent with strict validation mode."""
        return cls(
            name=name or "Strict Validation Agent",
            engine=engine,
            validation_mode=ValidationMode.STRICT,
            **kwargs,
        )

    @classmethod
    def create_permissive_validation(
        cls, engine: AugLLMConfig, name: str | None = None, **kwargs
    ):
        """Create agent with permissive validation mode."""
        return cls(
            name=name or "Permissive Validation Agent",
            engine=engine,
            validation_mode=ValidationMode.PERMISSIVE,
            **kwargs,
        )

    def __repr__(self) -> str:
        engine_info = f"model={getattr(self.engine, 'model', 'unknown')}"
        schema_info = f"structured_output={self.structured_output_model.__name__ if self.structured_output_model else 'None'}"
        validation_info = f"validation_mode={self.validation_mode.value}"
        return f"SimpleAgentWithValidation(name='{self.name}', {engine_info}, {schema_info}, {validation_info})"


# For backward compatibility, provide a function to upgrade SimpleAgent
def upgrade_simple_agent_with_validation(
    simple_agent: "SimpleAgent",
) -> SimpleAgentWithValidation:
    """Upgrade a SimpleAgent to use StateUpdatingValidationNode."""
    # Extract all fields from SimpleAgent
    agent_data = simple_agent.model_dump()

    # Remove any fields that might conflict
    agent_data.pop("graph", None)
    agent_data.pop("compiled_graph", None)

    # Create new agent with validation
    return SimpleAgentWithValidation(**agent_data)
