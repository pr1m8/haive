# SimpleAgentV3 Architecture Memory Guide

**Document Version**: 1.0  
**Purpose**: Living memory guide for SimpleAgentV3 development and architectural research  
**Last Updated**: 2025-01-27  
**Session**: Continuation from tool routing debug session

## 🎯 Current Mission

Document architectural insights about hooks vs MultiAgent patterns, verify ReactAgentV3 status, and create incremental testing strategy to prove architectural decisions.

## ✅ SimpleAgentV3 Status: WORKING!

### 1. Tool Routing Actually Works
- **Test Result**: Successfully executed calculator tool and got correct answer (345)
- **Tool Registration**: Working correctly - `Tool routes: {'calculator': 'langchain_tool'}`
- **Validation Node**: Properly routing tool calls to tool_node
- **Tool Execution**: Calculator executed and returned "The answer is 345"
- **Status**: No fix needed - SimpleAgentV3 tools are working properly!

### 2. Validation Node Misuse
- **Problem**: Using ValidationNodeConfig as conditional edge function instead of actual node
- **Impact**: Validation logic never executes, direct routing to tool_node fails
- **Solution**: Use LangGraph's built-in `tools_condition` for routing

### 3. Architectural Confusion
- **Hooks vs MultiAgent**: Current hooks duplicate MultiAgent functionality
- **Node vs Agent boundaries**: Unclear separation of concerns
- **SimpleAgent → ReactAgent inheritance**: Fundamentally flawed

## 📋 Current TODO Status

1. ✅ **Test SimpleAgentV3 with debug=True** - Completed, tools working!
2. ✅ **SimpleAgentV3 tool routing** - No fix needed, already working
3. ✅ **ReactAgentV3 status** - Exists and working properly
4. ✅ **Document hooks vs MultiAgent** - Analysis complete
5. ✅ **Create testing strategy** - Incremental no-mocks strategy documented

## 🏗️ Architecture Discoveries

### Node vs Agent Boundaries

**Current Understanding**:
- **Nodes**: Stateless graph components, handle transformations
- **Agents**: Stateful orchestrators with LLM decision-making
- **Problem**: Agent hooks blur this boundary

**Key Insight**: Hooks should be node-level, not agent-level. The current agent hook system is essentially reimplementing MultiAgent coordination.

### Hook System Analysis

```python
# Current (BAD) - Agent-level hooks
class SimpleAgent:
    pre_agent_hooks: List[Callable]  # This is just MultiAgent!
    post_agent_hooks: List[Callable]  # This duplicates coordination
    
# Should Be - Node-level transforms
class NodeSchemaComposer:
    field_transforms: Dict[str, Transform]  # Pure data transformation
    validation_rules: List[Rule]           # Node-level validation
```

### SimpleAgent vs ReactAgent Inheritance

**Critical Flaw**: ReactAgent extends SimpleAgent but has fundamentally different execution patterns:
- SimpleAgent: Linear execution (call → response)
- ReactAgent: Iterative execution (reason → act → observe → repeat)

**Structured Output Problem**:
- In SimpleAgent: Direct output from LLM
- In ReactAgent: Final output after multiple iterations
- Current inheritance doesn't handle this difference

## 🔧 Technical Details

### Tool Registration Issue

```python
# WRONG - What we were doing
agent = SimpleAgentV3(tools=[calculator])  # Tools ignored!

# CORRECT - Tools go to engine
config = AugLLMConfig(tools=[calculator])
agent = SimpleAgentV3(engine=config)
```

### Validation Node Routing

```python
# BROKEN - Current implementation
graph.add_conditional_edges(
    "agent_node",
    validation_config,  # Using node as function!
    {"tool_node": "tool_node", END: END}
)

# SHOULD BE - Proper node usage
graph.add_node("validation", validation_config)
graph.add_conditional_edges(
    "agent_node",
    tools_condition,  # LangGraph's built-in
    {
        "tools": "validation",  # Route to validation node
        END: END
    }
)
```

### LangGraph tools_condition

**Research Needed**:
- How does `tools_condition` work?
- What's the "injected tool call" format?
- How does tool_node expect to receive calls?

## 🧪 Incremental Testing Strategy

### Phase 1: Fix SimpleAgentV3 Tool Routing
```python
# test_simple_agent_v3_tools.py
def test_tools_condition_routing():
    """Test LangGraph tools_condition properly routes."""
    # Document actual routing behavior
    
def test_tool_node_receives_correct_format():
    """Test tool_node gets proper injected tool calls."""
    # Verify message format expectations
```

### Phase 2: Document Current Architecture
```python
# test_node_vs_agent_architecture.py
def test_current_boundaries():
    """Document where node/agent boundaries are."""
    # Map current implementation
    
def test_hook_execution_order():
    """Document when hooks actually fire."""
    # Trace execution paths
```

