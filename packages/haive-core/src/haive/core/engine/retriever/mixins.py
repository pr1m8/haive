# src/haive/core/engine/retriever/mixins.py

"""Retriever mixins for the Haive framework."""

from typing import Any, Dict, List, Optional, Union

from langchain_core.documents import Document
from pydantic import Field, field_validator

from haive.core.engine.retriever.retriever import (
    BaseRetrieverConfig,
    VectorStoreRetrieverConfig,
)
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig
from haive.core.models.embeddings.base import (
    BaseEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
)


class RetrieverMixin:
    """Mixin that provides retriever functionality with field validators and class methods.

    This mixin adds retriever capabilities to any class that inherits from it.
    It provides:
    - Field validator to automatically convert VectorStoreConfig to VectorStoreRetrieverConfig
    - Class methods to create instances with retrievers from various sources
    """

    @field_validator("engine", mode="before")
    @classmethod
    def convert_vectorstore_to_retriever(cls, v):
        """Convert VectorStoreConfig to VectorStoreRetrieverConfig if needed."""
        if isinstance(v, VectorStoreConfig):
            return VectorStoreRetrieverConfig(
                name=f"retriever_{v.name}", vector_store_config=v
            )
        return v

    @classmethod
    def from_vectorstore(
        cls,
        vector_store_config: VectorStoreConfig,
        retriever_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Create instance with a retriever from a vector store configuration.

        Args:
            vector_store_config: Vector store configuration
            retriever_kwargs: Additional kwargs for retriever creation
            **kwargs: Additional arguments for the class instance

        Returns:
            Instance with retriever created from vector store
        """
        retriever_config = VectorStoreRetrieverConfig(
            name=f"retriever_{vector_store_config.name}",
            vector_store_config=vector_store_config,
            **(retriever_kwargs or {}),
        )

        return cls(engine=retriever_config, **kwargs)

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        embedding_model: Optional[BaseEmbeddingConfig] = None,
        vector_store_provider: str = "FAISS",
        retriever_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        """Create instance with a retriever from documents.

        Args:
            documents: Documents to create vector store from
            embedding_model: Optional embedding model for the vector store
            vector_store_provider: Vector store provider to use
            retriever_kwargs: Additional kwargs for retriever creation
            **kwargs: Additional arguments for the class instance

        Returns:
            Instance with retriever created from documents
        """
        # Use a sensible default name if not provided
        if "name" not in kwargs:
            kwargs["name"] = cls.__name__

        # Use default embedding model if not provided
        if embedding_model is None:
            embedding_model = HuggingFaceEmbeddingConfig(
                model="sentence-transformers/all-mpnet-base-v2"
            )

        # Create vector store config from documents
        vs_config = VectorStoreConfig(
            name=kwargs.get("name", "document_vectorstore"),
            documents=documents,
            embedding_model=embedding_model,
            vector_store_provider=vector_store_provider,
        )

        # Create retriever config
        retriever_config = VectorStoreRetrieverConfig(
            name=f"retriever_{vs_config.name}",
            vector_store_config=vs_config,
            **(retriever_kwargs or {}),
        )

        return cls(engine=retriever_config, **kwargs)

    @classmethod
    def from_retriever(cls, retriever_config: BaseRetrieverConfig, **kwargs):
        """Create instance with a retriever configuration.

        Args:
            retriever_config: Retriever configuration
            **kwargs: Additional arguments for the class instance

        Returns:
            Instance with the specified retriever
        """
        return cls(engine=retriever_config, **kwargs)
