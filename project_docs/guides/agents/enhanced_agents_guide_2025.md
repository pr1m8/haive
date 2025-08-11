# Enhanced Agents Guide - Haive Framework

**Date**: August 7, 2025  
**Version**: 1.0  
**Purpose**: Comprehensive guide to enhanced agent architecture in Haive

## 🚀 Quick Start

The Haive framework provides three powerful enhanced agents as of August 2025:

1. **Enhanced Base Agent** - Foundation with lifecycle management
2. **SimpleAgentV3** - Dynamic agent with hooks and recompilation
3. **ReactAgentV4** - Minimal ReAct pattern with reasoning loops

## 📋 Architecture Overview

### Hierarchy

```
Workflow (pure orchestration - no LLM)
└── Agent (Workflow + Engine)
    ├── SimpleAgent
    ├── ReactAgent  
    └── MultiAgent
```

### Key Innovation: Engine-Centric Generics

```python
from haive.agents.base.enhanced_agent import Agent
from haive.core.engine.aug_llm import AugLLMConfig

# Agents are generic on their engine type
class MyAgent(Agent[AugLLMConfig]):
    pass
```

## 🎯 SimpleAgentV3 - The Workhorse

### Basic Usage

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# Create agent with convenience fields
agent = SimpleAgentV3(
    name="assistant",
    temperature=0.7,          # Auto-syncs to engine
    max_tokens=1000,         # Auto-syncs to engine
    model_name="gpt-4",      # Auto-syncs to engine
    debug=True               # Default is True!
)

# Execute
result = await agent.arun("Hello, how can you help?")
```

### Dynamic Tool Management

```python
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

# Add tools dynamically
agent = SimpleAgentV3(
    name="math_assistant",
    tools=[calculator],
    force_tool_use=True  # Forces tool usage when available
)

# Tools trigger recompilation automatically
agent.add_tool(another_tool)  # Graph rebuilds!
```

### Hooks System

```python
# Add hooks using decorators
@agent.before_run
def log_input(context):
    print(f"Input: {context.input_data}")

@agent.after_run
def log_output(context):
    print(f"Output: {context.output_data}")

@agent.on_error
def handle_error(context):
    print(f"Error: {context.error}")

# Execute with hook monitoring
result = await agent.arun("Calculate 15 * 23")
```

### Structured Output

```python
from pydantic import BaseModel

class AnalysisResult(BaseModel):
    sentiment: str
    confidence: float
    key_points: list[str]

# Configure structured output
agent = SimpleAgentV3(
    name="analyzer",
    structured_output_model=AnalysisResult
)

# Get typed results
result: AnalysisResult = await agent.arun("Analyze this text...")
```

## 🔄 ReactAgentV4 - Reasoning Loops

### Usage

```python
from haive.agents.react.agent_v4 import ReactAgentV4

# Create ReAct agent with tools
agent = ReactAgentV4(
    name="researcher",
    tools=[web_search_tool, calculator],
    debug=True
)

# Executes reasoning loops automatically
result = await agent.arun(
    "Find the current stock price of AAPL and calculate its P/E ratio"
)
```

### Key Difference from V3

ReactAgentV4 modifies graph edges to create reasoning loops:
- `tool_node → agent_node` (continues reasoning)
- `parse_output → agent_node` (continues reasoning)

## 🛠️ Agent-as-Tool Pattern

### Convert Any Agent to a Tool

```python
# Class method - no instance needed
simple_tool = SimpleAgentV3.as_tool(
    name="research_assistant",
    description="Research and summarize topics",
    temperature=0.3
)

# Use in another agent
coordinator = ReactAgentV4(
    name="coordinator",
    tools=[simple_tool]  # Agent as tool!
)
```

### Structured Tool Output

```python
# Create tool with structured output
analyzer_tool = SimpleAgentV3.as_structured_tool(
    output_model=AnalysisResult,
    name="analyzer",
    description="Analyze text sentiment"
)
```

## 🔗 Pre/Post Processing

### Reflection Pattern

```python
from haive.agents.base.pre_post_agent_mixin import create_reflection_agent

# Create agent with reflection
reflective_agent = create_reflection_agent(
    main_agent=SimpleAgentV3(name="writer"),
    reflection_agent=SimpleAgentV3(name="critic")
)

# Executes: writer → critic → improved output
result = await reflective_agent.arun("Write a story")
```

### Graded Reflection

```python
from haive.agents.base.pre_post_agent_mixin import create_graded_reflection_agent

# Add grading before reflection
graded_agent = create_graded_reflection_agent(
    main_agent=SimpleAgentV3(name="writer"),
    grading_agent=SimpleAgentV3(name="grader"),
    reflection_agent=SimpleAgentV3(name="improver")
)

# Executes: writer → grader → improver (if needed)
result = await graded_agent.arun("Write an essay")
```

## 🎨 Meta-State Integration

### Make Any Agent Meta-Capable

```python
# Convert to meta-capable
agent = SimpleAgentV3(name="worker")
meta_state = agent.as_meta_capable()

# Execute with tracking
result = await meta_state.execute_agent({"query": "Hello"})

# Check execution summary
summary = meta_state.get_execution_summary()
print(f"Executions: {summary['execution_count']}")
```

## 📊 Built-in Hooks

### Available Hook Events

```python
# Lifecycle hooks
@agent.before_setup
@agent.after_setup
@agent.before_build_graph
@agent.after_build_graph

# Execution hooks
@agent.before_run
@agent.after_run
@agent.before_arun
@agent.after_arun

# Node hooks
@agent.before_node
@agent.after_node

