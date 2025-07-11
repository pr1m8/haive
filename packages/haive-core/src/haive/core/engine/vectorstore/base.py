"""Base vector store configuration for the Haive framework.

This module provides the base configuration class and registration system for vector stores,
following the same pattern as the retriever configurations.
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.vectorstores import VectorStore
from pydantic import Field

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.models.embeddings.base import BaseEmbeddingConfig

logger = logging.getLogger(__name__)

# Registry defined outside the class to avoid Pydantic model conflicts
_VECTOR_STORE_REGISTRY: dict[str, type[BaseVectorStoreConfig]] = {}


class BaseVectorStoreConfig(InvokableEngine):
    """Base configuration for all vector store implementations.

    This class provides the common interface and registration mechanism for vector store
    configurations in the Haive framework. All vector store configurations should extend
    this class and implement the required methods.

    The registration system allows vector stores to be automatically discovered and
    instantiated based on their type, providing a consistent interface across all
    vector store implementations.

    Attributes:
        engine_type (EngineType): The type of engine (always VECTOR_STORE).
        embedding (BaseEmbeddingConfig): Configuration for the embedding model.
        collection_name (str): Name of the collection/index in the vector store.

    Examples:
        >>> from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
        >>> from haive.core.engine.vectorstore.types import VectorStoreType
        >>>
        >>> @BaseVectorStoreConfig.register(VectorStoreType.CUSTOM)
        >>> class CustomVectorStoreConfig(BaseVectorStoreConfig):
        ...     def instantiate(self):
        ...         # Implementation
        ...         pass
    """

    engine_type: EngineType = Field(
        default=EngineType.VECTOR_STORE, description="The type of engine"
    )

    # Core configuration
    embedding: BaseEmbeddingConfig = Field(
        ..., description="Embedding model configuration"
    )

    collection_name: str = Field(
        default="default",
        description="Name of the collection/index in the vector store",
    )

    @classmethod
    def register(cls, vector_store_type: str | Any) -> Any:
        """Register a vector store configuration class.

        This decorator registers a vector store configuration class with a specific type,
        allowing it to be automatically discovered and instantiated.

        Args:
            vector_store_type: The type identifier for the vector store.

        Returns:
            Decorator function that registers the class.

        Examples:
            >>> @BaseVectorStoreConfig.register("custom")
            >>> class CustomVectorStoreConfig(BaseVectorStoreConfig):
            ...     pass
        """

        def decorator(
            config_cls: type[BaseVectorStoreConfig],
        ) -> type[BaseVectorStoreConfig]:
            type_str = str(
                vector_store_type.value
                if hasattr(vector_store_type, "value")
                else vector_store_type
            )
            _VECTOR_STORE_REGISTRY[type_str] = config_cls
            logger.info(
                f"Registered vector store config: {config_cls.__name__} as {type_str}"
            )
            return config_cls

        return decorator

    @classmethod
    def get_config_class(
        cls, vector_store_type: str | Any
    ) -> type[BaseVectorStoreConfig] | None:
        """Get a registered vector store configuration class by type.

        Args:
            vector_store_type: The type identifier for the vector store.

        Returns:
            The registered configuration class, or None if not found.
        """
        type_str = str(
            vector_store_type.value
            if hasattr(vector_store_type, "value")
            else vector_store_type
        )
        return _VECTOR_STORE_REGISTRY.get(type_str)

    @classmethod
    def list_registered_types(cls) -> list[str]:
        """List all registered vector store types.

        Returns:
            List of registered type identifiers.
        """
        return list(_VECTOR_STORE_REGISTRY.keys())

    @abstractmethod
    def instantiate(self) -> VectorStore:
        """Create a vector store instance from this configuration.

        This method must be implemented by all vector store configurations to create
        the actual vector store instance with the configured parameters.

        Returns:
            VectorStore: An instantiated vector store ready for use.

        Raises:
            NotImplementedError: If not implemented by subclass.
        """
        raise NotImplementedError("Subclasses must implement instantiate()")

    def create_runnable(
        self, runnable_config: dict[str, Any] | None = None
    ) -> VectorStore:
        """Create a runnable vector store instance.

        This method is required by InvokableEngine and delegates to instantiate().

        Args:
            runnable_config: Optional runtime configuration (not used for vector stores).

        Returns:
            VectorStore: An instantiated vector store.
        """
        return self.instantiate()

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for vector stores.

        Default implementation for adding documents to vector stores.
        Subclasses can override this if they have different input requirements.

        Returns:
            Dictionary mapping field names to (type, default) tuples.
        """
        from langchain_core.documents import Document
        from pydantic import Field

        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for vector stores.

        Default implementation returns document IDs.
        Subclasses can override this if they have different output types.

        Returns:
            Dictionary mapping field names to (type, default) tuples.
        """
        from pydantic import Field

        return {
            "ids": (list[str], Field(description="IDs of the added documents")),
        }

    def validate_embedding(self) -> None:
        """Validate that the embedding configuration is properly set.

        Raises:
            ValueError: If embedding is not configured.
        """
        if not self.embedding:
            raise ValueError(
                f"{self.__class__.__name__} requires an embedding configuration"
            )
