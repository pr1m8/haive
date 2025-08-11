
:py:mod:`haive.core.engine.document.loaders.adapters`
========================

.. py:module:: haive.core.engine.document.loaders.adapters

.. autoapi-nested-parse::

   Document loader adapters for the Haive framework.

   This module provides adapter implementations that bridge different document
   loading approaches and normalize interfaces between various loader types.

   Adapters handle the translation between different loader interfaces, data
   formats, and execution patterns, ensuring consistent behavior across the
   document loading system.

   Key Components:
       BaseAdapter: Abstract base class for all loader adapters
       LocalAdapter: Adapter for local file system loaders

   Features:
       - Interface normalization between loader types
       - Data format translation and conversion
       - Error handling and retry logic
       - Performance optimization through caching
       - Consistent metadata handling

   .. admonition:: Examples

      Using a local file adapter::
      
          from haive.core.engine.document.loaders.adapters import LocalAdapter
      
          # Create adapter for local files
          adapter = LocalAdapter()
      
          # Load document through adapter
          documents = adapter.load("document.pdf")

   .. seealso::

      - Document loaders base classes
      - Source implementations
      - Loader registry system





Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.loaders.adapters.base   haive.core.engine.document.loaders.adapters.local
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/document/loaders/adapters/base/index   /api_clean/haive/core/engine/document/loaders/adapters/local/index





Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.adapters.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.document.loaders.adapters.BaseAdapter   haive.core.engine.document.loaders.adapters.LocalAdapter

.. automodule:: haive.core.engine.document.loaders.adapters
   :members:
   :undoc-members:
   :show-inheritance: