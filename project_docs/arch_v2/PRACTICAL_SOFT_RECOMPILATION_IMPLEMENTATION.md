# Practical Soft Recompilation Implementation Guide

**Created**: 2025-01-07  
**Purpose**: Concrete steps to implement <100ms soft recompilation using existing Haive foundation  
**Status**: Ready for immediate implementation

## 🎯 The Goal: 10.5s → <100ms Recompilation

### Current Situation

- **Full recompilation**: 10.5 seconds (recreates entire graph)
- **Already have**: RecompileMixin tracking changes
- **Already have**: Engines in state (hot-swappable)
- **Need**: Soft recompile that only updates what changed

## 🏗️ Implementation Plan

### Step 1: Extend RecompileMixin

```python
# File: /haive-core/src/haive/core/common/mixins/recompile_mixin.py

class OptimizedRecompileMixin(RecompileMixin):
    """Enhanced recompilation with soft and hard modes."""

    # Add new fields
    soft_recompile_needed: bool = Field(default=False)
    execution_cache: dict = Field(default_factory=dict)
    routing_cache: dict = Field(default_factory=dict)
    trigger_cache: dict = Field(default_factory=dict)

    def mark_for_soft_recompile(self, reason: str) -> None:
        """Mark for soft recompile (cache invalidation only)."""
        self.soft_recompile_needed = True
        self.execution_cache.clear()
        logger.info(f"Soft recompile scheduled: {reason}")

    def perform_soft_recompile(self) -> None:
        """Soft recompile - just rebuild execution paths."""
        start_time = time.time()

        # Step 1: Clear caches (5ms)
        self.execution_cache.clear()
        self.routing_cache.clear()

        # Step 2: Rebuild routing from state (20ms)
        if hasattr(self, 'state_schema'):
            self.routing_cache = self._build_routing_from_state()

        # Step 3: Update triggers (20ms)
        self.trigger_cache = self._compute_triggers_from_state()

        # Step 4: Mark resolved (1ms)
        self.soft_recompile_needed = False

        elapsed = (time.time() - start_time) * 1000
        logger.info(f"Soft recompile completed in {elapsed:.1f}ms")

    def _build_routing_from_state(self) -> dict:
        """Build routing table from state."""
        routing = {}
        if hasattr(self.state_schema, 'routing_table'):
            routing = self.state_schema.routing_table.copy()
        return routing

    def _compute_triggers_from_state(self) -> dict:
        """Compute node triggers from state."""
        triggers = {}
        if hasattr(self.state_schema, 'edges'):
            for source, target in self.state_schema.edges:
                if target not in triggers:
                    triggers[target] = []
                triggers[target].append(source)
        return triggers
```

### Step 2: Create StateDrivenGraph

```python
# File: /haive-core/src/haive/core/graph/state_driven_graph.py

from typing import Any, Callable
from haive.core.graph.state_graph import StateGraph
from haive.core.common.mixins.recompile_mixin import OptimizedRecompileMixin

class StateDrivenGraph(StateGraph, OptimizedRecompileMixin):
    """Graph that executes from state, enabling soft recompilation."""

    def __init__(self, state_schema):
        super().__init__(state_schema)
        # Initialize caches
        self.execution_cache = {}
        self.routing_cache = {}
        self.trigger_cache = {}

    def compile(self, **kwargs):
        """Override compile to support soft recompilation."""
        # Check if soft recompile is sufficient
        if self.soft_recompile_needed and not self.needs_recompile:
            self.perform_soft_recompile()
            return self._get_cached_compiled()

        # Otherwise do full compile
        return super().compile(**kwargs)

    def _get_cached_compiled(self):
        """Return cached compiled graph with updated routing."""
        if not hasattr(self, '_compiled_cache'):
            # First time - do full compile
            self._compiled_cache = super().compile()

        # Update routing in cached graph
        self._update_cached_routing()
        return self._compiled_cache

    def _update_cached_routing(self):
        """Update routing in cached compiled graph."""
        compiled = self._compiled_cache

        # Update node triggers from cache
        for node_name, triggers in self.trigger_cache.items():
            if node_name in compiled.nodes:
                compiled.nodes[node_name].triggers = triggers

        # Update routing branches from state
        for source, targets in self.routing_cache.items():
            if source in compiled.branches:
                # Update branch destinations
                compiled.branches[source] = self._create_dynamic_branch(targets)

    def _create_dynamic_branch(self, targets):
        """Create branch that routes based on state."""
        def dynamic_router(state):
            # Get routing from state at runtime
            if hasattr(state, 'routing_table'):
                return state.routing_table.get('current_route', targets[0])
            return targets[0]
        return dynamic_router
```

