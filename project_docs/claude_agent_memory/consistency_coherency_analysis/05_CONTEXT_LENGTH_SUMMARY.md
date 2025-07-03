# Critical Issues Summary - Context Length Aware

## 🚨 Five Critical Consistency Issues

### 1. **Hook Integration Failure**

**Problem**: Pre/post hooks don't work with node sequences or multi-agent workflows

- Hooks are isolated from schema composition
- Multi-agent bypasses individual agent hooks
- No inter-node or agent transition hooks

**Fix**: Integrate hooks into AgentSchemaComposer and graph execution

### 2. **Agent vs Component Confusion**

**Problem**: Everything inherits from Agent even when it's not reasoning-capable

- Retrievers, loaders, callables all use Agent base class
- `engine_type: EngineType.AGENT` for non-reasoning components
- No clear distinction between LLM agents and deterministic components

**Fix**: Create Component hierarchy separate from Agent hierarchy

### 3. **Multi-Agent Pattern Chaos**

**Problem**: Three incompatible multi-agent implementations

- **MultiAgent**: Uses AgentSchemaComposer (good)
- **ChainAgent**: No schema composition, manual data passing (broken)
- **SequentialAgent**: Mixed approaches, inconsistent patterns

**Fix**: Unified MultiAgentBase with consistent schema composition

### 4. **NodeConfig-Schema Disconnect**

**Problem**: Graph node configuration doesn't integrate with schema composition

- EngineNodeConfig uses string references, SchemaComposer uses objects
- No field mapping from schema to node execution
- Type safety lost between schema and graph execution

**Fix**: Schema-aware NodeConfig with field mapping integration

### 5. **Engine Type Inheritance Issues**

**Problem**: Engine types don't reflect actual capabilities

- All agents use same engine_type regardless of function
- Inheritance hierarchy doesn't match functional capabilities
- No clear mapping between engine type and required features

**Fix**: Capability-based engine typing with proper inheritance

## 🎯 Priority Actions (Context Constrained)

### Immediate (Week 1)

1. **Fix ChainAgent schema composition** - Use AgentSchemaComposer
2. **Create Component base class** - Separate from Agent hierarchy
3. **Audit Agent vs Component misclassifications**

### Short-term (Month 1)

4. **Implement unified MultiAgentBase**
5. **Create schema-aware NodeConfig bridge**
6. **Integrate hooks with schema composition**

### Medium-term (Quarter 1)

7. **Migrate all multi-agent patterns to unified base**
8. **Update engine type taxonomy**
9. **Full hook system integration**

## 🔧 Quick Wins for Immediate Impact

### ChainAgent Schema Fix (2 hours)

```python
# Replace DynamicGraph with AgentSchemaComposer
self.state_schema = AgentSchemaComposer.from_agents(
    agents=self.agents,  # Not engines!
    separation="sequence",
    build_mode=BuildMode.SEQUENCE
)
```

### Component Separation (4 hours)

```python
# Create new hierarchy
class Component(BaseComponent):
    engine_type: EngineType.COMPONENT

class RetrieverComponent(Component):
    engine_type: EngineType.RETRIEVER
```

### Hook-Schema Integration (6 hours)

```python
# Add hooks to AgentSchemaComposer
AgentSchemaComposer.from_agents(agents, hooks=hook_registry)
```

## 📊 Impact Assessment

### High Impact, Low Effort

- **ChainAgent fix**: Solves tool_call_id loss, enables proper field mapping
- **Component separation**: Immediate conceptual clarity

### High Impact, Medium Effort

- **MultiAgentBase**: Unifies all multi-agent patterns
- **NodeConfig bridge**: Enables type-safe graph execution

### Medium Impact, High Effort

- **Full hook integration**: Complete workflow customization
- **Engine type migration**: Requires extensive testing

## 🎯 Success Metrics

### Technical

- All multi-agent patterns use AgentSchemaComposer ✅
- Zero tool_call_id loss across workflows ✅
- Type-safe node execution with schema validation ✅
- Clear Agent vs Component distinction ✅

### Developer Experience

- Consistent API across all multi-agent types
- Clear guidance on which pattern to use when
- Hooks work seamlessly with complex workflows
- Schema composition "just works" for all patterns

## 🚧 Risk Mitigation

### Context Length Constraints

- Focus on high-impact, low-effort fixes first
- Document decisions for future detailed implementation
- Create focused analysis documents (like this folder)
- Prioritize API consistency over internal optimization

### Breaking Changes

- Maintain backward compatibility during migration
- Deprecate old patterns gradually
- Provide clear migration guides
- Test extensively before removing old code

This analysis provides the foundation for resolving the core consistency and coherency issues in the Haive agent framework while being mindful of context length constraints.
