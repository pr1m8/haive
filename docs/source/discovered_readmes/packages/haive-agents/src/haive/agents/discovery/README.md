# Haive Discovery Module

**Parent Documentation**: [CLAUDE_DISCOVERY_SYSTEM.md](/home/will/Projects/haive/backend/haive/CLAUDE_DISCOVERY_SYSTEM.md)

## Overview

The discovery module provides intelligent component discovery and selection capabilities for Haive agents. It implements semantic search, capability matching, and dynamic selection patterns inspired by LangGraph.

## Module Structure

```
discovery/
├── __init__.py                    # Public API exports
├── semantic_discovery.py          # Core semantic discovery engine
├── dynamic_tool_selector.py       # LangGraph-style dynamic selection
├── selection_strategies.py        # Various selection strategies
└── README.md                      # This file
```

## Components

### SemanticDiscoveryEngine (`semantic_discovery.py`)

Main discovery engine combining vector search, query analysis, and capability matching.

**Key Classes:**

- `SemanticDiscoveryEngine` - Main entry point
- `VectorBasedToolSelector` - Handles embedding-based search
- `QueryAnalyzer` - Analyzes natural language queries
- `CapabilityMatcher` - Matches tools by capabilities

**Usage:**

```python
from haive.agents.discovery import SemanticDiscoveryEngine

engine = SemanticDiscoveryEngine()
tools, analysis = await engine.semantic_tool_selection(
    "Search web data and analyze trends",
    max_tools=5
)
```

### DynamicToolSelector (`dynamic_tool_selector.py`)

Implements LangGraph-style dynamic tool selection with state awareness.

**Key Classes:**

- `DynamicToolSelector` - Base selector interface
- `LangGraphStyleSelector` - LangGraph pattern implementation
- `ContextAwareSelector` - Context-based selection
- `ToolUsageTracker` - Tracks tool performance

**Usage:**

```python
from haive.agents.discovery import LangGraphStyleSelector

selector = LangGraphStyleSelector(available_tools=tools)
result = await selector.select_tools_with_state({
    "task": "research",
    "context": "academic",
    "history": ["searched_papers"]
})
```

### Selection Strategies (`selection_strategies.py`)

Pluggable strategies for component selection.

**Available Strategies:**

1. `SemanticSelectionStrategy` - Embedding similarity based
2. `CapabilityBasedStrategy` - Exact capability matching
3. `AdaptiveSelectionStrategy` - Learns from usage
4. `ContextualSelectionStrategy` - Uses conversation context
5. `EnsembleSelectionStrategy` - Combines multiple strategies

**Usage:**

```python
from haive.agents.discovery import AdaptiveSelectionStrategy

strategy = AdaptiveSelectionStrategy(
    learning_rate=0.1,
    exploration_rate=0.2
)

# Use with discovery engine
engine = SemanticDiscoveryEngine(selection_strategy=strategy)
```

## Integration with Core Registry

The discovery module builds on top of `haive.core.registry`:

```python
from haive.core.registry import create_component_registry
from haive.agents.discovery import SemanticDiscoveryEngine

# Registry provides storage and indexing
registry = create_component_registry()

# Discovery adds intelligent search
engine = SemanticDiscoveryEngine(component_registry=registry)
```

## Advanced Features

### Query Analysis

```python
analyzer = QueryAnalyzer()
analysis = analyzer.analyze_query("search for AI papers and summarize")
# Returns: keywords, capabilities, domain tags, complexity score
```

### Capability Matching

```python
matcher = CapabilityMatcher()
matcher.build_capability_matrix(tools)
matches = matcher.match_tools(
    required_capabilities=["search", "summarize"],
    optional_capabilities=["async"]
)
```

### Performance Tracking

```python
tracker = ToolUsageTracker()
tracker.record_usage("web_search", success=True, duration=1.2)
performance = tracker.get_tool_performance("web_search")
```

## Configuration

### Environment Variables

```bash
# Discovery-specific settings
HAIVE_DISCOVERY_DEFAULT_STRATEGY=hybrid
HAIVE_DISCOVERY_MAX_TOOLS=10
HAIVE_DISCOVERY_SIMILARITY_THRESHOLD=0.7
```

### Programmatic Configuration

```python
config = {
    "vector_selector": {
        "similarity_threshold": 0.7,
        "max_tools": 5
    },
    "query_analyzer": {
        "enable_query_expansion": True,
        "use_synonyms": True
    },
    "selection_strategy": {
        "type": "ensemble",
        "weights": {
            "semantic": 0.4,
            "capability": 0.3,
            "contextual": 0.3
        }
    }
}

engine = SemanticDiscoveryEngine(**config)
```

## Testing

### Unit Tests

```bash
poetry run pytest packages/haive-agents/tests/discovery/ -v
```

### Test Coverage

- `test_semantic_discovery.py` - Core engine tests
- `test_dynamic_tool_selector.py` - Dynamic selection tests
- `test_selection_strategies.py` - Strategy implementations

## Performance Considerations

1. **Embedding Computation**: Cache embeddings for frequently used components
2. **Vector Search**: Use appropriate similarity thresholds
3. **Memory Usage**: ~100MB per 1000 components with embeddings
4. **Search Time**: <50ms for semantic search on 10k components

## Common Patterns

### Tool Discovery for Agents

```python
class ResearchAgent:
    def __init__(self):
        self.discovery = SemanticDiscoveryEngine()

    async def select_tools_for_task(self, task: str):
        tools, _ = await self.discovery.semantic_tool_selection(
            task,
            strategy=ToolSelectionStrategy.HYBRID
        )
        return tools
```

### Dynamic Tool Binding

```python
async def bind_tools_dynamically(llm, query):
    selector = LangGraphStyleSelector()
    result = await selector.select_tools_for_query(query)

    # Bind selected tools to LLM
    llm_with_tools = llm.bind_tools(result.selected_tools)
    return llm_with_tools
```

### Capability-First Selection

```python
async def get_tools_for_workflow(workflow_steps):
    engine = SemanticDiscoveryEngine()
    workflow_tools = []

    for step in workflow_steps:
        tools = await engine.get_tools_for_capabilities(
            required_capabilities=step.required_capabilities,
            optional_capabilities=step.optional_capabilities
        )
        workflow_tools.extend(tools)

    return workflow_tools
```

## Troubleshooting

### Issue: No tools returned

- Check if tools are registered in the component registry
- Verify embedding provider is configured
- Try broader search queries

### Issue: Wrong tools selected

- Adjust similarity threshold
- Improve tool descriptions and capability metadata
- Use capability-based strategy for precise matching

### Issue: Slow search performance

- Disable embeddings for keyword-only search
- Limit search scope with component_types parameter
- Use caching for repeated queries

## Future Enhancements

1. **Memory Integration**: Cross-session tool preferences
2. **Tool Versioning**: Support for multiple tool versions
3. **Feedback Loop**: Learn from tool execution results
4. **Discovery UI**: Visual tool exploration interface

## Related Documentation

- [Component Registry](../../core/registry/README.md)
- [Discovery System Guide](../../../../../CLAUDE_DISCOVERY_SYSTEM.md)
- [Agent Development](../../../../../CLAUDE_AGENTS.md)
