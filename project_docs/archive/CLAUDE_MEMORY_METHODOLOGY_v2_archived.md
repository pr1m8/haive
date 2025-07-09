# Claude Memory Methodology & Development Framework

**Version**: 2.0  
**Purpose**: Unified memory structure, development methodology, and code style guide for Haive AI Agent Framework  
**Author**: Claude Code Agent  
**Date**: 2025-01-05

## 🧠 Memory Architecture Overview

### Core Principles

1. **Hierarchical Memory Structure**: Global → Project → Package → Individual components
2. **Cross-Referenced Documentation**: Every document links to related contexts with numbered tags
3. **Contextual Memory Layers**: Different granularity levels for different needs
4. **Progressive Memory Building**: Start broad, narrow down to specifics
5. **Living Documentation**: Memory evolves with the codebase
6. **Global Memory Preservation**: Never modify ~/.claude/CLAUDE.md without explicit permission
7. **Numerical Memory Ordering**: All memories tagged and ordered for easy navigation
8. **Cross-Memory Linking**: All memories reference related memories with [MEM-XXX] tags

### Memory Hierarchy with Numbered Organization

```
Global Memory (User Level) [MEM-001]
├── ~/.claude/CLAUDE.md (Universal coding principles) [MEM-001-A] 🔒 PROTECTED
├── ~/.claude/projects/{project}.md (Project-specific patterns) [MEM-001-B] 🔒 PROTECTED
│
Project Memory (Repository Level) [MEM-002]
├── CLAUDE.md (Main routing and commands) [MEM-002-A]
├── CLAUDE_MEMORY_METHODOLOGY.md (This file - unified standards) [MEM-002-B]
├── project_docs/ [MEM-003]
│   ├── 00_MEMORY_INDEX.md (Central memory index with tags) [MEM-003-A]
│   ├── 01_GLOBAL_STATUS.md (Overall project status) [MEM-003-B]
│   ├── {package_name}/ [MEM-004-XXX]
│   │   ├── 01_PACKAGE_OVERVIEW.md (Package summary with links) [MEM-004-XXX-A]
│   │   ├── 02_CURRENT_STATUS.md (Progress tracking) [MEM-004-XXX-B]
│   │   ├── 03_DEVELOPMENT_GUIDE.md (Methodology) [MEM-004-XXX-C]
│   │   ├── 04_CODE_STANDARDS.md (Package-specific standards) [MEM-004-XXX-D]
│   │   ├── progress_tracking/ [MEM-004-XXX-E]
│   │   │   ├── 01_COMPLETED.md (Finished work log)
│   │   │   ├── 02_IN_PROGRESS.md (Current work status)
│   │   │   └── 03_PLANNED.md (Future work pipeline)
│   │   ├── testing/ [MEM-004-XXX-F]
│   │   │   ├── 01_TEST_METHODOLOGY.md (Testing approach)
│   │   │   ├── 02_NO_MOCKS_ENFORCEMENT.md (Real testing standards)
│   │   │   └── 03_TEST_COVERAGE_REPORT.md (Coverage tracking)
│   │   └── individual_components/ [MEM-004-XXX-G]
│   │       ├── 01_COMPONENT_INDEX.md (Component listing)
│   │       └── {component_name}/ [MEM-004-XXX-G-YYY]
│   │           ├── 01_ANALYSIS.md (Component analysis)
│   │           ├── 02_FIXES_APPLIED.md (Changes made)
│   │           └── 03_CROSS_REFERENCES.md (Related components)
│   ├── claude_documentation/ [MEM-005]
│   │   ├── 00_CLAUDE_INDEX.md (Claude memory navigation) [MEM-005-A]
│   │   ├── CLAUDE_QUICKREF.md (Essential commands) [MEM-005-B]
│   │   ├── CLAUDE_AGENTS.md (Agent documentation) [MEM-005-C]
│   │   └── package_guides/ [MEM-005-D]
│   │       └── {package}_GUIDE.md [MEM-005-D-XXX]
│   └── git_management/ [MEM-006]
│       ├── 01_GIT_WORKFLOW.md (Proper git usage) [MEM-006-A]
│       ├── 02_COMMIT_STANDARDS.md (Commit message format) [MEM-006-B]
│       └── 03_BRANCH_STRATEGY.md (Branching methodology) [MEM-006-C]
```

## 🎯 Haive Project Structure

### Essential Information

- **Package Location**: `/home/will/Projects/haive/backend/haive/packages/`
- **Test Location**: `packages/{package_name}/tests/`
- **Always use**: `poetry run` for all commands
- **Development Branch**: `feature/enhanced-tool-management`

### Core Packages Architecture

```
packages/
├── haive-core/             # Foundation (engines, graphs, schemas)
├── haive-agents/           # Agent implementations
├── haive-tools/            # Tool implementations
├── haive-games/            # Game implementations
├── haive-dataflow/         # Dataflow and streaming
├── haive-mcp/              # MCP integration
└── haive-prebuilt/         # Prebuilt components
```

### Development Environment

- **Python**: 3.12+
- **Package Manager**: Poetry
- **Local Development**: All packages in dev mode (`develop = true`)
- **Testing**: pytest with real components (NO MOCKS)

## 📁 File Management & Memory Organization Standards [MEM-007]

### 🔒 Global Memory Protection Rules

**CRITICAL: Global memories are SACRED and PROTECTED**

```bash
# ❌ NEVER MODIFY these without explicit user permission:
~/.claude/CLAUDE.md                    # Global coding principles
~/.claude/projects/{project}.md        # Project-specific patterns

# ✅ ALWAYS preserve global memory content
# ✅ ALWAYS backup before any global changes
# ✅ ALWAYS ask permission before global modifications
```

### 📋 Memory Cross-Referencing System [MEM-007-A]

#### Memory Tag Format:

```
[MEM-XXX]           # Top-level memory area
[MEM-XXX-Y]         # Sub-area within memory
[MEM-XXX-Y-ZZZ]     # Specific component/file
```

#### Cross-Reference Examples:

```markdown
**Memory References:**

- **Parent**: [MEM-002-A] Main Project Routing
- **Related**: [MEM-004-CORE] Haive Core Package Documentation
- **Child**: [MEM-004-CORE-G-001] ReactAgent Component Analysis
- **See Also**: [MEM-005-B] Claude Quick Reference

**File References:**

- **Previous Version**: [MEM-004-CORE-G-001] ReactAgent v1.0 Analysis
- **Dependencies**: [MEM-004-TOOLS] Tools Package Requirements
- **Cross-Package**: [MEM-004-AGENTS] Agent Integration Patterns
```

### 📁 Proper File Management Standards [MEM-007-B]

#### File Naming Conventions:

```
✅ CORRECT - Numbered, descriptive, hierarchical:
01_PACKAGE_OVERVIEW.md              # Clear sequence and purpose
02_CURRENT_STATUS.md                # Status tracking
03_DEVELOPMENT_GUIDE.md             # Methodology
react_agent_implementation.py       # Descriptive component name
tool_validation_mixin.py            # Clear pattern indication

❌ WRONG - Generic, unclear, random:
overview.md                         # Too generic
status.md                          # No context
guide.md                           # Unclear scope
agent.py                           # Not specific enough
utils.py                           # Everything becomes utils
helper.py                          # Unclear purpose
temp_file.py                       # Temporary files left behind
test_thing.py                      # Vague test purpose
```

#### Directory Organization Rules:

```
✅ CORRECT - Hierarchical with clear purpose:
project_docs/
├── 00_MEMORY_INDEX.md             # Central navigation
├── claude_documentation/          # Claude-specific memory
│   ├── 00_CLAUDE_INDEX.md        # Claude navigation
│   └── package_guides/           # Per-package guides
├── haive-core/                   # Package-specific docs
│   ├── 01_PACKAGE_OVERVIEW.md   # Package summary
│   ├── progress_tracking/        # Status tracking
│   └── individual_components/    # Component-specific
└── git_management/               # Git workflow docs

❌ WRONG - Flat, unclear, chaotic:
docs/
├── stuff.md
├── notes.md
├── random_file.py
├── temp/
└── backup_old/
```

### Package-Level Folder Structure [MEM-007-C]

```
packages/{package-name}/
├── src/haive/{package}/          # Source code
│   ├── __init__.py              # Package exports and API
│   ├── README.md                # Package overview
│   ├── agents/                  # Agent implementations
│   ├── tools/                   # Tool implementations
│   ├── config/                  # Configuration models
│   ├── utils/                   # Utility functions
│   └── examples/                # Usage examples
├── tests/                       # Test files (mirrors src structure)
│   ├── __init__.py
│   ├── test_{module}.py         # Test files named after modules
│   ├── fixtures/                # Test data and fixtures
│   ├── integration/             # Integration tests
│   └── resources/               # Test resources (state history, etc.)
├── docs/                        # Package-specific documentation
├── pyproject.toml              # Package dependencies
└── README.md                   # Package documentation
```

### Core Codebase Organization Principles

#### 1. **Reference-Based Organization**

