# Haive Documentation Style Guide

## Overview
This guide defines the documentation standards for the Haive project. All documentation should follow these guidelines to ensure consistency, clarity, and maintainability.

## Documentation Types

### 1. Python Docstrings (Google Style)

#### Module Docstrings
```python
"""One-line summary of module purpose.

Detailed description of the module's functionality, design decisions,
and usage patterns. Include architectural notes and relationships to
other modules.

Typical usage example:
    Basic usage of the module::

        from haive.agents import SimpleAgent
        agent = SimpleAgent(name="assistant")
        result = await agent.arun("Hello")

    Advanced usage with configuration::

        config = SimpleAgentConfig(
            temperature=0.7,
            max_tokens=1000
        )
        agent = SimpleAgent.from_config(config)

Attributes:
    MODULE_VERSION: Current version of this module
    DEFAULT_TIMEOUT: Default timeout for operations (30 seconds)

Todo:
    * Add support for streaming responses
    * Implement retry logic for failed operations

.. versionadded:: 0.1.0
.. versionchanged:: 0.2.0
   Added support for async operations
"""
```

#### Class Docstrings
```python
class AgentEngine(BaseEngine):
    """Engine for running AI agents with tool support.
    
    This engine provides a unified interface for running agents with
    various LLM backends and tool integrations. It handles state
    management, tool execution, and response streaming.
    
    Args:
        model (str): Model identifier (e.g., "gpt-4", "claude-3")
        temperature (float): Sampling temperature, 0.0 to 2.0. Defaults to 0.7.
        tools (List[Tool], optional): List of tools available to the agent.
            If None, no tools will be available.
        **kwargs: Additional model-specific parameters.
    
    Attributes:
        model (str): The model being used
        tools (Dict[str, Tool]): Mapping of tool names to tool instances
        conversation_history (List[Message]): Full conversation history
        total_tokens (int): Total tokens used across all calls
    
    Example:
        Basic usage::
        
            engine = AgentEngine(model="gpt-4")
            response = await engine.arun("What's the weather?")
            
        With tools::
        
            from haive.tools import Calculator, WebSearch
            
            engine = AgentEngine(
                model="gpt-4",
                tools=[Calculator(), WebSearch()],
                temperature=0.5
            )
            response = await engine.arun("Search for Python tutorials")
    
    Raises:
        ValueError: If model is not supported or temperature is out of range
        EngineError: If engine initialization fails
        ToolExecutionError: If a tool fails during execution
    
    Note:
        The engine maintains conversation state between calls. Use
        `reset_conversation()` to clear the history.
        
    See Also:
        - :class:`BaseEngine`: Parent class with core interface
        - :class:`Tool`: Tool interface documentation
        - :doc:`/guides/engines`: Engine usage guide
    
    .. versionadded:: 0.1.0
    .. versionchanged:: 0.3.0
       Added streaming support via `astream()` method
    """
```

#### Method Docstrings
```python
async def execute_tool(
    self, 
    tool_name: str, 
    arguments: Dict[str, Any],
    context: Optional[ExecutionContext] = None
) -> ToolResult:
    """Execute a tool with given arguments and return the result.
    
    This method handles tool validation, execution, and error handling.
    It supports both synchronous and asynchronous tools, automatically
    handling the execution mode based on the tool's implementation.
    
    Args:
        tool_name: Name of the tool to execute. Must be registered.
        arguments: Dictionary of arguments to pass to the tool.
            Keys must match the tool's expected parameters.
        context: Optional execution context containing metadata
            about the current execution (e.g., user info, session ID).
            If None, a default context will be created.
    
    Returns:
        ToolResult: Object containing:
            - output (Any): The tool's return value
            - success (bool): Whether execution succeeded
            - error (Optional[str]): Error message if failed
            - metadata (Dict): Execution metadata (timing, tokens used)
    
    Raises:
        ToolNotFoundError: If tool_name is not registered
        ToolValidationError: If arguments don't match tool schema
        ToolExecutionError: If tool execution fails
        TimeoutError: If tool execution exceeds timeout
    
    Example:
        Simple tool execution::
        
            result = await engine.execute_tool(
                "calculator",
                {"expression": "2 + 2"}
            )
            print(result.output)  # 4
            
        With context::
        
            context = ExecutionContext(
                user_id="user123",
                session_id="session456",
                timeout=30.0
            )
            result = await engine.execute_tool(
                "web_search",
                {"query": "Python tutorials"},
                context=context
            )
    
    Note:
        Tool execution is logged and can be monitored via the
        engine's event system. Subscribe to 'tool.execution' events
        for real-time monitoring.
        
    .. warning::
        Tools may have side effects. Ensure proper permissions
        are set before executing tools that modify external state.
    """
```

