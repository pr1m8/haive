# haive/agents/base/enhanced_agent.py

"""Enhanced Agent hierarchy with engine-focused generics and backward compatibility.

This module provides the enhanced agent architecture:
- Workflow: Pure orchestration without LLM
- Agent: Workflow + Engine (generic on engine type)
- MultiAgent: Agent + multi-agent coordination

Key features:
- Engine-centric generics: Agent[EngineT]
- Full backward compatibility with existing code
- Clear separation of concerns: orchestration vs LLM vs coordination
- Type safety when needed, flexibility when desired
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Generic, Literal, TypeVar

from haive.core.engine.base import Engine, EngineType, InvokableEngine
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field, PrivateAttr, model_validator

from haive.agents.base.agent_structured_output_mixin import StructuredOutputMixin

# Import hooks system
from haive.agents.base.hooks import HookContext, HookEvent, HookFunction

# Import mixins from existing agent
from haive.agents.base.mixins.execution_mixin import ExecutionMixin
from haive.agents.base.mixins.persistence_mixin import PersistenceMixin
from haive.agents.base.mixins.state_mixin import StateMixin

# Import pre/post processing mixin
from haive.agents.base.pre_post_agent_mixin import PrePostAgentMixin
from haive.agents.base.serialization_mixin import SerializationMixin

logger = logging.getLogger(__name__)

# Generic type variables with defaults (PEP 696)
try:
    from typing_extensions import TypeVar
except ImportError:
    from typing import TypeVar

# ENGINE FOCUSED with defaults
EngineT = TypeVar("EngineT", bound=InvokableEngine)


# Create a custom InvokableEngine that accepts our EngineT
class TypedInvokableEngine(InvokableEngine[BaseModel, BaseModel], Generic[EngineT]):
    """InvokableEngine that's parameterized by the engine type."""


# ========================================================================
# 1. WORKFLOW - Pure orchestration, no engine
# ========================================================================


