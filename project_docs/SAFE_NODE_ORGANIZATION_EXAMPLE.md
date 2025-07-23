# Safe Node Organization Example

## Current Structure (Keep As-Is)

```
packages/haive-core/src/haive/core/graph/node/
├── engine_node.py                    # Keep here
├── engine_node_generic.py            # Keep here
├── agent_node_v3.py                  # Keep here
├── multi_agent_node.py               # Keep here
├── validation_node_config.py         # Keep here
└── ... (all other files stay put)
```

## Organized **init**.py (New)

```python
"""Graph Node System for haive-core.

This module provides a comprehensive node system organized into logical groups:

Engine Nodes
------------
Engine-based nodes with field mapping and intelligent I/O handling.

Agent Nodes
-----------
Agent-based nodes for multi-agent orchestration and coordination.

Validation Nodes
----------------
Validation, routing, and conditional logic nodes.

Field Mapping
-------------
Advanced field mapping and schema composition utilities.

Utilities
---------
Factories, registries, and helper functions.
"""

# ===== ENGINE NODES =====
from .engine_node import EngineNodeConfig
from .engine_node_generic import GenericEngineNode

# ===== AGENT NODES =====
from .agent_node_v3 import AgentNodeV3
from .multi_agent_node import MultiAgentNode
from .intelligent_multi_agent_node import IntelligentMultiAgentNode

# ===== VALIDATION NODES =====
from .validation_node_config import ValidationNodeConfig
from .routing_validation_node import RoutingValidationNode
from .state_updating_validation_node import StateUpdatingValidationNode
from .unified_validation_node import UnifiedValidationNode

# ===== FIELD MAPPING =====
from .composer.field_mapping import FieldMapping, FieldMappingConfig
from .composer.node_schema_composer import NodeSchemaComposer

# ===== UTILITIES =====
from .factory import NodeFactory, create_node
from .registry import NodeRegistry
from .utils import get_node_types

# ===== BASE CLASSES =====
from .base_config import NodeConfig
from .types import NodeType

# Organize exports by category for AutoAPI
__all__ = [
    # Engine Nodes
    "EngineNodeConfig",
    "GenericEngineNode",

    # Agent Nodes
    "AgentNodeV3",
    "MultiAgentNode",
    "IntelligentMultiAgentNode",

    # Validation Nodes
    "ValidationNodeConfig",
    "RoutingValidationNode",
    "StateUpdatingValidationNode",
    "UnifiedValidationNode",

    # Field Mapping
    "FieldMapping",
    "FieldMappingConfig",
    "NodeSchemaComposer",

    # Utilities
    "NodeFactory",
    "create_node",
    "NodeRegistry",
    "get_node_types",

    # Base Classes
    "NodeConfig",
    "NodeType"
]

# Add metadata for Sphinx AutoAPI grouping
__sphinx_groups__ = {
    "Engine Nodes": [
        "EngineNodeConfig",
        "GenericEngineNode"
    ],
    "Agent Nodes": [
        "AgentNodeV3",
        "MultiAgentNode",
        "IntelligentMultiAgentNode"
    ],
    "Validation Nodes": [
        "ValidationNodeConfig",
        "RoutingValidationNode",
        "StateUpdatingValidationNode",
        "UnifiedValidationNode"
    ],
    "Field Mapping": [
        "FieldMapping",
        "FieldMappingConfig",
        "NodeSchemaComposer"
    ],
    "Utilities": [
        "NodeFactory",
        "create_node",
        "NodeRegistry",
        "get_node_types"
    ]
}
```

## Benefits

- ✅ **No breaking changes** - all existing imports work
- ✅ **Better AutoAPI docs** - logical grouping
- ✅ **Cleaner public API** - organized exports
- ✅ **Easy maintenance** - files stay where they are
- ✅ **Backward compatible** - existing code unaffected

## AutoAPI Result

```
haive.core.graph.node
├── Engine Nodes
│   ├── EngineNodeConfig
│   └── GenericEngineNode
├── Agent Nodes
│   ├── AgentNodeV3
│   └── MultiAgentNode
├── Validation Nodes
│   ├── ValidationNodeConfig
│   └── RoutingValidationNode
└── Field Mapping
    ├── FieldMapping
    └── NodeSchemaComposer
```