# Error handling
@agent.on_error
@agent.on_retry

# Enhanced features
@agent.before_reflection
@agent.after_reflection
@agent.before_grading
@agent.after_grading
```

### Comprehensive Monitoring

```python
from haive.agents.base.hooks import comprehensive_workflow_hook

# Add comprehensive monitoring
agent.add_hook("before_run", comprehensive_workflow_hook)
agent.add_hook("after_run", comprehensive_workflow_hook)
agent.add_hook("on_error", comprehensive_workflow_hook)
```

## 🚀 Performance Tips

### 1. Debug Mode

```python
# Development (default)
agent = SimpleAgentV3(name="dev", debug=True)

# Production
agent = SimpleAgentV3(name="prod", debug=False)
```

### 2. Recompilation Control

```python
# Check if recompilation needed
if agent.needs_recompile:
    print(f"Reason: {agent.last_recompile_reason}")

# Force recompilation
agent.mark_for_recompile("Configuration changed")
```

### 3. Hook Performance

```python
# Disable hooks for performance
agent.disable_hooks()

# Re-enable when needed
agent.enable_hooks()
```

## 🔍 Debugging

### Enable Comprehensive Logging

```python
import logging

# Set logging level
logging.basicConfig(level=logging.DEBUG)

# Agent will log extensively
agent = SimpleAgentV3(name="debug_me", debug=True)
```

### Inspect Agent State

```python
# Check current configuration
print(f"Temperature: {agent.temperature}")
print(f"Tools: {agent.tools}")
print(f"Needs recompile: {agent.needs_recompile}")

# Get engine configuration
engine_config = agent.engine.model_dump()
print(f"Engine: {engine_config}")
```

### Monitor Execution

```python
# Use timing hook
from haive.agents.base.hooks import timing_hook

agent.add_hook("before_run", timing_hook)
agent.add_hook("after_run", timing_hook)

# Execute and see timing
result = await agent.arun("Complex task")
```

## 📚 Common Patterns

### 1. Multi-Stage Processing

```python
# Research → Analyze → Summarize
research_agent = ReactAgentV4(name="researcher", tools=[search])
analysis_agent = SimpleAgentV3(name="analyzer")
summary_agent = SimpleAgentV3(name="summarizer")

# Chain execution
research_result = await research_agent.arun("Find info on topic X")
analysis = await analysis_agent.arun(research_result)
summary = await summary_agent.arun(analysis)
```

### 2. Dynamic Tool Selection

```python
# Add tools based on context
base_agent = SimpleAgentV3(name="adaptive")

if user_needs_math:
    base_agent.add_tool(calculator)
if user_needs_search:
    base_agent.add_tool(web_search)
if user_needs_code:
    base_agent.add_tool(code_executor)
```

### 3. Conditional Structured Output

```python
# Different output models based on task
if task_type == "analysis":
    agent.structured_output_model = AnalysisResult
elif task_type == "summary":
    agent.structured_output_model = SummaryResult
else:
    agent.structured_output_model = None  # Free-form
```

## 🎯 Best Practices

1. **Always Use Debug in Development**
   - Default is `debug=True` - keep it!
   - Disable only in production

2. **Leverage Convenience Fields**
   - Use `temperature`, `max_tokens` etc. directly
   - They auto-sync to engine
   - Trigger proper recompilation

3. **Add Hooks for Observability**
   - Use decorators for clean code
   - Monitor without modifying logic
   - Great for debugging complex flows

4. **Compose Agents**
   - Use agent-as-tool pattern
   - Build complex from simple
   - Keep each agent focused

5. **Handle Recompilation**
   - Check `needs_recompile` flag
   - Understand what triggers it
   - Use for dynamic behavior

## 🚨 Common Pitfalls

1. **Forgetting Async**
   ```python
   # ❌ WRONG
   result = agent.run("Hello")  # Will fail!
   
   # ✅ CORRECT
   result = await agent.arun("Hello")
   ```

2. **Direct Engine Modification**
   ```python
   # ❌ WRONG
   agent.engine.temperature = 0.9  # Won't sync!
   
   # ✅ CORRECT
   agent.temperature = 0.9  # Auto-syncs
   ```

3. **Ignoring Recompilation**
   ```python
   # ❌ WRONG
   agent.add_tool(new_tool)
   # Immediate execution without checking
   
   # ✅ CORRECT
   agent.add_tool(new_tool)
   if agent.needs_recompile:
       # Handle or wait for auto-recompile
   ```

## 📅 What's New (August 2025)

- **Hooks System**: Comprehensive lifecycle monitoring
- **Dynamic Recompilation**: Hash-based change detection
- **Agent-as-Tool**: Any agent can be a tool
- **Pre/Post Processing**: Built-in reflection patterns
- **Meta-State Integration**: Full execution tracking
- **Debug-First**: Debug enabled by default
- **Convenience Fields**: Auto-sync to engine

## 🔗 Related Documentation

- [Enhanced Base Agent Implementation](../../packages/haive-agents/src/haive/agents/base/enhanced_agent.py)
- [SimpleAgentV3 Source](../../packages/haive-agents/src/haive/agents/simple/agent_v3.py)
- [ReactAgentV4 Source](../../packages/haive-agents/src/haive/agents/react/agent_v4.py)
- [Hooks System](../../packages/haive-agents/src/haive/agents/base/hooks.py)
- [CLAUDE.md](../../../CLAUDE.md) - Main project documentation

---

**Last Updated**: August 7, 2025  
**Framework Version**: haive-agents 0.2.0+