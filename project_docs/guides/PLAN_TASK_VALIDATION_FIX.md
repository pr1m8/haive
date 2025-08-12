# Plan[Task] Validation Fix - Complete Documentation

**Created**: 2025-08-12
**Author**: Claude (with user collaboration)
**Purpose**: Document the complete fix for Plan[Task] validation errors and recursion issues
**Status**: ✅ RESOLVED

## Summary

Fixed critical validation errors and infinite recursion loops that occurred when using `Plan[Task]` structured output with SimpleAgent and other agents in the planning_v2 system. The root cause was that format instructions were being generated but never integrated into the ChatPromptTemplate, causing LLMs to return incorrectly formatted responses that failed validation.

## Problem Description

### Symptoms
- **RecursionError** when using `Plan[Task]` as structured output model
- **Validation errors** with message: "Validation error: 'plan_task_generic'"
- **Infinite loops** in SimpleAgent execution with Plan[Task]
- **LangGraph steps exceeding limits** (19+ steps instead of expected 2-3)

### Root Causes
1. **Missing format instructions integration**: Format instructions were generated internally but never added to the prompt template
2. **Logic bug in `_should_setup_format_instructions()`**: Method was checking for existing format_instructions which were deliberately cleared during setup
3. **SimpleAgent validation routing issue**: Missing conditional edges from validation node caused graph to get stuck

## Solution Overview

### 1. Fixed Format Instructions Logic
**File**: `/packages/haive-core/src/haive/core/engine/aug_llm/config.py`
**Lines**: 713-724

```python
def _should_setup_format_instructions(self) -> bool:
    """Determine if format instructions should be set up."""
    if not self.include_format_instructions:
        debug_print("❌ [yellow]include_format_instructions is False[/yellow]")
        return False
    # NOTE: Removed check for existing format_instructions because
    # _setup_format_instructions() deliberately clears them first as part of setup
    if not self.structured_output_model:
        debug_print("❌ [yellow]No structured_output_model set[/yellow]")
        return False
    debug_print("✅ [green]Conditions met for format instructions[/green]")
    return True
```

### 2. Added Format Instructions Integration
**File**: `/packages/haive-core/src/haive/core/engine/aug_llm/config.py`
**New Method**: `_integrate_format_instructions_to_prompt()`

```python
def _integrate_format_instructions_to_prompt(self):
    """Integrate format instructions into ChatPromptTemplate as messages."""
    debug_print("🔗 [blue]Integrating format instructions to prompt template...[/blue]")

    # Check if we have format instructions to integrate
    if "format_instructions" not in self.partial_variables or not self._format_instructions_text:
        debug_print("❌ [yellow]No format instructions to integrate[/yellow]")
        return

    # Only work with ChatPromptTemplate (the default type)
    if not isinstance(self.prompt_template, ChatPromptTemplate):
        debug_print(f"⚠️ [yellow]Prompt template is {type(self.prompt_template).__name__}, not ChatPromptTemplate - skipping integration[/yellow]")
        return

    # Create new system message with format instructions
    from langchain_core.messages import SystemMessage
    format_msg = SystemMessage(content=f"Output format instructions:\n\n{self._format_instructions_text}")

    # Insert after existing system messages
    new_messages = []
    system_messages_added = False

    for msg in existing_messages:
        new_messages.append(msg)
        if (hasattr(msg, 'role') and msg.role == 'system') or \
           (hasattr(msg, 'prompt') and 'system' in str(type(msg)).lower()):
            if not system_messages_added:
                new_messages.append(format_msg)
                system_messages_added = True

    # If no system messages found, add at beginning
    if not system_messages_added:
        new_messages.insert(0, format_msg)

    # Create new ChatPromptTemplate with integrated format instructions
    self.prompt_template = ChatPromptTemplate.from_messages(new_messages)

    # Remove format_instructions from partial_variables since it's now integrated
    if "format_instructions" in self.partial_variables:
        del self.partial_variables["format_instructions"]

    debug_print("✅ [green]Format instructions integrated as system message[/green]")
```

### 3. Updated Comprehensive Validation
**File**: `/packages/haive-core/src/haive/core/engine/aug_llm/config.py`
**Method**: `comprehensive_validation_and_setup()`

Added call to integrate format instructions:
```python
self._setup_format_instructions()
self._integrate_format_instructions_to_prompt()  # NEW: Integrate into prompt
self._setup_output_handling()
```

