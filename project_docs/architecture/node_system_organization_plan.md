# Node System Organization Plan

**Version**: 1.0
**Date**: 2025-01-21
**Status**: Implementation Plan

## 🎯 **Current Problem**

The node system has multiple overlapping implementations that are confusing:

- Multiple EngineNode versions
- Confusing agent node configurations
- Field mapping scattered across different files
- No clear inheritance hierarchy
- Backward compatibility concerns

## 🏗️ **Proposed Organization**

### New Node Hierarchy (haive-core)

```
packages/haive-core/src/haive/core/graph/node/
├── __init__.py                     # Clean public API
├── base/                           # Base implementations
│   ├── __init__.py
│   ├── base_node.py               # Abstract base node
│   ├── base_config.py             # Base configuration (existing)
│   └── types.py                   # Node types and enums
├── engine/                         # Engine-based nodes
│   ├── __init__.py
│   ├── engine_node.py             # Main EngineNode (cleaned up)
│   ├── engine_config.py           # EngineNodeConfig (refactored)
│   └── field_mapping.py           # Field mapping utilities
├── agent/                          # Agent-based nodes
│   ├── __init__.py
│   ├── agent_node_v3.py           # Current AgentNode (kept)
│   ├── agent_config.py            # AgentNodeConfig (new)
│   └── compatibility.py           # Backward compatibility
├── specialized/                    # Specialized node types
│   ├── __init__.py
│   ├── function_node.py           # Function-based nodes
│   ├── workflow_node.py           # Custom workflow nodes
│   └── conditional_node.py        # Conditional routing nodes
└── utils/                          # Node utilities
    ├── __init__.py
    ├── mapping_utils.py           # Field mapping helpers
    ├── validation_utils.py        # Node validation
    └── factory.py                 # Node factories
```

### Agent Integration (haive-agents)

```
packages/haive-agents/src/haive/agents/
├── base/
│   ├── agent.py                   # Base Agent (cleaned up)
│   └── node_integration.py       # Node system integration
├── enhanced/                      # Enhanced multi-agent system
│   ├── __init__.py
│   ├── enhanced_base.py           # MultiAgentBase (organized)
│   ├── field_coordination.py     # Multi-agent field mapping
│   └── examples/                  # Usage examples
├── simple/
│   ├── agent.py                   # SimpleAgent (simplified)
│   └── node_config.py            # Simple node configuration
└── multi/
    ├── enhanced_multi_agent_v3.py # Current implementation (kept)
    └── field_mapping_examples.py  # Field mapping examples
```

## 📋 **Implementation Plan**

### Phase 1: Core Node System Cleanup ✅ **Start Here**

#### Step 1.1: Create Base Node Infrastructure

```python
# packages/haive-core/src/haive/core/graph/node/base/base_node.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class BaseNode(ABC):
    """Abstract base for all node types."""

    @abstractmethod
    def execute(self, state: Any, config: Any = None) -> Any:
        """Execute the node with given state."""
        pass

    @abstractmethod
    def validate_config(self) -> bool:
        """Validate node configuration."""
        pass

class BaseNodeConfig(BaseModel):
    """Base configuration for all nodes."""
    name: str = Field(..., description="Node name")
    node_type: str = Field(..., description="Type of node")
    description: Optional[str] = Field(None, description="Node description")

    # Field mapping (universal across all nodes)
    input_fields: Optional[Dict[str, str] | List[str]] = Field(None)
    output_fields: Optional[Dict[str, str] | List[str]] = Field(None)
```

#### Step 1.2: Refactor EngineNode

```python
# packages/haive-core/src/haive/core/graph/node/engine/engine_config.py
from ..base.base_config import BaseNodeConfig
from haive.core.engine.base import Engine

class EngineNodeConfig(BaseNodeConfig):
    """Clean EngineNode configuration with field mapping."""

    node_type: str = Field(default="engine", description="Engine node type")
    engine: Optional[Engine] = Field(None, description="Engine instance")
    engine_name: Optional[str] = Field(None, description="Engine name for lookup")

    # Field mapping (inherited from base)
    # input_fields: Dict[str, str] | List[str] | None
    # output_fields: Dict[str, str] | List[str] | None

    # Engine-specific options
    retry_policy: Optional[Any] = Field(None)
    timeout: Optional[float] = Field(None)

    class Config:
        arbitrary_types_allowed = True
```

#### Step 1.3: Create Clean Public API

```python
# packages/haive-core/src/haive/core/graph/node/__init__.py
"""Clean node system API with backward compatibility."""

# New clean API
from .base.base_node import BaseNode, BaseNodeConfig
from .engine.engine_config import EngineNodeConfig
from .agent.agent_config import AgentNodeConfig
from .utils.factory import create_node, create_engine_node, create_agent_node

# Field mapping utilities
from .utils.mapping_utils import FieldMapper, create_field_mapping

# Backward compatibility (deprecated but working)
from .engine_node import EngineNodeConfig as LegacyEngineNodeConfig
from .agent_node import AgentNodeConfig as LegacyAgentNodeConfig

__all__ = [
    # New API
    "BaseNode", "BaseNodeConfig",
    "EngineNodeConfig", "AgentNodeConfig",
    "create_node", "create_engine_node", "create_agent_node",
    "FieldMapper", "create_field_mapping",

    # Legacy (deprecated)
    "LegacyEngineNodeConfig", "LegacyAgentNodeConfig"
]
```

### Phase 2: Agent System Integration

#### Step 2.1: Simplify Base Agent

