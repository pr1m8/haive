# Schema Registry & Prebuilt Components Design

## Overview

Create a registry-based schema system with prebuilt schemas for common patterns, engine-specific states, and easier callable node creation.

## Core Components

### 1. Schema Registry

```python
from typing import Type, TypeVar, Dict, Any
from pydantic import BaseModel
from abc import ABC, abstractmethod

TSchema = TypeVar("TSchema", bound=BaseModel)

class SchemaRegistry:
    """Central registry for all schema types."""

    _instance = None
    _schemas: Dict[str, Type[BaseModel]] = {}
    _engine_schemas: Dict[str, Dict[str, Type[BaseModel]]] = {}
    _sub_schemas: Dict[str, Type[BaseModel]] = {}

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_schema(self, name: str, schema: Type[BaseModel], category: str = "general"):
        """Register a schema with the registry."""
        if category == "engine":
            # Special handling for engine schemas
            engine_type, schema_type = name.split(".", 1)
            if engine_type not in self._engine_schemas:
                self._engine_schemas[engine_type] = {}
            self._engine_schemas[engine_type][schema_type] = schema
        elif category == "sub":
            self._sub_schemas[name] = schema
        else:
            self._schemas[name] = schema

    def get_schema(self, name: str) -> Type[BaseModel] | None:
        """Get a schema by name."""
        # Try general schemas first
        if name in self._schemas:
            return self._schemas[name]

        # Try engine schemas
        if "." in name:
            engine_type, schema_type = name.split(".", 1)
            if engine_type in self._engine_schemas:
                return self._engine_schemas[engine_type].get(schema_type)

        # Try sub schemas
        return self._sub_schemas.get(name)

    def create_composite(self, name: str, components: list[str]) -> Type[BaseModel]:
        """Create a composite schema from multiple registered schemas."""
        fields = {}
        for component in components:
            schema = self.get_schema(component)
            if schema:
                for field_name, field_info in schema.model_fields.items():
                    fields[field_name] = (field_info.annotation, field_info)

        return create_model(name, **fields)
```

### 2. Prebuilt Engine State Schemas

```python
# LLM Engine States
class LLMInputState(BaseModel):
    """Standard input state for LLM engines."""
    prompt: str | None = Field(None, description="Direct prompt")
    messages: list[BaseMessage] = Field(default_factory=list, description="Conversation messages")
    context: str | None = Field(None, description="Additional context")
    temperature: float = Field(0.7, description="Sampling temperature")
    max_tokens: int | None = Field(None, description="Maximum tokens")

    class Config:
        schema_extra = {
            "engine_type": "llm",
            "schema_type": "input"
        }

class LLMOutputState(BaseModel):
    """Standard output state for LLM engines."""
    response: str = Field(..., description="LLM response")
    messages: list[BaseMessage] = Field(default_factory=list, description="Updated messages")
    usage: dict[str, int] | None = Field(None, description="Token usage")

    class Config:
        schema_extra = {
            "engine_type": "llm",
            "schema_type": "output"
        }

# Retriever Engine States
class RetrieverInputState(BaseModel):
    """Standard input state for retriever engines."""
    query: str = Field(..., description="Search query")
    top_k: int = Field(5, description="Number of results")
    filters: dict[str, Any] = Field(default_factory=dict, description="Search filters")

    class Config:
        schema_extra = {
            "engine_type": "retriever",
            "schema_type": "input"
        }

class RetrieverOutputState(BaseModel):
    """Standard output state for retriever engines."""
    documents: list[Document] = Field(..., description="Retrieved documents")
    context: str | None = Field(None, description="Concatenated document content")
    scores: list[float] | None = Field(None, description="Relevance scores")

    class Config:
        schema_extra = {
            "engine_type": "retriever",
            "schema_type": "output"
        }

# Tool Engine States
class ToolInputState(BaseModel):
    """Standard input state for tool engines."""
    tool_name: str = Field(..., description="Tool to invoke")
    tool_args: dict[str, Any] = Field(..., description="Tool arguments")

    class Config:
        schema_extra = {
            "engine_type": "tool",
            "schema_type": "input"
        }

class ToolOutputState(BaseModel):
    """Standard output state for tool engines."""
    tool_result: Any = Field(..., description="Tool execution result")
    tool_error: str | None = Field(None, description="Error if tool failed")

    class Config:
        schema_extra = {
            "engine_type": "tool",
            "schema_type": "output"
        }
```