#### Property Docstrings
```python
@property
def is_configured(self) -> bool:
    """Check if the engine is properly configured and ready to use.
    
    An engine is considered configured if:
    - Model is set and valid
    - Required API keys are present
    - All tools are properly initialized
    
    Returns:
        bool: True if ready to use, False otherwise
        
    Example:
        >>> engine = AgentEngine(model="gpt-4")
        >>> if engine.is_configured:
        ...     response = await engine.arun("Hello")
    """
```

### 2. Type Hints and Annotations

```python
from typing import (
    Dict, List, Optional, Union, Any, Callable, 
    TypeVar, Generic, Literal, Protocol, TypedDict,
    Awaitable, AsyncIterator, overload
)
from typing_extensions import Annotated, NotRequired
from pydantic import BaseModel, Field, validator

# Type variables for generics
T = TypeVar('T')
StateT = TypeVar('StateT', bound='BaseState')

# Type aliases for clarity
ToolName = str
ToolArgs = Dict[str, Any]
ToolResult = Union[str, Dict[str, Any], BaseModel]
MessageRole = Literal["system", "user", "assistant", "tool"]

# Protocol for tool interface
class ToolProtocol(Protocol):
    """Protocol defining the tool interface."""
    
    name: str
    description: str
    
    async def execute(self, **kwargs: Any) -> ToolResult:
        """Execute the tool with given arguments."""
        ...

# TypedDict for structured data
class ConversationTurn(TypedDict):
    """Structure for a conversation turn."""
    role: MessageRole
    content: str
    timestamp: float
    metadata: NotRequired[Dict[str, Any]]

# Complex type hints with documentation
AsyncToolExecutor = Callable[
    [ToolName, ToolArgs], 
    Awaitable[ToolResult]
]
"""Type for async tool execution functions.

Args:
    Tool name and arguments dictionary
Returns:
    Awaitable that resolves to tool result
"""
```

### 3. RST Documentation Files

