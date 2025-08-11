
haive.core.engine.retriever.providers.BedrockRetrieverConfig
============================================================

.. py:module:: haive.core.engine.retriever.providers.BedrockRetrieverConfig

.. autoapi-nested-parse::

   Amazon Bedrock Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Amazon Bedrock retriever,
   which uses AWS Bedrock's foundation models for retrieval tasks. Bedrock provides
   access to foundation models from various providers (Anthropic, AI21, etc.) and
   can be used for retrieval-augmented generation workflows.

   The BedrockRetriever works by:
   1. Connecting to Amazon Bedrock service
   2. Using foundation models for embedding generation
   3. Performing semantic search using model-generated embeddings
   4. Supporting various foundation model providers

   This retriever is particularly useful when:
   - Building RAG applications with AWS Bedrock
   - Need access to multiple foundation model providers
   - Want managed AI model infrastructure
   - Building enterprise applications on AWS
   - Need consistent API across different model providers

   The implementation integrates with LangChain's BedrockRetriever while
   providing a consistent Haive configuration interface with secure AWS credential management.







Classes
-------

* :py:class:`BedrockRetrieverConfig` - Configuration for Amazon Bedrock retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/BedrockRetrieverConfig/BedrockRetrieverConfig

Package Contents
----------------

