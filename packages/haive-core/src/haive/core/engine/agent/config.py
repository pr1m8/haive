"""Agent configuration for the Haive framework with protocol support.

This module provides the AgentConfig base class for configuring agent components
with protocol-based validation and type checking to ensure that agent implementations
conform to the expected interfaces.

TODO: Consisnteny in naming of persistence configs.
TODO: Need to seperate and implement the registry system, similar to retrievers and add base.
TODO: Need to clean up patterns and registry system.
"""

import json
import logging
import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Dict,
    Generic,
    List,
    Literal,
    Optional,
    Type,
    TypeVar,
    Union,
    get_args,
    get_origin,
)

from langchain_core.runnables import RunnableConfig
from langgraph.graph import END
from pydantic import BaseModel, Field, model_validator

from haive.core.config.runnable import RunnableConfigManager

# Import the protocol definitions
from haive.core.engine.agent.protocols import (
    AgentProtocol,
    ExtensibilityAgentProtocol,
    PersistentAgentProtocol,
    StreamingAgentProtocol,
    VisualizationAgentProtocol,
)
from haive.core.engine.base import Engine, EngineType, InvokableEngine
from haive.core.graph.node.config import NodeConfig
from haive.core.persistence.base import CheckpointerConfig

# Import persistence-related functionality
from haive.core.schema.schema_composer import SchemaComposer

# Check if PostgreSQL dependencies are available
try:
    from langgraph.checkpoint.postgres import PostgresSaver

    from haive.core.persistence.memory import MemoryCheckpointerConfig
    from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

    POSTGRES_AVAILABLE = True
except ImportError:
    from haive.core.persistence.memory import MemoryCheckpointerConfig

    POSTGRES_AVAILABLE = False

if TYPE_CHECKING:
    from haive.core.engine.agent.agent import Agent

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

# Type variables for generics
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")
TState = TypeVar("TState")


class PatternConfig(BaseModel):
    """Configuration for a pattern to be applied to an agent.

    This allows detailed configuration of pattern application,
    including parameters, application order, and conditions.
    """

    name: str = Field(description="Name of the pattern to apply")
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Parameters for pattern application"
    )
    order: int | None = Field(
        default=None, description="Order to apply pattern (lower numbers first)"
    )
    condition: str | None = Field(
        default=None, description="Condition for pattern application"
    )
    enabled: bool = Field(default=True, description="Whether this pattern is enabled")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    model_config = {"arbitrary_types_allowed": True}

    def merge_with(self, other: "PatternConfig") -> "PatternConfig":
        """Merge this pattern configuration with another.

        Args:
            other: The other pattern config to merge with

        Returns:
            New merged pattern config
        """
        # Start with a copy of this config
        merged_params = self.parameters.copy()

        # Update with other parameters
        merged_params.update(other.parameters)

        # Create new config with merged parameters
        return PatternConfig(
            name=self.name,
            parameters=merged_params,
            order=other.order if other.order is not None else self.order,
            condition=(
                other.condition if other.condition is not None else self.condition
            ),
            enabled=other.enabled,
            metadata={**self.metadata, **other.metadata},
        )


