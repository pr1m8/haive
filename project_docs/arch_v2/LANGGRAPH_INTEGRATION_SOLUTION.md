# LangGraph Integration Solution - Type-Safe Dynamic Execution

**Created**: 2025-01-07  
**Purpose**: Proper integration with LangGraph's Send/Command types and StateGraph  
**Status**: Implementation-ready solution based on actual LangGraph code

## 📋 Summary

After analyzing the actual LangGraph implementation in the virtual environment, here's the correct approach for type-safe dynamic execution that works with the existing LangGraph architecture.

## 🔍 Key Findings from LangGraph Source

### 1. Send Type (from langgraph/types.py)

```python
class Send:
    """A message or packet to send to a specific node in the graph."""
    __slots__ = ("node", "arg")

    node: str  # Target node name
    arg: Any   # State or message to send

    def __init__(self, /, node: str, arg: Any) -> None:
        self.node = node
        self.arg = arg
```

### 2. Command Type (from langgraph/types.py)

```python
@dataclasses.dataclass(frozen=True, kw_only=True, slots=True)
class Command(Generic[N], ToolOutputMixin):
    """Commands to update the graph's state and send messages to nodes."""

    graph: Optional[str] = None
    update: Optional[Any] = None
    resume: Optional[Union[Any, dict[str, Any]]] = None
    goto: Union[Send, Sequence[Union[Send, str]], str] = ()
```

### 3. StateGraph Dynamic Schema (from langgraph/graph/state.py)

```python
# StateGraph uses TypedDict or Annotated fields with reducers
class State(TypedDict):
    x: Annotated[list, reducer]  # Field with reducer function

# Dynamic model creation using langgraph.utils.pydantic.create_model
create_model(
    name,
    field_definitions={
        k: (channels[k].UpdateType, get_field_default(k, channels[k].UpdateType, typ))
        for k in schemas[typ]
    },
)
```

## ✅ The Correct Solution

### 1. Type-Safe Send Wrapper

```python
from typing import TypeVar, Generic, Type, Any, Protocol
from langgraph.types import Send as LangGraphSend
from pydantic import BaseModel

StateT = TypeVar('StateT', bound=BaseModel)

class TypedSend(Generic[StateT]):
    """Type-safe wrapper around LangGraph Send."""

    def __init__(self, node: str, arg: StateT):
        self.node = node
        self.arg = arg
        self._state_type: Type[StateT] = type(arg)
        # Create actual LangGraph Send
        self._send = LangGraphSend(node, arg)

    def to_langgraph(self) -> LangGraphSend:
        """Convert to LangGraph Send for execution."""
        return self._send

    def validate_state(self, expected_type: Type) -> bool:
        """Validate that arg matches expected state type."""
        return isinstance(self.arg, expected_type)
```

### 2. Type-Safe Command Wrapper

```python
from langgraph.types import Command as LangGraphCommand
from typing import Optional, Union, Sequence

class TypedCommand(Generic[StateT]):
    """Type-safe wrapper around LangGraph Command."""

    def __init__(
        self,
        graph: Optional[str] = None,
        update: Optional[StateT] = None,
        resume: Optional[Union[Any, dict[str, Any]]] = None,
        goto: Union[str, Sequence[str], TypedSend[StateT], Sequence[TypedSend[StateT]]] = ()
    ):
        self.graph = graph
        self.update = update
        self.resume = resume
        self.typed_goto = goto

        # Convert TypedSend to LangGraph Send
        if isinstance(goto, TypedSend):
            goto_langgraph = goto.to_langgraph()
        elif isinstance(goto, (list, tuple)):
            goto_langgraph = [
                g.to_langgraph() if isinstance(g, TypedSend) else g
                for g in goto
            ]
        else:
            goto_langgraph = goto

        # Create actual LangGraph Command
        self._command = LangGraphCommand(
            graph=graph,
            update=update,
            resume=resume,
            goto=goto_langgraph
        )

    def to_langgraph(self) -> LangGraphCommand:
        """Convert to LangGraph Command for execution."""
        return self._command
```

