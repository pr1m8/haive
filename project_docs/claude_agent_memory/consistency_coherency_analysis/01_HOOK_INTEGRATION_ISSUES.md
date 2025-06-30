# Hook Integration Issues Analysis

## Current Hook System Problems

### 1. **Isolated Hook Implementation**
**Location**: `packages/haive-agents/src/haive/agents/base/agent.py`

**Current Pattern**:
```python
# Hooks exist but are disconnected from schema composition
def setup_agent(self):
    """Subclass hook for field syncing"""
    pass  # Individual agents override this

def _setup_schemas(self):
    """Schema generation happens AFTER setup_agent"""
    # No hook integration here
```

**Problems**:
- Setup hooks run BEFORE schema generation
- No pre/post schema composition hooks
- Multi-agent workflows bypass individual agent hooks entirely

### 2. **Multi-Agent Hook Bypass**

**MultiAgent Workflow Issue**:
```python
# MultiAgent uses AgentSchemaComposer.from_agents()
# This bypasses individual agent setup_agent() hooks
self.state_schema = AgentSchemaComposer.from_agents(
    agents=agent_list,  # Agents already initialized
    # No hook execution during composition
)
```

**Impact**: 
- Sub-agents in multi-agent workflows don't get their hooks called
- Field syncing between agents doesn't happen
- Pre/post composition logic is lost

### 3. **ChainAgent Hook Absence**

**ChainAgent has NO hook system**:
```python
# ChainAgent doesn't inherit proper hook patterns
def setup_workflow(self):
    # Manual setup without hooks
    # No integration with schema composition
```

**Missing Capabilities**:
- No pre-chain execution hooks
- No inter-step hooks between chain nodes
- No post-chain completion hooks

## Required Hook Integration Points

### Schema Composition Hooks
```python
def pre_schema_composition(self, components: list) -> list:
    """Hook called before schema composition starts"""
    
def post_schema_composition(self, schema: StateSchema) -> StateSchema:
    """Hook called after schema composition completes"""
    
def field_conflict_resolution(self, conflicts: dict) -> dict:
    """Hook for custom field conflict resolution"""
```

### Multi-Agent Coordination Hooks
```python
def pre_agent_execution(self, agent_name: str, state: Any) -> Any:
    """Hook before individual agent executes"""
    
def post_agent_execution(self, agent_name: str, result: Any) -> Any:
    """Hook after individual agent executes"""
    
def agent_transition(self, from_agent: str, to_agent: str, state: Any) -> Any:
    """Hook during agent transitions"""
```

### Node Sequence Hooks
```python
def pre_node_sequence(self, nodes: list[Node]) -> list[Node]:
    """Hook before node sequence execution"""
    
def inter_node_hook(self, current_node: Node, next_node: Node, state: Any) -> Any:
    """Hook between node executions"""
    
def post_node_sequence(self, results: list) -> list:
    """Hook after node sequence completion"""
```

## Integration with Schema Composers

### AgentSchemaComposer Enhancement
```python
class AgentSchemaComposer:
    @classmethod
    def from_agents(cls, agents, hooks=None, **kwargs):
        # Call pre-composition hooks
        if hooks and hasattr(hooks, 'pre_schema_composition'):
            agents = hooks.pre_schema_composition(agents)
            
        # Existing composition logic...
        
        # Call post-composition hooks
        if hooks and hasattr(hooks, 'post_schema_composition'):
            schema = hooks.post_schema_composition(schema)
            
        return schema
```

### Hook-Aware Multi-Agent
```python
class MultiAgent:
    def __init__(self, agents, hooks=None, **kwargs):
        self.hooks = hooks or DefaultHooks()
        
        # Schema composition with hook integration
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=agents,
            hooks=self.hooks,
            **kwargs
        )
```

## Proposed Hook Architecture

### 1. **Hook Registry System**
```python
class HookRegistry:
    def register_hook(self, event: str, callback: callable):
        """Register hook for specific event"""
        
    def execute_hooks(self, event: str, *args, **kwargs):
        """Execute all hooks for event"""
```

### 2. **Standardized Hook Events**
- `pre_schema_composition`
- `post_schema_composition` 
- `field_conflict_detected`
- `pre_agent_execution`
- `post_agent_execution`
- `pre_node_sequence`
- `post_node_sequence`
- `agent_transition`
- `workflow_started`
- `workflow_completed`

### 3. **Hook Context Object**
```python
class HookContext:
    agent_name: str
    current_state: Any
    schema_metadata: dict
    execution_phase: str
    
    def update_state(self, updates: dict):
        """Update state with validation"""
        
    def add_metadata(self, key: str, value: Any):
        """Add metadata for downstream hooks"""
```

## Implementation Priority

### Phase 1: Core Hook Infrastructure
1. Standardize hook events across all agent types
2. Create HookRegistry and HookContext classes
3. Update AgentSchemaComposer to support hooks

### Phase 2: Multi-Agent Integration  
1. Ensure sub-agent hooks execute during composition
2. Add agent transition hooks
3. Test hook execution order in complex workflows

### Phase 3: Node Sequence Integration
1. Add inter-node hooks to graph execution
2. Integrate with ChainAgent workflow
3. Support conditional hook execution based on state

This will resolve the current hook isolation and enable proper pre/post processing in complex agent workflows.