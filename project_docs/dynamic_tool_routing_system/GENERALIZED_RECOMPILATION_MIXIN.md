# Generalized Recompilation Hook System

## Overview

The dynamic tool routing mixin demonstrates a powerful pattern for **observable change detection** and **recompilation signaling**. This pattern can be generalized for any component that needs to track changes and signal when updates are required.

## Core Pattern Analysis

### **The Recompilation Hook Pattern**

```python
# 1. Change Detection
def _compute_state_hash(self) -> str:
    """Compute hash of current configuration."""
    
# 2. Change Notification  
def _notify_change(self, change_type: str, details: Dict):
    """Notify observers of changes."""
    
# 3. Observer Registration
def register_change_callback(self, callback: Callable):
    """Register callback for change events."""
    
# 4. Recompilation Signaling
def needs_recompilation(self) -> bool:
    """Check if component needs recompilation."""
```

This pattern provides:
- **Automatic change detection** via hashing
- **Observer pattern** for decoupled notifications
- **Lazy recompilation** - signal need but don't force immediate action
- **Batch operations** - multiple changes before recompilation

## Generalized Implementation

### **1. Core Recompilation Mixin**

```python
class RecompilationMixin:
    """
    Generalized mixin for components that need recompilation tracking.
    
    Provides:
    - Hash-based change detection
    - Observer pattern for change notifications
    - Configurable state tracking
    - Batch operation support
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._state_hash: Optional[str] = None
        self._last_recompiled: Optional[datetime] = None
        self._change_callbacks: List[Callable] = []
        self._pending_changes: Set[str] = set()
        self._recompilation_reason: Optional[str] = None
        self._batch_mode: bool = False
    
    # ========================================================================
    # ABSTRACT METHODS (to be implemented by subclasses)
    # ========================================================================
    
    def _compute_state_hash(self) -> str:
        """
        Compute hash of current state.
        
        Subclasses must implement this to define what constitutes "state"
        for change detection purposes.
        """
        raise NotImplementedError("Subclasses must implement _compute_state_hash")
    
    def _get_change_details(self, change_type: str) -> Dict[str, Any]:
        """
        Get details about a specific change.
        
        Subclasses can override to provide richer change information.
        """
        return {"change_type": change_type, "timestamp": datetime.now()}
    
    # ========================================================================
    # CHANGE DETECTION
    # ========================================================================
    
    def needs_recompilation(self) -> bool:
        """Check if component needs recompilation."""
        if self._state_hash is None:
            return True
            
        current_hash = self._compute_state_hash()
        return current_hash != self._state_hash
    
    def mark_compiled(self, reason: Optional[str] = None) -> None:
        """Mark component as compiled with current state."""
        self._state_hash = self._compute_state_hash()
        self._last_recompiled = datetime.now()
        self._pending_changes.clear()
        self._recompilation_reason = reason
    
    def get_recompilation_info(self) -> Dict[str, Any]:
        """Get detailed recompilation information."""
        return {
            "needs_recompilation": self.needs_recompilation(),
            "last_recompiled": self._last_recompiled,
            "current_hash": self._compute_state_hash(),
            "stored_hash": self._state_hash,
            "pending_changes": list(self._pending_changes),
            "last_reason": self._recompilation_reason
        }
    
    # ========================================================================
    # CHANGE NOTIFICATION
    # ========================================================================
    
    def register_change_callback(
        self, 
        callback: Callable[[str, Dict[str, Any]], None]
    ) -> str:
        """
        Register callback for change notifications.
        
        Args:
            callback: Function called with (change_type, details)
            
        Returns:
            Callback ID for later removal
        """
        callback_id = f"callback_{len(self._change_callbacks)}"
        self._change_callbacks.append((callback_id, callback))
        return callback_id
    
    def unregister_change_callback(self, callback_id: str) -> bool:
        """Remove a registered callback."""
        for i, (cid, _) in enumerate(self._change_callbacks):
            if cid == callback_id:
                del self._change_callbacks[i]
                return True
        return False
    
    def _notify_change(self, change_type: str, **kwargs) -> None:
        """Notify all registered callbacks of a change."""
        if not self._batch_mode:
            self._pending_changes.add(change_type)
            
        details = self._get_change_details(change_type)
        details.update(kwargs)
        
        for _, callback in self._change_callbacks:
            try:
                callback(change_type, details)
            except Exception as e:
                # Log error but don't fail the operation
                import logging
                logging.error(f"Error in change callback: {e}")
    
    # ========================================================================
    # BATCH OPERATIONS
    # ========================================================================
    
    def start_batch_mode(self) -> None:
        """Start batch mode to defer change notifications."""
        self._batch_mode = True
    
    def end_batch_mode(self, notify: bool = True) -> None:
        """End batch mode and optionally notify of all changes."""
        self._batch_mode = False
        
        if notify and self._pending_changes:
            self._notify_change("batch_update", changes=list(self._pending_changes))
            self._pending_changes.clear()
    
    def batch_operation(self, operation: Callable) -> Any:
        """Execute operation in batch mode."""
        self.start_batch_mode()
        try:
            result = operation()
            return result
        finally:
            self.end_batch_mode()
```

