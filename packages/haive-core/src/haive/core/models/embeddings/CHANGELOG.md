# Embeddings Module Changelog

## 2025-06-19: Enhanced Embedding Providers

### Added

- Added 11 new embedding providers to the EmbeddingProvider enum:
  - OPENAI: OpenAI embedding models
  - COHERE: Cohere embedding models
  - OLLAMA: Ollama local embedding models
  - SENTENCE_TRANSFORMERS: Sentence Transformers embedding models
  - FASTEMBED: FastEmbed lightweight embedding models
  - JINA: Jina AI embedding models
  - VERTEXAI: Google Vertex AI embedding models
  - BEDROCK: AWS Bedrock embedding models
  - CLOUDFLARE: Cloudflare Workers AI embedding models
  - LLAMACPP: LlamaCPP local embedding models
  - VOYAGEAI: Voyage AI embedding models
  - ANYSCALE: Anyscale embedding models
  - NOVITA: NovitaAI embedding models

- Added corresponding configuration classes for all new providers:
  - OpenAIEmbeddingConfig
  - CohereEmbeddingConfig
  - OllamaEmbeddingConfig
  - SentenceTransformerEmbeddingConfig
  - FastEmbedEmbeddingConfig
  - JinaEmbeddingConfig
  - VertexAIEmbeddingConfig
  - BedrockEmbeddingConfig
  - CloudflareEmbeddingConfig
  - LlamaCppEmbeddingConfig
  - VoyageAIEmbeddingConfig
  - AnyscaleEmbeddingConfig

- Added enhanced API key resolution for all providers in the SecureConfigMixin
- Added comprehensive test suite for embedding providers
- Updated module documentation to include the new providers

### Organization Improvements

- Reorganized imports for better readability
- Categorized providers into cloud-based and local in the documentation
- Added consistent default models for each provider
- Standardized instantiation methods across all providers

### Future Improvements

- Implement NovitaEmbeddingConfig once an official implementation is available in langchain-community
- Add specific configuration models for additional parameters unique to each provider
- Implement embeddings registry similar to the VectorStoreProviderRegistry
- Add more examples for each embedding provider
- Enhance error handling for provider-specific issues
- Add support for model caching across all providers where applicable
