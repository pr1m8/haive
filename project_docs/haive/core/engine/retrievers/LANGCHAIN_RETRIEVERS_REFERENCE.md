# LangChain Retrievers Comprehensive Reference

## Overview

This document provides a comprehensive reference of all retrievers available in the LangChain ecosystem, including their purposes, deprecation status, and implementation notes for the Haive retriever provider system.

Generated from LangChain packages analysis on 2025-07-04.

## Core Retrievers (langchain-core)

### BaseRetriever

- **Purpose**: Abstract base class for all retrieval systems
- **Status**: Active - Foundation class
- **Usage**: All retrievers inherit from this
- **Implementation Priority**: ✅ Required for base provider

## Main LangChain Retrievers (langchain package)

### Advanced Strategy Retrievers

#### ContextualCompressionRetriever

- **Purpose**: Wraps a base retriever and compresses results using context
- **Status**: Active
- **Implementation Priority**: 🔥 High - Very useful for reducing token usage
- **Dependencies**: langchain
- **Use Case**: Compress retrieved documents to remove irrelevant parts

#### MultiQueryRetriever

- **Purpose**: Uses LLM to generate multiple queries from one input for better coverage
- **Status**: Active
- **Implementation Priority**: ✅ Implemented
- **Dependencies**: langchain
- **Use Case**: Improve retrieval by exploring query variations

#### MultiVectorRetriever

- **Purpose**: Retrieve from multiple embeddings for the same document
- **Status**: Active
- **Implementation Priority**: 🔥 High - Advanced strategy
- **Dependencies**: langchain
- **Use Case**: Use different embeddings for summaries, questions, etc.

#### ParentDocumentRetriever

- **Purpose**: Retrieve small chunks then fetch their parent documents
- **Status**: Active
- **Implementation Priority**: 🔥 High - Useful for maintaining context
- **Dependencies**: langchain
- **Use Case**: Index small chunks but return full documents

#### SelfQueryRetriever

- **Purpose**: Uses LLM to generate structured queries from natural language
- **Status**: Active
- **Implementation Priority**: 🔥 High - Smart query generation
- **Dependencies**: langchain
- **Use Case**: Convert natural language to structured filters

#### TimeWeightedVectorStoreRetriever

- **Purpose**: Combines embedding similarity with recency scoring
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Useful for time-sensitive data
- **Dependencies**: langchain
- **Use Case**: Favor recent documents in retrieval

#### RePhraseQueryRetriever

- **Purpose**: Uses LLM to rephrase queries before retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Similar to MultiQuery
- **Dependencies**: langchain
- **Use Case**: Improve query formulation

### Ensemble Retrievers

#### EnsembleRetriever

- **Purpose**: Combines multiple retrievers using rank fusion
- **Status**: Active
- **Implementation Priority**: ✅ Implemented
- **Dependencies**: langchain
- **Use Case**: Combine vector and keyword search

#### MergerRetriever

- **Purpose**: Simple merger of multiple retriever results
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Similar to Ensemble
- **Dependencies**: langchain
- **Use Case**: Combine results without rank fusion

## Community Retrievers (langchain-community)

### Sparse/Keyword Retrievers

#### BM25Retriever

- **Purpose**: Best Match 25 algorithm for keyword search
- **Status**: Active
- **Implementation Priority**: ✅ Implemented
- **Dependencies**: langchain-community
- **Use Case**: Traditional keyword-based search

#### TFIDFRetriever

- **Purpose**: Term Frequency-Inverse Document Frequency search
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Similar to BM25
- **Dependencies**: langchain-community
- **Use Case**: Statistical keyword matching

#### KNNRetriever

- **Purpose**: K-Nearest Neighbors search
- **Status**: Active
- **Implementation Priority**: 🔶 Medium
- **Dependencies**: langchain-community, sklearn
- **Use Case**: Simple similarity search

#### SVMRetriever

- **Purpose**: Support Vector Machine based retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Niche use case
- **Dependencies**: langchain-community, sklearn
- **Use Case**: Classification-based retrieval

#### ElasticSearchBM25Retriever

- **Purpose**: BM25 search using Elasticsearch
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - DB-specific
- **Dependencies**: langchain-community, elasticsearch
- **Use Case**: Elasticsearch-powered keyword search

### Vector Store Specific Retrievers

#### MilvusRetriever

- **Purpose**: Milvus vector database retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - DB-specific
- **Dependencies**: langchain-community, pymilvus
- **Use Case**: Milvus-optimized retrieval

#### PineconeHybridSearchRetriever

- **Purpose**: Hybrid search (vector + keyword) for Pinecone
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Popular vector DB
- **Dependencies**: langchain-community, pinecone
- **Use Case**: Pinecone's hybrid search capabilities

