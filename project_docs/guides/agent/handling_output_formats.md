# Handling Various Output Formats in Haive Agents

**Version**: 1.0
**Purpose**: Comprehensive guide for handling different output formats in agent workflows
**Last Updated**: 2025-01-18

## 🎯 Overview

Haive agents can produce outputs in various formats: strings, AIMessages, ToolMessages, dictionaries, and more. This guide shows how to handle all these formats gracefully, especially when converting to structured outputs.

## 📋 Output Format Types

### 1. String Output

The simplest format - plain text responses.

```python
# Simple string output
output = "The analysis shows positive trends with 15% growth."
```

### 2. AIMessage Output

LangChain message objects with content and metadata.

```python
from langchain_core.messages import AIMessage

# AIMessage with content
output = AIMessage(content="The analysis shows positive trends.")

# AIMessage with tool calls
output = AIMessage(
    content="",
    tool_calls=[{
        "name": "AnalysisResult",
        "args": {
            "summary": "Positive trends",
            "growth_rate": 0.15
        }
    }]
)
```

### 3. ToolMessage Output

Messages from tool executions.

```python
from langchain_core.messages import ToolMessage

output = ToolMessage(
    content='{"result": "Analysis complete"}',
    tool_call_id="call_123",
    name="analyzer_tool"
)
```

### 4. Dictionary Output

Common in custom agents and API responses.

```python
# Simple dict
output = {
    "output": "Analysis complete",
    "confidence": 0.95
}

# Nested dict
output = {
    "result": {
        "summary": "Positive trends",
        "metrics": {"growth": 0.15}
    }
}
```

### 5. BaseModel Output

Already structured Pydantic models.

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    summary: str
    confidence: float

output = AnalysisResult(
    summary="Positive trends",
    confidence=0.95
)
```

## 🔧 Handling Strategies

### 1. Using ensure_structured_output()

The `ensure_structured_output()` method on agents handles all formats:

```python
from haive.agents.simple import SimpleAgent
from pydantic import BaseModel, Field

class ResultModel(BaseModel):
    summary: str
    confidence: float = Field(ge=0.0, le=1.0)

agent = SimpleAgent(name="analyzer", engine=config)

# Handle various outputs
outputs = [
    "Summary: positive trends, high confidence",
    AIMessage(content="Very positive outlook"),
    {"output": "Good results", "confidence": 0.9},
    ToolMessage(content='{"summary": "Great"}', tool_call_id="1")
]

for output in outputs:
    structured = agent.ensure_structured_output(
        output,
        ResultModel,
        handle_errors=True
    )
    if structured:
        print(f"✅ Converted: {structured}")
```

### 2. In MessagesState

MessagesState provides built-in parsing for structured outputs:

```python
from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.output_parsers import PydanticToolsParser

# Enable structured output parsing
state = MessagesState()
state.enable_structured_output_parsing(
    models=[ResultModel],
    parser=PydanticToolsParser(tools=[ResultModel])
)

# AI messages are automatically parsed
state.add_message(AIMessage(
    content="",
    tool_calls=[{
        "name": "ResultModel",
        "args": {"summary": "Good", "confidence": 0.8}
    }]
))

# Get parsed result
parsed = state.get_latest_structured_output()
```

### 3. Multi-Agent Pattern

Sequential agent pattern for structured conversion:

```python
# Any agent produces output
analyzer = ReactAgent(name="analyzer", tools=[data_tool])

# Structured output agent converts it
structurer = StructuredOutputAgent(
    name="structurer",
    output_model=ResultModel
)

# In workflow
result = analyzer.run("Analyze the data")
structured = structurer.run(result)  # Handles any format
```

## 💡 Best Practices

### 1. Always Use Tool-Based Extraction

```python
# ✅ CORRECT - Tool-based (v2)
agent = StructuredOutputAgent(
    output_model=MyModel,
    structured_output_version="v2"  # Default
)

