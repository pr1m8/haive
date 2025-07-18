# CLAUDE.md - Haive Agent Framework

**Purpose**: Central memory hub for Haive development
**Version**: 4.0
**Last Updated**: 2025-01-15

## 🎯 Project Context

- **Directory**: `/home/will/Projects/haive/backend/haive`
- **Branch**: `feature/fix_everything`
- **Core Rules**:
  - Always use `poetry run` prefix for ALL Python commands
  - Real components only - NO MOCKS EVER in tests
  - Always use explicit imports: `from haive.core.*`

## 📚 Essential Documentation

### 🧠 Memory Index System

- **@memory_index/README.md** - Central memory index for all discoveries
- **@memory_index/quick_reference.md** - Most-used patterns and fixes
- **@memory_index/by_date/** - Chronological memory tracking
- **@project_docs/README.md** - Main project documentation hub

### Standards & Guides (Import for details)

- @project_docs/active/standards/coding/COMMAND_EXECUTION_GUIDE.md
- @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
- @project_docs/active/standards/testing/philosophy.md
- @project_docs/active/standards/git/workflow.md

### Architecture & Patterns

- @project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md
- @project_docs/active/architecture/meta_state_pattern.md
- @project_docs/active/architecture/agent_as_tool_pattern.md

## 🚀 Current Focus

- **Active Work**: MultiAgent Sequential Pattern (ReactAgent → SimpleAgent)
- **Issues**: @project_docs/sessions/active/current_issues.md
- **Recent Achievements**: See @memory_index/by_date/2025-01-16/

## 🔥 Git Safety Protocol (CRITICAL)

```bash
# BEFORE ANY WORK
git status && git diff

# BEFORE CREATING FILES
find . -name "similar_file*"  # Check if exists

# BEFORE COMMITTING
git diff --cached           # Review staged changes
trunk check --all          # Run linting
poetry run pytest          # Run tests

# COMMIT SAFELY
git add specific_file.py   # Add individually
git commit -m "feat: clear description"
```

## 🛠️ Most Used Commands

```bash
# Development (ALWAYS with poetry run)
poetry run python script.py
poetry run pytest packages/haive-agents/tests/ -v
poetry run python -c "from haive.core import *; print('Imports OK')"

# Quality Checks
trunk check --all
trunk check --fix --all
poetry run mypy packages/
poetry run ruff check

# Research Before Coding
find packages/ -name "*.py" | xargs grep -l "YourPattern" | head -5
```

## 📦 Project Structure

```
packages/
├── haive-core/     # Engines, graphs, schemas (foundation)
├── haive-agents/   # Agent implementations
├── haive-tools/    # Tool implementations
├── haive-games/    # Game environments
├── haive-mcp/      # MCP integration
└── haive-prebuilt/ # Pre-configured components

project_docs/
├── active/         # Current standards & architecture
├── sessions/       # Working memory
└── {package}/      # Package-specific docs
```

## 🎯 Critical Development Rules

1. **NO MOCKS EVER**: Test with real LLMs, real tools, real components
2. **Poetry Run Everything**: Never run Python directly
3. **Research First**: Check existing patterns before implementing
4. **Explicit Imports**: `from haive.core.engine import X` not `from engine import X`
5. **Pydantic Patterns**: Never override `__init__`, use Field validation
6. **Git Safety**: Always check diff before commits
7. **Use TodoWrite**: For planning and tracking

## 📝 Quick Code Reference

### Essential Imports

```python
# Core
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Agents
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.rag.base.agent import BaseRAGAgent

# Tools
from langchain_core.tools import Tool, tool
from langchain_core.messages import HumanMessage, AIMessage
```

### Agent Configuration Patterns

```python
# AugLLMConfig (NEVER set model parameter directly)
config = AugLLMConfig()  # Uses defaults
config = AugLLMConfig(
    temperature=0.7,
    max_tokens=1000,
    system_message="You are a helpful assistant"
)

# SimpleAgent
agent = SimpleAgent(
    name="my_agent",
    engine=config
)

# ReactAgent with tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

agent = ReactAgent(
    name="react_agent",
    engine=config,
    tools=[calculator]
)
```

### Testing Pattern (NO MOCKS)

```python
def test_agent_real_execution():
    """Test with REAL components."""
    config = AugLLMConfig()
    agent = SimpleAgent(engine=config)

    result = agent.run("Hello")
    assert isinstance(result, str)
    assert len(result) > 0
```

## 🧠 Incremental Development Workflow

### 1. Start Work Protocol

```bash
# Check current state
git status && git diff

# Load relevant memories
# @project_docs/haive-agents/README.md (if working on agents)
# @project_docs/haive-core/README.md (if working on core)

# Create session workspace
mkdir -p project_docs/claude_sessions/claude_$(date +%Y%m%d_%H%M%S)_${purpose}
```

### 2. Research & Plan (ALWAYS FIRST)

```bash
# Find existing patterns
find packages/ -name "*.py" | xargs grep -l "YourPattern" | head -5

# Check existing tests
find packages/ -name "test_*.py" | xargs grep -l "similar_concept"

# Use TodoWrite for planning
```

### 3. Build Incrementally (Test Each Step)

```python
# Step 1: Create minimal class
class MyAgent:
    def __init__(self):
        pass

# Step 2: Test basic creation
def test_agent_creation():
    agent = MyAgent()
    assert agent is not None

# Step 3: Add one feature
class MyAgent:
    def __init__(self, name: str):
        self.name = name

# Step 4: Test that feature
def test_agent_with_name():
    agent = MyAgent("test")
    assert agent.name == "test"

# Continue this pattern...
```

### 4. Testing Strategy - Build As You Go

#### Test File Locations

```
packages/haive-{package}/
├── src/haive/{package}/
│   └── my_module.py           # Your source code
└── tests/
    └── test_my_module.py      # Test for that module
```

#### Test Each Addition Immediately

```python
# ✅ CORRECT - Test each piece as you build
def test_step_1_basic_creation():
    """Test basic agent creation works."""
    agent = MyAgent()
    assert agent is not None

def test_step_2_with_config():
    """Test agent with configuration."""
    config = AugLLMConfig()
    agent = MyAgent(config=config)
    assert agent.config == config

def test_step_3_basic_execution():
    """Test basic agent execution."""
    agent = MyAgent(config=AugLLMConfig())
    result = agent.run("Hello")
    assert isinstance(result, str)
    assert len(result) > 0
```

#### Ask for Help When Stuck

```python
# When you encounter issues:
# 1. Check existing similar implementations
# 2. Look at test patterns in other packages
# 3. Ask specific questions like:
#    "How do other agents handle configuration?"
#    "What's the pattern for tool integration?"
#    "How should I structure this test?"
```

### 5. Memory Management for Agents & Instances

#### Agent-Specific Memories

```python
# When working with specific agents, load their memories:
# @project_docs/haive-agents/simple/patterns.md
# @project_docs/haive-agents/react/implementation.md
# @project_docs/haive-agents/rag/configuration.md

# For agent instances in tests:
# @project_docs/haive-agents/testing/real_component_patterns.md
```

#### Instance Management

```python
# When creating agent instances, document patterns:
# @project_docs/sessions/active/agent_instance_patterns.md

# Common instance patterns:
config = AugLLMConfig(temperature=0.1)  # Low temp for tests
agent = SimpleAgent(name="test_agent", engine=config)

# Store instance patterns for reuse
test_config = AugLLMConfig(temperature=0.0)  # Deterministic
```

## 🔗 Package Import Hierarchy

```
# ALLOWED:
- Core → standard library, third-party
- Agents → core, standard library, third-party
- Tools → core, standard library, third-party
- Games → core, agents, tools, third-party

# FORBIDDEN:
- Core → agents/tools/games (circular!)
```

## 🎨 Coding Style & Standards

### Python Code Style

```python
# ✅ CORRECT - Descriptive names, type hints, early returns
def process_agent_response(
    agent_response: str,
    validation_config: ValidationConfig
) -> ProcessedResponse:
    """Process agent response with validation.

    Args:
        agent_response: Raw response from agent
        validation_config: Configuration for validation rules

    Returns:
        ProcessedResponse with validation results

    Raises:
        ValidationError: If response fails validation
    """
    if not agent_response:
        raise ValidationError("Empty response")

    if not validation_config.enabled:
        return ProcessedResponse(content=agent_response, validated=False)

    # Process with validation
    validated_content = validate_response(agent_response, validation_config)
    return ProcessedResponse(
        content=validated_content,
        validated=True,
        validation_score=validated_content.score
    )

# ❌ WRONG - Poor naming, no types, nested logic
def process(resp, config):
    if resp:
        if config:
            if config.enabled:
                return validate_response(resp, config)
            else:
                return resp
        else:
            return resp
    else:
        return None
```

### Pydantic Model Patterns

```python
# ✅ CORRECT - Proper Pydantic usage
class AgentConfig(BaseModel):
    """Configuration for agent behavior."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid"
    )

    name: str = Field(..., min_length=1, max_length=50)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    tools: List[str] = Field(default_factory=list)

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores")
        return v

# Usage - Pydantic handles initialization automatically
config = AgentConfig(name="my_agent", temperature=0.8)
# Pydantic validates all fields and creates the instance
```

### Error Handling Patterns

```python
# ✅ CORRECT - Structured error handling
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def execute_agent_safely(
    agent: Agent,
    input_data: str
) -> Optional[AgentResponse]:
    """Execute agent with comprehensive error handling."""
    try:
        logger.info(f"Executing agent {agent.name} with input length {len(input_data)}")

        response = agent.run(input_data)

        if not response:
            logger.warning(f"Agent {agent.name} returned empty response")
            return None

        logger.info(f"Agent {agent.name} completed successfully")
        return response

    except ValidationError as e:
        logger.error(f"Validation error in agent {agent.name}: {e}")
        raise AgentValidationError(f"Agent validation failed: {e}")

    except Exception as e:
        logger.error(f"Unexpected error in agent {agent.name}: {e}")
        raise AgentExecutionError(f"Agent execution failed: {e}")

# ❌ WRONG - Silent failures, print statements
def bad_execute(agent, input_data):
    try:
        result = agent.run(input_data)
        print(f"Got result: {result}")  # Use logger!
        return result
    except:
        print("Something went wrong")   # No error context!
        return None                     # Silent failure!
```

### Testing Patterns (NO MOCKS)

```python
# ✅ CORRECT - Real component testing with descriptive names
def test_simple_agent_handles_basic_conversation_with_real_llm():
    """Test SimpleAgent maintains conversation context with real LLM."""
    config = AugLLMConfig(temperature=0.1)  # Low for consistency
    agent = SimpleAgent(name="test_conversation", engine=config)

    # First exchange
    response1 = agent.run("My name is Alice")
    assert isinstance(response1, str)
    assert len(response1) > 0

    # Second exchange - should remember context
    response2 = agent.run("What's my name?")
    assert "alice" in response2.lower()

    # Verify state persistence
    assert len(agent.conversation_history) >= 4  # 2 user + 2 assistant

def test_react_agent_with_real_calculator_tool_integration():
    """Test ReactAgent uses real calculator tool correctly."""
    @tool
    def calculator(expression: str) -> str:
        """Real calculator tool."""
        return str(eval(expression))

    config = AugLLMConfig(temperature=0.1)
    agent = ReactAgent(
        name="test_calculator",
        engine=config,
        tools=[calculator]
    )

    result = agent.run("What is 15 * 23?")
    assert "345" in str(result)
    assert agent.tool_calls_made > 0

# ❌ WRONG - Mocks, vague names, no real testing
def test_agent():  # Vague name!
    mock_llm = Mock()  # NO MOCKS!
    mock_llm.return_value = "fake response"
    agent = SimpleAgent(llm=mock_llm)
    result = agent.run("test")
    assert result == "fake response"  # Tests nothing real!
```

## 🚨 Common Pitfalls to Avoid

1. **Running Python without poetry run** → ImportError
2. **Using mocks in tests** → False confidence
3. **Generic imports** → Use explicit haive.core.\*
4. **Overriding Pydantic **init\*\*\*\* → Breaks validation
5. **Using print() instead of logger** → Poor debugging
6. **git add .** → Stage files individually
7. **Building without testing** → Large broken changes
8. **Not asking for help** → Stuck for hours on solvable problems
9. **Skipping research phase** → Reinventing existing patterns
10. **Testing at the end** → Hard to debug failures

## 📊 MCP Integration (Recommended)

### Quick Setup for Common Tools

```bash
# PostgreSQL - Database operations
claude mcp add haive-db -s user -- npx -y @modelcontextprotocol/server-postgres "postgresql://localhost/haive"

# Filesystem - Enhanced file operations
claude mcp add haive-files -s user -- npx -y @modelcontextprotocol/server-filesystem /home/will/Projects/haive

# GitHub - Repository management
claude mcp add haive-github -s user -e GITHUB_TOKEN=$GITHUB_TOKEN -- npx -y @modelcontextprotocol/server-github

# List configured servers
claude mcp list
```

See: @project_docs/claude_documentation/MCP_SETUP.md for complete setup guide with 8+ servers

## 🆘 When to Ask for Help

### Don't Stay Stuck - Ask Specific Questions

```python
# ✅ GOOD - Specific questions with context
"I'm implementing a ReactAgent with tools but getting ImportError on langchain_core.tools.
I've checked that langchain is installed with poetry show. What should I check next?"

"My agent test passes but the agent isn't actually using the tools I provided.
Here's my test code: [code]. What's the pattern for testing tool usage?"

"I'm following the MetaStateSchema pattern but getting a Pydantic validation error
when trying to embed my agent. The error is: [error]. How do I fix this?"

# ❌ BAD - Vague questions
"My code doesn't work"
"I'm getting an error"
"How do I make an agent?"
```

### When to Ask vs When to Research

```python
# ✅ RESEARCH FIRST - Common patterns
find packages/ -name "*.py" | xargs grep -l "similar_problem"
# Look at existing agent implementations
# Check test files for patterns

# ✅ ASK FOR HELP - After research doesn't work
"I found 3 similar implementations [X, Y, Z] but none handle my specific case of [description].
What's the best approach for [specific problem]?"

# ✅ ASK FOR HELP - Time-sensitive issues
"I'm getting a blocking error that's preventing all tests from running: [error]"

# ✅ ASK FOR HELP - Architecture decisions
"Should I extend SimpleAgent or create a new agent type for [use case]?"
```

### Debugging Workflow

```bash
# 1. Check the basics
poetry run python -c "import haive.core; print('Core imports OK')"
poetry run python -c "import haive.agents; print('Agents imports OK')"
git status && git diff

# 2. Run minimal test
poetry run python -c "
from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
config = AugLLMConfig()
agent = SimpleAgent(engine=config)
print('Basic agent creation works')
"

# 3. If still stuck, ask for help with:
# - What you're trying to do
# - What you've tried
# - Exact error message
# - Minimal reproduction code
```

## 🔍 Quick Debugging

### Runtime Agent Debugging

```python
# ✅ ALWAYS use debug=True when developing/testing agents
agent = SimpleAgent(name="test_agent", engine=config)
result = agent.run("Hello", debug=True)  # Shows detailed execution info

# For ReactAgent with tools
agent = ReactAgent(name="debug_agent", engine=config, tools=[calculator])
result = agent.run("Calculate 15 * 23", debug=True)  # Shows tool calls, reasoning steps

# For async agents
result = await agent.arun("Hello", debug=True)  # Async version with debug info

# ✅ ALWAYS logically check outputs
print(f"Agent result: {result}")
print(f"Result type: {type(result)}")
print(f"Result length: {len(str(result))}")

# Check if result makes sense
if "345" in str(result):
    print("✅ Calculation appears correct")
else:
    print("❌ Expected calculation result not found")

# For structured outputs, check fields
if hasattr(result, 'content'):
    print(f"Content: {result.content}")
if hasattr(result, 'metadata'):
    print(f"Metadata: {result.metadata}")
```

### Environment Debugging

```bash
# Check imports work
poetry run python -c "from haive.core import *; from haive.agents import *"

# Verify environment
poetry env info
which python  # Should show .venv path

# Fix common issues
poetry install --all-extras
poetry cache clear pypi --all
```

### Documentation Build Debugging

```bash
# Build docs (check for errors)
nox -s docs

# Quick build test
poetry run sphinx-build -b html docs/source docs/build/html -W --keep-going

# Check for syntax errors in examples
find packages -name "*.py" -exec python -m py_compile {} \; 2>&1 | grep -E "Error|Sorry"

# Find files with invalid names (spaces, parentheses)
find . -name "*\ *" -o -name "*(*" -o -name "*)*"

# View docs locally
python -m http.server 8003 --directory docs/build/html/
# Then open http://localhost:8003
```

📚 **Documentation Memories**:

- @memory_index/by_task/documentation/ - All documentation-related memories
- @memory_index/by_error/build_errors/ - Build error solutions
- @memory_index/quick_reference.md - Common patterns and fixes

## 🧪 Testing: NO MOCKS + Proper Structure

### Test File Organization

```
packages/haive-{package}/
├── src/haive/{package}/
│   └── my_module.py           # Your source code
└── tests/
    └── test_my_module.py      # Test for that module

# ALWAYS: Test files go in packages/haive-*/tests/
# NEVER: Create test files in root or random locations

