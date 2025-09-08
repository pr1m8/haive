# HAIVE ARCHITECTURE MASTER PLAN

# Complete Implementation Roadmap: From Monoliths to Protocol-Based Architecture

**Created**: 2025-01-30  
**Version**: 1.0  
**Purpose**: THE definitive plan for transforming Haive from architectural collapse to protocol-based elegance  
**Status**: Ready for immediate implementation

---

## 🎯 EXECUTIVE SUMMARY

After analyzing **87 architectural documents**, **293 source files**, and **~81,000 lines of code**, the verdict is clear:

**Haive suffers from complete architectural collapse. An 88% reduction to ~10,000 lines is not only possible but essential.**

### The Core Discovery

**NodeSchemaComposer EXISTS** at `/packages/haive-core/src/haive/core/graph/node/composer/node_schema_composer.py` and can already do "result → potato" field mappings, but it's **completely disconnected** from the rest of the system!

### The Solution

**Don't rebuild - CONNECT what already exists through protocol-based architecture.**

---

## 📊 THE MONOLITHIC DISASTER

### The Seven Deadly Monoliths

| Component          | Current Lines | Methods | Primary Sin                                    | Target Lines | Reduction |
| ------------------ | ------------- | ------- | ---------------------------------------------- | ------------ | --------- |
| **BaseGraph**      | 3,972         | 112     | "Intelligent" routing with hardcoded patterns  | 500          | 87%       |
| **Agent**          | 3,600         | 47+     | Base class doing everything                    | 400          | 89%       |
| **SchemaComposer** | 3,378         | ?       | Schema management gone wild                    | 300          | 91%       |
| **AugLLMConfig**   | 2,601         | 98      | Configuration + execution + tools + everything | 300          | 88%       |
| **StateSchema**    | 2,323         | 74      | State + validation + engines + kitchen sink    | 200          | 91%       |
| **LLM/Base**       | 2,042         | ?       | LLM abstraction overload                       | 250          | 88%       |
| **DynamicGraph**   | 1,985         | ?       | Builder + compiler + visualizer                | 250          | 87%       |

### The File Explosion Crisis

```
📁 Current State (Chaos):
├── Engine Layer: 8 files, ~6,000 lines
├── Node Layer: 45 files, ~15,000 lines (45 files of GUESSING!)
├── Schema Layer: 10 files, ~7,000 lines
├── Graph Layer: 6 files, ~8,000 lines
├── Agent Layer: 119 files, ~25,000 lines
└── MultiAgent Layer: 105 files, ~20,000 lines
   Total: 293 files, ~81,000 lines

🎯 Target State (Order):
├── Engine Layer: 6 files, ~1,500 lines
├── Node Layer: 10 files, ~1,000 lines
├── Schema Layer: 8 files, ~1,200 lines
├── Graph Layer: 6 files, ~1,500 lines
├── Workflow Layer: 2 files, ~300 lines (NEW)
├── Agent Layer: 15 files, ~3,000 lines
└── MultiAgent Layer: 5 files, ~1,500 lines
   Total: 52 files, ~10,000 lines (88% REDUCTION!)
```

---

## 🔴 THE FUNDAMENTAL PROBLEMS

### 1. LangGraph's Static Constraint vs Haive's Dynamic Dreams

```python
# LangGraph's Reality (IMMUTABLE):
@dataclass(frozen=True)
class Command:
    # CANNOT change after compilation!

# Haive's Vision (MUTABLE):
class StateSchema:
    engines: dict  # Want to change engines at runtime!

# 🚨 This mismatch created ALL the monoliths
```

### 2. The Three Fatal Confusions

#### A. Data vs Behavior Confusion

```python
# ❌ WRONG - Pydantic models doing everything
class StateSchema(BaseModel):
    messages: List      # Data ✅
    def execute(self):  # Behavior ❌ (NOT PYDANTIC'S JOB!)
    def recompile(self): # More behavior ❌
```

#### B. Configuration vs Runtime Confusion