### 3. Sub-State Schemas (Composable Components)

```python
# Common sub-schemas that can be mixed into larger states
class MessageHistory(BaseModel):
    """Conversation message history."""
    messages: list[BaseMessage] = Field(
        default_factory=list,
        description="Conversation messages"
    )

    __reducer_fields__ = {
        "messages": add_messages
    }

class DocumentContext(BaseModel):
    """Document retrieval context."""
    documents: list[Document] = Field(default_factory=list)
    context: str = Field(default="")

    def update_context(self):
        """Update context from documents."""
        self.context = "\n\n".join(doc.page_content for doc in self.documents)

class QueryState(BaseModel):
    """Query handling state."""
    query: str = Field(default="")
    query_history: list[str] = Field(default_factory=list)

    def add_query(self, query: str):
        self.query = query
        self.query_history.append(query)

class ErrorState(BaseModel):
    """Error tracking state."""
    errors: list[dict[str, Any]] = Field(default_factory=list)
    last_error: str | None = None

    def add_error(self, error: str, details: dict | None = None):
        self.last_error = error
        self.errors.append({
            "error": error,
            "details": details or {},
            "timestamp": datetime.now()
        })

class MetadataState(BaseModel):
    """Metadata tracking."""
    metadata: dict[str, Any] = Field(default_factory=dict)
    tags: list[str] = Field(default_factory=list)

    def add_metadata(self, key: str, value: Any):
        self.metadata[key] = value
```

### 4. Schema Composition Helpers

```python
class SchemaComposer:
    """Helper for composing schemas from components."""

    @staticmethod
    def create_agent_state(
        name: str,
        components: list[str],
        additional_fields: dict[str, Any] | None = None
    ) -> Type[StateSchema]:
        """Create an agent state from components."""

        registry = SchemaRegistry.get_instance()

        # Base fields from StateSchema
        fields = {}

        # Add component fields
        for component in components:
            schema = registry.get_schema(component)
            if not schema:
                # Try sub-schemas
                schema = registry.get_schema(f"sub.{component}")

            if schema:
                for field_name, field_info in schema.model_fields.items():
                    fields[field_name] = (field_info.annotation, field_info)

        # Add additional fields
        if additional_fields:
            fields.update(additional_fields)

        # Create the state class
        state_class = create_model(
            name,
            __base__=StateSchema,
            **fields
        )

        # Register it
        registry.register_schema(name, state_class)

        return state_class

# Usage example
RAGAgentState = SchemaComposer.create_agent_state(
    "RAGAgentState",
    components=["messages", "query", "documents", "context"],
    additional_fields={
        "summary": (str, Field(default="", description="Summary of conversation"))
    }
)
```

### 5. Easier Callable Nodes

```python
from functools import wraps
from typing import Callable, TypeVar

TState = TypeVar("TState", bound=BaseModel)

def callable_node(
    name: str | None = None,
    input_state: Type[BaseModel] | str | None = None,
    output_state: Type[BaseModel] | str | None = None,
    goto: str | None = None
):
    """Decorator to create callable nodes easily."""

    def decorator(func: Callable) -> NodeFunction:
        node_name = name or func.__name__

        # Resolve state types from registry if strings
        registry = SchemaRegistry.get_instance()

        if isinstance(input_state, str):
            input_type = registry.get_schema(input_state)
        else:
            input_type = input_state

        if isinstance(output_state, str):
            output_type = registry.get_schema(output_state)
        else:
            output_type = output_state

        @wraps(func)
        def node_function(state: Any, config: dict | None = None) -> Command:
            # Validate input if type specified
            if input_type:
                if hasattr(state, "model_validate"):
                    validated_state = input_type.model_validate(state.model_dump())
                else:
                    validated_state = input_type(**state)
            else:
                validated_state = state

            # Call the function
            result = func(validated_state, config)

            # Handle result
            if isinstance(result, Command):
                return result

            # Validate output if type specified
            if output_type and not isinstance(result, output_type):
                result = output_type.model_validate(result)

            return Command(update=result, goto=goto)

        # Add metadata
        node_function.__node_name__ = node_name
        node_function.__input_state__ = input_type
        node_function.__output_state__ = output_type

        return node_function

    return decorator

# Usage examples
@callable_node(
    name="process_query",
    input_state="llm.input",
    output_state="llm.output",
    goto="next_node"
)
def process_query_node(state: LLMInputState, config: dict | None = None) -> LLMOutputState:
    # Simple function that returns output state
    return LLMOutputState(
        response=f"Processed: {state.prompt}",
        messages=state.messages
    )

@callable_node()  # Minimal decorator
def simple_node(state, config=None):
    # Just modify state directly
    state.counter = getattr(state, "counter", 0) + 1
    return state
```

