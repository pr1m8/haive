# Design Decisions - Dynamic Supervisor

## Key Architectural Decisions

### NEW: Agent Execution Node Pattern

**Decision**: Use general agent_execution_node instead of pre-compiled handoff tools
**Rationale**: Pre-compiled tools can't handle dynamic agent addition after graph compilation
**Implementation**: Single node that executes any agent based on routing state
**Benefits**: True dynamic agent management, similar to tool_node pattern

### 1. Supervisor as Extended ReactAgent

**Decision**: Build supervisor on top of ReactAgent rather than multi/base.py
**Rationale**: ReactAgent provides reasoning capabilities needed for dynamic routing
**Trade-offs**: More complex but more flexible than simple orchestration

### 2. Handoff Tools Pattern

**Decision**: Use langgraph_supervisor handoff tools (transfer_to_X)
**Rationale**: Provides proper state management and agent communication
**Alternative**: Direct tool routing (rejected - less maintainable)

### 3. Agent Registry with Serialization

**Decision**: Store full agent instances in registry, not just references
**Rationale**: Agents are serializable in Haive, allows dynamic activation
**Implementation**: AgentRegistry holds agent + description + active state

### 4. DynamicChoiceModel Integration

**Decision**: Use DynamicChoiceModel for validated agent selection
**Rationale**: Provides type-safe, validated choices that update dynamically
**Benefits**: Prevents invalid agent routing, auto-updates when registry changes

### 5. Pydantic Model Validators

**Decision**: Use @model_validator(mode="after") instead of **init**
**Rationale**: Proper Pydantic pattern, ensures all fields initialized first
**Pattern**: Setup logic in validators, not constructors
