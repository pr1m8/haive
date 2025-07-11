# Quick Reference: Dynamic Tool Routing

## Key Files & What They Do

### 1. `real_dynamic_agent_system.py`

**The main working implementation**

- Uses real SimpleAgent and ReactAgent
- Demonstrates dynamic tool addition
- Shows recompilation detection
- **Run**: `poetry run python project_docs/dynamic_tool_routing_system/real_dynamic_agent_system.py`

### 2. `DYNAMIC_TOOL_ROUTING_ARCHITECTURE.md`

**Complete architecture documentation**

- Full system design
- Implementation patterns
- Code examples
- Integration roadmap

### 3. `META_AGENT_INTEGRATION_GUIDE.md`

**Specific guide for meta-agent implementation**

- Key insights from testing
- Recompilation strategies
- Meta-agent specific patterns

## Core Patterns

### Dynamic Routing (No Literals)

```python
def router(state) -> Send:
    return Send("agent_executor", {
        "agent_name": "dynamic_agent",
        "state": state
    })
```

### Recompilation Detection

```python
def needs_recompilation(self) -> bool:
    current_hash = self._compute_tool_route_hash()
    return current_hash != self._tool_route_hash
```

### Tool Addition

```python
agent.add_tool_dynamically(new_tool, "tool_node")
if agent.needs_recompilation():
    agent.recompile_if_needed()
```

## Test Results Summary

✅ **Dynamic routing works** - no compile-time literals needed
✅ **Tool addition works** - tools successfully added to agents  
✅ **Recompilation detection works** - hash-based change detection
✅ **Multi-agent coordination works** - state-driven routing

⚠️ **Issue identified**: SimpleAgent uses placeholder validation node instead of ValidationNodeConfigV2

## For Meta-Agent Implementation

1. **Use Send/Command** for dynamic routing
2. **Implement recompilation detection** with hash-based system
3. **Create tool route registry** for centralized management
4. **Wait for V2 validation node** for proper tool message handling

## Quick Commands

```bash
# Test the system
poetry run python project_docs/dynamic_tool_routing_system/real_dynamic_agent_system.py

# Debug tool addition
poetry run python project_docs/dynamic_tool_routing_system/debug_tool_addition.py

# Debug validation node
poetry run python project_docs/dynamic_tool_routing_system/debug_validation_node_v2.py
```
