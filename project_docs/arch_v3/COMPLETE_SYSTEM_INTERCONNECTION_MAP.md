# Complete System Interconnection Map

**Created**: 2025-09-08
**Purpose**: Comprehensive map of how ALL components interconnect
**Status**: Active Analysis
**Complexity Score**: 82🔥 → Target <20🔥

## 🎯 Executive Summary

The Haive system has evolved into a tangled web where "Everything IS Everything". This document maps the complete interconnection between:

- **12+ Engine Types** (AugLLMConfig, DocumentEngine, ToolEngine, etc.)
- **12+ Node Types** (AgentNode, ValidationNode, ToolNode, etc.)
- **6 Schema Systems** (StateSchema, BaseModel, FieldDefinition, etc.)
- **Workflow vs Agent vs MultiAgent** hierarchy
- **State Injection Mechanisms** across all layers

## 🔥 The Core Problem: Circular Identity Crisis

```
Agent IS Engine (extends InvokableEngine)
    ↓
Agent HAS Engines (engine field)
    ↓
Engine HAS Nodes (creates nodes)
    ↓
Node HAS Engine (uses engines)
    ↓
Node IS Tool (can be tool)
    ↓
Tool IS Engine (ToolEngine)
    ↓
Engine IS Tool (can be used as tool)
```

**Result**: 82🔥 complexity score from circular dependencies and multiple identities.

## 📊 Complete Component Map

### 1. Engine Types and Their Usage

#### 1.1 AugLLMConfig (The Monster - 2,647 LOC)

```
Location: /haive/core/engine/aug_llm/config.py
Purpose: Everything - LLM config, tool management, validation, structured output
Used By: EVERYTHING (Agents, Nodes, Tools, Tests)
Problems:
  - 58 methods doing unrelated things
  - 15+ mixins creating inheritance chaos
  - Circular imports with nodes, agents, schemas
```

#### 1.2 DocumentEngine (Major Subsystem)

```
Location: /haive/core/engine/document/
Purpose: Document processing and state management
Extends: InvokableEngine
Used By:
  - DocumentNode
  - RAG Agents
  - Memory Systems
Problems:
  - IS an Engine but also HAS engines
  - Creates its own nodes internally
  - Manages state outside state system
```

#### 1.3 ToolEngine

```
Location: /haive/core/engine/tool/tool_engine.py (1,800 LOC)
Purpose: Tool execution and routing
Used By:
  - ToolNode
  - ValidationNode (for tool validation)
  - ReactAgent (for tool calls)
Problems:
  - Tools can BE engines
  - Engines can BE tools
  - Circular dependency
```

#### 1.4 RetrieverEngine

```
Location: /haive/core/engine/retriever/
Purpose: Vector store and retrieval operations
Used By:
  - RAG Agents
  - Memory Systems
  - Search Nodes
Problems:
  - Duplicates VectorStoreEngine functionality
  - Unclear separation from DocumentEngine
```

#### 1.5 VectorStoreEngine

```
Location: /haive/core/engine/vectorstore/
Purpose: Vector database operations
Used By:
  - RetrieverEngine (circular!)
  - RAG Agents
  - Memory Nodes
```

#### 1.6 EmbeddingEngine

```
Location: /haive/core/engine/embedding/
Purpose: Text embedding generation
Used By:
  - VectorStoreEngine
  - RetrieverEngine
  - Similarity Nodes
```

#### 1.7 OutputParserEngine

```
Location: /haive/core/engine/parser/
Purpose: Parse and validate LLM outputs
Used By:
  - ValidationNode
  - StructuredOutputMixin
  - Agents with structured output
```

#### 1.8 ValidationEngine

```
Location: /haive/core/engine/validation/
Purpose: Input/output validation
Used By:
  - ValidationNode
  - ToolNode
  - AgentNode
```

#### 1.9 CacheEngine

```
Location: /haive/core/engine/cache/
Purpose: Response caching
Used By:
  - AugLLMConfig
  - Agents
  - Expensive nodes
```

#### 1.10 RouterEngine

```
Location: /haive/core/engine/router/
Purpose: Route decisions
Used By:
  - RoutingNode
  - ConditionalNode
  - MultiAgent
```

#### 1.11 CompositeEngine

```
Location: /haive/core/engine/composite/
Purpose: Combine multiple engines
Used By:
  - Complex Agents
  - MultiAgent systems
Problems:
  - Engine of engines (inception!)
```

#### 1.12 StreamingEngine

```
Location: /haive/core/engine/streaming/
Purpose: Stream responses
Used By:
  - Streaming Agents
  - Real-time nodes
```

