# Tool Types and Routing Patterns in Haive

## Overview

This guide documents the different tool types in Haive and how they are routed through the agent graph. Understanding tool routing is crucial for building effective agents.

## Tool Types

### 1. LangChain Tools (`langchain_tool`)

Standard LangChain BaseTool implementations that perform actions and return string results.

**Characteristics:**

- Inherit from `BaseTool`
- Return string results
- Can be sync or async
- Support tool descriptions and schemas

**Routing:** `langchain_tool` → `tool_node`

**Example:**

```python
from langchain_core.tools import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information about a topic."""
    # Implementation
    return f"Search results for: {query}"

@tool
async def fetch_data(url: str) -> str:
    """Fetch data from a URL."""
    # Async implementation
    return await fetch(url)
```

### 2. Pydantic Model Tools (`pydantic_model`)

Tools that return structured Pydantic models instead of strings.

**Characteristics:**

- Return Pydantic BaseModel instances
- Provide structured, typed outputs
- Enable complex data structures
- Support validation

**Routing:** `pydantic_model` → `parser_node`

**Example:**

```python
from pydantic import BaseModel
from typing import List

class AnalysisResult(BaseModel):
    summary: str
    confidence: float
    key_points: List[str]
    metadata: dict

def analyze_document(text: str) -> AnalysisResult:
    """Analyze a document and return structured results."""
    return AnalysisResult(
        summary="Document analysis complete",
        confidence=0.92,
        key_points=["Point 1", "Point 2"],
        metadata={"word_count": 500}
    )
```

### 3. Function Tools (`function`)

Simple Python functions that can be called directly.

**Characteristics:**

- Plain Python functions
- Can have any signature
- Often used for calculations or transformations

**Routing:** `function` → `tool_node` (usually)

**Example:**

```python
def calculate_compound_interest(
    principal: float,
    rate: float,
    time: int
) -> float:
    """Calculate compound interest."""
    return principal * (1 + rate) ** time
```

### 4. Engine Tools (`engine`)

Tools that are handled directly by the engine without separate nodes.

**Characteristics:**

- Integrated into the engine's processing
- No separate tool node needed
- Often for simple transformations

**Routing:** `engine` → stays in engine node

**Example:**

```python
# These are typically defined in engine configuration
# and handled internally by the engine
```

## Tool Routing Configuration

### 1. Defining Tool Routes

Tool routes are defined in the engine configuration:

```python
from haive.core.engine.aug_llm import AugLLMConfig

engine = AugLLMConfig(
    name="my_engine",
    tools=[search_web, analyze_document, calculate_compound_interest],
    tool_routes={
        "search_web": "langchain_tool",
        "analyze_document": "pydantic_model",
        "calculate_compound_interest": "function",
    }
)
```

### 2. Automatic Route Detection

If tool routes aren't specified, Haive attempts to detect them:

```python
def detect_tool_type(tool):
    """Automatically detect tool type."""
    if isinstance(tool, BaseTool):
        return "langchain_tool"
    elif hasattr(tool, "__annotations__"):
        # Check if return type is a Pydantic model
        return_type = tool.__annotations__.get("return", None)
        if is_pydantic_model(return_type):
            return "pydantic_model"
    return "function"  # Default
```

### 3. Route Handling in Graph

The agent graph uses routing information to direct tool calls:

```python
def build_graph(self) -> BaseGraph:
    graph = BaseGraph(name=self.name)

    # Check what nodes we need based on tool routes
    tool_routes = self.get_tool_routes()

    # Add tool node for langchain tools
    langchain_tools = [
        tool for tool, route in tool_routes.items()
        if route in ["langchain_tool", "function", "tool_node"]
    ]
    if langchain_tools:
        graph.add_node("tool_node", ToolNodeConfig(...))

    # Add parser node for pydantic tools
    pydantic_tools = [
        tool for tool, route in tool_routes.items()
        if route == "pydantic_model"
    ]
    if pydantic_tools:
        graph.add_node("parse_output", ParserNodeConfigV2(...))
```

## Validation Node and Tool Routing

The ValidationNodeConfigV2 handles intelligent routing based on tool types:

```python
validation_config = ValidationNodeConfigV2(
    name="validation",
    engine_name=self.engine.name,
    tool_node="tool_node",        # For langchain_tool routes
    parser_node="parse_output",    # For pydantic_model routes
    available_nodes=["agent_node", "tool_node", "parse_output"],
)
```

The validation node:

1. Examines the tool calls from the agent
2. Checks the tool_routes to determine routing
3. Sends tool calls to appropriate nodes using Command/Send

