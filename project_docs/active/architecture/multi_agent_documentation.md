# Multi-Agent System Documentation

**Version**: 1.0  
**Purpose**: Documentation for the clean, simple multi-agent implementation  
**Last Updated**: 2025-01-17

## 🎯 Overview

The Haive multi-agent system provides a clean, simple way to coordinate multiple agents with intelligent routing and execution patterns. It uses the `MultiAgent` class from `haive.agents.multi.clean` for straightforward agent coordination.

## 🚀 Quick Start

### Basic Sequential Multi-Agent

```python
from haive.agents.multi import MultiAgent
from haive.agents.simple import SimpleAgent
from haive.agents.react import ReactAgent
from haive.core.engine.aug_llm import AugLLMConfig

# Create individual agents
writer = SimpleAgent(
    name="writer",
    engine=AugLLMConfig(
        system_message="You are a creative writer. Write engaging stories.",
        temperature=0.8
    )
)

editor = ReactAgent(
    name="editor",
    engine=AugLLMConfig(
        system_message="You are an editor. Improve and refine text.",
        temperature=0.3
    ),
    tools=[grammar_checker, style_analyzer]
)

# Create multi-agent system
content_pipeline = MultiAgent.create(
    agents=[writer, editor],
    name="content_pipeline",
    execution_mode="sequential"
)

# Run the system
result = await content_pipeline.arun("Write a story about AI discovering emotions")
```

## 📋 Core Features

### 1. **Simple Agent Management**

- Agents stored as dictionary with automatic list→dict conversion
- Agent names used as keys for easy access
- Supports both single `agent` and multiple `agents` fields

### 2. **Execution Modes**

- **`"sequential"`**: Execute agents one after another in order
- **`"parallel"`**: Execute agents simultaneously (future feature)
- **`"infer"`**: Automatically determine execution pattern (default)
- **`"conditional"`**: Route based on conditions
- **`"branch"`**: Complex branching logic

### 3. **State Management**

- Uses `MultiAgentState` for coordinated state management
- Automatic agent registration in state
- Hierarchical state isolation per agent
- Engine synchronization across agents

### 4. **Intelligent Routing**

- Leverages `BaseGraph` for intelligent routing
- Automatic sequence inference from agent dependencies
- Support for conditional branching
- Clean agent name routing (no prefixes)

## 💻 API Reference

### MultiAgent Class

```python
class MultiAgent(Agent):
    """Simple multi-agent that coordinates other agents."""

    agents: Dict[str, Agent]  # Dictionary of managed agents
    agent: Agent | None      # Single default agent
    execution_mode: str      # How to execute: "infer", "sequential", "parallel", etc.
    infer_sequence: bool     # Auto-infer execution sequence
    branches: Dict[str, Dict[str, Any]]  # Branch configurations
```

### Factory Method

```python
@classmethod
def create(
    cls,
    agents: List[Agent],
    name: str = "multi_agent",
    execution_mode: str = "infer",
    **kwargs
) -> "MultiAgent":
    """Create a multi-agent from a list of agents."""
```

### Configuration Methods

```python
def add_branch(self, source_agent: str, condition: str, target_agents: List[str]):
    """Add a branch condition for routing between agents."""

def set_sequence(self, sequence: List[str]):
    """Manually set the execution sequence of agents."""
```

## 🎯 Usage Patterns

### 1. Content Creation Pipeline

```python
# Research → Write → Edit → Review
research_agent = SimpleAgent(name="researcher", engine=research_config)
writer_agent = SimpleAgent(name="writer", engine=writer_config)
editor_agent = ReactAgent(name="editor", engine=editor_config, tools=[grammar_tool])
reviewer_agent = SimpleAgent(name="reviewer", engine=review_config)

content_system = MultiAgent.create(
    agents=[research_agent, writer_agent, editor_agent, reviewer_agent],
    name="content_creation",
    execution_mode="sequential"
)

result = await content_system.arun("Create an article about renewable energy")
```

### 2. Analysis Pipeline

