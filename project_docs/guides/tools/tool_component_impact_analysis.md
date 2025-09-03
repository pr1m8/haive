# Tool Component Impact Analysis & Migration Plan

**Date**: 2025-08-08  
**Purpose**: Comprehensive mapping of all tool-related components for unified typing  
**Status**: Complete component analysis with migration strategy  

## 🚨 Critical Finding: Tool Types Are Everywhere!

We have **multiple, inconsistent tool type definitions** across the codebase:
- Some use `list[Any]`
- Some use `list[BaseTool]`  
- Some use complex Union types with 6+ variants
- Some use `Sequence` vs `list`

## 📊 Complete Tool Component Inventory

### 1. Core Tool Infrastructure

#### Tool Management Mixins (Must Update)
```python
# ToolRouteMixin - PRIMARY INTEGRATION POINT
- Location: haive/core/common/mixins/tool_route_mixin.py
- Current: Handles tool routing, metadata, sanitization
- Update: Make aware of ToolEngine types
- Impact: Everything inherits from this

# ToolListMixin - SECONDARY INTEGRATION POINT  
- Location: haive/core/common/mixins/tool_list_mixin.py
- Current: Uses complex Union type for tools
- Update: Use ToolEngine's unified ToolType
- Impact: Used by many agents

# DynamicToolRouteMixin
- Location: haive/core/common/mixins/dynamic_tool_route_mixin.py
- Current: Extends ToolRouteMixin with callbacks
- Update: Inherit updated typing from parent
```

#### Tool State Schemas (Critical Updates)
```python
# ToolState - MAIN TOOL STATE
- Location: haive/core/schema/prebuilt/tool_state.py
- Inherits: ToolRouteMixin + MessagesStateWithTokenUsage
- Update: Will get typing from ToolRouteMixin

# ToolStateWithValidation
- Location: haive/core/schema/prebuilt/tool_state_with_validation.py
- Update: Inherit from updated ToolState

# ValidationAwareToolState  
- Location: haive/core/schema/prebuilt/validation_aware_tool_state.py
- Update: Inherit unified typing
```

### 2. Tool Nodes (Validation & Execution)

#### Validation Nodes - COMPLEX TOOL ROUTING
```python
# ValidationNodeConfigV2 - CRITICAL UPDATE
- Location: haive/core/graph/node/validation_node_config_v2.py
- Current Logic:
  if route == "pydantic_model":
      tool_msg = self._create_tool_message_for_pydantic()
  elif route in ["langchain_tool", "function", "tool_node"]:
      # Different handling
- Update: Use ToolEngine's capability-based routing

# ValidationNodeV2
- Inherits: NodeConfig + ToolRouteMixin
- Update: Will get unified typing through mixin
```

#### Tool Execution Nodes
```python
# ToolNodeConfigV2 and subclasses
- LangChainToolNode
- FunctionToolNode  
- PydanticToolNode
- Update: Use ToolEngine analyzer for type detection
```

### 3. Engine Integration

#### AugLLMConfig - MAJOR INTEGRATION
```python
# Current fields:
tools: Sequence[Union[Type[BaseTool], Type[BaseModel], Callable, StructuredTool, BaseModel]]
schemas: dict[str, type[BaseModel]]
pydantic_tools: dict[str, type[BaseModel]]

# Update: Use ToolEngine's unified type
tools: ToolSequence  # From ToolEngine
```

### 4. Utility Components

#### ToolList Class
```python
# Location: haive/core/utils/tool_list.py
# Current: Complex type handling
# Update: Use ToolEngine's analyzer
```

#### tool_utils Functions
```python
# Location: haive/agents/tool_utils.py
# Functions: prepare_tools(), tools_router(), create_tool_executor()
# Update: Use ToolEngine types and capabilities
```

## 🎯 Unified Typing Integration Plan

### Phase 1: Define Core Types in ToolEngine

```python
# haive/core/engine/tool/types.py
from typing import Union, Callable, TypeAlias, Protocol
from langchain_core.tools import BaseTool, StructuredTool
from pydantic import BaseModel

# Unified tool type
ToolType: TypeAlias = Union[
    BaseTool,                    # LangChain tool instances
    StructuredTool,              # Structured tool instances  
    type[BaseTool],              # Tool classes
    type[BaseModel],             # Pydantic models as tools
    Callable[..., Any],          # Functions as tools
]

# Tool capabilities from ToolEngine
class ToolCapabilities(str, Enum):
    INTERRUPTIBLE = "interruptible"
    STATE_READER = "state_reader"
    STATE_WRITER = "state_writer"
    STRUCTURED_OUTPUT = "structured_output"
    VALIDATABLE = "validatable"
    ASYNC_CAPABLE = "async_capable"
    RETRIEVER = "retriever"

# Tool properties for analysis
class ToolProperties(BaseModel):
    tool_type: str
    capabilities: set[ToolCapabilities]
    metadata: dict[str, Any]
```

