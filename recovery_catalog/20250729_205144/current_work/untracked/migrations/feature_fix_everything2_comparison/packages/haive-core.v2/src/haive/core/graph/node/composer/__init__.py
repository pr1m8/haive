"""Node Schema Composer - Flexible I/O configuration for graph nodes."""

from haive.core.graph.node.composer.extract_functions import (
    ExtractFunctions,
    extract_conditional,
    extract_functions,
    extract_messages_content,
    extract_multi_field,
    extract_simple_field,
    extract_typed,
    extract_with_path,
    extract_with_projection,
)
from haive.core.graph.node.composer.field_mapping import FieldMapping
from haive.core.graph.node.composer.node_schema_composer import (
    ComposedCallableNode,
    ComposedNode,
    NodeSchemaComposer,
    SchemaAdapter,
    change_input_key,
    change_output_key,
    remap_fields,
)
from haive.core.graph.node.composer.path_resolver import PathResolver
from haive.core.graph.node.composer.protocols import (
    ExtractFunction,
    TransformFunction,
    UpdateFunction,
)
from haive.core.graph.node.composer.update_functions import (
    UpdateFunctions,
    update_conditional,
    update_functions,
    update_hierarchical,
    update_messages_append,
    update_multi_field,
    update_simple_field,
    update_type_aware,
    update_with_path,
    update_with_transform,
)

# Import advanced features if available
try:

    _advanced_available = True
except ImportError:
    _advanced_available = False

__all__ = [
    "ComposedCallableNode",
    "ComposedNode",
    "ExtractFunction",
    # Extract functions
    "ExtractFunctions",
    # Foundation classes
    "FieldMapping",
    # Core composer
    "NodeSchemaComposer",
    "PathResolver",
    "SchemaAdapter",
    "TransformFunction",
    "UpdateFunction",
    # Update functions
    "UpdateFunctions",
    "change_input_key",
    # Quick factory functions
    "change_output_key",
    "extract_conditional",
    "extract_functions",
    "extract_messages_content",
    "extract_multi_field",
    "extract_simple_field",
    "extract_typed",
    "extract_with_path",
    "extract_with_projection",
    "remap_fields",
    "update_conditional",
    "update_functions",
    "update_hierarchical",
    "update_messages_append",
    "update_multi_field",
    "update_simple_field",
    "update_type_aware",
    "update_with_path",
    "update_with_transform",
]

# Add advanced features to __all__ if available
if _advanced_available:
    __all__.extend(
        [
            "AdvancedComposedNode",
            "AdvancedNodeComposer",
            "TypedCallableNode",
            "as_node",
            "callable_to_node",
            "node_with_custom_logic",
        ]
    )

# Import integrated features if available
try:

    _integrated_available = True
except ImportError:
    _integrated_available = False

# Add integrated features to __all__ if available
if _integrated_available:
    __all__.extend(
        [
            "IntegratedNodeComposer",
            "SchemaAwareComposedNode",
            "StateSchemaAdapter",
            "create_schema_aware_node",
            "integrate_node_with_schema",
            "with_state_schema",
        ]
    )
