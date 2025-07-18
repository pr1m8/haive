# Meta-Agent Recompilation Integration

## Architecture Overview

The recompilation mixin needs to work across multiple layers:

```
MetaAgentState (ToolState + recompilation tracking)
├── Individual Agent States (SimpleAgentState, ReactAgentState, etc.)
├── Graph Layer (BaseGraph with recompilation hooks)
├── Node Layer (ValidationNodeConfigV2, ToolNodeConfig, etc.)
└── Engine Layer (AugLLMConfig with tool routing)
```

Each layer can change independently and needs to signal recompilation needs upward.

## State Schema Integration

### **1. Enhanced State Hierarchy**

```python
# Base recompilable state
class RecompilableStateSchema(RecompilationMixin, StateSchema):
    """
    Base state schema with recompilation tracking.
    All agent states inherit from this.
    """

    def _compute_state_hash(self) -> str:
        """Default implementation - hash all field values."""
        import hashlib

        # Get all non-excluded fields
        field_values = []
        for field_name, field_info in self.__fields__.items():
            if not field_info.field_info.exclude:
                value = getattr(self, field_name, None)
                field_values.append(f"{field_name}:{str(value)}")

        state_str = "|".join(sorted(field_values))
        return hashlib.md5(state_str.encode()).hexdigest()

# Enhanced tool state with recompilation
class RecompilableToolState(RecompilableStateSchema, ToolState):
    """ToolState with recompilation tracking."""

    def _compute_state_hash(self) -> str:
        """Hash based on tool routes and messages."""
        import hashlib

        components = [
            str(sorted(self.tool_routes.items())),
            str(len(self.messages)),
            str(self.token_usage.total_tokens if hasattr(self, 'token_usage') else 0)
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    # Override tool route methods to trigger change notifications
    def update_tool_routes(self, new_routes: Dict[str, str]) -> None:
        old_routes = self.tool_routes.copy()
        super().update_tool_routes(new_routes)

        self._notify_change("tool_routes_updated",
            old_routes=old_routes,
            new_routes=self.tool_routes
        )

# Meta-agent specific state
class MetaAgentState(RecompilableToolState):
    """
    Meta-agent state with multi-agent coordination.
    Extends RecompilableToolState with agent management.
    """

    # Agent management
    agents: Dict[str, Agent] = Field(
        default_factory=dict,
        description="Managed agents",
        exclude=True  # Like dynamic supervisor - exclude for serialization
    )

    agent_metadata: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Serializable agent metadata"
    )

    # Global capability tracking
    global_tool_routes: Dict[str, str] = Field(
        default_factory=dict,
        description="Global tool name to agent.route mapping"
    )

    # Recompilation coordination
    agents_needing_recompile: Set[str] = Field(
        default_factory=set,
        description="Agents that need recompilation"
    )

    agent_recompilation_callbacks: Dict[str, str] = Field(
        default_factory=dict,
        description="Callback IDs for agent recompilation tracking",
        exclude=True
    )

    def _compute_state_hash(self) -> str:
        """Hash based on meta-agent specific state."""
        import hashlib

        components = [
            # Base tool state
            super()._compute_state_hash(),
            # Agent metadata (not full agents)
            str(sorted(self.agent_metadata.items())),
            # Global tool routes
            str(sorted(self.global_tool_routes.items())),
            # Agent registry
            str(sorted(self.agents.keys()))
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    # ========================================================================
    # AGENT MANAGEMENT WITH RECOMPILATION TRACKING
    # ========================================================================

    def add_agent(self, name: str, agent: Agent, metadata: Optional[Dict] = None) -> None:
        """Add agent and register for recompilation tracking."""

        # Store agent and metadata
        self.agents[name] = agent
        self.agent_metadata[name] = metadata or {}

        # Register recompilation callback if agent supports it
        if isinstance(agent, RecompilationMixin):
            callback_id = agent.register_change_callback(
                lambda change_type, details: self._handle_agent_change(name, change_type, details)
            )
            self.agent_recompilation_callbacks[name] = callback_id

        # Update global tool routes
        if hasattr(agent, 'engine') and hasattr(agent.engine, 'tool_routes'):
            for tool_name, route in agent.engine.tool_routes.items():
                self.global_tool_routes[tool_name] = f"{name}.{route}"

        # Notify of change
        self._notify_change("agent_added",
            agent_name=name,
            agent_type=type(agent).__name__,
            metadata=metadata
        )

    def remove_agent(self, name: str) -> None:
        """Remove agent and cleanup recompilation tracking."""

        if name in self.agents:
            agent = self.agents[name]

            # Cleanup recompilation callback
            if name in self.agent_recompilation_callbacks:
                callback_id = self.agent_recompilation_callbacks[name]
                if isinstance(agent, RecompilationMixin):
                    agent.unregister_change_callback(callback_id)
                del self.agent_recompilation_callbacks[name]

            # Remove from global tool routes
            tools_to_remove = []
            for tool_name, route in self.global_tool_routes.items():
                if route.startswith(f"{name}."):
                    tools_to_remove.append(tool_name)

            for tool_name in tools_to_remove:
                del self.global_tool_routes[tool_name]

            # Remove agent and metadata
            del self.agents[name]
            if name in self.agent_metadata:
                del self.agent_metadata[name]

            # Cleanup recompilation tracking
            self.agents_needing_recompile.discard(name)

            # Notify of change
            self._notify_change("agent_removed",
                agent_name=name,
                removed_tools=tools_to_remove
            )

    def _handle_agent_change(self, agent_name: str, change_type: str, details: Dict) -> None:
        """Handle changes from managed agents."""

        # Mark agent as needing recompilation
        if change_type in ["tool_routes_updated", "engine_changed", "graph_modified"]:
            self.agents_needing_recompile.add(agent_name)

        # Update global tool routes if needed
        if change_type == "tool_routes_updated" and agent_name in self.agents:
            agent = self.agents[agent_name]
            if hasattr(agent, 'engine') and hasattr(agent.engine, 'tool_routes'):
                # Update global routes for this agent
                old_global_routes = self.global_tool_routes.copy()

                # Remove old routes for this agent
                tools_to_remove = [
                    tool for tool, route in self.global_tool_routes.items()
                    if route.startswith(f"{agent_name}.")
                ]
                for tool in tools_to_remove:
                    del self.global_tool_routes[tool]

                # Add new routes
                for tool_name, route in agent.engine.tool_routes.items():
                    self.global_tool_routes[tool_name] = f"{agent_name}.{route}"

                # Notify of global route change
                self._notify_change("global_tool_routes_updated",
                    agent_name=agent_name,
                    old_routes=old_global_routes,
                    new_routes=self.global_tool_routes
                )

        # Propagate change notification to meta-agent level
        self._notify_change("agent_changed",
            agent_name=agent_name,
            agent_change_type=change_type,
            agent_details=details
        )
```

