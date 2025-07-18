# New Modular Schema Architecture Design

## Architecture Overview

The new schema system follows a **Component-Based Architecture** with clear separation of concerns, standardized interfaces, and composable modules. This design eliminates the monolithic StateSchema while maintaining full backwards compatibility.

## Core Design Principles

### 1. Single Responsibility Principle

Each component handles exactly one concern:

- **FieldManager**: Field definition, validation, and sharing
- **EngineManager**: Engine access and coordination
- **ToolManager**: Tool discovery and execution
- **SerializationManager**: JSON/dict conversion
- **VisualizationManager**: Pretty printing and UI

### 2. Interface Segregation

Clear, focused interfaces prevent coupling:

- **EngineProvider**: Engine access contract
- **ToolProvider**: Tool access contract
- **FieldRegistry**: Field management contract
- **SchemaMetadata**: Unified metadata interface

### 3. Dependency Inversion

High-level modules depend on abstractions, not concretions:

- Components use interfaces, not concrete implementations
- Easy to swap implementations for testing/customization
- Clear boundaries between layers

### 4. Composition Over Inheritance

Build schemas by composing components rather than complex inheritance:

- Flexible schema construction
- Avoid diamond problem and fragile base classes
- Easy to test individual components

## New Architecture Structure

```
schema_test/
├── core/
│   ├── interfaces/          # Abstract contracts
│   ├── components/          # Single-responsibility components
│   ├── schemas/            # Clean schema implementations
│   └── managers/           # High-level coordination
├── adapters/               # Legacy compatibility
├── compatibility/          # Lightweight type conversion
└── migration/             # Migration utilities
```

## Interface Definitions

### 1. Engine Provider Interface

```python
# core/interfaces/engine_provider.py
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List

class EngineProvider(ABC):
    """Contract for engine access and management."""

    @abstractmethod
    def get_engine(self, name: str) -> Optional[Any]:
        """Get engine by name."""
        pass

    @abstractmethod
    def get_primary_engine(self) -> Optional[Any]:
        """Get the primary/default engine."""
        pass

    @abstractmethod
    def list_engines(self) -> Dict[str, Any]:
        """Get all available engines."""
        pass

    @abstractmethod
    def add_engine(self, name: str, engine: Any) -> None:
        """Add an engine to the provider."""
        pass

    @abstractmethod
    def remove_engine(self, name: str) -> bool:
        """Remove an engine from the provider."""
        pass

class EngineAccessor(ABC):
    """Interface for objects that can access engines."""

    @abstractmethod
    def get_engine_provider(self) -> EngineProvider:
        """Get the engine provider for this object."""
        pass
```

### 2. Tool Provider Interface

```python
# core/interfaces/tool_provider.py
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

class Tool(ABC):
    """Standard tool interface."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool identifier."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM context."""
        pass

    @abstractmethod
    async def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool asynchronously."""
        pass

class ToolProvider(ABC):
    """Contract for tool access and management."""

    @abstractmethod
    def get_tools(self) -> List[Tool]:
        """Get all available tools."""
        pass

    @abstractmethod
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name."""
        pass

    @abstractmethod
    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the provider."""
        pass

    @abstractmethod
    def remove_tool(self, name: str) -> bool:
        """Remove a tool from the provider."""
        pass

    @abstractmethod
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get tool schemas for LLM integration."""
        pass
```

### 3. Field Registry Interface

```python
# core/interfaces/field_registry.py
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum

class FieldType(Enum):
    """Standard field types."""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    LIST = "list"
    DICT = "dict"
    OBJECT = "object"

@dataclass
class FieldDefinition:
    """Clean field definition with minimal metadata."""
    name: str
    type: FieldType
    default: Any = None
    required: bool = True
    description: Optional[str] = None
    validator: Optional[Callable] = None
    shared: bool = False

class FieldRegistry(ABC):
    """Contract for field management."""

    @abstractmethod
    def register_field(self, field_def: FieldDefinition) -> None:
        """Register a field definition."""
        pass

    @abstractmethod
    def get_field(self, name: str) -> Optional[FieldDefinition]:
        """Get field definition by name."""
        pass

    @abstractmethod
    def list_fields(self) -> List[FieldDefinition]:
        """Get all registered fields."""
        pass

    @abstractmethod
    def share_field(self, name: str) -> None:
        """Mark a field as shared across agents."""
        pass

    @abstractmethod
    def is_shared(self, name: str) -> bool:
        """Check if a field is shared."""
        pass

    @abstractmethod
    def add_reducer(self, field_name: str, reducer: Callable) -> None:
        """Add a reducer function for a field."""
        pass
```

