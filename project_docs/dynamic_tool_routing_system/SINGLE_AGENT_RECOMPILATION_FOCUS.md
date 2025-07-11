# Single Agent Recompilation System

## Focus: Perfect Single Agent Implementation

Let's nail the recompilation system for one agent first, then scale up to multi-agent scenarios.

## Core Architecture - Single Agent

### **1. Agent State with Recompilation**

```python
class RecompilableAgentState(RecompilationMixin, ToolState):
    """
    Single agent state with recompilation tracking.

    This is the foundation - get this right first.
    """

    # Tool route tracking (extends ToolState)
    # inherited: tool_routes, tool_metadata, tool_instances

    # Recompilation specific fields
    last_recompiled_at: Optional[datetime] = Field(
        default=None,
        description="When this agent was last recompiled"
    )

    recompilation_triggers: List[str] = Field(
        default_factory=list,
        description="What triggered recompilation needs"
    )

    tool_addition_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of tool additions for debugging"
    )

    def _compute_state_hash(self) -> str:
        """Hash the parts of state that should trigger recompilation."""
        import hashlib

        # Focus on what actually matters for recompilation
        components = [
            # Tool routes - core functionality
            str(sorted(self.tool_routes.items())),

            # Tool metadata - affects behavior
            str(sorted(self.tool_metadata.items())),

            # Message count - affects context
            str(len(self.messages)),

            # Token usage - affects limits
            str(self.token_usage.total_tokens if hasattr(self, 'token_usage') else 0)
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_tool_with_tracking(self, tool: Any, route: str = "tool_node") -> None:
        """Add tool and track the change."""
        old_routes = self.tool_routes.copy()
        tool_name = tool.name if hasattr(tool, 'name') else str(tool)

        # Add to tool routes (ToolState functionality)
        self.tool_routes[tool_name] = route

        # Track the addition
        self.tool_addition_history.append({
            "tool_name": tool_name,
            "route": route,
            "timestamp": datetime.now(),
            "old_routes": old_routes,
            "new_routes": self.tool_routes.copy()
        })

        # Notify change
        self._notify_change("tool_added",
            tool_name=tool_name,
            route=route,
            old_routes=old_routes,
            new_routes=self.tool_routes
        )

    def get_recompilation_summary(self) -> Dict[str, Any]:
        """Get detailed recompilation status."""
        return {
            "needs_recompilation": self.needs_recompilation(),
            "last_recompiled": self.last_recompiled_at,
            "triggers": self.recompilation_triggers,
            "tool_history": self.tool_addition_history,
            "current_tools": list(self.tool_routes.keys()),
            "hash_info": self.get_recompilation_info()
        }
```

### **2. Agent Class with Recompilation**

```python
class RecompilableSimpleAgent(RecompilationMixin, SimpleAgent):
    """
    SimpleAgent with recompilation tracking.

    Focus on getting this working perfectly first.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Track engine changes if possible
        if hasattr(self.engine, 'register_change_callback'):
            self.engine.register_change_callback(self._handle_engine_change)

    def _compute_state_hash(self) -> str:
        """Hash the agent configuration that affects graph structure."""
        import hashlib

        components = [
            # Agent identity
            str(self.name),

            # Engine configuration
            str(type(self.engine).__name__),
            str(getattr(self.engine, 'tool_routes', {})),
            str(getattr(self.engine, 'system_message', '')),

            # Graph structure (if built)
            str(list(self.graph.nodes.keys()) if hasattr(self, 'graph') and self.graph else []),

            # State schema
            str(type(self.state_schema).__name__ if self.state_schema else "None")
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_tool_dynamically(self, tool: Any, route: str = "tool_node") -> None:
        """
        Add tool and handle recompilation automatically.

        This is the main interface for dynamic tool addition.
        """
        print(f"Adding tool {tool.name} to agent {self.name}")

        # Add to engine if it supports it
        if hasattr(self.engine, 'add_tool'):
            old_routes = getattr(self.engine, 'tool_routes', {}).copy()
            self.engine.add_tool(tool, route)
            new_routes = getattr(self.engine, 'tool_routes', {}).copy()

            print(f"Engine tool routes updated: {old_routes} -> {new_routes}")

            # Notify change
            self._notify_change("tool_added_to_engine",
                tool_name=tool.name,
                route=route,
                old_routes=old_routes,
                new_routes=new_routes
            )

        # Add to state if it supports tracking
        if hasattr(self, 'state') and hasattr(self.state, 'add_tool_with_tracking'):
            self.state.add_tool_with_tracking(tool, route)

    def _handle_engine_change(self, change_type: str, details: Dict) -> None:
        """Handle changes from the engine."""
        print(f"Agent {self.name} engine changed: {change_type}")

        # Propagate as agent change
        self._notify_change("engine_changed",
            engine_change_type=change_type,
            engine_details=details
        )

    def recompile_if_needed(self) -> Dict[str, Any]:
        """
        Check if recompilation is needed and perform it.

        Returns detailed information about what was recompiled.
        """
        result = {
            "was_recompiled": False,
            "recompilation_reason": None,
            "before_hash": self._compute_state_hash(),
            "after_hash": None,
            "graph_nodes_before": None,
            "graph_nodes_after": None,
            "timestamp": datetime.now()
        }

        if self.needs_recompilation():
            print(f"Agent {self.name} needs recompilation")

            # Get current state
            result["graph_nodes_before"] = list(self.graph.nodes.keys()) if hasattr(self, 'graph') and self.graph else []
            result["recompilation_reason"] = "State hash changed"

            # Rebuild graph
            print(f"Rebuilding graph for agent {self.name}")
            self.graph = self.build_graph()

            # Update state
            result["graph_nodes_after"] = list(self.graph.nodes.keys()) if hasattr(self, 'graph') and self.graph else []
            result["after_hash"] = self._compute_state_hash()
            result["was_recompiled"] = True

            # Mark as compiled
            self.mark_compiled(f"Agent {self.name} recompiled")

            print(f"Agent {self.name} recompiled successfully")
            print(f"  Nodes before: {result['graph_nodes_before']}")
            print(f"  Nodes after: {result['graph_nodes_after']}")

        else:
            print(f"Agent {self.name} does not need recompilation")
            result["after_hash"] = result["before_hash"]

        return result

    def get_recompilation_status(self) -> Dict[str, Any]:
        """Get detailed recompilation status."""
        return {
            "agent_name": self.name,
            "needs_recompilation": self.needs_recompilation(),
            "recompilation_info": self.get_recompilation_info(),
            "engine_tools": list(getattr(self.engine, 'tool_routes', {}).keys()),
            "graph_nodes": list(self.graph.nodes.keys()) if hasattr(self, 'graph') and self.graph else [],
            "state_tools": list(getattr(self, 'state', {}).get('tool_routes', {}).keys()) if hasattr(self, 'state') else []
        }
```