# For nested modules, mirror the source structure:
packages/haive-agents/
├── src/haive/agents/
│   └── reasoning_and_critique/
│       └── self_discover/
│           └── agent.py
└── tests/
    └── reasoning_and_critique/
        └── self_discover/
            └── test_agent.py   # Mirror the directory structure
```

### Running Tests

```bash
# Run all tests in a package
poetry run pytest packages/haive-agents/tests/ -v

# Run specific test subdirectory
poetry run pytest packages/haive-agents/tests/multi/ -v
poetry run pytest packages/haive-agents/tests/rag/ -v

# Run single test file
poetry run pytest packages/haive-agents/tests/multi/test_simple_multi_agent.py -v

# Run specific test function
poetry run pytest packages/haive-agents/tests/multi/test_simple_multi_agent.py::test_sequential_execution -v

# Run with coverage
poetry run pytest packages/haive-agents/tests/ --cov=haive.agents --cov-report=html

# Run tests matching pattern
poetry run pytest -k "test_react" -v
```

## 📂 File Organization Standards

### Project File Structure

```
haive/
├── packages/              # All package code
│   ├── haive-core/
│   │   ├── src/          # Source code
│   │   └── tests/        # Test files organized by module
│   │       ├── graph/    # Graph-related tests
│   │       ├── memory/   # Memory system tests
│   │       ├── schema/   # Schema tests
│   │       └── persistence/ # Persistence tests
│   ├── haive-agents/
│   │   ├── src/
│   │   └── tests/
│   │       ├── multi/    # Multi-agent tests
│   │       ├── rag/      # RAG agent tests
│   │       ├── planning/ # Planning agent tests
│   │       ├── research/ # Research agent tests
│   │       └── reasoning/ # Reasoning agent tests
│   └── ...
├── scripts/              # Utility scripts
│   ├── maintenance/      # Maintenance and fix scripts
│   │   ├── docs/        # Documentation build scripts
│   │   └── agents/      # Agent enhancement scripts
│   └── debug/           # Debug utilities
├── project_docs/         # Documentation
│   ├── active/          # Current standards
│   ├── summaries/       # Implementation summaries
│   ├── guides/          # User guides
│   ├── build-reports/   # Build and test reports
│   ├── issues/          # Issue tracking
│   └── plans/           # Architecture plans
├── examples/            # Example scripts
└── docs/                # Sphinx documentation