```python
# Data Processing → Analysis → Visualization
data_processor = ReactAgent(name="processor", engine=config, tools=[data_tools])
analyzer = SimpleAgent(name="analyzer", engine=analysis_config)
visualizer = SimpleAgent(name="visualizer", engine=viz_config)

analysis_system = MultiAgent.create(
    agents=[data_processor, analyzer, visualizer],
    name="data_analysis",
    execution_mode="sequential"
)

result = await analysis_system.arun("Analyze sales data for Q4 trends")
```

### 3. Quality Assurance System

```python
# Parallel quality checks
syntax_checker = ReactAgent(name="syntax", engine=config, tools=[syntax_tools])
style_checker = SimpleAgent(name="style", engine=style_config)
security_checker = ReactAgent(name="security", engine=config, tools=[security_tools])

qa_system = MultiAgent.create(
    agents=[syntax_checker, style_checker, security_checker],
    name="quality_assurance",
    execution_mode="parallel"  # Run all checks simultaneously
)

result = await qa_system.arun("Check this code for issues")
```

### 4. Conditional Routing

```python
# Route based on input type
text_processor = SimpleAgent(name="text_processor", engine=text_config)
image_processor = ReactAgent(name="image_processor", engine=config, tools=[vision_tools])
data_processor = ReactAgent(name="data_processor", engine=config, tools=[data_tools])

smart_processor = MultiAgent.create(
    agents=[text_processor, image_processor, data_processor],
    name="smart_processor",
    execution_mode="conditional"
)

# Add routing logic
smart_processor.add_branch(
    source_agent="router",
    condition="if input_type == 'image'",
    target_agents=["image_processor"]
)

result = await smart_processor.arun("Process this image file")
```

## 🔧 Configuration Options

### Agent Normalization

The system automatically normalizes agent input:

```python
# All of these work:
MultiAgent.create(agents=[agent1, agent2])           # List → Dict
MultiAgent.create(agents={"a1": agent1, "a2": agent2})  # Dict (direct)
MultiAgent.create(agent=single_agent)                # Single → Dict
```

### Execution Modes

```python
# Sequential execution (default for most cases)
MultiAgent.create(agents=[...], execution_mode="sequential")

# Parallel execution (for independent tasks)
MultiAgent.create(agents=[...], execution_mode="parallel")

# Intelligent inference (automatic routing)
MultiAgent.create(agents=[...], execution_mode="infer")

# Conditional routing (with branch logic)
MultiAgent.create(agents=[...], execution_mode="conditional")
```

### Branch Configuration

```python
system = MultiAgent.create(agents=[...], execution_mode="conditional")

# Simple condition
system.add_branch(
    source_agent="classifier",
    condition="if confidence > 0.8",
    target_agents=["high_confidence_handler"]
)

# Complex routing
system.add_branch(
    source_agent="router",
    condition="switch on input_type",
    target_agents=["text_handler", "image_handler", "data_handler"]
)
```

## 🧪 Testing

### Basic Test Pattern

```python
import pytest
from haive.agents.multi import MultiAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig

@pytest.mark.asyncio
async def test_sequential_multi_agent():
    """Test sequential multi-agent execution."""
    agent1 = SimpleAgent(name="agent1", engine=AugLLMConfig())
    agent2 = SimpleAgent(name="agent2", engine=AugLLMConfig())

    system = MultiAgent.create(
        agents=[agent1, agent2],
        name="test_system",
        execution_mode="sequential"
    )

    result = await system.arun("Test input")

    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0
```

### Integration Test

```python
@pytest.mark.asyncio
async def test_react_to_simple_flow():
    """Test ReactAgent → SimpleAgent flow."""
    from haive.agents.react import ReactAgent
    from langchain_core.tools import tool

    @tool
    def calculator(expression: str) -> str:
        """Calculate mathematical expressions."""
        return str(eval(expression))

    # ReactAgent with tools
    react_agent = ReactAgent(
        name="calculator",
        engine=AugLLMConfig(temperature=0.1),
        tools=[calculator]
    )

    # SimpleAgent for formatting
    simple_agent = SimpleAgent(
        name="formatter",
        engine=AugLLMConfig(temperature=0.3)
    )

    system = MultiAgent.create(
        agents=[react_agent, simple_agent],
        name="calc_system",
        execution_mode="sequential"
    )

    result = await system.arun("Calculate 15 * 23 and format the result nicely")

    assert "345" in result
    assert len(result) > 10  # Should be formatted nicely
```

