
haive.core.engine.retriever.providers.NeuralDBRetrieverConfig
=============================================================

.. py:module:: haive.core.engine.retriever.providers.NeuralDBRetrieverConfig

.. autoapi-nested-parse::

   NeuralDB Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the NeuralDB retriever,
   which uses ThirdAI's NeuralDB for fast neural search without GPUs.
   NeuralDB provides efficient neural information retrieval with CPU-only
   inference and training capabilities.

   The NeuralDBRetriever works by:
   1. Using ThirdAI's NeuralDB engine for neural search
   2. Performing efficient CPU-based neural retrieval
   3. Supporting fast training and inference
   4. Enabling neural search without GPU requirements

   This retriever is particularly useful when:
   - Need neural search without GPU infrastructure
   - Want fast CPU-based neural retrieval
   - Building cost-effective neural search systems
   - Need efficient training on CPU
   - Using ThirdAI's NeuralDB platform

   The implementation integrates with LangChain's NeuralDBRetriever while
   providing a consistent Haive configuration interface with secure API key management.







Classes
-------

* :py:class:`NeuralDBRetrieverConfig` - Configuration for NeuralDB retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/NeuralDBRetrieverConfig/NeuralDBRetrieverConfig

Package Contents
----------------

