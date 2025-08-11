# LangGraph Tool Calling Patterns

**Reference**: @https://langchain-ai.github.io/langgraph/how-tos/tool-calling/  
**Topic**: Comprehensive guide to tool calling patterns in LangGraph  
**Research Date**: 2025-08-08

## Core Tool Concepts

### Basic Tool Definition

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b
```

Key aspects:

- Tools are callable functions with input schemas
- Use `@tool` decorator for automatic schema generation
- Type hints and docstrings define tool behavior
- Can be passed to chat models for automatic invocation

## Tool Calling Patterns

### 1. Direct Tool Invocation

```python
# Method 1: Direct invoke
result = multiply.invoke({"a": 3, "b": 4})

# Method 2: Tool call dictionary
tool_call = {
    "name": "multiply",
    "args": {"a": 3, "b": 4},
    "id": "call_123"
}
result = multiply.invoke(tool_call)

# Returns ToolMessage object
```

### 2. Agent-Based Tool Calling

```python
from langgraph.prebuilt import create_react_agent

# Create agent with tools
agent = create_react_agent(model, tools=[multiply])

# Agent dynamically selects tools
result = agent.invoke({"messages": [("user", "What is 3 times 4?")]})
```

### 3. Context Management Strategies

#### Configuration Access (Immutable Runtime Data)

```python
@tool
def get_user_info(config: RunnableConfig) -> str:
    """Get user information from config"""
    user_id = config["configurable"].get("user_id")
    return f"User: {user_id}" if user_id else "Unknown user"

# Usage with config
result = agent.invoke(
    {"messages": [("user", "Who am I?")]},
    config={"configurable": {"user_id": "12345"}}
)
```

#### Short-term Memory (InjectedState)

```python
from langgraph.prebuilt import InjectedState
from typing import Annotated

@tool
def get_user_name(state: Annotated[dict, InjectedState]) -> str:
    """Get user name from current state"""
    return state.get("user_name", "Unknown user")

# State automatically injected during execution
```

#### Long-term Memory (Persistent Storage)

```python
@tool
def remember_preference(preference: str, config: RunnableConfig) -> str:
    """Store user preference persistently"""
    user_id = config["configurable"]["user_id"]
    # Store in database/file system
    save_user_preference(user_id, preference)
    return f"Remembered: {preference}"
```

## Advanced Tool Features

### 1. Immediate Return (`return_direct=True`)

```python
@tool(return_direct=True)
def get_weather(location: str) -> str:
    """Get weather - returns immediately without LLM processing"""
    return f"Weather in {location}: Sunny, 72°F"
```

### 2. Force Tool Usage (`tool_choice`)

```python
# Force specific tool usage
response = model.invoke(
    messages,
    tool_choice="multiply"  # Must use multiply tool
)
```

### 3. Error Handling with ToolNode

```python
from langgraph.prebuilt import ToolNode

# Handles tool execution and error management
tool_node = ToolNode([multiply, calculator])

# Automatically processes tool calls from agent
```

### 4. Parallel Tool Calls

```python
# LLM can call multiple tools simultaneously
response = agent.invoke({
    "messages": [("user", "Calculate 3*4 and 5*6")]
})
# May trigger parallel tool calls
```

## Context Access Patterns

### Pattern 1: Configuration for Static Data

Use for:

- User IDs, session data
- API keys, connection strings
- Immutable runtime configuration

```python
@tool
def api_call(endpoint: str, config: RunnableConfig) -> str:
    """Make API call with configured credentials"""
    api_key = config["configurable"]["api_key"]
    return make_request(endpoint, api_key)
```

### Pattern 2: InjectedState for Dynamic Data

Use for:

- Current conversation state
- Temporary workflow data
- Dynamic context that changes

```python
@tool
def analyze_conversation(
    topic: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Analyze conversation about topic"""
    messages = state.get("messages", [])
    return analyze_topic_in_messages(topic, messages)
```

### Pattern 3: Long-term Memory for Persistence

Use for:

- User preferences and history
- Learned facts and relationships
- Cross-session data

```python
@tool
def recall_fact(query: str, config: RunnableConfig) -> str:
    """Recall stored facts"""
    user_id = config["configurable"]["user_id"]
    facts = load_user_facts(user_id)
    return search_facts(facts, query)
```

## Tool Design Best Practices

### 1. Clear Tool Interfaces

```python
@tool
def search_documents(
    query: str,
    max_results: int = 5,
    state: Annotated[dict, InjectedState]
) -> list[str]:
    """
    Search user's documents with automatic context.

    Args:
        query: Search terms
        max_results: Maximum number of results to return
        state: Automatically injected current state
    """
    user_prefs = state.get("search_preferences", {})
    return perform_search(query, max_results, user_prefs)
```

### 2. Error Handling

```python
@tool
def safe_calculation(expression: str) -> str:
    """Safely evaluate mathematical expressions"""
    try:
        # Validate and evaluate safely
        result = safe_eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
```

### 3. Type Safety and Validation

```python
from pydantic import BaseModel, Field

class SearchParams(BaseModel):
    query: str = Field(description="Search query")
    filters: dict = Field(default_factory=dict, description="Search filters")

@tool(args_schema=SearchParams)
def advanced_search(params: SearchParams) -> dict:
    """Advanced search with structured parameters"""
    return perform_search(params.query, params.filters)
```

## Integration with Haive Patterns

### 1. Agent Tool Integration

```python
# Haive agent with LangGraph tools
agent = ReactAgent(
    name="research_agent",
    engine=AugLLMConfig(),
    tools=[search_documents, analyze_conversation, recall_fact]
)
```

### 2. State-Aware Tools

```python
@tool
def update_agent_memory(
    memory_item: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Update agent's working memory"""
    current_memory = state.get("agent_memory", [])
    current_memory.append(memory_item)
    state["agent_memory"] = current_memory
    return f"Added to memory: {memory_item}"
```

### 3. Multi-Agent Tool Coordination

```python
@tool
def coordinate_agents(
    task_description: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Coordinate between multiple agents"""
    available_agents = state.get("available_agents", {})
    best_agent = select_best_agent(task_description, available_agents)
    return delegate_task(best_agent, task_description)
```

## Performance Considerations

### 1. Async Tools

```python
import asyncio

@tool
async def async_web_search(query: str) -> str:
    """Asynchronous web search"""
    results = await async_search_api(query)
    return format_results(results)
```

### 2. Caching Results

```python
from functools import lru_cache

@tool
def cached_lookup(key: str) -> str:
    """Lookup with caching"""
    return _cached_lookup_impl(key)

@lru_cache(maxsize=100)
def _cached_lookup_impl(key: str) -> str:
    return expensive_lookup(key)
```

## Summary

LangGraph tool calling provides:

- Flexible tool definition and invocation patterns
- Rich context management (config, state, memory)
- Advanced features (parallel calls, error handling, immediate return)
- Clean integration with agent workflows
- Strong typing and validation support

Key principles:

- Use appropriate context pattern for your data type
- Design clean, focused tool interfaces
- Handle errors gracefully
- Leverage type hints and documentation
- Consider performance and caching needs

## Tags

`#langgraph` `#tool-calling` `#context-management` `#agent-tools` `#injected-state` `#configuration` `#async-tools`
