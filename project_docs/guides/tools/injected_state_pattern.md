# InjectedState Pattern for Tool Design

**Reference**: @project_docs/to_do/injected_state.md  
**Topic**: Clean tool design using InjectedState for automatic context injection  
**Research Date**: 2025-08-08

## Core Concept

`InjectedState` is a LangGraph pattern that automatically provides tools access to graph state without requiring the LLM to pass that state as parameters.

### The Problem It Solves

**Without InjectedState**:

- LLM must somehow pass context data (user prefs, history, etc.) to tools
- Tool interfaces become cluttered with context parameters
- LLM can't access internal state it doesn't know about

**With InjectedState**:

- Framework automatically injects current state into tools
- LLM only provides the actual user input
- Tools get full context without explicit parameter passing

## Key Benefits

### 1. Simpler Tool Interfaces

```python
# Clean - LLM just provides the query
@tool
def search_with_context(
    query: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Search with automatic user context"""
    user_prefs = state.get("user_preferences", {})
    history = state.get("search_history", [])
    return enhanced_search(query, user_prefs, history)
```

### 2. Automatic Context Access

- Conversation history available without passing
- User preferences accessible automatically
- Previous tool results available for follow-ups
- State metadata (user_id, session_id) injected automatically

### 3. Cleaner LLM Prompts

- Tool schemas are focused on actual user input
- Less parameters for LLM to fill out
- More natural tool calling behavior

## Practical Implementation Patterns

### Pattern 1: Contextual Search

```python
@tool
def web_search(
    query: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Search with user context"""
    preferred_sources = state.get("user_preferences", {}).get("sources", [])
    recent_queries = state.get("search_history", [])[-5:]
    return enhanced_search(query, preferred_sources, recent_queries)
```

### Pattern 2: Memory Tools

```python
@tool
def remember_fact(
    fact: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Remember important information"""
    user_id = state.get("user_id")
    conversation_id = state.get("conversation_id")
    store_memory(user_id, conversation_id, fact)
    return f"I'll remember that."
```

### Pattern 3: Multi-Step Workflows

```python
@tool
def continue_analysis(
    next_step: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Continue current analysis with context"""
    previous_results = state.get("analysis_results", {})
    current_stage = state.get("analysis_stage", 1)
    return perform_analysis_step(next_step, previous_results, current_stage)
```

## Haive Implementation Ideas

### Planning Context Tools

```python
@tool
def refine_plan(
    refinement_request: str,
    state: Annotated[dict, InjectedState]
) -> Plan:
    """Refine current plan with execution history"""
    current_plan = state.get("current_plan")
    execution_history = state.get("execution_history", [])
    return update_plan(current_plan, refinement_request, execution_history)
```

### Tool Result Aggregation

```python
@tool
def summarize_findings(
    focus_area: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Summarize previous tool results"""
    all_results = state.get("tool_results", [])
    return create_summary(all_results, focus_area)
```

## Best Practices

1. **Focus Tool Interfaces**: Only require parameters the user would naturally provide
2. **Organize State Well**: Use clear key names and document state structure
3. **Descriptive Tool Names**: Name based on what they do, not how they work
4. **Type Your State**: Use TypedDict for better state structure

## Implementation Template

```python
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool

class AgentState(TypedDict):
    messages: list
    user_preferences: dict
    tool_results: list
    current_task: str

@tool
def execute_task(
    instructions: str,
    state: Annotated[AgentState, InjectedState]
) -> str:
    """Execute task with full context"""
    current_task = state.get("current_task")
    previous_results = state.get("tool_results", [])
    return perform_task(instructions, current_task, previous_results)
```

## Summary

InjectedState makes tools more focused and natural by:

- Automatically providing context the LLM can't access
- Reducing tool parameter complexity
- Enabling stateful tool behaviors without explicit state passing
- Making tool calls cleaner and more intuitive

## Tags

`#injected-state` `#tool-design` `#langgraph` `#context-injection` `#clean-interfaces`
