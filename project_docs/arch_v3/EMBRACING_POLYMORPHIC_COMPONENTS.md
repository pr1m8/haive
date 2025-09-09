# Embracing Polymorphic Components - The "Can Be" Architecture

**Created**: 2025-01-30  
**Purpose**: Accept and design for the reality that components can be many things  
**Philosophy**: Don't fight polymorphism, embrace and structure it

## 🎯 The Reality: Everything CAN BE Everything (And That's OK!)

```
Tool CAN BE Engine
Tool CAN BE Node
Tool CAN BE BaseModel
Node CAN BE Agent
Node CAN BE Tool
Agent CAN BE Tool (as_tool())
Engine CAN BE Node
Document CAN BE Tool
Document CAN BE Engine
...and so on
```

**This isn't wrong - it's FLEXIBLE!**

## 💡 The Insight: It's About CONTEXT

A component isn't inherently one thing - it becomes what's needed in context:

```python
# A search tool in different contexts

class SearchComponent:
    """One component, many roles"""

    def search(self, query: str) -> list[str]:
        """Core functionality"""
        return perform_search(query)

# Context 1: As a Tool (for agents)
tool_context = Tool(
    name="search",
    func=SearchComponent().search,
    description="Search for information"
)

# Context 2: As an Engine (creates search executables)
class SearchEngine(InvokableEngine):
    def invoke(self, input):
        return SearchComponent().search(input["query"])

# Context 3: As a Node (in a graph)
class SearchNode(NodeConfig):
    def __call__(self, state):
        query = state["query"]
        results = SearchComponent().search(query)
        return {"search_results": results}

# Context 4: As a BaseModel (for structured output)
class SearchModel(BaseModel):
    query: str
    max_results: int = 10

    def __call__(self):
        return SearchComponent().search(self.query)[:self.max_results]
```

## 🏗️ The Solution: Role-Based Architecture

### 1. Core Functionality + Role Adapters

```python
from typing import Protocol

# Define what each role needs
class ToolRole(Protocol):
    """What it means to be a tool"""
    def execute_as_tool(self, input: str) -> Any: ...

class NodeRole(Protocol):
    """What it means to be a node"""
    def execute_as_node(self, state: dict) -> dict: ...

class EngineRole(Protocol):
    """What it means to be an engine"""
    def create_runnable(self) -> Callable: ...

# Components can fulfill multiple roles
class VersatileComponent:
    """Component that can be many things"""

    def __init__(self):
        self.core_logic = self._do_work

    def _do_work(self, input):
        """The actual work"""
        return f"processed: {input}"

    # Role implementations
    def execute_as_tool(self, input: str) -> Any:
        """Tool role"""
        return self.core_logic(input)

    def execute_as_node(self, state: dict) -> dict:
        """Node role"""
        result = self.core_logic(state.get("input", ""))
        return {"output": result}

    def create_runnable(self) -> Callable:
        """Engine role"""
        return lambda x: self.core_logic(x)

    # Context-aware interface
    def as_tool(self) -> Tool:
        return Tool(func=self.execute_as_tool)

    def as_node(self) -> NodeConfig:
        return NodeConfig(callable_func=self.execute_as_node)

    def as_engine(self) -> Engine:
        return Engine(create_func=self.create_runnable)
```

### 2. The Role Registry Pattern

```python
class RoleRegistry:
    """Tracks what roles a component can play"""

    def __init__(self):
        self.components = {}
        self.roles = defaultdict(list)

    def register(self, component, roles: list[str]):
        """Register a component with its capabilities"""
        comp_id = id(component)
        self.components[comp_id] = component

        for role in roles:
            self.roles[role].append(comp_id)

    def get_as(self, component, role: str):
        """Get component in specific role"""
        adapters = {
            "tool": lambda c: c.as_tool() if hasattr(c, 'as_tool') else ToolAdapter(c),
            "node": lambda c: c.as_node() if hasattr(c, 'as_node') else NodeAdapter(c),
            "engine": lambda c: c.as_engine() if hasattr(c, 'as_engine') else EngineAdapter(c),
        }
        return adapters[role](component)

    def find_by_role(self, role: str):
        """Find all components that can play a role"""
        return [self.components[cid] for cid in self.roles[role]]
```

### 3. Document System Example - Embracing All Roles

