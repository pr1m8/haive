# Haive Project Coding Style Guide

## Table of Contents

1. [Project Structure](#project-structure)
2. [Python Code Style](#python-code-style)
3. [Testing Guidelines](#testing-guidelines)
4. [Documentation Standards](#documentation-standards)
5. [Examples and Demos](#examples-and-demos)
6. [Package Development](#package-development)
7. [Git Workflow](#git-workflow)
8. [Performance Guidelines](#performance-guidelines)
9. [Agent Development Patterns](#agent-development-patterns)

## Project Structure

### Namespaced Polyrepo Layout

The Haive project uses a namespaced polyrepo structure with multiple packages under the `haive` namespace, developed in a single workspace for convenience:

```
haive/ (workspace)
├── packages/
│   ├── haive-core/           # Core framework package
│   │   ├── src/haive/core/
│   │   ├── tests/
│   │   ├── examples/
│   │   └── pyproject.toml
│   ├── haive-agents/         # Agent implementations package
│   │   ├── src/haive/agents/
│   │   ├── tests/
│   │   ├── examples/
│   │   └── pyproject.toml
│   ├── haive-tools/          # Tool implementations package
│   ├── haive-games/          # Game environments package
│   ├── haive-dataflow/       # Data processing package
│   ├── haive-mcp/            # MCP integration package
│   └── haive-prebuilt/       # Pre-built agents package
├── project_docs/             # Development documentation
├── docs/                     # User documentation
├── scripts/                  # Build and utility scripts
└── pyproject.toml           # Workspace configuration
```

**Key Characteristics:**
- Each package is independently versioned and publishable
- Packages share the `haive` namespace but can be installed separately
- Workspace configuration coordinates development across packages
- Each package has its own dependencies and can be released independently

### Package Structure

Each package follows this structure:

```
packages/haive-{package}/
├── src/haive/{package}/
│   ├── __init__.py          # Package entry point with exports
│   ├── base/                # Base classes and interfaces
│   ├── {module}/            # Feature modules
│   │   ├── __init__.py
│   │   ├── agent.py         # Main agent implementation
│   │   ├── config.py        # Configuration classes
│   │   ├── state.py         # State schemas
│   │   └── example.py       # Usage examples
│   └── utils/               # Package utilities
├── tests/
│   ├── conftest.py          # Shared test fixtures
│   ├── test_{module}/       # Module-specific tests
│   └── integration/         # Integration tests
├── examples/
│   ├── basic/               # Simple examples
│   ├── advanced/            # Complex use cases
│   └── notebooks/           # Jupyter notebooks
├── README.md                # Package documentation
└── pyproject.toml          # Package configuration
```

## Python Code Style

### General Principles

1. **Follow PEP 8** with 88-character line limit
2. **Use type hints everywhere** - no untyped public APIs
3. **Prefer composition over inheritance**
4. **Write defensive code** with proper error handling
5. **Use descriptive names** - clarity over brevity

### Code Formatting

```python
# Use black with 88-character line limit
# Use isort for import sorting
# Use ruff for linting

# Good: Clear, descriptive names
def create_rag_agent_with_vector_store(
    retriever: VectorRetriever,
    llm_config: LLMConfig,
    max_context_length: int = 4000
) -> RAGAgent:
    """Create a RAG agent with vector store retrieval.
    
    Args:
        retriever: Vector store retriever for document lookup
        llm_config: Configuration for the language model
        max_context_length: Maximum context window size
        
    Returns:
        Configured RAG agent ready for use
        
    Raises:
        ValueError: If retriever is not properly configured
        ConfigError: If llm_config is invalid
    """
    if not retriever.is_ready():
        raise ValueError("Retriever must be initialized before use")
    
    return RAGAgent(
        retriever=retriever,
        llm_config=llm_config,
        max_context_length=max_context_length
    )

# Bad: Unclear names and missing types
def make_agent(r, cfg, ctx=4000):
    return RAGAgent(r, cfg, ctx)
```

### Type Hints

```python
from typing import Dict, List, Optional, Union, Any, TypeVar, Generic
from typing_extensions import Literal, NotRequired, TypedDict
from pydantic import BaseModel

# Use Pydantic for data models
class AgentConfig(BaseModel):
    name: str
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    tools: List[str] = []
    
# Use TypedDict for simple dictionaries
class StateDict(TypedDict):
    messages: List[str]
    user_id: str
    session_id: NotRequired[str]  # Optional field

# Use generics for flexible APIs
T = TypeVar('T', bound=BaseModel)

class Agent(Generic[T]):
    def __init__(self, state_schema: type[T]) -> None:
        self.state_schema = state_schema
        
    def run(self, state: T) -> T:
        # Implementation
        pass
```

### Error Handling

```python
# Good: Specific exceptions with context
class AgentError(Exception):
    """Base exception for agent-related errors."""
    pass

class ConfigurationError(AgentError):
    """Raised when agent configuration is invalid."""
    pass

class ToolExecutionError(AgentError):
    """Raised when tool execution fails."""
    def __init__(self, tool_name: str, error: str):
        self.tool_name = tool_name
        super().__init__(f"Tool '{tool_name}' failed: {error}")

# Implementation with proper error handling
async def execute_tool(tool: Tool, input_data: Dict[str, Any]) -> ToolResult:
    try:
        result = await tool.arun(input_data)
        return result
    except ValidationError as e:
        raise ToolExecutionError(tool.name, f"Invalid input: {e}")
    except TimeoutError:
        raise ToolExecutionError(tool.name, "Tool execution timed out")
    except Exception as e:
        logger.exception(f"Unexpected error in tool {tool.name}")
        raise ToolExecutionError(tool.name, f"Unexpected error: {e}")
```

### Logging

```python
import logging
from haive.core.logging import get_logger

# Use structured logging
logger = get_logger(__name__)

# Good: Structured logging with context
def process_user_request(user_id: str, request: str) -> Response:
    logger.info(
        "Processing user request",
        extra={
            "user_id": user_id,
            "request_length": len(request),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    try:
        response = generate_response(request)
        logger.info(
            "Request processed successfully",
            extra={"user_id": user_id, "response_length": len(response.text)}
        )
        return response
    except Exception as e:
        logger.error(
            "Failed to process request",
            extra={"user_id": user_id, "error": str(e)},
            exc_info=True
        )
        raise
```

## Testing Guidelines

### Test Structure

```
tests/
├── conftest.py              # Shared fixtures
├── unit/                    # Unit tests
│   ├── test_agents/
│   ├── test_tools/
│   └── test_core/
├── integration/             # Integration tests
│   ├── test_agent_workflows/
│   └── test_tool_chains/
├── e2e/                     # End-to-end tests
└── fixtures/                # Test data and fixtures
    ├── sample_documents/
    └── mock_responses/
```

### Test Naming and Structure

```python
import pytest
from unittest.mock import Mock, patch
from haive.agents.simple import SimpleAgent
from haive.core.engine import AugLLMConfig

class TestSimpleAgent:
    """Test suite for SimpleAgent functionality."""
    
    @pytest.fixture
    def agent_config(self) -> AugLLMConfig:
        """Create a test agent configuration."""
        return AugLLMConfig(
            temperature=0.7,
            max_tokens=100,
            system_message="Test agent"
        )
    
    @pytest.fixture
    def simple_agent(self, agent_config: AugLLMConfig) -> SimpleAgent:
        """Create a test SimpleAgent instance."""
        return SimpleAgent(
            name="test_agent",
            engine=agent_config
        )
    
    async def test_simple_agent_responds_to_basic_query(
        self, simple_agent: SimpleAgent
    ) -> None:
        """Test that agent responds to basic user query."""
        # Arrange
        user_input = "Hello, how are you?"
        
        # Act
        response = await simple_agent.arun(user_input)
        
        # Assert
        assert response is not None
        assert len(response) > 0
        assert isinstance(response, str)
    
    async def test_simple_agent_maintains_conversation_state(
        self, simple_agent: SimpleAgent
    ) -> None:
        """Test that agent maintains state across multiple turns."""
        # Arrange
        thread_id = "test-conversation-123"
        config = {"configurable": {"thread_id": thread_id}}
        
        # Act
        await simple_agent.arun("My name is Alice", config=config)
        response = await simple_agent.arun("What's my name?", config=config)
        
        # Assert
        assert "alice" in response.lower()
    
    async def test_simple_agent_handles_invalid_input_gracefully(
        self, simple_agent: SimpleAgent
    ) -> None:
        """Test agent error handling with invalid input."""
        # Arrange
        invalid_input = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="Input cannot be None"):
            await simple_agent.arun(invalid_input)
    
    @patch('haive.core.engine.openai_client')
    async def test_simple_agent_handles_llm_timeout(
        self, mock_openai: Mock, simple_agent: SimpleAgent
    ) -> None:
        """Test agent behavior when LLM times out."""
        # Arrange
        mock_openai.chat.completions.create.side_effect = TimeoutError()
        
        # Act & Assert
        with pytest.raises(AgentError, match="LLM request timed out"):
            await simple_agent.arun("Hello")
```

### Integration Testing

```python
@pytest.mark.integration
class TestRAGAgentIntegration:
    """Integration tests for RAG agent with real components."""
    
    @pytest.fixture(scope="module")
    async def vector_store(self) -> VectorStore:
        """Create test vector store with sample documents."""
        store = VectorStore.create_memory_store()
        
        # Load test documents
        documents = load_test_documents("fixtures/sample_docs/")
        await store.add_documents(documents)
        
        yield store
        await store.cleanup()
    
    @pytest.fixture
    def rag_agent(self, vector_store: VectorStore) -> RAGAgent:
        """Create RAG agent with test vector store."""
        return RAGAgent(
            retriever=VectorRetriever(vector_store),
            llm_config=AugLLMConfig(temperature=0.0)  # Deterministic
        )
    
    async def test_rag_agent_retrieves_relevant_documents(
        self, rag_agent: RAGAgent
    ) -> None:
        """Test that RAG agent retrieves and uses relevant context."""
        # Arrange
        query = "What is the company's return policy?"
        
        # Act
        response = await rag_agent.arun(query)
        sources = rag_agent.get_source_documents()
        
        # Assert
        assert response is not None
        assert len(sources) > 0
        assert any("return" in doc.content.lower() for doc in sources)
        assert "policy" in response.lower()
```

### Mocking Guidelines

```python
# Good: Mock external dependencies, not internal logic
@patch('haive.tools.web.requests.get')
async def test_web_search_tool_handles_api_error(mock_get: Mock) -> None:
    mock_get.side_effect = requests.RequestException("API Error")
    
    tool = WebSearchTool()
    with pytest.raises(ToolExecutionError):
        await tool.search("test query")

# Good: Use factories for complex test data
def create_test_agent(
    name: str = "test_agent",
    tools: Optional[List[Tool]] = None,
    **kwargs
) -> ReactAgent:
    """Factory for creating test agents with sensible defaults."""
    if tools is None:
        tools = [MockTool(), MockCalculator()]
    
    return ReactAgent(
        name=name,
        tools=tools,
        max_iterations=3,
        **kwargs
    )
```

## Documentation Standards

### Module Documentation

```python
"""Haive Agents - Simple Agent Implementation.

This module provides the SimpleAgent class, which implements basic
conversational capabilities with state management and streaming support.

The SimpleAgent is designed for:
- Basic question-answering scenarios
- Conversational interfaces
- Stateful dialogue management
- Integration with various LLM providers

Examples:
    Basic usage::

        from haive.agents.simple import SimpleAgent
        
        agent = SimpleAgent(name="assistant")
        response = await agent.arun("Hello!")

    With custom configuration::

        config = AugLLMConfig(
            temperature=0.7,
            system_message="You are a helpful assistant."
        )
        agent = SimpleAgent(name="assistant", engine=config)

See Also:
    - :class:`~haive.agents.react.ReactAgent`: For tool-using agents
    - :class:`~haive.agents.rag.BaseRAGAgent`: For knowledge-grounded agents
"""
```

### Class Documentation

```python
class SimpleAgent(Agent[MessageState]):
    """A basic conversational agent with state management.
    
    The SimpleAgent provides fundamental conversational capabilities,
    including message history, state persistence, and streaming responses.
    It serves as the foundation for more complex agent implementations.
    
    Args:
        name: Unique identifier for the agent instance
        engine: LLM configuration and client wrapper
        system_message: Optional system prompt override
        state_schema: Pydantic model for state validation
        enable_streaming: Whether to support streaming responses
        max_history: Maximum number of messages to retain
        
    Attributes:
        name: The agent's identifier
        engine: The configured LLM engine
        state_schema: Schema class for state validation
        
    Examples:
        Create a basic agent::
        
            agent = SimpleAgent(name="helper")
            response = await agent.arun("What's the weather?")
            
        With conversation state::
        
            config = {"configurable": {"thread_id": "conv-123"}}
            await agent.arun("I'm Alice", config=config)
            response = await agent.arun("What's my name?", config=config)
            # Response: "Your name is Alice"
            
        Custom system message::
        
            agent = SimpleAgent(
                name="specialist",
                system_message="You are an expert in Python programming."
            )
            
    Note:
        The agent automatically handles conversation persistence when
        a thread_id is provided in the configuration.
        
    See Also:
        - :meth:`arun`: Main method for running the agent
        - :meth:`astream`: For streaming responses
        - :class:`MessageState`: Default state schema
    """
```

### Function Documentation

```python
async def process_conversation_turn(
    agent: Agent,
    user_input: str,
    conversation_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> ConversationResult:
    """Process a single conversation turn with an agent.
    
    This function handles the complete flow of processing user input
    through an agent, including state management, error handling,
    and result formatting.
    
    Args:
        agent: The agent instance to use for processing
        user_input: The user's message or query
        conversation_id: Optional identifier for conversation continuity.
            If provided, the agent will maintain state across turns.
        metadata: Optional metadata to include with the request.
            Can contain user preferences, context flags, etc.
            
    Returns:
        ConversationResult containing:
            - response: The agent's response text
            - sources: Any source documents referenced (for RAG agents)
            - metadata: Processing metadata (tokens used, timing, etc.)
            - state: Current conversation state
            
    Raises:
        AgentError: If the agent fails to process the input
        ValidationError: If the input doesn't meet schema requirements
        TimeoutError: If processing exceeds configured timeout
        
    Examples:
        Basic usage::
        
            result = await process_conversation_turn(
                agent=my_agent,
                user_input="Hello, how are you?"
            )
            print(result.response)
            
        With conversation continuity::
        
            result = await process_conversation_turn(
                agent=my_agent,
                user_input="My name is Bob",
                conversation_id="user-123-session-1"
            )
            
            result = await process_conversation_turn(
                agent=my_agent,
                user_input="What's my name?",
                conversation_id="user-123-session-1"
            )
            # result.response will reference "Bob"
            
        With metadata::
        
            result = await process_conversation_turn(
                agent=my_agent,
                user_input="Summarize this document",
                metadata={
                    "user_preferences": {"format": "bullet_points"},
                    "source_language": "en"
                }
            )
            
    Note:
        The function automatically handles conversation state persistence
        when a conversation_id is provided. State is stored using the
        agent's configured persistence backend.
        
    See Also:
        - :class:`ConversationResult`: Return value structure
        - :func:`create_agent_session`: For managing multiple conversations
    """
```

## Examples and Demos

### Example File Structure

```python
# examples/basic/simple_conversation.py
"""Basic conversation example with SimpleAgent.

This example demonstrates:
- Creating a simple conversational agent
- Single-turn and multi-turn conversations
- State persistence across turns
"""

import asyncio
from haive.agents.simple import SimpleAgent
from haive.core.engine import AugLLMConfig

async def main() -> None:
    """Run the simple conversation example."""
    # Create agent with custom configuration
    config = AugLLMConfig(
        temperature=0.7,
        system_message="You are a helpful and friendly assistant."
    )
    
    agent = SimpleAgent(
        name="friendly_assistant",
        engine=config
    )
    
    print("=== Single Turn Conversation ===")
    response = await agent.arun("What's the capital of France?")
    print(f"Agent: {response}")
    
    print("\n=== Multi-Turn Conversation ===")
    conversation_id = "example-conversation-1"
    config = {"configurable": {"thread_id": conversation_id}}
    
    # First turn - establish context
    await agent.arun("My favorite color is blue", config=config)
    print("User: My favorite color is blue")
    
    # Second turn - reference previous context
    response = await agent.arun("What's my favorite color?", config=config)
    print(f"Agent: {response}")
    
    print("\n=== Conversation Complete ===")

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Examples

```python
# examples/advanced/multi_agent_research.py
"""Advanced example: Multi-agent research pipeline.

This example demonstrates:
- Coordinating multiple specialized agents
- Sharing state between agents
- Error handling and recovery
- Performance monitoring
"""

import asyncio
from typing import Dict, Any
from haive.agents.research import PersonResearchAgent
from haive.agents.rag import BaseRAGAgent
from haive.agents.simple import SimpleAgent
from haive.agents.multi import MultiAgent

async def create_research_pipeline() -> MultiAgent:
    """Create a multi-agent research pipeline."""
    
    # Specialized research agent
    researcher = PersonResearchAgent(
        name="researcher",
        search_depth="comprehensive",
        max_sources=10
    )
    
    # Fact-checking agent with knowledge base
    fact_checker = BaseRAGAgent(
        name="fact_checker",
        retriever=create_fact_database_retriever(),
        verification_threshold=0.8
    )
    
    # Writing agent for final output
    writer = SimpleAgent(
        name="writer",
        system_message=(
            "You are a professional writer who creates well-structured, "
            "engaging content based on research findings."
        )
    )
    
    # Coordinate agents in pipeline
    pipeline = MultiAgent(
        name="research_pipeline",
        agents=[researcher, fact_checker, writer],
        routing_strategy="sequential",
        state_sharing="full"
    )
    
    return pipeline

async def run_research_task(
    pipeline: MultiAgent,
    topic: str,
    output_format: str = "report"
) -> Dict[str, Any]:
    """Run a complete research task through the pipeline."""
    
    task_config = {
        "topic": topic,
        "output_format": output_format,
        "quality_threshold": 0.9,
        "max_iterations": 3
    }
    
    try:
        result = await pipeline.arun(task_config)
        return {
            "success": True,
            "result": result,
            "metadata": pipeline.get_execution_metadata()
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "partial_results": pipeline.get_partial_results()
        }

async def main() -> None:
    """Run the advanced research example."""
    print("Creating research pipeline...")
    pipeline = await create_research_pipeline()
    
    print("Running research task...")
    result = await run_research_task(
        pipeline=pipeline,
        topic="Recent developments in quantum computing",
        output_format="technical_report"
    )
    
    if result["success"]:
        print("Research completed successfully!")
        print(f"Result: {result['result']}")
        print(f"Execution time: {result['metadata']['total_time']:.2f}s")
    else:
        print(f"Research failed: {result['error']}")
        if result["partial_results"]:
            print("Partial results available for debugging")

if __name__ == "__main__":
    asyncio.run(main())
```

## Package Development

### Adding New Agents

1. **Create the module structure**:
   ```
   packages/haive-agents/src/haive/agents/new_agent_type/
   ├── __init__.py
   ├── agent.py
   ├── config.py
   ├── state.py
   └── example.py
   ```

2. **Implement the agent class**:
   ```python
   from haive.agents.base import Agent
   from .config import NewAgentConfig
   from .state import NewAgentState
   
   class NewAgent(Agent[NewAgentState]):
       """New agent implementation."""
       
       def __init__(self, config: NewAgentConfig) -> None:
           super().__init__(
               name=config.name,
               state_schema=NewAgentState
           )
           self.config = config
   ```

3. **Add to package exports**:
   ```python
   # In packages/haive-agents/src/haive/agents/__init__.py
   from haive.agents.new_agent_type import NewAgent
   
   __all__ = [..., "NewAgent"]
   ```

4. **Write comprehensive tests**:
   ```python
   # tests/test_new_agent_type/test_agent.py
   class TestNewAgent:
       async def test_new_agent_basic_functionality(self):
           # Test implementation
           pass
   ```

### Configuration Management

```python
# config.py - Agent configuration
from pydantic import BaseModel, Field
from typing import Optional, List

class NewAgentConfig(BaseModel):
    """Configuration for NewAgent."""
    
    name: str = Field(..., description="Agent identifier")
    max_iterations: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum processing iterations"
    )
    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="LLM temperature setting"
    )
    tools: List[str] = Field(
        default_factory=list,
        description="List of tool names to enable"
    )
    custom_prompt: Optional[str] = Field(
        default=None,
        description="Custom system prompt override"
    )
    
    class Config:
        """Pydantic configuration."""
        validate_assignment = True
        extra = "forbid"  # Prevent unknown fields
```

## Git Workflow

### Commit Message Format

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(agents): add TreeOfThoughts reasoning agent

Implements the Tree of Thoughts algorithm for multi-path reasoning.
Includes support for value function evaluation and branch pruning.

Closes #123

fix(core): resolve MRO conflict in mixin inheritance

The SecureConfigMixin and ModelMetadataMixin had conflicting
method resolution order. Refactored to use composition instead.

test(rag): add integration tests for adaptive retrieval

Added comprehensive test suite covering strategy selection
and fallback behavior in adaptive RAG agents.
```

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes  
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Pull Request Process

1. **Create feature branch**: `git checkout -b feature/new-agent-type`
2. **Implement changes with tests**
3. **Run full test suite**: `poetry run pytest`
4. **Update documentation** if needed
5. **Create pull request** with:
   - Clear description of changes
   - Link to related issues
   - Test results
   - Breaking changes (if any)

## Performance Guidelines

### Async/Await Best Practices

```python
# Good: Proper async context management
async def process_multiple_requests(
    agent: Agent,
    requests: List[str]
) -> List[str]:
    """Process multiple requests concurrently."""
    
    # Use asyncio.gather for concurrent execution
    tasks = [agent.arun(request) for request in requests]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle exceptions appropriately
    responses = []
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            logger.error(f"Request {i} failed: {result}")
            responses.append(f"Error: {result}")
        else:
            responses.append(result)
    
    return responses

# Good: Resource cleanup
async def run_agent_with_cleanup(agent: Agent, input_data: str) -> str:
    """Run agent with proper resource cleanup."""
    try:
        result = await agent.arun(input_data)
        return result
    finally:
        # Cleanup resources
        await agent.cleanup()
        if hasattr(agent, 'close'):
            await agent.close()
```

### Memory Management

```python
# Good: Streaming for large responses
async def stream_agent_response(
    agent: Agent,
    input_data: str
) -> AsyncGenerator[str, None]:
    """Stream agent response to handle large outputs."""
    
    async for chunk in agent.astream(input_data):
        yield chunk

# Good: Batch processing with memory limits
async def process_large_dataset(
    agent: Agent,
    dataset: List[str],
    batch_size: int = 10
) -> List[str]:
    """Process large dataset in memory-efficient batches."""
    
    results = []
    for i in range(0, len(dataset), batch_size):
        batch = dataset[i:i + batch_size]
        batch_results = await process_multiple_requests(agent, batch)
        results.extend(batch_results)
        
        # Optional: Force garbage collection between batches
        import gc
        gc.collect()
    
    return results
```

### Monitoring and Profiling

```python
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

@asynccontextmanager
async def performance_monitor(
    operation_name: str
) -> AsyncGenerator[Dict[str, Any], None]:
    """Context manager for monitoring operation performance."""
    
    start_time = time.time()
    metrics = {"operation": operation_name, "start_time": start_time}
    
    try:
        yield metrics
    finally:
        end_time = time.time()
        metrics.update({
            "end_time": end_time,
            "duration": end_time - start_time
        })
        
        logger.info(
            f"Operation {operation_name} completed",
            extra=metrics
        )

# Usage
async def run_monitored_agent(agent: Agent, input_data: str) -> str:
    """Run agent with performance monitoring."""
    
    async with performance_monitor("agent_execution") as metrics:
        result = await agent.arun(input_data)
        metrics["tokens_used"] = getattr(agent, 'last_token_count', 0)
        return result
```

## Agent Development Patterns

### State Management Pattern

```python
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AgentState(BaseModel):
    """Base state schema for agents."""
    
    messages: List[str] = []
    metadata: Dict[str, Any] = {}
    iteration_count: int = 0
    
class SpecializedAgentState(AgentState):
    """Extended state for specialized agents."""
    
    reasoning_trace: List[str] = []
    tool_results: Dict[str, Any] = {}
    confidence_scores: List[float] = []
    
    def add_reasoning_step(self, step: str, confidence: float) -> None:
        """Add a reasoning step with confidence score."""
        self.reasoning_trace.append(step)
        self.confidence_scores.append(confidence)
        
    def get_average_confidence(self) -> float:
        """Calculate average confidence across reasoning steps."""
        if not self.confidence_scores:
            return 0.0
        return sum(self.confidence_scores) / len(self.confidence_scores)
```

### Tool Integration Pattern

```python
from abc import ABC, abstractmethod
from typing import Dict, Any, List

class Tool(ABC):
    """Base class for agent tools."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Tool identifier."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM context."""
        pass
    
    @abstractmethod
    async def arun(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the tool asynchronously."""
        pass

class ToolRegistry:
    """Registry for managing agent tools."""
    
    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}
    
    def register(self, tool: Tool) -> None:
        """Register a tool."""
        self._tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """Get a tool by name."""
        return self._tools.get(name)
    
    def get_tool_descriptions(self) -> List[Dict[str, str]]:
        """Get descriptions of all registered tools."""
        return [
            {"name": tool.name, "description": tool.description}
            for tool in self._tools.values()
        ]
```

---

This style guide should be treated as a living document and updated as the project evolves. All team members should follow these guidelines to ensure consistency and maintainability across the Haive codebase.