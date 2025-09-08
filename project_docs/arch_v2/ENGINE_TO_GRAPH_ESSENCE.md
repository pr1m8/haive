# The Engine → Schema → Node → Graph Essence

**Created**: 2025-01-06
**Purpose**: Understanding the core architectural flow of Haive
**Status**: Essential architecture mapping

## 🎯 The Core Flow

The Haive framework fundamentally follows this pattern:

```
Engine (Configuration)
    ↓
Schema (State Management)
    ↓
Node (Execution Unit)
    ↓
Graph (Workflow Orchestration)
```

## 🔧 1. ENGINE - The Configuration Layer

### Purpose

Engines are **lightweight, serializable configurations** that create heavy runtime components when needed.

### Core Concept

```python
# Engines separate configuration from runtime
class MyEngine(Engine):
    model_name: str = "gpt-4"
    temperature: float = 0.7

    def create_runnable(self) -> Runnable:
        """Create the actual runtime component."""
        return ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature
        )

# Configuration is lightweight
config = MyEngine(temperature=0.3)  # Just config, no resources

# Runtime component is heavy
llm = config.create_runnable()  # Actual LLM instance
```

### Key Engine Types

- **AugLLMConfig** - The 98-method monster that configures LLMs
- **RetrieverEngine** - Configures vector stores and retrievers
- **ToolEngine** - Manages tool execution
- **EmbeddingEngine** - Handles embeddings

### Problems Found

- **AugLLMConfig** has 98 methods, 2,601 lines - doing WAY too much
- Mixing configuration with execution logic
- Multiple competing systems (v1 vs v2 structured output)

## 📊 2. SCHEMA - The State Management Layer

### Purpose

Schemas define and manage the **state** that flows through the system.

### Core Concept

```python
# Schemas define state structure
class MessagesState(StateSchema):
    messages: List[BaseMessage]

    # StateSchema adds 74 methods for:
    # - Validation
    # - Engine management
    # - Dirty tracking
    # - Serialization
```

### The StateSchema Problem

StateSchema has **74 methods** handling:

- State data storage
- Field validation
- Engine registration
- Dirty field tracking
- Serialization/deserialization
- Schema composition
- Conflict resolution (broken!)

### Schema Composition Issue

```python
# When schemas compose, fields conflict
Schema1: {messages: List, context: Dict}
Schema2: {messages: List, tools: List}
Composed: {messages: ???, context: Dict, tools: List}
# No proper conflict resolution!
```

## 🔄 3. NODE - The Execution Unit

### Purpose

Nodes are the **execution units** that process state in a graph.

### Core Node Types

```python
# Different node types for different purposes
class AgentNode:      # Wraps an agent
class ToolNode:       # Executes tools
class ValidationNode: # Validates/routes
class RouterNode:     # Conditional routing
```

### The Node Explosion

- **45 node files** when ~10 would suffice
- Multiple versions (\_v2, \_v3)
- **AgentNodeConfig** has 105 log statements!
- Mixed responsibilities everywhere

### Node Wrapping Pattern

```python
# Nodes wrap engines/agents
agent = SimpleAgent(engine=config)
node = AgentNode(agent=agent)  # Wraps agent as node
```

## 🌐 4. GRAPH - The Workflow Orchestration

### Purpose

Graphs orchestrate the flow of state through nodes.

### The BaseGraph Monster

BaseGraph has **112 methods** including "intelligent" routing:

```python
# BaseGraph tries to guess workflow order!
def _infer_from_naming_patterns(self, agent_names):
    patterns = [
        "planner",    # Assumes planner comes first
        "analyzer",   # Then analyzer
        "executor",   # Then executor
        # 30+ hardcoded patterns!
    ]
```

### Graph Building Pattern

```python
# Intended pattern
graph = BaseGraph()
graph.add_node("process", process_func)
graph.add_edge(START, "process")
graph.add_edge("process", END)

# Reality: 112 methods of complexity
graph.add_intelligent_agent_routing(agents)  # "Magic"
```

## 🔥 The Broken Flow

### What Should Happen

```
1. Engine defines configuration
2. Schema defines state structure
3. Node wraps execution logic
4. Graph orchestrates flow
```

### What Actually Happens

```
1. AugLLMConfig (98 methods) does EVERYTHING
2. StateSchema (74 methods) manages EVERYTHING
3. Nodes (45 files) duplicate EVERYTHING
4. BaseGraph (112 methods) tries to be INTELLIGENT
```

## 🕸️ The Circular Dependencies

```
StateSchema needs Engines (has engine registry)
    ↓↑
Engines need StateSchema (for validation)
    ↓↑
Nodes need both (wrap agents with engines)
    ↓↑
Graph needs all three (orchestrates everything)
    ↓↑
Everything depends on everything!
```

## 💡 The Essence We Need

### 1. Simple Engine

```python
class Engine:
    """Just configuration."""
    def create_runnable(self): ...
```

### 2. Simple Schema

```python
class Schema:
    """Just state definition."""
    fields: Dict[str, Type]
```

### 3. Simple Node

```python
class Node:
    """Just execution."""
    def execute(self, state): ...
```

### 4. Simple Graph

```python
class Graph:
    """Just orchestration."""
    nodes: List[Node]
    edges: List[Edge]
```

## 🎯 The Core Problem

**Every layer is trying to do everything:**

1. **Engines** should just configure → but they validate, route, manage tools
2. **Schemas** should just define state → but they manage engines, track changes
3. **Nodes** should just execute → but they log, validate, route
4. **Graphs** should just orchestrate → but they compile, visualize, "intelligently" route

## 🔧 The Fix

### Decompose Each Layer

**Engine Layer**:

- Config (pure configuration)
- Factory (creates runnables)
- Registry (manages types)

**Schema Layer**:

- Fields (state definition)
- Validator (validation rules)
- Composer (composition logic)

**Node Layer**:

- Executor (runs logic)
- Wrapper (wraps components)
- Router (handles routing)

**Graph Layer**:

- Structure (nodes + edges)
- Builder (construction)
- Compiler (creates runnable)

## 📈 Metrics

| Layer        | Current Methods | Should Be | Reduction |
| ------------ | --------------- | --------- | --------- |
| AugLLMConfig | 98              | ~15       | 85%       |
| StateSchema  | 74              | ~10       | 86%       |
| Node System  | 45 files        | ~10 files | 78%       |
| BaseGraph    | 112             | ~20       | 82%       |

## 🚨 Critical Insight

The system's complexity comes from **each layer trying to be smart**:

- Engines try to be smart about tool management
- Schemas try to be smart about composition
- Nodes try to be smart about routing
- Graphs try to be "intelligent" about order

**Smart systems are fragile. Simple systems are robust.**

## 🎭 The Way Forward

1. **Accept simplicity** - Each layer does ONE thing
2. **Explicit over implicit** - No magic, no inference
3. **Composition over inheritance** - Small, focused components
4. **Configuration over code** - Separate config from logic

The essence is simple:

- **Engine** = Configuration
- **Schema** = State
- **Node** = Execution
- **Graph** = Orchestration

Everything else is accidental complexity that needs to be removed.

---

_"The architecture isn't complex because the problem is complex. It's complex because we made it complex."_