```python
# ✅ CORRECT - Clear references in imports
from haive.core.engine import ReactAgent          # Core reference
from haive.agents.conversational import ChatAgent # Package reference
from haive.tools.math import Calculator           # Tool reference

# ❌ WRONG - Unclear references
from agents import ChatAgent  # Where is this from?
from utils import helper      # Which utils?
```

#### 2. **Hierarchical Folder Naming**

```
# ✅ CORRECT - Clear hierarchy
haive-core/
├── src/haive/core/
│   ├── engine/              # Core engines
│   │   ├── base/           # Base classes
│   │   ├── agent/          # Agent engines
│   │   └── llm/            # LLM engines
│   ├── graph/              # Graph system
│   │   ├── state_graph/    # State graph implementation
│   │   ├── node/           # Node definitions
│   │   └── patterns/       # Graph patterns
│   └── schema/             # Schema system
│       ├── prebuilt/       # Pre-built schemas
│       └── compatibility/  # Schema compatibility
```

#### 3. **Documentation Folder Standards**

```
project_docs/
├── claude_documentation/        # Claude agent memory
│   ├── CLAUDE_QUICKREF.md      # Essential commands
│   ├── CLAUDE_AGENTS.md        # Agent documentation
│   └── package_guides/         # Per-package guides
├── {package_name}/             # Package-specific docs
│   ├── README.md               # Package overview
│   ├── 01_CURRENT_STATUS.md    # Progress tracking
│   ├── 02_DEVELOPMENT_GUIDE.md # Development methodology
│   ├── code_standards/         # Code standards
│   ├── progress_tracking/      # Status tracking
│   ├── testing/               # Testing guides
│   └── individual_components/ # Component-specific docs
└── CLAUDE_MEMORY_METHODOLOGY.md # This file
```

### Core Codebase Reference Standards

#### 1. **Import Organization**

```python
# ✅ CORRECT - Organized imports with clear references
"""Module imports organized by reference type."""

# Standard library
import os
import logging
from typing import List, Dict, Any, Optional

# Third-party packages
from pydantic import BaseModel, Field
from langchain_core.agents import AgentExecutor

# Haive core references (always first)
from haive.core.engine import BaseEngine, ReactAgent
from haive.core.schema import BasicAgentState
from haive.core.graph import BaseGraph

# Haive package references
from haive.tools.math import Calculator
from haive.agents.conversational import ChatAgent

# Local module references (relative imports)
from .config import AgentConfig
from .utils import validate_input
```

#### 2. **File Naming Conventions**

```
# ✅ CORRECT - Descriptive, hierarchical names
agent_config.py              # Clear purpose
react_agent_implementation.py # Specific implementation
tool_validation_mixin.py     # Mixin pattern
base_graph_builder.py        # Base class

# ❌ WRONG - Vague or misleading names
config.py                    # Too generic
agent.py                     # Not specific enough
utils.py                     # Everything becomes "utils"
helper.py                    # Unclear purpose
```

#### 3. **Package Reference Patterns**

```python
# ✅ CORRECT - Clear package boundaries
class ReactAgent(BaseEngine):  # Inherits from core
    """ReactAgent implementation with clear core dependencies."""

    def __init__(self, tools: List[str] = None):
        # Reference tools by their package path
        self.available_tools = {
            "calculator": "haive.tools.math.Calculator",
            "search": "haive.tools.web.SearchTool",
            "file_ops": "haive.tools.file.FileOperations"
        }

    def load_tool(self, tool_name: str):
        """Load tool with explicit package reference."""
        if tool_name in self.available_tools:
            tool_path = self.available_tools[tool_name]
            # Import with full path for clarity
            module_path, class_name = tool_path.rsplit('.', 1)
            module = importlib.import_module(module_path)
            return getattr(module, class_name)()
```

### Folder Labeling & Navigation

#### 1. **README File Standards**

```markdown
# Package/Folder Name

## 🎯 Purpose

Brief description of what this folder/package contains

## 📁 Structure
```

folder/
├── subfolder1/ # Description of contents
├── subfolder2/ # Description of contents
└── files.py # Description of purpose

```

## 🔗 References
- **Parent**: [Main Package](../README.md)
- **Core Dependencies**: [haive-core](../haive-core/)
- **Related Packages**: [haive-tools](../haive-tools/)

## 🚀 Quick Start
[Basic usage examples]
```

#### 2. **Cross-Reference Maintenance**

```bash
# Update references when moving files
find . -name "*.py" -exec grep -l "old_reference" {} \;
find . -name "*.md" -exec grep -l "old_reference" {} \;

# Verify all references are valid
python scripts/check_references.py
```

## 📝 Code Style Standards

### Python Standards

- **PEP 8 Compliance**: 100% adherence
- **Type Hints**: Required on all public functions
- **Line Length**: 100 characters max
- **Docstring Style**: Google format for Sphinx compatibility
- **Error Handling**: Always use structured logging, never print statements

### Critical Violations (NEVER DO)

```python
# ❌ WRONG - Print statements
print("Debug info")

# ❌ WRONG - Mutable default arguments
def process_data(items=[]):
    pass

# ❌ WRONG - Missing type hints
def calculate_score(data):
    pass

# ❌ WRONG - Hardcoded values
api_key = "sk-1234567890"
```

### Required Patterns (ALWAYS DO)

```python
# ✅ CORRECT - Structured logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Processing data")

# ✅ CORRECT - Safe defaults
def process_data(items: List[str] = None) -> List[str]:
    if items is None:
        items = []
    return items

# ✅ CORRECT - Type hints
def calculate_score(data: Dict[str, Any]) -> float:
    pass

# ✅ CORRECT - Environment variables
import os
api_key = os.getenv("OPENAI_API_KEY")
```

### Enhanced Pydantic Model Documentation Standards [MEM-012]