```python
# ❌ WRONG - Engines are both config AND runtime
class Engine(BaseModel):
    model: str          # Configuration ✅
    temperature: float  # Configuration ✅
    def invoke(self):   # Runtime execution ❌ (MIXED CONCERNS!)
```

#### C. Inheritance vs Composition Confusion

```python
# ❌ WRONG - Deep inheritance hell
class SimpleAgent(
    Agent, Mixin1, Mixin2, Mixin3, Mixin4, Mixin5, Mixin6, Mixin7
):
    # 14+ classes in MRO! INSANE!
```

---

## 🔗 THE CRITICAL DISCOVERY: DISCONNECTED COMPONENTS

### NodeSchemaComposer EXISTS But Operates in a Vacuum!

```python
# 🎉 THIS EXISTS AND WORKS!
composer = NodeSchemaComposer()
retriever_node = composer.compose_node(
    base_node=existing_retriever_node,
    output_mappings=[
        FieldMapping("documents", "retrieved_documents")  # "result → potato"
    ]
)

# 🚨 BUT IT'S COMPLETELY DISCONNECTED:
# ❌ Can't validate if StateSchema has "documents" field
# ❌ Can't check what type "documents" is
# ❌ Can't verify if engine expects "retrieved_documents" type
# ❌ 45 node files don't even know it exists!
```

### The Six Missing Links

1. **Engine ↔ Node**: ExecutionContract (missing) - Engines don't declare what they need
2. **Node ↔ Schema**: NodeSchemaComposer (EXISTS but DISCONNECTED!)
3. **Schema ↔ Graph**: SchemaProjection (broken) - Can't validate mappings
4. **Graph ↔ Workflow**: GraphStructure (overcomplicated) - 112 methods
5. **Workflow ↔ Agent**: Engine addition (embedded in base) - No clean separation
6. **Agent ↔ MultiAgent**: Agent composition (105 attempts) - No standard pattern

---

## ✅ THE PROTOCOL-BASED SOLUTION

### Core Principle: Contracts Over Guessing

Instead of 45 node files with 900 lines of guessing each:

```python
# 🎯 THE SOLUTION: ExecutionContract Protocol
class ExecutionContract(Protocol):
    """What every component MUST declare"""

    @property
    def input_schema(self) -> Schema:
        """What I need"""

    @property
    def output_schema(self) -> Schema:
        """What I produce"""

    def extract(self, state: State) -> Input:
        """How to get my input (NO GUESSING!)"""

    def update(self, state: State, output: Output) -> State:
        """How to update state (EXPLICIT!)"""

# Then ONE node replaces 45:
class ContractNode:  # 50 lines replaces 900!
    def __init__(self, contract: ExecutionContract):
        self.contract = contract

    def __call__(self, state: State) -> State:
        input = self.contract.extract(state)     # Explicit!
        output = self.execute(input)
        return self.contract.update(state, output)  # No guessing!
```

### The Four-Layer Clean Architecture

#### Layer 1: Data Models (Pydantic's Domain)

```python
# Pure data validation - NO BEHAVIOR
@dataclass(frozen=True)
class StateSnapshot:
    messages: tuple[Message, ...]
    context: FrozenDict
    version: int
    # ONLY data, ZERO methods
```

#### Layer 2: Protocols (Capability Contracts)

```python
# Define what components CAN do
class Executable(Protocol):
    async def execute(self, state: State) -> State: ...

class Compilable(Protocol):
    def compile(self) -> Compiled: ...

class Stateful(Protocol):
    def get_state(self) -> StateSnapshot: ...
```

#### Layer 3: Components (Composition)

```python
# Build complex from simple - HAS-A relationships
class Component:
    def __init__(self):
        self.state = StateContainer()      # Has-a state
        self.executor = Executor()         # Has-an executor
        self.compiler = Compiler()         # Has-a compiler
        # Compose, don't inherit!
```

#### Layer 4: Hierarchy (Simple Inheritance)

```python
# Maximum 3 levels, clear progression
Component                    # Base composition
├── Workflow                # + orchestration (no LLM)
├── Agent (Workflow)        # + intelligence (LLM)
└── MultiAgent (Agent)      # + coordination
```

