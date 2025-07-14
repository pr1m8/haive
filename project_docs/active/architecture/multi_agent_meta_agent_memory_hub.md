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
4. **Testing Foundation** - Basic MetaAgentState test created

### 🔄 In Progress
1. **MetaAgentState Implementation** - Making execute_agent async
2. **AgentNodeV2 Updates** - Meta-state awareness
3. **State Transfer Rules** - Inter-agent data flow

### 📅 Pending
1. **Shared vs Private Fields** - Field visibility mechanism
2. **Schema Composition for Nodes** - NodeSchemaComposer
3. **Dynamic Graph Modification** - Runtime adaptation
4. **SimpleAgent Cleanup** - Minimal foundation pattern

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
- Testing: `packages/haive-core/tests/test_meta_agent_state.py`

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

### Phase 1: Foundation (Current)
- [x] Design MetaAgentState pattern
- [x] Create basic test structure
- [ ] Make execute_agent async
- [ ] Update AgentNodeV2 for projections

### Phase 2: State Management
- [ ] Implement field visibility annotations
- [ ] Create state transfer rules
- [ ] Build projection system
- [ ] Test with 2-agent flow

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

### MetaAgentState Testing
- **File**: `packages/haive-core/tests/test_meta_agent_state.py`
- **Status**: Basic structure created, needs async updates
- **Coverage**: State creation, agent registration, basic execution

### Multi-Agent Integration
- **Target**: Plan-and-Execute pattern
- **Agents**: PlannerAgent → ExecutorAgent
- **Validation**: Type safety, state transfer, no flattening

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
1. **Complete MetaAgentState Implementation**
   - Make execute_agent async
   - Add proper error handling
   - Implement state projections

2. **Design Shared vs Private Fields**
   - Field annotation mechanism
   - Visibility enforcement
   - State view filtering

3. **Create NodeSchemaComposer**
   - Flexible I/O mapping
   - Extract/update functions
   - "result → potato" vision

### Medium Priority
4. **Test Recompilable Mixin**
   - With real graph changes
   - Dynamic adaptation

5. **Clean Up SimpleAgent**
   - Minimal implementation
   - Clear patterns
   - Foundation for others

6. **Build Agent vs Workflow Base**
   - Clear separation
   - Shared functionality
   - Type safety

## 🎯 Success Metrics

1. **Type Safety**: Agents receive expected state types
2. **Performance**: <1ms state projection overhead
3. **Developer Experience**: <10 lines to add new agent
4. **Test Coverage**: 100% real component testing
5. **Documentation**: Clear patterns and examples

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