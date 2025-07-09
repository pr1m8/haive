"""Haive Schema System - Dynamic State Management for AI Agents.

This package provides a powerful foundation for dynamic state management in AI agents
and workflows. It extends Pydantic's model system with features specifically designed
for graph-based AI workflows, including field sharing between graphs, reducer functions
for state updates, and engine I/O tracking.

The schema system enables fully dynamic and serializable state schemas that can be
composed, modified, and extended at runtime, making it ideal for complex agent
architectures and nested workflows.

Architecture:
    The schema system is built around a core StateSchema that extends Pydantic BaseModel
    with additional capabilities for AI agent workflows:

    - Field sharing between parent and child graphs
    - Reducer functions for intelligent state merging
    - Engine I/O tracking for workflow coordination
    - Structured output model integration
    - Rich visualization and debugging tools

Core Components:
    StateSchema: Base class that extends Pydantic models with sharing, reducers,
        and I/O tracking. Serves as the foundation for all agent state management.
    SchemaComposer: Utility for building schemas from components dynamically.
        Supports field extraction from engines, models, and dictionaries.
    StateSchemaManager: Tool for manipulating schemas at runtime.
        Provides methods for schema modification and transformation.
    MultiAgentStateSchema: Enhanced schema for multi-agent architectures.
        Handles complex state coordination across multiple agents.
    AgentSchemaComposer: Schema composer specialized for agent architectures.
        Includes build modes and agent-specific optimizations.
    FieldDefinition: Representation of field type, default, and metadata.
        Provides comprehensive field information for schema building.
    FieldExtractor: Utility for extracting fields from various sources.
        Supports engines, models, tools, and custom components.
    Field Utilities: Common functions for field manipulation.
        Includes type inference, reducer resolution, and field creation.

Prebuilt Schemas:
    BasicAgentState: Simple state with common agent fields
    MessagesState: State optimized for conversation handling
    ToolState: State with built-in tool management
    TokenUsage: Token tracking and cost calculation utilities

Usage Patterns:
    Basic Usage::

        from haive.core.schema import StateSchema, Field
        from typing import List, Dict, Any

        class MyAgentState(StateSchema):
            messages: List[str] = Field(default_factory=list)
            context: Dict[str, Any] = Field(default_factory=dict)

            __shared_fields__ = ["messages"]
            __reducer_fields__ = {
                "messages": lambda a, b: a + b
            }

    Dynamic Schema Building::

        from haive.core.schema import SchemaComposer

        composer = SchemaComposer(name="DynamicState")
        composer.add_field("query", str, default="")
        composer.add_field("results", List[str], default_factory=list)

        DynamicState = composer.build()
        state = DynamicState()

    Multi-Agent Coordination::

        from haive.core.schema import MultiAgentStateSchema

        class CoordinatedState(MultiAgentStateSchema):
            shared_memory: Dict[str, Any] = Field(default_factory=dict)
            agent_states: Dict[str, Dict] = Field(default_factory=dict)

            __shared_fields__ = ["shared_memory"]

Examples:
    For detailed usage examples, see the documentation and examples directory.
    Key example files:
    - examples/basic_schema_usage.py
    - examples/dynamic_schema_building.py
    - examples/multi_agent_coordination.py
    - examples/engine_integration.py

Version: 2.0.0
Author: Haive Team
License: MIT
"""

# Version information
__version__ = "2.0.0"
__author__ = "Haive Team"
__license__ = "MIT"

# Type imports for better IDE support
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
)

if TYPE_CHECKING:
    from pydantic import BaseModel
    from typing_extensions import TypeAlias

# Core schema imports
# Schema composition imports
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode

# Field management imports
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_extractor import FieldExtractor
from haive.core.schema.field_utils import (
    create_annotated_field,
    create_field,
    extract_type_metadata,
    get_common_reducers,
    infer_field_type,
    resolve_reducer,
)
from haive.core.schema.multi_agent_state_schema import (
    MultiAgentSchemaComposer,
)
from haive.core.schema.multi_agent_state_schema import MultiAgentStateSchema
from haive.core.schema.multi_agent_state_schema import (
    MultiAgentStateSchema as PrebuiltMultiAgentStateSchema,
)

# Prebuilt state schemas
from haive.core.schema.prebuilt.basic_agent_state import BasicAgentState

