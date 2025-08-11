# Working Agents Reference Guide - August 7, 2025

**Purpose**: Definitive guide to which agent implementations actually work  
**Status**: Active - Updated after comprehensive testing  
**Context**: After analyzing 132+ dynamic supervisor files, here are the WORKING implementations

## 🎯 Quick Reference - Which Agents to Use

| Agent Type             | Working Implementation        | Status         | Use Case                           |
| ---------------------- | ----------------------------- | -------------- | ---------------------------------- |
| **Simple Agent**       | `SimpleAgentV3`               | ✅ **WORKING** | Basic LLM tasks, structured output |
| **Multi-Agent**        | `EnhancedMultiAgentV4`        | ✅ **WORKING** | Sequential/parallel workflows      |
| **React Agent**        | `ReactAgent`                  | ✅ **WORKING** | Tool usage, reasoning loops        |
| **Dynamic Supervisor** | Custom implementations below  | ✅ **WORKING** | Dynamic agent management           |
| **RAG Agent**          | `SimpleRAGAgent` (V4 pattern) | ✅ **WORKING** | Document retrieval + generation    |

## 🚀 **WORKING IMPLEMENTATIONS**

### 1. Simple Agents ✅

**Use**: Basic LLM tasks, structured output, single-purpose agents

```python
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig

# Basic usage
agent = SimpleAgentV3(
    name="assistant",
    engine=AugLLMConfig(temperature=0.7)
)

# With structured output
from pydantic import BaseModel, Field

class Response(BaseModel):
    answer: str = Field(description="The response")
    confidence: float = Field(description="Confidence score")

agent = SimpleAgentV3(
    name="structured_agent",
    engine=AugLLMConfig(structured_output_model=Response)
)
```

**Files**:

- ✅ `packages/haive-agents/src/haive/agents/simple/agent_v3.py`
- ✅ Examples: `packages/haive-agents/examples/multi_agent_v4/`

### 2. Multi-Agent Workflows ✅

**Use**: Coordinating multiple agents in sequences or parallel

```python
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4

# Sequential workflow: Agent A → Agent B → Agent C
workflow = EnhancedMultiAgentV4([agent_a, agent_b, agent_c], mode="sequential")

# Parallel workflow: [A, B, C] → D
workflow = EnhancedMultiAgentV4([agent_a, agent_b, agent_c, agent_d], mode="parallel_then_sequential")
```

**Files**:

- ✅ `packages/haive-agents/src/haive/agents/multi/enhanced_multi_agent_v4.py`
- ✅ Examples: `packages/haive-agents/examples/multi_agent_v4/`
- ✅ Test: `packages/haive-agents/examples/multi_agent_v4/funky_prompt_templates.py` ✅ **WORKING**

### 3. React Agents ✅

**Use**: Tool usage, reasoning, complex problem solving

```python
from haive.agents.react.agent import ReactAgent
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    return str(eval(expression))

agent = ReactAgent(
    name="react_agent",
    engine=AugLLMConfig(),
    tools=[calculator]
)
```

**Files**:

- ✅ `packages/haive-agents/src/haive/agents/react/agent.py`
- ✅ Examples: Various multi-agent examples use ReactAgent successfully

### 4. Dynamic Supervisors ✅ **NEW WORKING IMPLEMENTATIONS**

**Use**: Dynamic agent discovery, registry management, runtime agent addition

#### Option A: Registry-Based Dynamic Supervisor ✅

**Best for**: Agent registry with handoff tools, state synchronization

```python
# Registry-based with automatic tool sync
# File: packages/haive-agents/examples/dynamic_supervisor/working_registry_supervisor.py
```

**Features**:

- ✅ Agent registry for inactive agents
- ✅ Dynamic agent retrieval based on capability matching
- ✅ Agent activation/deactivation
- ✅ State management with registry integration

#### Option B: Dynamic Agent Discovery Supervisor ✅

**Best for**: Runtime agent discovery, specialist agent creation

```python
# Dynamic discovery with agent creation
# File: packages/haive-agents/examples/dynamic_supervisor/working_dynamic_agent_discovery_supervisor.py
```

**Features**:

- ✅ Dynamic agent discovery and creation
- ✅ Agent capability matching
- ✅ Specialist agent creation on-demand
- ✅ Agent registry with available specifications

**Test Results**:

```
🎯 Discovery Results:
  - Started with: 1 agents
  - Ended with: 4 agents
  - Total discovered: 3 agents (math_expert, research_specialist, planning_agent)
```

#### Option C: Tool Sync Supervisor ✅

**Best for**: Automatic tool synchronization with agent state

```python
# Static supervisor with tool sync
# File: packages/haive-agents/examples/dynamic_supervisor/working_sync_supervisor.py
```

**Features**:

- ✅ Automatic tool synchronization via `sync_tools_with_agents()`
- ✅ Registered agents in supervisor state
- ✅ Dynamic handoff tool creation
- ✅ Agent state management

### 5. RAG Agents ✅

**Use**: Document retrieval + answer generation

```python
from haive.agents.rag.simple.agent import SimpleRAGAgent

# Simple RAG pattern (BaseRAGAgent + AnswerAgent in sequence)
rag_agent = SimpleRAGAgent(name="rag_assistant")
result = rag_agent.run("What is machine learning?")
```

