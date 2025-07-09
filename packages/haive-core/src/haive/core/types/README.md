# Haive Core: Types Module

## Overview

The Types module provides specialized type definitions and utilities that enhance Python's type system for use within the Haive framework. It includes dynamic enumerations, serializable callables, advanced registries, and other type-related utilities that enable more flexible, extensible, and type-safe code throughout the framework.

## Key Features

- **Dynamic Enumerations**: Runtime-extensible enum types for flexible validation
- **Serializable Callables**: Type-safe serialization and deserialization of function references
- **Advanced Registries**: Enhanced registries for component management
- **Type Literals**: Dynamic type literals for improved type hinting
- **Domain-Specific Types**: Pre-defined types for common domains like programming languages and file types

## Installation

This module is part of the `haive-core` package. Install the full package with:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Quick Start

```python
from haive.core.types.dynamic_enum import DynamicEnum
from haive.core.types.serializable_callable import SerializableCallable

# Define a dynamic enum with initial values
class ModelProvider(DynamicEnum):
    START_VALUES = ["openai", "anthropic", "google"]

# Use the enum
provider = "openai"
assert provider in ModelProvider._values

# Register new values at runtime
ModelProvider.register("cohere", "mistral")
assert "mistral" in ModelProvider._values

# Serialize a callable
def process_data(data: dict) -> dict:
    return {"processed": data}

# Check if serializable
is_serializable = SerializableCallable.is_serializable(process_data)

# Serialize to string
if is_serializable:
    func_path = SerializableCallable.serialize(process_data)
    print(func_path)  # "module.process_data"

    # Deserialize back to callable
    restored_func = SerializableCallable.deserialize(func_path)
    result = restored_func({"input": "value"})
```

## Components

### Dynamic Enum

A runtime-extensible enum type for flexible validation with Pydantic.

```python
from haive.core.types.dynamic_enum import DynamicEnum
from pydantic import BaseModel, Field

# Define a dynamic enum for document types
class DocumentType(DynamicEnum):
    START_VALUES = ["pdf", "docx", "txt", "html"]

# Register additional values at runtime
DocumentType.register("markdown", "csv")

# Use in a Pydantic model
class Document(BaseModel):
    name: str
    doc_type: DocumentType
    content: str

# Valid document types are validated
doc1 = Document(name="example.pdf", doc_type="pdf", content="...")
doc2 = Document(name="data.csv", doc_type="csv", content="...")

# Invalid types raise validation errors
try:
    Document(name="invalid.xyz", doc_type="xyz", content="...")
except ValueError as e:
    print(f"Validation error: {e}")
```

### Serializable Callable

A protocol for callables that can be serialized to and from importable strings.

```python
from haive.core.types.serializable_callable import SerializableCallable
from typing import Dict, Any

# Define a function
def transform_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"transformed": data}

# Serialize the function
if SerializableCallable.is_serializable(transform_data):
    func_path = SerializableCallable.serialize(transform_data)
    print(f"Serialized to: {func_path}")

    # Store the path in configuration, database, etc.

    # Later, deserialize back to callable
    restored_func = SerializableCallable.deserialize(func_path)
    result = restored_func({"input": "value"})
    print(result)  # {"transformed": {"input": "value"}}
```

### Advanced Registry

An enhanced registry system for managing components with validation and lookup capabilities.

```python
from haive.core.types.advanced_registry import AdvancedRegistry
from typing import Dict, Type, TypeVar, Generic

T = TypeVar('T')

# Create a registry for a specific component type
class ToolRegistry(AdvancedRegistry, Generic[T]):
    """Registry for tool components."""

    @classmethod
    def validate_component(cls, component: Type[T]) -> bool:
        # Validate that the component meets requirements
        return hasattr(component, "name") and hasattr(component, "run")

# Register components
@ToolRegistry.register
class SearchTool:
    name = "search"

    def run(self, query: str) -> str:
        return f"Search results for: {query}"

# Get registered components
tools = ToolRegistry.get_all()
search_tool = ToolRegistry.get("search")
```

### Tree Leaf

A utility for working with tree-like data structures.

```python
from haive.core.types.tree_leaf import TreeLeaf
from typing import Dict, List, Optional

# Create a tree structure
root = TreeLeaf(name="root")
child1 = TreeLeaf(name="child1", parent=root)
child2 = TreeLeaf(name="child2", parent=root)
grandchild = TreeLeaf(name="grandchild", parent=child1)

# Navigate the tree
assert child1.parent == root
assert grandchild.parent == child1
assert root.children == [child1, child2]
assert child1.children == [grandchild]

# Find paths
path = grandchild.get_path()
print(path)  # ["root", "child1", "grandchild"]

# Find by path
found = root.find_by_path(["child1", "grandchild"])
assert found == grandchild
```

