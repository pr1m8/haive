
haive.core.engine.retriever.types
=================================

.. py:module:: haive.core.engine.retriever.types

.. autoapi-nested-parse::

   Types module for the Haive retriever engine.

   This module defines the core types and enumerations used throughout the retriever
   engine implementation. It provides a structured way to identify and categorize
   different retriever implementations available in the Haive framework.

   The main component of this module is the RetrieverType enum, which defines all
   supported retriever implementations and their categories. This helps in organizing
   and selecting appropriate retriever strategies for different use cases.

   .. admonition:: Example

      ```python
      from haive.core.engine.retriever.types import RetrieverType
      
      # Use specific retriever types
      vector_store_type = RetrieverType.VECTOR_STORE
      ensemble_type = RetrieverType.ENSEMBLE
      
      # Check retriever type
      if retriever_type == RetrieverType.MULTI_QUERY:
          print("Using multi-query retrieval strategy")
      ```







Classes
-------

* :py:class:`RetrieverType` - Enumeration of supported retriever types in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/types/RetrieverType

Package Contents
----------------