## Agent Class Integration

### **2. Recompilable Agent Classes**

```python
class RecompilableAgent(RecompilationMixin, Agent):
    """
    Base agent class with recompilation tracking.
    All agents can inherit from this instead of just Agent.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Register for engine changes if engine supports it
        if hasattr(self.engine, 'register_change_callback'):
            self.engine.register_change_callback(
                lambda change_type, details: self._handle_engine_change(change_type, details)
            )

    def _compute_state_hash(self) -> str:
        """Hash based on agent configuration."""
        import hashlib

        components = [
            str(self.name),
            str(type(self.engine).__name__),
            str(getattr(self.engine, 'tool_routes', {})),
            str(type(self.state_schema).__name__ if self.state_schema else "None"),
            str(list(self.graph.nodes.keys()) if hasattr(self, 'graph') and self.graph else [])
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def _handle_engine_change(self, change_type: str, details: Dict) -> None:
        """Handle changes from the engine."""
        # Propagate engine changes as agent changes
        self._notify_change("engine_changed",
            engine_change_type=change_type,
            engine_details=details
        )

    def build_graph(self) -> BaseGraph:
        """Build graph and register for graph changes."""
        graph = super().build_graph()

        # If graph supports recompilation tracking, register for changes
        if isinstance(graph, RecompilationMixin):
            graph.register_change_callback(
                lambda change_type, details: self._handle_graph_change(change_type, details)
            )

        return graph

    def _handle_graph_change(self, change_type: str, details: Dict) -> None:
        """Handle changes from the graph."""
        self._notify_change("graph_modified",
            graph_change_type=change_type,
            graph_details=details
        )

# Specific agent implementations
class RecompilableSimpleAgent(RecompilableAgent, SimpleAgent):
    """SimpleAgent with recompilation tracking."""
    pass

class RecompilableReactAgent(RecompilableAgent, ReactAgent):
    """ReactAgent with recompilation tracking."""
    pass
```

