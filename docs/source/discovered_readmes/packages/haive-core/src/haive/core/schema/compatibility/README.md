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

## Use Cases in Haive

### 1. Agent Composition & Chaining

Validate agent compatibility before building graphs:

```python
from haive.agents.base import Agent
from haive.core.graph import GraphBuilder

def build_agent_pipeline(agents: List[Agent]):
    """Validate agent chain compatibility before building."""
    builder = GraphBuilder()

    # Check each connection
    for i in range(len(agents) - 1):
        source, target = agents[i], agents[i + 1]

        # Check compatibility
        result = check_compatibility(
            source.output_schema,
            target.input_schema
        )

        if not result.is_compatible:
            # Create adapter if possible
            mapper = FieldMapper()
            for suggestion in result.suggested_mappings.items():
                mapper.add_mapping(suggestion[0], suggestion[1])

            # Add adapter node
            builder.add_adapter_node(f"adapter_{i}", mapper)

        # Add connection
        builder.add_edge(source.name, target.name)

    return builder.build()
```

### 2. Engine I/O Validation

Ensure engines can communicate properly:

```python
from haive.core.engine import Engine, EngineNode
from haive.core.schema import StateSchema

class AgentBuilder:
    def add_engine(self, engine: Engine, state_schema: Type[StateSchema]):
        """Validate engine compatibility with state schema."""

        # Get engine I/O requirements
        engine_inputs = engine.get_input_schema()
        engine_outputs = engine.get_output_schema()

        # Check if state has required fields
        input_compat = check_compatibility(state_schema, engine_inputs)
        if not input_compat.is_compatible:
            raise ValueError(
                f"State missing fields for engine: "
                f"{input_compat.missing_required_fields}"
            )

        # Check if engine outputs can be merged back
        output_compat = check_compatibility(engine_outputs, state_schema)
        if output_compat.requires_mapping:
            # Auto-configure mapping
            self._configure_output_mapping(engine, output_compat)
```

### 3. Multi-Agent Team Validation

Ensure agents in a team can share state:

```python
from haive.agents.team import TeamAgent

def create_agent_team(agents: List[Agent], shared_state: Type[StateSchema]):
    """Create a team with compatible agents."""

    # Analyze what each agent needs/provides
    agent_schemas = [agent.state_schema for agent in agents]

    # Find common ground
    merger = SchemaMerger(strategy="union")
    unified_schema = merger.merge_schemas(agent_schemas)

    # Validate each agent can work with unified schema
    for agent in agents:
        result = check_compatibility(unified_schema, agent.state_schema)
        if not result.is_compatible:
            print(f"Agent {agent.name} incompatible: {result.issues}")

    return TeamAgent(agents=agents, state_schema=unified_schema)
```

### 4. Dynamic Graph Construction

Build graphs with automatic compatibility handling:

```python
from haive.core.graph.node_factory import NodeFactory
from haive.core.schema.schema_composer import SchemaComposer

class SmartGraphBuilder:
    def connect_nodes(self, source_node, target_node):
        """Connect nodes with automatic adaptation."""

        # Get schemas
        source_schema = source_node.output_schema
        target_schema = target_node.input_schema

        # Check compatibility
        compat = check_compatibility(source_schema, target_schema)

        if compat.is_compatible:
            # Direct connection
            self.add_edge(source_node, target_node)
        else:
            # Need adapter
            report = generate_report(source_schema, target_schema)

            # Create adapter based on report recommendations
            adapter = self._create_adapter_from_report(report)
            self.add_node(adapter)
            self.add_edge(source_node, adapter)
            self.add_edge(adapter, target_node)
```

### 5. Schema Evolution & Versioning

Handle schema changes over time:

```python
from haive.core.schema.compatibility import SchemaEvolution

class VersionedAgent(Agent):
    """Agent with schema versioning support."""

    schema_version = "2.0"
    schema_migrations = {
        "1.0": "2.0": migrate_v1_to_v2,
        "2.0": "3.0": migrate_v2_to_v3,
    }

    @classmethod
    def load_from_checkpoint(cls, checkpoint_data: dict):
        """Load agent from checkpoint with schema migration."""
        saved_version = checkpoint_data.get("schema_version", "1.0")

        if saved_version != cls.schema_version:
            # Migrate data
            migrator = SchemaEvolution()
            checkpoint_data = migrator.migrate(
                checkpoint_data,
                from_version=saved_version,
                to_version=cls.schema_version
            )

        return cls(**checkpoint_data)
```

