# Haive-Agents Pyright Issues

**Package**: haive-agents
**Total Errors**: 4828
**Total Warnings**: 434

## Critical Issues to Fix

### 1. Base Agent Issues (haive/agents/agent.py)

- **Error**: Expected mapping for dictionary unpack operator (line 150, 156)
- **Error**: Argument type mismatch in format_descriptions function (line 151)
- **Error**: "add_node" is not a known attribute of "None" (line 173, 177)
- **Error**: "add_edge" is not a known attribute of "None" (line 174)

**Fix**: Add proper null checks for graph operations and fix dictionary unpack issues.

### 2. Memory Models Issues

Multiple type errors in memory models that were recently restructured.

### 3. Import Path Issues

Many import errors from recent refactoring.

## Status

- [x] Fix base agent.py graph issues (Added null checks and typed lambda functions)
- [x] Fix base agent.py state dict access issues (All 12 errors fixed - 0 errors remaining)
- [ ] Fix memory models type issues
- [ ] Address remaining 4800+ type errors