## Engine Integration

### **3. Recompilable Engine Classes**

```python
class RecompilableAugLLMConfig(RecompilationMixin, AugLLMConfig):
    """AugLLMConfig with recompilation tracking."""

    def _compute_state_hash(self) -> str:
        """Hash based on engine configuration."""
        import hashlib

        components = [
            str(sorted(self.tool_routes.items())),
            str(self.system_message),
            str(self.temperature),
            str(self.max_tokens),
            str(len(self.tools)),
            str(getattr(self, 'structured_output_model', None))
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_tool(self, tool: Any, route: Optional[str] = None) -> "RecompilableAugLLMConfig":
        """Add tool and notify of changes."""
        old_routes = self.tool_routes.copy()

        result = super().add_tool(tool, route)

        tool_name = tool.name if hasattr(tool, 'name') else str(tool)
        self._notify_change("tool_added",
            tool_name=tool_name,
            route=route,
            old_routes=old_routes,
            new_routes=self.tool_routes
        )

        return result
```

## Graph Integration

### **4. Recompilable Graph Classes**

```python
class RecompilableBaseGraph(RecompilationMixin, BaseGraph):
    """BaseGraph with recompilation tracking."""

    def _compute_state_hash(self) -> str:
        """Hash based on graph structure."""
        import hashlib

        components = [
            str(sorted(self.nodes.keys())),
            str(sorted(self.edges)),
            str(sorted(self.branches.keys())),
            str(getattr(self, 'metadata', {}))
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_node(self, *args, **kwargs) -> "RecompilableBaseGraph":
        """Add node and notify of changes."""
        old_nodes = set(self.nodes.keys())

        result = super().add_node(*args, **kwargs)

        new_nodes = set(self.nodes.keys())
        added_nodes = new_nodes - old_nodes

        if added_nodes:
            self._notify_change("nodes_added",
                added_nodes=list(added_nodes),
                total_nodes=len(self.nodes)
            )

        return result
```

## Complete Integration Example

### **5. How It All Works Together**

