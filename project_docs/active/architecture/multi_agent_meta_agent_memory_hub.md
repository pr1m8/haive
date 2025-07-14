# Multi-Agent & Meta-Agent Architecture Memory Hub

**Document Version**: 1.0  
**Purpose**: Central memory hub linking all multi-agent and meta-agent architecture decisions  
**Last Updated**: 2025-01-13  
**Status**: Active Development

## 🎯 Quick Navigation

### Core Architecture Documents
- **[Multi-Agent State Design](../sessions/archive/meta_agent_state_design.md)** - Meta-agent state pattern with projections
- **[Agent vs Workflow Distinction](#agent-vs-workflow-architecture)** - Core architectural separation
- **[Node Analysis Requirements](../../../packages/haive-core/docs/node_analysis_requirements.md)** - Node schema composition analysis
- **[Current Issues](../sessions/active/current_issues.md)** - Active problems being solved

### Implementation Status
- **[Todo List](#current-todos)** - Active implementation tasks
- **[Testing Progress](#testing-status)** - MetaAgentState validation
- **[Schema Composition](#schema-composition-patterns)** - Field visibility work

## 🏗️ Architecture Overview

### Hierarchy
```
Workflow (pure orchestration - no LLM)
└── Agent (Workflow + AugLLMConfig)
    ├── SimpleAgent (basic agent pattern)
    ├── ReactAgent (reasoning loop pattern)
    └── MultiAgent (has agents field)
        ├── Sequential execution
        ├── Parallel execution
        └── Meta-agent patterns
```

### Key Distinctions
- **Workflow**: No `agents` field, no LLM required
- **Agent**: Has `engine: AugLLMConfig` (required)
- **MultiAgent**: Has `agents: Dict[str, Agent]` field

## 📋 Current Implementation Status

### ✅ Completed
1. **MetaAgentState Design** - Projection-based state container pattern
2. **Agent Architecture Analysis** - Clear Agent vs Workflow distinction
3. **Problem Identification** - Schema flattening issues documented
4. **MetaAgentState Testing** - ✅ **VALIDATED with SimpleAgentV2**
   - Real LLM execution (Azure OpenAI)
   - Agent embedding and execution working
   - State management and persistence validated
5. **Recompilation Mixin** - ✅ **WORKING Dynamic tool addition**
   - Tool change detection and recompilation triggering
   - Real state transitions (tools: 2 → 3)
   - Auto-recompilation workflow complete

### 🔄 In Progress - Ready for Implementation
1. **MultiAgent Sequential Pattern** - ReactAgent → SimpleAgent flow
2. **Structured Output in Multi-Agent** - Cross-agent data flow
3. **State Transfer Rules** - Inter-agent communication

### 📅 Pending
1. **Shared vs Private Fields** - Field visibility mechanism
2. **Schema Composition for Nodes** - NodeSchemaComposer
3. **Dynamic Graph Modification** - Runtime adaptation
4. **Async execute_agent** - MetaStateSchema async execution

## 🔑 Core Concepts

### 1. Meta-Agent State Pattern

**Problem Solved**: Schema flattening breaks type safety

**Solution**: Projection-based state container
```python
class MetaAgentState(StateSchema):
    # Shared state
    messages: List[BaseMessage]
    shared_context: Dict[str, Any]
    
    # Agent states (typed but stored as dicts)
    agent_states: Dict[str, Dict[str, Any]]
    agent_schemas: Dict[str, Type[StateSchema]]
    
    # Type-safe projections
    def get_agent_view(self, agent_name: str) -> AgentStateView
```

**References**:
- Design: `project_docs/sessions/archive/meta_agent_state_design.md`
- Implementation: `packages/haive-core/src/haive/core/schema/prebuilt/meta_state.py`
- Testing: `packages/haive-core/tests/test_meta_agent_state_simple_v2.py` ✅ **PASSING**

**Validation Results** (2025-01-13):
- **Real LLM Execution**: Azure OpenAI integration working
- **Agent Embedding**: SimpleAgentV2 properly contained in MetaStateSchema
- **Recompilation**: Dynamic tool addition triggers recompilation correctly
- **State Management**: Tools increased from 2 → 3, no mocks used

### 2. Agent vs Workflow Architecture

**Workflow** (Base):
- Pure orchestration logic
- No LLM requirement
- No agents field

**Agent** (Workflow + LLM):
- Required `engine: AugLLMConfig`
- LLM-powered decision making
- Can extend to MultiAgent

**MultiAgent** (Agent + Agents):
- Has `agents` field
- Coordinates multiple agents
- Uses LLM for orchestration decisions

### 3. State Management Patterns

**Shared Fields**:
- `messages` - All agents see
- `shared_context` - Common data

**Private Fields**:
- Agent-specific state
- Internal computations
- Temporary data

**Coordinator Fields**:
- Routing history
- Execution metadata
- Coordination state

### 4. Schema Composition Hierarchy

```
NodeSchemaComposer (missing - needed)
    ↓
AgentSchemaComposer (exists - for agents)
    ↓
MultiAgentSchemaComposer (needs update - field visibility)
```

## 🚀 Implementation Roadmap

### Phase 1: Foundation ✅ **COMPLETED**
- [x] Design MetaAgentState pattern
- [x] Create basic test structure ✅ **PASSING TESTS**
- [x] Validate recompilation mixin ✅ **WORKING**
- [x] Real LLM integration ✅ **AZURE OPENAI**
- [ ] Make execute_agent async
- [ ] Update AgentNodeV2 for projections

### Phase 2: MultiAgent Implementation 🔄 **CURRENT FOCUS**
- [ ] **ReactAgent → SimpleAgent sequential flow** - Primary target
- [ ] **Structured output cross-agent transfer** - Data flow patterns
- [ ] **Multi-agent state management** - Shared vs private fields
- [ ] **Real component testing** - No mocks, full integration

### Phase 3: Schema Composition
- [ ] Create NodeSchemaComposer
- [ ] Update MultiAgentSchemaComposer
- [ ] Handle dynamic composition
- [ ] Support runtime changes

### Phase 4: Integration
- [ ] Update existing multi-agents
- [ ] Clean up SimpleAgent
- [ ] Document patterns
- [ ] Performance optimization

## 📊 Testing Status

### MetaAgentState Testing ✅ **PASSING**
- **File**: `packages/haive-core/tests/test_meta_agent_state_simple_v2.py`
- **Status**: ✅ **VALIDATED with real Azure OpenAI**
- **Coverage**: State creation, agent embedding, real execution, recompilation
- **Results**: 
  - Real LLM calls working (3.49s execution time)
  - Tool management validated (2 → 3 tools)
  - Recompilation mixin functioning
  - No mocks used

### Multi-Agent Integration 🔄 **READY FOR IMPLEMENTATION**
- **Target**: ReactAgent → SimpleAgent sequential pattern
- **Agents**: ReactAgent (reasoning) → SimpleAgent (structured output)
- **Validation**: Cross-agent data flow, structured output transfer
- **Next**: Create test file for multi-agent sequential execution

## 🔗 Related Documentation

### Core Standards
- **[Coding Style Guide](../standards/coding/style_guide.md)** - Python standards
- **[Testing Philosophy](../standards/testing/philosophy.md)** - No mocks approach
- **[Memory System](../standards/documentation/memory_system.md)** - Documentation structure

### Package Documentation
- **[haive-core README](../haive-core/README.md)** - Core architecture
- **[haive-agents README](../haive-agents/README.md)** - Agent patterns
- **[CLAUDE.md](../../../CLAUDE.md)** - Main project hub

### Session Archives
- **Friday's Multi-Agent Work** - `project_docs/sessions/archive/meta_agent_state_design.md`
- **Schema Composition Analysis** - Various session files
- **Agent Review Sessions** - Base agent analysis

## 📝 Current TODOs

### High Priority
1. **✅ COMPLETED: MetaAgentState Implementation**
   - ✅ Real agent embedding and execution
   - ✅ Recompilation mixin validation
   - ✅ Azure OpenAI integration
   - [ ] Make execute_agent async

2. **🔄 CURRENT: MultiAgent Sequential Implementation**
   - ReactAgent → SimpleAgent pattern
   - Structured output cross-agent transfer
   - Real component testing (no mocks)
   - State management between agents

3. **Create NodeSchemaComposer**
   - Flexible I/O mapping
   - Extract/update functions
   - "result → potato" vision

### Medium Priority
4. **✅ COMPLETED: Test Recompilable Mixin**
   - ✅ Real tool addition (calculator → word_counter)
   - ✅ Dynamic recompilation triggering
   - ✅ State transitions validated

5. **Clean Up SimpleAgent**
   - Minimal implementation
   - Clear patterns
   - Foundation for others

6. **Build Agent vs Workflow Base**
   - Clear separation
   - Shared functionality
   - Type safety

## 🎯 Success Metrics

1. **✅ Type Safety**: Agents receive expected state types (MetaStateSchema validated)
2. **✅ Real Component Testing**: 100% no-mocks validation (Azure OpenAI working)
3. **✅ Recompilation**: Dynamic tool addition working (2 → 3 tools)
4. **Performance**: <1ms state projection overhead
5. **Developer Experience**: <10 lines to add new agent
6. **Documentation**: Clear patterns and examples

## 🚀 **NEXT IMPLEMENTATION: MultiAgent Sequential Pattern**

**Target**: ReactAgent → SimpleAgent flow with structured output transfer

**Key Requirements**:
1. **ReactAgent** performs reasoning and planning
2. **SimpleAgent** produces structured output from ReactAgent results
3. **State transfer** between agents without schema flattening
4. **Real LLM execution** for both agents (no mocks)
5. **Cross-agent data flow** validation

**Test Structure**:
```python
# Create ReactAgent for reasoning
react_agent = ReactAgent(name="reasoner", tools=[...])

# Create SimpleAgent for structured output  
simple_agent = SimpleAgent(name="formatter", structured_output_model=ResultModel)

# Sequential execution: ReactAgent → SimpleAgent
reasoning_result = await react_agent.arun("Analyze problem X")
structured_result = await simple_agent.arun(reasoning_result)
```

## 🚨 Critical Decisions Needed

1. **Field Visibility Mechanism**
   - Annotations: `Field(..., visibility="shared")`
   - Separate schemas: SharedState, PrivateState
   - Runtime rules: Dynamic filtering

2. **State Storage**
   - Agents in state (current plan)
   - Agent references only
   - Hybrid approach

3. **Schema Evolution**
   - Static at creation
   - Dynamic with recompilation
   - Fully runtime adaptive

4. **Coordination Patterns**
   - Sequential only
   - Full parallel support
   - Complex DAG workflows

## 📚 Quick Reference Code

### MetaAgentState Usage
```python
# Create meta state
meta_state = MetaAgentState()
meta_state.register_agent("planner", PlannerState)
meta_state.register_agent("executor", ExecutorState)

# Get typed view for agent
planner_view = meta_state.get_agent_view("planner")
# planner_view.agent_state is typed as PlannerState!

# Execute agent with proper state
result = await planner_agent.arun(planner_view.agent_state)

# Update meta state
meta_state.update_from_agent("planner", result)
```

### State Transfer Rules
```python
STATE_TRANSFERS = {
    ("planner", "executor"): {
        "plan": "plan",  # planner.plan → executor.plan
        "steps": "tasks"  # planner.steps → executor.tasks
    }
}
```

---

**Navigation**: 
- [Back to CLAUDE.md](../../../CLAUDE.md)
- [Current Issues](../sessions/active/current_issues.md)
- [Testing Philosophy](../standards/testing/philosophy.md)