### 2. Node Types and Engine Relationships

#### 2.1 AgentNode / AgentNodeV2

```
Engines Used:
  - AugLLMConfig (primary)
  - ToolEngine (if tools)
  - ValidationEngine (for validation)
  - CacheEngine (optional)
State Flow:
  GraphState → extract agent fields → inject to Agent → Agent.run()
Problems:
  - Agent IS an Engine (InvokableEngine)
  - Node HAS Agent which IS Engine
  - Double engine execution
```

#### 2.2 ToolNode

```
Engines Used:
  - ToolEngine (primary)
  - ValidationEngine (input validation)
State Flow:
  GraphState → extract tool_calls → execute tools → update state
Problems:
  - Tools can BE engines themselves
  - Node executes Engine that might be Node
```

#### 2.3 ValidationNode / ValidationNodeV2

```
Engines Used:
  - ValidationEngine
  - OutputParserEngine
  - ToolEngine (for tool validation)
State Flow:
  GraphState → validate → route based on validation → update state
Problems:
  - Multiple validation systems
  - Routes to different nodes based on validation
```

#### 2.4 LLMNode

```
Engines Used:
  - AugLLMConfig (simplified)
State Flow:
  GraphState → extract messages → LLM call → update messages
Problems:
  - Duplicate of AgentNode without agent wrapper
```

#### 2.5 RoutingNode

```
Engines Used:
  - RouterEngine
  - Sometimes AugLLMConfig for LLM-based routing
State Flow:
  GraphState → evaluate conditions → determine next node
```

#### 2.6 ConditionalNode

```
Engines Used:
  - RouterEngine
  - ValidationEngine (condition checking)
State Flow:
  GraphState → check conditions → branch execution
```

#### 2.7 ParallelNode

```
Engines Used:
  - Multiple engines in parallel
State Flow:
  GraphState → split → parallel execution → merge results
Problems:
  - State synchronization issues
```

#### 2.8 MergeNode

```
Engines Used:
  - Custom merge logic
State Flow:
  Multiple states → merge strategy → unified state
```

#### 2.9 StartNode / EndNode

```
Engines Used: None (terminal nodes)
State Flow:
  StartNode: Initialize GraphState
  EndNode: Finalize and return
```

#### 2.10 CustomNode

```
Engines Used: Any combination
Problems:
  - No standard interface
  - Breaks all patterns
```

### 3. Schema Systems and State Injection

#### 3.1 StateSchema (Base State System)

```
Location: /haive/core/schema/state_schema.py
Purpose: Base state container
Used By: Everything
Injection:
  - Nodes receive full StateSchema
  - Must extract needed fields manually
Problems:
  - No type safety for field access
  - Schema flattening in composed states
```

#### 3.2 BaseModel (Pydantic Models)

```
Purpose: Configuration and structured data
Used By:
  - All configs (AugLLMConfig, etc.)
  - Structured output models
  - Tool definitions
Injection:
  - Validated on creation
  - Serialized for passing between components
```

#### 3.3 FieldDefinition System

```
Location: /haive/core/schema/field_definition.py
Purpose: Dynamic field definitions
Used By:
  - StateSchema
  - Dynamic schema composition
Problems:
  - Parallel to Pydantic Field
  - Inconsistent validation
```

#### 3.4 SchemaComposer

```
Location: /haive/core/schema/composer/
Purpose: Compose schemas dynamically
Used By:
  - MultiAgent
  - Complex workflows
Problems:
  - Loses type information
  - Field name conflicts
```

#### 3.5 Dict-based Schemas

```
Purpose: Legacy dynamic schemas
Used By:
  - Old agents
  - Dynamic nodes
Problems:
  - No validation
  - No type safety
```

#### 3.6 create_model() Dynamic Schemas

```
Purpose: Runtime schema creation
Used By:
  - Engine.derive_input_schema()
  - Dynamic agents
Problems:
  - No static type checking
  - Performance overhead
```

### 4. State Injection Flow

#### 4.1 Complete State Flow Path

```
1. User Input
   ↓
2. Graph.run(input) - Creates initial state
   ↓
3. GraphState (Complete state container)
   ↓
4. Node receives GraphState
   ↓
5. Node extracts needed fields (manual)
   ↓
6. Node passes to Engine
   ↓
7. Engine transforms for execution
   ↓
8. Actual execution (LLM, Tool, etc.)
   ↓
9. Result processing
   ↓
10. State update
    ↓
11. Next node
```

#### 4.2 State Injection Problems

**Problem 1: No Clear Contracts**