# Files that MUST stay in root:
- CLAUDE.md              # This file - central memory
- README.md              # Project readme
- pyproject.toml         # Poetry configuration
- noxfile.py            # Nox automation
- .gitignore            # Git ignore rules
```

### Creating New Files

```bash
# ALWAYS check if similar file exists first
find packages/ -name "*similar_pattern*" -type f

# Create test file in correct location
# For agent tests:
touch packages/haive-agents/tests/category/test_new_feature.py

# For core tests:
touch packages/haive-core/tests/module/test_new_component.py

# For scripts:
touch scripts/maintenance/category/new_script.py

# For documentation:
touch project_docs/category/new_doc.md
```

### Moving Files to Proper Locations

```bash
# If you accidentally create a test in root:
mv test_something.py packages/haive-agents/tests/appropriate_category/

# If you create a debug script in root:
mv fix_something.py scripts/debug/

# If you create documentation in root:
mv SOMETHING_SUMMARY.md project_docs/summaries/
```

## 📚 Documentation Standards

### Google-Style Docstrings (Required for Sphinx AutoAPI)

```python
def process_agent_data(
    agent_name: str,
    data: List[Dict[str, Any]],
    config: Optional[ProcessConfig] = None,
    validate: bool = True
) -> ProcessResult:
    """Process raw agent data with optional validation.

    This function takes raw agent data and processes it according to
    the provided configuration. It supports batch processing and
    optional validation.

    Args:
        agent_name: Name of the agent processing the data.
        data: List of dictionaries containing raw data entries.
            Each entry must have 'id' and 'content' keys.
        config: Optional configuration for processing behavior.
            If None, uses default configuration.
        validate: Whether to validate data before processing.
            Defaults to True.

    Returns:
        ProcessResult: Object containing:
            - processed_data: List of processed entries
            - errors: List of any errors encountered
            - metadata: Processing metadata including timing

    Raises:
        ValueError: If agent_name is empty or data is malformed.
        ProcessingError: If processing fails after retries.
        ValidationError: If validate=True and data fails validation.

    Examples:
        Basic usage:

        >>> data = [{'id': 1, 'content': 'Hello'}]
        >>> result = process_agent_data('analyzer', data)
        >>> print(result.processed_data)
        [{'id': 1, 'content': 'Hello', 'processed': True}]

        With configuration:

        >>> config = ProcessConfig(batch_size=10, timeout=30)
        >>> result = process_agent_data('analyzer', data, config=config)

    Note:
        This function is thread-safe and can be used in concurrent
        processing pipelines. For large datasets, consider using
        the async version: process_agent_data_async().

    See Also:
        process_agent_data_async: Async version of this function.
        ProcessConfig: Configuration options documentation.
        validate_agent_data: Standalone validation function.
    """
