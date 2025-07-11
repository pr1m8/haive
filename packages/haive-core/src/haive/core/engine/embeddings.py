# src/haive/core/engine/embeddings.py

import logging
from typing import Any, Optional, Union

from langchain_core.embeddings import Embeddings
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, ConfigDict, Field, create_model, field_validator

from haive.core.engine.base import EngineType, NonInvokableEngine
from haive.core.models.embeddings.base import BaseEmbeddingConfig

logger = logging.getLogger(__name__)


class EmbeddingsEngineConfig(
    NonInvokableEngine[Union[str, list[str]], Union[list[float], list[list[float]]]]
):
    """Configuration for embedding engines.

    EmbeddingsEngineConfig wraps an embedding model and provides methods for
    embedding documents and queries.
    """

    engine_type: EngineType = Field(default=EngineType.EMBEDDINGS)

    # Core configuration
    embedding_config: BaseEmbeddingConfig = Field(
        ..., description="Configuration for the embedding model"  # Required
    )

    # Batch processing parameters
    batch_size: int = Field(
        default=32, description="Batch size for embedding operations"
    )
    normalize_embeddings: bool = Field(
        default=False, description="Whether to normalize embedding vectors"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    @field_validator("engine_type")
    def validate_engine_type(cls, v):
        if v != EngineType.EMBEDDINGS:
            raise ValueError("engine_type must be EMBEDDINGS")
        return v

    def create_runnable(
        self, runnable_config: RunnableConfig | None = None
    ) -> Embeddings:
        """Create an embedding model with configuration applied.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            Instantiated embedding model
        """
        # Extract config parameters
        params = self.apply_runnable_config(runnable_config)

        # Create a modified copy if we have relevant parameters
        if params:
            # Create a copy to avoid modifying the original
            config_copy = self.embedding_config.model_copy(deep=True)

            # Apply model override if specified
            if "model" in params:
                config_copy.model = params["model"]

            # Instantiate with modified config
            return config_copy.instantiate(
                normalize=params.get("normalize", self.normalize_embeddings)
            )

        # Use default configuration
        return self.embedding_config.instantiate(normalize=self.normalize_embeddings)

    def apply_runnable_config(
        self, runnable_config: RunnableConfig | None = None
    ) -> dict[str, Any]:
        """Extract parameters from runnable_config relevant to embeddings.

        Args:
            runnable_config: Runtime configuration

        Returns:
            Dictionary of relevant parameters
        """
        # Start with common parameters
        params = super().apply_runnable_config(runnable_config)

        if runnable_config and "configurable" in runnable_config:
            configurable = runnable_config["configurable"]

            # Extract embeddings-specific parameters
            if "normalize" in configurable:
                params["normalize"] = configurable["normalize"]
            if "batch_size" in configurable:
                params["batch_size"] = configurable["batch_size"]

        return params

    def embed_documents(
        self,
        documents: list[str],
        batch_size: int | None = None,
        normalize: bool | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> list[list[float]]:
        """Embed multiple documents.

        Args:
            documents: List of text documents to embed
            batch_size: Optional batch size override
            normalize: Optional normalization override
            runnable_config: Optional runtime configuration

        Returns:
            List of embedding vectors
        """
        # Get embedding model with config
        embeddings = self.create_runnable(runnable_config)

        # Extract parameters from config
        params = self.apply_runnable_config(runnable_config)

        # Use provided batch size, config batch size, or default
        batch_size = batch_size or params.get("batch_size", self.batch_size)

        # Process in batches for efficiency
        if batch_size > 1 and len(documents) > batch_size:
            results = []
            for i in range(0, len(documents), batch_size):
                batch = documents[i : i + batch_size]
                batch_results = embeddings.embed_documents(batch)
                results.extend(batch_results)
            return results

        # Process all at once for small batches
        return embeddings.embed_documents(documents)

    def embed_query(
        self,
        text: str,
        normalize: bool | None = None,
        runnable_config: RunnableConfig | None = None,
    ) -> list[float]:
        """Embed a single query text.

        Args:
            text: Query text to embed
            normalize: Optional normalization override
            runnable_config: Optional runtime configuration

        Returns:
            Embedding vector
        """
        # Get embedding model with config
        embeddings = self.create_runnable(runnable_config)

        # Embed the query
        return embeddings.embed_query(text)

    def derive_input_schema(self) -> type[BaseModel]:
        """Derive input schema for this engine.

        Returns:
            Pydantic model for input schema
        """
        # Use provided schema if available
        if self.input_schema:
            return self.input_schema

        # Create input schema
        return create_model(
            f"{self.__class__.__name__}Input",
            text=(Optional[str], None),
            documents=(Optional[list[str]], None),
            batch_size=(Optional[int], None),
            normalize=(Optional[bool], None),
        )

    def derive_output_schema(self) -> type[BaseModel]:
        """Derive output schema for this engine.

        Returns:
            Pydantic model for output schema
        """
        # Use provided schema if available
        if self.output_schema:
            return self.output_schema

        # Create output schema
        return create_model(
            f"{self.__class__.__name__}Output",
            embeddings=(Union[list[float], list[list[float]]], ...),
        )

    def get_schema_fields(self) -> dict[str, tuple[type, Any]]:
        """Get schema fields for this engine.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        from typing import Optional

        fields = {
            "text": (Optional[str], None),
            "documents": (Optional[list[str]], None),
            "batch_size": (Optional[int], None),
            "normalize": (Optional[bool], None),
        }

        return fields


# Convenience factory functions


def create_embeddings_engine(
    embedding_config: BaseEmbeddingConfig,
    name: str | None = None,
    batch_size: int = 32,
    normalize_embeddings: bool = False,
) -> EmbeddingsEngineConfig:
    """Create an embeddings engine configuration.

    Args:
        embedding_config: Configuration for the embedding model
        name: Optional name for the engine
        batch_size: Batch size for embedding operations
        normalize_embeddings: Whether to normalize embedding vectors

    Returns:
        Configured EmbeddingsEngineConfig
    """
    return EmbeddingsEngineConfig(
        name=name or f"embeddings_{embedding_config.model.split('/')[-1]}",
        embedding_config=embedding_config,
        batch_size=batch_size,
        normalize_embeddings=normalize_embeddings,
    )


def embed_documents(
    config: EmbeddingsEngineConfig,
    documents: list[str],
    batch_size: int | None = None,
    runnable_config: RunnableConfig | None = None,
) -> list[list[float]]:
    """Embed multiple documents using an embeddings engine.

    Args:
        config: Embeddings engine configuration
        documents: List of text documents to embed
        batch_size: Optional batch size override
        runnable_config: Optional runtime configuration

    Returns:
        List of embedding vectors
    """
    return config.embed_documents(
        documents, batch_size, runnable_config=runnable_config
    )


def embed_query(
    config: EmbeddingsEngineConfig,
    text: str,
    runnable_config: RunnableConfig | None = None,
) -> list[float]:
    """Embed a single query text using an embeddings engine.

    Args:
        config: Embeddings engine configuration
        text: Query text to embed
        runnable_config: Optional runtime configuration

    Returns:
        Embedding vector
    """
    return config.embed_query(text, runnable_config=runnable_config)
