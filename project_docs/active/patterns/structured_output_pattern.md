# Structured Output Pattern

**Version**: 1.0  
**Purpose**: Using PydanticToolsParser for structured output in MessagesState  
**Last Updated**: 2025-01-16

## 🎯 Overview

The structured output pattern leverages `PydanticToolsParser` from `langchain_core.output_parsers` to automatically parse AI messages into structured Pydantic models and convert them to tool messages. This is integrated directly into `MessagesState` using field validators.

## 🏗️ Architecture

### Integration Points

1. **MessagesState Fields**:
   - `structured_output_models`: List of Pydantic models to parse
   - `structured_output_parser`: The parser (auto-configured)
   - `parse_structured_outputs`: Enable/disable parsing

2. **Field Validator**:
   - `parse_ai_structured_outputs`: Automatically parses AI messages

3. **PydanticToolsParser**:
   - Converts Pydantic model instances to tool call messages
   - Maintains proper message flow

## 💻 Usage Examples

### Basic Usage

```python
from pydantic import BaseModel, Field
from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import AIMessage

# Define structured output models
class SearchQuery(BaseModel):
    query: str = Field(description="Search query text")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Search filters")
    limit: int = Field(default=10, description="Number of results")

class AnalysisResult(BaseModel):
    summary: str = Field(description="Analysis summary")
    score: float = Field(description="Confidence score")
    recommendations: List[str] = Field(description="List of recommendations")

# Create state with structured output parsing
state = MessagesState(
    structured_output_models=[SearchQuery, AnalysisResult],
    parse_structured_outputs=True
)

# Or enable after creation
state.enable_structured_output_parsing([SearchQuery, AnalysisResult])

# AI message with structured output gets parsed automatically
ai_msg = AIMessage(
    content='{"query": "python tutorials", "filters": {"level": "beginner"}, "limit": 20}'
)
state.messages.append(ai_msg)

# The field validator automatically creates a ToolMessage
# Check parsed output
latest_tool = state.get_latest_structured_output()
print(f"Parsed tool: {latest_tool.name}")  # "SearchQuery"
print(f"Content: {latest_tool.content}")   # JSON of the parsed model
```

### With Agents

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent with structured output state
agent = SimpleAgent(
    name="search_agent",
    engine=AugLLMConfig(
        system_message="You are a search assistant. Always respond with SearchQuery format."
    ),
    state_schema=MessagesState
)

# Configure state for structured output
agent.state_schema = MessagesState(
    structured_output_models=[SearchQuery],
    parse_structured_outputs=True
)

# Run agent - output will be automatically parsed
result = await agent.arun("Find Python tutorials for beginners")

# Get the parsed structured output
state = agent.get_state()
parsed_output = state.get_latest_structured_output()
```

### Token Tracking Integration

```python
from haive.core.schema.prebuilt.messages.messages_with_token_usage import MessagesStateWithTokenUsage

# Works with token tracking too
state = MessagesStateWithTokenUsage(
    structured_output_models=[SearchQuery, AnalysisResult],
    parse_structured_outputs=True
)

# Add AI message with token usage
ai_msg = AIMessage(
    content='{"query": "AI news", "limit": 5}',
    response_metadata={"token_usage": {"total_tokens": 50}}
)
state.messages.append(ai_msg)

# Both token tracking and structured output parsing work
print(f"Tokens used: {state.token_usage['total_tokens']}")
print(f"Parsed output: {state.get_latest_structured_output()}")
```

## 🔧 How It Works

### 1. Setup Phase

```python
@model_validator(mode="before")
def setup_structured_output_parser(cls, data: Any) -> Any:
    """Auto-configure PydanticToolsParser if models provided."""
    if (data.get("structured_output_models") and
        not data.get("structured_output_parser") and
        data.get("parse_structured_outputs", False)):

        # Use PydanticToolsParser to convert models to tool calls
        data["structured_output_parser"] = PydanticToolsParser(
            tools=data["structured_output_models"]
        )
    return data
```

### 2. Parsing Phase

```python
@field_validator("messages", mode="after")
def parse_ai_structured_outputs(cls, messages: List[AnyMessage], info) -> List[AnyMessage]:
    """Parse AI messages with structured output."""
    enhanced_messages = []

    for msg in messages:
        enhanced_messages.append(msg)

        # Only process AI messages
        if isinstance(msg, AIMessage) and msg.content:
            try:
                # Parse with PydanticToolsParser
                parsed_tools = parser.parse(msg.content)

                # Create tool messages
                for tool_instance in parsed_tools:
                    tool_msg = ToolMessage(
                        content=tool_instance.json(),
                        tool_call_id=f"parse_{id(msg)}_{idx}",
                        name=tool_instance.__class__.__name__
                    )
                    enhanced_messages.append(tool_msg)
            except:
                pass  # Keep original on parse failure

    return enhanced_messages
```

## 🎨 Advanced Patterns

### Multiple Output Types

```python
# Define multiple output types
class WebSearch(BaseModel):
    query: str
    engine: Literal["google", "bing", "duckduckgo"] = "google"

class ImageGeneration(BaseModel):
    prompt: str
    style: str = "realistic"
    size: Literal["256x256", "512x512", "1024x1024"] = "512x512"

class DataAnalysis(BaseModel):
    dataset: str
    metrics: List[str]
    visualization: bool = True

# Enable all types
state.enable_structured_output_parsing([
    WebSearch,
    ImageGeneration,
    DataAnalysis
])

