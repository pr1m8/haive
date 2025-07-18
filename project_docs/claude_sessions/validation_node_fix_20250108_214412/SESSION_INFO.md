# Session: Validation Node Fix

**Date**: 2025-01-08
**Session ID**: validation_node_fix_20250108_214412
**Goal**: Fix validation node to properly handle tool messages and dynamic routing

## Objectives

1. Add computed fields to state schema for current tool calls
2. Update validation node to handle tool messages properly
3. Ensure parser node adds ToolMessages for Pydantic models
4. Test with various tool types (Pydantic, @tool, regular functions)

## Key Context

- Validation node is used as conditional edge, can't update state
- Parser node needs to add ToolMessages for Pydantic models
- Tool node already adds ToolMessages for regular tools
- Need to handle dynamic routing without knowing all destinations at compile time

## Related Files

- @packages/haive-core/src/haive/core/graph/node/validation_node_config.py
- @packages/haive-core/src/haive/core/graph/node/parser_node_config.py
- @packages/haive-agents/src/haive/agents/simple/agent.py

## Key Decisions

- Split validation into proper node + routing edge for state updates
- Use computed fields for accessing current tool calls
- Ensure consistent ToolMessage creation across all paths
