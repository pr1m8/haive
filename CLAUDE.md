# CLAUDE.md - Haive Agent Framework Memory Hub

**Purpose**: Central routing and quick access to Haive development resources  
**Version**: 3.0  
**Last Updated**: 2025-01-09

## 🎯 Quick Access

- **Working Directory**: `/home/will/Projects/haive/backend/haive`
- **Active Branch**: `feature/engine-typing-generics`
- **Main Commands**: Always use `poetry run` for all operations
- **Test Pattern**: Real components only, NO MOCKS EVER
- **Import Pattern**: `from haive.core.*` (explicit package references)

## 📁 Memory Organization

### Core Memories (Import these as needed)

- **Command Execution**: @project_docs/active/standards/coding/COMMAND_EXECUTION_GUIDE.md - CRITICAL: Always use `poetry run`
- **Memory System**: @project_docs/active/standards/documentation/memory_system.md - Memory architecture and principles
- **Development Workflow**: @project_docs/active/standards/coding/development_workflow.md - Complete development methodology
- **Build & Test**: @project_docs/active/standards/coding/BUILD_AND_TEST_GUIDE.md - Trunk, nox, and testing procedures
- **Agent Configuration**: @project_docs/active/standards/coding/AGENT_CONFIGURATION_GUIDE.md - AugLLM, Simple, React, RAG agent patterns
- **Pydantic Patterns**: @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md - Proper Pydantic usage and anti-patterns
- **Code Style**: @project_docs/active/standards/coding/style_guide.md - Python coding standards
- **Testing**: @project_docs/active/standards/testing/philosophy.md - No-mocks testing approach
- **Git Workflow**: @project_docs/active/standards/git/workflow.md - Git best practices

### Package-Specific Memories

- **haive-agents**: @project_docs/haive-agents/README.md - Agent development guide
- **haive-core**: @project_docs/haive-core/README.md - Core architecture
- **haive-games**: @project_docs/haive-games/README.md - Games framework
- **haive-tools**: @project_docs/haive-tools/README.md - Tool implementations
- **haive-mcp**: @project_docs/haive-mcp/README.md - MCP integration

### Current Work Context

- **Active Issues**: @project_docs/sessions/active/current_issues.md
- **Sprint Progress**: @project_docs/sessions/active/current_sprint.md
- **MultiAgent Memory Hub**: @project_docs/active/architecture/multi_agent_meta_agent_memory_hub.md ✅ **UPDATED**
- **Recent Sessions**: @project_docs/sessions/active/README.md

### ✅ Recent Achievements (2025-01-13)

1. **MetaAgentState Validation** - Real Azure OpenAI execution with SimpleAgentV2
2. **Recompilation Mixin Testing** - Dynamic tool addition working (2 → 3 tools)
3. **No-Mocks Architecture** - 100% real component integration validated

## 🚀 Current Focus Areas

### 🔄 Active Development - MultiAgent Sequential Pattern

1. **ReactAgent → SimpleAgent Flow** - Sequential execution with structured output
2. **Cross-Agent Data Transfer** - State management between agents
3. **Real Component Testing** - No mocks, full Azure OpenAI integration
4. **Multi-Agent State Schema** - Coordinated state without flattening

### ✅ Completed Development

1. **MetaAgentState** - Agent embedding and execution working
2. **Recompilation Mixin** - Dynamic tool changes with auto-recompilation
3. **Schema Composition** - Engine-based state generation
4. **Engine Typing** - Proper generics implementation

### Known Critical Issues

- Schema field conflicts with multiple engines
- Import cycles in agent/engine dependencies
- See full list: @project_docs/claude_sessions/current_issues.md

## 🧠 Smart Memory Protocol

### Session Start Checklist

```bash
# 1. Check current state
git status && git diff

# 2. Load relevant package memory
# Read the specific package README you're working on

# 3. Create session workspace
mkdir -p project_docs/claude_sessions/claude_$(date +%Y%m%d_%H%M%S)_{purpose}

# 4. Use TodoWrite for planning
```

### During Development

1. **Track Progress**: Update @project_docs/progress_tracking/current_sprint.md
2. **Document Issues**: Add to @project_docs/claude_sessions/current_issues.md
3. **Save Patterns**: Document in session memory for reuse
4. **Cross-Reference**: Use [MEM-XXX] tags for navigation

### After Tasks

1. **Update Status**: Mark todos complete
2. **Document Learning**: Add to relevant package docs
3. **Clean Up**: Move completed work to archives
4. **Commit Properly**: Follow @project_docs/GIT_WORKFLOW.md

## 🔗 Essential Paths

