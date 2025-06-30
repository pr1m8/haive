# Enhanced Routing System

This module provides sophisticated routing capabilities for dynamic graph execution,
including type-hint based routing, conditional strategies, and parallel execution support.

## Overview

The enhanced routing system addresses key limitations:

- **Dynamic Type Resolution**: Routes determined from type hints and state values
- **No Hardcoded Literals**: Routes come from runtime state, not compile-time constants
- **Parallel Execution**: Native Send command support for concurrent processing
- **Validation Integration**: Routes validated against available nodes/types

## Core Components

### `RoutingEngine`

Central coordination for all routing decisions with caching and optimization.

### `RoutingStrategy` Implementations

- `DynamicTypeRoutingStrategy`: Routes based on type hints and state values
- `ConditionalRoutingStrategy`: Multi-condition routing with fallbacks
- `ParallelRoutingStrategy`: Send-based parallel execution routing
- `StateFieldRoutingStrategy`: Route from state field values

### `RouteValidator`

Validates routes exist and types match before execution.

### `TypeResolver`

Resolves type hints to actual route destinations.

## Integration Notes

**🚨 Schema Integration Required:**

- Connect with `/core/schema/schema_manager.py` for input/output validation
- Use existing schema composers for node type validation
- Bridge compatibility gap between schema systems

**🗂️ Organization Improvements Needed:**

- Consolidate routing logic scattered across packages
- Create clear hierarchy: generic → routing → haive-specific
- Reduce directory proliferation

## Usage

```python
from haive.core.graph.routing import RoutingEngine, DynamicTypeRoutingStrategy

# Create routing engine
engine = RoutingEngine()

# Add dynamic type routing
strategy = DynamicTypeRoutingStrategy(
    type_field_path="tool_routes",
    engine_path="engines.main"
)
engine.add_strategy("tool_routing", strategy)

# Route based on state
next_nodes = engine.route(state, result, node)
```