### 3. Dynamic State Schema with Type Hints

```python
from typing import Dict, Type, Any, get_type_hints
from typing_extensions import Annotated
from pydantic import create_model as pydantic_create_model
from langgraph.graph import StateGraph

class TypedStateBuilder:
    """Build StateGraph-compatible schemas with runtime type safety."""

    def __init__(self, base_schema: Type[BaseModel]):
        self.base_schema = base_schema
        self.dynamic_fields: Dict[str, tuple[type, Any]] = {}
        self.reducers: Dict[str, callable] = {}

    def add_field(
        self,
        name: str,
        field_type: type,
        default: Any = ...,
        reducer: Optional[callable] = None
    ) -> 'TypedStateBuilder':
        """Add field with optional reducer for StateGraph."""
        if reducer:
            # Create Annotated type for reducer
            self.dynamic_fields[name] = (
                Annotated[field_type, reducer],
                default
            )
            self.reducers[name] = reducer
        else:
            self.dynamic_fields[name] = (field_type, default)
        return self

    def build_for_stategraph(self) -> Type[BaseModel]:
        """Build schema compatible with StateGraph."""
        # Get base fields
        base_fields = {}
        if hasattr(self.base_schema, '__annotations__'):
            base_fields = get_type_hints(self.base_schema, include_extras=True)

        # Merge with dynamic fields
        all_fields = {**base_fields}
        for name, (field_type, default) in self.dynamic_fields.items():
            all_fields[name] = field_type

        # Create TypedDict-style class for StateGraph
        class DynamicState(self.base_schema):
            __annotations__ = all_fields

        # Add defaults
        for name, (_, default) in self.dynamic_fields.items():
            if default is not ...:
                setattr(DynamicState, name, default)

        return DynamicState
```

### 4. Enhanced Validation Node

```python
from langgraph.graph import END
from typing import Union

class TypeSafeValidationNode:
    """Validation node that properly handles Send/Command with types."""

    def __init__(self, expected_state_type: Type[BaseModel]):
        self.expected_state_type = expected_state_type

    def __call__(self, state: Any) -> Union[str, LangGraphSend, LangGraphCommand]:
        """Process state and return routing decision."""

        # Validate state type
        if not isinstance(state, self.expected_state_type):
            # Try to coerce
            try:
                state = self.expected_state_type(**state)
            except Exception as e:
                raise TypeError(f"Invalid state type: {e}")

        # Process and route
        if hasattr(state, 'command'):
            cmd = state.command
            if isinstance(cmd, TypedCommand):
                return cmd.to_langgraph()
            elif isinstance(cmd, LangGraphCommand):
                return cmd

        if hasattr(state, 'send'):
            send = state.send
            if isinstance(send, TypedSend):
                return send.to_langgraph()
            elif isinstance(send, LangGraphSend):
                return send

        # Default routing
        return END
```

## 🚀 Integration with Haive's BaseGraph2

### Fix for BaseGraph2 Validation

```python
# In BaseGraph2._create_validation_wrapper

def _create_validation_wrapper(self, node_func, node_name):
    """Create wrapper that handles Send/Command properly."""

    def wrapper(state):
        result = node_func(state)

        # Handle LangGraph Send
        if isinstance(result, LangGraphSend):
            return result

        # Handle TypedSend
        if isinstance(result, TypedSend):
            return result.to_langgraph()

        # Handle LangGraph Command
        if isinstance(result, LangGraphCommand):
            return result

        # Handle TypedCommand
        if isinstance(result, TypedCommand):
            return result.to_langgraph()

        # Handle string-based checks (keep for compatibility)
        if hasattr(result, "__class__"):
            class_name = result.__class__.__name__
            if "Command" in class_name or "Send" in class_name:
                # Try to convert if it's our typed version
                if hasattr(result, "to_langgraph"):
                    return result.to_langgraph()
                return result

        return result

    return wrapper
```