# ❌ AVOID - Parser-based (v1)
# Less reliable, especially with complex models
```

### 2. Handle Tool Calls Explicitly

```python
def extract_from_message(msg: AIMessage, model: Type[BaseModel]):
    """Extract structured data from AIMessage."""

    # Check tool calls first
    if hasattr(msg, 'tool_calls') and msg.tool_calls:
        parser = PydanticToolsParser(tools=[model])
        parsed = parser.parse(msg)
        if parsed:
            return parsed[0]

    # Fall back to content
    if msg.content:
        return convert_text_to_model(msg.content, model)

    return None
```

### 3. Graceful Fallbacks

```python
def get_structured_output(output: Any, model: Type[BaseModel]):
    """Convert any output to structured format with fallbacks."""

    try:
        # Already the right type?
        if isinstance(output, model):
            return output

        # Try direct construction
        if isinstance(output, dict):
            try:
                return model(**output)
            except:
                pass

        # Use StructuredOutputAgent as fallback
        structurer = StructuredOutputAgent(
            name="fallback_structurer",
            output_model=model
        )
        return structurer.run(output)

    except Exception as e:
        # Log error and return None
        logger.error(f"Failed to structure output: {e}")
        return None
```

## 🔄 Format Conversion Patterns

### String to Structured

```python
text = "Revenue: $1M, Growth: 15%, Customers: 1000"

class Metrics(BaseModel):
    revenue: str
    growth_percentage: float
    customer_count: int

# Using StructuredOutputAgent
structurer = StructuredOutputAgent(output_model=Metrics)
result = structurer.run(text)
# Result: Metrics(revenue="$1M", growth_percentage=15.0, customer_count=1000)
```

### AIMessage to Structured

```python
# With tool calls
msg = AIMessage(
    content="",
    tool_calls=[{
        "name": "Metrics",
        "args": {
            "revenue": "$1M",
            "growth_percentage": 15.0,
            "customer_count": 1000
        }
    }]
)

# Parse tool calls
parser = PydanticToolsParser(tools=[Metrics])
result = parser.parse(msg)[0]
```

### Dict to Structured

```python
data = {
    "output": {
        "revenue": "$1M",
        "metrics": {
            "growth": 0.15,
            "customers": 1000
        }
    }
}

# Flatten and convert
flat_data = {
    "revenue": data["output"]["revenue"],
    "growth_percentage": data["output"]["metrics"]["growth"] * 100,
    "customer_count": data["output"]["metrics"]["customers"]
}
result = Metrics(**flat_data)
```

## 🚀 Advanced Patterns

### 1. Format Detection

```python
def detect_output_format(output: Any) -> str:
    """Detect the format of agent output."""

    if isinstance(output, str):
        return "string"
    elif isinstance(output, BaseModel):
        return "pydantic"
    elif isinstance(output, AIMessage):
        if hasattr(output, 'tool_calls') and output.tool_calls:
            return "ai_message_with_tools"
        return "ai_message"
    elif isinstance(output, ToolMessage):
        return "tool_message"
    elif isinstance(output, dict):
        return "dictionary"
    elif isinstance(output, list):
        return "list"
    else:
        return "unknown"
```

### 2. Universal Converter

```python
class UniversalOutputConverter:
    """Convert any output format to structured data."""

    def __init__(self, target_model: Type[BaseModel]):
        self.target_model = target_model
        self.structurer = StructuredOutputAgent(
            output_model=target_model,
            name="universal_converter"
        )

    def convert(self, output: Any) -> Optional[BaseModel]:
        """Convert output to target model."""

        # Already correct type
        if isinstance(output, self.target_model):
            return output

        # Extract content based on type
        content = self._extract_content(output)

        if content:
            return self.structurer.run(content)

        return None

    def _extract_content(self, output: Any) -> Optional[str]:
        """Extract string content from any format."""

        if isinstance(output, str):
            return output

        elif isinstance(output, BaseMessage):
            # Handle tool calls
            if hasattr(output, 'tool_calls') and output.tool_calls:
                return json.dumps(output.tool_calls[0]["args"])
            return output.content

        elif isinstance(output, dict):
            # Try common keys
            for key in ['output', 'content', 'result', 'text']:
                if key in output:
                    return str(output[key])
            return json.dumps(output)

        elif isinstance(output, list):
            # Handle list of messages
            if output and isinstance(output[0], BaseMessage):
                return self._extract_content(output[-1])
            return str(output)

        else:
            return str(output)