---

## 🚀 IMPLEMENTATION ROADMAP

### 🏁 Phase 0: Connect Existing Components (Week 1)

**Goal**: Connect NodeSchemaComposer to the system

#### Day 1-2: Create Missing Contracts

```python
# File: /packages/haive-core/src/haive/core/protocols/execution.py
class ExecutionContract(Protocol):
    """Engine-Node communication contract"""

    @property
    def input_schema(self) -> Type[BaseModel]: ...

    @property
    def output_schema(self) -> Type[BaseModel]: ...
```

#### Day 3-4: Connect NodeSchemaComposer

```python
# Update 45 node files to use composer instead of guessing
class EngineNode:  # From 899 lines to 50!
    def __init__(self, contract: ExecutionContract):
        self.contract = contract
        self.composer = NodeSchemaComposer()  # Use existing!

    def __call__(self, state):
        # No more guessing - use contract + composer
        input = self.contract.extract(state)
        output = self.execute(input)
        return self.contract.update(state, output)
```

#### Day 5: Schema Interface for Composer

```python
# File: /packages/haive-core/src/haive/core/protocols/schema.py
class SchemaInterface(Protocol):
    """Clean interface for NodeSchemaComposer to validate against"""

    def has_field(self, field: str) -> bool: ...
    def get_field_type(self, field: str) -> Type: ...
    def validate_mapping(self, source: str, target: str) -> bool: ...
```

### 🔧 Phase 1: Engine Layer Decomposition (Week 2)

#### Current Monster: AugLLMConfig (2,601 lines, 98 methods)

```
❌ CURRENT: AugLLMConfig does EVERYTHING
├── Configuration (good) ✅
├── Execution (wrong!) ❌
├── Tool management (wrong!) ❌
├── Structured output v1 AND v2 (competing!) ❌
├── Validation, routing, serialization... ❌
```

#### Target Decomposition:

```python
# Decompose into focused components:
LLMConfig         # ~200 lines - pure configuration
LLMExecutor       # ~300 lines - execution only
ToolRegistry      # ~200 lines - tool management
OutputParser      # ~300 lines - structured output
MessageHandler    # ~200 lines - message handling
ValidationConfig  # ~150 lines - validation rules
RouteManager      # ~150 lines - routing logic
```

### 🧩 Phase 2: State System Modularization (Week 2)

#### Current God Object: StateSchema (2,323 lines, 74 methods)

```python
# ❌ CURRENT: StateSchema does EVERYTHING
class StateSchema:
    fields: dict                    # Data storage ✅
    engines: dict[str, Engine]      # Engine management ❌ (WHY HERE?!)
    _dirty_fields: set             # Dirty tracking ❌ (NOT DATA!)
    def compose_with()             # Composition ❌ (BROKEN!)
    def execute(), validate(), serialize()... # Everything ❌
```

#### Target Decomposition:

```python
StateData       # ~100 lines - pure data holder
StateValidator  # ~200 lines - validation only
StateSerializer # ~150 lines - I/O operations
EngineRegistry  # ~250 lines - engine management (SEPARATE!)
DirtyTracker    # ~150 lines - change tracking
SchemaComposer  # ~350 lines - composition logic
```

### 🏗️ Phase 3: Node Consolidation (Week 3)

#### Current Disaster: 45 Files of Guessing

```
❌ CURRENT: 45 files, ~15,000 lines
├── agent_node.py        # 566 lines - guessing
├── agent_node_v2.py     # 795 lines - still guessing
├── agent_node_v3.py     # 852 lines - "hierarchical" guessing
├── engine_node.py       # 899 lines - THE GUESSING MONSTER
└── ... 41 more files of guessing!
```

#### Target Solution: ContractNode System

```python
# ✅ NEW: 10 files, ~1,000 lines
ContractNode      # ~100 lines - base contract execution
EngineNode        # ~150 lines - engine-specific contracts
AgentNode         # ~150 lines - agent-specific contracts
ToolNode          # ~100 lines - tool execution contracts
ValidationNode    # ~100 lines - validation contracts
RouterNode        # ~100 lines - routing contracts
TransformNode     # ~100 lines - transformation contracts
ComposerNode      # ~100 lines - NodeSchemaComposer integration
StateNode         # ~50 lines - state management
EndNode           # ~50 lines - terminal nodes
```