### 6. Tool Integration Validation

Ensure tools work with agent states:

```python
from langchain_core.tools import BaseTool
from haive.core.tools import ToolEngine

def validate_tool_compatibility(tool: BaseTool, agent_state: Type[StateSchema]):
    """Check if tool can be used with agent state."""

    # Get tool input schema
    tool_schema = tool.args_schema

    # Check if agent state has required fields
    result = check_compatibility(agent_state, tool_schema)

    if not result.is_compatible:
        # Create wrapper to adapt
        mapper = FieldMapper()

        # Map agent fields to tool inputs
        for tool_field in result.missing_required_fields:
            agent_field = find_similar_field(tool_field, agent_state.model_fields)
            if agent_field:
                mapper.add_mapping(agent_field, tool_field)

        return create_tool_wrapper(tool, mapper)

    return tool
```

### 7. Agent Game Compatibility

Validate agents can play games together:

```python
from haive.games import GameEnvironment

class GameValidator:
    def validate_player(self, agent: Agent, game: GameEnvironment):
        """Check if agent can play the game."""

        # Get game's required interface
        game_schema = game.get_player_schema()

        # Check agent compatibility
        result = check_compatibility(agent.output_schema, game_schema)

        if not result.is_compatible:
            report = generate_report(agent.output_schema, game_schema)
            raise ValueError(
                f"Agent cannot play {game.name}:\n"
                f"{report.to_markdown()}"
            )
```

### 8. Runtime Schema Composition

Dynamically compose schemas based on available components:

```python
from haive.core.schema import SchemaComposer

def create_dynamic_agent(engines: List[Engine], tools: List[BaseTool]):
    """Create agent with dynamically composed schema."""

    composer = SchemaComposer()

    # Analyze each component
    for engine in engines:
        analyzer = TypeAnalyzer()

        # Extract fields from engine
        if hasattr(engine, 'input_schema'):
            input_info = analyzer.analyze_schema(engine.input_schema)
            for field_name, field_info in input_info.fields.items():
                composer.add_field_from_info(field_info)

    # Check compatibility between components
    compatibility_matrix = {}
    for i, engine1 in enumerate(engines):
        for j, engine2 in enumerate(engines[i+1:], i+1):
            compat = check_compatibility(
                engine1.output_schema,
                engine2.input_schema
            )
            compatibility_matrix[(i, j)] = compat

    # Build optimal schema
    final_schema = composer.build()
    return Agent(state_schema=final_schema, engines=engines)
```

### 9. Prebuilt Agent Validation

Ensure prebuilt agents meet requirements:

```python
from haive.prebuilt import PrebuiltRegistry

def validate_prebuilt_agent(agent_class: Type[Agent], requirements: dict):
    """Validate prebuilt agent meets requirements."""

    analyzer = TypeAnalyzer()
    schema_info = analyzer.analyze_schema(agent_class.state_schema)

    # Check required capabilities
    missing_capabilities = []

    if requirements.get("needs_memory"):
        if "memory" not in schema_info.fields:
            missing_capabilities.append("memory field")

    if requirements.get("needs_tools"):
        if "tools" not in schema_info.fields:
            missing_capabilities.append("tools support")

    if missing_capabilities:
        # Try to extend schema
        merger = SchemaMerger()
        extended_schema = merger.merge_schemas([
            agent_class.state_schema,
            create_requirements_schema(requirements)
        ])

        return create_extended_agent(agent_class, extended_schema)

    return agent_class
```

### 10. LangGraph Integration

Ensure proper state management in LangGraph:

```python
from langgraph.graph import StateGraph
from haive.core.schema.compatibility import check_compatibility

def create_langgraph_workflow(nodes: Dict[str, callable], edges: List[tuple]):
    """Create LangGraph with compatibility validation."""

    # Infer schemas from nodes
    node_schemas = {}
    for name, node in nodes.items():
        if hasattr(node, "__annotations__"):
            # Extract input/output schemas
            node_schemas[name] = analyze_node_schema(node)

    # Validate all edges
    for source, target in edges:
        if source in node_schemas and target in node_schemas:
            compat = check_compatibility(
                node_schemas[source]["output"],
                node_schemas[target]["input"]
            )

            if not compat.is_compatible:
                logger.warning(
                    f"Edge {source} -> {target} has compatibility issues: "
                    f"{compat.issues}"
                )

    # Build graph with confidence
    graph = StateGraph(state_schema)
    # ... add nodes and edges
    return graph
```

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