```

### 3. Batch Processing

```python
def batch_convert_outputs(
    outputs: List[Any],
    model: Type[BaseModel],
    parallel: bool = True
) -> List[Optional[BaseModel]]:
    """Convert multiple outputs to structured format."""

    if parallel:
        import asyncio
        from concurrent.futures import ThreadPoolExecutor

        with ThreadPoolExecutor() as executor:
            futures = []
            for output in outputs:
                future = executor.submit(
                    ensure_structured_output,
                    output, model
                )
                futures.append(future)

            results = [f.result() for f in futures]
    else:
        results = [
            ensure_structured_output(output, model)
            for output in outputs
        ]

    return results
```

## 📊 Format Comparison Table

| Format      | Pros                 | Cons                  | Best For               |
| ----------- | -------------------- | --------------------- | ---------------------- |
| String      | Simple, universal    | No structure          | Human-readable outputs |
| AIMessage   | LangChain native     | Complex structure     | Agent communication    |
| ToolMessage | Clear tool results   | Requires tool context | Tool-based workflows   |
| Dict        | Flexible             | No validation         | API responses          |
| BaseModel   | Type-safe, validated | Requires schema       | Structured workflows   |

## 🎯 Choosing the Right Approach

### Use String When:

- Output is primarily for human consumption
- Structure is not critical
- Maximum compatibility needed

### Use AIMessage When:

- Working within LangChain ecosystem
- Need to preserve conversation context
- Using tool calls for structured data

### Use Dict When:

- Interfacing with external APIs
- Need flexible, dynamic structure
- Performance is critical

### Use BaseModel When:

- Type safety is required
- Validation is important
- Building robust production systems

## 🔗 Integration Examples

### With State Management

```python
class WorkflowState(MessagesState):
    # Structured fields auto-populated
    summary: str = ""
    confidence: float = 0.0
    recommendations: List[str] = Field(default_factory=list)

# Agent outputs unstructured
agent = SimpleAgent(name="analyzer")
result = agent.run("Analyze this")

# Structurer populates state fields
structurer = StructuredOutputAgent(
    output_model=AnalysisResult,
    name="structurer"
)
# State fields are automatically updated
```

### With Tool Calls

```python
@tool
def process_data(data: AnalysisResult) -> str:
    """Process structured analysis data."""
    return f"Processed with {data.confidence} confidence"

# Agent with structured tool
agent = ReactAgent(
    name="processor",
    tools=[process_data]
)

# Tool receives typed data automatically
```

## 🚨 Common Pitfalls

### 1. Not Handling Tool Calls

```python
# ❌ WRONG - Ignores tool calls
if isinstance(msg, AIMessage):
    return msg.content  # Might be empty!

# ✅ CORRECT - Check tool calls first
if isinstance(msg, AIMessage):
    if msg.tool_calls:
        return parse_tool_calls(msg.tool_calls)
    return msg.content
```

### 2. Assuming Format

```python
# ❌ WRONG - Assumes dict structure
result = output["data"]["summary"]

# ✅ CORRECT - Safe extraction
result = output.get("data", {}).get("summary", "")
```

### 3. No Error Handling

```python
# ❌ WRONG - Will crash on bad data
structured = MyModel(**output)

# ✅ CORRECT - Graceful handling
try:
    structured = MyModel(**output)
except Exception as e:
    logger.error(f"Structuring failed: {e}")
    structured = None
```

## 📚 Further Reading

- [StructuredOutputAgent Guide](structured_output_agent.md)
- [MessagesState Documentation](../../active/architecture/messages_state.md)
- [Multi-Agent Patterns](multi/README.md)
- [Agent Building Guide](building_guide.md)

---

**Remember**: Always use tool-based extraction (v2) and handle errors gracefully. The goal is to make your agents robust to any output format they might encounter.