#### QdrantSparseVectorRetriever

- **Purpose**: Sparse vector search in Qdrant
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific to Qdrant sparse vectors
- **Dependencies**: langchain-community, qdrant-client
- **Use Case**: Qdrant sparse vector search

#### WeaviateHybridSearchRetriever

- **Purpose**: Hybrid search for Weaviate
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Popular vector DB
- **Dependencies**: langchain-community, weaviate-client
- **Use Case**: Weaviate's hybrid search

#### VespaRetriever

- **Purpose**: Vespa search engine retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Enterprise-focused
- **Dependencies**: langchain-community, pyvespa
- **Use Case**: Vespa search platform

#### ZepRetriever / ZepCloudRetriever

- **Purpose**: Zep memory store retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Memory-specific
- **Dependencies**: langchain-community, zep-python
- **Use Case**: Conversational memory retrieval

#### ZillizRetriever

- **Purpose**: Zilliz cloud vector database
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Cloud service specific
- **Dependencies**: langchain-community, pymilvus
- **Use Case**: Zilliz cloud service

### API-Based Retrievers

#### ArxivRetriever

- **Purpose**: Retrieve papers from arXiv
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Academic use
- **Dependencies**: langchain-community, arxiv
- **Use Case**: Academic paper retrieval

#### WikipediaRetriever

- **Purpose**: Retrieve articles from Wikipedia
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - General knowledge
- **Dependencies**: langchain-community, wikipedia
- **Use Case**: Encyclopedia knowledge retrieval

#### PubMedRetriever / PupMedRetriever

- **Purpose**: Medical literature from PubMed
- **Status**: Active (note: PupMed appears to be a typo)
- **Implementation Priority**: 🔶 Low - Medical domain specific
- **Dependencies**: langchain-community
- **Use Case**: Medical/scientific literature

#### TavilySearchAPIRetriever

- **Purpose**: Web search using Tavily API
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Web search
- **Dependencies**: langchain-community, tavily-python
- **Use Case**: Current web information retrieval

#### WebResearchRetriever

- **Purpose**: Web research using search engines
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Web research
- **Dependencies**: langchain-community
- **Use Case**: Comprehensive web research

#### YouRetriever

- **Purpose**: You.com search API
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific search engine
- **Dependencies**: langchain-community
- **Use Case**: You.com powered search

#### ChatGPTPluginRetriever

- **Purpose**: Retrieve from ChatGPT plugins
- **Status**: ⚠️ Potentially deprecated (plugins discontinued)
- **Implementation Priority**: ❌ Skip - Deprecated ecosystem
- **Dependencies**: langchain-community
- **Use Case**: ChatGPT plugin integration

### Cloud Service Retrievers

#### AzureAISearchRetriever

- **Purpose**: Azure Cognitive Search retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Major cloud provider
- **Dependencies**: langchain-community, azure-search-documents
- **Use Case**: Azure search service

#### BedrockRetriever

- **Purpose**: Amazon Bedrock knowledge bases
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - AWS service
- **Dependencies**: langchain-community, boto3
- **Use Case**: AWS Bedrock knowledge retrieval

#### GoogleCloudDocumentAIWarehouseRetriever

- **Purpose**: Google Cloud Document AI Warehouse
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific GCP service
- **Dependencies**: langchain-community, google-cloud-documentai
- **Use Case**: Google document processing

#### GoogleVertexAISearchRetriever

- **Purpose**: Google Vertex AI Search
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Google AI service
- **Dependencies**: langchain-community, google-cloud-discoveryengine
- **Use Case**: Google's enterprise search

#### KendraRetriever

- **Purpose**: Amazon Kendra enterprise search
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - AWS enterprise search
- **Dependencies**: langchain-community, boto3
- **Use Case**: AWS Kendra search service

### Specialized/Enterprise Retrievers

#### ArceeRetriever

- **Purpose**: Arcee AI retrieval service
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Arcee AI platform

#### AskNewsRetriever

- **Purpose**: AskNews API for news retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - News specific
- **Dependencies**: langchain-community
- **Use Case**: News article retrieval

#### BreebsRetriever

- **Purpose**: Breebs service integration
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Breebs platform integration

#### ChaindeskRetriever

- **Purpose**: Chaindesk knowledge base
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific platform
- **Dependencies**: langchain-community
- **Use Case**: Chaindesk integration

#### CohereRAGRetriever

- **Purpose**: Cohere's RAG retrieval service
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Major AI company
- **Dependencies**: langchain-community, cohere
- **Use Case**: Cohere's RAG service

#### DataberryRetriever

- **Purpose**: Databerry platform retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific platform
- **Dependencies**: langchain-community
- **Use Case**: Databerry integration

#### DocArrayRetriever

