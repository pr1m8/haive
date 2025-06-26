# Haive Core

## Overview

Haive Core is the foundational framework for building AI agents, workflows, and systems with a focus on composability, type safety, and production readiness. It provides a comprehensive set of modules for creating state-of-the-art AI applications with robust architecture, consistent patterns, and extensive tooling.

The core framework extends and enhances LangChain and LangGraph capabilities, adding structured state management, advanced node systems, enhanced LLM integration, and comprehensive tooling support.

## Key Features

- **Graph-Based Architecture**: Build complex AI workflows with a flexible, typed graph system
- **State Management**: Robust state handling with schema validation and serialization
- **Enhanced LLM Integration**: Streamlined LLM configuration and tool integration
- **Composable Node System**: Reusable, configurable node components for workflows
- **Agent Framework**: Pre-built agent patterns and customizable agent architecture
- **Tool Integration**: Comprehensive tool management and discovery
- **Documentation Generation**: Automatic documentation for agents and components
- **Visualization**: Built-in visualization for graphs, states, and executions
- **Type Safety**: End-to-end type validation with Pydantic integration

## Installation

Install the full package with pip:

```bash
pip install haive-core
```

Or install via Poetry:

```bash
poetry add haive-core
```

## Modules

### Core Modules

- **[common](common/)**: Common utilities, mixins, and types used across the framework
- **[engine](engine/)**: Core engine implementations for various AI components
- **[graph](graph/)**: Comprehensive graph system for building workflows
- **[schema](schema/)**: Schema definitions and validation for state management
- **[utils](utils/)**: Utility functions and helpers for common tasks

### Specialized Modules

- **[engine/agent](engine/agent/)**: Agent implementation and orchestration
- **[engine/aug_llm](engine/aug_llm/)**: Enhanced LLM integration with configuration
- **[graph/node](graph/node/)**: Node system for workflow components
- **[graph/state_graph](graph/state_graph/)**: State graph implementation for workflows

## Quick Start

```python
from haive.core.graph.state_graph import SchemaGraph
from haive.core.graph.node import create_node
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from langgraph.graph import START, END
from pydantic import BaseModel, Field
from typing import List

# Define state schema
class AgentState(BaseModel):
    messages: List[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)

# Create LLM configurations
retriever_config = AugLLMConfig(
    name="retriever",
    system_message="Extract key information from the user query.",
    temperature=0.1
)

generator_config = AugLLMConfig(
    name="generator",
    system_message="Generate a helpful response based on the retrieved information.",
    temperature=0.7
)

# Create runnables
retriever = compose_runnable(retriever_config)
generator = compose_runnable(generator_config)

# Create a graph with schema validation
graph = SchemaGraph(name="simple_agent", state_schema=AgentState)

# Add nodes
graph.add_node("retrieve", create_node(retriever, name="retrieve"))
graph.add_node("generate", create_node(generator, name="generate"))

# Add edges
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Compile and run the graph
compiled = graph.compile()
result = compiled.invoke({"messages": [{"role": "user", "content": "What is Haive?"}]})
```

## Core Concepts

### Graph System

The graph system is the foundation of Haive's workflow architecture, providing a flexible way to build complex AI applications.

```python
from haive.core.graph.state_graph import BaseGraph
from langgraph.graph import START, END

# Create a graph
graph = BaseGraph(name="workflow")

# Add nodes
graph.add_node("process", process_node)
graph.add_node("retrieve", retrieval_node)
graph.add_node("generate", generation_node)

# Add edges
graph.add_edge(START, "process")
graph.add_edge("process", "retrieve")
graph.add_edge("retrieve", "generate")
graph.add_edge("generate", END)

# Add conditional branches
graph.add_conditional_edges(
    "process",
    lambda state: "need_retrieval" if state["needs_retrieval"] else "direct_generation",
    {
        "need_retrieval": "retrieve",
        "direct_generation": "generate"
    }
)
```

### Node System

The node system provides composable components for graph workflows with flexible configuration.

```python
from haive.core.graph.node import create_node, create_branch_node, create_tool_node

# Create a basic node
process_node = create_node(
    process_function,
    name="process",
    input_mapping={"input": "query"},
    output_mapping={"result": "processed_query"}
)

# Create a branch node
router_node = create_branch_node(
    condition=lambda state: "needs_tools" if state.get("tool_calls") else "final",
    routes={
        "needs_tools": "tool_node",
        "final": "end_node"
    }
)

# Create a tool node
tools_node = create_tool_node(
    tools=[search_tool, calculator_tool],
    handle_tool_errors=True
)
```

### Engine System

