# Agent Output Field Update Strategy

**Date**: 2025-01-18
**Purpose**: Define how agents update the right fields in MultiAgentState

## 🎯 Core Principles

1. **Simple agents without structured output** → Output `messages` field
2. **Agents with structured output models** → Output their schema fields (NO messages)
3. **Agent nodes pass full state** → Agents decide what to extract
4. **Command pattern updates** → Clean field updates based on output

## 📋 Test Coverage Created

### 1. MultiAgentState Schema Tests

**File**: `/packages/haive-core/tests/schema/prebuilt/multi/test_multi_agent_state_schema.py`

Tests:

- Basic field structure and defaults
- Message field annotations
- Agent output field types (dict[str, Any])
- Agent state isolation
- Mixed outputs (messages vs structured)

### 2. Agent Node I/O Pattern Tests

**File**: `/packages/haive-core/tests/node/test_agent_node_io_patterns.py`

Tests:

- Agent receives full state (not projected)
- Simple agents output messages by default
- Structured agents output NO messages
- Command update patterns
- Output schema field mapping

## 🔧 Implementation Strategy

### Default Behavior (Simple Agents)

```python
# Agent without structured_output_model
class SimpleAgent:
    output_schema = None  # or messages-based schema

    def invoke(self, state, config):
        return {
            "messages": [AIMessage(content="Response")]
        }

# In MultiAgentState.agent_outputs:
{
    "simple_agent": {
        "messages": [...]  # Has messages field
    }
}
```

### Structured Output (No Messages)

```python
# Agent with structured_output_model
class StructuredAgent:
    output_schema = SelectedModules  # Pydantic model

    def invoke(self, state, config):
        return SelectedModules(
            selected_modules=["reasoning", "analysis"],
            rationale="Best for task"
        )

# In MultiAgentState.agent_outputs:
{
    "select_modules": {
        "selected_modules": [...],  # Schema fields
        "rationale": "..."          # NO messages field!
    }
}
```

## 🎯 Key Decisions

1. **Message Handling**:
   - Default: Agents output messages
   - Structured: Agents output their schema (no messages)
   - Global messages: Separate in MultiAgentState.messages

2. **Field Updates**:
   - Each agent updates `agent_outputs[agent_name]`
   - Output structure matches agent's output_schema
   - No cross-contamination between agents

3. **Preventing Messages**:
   - If agent has `structured_output_model` → No messages in output
   - If agent has specific `output_schema` → Use those fields only
   - Filter out fields not in schema (TODO: Implement)

## 📊 Examples from Self-Discover

```python
# Each agent has specific output schema
agent_outputs = {
    "select_modules": {
        "selected_modules": ["reasoning", "planning"],
        # NO messages field
    },
    "adapt_modules": {
        "adapted_modules": [{"module": "...", "adaptation": "..."}],
        # NO messages field
    },
    "create_structure": {
        "reasoning_structure": {...},
        "steps": [...],
        # NO messages field
    },
    "final_reasoning": {
        "answer": "...",
        "reasoning_steps": {...},
        # NO messages field
    }
}
```

## 🚀 Next Steps

1. **Update agent_node_v3.py** to use Command pattern properly
2. **Implement output filtering** based on agent.output_schema
3. **Test with real agents** (SimpleAgent vs Self-Discover agents)
4. **Document the pattern** for other developers

---

**Remember**: The goal is clean, typed outputs where each agent updates exactly the fields it declares in its output schema!
