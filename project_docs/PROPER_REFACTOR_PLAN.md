# Proper Node System Refactor Plan

## 🎯 **Goal**: Better organization for Sphinx AutoAPI without breaking existing code

## 📊 **Current Import Analysis**

Based on the codebase analysis, these are the **actual imports being used**:

### **Most Common Imports**

```python
from haive.core.graph.node import create_node                    # ✅ Works
from haive.core.graph.node.config import NodeConfig            # ✅ Direct import
from haive.core.graph.node.factory import NodeFactory          # ✅ Direct import
from haive.core.graph.node.engine_node import EngineNodeConfig # ✅ Direct import
from haive.core.graph.node.tool_node_config import ToolNodeConfig # ✅ Direct import
```

### **Key Finding**:

- ✅ **Main imports work** (from `__init__.py`)
- ✅ **Direct imports work** (from specific files)
- ✅ **No one is using submodule imports** (because they don't exist yet)

## 🚀 **Safe Refactor Strategy**

### **Phase 1: Revert Submodule Directories (Safe)**

Remove the submodule dirs we created and go back to flat structure:

```bash
# Remove what we created
rm -rf packages/haive-core/src/haive/core/graph/node/{base,engine,agent,validation,utils}

# Keep all files in original location:
packages/haive-core/src/haive/core/graph/node/
├── __init__.py                    # ← Organize this file
├── engine_node.py                 # ← Keep here
├── agent_node_v3.py               # ← Keep here
├── validation_node_config.py      # ← Keep here
├── composer/                      # ← Already well organized
└── ... (all other files stay)
```

### **Phase 2: Create Organized **init**.py**

```python
"""Graph Node System - Organized for Better Documentation.

This module provides nodes for building LangGraph workflows, organized into
logical groups for better discoverability and documentation.

Engine Nodes
============
Nodes that execute engines with field mapping and I/O handling.

.. autosummary::
   :toctree: generated/

   EngineNodeConfig
   GenericEngineNode

Agent Nodes
===========
Nodes for agent execution and multi-agent coordination.

.. autosummary::
   :toctree: generated/

   AgentNodeV3
   MultiAgentNode
   IntelligentMultiAgentNode

Validation Nodes
================
Nodes for validation, routing, and conditional logic.

.. autosummary::
   :toctree: generated/

   ValidationNodeConfig
   RoutingValidationNode
   StateUpdatingValidationNode
   UnifiedValidationNode

Field Mapping & Composition
===========================
Advanced field mapping and schema composition utilities.

.. autosummary::
   :toctree: generated/

   FieldMapping
   FieldMappingConfig
   NodeSchemaComposer

Utilities & Factories
=====================
Factory functions and utilities for creating nodes.

.. autosummary::
   :toctree: generated/

   NodeFactory
   create_node
   create_engine_node
   NodeRegistry
"""

# ===== ENGINE NODES =====
from .engine_node import EngineNodeConfig
try:
    from .engine_node_generic import GenericEngineNode
except ImportError:
    pass

# ===== AGENT NODES =====
from .agent_node_v3 import AgentNodeV3Config as AgentNodeV3
try:
    from .multi_agent_node import MultiAgentNode
except ImportError:
    pass
try:
    from .intelligent_multi_agent_node import IntelligentMultiAgentNode
except ImportError:
    pass

# ===== VALIDATION NODES =====
try:
    from .validation_node_config import ValidationNodeConfig
except ImportError:
    pass
try:
    from .routing_validation_node import RoutingValidationNode
except ImportError:
    pass
try:
    from .state_updating_validation_node import StateUpdatingValidationNode
except ImportError:
    pass
try:
    from .unified_validation_node import UnifiedValidationNode
except ImportError:
    pass

# ===== FIELD MAPPING & COMPOSITION =====
try:
    from .composer.field_mapping import FieldMapping, FieldMappingConfig
except ImportError:
    pass
try:
    from .composer.node_schema_composer import NodeSchemaComposer
except ImportError:
    pass

# ===== UTILITIES & FACTORIES =====
from .factory import NodeFactory
from .config import NodeConfig
from .types import NodeType
from .registry import NodeRegistry

# Keep all existing factory functions working
from .utils import create_send_node, extract_io_mapping_from_schema

# ===== ORGANIZED EXPORTS =====
__all__ = [
    # Engine Nodes
    "EngineNodeConfig",

    # Agent Nodes
    "AgentNodeV3",

    # Validation Nodes
    "ValidationNodeConfig",
    "RoutingValidationNode",
    "StateUpdatingValidationNode",
    "UnifiedValidationNode",

    # Field Mapping
    "FieldMapping",
    "FieldMappingConfig",
    "NodeSchemaComposer",

    # Base & Utilities
    "NodeConfig",
    "NodeType",
    "NodeFactory",
    "NodeRegistry",

    # Factory Functions (keep existing API)
    "create_node",
    "create_engine_node",
    "create_validation_node",
    "create_tool_node",
    "create_branch_node",
    "create_send_node"
]

# Add conditionally available items
try:
    GenericEngineNode
    __all__.append("GenericEngineNode")
except NameError:
    pass

try:
    MultiAgentNode
    __all__.append("MultiAgentNode")
except NameError:
    pass

# Keep existing factory functions (preserve API compatibility)
def create_node(engine_or_callable, name=None, **kwargs):
    """Create a node - existing implementation preserved."""
    node_config = NodeConfig(
        name=name or getattr(engine_or_callable, "name", None) or "unnamed_node",
        engine=engine_or_callable,
        **kwargs
    )
    return NodeFactory.create_node_function(node_config)

def create_engine_node(engine, name=None, **kwargs):
    """Create an engine node - existing implementation preserved."""
    return create_node(engine, name=name, node_type=NodeType.ENGINE, **kwargs)

# ... (keep other create_* functions as they were)
```

### **Phase 3: Test Compatibility**

```bash
# Test that all existing imports still work
poetry run python -c "from haive.core.graph.node import create_node; print('✅ Works')"
poetry run python -c "from haive.core.graph.node.config import NodeConfig; print('✅ Works')"
poetry run python -c "from haive.core.graph.node.engine_node import EngineNodeConfig; print('✅ Works')"
```

### **Phase 4: Sphinx Configuration**

```python
# docs/source/conf.py additions
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members',
]

# Configure AutoAPI to group by the docstring sections
autoapi_python_class_content = 'both'  # Show both class and __init__ docstrings
autoapi_member_order = 'groupwise'     # Group by the sections we defined
```

## ✅ **Benefits of This Approach**

1. **Zero Breaking Changes**: All existing imports continue to work
2. **Better Documentation**: Sphinx AutoAPI shows organized groups
3. **Cleaner Public API**: Related items grouped together
4. **Easy Maintenance**: Files stay where developers expect them
5. **Gradual Migration**: Can add new patterns without disrupting old ones

## 🔄 **Migration Timeline**

- **Week 1**: Implement organized `__init__.py`
- **Week 2**: Test all existing imports work
- **Week 3**: Generate docs and verify AutoAPI output
- **Week 4**: Document the new organization patterns
- **Future**: Gradually deprecate confusing file names (optional)

## 📋 **Implementation Steps**

1. **Revert submodule directories** we created
2. **Create organized `__init__.py`** with sphinx sections
3. **Test all imports** work as before
4. **Generate documentation** and verify AutoAPI grouping
5. **Create usage examples** showing the organized imports

This approach gives us **all the benefits** (better docs, cleaner API) with **none of the risks** (breaking changes, import confusion).
