# Haive Agent Framework Best Practices

## Engine Selection Guidelines

### When to use each engine type:

#### AugLLM Engine

- **Use When**: You need enhanced LLM capabilities with integrated tools, prompts, and structured outputs
- **Key Features**: Structured output formatting, tool augmentation, few-shot examples support
- **Best For**: Complex reasoning tasks, tool-augmented generation, ensuring structured responses

#### Agent Engine

- **Use When**: You need a complete workflow with multiple steps and decision making
- **Key Features**: Full graph-based workflows, state persistence, streaming capabilities
- **Best For**: Multi-step reasoning, complex tool orchestration, stateful interactions

#### Retriever Engine

- **Use When**: You need to retrieve relevant documents from a knowledge base
- **Key Features**: Configurable search parameters, filter support, document scoring
- **Best For**: RAG applications, knowledge-intensive tasks, contextual information retrieval

#### VectorStore Engine

- **Use When**: You need low-level control over vector embeddings and similarity search
- **Key Features**: Direct embedding management, custom similarity metrics, batch operations
- **Best For**: Custom embedding workflows, specialized vector operations, data indexing

#### Persistence

- **Default**: PostgreSQL is the default persistence layer for agent state
- **Key Features**: Checkpointing, state history, trace recording, connection pooling
- **Best For**: Production deployments, long-running agents, state recovery

## State Management

### BaseModel vs Dict

Always prefer using Pydantic BaseModel for state instead of plain dictionaries:

```python
# PREFERRED: Strong typing with BaseModel
class AgentState(BaseModel):
    messages: List[BaseMessage] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)

# AVOID: Untyped dictionary
state = {
    "messages": [],
    "context": {}
}
```

**Benefits of BaseModel approach:**

- Type safety with runtime validation
- Self-documenting code with field descriptions
- IDE autocompletion support
- Serialization/deserialization handling
- Schema introspection capabilities

### Pydantic v2 Requirements

Haive uses Pydantic v2 throughout the codebase. Key differences from v1 include:

1. **Model Configuration**:

   ```python
   # Pydantic v2 style
   model_config = {"arbitrary_types_allowed": True}

   # NOT v1 style
   class Config:
       arbitrary_types_allowed = True
   ```

2. **Field Validation**:

   ```python
   # Pydantic v2 style
   @field_validator("field_name")
   def validate_field(cls, value):
       return value

   # NOT v1 style
   @validator("field_name")
   def validate_field(cls, value):
       return value
   ```

3. **Model Methods**:

   ```python
   # Pydantic v2 style
   model.model_dump()  # Not model.dict()
   model.model_dump_json()  # Not model.json()
   model.model_validate()  # Not model.parse_obj()
   ```

4. **Type Annotations**:
   ```python
   # Annotated fields for reducers and other metadata
   messages: Annotated[List[BaseMessage], operator.add]
   ```

## Node Implementation

### When to Use NodeConfig vs Direct Functions

- **Use NodeConfig**: For complex nodes that need input/output mapping, debugging support, or tool integration
- **Use Direct Functions**: For simple transformations or when maximum performance is needed

### Debugging Best Practices

Enable rich debugging for complex nodes:

```python
from haive.core.graph.node.factory import NodeFactory

# Enable global debug mode
NodeFactory.set_debug(True, rich_ui=True)

# Or enable per-node debugging
node_config = NodeConfig(
    debug=True,
    rich_debug=True,
    debug_log_path="path/to/logs"
)
```

## State Schema Design

### Field Sharing Patterns

Use the schema composer to properly designate shared fields:

```python
from haive.core.schema.schema_composer import SchemaComposer

composer = SchemaComposer("MyAgentSchema")
composer.add_field(
    name="messages",
    field_type=List[BaseMessage],
    shared=True,  # This field will be shared with parent graphs
    reducer=operator.add  # This defines how the field is reduced in branches
)
```

### Engine I/O Mappings

Properly map fields to engine inputs and outputs:

```python
composer.add_field(
    name="query",
    field_type=str,
    input_for=["retriever_engine", "llm_engine"],  # Used as input for these engines
)

composer.add_field(
    name="documents",
    field_type=List[Document],
    output_from=["retriever_engine"],  # Produced by this engine
)
```
