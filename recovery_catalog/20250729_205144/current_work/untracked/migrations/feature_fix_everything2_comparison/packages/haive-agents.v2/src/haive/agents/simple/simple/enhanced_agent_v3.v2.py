"""Enhanced SimpleAgent V3 - Full feature implementation using enhanced base Agent.

This version leverages all advanced features from the enhanced base Agent class:
- Dynamic schema generation and composition
- Advanced engine management and routing
- Rich execution capabilities with debugging
- Sophisticated state management
- Comprehensive persistence and serialization
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field, field_validator

# Import the enhanced base Agent
from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)


# ========================================================================
# HELPER FUNCTIONS
# ========================================================================


def has_tool_calls(state: dict[str, Any]) -> Literal["true", "false"]:
    """Check if the last message has tool calls."""
    messages = state.get("messages", [])
    if not messages:
        return "false"

    last_message = messages[-1]
    if isinstance(last_message, AIMessage) and last_message.tool_calls:
        return "true"
    return "false"


def should_continue(state: dict[str, Any]) -> bool:
    """Enhanced routing logic for tool calls and structured output."""
    last_msg = state.get("messages", [])[-1] if state.get("messages") else None
    if not last_msg:
        return False

    # Check for tool calls
    tool_calls = getattr(last_msg, "tool_calls", None)
    if tool_calls:
        return True

    # Check for structured output needs
    if hasattr(state, "structured_output_model") and state.structured_output_model:
        return True

    return False


# ========================================================================
# ENHANCED SIMPLE AGENT V3
# ========================================================================


class EnhancedSimpleAgent(Agent):
    """Enhanced SimpleAgent V3 with full advanced features.

    This agent leverages all capabilities of the enhanced base Agent class:

    Core Features:
    - Dynamic schema generation from engines
    - Advanced engine management and routing
    - Rich execution capabilities with detailed debugging
    - Sophisticated state management with field visibility
    - Comprehensive persistence and checkpointing
    - Full serialization support

    SimpleAgent-Specific Features:
    - AugLLMConfig engine with validation and convenience fields
    - Automatic field syncing (temperature, max_tokens, etc.)
    - Adaptive graph building based on configuration
    - Support for tools, structured output, and custom parsing

    Enhanced Capabilities:
    - Multi-engine support for advanced workflows
    - Advanced tool routing and state management
    - Rich debugging and observability features
    - Dynamic schema evolution and composition
    - Performance optimization and caching

    Attributes:
        engine: Primary AugLLMConfig engine (required)
        temperature: LLM temperature (syncs to engine)
        max_tokens: Maximum response tokens (syncs to engine)
        model_name: Model name override (syncs to engine.model)
        force_tool_use: Force tool usage flag (syncs to engine)
        structured_output_model: Pydantic model for structured output
        system_message: System message override (syncs to engine)
        llm_config: LLM configuration dict or object
        output_parser: Custom output parser
        prompt_template: Custom prompt template

    Enhanced Features:
        multi_engine_mode: Enable multiple engines per agent
        advanced_routing: Enable sophisticated tool/engine routing
        performance_mode: Enable caching and optimization
        debug_mode: Enable rich debugging and observability
        persistence_config: Advanced persistence configuration

    Examples:
        Basic usage (backwards compatible)::

            agent = EnhancedSimpleAgent(name="assistant")
            result = agent.run("Hello, how are you?")

        With enhanced features::

            agent = EnhancedSimpleAgent(
                name="advanced_agent",
                temperature=0.7,
                max_tokens=1000,
                system_message="You are an expert assistant",
                multi_engine_mode=True,
                debug_mode=True,
                persistence_config={"checkpoint_mode": "async"}
            )

        With structured output::

            class Analysis(BaseModel):
                summary: str = Field(description="Analysis summary")
                confidence: float = Field(description="Confidence score")
                recommendations: list[str] = Field(description="Recommendations")

            agent = EnhancedSimpleAgent(
                name="analyzer",
                structured_output_model=Analysis,
                performance_mode=True
            )
            analysis = agent.run("Analyze the current market trends")

        Multi-engine configuration::

            agent = EnhancedSimpleAgent(
                name="multi_engine_agent",
                engines={
                    "primary": AugLLMConfig(model="gpt-4", temperature=0.3),
                    "creative": AugLLMConfig(model="gpt-4", temperature=0.9),
                    "fallback": AugLLMConfig(model="gpt-3.5-turbo")
                },
                advanced_routing=True
            )
    """

    # ========================================================================
    # CORE ENGINE CONFIGURATION
    # ========================================================================

    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="Primary AugLLM engine for this agent"
    )

    # ========================================================================
    # CONVENIENCE FIELDS (sync to engine automatically)
    # ========================================================================

    temperature: float | None = Field(
        default=None,
        ge=0.0,
        le=2.0,
        description="Temperature for the LLM (syncs to engine)",
    )

    max_tokens: int | None = Field(
        default=None, ge=1, description="Max tokens for the LLM (syncs to engine)"
    )

    model_name: str | None = Field(
        default=None, description="Model name for the LLM (syncs to engine.model)"
    )

    force_tool_use: bool | None = Field(
        default=None, description="Force tool use (syncs to engine)"
    )

    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Structured output model (syncs to engine)"
    )

    system_message: str | None = Field(
        default=None, description="System message (syncs to engine)"
    )

    llm_config: LLMConfig | dict[str, Any] | None = Field(
        default=None, description="LLM config (syncs to engine)"
    )

    # ========================================================================
    # ENHANCED FEATURES
    # ========================================================================

    # Agent-specific configuration
    output_parser: BaseOutputParser | None = Field(
        default=None, description="Optional output parser"
    )

    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None, description="Optional prompt template"
    )

    # Enhanced capabilities
    multi_engine_mode: bool = Field(
        default=False, description="Enable multiple engines per agent"
    )

    advanced_routing: bool = Field(
        default=False, description="Enable sophisticated tool/engine routing"
    )

    performance_mode: bool = Field(
        default=False, description="Enable caching and optimization"
    )

    debug_mode: bool = Field(
        default=False, description="Enable rich debugging and observability"
    )

    persistence_config: dict[str, Any] | None = Field(
        default=None, description="Advanced persistence configuration"
    )

    # ========================================================================
    # VALIDATION
    # ========================================================================

    @field_validator("engine")
    @classmethod
    def ensure_aug_llm_config(cls, v):
        """Ensure engine is AugLLMConfig or create one."""
        if v is None:
            return AugLLMConfig()
        if isinstance(v, dict):
            return AugLLMConfig(**v)
        if not isinstance(v, AugLLMConfig):
            raise ValueError(
                f"EnhancedSimpleAgent requires AugLLMConfig, got {type(v)}"
            )
        return v

    @field_validator("temperature")
    @classmethod
    def validate_temperature(cls, v):
        """Validate temperature range."""
        if v is not None and not (0.0 <= v <= 2.0):
            raise ValueError("Temperature must be between 0.0 and 2.0")
        return v

    # ========================================================================
    # AGENT SETUP AND CONFIGURATION
    # ========================================================================

    def setup_agent(self) -> None:
        """Enhanced setup with full feature integration.

        This setup method:
        1. Configures the primary engine and adds to engines dict
        2. Syncs all convenience fields to the engine
        3. Sets up multi-engine mode if enabled
        4. Configures advanced routing if enabled
        5. Sets up performance optimizations if enabled
        6. Configures debug mode if enabled
        7. Sets up advanced persistence if configured
        8. Enables automatic schema generation
        """
        logger.debug(f"Setting up EnhancedSimpleAgent: {self.name}")

        if self.engine:
            # Add primary engine to engines dict
            self.engines["main"] = self.engine
            logger.debug(f"Added primary engine: {self.engine.name}")

            # Sync convenience fields to engine
            self._sync_convenience_fields()

            # Setup multi-engine mode
            if self.multi_engine_mode:
                self._setup_multi_engine_mode()

            # Setup advanced routing
            if self.advanced_routing:
                self._setup_advanced_routing()

            # Setup performance optimizations
            if self.performance_mode:
                self._setup_performance_mode()

            # Setup debug mode
            if self.debug_mode:
                self._setup_debug_mode()

            # Setup advanced persistence
            if self.persistence_config:
                self._setup_advanced_persistence()

            # Enable automatic schema generation
            self.set_schema = True
            logger.debug("Enabled automatic schema generation")

    def _sync_convenience_fields(self) -> None:
        """Sync convenience fields to engine with validation."""
        if not self.engine:
            return

        logger.debug("Syncing convenience fields to engine")

        # Sync all convenience fields with validation
        if self.temperature is not None:
            self.engine.temperature = self.temperature
            logger.debug(f"Synced temperature: {self.temperature}")

        if self.max_tokens is not None:
            self.engine.max_tokens = self.max_tokens
            logger.debug(f"Synced max_tokens: {self.max_tokens}")

        if self.model_name is not None:
            self.engine.model = self.model_name
            logger.debug(f"Synced model: {self.model_name}")

        if self.force_tool_use is not None:
            self.engine.force_tool_use = self.force_tool_use
            logger.debug(f"Synced force_tool_use: {self.force_tool_use}")

        if self.structured_output_model is not None:
            self.engine.structured_output_model = self.structured_output_model
            logger.debug(
                f"Synced structured_output_model: {self.structured_output_model.__name__}"
            )

        if self.system_message is not None:
            self.engine.system_message = self.system_message
            logger.debug(f"Synced system_message: {self.system_message[:50]}...")

        if self.llm_config is not None:
            self.engine.llm_config = self.llm_config
            logger.debug("Synced llm_config")

    def _setup_multi_engine_mode(self) -> None:
        """Setup multi-engine capabilities."""
        logger.debug("Setting up multi-engine mode")
        # TODO: Implement multi-engine setup
        # - Engine routing configuration
        # - Load balancing strategies
        # - Fallback mechanisms

    def _setup_advanced_routing(self) -> None:
        """Setup advanced tool and engine routing."""
        logger.debug("Setting up advanced routing")
        # TODO: Implement advanced routing
        # - Intelligent tool selection
        # - Engine capability matching
        # - Dynamic routing rules

    def _setup_performance_mode(self) -> None:
        """Setup performance optimizations."""
        logger.debug("Setting up performance mode")
        # TODO: Implement performance optimizations
        # - Schema caching
        # - Graph compilation caching
        # - Engine pooling

    def _setup_debug_mode(self) -> None:
        """Setup rich debugging and observability."""
        logger.debug("Setting up debug mode")
        # Enable verbose logging
        self.verbose = True
        # TODO: Implement additional debug features
        # - Execution tracing
        # - Performance metrics
        # - Rich error reporting

    def _setup_advanced_persistence(self) -> None:
        """Setup advanced persistence configuration."""
        logger.debug("Setting up advanced persistence")
        if self.persistence_config:
            # Apply persistence configuration
            for key, value in self.persistence_config.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                    logger.debug(f"Applied persistence config: {key}={value}")

    # ========================================================================
    # ENHANCED GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build enhanced graph with adaptive features.

        Creates an intelligent graph structure that adapts based on:
        - Available tools and their routing requirements
        - Structured output models and parsing needs
        - Performance optimizations and caching
        - Debug mode and observability requirements

        Graph Structure:
        1. Basic: START → agent_node → END
        2. With tools: START → agent_node → validation → tool_node → agent_node
        3. With parsing: START → agent_node → validation → parse_output → END
        4. Enhanced: Includes performance optimizations and debug nodes

        Returns:
            BaseGraph: The compiled agent graph with all enhancements
        """
        logger.debug(f"Building enhanced graph for {self.name}")

        graph = BaseGraph(name=self.name)

        # Add main agent node
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")

        # Analyze what additional capabilities we need
        needs_tools = self._has_tools()
        needs_parsing = self._has_structured_output() or self.output_parser
        needs_validation = needs_tools or needs_parsing

        logger.debug(
            f"Graph analysis: tools={needs_tools}, parsing={needs_parsing}, validation={needs_validation}"
        )

        # Simple case - just LLM
        if not needs_validation:
            graph.add_edge("agent_node", END)
            logger.debug("Built simple graph: START → agent_node → END")
            return graph

        # Add enhanced validation node
        if needs_validation:
            validation_config = ValidationNodeConfigV2(
                name="validation",
                engine_name=self.engine.name,
                tool_node="tool_node" if needs_tools else None,
                parser_node="parse_output" if needs_parsing else None,
                enhanced_mode=True,  # Enable enhanced features
            )
            graph.add_node("validation", validation_config)

        # Add tool node if needed
        if needs_tools:
            tool_config = ToolNodeConfig(
                name="tool_node",
                engine_name=self.engine.name,
                advanced_routing=self.advanced_routing,
            )
            graph.add_node("tool_node", tool_config)

        # Add parser node if needed
        if needs_parsing:
            parser_config = ParserNodeConfigV2(
                name="parse_output",
                engine_name=self.engine.name,
                structured_output_model=self.structured_output_model,
                output_parser=self.output_parser,
            )
            graph.add_node("parse_output", parser_config)

        # Setup routing logic
        if needs_validation:
            if self.force_tool_use or self._always_needs_validation():
                graph.add_edge("agent_node", "validation")
                logger.debug("Added direct routing: agent_node → validation")
            else:
                graph.add_conditional_edges(
                    "agent_node", should_continue, {True: "validation", False: END}
                )
                logger.debug("Added conditional routing: agent_node → [validation|END]")

        logger.debug(f"Built enhanced graph with {len(graph.nodes)} nodes")
        return graph

    def _has_tools(self) -> bool:
        """Check if agent has tools available."""
        return bool(self.engine and getattr(self.engine, "tools", None))

    def _has_structured_output(self) -> bool:
        """Check if agent has structured output configured."""
        return bool(
            self.structured_output_model
            or (self.engine and getattr(self.engine, "structured_output_model", None))
        )

    def _always_needs_validation(self) -> bool:
        """Check if we always need validation routing."""
        return self._has_structured_output() or bool(self.output_parser)

    # ========================================================================
    # ENHANCED CAPABILITIES
    # ========================================================================

    def get_capabilities_summary(self) -> dict[str, Any]:
        """Get comprehensive summary of agent capabilities."""
        return {
            "agent_name": self.name,
            "agent_type": "EnhancedSimpleAgent",
            "engine_type": type(self.engine).__name__,
            "features": {
                "has_tools": self._has_tools(),
                "has_structured_output": self._has_structured_output(),
                "multi_engine_mode": self.multi_engine_mode,
                "advanced_routing": self.advanced_routing,
                "performance_mode": self.performance_mode,
                "debug_mode": self.debug_mode,
                "has_persistence": bool(self.persistence_config),
            },
            "configuration": {
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
                "model_name": self.model_name,
                "force_tool_use": self.force_tool_use,
            },
            "engines": {
                "primary": self.engine.name if self.engine else None,
                "total_engines": len(self.engines),
                "engine_names": list(self.engines.keys()),
            },
            "schemas": {
                "state_schema": (
                    getattr(self.state_schema, "__name__", None)
                    if self.state_schema
                    else None
                ),
                "input_schema": (
                    getattr(self.input_schema, "__name__", None)
                    if self.input_schema
                    else None
                ),
                "output_schema": (
                    getattr(self.output_schema, "__name__", None)
                    if self.output_schema
                    else None
                ),
            },
        }

    def display_capabilities(self) -> None:
        """Display comprehensive capabilities summary."""
        summary = self.get_capabilities_summary()

        from rich.console import Console
        from rich.table import Table

        console = Console()

        # Create capabilities table
        table = Table(title=f"Enhanced SimpleAgent Capabilities: {self.name}")
        table.add_column("Category", style="cyan")
        table.add_column("Details", style="green")

        # Agent info
        table.add_row("Type", summary["agent_type"])
        table.add_row("Engine", summary["engine_type"])

        # Features
        features = summary["features"]
        table.add_section()
        table.add_row("Has Tools", "✅" if features["has_tools"] else "❌")
        table.add_row(
            "Structured Output", "✅" if features["has_structured_output"] else "❌"
        )
        table.add_row("Multi-Engine", "✅" if features["multi_engine_mode"] else "❌")
        table.add_row(
            "Advanced Routing", "✅" if features["advanced_routing"] else "❌"
        )
        table.add_row(
            "Performance Mode", "✅" if features["performance_mode"] else "❌"
        )
        table.add_row("Debug Mode", "✅" if features["debug_mode"] else "❌")

        # Configuration
        config = summary["configuration"]
        table.add_section()
        table.add_row("Temperature", str(config["temperature"]))
        table.add_row("Max Tokens", str(config["max_tokens"]))
        table.add_row("Model", str(config["model_name"]))

        console.print(table)

    def __repr__(self) -> str:
        """Enhanced string representation."""
        engine_info = f"{type(self.engine).__name__}" if self.engine else "None"
        features = []
        if self.multi_engine_mode:
            features.append("multi-engine")
        if self.advanced_routing:
            features.append("advanced-routing")
        if self.performance_mode:
            features.append("performance")
        if self.debug_mode:
            features.append("debug")

        feature_str = f" ({', '.join(features)})" if features else ""
        return f"EnhancedSimpleAgent(name='{self.name}', engine={engine_info}{feature_str})"
