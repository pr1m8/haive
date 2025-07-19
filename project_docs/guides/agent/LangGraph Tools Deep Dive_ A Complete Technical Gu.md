<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# LangGraph Tools Deep Dive: A Complete Technical Guide

This comprehensive guide explores the various approaches to creating and using tools in LangGraph, from basic `@tool` decorators to advanced structured tools with state injection and validation.

## Table of Contents

1. [Tool Creation Methods](#tool-creation-methods)
2. [StructuredTool vs @tool Decorator](#structuredtool-vs-tool-decorator)
3. [ToolNode Implementation](#toolnode-implementation)
4. [BaseModel as Tool Schema](#basemodel-as-tool-schema)
5. [State Injection Patterns](#state-injection-patterns)
6. [Tool Validation and Error Handling](#tool-validation-and-error-handling)
7. [Advanced Tool Patterns](#advanced-tool-patterns)
8. [Best Practices and Optimization](#best-practices-and-optimization)

## Tool Creation Methods

### 1. @tool Decorator (Recommended)

The `@tool` decorator is the simplest and most commonly used method for creating tools in LangGraph[^1]. It automatically infers the tool's name, description, and arguments from the function signature and docstring.

```python
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# Tool attributes are automatically generated
print(multiply.name)        # "multiply"
print(multiply.description) # "Multiply two numbers."
print(multiply.args)        # JSON schema for arguments
```

**Key Benefits:**

- Automatic schema generation
- Minimal boilerplate code
- Type hints automatically converted to JSON schema
- Docstring becomes tool description

### 2. StructuredTool Class

For more complex scenarios requiring custom validation or async operations, `StructuredTool` provides greater control[^2][^3].

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="Search query")
    limit: int = Field(default=10, description="Number of results")

def search_function(query: str, limit: int) -> str:
    """Search for information."""
    return f"Found {limit} results for: {query}"

search_tool = StructuredTool.from_function(
    func=search_function,
    name="search",
    description="Search for information",
    args_schema=SearchInput,
    return_direct=False
)
```

### 3. Custom BaseTool Subclass

For maximum flexibility, inherit from `BaseTool` and implement custom `_run` and `_arun` methods:

```python
from langchain_core.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class WeatherInput(BaseModel):
    location: str = Field(description="City or location name")

class WeatherTool(BaseTool):
    name = "get_weather"
    description = "Get current weather for a location"
    args_schema: Type[BaseModel] = WeatherInput

    def _run(self, location: str) -> str:
        """Synchronous implementation."""
        return f"Weather in {location}: 72°F, sunny"

    async def _arun(self, location: str) -> str:
        """Asynchronous implementation."""
        return f"Weather in {location}: 72°F, sunny"

weather_tool = WeatherTool()
```

## StructuredTool vs @tool Decorator

### When to Use @tool Decorator

**Best for:**

- Simple, stateless functions
- Quick prototyping
- Standard parameter types
- Minimal validation requirements

```python
@tool
def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates."""
    import math

    # Haversine formula
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c  # Earth's radius in kilometers
```

### When to Use StructuredTool

**Best for:**

- Complex validation logic
- Custom error handling
- Async operations
- Response formatting requirements

```python
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any

class DatabaseQueryInput(BaseModel):
    table: str = Field(description="Database table name")
    columns: List[str] = Field(description="Columns to select")
    conditions: Dict[str, Any] = Field(default={}, description="WHERE conditions")

    @validator('table')
    def validate_table(cls, v):
        allowed_tables = ['users', 'orders', 'products']
        if v not in allowed_tables:
            raise ValueError(f"Table must be one of {allowed_tables}")
        return v

def execute_query(table: str, columns: List[str], conditions: Dict[str, Any]) -> str:
    """Execute a database query with validation."""
    # Simulated database query
    query = f"SELECT {', '.join(columns)} FROM {table}"
    if conditions:
        where_clause = " AND ".join([f"{k} = '{v}'" for k, v in conditions.items()])
        query += f" WHERE {where_clause}"

    return f"Query executed: {query}"

db_tool = StructuredTool.from_function(
    func=execute_query,
    name="database_query",
    description="Execute safe database queries",
    args_schema=DatabaseQueryInput,
    handle_tool_error=True
)
```

## ToolNode Implementation

`ToolNode` is a specialized LangGraph node that executes tools and manages the tool-calling workflow[^4][^5].

### Basic ToolNode Usage

```python
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Get weather for a location."""
    return f"Weather in {location}: 72°F, sunny"

@tool
def get_time() -> str:
    """Get current time."""
    from datetime import datetime
    return datetime.now().strftime("%H:%M:%S")

# Create tools list
tools = [get_weather, get_time]

# Create ToolNode
tool_node = ToolNode(tools)

# Usage in graph
from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import tools_condition

graph = StateGraph(MessagesState)
graph.add_node("agent", call_model)  # Your LLM node
graph.add_node("tools", tool_node)
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", "agent")
```

### ToolNode with Custom Error Handling

```python
from langchain_core.messages import ToolMessage

def custom_tool_node(state):
    """Custom tool node with enhanced error handling."""
    tools_by_name = {tool.name: tool for tool in tools}
    tool_calls = state["messages"][-1].tool_calls
    results = []

    for tool_call in tool_calls:
        try:
            tool = tools_by_name[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            results.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            ))
        except Exception as e:
            results.append(ToolMessage(
                content=f"Error: {str(e)}",
                tool_call_id=tool_call["id"],
                name=tool_call["name"],
                additional_kwargs={"is_error": True}
            ))

    return {"messages": results}
```

## BaseModel as Tool Schema

Using Pydantic `BaseModel` as the tool schema provides powerful validation and documentation capabilities[^2].

### Advanced Schema Example

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class TaskInput(BaseModel):
    title: str = Field(
        description="Task title",
        min_length=1,
        max_length=100
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed task description"
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        description="Task priority level"
    )
    due_date: Optional[datetime] = Field(
        default=None,
        description="Due date in ISO format"
    )
    tags: List[str] = Field(
        default=[],
        description="List of tags",
        max_items=5
    )
    assignee: Optional[str] = Field(
        default=None,
        description="Person assigned to task"
    )

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < datetime.now():
            raise ValueError("Due date must be in the future")
        return v

    @validator('tags')
    def validate_tags(cls, v):
        if len(set(v)) != len(v):
            raise ValueError("Tags must be unique")
        return v

@tool(args_schema=TaskInput)
def create_task(
    title: str,
    description: Optional[str] = None,
    priority: Priority = Priority.MEDIUM,
    due_date: Optional[datetime] = None,
    tags: List[str] = [],
    assignee: Optional[str] = None
) -> str:
    """Create a new task with validation."""
    task = {
        "title": title,
        "description": description,
        "priority": priority.value,
        "due_date": due_date.isoformat() if due_date else None,
        "tags": tags,
        "assignee": assignee,
        "created_at": datetime.now().isoformat()
    }
    return f"Task created: {task}"
```

## State Injection Patterns

### InjectedState for Graph State Access

`InjectedState` allows tools to access the current graph state without exposing it to the LLM[^6][^7].

```python
from typing_extensions import Annotated
from langgraph.prebuilt import InjectedState

@tool
def analyze_conversation(
    topic: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Analyze conversation history for a specific topic."""
    messages = state.get("messages", [])
    relevant_messages = [
        msg for msg in messages
        if hasattr(msg, 'content') and topic.lower() in msg.content.lower()
    ]

    return f"Found {len(relevant_messages)} messages about {topic}"

# Field-specific injection
@tool
def get_user_context(
    query: str,
    user_info: Annotated[dict, InjectedState("user_info")]
) -> str:
    """Get user context for personalized responses."""
    return f"User {user_info.get('name', 'Unknown')}: {query}"
```

### Complete State Management Example

```python
from typing import Dict, List, Any
from typing_extensions import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.prebuilt import InjectedState

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_info: Dict[str, Any]
    session_data: Dict[str, Any]
    tools_used: List[str]

@tool
def personalized_recommendation(
    category: str,
    state: Annotated[AgentState, InjectedState]
) -> str:
    """Provide personalized recommendations based on user state."""
    user_info = state.get("user_info", {})
    session_data = state.get("session_data", {})

    # Access user preferences
    preferences = user_info.get("preferences", {})
    previous_searches = session_data.get("searches", [])

    recommendation = f"Based on your interest in {category}"
    if preferences:
        recommendation += f" and preferences for {preferences}"
    if previous_searches:
        recommendation += f" and recent searches: {previous_searches}"

    return recommendation

# Usage in graph with state injection
tool_node = ToolNode([personalized_recommendation])
```

## Tool Validation and Error Handling

### ValidationNode for Schema Validation

`ValidationNode` validates tool calls without executing them, useful for structured output generation[^8].

```python
from langgraph.prebuilt import ValidationNode
from pydantic import BaseModel, Field

class ExtractedData(BaseModel):
    name: str = Field(description="Person's name")
    age: int = Field(description="Person's age", ge=0, le=150)
    email: str = Field(description="Email address")

# Create validation node
validation_node = ValidationNode([ExtractedData])

# Use in graph for validation-only flow
def should_validate(state):
    if state["messages"][-1].tool_calls:
        return "validation"
    return "__end__"

graph.add_node("validation", validation_node)
graph.add_conditional_edges("model", should_validate)
```

### Custom Error Handling

```python
from langchain_core.messages import ToolMessage

@tool
def risky_operation(data: str) -> str:
    """An operation that might fail."""
    if not data:
        raise ValueError("Data cannot be empty")
    if len(data) > 100:
        raise ValueError("Data too long")
    return f"Processed: {data}"

# Handle errors in tool node
def safe_tool_execution(state):
    """Execute tools with comprehensive error handling."""
    tools_by_name = {tool.name: tool for tool in tools}
    tool_calls = state["messages"][-1].tool_calls
    results = []

    for tool_call in tool_calls:
        try:
            tool = tools_by_name[tool_call["name"]]
            result = tool.invoke(tool_call["args"])
            results.append(ToolMessage(
                content=result,
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            ))
        except ValueError as e:
            # User input error - return helpful message
            results.append(ToolMessage(
                content=f"Invalid input: {str(e)}. Please try again.",
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            ))
        except Exception as e:
            # System error - return generic message
            results.append(ToolMessage(
                content="An unexpected error occurred. Please try again later.",
                tool_call_id=tool_call["id"],
                name=tool_call["name"]
            ))

    return {"messages": results}
```

## Advanced Tool Patterns

### Command Objects for State Updates

Tools can return `Command` objects to update graph state beyond just messages[^9][^10].

```python
from langgraph.types import Command
from typing import Tuple, Dict, Any

@tool
def update_user_profile(
    user_id: str,
    updates: Dict[str, Any],
    state: Annotated[dict, InjectedState]
) -> Tuple[str, Dict[str, Any]]:
    """Update user profile and return both message and state update."""
    # Process updates
    updated_profile = {**state.get("user_info", {}), **updates}

    return Command(
        update={
            "user_info": updated_profile,
            "messages": [ToolMessage(
                content=f"Profile updated for user {user_id}",
                tool_call_id="update_id"
            )]
        }
    )
```

### Retrieval-as-a-Tool Pattern

```python
from langchain_core.tools import create_retriever_tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# Create retriever tool
retriever_tool = create_retriever_tool(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
    name="knowledge_search",
    description="Search company knowledge base for information"
)

# Enhanced retriever with context
@tool
def contextual_search(
    query: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Search with user context for better results."""
    user_info = state.get("user_info", {})

    # Enhance query with user context
    enhanced_query = f"{query} user_role:{user_info.get('role', 'general')}"

    # Use retriever
    docs = retriever.get_relevant_documents(enhanced_query)

    return "\n".join([doc.page_content for doc in docs])
```

### Multi-Tool Orchestration

```python
@tool
def orchestrate_research(
    topic: str,
    depth: Literal["basic", "detailed", "comprehensive"] = "basic"
) -> str:
    """Orchestrate multiple research tools based on depth requirement."""
    results = []

    if depth in ["basic", "detailed", "comprehensive"]:
        # Always do basic search
        search_result = search_tool.invoke({"query": topic})
        results.append(f"Search: {search_result}")

    if depth in ["detailed", "comprehensive"]:
        # Add knowledge base search
        kb_result = knowledge_search.invoke({"query": topic})
        results.append(f"Knowledge Base: {kb_result}")

    if depth == "comprehensive":
        # Add expert analysis
        analysis_result = expert_analysis.invoke({"topic": topic})
        results.append(f"Expert Analysis: {analysis_result}")

    return "\n---\n".join(results)
```

## Best Practices and Optimization

### 1. Tool Naming and Description

```python
@tool
def calculate_mortgage_payment(
    principal: float,
    annual_rate: float,
    years: int
) -> str:
    """Calculate monthly mortgage payment.

    Use this tool when users ask about mortgage calculations, monthly payments,
    or loan affordability. Provide clear breakdowns of payment components.

    Args:
        principal: Loan amount in dollars
        annual_rate: Annual interest rate as percentage (e.g., 3.5 for 3.5%)
        years: Loan term in years

    Returns:
        Formatted payment breakdown with principal, interest, and total
    """
    monthly_rate = annual_rate / 100 / 12
    num_payments = years * 12

    if monthly_rate == 0:
        monthly_payment = principal / num_payments
    else:
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    total_paid = monthly_payment * num_payments
    total_interest = total_paid - principal

    return f"""
    Monthly Payment: ${monthly_payment:.2f}
    Total Amount Paid: ${total_paid:.2f}
    Total Interest: ${total_interest:.2f}
    """
```

### 2. Performance Optimization

```python
from functools import lru_cache
import asyncio

@tool
async def cached_api_call(endpoint: str, params: dict) -> str:
    """API call with caching and async support."""

    @lru_cache(maxsize=100)
    def _cached_call(endpoint: str, params_str: str):
        # Simulate API call
        return f"API response for {endpoint} with {params_str}"

    # Convert dict to string for caching
    params_str = str(sorted(params.items()))

    # Run cached call in thread pool for true async
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _cached_call, endpoint, params_str)

    return result
```

### 3. Testing Tools

```python
import pytest
from unittest.mock import Mock, patch

def test_weather_tool():
    """Test weather tool with mocked external service."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {
            'temperature': 72,
            'condition': 'sunny'
        }

        result = get_weather.invoke({"location": "San Francisco"})
        assert "72°F" in result
        assert "sunny" in result

def test_tool_validation():
    """Test tool input validation."""
    with pytest.raises(ValueError, match="Location cannot be empty"):
        get_weather.invoke({"location": ""})

def test_tool_with_state():
    """Test tool with injected state."""
    mock_state = {
        "messages": [Mock()],
        "user_info": {"name": "John", "preferences": {"units": "metric"}}
    }

    # Test tool execution with state
    result = analyze_conversation.invoke({
        "topic": "weather",
        "state": mock_state
    })

    assert "Found" in result
    assert "weather" in result
```

This comprehensive guide provides the foundation for building sophisticated tool systems in LangGraph. Each pattern can be combined and extended based on your specific use case requirements.

<div style="text-align: center">⁂</div>

[^1]: https://python.langchain.com/docs/concepts/tools/

[^2]: https://blog.langchain.com/structured-tools/

[^3]: https://python.langchain.com/api_reference/core/tools/langchain_core.tools.structured.StructuredTool.html

[^4]: https://langchain-ai.github.io/langgraphjs/how-tos/tool-calling/

[^5]: https://blog.csdn.net/qq_41472205/article/details/144199492

[^6]: https://blog.csdn.net/u013172930/article/details/148011556

[^7]: https://stackoverflow.com/questions/79524355/how-to-access-the-langraph-state-inside-the-langraph-tool

[^8]: https://langchain-ai.github.io/langgraph/reference/agents/

[^9]: https://github.com/langchain-ai/langgraph/discussions/1616

[^10]: https://changelog.langchain.com/announcements/modify-graph-state-from-tools-in-langgraph

[^11]: https://pypi.org/project/langgraph/0.0.27/

[^12]: https://github.com/kaigouthro/langraph

[^13]: https://aiproduct.engineer/tutorials/langgraph-tutorial-mastering-toolnode-implementation-unit-22-exercise-6

[^14]: https://langchain-ai.github.io/langgraph/concepts/low_level/

[^15]: https://www.youtube.com/watch?v=0i9NzY_b3pg

[^16]: https://juejin.cn/post/7459701053660151846

[^17]: https://www.youtube.com/watch?v=pDuNkb6VWaM

[^18]: https://langchain-ai.github.io/langgraph/

[^19]: https://langchain-ai.github.io/langgraph/how-tos/react-agent-structured-output/

[^20]: https://github.com/langchain-ai/langgraph/discussions/1162

[^21]: https://campus.datacamp.com/courses/designing-agentic-systems-with-langchain/building-chatbots-with-langgraph?ex=9

[^22]: https://www.reddit.com/r/LangChain/comments/1eg12qg/discussion_how_to_dynamically_modify_tool/

[^23]: https://dev.to/airabbit/building-structured-workflows-with-tools-and-functions-in-langgraph-3l6j

[^24]: https://blog.csdn.net/qq_41472205/article/details/145409607

[^25]: https://www.youtube.com/watch?v=MoHtLAhoMp4

[^26]: https://langchain-ai.github.io/langgraph/how-tos/state-model/

[^27]: https://stackoverflow.com/questions/79293447/getting-validationerror-when-trying-to-inspect-the-message-traceback-of-langgrap

[^28]: https://www.npmjs.com/package/@langchain/langgraph-checkpoint-validation?activeTab=dependencies

[^29]: https://docs.smith.langchain.com/evaluation/how_to_guides/langgraph

[^30]: https://github.com/langchain-ai/langchain/discussions/26399

[^31]: https://www.npmjs.com/package/@langchain/langgraph-checkpoint-validation?activeTab=versions

[^32]: https://www.reddit.com/r/LangChain/comments/1f8ui4a/tool_calling_in_langgraph_and_how_to_update_the/

[^33]: https://python.langchain.com/docs/how_to/custom_tools/

[^34]: https://www.youtube.com/watch?v=0gJLFTlGFVU

[^35]: https://www.reddit.com/r/LangChain/comments/1gc06vn/getting_messages_from_within_a_tool_in_langgraph/

[^36]: https://aws-samples.github.io/amazon-bedrock-samples/agents-and-function-calling/open-source-agents/langgraph/langgraph-fact-checker-feedback-loop/

[^37]: https://github.com/langchain-ai/langgraph/discussions/2806

[^38]: https://www.reddit.com/r/LangChain/comments/1j38fca/structured_output_with_langgraph_sucks/

[^39]: https://langchain-ai.github.io/langgraphjs/how-tos/update-state-from-tools/

[^40]: https://aiproduct.engineer/tutorials/langgraph-tutorial-error-handling-patterns-unit-23-exercise-6

[^41]: https://docs.bentoml.com/en/latest/examples/langgraph.html

[^42]: https://www.linkedin.com/posts/abhinav-mg-k_langgraph-langchain-llmops-activity-7345845615899176960-rnsO

[^43]: https://www.linkedin.com/pulse/masterclass-blog-post-8-ensuring-smooth-operations-agent-govender-0vh5f

[^44]: https://langchain-ai.github.io/langgraph/examples/

[^45]: https://langchain-ai.github.io/langgraphjs/how-tos/tool-calling-errors/

[^46]: https://blog.gopenai.com/building-stateful-applications-with-langgraph-860de3c9fa90

[^47]: https://langchain-ai.github.io/langgraph/how-tos/update-state-from-tools/

[^48]: https://blog.csdn.net/u013172930/article/details/148119232

[^49]: https://python.langchain.com/docs/how_to/tool_artifacts/

[^50]: https://python.langchain.com/api_reference/core/tools/langchain_core.tools.retriever.create_retriever_tool.html

[^51]: https://github.com/rkafh/LangGraph-Custom-Tool-Calling

[^52]: https://api.python.langchain.com/en/latest/tools/langchain.tools.retriever.create_retriever_tool.html

[^53]: https://github.com/jakenolan/langgraph-custom-tools

[^54]: https://github.com/langchain-ai/langgraph/discussions/3443

[^55]: https://langchain-ai.github.io/langgraph/tutorials/rag/langgraph_agentic_rag/

[^56]: https://ai.gopubby.com/extend-langgraph-agents-with-custom-tools-4db292595b95?gi=6a1888ef241c

[^57]: https://github.com/langchain-ai/langgraph/discussions/1055

[^58]: https://microsoft.github.io/autogen/dev/user-guide/core-user-guide/cookbook/langgraph-agent.html

[^59]: https://www.datacamp.com/tutorial/langgraph-agents

[^60]: https://python.langchain.com/v0.2/api_reference/core/tools/langchain_core.tools.retriever.create_retriever_tool.html

[^61]: https://www.youtube.com/watch?v=t_0JX4srrzI

[^62]: https://realpython.com/langgraph-python/

[^63]: https://api.python.langchain.com/en/latest/tools/langchain_core.tools.create_retriever_tool.html

[^64]: https://www.youtube.com/watch?v=UiK6ln_Qh7E

[^65]: https://langchain-ai.github.io/langgraphjs/tutorials/rag/langgraph_agentic_rag/
