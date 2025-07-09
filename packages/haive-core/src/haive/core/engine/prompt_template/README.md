# PromptTemplateEngine

A sophisticated engine that wraps LangChain prompt templates as first-class InvokableEngines with automatic schema derivation and robust formatting capabilities.

## Overview

The PromptTemplateEngine bridges the gap between LangChain's prompt template system and Haive's engine architecture, enabling prompt templates to be treated as composable, schema-aware components within complex agent workflows.

## Key Features

- **Automatic Schema Derivation**: Input schemas are automatically generated from prompt template variables
- **Smart Type Inference**: Intelligent type detection for common patterns (messages, lists, context, etc.)
- **Enhanced Variable Detection**: Extracts variables from message content using advanced regex parsing
- **Robust Formatting**: Uses LangChain's PromptValue system for reliable template formatting
- **Template Support**: Works with both text templates and complex chat templates
- **Engine Integration**: Seamless composition with other Haive engines

## Quick Start

### Basic Text Template

```python
from langchain_core.prompts import PromptTemplate
from haive.core.engine.prompt_template import PromptTemplateEngine

# Create a simple prompt template
template = PromptTemplate.from_template(
    "Question: {question}\nContext: {context}\nAnswer:"
)

# Wrap as an engine
engine = PromptTemplateEngine(
    name="qa_prompt",
    prompt_template=template
)

# Auto-derived schema includes 'question' and 'context' fields
schema = engine.derive_input_schema()
print(schema.model_fields.keys())  # dict_keys(['question', 'context'])

# Use the engine
result = engine.invoke({
    "question": "What is Python?",
    "context": "Python is a programming language"
})
print(result)  # "Question: What is Python?\nContext: Python is a programming language\nAnswer:"
```

### Chat Template with Messages

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Create a chat template with messages placeholder
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    MessagesPlaceholder(variable_name="chat_history", optional=True),
    ("human", "Question: {question}")
])

# Wrap as an engine
engine = PromptTemplateEngine(
    name="chat_prompt",
    prompt_template=chat_template
)

# Schema includes both 'question' and 'chat_history' fields
schema = engine.derive_input_schema()

# Format with messages
result = engine.invoke({
    "question": "How are you?",
    "chat_history": []  # Optional
})
# Returns List[AnyMessage] with formatted messages
```

## Advanced Usage

### Custom Input Schema

```python
from pydantic import BaseModel, Field

class CustomInput(BaseModel):
    query: str = Field(description="User query")
    max_length: int = Field(default=100, description="Maximum response length")

engine = PromptTemplateEngine(
    name="custom_prompt",
    prompt_template=template,
    custom_input_schema=CustomInput
)
```

### Type Inference Examples

The engine automatically infers types based on variable name patterns:

- **Messages**: Variables named `messages`, `chat_history`, `conversation` → `List[AnyMessage]`
- **Lists**: Variables with `list`, `items`, `examples`, `docs` → `List[str]`
- **Context**: Variables named `context`, `background`, `info` → `str`
- **Queries**: Variables named `question`, `query`, `prompt` → `str`

## Schema Derivation Process

1. **Variable Detection**: Uses LangChain's built-in `input_variables` and `optional_variables`
2. **Enhanced Parsing**: Regex extraction from message content for chat templates
3. **Type Inference**: Smart type assignment based on variable name patterns
4. **Schema Generation**: Creates Pydantic BaseModel with inferred types
5. **Validation**: Automatic input validation against derived schema

## Engine Integration

The PromptTemplateEngine implements the full InvokableEngine interface:

```python
# Required methods
engine.derive_input_schema()   # Auto-generated schema
engine.derive_output_schema()  # Based on template type
engine.invoke(input_data)      # Format with validation
engine.get_input_fields()      # Field information
engine.get_output_fields()     # Output field information
engine.create_runnable()       # LangChain runnable conversion
```

## Output Types

The output type depends on the prompt template:

- **ChatPromptTemplate** → `List[AnyMessage]`
- **FewShotChatMessagePromptTemplate** → `List[AnyMessage]`
- **PromptTemplate** → `str`
- **FewShotPromptTemplate** → `str`

## Error Handling

The engine includes robust error handling:

- **Graceful Fallbacks**: Falls back to direct formatting if PromptValue fails
- **Validation Errors**: Clear error messages for invalid input data
- **Missing Variables**: Helpful feedback for required variables

## Performance Considerations

- **Lazy Schema Generation**: Schemas are created only when first accessed
- **Caching**: Template engines are cached to avoid recreation
- **Efficient Formatting**: Uses LangChain's optimized formatting pipeline

## Integration with AugLLMConfig

The PromptTemplateEngine is designed to work seamlessly with AugLLMConfig via the PromptTemplateMixin:

```python
from haive.core.engine.aug_llm.config import AugLLMConfig

config = AugLLMConfig(prompt_template=chat_template)
schema = config.derive_input_schema()  # Includes prompt variables + messages
```

## Best Practices

1. **Variable Naming**: Use descriptive names that match type inference patterns
2. **Optional Variables**: Use MessagesPlaceholder with `optional=True` for flexible schemas
3. **Validation**: Always validate input data against derived schemas
4. **Error Handling**: Implement proper error handling for formatting operations
5. **Testing**: Test with various input combinations to ensure robustness

## API Reference

See the inline documentation in `prompt_engine.py` for complete API details including all methods, parameters, and return types.
