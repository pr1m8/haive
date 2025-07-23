# Import Performance Optimization

**Task**: Optimize import performance for Haive framework
**Solution**: Comprehensive lazy loading pattern
**Date**: 2025-01-23

## Problem

Import times were severely impacting developer experience:
- SimpleAgentV3: 30.7 seconds
- AugLLMConfig: ~20 seconds
- 5365 modules loaded including NumExpr/pandas

## Solution Pattern

Use module-level `__getattr__` for lazy loading:

```python
# Define what to lazy load
_LAZY_IMPORTS = {
    "HeavyClass": ("heavy.module.path", "ActualClassName"),
}

def __getattr__(name: str):
    """Lazy load heavy components."""
    if name in _LAZY_IMPORTS:
        module_path, class_name = _LAZY_IMPORTS[name]
        
        # Import only when accessed
        import importlib
        module = importlib.import_module(module_path)
        component = getattr(module, class_name)
        
        # Cache for subsequent access
        globals()[name] = component
        return component
    
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

# Include in __all__ for proper behavior
__all__ = ["HeavyClass", ...]
```

## Key Insights

1. **Import chains matter** - One import can trigger thousands
2. **langchain_community is heavy** - Embeddings loads numpy/pandas
3. **Auto-registries are expensive** - Defer until needed
4. **Transparent to users** - Works exactly the same from outside

## Files to Modify

1. **Core module** (`__init__.py`) - Lazy load heavy classes
2. **Engine module** - Defer document/embedding/vectorstore
3. **Models module** - Prevent submodule cascade
4. **Package roots** - Lazy load agent classes

## Testing

```bash
# Measure import time
python -X importtime -c "from haive.agents.simple import SimpleAgentV3" 2>&1 | grep "import time"

# Or simpler
python -c "import time; start=time.time(); from haive.agents.simple import SimpleAgentV3; print(f'{time.time()-start:.2f}s')"
```

## Results

- 87% improvement in import times
- Sub-5 second imports achieved
- No functionality changes

See full details: @memory_index/by_date/2025-01-23/lazy_loading_optimization.md