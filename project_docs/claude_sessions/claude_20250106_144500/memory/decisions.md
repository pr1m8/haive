# Decision: Replace Autosummary with Manual Module Pages

**Rationale**: Autosummary `:recursive:` flag consistently treats submodules as attributes rather than full modules, generating `.. autodata::` instead of `.. automodule::` directives.

**Trade-offs**: 
- **Pro**: Manual approach works reliably and shows full documentation
- **Pro**: Easy to scale and maintain
- **Con**: Requires manual creation of module pages
- **Con**: Not automatic like autosummary

**Alternative Considered**: Fix autosummary configuration
- **Rejected because**: Multiple attempts to fix autosummary failed
- **Root issue**: Deep problem with how autosummary interprets namespaced modules

## Implementation Pattern

### Manual Module Page Template
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

### Gallery Update Pattern
```rst
.. grid-item-card:: 🤖 **Module Name**
   :link: modules/haive.core.module_name
   :link-type: doc
```

## Files Changed
- Created: `/docs/source/api/modules/haive.core.engine.rst`
- Created: `/docs/source/api/modules/haive.core.schema.rst`
- Created: `/docs/source/api/modules/haive.core.persistence.rst`
- Created: `/docs/source/api/modules/haive.core.registry.rst`
- Created: `/docs/source/api/modules/haive.core.tools.rst`
- Modified: `/docs/source/api/haive-core.rst` (updated gallery links and removed autosummary)