#### Module Index Page
```rst
Agent Module
============

.. module:: haive.agents
   :synopsis: Agent implementations and patterns

Overview
--------

The agents module provides a comprehensive set of agent architectures
and patterns for building intelligent AI systems. This module includes
base classes, common patterns, and specialized implementations.

.. contents:: Module Contents
   :local:
   :depth: 2

Architecture
------------

The agent architecture follows these principles:

1. **Composability**: Agents can be composed from smaller components
2. **Extensibility**: Easy to create custom agents by extending base classes
3. **Type Safety**: Full type hints and runtime validation
4. **Async First**: All operations are async by default

.. code-block:: text

   BaseAgent (Abstract)
   ├── SimpleAgent         # Basic conversational agent
   ├── ReactAgent         # Reasoning + Acting pattern
   ├── PlanExecuteAgent   # Planning then execution
   └── CustomAgent        # User implementations

Quick Start
-----------

Basic Usage
~~~~~~~~~~~

.. code-block:: python

   from haive.agents import SimpleAgent
   from haive.core.engine import create_engine
   
   # Create an agent
   agent = SimpleAgent(
       name="assistant",
       engine=create_engine("gpt-4"),
       system_prompt="You are a helpful assistant."
   )
   
   # Run the agent
   response = await agent.arun("What is the capital of France?")
   print(response)  # "The capital of France is Paris."

Advanced Usage
~~~~~~~~~~~~~~

.. code-block:: python

   from haive.agents import ReactAgent
   from haive.tools import Calculator, WebSearch
   
   # Create agent with tools
   agent = ReactAgent(
       name="research_assistant",
       engine=create_engine("gpt-4"),
       tools=[Calculator(), WebSearch()],
       max_iterations=5
   )
   
   # Complex query requiring reasoning and tools
   response = await agent.arun(
       "What is the population of Tokyo divided by the area of Japan?"
   )

API Reference
-------------

Base Classes
~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   
   BaseAgent
   AgentConfig
   AgentState
   AgentResult

Simple Agents
~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   
   SimpleAgent
   ConversationalAgent
   StructuredOutputAgent

Advanced Agents
~~~~~~~~~~~~~~~

.. autosummary::
   :toctree: _autosummary
   :template: custom-class-template.rst
   
   ReactAgent
   PlanExecuteAgent
   MultiAgent
   HierarchicalAgent

Configuration
-------------

Agent configuration is handled through Pydantic models:

.. code-block:: python

   from haive.agents import AgentConfig
   
   config = AgentConfig(
       name="my_agent",
       model="gpt-4",
       temperature=0.7,
       max_tokens=1000,
       tools=["calculator", "web_search"],
       memory_type="conversation_buffer",
       memory_size=10
   )
   
   agent = Agent.from_config(config)

Best Practices
--------------

1. **State Management**
   
   Always define clear state schemas::
   
       class MyAgentState(BaseState):
           conversation: List[Message] = Field(default_factory=list)
           context: Dict[str, Any] = Field(default_factory=dict)
           iteration_count: int = 0

2. **Error Handling**
   
   Use proper error handling for robustness::
   
       try:
           result = await agent.arun(query)
       except TokenLimitError:
           # Handle token limits
           result = await agent.arun(query, max_tokens=500)
       except ToolExecutionError as e:
           # Handle tool failures
           logger.error(f"Tool {e.tool_name} failed: {e.message}")

3. **Testing**
   
   Test agents with mocked engines::
   
       async def test_agent():
           mock_engine = MockEngine(
               responses=["Paris", "France"]
           )
           agent = SimpleAgent(engine=mock_engine)
           
           response = await agent.arun("Capital?")
           assert response == "Paris"

Examples
--------

See the following examples for common use cases:

.. toctree::
   :maxdepth: 1
   
   examples/simple_conversation
   examples/tool_usage
   examples/multi_agent_debate
   examples/hierarchical_planning

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Errors**

If you see import errors like::

    ModuleNotFoundError: No module named 'haive.agents.advanced'

Ensure you have installed the correct extras::

    pip install haive[agents]

**Tool Registration**

Tools must be properly registered::

    from haive.tools import tool_registry
    
    @tool_registry.register
    class MyTool(BaseTool):
        name = "my_tool"
        description = "My custom tool"

See Also
--------

- :doc:`/guides/building_agents` - Comprehensive agent building guide
- :doc:`/api/core/engine` - Engine documentation
- :doc:`/api/tools` - Available tools
- :doc:`/examples` - More examples

.. note::
   This module is under active development. APIs may change in minor versions.
   
.. versionadded:: 0.1.0
.. versionchanged:: 0.2.0
   Added multi-agent support
.. versionchanged:: 0.3.0
   Improved state management system
```

### 4. README.md for Modules

```markdown
# Haive Agents Module

## Overview

The `haive.agents` module provides a comprehensive collection of agent architectures and patterns for building intelligent AI systems. With 50+ pre-built agent types and a flexible framework for custom implementations, you can quickly build sophisticated AI applications.

## Installation

```bash
# Basic installation
pip install haive

# With all agent dependencies
pip install haive[agents]

# Development installation
pip install -e ".[agents,dev]"
```

## Quick Start

```python
from haive.agents import SimpleAgent
from haive.core.engine import create_engine

# Create a simple conversational agent
agent = SimpleAgent(
    name="assistant",
    engine=create_engine("gpt-4"),
    system_prompt="You are a helpful AI assistant."
)

# Run the agent
response = await agent.arun("What's the weather like?")
print(response)
```

## Agent Types

### 1. Simple Agents
- **SimpleAgent**: Basic conversational agent
- **StructuredOutputAgent**: Returns structured data (JSON, Pydantic models)

### 2. ReAct Agents
- **ReactAgent**: Reasoning + Acting pattern
- **ReactWithMemory**: ReAct with persistent memory

### 3. Planning Agents
- **PlanExecuteAgent**: Creates and executes multi-step plans
- **HierarchicalPlanner**: Nested planning with sub-goals

### 4. Multi-Agent Systems
- **DebateAgent**: Multiple agents debate to reach consensus
- **CollaborativeAgent**: Agents work together on tasks
- **SupervisorAgent**: Orchestrates other agents

### 5. Specialized Agents
- **ResearchAgent**: Deep research with citations
- **CodeAgent**: Code generation and debugging
- **DataAnalysisAgent**: Statistical analysis and visualization

## Key Features

### State Management
```python
from haive.agents import BaseState

class MyAgentState(BaseState):
    messages: List[Message] = []
    context: Dict[str, Any] = {}
    tools_used: List[str] = []
