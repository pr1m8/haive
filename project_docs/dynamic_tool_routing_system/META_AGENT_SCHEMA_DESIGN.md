# Meta-Agent Schema Architecture Design

## Overview

This document outlines how the existing Haive schema system should be extended for meta-agent implementations with dynamic tool routing and recompilation capabilities.

## Current Schema Hierarchy

```
StateSchema (Base)
├── MessagesState (messages + basic features)
├── MessagesStateWithTokenUsage (+ token tracking)
├── ToolState (+ tool routing, ToolRouteMixin)
└── LLMState (+ single LLM focus)
```

## Proposed Meta-Agent Schema Extensions

### 1. **MetaAgentState** - Core Meta-Agent Schema

```python
class MetaAgentState(ToolState):
    """
    Core state for meta-agent systems with dynamic capability management.

    Extends ToolState with:
    - Multi-agent management
    - Dynamic capability routing
    - Recompilation tracking
    - Agent lifecycle management
    """

    # ========================================================================
    # AGENT MANAGEMENT
    # ========================================================================

    # Registry of managed agents
    agents: Dict[str, Agent] = Field(
        default_factory=dict,
        description="Registry of managed agents by name"
    )

    # Agent selection and routing
    active_agents: Annotated[List[str], operator.add] = Field(
        default_factory=list,
        description="Stack of active agent names for routing"
    )

    # Agent metadata and capabilities
    agent_capabilities: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Capabilities (tools) available per agent"
    )

    # ========================================================================
    # DYNAMIC CAPABILITY MANAGEMENT
    # ========================================================================

    # Global tool route registry (extends ToolState.tool_routes)
    global_tool_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Global tool name to agent.route mapping"
    )

    # Pending capability operations
    pending_tool_additions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Tools waiting to be added to agents"
    )

    pending_agent_creations: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Agents waiting to be created"
    )

    # ========================================================================
    # RECOMPILATION TRACKING
    # ========================================================================

    # Agents needing recompilation
    agents_needing_recompile: Set[str] = Field(
        default_factory=set,
        description="Agent names that need graph recompilation"
    )

    # Recompilation metadata
    recompilation_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of recompilation events"
    )

    recompilation_count: int = Field(
        default=0,
        description="Total number of recompilations performed"
    )

    # ========================================================================
    # META-AGENT COORDINATION
    # ========================================================================

    # Task delegation and results
    task_queue: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Queue of tasks to be processed"
    )

    agent_results: Dict[str, Any] = Field(
        default_factory=dict,
        description="Results from agent executions"
    )

    # Coordination state
    coordination_mode: str = Field(
        default="sequential",
        description="How agents coordinate (sequential, parallel, hierarchical)"
    )

    # ========================================================================
    # COMPUTED FIELDS
    # ========================================================================

    @computed_field
    @property
    def current_agent(self) -> Optional[str]:
        """Get the currently active agent."""
        return self.active_agents[-1] if self.active_agents else None

    @computed_field
    @property
    def all_available_tools(self) -> List[str]:
        """Get all tools available across all agents."""
        tools = set()
        for capabilities in self.agent_capabilities.values():
            tools.update(capabilities)
        return sorted(list(tools))

    @computed_field
    @property
    def agents_needing_attention(self) -> Dict[str, List[str]]:
        """Get agents that need various types of attention."""
        return {
            "recompilation": list(self.agents_needing_recompile),
            "tool_additions": [
                item["agent_name"] for item in self.pending_tool_additions
            ],
            "creation": [
                item["name"] for item in self.pending_agent_creations
            ]
        }

    # ========================================================================
    # SHARED FIELDS FOR SUBGRAPHS
    # ========================================================================

    __shared_fields__ = [
        "messages",
        "global_tool_routes",
        "agent_capabilities",
        "agents_needing_recompile"
    ]

    # ========================================================================
    # REDUCER FUNCTIONS
    # ========================================================================

    __reducer_fields__ = {
        "active_agents": operator.add,
        "recompilation_history": operator.add,
        "task_queue": operator.add,
    }
```

### 2. **RecompilableAgentState** - Agent-Level Recompilation Tracking