```python
from pydantic import BaseModel, Field, ConfigDict, field_validator, model_validator
from typing import List, Optional, Dict, Any, Union, Literal
from datetime import datetime
from enum import Enum

class ModelType(str, Enum):
    """Supported LLM model types.

    Attributes:
        GPT4: OpenAI GPT-4 model
        GPT4_TURBO: OpenAI GPT-4 Turbo variant
        CLAUDE_3: Anthropic Claude 3 model
        LLAMA_3: Meta Llama 3 model

    Examples:
        Using enum in config::

            model_type = ModelType.GPT4
            config = AgentConfig(model=model_type)

        Validating model type::

            if config.model in [ModelType.GPT4, ModelType.GPT4_TURBO]:
                # Use OpenAI-specific parameters
    """
    GPT4 = "gpt-4"
    GPT4_TURBO = "gpt-4-turbo"
    CLAUDE_3 = "claude-3"
    LLAMA_3 = "llama-3"

class AgentConfig(BaseModel):
    """Agent configuration with comprehensive validation and examples.

    This model defines the configuration for AI agents including model selection,
    parameters, tools, and runtime settings. It provides strict validation and
    sensible defaults for production use.

    Attributes:
        name: Unique agent identifier used for logging and state management.
            Must be alphanumeric with underscores, 3-50 characters.
        model: LLM model to use, must be one of supported ModelType values.
            Defaults to GPT-4 for stability.
        temperature: Sampling temperature controlling randomness (0.0-2.0).
            Lower values (0.0-0.3) for factual tasks, higher (0.7-1.0) for creative.
        max_tokens: Maximum tokens in response (100-4000). None for model default.
        tools: List of tool names available to agent. Validated against registry.
        system_prompt: Optional system prompt override. Uses default if not provided.
        memory_enabled: Whether to persist conversation history. Default True.
        timeout_seconds: Maximum execution time per request. Default 300s.
        metadata: Optional metadata dictionary for custom tracking.

    Raises:
        ValidationError: If any field fails validation constraints.
            - name: Invalid format or length
            - model: Not in ModelType enum
            - temperature: Outside 0.0-2.0 range
            - max_tokens: Outside 100-4000 range
            - tools: Invalid tool names

    Examples:
        Basic agent configuration::

            config = AgentConfig(
                name="research_agent",
                model=ModelType.GPT4,
                temperature=0.7,
                tools=["web_search", "calculator"]
            )

        Low temperature for factual tasks::

            config = AgentConfig(
                name="fact_checker",
                model=ModelType.GPT4_TURBO,
                temperature=0.1,  # Very deterministic
                max_tokens=1000,
                tools=["wikipedia", "calculator"]
            )

        Creative writing agent::

            config = AgentConfig(
                name="creative_writer",
                model=ModelType.CLAUDE_3,
                temperature=0.9,  # More creative
                max_tokens=2000,
                system_prompt="You are a creative writing assistant..."
            )

        Agent with custom metadata::

            config = AgentConfig(
                name="customer_service",
                model=ModelType.GPT4,
                metadata={
                    "department": "support",
                    "version": "2.0",
                    "created_by": "team_lead"
                }
            )

        Validation example::

            try:
                config = AgentConfig(
                    name="test",
                    temperature=3.0  # Will raise ValidationError
                )
            except ValidationError as e:
                print(f"Validation failed: {e}")
                # Output: temperature must be <= 2.0

    See Also:
        - :class:`ModelType`: Available model types
        - :class:`ToolConfig`: Tool configuration
        - :ref:`agent-creation`: Agent creation guide

    Note:
        When using with LangChain/LangGraph, this config can be converted
        to their native formats using the `.to_langchain()` method.

    .. versionadded:: 1.0.0
        Initial implementation
    .. versionchanged:: 1.2.0
        Added metadata field and timeout_seconds
    """

    model_config = ConfigDict(
        # Pydantic v2 configuration
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
        extra="forbid",  # No extra fields allowed
        json_schema_extra={
            "examples": [
                {
                    "name": "research_agent",
                    "model": "gpt-4",
                    "temperature": 0.7,
                    "tools": ["web_search", "calculator"]
                },
                {
                    "name": "creative_writer",
                    "model": "claude-3",
                    "temperature": 0.9,
                    "max_tokens": 2000
                }
            ]
        }
    )

    name: str = Field(
        ...,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Unique agent identifier (alphanumeric + underscore)",
        examples=["research_agent", "chat_bot_v2", "customer_service_01"]
    )

    model: ModelType = Field(
        default=ModelType.GPT4,
        description="LLM model selection from supported types",
        examples=[ModelType.GPT4, ModelType.CLAUDE_3]
    )

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Sampling temperature (0.0=deterministic, 2.0=creative)",
        examples=[0.1, 0.7, 1.0]
    )

    max_tokens: Optional[int] = Field(
        default=None,
        ge=100,
        le=4000,
        description="Maximum response tokens (None for model default)",
        examples=[500, 1000, 2000]
    )

    tools: List[str] = Field(
        default_factory=list,
        min_length=0,
        max_length=20,
        description="Available tool names for the agent",
        examples=[["web_search"], ["calculator", "file_reader"]]
    )

    system_prompt: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Custom system prompt (None for default)",
        examples=["You are a helpful research assistant.", None]
    )

    memory_enabled: bool = Field(
        default=True,
        description="Enable conversation history persistence",
        examples=[True, False]
    )

    timeout_seconds: int = Field(
        default=300,
        ge=10,
        le=3600,
        description="Request timeout in seconds",
        examples=[60, 300, 600]
    )

    metadata: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Optional metadata for tracking",
        examples=[{"version": "1.0"}, {"department": "sales"}]
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate agent name format.

        Args:
            v: Name to validate

        Returns:
            Validated name

        Raises:
            ValueError: If name contains invalid characters

        Examples:
            >>> AgentConfig.validate_name("test_agent")
            'test_agent'
            >>> AgentConfig.validate_name("test-agent")
            ValueError: Name contains invalid characters
        """
        if not v.replace("_", "").isalnum():
            raise ValueError("Name must be alphanumeric with underscores only")
        return v

    @field_validator("tools")
    @classmethod
    def validate_tools(cls, v: List[str]) -> List[str]:
        """Validate tool names against registry.

        Args:
            v: List of tool names

        Returns:
            Validated tool list

        Raises:
            ValueError: If any tool name is invalid

        Examples:
            >>> AgentConfig.validate_tools(["calculator", "web_search"])
            ['calculator', 'web_search']
            >>> AgentConfig.validate_tools(["invalid_tool"])
            ValueError: Unknown tool: invalid_tool
        """
        # In real implementation, check against tool registry
        valid_tools = {"calculator", "web_search", "file_reader", "wikipedia"}
        invalid = set(v) - valid_tools
        if invalid:
            raise ValueError(f"Unknown tools: {', '.join(invalid)}")
        return v

    @model_validator(mode="after")
    def validate_model_compatibility(self) -> "AgentConfig":
        """Validate model-specific constraints.

        Ensures certain models have appropriate settings.

        Returns:
            Validated config instance

        Raises:
            ValueError: If settings incompatible with model

        Examples:
            Config with model-specific validation::

                # This will pass validation
                config = AgentConfig(
                    name="test",
                    model=ModelType.LLAMA_3,
                    max_tokens=2000  # Within Llama limits
                )

                # This will fail validation
                config = AgentConfig(
                    name="test",
                    model=ModelType.LLAMA_3,
                    max_tokens=4000  # Exceeds Llama limit
                )
        """
        # Example: Llama models have lower token limits
        if self.model == ModelType.LLAMA_3 and self.max_tokens and self.max_tokens > 2048:
            raise ValueError("Llama-3 models support maximum 2048 tokens")
        return self

    def to_langchain(self) -> Dict[str, Any]:
        """Convert to LangChain-compatible configuration.

        Returns:
            Dictionary with LangChain format

        Examples:
            >>> config = AgentConfig(name="test", model=ModelType.GPT4)
            >>> lc_config = config.to_langchain()
            >>> print(lc_config["model_name"])
            'gpt-4'
        """
        return {
            "model_name": self.model.value,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "timeout": self.timeout_seconds,
            "metadata": {"agent_name": self.name, **(self.metadata or {})}
        }
```

## 🧪 Testing Philosophy [MEM-008]

### Core Testing Principles

1. **ABSOLUTE NO MOCKS**: Always use real components, real APIs, real data
2. **Test Behavior**: Not implementation details or internals
3. **Descriptive Names**: `test_feature_with_condition_expects_result`
4. **Real State History**: Save actual state files like existing examples
5. **No Enhanced/Fake Tests**: Never create artificial or enhanced test scenarios
6. **No Cheating Tests**: Tests must validate actual functionality, not bypass logic
7. **Real Integration**: Test actual component interactions, not simulated ones
8. **Live Environment**: Use real LLMs, real APIs, real external services when possible

### 🚫 ABSOLUTE NO-MOCKS ENFORCEMENT [MEM-008-A]

#### Forbidden Testing Patterns:

```python
# 🚨 ABSOLUTELY FORBIDDEN - Mock usage in any form:
from unittest.mock import Mock, MagicMock, patch
mock_llm = Mock()                           # ❌ NO MOCKS EVER
@patch('haive.core.agent')                  # ❌ NO PATCHES EVER
with mock.patch() as mock_agent:            # ❌ NO MOCK CONTEXT MANAGERS
agent = MagicMock()                         # ❌ NO MAGIC MOCKS EVER

# 🚨 FORBIDDEN - Fake/stub implementations:
class FakeLLM:                              # ❌ NO FAKE CLASSES
    def __call__(self): return "fake"

def mock_function():                        # ❌ NO MOCK FUNCTIONS
    return {"fake": "data"}

# 🚨 FORBIDDEN - Test doubles or substitutes:
test_agent = TestDouble()                   # ❌ NO TEST DOUBLES
stub_response = Stub()                      # ❌ NO STUBS
fake_api = FakeAPI()                        # ❌ NO FAKE APIs
```

#### Required Real Testing Patterns:

```python
# ✅ MANDATORY - Real component testing:
def test_react_agent_with_real_llm_and_tools():
    """Test ReactAgent with actual LLM and real tools."""
    # Use REAL components only
    agent = ReactAgent(
        name="test_agent",
        model="gpt-4",                      # Real LLM
        tools=["calculator", "web_search"]  # Real tools
    )

    # Test with REAL input
    result = agent.process("Calculate 15 * 23 and search for Python tutorials")

    # Verify REAL behavior
    assert "345" in str(result.response)
    assert result.tool_calls_made > 0
    assert result.conversation_history is not None
    assert result.state_saved_to_file is True

# ✅ CORRECT - Real integration testing:
def test_agent_tool_integration_real_apis():
    """Test real agent with real tool integration."""
    calculator = Calculator()               # Real tool instance
    search_tool = WebSearchTool()          # Real search tool

    agent = ReactAgent(
        name="integration_test",
        model="gpt-4",
        tools=[calculator, search_tool]     # Real tools passed
    )

    result = agent.process("What's 50 * 30 and find current Python version")

    # Test real outcomes
    assert calculator in agent.active_tools
    assert search_tool in agent.active_tools
    assert "1500" in str(result.response)

# ✅ CORRECT - Real error condition testing:
def test_real_error_handling_with_invalid_tool():
    """Test how agent handles real tool errors."""
    agent = ReactAgent(name="error_test", model="gpt-4")

    # Cause real error by using non-existent tool
    result = agent.process("Use the nonexistent_tool to do something")

    # Test real error handling (not mocked)
    assert result.error_occurred is True
    assert "tool not found" in result.error_message.lower()
    assert result.recovery_attempted is True
```

### Test Structure

```python
import pytest
from haive.core.agent import ReactAgent

def test_react_agent_with_math_tool_saves_state_history():
    """Test ReactAgent with real math tool and state persistence."""
    # Arrange
    agent = ReactAgent(
        name="test_math_agent",
        model="gpt-4",
        tools=["math_calculator"],
        save_state_history=True
    )

    # Act
    result = agent.process("Calculate 25 * 37")

    # Assert
    assert result.answer == 925
    assert agent.state_history_saved
    assert len(agent.conversation_history) > 0
```

### Testing Standards & Anti-Patterns

#### ❌ FORBIDDEN Test Patterns