```python
# packages/haive-agents/src/haive/agents/base/agent.py (cleaned up)
from haive.core.graph.node import EngineNodeConfig, create_engine_node

class Agent(BaseModel):
    """Clean base agent with integrated node system."""

    name: str = Field(...)
    engine: Engine = Field(...)

    # Node configuration for field mapping
    input_mapping: Optional[Dict[str, str]] = Field(None)
    output_mapping: Optional[Dict[str, str]] = Field(None)

    def create_node(self, name: str = None) -> EngineNodeConfig:
        """Create node configuration with field mapping."""
        return create_engine_node(
            name=name or self.name,
            engine=self.engine,
            input_fields=self.input_mapping,
            output_fields=self.output_mapping
        )

    def with_field_mapping(self, input_map=None, output_map=None):
        """Create copy with field mapping."""
        return self.model_copy(update={
            "input_mapping": input_map,
            "output_mapping": output_map
        })
```

#### Step 2.2: Enhanced Multi-Agent with Field Coordination

```python
# packages/haive-agents/src/haive/agents/enhanced/field_coordination.py
from typing import Dict, List, Tuple
from haive.core.graph.node.utils.mapping_utils import FieldMapper

class MultiAgentFieldCoordinator:
    """Coordinate field mapping between multiple agents."""

    def __init__(self, field_transfers: Dict[Tuple[str, str], Dict[str, str]] = None):
        self.field_transfers = field_transfers or {}
        self.field_mapper = FieldMapper()

    def setup_agent_mappings(self, agents: Dict[str, Agent]) -> Dict[str, EngineNodeConfig]:
        """Setup field mappings for multi-agent coordination."""
        node_configs = {}

        for agent_name, agent in agents.items():
            # Find input mappings from previous agents
            input_mapping = self._get_input_mapping(agent_name)

            # Find output mappings to next agents
            output_mapping = self._get_output_mapping(agent_name)

            # Create node with mappings
            node_configs[agent_name] = agent.create_node().model_copy(update={
                "input_fields": input_mapping,
                "output_fields": output_mapping
            })

        return node_configs
```

### Phase 3: Backward Compatibility Layer

#### Step 3.1: Compatibility Imports

```python
# packages/haive-core/src/haive/core/graph/node/compatibility.py
"""Backward compatibility for existing code."""

import warnings
from .engine.engine_config import EngineNodeConfig as NewEngineNodeConfig

class EngineNodeConfig(NewEngineNodeConfig):
    """Backward compatible EngineNodeConfig."""

    def __init__(self, **kwargs):
        warnings.warn(
            "Direct EngineNodeConfig import is deprecated. "
            "Use 'from haive.core.graph.node import EngineNodeConfig'",
            DeprecationWarning,
            stacklevel=2
        )
        super().__init__(**kwargs)

# Keep old import paths working
from .agent_node_v3 import AgentNodeV3 as AgentNodeConfig
```

### Phase 4: Migration Utilities

#### Step 4.1: Migration Tools

```python
# packages/haive-core/src/haive/core/graph/node/utils/migration.py
"""Tools to migrate from old node system to new."""

def migrate_engine_node(old_config: dict) -> EngineNodeConfig:
    """Migrate old engine node config to new format."""
    return EngineNodeConfig(
        name=old_config.get("name", "unnamed"),
        engine=old_config.get("engine"),
        input_fields=old_config.get("input_fields"),
        output_fields=old_config.get("output_fields")
    )

def migrate_agent_config(old_agent: Any) -> Agent:
    """Migrate old agent to new format."""
    return Agent(
        name=getattr(old_agent, "name", "agent"),
        engine=getattr(old_agent, "engine", None)
    )
```

## 🔄 **Migration Strategy**

### For Existing Code

1. **Keep working**: All existing imports continue to work
2. **Add warnings**: Deprecated imports show warnings
3. **Provide migration path**: Tools to upgrade gradually
4. **Document changes**: Clear migration guide

### Migration Timeline

- **Week 1**: Implement Phase 1 (core cleanup)
- **Week 2**: Implement Phase 2 (agent integration)
- **Week 3**: Implement Phase 3 (compatibility)
- **Week 4**: Testing and documentation
- **Month 2**: Gradual migration of existing code
- **Month 3**: Deprecation warnings
- **Month 6**: Remove deprecated code

## 🎯 **Benefits After Organization**

### For Developers

- **Clear API**: Single import path for all node types
- **Better IntelliSense**: Proper type hints and documentation
- **Easy field mapping**: Simple API for common use cases
- **Consistent patterns**: All nodes follow same patterns

### For Framework

- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new node types
- **Performance**: Optimized node execution
- **Testing**: Better test coverage and validation

### Example Usage After Organization

```python
# New clean API
from haive.core.graph.node import create_engine_node, create_field_mapping
from haive.agents.simple import SimpleAgent

# Create agent with field mapping
agent = SimpleAgent(name="processor", engine=config)
agent_with_mapping = agent.with_field_mapping(
    output_map={"result": "potato"}
)

# Create node directly
node = create_engine_node(
    name="processor",
    engine=config,
    output_fields={"result": "potato"}
)

# Use in multi-agent with coordination
from haive.agents.enhanced import EnhancedMultiAgent, MultiAgentFieldCoordinator

coordinator = MultiAgentFieldCoordinator(
    field_transfers={
        ("agent1", "agent2"): {"findings": "context"}
    }
)

workflow = EnhancedMultiAgent(
    agents=[agent1, agent2],
    field_coordinator=coordinator
)
```

## 🚀 **Next Steps**

1. **Start with Phase 1**: Clean up core node system
2. **Create migration guide**: Document upgrade path
3. **Test compatibility**: Ensure existing code still works
4. **Gradual rollout**: Migrate components one at a time
5. **Community feedback**: Get input on new API design

This organization will make the node system much clearer while maintaining full backward compatibility!
