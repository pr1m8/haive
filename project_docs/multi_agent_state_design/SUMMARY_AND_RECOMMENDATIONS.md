# Multi-Agent State Design: Summary and Recommendations

## Key Findings

After analyzing the current multi-agent implementation and testing various approaches, we've identified:

### Current Issues
1. **Type Safety Loss**: Agents expect specific state types (e.g., `PlannerState`) but receive generic combined states
2. **Schema Composition Problems**: `AgentSchemaComposer` creates namespace conflicts and breaks agent expectations
3. **State Transfer Complexity**: No clear mechanism for passing data between agents
4. **Field Ownership Ambiguity**: Unclear who owns shared fields like `messages`

### Root Cause
The fundamental issue is trying to flatten all agent schemas into a single schema, which creates:
- Namespace collisions (multiple agents with `task` field)
- Type mismatches (agent expects `PlannerState`, gets `CombinedState`)
- Complex field mapping logic that's error-prone

## Recommended Solution: Meta Agent State Pattern

Based on our exploration, the **Meta Agent State** pattern provides the best balance of:
- ✅ **Type Safety**: Each agent maintains its typed state
- ✅ **Flexibility**: Dynamic agent registration
- ✅ **Clear Ownership**: Explicit shared vs. private state
- ✅ **Debuggability**: State transitions are traceable

### How It Works

```python
class MetaAgentState(StateSchema):
    # Shared state all agents can access
    messages: List[BaseMessage]
    shared_context: Dict[str, Any]
    
    # Agent-specific states (typed but stored as dicts)
    agent_states: Dict[str, Dict[str, Any]]
    
    # Type registry for validation
    agent_schemas: Dict[str, Type[StateSchema]]
    
    # Provides type-safe projections
    def get_agent_view(self, agent_name: str) -> AgentStateView
    def update_from_agent(self, agent_name: str, state: StateSchema)
```

### Key Benefits

1. **Type-Safe Views**: Agents get properly typed state views
2. **State Isolation**: Each agent's state is separate but accessible
3. **Easy Extension**: Adding agents doesn't break existing ones
4. **LangGraph Compatible**: Works with Command/Send patterns

## Implementation Approach

### Phase 1: Update AgentNodeV2
Modify `agent_node_v2.py` to work with MetaAgentState:

```python
class MetaAwareAgentNode(AgentNodeConfig):
    def __call__(self, state: MetaAgentState, config: Optional[ConfigLike]) -> Command:
        # 1. Get typed view for agent
        agent_view = state.get_agent_view(self.agent.name)
        
        # 2. Execute agent with proper typed state
        result = self.agent.invoke(agent_view.agent_state.model_dump())
        
        # 3. Update meta state
        state.update_from_agent(self.agent.name, result)
        
        # 4. Return Command with goto
        return Command(update=state.model_dump(), goto=next_node)
```

### Phase 2: State Transfer Rules
Define explicit transfer mappings:

```python
STATE_TRANSFERS = {
    ("planner", "executor"): {
        "plan": "plan",  # planner.plan -> executor.plan
        "plan_steps": "tasks"  # planner.plan_steps -> executor.tasks
    }
}
```

### Phase 3: Multi-Agent Base Update
Update the multi-agent base to use MetaAgentState:

```python
class EnhancedMultiAgent(Agent):
    def build_master_state(self) -> Type[MetaAgentState]:
        # Create MetaAgentState with registered agents
        meta_state = MetaAgentState()
        for name, agent in self.agents.items():
            meta_state.register_agent(name, agent.state_schema)
        return meta_state
```

## Migration Strategy

1. **Start Small**: Test with 2-agent sequential flow
2. **Validate Types**: Ensure type hints work end-to-end
3. **Add Transfers**: Implement state transfer rules
4. **Scale Up**: Test with parallel and conditional flows

## Alternative Approaches Considered

1. **Namespaced Fields**: `planner_task`, `executor_task` - rejected due to complexity
2. **Nested States**: `state.planner.task` - rejected due to serialization issues
3. **Dynamic Composition**: Runtime schema generation - rejected due to loss of type safety

## Next Actions

1. [ ] Implement `MetaAgentState` in core
2. [ ] Update `AgentNodeV2` to support meta state
3. [ ] Create state transfer mechanism
4. [ ] Test with existing sequential agents
5. [ ] Document patterns for agent developers

## Success Metrics

- **Type Safety**: mypy passes without errors
- **Performance**: < 1ms overhead for state projection
- **Developer Experience**: Adding agent requires < 10 lines
- **Reliability**: No runtime schema errors

## Conclusion

The Meta Agent State pattern solves the core issues while maintaining type safety and flexibility. It provides a clear path forward for multi-agent systems in Haive.