```python
class RecompilableAgentState(ToolState):
    """
    State for individual agents with recompilation tracking.

    Used by agents managed by meta-agents.
    """

    # Recompilation tracking
    tool_route_hash: Optional[str] = Field(
        default=None,
        description="Hash of tool routes at last compilation"
    )

    last_recompiled_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last recompilation"
    )

    pending_tool_additions: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Tools pending addition to this agent"
    )

    recompilation_triggered_by: List[str] = Field(
        default_factory=list,
        description="What triggered the need for recompilation"
    )

    # Tool addition metadata
    tool_addition_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of tool additions"
    )

    @computed_field
    @property
    def needs_recompilation(self) -> bool:
        """Check if recompilation is needed."""
        if not hasattr(self, '_computed_hash'):
            return True

        current_hash = self._compute_tool_route_hash()
        return current_hash != self.tool_route_hash

    def _compute_tool_route_hash(self) -> str:
        """Compute hash of current tool routes."""
        import hashlib
        route_str = str(sorted(self.tool_routes.items()))
        return hashlib.md5(route_str.encode()).hexdigest()
```

### 3. **HierarchicalAgentState** - Multi-Level Agent Management

```python
class HierarchicalAgentState(MetaAgentState):
    """
    State for hierarchical meta-agent systems.

    Supports parent-child agent relationships and delegation.
    """

    # Hierarchy management
    parent_agent: Optional[str] = Field(
        default=None,
        description="Parent agent name if this is a child"
    )

    child_agents: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Child agents for each parent"
    )

    # Delegation patterns
    delegation_rules: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Rules for delegating tasks to child agents"
    )

    # Cross-level communication
    messages_to_parent: List[BaseMessage] = Field(
        default_factory=list,
        description="Messages to send to parent agent"
    )

    messages_from_children: Dict[str, List[BaseMessage]] = Field(
        default_factory=dict,
        description="Messages received from child agents"
    )

    @computed_field
    @property
    def hierarchy_depth(self) -> int:
        """Calculate depth in hierarchy."""
        depth = 0
        current_parent = self.parent_agent
        while current_parent:
            depth += 1
            # Would need to resolve parent to check its parent
            break  # Simplified for now
        return depth

    __shared_fields__ = MetaAgentState.__shared_fields__ + [
        "delegation_rules",
        "child_agents"
    ]
```

### 4. **CapabilityAwareState** - Dynamic Capability Management

```python
class CapabilityAwareState(MetaAgentState):
    """
    State focused on dynamic capability management and routing.
    """

    # Capability registry
    available_capabilities: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Registry of all available capabilities with metadata"
    )

    # Capability routing
    capability_routes: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Which agents can handle each capability"
    )

    # Dynamic capability addition
    capability_requests: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Requests for new capabilities"
    )

    # Performance tracking
    capability_performance: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Performance metrics per capability per agent"
    )

    @computed_field
    @property
    def capability_coverage(self) -> Dict[str, int]:
        """How many agents can handle each capability."""
        coverage = {}
        for capability, agents in self.capability_routes.items():
            coverage[capability] = len(agents)
        return coverage

    @computed_field
    @property
    def agent_specializations(self) -> Dict[str, List[str]]:
        """What capabilities each agent specializes in."""
        specializations = {}
        for agent_name in self.agents:
            specializations[agent_name] = []
            for capability, agents in self.capability_routes.items():
                if agent_name in agents:
                    specializations[agent_name].append(capability)
        return specializations
```

## Schema Composition for Meta-Agents

### 1. **Dynamic Schema Building**

```python
class MetaAgentSchemaComposer(SchemaComposer):
    """
    Extended composer for meta-agent schemas.
    """

    def compose_meta_agent_schema(
        self,
        base_state: Type[StateSchema],
        managed_agents: List[Agent],
        capabilities: List[str],
        hierarchy_config: Optional[Dict] = None
    ) -> Type[StateSchema]:
        """
        Compose schema for meta-agent based on:
        - Base state schema
        - Managed agents and their capabilities
        - Hierarchy configuration
        """

        # Start with base meta-agent state
        if hierarchy_config:
            base_class = HierarchicalAgentState
        elif capabilities:
            base_class = CapabilityAwareState
        else:
            base_class = MetaAgentState

        # Extract fields from managed agents
        agent_fields = {}
        for agent in managed_agents:
            agent_fields.update(self.extract_fields_from_agent(agent))

        # Combine capability routes
        capability_routes = self.build_capability_routes(managed_agents)

        # Create dynamic schema
        schema_fields = {
            **agent_fields,
            "capability_routes": capability_routes,
            "managed_agent_types": [type(agent) for agent in managed_agents]
        }

        return self.create_dynamic_schema(
            base_class=base_class,
            additional_fields=schema_fields,
            name="DynamicMetaAgentState"
        )
```

### 2. **Tool Route Integration**

