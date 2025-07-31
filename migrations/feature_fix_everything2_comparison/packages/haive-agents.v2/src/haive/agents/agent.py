# haive/core/engine/agent/base.py

"""Base Agent class for the Haive framework.

This module provides the abstract base agent class that all agents inherit from,
including execution, state management, and persistence functionality through mixins.
"""

import logging
import re
from abc import ABC, abstractmethod
from typing import Any, Literal

from haive.core.engine.base import Engine, EngineType, InvokableEngine
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema

# Import BaseOutputParser to ensure it's available for LangGraph type
# evaluation
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field, PrivateAttr, create_model, model_validator
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table
from rich.tree import Tree

from haive.agents.base.agent_structured_output_mixin import StructuredOutputMixin

# Import mixins
from haive.agents.base.mixins.execution_mixin import ExecutionMixin
from haive.agents.base.mixins.persistence_mixin import PersistenceMixin
from haive.agents.base.mixins.state_mixin import StateMixin
from haive.agents.base.serialization_mixin import SerializationMixin

# Configure rich logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger(__name__)

# Console for visualization only
console = Console()


class Agent(
    InvokableEngine[BaseModel, BaseModel],
    ExecutionMixin,
    StateMixin,
    PersistenceMixin,
    SerializationMixin,
    StructuredOutputMixin,
    ABC,
):
    """Abstract base agent class that extends InvokableEngine with execution and state management.

    This class provides the foundation for all agent implementations in the Haive framework,
    combining the Engine interface with execution and state management capabilities through mixins.
    It supports automatic schema generation, persistence, and graph compilation.

    The agent lifecycle follows this initialization order:
        1. Normalize engines and setup name
        2. Subclass field syncing (hook: setup_agent())
        3. Schema generation from engines
        4. Persistence setup
        5. Graph building and compilation

    Args:
        name: Agent name, auto-generated from class name if not provided.
        engines: Dictionary of named engines used by this agent.
        engine: Primary/main engine for the agent.
        state_schema: Schema for agent state.
        input_schema: Schema for agent input.
        output_schema: Schema for agent output.
        config_schema: Schema for agent configuration.
        set_schema: Whether to auto-generate schemas from engines.

    Attributes:
        engine_type: Always EngineType.AGENT for agents.
        graph: The workflow graph (excluded from serialization).
        checkpointer: Persistence checkpointer (excluded from serialization).
        store: Optional state store (excluded from serialization).
        config: Reference to AgentConfig (excluded from serialization).

    Example:
        Creating a simple agent with one engine::

            class MyAgent(Agent):
                def setup_agent(self):
                    # Custom setup logic here
                    pass

                def build_graph(self) -> BaseGraph:
                    # Build the workflow graph
                    return my_graph

            agent = MyAgent(
                name="my_agent",
                engine=my_llm_engine
            )
            result = agent.invoke(input_data)

    Note:
        This is an abstract base class. Subclasses must implement the abstract
        methods for graph building and agent setup.
    """

    # Engine type for this agent
    engine_type: Literal[EngineType.AGENT] = Field(
        default=EngineType.AGENT, description="Engine type, always AGENT for agents"
    )

    # Core identification
    name: str = Field(
        default="Agent",
        description="Name of the agent - auto-generated from class name if not provided",
    )

    # Engine management
    engines: dict[str, Engine] = Field(
        default_factory=dict, description="Dictionary of engines this agent uses"
    )

    engine: Engine | None = Field(
        default=None, description="Main/default engine for this agent"
    )

    # Graph state - will be built after setup
    graph: BaseGraph | None = Field(
        default=None,
        exclude=True,
        description="The workflow graph (excluded from serialization)",
    )

    # Schema definitions
    state_schema: type[StateSchema] | type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent state"
    )
    use_prebuilt_base: bool = Field(
        default=False,
        description="Whether to use the state_schema as a base for composition",
    )
    input_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent input"
    )
    output_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent output"
    )
    config_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, exclude=True, description="Schema for agent configuration"
    )

    # Persistence fields (non-serialized)
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

    # Persistence Configuration - these fields ARE serializable
    persistence: Any | None = Field(
        default=True,
        description="Persistence configuration for state checkpointing (defaults to PostgreSQL/Supabase if available)",
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

    # Verbosity for debugging
    verbose: bool = Field(default=False, description="Enable verbose logging")

    # Debug and history flags
    debug: bool = Field(default=False, description="Enable debug mode")
    save_history: bool = Field(default=True, description="Save state history")
    visualize: bool = Field(default=True, description="Enable visualization")

    # Private state tracking
    _graph_built: bool = PrivateAttr(default=False)
    _compiled_graph: CompiledGraph | None = PrivateAttr(default=None)
    _is_compiled: bool = PrivateAttr(default=False)
    _setup_complete: bool = PrivateAttr(default=False)
    _checkpoint_mode: str = PrivateAttr(default="sync")
    _app: Any | None = PrivateAttr(default=None)
    _async_checkpointer: Any | None = PrivateAttr(default=None)
    _async_setup_pending: bool = PrivateAttr(default=False)

    # Schema control flag
    set_schema: Literal[True, False] = Field(
        default=False, description="Whether to auto-generate schemas from engines"
    )

    @model_validator(mode="before")
    @classmethod
    def normalize_engines_and_name(cls, values: dict[str, Any]) -> dict[str, Any]:
        """STEP 1: Normalize engines dict and auto-generate name.

        This validator:
        - Auto-generates agent name from class name if not provided
        - Normalizes engines into a dictionary format
        - Moves single engine to engines dict if needed
        """
        if not isinstance(values, dict):
            return values

        # Auto-generate name from class name if default or empty
        if "name" not in values or not values["name"] or values["name"] == "Agent":
            class_name = cls.__name__
            # Convert CamelCase to readable name (e.g., "SimpleAgent" ->
            # "Simple Agent")
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
        """STEP 2-5: Complete agent setup in proper order.

        This validator handles the main initialization sequence:
        2. Call subclass setup hook for field syncing
        3. Generate schemas from engines (if set_schema is True)
        4. Setup persistence (checkpointer and store)
        5. Build the initial graph
        """
        try:
            # STEP 2: Call subclass setup hook for field syncing
            self.setup_agent()

            # STEP 3: Generate schemas from engines
            self._setup_schemas()

            # STEP 4: Setup persistence using the new mixin
            self._setup_persistence_from_config()

            # STEP 5: Build the initial graph
            self._build_initial_graph()

            self._setup_complete = True

            # Log setup completion with rich formatting
            if self.verbose:
                tree = Tree(
                    f"[bold blue]Agent Setup Complete: {
                        self.name}[/bold blue]"
                )
                tree.add(f"Engine Type: {self.engine_type.value}")
                tree.add(f"Engines: {len(self.engines)}")
                tree.add(
                    f"State Schema: {
                        getattr(
                            self.state_schema,
                            '__name__',
                            'None')}"
                )
                tree.add(
                    f"Input Schema: {
                        getattr(
                            self.input_schema,
                            '__name__',
                            'None')}"
                )
                tree.add(
                    f"Output Schema: {
                        getattr(
                            self.output_schema,
                            '__name__',
                            'None')}"
                )
                logger.info(tree)

        except Exception as e:
            logger.exception(
                f"Failed to setup agent {
                    self.__class__.__name__}: {e}"
            )
            # Don't raise - allow partial setup for better debugging

        return self

    @model_validator(mode="after")
    def ensure_basic_schema(self) -> "Agent":
        """Ensure we always have at least a basic state schema.

        This provides a fallback schema with messages field if no schema is defined.
        """
        if not self.state_schema:
            logger.debug(
                f"No state schema found for {
                    self.name}, creating basic fallback"
            )
            try:
                # Try to import prebuilt MessagesState
                from haive.core.schema.prebuilt.messages_state import MessagesState

                self.state_schema = MessagesState
            except ImportError:
                # Create a very basic state schema as last resort

                from langchain_core.messages import BaseMessage
                from pydantic import BaseModel

                class BasicMessagesState(BaseModel):
                    """Fallback state schema with messages field."""

                    messages: list[BaseMessage] = []

                self.state_schema = BasicMessagesState
                logger.debug(
                    f"Created BasicMessagesState fallback for {
                        self.name}"
                )

        return self

    def setup_agent(self) -> None:
        """Hook for subclasses to perform field syncing and custom setup.

        This method is called BEFORE schema generation and graph building,
        allowing subclasses to sync fields to engines properly.

        Override this method in subclasses for custom setup logic.

        Example:
            def setup_agent(self):
                # Sync fields to engine
                if self.temperature is not None:
                    self.engine.temperature = self.temperature
                # Add engines to registry
                self.engines["main"] = self.engine
        """
        # Default implementation does nothing

    async def _asetup_persistence(self) -> None:
        """Set up asynchronous persistence using the PersistenceMixin."""
        await self._asetup_persistence_from_fields()

    def _setup_schemas(self) -> None:
        """Generate schemas from available engines using enhanced SchemaComposer.

        This method:
        1. Uses the new SchemaComposer instance API
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

        # CRITICAL: If setup_agent() already set a composed schema (like married schema), respect it
        # Check if the schema is not one of the default schemas (MessagesState,
        # etc.)
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

        # Collect all engines and agents
        engine_list = []
        agent_list = []

        if self.engine:
            engine_list.append(self.engine)

        for _name, component in self.engines.items():
            if isinstance(component, str):  # Skip string references
                continue
            if isinstance(component, Agent):
                # It's a sub-agent
                agent_list.append(component)
            else:
                # It's an engine
                engine_list.append(component)

        logger.debug(
            f"Setting up schemas for {
                self.name} with {
                len(engine_list)} engines "
            f"and {
                len(agent_list)} sub-agents"
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
            elif agent_list:
                # Use AgentSchemaComposer for multi-agent scenarios
                logger.debug(
                    f"Creating schema from {
                        len(agent_list)} sub-agents"
                )
                try:
                    from haive.core.schema.agent_schema_composer import (
                        AgentSchemaComposer,
                    )

                    self.state_schema = AgentSchemaComposer.from_agents(
                        agents=agent_list,
                        name=f"{self.__class__.__name__}State",
                        include_meta=True,
                        separation="smart",
                    )
                except ImportError:
                    logger.warning(
                        "AgentSchemaComposer not available, using regular composer"
                    )
                    # Fall back to regular composer for sub-agents
                    composer = SchemaComposer(name=f"{self.__class__.__name__}State")
                    for agent in agent_list:
                        if hasattr(agent, "state_schema"):
                            composer.add_fields_from_model(agent.state_schema)
                    self.state_schema = composer.build()
            elif engine_list:
                # Use enhanced SchemaComposer instance API
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
                logger.debug("No engines or agents found, using default MessagesState")
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
            logger.warning(
                f"Schema generation failed for {self.__class__.__name__}: {e}"
            )
            # Fallback to basic message state
            if not self.state_schema:
                self._create_basic_message_state()

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
                            self.input_schema = create_model(
                                f"{self.name}Input", **fields
                            )
                            logger.debug("Derived input schema from first engine")
                    except Exception as e:
                        logger.debug(f"Could not derive input schema from engine: {e}")

            # Final fallback - messages input
            if not self.input_schema:

                from langchain_core.messages import BaseMessage

                self.input_schema = create_model(
                    f"{self.name}Input",
                    messages=(list[BaseMessage], Field(default_factory=list)),
                )
                logger.debug("Using default messages-based input schema")

        # Derive output schema if not provided
        if not self.output_schema:
            logger.debug("No output schema provided, deriving from available sources")

            # Special handling for engines with structured output
            main_engine = self.main_engine
            if main_engine:
                # FIRST: Check if engine already has a modified output schema
                # (SimpleAgentV2 modifies the engine's output schema to include structured output)
                if hasattr(main_engine, "output_schema") and main_engine.output_schema:
                    # Check if engine has derive_output_schema method
                    if hasattr(main_engine, "derive_output_schema"):
                        try:
                            engine_output_schema = main_engine.derive_output_schema()
                            if engine_output_schema:
                                self.output_schema = engine_output_schema
                                logger.debug(
                                    f"Using engine's modified output schema: {
                                        engine_output_schema.__name__}"
                                )
                                return
                        except Exception as e:
                            logger.debug(
                                f"Could not derive output schema from engine: {e}"
                            )

                    # Fallback: use engine's output_schema directly
                    self.output_schema = main_engine.output_schema
                    logger.debug(
                        f"Using engine's output schema directly: {
                            main_engine.output_schema.__name__}"
                    )
                    return

                # SECOND: Check for structured output model (original logic)
                structured_output = getattr(
                    main_engine, "structured_output_model", None
                )
                if structured_output:
                    # Check if we're using v2 structured output (tool-based)
                    output_version = getattr(
                        main_engine, "structured_output_version", None
                    )

                    if output_version in {"v2", 2}:
                        # For v2, we need to create a schema that includes the parsed output field
                        # Use proper field naming utilities
                        from haive.core.schema.field_utils import (
                            get_field_info_from_model,
                        )

                        field_info = get_field_info_from_model(structured_output)
                        field_name = field_info["field_name"]

                        # Create output schema with just the structured field
                        self.output_schema = create_model(
                            f"{self.name}Output",
                            **{
                                field_name: (
                                    structured_output,
                                    Field(
                                        description=f"Parsed {structured_output.__name__}"
                                    ),
                                )
                            },
                        )
                        logger.debug(
                            f"Created output schema with structured field '{field_name}': {
                                self.output_schema.__name__}"
                        )
                    else:
                        # For v1 or direct structured output, use the model
                        # as-is
                        self.output_schema = structured_output
                        logger.debug(
                            f"Using structured output model as output schema: {
                                structured_output.__name__}"
                        )
                    return

                # Check if engine has specific output field configuration
                output_field_name = getattr(main_engine, "output_field_name", None)
                if output_field_name and hasattr(main_engine, "get_output_fields"):
                    try:
                        fields = main_engine.get_output_fields()
                        # Filter to only include the specified output field
                        if output_field_name in fields:
                            self.output_schema = create_model(
                                f"{self.name}Output",
                                **{output_field_name: fields[output_field_name]},
                            )
                            logger.debug(
                                f"Created output schema with field '{output_field_name}'"
                            )
                            return
                    except Exception as e:
                        logger.debug(
                            f"Could not create output schema from output field: {e}"
                        )

                # Check engine's output fields
                if hasattr(main_engine, "get_output_fields"):
                    try:
                        fields = main_engine.get_output_fields()
                        if fields:
                            # For agents, we typically want a focused output schema
                            # Check if this looks like a state schema (has many
                            # fields)
                            if len(fields) > 5:  # Likely a full state schema
                                # Try to extract just the output-relevant
                                # fields
                                output_fields = {}

                                # Common output field names to look for
                                output_field_names = [
                                    "output",
                                    "result",
                                    "response",
                                    "answer",
                                    "completion",
                                    "generated",
                                    "prediction",
                                    "summary",
                                    "extraction",
                                ]

                                # Also check for any field that matches the
                                # structured output model name
                                if structured_output:
                                    output_field_names.append(
                                        structured_output.__name__.lower()
                                    )

                                for field_name in output_field_names:
                                    if field_name in fields:
                                        output_fields[field_name] = fields[field_name]

                                # If we found output fields, use them
                                if output_fields:
                                    self.output_schema = create_model(
                                        f"{self.name}Output", **output_fields
                                    )
                                    logger.debug(
                                        f"Created focused output schema with fields: {
                                            list(
                                                output_fields.keys())}"
                                    )
                                    return

                                # Otherwise just use messages

                                from langchain_core.messages import BaseMessage

                                self.output_schema = create_model(
                                    f"{self.name}Output",
                                    messages=(
                                        list[BaseMessage],
                                        Field(default_factory=list),
                                    ),
                                )
                                logger.debug(
                                    "Using messages output schema to avoid exposing full state"
                                )
                                return
                            # Small number of fields, use them all
                            self.output_schema = create_model(
                                f"{self.name}Output", **fields
                            )
                            logger.debug("Created output schema from engine fields")
                            return
                    except Exception as e:
                        logger.debug(f"Could not derive output schema from engine: {e}")

            # Try to derive from state schema with focus on output fields
            if self.state_schema and hasattr(self.state_schema, "derive_output_schema"):
                try:
                    self.output_schema = self.state_schema.derive_output_schema(
                        name=f"{self.name}Output"
                    )
                    logger.debug(
                        f"Derived output schema from state schema: {
                            self.output_schema.__name__}"
                    )
                    return
                except Exception as e:
                    logger.debug(f"Could not derive output schema from state: {e}")

            # Final fallback - messages output
            if not self.output_schema:

                from langchain_core.messages import BaseMessage

                self.output_schema = create_model(
                    f"{self.name}Output",
                    messages=(list[BaseMessage], Field(default_factory=list)),
                )
                logger.debug("Using default messages-based output schema")

    def _create_basic_message_state(self) -> None:
        """Create a basic message state schema as fallback."""
        try:
            from haive.core.schema.prebuilt.messages_state import MessagesState

            self.state_schema = MessagesState
            logger.debug("Using MessagesState fallback")
        except ImportError:
            # Create basic state schema

            from langchain_core.messages import BaseMessage
            from pydantic import BaseModel

            class FallbackMessagesState(BaseModel):
                """Fallback state schema with messages field."""

                messages: list[BaseMessage] = []

            self.state_schema = FallbackMessagesState
            logger.debug("Using FallbackMessagesState")

    def _build_initial_graph(self) -> None:
        """Build the initial graph.

        This calls the abstract build_graph method that must be implemented by subclasses.
        """
        try:
            self.graph = self.build_graph()
            self._graph_built = True
        except Exception as e:
            logger.warning(
                f"Initial graph build failed for {
                    self.__class__.__name__}: {e}"
            )
            self.graph = None
            self._graph_built = False

    # ============================================================================
    # ENGINE INTERFACE IMPLEMENTATION
    # ============================================================================

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
            result = {}
            for name, field_info in self.input_schema.model_fields.items():
                field_type = field_info.annotation or Any
                default_value = (
                    field_info.default if field_info.default is not ... else None
                )
                result[name] = (field_type, default_value)
            return result

        # Fallback - return empty to avoid exposing internal state
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
            result = {}
            for name, field_info in self.output_schema.model_fields.items():
                field_type = field_info.annotation or Any
                default_value = (
                    field_info.default if field_info.default is not ... else None
                )
                result[name] = (field_type, default_value)
            return result

        # Fallback - return empty to avoid exposing internal state
        return {}

    def create_runnable(
        self, runnable_config: dict[str, Any] | None = None
    ) -> CompiledGraph:
        """Create and compile the runnable with proper schema kwargs.

        This implements the abstract method from Engine base class.
        """
        if not self._setup_complete:
            raise RuntimeError("Agent setup not complete")

        if not self.graph:
            self._ensure_graph_built()

        if not self.graph:
            raise ValueError("Graph could not be built")

        # Ensure we have schemas - regenerate if needed
        if not self.state_schema:
            logger.warning(
                f"No state schema found for {
                    self.name}, regenerating..."
            )
            self._setup_schemas()

        # Build schema kwargs - only pass what StateGraph expects
        schema_kwargs = {}

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
        logger.debug(
            f"Schema kwargs for {
                self.name}: {
                list(
                    schema_kwargs.keys())}"
        )
        logger.debug(f"State schema: {self.state_schema}")
        logger.debug(f"Input schema: {self.input_schema}")
        logger.debug(f"Output schema: {self.output_schema}")

        # Convert BaseGraph to LangGraph with schemas
        try:
            langgraph = self.graph.to_langgraph(**schema_kwargs)
        except Exception as e:
            logger.exception(f"Failed to convert graph to langgraph: {e}")
            logger.exception(
                f"Schema kwargs were: {
                    list(
                        schema_kwargs.keys())}"
            )
            logger.exception(f"State schema type: {type(self.state_schema)}")
            raise

        # Now compile the LangGraph StateGraph with checkpointer and runtime
        # config
        compile_kwargs = {}

        # Always add our checkpointer
        if self.checkpointer:
            compile_kwargs["checkpointer"] = self.checkpointer

        # Add store if available
        if self.store:
            compile_kwargs["store"] = self.store

        # Extract compilation-relevant parameters from runnable_config if
        # provided
        if runnable_config:
            if "interrupt_before" in runnable_config:
                compile_kwargs["interrupt_before"] = runnable_config["interrupt_before"]
            if "interrupt_after" in runnable_config:
                compile_kwargs["interrupt_after"] = runnable_config["interrupt_after"]

        # Compile the LangGraph StateGraph
        return langgraph.compile(**compile_kwargs)

    # ============================================================================
    # GRAPH MANAGEMENT
    # ============================================================================

    @property
    def main_engine(self) -> Engine | None:
        """Get the main engine (prioritize engine field, then first in engines dict)."""
        if self.engine:
            return self.engine
        if self.engines:
            return next(iter(self.engines.values()), None)
        return None

    def _invalidate_graph(self) -> None:
        """Mark graph as needing rebuild."""
        self._graph_built = False
        self._is_compiled = False
        self.graph = None
        self._compiled_graph = None

    def _ensure_graph_built(self) -> None:
        """Ensure the graph is built. Rebuild if needed."""
        if not self._graph_built or self.graph is None:
            self.graph = self.build_graph()
            self._graph_built = True

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Abstract method to build the agent's graph.

        This is called after field syncing and schema generation.
        Must be implemented by all concrete agent classes.

        Returns:
            The constructed BaseGraph for this agent
        """
        raise NotImplementedError(
            "build_graph method must be implemented by subclasses"
        )

    def rebuild_graph(self) -> BaseGraph:
        """Force rebuild the graph."""
        self._invalidate_graph()
        try:
            self.graph = self.build_graph()
            self._graph_built = True
        except Exception as e:
            logger.exception(
                f"Failed to rebuild graph for {self.__class__.__name__}: {e}"
            )
            raise
        return self.graph

    def regenerate_schemas(self) -> None:
        """Regenerate schemas from current engines."""
        # Clear existing schemas
        self.state_schema = None
        self.input_schema = None
        self.output_schema = None

        # Regenerate
        self._setup_schemas()

    def compile(self, **kwargs) -> CompiledGraph:
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
                self._ensure_graph_built()

            if not self.graph:
                raise RuntimeError("Graph not built")

            # Ensure persistence is set up if not already done
            # TEMPORARILY DISABLED to debug PydanticUndefined issue
            # if not hasattr(self, "checkpointer") or self.checkpointer is None:
            #     logger.debug("Setting up persistence before compilation")
            #     self._setup_persistence_from_config()

            # Make sure checkpointer tables are set up if needed
            if self.checkpointer and hasattr(self.checkpointer, "setup"):
                try:
                    from haive.core.persistence.handlers import ensure_pool_open

                    ensure_pool_open(self.checkpointer)
                    self.checkpointer.setup()
                    logger.debug("Checkpointer tables set up successfully")
                except Exception as e:
                    logger.exception(f"Error setting up checkpointer tables: {e}")

            # First, we need to convert BaseGraph to LangGraph StateGraph
            # Build schema kwargs for conversion
            schema_kwargs = {}

            # Ensure we have schemas
            if not self.state_schema:
                logger.warning(
                    f"No state schema found for {self.name}, regenerating..."
                )
                self._setup_schemas()

            # Add schemas to kwargs
            if self.state_schema:
                schema_kwargs["state_schema"] = self.state_schema
            else:
                raise ValueError(f"No state schema available for {self.name}")

            if self.input_schema:
                schema_kwargs["input"] = self.input_schema

            if self.output_schema:
                schema_kwargs["output"] = self.output_schema

            if self.config_schema:
                schema_kwargs["config_schema"] = self.config_schema

            # Convert BaseGraph to LangGraph StateGraph
            try:
                langgraph_graph = self.graph.to_langgraph(**schema_kwargs)
                logger.debug("Successfully converted BaseGraph to LangGraph StateGraph")
            except Exception as e:
                logger.exception(f"Failed to convert BaseGraph to LangGraph: {e}")
                raise

            # Now compile the LangGraph StateGraph with checkpointer and store
            compile_kwargs = kwargs.copy()

            # Add checkpointer if we have one and it's not already specified
            if self.checkpointer and "checkpointer" not in compile_kwargs:
                compile_kwargs["checkpointer"] = self.checkpointer

            # Add store if available and not already specified
            if self.store and "store" not in compile_kwargs:
                compile_kwargs["store"] = self.store

            logger.debug(
                f"Compiling LangGraph with kwargs: {
                    list(
                        compile_kwargs.keys())}"
            )

            # The LangGraph StateGraph.compile() method accepts checkpointer
            # and store
            self._app = langgraph_graph.compile(**compile_kwargs)
            self._compiled_graph = self._app
            self._is_compiled = True

        if self._compiled_graph is None:
            raise RuntimeError("Failed to compile graph")

        return self._compiled_graph

    # ============================================================================
    # ENGINE INVOCATION INTERFACE
    # ============================================================================

    def invoke(self, input_data: Any, config: RunnableConfig | None = None) -> Any:
        """Invoke the agent using ExecutionMixin's run method.

        This implements the Engine interface's invoke method.

        Args:
            input_data: Input data for the agent
            config: Optional runtime configuration

        Returns:
            Output from the agent
        """
        return self.run(input_data, config=config)

    async def ainvoke(
        self, input_data: Any, config: dict[str, Any] | None = None
    ) -> Any:
        """Async invoke the agent using ExecutionMixin's arun method.

        This implements the Engine interface's ainvoke method.

        Args:
            input_data: Input data for the agent
            config: Optional runtime configuration

        Returns:
            Output from the agent
        """
        return await self.arun(input_data, config=config)

    # ============================================================================
    # UTILITY METHODS
    # ============================================================================

    def __repr__(self) -> str:
        """String representation of the agent."""
        engine_count = len(self.engines)
        main_engine = self.main_engine
        engine_type = type(main_engine).__name__ if main_engine else "None"
        return f"{
            self.__class__.__name__}(name='{
            self.name}', engines={engine_count}, main_engine={engine_type})"

    def get_all_tools(self) -> list[Any]:
        """Collect all tools from all engines and state schema.

        Returns:
            List of all tools available across all engines and state schema
        """
        tools = []

        # Get tools from main engine
        if self.engine and hasattr(self.engine, "tools"):
            engine_tools = getattr(self.engine, "tools", None)
            if engine_tools:
                tools.extend(engine_tools)

        # Get tools from all engines
        for engine in self.engines.values():
            if not isinstance(engine, str) and hasattr(engine, "tools"):
                engine_tools = getattr(engine, "tools", None)
                if engine_tools:
                    tools.extend(engine_tools)

        # Get tools from state schema if available
        state_tools = self.get_state_tools()
        if state_tools:
            tools.extend(state_tools)

        # Get tools from class-level engines in state schema
        class_engines = self.get_all_class_engines()
        for engine in class_engines.values():
            if hasattr(engine, "tools"):
                engine_tools = getattr(engine, "tools", None)
                if engine_tools:
                    tools.extend(engine_tools)

        # Remove duplicates while preserving order
        seen = set()
        unique_tools = []
        for tool in tools:
            # Use tool name or id for deduplication
            tool_id = getattr(tool, "name", getattr(tool, "__name__", id(tool)))
            if tool_id not in seen:
                seen.add(tool_id)
                unique_tools.append(tool)

        logger.debug(
            f"Agent {
                self.name} collected {
                len(unique_tools)} unique tools from all sources"
        )
        return unique_tools

    def get_all_tool_schemas(self) -> list[Any]:
        """Collect all tool schemas from engines for validation.

        Returns:
            List of tool schemas/classes for validation
        """
        schemas = []
        tools = self.get_all_tools()

        for tool in tools:
            # Add the tool class itself if it's a Pydantic model
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                schemas.append(tool)
            # Check if tool has a schema attribute
            elif hasattr(tool, "args_schema") and tool.args_schema:
                schemas.append(tool.args_schema)
            # Check if tool has structured_output_model
            elif (
                hasattr(tool, "structured_output_model")
                and tool.structured_output_model
            ):
                schemas.append(tool.structured_output_model)

        logger.debug(
            f"Agent {
                self.name} collected {
                len(schemas)} tool schemas"
        )
        return schemas

    def visualize_graph(self, output_path: str | None = None) -> None:
        """Generate and save a visualization of the agent's graph.

        Args:
            output_path: Optional custom path for visualization output
        """
        if not self._app:
            logger.warning("Cannot visualize graph: Not compiled yet")
            return

        try:
            import os
            from datetime import datetime

            if not output_path:
                # Use default path
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_dir = "resources/graph_images"
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, f"{self.name}_{timestamp}.png")

            # Generate the visualization
            png_data = self._app.get_graph(xray=True).draw_mermaid_png()

            # Save the PNG data
            with open(output_path, "wb") as f:
                f.write(png_data)

            logger.info(f"Graph visualization saved to: {output_path}")

        except Exception as e:
            logger.exception(f"Error visualizing graph: {e}")

    # ============================================================================
    # ENGINE ACCESS METHODS (StateSchema-compatible interface)
    # ============================================================================

    def get_class_engine(self, name: str) -> Engine | None:
        """Get a class-level engine by name from the state schema.

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        if self.state_schema and hasattr(self.state_schema, "get_class_engine"):
            return self.state_schema.get_class_engine(name)
        return None

    def get_all_class_engines(self) -> dict[str, Engine]:
        """Get all class-level engines from the state schema.

        Returns:
            Dictionary of all engines
        """
        if self.state_schema and hasattr(self.state_schema, "get_all_class_engines"):
            return self.state_schema.get_all_class_engines()
        return {}

    def get_instance_engine(self, name: str) -> Engine | None:
        """Get an engine from instance or class level (via state schema).

        Args:
            name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        # First check agent's own engines
        if name in self.engines:
            return self.engines[name]

        # Check main engine
        if self.engine and getattr(self.engine, "name", None) == name:
            return self.engine

        # Then check state schema engines
        if self.state_schema and hasattr(self.state_schema, "get_instance_engine"):
            return self.state_schema.get_instance_engine(name)

        return None

    def get_all_instance_engines(self) -> dict[str, Engine]:
        """Get all engines from both instance and class level.

        Returns:
            Dictionary mapping engine names to engine instances
        """
        engines = {}

        # Get engines from state schema first
        if self.state_schema and hasattr(self.state_schema, "get_all_instance_engines"):
            engines.update(self.state_schema.get_all_instance_engines())

        # Add agent's own engines (may override schema engines)
        engines.update(self.engines)

        # Add main engine if it has a name
        if self.engine and hasattr(self.engine, "name") and self.engine.name:
            engines[self.engine.name] = self.engine

        return engines

    def has_engine(self, name: str) -> bool:
        """Check if an engine exists in this agent.

        Args:
            name: Name of the engine to check

        Returns:
            True if engine exists, False otherwise
        """
        return self.get_instance_engine(name) is not None

    def add_tool_to_state(
        self,
        tool: Any,
        route: str | None = None,
        target_engine: str | None = None,
    ) -> None:
        """Add a tool to the agent's state schema if it supports tools.

        Args:
            tool: Tool to add
            route: Optional explicit route/type
            target_engine: Optional specific engine name to add tool to
        """
        # Create a state instance to add the tool
        if self.state_schema:
            try:
                # Create a temporary state instance
                state_instance = self.state_schema()

                # Check if state supports tools
                if hasattr(state_instance, "add_tool"):
                    if target_engine:
                        state_instance.add_tool_to_engine(tool, target_engine, route)
                    else:
                        state_instance.add_tool(tool, route, target_engine)
                    logger.debug(
                        f"Added tool to state schema: {
                            getattr(
                                tool,
                                'name',
                                str(tool))}"
                    )
                else:
                    logger.warning(
                        f"State schema {
                            self.state_schema.__name__} does not support tools"
                    )
            except Exception as e:
                logger.exception(f"Failed to add tool to state: {e}")

    def configure_engine_routes(self, engine_type: str, routes: list[str]) -> None:
        """Configure which tool routes an engine type should accept in the state schema.

        Args:
            engine_type: The engine type (e.g., 'llm', 'retriever', etc.)
            routes: List of tool routes this engine type should accept
        """
        if self.state_schema:
            try:
                # Create a temporary state instance
                state_instance = self.state_schema()

                # Check if state supports route configuration
                if hasattr(state_instance, "configure_engine_routes"):
                    state_instance.configure_engine_routes(engine_type, routes)
                    logger.debug(
                        f"Configured routes for engine type '{engine_type}': {routes}"
                    )
                else:
                    logger.warning(
                        f"State schema {
                            self.state_schema.__name__} does not support route configuration"
                    )
            except Exception as e:
                logger.exception(f"Failed to configure engine routes: {e}")

    def get_state_tools(self) -> list[Any]:
        """Get all tools from the state schema if it supports tools.

        Returns:
            List of tools from the state schema, empty list if not supported
        """
        if self.state_schema:
            try:
                # Create a temporary state instance
                state_instance = self.state_schema()

                # Check if state has tools
                if hasattr(state_instance, "tools"):
                    return getattr(state_instance, "tools", [])
            except Exception as e:
                logger.exception(f"Failed to get state tools: {e}")

        return []

    def sync_tools_to_engines(self) -> None:
        """Manually trigger tool synchronization to engines in the state schema."""
        if self.state_schema:
            try:
                # Create a temporary state instance
                state_instance = self.state_schema()

                # Check if state supports tool syncing
                if hasattr(state_instance, "_sync_tools_to_engines_by_route"):
                    state_instance._sync_tools_to_engines_by_route()
                    logger.debug("Manually triggered tool synchronization to engines")
                else:
                    logger.warning(
                        f"State schema {
                            self.state_schema.__name__} does not support tool syncing"
                    )
            except Exception as e:
                logger.exception(f"Failed to sync tools to engines: {e}")

    def get_schema_info(self) -> dict[str, Any]:
        """Get comprehensive information about the agent's schema system.

        Returns:
            Dictionary containing schema information including engines, tools, and capabilities
        """
        info = {
            "agent_name": self.name,
            "agent_engines": list(self.engines.keys()),
            "main_engine": getattr(self.engine, "name", None) if self.engine else None,
            "state_schema": {
                "name": (
                    getattr(self.state_schema, "__name__", None)
                    if self.state_schema
                    else None
                ),
                "class_engines": [],
                "supports_tools": False,
                "supports_routing": False,
                "tools_count": 0,
            },
            "input_schema": {
                "name": (
                    getattr(self.input_schema, "__name__", None)
                    if self.input_schema
                    else None
                ),
                "fields": [],
            },
            "output_schema": {
                "name": (
                    getattr(self.output_schema, "__name__", None)
                    if self.output_schema
                    else None
                ),
                "fields": [],
            },
            "total_engines": 0,
            "total_tools": 0,
        }

        # Get class-level engines from state schema
        class_engines = self.get_all_class_engines()
        info["state_schema"]["class_engines"] = list(class_engines.keys())

        # Check if state schema supports tools and routing
        if self.state_schema:
            try:
                state_instance = self.state_schema()
                info["state_schema"]["supports_tools"] = hasattr(
                    state_instance, "tools"
                )
                info["state_schema"]["supports_routing"] = hasattr(
                    state_instance, "tool_routes"
                )

                if hasattr(state_instance, "tools"):
                    info["state_schema"]["tools_count"] = len(
                        getattr(state_instance, "tools", [])
                    )
            except Exception as e:
                logger.debug(f"Could not analyze state schema: {e}")

        # Add input schema fields
        if self.input_schema and hasattr(self.input_schema, "model_fields"):
            info["input_schema"]["fields"] = list(self.input_schema.model_fields.keys())

        # Add output schema fields
        if self.output_schema and hasattr(self.output_schema, "model_fields"):
            info["output_schema"]["fields"] = list(
                self.output_schema.model_fields.keys()
            )

        # Count total engines and tools
        all_engines = self.get_all_instance_engines()
        info["total_engines"] = len(all_engines)
        info["total_tools"] = len(self.get_all_tools())

        return info

    def display_schema_info(self) -> None:
        """Display comprehensive information about the agent's schema system using rich formatting."""
        info = self.get_schema_info()

        # Create a table for schema information
        table = Table(title=f"Agent Schema Information: {info['agent_name']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        # Add agent info
        table.add_row("Agent Engines", str(info["agent_engines"]))
        table.add_row("Main Engine", str(info["main_engine"]))
        table.add_row("Total Engines", str(info["total_engines"]))
        table.add_row("Total Tools", str(info["total_tools"]))

        # Add state schema info
        table.add_section()
        table.add_row("State Schema", str(info["state_schema"]["name"]))
        table.add_row("  Class Engines", str(info["state_schema"]["class_engines"]))
        table.add_row(
            "  Supports Tools", "✅" if info["state_schema"]["supports_tools"] else "❌"
        )
        table.add_row(
            "  Supports Routing",
            "✅" if info["state_schema"]["supports_routing"] else "❌",
        )
        table.add_row("  Tools Count", str(info["state_schema"]["tools_count"]))

        # Add input/output schema info
        table.add_section()
        table.add_row("Input Schema", str(info["input_schema"]["name"]))
        if info["input_schema"]["fields"]:
            table.add_row("  Fields", ", ".join(info["input_schema"]["fields"]))

        table.add_row("Output Schema", str(info["output_schema"]["name"]))
        if info["output_schema"]["fields"]:
            table.add_row("  Fields", ", ".join(info["output_schema"]["fields"]))

        logger.info(table)

        # Show detailed engine information if verbose
        if self.verbose:
            all_engines = self.get_all_instance_engines()
            if all_engines:
                engine_tree = Tree("All Available Engines")
                for name, engine in all_engines.items():
                    engine_type = getattr(engine, "engine_type", "unknown")
                    tool_count = len(getattr(engine, "tools", []))
                    engine_tree.add(f"{name}: {engine_type} ({tool_count} tools)")
                logger.info(engine_tree)

    def derive_input_schema(
        self, engine_name: str | None = None, name: str | None = None
    ) -> type[BaseModel] | None:
        """Derive input schema from the agent's state schema.

        Args:
            engine_name: Optional name of the engine to target (default: all inputs)
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for input validation, or None if state schema doesn't support it
        """
        if not self.state_schema:
            logger.warning("No state schema available to derive input schema from")
            return None

        # Check if state schema has derive_input_schema method
        if hasattr(self.state_schema, "derive_input_schema"):
            try:
                schema_name = name or f"{self.name}InputSchema"
                return self.state_schema.derive_input_schema(
                    engine_name=engine_name, name=schema_name
                )
            except Exception as e:
                logger.exception(f"Failed to derive input schema: {e}")
                return None
        else:
            logger.warning(
                f"State schema {
                    getattr(
                        self.state_schema,
                        '__name__',
                        'Unknown')} does not support input schema derivation"
            )
            return None

    def derive_output_schema(
        self, engine_name: str | None = None, name: str | None = None
    ) -> type[BaseModel] | None:
        """Derive output schema from the agent's state schema.

        Args:
            engine_name: Optional name of the engine to target (default: all outputs)
            name: Optional name for the schema class

        Returns:
            A BaseModel subclass for output validation, or None if state schema doesn't support it
        """
        if not self.state_schema:
            logger.warning("No state schema available to derive output schema from")
            return None

        # Check if state schema has derive_output_schema method
        if hasattr(self.state_schema, "derive_output_schema"):
            try:
                schema_name = name or f"{self.name}OutputSchema"
                return self.state_schema.derive_output_schema(
                    engine_name=engine_name, name=schema_name
                )
            except Exception as e:
                logger.exception(f"Failed to derive output schema: {e}")
                return None
        else:
            logger.warning(
                f"State schema {
                    getattr(
                        self.state_schema,
                        '__name__',
                        'Unknown')} does not support output schema derivation"
            )
            return None

    def auto_derive_schemas(self) -> None:
        """Automatically derive and set input and output schemas from the state schema.

        This convenience method will derive input and output schemas from the state schema
        and set them on the agent if they haven't been explicitly set.
        """
        # Only derive if not already set
        if not self.input_schema:
            derived_input = self.derive_input_schema()
            if derived_input:
                self.input_schema = derived_input
                logger.debug(f"Auto-derived input schema: {derived_input.__name__}")

        if not self.output_schema:
            derived_output = self.derive_output_schema()
            if derived_output:
                self.output_schema = derived_output
                logger.debug(f"Auto-derived output schema: {derived_output.__name__}")

    def get_derived_schemas(self) -> dict[str, type[BaseModel] | None]:
        """Get all derived schemas (input and output) from the state schema.

        Returns:
            Dictionary containing derived input and output schemas
        """
        return {
            "input_schema": self.derive_input_schema(),
            "output_schema": self.derive_output_schema(),
            "state_schema": self.state_schema,
        }

    # ============================================================================
    # AGENT AS TOOL CLASS METHODS - COMMENTED OUT FOR NOW
    # ============================================================================

    # @classmethod
    # def as_tool(
    #     cls, name: str | None = None, description: str | None = None, **agent_kwargs
    # ):
    #     """Convert this agent class to a LangChain tool.
    #
    #     This creates a tool that instantiates and executes the agent class.
    #     Uses the agent's input and output schemas for proper type handling.
    #
    #     Args:
    #         name: Optional tool name, defaults to class name + '_tool'
    #         description: Optional tool description
    #         **agent_kwargs: Arguments to pass to agent constructor
    #
    #     Returns:
    #         A LangChain tool that executes this agent class
    #     """
    #     from langchain_core.tools import tool
    #
    #     tool_name = name or f"{cls.__name__.lower()}_tool"
    #     tool_description = description or f"Execute {cls.__name__} for processing"
    #
    #     # Try to get input schema from the agent class
    #     # TODO: This could be enhanced to use actual agent input_schema when available
    #
    #     @tool(tool_name, description=tool_description)
    #     def agent_tool(query: str) -> str:
    #         # Create agent instance
    #         agent = cls(**agent_kwargs)
    #
    #         # Execute agent with query
    #         # TODO: Use agent's actual input schema format
    #         result = agent.invoke({"messages": [{"role": "user", "content": query}]})
    #
    #         # Extract response based on output schema
    #         # TODO: Use agent's actual output schema
    #         if isinstance(result, dict):
    #             if "messages" in result and result["messages"]:
    #                 return result["messages"][-1].get("content", str(result))
    #             elif "output" in result:
    #                 return result["output"]
    #
    #         return str(result)
    #
    #     return agent_tool
