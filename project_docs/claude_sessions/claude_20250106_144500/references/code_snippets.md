# Code Snippets - Autosummary Fix

## Manual Module Page Template

### Core Module Template
```rst
haive.core.module_name
=====================

.. py:module:: haive.core.module_name

.. currentmodule:: haive.core.module_name

.. raw:: html

   <div class="module-path" style="margin-bottom: 1rem; color: var(--color-foreground-secondary);">
      <code>haive.core.module_name</code>
   </div>

.. automodule:: haive.core.module_name
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :special-members: __init__, __call__, __new__
   :imported-members:
   :exclude-members: logger
```

## Gallery Card Update Pattern

### Before (Broken)
```rst
.. grid-item-card:: 🤖 **Engine System**
   :link: generated/haive.core.engine
   :link-type: doc
```

### After (Working)
```rst
.. grid-item-card:: 🤖 **Engine System**
   :link: modules/haive.core.engine
   :link-type: doc
```

## Toctree Replacement

### Before (Autosummary)
```rst
.. autosummary::
   :toctree: generated
   :template: module.rst
   :nosignatures:

   haive.core.engine
   haive.core.schema
   haive.core.persistence
```

### After (Manual Toctree)
```rst
.. toctree::
   :maxdepth: 2

   modules/haive.core.engine
   modules/haive.core.schema
   modules/haive.core.persistence
   modules/haive.core.registry
   modules/haive.core.tools
```

## Testing Commands

### Verify Module Import
```bash
python -c "import haive.core.engine; print(dir(haive.core.engine))"
```

### Build Single Module Page
```bash
poetry run sphinx-build -b html docs/source docs/build docs/source/api/modules/haive.core.engine.rst
```

### Debug Module Detection
```python
import haive.core.engine as engine_module
print('Module name:', engine_module.__name__)
print('Module file:', engine_module.__file__)
print('Is package:', hasattr(engine_module, '__path__'))
print('Has __all__:', hasattr(engine_module, '__all__'))
if hasattr(engine_module, '__all__'):
    print('__all__:', engine_module.__all__)
```

## Scaling Pattern

To apply this fix to other packages:

1. **Create manual module directory**: `/docs/source/api/modules/`
2. **Create module pages** using the template above
3. **Update gallery links** from `generated/` to `modules/`
4. **Replace autosummary** with manual toctree
5. **Test build** to verify full documentation appears