# ChainAgent Fix Design

## Problem Summary

ChainAgent is fundamentally broken due to lack of schema composition:
- No use of SchemaComposer or AgentSchemaComposer
- Operates at engine level instead of agent level  
- Manual data passing loses tool_call_id and type safety
- No message preservation between chain steps
- Cannot use existing agent ecosystem

## Current vs Desired State

### Current (Broken)
```python
# Current ChainAgent usage:
chain = ChainAgent(
    AugLLMConfig(model="gpt-4"),  # Engine config
    AugLLMConfig(model="claude"),  # Engine config
    edges=["0->1"]
)

# Problems:
- Uses engines, not agents
- No schema composition
- Manual state passing
- No tool_call_id preservation
```

### Desired (Fixed)  
```python
# Fixed ChainAgent usage:
chain = ChainAgent([
    SimpleAgent(engine=llm1, name="analyzer"),
    ReactAgent(engine=llm2, tools=[search], name="researcher"), 
    SimpleAgent(engine=llm3, name="summarizer")
])

# Benefits:
- Uses actual agents
- Proper schema composition with AgentSchemaComposer
- Automatic field mapping between steps
- tool_call_id preservation
```

## Fix Strategy Options

### Option 1: Create New SequentialAgent (Recommended)
- Create clean implementation using MultiAgent patterns
- Leave existing ChainAgent unchanged (avoid breaking changes)
- Provide migration path once new implementation is proven

### Option 2: Fix ChainAgent In-Place
- Rewrite existing ChainAgent to use proper schema composition
- Risk of breaking existing usage
- Benefit of immediate fix

### Option 3: Quick Patch Current ChainAgent
- Minimal changes to add basic schema composition
- Convert engines to agents automatically
- Band-aid solution but preserves compatibility

## Recommended Implementation: SequentialAgent

### Design Overview
```python
class SequentialAgent(MultiAgentBase):
    """Sequential agent execution with proper schema composition"""
    
    agents: list[Agent] = Field(...)
    execution_pattern: Literal["sequential"] = "sequential"
    
    def __init__(self, agents: list[Agent], **kwargs):
        # Use AgentSchemaComposer for proper field handling
        super().__init__(
            agents=agents,
            execution_pattern="sequential",
            **kwargs
        )
        
        # Sequential-specific setup
        self._setup_sequential_schema()
    
    def _setup_sequential_schema(self):
        """Set up schema for sequential execution"""
        self.state_schema = AgentSchemaComposer.from_agents(
            agents=self.agents,
            separation="sequence",  # Sequential field flow
            build_mode=BuildMode.SEQUENCE,
            include_meta=True,  # Chain coordination metadata
            preserve_messages=True  # Critical for tool_call_id
        )
```

### Schema Composition Strategy
```python
# Sequential field separation strategy:
class SequentialSeparation:
    """Field separation optimized for sequential execution"""
    
    def separate_fields(self, agents, all_fields):
        # Fields flow from one agent to the next
        # Shared fields: messages, meta_state, coordination
        # Private fields: agent-specific state
        # Output->Input mapping: automatic field routing
        
        shared_fields = ["messages", "meta_state", "chain_step"]
        
        for i, agent in enumerate(agents):
            agent_fields = extract_agent_fields(agent)
            
            # Map outputs of agent[i] to inputs of agent[i+1]
            if i < len(agents) - 1:
                next_agent = agents[i + 1]
                self._create_field_mapping(agent, next_agent)
```

### Graph Building Implementation
```python
def build_graph(self) -> BaseGraph:
    """Build sequential execution graph with schema awareness"""
    graph = BaseGraph(name=self.name)
    
    prev_node = None
    
    for i, agent in enumerate(self.agents):
        node_name = f"agent_{i}_{agent.name}"
        
        # Create schema-aware node function
        node_func = self._create_sequential_node(agent, i)
        graph.add_node(node_name, node_func)
        
        # Connect in sequence
        if prev_node:
            graph.add_edge(prev_node, node_name)
        else:
            graph.add_edge(START, node_name)
        
        prev_node = node_name
    
    # Connect final node to END
    if prev_node:
        graph.add_edge(prev_node, END)
    
    return graph

def _create_sequential_node(self, agent: Agent, step_index: int):
    """Create schema-aware node function for sequential execution"""
    
    def sequential_node(state):
        # Extract input for this agent using schema mappings
        agent_input = self._extract_sequential_input(state, agent, step_index)
        
        # Execute agent
        result = agent.invoke(agent_input)
        
        # Update state with result using sequential field mapping
        updated_state = self._update_sequential_state(state, result, agent, step_index)
        
        return updated_state
    
    return sequential_node
```