```

### Class Documentation

```python
class AgentProcessor:
    """Handles processing of agent-specific data streams.

    This class provides a high-level interface for processing
    data streams from various agent types. It supports real-time
    and batch processing modes.

    Attributes:
        name: Processor identifier.
        config: Current processing configuration.
        metrics: Performance metrics collector.
        is_running: Whether processor is actively processing.

    Example:
        >>> processor = AgentProcessor(
        ...     name="main_processor",
        ...     config=ProcessConfig(mode="realtime")
        ... )
        >>> processor.start()
        >>> processor.process(data_stream)
    """

    def __init__(
        self,
        name: str,
        config: ProcessConfig,
        metrics_enabled: bool = True
    ):
        """Initialize the agent processor.

        Args:
            name: Unique processor identifier.
            config: Processing configuration.
            metrics_enabled: Whether to collect metrics.
        """
```

### Module Documentation

```python
"""Agent processing utilities for the Haive framework.

This module provides core functionality for processing agent data
streams, including validation, transformation, and persistence.

Key Features:
    - Real-time and batch processing modes
    - Automatic retry with exponential backoff
    - Comprehensive validation framework
    - Performance metrics collection

Basic Usage:
    >>> from haive.core.processing import AgentProcessor
    >>> processor = AgentProcessor("main", config)
    >>> result = processor.process(data)

Advanced Usage:
    See the examples/ directory for complex processing pipelines
    and integration patterns.

Module Structure:
    - processor.py: Main AgentProcessor class
    - validators.py: Data validation utilities
    - transformers.py: Data transformation functions
    - metrics.py: Performance monitoring

See Also:
    - haive.agents: Agent implementations
    - haive.core.engine: Processing engines
"""
```

### README.md Structure for Packages

````markdown
# haive-agents

Agent implementations for the Haive framework.

## Overview

This package provides various agent types including:

- SimpleAgent: Basic conversational agents
- ReactAgent: Reasoning and action agents with tool use
- RAG Agents: Retrieval-augmented generation agents
- Multi-Agent Systems: Coordinated agent groups

## Installation

```bash
poetry add haive-agents
```
````

## Quick Start

```python
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent
config = AugLLMConfig(temperature=0.7)
agent = SimpleAgent(name="assistant", engine=config)

