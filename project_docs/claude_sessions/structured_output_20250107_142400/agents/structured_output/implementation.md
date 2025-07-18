# Structured Output Implementation Details

## Core Components

### 1. OutputAdapter (output_mixin.py)

The heart of the transformation system. Key methods:

```python
def transform(self, output: Any) -> Any:
    # 1. Convert to dict
    # 2. Extract specific field if requested
    # 3. Apply field mapping
    # 4. Apply output parser
    # 5. Validate against target schema
```

**Transformation Pipeline**:

1. **Input Normalization** - Convert BaseModel/dict/other to dict
2. **Field Extraction** - Pull nested data if `extract_field` specified
3. **Field Mapping** - Rename fields according to mapping
4. **Output Parsing** - Apply LangChain parser if provided
5. **Schema Validation** - Ensure output matches target schema

### 2. OutputMixin (output_mixin.py)

Provides structured output capabilities to any class:

```python
class MyAgent(OutputMixin):
    structured_output_model: type[BaseModel] = MyModel

    def process(self, data):
        return self.transform_output(data)
```

**Key Features**:

- Auto-creates OutputAdapter based on configuration
- Provides `transform_output()` convenience method
- Includes state transformation utilities (messages ↔ documents)
- Smart field name generation from model names

### 3. StructuredOutputAgent (structured_output_wrapper.py)

Wrapper that uses multi-agent composition:

```python
StructuredOutputAgent(MultiAgent):
    inner_agent: Agent  # The agent to wrap
    structured_output_model: Type[BaseModel]  # Desired output

    def __init__(self):
        # Creates transformation agent automatically
        transform_agent = SimpleAgent(
            structured_output_model=self.structured_output_model
        )
        # Sets up sequential multi-agent flow
        super().__init__(agents=[inner_agent, transform_agent])
```

**Architecture**:

- Leverages MultiAgent for composition
- First agent: Original agent execution
- Second agent: Transform to structured output
- State flows automatically between agents

### 4. StructuredOutputEnhancer (structured_output_wrapper.py)

Utility class with convenience patterns:

```python
# Pattern 1: Generic append
enhanced = StructuredOutputEnhancer.append_structured_output(
    agent=my_agent,
    structured_output_model=MyModel
)

# Pattern 2: RAG-specific
structured_rag = StructuredOutputEnhancer.create_rag_to_structured(
    rag_agent=rag_agent,
    structured_output_model=DocumentSummary
)

# Pattern 3: ReAct-specific
structured_react = StructuredOutputEnhancer.create_react_to_structured(
    react_agent=react_agent,
    structured_output_model=TaskResult
)
```

## Integration Points

### With SimpleAgent

SimpleAgent already has structured output support via engine modification. Our wrapper provides an alternative approach that doesn't modify the engine.

### With MultiAgent

Perfect fit - uses existing sequential execution pattern. State automatically flows between agents.

### With BaseRAGAgent

RAG agents output documents. Our transformer can:

- Extract document content
- Summarize into structured format
- Map document fields to output schema

### With ReactAgent

ReAct agents have reasoning traces. Our transformer can:

- Extract final results
- Include/exclude reasoning steps
- Structure tool outputs

## Performance Considerations

1. **Overhead**: Minimal - just dict transformations and validation
2. **Memory**: Creates new objects, doesn't modify in-place
3. **Async**: Currently sync, but could add async support
4. **Streaming**: Not supported yet, would need different approach
