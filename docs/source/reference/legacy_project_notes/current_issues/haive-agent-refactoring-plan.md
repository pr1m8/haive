# Haive Agent Architecture Refactoring Plan

## Executive Summary

The Haive agent architecture has evolved organically, resulting in several architectural inconsistencies and technical debt. This document outlines all identified issues, analyzes their root causes, and proposes a comprehensive refactoring plan to create a more maintainable, consistent, and extensible agent system.

## Current State Analysis

### 1. Engine Management Issues

#### 1.1 The `engine` vs `engines` Problem

- **Current State**: Agents have both `engine: Optional[Engine]` and `engines: Dict[str, Engine]`
- **Problems**:
  - Unclear relationship between the two fields
  - Redundant storage (same engine in both places)
  - Inconsistent usage across agent types
  - Complex normalization logic that tries to sync them

#### 1.2 Multiple Engine Scenarios

- Some agents need multiple engines (RAG needs retriever + LLM)
- No clear pattern for primary vs supporting engines
- Field syncing only works with single engine

### 2. Schema Generation Problems

#### 2.1 State Schema Generation

- **Current Approach**: `_setup_schemas()` tries to generate from engines
- **Issues**:
  - Complex logic with multiple code paths
  - Different behavior for agents vs engines
  - Schema modification happens in multiple places
  - No clear ownership of schema generation

#### 2.2 Input/Output Schema Derivation

- `_auto_derive_io_schemas()` is overly complex
- Special cases for structured output, tool parsing, etc.
- No consistent pattern for what fields belong in input vs output
- Output schema especially problematic with structured output models

#### 2.3 Structured Output Handling

- **Critical Issue**: SimpleAgent modifies engine's output schema directly
- This is a hack that:
  - Mutates shared engine instances
  - Breaks encapsulation
  - Makes testing difficult
  - Doesn't compose well

### 3. Field Synchronization

#### 3.1 Current Manual Approach

```python
def _sync_fields_to_engine(self):
    if self.temperature is not None:
        self.engine.temperature = self.temperature
    # ... repeat for each field
```

#### 3.2 Problems

- No bidirectional syncing
- Each agent reimplements this
- No standard list of syncable fields
- Doesn't work with multiple engines

### 4. Tool Management Chaos

#### 4.1 Multiple Tool Sources

- Tools can come from:
  - Engine's tools list
  - State schema's tools field
  - Agent's tools field
  - Class-level engines in state schema

#### 4.2 Tool Routing Complexity

- Tool routes scattered across multiple components
- No clear ownership model
- Synchronization issues between sources

### 5. Output Processing Pipeline

#### 5.1 Current State

- No unified output processing
- Structured output handled differently than output parsers
- Each agent type has different logic
- OutputParserNodeConfig exists but isn't integrated

#### 5.2 Problems

- Can't easily combine structured output + output parser
- No clear transformation pipeline
- Output schema doesn't reflect transformations

### 6. Configuration Management

#### 6.1 Multiple Configuration Systems

- `LLMConfig` at engine level
- `runnable_config` at runtime
- `AgentConfig` for agent setup
- Field-level config (temperature, max_tokens, etc.)

#### 6.2 No Hierarchical Configuration

- Can't configure all engines from agent level
- No config inheritance
- Runtime config doesn't flow properly

### 7. Architectural Inconsistencies

#### 7.1 Agent Type Differences

- SimpleAgent: Modifies engine schema, uses single engine
- ReactAgent: Inherits SimpleAgent but changes graph building
- MultiAgent: Completely different approach, uses engines dict
- RAGAgent: Unclear how it should handle retriever vs LLM

#### 7.2 No Shared Patterns

- Each agent implements common functionality differently
- Serialization handled inconsistently
- Graph building reimplemented each time

## Root Cause Analysis

### 1. **Organic Growth**

The system grew feature by feature without a comprehensive design, leading to:

- Incremental hacks (like schema modification)
- Multiple ways to do the same thing
- Backward compatibility constraints

### 2. **Unclear Ownership Model**

No clear boundaries for what belongs where:

- Should tools belong to agents or engines?
- Who owns schemas?
- Where should configuration live?

### 3. **Mixing Concerns**

Agents try to do too much:

- Configuration management
- Schema generation
- Engine management
- Graph building
- Execution

### 4. **Inheritance vs Composition**

Over-reliance on inheritance when composition might be better:

- Mixins help but aren't used consistently
- Deep inheritance hierarchies
- Difficult to mix and match capabilities

## Proposed Architecture

### Design Principles

1. **Single Responsibility**: Each component has one clear job
2. **Composition Over Inheritance**: Use mixins and composition
3. **Explicit Over Implicit**: Clear contracts and interfaces
4. **Immutable Engines**: Engines are configuration, don't modify them
5. **Agent-Level Control**: Agents orchestrate, engines execute

### Core Components

#### 1. Engine as Pure Configuration

```python
class Engine:
    """Engines are immutable configuration objects."""
    # No tools - tools belong to agents
    # No schema modification - schemas are derived, not modified
    # Clear input/output contracts
```