### Phase 3: Prove Hooks = MultiAgent
```python
# test_hooks_vs_multiagent_equivalence.py  
def test_hook_pattern_equals_multiagent():
    """Show hooks are just MultiAgent in disguise."""
    # Demonstrate equivalence
    
def test_multiagent_cleaner_than_hooks():
    """Show MultiAgent is clearer pattern."""
    # Compare implementations
```

### Phase 4: Node-Level Transforms
```python
# test_node_level_transforms.py
def test_nodeschemacomposer_transforms():
    """Test proper node-level field transforms."""
    # Show correct pattern
    
def test_basegraph2_node_composition():
    """Test BaseGraph2 node capabilities."""
    # Explore node composition
```

## 📊 Decision Matrix

| Aspect | Hooks Approach | MultiAgent Approach | Node Transforms |
|--------|---------------|-------------------|----------------|
| Separation of Concerns | ❌ Blurred | ✅ Clear | ✅ Clear |
| Type Safety | ❌ Lost | ✅ Maintained | ✅ Maintained |
| Testability | ❌ Complex | ✅ Simple | ✅ Simple |
| Performance | ❌ Overhead | ✅ Efficient | ✅ Efficient |
| Clarity | ❌ Confusing | ✅ Explicit | ✅ Explicit |

## 🚀 Key Discoveries Summary

### What We Found
1. **SimpleAgentV3 and ReactAgentV3 are both WORKING** - No fixes needed!
2. **Hooks are just MultiAgent in disguise** - Same pattern, hidden complexity
3. **Clear architectural boundaries exist**:
   - Nodes: Stateless transforms (pure functions)
   - Agents: Stateful orchestrators (LLM decision making)
   - Graphs: Execution flow control
   - MultiAgent: Agent coordination

### What We Documented
1. **[Hooks vs MultiAgent Analysis](../../active/architecture/hooks_vs_multiagent_analysis.md)** - Comprehensive comparison
2. **[Incremental Testing Strategy](../../active/standards/testing/incremental_architecture_testing_strategy.md)** - No-mocks approach

### Next Actions
1. Implement the incremental test suite to prove insights
2. Create migration guide from hooks to proper patterns
3. Build examples showing clear architectural boundaries
4. Propose deprecation of agent hooks in favor of MultiAgent

## 🧠 Key Learnings

1. **Tools must be registered with engine, not agent**
2. **Validation nodes are nodes, not routing functions**
3. **Hooks at agent level violate separation of concerns**
4. **SimpleAgent → ReactAgent inheritance is broken**
5. **Node-level transforms are the correct pattern**
6. **MultiAgent is cleaner than agent hooks**

## 📝 Research Notes

### User Feedback Patterns
- "no look how soimmempl agent does it" → Check existing implementations
- "get the engine.tool_routes" → Tool routes come from engine
- "look at git history" → Previous versions had working validation
- Multiple corrections about validation node usage

### Git History Findings
- Validation node worked ~1 week ago
- Commit a835138 has working ValidationNodeConfig
- Node returns list of Send objects for routing
- Tool routes determine destination nodes

### Architectural Questions
1. Should agents have hooks at all? (No - use MultiAgent)
2. Where do field transforms belong? (Nodes via NodeSchemaComposer)
3. How to handle structured output differences? (Separate agent types)
4. Is inheritance the right pattern? (No - composition better)

## 🔗 Related Files

### Core Implementation
- `/packages/haive-agents/src/haive/agents/simple/agent_v3.py`
- `/packages/haive-core/src/haive/core/graph/node/validation_node_config.py`
- `/packages/haive-core/src/haive/core/graph/node/validation_node_config_v2.py`

### Test Files
- `/test_tool_fix.py` - Current debugging test
- Future: `test_node_vs_agent_architecture.py`
- Future: `test_hooks_vs_multiagent_equivalence.py`

### Documentation
- This memory guide
- Future: Architecture decision record
- Future: Migration guide from hooks to proper patterns

## 🚨 Warnings

1. **DO NOT** pass tools to agent constructor
2. **DO NOT** use validation nodes as routing functions
3. **DO NOT** assume SimpleAgent patterns work for ReactAgent
4. **DO NOT** add more agent-level hooks
5. **DO NOT** mock anything in tests

## 📈 Progress Tracking

- [x] Identified tool routing issue
- [x] Found validation node misuse
- [x] Discovered architectural problems
- [ ] Fixed SimpleAgentV3 tools
- [ ] Researched tools_condition
- [ ] Rebuilt ReactAgentV3
- [ ] Created architecture tests
- [ ] Documented final patterns

---

**Next Update**: After researching LangGraph tools_condition and fixing routing