### 4. Schema Metadata Interface

```python
# core/interfaces/schema_metadata.py
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class SchemaMetadata(ABC):
    """Unified metadata management interface."""

    @abstractmethod
    def get_metadata(self, key: str) -> Any:
        """Get metadata value by key."""
        pass

    @abstractmethod
    def set_metadata(self, key: str, value: Any) -> None:
        """Set metadata value."""
        pass

    @abstractmethod
    def get_all_metadata(self) -> Dict[str, Any]:
        """Get all metadata."""
        pass

    @abstractmethod
    def clear_metadata(self) -> None:
        """Clear all metadata."""
        pass
```

## Component Implementations

### 1. Field Manager Component

```python
# core/components/field_manager.py
from typing import Dict, List, Optional, Callable, Any
from ..interfaces.field_registry import FieldRegistry, FieldDefinition, FieldType

class FieldManager(FieldRegistry):
    """Manages field definitions, validation, and sharing."""

    def __init__(self):
        self._fields: Dict[str, FieldDefinition] = {}
        self._reducers: Dict[str, Callable] = {}
        self._shared_fields: set = set()

    def register_field(self, field_def: FieldDefinition) -> None:
        """Register a field definition."""
        self._fields[field_def.name] = field_def
        if field_def.shared:
            self._shared_fields.add(field_def.name)

    def get_field(self, name: str) -> Optional[FieldDefinition]:
        """Get field definition by name."""
        return self._fields.get(name)

    def list_fields(self) -> List[FieldDefinition]:
        """Get all registered fields."""
        return list(self._fields.values())

    def share_field(self, name: str) -> None:
        """Mark a field as shared across agents."""
        if name in self._fields:
            self._fields[name].shared = True
            self._shared_fields.add(name)

    def is_shared(self, name: str) -> bool:
        """Check if a field is shared."""
        return name in self._shared_fields

    def add_reducer(self, field_name: str, reducer: Callable) -> None:
        """Add a reducer function for a field."""
        if field_name not in self._fields:
            raise ValueError(f"Field '{field_name}' not registered")
        self._reducers[field_name] = reducer

    def get_reducer(self, field_name: str) -> Optional[Callable]:
        """Get reducer for a field."""
        return self._reducers.get(field_name)

    def validate_field_value(self, name: str, value: Any) -> bool:
        """Validate a field value against its definition."""
        field_def = self.get_field(name)
        if not field_def:
            return False

        # Type validation
        if not self._validate_type(value, field_def.type):
            return False

        # Custom validator
        if field_def.validator and not field_def.validator(value):
            return False

        return True

    def _validate_type(self, value: Any, field_type: FieldType) -> bool:
        """Validate value against field type."""
        type_map = {
            FieldType.STRING: str,
            FieldType.INTEGER: int,
            FieldType.FLOAT: (int, float),
            FieldType.BOOLEAN: bool,
            FieldType.LIST: list,
            FieldType.DICT: dict,
        }

        expected_type = type_map.get(field_type)
        if expected_type:
            return isinstance(value, expected_type)

        return True  # OBJECT type allows anything
```

### 2. Engine Manager Component