```python
# Node doesn't declare what it needs
class MyNode:
    def run(self, state):
        # Randomly grabs fields
        messages = state.get("messages")  # Hope it exists!
        context = state.get("context")    # Maybe?
```

**Problem 2: Schema Flattening**

```python
# Multiple schemas composed
ComposedSchema = StateSchema + AgentSchema + ToolSchema
# All fields flattened to same level
# Field name conflicts!
```

**Problem 3: Type Loss**

```python
# Start with typed schema
class TypedState(StateSchema):
    messages: List[Message]

# Becomes dict in node
def node_func(state: dict):  # Lost types!
    messages = state["messages"]  # No type checking
```

### 5. Workflow vs Agent vs MultiAgent Hierarchy

#### 5.1 Workflow (Pure Orchestration)

```
Location: /haive/agents/base/workflow.py
Purpose: Coordinate execution without LLM
Extends: BaseModel, ABC
Characteristics:
  - No engine field
  - No LLM dependency
  - Pure graph orchestration
  - Simple BaseModel inheritance
Status:
  - EXISTS! But not widely used
  - Clean separation from Agent
```

#### 5.2 Agent (Workflow + LLM)

```
Location: /haive/agents/base/agent.py
Extends: TypedInvokableEngine[EngineT] (!!)
Full Inheritance Chain:
  Agent
    → TypedInvokableEngine[EngineT]
    → InvokableEngine[BaseModel, BaseModel]
    → Engine[BaseModel, BaseModel]
    → ABC, BaseModel

Mixins Added:
  - ExecutionMixin
  - StateMixin
  - PersistenceMixin
  - SerializationMixin
  - StructuredOutputMixin
  - PrePostAgentMixin

Characteristics:
  - engine: EngineT field (generic)
  - engines: Dict[str, Engine] field (multiple!)
  - IS an Engine (InvokableEngine)
  - HAS an Engine (engine field)
  - HAS multiple Engines (engines dict)

Problems:
  - Triple identity crisis (IS and HAS and HAS MANY)
  - 6+ mixins creating complexity
  - Generic on engine type but also IS engine
  - Used for everything including non-agent workflows
```

#### 5.3 MultiAgent (Agent with Agents)

```
Location: /haive/agents/multi/agent.py
Extends: Agent
Characteristics:
  - agents: List[Agent] | Dict[str, Agent] field
  - execution_mode: "sequential" | "parallel" | "supervisor"
  - Coordinates multiple agents
  - Can use LLM for orchestration decisions

Problems:
  - Agent managing Agents
  - Each Agent IS an Engine
  - Nested engine execution (3+ levels deep)
  - MultiAgent IS Engine HAS Engine HAS Agents (which ARE Engines)
```

### 6. Critical Interconnection Patterns

#### 6.1 The Engine-Node-Engine Loop

```
Agent (IS Engine)
  → creates Graph
  → Graph has Nodes
  → Nodes have Engines
  → Engines might be Agents
  → (Infinite loop potential)
```

#### 6.2 The Tool-Engine Paradox

```
Tool can BE Engine (ToolEngine)
Engine can BE Tool (used as tool)
Node executes Engine that might be Tool that might be Engine
```

#### 6.3 The State Schema Tower

```
UserInput → AgentState → GraphState → NodeState → EngineInput → ToolInput
  ↓           ↓            ↓           ↓            ↓            ↓
dict      StateSchema  StateSchema  dict       dict        dict
```

#### 6.4 The Validation Maze

```
Validation happens at:
  - Pydantic models (automatic)
  - ValidationNode (explicit)
  - ToolNode (before tool execution)
  - AgentNode (before agent execution)
  - OutputParserEngine (after LLM)
  - StructuredOutputMixin (for structured output)
```

### 6. The REAL Hierarchy Discovery

#### 6.1 What Actually Exists

```python
# From /haive/agents/base/workflow.py
class Workflow(BaseModel, ABC):
    """Pure workflow orchestration without engine dependencies."""
    name: str
    verbose: bool = False
    debug: bool = False
    # NO engine field!
    # NO InvokableEngine inheritance!

# From /haive/agents/base/agent.py
class Agent(
    TypedInvokableEngine[EngineT],  # IS an Engine!
    ExecutionMixin,
    StateMixin,
    PersistenceMixin,
    SerializationMixin,
    StructuredOutputMixin,
    PrePostAgentMixin,
    ABC,
):
    """Agent = Workflow + Engine (but actually IS Engine too!)."""
    engine: EngineT | None  # HAS an engine
    engines: dict[str, Engine]  # HAS multiple engines
    # Agent both IS and HAS engines!

# From /haive/agents/multi/agent.py
class MultiAgent(Agent):
    """MultiAgent coordinates multiple agents."""
    agents: List[Agent] | Dict[str, Agent]
    execution_mode: str = "sequential"
    # MultiAgent IS Agent IS Engine HAS Engines HAS Agents (which ARE Engines)
```