```python
# ❌ WRONG - Enhanced/artificial scenarios
def test_enhanced_agent_with_super_powers():
    pass

# ❌ WRONG - Fake/mocked components
def test_agent_with_fake_llm():
    mock_llm = MagicMock()
    pass

# ❌ WRONG - Cheating/bypassing logic
def test_agent_bypassing_validation():
    agent._skip_validation = True
    pass

# ❌ WRONG - Artificial success scenarios
def test_agent_always_succeeds():
    # Test that doesn't actually test real behavior
    pass
```

#### ✅ REQUIRED Test Patterns

```python
# ✅ CORRECT - Real components, real scenarios
def test_react_agent_with_actual_math_tool():
    """Test ReactAgent with real math tool using actual LLM."""
    agent = ReactAgent(
        name="math_agent",
        model="gpt-4",
        tools=["calculator"]  # Real tool, not mock
    )
    result = agent.process("What is 15 * 23?")
    assert "345" in result.response
    assert agent.conversation_history  # Real state saved

# ✅ CORRECT - Testing actual error conditions
def test_react_agent_handles_invalid_tool_gracefully():
    """Test how agent handles real tool failures."""
    agent = ReactAgent(name="test", model="gpt-4", tools=["nonexistent_tool"])
    result = agent.process("Use the tool")
    # Test real error handling, not mocked responses
    assert result.error_message is not None
```

### Commands for Testing

```bash
# Run tests for specific package
poetry run pytest packages/haive-agents/tests/

# Run all tests with coverage
poetry run pytest --cov=haive

# Run tests with verbose output
poetry run pytest -vv

# Run specific test file
poetry run pytest tests/test_react_agent.py

# Test with real components only (no mocks)
poetry run pytest -k "not mock" -v
```

## 🔄 Development Workflow

### 1. Memory-Driven Development Process

```bash
# 1. Context Loading
Read: CLAUDE.md (project routing)
Read: CLAUDE_MEMORY_METHODOLOGY.md (this file)
Read: project_docs/claude_documentation/CLAUDE_QUICKREF.md

# 2. Work Planning
TodoWrite: Specific tasks with priorities
git status && git diff: Check current state

# 3. Execution
Apply: Standards from this methodology
Document: Decisions and patterns
Update: Progress in real-time

# 4. Quality Assurance
poetry run pytest: Run tests
poetry run ruff check: Linting
poetry run mypy: Type checking
```

### 2. Essential Commands

```bash
# Development
poetry install --all-extras
poetry run python -m haive.your_module
poetry run pytest packages/your_package/tests/

# Documentation
poetry run nox -s docs
poetry run nox -s docs_serve

# Quality
poetry run nox -s lint
poetry run nox -s typecheck
```

### 3. Git Workflow Standards [MEM-009]

#### 🚨 MANDATORY Git Safety Protocol

```bash
# ALWAYS run these FIRST before any work
git status                              # See current state
git diff                               # See unstaged changes
git diff --cached                      # See staged changes
git log --oneline -5                   # Recent commit history
git branch -v                          # Current branch info

# SAFETY BACKUP before major changes
git stash push -m "Safety backup before work"

# NEVER work without knowing current state
# NEVER commit without reviewing changes first
# NEVER push without testing locally
```

#### Git Commit Standards [MEM-009-A]

```bash
# ✅ CORRECT - Conventional commits with context
git commit -m "feat(haive-core): add enhanced tool management with validation

- Added tool validation in ReactAgent
- Implemented state history saving
- Updated imports to use BaseGraph
- All tests pass with real components

Ref: [MEM-004-CORE-G-001] ReactAgent Enhancement
Fixes: Import errors from missing DynamicGraph"

git commit -m "fix(haive-mcp): resolve uvicorn dependency conflict

- Updated uvicorn version to ^0.34.0 in pyproject.toml
- Regenerated poetry.lock
- All packages now install cleanly

Ref: [MEM-006-A] Git Workflow Standards"

git commit -m "docs(memory): update methodology with git standards

- Added numbered memory tagging system
- Enhanced no-mocks testing enforcement
- Added git safety protocols
- Updated cross-reference format

Ref: [MEM-002-B] Memory Methodology v2.0"

# ❌ WRONG - Vague, unclear commits
git commit -m "fix stuff"              # No context
git commit -m "update"                 # What was updated?
git commit -m "wip"                    # Work in progress is not ready
git commit -m "temp"                   # Temporary commits pollute history
```

#### Branch Naming Standards [MEM-009-B]

```bash
# ✅ CORRECT - Descriptive with memory references
feature/mem-008-enhanced-testing       # Feature with memory reference
fix/mem-004-core-import-errors         # Fix with memory reference
docs/mem-002-methodology-update        # Documentation with memory reference
refactor/mem-007-file-organization     # Refactor with memory reference

# Traditional format also acceptable:
feature/enhanced-tool-management
fix/resolve-import-issues
docs/update-memory-methodology

# ❌ WRONG - Unclear or generic
feature/stuff                          # Too vague
fix/issues                            # What issues?
dev                                   # Not descriptive
temp-branch                           # Temporary branches shouldn't exist
user-changes                          # Unclear purpose
```

#### Git Workflow Process [MEM-009-C]

```bash
# 1. SAFETY FIRST - Save current work
git stash push -m "Work in progress backup"

# 2. UPDATE from remote (if collaborative)
git fetch origin
git status                             # Check for conflicts

# 3. CREATE proper branch
git checkout -b feature/mem-XXX-description

# 4. WORK incrementally with frequent commits
git add specific_files.py              # Stage specific files
git commit -m "feat(component): specific change with context"

# 5. TEST before final commit
poetry run pytest
poetry run ruff check

# 6. FINAL verification before push
git log --oneline -3                   # Review recent commits
git diff origin/main...HEAD            # See all changes since main

# 7. PUSH with upstream tracking
git push -u origin feature/mem-XXX-description

# 8. UPDATE memory documentation
# Document the change in appropriate [MEM-XXX] file
```

## 📊 Enhanced Documentation Standards [MEM-014]

### Comprehensive Docstring Requirements

#### 1. **Class Documentation Standards**

```python
class ReactAgent(BaseAgent):
    """Advanced ReAct (Reasoning and Acting) agent implementation.

    This agent implements the ReAct paradigm, combining chain-of-thought reasoning
    with the ability to use tools and take actions. It maintains conversation
    history, supports streaming responses, and provides comprehensive state management.

    The agent follows this reasoning cycle:
    1. Analyze the user request
    2. Decide if tools are needed
    3. Call tools and observe results
    4. Reason about the results
    5. Generate final response or iterate

    Attributes:
        name (str): Unique agent identifier for logging and persistence.
        model (ModelType): LLM model used for reasoning and generation.
        tools (List[BaseTool]): Available tools for the agent to use.
        memory (ConversationMemory): Conversation history and state storage.
        max_iterations (int): Maximum reasoning iterations before forcing response.
        stream_handler (Optional[StreamHandler]): Handler for streaming responses.

    Properties:
        is_configured (bool): Whether agent is properly configured.
        conversation_id (str): Current conversation identifier.
        tool_count (int): Number of available tools.
        memory_size (int): Current conversation memory size in tokens.

    Class Attributes:
        DEFAULT_MAX_ITERATIONS (int): Default iteration limit (5).
        SUPPORTED_MODELS (List[str]): Models compatible with ReAct.

    Examples:
        Basic agent creation and usage::

            agent = ReactAgent(
                name="research_assistant",
                model=ModelType.GPT4,
                tools=[WebSearchTool(), CalculatorTool()]
            )

            response = agent.run("What's the weather in Paris?")
            print(response.response)

        Agent with custom configuration::

            agent = ReactAgent(
                name="coding_assistant",
                model=ModelType.GPT4_TURBO,
                tools=[CodeExecutor(), FileReader(), Terminal()],
                max_iterations=10,  # More iterations for complex tasks
                memory=PostgresMemory(connection_string)  # Persistent memory
            )

        Streaming responses for real-time UI::

            async def stream_handler(chunk: str):
                print(chunk, end="", flush=True)

            agent = ReactAgent(
                name="chat_agent",
                model=ModelType.CLAUDE_3,
                stream_handler=stream_handler
            )

            await agent.arun("Write a poem about AI")

        Using agent in a web application::

            @app.post("/chat")
            async def chat_endpoint(request: ChatRequest):
                agent = get_or_create_agent(request.user_id)

                try:
                    response = await agent.arun(
                        request.message,
                        tools=request.allowed_tools,
                        timeout=30.0
                    )
                    return {"response": response.response, "tools_used": response.tool_calls}
                except Exception as e:
                    logger.error(f"Agent error: {e}")
                    return {"error": "Processing failed", "details": str(e)}

    See Also:
        - :class:`BaseAgent`: Abstract base class for all agents
        - :class:`Tool`: Tool interface documentation
        - :mod:`haive.agents`: Other agent implementations
        - :ref:`react-pattern`: ReAct pattern explanation

    Note:
        The agent requires at least one tool to function properly in ReAct mode.
        Without tools, it falls back to simple question-answering.

    Warning:
        High max_iterations values can lead to excessive API costs and latency.
        Monitor token usage when increasing iteration limits.

    .. versionadded:: 1.0.0
        Initial ReAct implementation
    .. versionchanged:: 1.2.0
        Added streaming support and PostgreSQL persistence
    .. versionchanged:: 1.3.0
        Improved tool calling with parallel execution
    """

    DEFAULT_MAX_ITERATIONS: ClassVar[int] = 5
    SUPPORTED_MODELS: ClassVar[List[str]] = ["gpt-4", "gpt-4-turbo", "claude-3"]

    def __init__(
        self,
        name: str,
        model: ModelType,
        tools: Optional[List[BaseTool]] = None,
        memory: Optional[BaseMemory] = None,
        max_iterations: int = DEFAULT_MAX_ITERATIONS,
        stream_handler: Optional[Callable[[str], Awaitable[None]]] = None,
        **kwargs
    ):
        """Initialize ReactAgent with configuration.

        Args:
            name: Unique identifier for the agent (3-50 chars, alphanumeric).
            model: LLM model to use for reasoning.
            tools: List of tools available to the agent. None for no tools.
            memory: Memory backend for conversation storage. None for in-memory.
            max_iterations: Maximum ReAct loop iterations (1-20).
            stream_handler: Async callback for streaming chunks.
            **kwargs: Additional configuration passed to parent class.

        Raises:
            ValueError: Invalid configuration:
                - name format invalid
                - model not supported
                - max_iterations out of range
            TypeError: Invalid tool or memory types

        Examples:
            >>> agent = ReactAgent("helper", ModelType.GPT4)
            >>> agent = ReactAgent(
            ...     "advanced",
            ...     ModelType.GPT4_TURBO,
            ...     tools=[Calculator()],
            ...     max_iterations=10
            ... )
        """
        # Implementation...
```