```

### Tool Integration
```python
from haive.tools import Calculator, WebSearch

agent = ReactAgent(
    name="research_assistant",
    tools=[Calculator(), WebSearch()],
    tool_choice="auto"  # auto, required, none
)
```

### Memory Systems
```python
from haive.agents.memory import ConversationMemory

agent = SimpleAgent(
    name="assistant",
    memory=ConversationMemory(max_turns=10)
)
```

### Streaming Responses
```python
async for chunk in agent.astream("Tell me a story"):
    print(chunk, end="", flush=True)
```

## Architecture

```
BaseAgent (Abstract)
├── Config: AgentConfig
├── State: AgentState
├── Engine: BaseEngine
├── Tools: List[BaseTool]
├── Memory: BaseMemory
└── Methods:
    ├── arun() -> str
    ├── astream() -> AsyncIterator[str]
    ├── abatch() -> List[str]
    └── ainvoke() -> AgentResult
```

## Configuration

### Using Config Files
```yaml
# agent_config.yaml
name: my_assistant
type: SimpleAgent
engine:
  model: gpt-4
  temperature: 0.7
tools:
  - calculator
  - web_search
memory:
  type: conversation_buffer
  max_size: 1000
```

```python
from haive.agents import load_agent

agent = load_agent("agent_config.yaml")
```

### Programmatic Configuration
```python
from haive.agents import AgentConfig, SimpleAgent

config = AgentConfig(
    name="assistant",
    model="gpt-4",
    temperature=0.7,
    max_tokens=1000,
    tools=["calculator"],
    system_prompt="You are helpful."
)

agent = SimpleAgent.from_config(config)
```

## Advanced Usage

### Custom Agents
```python
from haive.agents import BaseAgent

class MyCustomAgent(BaseAgent):
    """Custom agent implementation."""
    
    async def _process(self, input: str) -> str:
        # Custom processing logic
        state = self.state
        state.messages.append({"role": "user", "content": input})
        
        # Use engine for generation
        response = await self.engine.agenerate(
            messages=state.messages,
            tools=self.tools
        )
        
        return response.content
```

### Composition Patterns
```python
# Agent pipeline
pipeline = AgentPipeline([
    PreprocessAgent(),
    MainAgent(),
    PostprocessAgent()
])

result = await pipeline.arun("Complex query")

# Agent router
router = AgentRouter({
    "math": MathAgent(),
    "research": ResearchAgent(),
    "general": GeneralAgent()
})

result = await router.arun("What's 2+2?")  # Routes to MathAgent
```

### Error Handling
```python
from haive.agents.exceptions import (
    AgentError,
    TokenLimitError,
    ToolExecutionError
)

try:
    result = await agent.arun(query)
except TokenLimitError as e:
    # Reduce token usage
    result = await agent.arun(
        query, 
        max_tokens=e.suggested_max
    )
except ToolExecutionError as e:
    # Retry without the failing tool
    agent.disable_tool(e.tool_name)
    result = await agent.arun(query)
```

## Testing

### Unit Tests
```python
import pytest
from haive.agents import SimpleAgent
from haive.testing import MockEngine

@pytest.mark.asyncio
async def test_simple_agent():
    mock_engine = MockEngine(
        responses=["Hello!", "Goodbye!"]
    )
    
    agent = SimpleAgent(
        name="test_agent",
        engine=mock_engine
    )
    
    response1 = await agent.arun("Hi")
    assert response1 == "Hello!"
    
    response2 = await agent.arun("Bye")
    assert response2 == "Goodbye!"
```

### Integration Tests
```python
@pytest.mark.integration
async def test_agent_with_tools():
    agent = ReactAgent(
        name="test_agent",
        engine=create_engine("gpt-4"),
        tools=[Calculator()],
        max_iterations=3
    )
    
    result = await agent.arun("What's 123 * 456?")
    assert "56088" in result
```

## Performance Optimization

### Caching
```python
from haive.agents.cache import ResponseCache

agent = SimpleAgent(
    name="cached_agent",
    cache=ResponseCache(
        ttl=3600,  # 1 hour
        max_size=1000
    )
)
```

### Batching
```python
# Process multiple queries efficiently
queries = ["Question 1", "Question 2", "Question 3"]
responses = await agent.abatch(queries, max_concurrency=3)
```

### Token Management
```python
from haive.agents.tokens import TokenManager