```bash
# Source code locations
packages/haive-{package}/src/haive/{package}/
packages/haive-{package}/tests/

# Documentation hierarchy
project_docs/
├── claude_documentation/     # Claude-specific guides
├── {package_name}/          # Package documentation
├── claude_sessions/         # Work session memories
└── progress_tracking/       # Sprint and task tracking

# Key files to know
~/.claude/CLAUDE.md          # Global preferences (DO NOT MODIFY)
./CLAUDE.local.md           # Local overrides (if needed)
./pyproject.toml            # Workspace dependencies
```

## 🔥 GIT SAFETY FIRST - ALWAYS CHECK BEFORE ACTING

### MANDATORY Git Workflow - Run EVERY TIME

```bash
# 1. BEFORE ANY WORK - See what's changed
git status                    # What files are modified?
git diff                      # What exact changes were made?
git diff --cached             # What's staged for commit?

# 2. BEFORE CREATING FILES - Check if it exists
find . -name "similar_file*"  # Don't duplicate existing work

# 3. AFTER MAKING CHANGES - Review everything
git diff                      # Review your changes line by line
git status                    # Confirm which files you touched

# 4. BEFORE COMMITTING - Final safety check
git diff --cached             # Review what you're about to commit
trunk check --all             # Run linting
poetry run pytest             # Run tests

# 5. SAFE COMMIT PROCESS
git add specific_file.py      # Add files individually (NOT git add .)
git diff --cached             # Review staged changes AGAIN
git commit -m "feat: clear description"
```

### Git Commands You MUST Use

```bash
# CRITICAL - Use these constantly
git status                    # Current state - RUN OFTEN
git diff                      # Unstaged changes - REVIEW CAREFULLY
git diff --cached             # Staged changes - CHECK BEFORE COMMIT
git log --oneline -5          # Recent commits
git diff HEAD~1               # What changed in last commit

# USEFUL - For specific situations
git stash                     # Save work temporarily
git checkout -- file.py       # Undo changes to specific file
git reset HEAD file.py        # Unstage a file
```

## ⚡ Most Used Commands

```bash
# BEFORE ANY WORK - Research existing patterns
find packages/ -name "*.py" | xargs grep -l "YourPattern" | head -5

# Quality checks (ALWAYS run before committing)
trunk check --all                      # Primary linting tool
trunk check --fix --all                # Fix auto-fixable issues

# Development
poetry run python -m haive.agents.simple --example
poetry run pytest packages/haive-agents/tests/ -v
poetry run python -c "from haive.core import *; print('Imports OK')"

# Type checking and additional quality
poetry run mypy packages/haive-{package}/src/
poetry run ruff check packages/haive-{package}/

# Testing specific components
poetry run pytest packages/haive-{package}/tests/test_specific.py -v
poetry run pytest --cov=haive --cov-report=html
```

## 📊 Package Structure

```
haive/
├── core/      # Engines, graphs, schemas (foundation)
├── agents/    # Agent implementations (simple, react, rag)
├── tools/     # Tool implementations (math, web, file)
├── games/     # Game implementations (chess, go, puzzles)
├── dataflow/  # Streaming and data management
├── mcp/       # Model Context Protocol integration
└── prebuilt/  # Pre-configured components
```

### Package File Structure

```
packages/haive-{package}/
├── src/haive/{package}/        # Source code
│   ├── __init__.py            # Public exports
│   ├── base/                  # Base classes/interfaces
│   └── {feature}/             # Feature modules
├── tests/                     # REAL component tests
│   ├── conftest.py           # Shared fixtures
│   └── test_{feature}.py     # Test files
└── pyproject.toml            # Package dependencies
```

## 🎯 Development Patterns

### Import Hierarchy (CRITICAL)

```python
# Core can only import from: standard library, third-party
# Agents can import from: core, standard library, third-party
# Tools can import from: core, standard library, third-party
# Games can import from: core, agents, tools, third-party

# NEVER: Core importing from agents/tools/games (circular!)
```

### Standard Patterns

- **Configs**: Always use Pydantic models with validation
- **Errors**: Structured logging, never print()
- **State**: Use StateSchema for all agent states
- **Testing**: Real components, descriptive test names
- **Docs**: Google-style docstrings for Sphinx

### Schema Inheritance Patterns

```python
# Check existing schemas FIRST!
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from haive.core.schema.prebuilt.messages.messages_with_token_usage import MessagesStateWithTokenUsage

# When extending schemas, check what they expect:
# - MessagesState has: messages field
# - MessagesStateWithTokenUsage has: messages + token_usage fields
# - MetaStateSchema has: agent, agent_state, meta fields

# Example: Extending properly
class MyCustomState(MessagesStateWithTokenUsage):
    """Extends with token tracking built-in"""
    custom_field: str = Field(default="")
```