#### 2. **Method Documentation Standards**

```python
def process_with_tools(
    self,
    request: str,
    *,
    available_tools: Optional[List[str]] = None,
    tool_choice: Union[Literal["auto", "none"], str] = "auto",
    parallel_execution: bool = True,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> ToolExecutionResult:
    """Execute request using available tools with advanced control options.

    Processes the request by selecting and executing appropriate tools based on
    the request content and tool availability. Supports both sequential and
    parallel tool execution with comprehensive retry logic.

    Tool Selection Process:
    1. Analyze request to identify required capabilities
    2. Match capabilities to available tools
    3. Plan execution order (dependencies considered)
    4. Execute tools with specified strategy
    5. Aggregate and validate results

    Args:
        request: User request requiring tool usage. Supports markdown.
            Maximum 4000 characters. May reference previous context.
        available_tools: Subset of agent tools to consider. None uses all.
            Invalid tool names are ignored with warning.
        tool_choice: Tool selection strategy:
            - "auto": Agent decides which tools to use (default)
            - "none": Disable tool usage for this request
            - "{tool_name}": Force specific tool usage
        parallel_execution: Execute independent tools concurrently.
            Default True. False for sequential execution.
        max_retries: Maximum retry attempts for failed tools (0-5).
            Default 3. Applies exponential backoff.
        retry_delay: Initial retry delay in seconds. Doubles each retry.
            Default 1.0. Range: 0.1-10.0.

    Returns:
        ToolExecutionResult containing:
            - results: Dict[str, Any] mapping tool names to outputs
            - execution_order: List[str] of tools in execution order
            - errors: Dict[str, str] mapping tool names to error messages
            - total_duration: float total execution time in seconds
            - retry_count: int total retries across all tools

    Raises:
        ValueError: Invalid parameters:
            - Empty request
            - tool_choice references unknown tool
            - max_retries out of range
        ToolExecutionError: All retries exhausted for critical tool
        TimeoutError: Tool execution exceeded time limits

    Examples:
        Auto tool selection::

            result = agent.process_with_tools(
                "Search for Python tutorials and calculate 50 * 30"
            )
            print(result.results.keys())
            # Output: dict_keys(['web_search', 'calculator'])

        Force specific tool::

            result = agent.process_with_tools(
                "What's the weather?",
                tool_choice="weather_api"  # Force weather API usage
            )

        Sequential execution with retries::

            result = agent.process_with_tools(
                "Read file.txt then analyze its content",
                parallel_execution=False,  # Ensure read completes first
                max_retries=5  # More retries for file operations
            )

        Limited tool set::

            result = agent.process_with_tools(
                "Complex analysis task",
                available_tools=["calculator", "code_executor"],  # Limit tools
                tool_choice="auto"
            )

        Error handling::

            try:
                result = agent.process_with_tools(
                    "Use the database tool",
                    max_retries=1,
                    retry_delay=0.5
                )
            except ToolExecutionError as e:
                print(f"Tool failed after retries: {e.tool_name}")
                print(f"Error: {e.last_error}")
                # Fallback to non-tool response

    Performance Considerations:
        - Parallel execution can reduce latency by 50-70% for multi-tool requests
        - Each retry doubles the delay: 1s, 2s, 4s, 8s, 16s
        - Tool timeout is 30s per execution (configurable in tool definition)
        - Memory usage scales with number of parallel tools

    See Also:
        - :class:`ToolExecutionResult`: Result structure details
        - :meth:`register_tool`: Tool registration method
        - :ref:`tool-development`: Creating custom tools

    .. versionadded:: 1.1.0
    .. versionchanged:: 1.3.0
        Added parallel execution support
    """
    # Implementation...
```

#### 3. **Property and Descriptor Documentation**

```python
@property
def conversation_summary(self) -> str:
    """Generate a concise summary of the current conversation.

    Creates a summary of the conversation history, highlighting key topics,
    decisions made, and tools used. Useful for context switching or reporting.

    The summary includes:
    - Main topics discussed (up to 5)
    - Tools used and their purposes
    - Key decisions or conclusions
    - Unresolved questions

    Returns:
        Formatted summary string (200-500 words).
        Empty string if no conversation history.

    Examples:
        >>> agent.run("Help me plan a trip to Paris")
        >>> agent.run("Find flights under $500")
        >>> print(agent.conversation_summary)
        Summary of conversation (2 messages):

        Topics Discussed:
        - Travel planning for Paris
        - Flight search with budget constraints

        Tools Used:
        - web_search: Found flight options
        - calculator: Computed total costs

        Key Information:
        - Budget limit: $500
        - Destination: Paris
        - Found 3 suitable flights

        Status: Awaiting user selection

    Note:
        Summary generation uses the same LLM as the agent,
        incurring additional token costs.

    .. versionadded:: 1.2.0
    """
    # Implementation...

@cached_property
def tool_capabilities(self) -> Dict[str, List[str]]:
    """Mapping of available tools to their capabilities.

    Analyzes registered tools and extracts their capabilities for
    better tool selection during request processing.

    Returns:
        Dict mapping tool names to capability lists.

    Examples:
        >>> print(agent.tool_capabilities)
        {
            'calculator': ['arithmetic', 'math', 'computation'],
            'web_search': ['search', 'internet', 'research', 'current info'],
            'file_reader': ['read files', 'text extraction', 'documents']
        }

    .. versionadded:: 1.3.0
    """
    # Implementation...
```

#### 4. **Exception Documentation Standards**

```python
class AgentConfigurationError(Exception):
    """Raised when agent configuration is invalid or inconsistent.

    This exception indicates problems with agent setup that prevent
    proper initialization or operation. It includes detailed information
    about the configuration issue.

    Attributes:
        parameter: The configuration parameter that failed validation
        value: The invalid value provided
        reason: Detailed explanation of why the value is invalid
        suggestions: List of suggestions to fix the issue

    Examples:
        Invalid model selection::

            try:
                agent = ReactAgent(name="test", model="invalid-model")
            except AgentConfigurationError as e:
                print(f"Parameter: {e.parameter}")  # 'model'
                print(f"Value: {e.value}")  # 'invalid-model'
                print(f"Reason: {e.reason}")  # 'Model not in supported list'
                print(f"Suggestions: {e.suggestions}")  # ['Use one of: gpt-4, claude-3']

        Tool compatibility issue::

            try:
                agent = ReactAgent(
                    name="test",
                    model=ModelType.LLAMA_3,
                    tools=[AdvancedCodeExecutor()]  # Requires GPT-4
                )
            except AgentConfigurationError as e:
                print(e.reason)  # 'AdvancedCodeExecutor requires GPT-4 or better'

    See Also:
        - :class:`ValidationError`: For input validation failures
        - :class:`ProcessingError`: For runtime processing failures

    .. versionadded:: 1.0.0
    """

    def __init__(
        self,
        parameter: str,
        value: Any,
        reason: str,
        suggestions: Optional[List[str]] = None
    ):
        self.parameter = parameter
        self.value = value
        self.reason = reason
        self.suggestions = suggestions or []

        message = f"Configuration error for '{parameter}': {reason}"
        if self.suggestions:
            message += f"\nSuggestions: {', '.join(self.suggestions)}"

        super().__init__(message)
```

### Enhanced Docstring Summary [MEM-014-A]