#### 6.2 The Inheritance Nightmare

```
MultiAgent
  ↓ extends
Agent
  ↓ extends
TypedInvokableEngine[EngineT]
  ↓ extends
InvokableEngine[BaseModel, BaseModel]
  ↓ extends
Engine[BaseModel, BaseModel]
  ↓ extends
ABC, BaseModel

+ 6 Mixins:
  - ExecutionMixin
  - StateMixin
  - PersistenceMixin
  - SerializationMixin
  - StructuredOutputMixin
  - PrePostAgentMixin
```

#### 6.3 Why This Is Insane

1. **Agent IS an Engine** (through inheritance)
2. **Agent HAS an engine** (engine field)
3. **Agent HAS engines** (engines dict field)
4. **MultiAgent IS Agent** (so also IS Engine)
5. **MultiAgent HAS Agents** (which ARE Engines)

This creates infinite recursion potential:

- MultiAgent executes → creates Agents → which ARE Engines → which create nodes → which use Engines → which might be Agents → ...

## 🎯 Integration Approach Based on V3 Architecture

### Phase 1: Protocol Contracts (Foundation)

```
1. Executable - Things that execute
2. StateAware - Things that need state injection
3. Composable - Things that connect
4. RoleAdaptable - Things with multiple roles
```

### Phase 2: Engine Decomposition

```
Break AugLLMConfig into:
  - LLMConfig (pure LLM settings)
  - ToolConfig (tool management)
  - StructuredConfig (structured output)
  - ValidationConfig (validation rules)
  - CachingConfig (cache settings)
  - CompositeConfig (combination)
```

### Phase 3: Node Consolidation

```
Reduce to 4 core types:
  - ExecutionNode (pure execution)
  - ValidationNode (validation only)
  - RoutingNode (routing only)
  - TerminalNode (start/end)
```

### Phase 4: Schema Modularization

```
Separate schemas by domain:
  - StateSchemas (state management)
  - ConfigSchemas (configuration)
  - MessageSchemas (communication)
  - DomainSchemas (business logic)
```

### Phase 5: Clear Hierarchy

```
Workflow (no LLM, pure orchestration)
  ↓
Agent (Workflow + LLM)
  ↓
MultiAgent (Agent + agents field)
```

## 📊 Complexity Reduction Plan

### Current: 82🔥

- 12+ engine types with overlapping responsibilities
- 12+ node types with mixed concerns
- 6 parallel schema systems
- Circular dependencies everywhere
- No clear contracts

### Target: <20🔥

- 6 focused engine configs
- 4 single-responsibility nodes
- 1 unified schema system with composition
- Clean dependency hierarchy
- Protocol-based contracts

### Key Transformations

1. **AugLLMConfig**: 2,647 LOC → 6 configs @ ~300 LOC each
2. **12 Nodes**: 8,000 LOC → 4 nodes @ ~300 LOC each
3. **Schema Chaos**: 6 systems → 1 composed system
4. **Agent Identity**: Agent is NOT Engine, HAS engines
5. **State Injection**: Explicit contracts for what each component needs

## 🚨 Critical Path Forward

1. **Stop the Bleeding**: No new Engine types or Node types
2. **Implement Contracts**: Start with protocols, not inheritance
3. **Decompose AugLLMConfig**: Highest impact change
4. **Consolidate Nodes**: Reduce to 4 core types
5. **Fix State Injection**: Explicit state requirements
6. **Create Workflow**: Pure orchestration without Agent
7. **Refactor Agent**: Remove InvokableEngine inheritance
8. **Clean MultiAgent**: Use composition, not inheritance

## 🔑 Success Metrics

- **Complexity Score**: 82🔥 → <20🔥
- **Circular Dependencies**: 15+ → 0
- **Engine Types**: 12+ → 6 configs
- **Node Types**: 12+ → 4 core
- **Schema Systems**: 6 → 1 composed
- **LOC Reduction**: 50,000 → 30,500 (39%)
- **Test Coverage**: 60% → 95%+
- **Import Depth**: 12 layers → 8 layers

## 📋 Next Steps

1. Review this complete map
2. Validate understanding of all interconnections
3. Begin Protocol Contract implementation
4. Start AugLLMConfig decomposition
5. Create migration plan for existing code
