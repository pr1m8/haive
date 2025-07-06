# CLAUDE.md - Haive Agent Development & Memory System

**Version**: 2.0  
**Purpose**: Comprehensive guide for Claude Code to develop agents with smart memory management  
**Date**: 2025-01-06  
**Memory System**: Active

## 🧠 Memory Architecture Overview

This document serves as Claude Code's primary reference for developing agents in the Haive framework. It includes:

- Agent development patterns and best practices
- Code style guidelines specific to Haive
- Smart memory management system
- Self-documenting workspace structure

## 🚀 Quick Start

```bash
# Always use poetry run for all commands
poetry run python -m haive.your_module
poetry run pytest packages/your_package/tests/

# Common commands for agent development
poetry run python -m haive.agents.simple --example
poetry run pytest packages/haive-agents/tests/test_simple/ -v
```

**Package Location**: `/home/will/Projects/haive/backend/haive/packages/`  
**Test Location**: `packages/{package_name}/tests/`  
**Claude Workspace**: `/home/will/Projects/haive/backend/haive/project_docs/claude_sessions/`

## 📁 Claude Code Workspace Structure

When working on agent development, create your own workspace:

```
project_docs/claude_sessions/{session_id}/
├── SESSION_INFO.md          # Session metadata and goals
├── memory/
│   ├── context.md          # Current working context
│   ├── decisions.md        # Design decisions and rationale
│   └── issues.md           # Problems encountered and solutions
├── agents/
│   ├── {agent_name}/       # Agent-specific development
│   │   ├── design.md       # Architecture and design
│   │   ├── implementation.md # Code snippets and patterns
│   │   └── testing.md      # Test strategies and results
│   └── patterns.md         # Reusable patterns discovered
└── references/
    ├── code_snippets.md    # Useful code examples
    └── dependencies.md     # Package dependencies tracked
```

### Creating Your Workspace

```python
# When starting a new agent development session:
session_id = f"claude_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
workspace_path = f"/home/will/Projects/haive/backend/haive/project_docs/claude_sessions/{session_id}"
```

## 🎯 Agent Development Guide

### 1. Understanding the Agent Hierarchy

```
Agent (Abstract Base)
├── SimpleAgent          # Basic conversational agent
├── ReactAgent          # Reasoning and acting agent
├── BaseRAGAgent        # Retrieval-augmented generation
├── PersonResearchAgent # Specialized research agent
└── [Your New Agent]    # Custom implementations
```

### 2. Essential Agent Components

Every agent needs:

1. **State Schema** - Defines the agent's memory structure
2. **Configuration** - Agent-specific settings
3. **Graph Builder** - Workflow definition
4. **Engine Integration** - LLM or tool connections

### 3. Agent Development Workflow

```python
# Step 1: Define State Schema
from haive.core.schema import StateSchema
from pydantic import Field
from typing import List, Dict, Any

class MyAgentState(StateSchema):
    """State schema for custom agent."""
    messages: List[str] = Field(default_factory=list)
    context: Dict[str, Any] = Field(default_factory=dict)
    custom_field: str = Field(default="")

# Step 2: Create Agent Class
from haive.agents.base import Agent
from haive.core.graph import BaseGraph

class MyCustomAgent(Agent[MyAgentState]):
    """Custom agent implementation."""

    def setup_agent(self) -> None:
        """Initialize agent components."""
        # Sync fields from engine
        self._sync_fields_from_engine()
        # Setup schemas
        self._setup_schemas()
        # Build initial graph
        self._build_initial_graph()

    def build_graph(self) -> BaseGraph:
        """Define agent workflow."""
        graph = BaseGraph()

        # Add nodes
        graph.add_node("process", self._process_input)
        graph.add_node("respond", self._generate_response)

        # Add edges
        graph.add_edge("process", "respond")
        graph.set_entry_point("process")

        return graph.compile()

# Step 3: Test Your Agent
async def test_agent():
    agent = MyCustomAgent(
        name="test_agent",
        engine=aug_llm_engine
    )

    result = await agent.arun("Hello!")
    assert result is not None
```

