# Enhanced MultiAgent V3 - Quick Reference Guide

**Purpose**: Developer quick reference for Enhanced MultiAgent V3
**Updated**: 2025-07-21

## 🚀 Import & Basic Setup

```python
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent
from haive.agents.simple.enhanced_agent_v3 import EnhancedSimpleAgent
from haive.core.schema.prebuilt.enhanced_multi_agent_state import EnhancedMultiAgentState
```

## ⚡ Quick Patterns

### Sequential (A → B → C)

```python
workflow = EnhancedMultiAgent(
    name="pipeline",
    agents=[agent_a, agent_b, agent_c],
    execution_mode="sequential"
)
```

### Parallel (A || B || C)

```python
panel = EnhancedMultiAgent(
    name="experts",
    agents=[expert_a, expert_b, expert_c],
    execution_mode="parallel"
)
```

### Conditional (Router → Specialist)

```python
router = EnhancedMultiAgent(
    name="router",
    agents={"classifier": classifier, "billing": billing_agent, "tech": tech_agent},
    entry_point="classifier",
    execution_mode="conditional"
)
```

### Branch (A → (B || C) → D)

```python
complex_flow = EnhancedMultiAgent(
    name="processor",
    agents=[validator, proc_1, proc_2, aggregator],
    execution_mode="branch",
    advanced_routing=True
)
```

## 🎛️ Configuration Options

```python
EnhancedMultiAgent(
    name="workflow",                    # Required
    agents=[agent1, agent2],           # Required: List or Dict

    # Execution
    execution_mode="sequential",       # infer/sequential/parallel/conditional/branch
    entry_point="agent1",             # Starting agent (conditional/branch)
    max_iterations=10,                # Max loops for conditional

    # Enhanced Features
    performance_mode=True,            # Track & optimize performance
    debug_mode=True,                  # Rich debugging
    multi_engine_mode=True,           # Multiple engines
    advanced_routing=True,            # Complex routing

    # Tuning
    adaptation_rate=0.2,              # Learning rate (0.0-1.0)
)
```

## 📊 Performance Features

```python
# Enable performance tracking
multi = EnhancedMultiAgent(
    agents={"fast": fast_agent, "accurate": slow_agent},
    performance_mode=True,
    adaptation_rate=0.3
)

# Manual performance updates
multi.update_performance("fast", success=True, duration=0.5)

# Get best performer
best = multi.get_best_agent_for_task()

# Analyze performance
analysis = multi.analyze_agent_performance()
print(f"Best agent: {analysis['overall']['best_agent']}")
```

## 🔧 Routing Configuration

```python
# Conditional routing
def route_by_content(state):
    content = str(state["messages"][-1].content).lower()
    if "billing" in content:
        return "billing_agent"
    elif "technical" in content:
        return "tech_agent"
    else:
        return "general_agent"

multi.add_conditional_routing(
    "classifier",
    route_by_content,
    {
        "billing_agent": "billing_agent",
        "tech_agent": "tech_agent",
        "general_agent": "general_agent"
    }
)

# Parallel groups
multi.add_parallel_group(["proc_1", "proc_2"], next_agent="aggregator")

# Direct edges
multi.add_edge("validator", "processor")
```

## 🏃 Execution

```python
# Compile workflow
compiled = multi.compile()

# Synchronous execution
result = compiled.invoke({
    "messages": [HumanMessage(content="Process this data")]
})

# Check results
print(f"Final result: {result['messages'][-1].content}")
print(f"Execution status: {result.get('execution_status', 'unknown')}")
```

## 🔍 Debugging & Monitoring

```python
# Enable debug mode
debug_multi = EnhancedMultiAgent(
    name="debug_workflow",
    agents=[agent1, agent2],
    debug_mode=True
)

# Display capabilities
debug_multi.display_capabilities()

# Get summary
summary = debug_multi.get_capabilities_summary()
print(f"Features: {summary['features']}")
print(f"Agent count: {summary['agent_count']}")

# Check performance
if debug_multi.performance_mode:
    perf = debug_multi.analyze_agent_performance()
    print(f"Success rate: {perf['overall']['average_success_rate']}")
```

## 🧪 Testing Patterns

```python
def test_sequential_workflow():
    """Test sequential execution pattern."""
    workflow = EnhancedMultiAgent(
        name="test_seq",
        agents=[analyzer, summarizer],
        execution_mode="sequential",
        debug_mode=True
    )

    compiled = workflow.compile()
    result = compiled.invoke({
        "messages": [HumanMessage(content="Test input")]
    })

    # Validate
    assert result is not None
    assert "messages" in result
    assert len(result["messages"]) > 0
```

## 🔄 Migration from Basic MultiAgent

```python
# Old way
from haive.agents.multi.clean import MultiAgent

old = MultiAgent(
    name="old_workflow",
    agents=[agent1, agent2]
)

# New way - drop-in replacement + new features
from haive.agents.multi.enhanced_multi_agent_v3 import EnhancedMultiAgent

new = EnhancedMultiAgent(
    name="new_workflow",
    agents=[agent1, agent2],
    # Same interface + new capabilities
    performance_mode=True,
    debug_mode=True
)
```

## 📝 State Schema Features

```python
# Access enhanced state
result = compiled.invoke(input_data)
state = result  # EnhancedMultiAgentState

# Execution tracking
print(f"Total executions: {state.total_executions}")
print(f"Current status: {state.execution_status}")

# Performance data
for agent, perf in state.agent_performance.items():
    print(f"{agent}: {perf['success_rate']} success rate")

# Debug information
if state.debug_info:
    print(f"Debug traces: {len(state.execution_trace)}")
```

## ⚠️ Common Gotchas

1. **Message Format**: Use `HumanMessage(content="...")` not `{"role": "user", "content": "..."}`
2. **Performance Mode**: Must be enabled to use performance features
3. **Entry Point**: Required for conditional and branch modes
4. **Agent Names**: Must match between agents dict and routing config

## 🎯 Best Practices

1. **Start Simple**: Begin with sequential, add complexity gradually
2. **Enable Performance**: Use `performance_mode=True` in production
3. **Debug During Development**: Use `debug_mode=True` while building
4. **Test All Patterns**: Validate each execution mode thoroughly
5. **Monitor Performance**: Check `analyze_agent_performance()` regularly

## 📚 Quick Links

- **Full Documentation**: [enhanced_multi_agent_v3_documentation.md](../memory_index/by_date/2025-07-21/enhanced_multi_agent_v3_documentation.md)
- **Test Examples**: `packages/haive-agents/tests/multi/test_enhanced_multi_agent_v3_comprehensive.py`
- **Implementation**: `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v3.py`

---

**Happy Multi-Agent Building! 🚀**
