# Agent Types Issues Analysis

## Overview
This document analyzes the issues found in the different agent types in the Haive codebase, focusing on broken imports, inconsistent patterns, duplicate code, and missing functionality.

## 1. Chain Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/chain_agent.py`
- `/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py`

### Problems Found
1. **Broken Imports**: The main `chain_agent.py` has incorrect imports:
   ```python
   from agents.simple.agent import SimpleAgent, SimpleAgentConfig, SimpleAgentStateSchema
   ```
   - Should be: `from haive.agents.simple.agent import SimpleAgent`
   - `SimpleAgentConfig` and `SimpleAgentStateSchema` don't exist

2. **Duplicate Implementations**: Two different chain agent implementations exist:
   - Old: `chain_agent.py` - Complex, broken imports, uses non-existent classes
   - New: `chain/chain_agent_simple.py` - Simpler, cleaner implementation

3. **Schema Issues**: The old implementation tries to extend non-existent schemas

### Recommendation
- Remove the old `chain_agent.py` 
- Use the newer `chain/chain_agent_simple.py` as the primary implementation
- Fix any references to the old implementation

## 2. RAG Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/rag/` (multiple subdirectories)

### Problems Found
1. **Over-proliferation**: Too many RAG variants without clear organization:
   - `base/agent.py` - BaseRAGAgent
   - `simple/agent.py` - SimpleRAGAgent
   - `corrective/agent.py` - CorrectiveRAGAgent
   - `hyde/agent.py` - HydeRAGAgent
   - And many more...

2. **Inconsistent Base Classes**: 
   - Some inherit from `Agent`
   - Others inherit from `SequentialAgent` 
   - Some use mixins like `RetrieverMixin`

3. **Missing Core Functionality**: The base `Agent` class doesn't have consistent RAG support

### Recommendation
- Create a clear hierarchy: BaseRAGAgent → specialized variants
- Standardize the interface for all RAG agents
- Document which variant to use when

## 3. ReAct Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/react/agent.py`
- `/packages/haive-agents/src/haive/agents/react_class/` (multiple versions)

### Problems Found
1. **Multiple Implementations**: 
   - `react/agent.py` - Simple, inherits from SimpleAgent
   - `react_class/react/agent.py`
   - `react_class/react_v2/agent.py`
   - `react_class/react_v3/agent.py`
   - `react_class/react_agent/agent.py`
   - `react_class/react_agent2/agent.py`

2. **Unclear Versioning**: No clear indication of which version to use
3. **Duplicate Code**: Similar functionality implemented multiple times

### Recommendation
- Consolidate to one primary ReAct implementation
- Archive or remove experimental versions
- Clear documentation on the canonical implementation

## 4. Simple Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/simple/agent.py`

### Problems Found
1. **Schema Modification Complexity**: The agent modifies engine schemas in complex ways
2. **Node Detection Logic**: Complex conditional logic for determining which nodes to add
3. **Missing Base Features**: Doesn't use some of the base Agent class features effectively

### Recommendation
- Simplify the schema modification approach
- Extract node detection to separate methods
- Better leverage base class functionality

## 5. Generic Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/base/generic_agent.py`

### Problems Found
1. **Over-engineering**: Complex generic type system that's rarely used
2. **Auto-configuration**: The `__init_subclass__` pattern adds complexity
3. **Adapter System**: The adapter creation is complex and untested

### Recommendation
- Simplify or remove if not actively used
- Focus on concrete implementations rather than generic abstractions

## 6. Base Agent Issues

### Location
- `/packages/haive-agents/src/haive/agents/base/agent.py`

### Problems Found
1. **Overly Complex**: 1749 lines with too many responsibilities
2. **Schema Generation**: Complex schema generation logic that's hard to follow
3. **Mixin Overload**: Too many mixins (ExecutionMixin, StateMixin, SerializationMixin)
4. **Persistence Logic**: Complex persistence setup that could be simplified

### Recommendation
- Split into smaller, focused components
- Simplify schema generation
- Extract persistence to a separate concern

## Common Issues Across All Agent Types

### 1. Import Path Inconsistencies
- Some use absolute imports: `from haive.agents.simple.agent import`
- Others use relative imports: `from agents.simple.agent import`

### 2. Schema Management
- Each agent type handles schemas differently
- No consistent pattern for schema inheritance
- Complex schema modification in various places

### 3. Engine Management
- Inconsistent handling of single vs multiple engines
- Complex engine registration and discovery
- Duplicate engine management code

### 4. Graph Building
- Each agent implements `build_graph()` differently
- No shared utilities for common patterns
- Complex node configuration

### 5. Missing Documentation
- No clear guide on which agent to use when
- Missing examples for many agent types
- Unclear migration paths between agent types

## Prioritized Fix List

1. **Critical - Broken Imports**
   - Fix `chain_agent.py` imports
   - Remove references to non-existent classes

2. **High - Consolidate Implementations**
   - Choose one chain agent implementation
   - Choose one ReAct implementation
   - Organize RAG agents hierarchically

3. **Medium - Standardize Patterns**
   - Create consistent schema handling
   - Standardize engine management
   - Create shared graph building utilities

4. **Low - Documentation**
   - Document each agent type's purpose
   - Create migration guides
   - Add comprehensive examples

## Specific Broken Implementations

### 1. ChainAgent Import Error
File: `/packages/haive-agents/src/haive/agents/chain_agent.py`
```python
# BROKEN - Line 7
from agents.simple.agent import SimpleAgent, SimpleAgentConfig, SimpleAgentStateSchema
# Should be:
from haive.agents.simple.agent import SimpleAgent
# SimpleAgentConfig and SimpleAgentStateSchema don't exist
```

### 2. Test Workarounds
File: `/packages/haive-agents/tests/test_direct_rag_import.py`
- Comment indicates "without going through broken __init__.py"
- Tests have to bypass normal imports due to broken initialization

### 3. Missing Classes Referenced
- `SimpleAgentConfig` - Referenced but doesn't exist
- `SimpleAgentStateSchema` - Referenced but doesn't exist
- Various `__init__.py` files appear to have import issues

## Recommended Architecture

```
Agent (base)
├── SimpleAgent (basic LLM + tools)
├── ChainAgent (sequential execution)
├── ReactAgent (reasoning + acting loops)
├── BaseRAGAgent (retrieval augmented generation)
│   ├── SimpleRAGAgent
│   ├── CorrectiveRAGAgent
│   └── HydeRAGAgent
└── MultiAgent (agent composition)
```

Each agent should:
- Have a clear, single responsibility
- Use consistent schema patterns
- Share common utilities
- Be well-documented with examples

## Immediate Actions Required

1. **Fix chain_agent.py imports**:
   ```python
   # Remove non-existent imports
   from haive.agents.simple.agent import SimpleAgent
   from haive.agents.base.agent import Agent
   ```

2. **Remove duplicate chain implementations**:
   - Keep `/packages/haive-agents/src/haive/agents/chain/chain_agent_simple.py`
   - Remove `/packages/haive-agents/src/haive/agents/chain_agent.py`

3. **Fix RAG __init__.py files** that are preventing proper imports

4. **Consolidate ReAct implementations** to a single version

5. **Create proper base classes** for commonly referenced but missing classes