# Lazy Loading Optimization - 2025-01-23

**Type**: Performance Optimization
**Impact**: Major - 87% import time reduction
**Status**: Completed and Deployed

## Quick Summary

Reduced SimpleAgentV3 import time from 30.7s to 4.59s by implementing comprehensive lazy loading across haive-core and haive-agents packages.

## Key Changes

1. **haive.core** - Made all heavy imports lazy (AugLLMConfig, Engine, etc.)
2. **haive.core.engine** - Deferred agent, document, embedding, vectorstore components
3. **haive.core.models** - Prevented numpy/pandas loading from embeddings
4. **haive.agents** - Made all agent classes lazy-loaded
5. **haive.agents.simple** - Lazy loading for SimpleAgent variants

## Full Documentation

See: [Lazy Loading Optimization Details](../../sessions/active/lazy_loading_optimization_2025-01-23.md)

## Code Pattern

```python
# Module-level lazy loading pattern used throughout
_LAZY_IMPORTS = {
    "Component": ("module.path", "ClassName"),
}

def __getattr__(name: str):
    if name in _LAZY_IMPORTS:
        module_path, class_name = _LAZY_IMPORTS[name]
        import importlib
        module = importlib.import_module(module_path)
        component = getattr(module, class_name)
        globals()[name] = component  # Cache
        return component
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
```

## Commits

- **haive-core**: `b4e66d1` - feat(haive-core): implement comprehensive lazy loading for import performance
- **haive-agents**: `b4f9f1e` - feat(haive-agents): implement lazy loading for import performance
