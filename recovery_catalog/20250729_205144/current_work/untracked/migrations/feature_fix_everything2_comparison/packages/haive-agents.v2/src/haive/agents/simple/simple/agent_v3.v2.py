"""Agent_V3 core module.

This module provides agent v3 functionality for the Haive framework.

Classes:
    with: with implementation.
    SimpleAgentV3: SimpleAgentV3 implementation.
    with: with implementation.

Functions:
    log_execution_start: Log Execution Start functionality.
    log_execution_complete: Log Execution Complete functionality.
    ensure_aug_llm_config_with_debug: Ensure Aug Llm Config With Debug functionality.
"""

# SimpleAgent v3 - Enhanced Dynamic Architecture Implementation
"""
SimpleAgent v3 implementation using proper dynamic architecture patterns.

This implementation follows the established Haive patterns:
- Enhanced base Agent with hooks system
- TypeVar defaulted to AugLLMConfig for SimpleAgent
- Structured output integration across agents
- RecompileMixin for hash-based change detection
- DynamicToolRouteMixin for dynamic tool routing
- MetaStateSchema for agent embedding capability
- GenericEngineNodeConfig for type-safe node configuration
- Agent-as-Tool pattern for composition
- Full hooks integration for lifecycle management
"""

import logging
from typing import Any

# Use typing_extensions for TypeVar with default support
try:
    from typing_extensions import TypeVar
except ImportError:
    from typing import TypeVar

from haive.core.common.mixins.dynamic_tool_route_mixin import DynamicToolRouteMixin
from haive.core.common.mixins.recompile_mixin import RecompileMixin

# Core Haive imports - proper dynamic architecture
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import InvokableEngine
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.engine_node_generic import (
    GenericEngineNodeConfig,
)
from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.node.validation_node_config_v2 import ValidationNodeConfigV2
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from langchain_core.output_parsers.base import BaseOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.tools import BaseTool
from langgraph.graph import END, START
from pydantic import BaseModel, Field, field_validator

# Use enhanced Agent base class with proper generic support
from haive.agents.base.enhanced_agent import Agent

# Hooks system - now integrated into enhanced Agent
from haive.agents.base.hooks import HookContext, HookEvent

logger = logging.getLogger(__name__)

# Default TypeVar to AugLLMConfig for SimpleAgent
EngineT = TypeVar("EngineT", bound=InvokableEngine, default=AugLLMConfig)
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)

# ========================================================================
# SIMPLE AGENT V3 - Enhanced Dynamic Architecture Implementation
# ========================================================================


