
```{note}
**Original Location:** `project_docs/agent_notes/README.md`

**Category:** general
```

# Haive Agent Framework Documentation

## Overview

This directory contains documentation for the Haive agent framework, focusing on best practices, patterns, and implementation guidelines.

## Contents

### Core Concepts

- [Best Practices](../../project_docs/agent_notes/best_practices.md) - General guidelines for working with the Haive framework
- [State Management](../../project_docs/agent_notes/state_management.md) - Detailed guide on creating and managing state in agents
- [Dynamic Graph Building](../../project_docs/agent_notes/dynamic_graph_building.md) - How to build and configure agent workflows
- [Engine Usage](../../project_docs/agent_notes/engine_usage.md) - Working with the different engine types
- [Agent Design Patterns](../../project_docs/agent_notes/agent_design_patterns.md) - Common patterns for building effective agents
- [Pydantic v2 Migration](../../project_docs/agent_notes/pydantic_v2_migration.md) - Guide for working with Pydantic v2 in Haive
- [Persistence](../../project_docs/agent_notes/persistence.md) - Using PostgreSQL for agent state persistence

## Key Principles

The Haive framework is built on several key principles:

1. **Generalizability** - Agents should be configurable and adaptable to different domains
2. **Serializability** - All components should be serializable for persistence and sharing
3. **Type Safety** - Strong typing with Pydantic for validation and documentation
4. **Modularity** - Components should be composable and reusable
5. **Extensibility** - The framework should support extension with new capabilities

## Quick Start

To create a basic agent:

1. Define your state schema
2. Configure your engines (LLM, retriever, etc.)
3. Build a workflow graph
4. Register and instantiate your agent

```python
from haive.core.schema.state_schema import StateSchema
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.agent.config import AgentConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langgraph.graph import START, END

# 1. Define state schema
class MyAgentState(StateSchema):
    messages: List[Dict[str, Any]] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

    __reducer_fields__ = {
        "messages": operator.add
    }

# 2. Configure engines
llm_config = AugLLMConfig(
    name="my_llm",
    model="gpt-4o"
)

# 3. Build workflow
graph = DynamicGraph(
    name="my_workflow",
    state_schema=MyAgentState,
    components=[llm_config]
)

# Add nodes and edges
graph.add_node("process", process_node)
graph.add_edge(START, "process")
graph.add_edge("process", END)

# Create runnable graph
runnable = graph.build()

# 4. Configure agent
agent_config = AgentConfig(
    name="my_agent",
    graph_config=graph,
    state_schema=MyAgentState
)

# Instantiate agent
agent = agent_config.instantiate()

# Use the agent
response = agent.invoke("Hello, agent!")
```

## Best Practices at a Glance

1. **Use Pydantic v2** - Always use Pydantic v2 style for models
2. **Prefer BaseModel over Dict** - Use typed models instead of dictionaries
3. **Explicit Reducers** - Define reducers for fields that will be merged
4. **Schema Composition** - Use SchemaComposer for complex schemas
5. **Engine Registration** - Register engines for discoverability
6. **Node Configuration** - Use NodeConfig for enhanced debugging
7. **Serialization** - Ensure all components are serializable
8. **Graph Visualization** - Use visualization tools for debugging

## Contributing

When adding to this documentation:

1. Focus on practical examples
2. Include code snippets that can be directly copied
3. Explain when and why to use specific patterns
4. Link to relevant sections in other documents

## Related Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Pydantic v2 Documentation](https://docs.pydantic.dev/latest/)
- [LangChain Core](https://langchain-ai.github.io/langchain/)