## 💻 Code Style Guidelines for Haive

### Core Principles

1. **Type Everything** - No untyped public APIs
2. **Async First** - All agent operations should be async
3. **Composition Over Inheritance** - Use mixins and composition
4. **Defensive Programming** - Validate inputs, handle errors gracefully
5. **Clear Naming** - `create_rag_agent_with_vector_store` not `make_agent`

### Haive-Specific Patterns

```python
# ALWAYS: Use Pydantic for configurations
from pydantic import BaseModel, Field

class AgentConfig(BaseModel):
    """Configuration for agent."""
    name: str = Field(..., description="Agent identifier")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)

    class Config:
        validate_assignment = True
        extra = "forbid"  # Prevent unknown fields

# ALWAYS: Use proper error handling
from haive.core.exceptions import AgentError, ConfigurationError

async def execute_agent_task(agent: Agent, task: str) -> str:
    """Execute task with proper error handling."""
    try:
        result = await agent.arun(task)
        return result
    except ValidationError as e:
        raise ConfigurationError(f"Invalid task format: {e}")
    except TimeoutError:
        raise AgentError(f"Agent {agent.name} timed out")
    except Exception as e:
        logger.exception(f"Unexpected error in {agent.name}")
        raise AgentError(f"Execution failed: {e}")

# ALWAYS: Use structured logging
from haive.core.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "Processing agent request",
    extra={
        "agent_name": agent.name,
        "task_type": task.type,
        "timestamp": datetime.utcnow().isoformat()
    }
)
```

### Testing Standards

```python
# ALWAYS: Use descriptive test names
async def test_simple_agent_maintains_conversation_state_across_multiple_turns():
    """Test that agent preserves context between interactions."""
    # Test implementation

# ALWAYS: Test error conditions
async def test_agent_handles_invalid_configuration_gracefully():
    """Test agent behavior with invalid config."""
    with pytest.raises(ConfigurationError, match="temperature must be between"):
        agent = SimpleAgent(temperature=3.0)

# ALWAYS: Use fixtures for common setup
@pytest.fixture
def configured_agent() -> SimpleAgent:
    """Create a properly configured test agent."""
    return SimpleAgent(
        name="test_agent",
        engine=create_test_engine()
    )
```

## 🧠 Smart Memory Management

### Memory Patterns for Agent Development

When developing agents, track:

1. **Design Decisions**

   ```markdown
   # Decision: Use SchemaComposer for dynamic state

   **Rationale**: Allows runtime schema generation from engines
   **Trade-offs**: More complex but more flexible
   **Alternative**: Static schemas (simpler but less adaptable)
   ```

2. **Common Issues & Solutions**

   ```markdown
   # Issue: Schema generation fails with multiple engines

   **Root Cause**: Field name conflicts between engines
   **Solution**: Use field prefixing in SchemaComposer
   **Code**: See schema_composer.py:L234
   ```

3. **Performance Insights**

   ```markdown
   # Performance: Streaming vs Batch Response

   **Finding**: Streaming reduces memory by 70% for large responses
   **Implementation**: Use astream() for responses > 1000 tokens
   **Benchmark**: 100ms first token vs 3s full response
   ```

### Memory File Templates

#### SESSION_INFO.md

```markdown
# Session: {session_id}

**Date**: {date}
**Goal**: Implement {agent_type} agent with {key_features}
**Related Issues**: #{issue_numbers}

## Objectives

1. Create base agent structure
2. Implement {specific_feature}
3. Add comprehensive tests
4. Document usage patterns

## Key Decisions

- Chose {approach} because {reason}
- Using {pattern} for {purpose}

## Results

- [ ] Agent class implemented
- [ ] Tests passing
- [ ] Documentation complete
- [ ] Example created
```

#### memory/context.md

```markdown
# Current Context

## Working On

- Implementing {feature} for {agent}
- File: {file_path}
- Line: {line_range}

## Key Insights

- Schema composition happens in `_setup_schemas()`
- Tool routing uses `tool_route` field
- Engine registration required for node discovery

## Next Steps

1. Complete {current_task}
2. Test {functionality}
3. Update documentation
```