### Phase 2: Update Core Mixins

```python
# ToolRouteMixin - Make ToolEngine-aware
class ToolRouteMixin:
    def _analyze_tool(self, tool: Any, name: str | None = None) -> dict[str, Any]:
        # Import from ToolEngine
        from haive.core.engine.tool.analyzer import ToolAnalyzer
        from haive.core.engine.tool.types import ToolProperties
        
        # Use ToolEngine analyzer
        properties = ToolAnalyzer().analyze(tool)
        
        # Update metadata with ToolEngine properties
        metadata = {
            "tool_properties": properties,
            "capabilities": list(properties.capabilities),
            # Convenience accessors
            "is_interruptible": ToolCapabilities.INTERRUPTIBLE in properties.capabilities,
            "is_validatable": ToolCapabilities.VALIDATABLE in properties.capabilities,
        }
        
        return metadata
```

### Phase 3: Update Validation Nodes

```python
# ValidationNodeConfigV2 - Use capability-based routing
def _determine_tool_route(self, tool_name: str) -> str:
    """Determine tool route using ToolEngine capabilities."""
    metadata = self.tool_metadata.get(tool_name, {})
    properties = metadata.get("tool_properties")
    
    if properties:
        # Route based on capabilities
        if ToolCapabilities.VALIDATABLE in properties.capabilities:
            return "pydantic_model"
        elif ToolCapabilities.STRUCTURED_OUTPUT in properties.capabilities:
            return "structured_tool"
        else:
            return "langchain_tool"
    
    # Fallback to current logic
    return self._legacy_route_detection(tool_name)
```

### Phase 4: Update State Schemas

```python
# ToolState - No direct changes needed
# Will inherit unified typing from ToolRouteMixin
# But add capability helpers:

class ToolState(ToolRouteMixin, MessagesStateWithTokenUsage):
    def get_interruptible_tools(self) -> list[str]:
        """Get all interruptible tool names."""
        return [
            name for name, meta in self.tool_metadata.items()
            if meta.get("is_interruptible", False)
        ]
    
    def get_tools_by_capability(self, capability: ToolCapabilities) -> list[str]:
        """Get tools with specific capability."""
        # Inherited from updated ToolRouteMixin
```

### Phase 5: Update ToolList Utility

```python
# ToolList - Use ToolEngine for type checking
class ToolList(UserList[ToolType]):  # Use ToolEngine's ToolType
    def _determine_tool_type(self, tool: Any) -> str:
        """Use ToolEngine analyzer."""
        from haive.core.engine.tool.analyzer import ToolAnalyzer
        properties = ToolAnalyzer().analyze(tool)
        return properties.tool_type
```

## 📋 Migration Checklist

### High Priority (Core Infrastructure)
- [ ] Create ToolEngine types module
- [ ] Create ToolAnalyzer in ToolEngine
- [ ] Update ToolRouteMixin to use ToolEngine
- [ ] Update ToolListMixin typing
- [ ] Update ToolList utility class
- [ ] Fix AugLLMConfig tool typing

### Medium Priority (Node Updates)
- [ ] Update ValidationNodeConfigV2 routing
- [ ] Update ToolNodeConfigV2 subclasses
- [ ] Update tool execution nodes
- [ ] Update router nodes

### Low Priority (Agent Updates)
- [ ] Update agent patterns
- [ ] Update tool utilities
- [ ] Update examples
- [ ] Update tests

## 🔄 Backward Compatibility Strategy

1. **Keep Legacy Methods**: Don't remove old routing logic immediately
2. **Add Deprecation Warnings**: Warn when using old patterns
3. **Dual Support Period**: Support both old and new for 2 releases
4. **Migration Helpers**: Provide tools to update old code

```python
# Example compatibility layer
def _analyze_tool(self, tool: Any, name: str | None = None) -> dict[str, Any]:
    # Try new ToolEngine analysis
    try:
        from haive.core.engine.tool.analyzer import ToolAnalyzer
        properties = ToolAnalyzer().analyze(tool)
        # Return new format
    except ImportError:
        # Fallback to legacy analysis
        warnings.warn("Using legacy tool analysis. Update to ToolEngine.", DeprecationWarning)
        return self._legacy_analyze_tool(tool, name)
```

## 🎯 End Goal

After migration:
1. **Single source of truth**: ToolEngine defines all tool types
2. **Consistent typing**: Same ToolType everywhere
3. **Capability-based routing**: Use capabilities not type checks
4. **Better tool discovery**: Find tools by capability
5. **Extensible system**: Easy to add new tool types

This creates a unified, ToolEngine-aware system across all components!