agent = SimpleAgent(
    name="efficient_agent",
    token_manager=TokenManager(
        max_tokens_per_call=1000,
        max_total_tokens=10000,
        truncation_strategy="sliding_window"
    )
)
```

## Monitoring and Debugging

### Logging
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("haive.agents")

# Agent operations are automatically logged
agent = SimpleAgent(name="logged_agent")
```

### Callbacks
```python
from haive.agents.callbacks import (
    ConsoleCallback,
    FileCallback,
    MetricsCallback
)

agent = SimpleAgent(
    name="monitored_agent",
    callbacks=[
        ConsoleCallback(),
        FileCallback("agent_logs.jsonl"),
        MetricsCallback(prometheus_gateway="localhost:9091")
    ]
)
```

### Tracing
```python
from haive.agents.tracing import enable_tracing

# Enable OpenTelemetry tracing
enable_tracing(
    service_name="my_agent_service",
    jaeger_endpoint="http://localhost:14268"
)
```

## Common Patterns

### Retry Logic
```python
from haive.agents.retry import RetryConfig

agent = SimpleAgent(
    name="reliable_agent",
    retry_config=RetryConfig(
        max_retries=3,
        backoff_factor=2.0,
        retry_on=[TokenLimitError, ToolExecutionError]
    )
)
```

### Fallback Agents
```python
from haive.agents.fallback import FallbackAgent

agent = FallbackAgent(
    primary=ComplexAgent(),
    fallback=SimpleAgent(),
    fallback_on=[TokenLimitError, TimeoutError]
)
```

### Rate Limiting
```python
from haive.agents.ratelimit import RateLimiter

agent = SimpleAgent(
    name="rate_limited_agent",
    rate_limiter=RateLimiter(
        calls_per_minute=60,
        burst_size=10
    )
)
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Ensure all dependencies are installed
   pip install haive[agents,tools,dev]
   ```

2. **API Key Issues**
   ```python
   # Set API keys via environment
   os.environ["OPENAI_API_KEY"] = "your-key"
   
   # Or via config
   engine = create_engine(
       "gpt-4",
       api_key="your-key"
   )
   ```

3. **Memory Issues**
   ```python
   # Limit memory usage
   agent = SimpleAgent(
       name="memory_efficient",
       memory=ConversationMemory(
           max_size=100,  # Max messages
           summarize_after=50  # Summarize old messages
       )
   )
   ```

## Contributing

See [CONTRIBUTING.md](../../../CONTRIBUTING.md) for guidelines.

## License

This module is part of the Haive project. See [LICENSE](../../../LICENSE) for details.
```

### 5. API Documentation Comments

```python
# For complex APIs, add inline documentation

def create_agent(
    agent_type: str,
    config: Optional[Union[Dict, AgentConfig]] = None,
    **kwargs
) -> BaseAgent:
    """Factory function to create agents.
    
    Args:
        agent_type: Type of agent to create. Valid values:
            - "simple": Basic conversational agent
            - "react": ReAct pattern agent
            - "planner": Planning agent
            - "multi": Multi-agent system
            
        config: Configuration object or dict. If dict, will be
            converted to appropriate config class. If None,
            default configuration will be used.
            
        **kwargs: Override configuration values. These take
            precedence over config values.
            
    Returns:
        Configured agent instance ready to use.
        
    Raises:
        ValueError: If agent_type is not recognized
        ConfigurationError: If configuration is invalid
        
    Example:
        >>> # Create with type and kwargs
        >>> agent = create_agent(
        ...     "simple",
        ...     name="my_agent",
        ...     temperature=0.5
        ... )
        
        >>> # Create with config object
        >>> config = SimpleAgentConfig(name="my_agent")
        >>> agent = create_agent("simple", config)
        
    Note:
        The agent is not started automatically. Call
        `agent.start()` to begin processing.
    """
```

## Documentation Standards Summary

1. **Be Comprehensive**: Include all parameters, returns, raises, and examples
2. **Be Precise**: Use exact type hints and clear descriptions
3. **Be Practical**: Include real-world examples and common patterns
4. **Be Organized**: Follow consistent structure and formatting
5. **Be Helpful**: Include troubleshooting, best practices, and links

## Tools and Validation

```bash
# Validate docstrings
pydocstyle haive/

# Check type hints
mypy haive/

# Generate API docs
sphinx-apidoc -o docs/api haive/

# Build documentation
sphinx-build -b html docs/source docs/build

# Check for missing docs
python -m pytest --doctest-modules
```