### 🌐 Phase 4: Graph Simplification (Week 3-4)

#### Current "Intelligent" Disaster: BaseGraph (3,972 lines, 112 methods)

```python
# ❌ ACTUAL CODE trying to be AI:
class BaseGraph:
    def _infer_from_naming_patterns(self, agent_names):
        patterns = ["planner", "analyzer", "executor"]
        # Guesses workflow from names! INSANITY!

    def _extract_dependencies_from_prompt(self):
        # Regex parsing prompts for {other_agent}_result
        # This is architectural failure!
```

#### Target Decomposition:

```python
GraphStructure   # ~200 lines - pure topology (nodes + edges)
GraphBuilder     # ~300 lines - construction patterns
GraphCompiler    # ~400 lines - LangGraph integration
GraphExecutor    # ~300 lines - execution only
GraphVisualizer  # ~200 lines - visualization
GraphSerializer  # ~100 lines - I/O
# DELETE ALL "INTELLIGENT" ROUTING!
```

### 🎭 Phase 5: Workflow Layer Creation (Week 4)

#### Currently Missing: Clean Orchestration

```python
# ❌ CURRENT: Everything inherits from complex Agent
# Can't have pure orchestration without LLM
```

#### Target: Clean Separation

```python
class Workflow:  # ~100 lines - NEW!
    """Pure orchestration, no LLM required"""

    def build_graph(self) -> GraphStructure:
        """Define workflow topology"""

    def execute(self, input: Any) -> Any:
        """Run workflow"""

# Then Agent extends Workflow
class Agent(Workflow):  # ~200 lines
    engine: LLMEngine  # NOW it needs intelligence
```

### 🤖 Phase 6: Agent Simplification (Week 4-5)

#### Current Explosion: 119 Files

```
❌ CURRENT CHAOS:
├── base/agent.py        # 791 lines - 7 mixins
├── simple/
│   ├── agent.py         # Why?
│   ├── agent_v2.py     # Why v2?
│   └── agent_v3.py     # Why v3?
└── react/agent.py       # Elegant loop buried in 984 lines
```

#### Target: Clean Patterns

```python
# Base agent with composition (not inheritance)
class Agent:  # ~200 lines
    def __init__(self):
        self.workflow = Workflow()      # Compose workflow
        self.engine = LLMEngine()       # Compose engine
        self.hooks = HookManager()      # Compose hooks
        # No mixins, no inheritance hell!

# Keep ReactAgent's elegant loop:
# SimpleAgent: tool_node → END
# ReactAgent: tool_node → agent_node (LOOP!)
```

### 🚀 Phase 7: MultiAgent Consolidation (Week 5)

#### Current Chaos: 105 Files!

```
❌ CURRENT INSANITY:
├── enhanced_multi_agent_v4.py
├── enhanced_multi_agent_generic.py
├── simple_multi_agent.py
├── proper_list_multi_agent.py
└── ... 101 more attempts!
```

#### Target: One Clean Solution

```python
class MultiAgentCoordinator:  # ~400 lines total
    """One way to do multi-agent coordination"""

    def sequential(agents: List[Agent]) -> GraphStructure:
        """A → B → C"""

    def parallel(agents: List[Agent]) -> GraphStructure:
        """[A, B, C] then merge"""

    def hierarchical(supervisor: Agent, workers: List[Agent]) -> GraphStructure:
        """Supervisor coordinates workers"""
```

### 🏁 Phase 8: Migration & Polish (Week 6)

#### Compatibility & Documentation

```python
# Backward compatibility adapters
class LegacyAgent(SimpleAgent):
    """Compatibility wrapper for old agent API"""

    @property
    def temperature(self):
        return self.engine.temperature

    @temperature.setter
    def temperature(self, value):
        warnings.warn("Direct temperature setting deprecated", DeprecationWarning)
        self.engine.temperature = value
```

