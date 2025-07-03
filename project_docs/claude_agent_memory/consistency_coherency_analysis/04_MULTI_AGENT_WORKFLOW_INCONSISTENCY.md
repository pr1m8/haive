# Multi-Agent Workflow Inconsistency Analysis

## Three Incompatible Multi-Agent Patterns

### Pattern A: MultiAgent (Gold Standard)

**Location**: `packages/haive-agents/src/haive/agents/multi/base.py`

```python
class MultiAgent(Agent):
    """Sophisticated schema composition with AgentSchemaComposer"""

    def __init__(self, agents: list[Agent], **kwargs):
        # Uses AgentSchemaComposer for intelligent field handling
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agents,
            separation="smart",  # Field conflict resolution
            build_mode=BuildMode.PARALLEL,
            include_meta=True
        )
```

**Features**:

- ✅ AgentSchemaComposer with field separation strategies
- ✅ preserve_messages_reducer for tool_call_id preservation
- ✅ Engine I/O mapping preservation
- ✅ Private state tracking per agent
- ✅ BuildMode support (PARALLEL, SEQUENCE, HIERARCHICAL)

### Pattern B: ChainAgent (Broken)

**Location**: `packages/haive-agents/src/haive/agents/chain/`

```python
class ChainAgent(Agent):
    """Manual data passing, NO schema composition"""

    def __init__(self, engines: list[AugLLMConfig], **kwargs):
        # Uses engines directly, not agents
        # NO schema composition
        # Manual data passing through chain_data dict
```

**Problems**:

- ❌ No schema composition at all
- ❌ Manual data passing via chain_data
- ❌ No tool_call_id preservation
- ❌ No field mapping between steps
- ❌ Operates at engine level, not agent level

### Pattern C: SequentialAgent (Mixed Approach)

**Location**: Various RAG implementations

```python
class SequentialAgent(Agent):
    """Uses AgentSchemaComposer but different patterns"""

    @classmethod
    def from_agents(cls, agents: list[Agent], **kwargs):
        # Good: Uses AgentSchemaComposer
        return cls(
            agents=agents,
            schema_separation="shared",  # Different default
            execution_mode="sequential"
        )
```

**Issues**:

- ⚠️ Different default separation strategy than MultiAgent
- ⚠️ Different execution mode handling
- ⚠️ Inconsistent class method signatures
- ⚠️ Some versions bypass AgentSchemaComposer entirely

## Consistency Problems

### 1. **Different Base Classes**

```python
# Pattern inconsistency:
MultiAgent(Agent)           # Direct inheritance
ChainAgent(Agent)          # Direct inheritance
SequentialAgent(Agent)     # Sometimes inherits from MultiAgent
```

**Should be**:

```python
# Unified base class:
class MultiAgentBase(Agent):
    """Common functionality for all multi-agent patterns"""

class MultiAgent(MultiAgentBase):      # Parallel execution
class ChainAgent(MultiAgentBase):      # Sequential execution
class SequentialAgent(MultiAgentBase): # Linear execution
```

### 2. **Incompatible Constructor Signatures**

```python
# Inconsistent initialization:
MultiAgent(agents=[], separation="smart", build_mode=BuildMode.PARALLEL)
ChainAgent(engines=[], chain_data={})  # Uses engines, not agents!
SequentialAgent.from_agents(agents=[], execution_mode="sequential")
```

**Should be**:

```python
# Unified constructor pattern:
MultiAgent(agents=[], execution_pattern="parallel", **kwargs)
ChainAgent(agents=[], execution_pattern="chain", **kwargs)
SequentialAgent(agents=[], execution_pattern="sequential", **kwargs)
```

### 3. **Different Schema Composition Approaches**

```python
# MultiAgent: Sophisticated composition
AgentSchemaComposer.from_agents(separation="smart", build_mode=BuildMode.PARALLEL)

# ChainAgent: No composition
DynamicGraph(components=engines)  # Wrong abstraction level

# SequentialAgent: Basic composition
AgentSchemaComposer.from_agents(separation="shared")  # Different defaults
```

### 4. **Inconsistent Execution Patterns**

```python
# MultiAgent: Graph-based with router
def build_graph(self) -> BaseGraph:
    # Sophisticated routing logic
    # Support for parallel execution
    # Agent coordination fields

# ChainAgent: Linear engine chain
def setup_workflow(self):
    # Manual step-by-step execution
    # No agent coordination
    # Engine-level operations

# SequentialAgent: Agent sequence
def build_graph(self) -> BaseGraph:
    # Simple linear agent execution
    # Basic state passing
```

## Proposed Unified Architecture

### 1. **Common Base Class**

