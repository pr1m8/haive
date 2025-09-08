# StateSchema Redesign - Breaking Down the Monolith

**Created**: 2025-01-06
**Purpose**: Redesign StateSchema to follow Single Responsibility Principle
**Status**: Brainstorming & Design Phase

## 🚨 Current Problems with StateSchema

### The Bloat Issue

StateSchema currently has **60+ methods** and tries to be:

1. A data container (Pydantic BaseModel)
2. An engine manager (add_engine, get_engine, remove_engine)
3. A message handler (add_message, clear_messages, merge_messages)
4. A serialization system (to_dict, from_dict, to_json, from_json)
5. A state merger (apply_reducers, update, merge)
6. A field manager (shared_fields, derive_input_schema, derive_output_schema)
7. A graph integration point (field sharing with parent/child)
8. A dirty tracking system (needs but doesn't have)
9. A dynamic field system (needs but doesn't have proper support)

**This is too much for one class!**

## 🎯 Core Requirements

What does a StateSchema ACTUALLY need to do?

### 1. **Hold Data for Nodes**

- Be a container that nodes can pass around
- Support type safety and validation
- Be serializable for persistence/network

### 2. **Track Changes (Dirty Tracking)**

- Know which fields have changed
- Support undo/redo potentially
- Enable efficient updates (only send changed fields)

### 3. **Dynamic Field Addition**

- Add fields at runtime based on needs
- Remove fields that are no longer needed
- Type-safe field operations

### 4. **Define Engine I/O**

- Specify what fields an engine needs as input
- Specify what fields an engine produces as output
- But NOT manage the engines themselves

### 5. **Support Field Merging**

- Define HOW fields should be merged (reducers)
- But not necessarily DO the merging itself

## 💡 Proposed Architecture: Separation of Concerns

### Core Principle: Composition Over Inheritance

Instead of one mega-class, break into focused components:

```python
# 1. Pure Data Container
class StateData(BaseModel):
    """Just the data, nothing else"""
    pass

# 2. Field Metadata (separate from data)
class FieldMetadata:
    """Describes a field without holding its value"""
    name: str
    type: Type
    is_shared: bool = False
    reducer: Optional[Callable] = None
    dirty: bool = False
    source: Optional[str] = None

# 3. State Manager (orchestrates everything)
class StateManager:
    """Manages state without BEING the state"""
    data: StateData
    metadata: Dict[str, FieldMetadata]
    dirty_fields: Set[str]

    def mark_dirty(self, field: str): ...
    def add_field(self, name: str, type: Type, value: Any): ...
    def remove_field(self, name: str): ...
    def get_dirty_fields(self): ...
    def clear_dirty(self): ...

# 4. Engine I/O Spec (separate concern)
class EngineIOSpec:
    """Defines what an engine needs/produces"""
    engine_name: str
    inputs: List[str]
    outputs: List[str]

# 5. Reducer Registry (separate concern)
class ReducerRegistry:
    """Central place for merge strategies"""
    strategies: Dict[str, Callable]

    def register(self, name: str, reducer: Callable): ...
    def get_reducer(self, field_name: str): ...
    def merge(self, field: str, old_val: Any, new_val: Any): ...
```

## 🏗️ Detailed Design

### 1. State Container Pattern

```python
@dataclass
class State:
    """Pure data container - no logic"""
    # User fields added dynamically
    __data__: Dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name):
        return self.__data__.get(name)

    def __setattr__(self, name, value):
        if name != '__data__':
            self.__data__[name] = value
            # Notify observers of change
```

### 2. Dirty Tracking System

```python
class DirtyTracker:
    """Tracks field changes"""
    def __init__(self):
        self._dirty_fields: Set[str] = set()
        self._change_history: List[FieldChange] = []

    def mark_dirty(self, field: str, old_value: Any, new_value: Any):
        self._dirty_fields.add(field)
        self._change_history.append(
            FieldChange(field, old_value, new_value, timestamp=now())
        )

    def get_changes_since(self, timestamp: datetime) -> List[FieldChange]:
        return [c for c in self._change_history if c.timestamp > timestamp]

    def clear(self):
        self._dirty_fields.clear()
        self._change_history.clear()
```

### 3. Dynamic Field System

```python
class FieldManager:
    """Manages dynamic fields"""
    def __init__(self):
        self.fields: Dict[str, FieldDefinition] = {}

    def add_field(self, name: str, type: Type, default: Any = None):
        """Add a new field at runtime"""
        self.fields[name] = FieldDefinition(
            name=name,
            type=type,
            default=default,
            added_at=now()
        )

    def remove_field(self, name: str):
        """Remove a field"""
        if name in self.fields:
            del self.fields[name]

    def validate_field(self, name: str, value: Any) -> bool:
        """Type check a field value"""
        if name not in self.fields:
            return False
        expected_type = self.fields[name].type
        return isinstance(value, expected_type)
```

### 4. Engine I/O Definition (Declarative)

```python
class EngineSpec:
    """Declarative engine I/O specification"""
    def __init__(self, name: str):
        self.name = name
        self.inputs: Set[str] = set()
        self.outputs: Set[str] = set()
        self.validators: Dict[str, Callable] = {}

    def requires(self, *fields: str) -> 'EngineSpec':
        """Declare required inputs"""
        self.inputs.update(fields)
        return self

    def produces(self, *fields: str) -> 'EngineSpec':
        """Declare outputs"""
        self.outputs.update(fields)
        return self

    def validate_input(self, state: State) -> List[str]:
        """Check if state has required fields"""
        missing = []
        for field in self.inputs:
            if not hasattr(state, field):
                missing.append(field)
        return missing
```

### 5. Composition Strategy

```python
class StateComposer:
    """Handles state composition with strategies"""

    def __init__(self):
        self.strategies: Dict[str, MergeStrategy] = {
            'replace': ReplaceStrategy(),
            'concat': ConcatStrategy(),
            'merge': MergeStrategy(),
            'custom': CustomStrategy()
        }

    def compose(
        self,
        state1: State,
        state2: State,
        field_strategies: Dict[str, str]
    ) -> State:
        """Compose two states with field-specific strategies"""
        result = State()

        # Get all fields from both states
        all_fields = set(state1.__data__.keys()) | set(state2.__data__.keys())

        for field in all_fields:
            strategy_name = field_strategies.get(field, 'replace')
            strategy = self.strategies[strategy_name]

            val1 = state1.__data__.get(field)
            val2 = state2.__data__.get(field)

            result.__data__[field] = strategy.merge(val1, val2)

        return result
```

## 🔄 Integration with Nodes

### How Nodes Would Use This

```python
class MyNode:
    def __init__(self):
        # Declare what this node needs/produces
        self.engine_spec = EngineSpec("my_node") \
            .requires("input_text", "context") \
            .produces("output_text", "metadata")

        # Track changes
        self.dirty_tracker = DirtyTracker()

    async def process(self, state: State) -> State:
        # Validate inputs
        missing = self.engine_spec.validate_input(state)
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        # Process
        input_text = state.input_text
        context = state.context

        # Do work...
        output_text = await self.generate(input_text, context)

        # Update state
        state.output_text = output_text
        state.metadata = {"processed_at": now()}

        # Track changes
        self.dirty_tracker.mark_dirty("output_text", None, output_text)
        self.dirty_tracker.mark_dirty("metadata", None, state.metadata)

        return state
```

## 🎯 Benefits of This Design

### 1. **Single Responsibility**

- Each class has ONE job
- Easy to understand and test
- Clear boundaries

### 2. **Composable**

- Mix and match components as needed
- Don't need all features for simple cases
- Can extend without modifying core

### 3. **Testable**

- Each component can be tested in isolation
- No global state issues
- Clear mocking boundaries

### 4. **Performance**

- Only pay for what you use
- Dirty tracking enables efficient updates
- No deep inheritance chains

### 5. **Type Safety**

- Can maintain type safety with dynamic fields
- Runtime validation where needed
- Clear contracts

## 📋 Migration Strategy

### Phase 1: Create New Components

- Build new components alongside existing StateSchema
- No breaking changes initially

### Phase 2: Adapter Layer

- Create adapters to convert between old and new
- Gradual migration of nodes

### Phase 3: Deprecate Old System

- Mark old StateSchema as deprecated
- Provide migration guide
- Remove in major version

## 🤔 Open Questions

1. **Persistence**: How do we serialize/deserialize efficiently?
2. **Validation**: Should we use Pydantic or custom validation?
3. **Performance**: Impact of dynamic field access?
4. **Backwards Compatibility**: How much do we preserve?
5. **Node Migration**: How to help users migrate?

## 🚀 Next Steps

1. **Prototype Core Components**
   - Build State, DirtyTracker, FieldManager
   - Test with simple examples

2. **Benchmark Performance**
   - Compare with current StateSchema
   - Measure memory usage
   - Test with large states

3. **Design Review**
   - Get feedback on architecture
   - Identify missing requirements
   - Refine design

4. **Implementation Plan**
   - Define implementation phases
   - Set migration timeline
   - Create documentation

## 📝 Design Principles

1. **Composition over Inheritance**
2. **Explicit over Implicit**
3. **Simple over Clever**
4. **Testable from Day One**
5. **Performance Matters**
6. **Type Safety Where Possible**
7. **Clear Error Messages**
8. **Progressive Enhancement**

---

**Key Insight**: The current StateSchema tries to be everything to everyone. By breaking it down into focused, composable components, we can build a more maintainable, testable, and performant system.
