# Haive Schema Compatibility Module

A comprehensive type checking, compatibility analysis, and schema transformation system for the Haive framework.

## Overview

The Schema Compatibility Module provides advanced tools for:

- **Type Analysis**: Deep introspection of Python types including generics, protocols, and Pydantic models
- **Compatibility Checking**: Multi-level compatibility analysis between schemas
- **Type Conversion**: Pluggable converter system with built-in support for common types and LangChain objects
- **Field Mapping**: Advanced field mapping with transformations, aggregations, and computed fields
- **Schema Merging**: Multiple strategies for combining schemas
- **Validation**: Comprehensive field and model validation framework
- **Reporting**: Detailed compatibility reports with actionable recommendations

## Installation

The module is part of the Haive core package:

```bash
# From haive-core directory
pip install -e .
```

## Quick Start

### Basic Compatibility Check

```python
from haive.core.schema.compatibility import check_compatibility
from pydantic import BaseModel

class SourceSchema(BaseModel):
    name: str
    age: int

class TargetSchema(BaseModel):
    name: str
    age: int
    email: str = ""

result = check_compatibility(SourceSchema, TargetSchema)
print(f"Compatible: {result.is_compatible}")  # True
```

### Type Conversion

```python
from haive.core.schema.compatibility import ConverterRegistry
from langchain_core.messages import HumanMessage, AIMessage

registry = ConverterRegistry()
human_msg = HumanMessage(content="Hello")
ai_msg = registry.convert(human_msg, HumanMessage, AIMessage)
```

### Field Mapping

```python
from haive.core.schema.compatibility import FieldMapper

mapper = FieldMapper()
mapper.add_mapping("user.firstName", "first_name", transformer=str.lower)
mapper.add_mapping("user.lastName", "last_name", transformer=str.lower)

result = mapper.map_data({
    "user": {"firstName": "John", "lastName": "Doe"}
})
# {"first_name": "john", "last_name": "doe"}
```

## Core Components

### TypeAnalyzer

Performs deep type introspection:

```python
from haive.core.schema.compatibility import TypeAnalyzer

analyzer = TypeAnalyzer()
info = analyzer.analyze_schema(MySchema)
print(info.fields)  # Field information
print(info.shared_fields)  # Haive StateSchema metadata
```

### CompatibilityChecker

Checks compatibility between schemas:

```python
from haive.core.schema.compatibility import CompatibilityChecker

checker = CompatibilityChecker()
result = checker.check_schema_compatibility(
    source_schema,
    target_schema,
    mode="subset"  # or "strict", "partial"
)
```

### ConverterRegistry

Manages type converters:

```python
from haive.core.schema.compatibility import ConverterRegistry, TypeConverter

class CustomConverter(TypeConverter):
    def can_convert(self, source_type, target_type):
        return source_type == MyType and target_type == OtherType

    def convert(self, value, context):
        return OtherType(value.data)

registry = ConverterRegistry()
registry.register(CustomConverter())
```

### FieldMapper

Maps fields between incompatible schemas:

```python
from haive.core.schema.compatibility import FieldMapper

mapper = FieldMapper()

# Simple mapping
mapper.add_mapping("source_field", "target_field")

# With transformation
mapper.add_mapping(
    "price",
    "formatted_price",
    transformer=lambda x: f"${x:.2f}"
)

# Nested paths
mapper.add_mapping("user.profile.name", "username")

# Computed fields
mapper.add_computed_field(
    "full_name",
    lambda: f"{data['first']} {data['last']}"
)
```

### SchemaMerger

Merges multiple schemas:

```python
from haive.core.schema.compatibility import SchemaMerger

merger = SchemaMerger(strategy="union")
MergedSchema = merger.merge_schemas([Schema1, Schema2, Schema3])
```

### Validators

Field and model validation:

```python
from haive.core.schema.compatibility.validators import ValidatorBuilder

validator = ValidatorBuilder.for_range(0, 100, "percentage")
email_validator = ValidatorBuilder.for_pattern(r".*@.*\..*", "email")
```

## Advanced Features

### LangChain Integration

Built-in converters for LangChain types:

```python
# Automatic registration
from haive.core.schema.compatibility import register_langchain_converters
register_langchain_converters()

# Convert between message types
converter = MessageConverter()
ai_msg = converter.convert(human_msg, context)

# Convert documents to messages
doc_converter = DocumentConverter()
message = doc_converter.convert(document, context)
```

### Compatibility Reports

Generate detailed analysis reports:

```python
from haive.core.schema.compatibility import generate_report

report = generate_report(source_schema, target_schema)
print(report.to_markdown())  # Human-readable report
print(report.to_json())      # Machine-readable format
```

### Plugin System

Extend functionality with plugins:

```python
from haive.core.schema.compatibility.protocols import (
    compatibility_plugin,
    CompatibilityPlugin
)

@compatibility_plugin(priority=100)
class MyPlugin:
    def check_compatibility(self, source_type, target_type):
        # Custom compatibility logic
        pass
```

### Performance Optimization

- **Caching**: Type analysis results are cached
- **Lazy Evaluation**: Expensive operations deferred
- **Path Finding**: Efficient multi-step conversion paths

## Integration with Haive

### StateSchema Support

Full support for Haive StateSchema features:

```python
class MyState(StateSchema):
    messages: List[BaseMessage] = Field(default_factory=list)

    __shared_fields__ = ["messages"]
    __reducer_fields__ = {"messages": add_messages}
    __engine_io_mappings__ = {
        "llm": {"inputs": ["messages"], "outputs": ["response"]}
    }

# Analyzer extracts all metadata
info = analyzer.analyze_schema(MyState)
print(info.shared_fields)  # {"messages"}
```

### Agent Compatibility

Check agent compatibility:

```python
def check_agent_chain(agent1: Agent, agent2: Agent):
    result = check_compatibility(
        agent1.output_schema,
        agent2.input_schema
    )
    if not result.is_compatible:
        print(f"Incompatible: {result.missing_required_fields}")
```

## Best Practices

1. **Explicit Over Implicit**: Always declare schemas explicitly
2. **Check Early**: Validate compatibility during development
3. **Use Type Hints**: Leverage Python's type system
4. **Cache Results**: Reuse analyzers and checkers
5. **Handle Errors**: Always check conversion results

## Common Patterns

### Schema Evolution

```python
# Version 1
class UserV1(BaseModel):
    name: str
    email: str

# Version 2
class UserV2(BaseModel):
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.now)

# Migration function
def migrate_v1_to_v2(v1_data: dict) -> dict:
    v2_data = v1_data.copy()
    v2_data["created_at"] = datetime.now()
    return v2_data
```

### Adapter Pattern

```python
class SchemaAdapter:
    def __init__(self, source_schema, target_schema):
        self.mapper = FieldMapper()
        # Configure mappings

    def adapt(self, data):
        return self.mapper.map_data(data)
```

## API Reference

See individual module documentation:

- `analyzer.py` - Type analysis
- `compatibility.py` - Compatibility checking
- `converters.py` - Type conversion
- `field_mapping.py` - Field mapping
- `validators.py` - Validation
- `mergers.py` - Schema merging
- `reports.py` - Report generation
- `langchain_converters.py` - LangChain types
- `protocols.py` - Extension protocols
- `types.py` - Type definitions
- `utils.py` - Utility functions

## Contributing

1. Follow existing patterns
2. Add tests for new features
3. Update documentation
4. Use type hints throughout
5. Handle edge cases gracefully

## License

Part of the Haive framework. See main LICENSE file.
