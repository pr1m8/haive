# Practical Implementation Plan - Haive Architecture Redesign

**Created**: 2025-01-07  
**Purpose**: Actionable implementation plan for fixing core architecture issues  
**Status**: Ready for implementation

## 🎯 Executive Summary

After deep analysis of Haive's architecture and LangGraph's static constraints, here's the practical plan to fix the core issues:

1. **Fix type safety** - Replace string-based checking with proper isinstance
2. **Work within static constraints** - Use comprehensive schemas and factory patterns
3. **Establish clear contracts** - Formal relationships between components
4. **Optimize design** - Not just reduce complexity, but improve architecture

## 🔴 Priority 1: Fix Type Safety Issues

### Problem: String-Based Type Checking in BaseGraph2

**Current Code** (base_graph2.py):

```python
# WRONG - String-based type checking
if hasattr(result, "__class__") and "Command" in result.__class__.__name__:
    return result
```

### Solution: Type-Safe Wrapper Implementation

**File**: `/packages/haive-core/src/haive/core/graph/type_safe_routing.py`

```python
from typing import TypeVar, Generic, Type, Any, Union, Optional
from langgraph.types import Send as LangGraphSend, Command as LangGraphCommand
from pydantic import BaseModel

StateT = TypeVar('StateT', bound=BaseModel)

class TypedSend(Generic[StateT]):
    """Type-safe wrapper around LangGraph Send."""

    def __init__(self, node: str, arg: StateT):
        self.node = node
        self.arg = arg
        self._state_type: Type[StateT] = type(arg)
        self._send = LangGraphSend(node, arg.model_dump() if isinstance(arg, BaseModel) else arg)

    def to_langgraph(self) -> LangGraphSend:
        return self._send

    def validate_state(self, expected_type: Type) -> bool:
        return isinstance(self.arg, expected_type)

class TypedCommand(Generic[StateT]):
    """Type-safe wrapper around LangGraph Command."""

    def __init__(
        self,
        graph: Optional[str] = None,
        update: Optional[StateT] = None,
        resume: Optional[Any] = None,
        goto: Union[str, TypedSend[StateT], list] = ()
    ):
        self.graph = graph
        self.update = update
        self.resume = resume

        # Convert TypedSend to LangGraph Send
        if isinstance(goto, TypedSend):
            goto_langgraph = goto.to_langgraph()
        elif isinstance(goto, list):
            goto_langgraph = [
                g.to_langgraph() if isinstance(g, TypedSend) else g
                for g in goto
            ]
        else:
            goto_langgraph = goto

        self._command = LangGraphCommand(
            graph=graph,
            update=update.model_dump() if isinstance(update, BaseModel) else update,
            resume=resume,
            goto=goto_langgraph
        )

    def to_langgraph(self) -> LangGraphCommand:
        return self._command
```

### Fix BaseGraph2 Validation Wrapper

**File**: `/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py`

```python
def _create_validation_wrapper(self, validation_config, destination_map):
    """Enhanced validation wrapper with proper type checking."""
    from langgraph.types import Send, Command
    from haive.core.graph.type_safe_routing import TypedSend, TypedCommand

    def validation_wrapper(state, config=None):
        try:
            result = validation_config(state, config) if callable(validation_config) else validation_config

            # Proper type checking - no string matching!
            if isinstance(result, (LangGraphSend, Send)):
                logger.info(f"Validation returned Send to {result.node}")
                return result

            if isinstance(result, TypedSend):
                logger.info(f"Validation returned TypedSend to {result.node}")
                return result.to_langgraph()

            if isinstance(result, (LangGraphCommand, Command)):
                logger.info("Validation returned Command")
                return result

            if isinstance(result, TypedCommand):
                logger.info("Validation returned TypedCommand")
                return result.to_langgraph()

            if isinstance(result, str) and result in destination_map:
                return result

            # Handle list of Send objects
            if isinstance(result, list) and all(isinstance(item, (Send, TypedSend)) for item in result):
                return [item.to_langgraph() if isinstance(item, TypedSend) else item for item in result]

            logger.warning(f"Unexpected validation result type: {type(result)}")
            return None

        except Exception as e:
            logger.error(f"Validation error: {e}")
            raise

    return validation_wrapper
```