### **2. Tool Route Specific Implementation**

```python
class DynamicToolRouteMixin(RecompilationMixin, ToolRouteMixin):
    """
    Tool route mixin with recompilation hooks.
    
    Specializes RecompilationMixin for tool route management.
    """
    
    def _compute_state_hash(self) -> str:
        """Compute hash based on tool routes."""
        import hashlib
        route_str = str(sorted(self.tool_routes.items()))
        return hashlib.md5(route_str.encode()).hexdigest()
    
    def _get_change_details(self, change_type: str) -> Dict[str, Any]:
        """Get tool route specific change details."""
        details = super()._get_change_details(change_type)
        details.update({
            "tool_routes": self.tool_routes.copy(),
            "tool_count": len(self.tool_routes)
        })
        return details
    
    # Override tool methods to add change notification
    def add_tool(self, tool: Any, route: Optional[str] = None, **kwargs) -> "DynamicToolRouteMixin":
        """Add tool and notify of changes."""
        tool_name = self._get_tool_name(tool)
        old_routes = self.tool_routes.copy()
        
        # Call parent implementation
        result = super().add_tool(tool, route, **kwargs)
        
        # Notify change
        self._notify_change("tool_added", 
            tool_name=tool_name, 
            route=route,
            old_routes=old_routes,
            new_routes=self.tool_routes
        )
        
        return result
    
    def remove_tool(self, tool_name: str, **kwargs) -> "DynamicToolRouteMixin":
        """Remove tool and notify of changes."""
        old_route = self.tool_routes.get(tool_name)
        old_routes = self.tool_routes.copy()
        
        # Call parent implementation  
        result = super().remove_tool(tool_name, **kwargs)
        
        # Notify change
        self._notify_change("tool_removed",
            tool_name=tool_name,
            old_route=old_route,
            old_routes=old_routes,
            new_routes=self.tool_routes
        )
        
        return result
```

### **3. ValidationNodeConfigV2 Integration**

```python
class RecompilableValidationNodeConfigV2(RecompilationMixin, ValidationNodeConfigV2):
    """
    ValidationNodeConfigV2 with recompilation tracking.
    """
    
    def _compute_state_hash(self) -> str:
        """Compute hash based on validation configuration."""
        import hashlib
        
        # Include tool routes, engine config, validation rules
        state_components = [
            str(sorted(self.tool_routes.items())),
            str(self.engine_name),
            str(getattr(self, 'validation_rules', {})),
            str(getattr(self, 'custom_validators', {}))
        ]
        
        state_str = "|".join(state_components)
        return hashlib.md5(state_str.encode()).hexdigest()
    
    def _get_change_details(self, change_type: str) -> Dict[str, Any]:
        """Get validation node specific change details."""
        details = super()._get_change_details(change_type)
        details.update({
            "engine_name": self.engine_name,
            "tool_routes": getattr(self, 'tool_routes', {}),
            "validation_rules": getattr(self, 'validation_rules', {})
        })
        return details
    
    def update_tool_routes(self, new_routes: Dict[str, str]) -> None:
        """Update tool routes and notify of changes."""
        old_routes = getattr(self, 'tool_routes', {}).copy()
        
        # Update routes
        if hasattr(self, 'tool_routes'):
            self.tool_routes.update(new_routes)
        else:
            self.tool_routes = new_routes.copy()
        
        # Notify change
        self._notify_change("tool_routes_updated",
            old_routes=old_routes,
            new_routes=self.tool_routes,
            added_routes={k: v for k, v in new_routes.items() if k not in old_routes},
            changed_routes={k: v for k, v in new_routes.items() 
                          if k in old_routes and old_routes[k] != v}
        )
    
    def add_validation_rule(self, rule_name: str, rule_func: Callable) -> None:
        """Add validation rule and notify of changes."""
        if not hasattr(self, 'validation_rules'):
            self.validation_rules = {}
            
        old_rules = self.validation_rules.copy()
        self.validation_rules[rule_name] = rule_func
        
        self._notify_change("validation_rule_added",
            rule_name=rule_name,
            old_rules=old_rules,
            new_rules=self.validation_rules
        )
```

