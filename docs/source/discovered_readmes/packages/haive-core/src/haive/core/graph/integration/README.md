# Graph System Integration

This module provides seamless integration between the existing BaseGraph system and the new GenericGraph architecture, enabling gradual migration while preserving all existing functionality.

## Overview

The integration system solves the compatibility challenge by:

- **Bridging Systems**: HybridGraph extends GenericGraph with BaseGraph compatibility
- **Protocol Adaptation**: Automatic NodeConfig → NodeProtocol conversion
- **Migration Tools**: Utilities for moving from BaseGraph to GenericGraph
- **Fallback Support**: Graceful degradation to BaseGraph when needed

## Core Components

### `HybridGraph`

Main integration class that extends GenericGraph while supporting BaseGraph patterns:

```python
# Import existing agent graph
base_graph = agent.build_graph()
hybrid_graph = HybridGraph("agent_graph", base_graph=base_graph)

# Use with both systems
hybrid_graph.add_node_from_config(engine_node_config)  # BaseGraph style
hybrid_graph.add_node(generic_node)                    # GenericGraph style
```

### `GraphMigrationUtility`

Tools for systematic migration between systems:

```python
# Migrate agent graphs
hybrid_graph = GraphMigrationUtility.migrate_agent_graph(agent)

# Validate migration
report = GraphMigrationUtility.validate_migration(base_graph, hybrid_graph)
```

## Integration Benefits

**Immediate Compatibility:**

- ✅ Existing agents work unchanged
- ✅ All NodeConfig types supported
- ✅ BaseGraph features preserved
- ✅ New GenericGraph capabilities available

**Migration Support:**

- ✅ Gradual migration path
- ✅ Validation and reporting
- ✅ Fallback mechanisms
- ✅ No breaking changes required

**Enhanced Capabilities:**

- ✅ Better type safety from GenericGraph
- ✅ Performance optimizations
- ✅ Flexible execution strategies
- ✅ Advanced validation features

## Usage Patterns

### Agent Migration

```python
from haive.core.graph.integration import migrate_base_graph

class MyAgent(Agent):
    def build_enhanced_graph(self) -> HybridGraph:
        # Get existing graph
        base_graph = self.build_graph()

        # Migrate to hybrid
        return migrate_base_graph(base_graph)
```

### Dual System Support

```python
from haive.core.graph.integration import create_hybrid_graph

# Create hybrid graph
graph = create_hybrid_graph("dual_system")

# Add BaseGraph-style nodes
graph.add_node_from_config(EngineNodeConfig(...))

# Add GenericGraph-style nodes
graph.add_node(MyGenericNode(...))

# Execute with compatibility
result = graph.execute_with_base_graph_compatibility(state)
```

## Schema Integration Notes

**Current Status**: Protocol bridge complete, schema integration deferred
**Rationale**: Schema system is complex, addressed in separate phase
**Compatibility**: Basic validation works, full schema integration planned

## Future Enhancements

- [ ] Complete schema system integration
- [ ] Performance optimization for hybrid execution
- [ ] Extended validation capabilities
- [ ] Advanced migration reporting
- [ ] Automated migration suggestions