```python
# core/components/engine_manager.py
from typing import Dict, Any, Optional, List
from ..interfaces.engine_provider import EngineProvider

class EngineManager(EngineProvider):
    """Manages engine access and coordination."""

    def __init__(self):
        self._engines: Dict[str, Any] = {}
        self._primary_engine: Optional[str] = None

    def get_engine(self, name: str) -> Optional[Any]:
        """Get engine by name."""
        return self._engines.get(name)

    def get_primary_engine(self) -> Optional[Any]:
        """Get the primary/default engine."""
        if self._primary_engine:
            return self._engines.get(self._primary_engine)

        # Return first engine if no primary set
        if self._engines:
            return next(iter(self._engines.values()))

        return None

    def list_engines(self) -> Dict[str, Any]:
        """Get all available engines."""
        return self._engines.copy()

    def add_engine(self, name: str, engine: Any) -> None:
        """Add an engine to the provider."""
        self._engines[name] = engine

        # Set as primary if first engine
        if not self._primary_engine:
            self._primary_engine = name

    def remove_engine(self, name: str) -> bool:
        """Remove an engine from the provider."""
        if name in self._engines:
            del self._engines[name]

            # Update primary if removed
            if self._primary_engine == name:
                self._primary_engine = next(iter(self._engines.keys()), None)

            return True
        return False

    def set_primary_engine(self, name: str) -> None:
        """Set the primary engine."""
        if name in self._engines:
            self._primary_engine = name
        else:
            raise ValueError(f"Engine '{name}' not found")

    def get_engine_for_node_config(self, node_config: Any) -> Optional[Any]:
        """Get engine for node config using standardized logic."""
        # Priority 1: Direct engine reference
        if hasattr(node_config, 'engine') and node_config.engine:
            return node_config.engine

        # Priority 2: Engine by name
        if hasattr(node_config, 'engine_name') and node_config.engine_name:
            return self.get_engine(node_config.engine_name)

        # Priority 3: Primary engine
        return self.get_primary_engine()
```

### 3. Tool Manager Component

```python
# core/components/tool_manager.py
from typing import List, Optional, Dict, Any
from ..interfaces.tool_provider import ToolProvider, Tool

class ToolManager(ToolProvider):
    """Manages tool discovery and execution."""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def get_tools(self) -> List[Tool]:
        """Get all available tools."""
        return list(self._tools.values())

    def get_tool(self, name: str) -> Optional[Tool]:
        """Get tool by name."""
        return self._tools.get(name)

    def add_tool(self, tool: Tool) -> None:
        """Add a tool to the provider."""
        self._tools[tool.name] = tool

    def remove_tool(self, name: str) -> bool:
        """Remove a tool from the provider."""
        if name in self._tools:
            del self._tools[name]
            return True
        return False

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get tool schemas for LLM integration."""
        schemas = []
        for tool in self._tools.values():
            schema = {
                "name": tool.name,
                "description": tool.description,
            }

            # Add additional schema info if available
            if hasattr(tool, 'input_schema'):
                schema["input_schema"] = tool.input_schema
            if hasattr(tool, 'output_schema'):
                schema["output_schema"] = tool.output_schema

            schemas.append(schema)

        return schemas

    def get_tools_from_engine(self, engine: Any) -> List[Tool]:
        """Extract tools from engine using standardized interface."""
        tools = []

        # Standard tool interfaces
        if hasattr(engine, 'get_tools') and callable(engine.get_tools):
            engine_tools = engine.get_tools()
            for tool in engine_tools:
                if self._is_tool_compatible(tool):
                    tools.append(self._wrap_tool_if_needed(tool))

        # Legacy tool attributes (for compatibility)
        legacy_attrs = ['tools', 'pydantic_tools', 'schemas']
        for attr in legacy_attrs:
            if hasattr(engine, attr):
                attr_tools = getattr(engine, attr, [])
                if attr_tools:
                    for tool in attr_tools:
                        wrapped_tool = self._wrap_tool_if_needed(tool)
                        if wrapped_tool:
                            tools.append(wrapped_tool)

        return tools

    def _is_tool_compatible(self, tool: Any) -> bool:
        """Check if tool implements our interface."""
        return hasattr(tool, 'name') and hasattr(tool, 'arun')

    def _wrap_tool_if_needed(self, tool: Any) -> Optional[Tool]:
        """Wrap legacy tools to match our interface."""
        if isinstance(tool, Tool):
            return tool

        # Wrap LangChain tools
        if hasattr(tool, 'name') and hasattr(tool, 'run'):
            return LangChainToolWrapper(tool)

        return None

class LangChainToolWrapper(Tool):
    """Adapter for LangChain tools."""

    def __init__(self, langchain_tool):
        self._tool = langchain_tool

    @property
    def name(self) -> str:
        return self._tool.name

    @property
    def description(self) -> str:
        return getattr(self._tool, 'description', f"Tool: {self.name}")

    async def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the LangChain tool."""
        try:
            if hasattr(self._tool, 'arun'):
                result = await self._tool.arun(input_data)
            else:
                result = self._tool.run(input_data)

            return {"result": result, "status": "success"}
        except Exception as e:
            return {"error": str(e), "status": "error"}
```

