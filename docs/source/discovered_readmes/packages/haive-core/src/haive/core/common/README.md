# Haive Core: Common Module

## Overview

The Common module provides foundational components used throughout the Haive framework. It contains utilities, models, types, and mixins that enable consistent behavior across different parts of the system. This module serves as the backbone for the framework's core functionality, providing standardized approaches to common tasks like identification, serialization, state management, and logging.

## Key Features

- **Reusable Mixins**: Collection of composable behaviors for object identification, timestamps, versioning, and more
- **Common Types**: Type definitions and protocols for consistent type hinting
- **Enhanced Data Structures**: Advanced collection structures with rich functionality
- **Centralized Logging**: Unified logging configuration
- **State Management**: Tools for managing component state and serialization

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
from haive.core.common.mixins import IdentifierMixin, TimestampMixin
from haive.core.common.types import JsonType, DictStrAny
from haive.core.common.logging_config import configure_logging

# Create a component with ID and timestamp capabilities
class MyComponent(IdentifierMixin, TimestampMixin):
    def __init__(self, name: str):
        super().__init__()
        self.name = name

# Configure logging
configure_logging(level="INFO")

# Create an instance
component = MyComponent(name="Test Component")
print(f"Component ID: {component.id}")
print(f"Created at: {component.created_at}")
```

## Components

### Mixins

The mixins package provides reusable functionality that can be composed into classes through multiple inheritance. Mixins help avoid code duplication and promote consistent behavior.

```python
# Basic ID mixin for UUID-based identification
from haive.core.common.mixins.general import IdMixin
from pydantic import BaseModel

class MyItem(IdMixin, BaseModel):
    name: str

item = MyItem(name="Test Item")
print(item.id)  # UUID string

# Create with specific ID
custom_item = MyItem.with_id("custom-id-123", name="Custom Item")
print(custom_item.id)  # "custom-id-123"
```

#### Available Mixins

- **IdMixin**: Basic UUID identification
- **IdentifierMixin**: Comprehensive identification with type and namespace
- **TimestampMixin**: Created/updated timestamps
- **VersionMixin**: Version tracking
- **SerializationMixin**: JSON serialization capabilities
- **MetadataMixin**: Flexible metadata storage
- **StateMixin**: State management and tracking
- **RichLoggerMixin**: Enhanced logging capabilities
- **SecureConfigMixin**: Secure configuration handling
- **ToolListMixin**: Tool management
- **CheckpointerMixin**: State checkpointing

### Types

Common type definitions used throughout the framework for consistent type hinting.

```python
from haive.core.common.types import JsonType, DictStrAny, StrOrPath

# JSON-compatible data
data: JsonType = {"name": "example", "values": [1, 2, 3]}

# Dictionary with string keys and any values
config: DictStrAny = {"api_key": "secret", "timeout": 30, "active": True}

# String or Path-like object
file_path: StrOrPath = "path/to/file.txt"
```

### Structures

Enhanced data structures with additional functionality beyond standard Python collections.

```python
from haive.core.common.structures.named_dict import NamedDict

# Create a named dictionary from objects with name attributes
components = NamedDict([
    {"name": "auth", "type": "service"},
    {"name": "db", "type": "database"}
])

# Access by key
auth_component = components["auth"]

# Access by attribute
db_component = components.db

# Use enhanced lookup methods
by_type = components.get_by_attr("type", "service")
```

### Models

Common data structures and models for use across the framework.

```python
from haive.core.common.models import DynamicChoiceModel, NamedList

# Create a named list
tools = NamedList(["search", "calculate", "transform"])
search_tool = tools.get("search")

# Dynamic choice model
from pydantic import BaseModel
from typing import List

class ModelWithChoices(BaseModel):
    choice_field: str = DynamicChoiceModel.field(
        ["option1", "option2", "option3"],
        default="option1"
    )
```

## Usage Patterns

### Composition with Mixins

```python
from haive.core.common.mixins import (
    IdentifierMixin,
    TimestampMixin,
    SerializationMixin
)
from pydantic import BaseModel