## 🟡 Priority 2: Work Within Static Constraints

### Problem: LangGraph Schemas Are Static

**Discovery**: LangGraph reads TypedDict `__annotations__` ONCE at graph creation and never updates.

### Solution: Comprehensive Schema Factory

**File**: `/packages/haive-core/src/haive/core/schema/schema_factory.py`

```python
from typing import Type, Dict, Any, List, Optional, get_type_hints
from typing_extensions import TypedDict, Annotated
from pydantic import BaseModel, create_model
import operator

class SchemaFactory:
    """Factory for creating comprehensive schemas at compile time."""

    # Pre-defined comprehensive base schema
    BASE_FIELDS = {
        "messages": (Annotated[List[Any], operator.add], ...),
        "context": (dict, {}),
        "metadata": (dict, {}),
        "engine_state": (dict, {}),
        "tool_calls": (Optional[List[dict]], None),
        "tool_results": (Optional[dict], None),
        "agent_state": (Optional[dict], None),
        "routing_history": (Optional[List[str]], None),
        "extensions": (dict, {}),  # For truly dynamic data
    }

    @classmethod
    def create_comprehensive_schema(
        cls,
        name: str = "ComprehensiveState",
        additional_fields: Dict[str, tuple[type, Any]] = None,
        use_pydantic: bool = False
    ) -> Type:
        """Create a comprehensive schema with all possible fields."""

        fields = {**cls.BASE_FIELDS}
        if additional_fields:
            fields.update(additional_fields)

        if use_pydantic:
            # Create Pydantic model
            return create_model(name, **fields)
        else:
            # Create TypedDict for LangGraph
            annotations = {k: v[0] for k, v in fields.items()}
            defaults = {k: v[1] for k, v in fields.items() if v[1] is not ...}

            # Create TypedDict class
            schema_class = type(name, (TypedDict,), {
                "__annotations__": annotations,
                **defaults
            })

            return schema_class

    @classmethod
    def create_agent_schema(cls, agent_type: str) -> Type:
        """Create schema variant for specific agent type."""

        agent_schemas = {
            "simple": {},
            "react": {
                "thought": (Optional[str], None),
                "action": (Optional[str], None),
                "observation": (Optional[str], None),
            },
            "rag": {
                "documents": (Optional[List[dict]], None),
                "query": (Optional[str], None),
                "retrieved_context": (Optional[str], None),
            },
            "planner": {
                "plan": (Optional[dict], None),
                "steps": (Optional[List[str]], None),
                "current_step": (Optional[int], 0),
            },
        }

        additional = agent_schemas.get(agent_type, {})
        return cls.create_comprehensive_schema(
            name=f"{agent_type.title()}AgentState",
            additional_fields=additional
        )
```

## 🟢 Priority 3: Establish Execution Contracts

### Problem: No Formal Relationship Between Components

### Solution: Contract-Based Architecture

**File**: `/packages/haive-core/src/haive/core/contracts/execution_contract.py`