### Field Mapping Between Steps
```python
def _extract_sequential_input(self, state, agent: Agent, step_index: int):
    """Extract input for agent based on sequential field mappings"""
    
    # Get field mappings from schema
    mappings = self.state_schema.__engine_io_mappings__
    agent_mapping = mappings.get(f"agent_{step_index}", {})
    
    # Extract required input fields
    input_fields = agent_mapping.get("input_fields", [])
    agent_input = {}
    
    for field in input_fields:
        if hasattr(state, field):
            agent_input[field] = getattr(state, field)
    
    # Always include messages for conversation continuity
    if hasattr(state, "messages"):
        agent_input["messages"] = state.messages
    
    # Add step metadata
    agent_input["chain_step"] = step_index
    agent_input["total_steps"] = len(self.agents)
    
    return agent_input

def _update_sequential_state(self, state, result, agent: Agent, step_index: int):
    """Update state with agent result using sequential field mapping"""
    
    updates = {}
    
    # Map agent outputs to state fields
    mappings = self.state_schema.__engine_io_mappings__
    agent_mapping = mappings.get(f"agent_{step_index}", {})
    output_fields = agent_mapping.get("output_fields", [])
    
    for field in output_fields:
        if field in result:
            updates[field] = result[field]
    
    # Always preserve messages (critical for tool_call_id)
    if "messages" in result:
        # Use preserve_messages_reducer to maintain tool_call_id
        existing_messages = getattr(state, "messages", [])
        updates["messages"] = preserve_messages_reducer(existing_messages, result["messages"])
    
    # Update step tracking
    updates["chain_step"] = step_index + 1
    updates["last_agent"] = agent.name
    
    return Command(update=updates)
```

## Message Preservation Implementation

### Critical Feature: tool_call_id Preservation
```python
def preserve_tool_call_ids_in_chain(state, new_messages):
    """Ensure tool_call_id is preserved across chain steps"""
    
    # Use preserve_messages_reducer from MultiAgent
    from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer
    
    existing_messages = getattr(state, "messages", [])
    return preserve_messages_reducer(existing_messages, new_messages)
```

### Tool Coordination Across Steps
```python
# Step 1: Agent calls tool
agent1_result = {
    "messages": [
        AIMessage(content="I'll search for that", tool_calls=[
            {"id": "call_123", "name": "search", "args": {"query": "python"}}
        ])
    ]
}

# Step 2: Tool result preserved
state_after_step1 = {
    "messages": [
        AIMessage(content="I'll search for that", tool_calls=[...]),
        ToolMessage(content="Search results...", tool_call_id="call_123")  # Preserved!
    ]
}

# Step 3: Next agent sees complete tool interaction
agent2_input = {
    "messages": state_after_step1["messages"]  # Complete context
}
```

## Testing Strategy

### Test Cases Required
1. **Basic Sequential Execution**
   ```python
   chain = SequentialAgent([
       SimpleAgent(engine=llm1),
       SimpleAgent(engine=llm2)
   ])
   ```

2. **Tool Usage Across Steps**
   ```python
   chain = SequentialAgent([
       ReactAgent(engine=llm1, tools=[search_tool]),
       SimpleAgent(engine=llm2)  # Should see search results
   ])
   ```

3. **Field Mapping Between Agents**
   ```python
   chain = SequentialAgent([
       AnalyzerAgent(produces=["analysis"]),
       SummarizerAgent(requires=["analysis"])
   ])
   ```

4. **Message Preservation**
   ```python
   # Verify tool_call_id preserved across all steps
   result = chain.invoke({"messages": [initial_message]})
   assert_tool_call_ids_preserved(result["messages"])
   ```

5. **Error Handling**
   ```python
   # Test graceful handling of agent failures
   chain = SequentialAgent([
       SimpleAgent(engine=llm1),
       FailingAgent(),  # Should not break entire chain
       SimpleAgent(engine=llm2)
   ])
   ```

## Migration Plan

### Phase 1: Implement SequentialAgent
- Create SequentialAgent with proper schema composition
- Extend MultiAgentBase for proven infrastructure
- Implement sequential field mapping and message preservation

### Phase 2: Test and Validate
- Comprehensive testing with real use cases
- Performance benchmarking vs current ChainAgent
- Validation of tool_call_id preservation

### Phase 3: Deprecate ChainAgent
- Add deprecation warning to existing ChainAgent
- Provide migration guide and examples
- Update documentation to recommend SequentialAgent

### Phase 4: Clean Migration Path
```python
# Migration helper
def migrate_chain_to_sequential(chain_config):
    """Convert ChainAgent config to SequentialAgent"""
    agents = []
    for node in chain_config.nodes:
        if isinstance(node, Engine):
            agents.append(SimpleAgent(engine=node))
        elif isinstance(node, Agent):
            agents.append(node)
    
    return SequentialAgent(agents)
```

## Expected Benefits

### 1. **Proper Schema Composition**
- Uses AgentSchemaComposer for intelligent field handling
- Automatic field mapping between chain steps
- Type safety throughout execution

### 2. **Tool Coordination**
- tool_call_id preserved across all steps
- Complete tool interaction context maintained
- Agents can build on previous tool usage

### 3. **Agent Ecosystem Integration**
- Works with any Agent type (Simple, React, Multi, etc.)
- Composable with other workflows
- Uses proven MultiAgent infrastructure

### 4. **Performance and Reliability**
- Leverages optimized MultiAgent execution
- Proper error handling and recovery
- Performance metrics and monitoring

This design fixes the fundamental issues with ChainAgent while providing a clean, compatible upgrade path for existing users.