# Token usage and messages utilities
from haive.core.schema.prebuilt.messages import (
    MessagesStateWithTokenUsage,
    TokenUsage,
    TokenUsageMixin,
    aggregate_token_usage,
    calculate_token_cost,
    extract_token_usage_from_message,
)
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.tool_state import ToolState

# Reducer utilities
from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer
from haive.core.schema.schema_manager import StateSchemaManager
from haive.core.schema.state_schema import StateSchema
from haive.core.schema.ui import SchemaUI

# Schema composer with fallback handling
try:
    from haive.core.schema.composer.schema_composer import SchemaComposer
except ImportError:
    # Fallback to original location for backward compatibility
    from haive.core.schema.schema_composer import (
        SchemaComposer,  # type: ignore[attr-defined]
    )

# Type aliases for better API clarity
SchemaType: "TypeAlias" = Type[StateSchema]
FieldType: "TypeAlias" = Type[Any]
ReducerType: "TypeAlias" = Callable[[Any, Any], Any]
ValidatorType: "TypeAlias" = Callable[[Any], Any]

# Define public API
__all__ = [
    # Version information
    "__version__",
    "__author__",
    "__license__",
    # Core classes
    "StateSchema",
    "StateSchemaManager",
    "SchemaUI",
    # Schema composition
    "SchemaComposer",
    "AgentSchemaComposer",
    "BuildMode",
    "MultiAgentStateSchema",
    "MultiAgentSchemaComposer",
    "PrebuiltMultiAgentStateSchema",
    # Field management
    "FieldDefinition",
    "FieldExtractor",
    "create_field",
    "create_annotated_field",
    "extract_type_metadata",
    "infer_field_type",
    "get_common_reducers",
    "resolve_reducer",
    # Prebuilt schemas
    "BasicAgentState",
    "MessagesState",
    "ToolState",
    # Token usage utilities
    "TokenUsage",
    "TokenUsageMixin",
    "MessagesStateWithTokenUsage",
    "extract_token_usage_from_message",
    "aggregate_token_usage",
    "calculate_token_cost",
    # Reducer utilities
    "preserve_messages_reducer",
    # Type aliases
    "SchemaType",
    "FieldType",
    "ReducerType",
    "ValidatorType",
    # Convenience functions
    "create_simple_state",
    "create_agent_state",
    "validate_schema",
    "get_schema_info",
]


# Module initialization
def _initialize_schema_module() -> None:
    """Initialize the schema module with default configurations."""
    import logging

    # Set up logging for schema operations
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Validate critical imports
    try:
        from typing import get_type_hints

        from pydantic import BaseModel, Field
    except ImportError as e:
        raise ImportError(
            f"Critical schema dependencies missing: {e.name}. "
            f"Please install with: pip install haive-core[schema]"
        )


# Convenience factory functions
def create_simple_state(
    fields: Dict[str, Any],
    name: str = "SimpleState",
    shared_fields: Optional[List[str]] = None,
    reducers: Optional[Dict[str, ReducerType]] = None,
) -> SchemaType:
    """Create a simple state schema with basic configuration.

    Args:
        fields: Dictionary mapping field names to types or (type, default) tuples
        name: Name for the generated schema class
        shared_fields: List of fields to share with parent graphs
        reducers: Dictionary mapping field names to reducer functions

    Returns:
        StateSchema subclass with specified configuration

    Examples:
        Basic state::

            MyState = create_simple_state({
                "messages": (List[str], []),
                "query": str,
                "response": (str, "")
            })

        With sharing and reducers::

            ConversationState = create_simple_state(
                fields={"messages": (List[BaseMessage], [])},
                shared_fields=["messages"],
                reducers={"messages": preserve_messages_reducer}
            )
    """
    composer = SchemaComposer(name=name)

    # Add fields
    for field_name, field_spec in fields.items():
        if isinstance(field_spec, tuple):
            field_type, default = field_spec
            composer.add_field(
                name=field_name,
                field_type=field_type,
                default=default,
                shared=shared_fields and field_name in shared_fields,
            )
        else:
            composer.add_field(
                name=field_name,
                field_type=field_spec,
                shared=shared_fields and field_name in shared_fields,
            )

    # Add reducers
    if reducers:
        for field_name, reducer in reducers.items():
            composer.add_reducer(field_name, reducer)

    return composer.build()


