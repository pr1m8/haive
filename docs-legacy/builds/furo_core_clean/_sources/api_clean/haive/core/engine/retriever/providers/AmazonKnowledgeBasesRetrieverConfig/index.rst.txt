
haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig
=========================================================================

.. py:module:: haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig

.. autoapi-nested-parse::

   Amazon Knowledge Bases Retriever implementation for the Haive framework.

   from typing import Any
   This module provides a configuration class for the Amazon Knowledge Bases retriever,
   which uses AWS Bedrock Knowledge Bases for retrieval-augmented generation (RAG).
   Knowledge Bases provides a fully managed service that enables RAG workflows
   using foundation models with your data sources.

   The AmazonKnowledgeBasesRetriever works by:
   1. Connecting to an Amazon Bedrock Knowledge Base
   2. Performing semantic search using embeddings
   3. Retrieving relevant document chunks with metadata
   4. Supporting various data sources (S3, web crawling, etc.)

   This retriever is particularly useful when:
   - Building RAG applications with AWS Bedrock
   - Need managed vector storage and retrieval
   - Working with diverse data sources
   - Want serverless RAG infrastructure
   - Building enterprise AI applications on AWS

   The implementation integrates with LangChain's AmazonKnowledgeBasesRetriever while
   providing a consistent Haive configuration interface with secure AWS credential management.







Classes
-------

* :py:class:`AmazonKnowledgeBasesRetrieverConfig` - Configuration for Amazon Knowledge Bases retriever in the Haive framework.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/retriever/providers/AmazonKnowledgeBasesRetrieverConfig/AmazonKnowledgeBasesRetrieverConfig

Package Contents
----------------