## Tool Integration Patterns

### 1. Mixed Tool Types

```python
from langchain_core.tools import tool
from pydantic import BaseModel

# LangChain tool
@tool
def search(query: str) -> str:
    """Search for information."""
    return "search results"

# Pydantic tool
class Analysis(BaseModel):
    score: float
    summary: str

def analyze(text: str) -> Analysis:
    """Analyze text."""
    return Analysis(score=0.9, summary="Good")

# Create agent with mixed tools
agent = SimpleAgent(
    tools=[search, analyze],
    tool_routes={
        "search": "langchain_tool",
        "analyze": "pydantic_model"
    }
)
```

### 2. Force Tool Use Pattern

```python
agent = SimpleAgent(
    tools=[calculator, analyzer],
    force_tool_use=True,  # Always route through validation
    structured_output_model=ResultModel
)
```

### 3. Tool Chaining Pattern

```python
# Tools can call other tools
@tool
def research_and_analyze(topic: str) -> str:
    """Research a topic and analyze findings."""
    # First search
    search_results = search_web(topic)

    # Then analyze (returns pydantic model)
    analysis = analyze_document(search_results)

    # Return formatted string
    return f"Analysis: {analysis.summary} (confidence: {analysis.confidence})"
```

## Advanced Routing Patterns

### 1. Conditional Tool Routing

```python
def has_tool_calls(state) -> bool:
    """Check if the last AI message has tool calls."""
    last_msg = state.messages[-1]
    if isinstance(last_msg, AIMessage):
        return bool(getattr(last_msg, "tool_calls", None))
    return False

# In graph building
graph.add_conditional_edges(
    "agent_node",
    has_tool_calls,
    {True: "validation", False: END}
)
```

### 2. Dynamic Tool Selection

```python
class DynamicToolAgent(SimpleAgent):
    def get_tool_routes(self) -> dict[str, str]:
        """Dynamically determine tool routes based on context."""
        routes = {}
        for tool in self.tools:
            if self.requires_structured_output:
                routes[tool.name] = "pydantic_model"
            else:
                routes[tool.name] = "langchain_tool"
        return routes
```

### 3. Tool Route Override

```python
# Override specific tool routes
agent = SimpleAgent(
    tools=[search, analyze, calculate],
    tool_routes={
        "search": "langchain_tool",
        "analyze": "pydantic_model",
        "calculate": "engine",  # Keep in engine
    }
)
```

## Best Practices

### 1. Choose the Right Tool Type

- Use `langchain_tool` for actions with string results
- Use `pydantic_model` for structured data returns
- Use `function` for simple calculations
- Use `engine` for integrated processing

### 2. Explicit Route Definition

```python
# Be explicit about tool routes
tool_routes = {
    "web_search": "langchain_tool",
    "data_analysis": "pydantic_model",
    "math_calc": "function",
}
```

### 3. Tool Documentation

```python
@tool
def search_knowledge_base(query: str, limit: int = 10) -> str:
    """Search the knowledge base for relevant information.

    Args:
        query: The search query
        limit: Maximum number of results to return

    Returns:
        Formatted search results
    """
    return search_results
```

### 4. Error Handling in Tools

```python
@tool
def safe_calculation(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    try:
        result = eval(expression, {"__builtins__": {}}, safe_math_dict)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: Could not evaluate expression - {str(e)}"
```

## Debugging Tool Routing

### 1. Check Tool Routes

```python
# Debug tool routing
agent = SimpleAgent(...)
print("Tool routes:", agent.get_tool_routes())
print("Available nodes:", agent.graph.metadata.get("available_nodes"))
```

### 2. Trace Tool Execution

```python
# Enable verbose logging
import logging
logging.getLogger("haive.core.graph.node").setLevel(logging.DEBUG)

# Run agent and observe routing
result = await agent.arun("Use the search tool")
```

### 3. Validate Tool Configuration

```python
# Ensure tools are properly configured
for tool in agent.tools:
    print(f"Tool: {tool.name}")
    print(f"  Type: {type(tool)}")
    print(f"  Route: {agent.get_tool_routes().get(tool.name, 'unknown')}")
```

## Summary

Tool routing in Haive provides flexibility in how different types of tools are processed:

- **LangChain tools** go through `tool_node` for execution
- **Pydantic tools** go through `parser_node` for structured output handling
- **Function tools** typically go through `tool_node`
- **Engine tools** stay within the engine

The ValidationNodeConfigV2 intelligently routes tool calls based on their types, ensuring proper handling of results. Understanding these patterns enables building sophisticated agents with mixed tool types and complex workflows.