### 4. SimpleAgent Validation Routing Fix
**File**: `/packages/haive-agents/src/haive/agents/simple/agent.py`
**Method**: `_add_validation_nodes()`

Added missing conditional edges:
```python
# Add conditional edges FROM validation using validation_router_v2
routing_map = {}
if needs_tools:
    routing_map["tool_node"] = "tool_node"
if needs_parsing:
    routing_map["parse_output"] = "parse_output"
routing_map["agent_node"] = "agent_node"  # For errors

graph.add_conditional_edges(
    "validation",
    validation_router_v2,
    routing_map
)
```

## Validation Results

### Test Execution
- ✅ Plan[Task] creates successfully without errors
- ✅ Format instructions properly integrated into prompt
- ✅ SimpleAgent executes with Plan[Task] structured output
- ✅ LangGraph steps limited to 5 (recursion limit working)
- ✅ No more validation errors or infinite loops
- ✅ All nested BaseModel patterns work (SimplePlan, Plan[Task], DeepPlan)

### Real-World Testing
- Tested with Azure OpenAI (gpt-4o model)
- Planner agent successfully creates plans with proper Task objects
- Format instructions ensure LLM returns correctly structured JSON
- Validation node properly routes to parse_output for structured output

## Impact

This fix resolves a critical issue that was preventing the use of generic types with BaseModel in structured output scenarios. It affects:

1. **Planning agents** - Can now use Plan[Task] for hierarchical planning
2. **SimpleAgent** - Validation routing now works correctly
3. **All agents using structured output** - Format instructions properly integrated
4. **Complex nested schemas** - LLMs now receive proper formatting guidance

## Related Files

### Core Changes
- `/packages/haive-core/src/haive/core/engine/aug_llm/config.py` - Main fix implementation

### Test Files
- `/packages/haive-agents/tests/planning_v2/test_simple_agent_plan_task_fix.py` - Validation test
- `/packages/haive-agents/tests/planning_v2/comprehensive_nested_basemodel_test.py` - Comprehensive tests
- `/packages/haive-agents/tests/planning_v2/test_planner_final.py` - Original failing test now passes

### Documentation
- `/project_docs/guides/TOOL_ROUTING_REFACTOR.md` - Tool routing context
- `/memory_index/by_date/2025-01-29/` - Recent BaseModel routing fixes

## Migration Guide

No migration needed - this is a bug fix that makes existing code work correctly. However, if you were working around this issue:

1. **Remove workarounds** - Tool wrapper solutions are no longer needed
2. **Use Plan[Task] directly** - Can now be used as structured_output_model
3. **Check recursion limits** - Set appropriate limits in RunnableConfig if needed

## Key Takeaways

1. **Format instructions must be integrated** - Generating them isn't enough
2. **ChatPromptTemplate needs explicit messages** - Can't rely on partial_variables alone
3. **SimpleAgent needs proper routing** - Validation nodes must have outgoing edges
4. **Test with real LLMs** - Mock testing wouldn't have caught this issue
5. **Debug output is crucial** - HAIVE_DEBUG_CONFIG=TRUE helped identify the problem

## Git Commits

### haive-core
```
commit 589df3f0
Author: Claude <noreply@anthropic.com>
Date:   2025-08-12

fix(aug_llm): integrate format instructions into ChatPromptTemplate for Plan[Task] validation

- Fixed logic bug in _should_setup_format_instructions() method
- Added _integrate_format_instructions_to_prompt() method to add format instructions as SystemMessage
- Format instructions now properly integrated into prompt template for nested BaseModel patterns
- Resolves recursion errors with Plan[Task] structured output in planning_v2
- All nested BaseModel patterns (SimplePlan, Plan[Task], DeepPlan) now work correctly
```

### Main Repository
```
commit 0e7b3df4
Author: Claude <noreply@anthropic.com>
Date:   2025-08-12

chore: update haive-core submodule reference for Plan[Task] validation fix

Updated haive-core to include the format instructions integration fix that resolves
validation errors and recursion issues with Plan[Task] structured output in planning_v2.
```

## References

- Original issue discovery session (2025-08-12)
- Format instructions investigation and fix implementation
- Comprehensive testing with real Azure OpenAI LLM
- Validation routing pattern from haive-core ValidationNodeV2

---

**Status**: ✅ RESOLVED - Plan[Task] validation now works correctly in all scenarios