---

## 🔄 META-STATE SOLUTION FOR LANGGRAPH CONSTRAINTS

### The Workaround: Put Mutability IN State as Data

```python
class MetaStateSchema:
    """Put mutability IN the state as data"""

    # Engines are state data, not class attributes
    engines: dict[str, Engine]

    # Routing is data, not code
    routing_table: dict[str, str]

    # Everything dynamic goes IN state
    # State container is immutable, but its contents aren't!
```

This solves LangGraph's frozen compilation constraint while preserving runtime dynamism.

---

## 📋 IMPLEMENTATION PRIORITIES

### 🔥 Critical Path (Do First)

1. **Connect NodeSchemaComposer** - It exists, just wire it up!
2. **Create ExecutionContract protocol** - Stop the guessing
3. **Replace 45 node files with ContractNode** - Biggest immediate win
4. **Decompose StateSchema** - Break the god object

### 🎯 High Impact (Do Second)

1. **Engine layer decomposition** - AugLLMConfig → 7 focused components
2. **Graph simplification** - Delete "intelligent" routing
3. **Agent inheritance cleanup** - Composition over inheritance

### 🔧 Infrastructure (Do Third)

1. **Workflow layer creation** - Clean orchestration
2. **MultiAgent consolidation** - 105 → 5 files
3. **Migration tools** - Backward compatibility

---

## 📊 SUCCESS METRICS

### Code Quality Metrics

- **90% code reduction** in critical paths (81,000 → 10,000 lines)
- **No more guessing** - explicit contracts everywhere
- **<100ms soft recompilation** (vs 10.5s currently)
- **Clean separation** - each component does ONE thing
- **Type safety** throughout the system

### Developer Experience Metrics

- **Junior dev understands in 10 min** (vs current confusion)
- **Single source of truth** for each concept
- **95% test coverage** with real components (no mocks)
- **Clear migration path** from old to new

### Performance Metrics

- **<100ms recompilation** (from 10.5s)
- **<10ms state operations**
- **<50ms hot-swapping**
- **50% memory reduction**

---

## 🗂️ DOCUMENT REFERENCES

### Must Read Foundation Documents

- **[COMPLETE_ARCHITECTURE_ANALYSIS.md](COMPLETE_ARCHITECTURE_ANALYSIS.md)** - Deep architectural analysis
- **[UNIFIED_ARCHITECTURE_SYNTHESIS.md](UNIFIED_ARCHITECTURE_SYNTHESIS.md)** - 70+ doc synthesis
- **[IMPLEMENTATION_ROADMAP.md](IMPLEMENTATION_ROADMAP.md)** - Protocol-based transformation

### Key Implementation Guides

- **[CONTRACT_IMPLEMENTATION_EXAMPLE.md](CONTRACT_IMPLEMENTATION_EXAMPLE.md)** - How protocols work
- **[SERIALIZABLE_MODIFICATION_ARCHITECTURE.md](SERIALIZABLE_MODIFICATION_ARCHITECTURE.md)** - Runtime modifications
- **[LANGGRAPH_LIMITATIONS_AND_HAIVE_WORKAROUNDS.md](LANGGRAPH_LIMITATIONS_AND_HAIVE_WORKAROUNDS.md)** - Static constraint solutions

### Problem Analysis Documents

- **[THE_MONOLITH_CRISIS.md](THE_MONOLITH_CRISIS.md)** - Why StateSchema is bad
- **[NODE_MODULE_CRISIS.md](NODE_MODULE_CRISIS.md)** - 50+ node variants problem
- **[CIRCULAR_DEPENDENCY_ANALYSIS.md](CIRCULAR_DEPENDENCY_ANALYSIS.md)** - Import cycle issues

### All 87 Supporting Documents

