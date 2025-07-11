"""Base Embedding Models Module.

This module provides the foundational abstractions for embedding models in the Haive framework.
It includes base classes and implementations for different embedding providers that transform
text into high-dimensional vector representations for use in semantic search, clustering,
and other NLP tasks.

Typical usage example:
    ```python
    from haive.core.models.embeddings.base import create_embeddings, HuggingFaceEmbeddingConfig

    # Create a HuggingFace embedding model configuration
    config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Instantiate the embeddings model
    embeddings = create_embeddings(config)

    # Use the model to embed documents or queries
    doc_embeddings = embeddings.embed_documents(["Text to embed"])
    ```
"""

import os
from typing import Any, Dict

import torch
from dotenv import load_dotenv
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_community.embeddings.anyscale import AnyscaleEmbeddings
from langchain_community.embeddings.bedrock import BedrockEmbeddings
from langchain_community.embeddings.cloudflare_workersai import (
    CloudflareWorkersAIEmbeddings,
)
from langchain_community.embeddings.cohere import CohereEmbeddings
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.embeddings.jina import JinaEmbeddings
from langchain_community.embeddings.llamacpp import LlamaCppEmbeddings
from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
from langchain_community.embeddings.voyageai import VoyageEmbeddings
from langchain_google_vertexai import VertexAIEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings
from pydantic import BaseModel, Field, SecretStr, field_validator

from haive.core.config.constants import EMBEDDINGS_CACHE_DIR
from haive.core.models.embeddings.provider_types import EmbeddingProvider

# Load environment variables from .env file if present
load_dotenv(".env")


class SecureConfigMixin:
    """Mixin for securely handling API keys from environment variables.

    This mixin provides methods for securely resolving API keys from environment
    variables or explicitly provided values, with appropriate fallbacks.
    """

    @field_validator("api_key", mode="after")
    @classmethod
    def resolve_api_key(cls, v, values):
        """Resolve API key from provided value or environment variables.

        Args:
            v: The provided API key value
            values: The other field values

        Returns:
            SecretStr: The resolved API key as a SecretStr
        """
        if v and v.get_secret_value().strip():
            return v

        provider = values.get("provider")
        if not provider:
            return SecretStr("")

        env_map = {
            "azure": "AZURE_OPENAI_API_KEY",
            "huggingface": "HUGGING_FACE_API_KEY",
            "openai": "OPENAI_API_KEY",
            "cohere": "COHERE_API_KEY",
            "jina": "JINA_API_KEY",
            "vertexai": "GOOGLE_API_KEY",
            "bedrock": "AWS_ACCESS_KEY_ID",
            "cloudflare": "CLOUDFLARE_API_TOKEN",
            "voyageai": "VOYAGE_API_KEY",
            "anyscale": "ANYSCALE_API_KEY",
            "novita": "NOVITA_API_KEY",
        }

        env_key = env_map.get(provider.value.lower())
        if env_key:
            key = os.getenv(env_key, "")
            if key.strip():
                return SecretStr(key)
        return SecretStr("")


