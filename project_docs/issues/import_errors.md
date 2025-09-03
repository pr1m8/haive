# Import and Module Resolution Issues

**Date**: August 1, 2025
**Priority**: HIGH - Multiple modules failing
**Status**: Open

## Problem

Multiple import errors preventing documentation generation:

### Missing External Dependencies

- `google-search-results` package not installed
- Affects: haive.agents.planning, haive.tools.google.google_finance

### Module Not Found Errors

- `haive.agents.multi.base_multi_agent`
- `haive.core.graph.state_graph.compiled_state_graph`
- `haive.core.engine.base.agent_types`
- `agents.web_nav`

### Import Errors

- Cannot import 'as_str' from haive.agents.research.storm.outline_generator.models
- Cannot import 'build_graph' from haive.agents.archive.meta.agent
- Cannot import 'complex_rag' from haive.agents.chain.chain_examples

## Root Causes

1. **Missing dependencies** in pyproject.toml
2. **Removed/renamed modules** still being imported
3. **Circular imports** in some modules
4. **Lazy loading issues** with provider classes

## Proposed Solutions

### 1. Install Missing Dependencies

```bash
poetry add google-search-results
```

### 2. Add to autodoc_mock_imports

Already handled by import diagnostics, but may need manual additions:

```python
autodoc_mock_imports.extend([
    "serpapi",
    "google_search_results",
    "agents.web_nav",
])
```

### 3. Fix Module References

- Update imports to use correct module paths
- Remove imports for deleted modules
- Fix circular imports with TYPE_CHECKING

### 4. Handle Lazy Loading

The force_load_lazy_imports() function in conf.py helps but may need expansion

## Files to Check

- `/packages/haive-agents/src/haive/agents/planning/` - google finance imports
- `/packages/haive-agents/src/haive/agents/research/storm/` - as_str import
- `/packages/haive-agents/src/haive/agents/chain/` - complex_rag import

## Testing

```bash
# Test imports directly
poetry run python -c "import haive.agents.planning"
```

## Success Criteria

- All modules import successfully
- No ModuleNotFoundError in docs build
- External dependencies properly mocked
