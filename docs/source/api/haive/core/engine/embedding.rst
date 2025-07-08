Embedding Engine
================

Embedding engine implementations.

.. currentmodule:: haive.core.engine.embedding

Overview
--------

The embedding engine provides a unified interface for various embedding models through
engine implementations in the ``providers`` submodule.

Engine Implementation
---------------------

.. automodule:: haive.core.engine.embedding
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
   providers/openai
   providers/huggingface
   providers/cohere
   providers/ollama

Examples
--------

.. code-block:: python

   from haive.core.engine.embedding import EmbeddingEngine
   from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig
   
   # Create embedding configuration
   config = OpenAIEmbeddingConfig(
       model="text-embedding-3-small",
       dimensions=1536
   )
   
   # Create engine
   engine = EmbeddingEngine(config)
   
   # Generate embeddings
   embeddings = await engine.aembed_documents(["text1", "text2"])

See Also
--------

- :doc:`/api/haive/core/index` - Package overview
- :doc:`/api/haive/core/engine/index` - Module overview
- :doc:`providers/index` - All embedding engines
- :doc:`/api/haive/core/models/embeddings` - Embedding model configurations