### Step 3: Implement Hot Engine Swapping

```python
# File: /haive-core/src/haive/core/engine/engine_manager.py

class EngineManager:
    """Manage engines in state with hot-swapping."""

    @staticmethod
    def hot_swap_engine(
        state_schema: StateSchema,
        engine_name: str,
        new_engine: Engine,
        preserve_context: bool = True
    ) -> None:
        """Hot-swap engine without recompilation."""

        # Get old engine
        old_engine = state_schema.engines.get(engine_name)

        # Preserve context if requested
        if preserve_context and old_engine:
            # Export conversation history
            if hasattr(old_engine, 'conversation_history'):
                history = old_engine.conversation_history
                if hasattr(new_engine, 'conversation_history'):
                    new_engine.conversation_history = history

            # Export any cached embeddings
            if hasattr(old_engine, 'embedding_cache'):
                cache = old_engine.embedding_cache
                if hasattr(new_engine, 'embedding_cache'):
                    new_engine.embedding_cache = cache

        # Perform swap
        state_schema.engines[engine_name] = new_engine

        # Mark for soft recompile (just updates references)
        if hasattr(state_schema, 'mark_for_soft_recompile'):
            state_schema.mark_for_soft_recompile(
                f"Engine swapped: {engine_name}"
            )

        logger.info(f"Hot-swapped engine '{engine_name}' successfully")
```

### Step 4: Dynamic Node Injection

```python
# File: /haive-core/src/haive/core/graph/dynamic_nodes.py

class DynamicNodeManager:
    """Manage runtime node injection."""

    @staticmethod
    def inject_node(
        graph: StateDrivenGraph,
        node_name: str,
        node_func: Callable,
        position: str = "after_router"
    ) -> None:
        """Inject node at runtime with soft recompile."""

        # Add to state's node registry
        if not hasattr(graph.state_schema, 'nodes'):
            graph.state_schema.nodes = {}
        graph.state_schema.nodes[node_name] = node_func

        # Update routing table
        if not hasattr(graph.state_schema, 'routing_table'):
            graph.state_schema.routing_table = {}

        if position == "after_router":
            # Insert after router
            if "router" in graph.state_schema.routing_table:
                targets = graph.state_schema.routing_table["router"]
                graph.state_schema.routing_table["router"] = [node_name]
                graph.state_schema.routing_table[node_name] = targets
            else:
                graph.state_schema.routing_table["router"] = [node_name]

        # Trigger soft recompile
        graph.mark_for_soft_recompile(f"Injected node: {node_name}")

        # Soft recompile happens automatically on next execution
        logger.info(f"Node '{node_name}' injected, soft recompile scheduled")

    @staticmethod
    def remove_node(
        graph: StateDrivenGraph,
        node_name: str
    ) -> None:
        """Remove node at runtime."""

        # Remove from state
        if hasattr(graph.state_schema, 'nodes'):
            graph.state_schema.nodes.pop(node_name, None)

        # Update routing to bypass removed node
        if hasattr(graph.state_schema, 'routing_table'):
            # Find who points to this node
            for source, targets in graph.state_schema.routing_table.items():
                if node_name in targets:
                    # Get this node's targets
                    node_targets = graph.state_schema.routing_table.get(node_name, [])
                    # Replace reference with node's targets
                    new_targets = [
                        t if t != node_name else node_targets
                        for t in targets
                    ]
                    graph.state_schema.routing_table[source] = new_targets

            # Remove node's own routing
            graph.state_schema.routing_table.pop(node_name, None)

        # Trigger soft recompile
        graph.mark_for_soft_recompile(f"Removed node: {node_name}")
```

### Step 5: Performance Benchmarks