```python
from abc import ABC, abstractmethod
from typing import Type, Dict, Any, Optional
from pydantic import BaseModel

class ExecutionContract(ABC):
    """Formal contract between engine, node, and state."""

    @abstractmethod
    def validate_state(self, state: BaseModel) -> bool:
        """Validate state meets contract requirements."""
        pass

    @abstractmethod
    def transform_input(self, state: BaseModel) -> Dict[str, Any]:
        """Transform state to engine input format."""
        pass

    @abstractmethod
    def transform_output(self, output: Any, state: BaseModel) -> BaseModel:
        """Transform engine output back to state format."""
        pass

class EngineStateContract(ExecutionContract):
    """Contract linking engine requirements to state schema."""

    def __init__(
        self,
        engine_type: str,
        required_fields: List[str],
        output_fields: List[str]
    ):
        self.engine_type = engine_type
        self.required_fields = required_fields
        self.output_fields = output_fields

    def validate_state(self, state: BaseModel) -> bool:
        """Ensure state has required fields for engine."""
        state_dict = state.model_dump() if hasattr(state, 'model_dump') else dict(state)
        return all(field in state_dict for field in self.required_fields)

    def transform_input(self, state: BaseModel) -> Dict[str, Any]:
        """Extract only required fields for engine."""
        state_dict = state.model_dump() if hasattr(state, 'model_dump') else dict(state)
        return {field: state_dict.get(field) for field in self.required_fields}

    def transform_output(self, output: Any, state: BaseModel) -> BaseModel:
        """Merge engine output back into state."""
        state_dict = state.model_dump() if hasattr(state, 'model_dump') else dict(state)

        if isinstance(output, dict):
            for field in self.output_fields:
                if field in output:
                    state_dict[field] = output[field]

        return type(state)(**state_dict)
```

## 🔵 Priority 4: Engine Injection Pattern

### Problem: Engines Not Properly Integrated with State

### Solution: Engine-Aware State Management

**File**: `/packages/haive-core/src/haive/core/engine/injection.py`

```python
from typing import Type, Dict, Any, Optional
from pydantic import BaseModel

class EngineInjector:
    """Manages engine injection into state schemas."""

    def __init__(self):
        self.engine_registry: Dict[str, Any] = {}
        self.contracts: Dict[str, ExecutionContract] = {}

    def register_engine(
        self,
        name: str,
        engine: Any,
        contract: ExecutionContract
    ):
        """Register an engine with its contract."""
        self.engine_registry[name] = engine
        self.contracts[name] = contract

    def inject_into_state(
        self,
        state: BaseModel,
        engine_name: str
    ) -> BaseModel:
        """Inject engine capabilities into state."""

        if engine_name not in self.engine_registry:
            raise ValueError(f"Engine {engine_name} not registered")

        engine = self.engine_registry[engine_name]
        contract = self.contracts[engine_name]

        # Validate state meets contract
        if not contract.validate_state(state):
            raise ValueError(f"State doesn't meet {engine_name} contract")

        # Add engine reference to state
        state_dict = state.model_dump() if hasattr(state, 'model_dump') else dict(state)
        state_dict['engine_state'][engine_name] = {
            'type': type(engine).__name__,
            'contract': contract.__class__.__name__,
            'ready': True
        }

        return type(state)(**state_dict)

    def execute_with_contract(
        self,
        engine_name: str,
        state: BaseModel
    ) -> BaseModel:
        """Execute engine with contract transformation."""

        engine = self.engine_registry[engine_name]
        contract = self.contracts[engine_name]

        # Transform state to engine input
        engine_input = contract.transform_input(state)

        # Execute engine
        output = engine.invoke(engine_input)

        # Transform output back to state
        return contract.transform_output(output, state)
```

## 🟣 Priority 5: Multi-Agent State Coordination

### Problem: No Clear Pattern for Agent Communication

### Solution: Hierarchical State Management

**File**: `/packages/haive-core/src/haive/core/multi/state_coordinator.py`

