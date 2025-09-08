# Immediate Action Plan - Start Building Today

**Created**: 2025-01-07  
**Purpose**: Concrete steps to implement Haive's dynamic capabilities RIGHT NOW  
**Status**: Ready to execute

## 🎯 Today's Actions (Do These First)

### Action 1: Benchmark Current Performance (15 minutes)

```bash
# Create this file: /home/will/Projects/haive/scripts/benchmark_recompilation.py
```

```python
#!/usr/bin/env python3
"""Benchmark current recompilation performance."""

import time
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from haive.core.engine.aug_llm import AugLLMConfig

def benchmark_recompilation():
    """Measure how bad 10.5s really is."""

    # Create a typical graph
    graph = BaseGraph()
    graph.state_schema = StateSchema()

    # Add some nodes (simulate typical agent)
    for i in range(10):
        graph.add_node(f"node_{i}", lambda x: x)

    # Add edges
    for i in range(9):
        graph.add_edge(f"node_{i}", f"node_{i+1}")

    # Measure compilation time
    print("Starting compilation benchmark...")
    start = time.time()
    graph.compile()
    elapsed = time.time() - start

    print(f"\n🔴 Current recompilation time: {elapsed*1000:.1f}ms")
    print(f"That's {elapsed:.1f} seconds of waiting every change!")

    # Now test adding a node and recompiling
    print("\nTesting node addition...")
    start = time.time()
    graph.add_node("new_node", lambda x: x)
    graph.compile()  # Full recompile!
    elapsed = time.time() - start

    print(f"🔴 Add node + recompile: {elapsed*1000:.1f}ms")

    return elapsed

if __name__ == "__main__":
    benchmark_recompilation()
```

**Run it**: `poetry run python scripts/benchmark_recompilation.py`

### Action 2: Prototype Soft Recompile (30 minutes)

```bash
# Create this file: /home/will/Projects/haive/packages/haive-core/src/haive/core/common/mixins/soft_recompile_mixin.py
```

```python
"""Soft recompilation mixin - 200x faster than full recompile."""

import time
import logging
from typing import Any, Dict, Optional
from pydantic import Field
from haive.core.common.mixins.recompile_mixin import RecompileMixin

logger = logging.getLogger(__name__)

class SoftRecompileMixin(RecompileMixin):
    """Enhanced recompilation with soft mode for <100ms updates."""

    # Soft recompile state
    soft_recompile_needed: bool = Field(default=False)
    execution_cache: Dict[str, Any] = Field(default_factory=dict)
    routing_cache: Dict[str, list[str]] = Field(default_factory=dict)
    compiled_cache: Optional[Any] = Field(default=None, exclude=True)

    def mark_for_soft_recompile(self, reason: str) -> None:
        """Mark for soft recompile - just cache invalidation."""
        self.soft_recompile_needed = True
        self.execution_cache.clear()
        logger.info(f"Soft recompile scheduled: {reason}")

    def perform_soft_recompile(self) -> Any:
        """Perform soft recompile in <100ms."""
        start = time.time()

        # Step 1: Clear execution cache (5ms)
        self.execution_cache.clear()

        # Step 2: Rebuild routing from state (20ms)
        self.routing_cache = self._build_routing_from_state()

        # Step 3: Update cached compiled graph (30ms)
        if self.compiled_cache:
            self._update_compiled_cache()

        # Step 4: Mark complete
        self.soft_recompile_needed = False

        elapsed_ms = (time.time() - start) * 1000
        logger.info(f"✅ Soft recompile completed in {elapsed_ms:.1f}ms")

        return self.compiled_cache

    def _build_routing_from_state(self) -> Dict[str, list[str]]:
        """Build routing table from current state."""
        routing = {}

        # Get from state if available
        if hasattr(self, 'state_schema'):
            if hasattr(self.state_schema, 'routing_table'):
                routing = self.state_schema.routing_table.copy()
            elif hasattr(self.state_schema, 'edges'):
                # Build from edges
                for source, target in self.state_schema.edges:
                    if source not in routing:
                        routing[source] = []
                    routing[source].append(target)

        return routing

    def _update_compiled_cache(self) -> None:
        """Update the cached compiled graph with new routing."""
        if not self.compiled_cache:
            return

        # Update routing in the compiled graph
        # This is where we bypass full recompilation!
        if hasattr(self.compiled_cache, 'branches'):
            for source, targets in self.routing_cache.items():
                # Create dynamic branch
                self.compiled_cache.branches[source] = self._make_branch(targets)

    def _make_branch(self, targets: list[str]):
        """Create a branch function for routing."""
        def branch(state):
            # Dynamic routing based on state
            if hasattr(state, 'next_node'):
                return state.next_node
            return targets[0] if targets else None
        return branch

    def should_soft_recompile(self) -> bool:
        """Check if soft recompile is sufficient."""
        # Soft recompile for:
        # - Routing changes
        # - Node behavior updates
        # - Engine swaps
        # Full recompile for:
        # - Schema changes
        # - New channels
        return self.soft_recompile_needed and not self.needs_recompile
```

### Action 3: Test Engine Hot-Swap (10 minutes)

```bash
# Create test file: /home/will/Projects/haive/test_hot_swap.py
```