## 🔧 Common Imports & Configuration Patterns

### Essential Imports

```python
# Core engine configurations
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.meta_state import MetaStateSchema

# Agent types
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.rag.base.agent import BaseRAGAgent

# LangChain core tools
from langchain_core.tools import Tool
from langchain_core.tools import tool  # decorator
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Common utilities
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
```

### AugLLMConfig Setup (CORRECT WAY)

```python
# ✅ CORRECT - Don't specify model parameter
config = AugLLMConfig()  # Uses defaults (gpt-4o-mini)

# ✅ CORRECT - With custom settings
config = AugLLMConfig(
    temperature=0.7,
    max_tokens=1000,
    system_message="You are a helpful assistant"
)

# ❌ WRONG - Don't set model parameter
config = AugLLMConfig(model="gpt-4")  # This causes issues
```

### Simple Agent Setup

```python
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Basic setup
config = AugLLMConfig()
agent = SimpleAgent(engine=config)

# With custom name and settings
config = AugLLMConfig(
    temperature=0.3,
    system_message="You are a code reviewer"
)
agent = SimpleAgent(
    name="code_reviewer",
    engine=config
)

# Usage
result = agent.run("Review this code: def hello(): print('hi')")
```

### React Agent Setup

```python
from haive.agents.react.agent import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Basic setup with tools
config = AugLLMConfig()
agent = ReactAgent(
    name="react_agent",
    engine=config,
    tools=["calculator", "search"]  # Tool names
)

# Usage
result = agent.run("Calculate 15 * 23 and search for Python tutorials")
```

### RAG Agent Setup

```python
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Setup with documents
documents = [...]  # Your documents
config = AugLLMConfig()

vector_config = VectorStoreConfig(
    name="my_vectorstore",
    documents=documents,
    vector_store_provider=VectorStoreProvider.FAISS
)

agent = BaseRAGAgent(
    name="rag_agent",
    engine=vector_config,
    llm_config=config
)

# Usage
result = agent.run("What does the documentation say about X?")
```

### Tool Creation with LangChain

```python
from langchain_core.tools import Tool, tool
from typing import Any

# Method 1: Using @tool decorator
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        result = eval(expression)
        return str(result)
    except:
        return "Error in calculation"

# Method 2: Using Tool class
def search_function(query: str) -> str:
    """Search for information."""
    return f"Search results for: {query}"

search_tool = Tool(
    name="search",
    description="Search for information on any topic",
    func=search_function
)

# Usage with agents
tools = [calculator, search_tool]
agent = ReactAgent(engine=config, tools=tools)
```

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

## 🚨 Critical Reminders

1. **GIT DIFF ALWAYS** - `git status` and `git diff` before ANY work
2. **RESEARCH FIRST** - Check existing patterns before implementing anything
3. **USE TRUNK** - Always run `trunk check --all` before committing
4. **NO MOCKS IN TESTS** - Use real LLMs, real tools, real components
5. **PROPER PYDANTIC** - No manual **init**, use Field validation, check existing patterns
6. **EXPLICIT IMPORTS** - `from haive.core.engine import X`, not `from engine import X`
7. **GIT REVIEW CHANGES** - `git diff --cached` before every commit
8. **USE TODOS** - TodoWrite for planning, tracking, and organization
9. **POETRY RUN EVERYTHING** - Never run Python directly, always `poetry run python`
10. **CHECK EXISTING SCHEMAS** - Look at MessagesState, MetaStateSchema patterns first
11. **STAGE FILES INDIVIDUALLY** - `git add file.py` NOT `git add .`
12. **DOCUMENT PROGRESS** - Update session memory as you work

## 📝 Quick Memory Access

Need details? Import the full guides:

- Memory architecture: @project_docs/active/standards/documentation/memory_system.md
- Development workflow: @project_docs/active/standards/coding/development_workflow.md
- Build & test procedures: @project_docs/active/standards/coding/BUILD_AND_TEST_GUIDE.md
- Pydantic patterns: @project_docs/active/standards/coding/PYDANTIC_PATTERNS.md
- Code examples: @project_docs/claude_documentation/CLAUDE_AGENTS.md
- Testing details: @project_docs/active/standards/testing/philosophy.md
- Git workflows: @project_docs/active/standards/git/workflow.md

---

**Remember**: This file is loaded at every session start. Keep it lean and use imports for detailed information!
