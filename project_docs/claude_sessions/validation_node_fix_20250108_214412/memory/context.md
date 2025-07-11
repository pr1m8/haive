# Current Context

## Working On

- Creating test for simple agent with validation improvements
- File: Creating new test file in haive-agents/tests/

## Key Issues Identified

1. **Validation node as conditional edge**: Can't update state to add error ToolMessages
2. **Parser node**: Not adding ToolMessages for Pydantic model results
3. **Dynamic routing**: Need to handle unknown destinations at compile time
4. **Tool call tracking**: Need to only process current message's tool calls, not all pending

## Solution Approach

1. Add computed field to state for `current_tool_calls` (last AI message only)
2. Update parser node to create ToolMessages
3. Split validation into:
   - Validation node: Adds error messages, updates state
   - Routing edge: Uses Send for dynamic routing

## Next Steps

1. Create comprehensive test file
2. Track changes with git
3. Test with multiple scenarios