class BaseEmbeddingConfig(BaseModel, SecureConfigMixin):
    """Base configuration for embedding models.

    This abstract base class defines the common interface for all embedding model
    configurations, ensuring consistent instantiation patterns across providers.

    Attributes:
        provider: The embedding provider (e.g., Azure, HuggingFace)
        model: The specific model identifier or name
        api_key: The API key for the provider (if required)
    """

    provider: EmbeddingProvider
    model: str
    api_key: SecretStr = Field(
        default=SecretStr(""), description="API key for the embedding provider"
    )

    def instantiate(self, **kwargs) -> Any:
        """Instantiate the embedding model with the configuration.

        Args:
            **kwargs: Additional keyword arguments to pass to the model constructor

        Returns:
            Any: The instantiated embedding model

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError


class AzureEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Azure OpenAI embedding models.

    This class configures embedding models from Azure OpenAI services,
    supporting environment variable resolution for credentials.

    Attributes:
        provider: Set to EmbeddingProvider.AZURE
        model: The Azure deployment name for the embedding model
        api_version: The Azure OpenAI API version to use
        api_base: The Azure endpoint URL
        api_type: The API type (typically "azure")
    """

    provider: EmbeddingProvider = EmbeddingProvider.AZURE

    api_version: str = Field(
        default_factory=lambda: os.getenv(
            "AZURE_OPENAI_API_VERSION", "2024-02-15-preview"
        ),
        description="Azure API version",
    )
    api_base: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_API_BASE", ""),
        description="Azure API endpoint",
    )
    api_type: str = Field(
        default_factory=lambda: os.getenv("AZURE_OPENAI_API_TYPE", "azure"),
        description="Azure API type",
    )

    def instantiate(self, **kwargs) -> AzureOpenAIEmbeddings:
        """Instantiate an Azure OpenAI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to AzureOpenAIEmbeddings

        Returns:
            AzureOpenAIEmbeddings: The instantiated embedding model
        """
        return AzureOpenAIEmbeddings(
            model=self.model,
            api_key=self.get_api_key(),
            api_version=self.api_version,
            azure_endpoint=self.api_base,
            **kwargs,
        )

    def get_api_key(self) -> str:
        """Get the API key as a string.

        Returns:
            str: The API key
        """
        return self.api_key.get_secret_value()


class HuggingFaceEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for HuggingFace embedding models.

    This class configures embedding models from HuggingFace's model hub,
    with support for local caching and hardware acceleration.

    Attributes:
        provider: Set to EmbeddingProvider.HUGGINGFACE
        model: The HuggingFace model ID (defaults to all-MiniLM-L6-v2)
        model_kwargs: Additional keyword arguments for model instantiation
        encode_kwargs: Additional keyword arguments for encoding
        query_encode_kwargs: Additional keyword arguments for query encoding
        multi_process: Whether to use multi-processing for encoding
        cache_folder: Where to cache the model files
        show_progress: Whether to show progress bars
        use_cache: Whether to use embedding caching
    """

    provider: EmbeddingProvider = EmbeddingProvider.HUGGINGFACE

    model_kwargs: dict[str, Any] | None = Field(
        default_factory=lambda: {
            "device": "cuda" if torch.cuda.is_available() else "cpu"
        },
        description="Additional keyword arguments for model instantiation",
    )
    model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="HuggingFace model ID",
    )
    encode_kwargs: dict[str, Any] | None = Field(
        default_factory=dict, description="Additional keyword arguments for encoding"
    )
    query_encode_kwargs: dict[str, Any] | None = Field(
        default_factory=dict,
        description="Additional keyword arguments for query encoding",
    )
    multi_process: bool = Field(
        default=False, description="Whether to use multi-processing for encoding"
    )
    cache_folder: str | None = Field(
        default=str(EMBEDDINGS_CACHE_DIR), description="Where to cache the model files"
    )
    show_progress: bool = Field(
        default=False, description="Whether to show progress bars"
    )
    use_cache: bool = Field(
        default=True, description="Whether to use embedding caching"
    )

    def instantiate(self, **kwargs) -> HuggingFaceEmbeddings:
        """Instantiate a HuggingFace embedding model.

        This method includes error handling and GPU memory cleanup
        in case of initialization failures.

        Args:
            **kwargs: Additional keyword arguments to pass to HuggingFaceEmbeddings

        Returns:
            HuggingFaceEmbeddings: The instantiated embedding model

        Raises:
            Exception: If model instantiation fails after cleanup attempt
        """
        try:
            embedder = HuggingFaceEmbeddings(
                model_name=self.model,
                model_kwargs=self.model_kwargs,
                encode_kwargs=self.encode_kwargs,
                multi_process=self.multi_process,
                cache_folder=self.cache_folder,
                show_progress=self.show_progress,
                **kwargs,
            )

            if self.use_cache:
                store = LocalFileStore(self.cache_folder)
                return CacheBackedEmbeddings.from_bytes_store(
                    embedder,
                    document_embedding_cache=store,
                    query_embedding_cache=True,
                    namespace=self.model,
                )
            return embedder

        except Exception:
            # If first attempt fails, try cleaning up GPU memory and retry
            try:
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
                embedder = HuggingFaceEmbeddings(
                    model_name=self.model,
                    model_kwargs=self.model_kwargs,
                    encode_kwargs=self.encode_kwargs,
                    multi_process=self.multi_process,
                    cache_folder=self.cache_folder,
                    show_progress=self.show_progress,
                    **kwargs,
                )
                if self.use_cache:
                    store = LocalFileStore(self.cache_folder)
                    return CacheBackedEmbeddings.from_bytes_store(
                        embedder,
                        document_embedding_cache=store,
                        query_embedding_cache=True,
                        namespace=self.model,
                    )
                return embedder
            except Exception:
                raise


class OpenAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for OpenAI embedding models.

    This class configures embedding models from OpenAI services,
    supporting multiple model types and configurations.

    Attributes:
        provider: Set to EmbeddingProvider.OPENAI
        model: The OpenAI model name for embeddings (defaults to text-embedding-3-small)
        dimensions: Output dimensions for the embedding vectors
        show_progress_bar: Whether to show progress bars during embedding
        chunk_size: Batch size for embedding operations
    """

    provider: EmbeddingProvider = EmbeddingProvider.OPENAI
    model: str = Field(
        default="text-embedding-3-small", description="OpenAI embedding model name"
    )
    dimensions: int | None = Field(
        default=None, description="Output dimensions for the embedding vectors"
    )
    show_progress_bar: bool = Field(
        default=False, description="Whether to show progress bars during embedding"
    )
    chunk_size: int = Field(
        default=1000, description="Batch size for embedding operations"
    )

    def instantiate(self, **kwargs) -> OpenAIEmbeddings:
        """Instantiate an OpenAI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to OpenAIEmbeddings

        Returns:
            OpenAIEmbeddings: The instantiated embedding model
        """
        embedding_kwargs = {
            "model": self.model,
            "openai_api_key": self.api_key.get_secret_value(),
            "chunk_size": self.chunk_size,
            "show_progress_bar": self.show_progress_bar,
        }

        if self.dimensions:
            embedding_kwargs["dimensions"] = self.dimensions

        return OpenAIEmbeddings(**embedding_kwargs, **kwargs)


class CohereEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Cohere embedding models.

    This class configures embedding models from Cohere services.

    Attributes:
        provider: Set to EmbeddingProvider.COHERE
        model: The Cohere model name for embeddings (defaults to embed-english-v3.0)
        input_type: Type of input to be embedded (defaults to search_document)
    """

    provider: EmbeddingProvider = EmbeddingProvider.COHERE
    model: str = Field(
        default="embed-english-v3.0", description="Cohere embedding model name"
    )
    input_type: str = Field(
        default="search_document", description="Type of input to be embedded"
    )

    def instantiate(self, **kwargs) -> CohereEmbeddings:
        """Instantiate a Cohere embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to CohereEmbeddings

        Returns:
            CohereEmbeddings: The instantiated embedding model
        """
        return CohereEmbeddings(
            model=self.model,
            cohere_api_key=self.api_key.get_secret_value(),
            input_type=self.input_type,
            **kwargs,
        )


class OllamaEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Ollama embedding models.

    This class configures embedding models from Ollama, which runs
    locally and doesn't require an API key.

    Attributes:
        provider: Set to EmbeddingProvider.OLLAMA
        model: The Ollama model name (defaults to nomic-embed-text)
        base_url: The base URL for the Ollama server
    """

    provider: EmbeddingProvider = EmbeddingProvider.OLLAMA
    model: str = Field(default="nomic-embed-text", description="Ollama model name")
    base_url: str = Field(
        default="http://localhost:11434", description="Base URL for the Ollama server"
    )

    def instantiate(self, **kwargs) -> OllamaEmbeddings:
        """Instantiate an Ollama embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to OllamaEmbeddings

        Returns:
            OllamaEmbeddings: The instantiated embedding model
        """
        return OllamaEmbeddings(
            model=self.model,
            base_url=self.base_url,
            **kwargs,
        )


class SentenceTransformerEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for SentenceTransformer embedding models.

    This class configures embedding models from SentenceTransformers library,
    which provides efficient and accurate sentence and text embeddings.

    Attributes:
        provider: Set to EmbeddingProvider.SENTENCE_TRANSFORMERS
        model: The model name or path (defaults to all-MiniLM-L6-v2)
        cache_folder: Where to cache the model files
        use_cache: Whether to use embedding caching
    """

    provider: EmbeddingProvider = EmbeddingProvider.SENTENCE_TRANSFORMERS
    model: str = Field(
        default="all-MiniLM-L6-v2", description="SentenceTransformer model name or path"
    )
    cache_folder: str | None = Field(
        default=str(EMBEDDINGS_CACHE_DIR), description="Where to cache the model files"
    )
    use_cache: bool = Field(
        default=True, description="Whether to use embedding caching"
    )

    def instantiate(self, **kwargs) -> SentenceTransformerEmbeddings:
        """Instantiate a SentenceTransformer embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to SentenceTransformerEmbeddings

        Returns:
            SentenceTransformerEmbeddings: The instantiated embedding model
        """
        embedder = SentenceTransformerEmbeddings(
            model_name=self.model,
            cache_folder=self.cache_folder,
            **kwargs,
        )

        if self.use_cache:
            store = LocalFileStore(self.cache_folder)
            return CacheBackedEmbeddings.from_bytes_store(
                embedder,
                document_embedding_cache=store,
                query_embedding_cache=True,
                namespace=self.model,
            )
        return embedder


class FastEmbedEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for FastEmbed embedding models.

    This class configures FastEmbed models, which are lightweight and efficient
    embeddings that can run on CPU.

    Attributes:
        provider: Set to EmbeddingProvider.FASTEMBED
        model: The model name (defaults to BAAI/bge-small-en-v1.5)
        max_length: Maximum sequence length
        cache_folder: Where to cache the model files
        use_cache: Whether to use embedding caching
    """

    provider: EmbeddingProvider = EmbeddingProvider.FASTEMBED
    model: str = Field(
        default="BAAI/bge-small-en-v1.5", description="FastEmbed model name"
    )
    max_length: int = Field(default=512, description="Maximum sequence length")
    cache_folder: str | None = Field(
        default=str(EMBEDDINGS_CACHE_DIR), description="Where to cache the model files"
    )
    use_cache: bool = Field(
        default=True, description="Whether to use embedding caching"
    )

    def instantiate(self, **kwargs) -> FastEmbedEmbeddings:
        """Instantiate a FastEmbed embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to FastEmbedEmbeddings

        Returns:
            FastEmbedEmbeddings: The instantiated embedding model
        """
        embedder = FastEmbedEmbeddings(
            model_name=self.model,
            max_length=self.max_length,
            cache_dir=self.cache_folder,
            **kwargs,
        )

        if self.use_cache:
            store = LocalFileStore(self.cache_folder)
            return CacheBackedEmbeddings.from_bytes_store(
                embedder,
                document_embedding_cache=store,
                query_embedding_cache=True,
                namespace=self.model,
            )
        return embedder


class JinaEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Jina AI embedding models.

    This class configures embedding models from Jina AI.

    Attributes:
        provider: Set to EmbeddingProvider.JINA
        model: The model name (defaults to jina-embeddings-v2-base-en)
    """

    provider: EmbeddingProvider = EmbeddingProvider.JINA
    model: str = Field(
        default="jina-embeddings-v2-base-en", description="Jina AI model name"
    )

    def instantiate(self, **kwargs) -> JinaEmbeddings:
        """Instantiate a Jina AI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to JinaEmbeddings

        Returns:
            JinaEmbeddings: The instantiated embedding model
        """
        return JinaEmbeddings(
            model_name=self.model,
            jina_api_key=self.api_key.get_secret_value(),
            **kwargs,
        )


class VertexAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Google Vertex AI embedding models.

    This class configures embedding models from Google Vertex AI.

    Attributes:
        provider: Set to EmbeddingProvider.VERTEXAI
        model: The model name (defaults to textembedding-gecko@latest)
        project: Google Cloud project ID
        location: Google Cloud region
    """

    provider: EmbeddingProvider = EmbeddingProvider.VERTEXAI
    model: str = Field(
        default="textembedding-gecko@latest", description="Vertex AI model name"
    )
    project: str | None = Field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        description="Google Cloud project ID",
    )
    location: str = Field(default="us-central1", description="Google Cloud region")

    def instantiate(self, **kwargs) -> VertexAIEmbeddings:
        """Instantiate a Google Vertex AI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to VertexAIEmbeddings

        Returns:
            VertexAIEmbeddings: The instantiated embedding model
        """
        return VertexAIEmbeddings(
            model_name=self.model,
            project=self.project,
            location=self.location,
            **kwargs,
        )


class BedrockEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for AWS Bedrock embedding models.

    This class configures embedding models from AWS Bedrock service.

    Attributes:
        provider: Set to EmbeddingProvider.BEDROCK
        model: The model ID (defaults to amazon.titan-embed-text-v1)
        region: AWS region
        credentials_profile_name: AWS credentials profile name
    """

    provider: EmbeddingProvider = EmbeddingProvider.BEDROCK
    model: str = Field(
        default="amazon.titan-embed-text-v1", description="AWS Bedrock model ID"
    )
    region: str = Field(
        default_factory=lambda: os.getenv("AWS_REGION", "us-east-1"),
        description="AWS region",
    )
    credentials_profile_name: str | None = Field(
        default=None, description="AWS credentials profile name"
    )

    def instantiate(self, **kwargs) -> BedrockEmbeddings:
        """Instantiate an AWS Bedrock embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to BedrockEmbeddings

        Returns:
            BedrockEmbeddings: The instantiated embedding model
        """
        config = {
            "model_id": self.model,
            "region_name": self.region,
        }

        if self.credentials_profile_name:
            config["credentials_profile_name"] = self.credentials_profile_name

        return BedrockEmbeddings(**config, **kwargs)


class CloudflareEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Cloudflare Workers AI embedding models.

    This class configures embedding models from Cloudflare Workers AI.

    Attributes:
        provider: Set to EmbeddingProvider.CLOUDFLARE
        model: The model name (defaults to @cf/baai/bge-small-en-v1.5)
        account_id: Cloudflare account ID
    """

    provider: EmbeddingProvider = EmbeddingProvider.CLOUDFLARE
    model: str = Field(
        default="@cf/baai/bge-small-en-v1.5",
        description="Cloudflare Workers AI model name",
    )
    account_id: str = Field(
        default_factory=lambda: os.getenv("CLOUDFLARE_ACCOUNT_ID", ""),
        description="Cloudflare account ID",
    )

    def instantiate(self, **kwargs) -> CloudflareWorkersAIEmbeddings:
        """Instantiate a Cloudflare Workers AI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to CloudflareWorkersAIEmbeddings

        Returns:
            CloudflareWorkersAIEmbeddings: The instantiated embedding model
        """
        return CloudflareWorkersAIEmbeddings(
            model_name=self.model,
            account_id=self.account_id,
            api_token=self.api_key.get_secret_value(),
            **kwargs,
        )


class LlamaCppEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for LlamaCpp local embedding models.

    This class configures embedding models using LlamaCpp for local execution.

    Attributes:
        provider: Set to EmbeddingProvider.LLAMACPP
        model: Required model name parameter (for compatibility with BaseEmbeddingConfig)
        model_path: Path to the model file
        n_ctx: Context size for the model
        n_batch: Batch size for inference
        n_gpu_layers: Number of layers to offload to GPU
    """

    provider: EmbeddingProvider = EmbeddingProvider.LLAMACPP
    model: str = Field(
        default="llama2", description="Model name (required for BaseEmbeddingConfig)"
    )
    model_path: str = Field(description="Path to the model file")
    n_ctx: int = Field(default=2048, description="Context size for the model")
    n_batch: int = Field(default=8, description="Batch size for inference")
    n_gpu_layers: int = Field(
        default=0, description="Number of layers to offload to GPU"
    )

    def instantiate(self, **kwargs) -> LlamaCppEmbeddings:
        """Instantiate a LlamaCpp embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to LlamaCppEmbeddings

        Returns:
            LlamaCppEmbeddings: The instantiated embedding model
        """
        return LlamaCppEmbeddings(
            model_path=self.model_path,
            n_ctx=self.n_ctx,
            n_batch=self.n_batch,
            n_gpu_layers=self.n_gpu_layers,
            **kwargs,
        )


class VoyageAIEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Voyage AI embedding models.

    This class configures embedding models from Voyage AI.

    Attributes:
        provider: Set to EmbeddingProvider.VOYAGEAI
        model: The model name (defaults to voyage-2)
        voyage_api_url: The API URL for Voyage AI
        voyage_api_version: The API version for Voyage AI
    """

    provider: EmbeddingProvider = EmbeddingProvider.VOYAGEAI
    model: str = Field(default="voyage-2", description="Voyage AI model name")
    voyage_api_url: str = Field(
        default="https://api.voyageai.com/v1/embeddings",
        description="Voyage AI API URL",
    )
    voyage_api_version: str = Field(
        default="2023-11-06", description="Voyage AI API version"
    )

    def instantiate(self, **kwargs) -> VoyageEmbeddings:
        """Instantiate a Voyage AI embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to VoyageEmbeddings

        Returns:
            VoyageEmbeddings: The instantiated embedding model
        """
        return VoyageEmbeddings(
            model_name=self.model,
            voyage_api_key=self.api_key.get_secret_value(),
            voyage_api_url=self.voyage_api_url,
            voyage_api_version=self.voyage_api_version,
            **kwargs,
        )


class AnyscaleEmbeddingConfig(BaseEmbeddingConfig):
    """Configuration for Anyscale embedding models.

    This class configures embedding models from Anyscale.

    Attributes:
        provider: Set to EmbeddingProvider.ANYSCALE
        model: The model name (defaults to thenlper/gte-large)
        base_url: The base URL for the Anyscale API
    """

    provider: EmbeddingProvider = EmbeddingProvider.ANYSCALE
    model: str = Field(default="thenlper/gte-large", description="Anyscale model name")
    base_url: str | None = Field(
        default=None, description="Base URL for the Anyscale API"
    )

    def instantiate(self, **kwargs) -> AnyscaleEmbeddings:
        """Instantiate an Anyscale embedding model.

        Args:
            **kwargs: Additional keyword arguments to pass to AnyscaleEmbeddings

        Returns:
            AnyscaleEmbeddings: The instantiated embedding model
        """
        config = {
            "model": self.model,
            "anyscale_api_key": self.api_key.get_secret_value(),
        }

        if self.base_url:
            config["anyscale_api_base"] = self.base_url

        return AnyscaleEmbeddings(**config, **kwargs)


def create_embeddings(config: BaseEmbeddingConfig) -> Any:
    """Factory function to create embedding models from a configuration.

    This function simplifies the instantiation of embedding models by
    delegating to the appropriate configuration class.

    Args:
        config: The embedding model configuration

    Returns:
        Any: The instantiated embedding model

    Example:
        ```python
        config = HuggingFaceEmbeddingConfig(model="sentence-transformers/all-mpnet-base-v2")
        embeddings = create_embeddings(config)
        ```
    """
    return config.instantiate()
