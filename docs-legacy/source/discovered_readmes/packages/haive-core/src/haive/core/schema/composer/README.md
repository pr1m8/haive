# Schema Composer Module

This module provides a powerful and flexible system for dynamically creating and managing state schemas in the Haive framework. It is designed to facilitate schema composition by combining fields from various components, such as engines, Pydantic models, and dictionaries.

## Overview

The `SchemaComposer` is the central class in this module, offering a builder-style API for constructing complex state schemas at runtime. This is particularly useful for building schemas based on the components available in an agent's configuration, ensuring that the state is always consistent with the agent's architecture.

### Key Features

- **Dynamic Field Extraction**: Automatically extract fields from engines, models, and other components.
- **Flexible Field Definition**: Add and configure fields with comprehensive options for type, default values, sharing, and reducers.
- **Engine I/O Management**: Track input and output relationships between state fields and engines.
- **Rich Visualization**: Generate rich terminal outputs for debugging and analyzing schema composition.
- **Factory Methods**: Convenient class methods for creating schemas from components in a single step.

## Module Structure

The `SchemaComposer` is broken down into several mixin classes to separate concerns and improve maintainability:

- `composer.py`: The main `SchemaComposer` class that inherits from all mixins. This is the primary public interface.
- `_base.py`: The core `__init__` and `build` logic for the composer.
- `_extraction.py`: Mixin for methods that extract fields from various components (`add_fields_from_*`).
- `_engine.py`: Mixin for methods related to engine management.
- `_visualization.py`: Mixin for methods that generate rich terminal displays.
- `_factories.py`: Mixin for class methods that act as alternative constructors.

## Basic Usage

To create a schema, you can use the `SchemaComposer` builder pattern or the `from_components` factory method.

### Builder Pattern

```python
from haive.core.schema.composer import SchemaComposer
from typing import List
from langchain_core.messages import BaseMessage

# Create a composer
composer = SchemaComposer(name="MyAgentState")

# Add fields
composer.add_field("messages", List[BaseMessage], default_factory=list, shared=True)
composer.add_fields_from_components([my_llm_engine, my_retriever])

# Build the schema
AgentState = composer.build()
```

### Factory Method

```python
from haive.core.schema.composer import SchemaComposer

# Create a schema directly from components
AgentState = SchemaComposer.from_components(
    [my_llm_engine, my_retriever],
    name="MyAgentState"
)
```