```python
class DocumentProcessor:
    """Document processor that can be everything"""

    def __init__(self):
        self.pipeline = []

    def process(self, input):
        """Core processing logic"""
        result = input
        for stage in self.pipeline:
            result = stage(result)
        return result

    # As Tool (for agent use)
    def as_tool(self) -> Tool:
        return Tool(
            name="document_processor",
            func=self.process,
            description="Process documents"
        )

    # As Node (for graph use)
    def as_node(self) -> NodeConfig:
        def node_func(state):
            docs = state.get("documents", [])
            processed = [self.process(doc) for doc in docs]
            return {"processed_documents": processed}

        return NodeConfig(
            name="document_processor_node",
            callable_func=node_func
        )

    # As Engine (for creating processors)
    def as_engine(self) -> Engine:
        class DocEngine(InvokableEngine):
            def __init__(self, processor):
                self.processor = processor

            def invoke(self, input):
                return self.processor.process(input)

            def create_runnable(self):
                return self.processor.process

        return DocEngine(self)

    # As BaseModel (for structured output)
    def as_model(self) -> type[BaseModel]:
        class DocModel(BaseModel):
            content: str
            metadata: dict = {}

            def process(self):
                return DocumentProcessor().process(self.dict())

        return DocModel
```

### 4. The Universal Adapter Pattern

```python
class UniversalAdapter:
    """Adapts anything to anything"""

    @staticmethod
    def adapt(source: Any, target_role: str) -> Any:
        """Smart adaptation based on source and target"""

        # Check if source already has the role
        if hasattr(source, f"as_{target_role}"):
            return getattr(source, f"as_{target_role}")()

        # Check known patterns
        if target_role == "tool":
            if callable(source):
                return Tool(func=source)
            elif isinstance(source, type) and issubclass(source, BaseModel):
                return StructuredTool.from_model(source)
            elif hasattr(source, "invoke"):
                return Tool(func=source.invoke)

        elif target_role == "node":
            if callable(source):
                return NodeConfig(callable_func=source)
            elif hasattr(source, "execute"):
                return NodeConfig(callable_func=source.execute)

        elif target_role == "engine":
            if hasattr(source, "create_runnable"):
                return source  # Already an engine
            else:
                # Wrap in engine
                class AdaptedEngine(InvokableEngine):
                    def invoke(self, input):
                        if callable(source):
                            return source(input)
                        raise NotImplementedError
                return AdaptedEngine()

        raise ValueError(f"Cannot adapt {type(source)} to {target_role}")
```

## 🎨 Design Principles for Polymorphic Components

### 1. Core + Roles Separation

- **Core**: The actual logic/functionality
- **Roles**: Different interfaces to that functionality

### 2. Explicit Role Declaration

```python
@roles(["tool", "node", "engine"])
class MyComponent:
    """Explicitly declares what roles it can play"""
    pass
```

### 3. Context-Aware Usage

```python
# Use the right role for the context
component = MyComponent()

# In agent context
agent.add_tool(component.as_tool())

# In graph context
graph.add_node(component.as_node())

# In engine context
engine_registry.register(component.as_engine())
```

### 4. Role Validation

```python
def validate_role(component, role: str) -> bool:
    """Check if component can play a role"""
    required_methods = {
        "tool": ["execute_as_tool"],
        "node": ["execute_as_node"],
        "engine": ["create_runnable"]
    }

    for method in required_methods.get(role, []):
        if not hasattr(component, method):
            return False
    return True
```

## 🔄 Migration to Role-Based Architecture

### Step 1: Identify Core Functionality

```python
# Before: Mixed concerns
class MessyComponent(Engine, Tool, Node):
    def invoke(self): ...
    def __call__(self): ...
    def execute(self): ...

# After: Clear core
class CleanComponent:
    def core_logic(self): ...
    def as_tool(self): ...
    def as_node(self): ...
    def as_engine(self): ...
```

### Step 2: Create Role Adapters

```python
# Adapter for each role
class ToolAdapter:
    def __init__(self, component):
        self.component = component

    def execute(self, input):
        return self.component.core_logic(input)
```

### Step 3: Use Role Registry

```python
registry = RoleRegistry()
registry.register(component, ["tool", "node", "engine"])

# Get component in needed role
tool_version = registry.get_as(component, "tool")
```

## 💡 Key Insight

**The flexibility of "CAN BE" is a FEATURE, not a bug!**

Instead of fighting it, we:

1. **Embrace** the polymorphism
2. **Structure** it with roles
3. **Control** it with adapters
4. **Document** what roles each component can play

This gives us maximum flexibility while maintaining clarity and type safety.