## Usage Patterns

### Dynamic Type Validation

```python
from haive.core.types.dynamic_enum import DynamicEnum
from pydantic import BaseModel, Field

# Define a dynamic enum for API endpoints
class APIEndpoint(DynamicEnum):
    START_VALUES = ["users", "products", "orders"]

# Create a configuration model
class APIConfig(BaseModel):
    base_url: str
    endpoint: APIEndpoint
    version: str = "v1"

# Register new endpoints from configuration
def load_additional_endpoints(config_file: str):
    # Load from config file
    additional_endpoints = ["invoices", "payments", "shipping"]
    APIEndpoint.register(*additional_endpoints)

# Use in validation
config = APIConfig(base_url="https://api.example.com", endpoint="invoices")
```

### Serializable Function Registry

```python
from haive.core.types.serializable_callable import SerializableCallable
from haive.core.types.advanced_registry import AdvancedRegistry
from typing import Callable, Dict, Any

# Create a registry for serializable functions
class FunctionRegistry(AdvancedRegistry):
    _functions: Dict[str, str] = {}  # Store serialized paths

    @classmethod
    def register_function(cls, name: str, func: Callable):
        if not SerializableCallable.is_serializable(func):
            raise ValueError(f"Function {func.__name__} is not serializable")

        cls._functions[name] = SerializableCallable.serialize(func)

    @classmethod
    def get_function(cls, name: str) -> Callable:
        if name not in cls._functions:
            raise KeyError(f"Function {name} not found in registry")

        return SerializableCallable.deserialize(cls._functions[name])

    @classmethod
    def list_functions(cls) -> Dict[str, str]:
        return cls._functions.copy()

# Register functions
def process_data(data: Dict[str, Any]) -> Dict[str, Any]:
    return {"processed": True, **data}

FunctionRegistry.register_function("process", process_data)

# Use registered functions
func = FunctionRegistry.get_function("process")
result = func({"input": "value"})
```

## Configuration

The types module is generally used without specific configuration, but some components can be configured when used:

```python
from haive.core.types.dynamic_enum import DynamicEnum
from haive.core.types.advanced_registry import AdvancedRegistry

# Configure a dynamic enum with validation
class RestrictedEnum(DynamicEnum):
    START_VALUES = ["allowed1", "allowed2"]

    @classmethod
    def validate_value(cls, value: str) -> bool:
        """Only allow values with a specific pattern."""
        return value.startswith("allowed")

    @classmethod
    def register(cls, *vals: str) -> None:
        # Filter values through validation
        valid_values = [v for v in vals if cls.validate_value(v)]
        super().register(*valid_values)

# Configure an advanced registry with custom lookup
class ComponentRegistry(AdvancedRegistry):
    @classmethod
    def lookup_by_capability(cls, capability: str):
        """Find components with a specific capability."""
        return [
            component for name, component in cls._registry.items()
            if hasattr(component, "capabilities") and capability in component.capabilities
        ]
```

## Integration with Other Modules

### Integration with Graph Module

```python
from haive.core.types.serializable_callable import SerializableCallable
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

# Define node functions
def process_node(state):
    return {"processed": True, **state}

def generate_node(state):
    return {"generated": True, **state}

# Create a graph
graph = BaseGraph(name="workflow")

# Add nodes with serializable functions
graph.add_node("process", process_node)
graph.add_node("generate", generate_node)

# Connect nodes
graph.add_edge(START, "process")
graph.add_edge("process", "generate")
graph.add_edge("generate", END)

# Serialize the graph (with node functions)
serialized_graph = {
    "name": graph.name,
    "nodes": {
        name: SerializableCallable.serialize(func)
        for name, func in graph.nodes.items()
        if SerializableCallable.is_serializable(func)
    },
    "edges": graph.edges
}

# Deserialize the graph
deserialized_graph = BaseGraph(name=serialized_graph["name"])
for name, func_path in serialized_graph["nodes"].items():
    func = SerializableCallable.deserialize(func_path)
    deserialized_graph.add_node(name, func)

for source, target in serialized_graph["edges"]:
    deserialized_graph.add_edge(source, target)
```

### Integration with Engine Module