```python
class MetaAgentToolRouteMixin(ToolRouteMixin):
    """
    Extended tool routing for meta-agents.
    """

    def update_global_tool_routes(self, agent_name: str, tool_routes: Dict[str, str]):
        """Update global tool routes with agent-specific routes."""
        for tool_name, route in tool_routes.items():
            self.global_tool_routes[tool_name] = f"{agent_name}.{route}"

    def get_tool_route_for_agent(self, tool_name: str) -> Optional[Tuple[str, str]]:
        """Get agent and route for a tool."""
        global_route = self.global_tool_routes.get(tool_name)
        if global_route and '.' in global_route:
            agent_name, route = global_route.split('.', 1)
            return agent_name, route
        return None

    def distribute_tool_to_agents(
        self,
        tool: Any,
        target_agents: List[str],
        route: str = "tool_node"
    ):
        """Distribute a tool to multiple agents."""
        for agent_name in target_agents:
            self.pending_tool_additions.append({
                "agent_name": agent_name,
                "tool": tool,
                "route": route,
                "timestamp": datetime.now()
            })
```

## Recompilation Integration

### 1. **Schema-Level Recompilation Tracking**

```python
class RecompilationTrackingMixin:
    """
    Mixin for tracking recompilation needs at schema level.
    """

    def mark_agent_for_recompilation(self, agent_name: str, reason: str):
        """Mark an agent as needing recompilation."""
        self.agents_needing_recompile.add(agent_name)
        self.recompilation_history.append({
            "agent_name": agent_name,
            "reason": reason,
            "timestamp": datetime.now(),
            "resolved": False
        })

    def resolve_recompilation(self, agent_name: str):
        """Mark recompilation as resolved for an agent."""
        self.agents_needing_recompile.discard(agent_name)
        self.recompilation_count += 1

        # Update history
        for entry in reversed(self.recompilation_history):
            if entry["agent_name"] == agent_name and not entry["resolved"]:
                entry["resolved"] = True
                entry["resolved_at"] = datetime.now()
                break
```

### 2. **Agent Factory Integration**

```python
class MetaAgentFactory:
    """
    Factory for creating meta-agents with proper schema composition.
    """

    def create_meta_agent(
        self,
        name: str,
        managed_agents: List[Agent],
        coordination_mode: str = "sequential",
        hierarchy_config: Optional[Dict] = None
    ) -> Agent:
        """Create meta-agent with composed schema."""

        # Compose schema based on managed agents
        composer = MetaAgentSchemaComposer()
        state_schema = composer.compose_meta_agent_schema(
            base_state=MetaAgentState,
            managed_agents=managed_agents,
            capabilities=self.extract_capabilities(managed_agents),
            hierarchy_config=hierarchy_config
        )

        # Create meta-agent engine
        engine = self.create_meta_agent_engine(managed_agents, coordination_mode)

        # Create agent with composed schema
        meta_agent = Agent(
            name=name,
            engine=engine,
            state_schema=state_schema
        )

        return meta_agent
```

## Integration with Existing Systems

### 1. **Base Agent Compatibility**

The meta-agent schemas extend existing schemas, ensuring compatibility:

```python
# Existing SimpleAgent with ToolState
simple_agent = SimpleAgent(engine=engine)  # Uses ToolState

# Meta-agent managing SimpleAgents
meta_agent = MetaAgent(
    managed_agents=[simple_agent],
    state_schema=MetaAgentState  # Extends ToolState
)
```

### 2. **Prebuilt Schema Reuse**

Meta-agents leverage all existing prebuilt schemas:

- **Messages**: Full conversation management
- **Tools**: Tool routing and management
- **Tokens**: Usage tracking across all managed agents
- **LLM**: Model management and optimization

### 3. **Schema Composer Integration**

The existing SchemaComposer automatically handles meta-agent schemas:

```python
# Automatic base class detection
if is_meta_agent:
    base_class = MetaAgentState
elif has_tools:
    base_class = ToolState
elif has_messages:
    base_class = MessagesState
```

## Summary

This design provides:

1. **Hierarchical schema architecture** extending existing prebuilt schemas
2. **Dynamic capability management** with tool routing
3. **Recompilation tracking** integrated at schema level
4. **Agent lifecycle management** with proper state tracking
5. **Composition patterns** for complex meta-agent scenarios
6. **Full compatibility** with existing Haive agent systems

The meta-agent schemas build on the robust foundation of existing schemas while adding the dynamic capabilities needed for sophisticated agent orchestration and management.