The engine system provides standardized interfaces for AI components with input/output validation.

```python
from haive.core.engine.base import BaseEngine
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from pydantic import BaseModel, Field

# Define input/output schemas
class QueryInput(BaseModel):
    query: str = Field(description="The user query")

class ResponseOutput(BaseModel):
    response: str = Field(description="The generated response")
    sources: list[str] = Field(default_factory=list, description="Sources used")

# Create a custom engine
class CustomEngine(BaseEngine):
    name = "custom_engine"
    input_schema = QueryInput
    output_schema = ResponseOutput

    def __init__(self, config=None):
        super().__init__(config)
        self.llm_config = AugLLMConfig(
            name="custom_llm",
            system_message="You are a helpful assistant."
        )
        self.llm = compose_runnable(self.llm_config)

    def _run(self, input_data: QueryInput) -> ResponseOutput:
        # Process input
        result = self.llm.invoke(input_data.query)

        # Return validated output
        return ResponseOutput(
            response=result,
            sources=[]
        )
```

### Schema System

The schema system provides type validation and serialization for graph states.

```python
from haive.core.schema import SchemaComposer
from haive.core.schema.fields import MessagesField, DictField, ListField
from pydantic import BaseModel, Field

# Define a schema using Pydantic
class AgentState(BaseModel):
    messages: list[dict] = Field(default_factory=list)
    context: dict = Field(default_factory=dict)

# Or define using SchemaComposer
schema = SchemaComposer.create({
    "messages": MessagesField(),
    "context": DictField(),
    "results": ListField(item_type=DictField())
})

# Use in a graph
from haive.core.graph.state_graph import SchemaGraph

graph = SchemaGraph(
    name="validated_workflow",
    state_schema=schema
)
```

## Best Practices

- **Use Schema Validation**: Always define state schemas for type safety and validation
- **Compose Functionality**: Break complex workflows into manageable, reusable components
- **Follow Naming Conventions**: Use consistent naming for nodes, schemas, and configurations
- **Leverage Mixins**: Use common mixins for consistent behavior across components
- **Document Components**: Add docstrings and type hints for better code understanding
- **Visualize Workflows**: Use visualization tools to understand and debug graph execution
- **Test Components**: Write tests for individual components before integration
- **Use Type Hints**: Add comprehensive type hints for better IDE support and documentation

## Advanced Usage

### Custom Node Types

```python
from haive.core.graph.node import register_custom_node_type, NodeConfig
from pydantic import Field

# Define custom node configuration
class StreamingNodeConfig(NodeConfig):
    chunk_size: int = Field(default=100)
    interval: float = Field(default=0.1)

# Register custom node type
register_custom_node_type("streaming", StreamingNodeConfig)

# Create custom node creation function
def create_streaming_node(process_func, chunk_size=100, interval=0.1, **kwargs):
    return create_node(
        process_func,
        node_type="streaming",
        chunk_size=chunk_size,
        interval=interval,
        **kwargs
    )
```

### Component Discovery

```python
from haive.core.utils.haive_discovery import discover_tools, discover_engines

# Discover available tools
tools = discover_tools()
print(f"Discovered {len(tools)} tools")

# Discover available engines
engines = discover_engines()
print(f"Discovered {len(engines)} engines")

# Generate documentation
from haive.core.utils.haive_discovery import generate_markdown_report

generate_markdown_report(
    tools=tools,
    engines=engines,
    output_path="haive_components.md"
)
```

### Extending Base Classes

```python
from haive.core.engine.base import BaseEngine
from haive.core.common.mixins import IdentifierMixin, TimestampMixin, SerializationMixin
from pydantic import BaseModel

# Create a custom engine with enhanced capabilities
class EnhancedEngine(BaseEngine, IdentifierMixin, TimestampMixin, SerializationMixin):
    def __init__(self, config=None, id=None):
        BaseEngine.__init__(self, config)
        IdentifierMixin.__init__(self, id=id)
        TimestampMixin.__init__(self)
        SerializationMixin.__init__(self)

    def _run(self, input_data):
        # Implementation here
        pass

    def to_json_file(self, path):
        """Save engine state to JSON file."""
        data = self.to_dict()
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def from_json_file(cls, path):
        """Load engine state from JSON file."""
        with open(path, "r") as f:
            data = json.load(f)
        return cls.from_dict(data)
```

## API Reference

For complete API reference, see the [documentation](https://docs.haive.ai/core/).

## Contributing

Contributions to Haive Core are welcome! Please see the [contribution guidelines](https://docs.haive.ai/contributing/) for more information.

## License

Haive Core is licensed under the terms of the license included in the repository.
