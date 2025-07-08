haive.core.engine.retriever
===========================

.. currentmodule:: haive.core.engine.retriever

.. automodule:: haive.core.engine.retriever
   :members:
   :undoc-members:
   :show-inheritance:
   :inherited-members:
   :private-members:
   :special-members: __init__, __call__

Classes
-------

.. .. autosummary::
..    :nosignatures:
   :toctree: _autosummary

Functions
---------

.. .. autosummary::
..    :nosignatures:
   :toctree: _autosummary

Engines
-------

.. toctree::
   :maxdepth: 1
   :caption: Available Engines
   :hidden:
   
   providers/index
   providers/vectorstore
   providers/multiquery
   providers/ensemble
   providers/contextual

Examples
--------

.. code-block:: python

   from haive.core.engine.retriever import RetrieverEngine
   from haive.core.engine.retriever.providers import VectorStoreRetrieverConfig
   from haive.core.engine.vectorstore.providers import ChromaVectorStoreConfig
   
   # Configure vector store
   vector_store_config = ChromaVectorStoreConfig(
       collection_name="documents",
       persist_directory="./chroma_db"
   )
   
   # Configure retriever
   retriever_config = VectorStoreRetrieverConfig(
       vector_store_config=vector_store_config,
       search_type="similarity",
       search_kwargs={"k": 5}
   )
   
   # Create retriever engine
   retriever = RetrieverEngine(config=retriever_config)
   
   # Retrieve documents
   docs = await retriever.aretrieve("What is machine learning?")

See Also
--------

- :doc:`/api/haive/core/index` - Package overview
- :doc:`/api/haive/core/engine/index` - Module overview
- :doc:`/api/haive/core/engine/vectorstore` - Vector store engines
- :doc:`/api/haive/core/models/retriever` - Retriever models