# Use agent
response = agent.run("Hello, how can you help?")
```

## Features

- **Type Safety**: Full type hints and Pydantic models
- **Real Components**: No mocks, tested with real LLMs
- **Extensible**: Easy to create custom agents
- **Async Support**: All agents support async execution

## Documentation

- [API Reference](https://haive.readthedocs.io/api/agents)
- [User Guide](../../project_docs/guides/agents_guide.md)
- [Examples](../../examples/agents/)

## Testing

```bash
poetry run pytest packages/haive-agents/tests/
```

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md)

````

### Using '@' for Memory References

```python
# In code comments and docstrings, use @ to reference memories:

def complex_implementation():
    """Implement complex multi-agent pattern.

    This implementation follows the pattern described in
    @project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md

    For state management details, see:
    @project_docs/active/architecture/meta_state_pattern.md
    """

    # Load configuration as per @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
    config = load_config()

    # Follow testing approach from @project_docs/active/standards/testing/philosophy.md
    validate_real_components(config)
````

### Documentation Hierarchy

```
1. Code-Level Documentation (Highest Priority)
   - Google-style docstrings on ALL public functions/classes
   - Type hints on ALL parameters and returns
   - Examples in docstrings for complex functions

2. Module-Level Documentation
   - Module docstring explaining purpose and structure
   - README.md in each package root
   - __init__.py docstrings for public API

3. Package-Level Documentation
   - Comprehensive README.md with examples
   - API reference (auto-generated by Sphinx)
   - Migration guides for version changes

4. Project-Level Documentation
   - project_docs/ for architecture and decisions
   - Memory documents with @ references
   - Implementation guides and patterns
```

