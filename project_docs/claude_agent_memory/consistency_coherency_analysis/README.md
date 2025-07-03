# Consistency & Coherency Analysis - Critical Issues

**Date**: 2025-06-30
**Focus**: Core architectural inconsistencies affecting agent workflows

## Critical Issues Identified

### 1. **Pre/Post Hook Integration Failure**

**Problem**: Hooks don't integrate properly with node sequences or multi-agent workflows

- BaseAgent has hooks but they're isolated from schema composition
- MultiAgent workflows bypass hook systems entirely
- ChainAgent has no hook integration at all

### 2. **Multi-Agent Workflow Inconsistency**

**Problem**: Three different patterns with incompatible approaches

- **MultiAgent**: Sophisticated AgentSchemaComposer + BuildModes
- **ChainAgent**: Manual data passing, no schema composition
- **SequentialAgent**: Uses AgentSchemaComposer but different patterns

### 3. **Agent vs Component Distinction Crisis**

**Problem**: Unclear boundaries between AI agents and callable components

- **LLM Agents**: Need reasoning capability, tool coordination
- **Retrievers**: Deterministic, no LLM needed
- **Callables**: Pure functions, no state management
- **Current**: Everything inherits from Agent base class

### 4. **Engine Type Inheritance Confusion**

**Problem**: Engine types don't map cleanly to agent capabilities

- `engine_type: EngineType.AGENT` used for everything
- No distinction between LLM-based vs retriever-based vs callable-based
- Inheritance hierarchy doesn't reflect functional capabilities

### 5. **NodeConfig-SchemaComposer Incompatibility**

**Problem**: Node configurations don't integrate with schema composition system

- EngineNodeConfig operates at engine level
- SchemaComposer operates at agent/component level
- No bridge between graph node configuration and state schemas

## Root Cause Analysis

### Architecture Mismatch

The system has **three incompatible abstraction layers**:

1. **Engine Layer**: LLM configs, retrievers, callables
2. **Node Layer**: Graph execution units with NodeConfig
3. **Agent Layer**: Schema composition and workflow orchestration

### Schema Composition Fragmentation

Different agent types use different composition strategies:

- **SimpleAgent**: Direct engine modification (dangerous)
- **MultiAgent**: AgentSchemaComposer (gold standard)
- **ChainAgent**: No composition (broken)
- **BaseAgent**: Flexible but inconsistent

### Hook System Isolation

Hooks exist but are disconnected from:

- Schema generation process
- Multi-agent coordination
- Node execution sequences
- State management between components

## Impact Assessment

### Development Experience

- **Confusion**: Developers don't know which pattern to use
- **Inconsistency**: Same functionality implemented differently across agents
- **Fragility**: Changes in one area break unrelated components

### Runtime Issues

- **tool_call_id loss**: ChainAgent and others lose critical tool coordination data
- **Schema conflicts**: No unified approach to field collision resolution
- **Hook failures**: Pre/post hooks don't integrate with complex workflows

### Maintenance Burden

- **Code duplication**: Each agent type reimplements schema logic
- **Testing complexity**: Different patterns require different test approaches
- **Documentation gaps**: Unclear guidance on which patterns to use when

## Proposed Solutions Framework

### 1. Clear Component Taxonomy

```
Agent (LLM-based reasoning)
├── SimpleAgent (single LLM)
├── ReactAgent (reasoning + tools)
└── MultiAgent (coordinated LLMs)

Component (deterministic processing)
├── RetrieverComponent (data retrieval)
├── CallableComponent (pure functions)
└── ProcessorComponent (transformations)

Workflow (orchestration)
├── SequentialWorkflow
├── ParallelWorkflow
└── ConditionalWorkflow
```

### 2. Unified Schema Composition

- **AgentSchemaComposer**: For LLM-based agents only
- **ComponentSchemaComposer**: For deterministic components
- **WorkflowSchemaComposer**: For orchestration patterns

### 3. Hook-Schema Integration

- Hooks should be first-class citizens in schema composition
- Pre/post hooks need access to state schema metadata
- Multi-agent workflows need hook coordination

### 4. NodeConfig-Schema Bridge

- EngineNodeConfig should derive from schema composition
- Node execution should respect schema field mappings
- Graph topology should align with schema structure

## Next Steps

1. **Audit current hook usage patterns**
2. **Design Component vs Agent distinction**
3. **Create NodeConfig-Schema integration spec**
4. **Prototype unified schema composition**
5. **Test hook integration with multi-agent workflows**

---

**Priority**: CRITICAL - These issues affect core framework usability and consistency