### 6. Fixed Validation Nodes

```python
class ValidationNodeConfig(NodeConfig):
    """Fixed validation node with better engine handling."""

    validation_schema: Type[BaseModel] | str
    error_handler: Callable[[Any, Exception], Any] | None = None
    strict: bool = True

    def create_node(self) -> NodeFunction:
        # Resolve schema from registry if string
        registry = SchemaRegistry.get_instance()

        if isinstance(self.validation_schema, str):
            schema = registry.get_schema(self.validation_schema)
            if not schema:
                raise ValueError(f"Schema {self.validation_schema} not found")
        else:
            schema = self.validation_schema

        def validation_node(state: Any, config: dict | None = None) -> Any:
            try:
                # Validate state against schema
                if hasattr(state, "model_dump"):
                    state_dict = state.model_dump()
                else:
                    state_dict = dict(state)

                validated = schema.model_validate(state_dict)

                # Update state with validated data
                if hasattr(state, "model_copy"):
                    return state.model_copy(update=validated.model_dump())
                else:
                    return {**state, **validated.model_dump()}

            except Exception as e:
                if self.error_handler:
                    return self.error_handler(state, e)
                elif self.strict:
                    raise
                else:
                    # Add error to state
                    error_state = {"validation_error": str(e)}
                    if hasattr(state, "model_copy"):
                        return state.model_copy(update=error_state)
                    else:
                        return {**state, **error_state}

        return validation_node
```

### 7. Auto-Registration

```python
# Auto-register all prebuilt schemas
def register_builtin_schemas():
    registry = SchemaRegistry.get_instance()

    # Engine schemas
    registry.register_schema("llm.input", LLMInputState, "engine")
    registry.register_schema("llm.output", LLMOutputState, "engine")
    registry.register_schema("retriever.input", RetrieverInputState, "engine")
    registry.register_schema("retriever.output", RetrieverOutputState, "engine")
    registry.register_schema("tool.input", ToolInputState, "engine")
    registry.register_schema("tool.output", ToolOutputState, "engine")

    # Sub schemas
    registry.register_schema("messages", MessageHistory, "sub")
    registry.register_schema("documents", DocumentContext, "sub")
    registry.register_schema("query", QueryState, "sub")
    registry.register_schema("errors", ErrorState, "sub")
    registry.register_schema("metadata", MetadataState, "sub")

# Call on module import
register_builtin_schemas()
```

## Usage Examples

### 1. Creating a Custom Agent State

```python
# Compose from prebuilt components
MyAgentState = SchemaComposer.create_agent_state(
    "MyAgentState",
    components=["messages", "query", "documents"],
    additional_fields={
        "custom_field": (str, Field(default=""))
    }
)
```

### 2. Using Engine-Specific States

```python
@callable_node(input_state="llm.input", output_state="llm.output")
def llm_node(state: LLMInputState, config=None) -> LLMOutputState:
    # Type-safe input and output
    response = call_llm(state.prompt)
    return LLMOutputState(response=response, messages=state.messages)
```

### 3. Creating Validation Nodes

```python
validation = ValidationNodeConfig(
    validation_schema="llm.input",
    error_handler=lambda s, e: {**s, "error": str(e)},
    strict=False
)
node = validation.create_node()
```

## Benefits

1. **Registry-based** - All schemas in one place
2. **Prebuilt schemas** - Common patterns ready to use
3. **Composable** - Mix and match sub-schemas
4. **Type-safe** - Preserves type information
5. **Easy callables** - Simple decorator for functions
6. **Engine-specific** - Schemas tailored to engine types
7. **Backwards compatible** - Works with existing nodes