def create_agent_state(
    agent_name: str,
    engines: Optional[List[Any]] = None,
    tools: Optional[List[Any]] = None,
    include_messages: bool = True,
    include_tools: bool = True,
    custom_fields: Optional[Dict[str, Any]] = None,
) -> SchemaType:
    """Create an agent state schema with common patterns.

    Args:
        agent_name: Name for the agent and schema
        engines: List of engines to extract fields from
        tools: List of tools to include
        include_messages: Whether to include message handling
        include_tools: Whether to include tool state
        custom_fields: Additional custom fields to add

    Returns:
        StateSchema subclass optimized for agent use

    Examples:
        Basic agent state::

            MyAgentState = create_agent_state(
                agent_name="MyAgent",
                engines=[llm_engine, retriever]
            )

        Customized agent state::

            SpecializedState = create_agent_state(
                agent_name="SpecializedAgent",
                custom_fields={
                    "special_data": (Dict[str, Any], {}),
                    "processing_stage": (str, "init")
                }
            )
    """
    composer = AgentSchemaComposer(name=f"{agent_name}State")

    # Add engines
    if engines:
        for engine in engines:
            composer.add_engine(engine)

    # Add tools
    if tools:
        for tool in tools:
            composer.add_tool(tool)

    # Configure base schema
    if include_messages and include_tools:
        composer.set_base_schema(ToolState)
    elif include_messages:
        composer.set_base_schema(MessagesState)
    elif include_tools:
        composer.set_base_schema(ToolState)
    else:
        composer.set_base_schema(BasicAgentState)

    # Add custom fields
    if custom_fields:
        for field_name, field_spec in custom_fields.items():
            if isinstance(field_spec, tuple):
                field_type, default = field_spec
                composer.add_field(
                    name=field_name, field_type=field_type, default=default
                )
            else:
                composer.add_field(name=field_name, field_type=field_spec)

    return composer.build()


def validate_schema(schema: SchemaType) -> bool:
    """Validate a schema for common issues.

    Args:
        schema: StateSchema class to validate

    Returns:
        True if schema is valid, False otherwise

    Raises:
        ValueError: If schema has critical issues
    """
    import logging

    logger = logging.getLogger(__name__)

    # Check basic inheritance
    if not issubclass(schema, StateSchema):
        raise ValueError(f"Schema {schema.__name__} must inherit from StateSchema")

    # Check for field conflicts
    field_names = set(schema.model_fields.keys())
    reserved_names = {"model_fields", "model_config", "model_validate"}
    conflicts = field_names & reserved_names
    if conflicts:
        logger.warning(
            f"Schema {schema.__name__} has conflicting field names: {conflicts}"
        )

    # Check shared fields exist
    shared_fields = getattr(schema, "__shared_fields__", [])
    missing_shared = set(shared_fields) - field_names
    if missing_shared:
        logger.warning(
            f"Schema {schema.__name__} has missing shared fields: {missing_shared}"
        )

    # Check reducer fields exist
    reducer_fields = getattr(schema, "__reducer_fields__", {})
    missing_reducer = set(reducer_fields.keys()) - field_names
    if missing_reducer:
        logger.warning(
            f"Schema {schema.__name__} has missing reducer fields: {missing_reducer}"
        )

    return True


def get_schema_info(schema: SchemaType) -> Dict[str, Any]:
    """Get comprehensive information about a schema.

    Args:
        schema: StateSchema class to analyze

    Returns:
        Dictionary with schema information
    """
    info = {
        "name": schema.__name__,
        "base_classes": [cls.__name__ for cls in schema.__bases__],
        "fields": {},
        "shared_fields": getattr(schema, "__shared_fields__", []),
        "reducers": getattr(schema, "__serializable_reducers__", {}),
        "engine_io": getattr(schema, "__engine_io_mappings__", {}),
        "structured_models": getattr(schema, "__structured_models__", {}),
    }

    # Analyze fields
    for field_name, field_info in schema.model_fields.items():
        info["fields"][field_name] = {
            "type": str(field_info.annotation),
            "required": field_info.is_required(),
            "default": field_info.default if field_info.default is not ... else None,
            "description": field_info.description,
        }

    return info


def __dir__() -> List[str]:
    """Override dir() to show only public API."""
    return __all__


# Initialize module
_initialize_schema_module()

# Add convenience imports to global namespace
create_simple_state.__module__ = __name__
create_agent_state.__module__ = __name__
validate_schema.__module__ = __name__
get_schema_info.__module__ = __name__