class AgentConfig(InvokableEngine[TIn, TOut], Generic[TIn, TOut, TState]):
    """Base configuration for an agent architecture.
    Extends InvokableEngine to provide a consistent interface with the Engine framework.

    This class is designed to NEVER include __runnable_config__ in any schemas.
    By default, it uses PostgreSQL for persistence if available.

    This implementation supports protocol validation to ensure that agent
    implementations conform to the expected interfaces.
    """

    # Class variables for schema caching
    _schema_cache: ClassVar[dict[str, type[BaseModel]]] = {}
    _input_schema_cache: ClassVar[dict[str, type[BaseModel]]] = {}
    _output_schema_cache: ClassVar[dict[str, type[BaseModel]]] = {}

    # Expected protocols for agent implementations
    expected_protocols: ClassVar[list[type]] = [
        AgentProtocol,  # Core functionality (required)
        StreamingAgentProtocol,  # Streaming support
        PersistentAgentProtocol,  # Persistence capabilities
        VisualizationAgentProtocol,  # Visualization support
        ExtensibilityAgentProtocol,  # Pattern-based extensibility
    ]

    engine_type: EngineType = Field(default=EngineType.AGENT)
    name: str = Field(default_factory=lambda: f"agent_{uuid.uuid4().hex[:8]}")

    # Primary engine (used as default processor)
    engine: Engine | str | None = None

    # Additional named engines
    engines: dict[str, Engine | str] = Field(default_factory=dict)

    # Schema definitions
    state_schema: Type[BaseModel] | Dict[str, Any] | None = None
    input_schema: Type[BaseModel] | Dict[str, Any] | None = None
    output_schema: Type[BaseModel] | Dict[str, Any] | None = None

    # Node configurations
    node_configs: dict[str, NodeConfig] = Field(
        default_factory=dict,
        description="Node configurations for explicit workflow definition",
    )

    # Pattern system integration
    patterns: list[PatternConfig] = Field(
        default_factory=list, description="Patterns to apply to this agent"
    )
    pattern_parameters: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Global parameters for patterns by name"
    )
    default_patterns: list[str | dict[str, Any]] = Field(
        default_factory=list,
        description="Patterns to apply by default during initialization",
    )

    # Visualization and debugging
    visualize: bool = Field(default=True)
    output_dir: str = Field(default="resources/graph_images")
    debug: bool = Field(default=False)
    save_history: bool = Field(default=True)

    # Runtime settings
    runnable_config: RunnableConfig = Field(
        default={
            "configurable": {"thread_id": str(uuid.uuid4()), "recursion_limit": 200}
        }
    )

    # Storage
    add_store: bool = Field(default=False)

    # Agent-specific settings (to be overridden by subclasses)
    agent_settings: dict[str, Any] = Field(default_factory=dict)

    # Recursive agent composition
    subagents: dict[str, "AgentConfig"] = Field(
        default_factory=dict, description="Subagents for recursive composition"
    )

    # Version and metadata for serialization
    version: str = Field(
        default="1.0.0", description="Version of this agent configuration"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for this agent"
    )

    # =============================================
    # Persistence Configuration - DEFAULT TO POSTGRES IF AVAILABLE
    # =============================================
    persistence: CheckpointerConfig | None = Field(
        default_factory=lambda: (
            PostgresCheckpointerConfig()
            if POSTGRES_AVAILABLE
            else MemoryCheckpointerConfig()
        ),
        description="Persistence configuration for state checkpointing",
    )

    # Add new checkpoint_mode field with default "sync"
    checkpoint_mode: str = Field(
        default="sync", description="Checkpoint mode: 'sync', 'async', or 'none'"
    )

    model_config = {"arbitrary_types_allowed": True}

    # Instance cache for derived schemas
    _state_schema_instance: type[BaseModel] | None = None
    _input_schema_instance: type[BaseModel] | None = None
    _output_schema_instance: type[BaseModel] | None = None

    # Pattern application tracking
    _applied_patterns: set = set()

    # Testing mode flag
    _testing_mode: bool = False

    @model_validator(mode="after")
    def ensure_engine(self):
        """Ensure at least one engine is available."""
        if not self.engine and not self.engines and not self.node_configs:
            from haive.core.engine.aug_llm import AugLLMConfig

            self.engine = AugLLMConfig()
        return self

    @model_validator(mode="after")
    def ensure_state_schema(self):
        """Ensure state schema is derived if not provided."""
        # Only auto-generate schema if explicitly requested AND no schema is provided
        if self.state_schema is None and getattr(self, "set_schema", False):
            self.state_schema = self.derive_schema()
        return self

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions as field_name -> (type, default) pairs.

        Implements the abstract method from Engine base class.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        # Check if we have an explicit input_schema defined
        if self.input_schema is not None:
            return {
                name: (field_info.annotation, field_info.default)
                for name, field_info in self.input_schema.model_fields.items()
            }

        # Fallback to state_schema if available
        if hasattr(self, "state_schema") and self.state_schema is not None:
            return {
                name: (field_info.annotation, field_info.default)
                for name, field_info in self.state_schema.model_fields.items()
            }

        # Return empty dict if no schema available
        return {}

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions as field_name -> (type, default) pairs.

        Implements the abstract method from Engine base class.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        # Check if we have an explicit output_schema defined
        if self.output_schema is not None:
            return {
                name: (field_info.annotation, field_info.default)
                for name, field_info in self.output_schema.model_fields.items()
            }

        # Fallback to state_schema if available
        if hasattr(self, "state_schema") and self.state_schema is not None:
            return {
                name: (field_info.annotation, field_info.default)
                for name, field_info in self.state_schema.model_fields.items()
            }

        # Return empty dict if no schema available
        return {}

    def add_node_config(
        self, name: str, engine: Union[Engine, str, "NodeConfig"], **kwargs
    ) -> "AgentConfig":
        """Add a node configuration to this agent with schema integration.

        Args:
            name: Name of the node
            engine: Engine, engine name, or NodeConfig
            **kwargs: Additional parameters for NodeConfig

        Returns:
            Self for method chaining
        """
        # Import here to avoid circular imports
        from haive.core.graph.node.config import NodeConfig

        # Handle END constant conversion for command_goto
        if "command_goto" in kwargs and kwargs["command_goto"] == "END":
            kwargs["command_goto"] = END

        # Create NodeConfig if not already one
        if not isinstance(engine, NodeConfig):
            node_config = NodeConfig(name=name, engine=engine, **kwargs)
        else:
            node_config = engine

        self.node_configs[name] = node_config

        # Add engine to components if it's an Engine
        engine_ref = node_config.engine
        if isinstance(engine_ref, Engine):
            if self.engine is None:
                self.engine = engine_ref
            elif engine_ref not in self.engines.values():
                engine_name = getattr(engine_ref, "name", f"engine_{len(self.engines)}")
                self.engines[engine_name] = engine_ref

            # Invalidate schema caches since components changed
            self._invalidate_schema_caches()

        return self

    def _invalidate_schema_caches(self):
        """Invalidate all schema caches for this specific instance.

        This focuses on instance-level caches without affecting class-level caches.
        """
        self._state_schema_instance = None
        self._input_schema_instance = None
        self._output_schema_instance = None

    def add_subagent(self, name: str, agent_config: "AgentConfig") -> "AgentConfig":
        """Add a subagent for recursive composition with proper schema integration.

        Args:
            name: Name of the subagent
            agent_config: Configuration for the subagent

        Returns:
            Self for method chaining
        """
        self.subagents[name] = agent_config

        # Invalidate schema caches
        self._invalidate_schema_caches()

        return self

    def get_schema_manager(self, schema_instance=None):
        """Get a StateSchemaManager for the agent's schema.

        Args:
            schema_instance: Optional specific schema to use (defaults to state_schema)

        Returns:
            StateSchemaManager instance for schema manipulation
        """
        from haive.core.schema.schema_manager import StateSchemaManager

        if schema_instance is None:
            # Use state schema by default
            schema_instance = self.derive_schema()

        return StateSchemaManager(schema_instance)

    def _generate_cache_key(self) -> str:
        """Generate a deterministic cache key for schema caching.

        Returns:
            A string key based on component identifiers
        """
        # Base key on name
        key_parts = [self.name]

        # Add engine identifier
        if self.engine:
            engine_id = getattr(self.engine, "id", None) or getattr(
                self.engine, "name", str(id(self.engine))
            )
            key_parts.append(f"engine:{engine_id}")

        # Add additional engines
        if self.engines:
            for name, engine in sorted(self.engines.items()):
                engine_id = getattr(engine, "id", None) or getattr(
                    engine, "name", str(id(engine))
                )
                key_parts.append(f"{name}:{engine_id}")

        # Add node configs
        if hasattr(self, "node_configs") and self.node_configs:
            key_parts.append(f"nodes:{len(self.node_configs)}")

        # Add patterns
        if hasattr(self, "patterns") and self.patterns:
            key_parts.append(f"patterns:{len(self.patterns)}")

        return ":".join(key_parts)

    def derive_schema(self) -> type[BaseModel]:
        """Derive state schema from components and engines using SchemaComposer.

        Returns:
            A state schema class (with no __runnable_config__ field)
        """
        # Testing mode check - bypass caching entirely if in testing mode
        if getattr(self, "_testing_mode", False):
            # Generate schema directly without caching for testing
            return self._generate_schema_without_caching()

        # Return cached instance if available
        if self._state_schema_instance:
            return self._state_schema_instance

        # Generate cache key
        cache_key = self._generate_cache_key()

        # Check class-level cache
        if cache_key in self.__class__._schema_cache:
            self._state_schema_instance = self.__class__._schema_cache[cache_key]
            return self._state_schema_instance

        # Create new schema
        schema = self._generate_schema_without_caching()

        # Cache the result
        self._state_schema_instance = schema
        self.__class__._schema_cache[cache_key] = schema

        return schema

    def _generate_schema_without_caching(self) -> type[BaseModel]:
        """Generate schema directly without caching.

        This is used internally by derive_schema and in testing contexts.

        Returns:
            Generated state schema
        """
        # Get all components including engines
        all_components = []
        if self.engine:
            all_components.append(self.engine)
        all_components.extend(self.engines.values())

        # Add components from node configs
        for node_config in getattr(self, "node_configs", {}).values():
            if (
                isinstance(node_config.engine, Engine)
                and node_config.engine not in all_components
            ):
                all_components.append(node_config.engine)

        # Add components from pattern requirements
        pattern_components = self._get_pattern_schema_components()
        for component in pattern_components:
            if component not in all_components:
                all_components.append(component)

        # Create schema
        schema_name = f"{self.name.replace('-', '_').title()}State"
        schema = SchemaComposer.from_components(
            components=all_components,
            name=schema_name,
        )

        # Enhance schema with pattern-specific fields
        schema = self._enhance_schema_with_patterns(schema)

        return schema

    def _get_pattern_schema_components(self) -> list[Any]:
        """Get components required by patterns.

        Returns:
            List of components required by patterns
        """
        components = []

        # Load pattern registry if needed
        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()

            # Check each pattern for required components
            for pattern_config in self.patterns:
                if not pattern_config.enabled:
                    continue

                pattern = registry.get_pattern(pattern_config.name)
                if pattern:
                    # Extract requirements from pattern metadata
                    for req in pattern.metadata.get("required_components", []):
                        # This is a simplified approach - actual implementation would be more sophisticated
                        component_type = req.get("type")
                        if component_type == "llm" and self.engine is None:
                            from haive.core.engine.aug_llm import AugLLMConfig

                            components.append(AugLLMConfig())
                        elif component_type == "retriever" and not any(
                            getattr(c, "engine_type", None) == EngineType.RETRIEVER
                            for c in [self.engine, *list(self.engines.values())]
                        ):
                            from haive.core.engine.retriever import (
                                VectorStoreRetrieverConfig,
                            )

                            components.append(
                                VectorStoreRetrieverConfig(
                                    name="pattern_required_retriever"
                                )
                            )
        except ImportError:
            # Pattern system not available
            logger.debug("Pattern system not available for schema component extraction")
        except Exception as e:
            logger.debug(f"Error getting pattern components: {e}")

        return components

    def _enhance_schema_with_patterns(self, schema: type[BaseModel]) -> type[BaseModel]:
        """Enhance schema with pattern-specific fields and reducers.

        Args:
            schema: Base schema to enhance

        Returns:
            Enhanced schema
        """
        manager = self.get_schema_manager(schema)

        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()

            # Process each pattern
            for pattern_config in self.patterns:
                if not pattern_config.enabled:
                    continue

                pattern = registry.get_pattern(pattern_config.name)
                if pattern:
                    # Add schema customizations based on pattern type
                    pattern_type = pattern.metadata.get("pattern_type")

                    # This is where we would add pattern-specific schema enhancements
                    # For example, RAG patterns might add context fields
                    if pattern_type == "retrieval":
                        if not manager.has_field("context"):
                            manager.add_field(
                                "context", list[dict[str, Any]], default_factory=list
                            )
                    elif pattern_type == "agent":
                        if not manager.has_field("tools"):
                            manager.add_field(
                                "tools", list[dict[str, Any]], default_factory=list
                            )
        except ImportError:
            # Pattern system not available
            logger.debug("Pattern system not available for schema enhancement")

        return manager.get_model()

    def derive_input_schema(self) -> type[BaseModel]:
        """Derive input schema for this agent.

        Returns:
            Input schema as BaseModel subclass
        """
        # Return cached instance if available
        if self._input_schema_instance:
            return self._input_schema_instance

        # Use provided schema if available
        if self.input_schema is not None:
            if isinstance(self.input_schema, type) and issubclass(
                self.input_schema, BaseModel
            ):
                # Get schema manager to handle customization
                manager = self.get_schema_manager(self.input_schema)

                # Remove __runnable_config__ field if present
                if manager.has_field("__runnable_config__"):
                    manager.remove_field("__runnable_config__")

                schema = manager.get_model()
                self._input_schema_instance = schema
                return schema

            if isinstance(self.input_schema, dict):
                # Create schema from dictionary using SchemaComposer
                composer = SchemaComposer(name=f"{self.name}Input")
                composer.add_fields_from_dict(self.input_schema)

                schema = composer  # .build()
                self._input_schema_instance = schema
                return schema

        # Try to derive from generic type arguments
        for base_cls in self.__class__.__orig_bases__:
            if get_origin(base_cls) is InvokableEngine:
                args = get_args(base_cls)
                if len(args) >= 1:
                    in_type = args[0]
                    if in_type is not TIn:  # Not the generic parameter itself
                        if isinstance(in_type, type) and issubclass(in_type, BaseModel):
                            # Get schema manager to handle customization
                            manager = self.get_schema_manager(in_type)

                            # Remove __runnable_config__ field if present
                            if manager.has_field("__runnable_config__"):
                                manager.remove_field("__runnable_config__")

                            schema = manager.get_model()
                            self._input_schema_instance = schema
                            return schema

        # Default to using SchemaComposer for input schema
        all_components = []
        if self.engine:
            all_components.append(self.engine)
        all_components.extend(self.engines.values())

        schema = SchemaComposer.compose_input_schema(
            components=all_components,
            name=f"{self.name}Input",
        )

        self._input_schema_instance = schema
        return schema

    def derive_output_schema(self) -> type[BaseModel]:
        """Derive output schema for this agent.

        Returns:
            Output schema as BaseModel subclass
        """
        # Return cached instance if available
        if self._output_schema_instance:
            return self._output_schema_instance

        # Use provided schema if available
        if self.output_schema is not None:
            if isinstance(self.output_schema, type) and issubclass(
                self.output_schema, BaseModel
            ):
                # Get schema manager to handle customization
                manager = self.get_schema_manager(self.output_schema)

                # Remove __runnable_config__ field if present
                if manager.has_field("__runnable_config__"):
                    manager.remove_field("__runnable_config__")

                schema = manager.get_model()
                self._output_schema_instance = schema
                return schema

            if isinstance(self.output_schema, dict):
                # Create schema from dictionary using SchemaComposer
                composer = SchemaComposer(name=f"{self.name}Output")
                composer.add_fields_from_dict(self.output_schema)

                schema = composer  # .build()
                self._output_schema_instance = schema
                return schema

        # Try to derive from generic type arguments
        for base_cls in self.__class__.__orig_bases__:
            if get_origin(base_cls) is InvokableEngine:
                args = get_args(base_cls)
                if len(args) >= 2:
                    out_type = args[1]
                    if out_type is not TOut:  # Not the generic parameter itself
                        if isinstance(out_type, type) and issubclass(
                            out_type, BaseModel
                        ):
                            # Get schema manager to handle customization
                            manager = self.get_schema_manager(out_type)

                            # Remove __runnable_config__ field if present
                            if manager.has_field("__runnable_config__"):
                                manager.remove_field("__runnable_config__")

                            schema = manager.get_model()
                            self._output_schema_instance = schema
                            return schema

        # Default to using SchemaComposer for output schema
        all_components = []
        if self.engine:
            all_components.append(self.engine)
        all_components.extend(self.engines.values())

        schema = SchemaComposer.compose_output_schema(
            components=all_components,
            name=f"{self.name}Output",
        )

        self._output_schema_instance = schema
        return schema

    def resolve_engine(self, engine_ref=None) -> Engine:
        """Resolve an engine reference to an actual engine.

        Args:
            engine_ref: Engine reference (name or object) or None to use default engine

        Returns:
            Resolved Engine object
        """
        # Use the provided reference, default engine, or first from engines dict
        ref = engine_ref or self.engine or next(iter(self.engines.values()), None)

        if ref is None:
            raise ValueError("No engine specified and no default engine available")

        # If it's already an Engine object, return it
        if isinstance(ref, Engine):
            return ref

        # If it's a string, first check our local engines dict
        if isinstance(ref, str) and ref in self.engines:
            return self.engines[ref]

        # If not found locally, look it up in the registry
        if isinstance(ref, str):
            # Try each engine type
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            for engine_type in EngineType:
                engine = registry.get(engine_type, ref)
                if engine:
                    return engine

            raise ValueError(f"Engine '{ref}' not found in registry")

        raise TypeError(f"Unsupported engine reference type: {type(ref)}")

    def build_agent(self) -> "Agent":
        """Build an agent instance from this configuration with protocol validation."""
        # Import locally to avoid circular imports
        from haive.core.engine.agent.agent import AGENT_REGISTRY

        # Try to find agent class in registry
        agent_class = None

        # Check exact class match first
        agent_class = AGENT_REGISTRY.get(self.__class__)

        # Try class attribute if not in registry
        if agent_class is None and hasattr(self.__class__, "agent_class"):
            agent_class = self.__class__.agent_class

        # Try to resolve by naming convention
        if agent_class is None:
            agent_class = self._resolve_agent_class_by_name()

        if agent_class is None:
            raise TypeError(f"No agent class found for {self.__class__.__name__}")

        # Instantiate the agent
        agent = agent_class(config=self)

        # Validate that agent implements required protocols
        self._validate_agent_protocols(agent)

        return agent

    def _validate_agent_protocols(self, agent: Any) -> None:
        """Validate that the agent implements the expected protocols.

        Args:
            agent: Agent instance to validate

        Raises:
            TypeError: If the agent doesn't implement required protocols
        """
        # Verify that agent implements the core protocol
        if not isinstance(agent, AgentProtocol):
            raise TypeError(
                f"Agent class {agent.__class__.__name__} must implement AgentProtocol"
            )

        # Log warnings for optional protocols
        if not isinstance(agent, StreamingAgentProtocol):
            logger.warning(
                f"Agent class {agent.__class__.__name__} doesn't implement StreamingAgentProtocol"
            )

        if not isinstance(agent, PersistentAgentProtocol):
            logger.warning(
                f"Agent class {agent.__class__.__name__} doesn't implement PersistentAgentProtocol"
            )

        if not isinstance(agent, VisualizationAgentProtocol):
            logger.warning(
                f"Agent class {agent.__class__.__name__} doesn't implement VisualizationAgentProtocol"
            )

        if not isinstance(agent, ExtensibilityAgentProtocol):
            logger.warning(
                f"Agent class {agent.__class__.__name__} doesn't implement ExtensibilityAgentProtocol"
            )

    def _resolve_agent_class_by_name(self) -> type["Agent"] | None:
        """Try to resolve agent class by naming convention."""
        import importlib

        agent_class_name = self.__class__.__name__.replace("Config", "")

        # Try same module
        try:
            module = importlib.import_module(self.__class__.__module__)
            return getattr(module, agent_class_name, None)
        except (ImportError, AttributeError):
            pass

        # Try sibling module
        try:
            base_module = self.__class__.__module__.rsplit(".", 1)[0]
            for suffix in ["agent", "impl", ""]:
                try:
                    agent_module = importlib.import_module(f"{base_module}.{suffix}")
                    return getattr(agent_module, agent_class_name, None)
                except (ImportError, AttributeError):
                    continue
        except Exception:
            pass

        return None

    def create_runnable(self, runnable_config: RunnableConfig | None = None) -> Any:
        """Create a runnable instance from this agent config.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            Built and compiled agent application
        """
        # Build the agent
        agent = self.build_agent()

        # Apply runtime config if provided
        if runnable_config:
            # Create a merged config
            merged_config = RunnableConfigManager.merge(
                self.runnable_config, runnable_config
            )

            # Update agent's runnable_config
            agent.runnable_config = merged_config

        # Return the built and compiled agent app
        return agent.app

    def invoke(
        self, input_data: TIn, runnable_config: RunnableConfig | None = None
    ) -> TOut:
        """Invoke the agent with input data.

        Args:
            input_data: Input data for the agent
            runnable_config: Optional runtime configuration

        Returns:
            Output from the agent
        """
        # Build the agent
        agent = self.build_agent()

        # Extract thread ID from runnable_config if present
        thread_id = None
        if (
            runnable_config
            and "configurable" in runnable_config
            and "thread_id" in runnable_config["configurable"]
        ):
            thread_id = runnable_config["configurable"]["thread_id"]

        # Run with input data and config
        return agent.run(input_data, thread_id=thread_id, config=runnable_config)

    async def ainvoke(
        self, input_data: TIn, runnable_config: RunnableConfig | None = None
    ) -> TOut:
        """Asynchronously invoke the agent with input data.

        Args:
            input_data: Input data for the agent
            runnable_config: Optional runtime configuration

        Returns:
            Output from the agent
        """
        # Build the agent
        agent = self.build_agent()

        # Extract thread ID from runnable_config if present
        thread_id = None
        if (
            runnable_config
            and "configurable" in runnable_config
            and "thread_id" in runnable_config["configurable"]
        ):
            thread_id = runnable_config["configurable"]["thread_id"]

        # Run with input data and config
        return await agent.arun(input_data, thread_id=thread_id, config=runnable_config)

    def apply_runnable_config(
        self, runnable_config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Extract parameters from runnable_config relevant to this agent.

        Args:
            runnable_config: Runtime configuration to extract from

        Returns:
            Dictionary of relevant parameters
        """
        # Start with common parameters from base class
        params = super().apply_runnable_config(runnable_config)

        if not runnable_config or "configurable" not in runnable_config:
            return params

        configurable = runnable_config["configurable"]

        # Extract agent-specific parameters
        agent_params = ["thread_id", "user_id", "save_history", "debug"]
        for param in agent_params:
            if param in configurable:
                params[param] = configurable[param]

        # Extract engine parameters if engine configs are present
        if "engine_configs" in configurable:
            for engine_name, engine_config in configurable["engine_configs"].items():
                # Handle primary engine
                if engine_name == self.name or (
                    self.engine
                    and hasattr(self.engine, "name")
                    and engine_name == self.engine.name
                ):
                    params.update(engine_config)
                # Handle named engines
                elif engine_name in self.engines:
                    if "engines" not in params:
                        params["engines"] = {}
                    params["engines"][engine_name] = engine_config

        return params

    def get_schema_fields(self) -> dict[str, tuple[type, Any]]:
        """Get schema fields for this agent.

        Returns:
            Dictionary mapping field names to (type, default) tuples
            Never includes __runnable_config__
        """
        # Use the StateSchema/StateSchemaManager functionality to get fields
        schema = self.derive_schema()

        if hasattr(schema, "get_field_definitions"):
            # Use StateSchema's built-in method if available
            return schema.get_field_definitions(include_runnable_config=False)
        # Otherwise use the manager
        manager = self.get_schema_manager(schema)
        return manager.get_field_definitions(include_runnable_config=False)

    def extract_params(self) -> dict[str, Any]:
        """Extract parameters from this engine for serialization.

        Returns:
            Dictionary of engine parameters
        """
        params = {}

        # Get fields from the model
        fields = self.model_fields

        # Add all relevant fields
        for field_name in fields:
            # Skip fields that shouldn't be in params
            if field_name.startswith("_") or field_name in [
                "input_schema",
                "output_schema",
                "id",
                "name",
                "engine_type",
            ]:
                continue

            # Get the value if it exists
            if hasattr(self, field_name):
                value = getattr(self, field_name)
                params[field_name] = value

        return params

    def to_dict(self) -> dict[str, Any]:
        """Convert agent config to a dictionary.

        Returns:
            Dictionary representation of the agent config
        """
        # Use model_dump for Pydantic v2
        data = self.model_dump(exclude={"input_schema", "output_schema"})

        # Convert engines to serializable format
        if "engine" in data and isinstance(data["engine"], Engine):
            if hasattr(data["engine"], "to_dict"):
                data["engine"] = data["engine"].to_dict()
            elif hasattr(data["engine"], "extract_params"):
                data["engine"] = data["engine"].extract_params()
            else:
                data["engine"] = {
                    "name": data["engine"].name,
                    "type": str(data["engine"].engine_type),
                }

        if "engines" in data:
            serialized_engines = {}
            for name, engine in data["engines"].items():
                if isinstance(engine, Engine):
                    if hasattr(engine, "to_dict"):
                        serialized_engines[name] = engine.to_dict()
                    elif hasattr(engine, "extract_params"):
                        serialized_engines[name] = engine.extract_params()
                    else:
                        serialized_engines[name] = {
                            "name": engine.name,
                            "type": str(engine.engine_type),
                        }
                else:
                    serialized_engines[name] = engine
            data["engines"] = serialized_engines

        # Convert node_configs
        if "node_configs" in data:
            serialized_nodes = {}
            for name, node_config in data["node_configs"].items():
                if hasattr(node_config, "to_dict"):
                    serialized_nodes[name] = node_config.to_dict()
                else:
                    serialized_nodes[name] = {"name": name}
            data["node_configs"] = serialized_nodes

        # Convert subagents
        if "subagents" in data:
            serialized_subagents = {}
            for name, subagent in data["subagents"].items():
                if hasattr(subagent, "to_dict"):
                    serialized_subagents[name] = subagent.to_dict()
                else:
                    serialized_subagents[name] = {"name": subagent.name}
            data["subagents"] = serialized_subagents

        # Convert persistence config
        if "persistence" in data and data["persistence"] is not None:
            if hasattr(data["persistence"], "to_dict"):
                data["persistence"] = data["persistence"].to_dict()

        # Add class information for type reconstruction
        data["agent_class"] = f"{self.__class__.__module__}.{self.__class__.__name__}"

        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentConfig":
        """Create an agent config from a dictionary.

        Args:
            data: Dictionary representation of the agent config

        Returns:
            Agent config instance
        """
        # Extract class information if available
        agent_class_path = data.pop("agent_class", None)

        if agent_class_path:
            try:
                # Dynamically load the class
                module_name, class_name = agent_class_path.rsplit(".", 1)
                module = __import__(module_name, fromlist=[class_name])
                agent_cls = getattr(module, class_name)

                # Instantiate the correct class
                return agent_cls(**data)
            except (ImportError, AttributeError) as e:
                logger.warning(f"Could not load agent class '{agent_class_path}': {e}")

        # Fallback to instantiating the base class
        return cls(**data)

    def to_json(self) -> str:
        """Convert agent config to JSON string.

        Returns:
            JSON representation of the agent config
        """
        from haive.core.utils.pydantic_utils import ensure_json_serializable

        data = self.to_dict()
        serializable_data = ensure_json_serializable(data)
        return json.dumps(serializable_data)

    @classmethod
    def from_json(cls, json_str: str) -> "AgentConfig":
        """Create an agent config from a JSON string.

        Args:
            json_str: JSON representation of the agent config

        Returns:
            Agent config instance
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    @classmethod
    def clear_schema_caches(cls):
        """Clear all schema caches completely for this class and its subclasses.

        This ensures both class-level and instance-level caches are reset.
        """
        # Clear class-level caches
        cls._schema_cache.clear()
        cls._input_schema_cache.clear()
        cls._output_schema_cache.clear()

        # Ensure any existing instances also clear their instance caches
        # This is only useful if instances are shared across tests
        for subclass in cls.__subclasses__():
            subclass.clear_schema_caches()

    # =========================================
    # Pattern-based composition methods
    # =========================================

    def use_pattern(
        self,
        pattern_name: str,
        parameters: dict[str, Any] | None = None,
        order: int | None = None,
        condition: str | None = None,
        enabled: bool = True,
    ) -> "AgentConfig":
        """Add a pattern to be applied to this agent.

        Args:
            pattern_name: Name of the pattern in the registry
            parameters: Parameters for pattern application
            order: Application order (lower numbers first)
            condition: Optional condition for pattern application
            enabled: Whether this pattern is enabled

        Returns:
            Self for method chaining
        """
        # Check if pattern exists in registry
        try:
            from haive.core.graph.patterns.registry import GraphPatternRegistry

            registry = GraphPatternRegistry.get_instance()
            if not registry.get_pattern(pattern_name):
                logger.warning(f"Pattern '{pattern_name}' not found in registry")
        except ImportError:
            logger.warning("Pattern registry not available")

        # Check if we already have this pattern
        existing_pattern = None
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                existing_pattern = pattern
                break

        if existing_pattern:
            # Update existing pattern
            new_pattern = PatternConfig(
                name=pattern_name,
                parameters=parameters or {},
                order=order,
                condition=condition,
                enabled=enabled,
            )

            # Replace with merged configuration
            self.patterns.remove(existing_pattern)
            self.patterns.append(existing_pattern.merge_with(new_pattern))
        else:
            # Add new pattern
            self.patterns.append(
                PatternConfig(
                    name=pattern_name,
                    parameters=parameters or {},
                    order=order,
                    condition=condition,
                    enabled=enabled,
                )
            )

        # Invalidate schema caches
        self._invalidate_schema_caches()

        return self

    def set_testing_mode(self, enabled=True):
        """Enable or disable testing mode to bypass caching behavior.

        Args:
            enabled: Whether testing mode should be enabled

        Returns:
            Self for method chaining
        """
        self._testing_mode = enabled
        return self

    def set_pattern_parameters(self, pattern_name: str, **parameters) -> "AgentConfig":
        """Set global parameters for a pattern.

        Args:
            pattern_name: Name of the pattern
            **parameters: Parameter values

        Returns:
            Self for method chaining
        """
        if pattern_name not in self.pattern_parameters:
            self.pattern_parameters[pattern_name] = {}

        # Update parameters
        self.pattern_parameters[pattern_name].update(parameters)

        # Update any existing pattern configs
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                for key, value in parameters.items():
                    if key not in pattern.parameters:
                        pattern.parameters[key] = value

        return self

    def disable_pattern(self, pattern_name: str) -> "AgentConfig":
        """Disable a pattern.

        Args:
            pattern_name: Name of the pattern to disable

        Returns:
            Self for method chaining
        """
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                pattern.enabled = False
                break

        return self

    def enable_pattern(self, pattern_name: str) -> "AgentConfig":
        """Enable a pattern.

        Args:
            pattern_name: Name of the pattern to enable

        Returns:
            Self for method chaining
        """
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                pattern.enabled = True
                break

        return self

    def get_pattern_order(self) -> list[str]:
        """Get ordered list of patterns to apply.

        Returns:
            List of pattern names in application order
        """
        # Sort patterns by order (None values last)
        sorted_patterns = sorted(
            self.patterns, key=lambda p: (p.order is None, p.order or 999999)
        )

        # Filter enabled patterns
        return [p.name for p in sorted_patterns if p.enabled]

    def get_pattern_parameters(self, pattern_name: str) -> dict[str, Any]:
        """Get combined parameters for a pattern.

        Args:
            pattern_name: Name of the pattern

        Returns:
            Combined parameters from pattern config and global parameters
        """
        # Start with global parameters
        combined = self.pattern_parameters.get(pattern_name, {}).copy()

        # Add pattern-specific parameters (overriding globals)
        for pattern in self.patterns:
            if pattern.name == pattern_name:
                combined.update(pattern.parameters)
                break

        return combined

    def is_pattern_applied(self, pattern_name: str) -> bool:
        """Check if a pattern has been applied.

        Args:
            pattern_name: Name of the pattern to check

        Returns:
            True if the pattern has been applied
        """
        return pattern_name in self._applied_patterns

    def mark_pattern_applied(self, pattern_name: str) -> None:
        """Mark a pattern as applied.

        Args:
            pattern_name: Name of the pattern to mark
        """
        self._applied_patterns.add(pattern_name)

    def with_config_overrides(self, overrides: dict[str, Any]) -> "AgentConfig":
        """Create a new agent config with configuration overrides.

        Args:
            overrides: Configuration overrides to apply

        Returns:
            New agent config instance with overrides applied
        """
        # Create a copy of this agent config
        config = self.model_dump()

        # Apply overrides
        for key, value in overrides.items():
            if key in config:
                config[key] = value

        # Create new instance
        return self.__class__.model_validate(config)

    @classmethod
    def register_agent_class(cls, agent_class: type["Agent"]) -> None:
        """Register an agent class for this configuration.

        This method checks protocol compliance before registration.

        Args:
            agent_class: Agent class to register

        Raises:
            TypeError: If the agent class doesn't implement required protocols
        """
        # Import Agent registry
        from haive.core.engine.agent.agent import AGENT_REGISTRY

        # First instance of agent to test protocol compliance
        test_instance = None
        try:
            # Create a mock config for testing
            test_config = cls(name="protocol_test_config")

            # Attempt to create an instance for testing protocols
            # This might fail if the agent class has special __init__ requirements
            try:
                test_instance = agent_class(config=test_config)
            except Exception as e:
                logger.warning(
                    f"Could not create test instance of {agent_class.__name__}: {e}"
                )

            # If we have an instance, verify it implements required protocols
            if test_instance and not isinstance(test_instance, AgentProtocol):
                raise TypeError(
                    f"Agent class {agent_class.__name__} must implement AgentProtocol"
                )
        except Exception as e:
            logger.warning(f"Protocol validation failed: {e}")
            # Even if validation fails, we still register the class but with a warning

        # Register with the agent registry
        AGENT_REGISTRY[cls] = agent_class

        # Add a reference to the config class for symmetry
        agent_class.config_class = cls

        logger.info(
            f"Registered agent class {agent_class.__name__} for config {cls.__name__}"
        )