```python
from haive.core.types.dynamic_enum import DynamicEnum
from haive.core.engine.base import BaseEngine
from pydantic import BaseModel, Field

# Define model provider enum
class ModelProvider(DynamicEnum):
    START_VALUES = ["openai", "anthropic", "google"]

# Define engine configuration
class LLMEngineConfig(BaseModel):
    provider: ModelProvider
    model_name: str
    temperature: float = 0.7
    max_tokens: int = 1000

# Create engine with dynamic enum configuration
class LLMEngine(BaseEngine):
    config_schema = LLMEngineConfig

    def __init__(self, config: LLMEngineConfig):
        super().__init__(config)

        # Initialize provider-specific client
        self.provider = config.provider
        self.model_name = config.model_name

    def _run(self, input_data):
        # Implementation using the configured provider
        pass

# Register new providers at runtime
ModelProvider.register("cohere", "mistral")

# Create engine with newly registered provider
engine = LLMEngine(config=LLMEngineConfig(
    provider="mistral",
    model_name="mistral-medium"
))
```

## Best Practices

- **Use Dynamic Enums for Extensible Options**: Prefer DynamicEnum over standard Enum when values may need to be extended at runtime
- **Validate Serializable Callables**: Always check if a callable is serializable before attempting to serialize it
- **Keep Tree Structures Simple**: Avoid circular references in tree structures
- **Registry Validation**: Implement validation in registries to ensure components meet requirements
- **Document Type Constraints**: Clearly document constraints and requirements for specialized types
- **Prefer Composition**: Use these types as building blocks in combination rather than creating complex inheritance hierarchies

## Advanced Usage

### Custom Dynamic Enum Validation

```python
from haive.core.types.dynamic_enum import DynamicEnum
from typing import Set, ClassVar
import re

# Create a dynamic enum with custom validation
class ModelName(DynamicEnum):
    START_VALUES = ["gpt-4", "claude-3-opus", "gemini-pro"]
    PROVIDER_PATTERNS: ClassVar[Set[str]] = {
        r"^gpt-\d",        # OpenAI models
        r"^claude-\d",      # Anthropic models
        r"^gemini-",        # Google models
        r"^mistral-"        # Mistral models
    }

    @classmethod
    def validate_value(cls, value: str) -> bool:
        """Validate that a model name matches known patterns."""
        return any(re.match(pattern, value) for pattern in cls.PROVIDER_PATTERNS)

    @classmethod
    def register(cls, *vals: str) -> None:
        """Only register values that pass validation."""
        valid_values = [v for v in vals if cls.validate_value(v)]
        invalid_values = set(vals) - set(valid_values)

        if invalid_values:
            print(f"Warning: Skipping invalid model names: {invalid_values}")

        super().register(*valid_values)

# Register new values
ModelName.register(
    "gpt-4-turbo",         # Valid - matches OpenAI pattern
    "claude-3-haiku",      # Valid - matches Anthropic pattern
    "llama-2-70b",         # Invalid - doesn't match any pattern
    "mistral-medium",      # Valid - matches Mistral pattern
)
```

### Enhanced Serializable Callable

```python
from haive.core.types.serializable_callable import SerializableCallable
import inspect
from typing import Callable, Dict, Any, Optional

# Extended serializable callable with signature information
class EnhancedSerializableCallable:
    @staticmethod
    def serialize_with_signature(func: Callable) -> Dict[str, Any]:
        """Serialize a callable with its signature information."""
        if not SerializableCallable.is_serializable(func):
            raise ValueError(f"Function {func.__name__} is not serializable")

        # Get function path
        func_path = SerializableCallable.serialize(func)

        # Get signature information
        sig = inspect.signature(func)
        params = {}

        for name, param in sig.parameters.items():
            param_info = {
                "kind": str(param.kind),
                "default": "NO_DEFAULT" if param.default is inspect.Parameter.empty else str(param.default),
            }

            # Try to get type annotation
            if param.annotation is not inspect.Parameter.empty:
                if hasattr(param.annotation, "__name__"):
                    param_info["annotation"] = param.annotation.__name__
                else:
                    param_info["annotation"] = str(param.annotation)

            params[name] = param_info

        # Get return type if available
        return_type = "unknown"
        if sig.return_annotation is not inspect.Parameter.empty:
            if hasattr(sig.return_annotation, "__name__"):
                return_type = sig.return_annotation.__name__
            else:
                return_type = str(sig.return_annotation)

        # Get docstring
        docstring = inspect.getdoc(func) or ""

        return {
            "path": func_path,
            "name": func.__name__,
            "module": func.__module__,
            "parameters": params,
            "return_type": return_type,
            "docstring": docstring
        }

    @staticmethod
    def deserialize(serialized_data: Dict[str, Any]) -> Callable:
        """Deserialize a callable from its serialized data."""
        return SerializableCallable.deserialize(serialized_data["path"])
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/types).

## Related Modules

- **haive.core.common**: Common utilities and mixins that complement these specialized types
- **haive.core.engine**: Engine implementations that use these types
- **haive.core.graph**: Graph system that leverages serializable callables and registries
- **haive.core.schema**: Schema definitions that work with dynamic enums and type literals
