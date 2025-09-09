# Essential Contracts and Architectural Layering

**Created**: 2025-01-30  
**Purpose**: Define the minimal set of contracts needed and how they layer  
**Goal**: Enable polymorphism while maintaining clarity

## 🎯 Core Contracts We Actually Need

### 1. Executable Contract (Foundation)

```python
from typing import Protocol, TypeVar, Generic

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

class Executable(Protocol[TIn, TOut]):
    """Anything that can execute - THE FOUNDATION CONTRACT"""

    def execute(self, input: TIn) -> TOut:
        """Synchronous execution"""
        ...

    async def aexecute(self, input: TIn) -> TOut:
        """Async execution"""
        ...
```

**Why Essential**: Everything in Haive ultimately executes something. This is the base behavior.

### 2. StateAware Contract (State Management)

```python
TState = TypeVar("TState")

class StateAware(Protocol[TState]):
    """Components that work with state"""

    def get_state_requirements(self) -> type[TState]:
        """What state this component needs"""
        ...

    def execute_with_state(self, input: TIn, state: TState) -> TOut:
        """Execute with injected state"""
        ...
```

**Why Essential**: Nodes need state injection, not random state grabbing.

### 3. Composable Contract (Building Blocks)

```python
class Composable(Protocol):
    """Components that can be composed into larger structures"""

    def get_input_schema(self) -> type:
        """What this accepts"""
        ...

    def get_output_schema(self) -> type:
        """What this produces"""
        ...

    def can_connect_to(self, other: "Composable") -> bool:
        """Check if output matches other's input"""
        return self.get_output_schema() == other.get_input_schema()
```

**Why Essential**: Enables type-safe composition of nodes, engines, tools.

### 4. RoleAdaptable Contract (Polymorphism Management)

```python
class RoleAdaptable(Protocol):
    """Components that can play multiple roles"""

    def get_roles(self) -> list[str]:
        """What roles this component can play"""
        ...

    def as_role(self, role: str) -> Any:
        """Get this component adapted to a specific role"""
        ...

    def validate_role(self, role: str) -> bool:
        """Check if this component can play a role"""
        ...
```

**Why Essential**: Manages the "everything can be everything" reality.

## 🏗️ How These Layer Together

### Layer 1: Execution Foundation

```python
# Everything builds on Executable
class BaseComponent(Executable[TIn, TOut]):
    """All components can execute"""

    def execute(self, input: TIn) -> TOut:
        # Core execution logic
        return self._process(input)
```

### Layer 2: State Management

```python
# Add state awareness to executable
class StatefulComponent(BaseComponent, StateAware[TState]):
    """Component with state injection"""

    def execute_with_state(self, input: TIn, state: TState) -> TOut:
        # Use injected state
        config = state.config
        context = state.context
        return self._process_with_context(input, config, context)
```

### Layer 3: Composition

```python
# Add composition to stateful components
class ComposableNode(StatefulComponent, Composable):
    """Node that can be composed with others"""

    input_schema: type = InputModel
    output_schema: type = OutputModel

    def get_input_schema(self) -> type:
        return self.input_schema

    def get_output_schema(self) -> type:
        return self.output_schema
```

### Layer 4: Role Adaptation

```python
# Add role flexibility
class VersatileComponent(ComposableNode, RoleAdaptable):
    """Component that can be tool, node, engine, etc."""

    def get_roles(self) -> list[str]:
        return ["tool", "node", "engine"]

    def as_role(self, role: str) -> Any:
        if role == "tool":
            return self._as_tool()
        elif role == "node":
            return self._as_node()
        elif role == "engine":
            return self._as_engine()
```

## 📐 How This Maps to Current Architecture

### Nodes → Implement All Contracts

```python
class EnhancedNode(Executable, StateAware, Composable, RoleAdaptable):
    """Modern node with all contracts"""

    # From Executable
    def execute(self, input):
        return self.process(input)

    # From StateAware
    def execute_with_state(self, input, state):
        return self.process_with_context(input, state)

    # From Composable
    def get_input_schema(self):
        return self.input_schema

    # From RoleAdaptable
    def as_role(self, role):
        return self.adapters[role](self)
```

### Engines → Factory Pattern with Contracts

```python
class ModernEngine(Composable):
    """Engine as factory, not executor"""

    def create_executable(self) -> Executable:
        """Create an executable component"""
        return ExecutableComponent(self.config)

    def get_input_schema(self):
        """Schema for what the created executable accepts"""
        return self.executable_input_schema

    def get_output_schema(self):
        """Schema for what the created executable produces"""
        return self.executable_output_schema
```

### Agents → Orchestrators Using Contracts

```python
class ModernAgent(Executable, StateAware):
    """Agent as orchestrator, not engine"""

    def __init__(self):
        self.nodes: list[Composable] = []
        self.state_manager: StateAware = StateManager()

    def execute(self, input):
        state = self.state_manager.get_state_requirements()

        # Orchestrate nodes
        result = input
        for node in self.nodes:
            if isinstance(node, StateAware):
                result = node.execute_with_state(result, state)
            else:
                result = node.execute(result)

        return result
```