## 🔧 Common Tasks & Solutions

### Creating a New Agent Type

```bash
# 1. Create module structure
mkdir -p packages/haive-agents/src/haive/agents/new_agent_type
touch packages/haive-agents/src/haive/agents/new_agent_type/{__init__.py,agent.py,config.py,state.py,example.py}

# 2. Run tests as you develop
poetry run pytest packages/haive-agents/tests/test_new_agent_type/ -v --lf

# 3. Check type safety
poetry run mypy packages/haive-agents/src/haive/agents/new_agent_type/
```

### Debugging Schema Issues

```python
# Debug schema generation
from haive.core.schema import SchemaComposer

# Inspect generated schema
composer = SchemaComposer(base_state_schema=MyAgentState)
schema = composer.compose_state([engine1, engine2])
print(schema.schema())  # View full schema

# Check field conflicts
for field_name, field_info in schema.__fields__.items():
    print(f"{field_name}: {field_info.type_}")
```

### Tool Integration Patterns

```python
# Pattern 1: Direct tool assignment
from haive.core.tools import tool

@tool
def calculate(expression: str) -> float:
    """Calculate mathematical expression."""
    return eval(expression)  # Simplified example

# Pattern 2: Tool routing
tool_routes = {
    "calculate": "calculator_engine",
    "search": "search_engine",
    "default": "main_engine"
}

# Pattern 3: Dynamic tool loading
from haive.core.registry import ToolRegistry

registry = ToolRegistry.get_instance()
for tool_name in config.enabled_tools:
    tool = registry.get_tool(tool_name)
    agent.add_tool(tool)
```

## 📊 Key Architecture Insights

### Schema System

- **StateSchema**: Base class for all agent states
- **SchemaComposer**: Dynamically generates schemas from engines
- **AgentSchemaComposer**: Handles multi-agent schema composition
- **Field Syncing**: Automatic field discovery from engines

### Engine System

- **BaseEngine**: Abstract engine interface
- **AugLLMEngine**: Enhanced LLM with tools
- **EngineRegistry**: Global engine registration
- **Engine Nodes**: Graph nodes that use engines

### Graph System

- **BaseGraph**: Core workflow definition
- **Node Types**: Regular, Engine, Conditional
- **Edge Types**: Direct, Conditional, Mapped
- **Compilation**: Graph → Executable workflow

## 🚦 Quick Reference Commands

```bash
# Run specific agent tests
poetry run pytest packages/haive-agents/tests/test_simple/ -k "test_name"

# Check test coverage
poetry run pytest --cov=haive.agents --cov-report=html

# Lint code
poetry run ruff check packages/haive-agents/src/

# Format code
poetry run black packages/haive-agents/src/

# Type checking
poetry run mypy packages/haive-agents/src/

# Run example
poetry run python packages/haive-agents/examples/simple_conversation.py

# Build documentation
poetry run sphinx-build -b html docs/source docs/build
```

## 🔗 Essential Resources

### Documentation

- **Agent Patterns**: `/project_docs/claude_agent_memory/agent_patterns/`
- **Schema Analysis**: `/project_docs/claude_agent_memory/schema_analysis/`
- **Code Examples**: `/packages/haive-agents/examples/`
- **Test Examples**: `/packages/haive-agents/tests/`

### Key Files to Study

- `packages/haive-core/src/haive/core/schema.py` - Schema system
- `packages/haive-core/src/haive/core/engine.py` - Engine base
- `packages/haive-agents/src/haive/agents/base.py` - Agent base
- `packages/haive-agents/src/haive/agents/simple/agent.py` - Simple implementation

### When Stuck

1. Check existing implementations in `/packages/haive-agents/src/haive/agents/`
2. Look for patterns in `/project_docs/claude_agent_memory/`
3. Review tests for usage examples
4. Create memory note for future reference

---

**Remember**: Always maintain your session workspace for continuity across conversations. Your memory is your strength in developing complex agents!
