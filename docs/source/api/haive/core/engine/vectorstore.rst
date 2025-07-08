haive.core.engine.vectorstore
=============================

.. currentmodule:: haive.core.engine.vectorstore

.. automodule:: haive.core.engine.vectorstore
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
   providers/chroma
   providers/faiss
   providers/qdrant
   providers/pinecone
   providers/pgvector

Examples
--------

.. code-block:: python

   from haive.core.engine.vectorstore import VectorStoreEngine
   from haive.core.engine.vectorstore.providers import ChromaVectorStoreConfig
   from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig
   from haive.core.models.embeddings import create_embeddings
   
   # Create embeddings
   embeddings = create_embeddings(
       OpenAIEmbeddingConfig(model="text-embedding-3-small")
   )
   
   # Configure vector store
   config = ChromaVectorStoreConfig(
       collection_name="documents",
       persist_directory="./chroma_db"
   )
   
   # Create vector store engine
   vector_store = VectorStoreEngine(
       config=config,
       embeddings=embeddings
   )
   
   # Add documents
   await vector_store.aadd_documents([
       {"text": "Document 1", "metadata": {"source": "file1.txt"}},
       {"text": "Document 2", "metadata": {"source": "file2.txt"}}
   ])
   
   # Search
   results = await vector_store.asimilarity_search("query text", k=5)

See Also
--------

- :doc:`/api/haive/core/index` - Package overview
- :doc:`/api/haive/core/engine/index` - Module overview
- :doc:`/api/haive/core/engine/embedding` - Embedding engines
- :doc:`/api/haive/core/models/vectorstore` - Vector store models