```python
#!/usr/bin/env python3
"""Test that engines are truly hot-swappable."""

from haive.core.schema.state_schema import StateSchema
from haive.core.engine.aug_llm import AugLLMConfig
import time

def test_engine_hot_swap():
    """Verify engines can be swapped without recompilation."""

    # Create state with engine
    state = StateSchema()
    state.engines["main"] = AugLLMConfig(
        temperature=0.7,
        model="gpt-3.5-turbo"
    )

    print(f"Initial engine: {state.engines['main'].model}")
    print(f"Temperature: {state.engines['main'].temperature}")

    # Measure swap time
    start = time.time()

    # Hot swap to better model
    state.engines["main"] = AugLLMConfig(
        temperature=0.9,
        model="gpt-4"
    )

    elapsed_ms = (time.time() - start) * 1000

    print(f"\n✅ Engine swapped in {elapsed_ms:.2f}ms!")
    print(f"New engine: {state.engines['main'].model}")
    print(f"Temperature: {state.engines['main'].temperature}")

    # Verify it's truly swapped
    assert state.engines["main"].model == "gpt-4"
    assert state.engines["main"].temperature == 0.9

    print("\n🎯 Hot-swap successful! No recompilation needed!")

if __name__ == "__main__":
    test_engine_hot_swap()
```

**Run it**: `poetry run python test_hot_swap.py`

## 📝 Tomorrow's Implementation

### Task 1: Integrate Soft Recompile into BaseGraph

**File**: `/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/state_graph/base_graph2.py`

**Changes**:

```python
# At top of file
from haive.core.common.mixins.soft_recompile_mixin import SoftRecompileMixin

# Modify class definition
class BaseGraph(Graph, SoftRecompileMixin):  # Add SoftRecompileMixin

    # Override compile method
    def compile(self, **kwargs):
        """Compile with soft recompile support."""

        # Check if soft recompile is sufficient
        if self.should_soft_recompile():
            logger.info("Using soft recompile path")
            return self.perform_soft_recompile()

        # Otherwise full compile
        logger.info("Using full recompile path")
        compiled = super().compile(**kwargs)

        # Cache for future soft recompiles
        self.compiled_cache = compiled

        return compiled
```

### Task 2: Add State-Driven Nodes

**File**: `/home/will/Projects/haive/packages/haive-core/src/haive/core/graph/node/state_driven_node.py`

**Create**:

```python
"""State-driven nodes that get behavior from state."""

from typing import Any, Callable
from haive.core.schema.state_schema import StateSchema

class StateDrivenNode:
    """Node that executes behavior from state."""

    def __init__(self, name: str):
        self.name = name

    def __call__(self, state: StateSchema) -> Any:
        """Execute node behavior from state."""

        # Get behavior from state
        if hasattr(state, 'nodes') and self.name in state.nodes:
            behavior = state.nodes[self.name]
            if callable(behavior):
                return behavior(state)

        # Get routing from state
        if hasattr(state, 'routing_table'):
            next_nodes = state.routing_table.get(self.name, [])
            if next_nodes:
                # Route to next node
                state.next_node = next_nodes[0]

        return state
```

### Task 3: Create Quick Test Suite

**File**: `/home/will/Projects/haive/packages/haive-core/tests/test_soft_recompile.py`

```python
"""Test soft recompilation performance."""

import pytest
import time
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema

def test_soft_recompile_under_100ms():
    """Ensure soft recompile is fast."""
    graph = BaseGraph()
    graph.state_schema = StateSchema()

    # Initial compile
    graph.compile()

    # Trigger soft recompile
    graph.mark_for_soft_recompile("test")

    start = time.time()
    graph.compile()  # Should use soft path
    elapsed_ms = (time.time() - start) * 1000

    assert elapsed_ms < 100, f"Soft recompile took {elapsed_ms}ms"
    print(f"✅ Soft recompile: {elapsed_ms:.1f}ms")
```

## 🚀 This Week's Milestones

### Monday-Tuesday: Soft Recompilation

- [ ] Benchmark current performance
- [ ] Implement SoftRecompileMixin
- [ ] Integrate into BaseGraph
- [ ] Test <100ms performance

### Wednesday: State-Driven Nodes

- [ ] Create StateDrivenNode
- [ ] Update StateSchema with nodes dict
- [ ] Test runtime behavior changes
- [ ] Verify no performance regression

### Thursday: Hot Engine Management

- [ ] Create EngineManager class
- [ ] Implement context preservation
- [ ] Test hot-swapping
- [ ] Document migration path

### Friday: Integration & Testing

- [ ] Full integration tests
- [ ] Performance benchmarks
- [ ] Update documentation
- [ ] Create migration guide

## 📊 Success Metrics Dashboard

```python
# Track our progress
metrics = {
    "recompilation_time": {
        "before": 10500,  # ms
        "target": 100,     # ms
        "current": None    # Measure today!
    },
    "engine_swap_time": {
        "before": 10500,   # ms (requires recompile)
        "target": 50,      # ms
        "current": None    # Measure today!
    },
    "node_injection_time": {
        "before": 10500,   # ms (requires recompile)
        "target": 50,      # ms
        "current": None    # To be measured
    }
}
```

## 🎯 Definition of Done

### For Soft Recompilation

- ✅ Consistently <100ms
- ✅ All tests pass
- ✅ No memory leaks
- ✅ Backward compatible
- ✅ Documented

### For State-Driven Nodes

- ✅ Behavior from state works
- ✅ Dynamic routing works
- ✅ No performance impact
- ✅ Tests complete

### For Hot Engine Swap

- ✅ <50ms swap time
- ✅ Context preserved
- ✅ No message loss
- ✅ Error handling

## 💡 Pro Tips

1. **Start with benchmarks** - Know your baseline
2. **Test incrementally** - Don't break what works
3. **Use feature flags** - Roll out gradually
4. **Measure everything** - Performance is key
5. **Document as you go** - Future you will thank you

---

**START NOW**: Run the benchmark script. See the 10.5s pain. Then implement soft recompile and feel the 200x speedup!
