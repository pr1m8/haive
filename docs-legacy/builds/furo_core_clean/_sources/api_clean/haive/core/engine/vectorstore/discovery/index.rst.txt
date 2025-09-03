
haive.core.engine.vectorstore.discovery
=======================================

.. py:module:: haive.core.engine.vectorstore.discovery

.. autoapi-nested-parse::

   Vector Store Provider Discovery and Management.

   This module provides utilities for discovering, comparing, and configuring
   vector store providers within the Haive framework. It offers comprehensive
   information about all available vector store backends.

   .. admonition:: Examples

      Basic discovery::
      
          from haive.core.engine.vectorstore.discovery import get_vectorstore_providers
      
          providers = get_vectorstore_providers()
          print(f"Available: {list(providers.keys())}")
      
      Get provider recommendations::
      
          from haive.core.engine.vectorstore.discovery import recommend_vectorstore
      
          # For development
          dev_stores = recommend_vectorstore("development")
          print(f"For development: {dev_stores}")
      
          # For production
          prod_stores = recommend_vectorstore("production")
          print(f"For production: {prod_stores}")






Functions
---------

   get_vectorstore_providers   filter_vectorstores   recommend_vectorstore   get_setup_instructions   compare_vectorstores
.. autofunction:: get_vectorstore_providers
.. autofunction:: filter_vectorstores
.. autofunction:: recommend_vectorstore
.. autofunction:: get_setup_instructions
.. autofunction:: compare_vectorstores

Classes
-------

* :py:class:`VectorStoreType` - Categories of vector stores.* :py:class:`CostTier` - Cost structure for vector stores.* :py:class:`VectorStoreInfo` - Comprehensive information about a vector store provider.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/vectorstore/discovery/VectorStoreType   /api_clean/haive/core/engine/vectorstore/discovery/CostTier   /api_clean/haive/core/engine/vectorstore/discovery/VectorStoreInfo

Package Contents
----------------