class SimpleAgentV3(
    Agent[AugLLMConfig],  # Use enhanced generic Agent with AugLLMConfig default
    RecompileMixin,
    DynamicToolRouteMixin,
    # Note: Removed HooksMixin to avoid conflicts - enhanced Agent has its own hook system
):
    """SimpleAgent v3 with enhanced dynamic architecture and hooks system.

    This implementation uses the complete Haive dynamic architecture:

    **Enhanced Architecture:**
    - Enhanced base Agent with hooks system integration
    - Uses LLMState for proper state management with token tracking
    - TypeVar defaulted to AugLLMConfig for SimpleAgent
    - Full hooks lifecycle management (before/after execution, setup, etc.)
    - Structured output integration across different agent types
    - Hash-based change detection via RecompileMixin
    - Dynamic tool routing via DynamicToolRouteMixin
    - Graph recompilation on structural changes
    - Meta-agent embedding via MetaStateSchema
    - Type-safe node configuration via GenericEngineNodeConfig

    **Hooks Integration:**
    - Pre/post execution hooks with context
    - Graph building hooks for customization
    - State update hooks for monitoring
    - Error handling hooks for recovery
    - Node-level execution hooks

    **Key Features:**
    - Engine name references (not direct engine objects)
    - Recompilable graph with change tracking
    - Agent-as-tool composition support
    - Async execution patterns with hooks
    - Full observability with debug=True default
    - Cross-agent structured output compatibility

    **Architecture Integration:**
    - Inherits from Agent[AugLLMConfig] with proper TypeVar default
    - Uses RecompileMixin for recompilation management
    - Uses DynamicToolRouteMixin for tool change detection
    - Uses HooksMixin for lifecycle event management
    - Integrates with MetaStateSchema for embedding
    - Uses BaseGraph for dynamic graph management

    Examples:
        Basic usage with hooks and debug::

            agent = SimpleAgentV3(
                name="enhanced_agent",
                temperature=0.7,
                debug=True,  # Full observability
                auto_recompile=True
            )

            # Add hooks for monitoring
            @agent.before_run
            def log_execution_start(context):
                logger.info(f"Starting execution: {context.input_data}")

            @agent.after_run
            def log_execution_complete(context):
                logger.info(f"Completed execution: {context.output_data}")

            # Agent automatically recompiles on changes with full logging
            agent.add_tool(calculator_tool)  # Triggers recompilation with hooks
            result = await agent.arun("Calculate 15 * 23", debug=True)

        Meta-agent embedding with hooks::

            meta_state = MetaStateSchema.from_agent(agent)
            result = await meta_state.execute_agent(input_data)

        Agent-as-tool with structured output::

            structured_tool = SimpleAgentV3.as_structured_tool(
                name="data_processor",
                output_model=ProcessedData,
                temperature=0.1,
                debug=True
            )
    """

    # ========================================================================
    # ENHANCED CONVENIENCE FIELDS - With hooks and change tracking
    # ========================================================================

    temperature: float | None = Field(
        default=None,
        description="Temperature for the LLM (syncs to engine, triggers recompile + hooks)",
    )
    max_tokens: int | None = Field(
        default=None,
        description="Max tokens for the LLM (syncs to engine, triggers recompile + hooks)",
    )
    model_name: str | None = Field(
        default=None,
        description="Model name for the LLM (syncs to engine.model, triggers recompile + hooks)",
    )
    force_tool_use: bool | None = Field(
        default=None,
        description="Force tool use (syncs to engine, triggers recompile + hooks)",
    )
    structured_output_model: type[BaseModel] | None = Field(
        default=None,
        description="Structured output model (syncs to engine, triggers recompile + hooks)",
    )
    system_message: str | None = Field(
        default=None,
        description="System message (syncs to engine, triggers recompile + hooks)",
    )

    # SimpleAgent v3 enhanced fields
    output_parser: BaseOutputParser | None = Field(
        default=None,
        description="Optional output parser (triggers recompile + hooks on change)",
    )
    prompt_template: ChatPromptTemplate | PromptTemplate | None = Field(
        default=None,
        description="Optional prompt template (triggers recompile + hooks on change)",
    )

    # Enhanced architecture flags - Debug enabled by default
    debug: bool = Field(
        default=True,  # Enable debug by default for full observability
        description="Enable debug mode with full logging and hooks",
    )
    # Note: auto_recompile is provided by RecompileMixin - no need to redeclare
    change_tracking_enabled: bool = Field(
        default=True, description="Enable change tracking for recompilation"
    )
    hooks_enabled: bool = Field(
        default=True, description="Enable hooks system for lifecycle management"
    )
    structured_output_compatible: bool = Field(
        default=True, description="Enable cross-agent structured output compatibility"
    )

    # ========================================================================
    # ENGINE VALIDATION - Ensure AugLLMConfig (with debug logging)
    # ========================================================================

    @field_validator("engine", mode="before")
    @classmethod
    def ensure_aug_llm_config_with_debug(cls, v):
        """Ensure engine is AugLLMConfig or create one with debug enabled."""
        if v is None:
            engine = AugLLMConfig()
            logger.debug("Created default AugLLMConfig engine")
            return engine
        if isinstance(v, dict):
            engine = AugLLMConfig(**v)
            logger.debug(f"Created AugLLMConfig from dict: {list(v.keys())}")
            return engine
        if not isinstance(v, AugLLMConfig):
            raise ValueError(f"SimpleAgentV3 requires AugLLMConfig, got {type(v)}")
        logger.debug("Using provided AugLLMConfig engine")
        return v

    # ========================================================================
    # INITIALIZATION - Setup enhanced architecture with hooks
    # ========================================================================

    def model_post_init(self, __context: Any) -> None:
        """Initialize enhanced dynamic architecture components with hooks."""
        if self.debug:
            logger.info(
                f"Initializing SimpleAgentV3 '{self.name}' with enhanced architecture"
            )

        # Initialize parent classes
        super().model_post_init(__context)

        # Initialize mixins with debug logging
        self._init_recompile_mixin()
        self._init_dynamic_tool_routing()
        self._init_hooks_system()

        # Setup agent-specific features
        self.setup_agent()

        # Register change callbacks
        self._register_change_callbacks()

        # Setup structured output compatibility
        self._setup_structured_output_compatibility()

        if self.debug:
            logger.info(f"SimpleAgentV3 '{self.name}' initialization complete")

    def _init_recompile_mixin(self) -> None:
        """Initialize recompilation mixin with debug logging."""
        if self.debug:
            logger.debug(f"Initializing RecompileMixin for '{self.name}'")

        # Set auto-recompile behavior
        if hasattr(self, "auto_recompile") and self.auto_recompile:
            self.mark_for_recompile("Initial setup - auto recompile enabled")
            if self.debug:
                logger.debug(f"Auto-recompile enabled for '{self.name}'")

    def _init_dynamic_tool_routing(self) -> None:
        """Initialize dynamic tool routing mixin with debug logging."""
        if self.debug:
            logger.debug(f"Initializing DynamicToolRouteMixin for '{self.name}'")

        # Register callback for tool changes
        self.register_route_change_callback(self._on_tool_route_change)

        # Enable batch operations for efficiency
        self._batch_operations_enabled = True

        if self.debug:
            logger.debug(f"Dynamic tool routing initialized for '{self.name}'")

    def _init_hooks_system(self) -> None:
        """Initialize hooks system with debug logging."""
        if not self.hooks_enabled:
            return

        if self.debug:
            logger.debug(f"Initializing hooks system for '{self.name}'")

        # Register default hooks for debugging and monitoring
        self._register_default_hooks()

        if self.debug:
            logger.debug(f"Hooks system initialized for '{self.name}'")

    def _register_default_hooks(self) -> None:
        """Register default hooks for debugging and monitoring."""
        if not self.debug:
            return

        # Setup lifecycle hooks
        @self.before_setup
        def log_setup_start(context: HookContext):
            logger.debug(f"[{self.name}] Setup starting...")

        @self.after_setup
        def log_setup_complete(context: HookContext):
            logger.debug(f"[{self.name}] Setup complete")

        @self.before_build_graph
        def log_graph_build_start(context: HookContext):
            logger.debug(f"[{self.name}] Graph building starting...")

        @self.after_build_graph
        def log_graph_build_complete(context: HookContext):
            logger.debug(f"[{self.name}] Graph building complete")

        # Setup execution hooks
        @self.before_run
        def log_execution_start(context: HookContext):
            logger.info(
                f"[{self.name}] Execution starting with input: {type(context.input_data)}"
            )

        @self.after_run
        def log_execution_complete(context: HookContext):
            logger.info(
                f"[{self.name}] Execution complete with output: {type(context.output_data)}"
            )

        @self.on_error
        def log_execution_error(context: HookContext):
            logger.error(f"[{self.name}] Execution error: {context.error}")

        # Setup state hooks
        @self.before_state_update
        def log_state_update_start(context: HookContext):
            if self.debug:
                logger.debug(f"[{self.name}] State update starting...")

        @self.after_state_update
        def log_state_update_complete(context: HookContext):
            if self.debug:
                logger.debug(f"[{self.name}] State update complete")

    def setup_agent(self) -> None:
        """Setup SimpleAgent v3 with enhanced architecture and structured output support.

        This method implements the abstract setup_agent method from the base Agent class
        with comprehensive initialization for structured output, tool management, hooks
        integration, and recompilation capabilities. Called automatically during agent
        instantiation to configure all enhanced features.

        The setup process includes:
        1. Engine registration and configuration validation
        2. Structured output model preparation and tool conversion
        3. Hooks system initialization and event binding
        4. Tool routing configuration and metadata extraction
        5. State schema selection (LLMState for token tracking)
        6. Recompilation system activation with change detection
        7. Debug logging configuration and observability setup

        This method is called automatically and should not be invoked manually
        unless implementing custom agent initialization patterns.

        Raises:
            EngineConfigurationError: If engine configuration is invalid or incompatible.
            StructuredOutputError: If structured_output_model is not a valid Pydantic model.
            HooksInitializationError: If hooks system fails to initialize properly.
            ToolRegistrationError: If tool registration or routing configuration fails.

        Examples:
            Automatic setup during agent creation::

                # Setup is called automatically during __init__
                agent = SimpleAgentV3(
                    name="auto_setup_agent",
                    engine=AugLLMConfig(
                        structured_output_model=TaskAnalysis,
                        tools=[calculator_tool],
                        temperature=0.3
                    ),
                    debug=True
                )
                # setup_agent() has already been called with full configuration

            Manual setup for custom initialization::

                class CustomSimpleAgent(SimpleAgentV3):
                    def setup_agent(self) -> None:
                        # Custom pre-setup logic
                        self.custom_configuration()

                        # Call parent setup for core functionality
                        super().setup_agent()

                        # Custom post-setup logic
                        self.additional_configuration()

            Validation of setup completion::

                agent = SimpleAgentV3(name="test_agent")

                # Verify setup was completed successfully
                assert hasattr(agent, 'engines')
                assert len(agent.engines) > 0
                assert agent.set_schema is True

        Note:
            - This method is idempotent and safe to call multiple times
            - Engine configuration is validated during setup
            - Structured output models are converted to tools automatically
            - Tool routing is configured based on available tools and models
            - LLMState is selected as the default state schema for token tracking
            - Debug mode affects the verbosity of setup logging

        See Also:
            Agent.setup_agent: Base class abstract method being implemented
            _sync_convenience_fields_with_tracking: Engine synchronization
            AugLLMConfig: Engine configuration options
            LLMState: Default state schema for token tracking
        """
        if self.debug:
            logger.debug(f"Setting up agent v3 features for '{self.name}'")

        if self.engine:
            # Add engine to engines dict with proper name tracking
            engine_name = getattr(self.engine, "name", "main")
            self.engines[engine_name] = self.engine

            if self.debug:
                logger.debug(f"Added engine '{engine_name}' to engines dict")

            # Sync convenience fields (with change detection and hooks)
            self._sync_convenience_fields_with_tracking()

            # Enable schema generation with LLMState as default
            self.set_schema = True

            # Set LLMState as the default state schema for SimpleAgent
            if not self.state_schema:
                self.state_schema = LLMState
                if self.debug:
                    logger.debug(
                        f"Using LLMState as default state schema for '{self.name}'"
                    )

            # Setup initial graph if auto-recompile is enabled
            if self.auto_recompile:
                self._trigger_initial_compilation()

    def _sync_convenience_fields_with_tracking(self) -> None:
        """Sync convenience fields to engine with change tracking and hooks."""
        if not self.engine:
            return

        changes_made = []

        # Execute before_sync hook
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_STATE_UPDATE,
                metadata={"sync_type": "convenience_fields"},
            )

        # Track each field change with debug logging
        if (
            self.temperature is not None
            and getattr(self.engine, "temperature", None) != self.temperature
        ):
            self.engine.temperature = self.temperature
            changes_made.append("temperature")
            if self.debug:
                logger.debug(f"Synced temperature: {self.temperature}")

        if (
            self.max_tokens is not None
            and getattr(self.engine, "max_tokens", None) != self.max_tokens
        ):
            self.engine.max_tokens = self.max_tokens
            changes_made.append("max_tokens")
            if self.debug:
                logger.debug(f"Synced max_tokens: {self.max_tokens}")

        if (
            self.model_name is not None
            and getattr(self.engine, "model", None) != self.model_name
        ):
            self.engine.model = self.model_name
            changes_made.append("model_name")
            if self.debug:
                logger.debug(f"Synced model_name: {self.model_name}")

        if (
            self.force_tool_use is not None
            and getattr(self.engine, "force_tool_use", None) != self.force_tool_use
        ):
            self.engine.force_tool_use = self.force_tool_use
            changes_made.append("force_tool_use")
            if self.debug:
                logger.debug(f"Synced force_tool_use: {self.force_tool_use}")

        if (
            self.structured_output_model is not None
            and getattr(self.engine, "structured_output_model", None)
            != self.structured_output_model
        ):
            self.engine.structured_output_model = self.structured_output_model
            changes_made.append("structured_output_model")
            if self.debug:
                logger.debug(
                    f"Synced structured_output_model: {self.structured_output_model}"
                )

        if (
            self.system_message is not None
            and getattr(self.engine, "system_message", None) != self.system_message
        ):
            self.engine.system_message = self.system_message
            changes_made.append("system_message")
            if self.debug:
                logger.debug(
                    f"Synced system_message length: {len(self.system_message) if self.system_message else 0}"
                )

        # Mark for recompilation if changes were made
        if changes_made and self.change_tracking_enabled:
            reason = f"Convenience field changes: {', '.join(changes_made)}"
            self.mark_for_recompile(reason)
            if self.debug:
                logger.debug(f"Marked for recompilation: {reason}")

        # Execute after_sync hook
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.AFTER_STATE_UPDATE,
                metadata={"sync_type": "convenience_fields", "changes": changes_made},
            )

    def _register_change_callbacks(self) -> None:
        """Register callbacks for change detection with hooks."""
        if self.debug:
            logger.debug(f"Registering change callbacks for '{self.name}'")

        # Tool route changes trigger recompilation with hooks
        self.register_route_change_callback(self._on_tool_route_change)

        # Engine changes trigger recompilation with hooks
        if hasattr(self.engine, "register_change_callback"):
            self.engine.register_change_callback(self._on_engine_change)

    def _on_tool_route_change(self, change_type: str, tool_name: str, **kwargs) -> None:
        """Handle tool route changes with hooks."""
        if self.debug:
            logger.info(
                f"[{self.name}] Tool route change: {change_type} for tool '{tool_name}'"
            )

        # Execute hook for tool change
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_STATE_UPDATE,
                metadata={"change_type": change_type, "tool_name": tool_name, **kwargs},
            )

        if self.change_tracking_enabled:
            reason = f"Tool route change: {change_type} - {tool_name}"
            self.mark_for_recompile(reason)
            if self.debug:
                logger.debug(f"Marked for recompilation: {reason}")

    def _on_engine_change(self, change_type: str, **kwargs) -> None:
        """Handle engine configuration changes with hooks."""
        if self.debug:
            logger.info(f"[{self.name}] Engine change: {change_type}")

        # Execute hook for engine change
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_STATE_UPDATE,
                metadata={"change_type": change_type, **kwargs},
            )

        if self.change_tracking_enabled:
            reason = f"Engine change: {change_type}"
            self.mark_for_recompile(reason)
            if self.debug:
                logger.debug(f"Marked for recompilation: {reason}")

    def _setup_structured_output_compatibility(self) -> None:
        """Setup cross-agent structured output compatibility."""
        if not self.structured_output_compatible:
            return

        if self.debug:
            logger.debug(
                f"Setting up structured output compatibility for '{self.name}'"
            )

        # Register hooks for structured output processing
        @self.after_run
        def handle_structured_output(context: HookContext):
            """Post-process output for structured format if needed."""
            if self.structured_output_model and context.output_data:
                if self.debug:
                    logger.debug(
                        f"Processing structured output for model: {self.structured_output_model}"
                    )
                # Additional structured output processing can be added here

    def _trigger_initial_compilation(self) -> None:
        """Trigger initial graph compilation with hooks."""
        try:
            if self.debug:
                logger.debug(f"Triggering initial compilation for '{self.name}'")

            # Execute before_build_graph hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.BEFORE_BUILD_GRAPH,
                    metadata={"compilation_type": "initial"},
                )

            # Build initial graph
            self._compiled_graph = self.build_dynamic_graph()

            if self.debug:
                logger.info(f"Initial graph compiled for agent '{self.name}'")

            # Execute after_build_graph hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.AFTER_BUILD_GRAPH,
                    metadata={
                        "compilation_type": "initial",
                        "graph": self._compiled_graph,
                    },
                )

        except Exception as e:
            logger.error(f"Failed to compile initial graph: {e}")
            self.mark_for_recompile(f"Initial compilation failed: {e}")

            # Execute error hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.ON_ERROR,
                    error=e,
                    metadata={"compilation_type": "initial"},
                )

    # ========================================================================
    # ENHANCED DYNAMIC GRAPH BUILDING - With hooks integration
    # ========================================================================

    def build_dynamic_graph(self) -> BaseGraph:
        """Build the dynamic agent graph with hooks integration.

        Creates a recompilable graph with enhanced features:

        1. **LLM Node**: Uses GenericEngineNodeConfig with engine name reference
        2. **Tool Nodes**: Dynamic tool routing with change detection and hooks
        3. **Parser Nodes**: Type-safe parsing with schema validation and hooks
        4. **Validation Nodes**: Conditional routing with hook-based monitoring

        The graph automatically recompiles when:
        - Tools are added/removed/modified (with hooks)
        - Engine configuration changes (with hooks)
        - Node schemas change (with hooks)
        - Routing logic changes (with hooks)

        **Hooks Integration:**
        - Pre/post node execution hooks
        - Graph structure change hooks
        - Routing decision hooks
        - Error handling hooks

        Returns:
            BaseGraph: Compiled graph ready for execution with hooks
        """
        if self.debug:
            logger.debug(f"Building dynamic graph for '{self.name}'")

        # Create graph with enhanced features
        graph = BaseGraph(name=f"{self.name}_graph")

        # Get engine name for node references
        engine_name = getattr(self.engine, "name", "main")

        if self.debug:
            logger.debug(f"Using engine name: {engine_name}")

        # Add main LLM node using existing EngineNodeConfig
        llm_node_config = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", llm_node_config)
        graph.add_edge(START, "agent_node")

        # Check what additional nodes we need
        needs_tools = self._has_tools()
        needs_parsing = self._has_structured_output() or self.output_parser

        if self.debug:
            logger.debug(
                f"Graph needs - tools: {needs_tools}, parsing: {needs_parsing}"
            )

        # Simple case - just LLM
        if not needs_tools and not needs_parsing:
            graph.add_edge("agent_node", END)
            if self.debug:
                logger.debug("Built simple graph: START -> agent_node -> END")
            return graph

        # Add dynamic tool nodes if needed
        if needs_tools:
            self._add_dynamic_tool_nodes(graph, engine_name)

        # Add parser nodes if needed
        if needs_parsing:
            self._add_parser_nodes(graph, engine_name)

        # Add validation/routing nodes
        if needs_tools or needs_parsing:
            self._add_validation_nodes(graph, engine_name, needs_tools, needs_parsing)

        # Register graph for recompilation with hooks
        self._register_graph_for_recompilation(graph)

        if self.debug:
            logger.debug(f"Dynamic graph building complete for '{self.name}'")

        return graph

    def _add_dynamic_tool_nodes(self, graph: BaseGraph, engine_name: str) -> None:
        """Add dynamic tool nodes with change tracking and hooks."""
        if self.debug:
            logger.debug(f"Adding dynamic tool nodes for engine: {engine_name}")

        # Create tool node config using existing ToolNodeConfig
        tool_node_config = ToolNodeConfig(name="tool_node", engine_name=engine_name)
        graph.add_node("tool_node", tool_node_config)

        # Register for tool change notifications with hooks
        def tool_change_handler(change_type: str, tool_name: str, **kwargs):
            if self.debug:
                logger.debug(f"Tool change detected: {change_type} - {tool_name}")

            graph.mark_for_recompile(f"Tool change: {change_type} - {tool_name}")

            # Execute hook for tool change
            if self.hooks_enabled:
                # Execute hook with metadata instead of HookContext
                self.execute_hooks(
                    HookEvent.BEFORE_STATE_UPDATE,
                    metadata={
                        "change_type": change_type,
                        "tool_name": tool_name,
                        **kwargs,
                    },
                )
                self.execute_hooks(HookEvent.BEFORE_STATE_UPDATE, context)

        self.register_route_change_callback(tool_change_handler)

    def _add_parser_nodes(self, graph: BaseGraph, engine_name: str) -> None:
        """Add parser nodes with schema validation and hooks."""
        if self.debug:
            logger.debug(f"Adding parser nodes for engine: {engine_name}")

        # Determine output schema based on structured output model
        output_schema = self.structured_output_model or MessagesState

        if self.debug:
            logger.debug(f"Parser output schema: {output_schema}")

        parser_node_config = ParserNodeConfigV2(
            name="parse_output", engine_name=engine_name
        )
        graph.add_node("parse_output", parser_node_config)

    def _add_validation_nodes(
        self, graph: BaseGraph, engine_name: str, needs_tools: bool, needs_parsing: bool
    ) -> None:
        """Add validation/routing nodes with hooks."""
        if self.debug:
            logger.debug(
                f"Adding validation nodes - tools: {needs_tools}, parsing: {needs_parsing}"
            )

        # Create validation config with only valid fields
        validation_kwargs = {
            "name": "validation",
            "engine_name": engine_name,
        }

        if needs_tools:
            validation_kwargs["tool_node"] = "tool_node"
        if needs_parsing:
            validation_kwargs["parser_node"] = "parse_output"

        validation_config = ValidationNodeConfigV2(**validation_kwargs)
        graph.add_node("validation", validation_config)

        # Add conditional edges based on message content
        if self.force_tool_use or self._always_needs_validation():
            graph.add_edge("agent_node", "validation")
            if self.debug:
                logger.debug("Added direct edge: agent_node -> validation")
        else:
            graph.add_conditional_edges(
                "agent_node",
                self._routing_condition_with_hooks,
                {
                    "tools": "tool_node" if needs_tools else END,
                    "parsing": "parse_output" if needs_parsing else END,
                    "end": END,
                },
            )
            if self.debug:
                logger.debug("Added conditional edges from agent_node")

    def _routing_condition_with_hooks(self, state: dict[str, Any]) -> str:
        """Determine routing based on state with hooks integration."""
        messages = state.get("messages", [])
        if not messages:
            if self.debug:
                logger.debug("No messages - routing to end")
            return "end"

        last_message = messages[-1]

        # Execute routing hook
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_NODE,
                metadata={"node_type": "routing", "last_message": last_message},
            )

        # Check for tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            if self.debug:
                logger.debug("Tool calls detected - routing to tools")
            return "tools"

        # Check if parsing is needed
        if self._has_structured_output() or self.output_parser:
            if self.debug:
                logger.debug("Structured output needed - routing to parsing")
            return "parsing"

        if self.debug:
            logger.debug("No special routing needed - routing to end")
        return "end"

    def _register_graph_for_recompilation(self, graph: BaseGraph) -> None:
        """Register graph for automatic recompilation with hooks."""
        if self.debug:
            logger.debug("Registering graph for recompilation")

        # Store reference for recompilation
        self._compiled_graph = graph

        # Store graph reference for recompilation (RecompileMixin pattern)
        self._current_graph = graph

        if self.debug:
            logger.debug(f"Graph registered for recompilation tracking: {graph.name}")

        # Check if recompilation is immediately needed
        if self.check_recompile_conditions():
            if self.debug:
                logger.debug("Recompilation needed during graph registration")
            if self.auto_recompile:
                self._trigger_auto_recompile()

    def _recompile_graph(self) -> None:
        """Recompile the graph with current configuration and hooks."""
        try:
            if self.debug:
                logger.info(f"Recompiling graph for agent '{self.name}'")

            # Execute before recompile hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.BEFORE_BUILD_GRAPH,
                    metadata={"compilation_type": "recompile"},
                )

            self._compiled_graph = self.build_dynamic_graph()
            self.resolve_recompile(success=True)

            if self.debug:
                logger.info(f"Graph recompilation successful for agent '{self.name}'")

            # Execute after recompile hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.AFTER_BUILD_GRAPH,
                    metadata={
                        "compilation_type": "recompile",
                        "graph": self._compiled_graph,
                    },
                )

        except Exception as e:
            logger.error(f"Graph recompilation failed: {e}")
            self.resolve_recompile(success=False)

            # Execute error hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.ON_ERROR,
                    error=e,
                    metadata={"compilation_type": "recompile"},
                )

    # _trigger_auto_recompile is implemented in enhanced base Agent

    # ========================================================================
    # ENHANCED EXECUTION METHODS - With debug=True and hooks
    # ========================================================================

    async def arun(self, input_data: Any, debug: bool = None, **kwargs) -> Any:
        """Enhanced async run with debug=True default and hooks integration."""
        # Use debug=True by default, or override with parameter
        run_debug = debug if debug is not None else self.debug

        if run_debug:
            logger.info(f"[{self.name}] Starting async execution with debug=True")

        # Execute before_run hook
        if self.hooks_enabled:
            self.execute_hooks(HookEvent.BEFORE_ARUN, input_data=input_data, **kwargs)

        try:
            # Call parent arun with debug enabled
            result = await super().arun(input_data, debug=run_debug, **kwargs)

            if run_debug:
                logger.info(f"[{self.name}] Async execution completed successfully")

            # Execute after_run hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.AFTER_ARUN,
                    input_data=input_data,
                    output_data=result,
                    **kwargs,
                )

            return result

        except Exception as e:
            if run_debug:
                logger.error(f"[{self.name}] Async execution failed: {e}")

            # Execute error hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.ON_ERROR, error=e, input_data=input_data, **kwargs
                )

            raise

    def run(self, input_data: Any, debug: bool = None, **kwargs) -> Any:
        """Execute the agent with synchronous processing and structured output support.

        This method runs the agent synchronously using the configured LLM engine with
        full hooks integration, debug logging, and structured output validation.
        The execution includes comprehensive observability and automatic recompilation
        when tools or configuration changes are detected.

        The execution flow follows this enhanced pattern:
        1. Pre-execution hooks and validation
        2. Input preprocessing and state initialization
        3. Recompilation check and graph rebuilding if needed
        4. LLM execution with tool calling and structured output
        5. Post-execution hooks and state persistence
        6. Response formatting and debug logging

        Args:
            input_data: Input for the agent execution. Supports multiple formats:
                - str: Simple text input (automatically converted to HumanMessage)
                - List[BaseMessage]: Pre-formatted LangChain message history
                - Dict[str, Any]: Structured input matching agent's schema
                - BaseModel: Pydantic model instances for type-safe input
            debug: Override the agent's default debug setting for this execution.
                - None: Use agent's configured debug setting (default: True)
                - True: Enable detailed execution tracing and state inspection
                - False: Minimal logging for production execution
            **kwargs: Additional execution arguments passed to LangGraph:
                - config: Execution configuration overrides
                - recursion_limit: Maximum graph traversal steps
                - configurable: Runtime configuration updates
                - stream_mode: Streaming execution options

        Returns:
            Any: Execution result format varies based on configuration:
                - With structured_output_model: Validated Pydantic model instance
                - With tools only: Final LLM response after tool execution
                - Basic execution: String response or state object
                - Debug mode: Enhanced state with execution metadata and timing

        Raises:
            ValidationError: When structured output fails Pydantic model validation.
            RecompilationError: When graph recompilation fails due to invalid changes.
            ToolExecutionError: When tool calls fail during execution.
            HookExecutionError: When before/after hooks raise exceptions.
            LLMProviderError: When LLM provider is unavailable or returns errors.
            StateManagementError: When state persistence or retrieval fails.

        Examples:
            Basic execution with default debug::

                # Agent created with debug=True by default
                agent = SimpleAgentV3(name="assistant")
                response = agent.run("Explain quantum computing")
                # Shows detailed execution trace by default

            Structured output with validation::

                from pydantic import BaseModel, Field

                class TechnicalExplanation(BaseModel):
                    topic: str = Field(description="Technical topic being explained")
                    difficulty: int = Field(ge=1, le=5, description="Difficulty level 1-5")
                    key_concepts: List[str] = Field(description="Main concepts covered")
                    summary: str = Field(description="Clear summary explanation")

                agent = SimpleAgentV3(
                    name="tech_explainer",
                    engine=AugLLMConfig(
                        structured_output_model=TechnicalExplanation,
                        temperature=0.3
                    )
                )

                explanation = agent.run("Explain machine learning algorithms")
                # Returns TechnicalExplanation with validated structure
                assert isinstance(explanation, TechnicalExplanation)
                print(f"Topic: {explanation.topic}")
                print(f"Difficulty: {explanation.difficulty}/5")

            Tools with structured output and debug::

                @tool
                def search_database(query: str) -> str:
                    '''Search internal database for information.'''
                    return f"Database results for: {query}"

                class ResearchResult(BaseModel):
                    query: str = Field(description="Original research query")
                    sources_found: int = Field(description="Number of sources located")
                    key_findings: List[str] = Field(description="Main research findings")
                    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in results")

                agent = SimpleAgentV3(
                    name="researcher",
                    engine=AugLLMConfig(
                        tools=[search_database],
                        structured_output_model=ResearchResult,
                        temperature=0.2
                    ),
                    debug=True  # Explicit debug enabling
                )

                # Execute with comprehensive logging
                research = agent.run("Research renewable energy trends", debug=True)
                # Shows: tool calls, LLM reasoning, structured output validation

            Production execution with minimal logging::

                agent = SimpleAgentV3(name="prod_agent", debug=False)
                result = agent.run("Process user request", debug=False)
                # Minimal logging for production performance

            With hooks for monitoring::

                @agent.before_run
                def log_start(context):
                    logger.info(f"Starting: {context.input_data}")

                @agent.after_run
                def log_completion(context):
                    logger.info(f"Completed in {context.execution_time}ms")

                result = agent.run("Execute with monitoring")
                # Hooks execute automatically during processing

            Dynamic tool addition with recompilation::

                agent = SimpleAgentV3(name="dynamic_agent", auto_recompile=True)

                # Initial execution
                result1 = agent.run("Hello")

                # Add new tool - triggers automatic recompilation
                @tool
                def new_calculator(expr: str) -> str:
                    return str(eval(expr))

                agent.add_tool(new_calculator)  # Graph recompiles automatically
                result2 = agent.run("Calculate 5 * 8")  # Uses new tool

        Note:
            - Debug mode is enabled by default (debug=True) for development visibility
            - Structured output models are converted to LangChain tools automatically
            - Graph recompilation happens automatically when tools/config changes
            - Hooks execute in order: before_run → execution → after_run
            - State is persisted after successful execution for conversation continuity
            - Token usage is tracked automatically via LLMState integration
            - All exceptions include detailed context for debugging

        Performance Considerations:
            - Debug mode adds ~20-30% execution overhead for logging
            - Structured output validation adds ~5-10ms per response
            - Recompilation takes ~100-200ms when triggered
            - Hook execution is minimal (~1-2ms total)

        See Also:
            arun: Asynchronous version with same functionality
            add_tool: Dynamic tool addition with recompilation
            set_structured_output: Runtime structured output configuration
            AugLLMConfig: Engine configuration options
            LLMState: State schema for token tracking and tool management
            RecompileMixin: Automatic recompilation functionality
        """
        # Use debug=True by default, or override with parameter
        run_debug = debug if debug is not None else self.debug

        if run_debug:
            logger.info(f"[{self.name}] Starting sync execution with debug=True")

        # Execute before_run hook
        if self.hooks_enabled:
            self.execute_hooks(HookEvent.BEFORE_RUN, input_data=input_data, **kwargs)

        try:
            # Call parent run with debug enabled
            result = super().run(input_data, debug=run_debug, **kwargs)

            if run_debug:
                logger.info(f"[{self.name}] Sync execution completed successfully")

            # Execute after_run hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.AFTER_RUN,
                    input_data=input_data,
                    output_data=result,
                    **kwargs,
                )

            return result

        except Exception as e:
            if run_debug:
                logger.error(f"[{self.name}] Sync execution failed: {e}")

            # Execute error hook
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.ON_ERROR, error=e, input_data=input_data, **kwargs
                )

            raise

    # ========================================================================
    # HELPER METHODS - Enhanced with debug logging
    # ========================================================================

    def _has_tools(self) -> bool:
        """Check if agent has tools with debug logging."""
        has_tools = bool(self.engine and getattr(self.engine, "tools", None))
        if self.debug:
            tool_count = len(getattr(self.engine, "tools", [])) if has_tools else 0
            logger.debug(f"[{self.name}] Has tools: {has_tools} (count: {tool_count})")
        return has_tools

    def _has_structured_output(self) -> bool:
        """Check if agent has structured output with debug logging."""
        has_structured = bool(
            self.structured_output_model
            or (self.engine and getattr(self.engine, "structured_output_model", None))
        )
        if self.debug:
            model_name = (
                self.structured_output_model.__name__
                if self.structured_output_model
                else None
            )
            logger.debug(
                f"[{self.name}] Has structured output: {has_structured} (model: {model_name})"
            )
        return has_structured

    def _always_needs_validation(self) -> bool:
        """Check if we always need validation with debug logging."""
        needs_validation = self._has_structured_output() or bool(self.output_parser)
        if self.debug:
            logger.debug(f"[{self.name}] Always needs validation: {needs_validation}")
        return needs_validation

    # ========================================================================
    # ENHANCED AGENT-AS-TOOL PATTERN - With structured output support
    # ========================================================================

    @classmethod
    def as_tool(
        cls,
        name: str | None = None,
        description: str | None = None,
        debug: bool = True,  # Enable debug by default
        **agent_kwargs,
    ) -> BaseTool:
        """Convert SimpleAgentV3 to a LangChain tool with debug support."""
        from langchain_core.tools import tool

        tool_name = name or "simple_agent_v3_tool"
        tool_description = (
            description or "SimpleAgent v3 with enhanced dynamic architecture"
        )

        # Ensure debug is enabled for tools
        agent_kwargs.setdefault("debug", debug)

        @tool(name=tool_name, description=tool_description)
        def agent_tool(query: str) -> str:
            """Execute SimpleAgent v3 with the given query."""
            if debug:
                logger.info(
                    f"Executing agent tool '{tool_name}' with query length: {len(query)}"
                )

            # Create agent instance with debug
            agent = cls(debug=debug, **agent_kwargs)

            # Execute synchronously (tool interface expects sync)
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(agent.arun(query, debug=debug))
            except RuntimeError:
                # Create new event loop if none exists
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(agent.arun(query, debug=debug))

            # Extract string result
            if isinstance(result, dict) and "messages" in result:
                messages = result["messages"]
                if messages:
                    return str(messages[-1].content)

            return str(result)

        return agent_tool

    @classmethod
    def as_structured_tool(
        cls,
        output_model: type[BaseModel],
        name: str | None = None,
        description: str | None = None,
        debug: bool = True,
        **agent_kwargs,
    ) -> BaseTool:
        """Convert SimpleAgentV3 to a structured output tool."""
        from langchain_core.tools import tool

        tool_name = name or f"structured_{output_model.__name__.lower()}_tool"
        tool_description = (
            description or f"Generate structured {output_model.__name__} output"
        )

        # Set structured output model in agent kwargs
        agent_kwargs["structured_output_model"] = output_model
        agent_kwargs.setdefault("debug", debug)

        # Create dynamic tool with proper input/output schemas
        @tool(name=tool_name, description=tool_description)
        def structured_agent_tool(query: str) -> dict:
            """Execute SimpleAgent v3 with structured output."""
            if debug:
                logger.info(
                    f"Executing structured agent tool '{tool_name}' for model: {output_model.__name__}"
                )

            # Create agent with structured output
            agent = cls(debug=debug, **agent_kwargs)

            # Execute with structured output
            import asyncio

            try:
                loop = asyncio.get_event_loop()
                result = loop.run_until_complete(agent.arun(query, debug=debug))
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(agent.arun(query, debug=debug))

            # Extract structured output
            if isinstance(result, dict):
                if "parsed_output" in result:
                    parsed = result["parsed_output"]
                    if isinstance(parsed, output_model):
                        return parsed.model_dump()

                # Try to parse from messages if no parsed_output
                if result.get("messages"):
                    last_content = result["messages"][-1].content
                    try:
                        import json

                        parsed_dict = json.loads(last_content)
                        return output_model(**parsed_dict).model_dump()
                    except:
                        pass

            # Fallback - return raw result
            return {"raw_output": str(result)}

        return structured_agent_tool

    # ========================================================================
    # META-STATE INTEGRATION - Enhanced with hooks
    # ========================================================================

    def as_meta_capable(
        self,
        initial_state: dict[str, Any] | None = None,
        graph_context: dict[str, Any] | None = None,
    ) -> MetaStateSchema:
        """Convert agent to meta-capable agent with hooks integration."""
        if self.debug:
            logger.info(f"Converting '{self.name}' to meta-capable agent")

        # Enhanced initial state with debug info
        enhanced_initial_state = {
            "ready": True,
            "debug": self.debug,
            "hooks_enabled": self.hooks_enabled,
            "auto_recompile": self.auto_recompile,
            **(initial_state or {}),
        }

        # Enhanced graph context
        enhanced_graph_context = {
            "agent_type": "SimpleAgentV3",
            "version": "3.0",
            "features": {
                "hooks": self.hooks_enabled,
                "recompilation": self.auto_recompile,
                "structured_output": self.structured_output_compatible,
                "debug": self.debug,
            },
            **(graph_context or {}),
        }

        # Create meta state without passing self as agent parameter
        # The from_agent method will handle the agent reference correctly
        meta_state = MetaStateSchema.from_agent(
            self,  # Pass self as positional argument, not as 'agent='
            initial_state=enhanced_initial_state,
            graph_context=enhanced_graph_context,
        )

        if self.debug:
            logger.info(f"Meta-capable agent created for '{self.name}'")

        return meta_state

    # ========================================================================
    # GRAPH BUILDING - Enhanced with hooks and recompilation
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the enhanced SimpleAgent v3 graph with hooks and dynamic features.

        Creates a graph structure that adapts based on agent configuration:
        1. Basic (no tools/parsing): START → agent_node → END
        2. With tools: START → agent_node → validation → tool_node → agent_node
        3. With parsing: START → agent_node → validation → parse_output → END
        4. With both: Combines tool and parsing flows with validation routing

        Enhanced with:
        - Hooks integration for lifecycle events
        - Dynamic recompilation triggers
        - Change tracking and monitoring
        - Debug logging throughout

        Returns:
            BaseGraph: The compiled agent graph with enhanced capabilities.
        """
        if self.debug:
            logger.info(f"Building enhanced graph for SimpleAgentV3 '{self.name}'")

        # Execute pre-build hooks
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_BUILD_GRAPH,
                metadata={"agent_name": self.name, "graph_type": "SimpleAgentV3"},
            )

        # Create base graph
        graph = BaseGraph(name=f"{self.name}_graph")

        if not self.engine:
            raise ValueError("No engine configured for SimpleAgentV3")

        engine_name = self.engine.name
        if self.debug:
            logger.debug(f"Using engine: {engine_name}")

        # Add main agent node with enhanced config
        self._add_agent_node(graph, engine_name)

        # Determine what additional nodes are needed
        needs_tools = self._has_tools()
        needs_parsing = self._has_structured_output() or self.output_parser

        if self.debug:
            logger.debug(
                f"Graph requirements - tools: {needs_tools}, parsing: {needs_parsing}"
            )

        # Simple case - just LLM execution
        if not needs_tools and not needs_parsing:
            graph.add_edge("agent_node", END)
            if self.debug:
                logger.debug("Simple graph: agent_node → END")
        else:
            # Add complex routing with tools and/or parsing
            self._add_complex_routing(graph, engine_name, needs_tools, needs_parsing)

        # Register for recompilation tracking
        self._register_graph_for_recompilation(graph)

        # Execute post-build hooks
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.AFTER_BUILD_GRAPH,
                metadata={
                    "graph": graph,
                    "nodes_count": len(graph.nodes) if hasattr(graph, "nodes") else 0,
                    "has_tools": needs_tools,
                    "has_parsing": needs_parsing,
                },
            )

        if self.debug:
            logger.info(f"Enhanced graph built successfully for '{self.name}'")

        return graph

    def _add_agent_node(self, graph: BaseGraph, engine_name: str) -> None:
        """Add the main agent node with enhanced configuration."""
        # Use GenericEngineNodeConfig with the actual engine object
        # This now has the full EngineNodeConfig implementation
        agent_node_config = GenericEngineNodeConfig(
            name="agent_node",
            engine=self.engine,  # Pass the actual engine, not engine_name
        )
        graph.add_node("agent_node", agent_node_config)
        graph.add_edge(START, "agent_node")

        if self.debug:
            logger.debug(f"Added agent node with engine: {engine_name}")

    def _add_complex_routing(
        self, graph: BaseGraph, engine_name: str, needs_tools: bool, needs_parsing: bool
    ) -> None:
        """Add complex routing with tools and parsing support."""
        # Add tool nodes if needed
        if needs_tools:
            self._add_tool_nodes(graph, engine_name)

        # Add parser nodes if needed
        if needs_parsing:
            self._add_parser_nodes(graph, engine_name)

        # Add validation/routing logic
        self._add_validation_nodes(graph, engine_name, needs_tools, needs_parsing)

    def _add_tool_nodes(self, graph: BaseGraph, engine_name: str) -> None:
        """Add tool execution nodes to the graph."""
        if self.debug:
            logger.debug(f"Adding tool nodes for engine: {engine_name}")

        tool_config = ToolNodeConfig(name="tool_node", engine_name=engine_name)
        graph.add_node("tool_node", tool_config)

        if self.debug:
            logger.debug("Tool node added successfully")

    # ========================================================================
    # ABSTRACT METHOD IMPLEMENTATIONS - Required by InvokableEngine
    # ========================================================================

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for SimpleAgentV3.

        Returns:
            Dictionary mapping field names to (type, default) tuples for input schema.
        """
        return {"messages": (list, []), "query": (str, ""), "input": (str, "")}

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for SimpleAgentV3.

        Returns:
            Dictionary mapping field names to (type, default) tuples for output schema.
        """
        if self.structured_output_model:
            # If structured output is defined, use that schema
            return {
                "output": (self.structured_output_model, None),
                "messages": (list, []),
            }
        # Default message-based output
        return {"messages": (list, []), "response": (str, "")}

    def create_runnable(self, runnable_config: Any = None) -> Any:
        """Create a runnable from this agent configuration.

        Args:
            runnable_config: Optional runtime configuration.

        Returns:
            The compiled graph as a runnable.
        """
        if not self._is_compiled and self.graph:
            # Convert BaseGraph to LangGraph first
            schema_kwargs = {}
            if self.state_schema:
                schema_kwargs["state_schema"] = self.state_schema
            if self.input_schema:
                schema_kwargs["input_schema"] = self.input_schema
            if self.output_schema:
                schema_kwargs["output_schema"] = self.output_schema

            # Convert to LangGraph
            langgraph = self.graph.to_langgraph(**schema_kwargs)

            # Now compile the LangGraph with checkpointer and store
            compile_kwargs = {}
            if self.checkpointer is not None:
                compile_kwargs["checkpointer"] = self.checkpointer
            if self.store is not None:
                compile_kwargs["store"] = self.store

            self._compiled_graph = langgraph.compile(**compile_kwargs)
            self._is_compiled = True

            if self.debug:
                logger.debug(f"Compiled SimpleAgentV3 graph for '{self.name}'")

        return self._compiled_graph

    def compile(self, **kwargs) -> Any:
        """Compile the agent's graph.

        This method ensures compatibility with ExecutionMixin.

        Returns:
            Compiled graph ready for execution
        """
        if not self._is_compiled:
            self._app = self.create_runnable()
            self._compiled_graph = self._app
        return self._app