### **3. Engine with Recompilation**

```python
class RecompilableAugLLMConfig(RecompilationMixin, AugLLMConfig):
    """
    AugLLMConfig with recompilation tracking.

    Focus on tool route changes.
    """

    def _compute_state_hash(self) -> str:
        """Hash engine configuration that affects agent behavior."""
        import hashlib

        components = [
            # Tool configuration
            str(sorted(self.tool_routes.items())),
            str(len(self.tools)),

            # Core configuration
            str(self.system_message),
            str(self.temperature),
            str(self.max_tokens),

            # Structured output
            str(type(self.structured_output_model).__name__ if self.structured_output_model else "None")
        ]

        state_str = "|".join(components)
        return hashlib.md5(state_str.encode()).hexdigest()

    def add_tool(self, tool: Any, route: Optional[str] = None) -> "RecompilableAugLLMConfig":
        """Add tool and notify of changes."""
        old_routes = self.tool_routes.copy()
        old_tools = len(self.tools)

        # Call parent implementation
        result = super().add_tool(tool, route)

        # Get tool name
        tool_name = tool.name if hasattr(tool, 'name') else str(tool)

        # Notify change
        self._notify_change("tool_added",
            tool_name=tool_name,
            route=route or "default",
            old_routes=old_routes,
            new_routes=self.tool_routes,
            old_tool_count=old_tools,
            new_tool_count=len(self.tools)
        )

        return result
```

## Testing the Single Agent System

### **4. Test Script**

```python
def test_single_agent_recompilation():
    """Test recompilation system on a single agent."""

    print("=== Single Agent Recompilation Test ===\n")

    # Create recompilable engine
    engine = RecompilableAugLLMConfig(
        tools=[calculate_tool],
        system_message="You are a helpful assistant."
    )

    # Create recompilable agent
    agent = RecompilableSimpleAgent(
        name="test_agent",
        engine=engine
    )

    # Initial state
    print("1. Initial state:")
    status = agent.get_recompilation_status()
    print(f"   Needs recompilation: {status['needs_recompilation']}")
    print(f"   Engine tools: {status['engine_tools']}")
    print(f"   Graph nodes: {status['graph_nodes']}")

    # Mark as compiled
    agent.mark_compiled("Initial compilation")

    print("\n2. After marking as compiled:")
    status = agent.get_recompilation_status()
    print(f"   Needs recompilation: {status['needs_recompilation']}")

    # Add tool dynamically
    print("\n3. Adding tool dynamically...")
    agent.add_tool_dynamically(search_tool, "tool_node")

    status = agent.get_recompilation_status()
    print(f"   Needs recompilation: {status['needs_recompilation']}")
    print(f"   Engine tools: {status['engine_tools']}")

    # Recompile
    print("\n4. Recompiling...")
    recompile_result = agent.recompile_if_needed()
    print(f"   Was recompiled: {recompile_result['was_recompiled']}")
    print(f"   Reason: {recompile_result['recompilation_reason']}")
    print(f"   Nodes before: {recompile_result['graph_nodes_before']}")
    print(f"   Nodes after: {recompile_result['graph_nodes_after']}")

    # Final state
    print("\n5. Final state:")
    status = agent.get_recompilation_status()
    print(f"   Needs recompilation: {status['needs_recompilation']}")
    print(f"   Engine tools: {status['engine_tools']}")
    print(f"   Graph nodes: {status['graph_nodes']}")

    return agent

if __name__ == "__main__":
    test_single_agent_recompilation()
```

## Key Benefits of This Focused Approach

### **1. Simple and Testable**

- One agent, one engine, one graph
- Clear cause and effect
- Easy to debug and verify

### **2. Foundation for Scale**

- Patterns work for any agent type
- Can extend to multi-agent later
- Recompilation mixin is reusable

### **3. Observable Changes**

- Every change is tracked and logged
- Rich debugging information
- Clear recompilation reasons

### **4. Backward Compatible**

- Existing SimpleAgent works unchanged
- Can gradually adopt recompilation tracking
- No breaking changes

## Next Steps

1. **Test this single agent system thoroughly**
2. **Verify it works with ValidationNodeConfigV2**
3. **Test with different agent types (ReactAgent, etc.)**
4. **Then scale up to multi-agent scenarios**

This focused approach ensures we get the recompilation mechanics right before adding the complexity of multi-agent coordination.