```python
class MetaAgentSystem:
    """
    Complete meta-agent system with recompilation tracking.
    """

    def __init__(self):
        # Create meta-agent state
        self.state = MetaAgentState()

        # Register for meta-agent state changes
        self.state.register_change_callback(self._handle_state_change)

        # Track recompilation needs
        self.needs_full_recompilation = False

    def create_managed_agent(self, name: str, agent_type: str, **config) -> RecompilableAgent:
        """Create a new managed agent with recompilation tracking."""

        # Create recompilable engine
        engine = RecompilableAugLLMConfig(**config.get('engine_config', {}))

        # Create recompilable agent
        if agent_type == "simple":
            agent = RecompilableSimpleAgent(name=name, engine=engine)
        elif agent_type == "react":
            agent = RecompilableReactAgent(name=name, engine=engine)
        else:
            agent = RecompilableAgent(name=name, engine=engine)

        # Add to meta-agent state
        self.state.add_agent(name, agent, {"type": agent_type, **config})

        return agent

    def add_tool_to_agent(self, agent_name: str, tool: Any, route: str = "tool_node") -> None:
        """Add tool to specific agent - triggers recompilation cascade."""

        if agent_name in self.state.agents:
            agent = self.state.agents[agent_name]

            # Add tool to agent's engine (triggers engine change notification)
            if hasattr(agent.engine, 'add_tool'):
                agent.engine.add_tool(tool, route)
                # This automatically triggers:
                # 1. Engine change notification
                # 2. Agent change notification
                # 3. Meta-agent state change notification
                # 4. Global tool route update

    def _handle_state_change(self, change_type: str, details: Dict) -> None:
        """Handle changes to meta-agent state."""

        print(f"Meta-agent state changed: {change_type}")

        # Different response strategies based on change type
        if change_type in ["agent_added", "agent_removed"]:
            # Agent topology changed - might need full recompilation
            self.needs_full_recompilation = True

        elif change_type == "global_tool_routes_updated":
            # Tool routes changed - affected agents need recompilation
            agent_name = details.get("agent_name")
            if agent_name:
                self.state.agents_needing_recompile.add(agent_name)

        elif change_type == "agent_changed":
            # Individual agent changed - mark for recompilation
            agent_name = details.get("agent_name")
            if agent_name:
                self.state.agents_needing_recompile.add(agent_name)

    def recompile_if_needed(self) -> Dict[str, Any]:
        """Check and perform recompilation as needed."""

        recompilation_report = {
            "meta_agent_recompiled": False,
            "agents_recompiled": [],
            "recompilation_reasons": []
        }

        # Check if meta-agent state needs recompilation
        if self.state.needs_recompilation():
            print("Meta-agent state needs recompilation")
            self.state.mark_compiled("Meta-agent state updated")
            recompilation_report["meta_agent_recompiled"] = True
            recompilation_report["recompilation_reasons"].append("meta_agent_state_changed")

        # Check individual agents
        for agent_name in list(self.state.agents_needing_recompile):
            agent = self.state.agents[agent_name]

            if isinstance(agent, RecompilationMixin) and agent.needs_recompilation():
                print(f"Recompiling agent: {agent_name}")

                # Rebuild agent's graph
                if hasattr(agent, 'build_graph'):
                    agent.graph = agent.build_graph()

                # Mark as compiled
                agent.mark_compiled(f"Agent {agent_name} recompiled")

                recompilation_report["agents_recompiled"].append(agent_name)

            # Remove from recompilation list
            self.state.agents_needing_recompile.discard(agent_name)

        return recompilation_report

# Usage Example
meta_system = MetaAgentSystem()

# Create managed agents
simple_agent = meta_system.create_managed_agent("simple", "simple",
    engine_config={"tools": [calculate_tool]})

react_agent = meta_system.create_managed_agent("react", "react",
    engine_config={"tools": [search_tool]})

# Add tool - triggers recompilation cascade
meta_system.add_tool_to_agent("simple", new_analysis_tool)

# Check what needs recompilation
report = meta_system.recompile_if_needed()
print(f"Recompilation report: {report}")
```

## Key Benefits

### **1. Cascading Change Detection**

- Engine changes → Agent changes → Meta-agent changes
- Each layer can respond appropriately to changes below it
- Fine-grained control over what triggers recompilation

### **2. Efficient Recompilation**

- Only components that actually changed get recompiled
- Batch operations prevent notification spam
- Lazy recompilation - signal need but don't force immediate action

### **3. Observable Architecture**

- Every layer is observable and can notify observers
- Decoupled - components don't need to know who's listening
- Rich change details for debugging and optimization

### **4. Backward Compatibility**

- Existing agents work without changes
- Can gradually adopt recompilation tracking
- Mixin pattern doesn't break existing inheritance

This creates a **fully observable meta-agent architecture** where changes at any level (engine, agent, graph, state) automatically propagate and trigger appropriate recompilation responses.