#### 2. Unified Engine Management

```python
class Agent:
    # Single engines dict - no dual fields
    engines: Dict[str, Engine] = Field(default_factory=dict)

    # Properties for convenience
    @property
    def primary_engine(self) -> Optional[Engine]:
        """The main engine (if any)."""
        return self.engines.get("primary")
```

#### 3. Agent-Level Schema Control

```python
class Agent:
    # Explicit schema definitions
    state_schema: Type[BaseModel] = MessagesState

    # Agent controls output transformation
    output_processors: List[OutputProcessor] = Field(default_factory=list)

    def process_output(self, raw_output: Any) -> Any:
        """Unified output processing pipeline."""
        output = raw_output
        for processor in self.output_processors:
            output = processor.process(output)
        return output
```

#### 4. Proper Field Syncing

```python
class FieldSyncMixin:
    """Bidirectional field syncing with clear contracts."""
    field_sync_map: ClassVar[Dict[str, str]] = {}
    sync_targets: List[str] = Field(default_factory=lambda: ["primary"])

    def sync_to_engines(self):
        """Sync fields to specified engines."""
        for target in self.sync_targets:
            if target in self.engines:
                self._sync_to_engine(self.engines[target])
```

#### 5. Tool Management

```python
class Agent:
    # Tools belong to agents, not engines
    tools: List[Tool] = Field(default_factory=list)

    # Clear tool routing
    tool_router: ToolRouter = Field(default_factory=ToolRouter)

    def get_tools_for_engine(self, engine_name: str) -> List[Tool]:
        """Get tools routed to specific engine."""
        return self.tool_router.get_tools(engine_name, self.tools)
```

## Implementation Plan

### Phase 1: Foundation (Breaking Changes)

1. **Unify Engine Management**
   - Remove `engine` field, use only `engines` dict
   - Add properties for backward compatibility
   - Update all agents to use new pattern

2. **Fix Structured Output**
   - Remove engine schema modification
   - Add `StructuredOutputProcessor`
   - Handle at agent level, not engine level

3. **Implement FieldSyncMixin**
   - Create proper bidirectional syncing
   - Define standard syncable fields
   - Support multiple engine targets

### Phase 2: Schema System

1. **Simplify Schema Generation**
   - Clear rules for state schema
   - Predictable input/output derivation
   - No special cases in base class

2. **Output Processing Pipeline**
   - Implement `OutputProcessor` interface
   - Built-in processors for common cases
   - Composable processing chain

### Phase 3: Consistency

1. **Standardize Agent Types**
   - Common patterns for all agents
   - Shared base functionality
   - Consistent graph building

2. **Configuration System**
   - Hierarchical configuration
   - Runtime config flow
   - Clear precedence rules

### Phase 4: Tool System

1. **Centralize Tool Management**
   - Tools owned by agents
   - Clear routing rules
   - Proper synchronization

2. **Remove Tool/Engine Coupling**
   - Engines don't have tools
   - Agents manage tool assignment
   - Clean separation of concerns

## Migration Strategy

### Backward Compatibility

1. **Deprecation Warnings**
   - Warn when using `engine` field
   - Warn when modifying engine schemas
   - Provide migration guides

2. **Compatibility Shims**
   - Properties to support old interfaces
   - Automatic migration where possible
   - Clear upgrade path

### Testing Strategy

1. **Comprehensive Test Suite**
   - Test all agent types
   - Test migration paths
   - Performance benchmarks

2. **Gradual Rollout**
   - Feature flags for new behavior
   - Side-by-side testing
   - Staged deployment

## Success Metrics

1. **Code Quality**
   - Reduced complexity scores
   - Better test coverage
   - Fewer special cases

2. **Developer Experience**
   - Clearer documentation
   - Predictable behavior
   - Easier to extend

3. **Performance**
   - No performance regression
   - Better resource usage
   - Improved startup time

## Risks and Mitigations

### Risk 1: Breaking Changes

- **Impact**: Existing code breaks
- **Mitigation**: Compatibility layer, deprecation period

### Risk 2: Performance Impact

- **Impact**: Slower execution
- **Mitigation**: Benchmark early, optimize critical paths

### Risk 3: Adoption Resistance

- **Impact**: Developers don't migrate
- **Mitigation**: Clear benefits, good docs, migration tools

## Timeline

- **Week 1-2**: Foundation work (Phase 1)
- **Week 3-4**: Schema system (Phase 2)
- **Week 5-6**: Consistency (Phase 3)
- **Week 7-8**: Tool system (Phase 4)
- **Week 9-10**: Testing and migration
- **Week 11-12**: Documentation and rollout

## Conclusion

This refactoring addresses fundamental architectural issues in the Haive agent system. By implementing these changes, we'll have:

1. Clearer separation of concerns
2. More predictable behavior
3. Easier maintenance and extension
4. Better developer experience
5. Improved performance and reliability

The investment in refactoring will pay dividends in reduced bugs, faster feature development, and happier developers.
