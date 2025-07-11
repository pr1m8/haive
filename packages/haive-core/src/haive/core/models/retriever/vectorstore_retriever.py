import logging
from typing import Any, Dict

from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from haive.core.models.embeddings.base import (
    BaseEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
)
from haive.core.models.retriever.base import RetrieverConfig, RetrieverType
from haive.core.models.vectorstore.base import VectorStoreConfig

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


@RetrieverConfig.register(RetrieverType.VECTOR_STORE)
class VectorStoreRetrieverConfig(RetrieverConfig):
    """Configuration for a vector store retriever."""

    retriever_type: RetrieverType = Field(
        default=RetrieverType.VECTOR_STORE, description="The type of retriever"
    )

    # Required vector store configuration
    vector_store_config: VectorStoreConfig = Field(
        ...,  # This makes it required
        description="Configuration for the vector store to retrieve from",
    )

    # Embedding configuration with default
    embedding_config: BaseEmbeddingConfig | None = Field(
        default_factory=lambda: HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
        description="Optional embedding configuration",
    )

    # Number of documents to retrieve
    k: int = Field(
        default=4,
        ge=1,  # minimum of 1 document
        description="Number of documents to retrieve",
    )

    # Search configuration
    search_type: str = Field(
        default="similarity", description="Search type: 'similarity', 'mmr', etc."
    )

    search_kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Additional search parameters"
    )

    filter: dict[str, Any] | None = Field(
        default=None, description="Filter to apply to vector store search"
    )

    def instantiate(self) -> BaseRetriever:
        """Create a VectorStoreRetriever instance based on this configuration."""
        try:
            # Prepare embedding
            embeddings = self._get_embeddings()

            # Create vector store
            vector_store = self._create_vector_store(embeddings)

            # Prepare retriever
            retriever = self._create_retriever(vector_store)

            logger.info(
                f"Created VectorStoreRetriever '{self.name}' with search_type={self.search_type}"
            )
            return retriever

        except Exception as e:
            logger.exception(f"Error instantiating VectorStoreRetriever: {e!s}")
            raise ValueError(f"Failed to create VectorStoreRetriever: {e!s}")

    def _get_embeddings(self):
        """Prepare embeddings, with fallback to default."""
        try:
            # Prioritize embedding config from this instance
            if self.embedding_config:
                return self.embedding_config.instantiate()

            # Fallback to default Hugging Face embeddings
            return HuggingFaceEmbeddingConfig(
                model="sentence-transformers/all-mpnet-base-v2"
            ).instantiate()
        except Exception as e:
            logger.exception(f"Error creating embeddings: {e!s}")
            raise ValueError(f"Failed to create embeddings: {e!s}")

    def _create_vector_store(self, embeddings):
        """Create vector store with given embeddings."""
        try:
            # Ensure we have a vector store config
            if not self.vector_store_config:
                raise ValueError("No vector store configuration provided")

            # Create vector store
            return self.vector_store_config.get_vectorstore(embedding=embeddings)
        except Exception as e:
            logger.exception(f"Error creating vector store: {e!s}")
            raise ValueError(f"Failed to create vector store: {e!s}")

    def _create_retriever(self, vector_store):
        """Create retriever from vector store."""
        try:
            # Prepare search kwargs
            search_kwargs = {"k": self.k}
            if self.search_kwargs:
                search_kwargs.update(self.search_kwargs)

            # Add filter if provided
            extra_kwargs = {}
            if self.filter:
                extra_kwargs["filter"] = self.filter

            # Create retriever
            return vector_store.as_retriever(
                search_type=self.search_type,
                search_kwargs=search_kwargs,
                **extra_kwargs,
            )
        except Exception as e:
            logger.exception(f"Error creating retriever: {e!s}")
            raise ValueError(f"Failed to create retriever: {e!s}")

    def get_retriever(self) -> BaseRetriever:
        """Helper method to create and return the retriever."""
        return self.instantiate()