### 4. Clean Schema Implementation

```python
# core/schemas/base_schema.py
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from ..interfaces.engine_provider import EngineProvider, EngineAccessor
from ..interfaces.tool_provider import ToolProvider
from ..interfaces.field_registry import FieldRegistry
from ..interfaces.schema_metadata import SchemaMetadata
from ..components.field_manager import FieldManager
from ..components.engine_manager import EngineManager
from ..components.tool_manager import ToolManager

class BaseSchema(BaseModel, EngineAccessor):
    """Clean, minimal base schema with component composition."""

    # Core data fields
    messages: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data):
        super().__init__(**data)

        # Initialize component managers
        self._field_manager = FieldManager()
        self._engine_manager = EngineManager()
        self._tool_manager = ToolManager()

        # Register default fields
        self._register_default_fields()

    def get_engine_provider(self) -> EngineProvider:
        """Get the engine provider for this schema."""
        return self._engine_manager

    def get_tool_provider(self) -> ToolProvider:
        """Get the tool provider for this schema."""
        return self._tool_manager

    def get_field_registry(self) -> FieldRegistry:
        """Get the field registry for this schema."""
        return self._field_manager

    def _register_default_fields(self) -> None:
        """Register default fields with the field manager."""
        from ..interfaces.field_registry import FieldDefinition, FieldType

        self._field_manager.register_field(
            FieldDefinition(
                name="messages",
                type=FieldType.LIST,
                default=[],
                description="Conversation messages"
            )
        )

        self._field_manager.register_field(
            FieldDefinition(
                name="metadata",
                type=FieldType.DICT,
                default={},
                description="Additional metadata"
            )
        )

class MessageSchema(BaseSchema):
    """Schema specialized for message handling."""

    def add_message(self, message: str) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def get_last_message(self) -> Optional[str]:
        """Get the most recent message."""
        return self.messages[-1] if self.messages else None

    def clear_messages(self) -> None:
        """Clear all messages."""
        self.messages.clear()

class ToolEnabledSchema(BaseSchema):
    """Schema with tool capabilities."""

    def __init__(self, **data):
        super().__init__(**data)

        # Register tool-related fields
        self._register_tool_fields()

    def _register_tool_fields(self) -> None:
        """Register tool-specific fields."""
        from ..interfaces.field_registry import FieldDefinition, FieldType

        self._field_manager.register_field(
            FieldDefinition(
                name="tool_results",
                type=FieldType.LIST,
                default=[],
                description="Results from tool executions"
            )
        )

    def add_tool_result(self, tool_name: str, result: Any) -> None:
        """Add a tool execution result."""
        if not hasattr(self, 'tool_results'):
            self.tool_results = []

        self.tool_results.append({
            "tool": tool_name,
            "result": result,
            "timestamp": self._get_timestamp()
        })

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.utcnow().isoformat()
```

## Benefits of New Architecture

### 1. **Clear Separation of Concerns**

- Each component has a single, well-defined responsibility
- Easy to understand, test, and modify individual components
- No more monolithic classes with mixed responsibilities

### 2. **Standardized Interfaces**

- Predictable engine and tool access patterns
- No more complex fallback logic in node configs
- Easy to swap implementations for testing

### 3. **Composition Over Inheritance**

- Build schemas by composing needed components
- Avoid complex inheritance hierarchies
- Flexible and extensible design

### 4. **Performance Optimized**

- Lazy initialization of expensive operations
- No complex model validators running on every creation
- Memory-efficient component design

### 5. **Testing Friendly**

- Components can be tested in isolation
- Clear interfaces make mocking straightforward
- No hidden dependencies or side effects

### 6. **Backwards Compatible**

- Adapter layer provides exact API compatibility
- Gradual migration path for existing code
- Feature flag system for safe transitions

This new architecture solves all the major issues identified in the current system while providing a clean, maintainable foundation for future development.