class Workflow(BaseModel, ABC):
    """Pure workflow orchestration without engine dependencies.

    Workflow handles pure orchestration - routing, transformation,
    coordination - without requiring engines. This is the foundation.

    Examples:
        class DataProcessor(Workflow):
            async def execute(self, data):
                # Pure processing, no LLM
                return processed_data

        class Router(Workflow):
            async def execute(self, request):
                # Route to appropriate handler
                return route_decision
    """

    # Core identification
    name: str = Field(default="Workflow", description="Name of the workflow")

    # Runtime config
    verbose: bool = Field(default=False, description="Enable verbose logging")
    debug: bool = Field(default=False, description="Enable debug mode")

    @model_validator(mode="before")
    @classmethod
    def auto_generate_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Auto-generate workflow name from class name if not provided."""
        if not isinstance(values, dict):
            return values

        if "name" not in values or not values["name"] or values["name"] == "Workflow":
            class_name = cls.__name__
            # Convert CamelCase to readable name
            name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", class_name)
            values["name"] = name

        return values

    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the workflow logic."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"


# ========================================================================
# 2. AGENT - Workflow + Engine (GENERIC ON ENGINE)
# ========================================================================


class Agent(
    # Engine interface with our generic parameter
    TypedInvokableEngine[EngineT],
    ExecutionMixin,  # Execution capabilities
    StateMixin,  # State management
    PersistenceMixin,  # Persistence capabilities
    SerializationMixin,  # Serialization support
    StructuredOutputMixin,  # Structured output support
    PrePostAgentMixin,  # Pre/post processing capabilities
    ABC,  # Abstract base class (must be last)
):
    """Enhanced Agent with engine-focused generics and full backward compatibility.

    Agent = Workflow + Engine. The engine type is the primary generic parameter,
    enabling type-safe engine-specific functionality while maintaining full
    backward compatibility.

    Generic Parameters:
        EngineT: Type of engine (defaults to InvokableEngine for backward compatibility)

    Key Benefits:
        - Engine-specific type safety: Agent[AugLLMConfig] vs Agent[ReactEngine]
        - Backward compatible: existing Agent() calls work unchanged
        - Engine-specific methods: BaseRAGAgent[RetrieverEngine] gets retriever methods
        - Flexible composition: Any engine type can be used

    Examples:
        # Backward compatible - works unchanged
        agent = SimpleAgent(name="test")

        # Engine-specific typing
        aug_agent: SimpleAgent[AugLLMConfig] = SimpleAgent(engine=aug_config)
        rag_agent: BaseRAGAgent[RetrieverEngine] = BaseRAGAgent(engine=retriever_engine)

        # Mixed usage - all compatible
        agents = [agent, aug_agent, rag_agent]
    """

    # Engine type marker
    engine_type: Literal[EngineType.AGENT] = Field(
        default=EngineType.AGENT, description="Engine type, always AGENT"
    )

    # Engine management - CORE GENERIC FIELD
    engines: dict[str, Engine] = Field(
        default_factory=dict, description="Dictionary of engines this agent uses"
    )

    engine: EngineT | None = Field(
        default=None, description="Main engine (determines agent type)"
    )

    # Graph and state management
    graph: BaseGraph | None = Field(
        default=None,
        exclude=True,
        description="The workflow graph (excluded from serialization)",
    )

    # Schema definitions (enhanced for type safety)
    state_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent state"
    )
    input_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent input"
    )
    output_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent output"
    )
    use_prebuilt_base: bool = Field(
        default=False,
        description="Whether to use the state_schema as a base for composition",
    )

    # Persistence fields (same as original for compatibility)
    checkpointer: Any = Field(
        default=None,
        exclude=True,
        description="Persistence checkpointer (excluded from serialization)",
    )
    store: Any | None = Field(
        default=None,
        exclude=True,
        description="Optional state store (excluded from serialization)",
    )

    persistence: Any | None = Field(
        default=True,
        description="Persistence configuration for state checkpointing",
    )

    checkpoint_mode: Literal["sync", "async"] = Field(
        default="sync", description="Checkpoint mode for persistence"
    )

    add_store: bool = Field(
        default=True,
        description="Whether to add a state store for cross-thread persistence",
    )

    # Runtime configuration
    runnable_config: RunnableConfig | None = Field(
        default=None, description="Default runtime configuration"
    )

    # Runtime configuration flags
    verbose: bool = Field(default=False, description="Enable verbose logging")
    debug: bool = Field(default=False, description="Enable debug mode")

    # Debug and history flags
    save_history: bool = Field(default=True, description="Save state history")
    visualize: bool = Field(default=True, description="Enable visualization")

    # Private state tracking (same as original)
    _graph_built: bool = PrivateAttr(default=False)
    _compiled_graph: CompiledGraph | None = PrivateAttr(default=None)
    _is_compiled: bool = PrivateAttr(default=False)
    _setup_complete: bool = PrivateAttr(default=False)
    _checkpoint_mode: str = PrivateAttr(default="sync")
    _app: Any | None = PrivateAttr(default=None)
    _async_checkpointer: Any | None = PrivateAttr(default=None)
    _async_setup_pending: bool = PrivateAttr(default=False)

    # Hooks system - integrated into base agent
    _hooks: dict[HookEvent, list[HookFunction]] = PrivateAttr(default_factory=dict)
    hooks_enabled: bool = Field(
        default=True, description="Whether hooks system is enabled"
    )

    # Schema control flag
    set_schema: Literal[True, False] = Field(
        default=False, description="Whether to auto-generate schemas from engines"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_engines_and_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """STEP 1: Normalize engines dict and auto-generate name."""
        if not isinstance(values, dict):
            return values

        # Auto-generate name from class name if default or empty
        if (
            "name" not in values
            or not values["name"]
            or values["name"] in ["Agent", "Workflow"]
        ):
            class_name = cls.__name__
            # Convert CamelCase to readable name
            name = re.sub("([a-z0-9])([A-Z])", r"\1 \2", class_name)
            values["name"] = name

        # Initialize engines dict if not present
        if "engines" not in values:
            values["engines"] = {}

        # Move single engine to engines dict
        if "engine" in values and values["engine"] is not None:
            engine = values["engine"]
            # Add to engines dict with appropriate key
            if hasattr(engine, "name") and engine.name:
                values["engines"][engine.name] = engine
            else:
                values["engines"]["main"] = engine

        # Normalize engines field to always be a dict
        if "engines" in values and values["engines"] is not None:
            engines = values["engines"]

            if isinstance(engines, list | tuple):
                # Convert list/tuple to dict
                engine_dict = {}
                for i, engine in enumerate(engines):
                    if hasattr(engine, "name") and engine.name:
                        engine_dict[engine.name] = engine
                    else:
                        engine_dict[f"engine_{i}"] = engine
                values["engines"] = engine_dict

            elif not isinstance(engines, dict):
                # Single engine not in dict form
                if hasattr(engines, "name") and engines.name:
                    values["engines"] = {engines.name: engines}
                else:
                    values["engines"] = {"main": engines}

        return values

    @model_validator(mode="after")
    def complete_agent_setup(self) -> "Agent":
        """STEP 2-5: Complete agent setup in proper order."""
        try:
            # STEP 1: Initialize hooks system first
            self._setup_hooks()

            # STEP 2: Call subclass setup hook for field syncing
            self.setup_agent()
            
            # STEP 2.5: Set up pre/post processing transformers if mixin is available
            if hasattr(self, 'setup_transformers'):
                self.setup_transformers()

            # STEP 3: Generate schemas from engines
            self._setup_schemas()

            # STEP 4: Setup persistence using the mixin
            self._setup_persistence_from_config()

            # STEP 5: Build the initial graph
            self._build_initial_graph()

            self._setup_complete = True

            if self.verbose:
                logger.info(f"Enhanced Agent setup complete: {self.name}")

        except Exception as e:
            logger.exception(
                f"Failed to setup agent {
                    self.__class__.__name__}: {e}"
            )

        return self

    def _setup_hooks(self) -> None:
        """Initialize the hooks system properly."""
        if not hasattr(self, "_hooks") or self._hooks is None:
            self._hooks = {}

        # Execute setup hooks if enabled
        if self.hooks_enabled:
            self.execute_hooks(HookEvent.BEFORE_SETUP)

    def setup_agent(self) -> None:
        """Hook for subclasses to perform field syncing and custom setup.

        This method is called BEFORE schema generation and graph building,
        allowing subclasses to sync fields to engines properly.

        Override this method in subclasses for custom setup logic.
        """
        # Default implementation does nothing - subclasses override

    def _auto_derive_io_schemas(self) -> None:
        """Automatically derive input and output schemas with intelligent defaults.

        This method:
        1. Derives input schema from state schema or first engine
        2. Derives output schema considering structured output models
        3. Falls back to messages-based schemas when appropriate
        """
        # Derive input schema if not provided
        if not self.input_schema:
            logger.debug("No input schema provided, deriving from available sources")

            # Try to derive from state schema first
            if self.state_schema and hasattr(self.state_schema, "derive_input_schema"):
                try:
                    self.input_schema = self.state_schema.derive_input_schema(
                        name=f"{self.name}Input"
                    )
                    logger.debug(
                        f"Derived input schema from state schema: {
                            self.input_schema.__name__}"
                    )
                except Exception as e:
                    logger.debug(f"Could not derive input schema from state: {e}")

            # If still no input schema, try first engine
            if not self.input_schema and self.engines:
                first_engine = next(iter(self.engines.values()), None)
                if first_engine and hasattr(first_engine, "get_input_fields"):
                    try:
                        fields = first_engine.get_input_fields()
                        if fields:
                            from pydantic import create_model

                            self.input_schema = create_model(
                                f"{self.name}Input", **fields
                            )
                            logger.debug("Derived input schema from first engine")
                    except Exception as e:
                        logger.debug(f"Could not derive input schema from engine: {e}")

            # Final fallback - use state schema as input
            if not self.input_schema and self.state_schema:
                self.input_schema = self.state_schema
                logger.debug("Using state schema as input schema")

        # Derive output schema if not provided
        if not self.output_schema:
            logger.debug("No output schema provided, deriving from available sources")

            # Special handling for engines with structured output
            main_engine = self.engine or next(iter(self.engines.values()), None)
            if main_engine:
                # Check if engine has structured output model
                if (
                    hasattr(main_engine, "structured_output_model")
                    and main_engine.structured_output_model
                ):
                    self.output_schema = main_engine.structured_output_model
                    logger.debug(
                        "Using engine's structured output model as output schema"
                    )
                # Check if engine has output schema
                elif (
                    hasattr(main_engine, "output_schema") and main_engine.output_schema
                ):
                    self.output_schema = main_engine.output_schema
                    logger.debug("Using engine's output schema")

            # If still no output schema, use state schema
            if not self.output_schema and self.state_schema:
                self.output_schema = self.state_schema
                logger.debug("Using state schema as output schema")

    def _setup_schemas(self) -> None:
        """Generate schemas from available engines using SchemaComposer.

        This method:
        1. Uses the SchemaComposer API
        2. Leverages automatic engine management
        3. Supports token usage tracking
        4. Automatically derives I/O schemas
        """
        # Check if we should skip schema generation
        if self.state_schema and not self.use_prebuilt_base and not self.engines:
            logger.debug(
                f"State schema already provided for {
                    self.name}, no engines to integrate"
            )
            # Still derive I/O schemas if needed
            self._auto_derive_io_schemas()
            return

        # CRITICAL: If setup_agent() already set a composed schema, respect it
        if (
            self.state_schema
            and self.use_prebuilt_base
            and hasattr(self.state_schema, "__name__")
            and self.state_schema.__name__
            not in ["MessagesState", "SimpleAgentState", "ToolState"]
        ):
            logger.debug(
                f"State schema already set by setup_agent() to {
                    self.state_schema.__name__}, skipping regeneration"
            )
            # Still derive I/O schemas if needed
            self._auto_derive_io_schemas()
            return

        # Collect all engines
        engine_list = []

        if self.engine:
            engine_list.append(self.engine)

        for _name, component in self.engines.items():
            if isinstance(component, str):  # Skip string references
                continue
            if not hasattr(component, "__class__"):
                continue
            # Check if it's an engine (not an agent)
            if (
                hasattr(component, "engine_type")
                or "Engine" in component.__class__.__name__
            ):
                engine_list.append(component)

        logger.debug(
            f"Setting up schemas for {
                self.name} with {
                len(engine_list)} engines"
        )

        try:
            # Handle case where we have a prebuilt base schema to extend
            if self.state_schema and self.use_prebuilt_base and engine_list:
                logger.debug(
                    f"Extending prebuilt schema {
                        self.state_schema.__name__} with engine fields"
                )
                composer = SchemaComposer(name=f"{self.__class__.__name__}State")

                # First add fields from the prebuilt schema
                composer.add_fields_from_model(self.state_schema)

                # Add all engines - composer will handle engine management and
                # I/O
                for engine in engine_list:
                    composer.add_engine(engine)
                    composer.add_fields_from_engine(engine)

                # Build schema - this will auto-add engine management if needed
                self.state_schema = composer.build()

                logger.debug(
                    f"Extended schema built: {
                        getattr(
                            self.state_schema,
                            '__name__',
                            'Unknown')}"
                )
            elif engine_list:
                # Use SchemaComposer to create schema from engines
                logger.debug(
                    f"Creating schema from {
                        len(engine_list)} engines"
                )
                composer = SchemaComposer(name=f"{self.__class__.__name__}State")

                # Add all engines - composer will handle engine management
                for engine in engine_list:
                    composer.add_engine(engine)
                    composer.add_fields_from_engine(engine)

                # Build schema - this will auto-add engine management if needed
                self.state_schema = composer.build()

                logger.debug(
                    f"Built schema: {
                        getattr(
                            self.state_schema,
                            '__name__',
                            'Unknown')}"
                )
            else:
                logger.debug("No engines found, using default MessagesState")
                # Use prebuilt MessagesState
                from haive.core.schema.prebuilt.messages_state import MessagesState

                self.state_schema = MessagesState

            # Automatically derive input/output schemas if not provided
            self._auto_derive_io_schemas()

            logger.debug(
                f"Schema setup complete. State schema: {
                    self.state_schema}"
            )

        except Exception as e:
            logger.warning(f"Schema generation failed: {e}")
            # Ensure we have at least a basic schema
            if not self.state_schema:
                from langchain_core.messages import BaseMessage
                from pydantic import BaseModel

                class BasicMessagesState(BaseModel):
                    """Fallback state schema with messages field."""

                    messages: list[BaseMessage] = []

                self.state_schema = BasicMessagesState

    def _setup_persistence_from_config(self) -> None:
        """Setup persistence using the PersistenceMixin."""
        # The PersistenceMixin provides this method
        if hasattr(self, "_setup_persistence_from_fields"):
            self._setup_persistence_from_fields()
        else:
            logger.debug(f"No persistence setup method found for {self.name}")

    def _build_initial_graph(self) -> None:
        """Build the initial graph."""
        if not self._graph_built:
            try:
                self.graph = self.build_graph()
                self._graph_built = True
            except Exception as e:
                logger.exception(f"Failed to build graph for {self.name}: {e}")
                # Continue without graph for debugging

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Abstract method to build the agent's graph."""

    # Bridge Workflow.execute and Agent.arun APIs
    async def execute(self, input_data: Any) -> Any:
        """Execute the agent (bridges Workflow API with Agent API)."""
        result = await self.arun(input_data)
        return result

    # Engine-specific convenience methods
    def get_engine(self) -> EngineT | None:
        """Get the main engine with proper typing."""
        return self.engine

    def set_engine(self, engine: EngineT) -> None:
        """Set the main engine with proper typing."""
        self.engine = engine
        # Add to engines dict
        if hasattr(engine, "name") and engine.name:
            self.engines[engine.name] = engine
        else:
            self.engines["main"] = engine

    # ========================================================================
    # HOOKS SYSTEM - Integrated into enhanced Agent
    # ========================================================================

    def add_hook(self, event: HookEvent, hook: HookFunction) -> None:
        """Add a hook function for an event."""
        if event not in self._hooks:
            self._hooks[event] = []
        self._hooks[event].append(hook)
        logger.debug(f"Added hook for {event} on {self.name}")

    def remove_hook(self, event: HookEvent, hook: HookFunction) -> None:
        """Remove a hook function."""
        if event in self._hooks and hook in self._hooks[event]:
            self._hooks[event].remove(hook)
            logger.debug(f"Removed hook for {event} on {self.name}")

    def clear_hooks(self, event: HookEvent | None = None) -> None:
        """Clear hooks for an event or all events."""
        if event:
            self._hooks[event] = []
            logger.debug(f"Cleared hooks for {event} on {self.name}")
        else:
            self._hooks.clear()
            logger.debug(f"Cleared all hooks on {self.name}")

    def execute_hooks(self, event: HookEvent, **context_kwargs) -> list[Any]:
        """Execute all hooks for an event."""
        if not self.hooks_enabled or event not in self._hooks or not self._hooks[event]:
            return []

        # Create context
        context = HookContext(
            event=event,
            agent_name=self.name,
            agent_type=self.__class__.__name__,
            **context_kwargs,
        )

        results = []
        for hook in self._hooks[event]:
            try:
                result = hook(context)
                if result is not None:
                    results.append(result)
            except Exception as e:
                logger.exception(f"Error in hook for {event}: {e}")
                continue

        return results

    # Hook decorators for convenience
    def before_setup(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_setup hook."""
        self.add_hook(HookEvent.BEFORE_SETUP, func)
        return func

    def after_setup(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_setup hook."""
        self.add_hook(HookEvent.AFTER_SETUP, func)
        return func

    def before_run(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_run hook."""
        self.add_hook(HookEvent.BEFORE_RUN, func)
        return func

    def after_run(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_run hook."""
        self.add_hook(HookEvent.AFTER_RUN, func)
        return func

    def on_error(self, func: HookFunction) -> HookFunction:
        """Decorator to add an on_error hook."""
        self.add_hook(HookEvent.ON_ERROR, func)
        return func

    def before_build_graph(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_build_graph hook."""
        self.add_hook(HookEvent.BEFORE_BUILD_GRAPH, func)
        return func

    def after_build_graph(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_build_graph hook."""
        self.add_hook(HookEvent.AFTER_BUILD_GRAPH, func)
        return func

    def before_arun(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_arun hook."""
        self.add_hook(HookEvent.BEFORE_ARUN, func)
        return func

    def after_arun(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_arun hook."""
        self.add_hook(HookEvent.AFTER_ARUN, func)
        return func

    def before_state_update(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_state_update hook."""
        self.add_hook(HookEvent.BEFORE_STATE_UPDATE, func)
        return func

    def after_state_update(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_state_update hook."""
        self.add_hook(HookEvent.AFTER_STATE_UPDATE, func)
        return func

    def pre_process(self, func: HookFunction) -> HookFunction:
        """Decorator to add a pre_process hook."""
        self.add_hook(HookEvent.PRE_PROCESS, func)
        return func

    def post_process(self, func: HookFunction) -> HookFunction:
        """Decorator to add a post_process hook."""
        self.add_hook(HookEvent.POST_PROCESS, func)
        return func

    def before_message_transform(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_message_transform hook."""
        self.add_hook(HookEvent.BEFORE_MESSAGE_TRANSFORM, func)
        return func

    def after_message_transform(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_message_transform hook."""
        self.add_hook(HookEvent.AFTER_MESSAGE_TRANSFORM, func)
        return func

    def before_reflection(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_reflection hook."""
        self.add_hook(HookEvent.BEFORE_REFLECTION, func)
        return func

    def after_reflection(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_reflection hook."""
        self.add_hook(HookEvent.AFTER_REFLECTION, func)
        return func

    def before_grading(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_grading hook."""
        self.add_hook(HookEvent.BEFORE_GRADING, func)
        return func

    def after_grading(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_grading hook."""
        self.add_hook(HookEvent.AFTER_GRADING, func)
        return func

    def before_structured_output(self, func: HookFunction) -> HookFunction:
        """Decorator to add a before_structured_output hook."""
        self.add_hook(HookEvent.BEFORE_STRUCTURED_OUTPUT, func)
        return func

    def after_structured_output(self, func: HookFunction) -> HookFunction:
        """Decorator to add an after_structured_output hook."""
        self.add_hook(HookEvent.AFTER_STRUCTURED_OUTPUT, func)
        return func

    # ========================================================================
    # RECOMPILATION MIXIN INTEGRATION
    # ========================================================================

    def _trigger_auto_recompile(self) -> None:
        """Override RecompileMixin's auto-recompile to trigger graph rebuilding."""
        if self.debug:
            logger.info(f"Auto-recompile triggered for agent '{self.name}'")

        # Execute hooks for recompilation
        if self.hooks_enabled:
            self.execute_hooks(
                HookEvent.BEFORE_BUILD_GRAPH,
                metadata={"compilation_type": "auto_recompile"},
            )

        try:
            # Rebuild the graph
            self.graph = self.build_graph()
            self._graph_built = True

            # Mark recompilation as successful
            self.resolve_recompile(success=True)

            if self.debug:
                logger.info(f"Auto-recompile successful for agent '{self.name}'")

            # Execute after-build hooks
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.AFTER_BUILD_GRAPH,
                    metadata={
                        "compilation_type": "auto_recompile",
                        "graph": self.graph,
                    },
                )

        except Exception as e:
            logger.exception(f"Auto-recompile failed for agent '{self.name}': {e}")
            self.resolve_recompile(success=False)

            # Execute error hooks
            if self.hooks_enabled:
                self.execute_hooks(
                    HookEvent.ON_ERROR,
                    error=e,
                    metadata={"compilation_type": "auto_recompile"},
                )

    def __repr__(self) -> str:
        engine_type = (
            getattr(type(self.engine), "__name__", "None") if self.engine else "None"
        )
        return f"{self.__class__.__name__}[{engine_type}](name='{self.name}')"

    # ========================================================================
    # COMPILATION METHODS
    # ========================================================================

    def compile(self, **kwargs) -> Any:
        """Compile the graph and cache the result.

        Args:
            **kwargs: Additional compilation arguments

        Returns:
            The compiled graph
        """
        if not self._is_compiled or kwargs:
            # Build graph if not already built
            if not hasattr(self, "graph") or self.graph is None:
                logger.debug("Building graph before compilation")
                self._build_initial_graph()

            if not self.graph:
                raise RuntimeError("No graph to compile")

            try:
                # Convert to LangGraph
                lg_graph = self.graph.to_langgraph(state_schema=self.state_schema)

                # Compile with checkpointer and store
                self._app = lg_graph.compile(
                    checkpointer=self.checkpointer,
                    store=self.store,
                    **kwargs
                )
                self._compiled_graph = self._app
                self._is_compiled = True

                logger.debug(f"Graph compiled for agent: {self.name}")
                return self._compiled_graph

            except Exception as e:
                logger.exception(f"Graph compilation failed: {e}")
                raise RuntimeError(f"Failed to compile graph: {e}") from e
        else:
            return self._compiled_graph or self._app

    # ========================================================================
    # REQUIRED ENGINE INTERFACE METHODS
    # ========================================================================

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions as field_name -> (type, default) pairs.

        This implements the abstract method from Engine base class.
        """
        # Return from input schema if defined
        if (
            self.input_schema
            and not isinstance(self.input_schema, dict)
            and hasattr(self.input_schema, "model_fields")
        ):
            fields = {}
            for field_name, field_info in self.input_schema.model_fields.items():
                field_type = field_info.annotation
                field_default = field_info.default
                fields[field_name] = (field_type, field_default)
            return fields

        # Default to empty dict
        return {}

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions as field_name -> (type, default) pairs.

        This implements the abstract method from Engine base class.
        """
        # Return from output schema if defined
        if (
            self.output_schema
            and not isinstance(self.output_schema, dict)
            and hasattr(self.output_schema, "model_fields")
        ):
            fields = {}
            for field_name, field_info in self.output_schema.model_fields.items():
                field_type = field_info.annotation
                field_default = field_info.default
                fields[field_name] = (field_type, field_default)
            return fields

        # Default to empty dict
        return {}

    def create_runnable(
        self, runnable_config: dict[str, Any] | None = None
    ) -> Any:
        """Create and compile the runnable with proper schema kwargs.

        This implements the abstract method from Engine base class.
        """
        if not self._setup_complete:
            raise RuntimeError("Agent setup not complete")

        if not self.graph:
            raise RuntimeError("Graph not built")

        # Compile the graph if not already compiled
        if not self._is_compiled:
            self.compile()

        # Return the compiled app
        return self._compiled_graph or self._app