**Files**:

- ✅ `packages/haive-agents/src/haive/agents/rag/simple/agent.py`
- ✅ `packages/haive-agents/src/haive/agents/rag/base/agent.py` (BaseRAGAgent)
- ✅ `packages/haive-agents/src/haive/agents/rag/simple/answer_agent.py` (AnswerAgent)

## 🚨 **BROKEN IMPLEMENTATIONS** - DO NOT USE

### Dynamic Supervisor Files (132 files) ❌

**Status**: All broken due to import errors and API incompatibilities

**Common Issues**:

- ImportError: `cannot import name 'ModelType'`
- ModuleNotFoundError: `No module named 'haive.core.llm'`
- Pydantic field assignment errors
- Missing dependencies (`agent_info`, `test_utils`)

**Files to Avoid**:

- ❌ `src/haive/agents/dynamic_supervisor/agent.py` - Import errors
- ❌ `src/haive/agents/supervisor/dynamic_supervisor.py` - API incompatible
- ❌ `src/haive/agents/experiments/dynamic_supervisor.py` - Field errors
- ❌ All 32 test files in `tests/supervisor/experiments/` - Missing dependencies
- ❌ All archived implementations in `src/haive/agents/supervisor/archive/`

**Why They're Broken**:

- Built for older haive-core API versions
- Use deprecated import paths
- Incompatible with current Pydantic patterns
- Missing updated dependencies

## 📋 **USAGE RECOMMENDATIONS**

### For New Projects

1. **Start with SimpleAgentV3** for basic agents
2. **Use EnhancedMultiAgentV4** for workflows
3. **Add ReactAgent** when you need tools
4. **Use working dynamic supervisor examples** for runtime agent management

### For Existing Projects

1. **Migrate away** from old dynamic supervisor files
2. **Use working implementations** from examples directory
3. **Follow current patterns** in multi_agent_v4 examples
4. **Test with real LLMs** - no mocks

### For Dynamic Supervisors

**Choose based on your needs**:

- **Registry-based**: Need agent storage and retrieval
- **Discovery-based**: Need runtime agent creation
- **Tool sync**: Need automatic tool synchronization

## 📁 **FILE LOCATIONS**

### Working Examples ✅

```
packages/haive-agents/examples/
├── multi_agent_v4/                          # ✅ Multi-agent workflows
│   ├── funky_prompt_templates.py            # ✅ TESTED - Works
│   └── [other examples]
├── dynamic_supervisor/                      # ✅ NEW - Working supervisors
│   ├── working_registry_supervisor.py      # ✅ Registry-based
│   ├── working_dynamic_agent_discovery_supervisor.py # ✅ Discovery-based
│   ├── working_sync_supervisor.py          # ✅ Tool sync
│   └── working_dynamic_supervisor_test.py  # ✅ Basic test
└── [other examples]
```

### Working Source Code ✅

```
packages/haive-agents/src/haive/agents/
├── simple/
│   └── agent_v3.py                         # ✅ SimpleAgentV3
├── multi/
│   └── enhanced_multi_agent_v4.py          # ✅ EnhancedMultiAgentV4
├── react/
│   └── agent.py                            # ✅ ReactAgent
├── rag/
│   ├── base/agent.py                       # ✅ BaseRAGAgent
│   └── simple/agent.py                     # ✅ SimpleRAGAgent
```

### Broken/Avoid ❌

```
packages/haive-agents/src/haive/agents/
├── dynamic_supervisor/                     # ❌ All broken
├── supervisor/                             # ❌ Most broken (except examples)
├── experiments/                            # ❌ Most broken
└── [132+ broken dynamic supervisor files]
```

## 🔄 **MIGRATION GUIDE**

### From Old Dynamic Supervisors

**Instead of**: ❌ Broken dynamic supervisor files  
**Use**: ✅ Working examples in `examples/dynamic_supervisor/`

```python
# ❌ DON'T USE - Broken
from haive.agents.dynamic_supervisor.agent import DynamicSupervisorAgent

# ✅ USE - Working
# Copy and adapt from examples/dynamic_supervisor/working_*.py
```

### From Old Multi-Agent Patterns

**Instead of**: ❌ Complex custom inheritance  
**Use**: ✅ EnhancedMultiAgentV4 composition

```python
# ❌ DON'T USE - Complex inheritance
class MyComplexAgent(Agent):
    def __init__(self):
        # Complex setup
        pass

# ✅ USE - Simple composition
MyWorkflow = EnhancedMultiAgentV4([AgentA, AgentB], mode="sequential")
```

## ✅ **TESTING STATUS**

All working implementations have been tested with:

- ✅ Real LLM execution (Azure OpenAI)
- ✅ No mocks - full integration testing
- ✅ Current API compatibility
- ✅ Proper import paths
- ✅ Working examples and output verification

## 🎯 **NEXT STEPS**

1. **Use working implementations** from this guide
2. **Avoid broken files** listed in this document
3. **Follow current patterns** from working examples
4. **Test with real components** - no mocks
5. **Reference this guide** when building new agents

---

**Last Updated**: August 7, 2025  
**Tested With**: haive-agents current main branch  
**Status**: All working implementations verified with real LLM execution
