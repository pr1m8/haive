# InjectedState Pattern: A Convenient Tool Design Pattern

**Created**: 2025-01-30
**Status**: Research & Implementation Guide
**Purpose**: Understanding how to use InjectedState for cleaner tool design in LangGraph

## Overview

The `InjectedState` pattern in LangGraph is a convenient way to give tools access to state without requiring the LLM to provide that state as an input. It's a clean design pattern that simplifies tool interfaces.

## What InjectedState Actually Does

It's simple and useful:

- Tools can access graph state without the LLM having to pass it
- Reduces the parameters the LLM needs to provide
- Makes tool calls cleaner and more focused
- The framework handles injecting the state automatically

## Why It's Cool

### Without InjectedState (Messy)

```python
# LLM has to somehow pass state - but how?
@tool
def search_with_context(query: str, user_preferences: dict, search_history: list) -> str:
    """Search with user context"""
    # Where does the LLM get user_preferences and search_history from?
    # It can't - this doesn't work well
```

### With InjectedState (Clean)

```python
@tool
def search_with_context(
    query: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Search with user context"""
    # State is automatically injected by the framework
    user_prefs = state.get("user_preferences", {})
    history = state.get("search_history", [])
    # Tool just needs the query from the LLM
```

## Benefits

1. **Simpler Tool Interfaces**
   - LLM only provides the actual user input (query, topic, etc.)
   - Framework handles passing the context

2. **Automatic Context**
   - Tools always have access to conversation history
   - User preferences available without explicit passing
   - Previous results accessible for follow-ups

3. **Cleaner Prompts**
   - Tool schemas are simpler
   - Less parameters for the LLM to fill out
   - More focused on the actual task

## Practical Examples

### Example 1: Personalized Search

```python
@tool
def web_search(
    query: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Search the web"""
    # Access user's preferred sources
    preferred_sources = state.get("user_preferences", {}).get("sources", [])

    # Use previous searches for context
    recent_queries = state.get("search_history", [])[-5:]

    # Perform search with automatic context
    return enhanced_search(query, preferred_sources, recent_queries)
```

### Example 2: Contextual Memory

```python
@tool
def remember_fact(
    fact: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Remember an important fact"""
    # Automatically get user context
    user_id = state.get("user_id")
    conversation_id = state.get("conversation_id")

    # Store with full context without LLM having to track IDs
    store_memory(user_id, conversation_id, fact)
    return f"I'll remember that."
```

### Example 3: Multi-Step Workflows

```python
@tool
def continue_analysis(
    next_step: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Continue the current analysis"""
    # Access previous analysis results automatically
    previous_results = state.get("analysis_results", {})
    current_stage = state.get("analysis_stage", 1)

    # LLM just says what to do next, not track all the context
    return perform_analysis_step(next_step, previous_results, current_stage)
```

## Implementation in Haive

For our agents, we could use this pattern for:

### 1. Planning Context

```python
@tool
def refine_plan(
    refinement_request: str,
    state: Annotated[dict, InjectedState]
) -> Plan:
    """Refine the current plan based on feedback"""
    current_plan = state.get("current_plan")
    execution_history = state.get("execution_history", [])

    # Agent just specifies what to refine, not pass entire plan
    return update_plan(current_plan, refinement_request, execution_history)
```

### 2. Tool Result Aggregation

```python
@tool
def summarize_findings(
    focus_area: str,
    state: Annotated[dict, InjectedState]
) -> str:
    """Summarize findings from previous tool calls"""
    all_results = state.get("tool_results", [])

    # LLM just specifies what to focus on
    return create_summary(all_results, focus_area)
```

## Best Practices

1. **Keep tool interfaces focused**
   - Only require parameters the user would naturally provide
   - Let state handle context, history, and metadata

2. **Use descriptive names**
   - Tool names should describe what they do, not how

3. **State organization**
   - Keep state well-structured
   - Use clear key names
   - Document what's available in state

## How to Implement

```python
from typing import Annotated
from langgraph.prebuilt import InjectedState
from langchain_core.tools import tool

# Define your state structure
class AgentState(TypedDict):
    messages: list
    user_preferences: dict
    tool_results: list
    current_task: str

# Create tools that use state
@tool
def execute_task(
    instructions: str,
    state: Annotated[AgentState, InjectedState]
) -> str:
    """Execute task with full context"""
    # Access anything from state
    current_task = state.get("current_task")
    previous_results = state.get("tool_results", [])

    # Tool logic here
    return result
```

## Summary

InjectedState is a convenient pattern that:

- Simplifies tool interfaces
- Automatically provides context
- Reduces what the LLM needs to track
- Makes tools more focused and easier to use

It's not about hiding state or preventing pollution - it's about making tools work better by not requiring the LLM to manually pass around context that the framework can handle automatically.