# AI can respond with any of these formats
```

### Custom Parser

```python
from langchain_core.output_parsers import PydanticOutputParser

# Use different parser for different behavior
single_model_parser = PydanticOutputParser(pydantic_object=SearchQuery)

state = MessagesState(
    structured_output_models=[SearchQuery],
    structured_output_parser=single_model_parser,  # Custom parser
    parse_structured_outputs=True
)
```

### Conditional Parsing

```python
class ConditionalState(MessagesState):
    """State that only parses certain messages."""

    @field_validator("messages", mode="after")
    @classmethod
    def conditional_parse(cls, messages: List[AnyMessage], info) -> List[AnyMessage]:
        """Only parse if message contains special marker."""
        enhanced = []

        for msg in messages:
            enhanced.append(msg)

            # Only parse if message has structured output marker
            if (isinstance(msg, AIMessage) and
                msg.content and
                "STRUCTURED_OUTPUT:" in msg.content):

                # Parse the part after the marker
                content = msg.content.split("STRUCTURED_OUTPUT:")[1].strip()
                # ... parsing logic

        return enhanced
```

## 🚀 Integration with Agents

### SimpleAgent with Structured Output

```python
# Create agent that always outputs structured data
search_agent = SimpleAgent(
    name="search_assistant",
    engine=AugLLMConfig(
        system_message="""You are a search assistant.
        Always respond with a SearchQuery JSON object containing:
        - query: the search query
        - filters: any filters as a dictionary
        - limit: number of results (default 10)
        """
    )
)

# Configure state
search_agent.state_schema = MessagesState(
    structured_output_models=[SearchQuery],
    parse_structured_outputs=True
)
```

### ReactAgent with Tools

```python
# ReactAgent can use both regular tools AND structured outputs
react_agent = ReactAgent(
    name="research_agent",
    tools=[web_search_tool, calculator_tool],
    engine=AugLLMConfig()
)

# Add structured output capability
react_agent.state_schema = MessagesState(
    structured_output_models=[AnalysisResult, SearchQuery],
    parse_structured_outputs=True
)

# Agent can now:
# 1. Use tools normally
# 2. Output structured data that gets parsed to tool messages
```

## 🎯 Best Practices

### 1. Clear Model Definitions

```python
# ✅ GOOD - Clear, well-documented models
class TaskResult(BaseModel):
    """Result of task execution."""
    task_id: str = Field(description="Unique task identifier")
    status: Literal["success", "failed", "pending"] = Field(description="Task status")
    result: Optional[Any] = Field(default=None, description="Task result if successful")
    error: Optional[str] = Field(default=None, description="Error message if failed")

# ❌ BAD - Vague models
class Result(BaseModel):
    data: Any
    status: str
```

### 2. Prompt Engineering

```python
# ✅ GOOD - Clear instructions for structured output
system_prompt = f"""You are an assistant that analyzes text.
Always respond with a JSON object matching the AnalysisResult schema:
{state.format_for_structured_output()}
"""

# ❌ BAD - No guidance on output format
system_prompt = "You are an analysis assistant."
```

### 3. Error Handling

```python
# ✅ GOOD - Handle parse failures gracefully
try:
    parsed = state.get_latest_structured_output()
    if parsed:
        # Process structured output
        process_result(parsed)
    else:
        # Fallback for non-structured response
        handle_text_response(state.get_last_ai_message())
except Exception as e:
    logger.warning(f"Structured output parsing failed: {e}")
```

## 🚨 Common Pitfalls

### 1. Forgetting to Enable Parsing

```python
# ❌ WRONG - Models defined but parsing not enabled
state = MessagesState(
    structured_output_models=[SearchQuery]
    # Missing: parse_structured_outputs=True
)

# ✅ CORRECT
state = MessagesState(
    structured_output_models=[SearchQuery],
    parse_structured_outputs=True
)
```

### 2. Incompatible Output Format

```python
# ❌ WRONG - AI outputs plain text
ai_msg = AIMessage(content="Search for Python tutorials")

# ✅ CORRECT - AI outputs JSON matching model
ai_msg = AIMessage(content='{"query": "Python tutorials", "limit": 10}')
```

### 3. Missing Field Validation

```python
# ❌ WRONG - No validation
class Query(BaseModel):
    text: str
    count: int

# ✅ CORRECT - Proper validation
class Query(BaseModel):
    text: str = Field(min_length=1, max_length=1000)
    count: int = Field(ge=1, le=100)
```

## 📊 Performance Considerations

1. **Parsing Overhead**: Field validator runs on every message update
2. **Memory Usage**: Tool messages are added to conversation
3. **Token Usage**: Structured outputs may use more tokens

## 🔗 Related Documentation

- [MessagesState Documentation](../haive-core/schema/messages_state.md)
- [LangChain Output Parsers](https://python.langchain.com/docs/modules/model_io/output_parsers/)
- [PydanticToolsParser Reference](https://api.python.langchain.com/en/latest/output_parsers/langchain_core.output_parsers.openai_tools.PydanticToolsParser.html)

## 📝 Summary

The structured output pattern provides:

1. **Automatic Parsing**: AI messages parsed to Pydantic models
2. **Tool Message Integration**: Models converted to tool messages
3. **Type Safety**: Full Pydantic validation
4. **Token Tracking**: Works with MessagesStateWithTokenUsage
5. **Flexibility**: Multiple models, custom parsers

It's integrated at the state schema level, making it available to all agents automatically.

---

**Quick Start**:

```python
state = MessagesState(
    structured_output_models=[YourModel],
    parse_structured_outputs=True
)
```