```
project_docs/arch_v2/
├── Core Analysis (20 docs)
│   ├── COMPLETE_ARCHITECTURAL_ANALYSIS.md
│   ├── COMPREHENSIVE_ARCHITECTURE_ANALYSIS.md
│   └── ... (18 more)
├── Implementation Plans (25 docs)
│   ├── IMPLEMENTATION_ROADMAP.md
│   ├── HAIVE_IMPROVEMENT_PLAN.md
│   └── ... (23 more)
├── Contract & Protocol Design (15 docs)
│   ├── CONTRACT_IMPLEMENTATION_EXAMPLE.md
│   ├── UNIFIED_CONTRACT_ARCHITECTURE.md
│   └── ... (13 more)
├── Performance & Optimization (12 docs)
│   ├── PRACTICAL_SOFT_RECOMPILATION_IMPLEMENTATION.md
│   ├── PERFORMANCE_BOTTLENECK_ANALYSIS.md
│   └── ... (10 more)
└── Supporting Analysis (15 docs)
    ├── LANGGRAPH_STATIC_ANALYSIS.md
    ├── CORRECTED_ARCHITECTURAL_UNDERSTANDING.md
    └── ... (13 more)
```

---

## 💡 KEY ARCHITECTURAL INSIGHTS

### 1. The Solution Already Exists - It Just Can't Talk

**NodeSchemaComposer is already built and working!** The problem isn't missing functionality - it's disconnected components that can't communicate.

### 2. Contracts Eliminate Guessing

45 node files with 900 lines of guessing each → 1 ContractNode with 50 lines of explicit contracts.

### 3. Every Layer is 5-10x Larger Than Needed

Due to violating separation of concerns and trying to guess instead of using explicit contracts.

### 4. LangGraph's Frozen Types Are The Root Constraint

Work around them with MetaStateSchema - put mutability IN state as data, not as class attributes.

### 5. "Intelligent" Routing is a Symptom of Architectural Failure

BaseGraph trying to guess dependencies from names shows the architecture has collapsed.

---

## 🎯 THE PATH FORWARD

### Week 1: Connect the Disconnected

- Create ExecutionContract protocol
- Wire NodeSchemaComposer into 45 node files
- Build SchemaInterface for validation
- **Result**: NodeSchemaComposer finally connected to system

### Week 2-3: Decompose the Monoliths

- Break StateSchema into 6 focused modules
- Decompose AugLLMConfig into 7 components
- Replace 45 node files with ContractNode
- **Result**: Clean separation of concerns

### Week 4-5: Build the Missing Layer

- Create Workflow layer for pure orchestration
- Simplify Agent to composition over inheritance
- Consolidate 105 MultiAgent files to 5 patterns
- **Result**: Clean 3-layer hierarchy

### Week 6: Migration & Polish

- Build compatibility adapters
- Create migration tools
- Write comprehensive documentation
- **Result**: Smooth transition to new architecture

---

## 🚨 CRITICAL SUCCESS FACTORS

### 1. Don't Rebuild - Connect

NodeSchemaComposer exists and works. The problem is communication, not functionality.

### 2. Protocols Over Guessing

Replace every instance of "guess what the engine needs" with explicit contracts.

### 3. Separation of Concerns

Data (Pydantic) | Behavior (Protocols) | Structure (Composition) | Execution (Contracts)

### 4. Maximum 3 Inheritance Levels

Component → Workflow → Agent → MultiAgent. No deeper hierarchies.

### 5. Real Component Testing

95% test coverage with actual LLMs, real tools, real components. Zero mocks.

---

## 🎯 CALL TO ACTION

The analysis is complete. The solution is clear. The path is mapped.

**The Haive framework is experiencing architectural collapse due to monolithic design violating basic software principles. The protocol-based architecture with explicit contracts is the only escape.**

**NodeSchemaComposer exists and works - it just needs to be connected to the system through ExecutionContract protocols.**

**Start with Phase 0: Connect what already exists. The transformation begins now.**

---

_"After 87 documents, 293 files, and 81,000 lines of analysis, the conclusion is unanimous: Separate concerns. Use protocols. Compose don't inherit. Make state immutable. The monoliths are symptoms of trying to force runtime mutability into compile-time frozen systems. The protocol-based architecture is the cure."_

**Implementation starts immediately. The architecture's future depends on it.**
