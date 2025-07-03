# Schema Composition Best Practices - Claude Discovery Agent

**Date**: 2025-06-28  
**Focus**: When and how to use different schema composition patterns

## Schema Composition Patterns

### **1. AgentSchemaComposer - The Gold Standard for Multi-Agent**

**When to use:**

- Multiple agents that need coordination
- Message preservation is critical (tool_call_id)
- Complex field separation strategies needed
- Build modes matter (parallel, sequential, hierarchical)

**Example:**

```python
from haive.core.schema.agent_schema_composer import AgentSchemaComposer, BuildMode

# For true multi-agent systems
schema = AgentSchemaComposer.from_agents(
    agents=[planner_agent, executor_agent, reviewer_agent],
    name="MultiAgentState",
    separation="smart",  # Intelligent field separation
    build_mode=BuildMode.SEQUENCE,  # Sequential execution
    include_meta=True  # For agent coordination
)
```

**Key Features:**

- `preserve_messages_reducer` - maintains tool_call_id
- Field separation strategies (smart/shared/namespaced)
- Build modes for execution patterns
- Meta state for coordination
- Auto-detection of requirements

### **2. SchemaComposer - For Simple Components**

**When to use:**

- Simple components without reasoning (retrievers, embeddings)
- Basic field composition without complex reducers
- No message preservation requirements
- Single-purpose execution nodes

**Example:**

```python
from haive.core.schema.schema_composer import SchemaComposer

# For simple component composition
schema = SchemaComposer.from_components(
    components=[retriever_engine, embedding_engine],
    name="ComponentState"
)
```

**Key Features:**

- Straightforward field extraction
- No complex reducer logic
- Lightweight composition
- Good for non-agent components

### **3. Direct Schema Definition - For Known Requirements**

**When to use:**

- Schema requirements are well-defined upfront
- Custom reducers or validators needed
- Performance-critical paths
- Simple, static schemas

**Example:**

```python
from pydantic import BaseModel, Field
from langchain_core.messages import BaseMessage

class SimpleRAGState(BaseModel):
    query: str = Field(description="User query")
    documents: list[Document] = Field(default_factory=list)
    messages: list[BaseMessage] = Field(default_factory=list)
```

## Anti-Patterns to Avoid

### **1. Using AgentSchemaComposer for Non-Agents**

```python
# WRONG - Overkill for simple retriever
schema = AgentSchemaComposer.from_agents(
    agents=[retriever_only_node],  # Not a real agent!
    separation="smart"
)

# RIGHT - Use simple composer
schema = SchemaComposer.from_components(
    components=[retriever_engine]
)
```

### **2. Modifying Engine Schemas Directly**

```python
# WRONG - SimpleAgent modifying engine schema
self.engine.output_schema = enhanced_schema  # Dangerous!

# RIGHT - Keep modifications local
self.output_schema = enhanced_schema  # Agent's own schema
```

### **3. Missing Message Preservation**

```python
# WRONG - Using default add operator for messages
composer.add_field("messages", list[BaseMessage], reducer=operator.add)

# RIGHT - Use preserve_messages_reducer
from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer
composer.add_field("messages", list[BaseMessage], reducer=preserve_messages_reducer)
```

### **4. No Schema at All**

```python
# WRONG - ChainAgent with no schema handling
class ChainAgent(Agent):
    def build_graph(self):
        # Just adds nodes, no schema composition!

# RIGHT - Add proper schema setup
def setup_agent(self):
    self.state_schema = AgentSchemaComposer.from_agents(...)
```

## Best Practices

### **1. Choose the Right Composer**

```python
def choose_composer(components):
    """Select appropriate composer based on components."""

    # Check if any are true agents
    agents = [c for c in components if hasattr(c, 'has_reasoning_capability')
              and c.has_reasoning_capability()]

    if agents:
        # Use AgentSchemaComposer for agents
        return AgentSchemaComposer.from_agents(
            agents=agents,
            separation="smart"
        )
    else:
        # Use basic composer for components
        return SchemaComposer.from_components(
            components=components
        )
```

### **2. Always Preserve Messages in Multi-Agent**

```python
# Ensure tool_call_id preservation
if "messages" in fields:
    composer.add_field(
        "messages",
        list[BaseMessage],
        reducer=preserve_messages_reducer,  # Critical!
        default_factory=list
    )
```

### **3. Use Type-Safe Field Definitions**

```python
# Define clear field types
composer.add_field(
    name="search_results",
    field_type=list[Document],  # Specific type
    default_factory=list,
    description="Retrieved documents"
)
```

### **4. Leverage Auto-Detection**

```python
# Let AgentSchemaComposer figure out requirements
schema = AgentSchemaComposer.from_agents(
    agents=agents,
    # These auto-detect if not specified:
    include_meta=None,  # Auto-detects need
    build_mode=None,    # Auto-selects mode
)
```

### **5. Document Schema Intent**

```python
class WorkflowState(StateSchema):
    """State schema for document processing workflow.

    Uses AgentSchemaComposer because:
    - Multiple agents need coordination
    - Tool calls must preserve IDs
    - Sequential execution required
    """
```

## Schema Composition Decision Tree

```
Is it a true agent (has LLM/reasoning)?
├─ Yes: Multiple agents?
│   ├─ Yes: Use AgentSchemaComposer
│   │   └─ Consider: separation strategy, build mode
│   └─ No: Single agent?
│       ├─ Complex schema needs: AgentSchemaComposer
│       └─ Simple schema: Direct definition
└─ No: It's a component
    ├─ Multiple components: Use SchemaComposer
    └─ Single component: Direct schema or none

Special Considerations:
- Need message preservation? → AgentSchemaComposer
- Need field separation? → AgentSchemaComposer
- Need meta state? → AgentSchemaComposer
- Simple I/O only? → SchemaComposer or direct
```

## Examples by Use Case

### **Multi-Agent RAG System**

```python
# Multiple agents with coordination
schema = AgentSchemaComposer.from_agents(
    agents=[query_processor, retriever_agent, synthesis_agent],
    separation="smart",
    build_mode=BuildMode.SEQUENCE
)
```

### **Simple Retrieval Pipeline**

```python
# Just components, no agents
schema = SchemaComposer.from_components(
    components=[embedder, retriever, reranker]
)
```

### **Single Agent with Tools**

```python
# Single agent but needs tool preservation
schema = AgentSchemaComposer.from_agents(
    agents=[react_agent],
    separation="shared"  # Single agent = all shared
)
```

### **Custom Workflow**

```python
# Known requirements, direct definition
class CustomWorkflowState(BaseModel):
    stage: str = "init"
    data: dict = Field(default_factory=dict)
    errors: list[str] = Field(default_factory=list)
```

## Summary

The key is to **match schema complexity to actual needs**:

1. **AgentSchemaComposer** - For true multi-agent scenarios with coordination needs
2. **SchemaComposer** - For simple component composition without agent complexity
3. **Direct schemas** - When requirements are clear and static
4. **No schema** - Almost never the right choice

Always remember: **Not everything needs the complexity of AgentSchemaComposer!**