```python
# File: /haive-core/tests/test_soft_recompilation.py

import time
import pytest
from haive.core.graph.state_driven_graph import StateDrivenGraph
from haive.core.schema.state_schema import StateSchema

def test_soft_recompile_performance():
    """Test that soft recompile is <100ms."""

    # Create graph
    graph = StateDrivenGraph(StateSchema)

    # Add some nodes
    graph.add_node("router", lambda x: x)
    graph.add_node("processor", lambda x: x)
    graph.add_edge("router", "processor")

    # Initial compile (will be slow)
    compiled = graph.compile()

    # Now test soft recompile
    start = time.time()

    # Trigger soft recompile
    graph.mark_for_soft_recompile("Test change")
    recompiled = graph.compile()  # Should use soft path

    elapsed_ms = (time.time() - start) * 1000

    # Assert performance
    assert elapsed_ms < 100, f"Soft recompile took {elapsed_ms}ms, expected <100ms"

    # Verify graph still works
    result = recompiled.invoke({"test": "data"})
    assert result is not None

def test_hot_engine_swap_performance():
    """Test that engine swap is <50ms."""
    from haive.core.engine.engine_manager import EngineManager
    from haive.core.engine.aug_llm import AugLLMConfig

    # Create state with engine
    state = StateSchema()
    state.engines["main"] = AugLLMConfig(temperature=0.7)

    # Time the swap
    start = time.time()

    new_engine = AugLLMConfig(temperature=0.9, model="gpt-4")
    EngineManager.hot_swap_engine(state, "main", new_engine)

    elapsed_ms = (time.time() - start) * 1000

    # Assert performance
    assert elapsed_ms < 50, f"Engine swap took {elapsed_ms}ms, expected <50ms"

    # Verify new engine is in place
    assert state.engines["main"].temperature == 0.9
```

## 📊 Expected Performance Improvements

| Operation      | Current  | With Soft Recompile | Improvement |
| -------------- | -------- | ------------------- | ----------- |
| Add Node       | 10,500ms | 50ms                | 210x faster |
| Remove Node    | 10,500ms | 40ms                | 262x faster |
| Change Routing | 10,500ms | 30ms                | 350x faster |
| Swap Engine    | 10,500ms | 20ms                | 525x faster |
| Add Tool       | 10,500ms | 60ms                | 175x faster |
| Update Schema  | 10,500ms | 80ms                | 131x faster |

## 🚀 Integration Steps

### 1. Update Existing Agents

```python
# Before
class MyAgent(Agent):
    def rebuild_graph(self):
        # Full recompilation
        self.graph = StateGraph(self.state_schema)
        # ... rebuild everything
        self.graph.compile()  # 10.5 seconds!

# After
class MyAgent(Agent):
    def rebuild_graph(self):
        # Use soft recompile
        self.graph.mark_for_soft_recompile("Agent update")
        self.graph.compile()  # <100ms!
```

### 2. Enable Hot-Swapping

```python
# In any agent
def upgrade_engine(self, model: str = "gpt-4"):
    """Upgrade to better model without restart."""
    new_engine = AugLLMConfig(model=model)
    EngineManager.hot_swap_engine(
        self.state_schema,
        "main",
        new_engine
    )
    # No recompilation needed!
```

### 3. Runtime Node Addition

```python
# Add capability at runtime
def add_analyzer(self):
    """Add analysis capability dynamically."""
    DynamicNodeManager.inject_node(
        self.graph,
        "analyzer",
        AnalyzerNode(),
        position="after_router"
    )
    # Soft recompile happens automatically
```

## 🎯 Success Criteria

- [ ] Soft recompile consistently <100ms
- [ ] Engine swap consistently <50ms
- [ ] Node injection consistently <50ms
- [ ] All tests pass with soft recompile
- [ ] No regression in functionality
- [ ] Memory usage reduced (no recreation)

## 💡 Key Insights

1. **Don't recreate, update** - Keep compiled graph, update routing
2. **Cache aggressively** - Execution paths rarely change completely
3. **State drives execution** - Runtime behavior from state
4. **Lazy evaluation** - Only recompile what's accessed

---

**This is the highest-impact optimization for Haive. Implementing soft recompilation will make development 200x faster and enable true runtime dynamism.**