- **Purpose**: DocArray-based retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific framework
- **Dependencies**: langchain-community, docarray
- **Use Case**: DocArray ecosystem

#### DriaIndexRetriever

- **Purpose**: Dria index retrieval
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Dria platform

#### EmbedchainRetriever

- **Purpose**: Embedchain framework integration
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Alternative framework
- **Dependencies**: langchain-community, embedchain
- **Use Case**: Embedchain ecosystem

#### KayRetriever

- **Purpose**: Kay AI retrieval service
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Kay AI platform

#### LlamaIndexRetriever

- **Purpose**: LlamaIndex integration
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Popular framework
- **Dependencies**: langchain-community, llama-index
- **Use Case**: LlamaIndex ecosystem

#### MetalRetriever

- **Purpose**: Metal vector database
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific vector DB
- **Dependencies**: langchain-community, metal_sdk
- **Use Case**: Metal vector database

#### NanoPQRetriever

- **Purpose**: NanoPQ vector compression
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific compression
- **Dependencies**: langchain-community, nanopq
- **Use Case**: Compressed vector search

#### NeedleRetriever

- **Purpose**: Needle search service
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Needle platform

#### OutlineRetriever

- **Purpose**: Outline knowledge base
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific platform
- **Dependencies**: langchain-community
- **Use Case**: Outline integration

#### RemoteRetriever

- **Purpose**: Remote retriever service
- **Status**: Active
- **Implementation Priority**: 🔶 Medium - Generic remote access
- **Dependencies**: langchain-community
- **Use Case**: Remote retrieval services

#### RememberizerRetriever

- **Purpose**: Rememberizer memory service
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific service
- **Dependencies**: langchain-community
- **Use Case**: Memory service integration

#### ThirdAINeuralDBRetriever

- **Purpose**: ThirdAI's NeuralDB
- **Status**: Active
- **Implementation Priority**: 🔶 Low - Specific AI service
- **Dependencies**: langchain-community, thirdai
- **Use Case**: ThirdAI platform

## Implementation Priority Legend

- ✅ **Implemented**: Already implemented in our provider system
- 🔥 **High Priority**: Should implement next - high value/usage
- 🔶 **Medium Priority**: Consider implementing - moderate value
- 🔶 **Low Priority**: Implement if needed - niche use cases
- ❌ **Skip**: Don't implement - deprecated or redundant

## Recommended Implementation Order

### Phase 1 (Core Advanced Retrievers)

1. ContextualCompressionRetriever - Token optimization
2. ParentDocumentRetriever - Context preservation
3. SelfQueryRetriever - Smart querying
4. MultiVectorRetriever - Advanced embeddings

### Phase 2 (Popular Services)

1. CohereRAGRetriever - Major AI service
2. AzureAISearchRetriever - Cloud provider
3. KendraRetriever - AWS enterprise
4. GoogleVertexAISearchRetriever - Google AI

### Phase 3 (Alternative Sparse Methods)

1. TFIDFRetriever - Alternative to BM25
2. ElasticSearchBM25Retriever - Elasticsearch users
3. KNNRetriever - Simple similarity

### Phase 4 (Vector Store Specific)

1. PineconeHybridSearchRetriever - Popular vector DB
2. WeaviateHybridSearchRetriever - Popular vector DB
3. TimeWeightedVectorStoreRetriever - Time-aware retrieval

### Phase 5 (Knowledge Sources)

1. ArxivRetriever - Academic papers
2. WikipediaRetriever - General knowledge
3. TavilySearchAPIRetriever - Web search
4. WebResearchRetriever - Research workflows

## Notes for Implementation

### Common Patterns

- Most retrievers follow the BaseRetriever interface
- Many require external API keys or services
- Vector store specific retrievers often have hybrid capabilities
- Ensemble patterns are popular for combining different approaches

### Deprecation Monitoring

- ChatGPT plugins have been discontinued - avoid implementing
- Monitor cloud service retrievers for API changes
- Some specialized services may become deprecated

### Dependencies

- Core retrievers: langchain-core only
- Advanced retrievers: langchain package
- Specialized retrievers: langchain-community + service-specific packages
- Cloud retrievers: cloud SDKs (boto3, azure-_, google-cloud-_)

### Testing Strategy

- Mock external services for unit tests
- Integration tests with sandbox/test environments
- Performance tests for high-volume retrievers
- Error handling tests for network failures

## Architecture Notes

This reference should guide the continued development of the Haive retriever provider system. The modular pattern we've established can accommodate all of these retrievers while maintaining a consistent interface and proper error handling.

Key architectural decisions:

1. Lazy loading for optional dependencies
2. Provider registry for extensibility
3. Factory pattern for universal creation
4. Proper MRO ordering for mixins
5. Comprehensive error handling and logging