# Compose functionality through multiple inheritance
class Component(IdentifierMixin, TimestampMixin, SerializationMixin, BaseModel):
    name: str
    description: str = None

    def __init__(self, **data):
        super().__init__(**data)

# Create component with auto-generated ID and timestamps
component = Component(name="Example Component")

# Serialize to JSON
json_data = component.to_json()

# Deserialize from JSON
restored = Component.from_json(json_data)
```

### Centralized Logging

```python
from haive.core.common.logging_config import configure_logging
from haive.core.common.mixins import RichLoggerMixin

# Configure global logging
configure_logging(level="INFO", log_file="app.log")

# Create component with rich logging capabilities
class LoggingComponent(RichLoggerMixin):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def process(self, data):
        self.logger.info(f"Processing data with {self.name}")
        # Process data...
        self.logger.success(f"Successfully processed data")
```

## Configuration

The Common module provides utilities for secure configuration management:

```python
from haive.core.common.mixins import SecureConfigMixin
from pydantic import BaseModel, SecretStr

class APIConfig(SecureConfigMixin, BaseModel):
    api_key: SecretStr
    endpoint: str
    timeout: int = 30

# Create configuration with secure handling of secrets
config = APIConfig(api_key="secret_key_123", endpoint="https://api.example.com")

# Access secure string value
key_value = config.api_key.get_secret_value()

# Get redacted representation for logs
safe_config = config.get_redacted_dict()
print(safe_config)  # {'api_key': '***', 'endpoint': 'https://api.example.com', 'timeout': 30}
```

## Integration with Other Modules

### Integration with Engine Module

```python
from haive.core.common.mixins import EngineMixin
from haive.core.engine import BaseEngine

class CustomEngine(BaseEngine):
    # Engine implementation...
    pass

# Component that integrates with engines
class EngineComponent(EngineMixin):
    def __init__(self, engine=None):
        super().__init__(engine=engine)

    def process(self, input_data):
        # Use the connected engine
        if self.engine:
            return self.engine.run(input_data)
        return None
```

### Integration with Graph Module

```python
from haive.core.common.structures.tree import Tree
from haive.core.graph.node import BaseNode

# Use tree structure to organize nodes
node_tree = Tree()

# Add nodes to the tree
node_tree.add("root", BaseNode(name="root"))
node_tree.add("root/child1", BaseNode(name="child1"))
node_tree.add("root/child1/grandchild", BaseNode(name="grandchild"))

# Access nodes by path
root_node = node_tree.get("root")
child_node = node_tree.get("root/child1")
```

## Best Practices

- **Prefer Composition**: Use mixins to compose functionality rather than deep inheritance hierarchies
- **Standardize Types**: Use the common type definitions throughout your codebase for consistency
- **Centralize Logging**: Configure logging once using the logging_config module
- **Secure Secrets**: Always use SecureConfigMixin for any configuration containing sensitive data
- **Consistent IDs**: Use the ID mixins to ensure consistent identification across components
- **Enhanced Collections**: Leverage the enhanced data structures for cleaner, more expressive code

## Advanced Usage

### Custom Mixins

```python
from haive.core.common.mixins.general import SerializationMixin
from pydantic import BaseModel
import json

# Create a custom mixin extending existing functionality
class CompressedSerializationMixin(SerializationMixin):
    def to_compressed_json(self):
        """Serialize to compressed JSON without whitespace."""
        return json.dumps(self.model_dump(), separators=(',', ':'))

    @classmethod
    def from_compressed_json(cls, data):
        """Deserialize from compressed JSON."""
        return cls(**json.loads(data))

# Use the custom mixin
class CompactModel(CompressedSerializationMixin, BaseModel):
    name: str
    data: dict

# Create instance and use the custom serialization
model = CompactModel(name="test", data={"a": 1, "b": 2})
compressed = model.to_compressed_json()
```

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/core/common).

## Related Modules

- **haive.core.engine**: Builds on common components for engine implementation
- **haive.core.graph**: Uses common structures for graph representation
- **haive.core.schema**: Extends common types for schema definition
- **haive.core.utils**: Provides additional utilities complementing common functionality