```python
class StateCoordinator:
    """Coordinates state between multiple agents."""

    def __init__(self):
        self.agent_states: Dict[str, BaseModel] = {}
        self.shared_state: Dict[str, Any] = {}
        self.transfer_rules: Dict[tuple[str, str], Dict[str, str]] = {}

    def register_agent(
        self,
        agent_name: str,
        state_schema: Type[BaseModel],
        initial_state: Optional[BaseModel] = None
    ):
        """Register an agent with the coordinator."""
        if initial_state:
            self.agent_states[agent_name] = initial_state
        else:
            self.agent_states[agent_name] = state_schema()

    def add_transfer_rule(
        self,
        from_agent: str,
        to_agent: str,
        field_mapping: Dict[str, str]
    ):
        """Add rule for transferring data between agents."""
        self.transfer_rules[(from_agent, to_agent)] = field_mapping

    def transfer_state(
        self,
        from_agent: str,
        to_agent: str
    ) -> BaseModel:
        """Transfer state from one agent to another."""

        if (from_agent, to_agent) not in self.transfer_rules:
            # No specific rules, transfer shared fields only
            return self.agent_states[to_agent]

        rules = self.transfer_rules[(from_agent, to_agent)]
        from_state = self.agent_states[from_agent]
        to_state = self.agent_states[to_agent]

        from_dict = from_state.model_dump() if hasattr(from_state, 'model_dump') else dict(from_state)
        to_dict = to_state.model_dump() if hasattr(to_state, 'model_dump') else dict(to_state)

        # Apply transfer rules
        for from_field, to_field in rules.items():
            if from_field in from_dict:
                to_dict[to_field] = from_dict[from_field]

        # Update shared state
        to_dict.update(self.shared_state)

        updated_state = type(to_state)(**to_dict)
        self.agent_states[to_agent] = updated_state

        return updated_state
```

## 📋 Implementation Timeline

### Week 1: Type Safety

- [ ] Implement TypedSend and TypedCommand wrappers
- [ ] Fix BaseGraph2 validation wrapper
- [ ] Add proper isinstance checks throughout
- [ ] Test with real LangGraph integration

### Week 2: Schema Management

- [ ] Build SchemaFactory with comprehensive base schemas
- [ ] Create agent-specific schema variants
- [ ] Implement schema caching for performance
- [ ] Test with different agent types

### Week 3: Contracts

- [ ] Implement ExecutionContract base class
- [ ] Create EngineStateContract
- [ ] Add contract validation to nodes
- [ ] Test contract enforcement

### Week 4: Engine Integration

- [ ] Build EngineInjector
- [ ] Register all existing engines
- [ ] Add injection to agent initialization
- [ ] Test engine execution with contracts

### Week 5: Multi-Agent

- [ ] Implement StateCoordinator
- [ ] Add transfer rules for common patterns
- [ ] Test sequential agent execution
- [ ] Test parallel agent coordination

## 🎯 Success Metrics

1. **Type Safety**: Zero string-based type checks
2. **Performance**: <10ms overhead for contract validation
3. **Reliability**: 100% test coverage with real components
4. **Maintainability**: 50% reduction in debugging time
5. **Flexibility**: Support for any agent combination

## 🔧 Migration Strategy

### Phase 1: Add New Components (Non-Breaking)

1. Add TypedSend/TypedCommand alongside existing
2. Add SchemaFactory without removing old schemas
3. Add contracts as optional enhancement

### Phase 2: Gradual Migration

1. Update one agent at a time to use new patterns
2. Keep backward compatibility layer
3. Add deprecation warnings

### Phase 3: Clean Up

1. Remove string-based type checking
2. Remove old schema patterns
3. Make contracts mandatory

## 🚀 Quick Wins

1. **Fix BaseGraph2 type checking** - 1 day, high impact
2. **Add TypedSend/Command** - 2 days, improves safety
3. **Create base comprehensive schema** - 1 day, enables progress
4. **Add simple contract validation** - 2 days, catches errors early

## 📚 Related Documentation

- [LangGraph Static Analysis](./LANGGRAPH_STATIC_ANALYSIS.md)
- [Complete Architecture Analysis](./COMPLETE_ARCHITECTURE_ANALYSIS.md)
- [Unified Contract Architecture](./UNIFIED_CONTRACT_ARCHITECTURE.md)
- [LangGraph Integration Solution](./LANGGRAPH_INTEGRATION_SOLUTION.md)

---

**Next Steps**: Start with Priority 1 - Fix type safety issues in BaseGraph2. This is a quick win that will immediately improve reliability.