### Documents → Implement Relevant Contracts

```python
class DocumentProcessor(Executable, Composable, RoleAdaptable):
    """Document processor with clear contracts"""

    # Core functionality
    def execute(self, input: DocumentInput) -> DocumentOutput:
        # Load → Split → Transform → Embed
        return self.pipeline.process(input)

    # Can be used as different things
    def as_role(self, role: str):
        if role == "tool":
            return Tool(func=self.execute)
        elif role == "node":
            return NodeAdapter(self)
        elif role == "engine":
            return EngineAdapter(self)
```

## 🎯 Architectural Goals Achievement

### Goal 1: Reduce Complexity (82🔥 → <20🔥)

**How Contracts Help**:

- Clear boundaries between components
- No more "everything inherits from everything"
- Explicit role management instead of implicit confusion

### Goal 2: Type Safety (0% → 100%)

**How Contracts Help**:

```python
# Full type checking with contracts
def connect_components(
    source: Composable,
    target: Composable
) -> bool:
    """Type-safe connection"""
    if source.get_output_schema() != target.get_input_schema():
        raise TypeError(f"Incompatible schemas: {source.get_output_schema()} → {target.get_input_schema()}")
    return True
```

### Goal 3: Maintain Flexibility

**How Contracts Help**:

```python
# Component can still be many things, but controlled
component = VersatileComponent()

# Explicit role usage
tool_version = component.as_role("tool")
node_version = component.as_role("node")
engine_version = component.as_role("engine")
```

### Goal 4: Enable Clean Node-to-Node Communication

**How Contracts Help**:

```python
# Nodes communicate through contracts
class Pipeline:
    def __init__(self, nodes: list[Composable & StateAware]):
        # Validate connections
        for i in range(len(nodes) - 1):
            source = nodes[i]
            target = nodes[i + 1]
            assert source.can_connect_to(target)

        self.nodes = nodes

    def execute(self, input, state):
        result = input
        for node in self.nodes:
            result = node.execute_with_state(result, state)
        return result
```

## 📊 Contract Implementation Priority

1. **Phase 1**: Implement Executable (everything can execute)
2. **Phase 2**: Add StateAware (enable state injection)
3. **Phase 3**: Add Composable (type-safe composition)
4. **Phase 4**: Add RoleAdaptable (manage polymorphism)

## 💡 Key Design Decisions

### 1. Contracts, Not Base Classes

```python
# ❌ OLD: Inheritance mess
class Node(Engine, Tool, Runnable, StateSchema):
    pass

# ✅ NEW: Protocol contracts
class Node:
    """Implements contracts, doesn't inherit mess"""

    def execute(self, input): ...  # Executable
    def execute_with_state(self, input, state): ...  # StateAware
    def get_input_schema(self): ...  # Composable
    def as_role(self, role): ...  # RoleAdaptable
```

### 2. Explicit Over Implicit

```python
# ❌ OLD: Is it a tool? Engine? Who knows?
component = SomeComponent()

# ✅ NEW: Explicit role declaration
component.as_role("tool")  # Now it's clearly a tool
```

### 3. Composition Over Inheritance

```python
# ❌ OLD: Agent IS Engine
class Agent(InvokableEngine):
    pass

# ✅ NEW: Agent HAS Executable components
class Agent:
    def __init__(self):
        self.executables: list[Executable] = []
```

## 🚀 Implementation Strategy

### Step 1: Define Protocol Module

```python
# haive/core/contracts/__init__.py
from .executable import Executable
from .state_aware import StateAware
from .composable import Composable
from .role_adaptable import RoleAdaptable

__all__ = [
    "Executable",
    "StateAware",
    "Composable",
    "RoleAdaptable"
]
```

### Step 2: Create Adapters for Existing Code

```python
# Make existing components comply with contracts
class LegacyAdapter:
    @staticmethod
    def make_executable(component) -> Executable:
        """Adapt any component to Executable contract"""
        if hasattr(component, "execute"):
            return component
        elif hasattr(component, "invoke"):
            return ExecutableWrapper(component.invoke)
        elif callable(component):
            return ExecutableWrapper(component)
```

### Step 3: Gradual Migration

- New components implement contracts directly
- Old components use adapters
- Eventually remove adapters as components are updated

## 🎯 Success Metrics

| Aspect             | Before                           | After with Contracts      |
| ------------------ | -------------------------------- | ------------------------- |
| Component Identity | Confused (IS many things)        | Clear (HAS many roles)    |
| Type Safety        | None                             | Full contract checking    |
| Testability        | Need entire system               | Test against contracts    |
| Coupling           | Everything depends on everything | Contract-based boundaries |
| Flexibility        | Chaotic                          | Structured polymorphism   |

The contracts provide the **minimal structure** needed to manage the **maximal flexibility** that makes Haive powerful.