```python
class MultiAgentBase(Agent):
    """Unified base for all multi-agent workflows"""

    agents: list[Agent] = Field(...)
    execution_pattern: ExecutionPattern = Field(...)
    separation_strategy: str = Field(default="smart")

    def __init__(self, agents: list[Agent], **kwargs):
        # Validate all components are actual agents
        for agent in agents:
            if not isinstance(agent, Agent):
                raise TypeError(f"{agent} must be an Agent instance")

        # Use AgentSchemaComposer for ALL multi-agent patterns
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agents,
            separation=self.separation_strategy,
            build_mode=self._get_build_mode(),
            include_meta=True
        )

        super().__init__(**kwargs)

    @abstractmethod
    def _get_build_mode(self) -> BuildMode:
        """Each pattern defines its build mode"""
        pass

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Each pattern implements its execution logic"""
        pass
```

### 2. **Specialized Implementations**

```python
class ParallelMultiAgent(MultiAgentBase):
    """Parallel agent execution with aggregation"""
    execution_pattern: Literal["parallel"] = "parallel"

    def _get_build_mode(self) -> BuildMode:
        return BuildMode.PARALLEL

    def build_graph(self) -> BaseGraph:
        # Implement parallel execution pattern
        # Use router for agent selection
        # Aggregate results

class SequentialMultiAgent(MultiAgentBase):
    """Sequential agent execution"""
    execution_pattern: Literal["sequential"] = "sequential"

    def _get_build_mode(self) -> BuildMode:
        return BuildMode.SEQUENCE

    def build_graph(self) -> BaseGraph:
        # Implement sequential execution pattern
        # Linear agent chain
        # State threading between agents

class ChainMultiAgent(MultiAgentBase):
    """Chain agent execution with field mapping"""
    execution_pattern: Literal["chain"] = "chain"

    def _get_build_mode(self) -> BuildMode:
        return BuildMode.SEQUENCE

    def build_graph(self) -> BaseGraph:
        # Fixed ChainAgent with proper schema composition
        # Use AgentSchemaComposer field mappings
        # Preserve tool_call_id through chain
```

### 3. **Unified Factory Pattern**

```python
class MultiAgentFactory:
    """Factory for creating multi-agent workflows"""

    @staticmethod
    def create_parallel(agents: list[Agent], **kwargs) -> ParallelMultiAgent:
        return ParallelMultiAgent(agents=agents, **kwargs)

    @staticmethod
    def create_sequential(agents: list[Agent], **kwargs) -> SequentialMultiAgent:
        return SequentialMultiAgent(agents=agents, **kwargs)

    @staticmethod
    def create_chain(agents: list[Agent], **kwargs) -> ChainMultiAgent:
        return ChainMultiAgent(agents=agents, **kwargs)

    @staticmethod
    def auto_select(agents: list[Agent], **kwargs) -> MultiAgentBase:
        """Auto-select best pattern based on agent I/O compatibility"""
        compatibility = AgentSchemaComposer._analyze_agent_compatibility(agents)

        if compatibility.suggests_parallel:
            return MultiAgentFactory.create_parallel(agents, **kwargs)
        elif compatibility.suggests_chain:
            return MultiAgentFactory.create_chain(agents, **kwargs)
        else:
            return MultiAgentFactory.create_sequential(agents, **kwargs)
```

## Migration Strategy

### Phase 1: Create Unified Base

1. Implement `MultiAgentBase` with common functionality
2. Ensure all patterns use `AgentSchemaComposer`
3. Standardize constructor signatures

### Phase 2: Fix ChainAgent

1. Update ChainAgent to use agents instead of engines
2. Implement proper schema composition
3. Add tool_call_id preservation

### Phase 3: Consolidate Patterns

1. Migrate existing MultiAgent to ParallelMultiAgent
2. Migrate RAG SequentialAgent usage
3. Update documentation and examples

### Phase 4: Factory Integration

1. Provide factory methods for common patterns
2. Add auto-selection based on agent compatibility
3. Deprecate old inconsistent constructors

## Benefits

### 1. **Consistency**

- All multi-agent patterns use same base class
- Unified constructor and configuration approach
- Consistent schema composition across patterns

### 2. **Reliability**

- All patterns get tool_call_id preservation
- Proper field mapping and conflict resolution
- Validated agent composition

### 3. **Maintainability**

- Single codebase for multi-agent functionality
- Shared testing patterns
- Easier to add new execution patterns

### 4. **Developer Experience**

- Clear pattern selection guidance
- Consistent API across all multi-agent types
- Auto-selection reduces decision complexity

This unified architecture resolves the current inconsistency and provides a solid foundation for multi-agent workflows.