### Sphinx AutoAPI Configuration

```python
# docs/source/conf.py additions for AutoAPI
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',  # For Google-style docstrings
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_autodoc_typehints',
    'autoapi.extension',
]

# AutoAPI configuration
autoapi_type = 'python'
autoapi_dirs = [
    '../../packages/haive-core/src',
    '../../packages/haive-agents/src',
    '../../packages/haive-tools/src',
]
autoapi_options = [
    'members',
    'undoc-members',
    'show-inheritance',
    'show-module-summary',
    'imported-members',
]

# Napoleon settings for Google-style
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
```

### Documentation Checklist

```markdown
## Before Committing Code

- [ ] All public functions have Google-style docstrings
- [ ] All parameters have type hints
- [ ] Return types are specified
- [ ] Complex functions include Examples section
- [ ] Exceptions are documented in Raises section
- [ ] Related functions listed in See Also section
- [ ] Module has comprehensive docstring
- [ ] Package has updated README.md
- [ ] Memory references use @ notation
- [ ] Run `poetry run sphinx-build -b html docs/source docs/build`
```

### Writing Tests - NO MOCKS PATTERN

```python
# packages/haive-agents/tests/test_simple_agent.py

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

def test_simple_agent_real_execution():
    """Test with REAL components - NO MOCKS."""
    # Create real config (don't set model param)
    config = AugLLMConfig()

    # Create real agent
    agent = SimpleAgent(engine=config)

    # Test real behavior
    result = agent.run("Hello")
    assert isinstance(result, str)
    assert len(result) > 0

# ❌ NEVER USE MOCKS
# ✅ ALWAYS USE REAL COMPONENTS
```

### Build-Test-Build Pattern

```python
# Step 1: Write minimal test
def test_agent_creation():
    """Test agent can be created."""
    agent = MyAgent()
    assert agent is not None

# Step 2: Write minimal code to pass
class MyAgent:
    def __init__(self):
        pass

# Step 3: Run test
poetry run pytest tests/test_my_agent.py::test_agent_creation -v

# Step 4: Add next feature test
def test_agent_with_config():
    """Test agent accepts configuration."""
    config = AugLLMConfig()
    agent = MyAgent(config=config)
    assert agent.config == config

# Step 5: Update code to pass
class MyAgent:
    def __init__(self, config=None):
        self.config = config

# Continue this pattern...
```

---

**Remember**: This file loads at every session. Keep frequently-used info here, import the rest!