## 📊 Complete Example

```python
from typing import List, Optional
from typing_extensions import Annotated, TypedDict
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel, Field
import operator

# Define base state with TypedDict (LangGraph style)
class BaseState(TypedDict):
    messages: Annotated[List[str], operator.add]  # With reducer
    context: dict

# Build dynamic state
builder = TypedStateBuilder(BaseState)
builder.add_field("tool_calls", List[str], default_factory=list, reducer=operator.add)
builder.add_field("agent_state", dict, default_factory=dict)

# Create StateGraph with dynamic schema
DynamicState = builder.build_for_stategraph()
graph = StateGraph(DynamicState)

# Add nodes with type-safe Send/Command
def router_node(state: DynamicState) -> Union[str, LangGraphSend, LangGraphCommand]:
    """Router that uses typed Send/Command."""

    if state.get("needs_tool"):
        # Type-safe Send
        send = TypedSend("tool_node", {"query": state["messages"][-1]})
        return send.to_langgraph()

    if state.get("needs_revision"):
        # Type-safe Command
        cmd = TypedCommand(
            update={"messages": ["Revising..."]},
            goto="revision_node"
        )
        return cmd.to_langgraph()

    return END

def tool_node(state: dict) -> dict:
    """Tool execution node."""
    return {"tool_calls": ["Tool executed"]}

# Build graph
graph.add_node("router", router_node)
graph.add_node("tool_node", tool_node)
graph.add_edge(START, "router")
graph.add_edge("tool_node", END)

# Compile and run
compiled = graph.compile()
result = compiled.invoke({"messages": ["Hello"], "needs_tool": True})
```

## 🔑 Key Benefits

1. **Type Safety**: Full type checking for Send/Command at development time
2. **Runtime Validation**: Validates state types before routing
3. **LangGraph Compatible**: Works directly with LangGraph's actual types
4. **Dynamic Fields**: Add fields at runtime while maintaining type hints
5. **No String Checking**: Replace string-based type checking with proper isinstance

## 🎯 Migration Path

### Phase 1: Wrapper Implementation

```python
# Create typed wrappers for existing usage
send = TypedSend(node_name, state_data)
langgraph_send = send.to_langgraph()  # Use in LangGraph
```

### Phase 2: Update Validation Nodes

```python
# Update validation nodes to handle both typed and untyped
if isinstance(result, (TypedSend, LangGraphSend)):
    return result.to_langgraph() if hasattr(result, 'to_langgraph') else result
```

### Phase 3: Full Integration

```python
# Use typed versions throughout codebase
# Gradually replace string-based checking
```

## 📈 Performance Considerations

1. **Minimal Overhead**: Wrappers are thin, conversion is O(1)
2. **Type Caching**: Cache type information to avoid repeated validation
3. **Lazy Validation**: Only validate when necessary
4. **Direct LangGraph**: Can always fall back to direct LangGraph types

## ⚠️ Important Notes

1. LangGraph's `Send` and `Command` are designed for flexibility - our wrappers add optional type safety
2. The `to_langgraph()` pattern allows gradual migration
3. StateGraph's dynamic schema uses TypedDict and Annotated, not Pydantic models directly
4. Reducers are functions attached via Annotated, not class methods

## 🔗 Related Files

- `/home/will/Projects/haive/.venv/lib/python3.12/site-packages/langgraph/types.py` - LangGraph type definitions
- `/home/will/Projects/haive/.venv/lib/python3.12/site-packages/langgraph/graph/state.py` - StateGraph implementation
- `/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py` - Haive's BaseGraph2

---

**This solution provides type-safe wrappers around LangGraph's existing types while maintaining full compatibility with the LangGraph ecosystem.**
