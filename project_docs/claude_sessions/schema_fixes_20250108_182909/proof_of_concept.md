# Proof of Concept Implementation Plan

## Goal
Create a minimal but complete implementation that validates the new architecture without breaking existing code.

## POC Components

### 1. Enhanced Engine with Optional State Type

```python
# haive/core/engine/base/typed_engine.py
from typing import Optional, Type, TypeVar, Generic
from pydantic import BaseModel, PrivateAttr

TState = TypeVar("TState", bound=BaseModel)

class TypedEngine(Engine, Generic[TState]):
    """Engine that can optionally know its state type."""
    
    # Optional state type for gradual migration
    _state_type: Optional[Type[TState]] = PrivateAttr(default=None)
    
    def with_state_type(self, state_type: Type[TState]) -> "TypedEngine[TState]":
        """Set the state type for this engine."""
        self._state_type = state_type
        return self
    
    def validate_state_compatibility(self, state: BaseModel) -> bool:
        """Check if given state is compatible with engine requirements."""
        if not self._state_type:
            return True  # No type set, assume compatible
            
        # Check if state has required fields
        required_fields = self.get_input_fields()
        for field_name in required_fields:
            if not hasattr(state, field_name):
                return False
        return True
```

### 2. Hierarchical State Prototype

```python
# haive/core/schema/multi_agent/hierarchical_state.py
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class AgentView(BaseModel):
    """View of state from a single agent's perspective."""
    agent_name: str
    shared: Dict[str, Any]  # Read-only shared fields
    private: Dict[str, Any]  # Agent's private fields
    
    def get_messages(self) -> List[BaseMessage]:
        """Safe access to shared messages."""
        return self.shared.get("messages", [])
    
    def add_message(self, message: BaseMessage) -> None:
        """Add message with agent attribution."""
        message.metadata = message.metadata or {}
        message.metadata["agent"] = self.agent_name
        self.shared["messages"].append(message)

class HierarchicalState(BaseModel):
    """POC hierarchical state."""
    shared: Dict[str, Any] = Field(default_factory=dict)
    agents: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    routing: Dict[str, Any] = Field(default_factory=dict)
    
    def create_agent_view(self, agent_name: str) -> AgentView:
        """Create isolated view for agent."""
        if agent_name not in self.agents:
            self.agents[agent_name] = {}
            
        return AgentView(
            agent_name=agent_name,
            shared=self.shared,  # TODO: Make read-only proxy
            private=self.agents[agent_name]
        )
```

### 3. Enhanced Schema Composer

```python
# haive/core/schema/composer/typed_composer.py
class TypedSchemaComposer:
    """Schema composer that uses type information."""
    
    def __init__(self):
        self.shared_fields: Dict[str, FieldDefinition] = {}
        self.agent_fields: Dict[str, Dict[str, FieldDefinition]] = {}
        self.engines: List[TypedEngine] = []
        
    def add_engine(self, engine: TypedEngine, agent_name: Optional[str] = None):
        """Add engine with optional agent assignment."""
        self.engines.append(engine)
        
        # Extract fields
        input_fields = engine.get_input_fields()
        output_fields = engine.get_output_fields()
        
        # If engine has state type, validate compatibility
        if hasattr(engine, '_state_type') and engine._state_type:
            self._validate_state_compatibility(engine._state_type, input_fields)
            
        # Add fields to appropriate collection
        if agent_name:
            self._add_agent_fields(agent_name, input_fields, output_fields)
        else:
            self._add_shared_fields(input_fields, output_fields)
            
    def compose(self) -> Type[BaseModel]:
        """Compose final schema."""
        if self.agent_fields:
            # Multi-agent hierarchical
            return self._compose_hierarchical()
        else:
            # Single agent flat
            return self._compose_flat()
```

### 4. Migration Adapter

```python
# haive/core/schema/migration/adapter.py
class StateAdapter:
    """Adapts between old flat states and new hierarchical states."""
    
    @staticmethod
    def flat_to_hierarchical(
        flat_state: Dict[str, Any],
        agent_mappings: Dict[str, List[str]]
    ) -> HierarchicalState:
        """Convert flat state to hierarchical.
        
        Args:
            flat_state: Traditional flat state dict
            agent_mappings: Map of agent_name -> list of field names
        """
        hierarchical = HierarchicalState()
        
        # Determine shared fields (not in any agent mapping)
        all_agent_fields = set()
        for fields in agent_mappings.values():
            all_agent_fields.update(fields)
            
        for key, value in flat_state.items():
            if key not in all_agent_fields:
                # Shared field
                hierarchical.shared[key] = value
            else:
                # Find owning agent
                for agent_name, fields in agent_mappings.items():
                    if key in fields:
                        if agent_name not in hierarchical.agents:
                            hierarchical.agents[agent_name] = {}
                        hierarchical.agents[agent_name][key] = value
                        break
                        
        return hierarchical
```

## Testing Strategy

### Test 1: Backward Compatibility
```python
def test_legacy_engine_still_works():
    """Ensure old engines work without modification."""
    # Create legacy engine
    engine = AugLLMConfig(name="test")
    
    # Should work as before
    fields = engine.get_input_fields()
    assert "messages" in fields
    
    # No state type required
    assert engine.create_runnable() is not None
```

### Test 2: Typed Engine Benefits
```python
def test_typed_engine_validation():
    """Test that typed engines provide validation."""
    # Define state type
    class MyState(BaseModel):
        messages: List[BaseMessage]
        context: str
        
    # Create typed engine
    engine = TypedAugLLMConfig().with_state_type(MyState)
    
    # Validate compatible state
    good_state = MyState(messages=[], context="test")
    assert engine.validate_state_compatibility(good_state)
    
    # Validate incompatible state
    class BadState(BaseModel):
        wrong_field: str
        
    bad_state = BadState(wrong_field="test")
    assert not engine.validate_state_compatibility(bad_state)
```

### Test 3: Multi-Agent Isolation
```python
def test_multi_agent_isolation():
    """Test that agents have isolated state."""
    state = HierarchicalState()
    
    # Agent 1 view
    view1 = state.create_agent_view("agent1")
    view1.private["my_data"] = "agent1_data"
    
    # Agent 2 view  
    view2 = state.create_agent_view("agent2")
    view2.private["my_data"] = "agent2_data"
    
    # Data is isolated
    assert view1.private["my_data"] == "agent1_data"
    assert view2.private["my_data"] == "agent2_data"
    
    # But shared is shared
    view1.shared["global"] = "shared_data"
    assert view2.shared["global"] == "shared_data"
```

## Implementation Timeline

### Week 1: Core Components
- [ ] Implement TypedEngine base class
- [ ] Create HierarchicalState prototype
- [ ] Build StateAdapter for migration
- [ ] Write comprehensive tests

### Week 2: Integration
- [ ] Update SchemaComposer to use type info
- [ ] Create TypedAugLLMConfig example
- [ ] Test with SimpleAgent
- [ ] Document migration path

### Week 3: Multi-Agent
- [ ] Update SequentialAgent to use hierarchical state
- [ ] Implement proper state isolation
- [ ] Test with self-discover example
- [ ] Performance benchmarks

### Week 4: Polish
- [ ] Complete documentation
- [ ] Migration tools
- [ ] More examples
- [ ] Community feedback

## Success Criteria

1. **No Breaking Changes**: All existing code continues to work
2. **Opt-in Type Safety**: New features are optional
3. **Better Multi-Agent**: Clear improvement in multi-agent scenarios
4. **Performance**: No significant performance degradation
5. **Developer Experience**: Easier to understand and debug