### **4. Graph-Level Integration**

```python
class RecompilableBaseGraph(RecompilationMixin, BaseGraph):
    """
    BaseGraph with recompilation tracking.
    """
    
    def _compute_state_hash(self) -> str:
        """Compute hash based on graph structure."""
        import hashlib
        
        components = [
            str(sorted(self.nodes.keys())),
            str(sorted(self.edges)),
            str(sorted(self.branches.keys())),
            str(getattr(self, 'tool_routes', {}))
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
    
    def add_edge(self, *args, **kwargs) -> "RecompilableBaseGraph":
        """Add edge and notify of changes."""
        old_edges = len(self.edges)
        
        result = super().add_edge(*args, **kwargs)
        
        new_edges = len(self.edges)
        if new_edges > old_edges:
            self._notify_change("edges_added",
                edges_added=new_edges - old_edges,
                total_edges=new_edges
            )
        
        return result
```

## Usage Patterns

### **1. Component-Level Recompilation Tracking**

```python
# For ValidationNodeConfigV2
validation_node = RecompilableValidationNodeConfigV2(
    name="dynamic_validation",
    engine_name="main_engine"
)

# Register for recompilation notifications
validation_node.register_change_callback(
    lambda change_type, details: print(f"Validation node changed: {change_type}")
)

# Add tools - automatically triggers change notification
validation_node.update_tool_routes({"search": "tool_node", "analyze": "validation"})

# Check if recompilation needed
if validation_node.needs_recompilation():
    # Rebuild validation logic
    validation_node.rebuild()
    validation_node.mark_compiled("Tool routes updated")
```

### **2. Graph-Level Integration**

```python
# For BaseGraph  
graph = RecompilableBaseGraph(name="dynamic_graph")

# Register callback to auto-recompile
def auto_recompile_callback(change_type: str, details: Dict):
    if change_type in ["nodes_added", "edges_added", "tool_routes_updated"]:
        print(f"Graph change detected: {change_type}")
        # Could trigger automatic recompilation here

graph.register_change_callback(auto_recompile_callback)

# Graph modifications automatically trigger notifications
graph.add_node("new_node", some_callable)  # Triggers "nodes_added"
graph.add_edge("start", "new_node")        # Triggers "edges_added"
```

### **3. Batch Operations**

```python
# For multiple changes
def bulk_update_validation_node(validation_node, updates):
    validation_node.start_batch_mode()
    
    for tool_name, route in updates["tool_routes"].items():
        validation_node.update_tool_routes({tool_name: route})
    
    for rule_name, rule_func in updates["validation_rules"].items():
        validation_node.add_validation_rule(rule_name, rule_func)
    
    validation_node.end_batch_mode()  # Single "batch_update" notification
```

### **4. Meta-Agent Integration**

```python
class MetaAgentWithRecompilation:
    def __init__(self):
        self.managed_components = {}
        
    def add_managed_component(self, name: str, component: RecompilationMixin):
        """Add component and register for recompilation tracking."""
        self.managed_components[name] = component
        
        # Register callback to track when this component needs recompilation
        component.register_change_callback(
            lambda change_type, details: self._handle_component_change(
                name, change_type, details
            )
        )
    
    def _handle_component_change(self, component_name: str, change_type: str, details: Dict):
        """Handle changes from managed components."""
        print(f"Component {component_name} changed: {change_type}")
        
        # Could trigger meta-agent recompilation logic here
        if self._should_recompile_meta_agent(change_type):
            self._schedule_meta_agent_recompilation()
```

## Benefits of This Generalized Pattern

### **1. Reusability**
- Same pattern works for any component that needs change tracking
- Easy to add to existing classes via mixin
- Consistent interface across different component types

### **2. Decoupling**
- Components don't need to know who's listening for changes
- Observer pattern allows multiple listeners
- Clean separation between change detection and reaction

### **3. Performance**
- Hash-based detection is efficient
- Batch mode prevents notification spam
- Lazy recompilation - signal need but don't force action

### **4. Debugging**
- Rich change details for troubleshooting
- Recompilation history tracking
- Clear timestamps and reasons

### **5. Flexibility**
- Configurable state tracking (subclasses define what matters)
- Pluggable callbacks for different response strategies
- Batch operations for complex updates

This generalized pattern makes the recompilation hook system a powerful, reusable tool for any component that needs observable change tracking.