## 🔄 Advanced Usage

### Custom Sequence Control

```python
system = MultiAgent.create(agents=[agent1, agent2, agent3])

# Override automatic sequence
system.set_sequence(["agent3", "agent1", "agent2"])

# Execution will follow the custom sequence
result = await system.arun("Input")
```

### State Access

```python
# Access agent outputs
system = MultiAgent.create(agents=[...])
result = await system.arun("Input")

# Get individual agent outputs if needed
if hasattr(system, '_last_state'):
    agent_outputs = system._last_state.agent_outputs
    writer_output = agent_outputs.get("writer")
```

### Dynamic Agent Management

```python
# Add agents after creation
system = MultiAgent.create(agents=[agent1, agent2])

# Add new agent
new_agent = SimpleAgent(name="new_agent", engine=config)
system.agents["new_agent"] = new_agent

# Update sequence
system.set_sequence(["agent1", "new_agent", "agent2"])
```

## 🚨 Best Practices

### 1. Agent Naming

```python
# ✅ Good - Descriptive names
agents = [
    SimpleAgent(name="data_collector", engine=config),
    ReactAgent(name="data_analyzer", engine=config, tools=[analysis_tools]),
    SimpleAgent(name="report_generator", engine=config)
]

# ❌ Bad - Generic names
agents = [
    SimpleAgent(name="agent1", engine=config),
    SimpleAgent(name="agent2", engine=config),
    SimpleAgent(name="agent3", engine=config)
]
```

### 2. Execution Mode Selection

```python
# ✅ Good - Choose appropriate mode
# Sequential for dependent tasks
MultiAgent.create(agents=[researcher, writer, editor], execution_mode="sequential")

# Parallel for independent tasks
MultiAgent.create(agents=[spell_check, grammar_check, style_check], execution_mode="parallel")

# Infer for automatic routing
MultiAgent.create(agents=[...], execution_mode="infer")
```

### 3. Tool Management

```python
# ✅ Good - Specific tools per agent
calculator_agent = ReactAgent(name="calc", engine=config, tools=[calculator])
search_agent = ReactAgent(name="search", engine=config, tools=[web_search])

# ❌ Bad - All tools on all agents
all_tools = [calculator, web_search, file_reader, email_sender]
agent1 = ReactAgent(name="agent1", engine=config, tools=all_tools)
agent2 = ReactAgent(name="agent2", engine=config, tools=all_tools)
```

### 4. Error Handling

```python
# ✅ Good - Graceful error handling
try:
    system = MultiAgent.create(agents=[...])
    result = await system.arun("Input")
except Exception as e:
    logger.error(f"Multi-agent execution failed: {e}")
    # Handle error appropriately
```

## 🔗 Related Documentation

- [SimpleAgent Documentation](../simple/README.md)
- [ReactAgent Documentation](../react/README.md)
- [MultiAgentState Schema](../../../core/schema/prebuilt/multi_agent_state.py)
- [BaseGraph Documentation](../../../core/graph/README.md)

## 📝 Migration Guide

### From ProperMultiAgent

```python
# Old ProperMultiAgent
from haive.agents.multi.proper_base import ProperMultiAgent

old_system = ProperMultiAgent(
    name="system",
    agents=[agent1, agent2],
    execution_mode="sequential"
)

# New clean MultiAgent
from haive.agents.multi import MultiAgent

new_system = MultiAgent.create(
    agents=[agent1, agent2],
    name="system",
    execution_mode="sequential"
)
```

### From Base MultiAgent

```python
# Old base MultiAgent
from haive.agents.multi.base import SequentialAgent

old_system = SequentialAgent(
    name="system",
    agents=[agent1, agent2]
)

# New clean MultiAgent
from haive.agents.multi import MultiAgent

new_system = MultiAgent.create(
    agents=[agent1, agent2],
    name="system",
    execution_mode="sequential"
)
```

---

**The clean MultiAgent implementation provides a simple, powerful way to coordinate multiple agents with intelligent routing and execution patterns. Use it for all multi-agent workflows in Haive.**