#### **Required Elements for ALL Docstrings:**

1. **One-line summary** - Clear, concise description
2. **Detailed explanation** - How it works, why it exists
3. **Type hints** - All parameters and returns fully typed
4. **Args section** - Every parameter documented with type and constraints
5. **Returns section** - Detailed return value description
6. **Raises section** - All exceptions with conditions
7. **Examples section** - Multiple realistic usage examples with outputs
8. **See Also section** - Cross-references to related items
9. **Version tracking** - versionadded, versionchanged, deprecated

#### **Pydantic-Specific Requirements:**

- **ConfigDict** with validation settings
- **Field** descriptors with constraints and examples
- **Validators** with detailed examples
- **JSON schema** examples in model_config
- **Comprehensive attribute documentation**

#### **Additional Best Practices:**

- **Performance notes** for expensive operations
- **Warning sections** for gotchas and pitfalls
- **Note sections** for important information
- **TODO/FIXME** comments with issue references
- **Code outputs** in examples (# Output: ...)
- **Error examples** showing exception handling
- **Real-world usage** patterns and integration

### Module Documentation with Full Sphinx Support

and usage patterns. Include architectural decisions and design patterns.

Examples:
Basic usage example::

        from haive.core import ReactAgent
        agent = ReactAgent(name="test", model="gpt-4")
        result = agent.process("Hello world")

    Advanced usage::

        with ReactAgent.from_config(config) as agent:
            result = agent.batch_process(tasks)

"""

````

### Enhanced Function Documentation Standards [MEM-013]

```python
from typing import List, Dict, Any, Optional, Union, Tuple, AsyncIterator
from pathlib import Path
import asyncio
from haive.core.agent import ReactAgent
from haive.core.schema import AgentResponse, ToolCall, MessageType

def process_agent_request(
    agent: ReactAgent,
    request: str,
    save_history: bool = True,
    tools: Optional[List[str]] = None,
    timeout: Optional[float] = None,
    stream: bool = False,
    callbacks: Optional[List[callable]] = None
) -> Union[AgentResponse, AsyncIterator[AgentResponse]]:
    """Process agent request with comprehensive configuration options.

    This function handles agent requests with support for streaming responses,
    custom tool selection, callbacks, and conversation history management.
    It implements retry logic, error recovery, and state persistence.

    The processing pipeline:
    1. Validates agent configuration and request format
    2. Optionally overrides agent tools for this request
    3. Executes request with timeout and retry logic
    4. Streams or returns complete response based on `stream` parameter
    5. Persists conversation history if enabled
    6. Triggers callbacks at key processing stages

    Args:
        agent: Configured ReactAgent instance with valid model and tools.
            Must be initialized with proper authentication.
        request: User request string, supports markdown formatting.
            Maximum 4000 characters. Empty strings raise ValueError.
        save_history: Whether to save conversation history to persistent storage.
            Default True. History saved to agent.history_path if set.
        tools: Optional tool override for this request only.
            If None, uses agent's default tools. Invalid tools raise ValueError.
        timeout: Maximum seconds to wait for response. None uses agent default.
            Range: 10-600 seconds. Timeout raises asyncio.TimeoutError.
        stream: Return streaming response iterator instead of complete response.
            Useful for real-time UI updates. Incompatible with some callbacks.
        callbacks: List of callback functions called during processing.
            Callbacks receive (stage: str, data: Dict) parameters.

    Returns:
        Union[AgentResponse, AsyncIterator[AgentResponse]]:
            If stream=False: Complete AgentResponse with all fields populated.
            If stream=True: Async iterator yielding partial responses.

            AgentResponse contains:
            - response: Generated text response
            - tool_calls: List of ToolCall objects if tools were used
            - metadata: Processing metadata (timing, tokens, model)
            - conversation_id: Unique conversation identifier
            - message_history: Full conversation if save_history=True

    Raises:
        ValueError: Invalid input parameters:
            - Empty request string
            - Invalid tool names in tools parameter
            - Agent not properly configured
        asyncio.TimeoutError: Request exceeded timeout
        ProcessingError: Request processing failed:
            - Model API errors
            - Tool execution failures
            - State persistence errors
        ConnectionError: Network issues accessing model API

    Examples:
        Basic synchronous processing::

            agent = ReactAgent(name="helper", model="gpt-4")
            response = process_agent_request(agent, "What's 2+2?")
            print(response.response)
            # Output: "2 + 2 equals 4"

        With custom tools and timeout::

            response = process_agent_request(
                agent,
                "Search for Python tutorials and summarize",
                tools=["web_search", "summarizer"],
                timeout=30.0
            )
            print(f"Used tools: {[tc.tool for tc in response.tool_calls]}")
            # Output: Used tools: ['web_search', 'summarizer']

        Streaming response for real-time UI::

            async def stream_response():
                async for partial in process_agent_request(
                    agent,
                    "Write a story about AI",
                    stream=True
                ):
                    print(partial.response, end="", flush=True)
                    # Prints story as it's generated

            asyncio.run(stream_response())

        With callbacks for monitoring::

            def progress_callback(stage: str, data: Dict):
                print(f"[{stage}] {data.get('message', '')}")

            response = process_agent_request(
                agent,
                "Complex analysis task",
                callbacks=[progress_callback]
            )
            # Output:
            # [start] Beginning request processing
            # [tool_call] Invoking calculator
            # [tool_result] Calculator returned: 42
            # [complete] Request processed successfully

        Error handling example::

            try:
                response = process_agent_request(
                    agent,
                    "Use the quantum_computer tool",
                    tools=["quantum_computer"],  # Invalid tool
                    timeout=5.0
                )
            except ValueError as e:
                print(f"Invalid tool: {e}")
                # Output: Invalid tool: Unknown tools: quantum_computer
            except asyncio.TimeoutError:
                print("Request timed out")

        Conversation history management::

            # First request saves history
            response1 = process_agent_request(
                agent,
                "My name is Alice",
                save_history=True
            )

            # Second request has context
            response2 = process_agent_request(
                agent,
                "What's my name?",
                save_history=True
            )
            print(response2.response)
            # Output: "Your name is Alice."

            # Check history
            print(len(response2.message_history))
            # Output: 4 (2 user messages + 2 assistant messages)

    See Also:
        - :class:`ReactAgent`: Agent configuration and initialization
        - :class:`AgentResponse`: Response structure documentation
        - :func:`create_agent`: Agent factory function
        - :ref:`streaming-guide`: Streaming responses guide
        - :ref:`tool-usage`: Tool selection and usage patterns

    Note:
        When using streaming mode, callbacks are called for each chunk.
        This can result in many callback invocations for long responses.
        Consider using debouncing or filtering in callbacks.

    Warning:
        Streaming mode is incompatible with some tools that require
        complete context before execution (e.g., code_executor).

    .. versionadded:: 1.0.0
        Initial implementation with basic functionality
    .. versionchanged:: 1.2.0
        Added streaming support and callbacks
    .. versionchanged:: 1.3.0
        Added tool override parameter
    .. deprecated:: 1.4.0
        The `max_retries` parameter is deprecated. Use agent config instead.
    """
    # Implementation details...

async def batch_process_requests(
    agent: ReactAgent,
    requests: List[Union[str, Dict[str, Any]]],
    *,
    max_concurrent: int = 5,
    stop_on_error: bool = False,
    progress_callback: Optional[callable] = None,
    save_results: Optional[Path] = None
) -> List[Union[AgentResponse, Exception]]:
    """Process multiple agent requests concurrently with rate limiting.

    Efficiently processes batches of requests with configurable concurrency,
    error handling, progress tracking, and optional result persistence.
    Implements intelligent rate limiting to avoid API throttling.

    Args:
        agent: Configured agent for processing all requests.
        requests: List of request strings or dicts with 'request' and 'metadata'.
            Dict format: {'request': str, 'metadata': dict, 'tools': list}
        max_concurrent: Maximum concurrent requests (1-20). Default 5.
            Higher values risk API rate limits.
        stop_on_error: Stop processing on first error. Default False.
            When False, errors are returned in results list.
        progress_callback: Called with (completed: int, total: int, current: str).
            Useful for progress bars. None disables progress tracking.
        save_results: Path to save results JSON. None disables saving.
            Creates parent directories if needed.

    Returns:
        List of AgentResponse objects or Exception objects for failed requests.
        Order matches input requests order. Successful responses are
        AgentResponse instances, failures are Exception instances.

    Raises:
        ValueError: Invalid input parameters (empty requests, invalid concurrent)
        IOError: Cannot write to save_results path
        KeyboardInterrupt: User interrupted batch processing

    Examples:
        Simple batch processing::

            requests = [
                "What is Python?",
                "Explain machine learning",
                "Compare React and Vue"
            ]

            responses = await batch_process_requests(agent, requests)
            for req, resp in zip(requests, responses):
                if isinstance(resp, Exception):
                    print(f"Failed: {req} - {resp}")
                else:
                    print(f"Success: {req[:20]}... - {len(resp.response)} chars")

        With metadata and progress tracking::

            requests = [
                {"request": "Analyze this", "metadata": {"priority": "high"}},
                {"request": "Summarize that", "tools": ["summarizer"]}
            ]

            def show_progress(done: int, total: int, current: str):
                print(f"Progress: {done}/{total} - Processing: {current[:50]}...")

            responses = await batch_process_requests(
                agent,
                requests,
                max_concurrent=3,
                progress_callback=show_progress
            )

        Save results with error handling::

            responses = await batch_process_requests(
                agent,
                requests,
                save_results=Path("results/batch_001.json"),
                stop_on_error=False  # Continue even if some fail
            )

            # Check results
            successful = [r for r in responses if isinstance(r, AgentResponse)]
            failed = [r for r in responses if isinstance(r, Exception)]
            print(f"Success: {len(successful)}, Failed: {len(failed)}")

    Performance Notes:
        - Processes in batches of max_concurrent to avoid overwhelming API
        - Implements exponential backoff on rate limit errors
        - Total time ≈ (num_requests / max_concurrent) * avg_response_time
        - Memory usage grows with max_concurrent and response sizes

    .. versionadded:: 1.2.0
    """
    # Implementation...
````

## 🛠️ Quality Assurance

### Pre-commit Checklist [MEM-010]

- [ ] **Memory System**: All relevant [MEM-XXX] files updated
- [ ] **Global Protection**: No ~/.claude/CLAUDE.md modifications without permission
- [ ] **Git Safety**: `git status` and `git diff` reviewed
- [ ] **File Organization**: Proper numbered naming and structure
- [ ] **Cross-References**: All [MEM-XXX] tags valid and linked
- [ ] **Import Standards**: Clear haive.core.\* references, no generic imports
- [ ] **No Print Statements**: All print() replaced with logger.debug()
- [ ] **Type Hints**: All public functions have complete type annotations
- [ ] **Docstrings**: Google-style docstrings for all classes/functions
- [ ] **Real Testing**: All tests use real components, ZERO mocks
- [ ] **No Hardcoded Secrets**: All sensitive data in environment variables
- [ ] **Poetry Standards**: All commands use `poetry run`
- [ ] **Linting**: `trunk check` or `poetry run ruff check` passes
- [ ] **Test Suite**: `poetry run pytest` passes completely
- [ ] **Import Verification**: `poetry run python -c "import haive.core"` succeeds

### Code Review Standards

```bash
# MANDATORY before any work - USER CREATES MESSES
git status    # See what's changed
git diff      # See EXACTLY what changes were made
git add -A    # Stage everything when ready

# MANDATORY checks before committing
poetry run pytest
poetry run ruff check
poetry run mypy

# During development
logger.debug("Processing started")  # Not print()
real_agent.process(input)  # Not mock_agent

# Verify package structure
find . -name "*.py" -exec python -m py_compile {} \;
grep -r "from utils import" . && echo "❌ FOUND GENERIC IMPORTS"
grep -r "print(" . --include="*.py" && echo "❌ FOUND PRINT STATEMENTS"

# CRITICAL: Always check what user changed
git status --porcelain | head -20  # Show first 20 changes
git diff --name-only | head -10     # Show changed files
```

### 🚨 CRITICAL USER BEHAVIOR WARNINGS

**THE USER CREATES ABSOLUTE CHAOS AND IGNORES ALL STANDARDS**

#### 🔥 Known Destructive Patterns:

- **NOT storing memories in project_docs** - Loses all context, destroys continuity
- **NOT using git properly** - Creates merge conflicts, loses work, no commit history
- **NOT linting with trunk** - Introduces massive code quality disasters, breaks CI/CD
- **NOT following code style** - Makes codebase unmaintainable, inconsistent, broken
- **Making a mess with files** - Random files everywhere, no organization, chaos
- **NOT considering if ruining previous work** - Destroys working functionality
- **NOT using core memories properly** - Ignores established patterns, reinvents broken wheels
- **Ignoring TodoWrite system** - No planning, chaotic execution
- **Creating random test files** - Pollutes test structure, breaks test discovery
- **Using print() instead of logging** - Breaks production, no log levels
- **Breaking import structure** - Circular dependencies, broken packages

#### 🛑 MANDATORY DAMAGE CONTROL PROTOCOL

**BEFORE TOUCHING ANYTHING:**

```bash
# 1. FORCE CHECK WHAT DISASTER THE USER CREATED
git status --porcelain
git diff --name-only | head -20
find . -name "*.py" -newer .git/HEAD | head -10

# 2. CHECK FOR COMMON USER DISASTERS
grep -r "print(" . --include="*.py" | head -5
find . -name "*.py" -exec python -m py_compile {} \; 2>&1 | head -10
find . -type f -name "test_*.py" | wc -l  # Check for random test files

# 3. VERIFY MEMORY SYSTEM STILL EXISTS
ls -la project_docs/CLAUDE_MEMORY_METHODOLOGY.md
ls -la project_docs/claude_documentation/
ls -la CLAUDE.md

# 4. CHECK CORE IMPORTS STILL WORK
poetry run python -c "from haive.core import BaseGraph; print('Core imports OK')" || echo "🚨 CORE BROKEN"
```

#### 🎯 RECOVERY AND PREVENTION PATTERNS

**1. Memory Recovery:**

```bash
# If user destroyed project_docs structure
mkdir -p project_docs/claude_documentation/
mkdir -p project_docs/progress_tracking/
mkdir -p project_docs/individual_components/

# Restore critical memory files if missing
if [ ! -f "project_docs/CLAUDE_MEMORY_METHODOLOGY.md" ]; then
    echo "🚨 USER DESTROYED MEMORY METHODOLOGY - RECREATING"
    # Recreate from backup or template
fi
```

**2. Git Disaster Recovery:**

```bash
# If user made a mess with git
git status
git stash push -m "User mess cleanup"
git reset --hard HEAD  # Only if absolutely necessary
git clean -fd  # Remove untracked files
```

**3. Code Quality Emergency Repair:**

```bash
# Remove user's print statement disasters
find . -name "*.py" -exec sed -i 's/print(/logger.debug(/g' {} \;
find . -name "*.py" -exec sed -i '1i import logging; logger = logging.getLogger(__name__)' {} \;

# Run trunk linting (what user should have done)
trunk check --fix --all
# If trunk not installed/configured, use alternatives:
poetry run ruff check --fix .
poetry run black .
poetry run isort .
```

**4. File Organization Cleanup:**

```bash
# Move random files to proper locations
find . -maxdepth 1 -name "*.py" -not -path "./packages/*" -exec mv {} temp_cleanup/ \;
find . -maxdepth 1 -name "test_*.py" -exec mv {} tests/user_mess/ \;
```

#### 🔒 PROTECTION PROTOCOLS

**Before ANY work:**

1. **SAVE CURRENT STATE**: `git stash push -m "Pre-work safety backup"`
2. **READ ALL MEMORY**: Load context from project_docs/
3. **CHECK IMPORTS**: Verify core functionality works
4. **DOCUMENT PLAN**: Write TodoWrite with specific steps
5. **WORK INCREMENTALLY**: One small change at a time
6. **TEST CONSTANTLY**: After every single change

**During work:**

1. **NEVER trust user descriptions** - Always verify with git diff
2. **ALWAYS use memory system** - Store progress in project_docs/
3. **ALWAYS use proper imports** - from haive.core.\* not random imports
4. **ALWAYS use logging** - Never print statements
5. **ALWAYS check dependencies** - Don't break existing functionality

**After work:**

1. **RUN FULL TEST SUITE**: `poetry run pytest`
2. **RUN LINTING**: `trunk check --all` (or `poetry run ruff check`)
3. **VERIFY IMPORTS**: `poetry run python -c "import haive.core"`
4. **UPDATE MEMORY**: Document what was done in project_docs/
5. **CLEAN COMMIT**: Proper commit message with context

#### 📚 MEMORY SYSTEM ENFORCEMENT

**MANDATORY Memory Usage:**

```bash
# ALWAYS check these exist before starting work
[ -f "project_docs/CLAUDE_MEMORY_METHODOLOGY.md" ] || echo "🚨 NO MEMORY METHODOLOGY"
[ -f "CLAUDE.md" ] || echo "🚨 NO MAIN ROUTING"
[ -d "project_docs/claude_documentation/" ] || echo "🚨 NO CLAUDE DOCS"

# ALWAYS read context first
cat project_docs/claude_documentation/CLAUDE_QUICKREF.md
cat CLAUDE.md | head -50

# ALWAYS use TodoWrite for planning
# NEVER start work without a plan in TodoWrite
```

**Memory Documentation Requirements:**

1. **Every major change** → Update progress_tracking/
2. **Every new component** → Create individual_components/ entry
3. **Every bug fix** → Document in relevant package docs
4. **Every refactor** → Update cross-references
5. **Every new pattern** → Add to methodology

**Core Memory Protection:**

```bash
# Backup critical memory files
cp project_docs/CLAUDE_MEMORY_METHODOLOGY.md /tmp/memory_backup.md
cp CLAUDE.md /tmp/routing_backup.md

# Check memory system integrity
find project_docs/ -name "*.md" -exec grep -l "CLAUDE" {} \; | wc -l
find . -name "CLAUDE*.md" -exec ls -la {} \;
```

### Core Codebase Maintenance Standards

#### 1. **Module Organization Rules**

```python
# ✅ CORRECT - Clear module hierarchy
haive/
├── core/                    # Core functionality (engines, graphs, schemas)
│   ├── engine/             # Engine implementations
│   │   ├── base/           # Base engine classes
│   │   ├── agent/          # Agent-specific engines
│   │   └── llm/            # LLM-specific engines
│   ├── graph/              # Graph building system
│   │   ├── state_graph/    # State graph implementation
│   │   ├── node/           # Node types and factories
│   │   └── patterns/       # Common graph patterns
│   └── schema/             # Schema management
│       ├── prebuilt/       # Pre-built schemas
│       └── compatibility/  # Schema conversion utilities
├── agents/                 # Agent implementations
│   ├── conversational/    # Chat-based agents
│   ├── task/              # Task-oriented agents
│   └── specialized/       # Domain-specific agents
├── tools/                  # Tool implementations
│   ├── web/               # Web-related tools
│   ├── file/              # File operations
│   ├── math/              # Mathematical tools
│   └── api/               # API integration tools
└── games/                  # Game implementations
    ├── board/             # Board games
    ├── strategy/          # Strategy games
    └── puzzle/            # Puzzle games
```

#### 2. **Import Dependency Rules**

```python
# ✅ CORRECT - Dependency flow
# Core can import from: standard library, third-party only
# Agents can import from: core, standard library, third-party
# Tools can import from: core, standard library, third-party
# Games can import from: core, agents, tools, standard library, third-party

# ❌ WRONG - Circular dependencies
# Core importing from agents/tools/games
# Agents importing from games
```

#### 3. **Package Boundary Enforcement**

```python
# ✅ CORRECT - Explicit cross-package imports
from haive.core.engine import ReactAgent
from haive.tools.math import Calculator
from haive.agents.conversational import ChatAgent

class MyCustomAgent(ReactAgent):
    def __init__(self):
        super().__init__()
        self.calculator = Calculator()
        self.chat_agent = ChatAgent()

# ❌ WRONG - Implicit or unclear imports
from engine import ReactAgent     # Which package?
from tools import Calculator      # No clear boundary
import agents                     # Too broad
```

### Memory Maintenance Standards [MEM-011]

#### After Each Task (MANDATORY):

```bash
# 1. UPDATE relevant memory files with [MEM-XXX] tags
echo "## [$(date +%Y-%m-%d)] Task Completed" >> project_docs/progress_tracking/02_IN_PROGRESS.md
echo "- Task: [Description]" >> project_docs/progress_tracking/02_IN_PROGRESS.md
echo "- Memory Reference: [MEM-XXX]" >> project_docs/progress_tracking/02_IN_PROGRESS.md
echo "- Files Modified: [List]" >> project_docs/progress_tracking/02_IN_PROGRESS.md
echo "- Cross-References Updated: [List]" >> project_docs/progress_tracking/02_IN_PROGRESS.md

# 2. CREATE component-specific memory if new component
mkdir -p project_docs/individual_components/[component_name]/
touch project_docs/individual_components/[component_name]/01_ANALYSIS.md
touch project_docs/individual_components/[component_name]/02_FIXES_APPLIED.md
touch project_docs/individual_components/[component_name]/03_CROSS_REFERENCES.md

# 3. VERIFY all [MEM-XXX] cross-references work
grep -r "\[MEM-" project_docs/ | grep -v ".md:" | wc -l  # Count references
find project_docs/ -name "*.md" -exec grep -l "\[MEM-" {} \; | wc -l  # Count files with refs

# 4. UPDATE success metrics
echo "Completed: $(date)" >> project_docs/progress_tracking/01_COMPLETED.md
```

#### Weekly Memory Hygiene (CRITICAL):

```bash
# 1. CONSOLIDATE duplicate information
find project_docs/ -name "*.md" -exec grep -l "duplicate content pattern" {} \;
# Review and merge duplicate sections

# 2. UPDATE navigation documents
# Regenerate 00_MEMORY_INDEX.md with current [MEM-XXX] structure
# Update 00_CLAUDE_INDEX.md with new memory additions

# 3. VALIDATE all cross-references
for file in $(find project_docs/ -name "*.md"); do
  grep -o "\[MEM-[^]]*\]" "$file" | sort -u
done | sort | uniq -c | sort -nr

# 4. ARCHIVE completed work to maintain clean structure
mv project_docs/progress_tracking/02_IN_PROGRESS.md project_docs/progress_tracking/archive/
touch project_docs/progress_tracking/02_IN_PROGRESS.md

# 5. BACKUP critical memory files
cp project_docs/CLAUDE_MEMORY_METHODOLOGY.md backup/methodology_$(date +%Y%m%d).md
cp CLAUDE.md backup/routing_$(date +%Y%m%d).md
```

#### Memory Integrity Checks [MEM-011-A]:

```bash
# Check memory system health
check_memory_integrity() {
  echo "🔍 Memory System Health Check"
  echo "================================"

  # 1. Core files exist
  [ -f "CLAUDE.md" ] && echo "✅ Main routing exists" || echo "🚨 MISSING: CLAUDE.md"
  [ -f "project_docs/CLAUDE_MEMORY_METHODOLOGY.md" ] && echo "✅ Methodology exists" || echo "🚨 MISSING: Methodology"

  # 2. Memory structure intact
  [ -d "project_docs/claude_documentation/" ] && echo "✅ Claude docs exist" || echo "🚨 MISSING: Claude docs"
  [ -d "project_docs/progress_tracking/" ] && echo "✅ Progress tracking exists" || echo "🚨 MISSING: Progress tracking"

  # 3. Global memory protected
  ls -la ~/.claude/CLAUDE.md 2>/dev/null && echo "✅ Global memory protected" || echo "⚠️  Global memory not found"

  # 4. Cross-reference count
  ref_count=$(grep -r "\[MEM-" project_docs/ 2>/dev/null | wc -l)
  echo "📊 Cross-references found: $ref_count"

  # 5. Recent updates
  recent_files=$(find project_docs/ -name "*.md" -mtime -7 | wc -l)
  echo "📅 Files updated in last 7 days: $recent_files"
}

# Run check
check_memory_integrity
```

## 🔗 Cross-Reference System

### Reference Pattern

```markdown
**Reference**: [CLAUDE_QUICKREF.md](claude_documentation/CLAUDE_QUICKREF.md)  
**Parent**: [Main Project](../CLAUDE.md)  
**Related**: [Package Documentation](haive-core/)  
**Child**: [Component Details](individual_components/)
```

### Navigation Links

- **Top of Document**: Essential navigation
- **Bottom of Document**: Extended references
- **Inline References**: Specific technical links

## 📈 Success Metrics

### Memory Quality Indicators

- **Navigation Efficiency**: Find any info in < 3 clicks
- **Cross-Reference Coverage**: 100% of documents linked
- **Information Currency**: Updated within 24 hours
- **Duplication Minimization**: No redundant information

### Development Efficiency

- **Context Loading**: < 2 minutes to understand current state
- **Decision Speed**: Standards clearly documented
- **Knowledge Retention**: Previous work discoverable
- **Quality Consistency**: All code follows standards

## 🚀 Implementation Guidelines

### For New Components

1. **Create memory structure first**
2. **Document before coding**
3. **Test with real components**
4. **Update cross-references**
5. **Maintain quality metrics**

### For Existing Components

1. **Load context from memory**
2. **Follow established patterns**
3. **Update documentation immediately**
4. **Test changes thoroughly**
5. **Update progress tracking**

## 🎓 Key Takeaways

### 1. Memory First, Code Second

- Always load full context before starting
- Update memory as you learn
- Use memory to guide decisions

### 2. Quality Over Speed

- No print statements ever
- Real components in tests
- Complete type hints

### 3. Living Documentation

- Update immediately when things change
- Regular review and consolidation
- Cross-reference validation

### 4. Consistent Standards

- PEP 8 compliance
- Google-style docstrings
- Poetry for all commands

### 5. Real Testing

- No mocks in tests
- Save actual state history
- Test behavior, not implementation

---

## 📚 Essential References

### Navigation Hub

- **Main Routing**: [CLAUDE.md](../CLAUDE.md)
- **Quick Commands**: [CLAUDE_QUICKREF.md](claude_documentation/CLAUDE_QUICKREF.md)
- **Project Structure**: [Package Documentation](../packages/)

### Code Standards

- **Python**: PEP 8 + type hints + Google docstrings
- **Testing**: pytest + real components + descriptive names
- **Git**: Conventional commits + feature branches

### Memory System

- **Global**: ~/.claude/CLAUDE.md
- **Project**: This file + claude_documentation/
- **Package**: Individual README files
- **Component**: progress_tracking/ + individual_components/

**Next Steps**: Apply this unified methodology to all Haive development work and maintain consistency across all packages.
