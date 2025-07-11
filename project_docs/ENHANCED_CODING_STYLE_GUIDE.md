# Haive Project Enhanced Coding Style Guide

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
10. [Type Hints Complete Guide](#type-hints-complete-guide)
11. [**init**.py Best Practices](#initpy-best-practices)
12. [README Templates](#readme-templates)

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

### Import Organization

```python
# Standard library imports
import asyncio
import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Third-party imports
import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, validator
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import AsyncSession

# Local application imports
from haive.core.base import Agent
from haive.core.config import Config
from haive.core.exceptions import AgentError, ConfigurationError
from haive.core.logging import get_logger
from haive.core.types import MessageType, StateType

# Relative imports (within the same package)
from .config import AgentConfig
from .state import AgentState
from .utils import format_response, validate_input
```

## Type Hints Complete Guide

### Basic Type Hints

```python
from typing import (
    Any, Dict, List, Set, Tuple, Optional, Union,
    Callable, Awaitable, Iterator, Generator,
    TypeVar, Generic, Protocol, Final, Literal,
    ClassVar, cast, overload
)
from typing_extensions import (
    NotRequired, Required, TypedDict, Annotated,
    Self, TypeAlias, TypeGuard, assert_never
)

# Basic types
name: str = "John"
age: int = 30
height: float = 5.9
is_active: bool = True
data: bytes = b"binary data"

# Collections
names: List[str] = ["Alice", "Bob"]
ages: Dict[str, int] = {"Alice": 30, "Bob": 25}
unique_ids: Set[int] = {1, 2, 3}
coordinates: Tuple[float, float] = (10.0, 20.0)

# Optional values
middle_name: Optional[str] = None  # or str | None in Python 3.10+
config: Optional[Dict[str, Any]] = None

# Union types
id_value: Union[int, str] = "abc123"  # or int | str in Python 3.10+
```

### Advanced Type Hints

```python
# Type aliases
JsonValue: TypeAlias = Union[None, bool, int, float, str, List["JsonValue"], Dict[str, "JsonValue"]]
ConnectionOptions: TypeAlias = Dict[str, Union[str, int, bool]]

# TypedDict for structured dictionaries
class UserData(TypedDict):
    id: int
    name: str
    email: str
    is_active: bool
    metadata: NotRequired[Dict[str, Any]]  # Optional key

class StrictUserData(TypedDict, total=True):  # All keys required
    id: int
    name: str
    email: str

# Callable types
ProcessFunc: TypeAlias = Callable[[str], str]
AsyncProcessFunc: TypeAlias = Callable[[str], Awaitable[str]]
CallbackFunc: TypeAlias = Callable[[int, str], None]

# Example usage
def apply_processor(data: str, processor: ProcessFunc) -> str:
    return processor(data)

async def apply_async_processor(data: str, processor: AsyncProcessFunc) -> str:
    return await processor(data)
```

### Generics

```python
from typing import TypeVar, Generic, List, Dict, Optional

# Simple generic
T = TypeVar('T')

def first_item(items: List[T]) -> Optional[T]:
    """Return the first item or None if empty."""
    return items[0] if items else None

# Bounded type variables
NumberT = TypeVar('NumberT', int, float)

def sum_values(values: List[NumberT]) -> NumberT:
    """Sum numeric values preserving type."""
    return sum(values) if values else type(values[0])(0)

# Generic classes
K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    """Generic cache implementation."""

    def __init__(self) -> None:
        self._cache: Dict[K, V] = {}

    def get(self, key: K) -> Optional[V]:
        return self._cache.get(key)

    def set(self, key: K, value: V) -> None:
        self._cache[key] = value

# Constrained type variables
StateT = TypeVar('StateT', bound='BaseState')

class Agent(Generic[StateT]):
    """Agent with typed state."""

    def __init__(self, state_class: type[StateT]) -> None:
        self.state_class = state_class
        self._state: Optional[StateT] = None

    def get_state(self) -> StateT:
        if self._state is None:
            self._state = self.state_class()
        return self._state
```

### Protocols

```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Comparable(Protocol):
    """Protocol for comparable objects."""

    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

class Persistable(Protocol):
    """Protocol for objects that can be persisted."""

    def save(self, path: Path) -> None: ...
    def load(self, path: Path) -> None: ...

    @property
    def is_dirty(self) -> bool: ...

# Using protocols
def sort_items[T: Comparable](items: List[T]) -> List[T]:
    """Sort items that implement Comparable protocol."""
    return sorted(items)

def backup_object(obj: Persistable, backup_path: Path) -> None:
    """Backup any persistable object."""
    if obj.is_dirty:
        obj.save(backup_path)
```

### Type Guards

```python
from typing import TypeGuard, Any, Dict

def is_valid_config(value: Any) -> TypeGuard[Dict[str, str]]:
    """Check if value is a valid configuration dictionary."""
    return (
        isinstance(value, dict) and
        all(isinstance(k, str) and isinstance(v, str)
            for k, v in value.items())
    )

def process_config(config: Any) -> None:
    if is_valid_config(config):
        # config is now typed as Dict[str, str]
        for key, value in config.items():
            print(f"{key}: {value}")
    else:
        raise ValueError("Invalid configuration")
```

### Literal Types and Overloading

```python
from typing import Literal, overload, Union

# Literal types
Mode = Literal["read", "write", "append"]
Format = Literal["json", "yaml", "toml"]

def open_file(path: Path, mode: Mode) -> None:
    """Open file with specific mode."""
    pass

# Overloading
@overload
def parse_value(value: str, type: Literal["int"]) -> int: ...

@overload
def parse_value(value: str, type: Literal["float"]) -> float: ...

@overload
def parse_value(value: str, type: Literal["bool"]) -> bool: ...

def parse_value(value: str, type: Literal["int", "float", "bool"]) -> Union[int, float, bool]:
    """Parse string value to specified type."""
    if type == "int":
        return int(value)
    elif type == "float":
        return float(value)
    else:
        return value.lower() in ("true", "1", "yes")
```

### Pydantic Models with Advanced Types

```python
from pydantic import BaseModel, Field, validator, root_validator
from typing import List, Dict, Optional, Union, Annotated
from datetime import datetime
from enum import Enum

class Status(str, Enum):
    """Status enumeration."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class TaskConfig(BaseModel):
    """Advanced task configuration with validation."""

    # Basic fields with constraints
    name: Annotated[str, Field(min_length=1, max_length=100)]
    priority: Annotated[int, Field(ge=1, le=10)] = 5
    timeout_seconds: Annotated[float, Field(gt=0)] = 60.0

    # Optional fields
    description: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    # Enum field
    status: Status = Status.PENDING

    # Datetime fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    scheduled_at: Optional[datetime] = None

    # Union types
    retry_policy: Union[int, Dict[str, Any]] = 3

    # Nested models
    dependencies: List["TaskConfig"] = Field(default_factory=list)

    # Validators
    @validator('name')
    def validate_name(cls, v: str) -> str:
        """Ensure name doesn't contain special characters."""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Name must be alphanumeric with _ or -')
        return v

    @validator('scheduled_at')
    def validate_scheduled_time(cls, v: Optional[datetime], values: Dict[str, Any]) -> Optional[datetime]:
        """Ensure scheduled time is in the future."""
        if v is not None and 'created_at' in values:
            if v <= values['created_at']:
                raise ValueError('Scheduled time must be after creation time')
        return v

    @root_validator
    def validate_dependencies(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure no circular dependencies."""
        # Implementation for circular dependency check
        return values

    class Config:
        """Pydantic configuration."""
        use_enum_values = True
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
```

## **init**.py Best Practices

### Package Level **init**.py

```python
"""Haive Core - Foundation for the Haive Agent Framework.

This package provides the core components for building intelligent agents:

- Base classes for agents, engines, and tools
- State management and schema composition
- Graph-based workflow execution
- Configuration and registry systems

Quick Start:
    >>> from haive.core import Agent, Engine, Tool
    >>> from haive.core.schema import StateSchema
    >>>
    >>> # Create a simple agent
    >>> agent = Agent(name="my_agent")
    >>> result = await agent.arun("Hello!")

Main Components:
    - Agent: Base class for all agents
    - Engine: LLM and tool execution engines
    - Graph: Workflow definition and execution
    - Schema: State management and composition
    - Registry: Global component registration

Version: 1.0.0
License: MIT
"""

# Version information
__version__ = "1.0.0"
__author__ = "Haive Team"
__email__ = "team@haive.ai"

# Core imports
from haive.core.agent import Agent, AgentConfig
from haive.core.engine import Engine, BaseEngine, AugLLMEngine
from haive.core.graph import Graph, Node, Edge
from haive.core.registry import Registry, get_registry
from haive.core.schema import StateSchema, SchemaComposer
from haive.core.tools import Tool, tool_decorator

# Type imports
from haive.core.types import (
    MessageType,
    StateType,
    ConfigType,
    EngineType,
)

# Exception imports
from haive.core.exceptions import (
    HaiveError,
    AgentError,
    EngineError,
    SchemaError,
    RegistryError,
)

# Utility imports
from haive.core.utils import (
    setup_logging,
    get_logger,
    load_config,
)

# Define public API
__all__ = [
    # Version info
    "__version__",
    "__author__",

    # Core classes
    "Agent",
    "AgentConfig",
    "Engine",
    "BaseEngine",
    "AugLLMEngine",
    "Graph",
    "Node",
    "Edge",
    "Registry",
    "get_registry",
    "StateSchema",
    "SchemaComposer",
    "Tool",
    "tool_decorator",

    # Types
    "MessageType",
    "StateType",
    "ConfigType",
    "EngineType",

    # Exceptions
    "HaiveError",
    "AgentError",
    "EngineError",
    "SchemaError",
    "RegistryError",

    # Utilities
    "setup_logging",
    "get_logger",
    "load_config",
]

# Package initialization
def _initialize_package() -> None:
    """Initialize package-level resources."""
    # Setup default logging
    setup_logging()

    # Register default components
    registry = get_registry()
    registry.register_defaults()

    # Validate environment
    _validate_environment()

def _validate_environment() -> None:
    """Validate runtime environment."""
    import sys

    # Check Python version
    if sys.version_info < (3, 10):
        raise RuntimeError(
            f"Haive requires Python 3.10+, got {sys.version}"
        )

    # Check required packages
    try:
        import pydantic
        import langgraph
    except ImportError as e:
        raise RuntimeError(
            f"Required dependency missing: {e.name}"
        )

# Run initialization
_initialize_package()

# Convenience functions
def create_agent(name: str, **kwargs) -> Agent:
    """Create an agent with default configuration.

    Args:
        name: Agent identifier
        **kwargs: Additional configuration options

    Returns:
        Configured agent instance
    """
    config = AgentConfig(name=name, **kwargs)
    return Agent(config)

def version_info() -> Dict[str, str]:
    """Get detailed version information.

    Returns:
        Dictionary with version details
    """
    return {
        "version": __version__,
        "author": __author__,
        "email": __email__,
        "python": sys.version,
        "dependencies": {
            "pydantic": pydantic.__version__,
            "langgraph": langgraph.__version__,
        }
    }
```

### Module Level **init**.py

```python
"""Schema module - State management and composition for Haive agents.

This module provides the schema system for managing agent state:

- StateSchema: Base class for all agent states
- SchemaComposer: Dynamic schema generation from engines
- Field management and validation
- State persistence and serialization

Example:
    >>> from haive.core.schema import StateSchema, Field
    >>>
    >>> class MyState(StateSchema):
    ...     messages: List[str] = Field(default_factory=list)
    ...     metadata: Dict[str, Any] = Field(default_factory=dict)
"""

# Public API imports
from .base import StateSchema, BaseSchema
from .composer import SchemaComposer, FieldInfo
from .fields import Field, create_field, merge_fields
from .validation import validate_state, ValidationError
from .serialization import serialize_state, deserialize_state

# Type exports
from .types import SchemaType, FieldType, ValidatorType

__all__ = [
    # Base schemas
    "StateSchema",
    "BaseSchema",

    # Composition
    "SchemaComposer",
    "FieldInfo",

    # Fields
    "Field",
    "create_field",
    "merge_fields",

    # Validation
    "validate_state",
    "ValidationError",

    # Serialization
    "serialize_state",
    "deserialize_state",

    # Types
    "SchemaType",
    "FieldType",
    "ValidatorType",
]

# Module metadata
__module_name__ = "schema"
__module_version__ = "1.0.0"

def __dir__():
    """Override dir() to show only public API."""
    return __all__
```

### Sub-package **init**.py

```python
"""RAG Agents - Retrieval-Augmented Generation agents.

This sub-package provides various RAG agent implementations:

- BaseRAGAgent: Foundation for RAG agents
- SimpleRAGAgent: Basic retrieval and generation
- AdaptiveRAGAgent: Dynamic retrieval strategies
- MultiSourceRAGAgent: Multiple knowledge sources

Components:
    - Retrievers: Document retrieval strategies
    - Rerankers: Result reranking algorithms
    - Generators: Response generation with context
    - Evaluators: Response quality assessment
"""

from .base import BaseRAGAgent, RAGConfig
from .simple import SimpleRAGAgent
from .adaptive import AdaptiveRAGAgent
from .multi_source import MultiSourceRAGAgent

# Retriever imports
from .retrievers import (
    VectorRetriever,
    KeywordRetriever,
    HybridRetriever,
    create_retriever,
)

# Reranker imports
from .rerankers import (
    CrossEncoderReranker,
    DiversityReranker,
    create_reranker,
)

# Utility imports
from .utils import (
    chunk_documents,
    create_embeddings,
    format_context,
)

__all__ = [
    # Agents
    "BaseRAGAgent",
    "RAGConfig",
    "SimpleRAGAgent",
    "AdaptiveRAGAgent",
    "MultiSourceRAGAgent",

    # Retrievers
    "VectorRetriever",
    "KeywordRetriever",
    "HybridRetriever",
    "create_retriever",

    # Rerankers
    "CrossEncoderReranker",
    "DiversityReranker",
    "create_reranker",

    # Utils
    "chunk_documents",
    "create_embeddings",
    "format_context",
]

# Lazy imports for optional dependencies
def __getattr__(name: str):
    """Lazy load optional components."""
    if name == "ChromaRetriever":
        try:
            from .retrievers.chroma import ChromaRetriever
            return ChromaRetriever
        except ImportError:
            raise ImportError(
                "ChromaRetriever requires 'chromadb' package. "
                "Install with: pip install haive[chroma]"
            )
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
```

## README Templates

### Package README Template

````markdown
# Haive Core

[![PyPI version](https://badge.fury.io/py/haive-core.svg)](https://badge.fury.io/py/haive-core)
[![Python Versions](https://img.shields.io/pypi/pyversions/haive-core.svg)](https://pypi.org/project/haive-core/)
[![License](https://img.shields.io/pypi/l/haive-core.svg)](https://github.com/haive/haive-core/blob/main/LICENSE)
[![Tests](https://github.com/haive/haive-core/workflows/Tests/badge.svg)](https://github.com/haive/haive-core/actions)
[![Coverage](https://codecov.io/gh/haive/haive-core/branch/main/graph/badge.svg)](https://codecov.io/gh/haive/haive-core)

Core framework for building intelligent agents with Haive.

## Features

- 🎯 **Flexible Agent Architecture** - Build agents with customizable behaviors
- 🔄 **State Management** - Robust state handling with schema validation
- 🔧 **Tool Integration** - Easy integration with external tools and APIs
- 📊 **Graph-Based Workflows** - Define complex agent behaviors as graphs
- 🚀 **Async First** - Built for performance with async/await
- 🔌 **Extensible** - Plugin system for custom components

## Installation

```bash
# Basic installation
pip install haive-core

# With optional dependencies
pip install haive-core[all]     # All optional features
pip install haive-core[dev]     # Development dependencies
pip install haive-core[docs]    # Documentation building
```
````

## Quick Start

```python
from haive.core import Agent, StateSchema
from haive.core.engine import AugLLMEngine

# Define your agent's state
class MyAgentState(StateSchema):
    messages: List[str] = []
    context: Dict[str, Any] = {}

# Create an agent
agent = Agent(
    name="my_assistant",
    state_schema=MyAgentState,
    engine=AugLLMEngine()
)

# Run the agent
result = await agent.arun("Hello, how can you help me?")
print(result)
```

## Core Concepts

### Agents

Agents are the primary building blocks in Haive. Each agent has:

- **State**: Managed data that persists across interactions
- **Engine**: LLM or tool execution backend
- **Graph**: Workflow definition for complex behaviors

```python
from haive.core import Agent
from haive.core.graph import Graph

class CustomAgent(Agent):
    def build_graph(self) -> Graph:
        graph = Graph()

        # Define nodes
        graph.add_node("process", self.process_input)
        graph.add_node("respond", self.generate_response)

        # Define edges
        graph.add_edge("process", "respond")
        graph.set_entry_point("process")

        return graph
```

### State Management

State schemas define the structure of agent memory:

```python
from haive.core.schema import StateSchema
from pydantic import Field

class ConversationState(StateSchema):
    messages: List[Message] = Field(default_factory=list)
    user_profile: Optional[UserProfile] = None
    session_id: str = Field(default_factory=lambda: str(uuid4()))

    def add_message(self, message: Message) -> None:
        self.messages.append(message)
        self.last_updated = datetime.utcnow()
```

### Tools

Integrate external functionality as tools:

```python
from haive.core.tools import tool

@tool
async def search_web(query: str, max_results: int = 5) -> List[SearchResult]:
    """Search the web for information."""
    # Implementation here
    return results

# Register with agent
agent.register_tool(search_web)
```

## Advanced Usage

### Custom Engines

```python
from haive.core.engine import BaseEngine

class CustomEngine(BaseEngine):
    async def invoke(self, input_data: Dict[str, Any]) -> Any:
        # Custom processing logic
        return result
```

### Middleware

```python
from haive.core.middleware import Middleware

class LoggingMiddleware(Middleware):
    async def process(self, state: StateSchema, next_handler):
        start_time = time.time()
        result = await next_handler(state)
        duration = time.time() - start_time
        logger.info(f"Processing took {duration:.2f}s")
        return result
```

### Persistence

```python
from haive.core.persistence import RedisPersistence

# Configure persistence backend
persistence = RedisPersistence(
    redis_url="redis://localhost:6379",
    ttl_seconds=3600
)

agent = Agent(
    name="persistent_agent",
    persistence=persistence
)
```

## Architecture

```
haive-core/
├── agent/          # Agent base classes and interfaces
├── engine/         # LLM and execution engines
├── graph/          # Graph-based workflow system
├── schema/         # State schema system
├── tools/          # Tool integration
├── middleware/     # Processing pipeline
└── persistence/    # State persistence backends
```

## Configuration

Configure Haive through environment variables or configuration files:

```python
# config.yaml
agent:
  default_timeout: 30
  max_retries: 3

engine:
  provider: openai
  model: gpt-4
  temperature: 0.7

logging:
  level: INFO
  format: json
```

Load configuration:

```python
from haive.core.config import load_config

config = load_config("config.yaml")
agent = Agent.from_config(config)
```

## Error Handling

Haive provides structured error handling:

```python
from haive.core.exceptions import AgentError, EngineError

try:
    result = await agent.arun(input_data)
except EngineError as e:
    # Handle engine-specific errors
    logger.error(f"Engine failed: {e}")
except AgentError as e:
    # Handle general agent errors
    logger.error(f"Agent error: {e}")
```

## Testing

Write tests for your agents:

```python
import pytest
from haive.core.testing import AgentTestCase

class TestMyAgent(AgentTestCase):
    async def test_basic_response(self):
        agent = await self.create_test_agent()
        response = await agent.arun("test input")

        assert response is not None
        assert len(response) > 0

    async def test_state_persistence(self):
        agent = await self.create_test_agent()

        # First interaction
        await agent.arun("My name is Alice")

        # Second interaction should remember
        response = await agent.arun("What's my name?")
        assert "Alice" in response
```

## Performance

Haive is designed for high performance:

- Async/await throughout for concurrent operations
- Connection pooling for external services
- Caching for expensive operations
- Streaming responses for large outputs

```python
# Stream responses
async for chunk in agent.astream("Generate a long story"):
    print(chunk, end="", flush=True)
```

## Debugging

Enable debug mode for detailed logging:

```python
import logging
from haive.core.logging import setup_logging

# Enable debug logging
setup_logging(level=logging.DEBUG)

# Use context manager for trace logging
from haive.core.debug import trace_context

async with trace_context() as trace:
    result = await agent.arun("Debug this")
    print(trace.get_timeline())
```

## Migration Guide

### From v0.x to v1.0

Key changes in v1.0:

1. **Async by default** - All agent methods are now async
2. **New state system** - Pydantic-based state schemas
3. **Graph workflows** - Replaced pipeline with graph-based system

```python
# Old (v0.x)
agent = Agent()
result = agent.run("input")

# New (v1.0)
agent = Agent()
result = await agent.arun("input")
```

## Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md) for details.

```bash
# Setup development environment
git clone https://github.com/haive/haive-core
cd haive-core
poetry install --with dev

# Run tests
poetry run pytest

# Run linting
poetry run ruff check src/
poetry run mypy src/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://docs.haive.ai)
- 💬 [Discord Community](https://discord.gg/haive)
- 🐛 [Issue Tracker](https://github.com/haive/haive-core/issues)
- 📧 [Email Support](mailto:support@haive.ai)

## Citation

If you use Haive in your research, please cite:

```bibtex
@software{haive2024,
  title = {Haive: A Framework for Intelligent Agents},
  author = {Haive Team},
  year = {2024},
  url = {https://github.com/haive/haive-core}
}
```

````

### Module README Template

```markdown
# Schema Module

Core state management and schema composition for Haive agents.

## Overview

The schema module provides:

- **StateSchema**: Base class for agent state definitions
- **SchemaComposer**: Dynamic schema generation from multiple sources
- **Field Management**: Utilities for field manipulation and validation
- **Serialization**: State persistence and restoration

## Quick Start

```python
from haive.core.schema import StateSchema, Field
from typing import List, Dict, Any

class MyAgentState(StateSchema):
    """Custom agent state."""

    messages: List[str] = Field(
        default_factory=list,
        description="Conversation history"
    )

    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional context"
    )

    def add_message(self, message: str) -> None:
        """Add a message to history."""
        self.messages.append(message)
````

## Schema Composition

Combine multiple schemas dynamically:

```python
from haive.core.schema import SchemaComposer

composer = SchemaComposer(base_schema=MyAgentState)

# Add fields from engines
for engine in engines:
    composer.add_engine_schema(engine)

# Generate final schema
FinalSchema = composer.compose()
```

## Field Operations

### Creating Fields

```python
from haive.core.schema import create_field

# Simple field
name_field = create_field(str, default="", description="User name")

# Complex field with validation
age_field = create_field(
    int,
    default=0,
    description="User age",
    ge=0,
    le=150
)
```

### Merging Fields

```python
from haive.core.schema import merge_fields

# Merge fields from multiple sources
merged = merge_fields([
    engine1.get_fields(),
    engine2.get_fields(),
    custom_fields
])
```

## Validation

Built-in validation with helpful error messages:

```python
from haive.core.schema import validate_state

try:
    state = MyAgentState(messages=123)  # Wrong type
except ValidationError as e:
    print(e.errors())
    # [{'loc': ('messages',), 'msg': 'value is not a valid list'}]
```

## Serialization

Save and restore state:

```python
from haive.core.schema import serialize_state, deserialize_state

# Save state
state_dict = serialize_state(agent_state)
json.dump(state_dict, file)

# Restore state
loaded_dict = json.load(file)
restored_state = deserialize_state(loaded_dict, MyAgentState)
```

## Advanced Features

### Custom Validators

```python
from pydantic import validator

class ValidatedState(StateSchema):
    email: str

    @validator('email')
    def validate_email(cls, v):
        if '@' not in v:
            raise ValueError('Invalid email')
        return v.lower()
```

### Dynamic Schemas

```python
def create_dynamic_schema(fields: Dict[str, Any]) -> type[StateSchema]:
    """Create schema class dynamically."""
    return type('DynamicState', (StateSchema,), fields)

# Usage
DynamicState = create_dynamic_schema({
    'field1': Field(str, default=""),
    'field2': Field(int, default=0)
})
```

### Schema Inheritance

```python
class BaseAgentState(StateSchema):
    """Common state for all agents."""
    id: str
    created_at: datetime

class SpecializedState(BaseAgentState):
    """Extended state with additional fields."""
    special_field: str
    tools_enabled: List[str] = []
```

## Performance Considerations

- Schemas are created once and reused
- Validation is optimized with Pydantic's Rust backend
- Large states can be chunked for serialization
- Use `exclude_unset=True` for minimal serialization

## API Reference

See the full [API documentation](https://docs.haive.ai/api/schema) for detailed reference.

## Testing

```python
import pytest
from haive.core.schema import StateSchema

def test_schema_creation():
    class TestState(StateSchema):
        value: int = 0

    state = TestState(value=42)
    assert state.value == 42
```

````

## Error Handling

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
````

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

### Parametrized Testing

```python
import pytest
from typing import List, Any

class TestSchemaValidation:
    """Test schema validation behaviors."""

    @pytest.mark.parametrize("field_type,value,expected", [
        (str, "hello", "hello"),
        (int, 42, 42),
        (float, 3.14, 3.14),
        (bool, True, True),
        (List[str], ["a", "b"], ["a", "b"]),
        (Dict[str, int], {"a": 1}, {"a": 1}),
    ])
    def test_field_type_validation(
        self,
        field_type: type,
        value: Any,
        expected: Any
    ) -> None:
        """Test field validation for various types."""
        from haive.core.schema import create_field

        field = create_field(field_type)
        validated = field.validate(value)
        assert validated == expected

    @pytest.mark.parametrize("invalid_value,error_match", [
        (123, "str type expected"),
        ([], "str type expected"),
        ({}, "str type expected"),
        (None, "none is not an allowed value"),
    ])
    def test_string_field_invalid_values(
        self,
        invalid_value: Any,
        error_match: str
    ) -> None:
        """Test string field rejects invalid values."""
        from haive.core.schema import create_field

        field = create_field(str)
        with pytest.raises(ValidationError, match=error_match):
            field.validate(invalid_value)
```

### Property-based Testing

```python
from hypothesis import given, strategies as st
from hypothesis import assume

class TestSchemaProperties:
    """Property-based tests for schema system."""

    @given(
        field_name=st.text(min_size=1, max_size=50),
        default_value=st.text(),
        description=st.text()
    )
    def test_field_creation_properties(
        self,
        field_name: str,
        default_value: str,
        description: str
    ) -> None:
        """Test field creation with random valid inputs."""
        assume(field_name.isidentifier())  # Valid Python identifier

        from haive.core.schema import create_field

        field = create_field(
            str,
            default=default_value,
            description=description
        )

        assert field.default == default_value
        assert field.description == description
        assert field.type_ == str
```

### Async Test Patterns

```python
import asyncio
import pytest

@pytest.mark.asyncio
class TestAsyncPatterns:
    """Test async behavior patterns."""

    async def test_concurrent_agent_execution(self) -> None:
        """Test agents can run concurrently."""
        agents = [
            SimpleAgent(name=f"agent_{i}")
            for i in range(5)
        ]

        # Run all agents concurrently
        tasks = [
            agent.arun(f"Process request {i}")
            for i, agent in enumerate(agents)
        ]

        results = await asyncio.gather(*tasks)

        assert len(results) == 5
        assert all(result is not None for result in results)

    async def test_agent_timeout_behavior(self) -> None:
        """Test agent handles timeouts gracefully."""
        agent = SimpleAgent(
            name="timeout_test",
            timeout=0.1  # 100ms timeout
        )

        # Simulate slow operation
        with patch.object(agent, '_process') as mock_process:
            async def slow_process(*args):
                await asyncio.sleep(1)  # Longer than timeout
                return "result"

            mock_process.side_effect = slow_process

            with pytest.raises(asyncio.TimeoutError):
                await agent.arun("test")
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

### Fixture Best Practices

```python
import pytest
from typing import Generator, AsyncGenerator

@pytest.fixture
def temp_directory() -> Generator[Path, None, None]:
    """Provide temporary directory for tests."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Provide async HTTP client."""
    async with AsyncClient() as client:
        yield client

@pytest.fixture(scope="session")
def shared_resource() -> Resource:
    """Expensive resource shared across tests."""
    resource = Resource()
    resource.initialize()
    yield resource
    resource.cleanup()

# Fixture factories
@pytest.fixture
def make_agent():
    """Factory fixture for creating agents."""
    created_agents = []

    def _make_agent(**kwargs) -> Agent:
        agent = Agent(**kwargs)
        created_agents.append(agent)
        return agent

    yield _make_agent

    # Cleanup
    for agent in created_agents:
        agent.cleanup()
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

# Good: Mock with realistic responses
class MockLLMEngine:
    """Mock LLM engine for testing."""

    def __init__(self, responses: Optional[Dict[str, str]] = None):
        self.responses = responses or {}
        self.call_count = 0
        self.last_input = None

    async def ainvoke(self, input_text: str) -> str:
        self.call_count += 1
        self.last_input = input_text

        # Return predefined response or generate one
        for pattern, response in self.responses.items():
            if pattern in input_text:
                return response

        return f"Mock response to: {input_text}"
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

### Error Recovery Pattern

```python
from typing import TypeVar, Callable, Optional
import asyncio

T = TypeVar('T')

async def retry_with_backoff(
    func: Callable[[], Awaitable[T]],
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True
) -> T:
    """Retry async function with exponential backoff.

    Args:
        func: Async function to retry
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries in seconds
        max_delay: Maximum delay between retries
        exponential_base: Base for exponential backoff
        jitter: Whether to add random jitter to delays

    Returns:
        Result from successful function call

    Raises:
        Last exception if all retries fail
    """
    delay = base_delay
    last_exception: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            return await func()
        except Exception as e:
            last_exception = e

            if attempt == max_retries:
                logger.error(
                    f"All {max_retries} retries failed",
                    extra={"last_error": str(e)}
                )
                raise

            # Calculate next delay
            if jitter:
                actual_delay = delay * (0.5 + random.random())
            else:
                actual_delay = delay

            logger.warning(
                f"Attempt {attempt + 1} failed, retrying in {actual_delay:.2f}s",
                extra={"error": str(e), "attempt": attempt + 1}
            )

            await asyncio.sleep(actual_delay)

            # Exponential backoff
            delay = min(delay * exponential_base, max_delay)

    # Should never reach here, but for type safety
    assert last_exception is not None
    raise last_exception

# Usage
async def fetch_with_retry(url: str) -> Dict[str, Any]:
    """Fetch URL with automatic retry on failure."""

    async def _fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()

    return await retry_with_backoff(_fetch)
```

### Context Management Pattern

```python
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Optional

class AgentContext:
    """Context manager for agent execution."""

    def __init__(self, agent: Agent):
        self.agent = agent
        self.start_time: Optional[float] = None
        self.metrics: Dict[str, Any] = {}

    async def __aenter__(self) -> "AgentContext":
        """Enter context and initialize resources."""
        self.start_time = time.time()
        await self.agent.initialize()

        logger.info(
            f"Agent {self.agent.name} context entered",
            extra={"agent_id": self.agent.id}
        )

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit context and cleanup resources."""
        duration = time.time() - self.start_time

        self.metrics.update({
            "duration": duration,
            "success": exc_type is None,
            "error": str(exc_val) if exc_val else None
        })

        await self.agent.cleanup()

        logger.info(
            f"Agent {self.agent.name} context exited",
            extra=self.metrics
        )

@asynccontextmanager
async def managed_agent_execution(
    agent: Agent
) -> AsyncGenerator[Agent, None]:
    """Manage agent lifecycle during execution."""

    async with AgentContext(agent):
        try:
            yield agent
        except Exception as e:
            logger.error(
                f"Error during agent execution: {e}",
                extra={"agent": agent.name}
            )
            raise
        finally:
            # Ensure state is persisted
            if hasattr(agent, 'persist_state'):
                await agent.persist_state()

# Usage
async def run_agent_with_context(agent: Agent, input_text: str) -> str:
    """Run agent with full context management."""

    async with managed_agent_execution(agent) as managed_agent:
        result = await managed_agent.arun(input_text)
        return result
```

---

This enhanced style guide provides comprehensive examples and templates for all aspects of Haive development. It should be treated as a living document and updated as the project evolves. All team members should follow these guidelines to ensure consistency and maintainability across the Haive codebase.
