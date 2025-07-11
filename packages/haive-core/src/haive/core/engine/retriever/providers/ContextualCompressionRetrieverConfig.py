"""
Contextual Compression Retriever implementation for the Haive framework.

This module provides a configuration class for the Contextual Compression retriever,
which compresses retrieved documents to extract only the most relevant information
relative to the query, improving both relevance and efficiency.

The ContextualCompressionRetriever works by:
1. Using a base retriever to get initial document candidates
2. Applying a compressor (LLM or extractive) to compress each document
3. Extracting only the parts of documents that are relevant to the query
4. Returning compressed, more focused document content

This retriever is particularly useful when:
- Documents are long and contain irrelevant sections
- Need to reduce token usage in downstream processing
- Want to improve precision by filtering out noise
- Building systems with strict context length limits

The implementation integrates with LangChain's ContextualCompressionRetriever while
providing a consistent Haive configuration interface with flexible compression options.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.CONTEXTUAL_COMPRESSION)
class ContextualCompressionRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Contextual Compression retriever in the Haive framework.

    This retriever compresses retrieved documents to extract only the most relevant
    information relative to the query, improving both relevance and efficiency.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always CONTEXTUAL_COMPRESSION).
        base_retriever (BaseRetrieverConfig): The underlying retriever to get initial candidates.
        compressor_type (str): Type of compressor to use ('llm_chain_extract', 'llm_chain_filter').
        llm_config (Optional[AugLLMConfig]): LLM configuration for compression (required for LLM compressors).
        chunk_size (int): Maximum size of compressed chunks.
        chunk_overlap (int): Overlap between compressed chunks.

    Examples:
        >>> from haive.core.engine.retriever import ContextualCompressionRetrieverConfig
        >>> from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> # Create base retriever and LLM config
        >>> base_config = VectorStoreRetrieverConfig(name="base", vectorstore_config=vs_config)
        >>> llm_config = AugLLMConfig(model_name="gpt-3.5-turbo", provider="openai")
        >>>
        >>> # Create contextual compression retriever
        >>> config = ContextualCompressionRetrieverConfig(
        ...     name="compression_retriever",
        ...     base_retriever=base_config,
        ...     compressor_type="llm_chain_extract",
        ...     llm_config=llm_config
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.CONTEXTUAL_COMPRESSION,
        description="The type of retriever",
    )

    # Core configuration
    base_retriever: BaseRetrieverConfig = Field(
        ...,
        description="Base retriever configuration to get initial document candidates",
    )

    # Compressor configuration
    compressor_type: str = Field(
        default="llm_chain_extract",
        description="Type of compressor: 'llm_chain_extract', 'llm_chain_filter'",
    )

    llm_config: Optional[AugLLMConfig] = Field(
        default=None,
        description="LLM configuration for compression (required for LLM compressors)",
    )

    @validator("compressor_type")
    def validate_compressor_type(cls, v):
        """Validate compressor type."""
        valid_types = ["llm_chain_extract", "llm_chain_filter"]
        if v not in valid_types:
            raise ValueError(f"compressor_type must be one of {valid_types}, got {v}")
        return v

    @validator("llm_config")
    def validate_llm_config_required(cls, v, values):
        """Validate that LLM config is provided for LLM compressors."""
        compressor_type = values.get("compressor_type", "")
        if compressor_type.startswith("llm_") and v is None:
            raise ValueError(
                f"llm_config is required for compressor_type '{compressor_type}'"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Contextual Compression retriever."""
        return {
            "query": (
                str,
                Field(description="Query for contextual compression and retrieval"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Contextual Compression retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Compressed documents relevant to the query",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Contextual Compression retriever from this configuration.

        Returns:
            ContextualCompressionRetriever: Instantiated retriever ready for compression retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import ContextualCompressionRetriever
            from langchain.retrievers.document_compressors import (
                LLMChainExtractor,
                LLMChainFilter,
            )
        except ImportError:
            raise ImportError(
                "ContextualCompressionRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate the base retriever
        try:
            base_retriever = self.base_retriever.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate base retriever: {e}")

        # Create the appropriate compressor
        if self.compressor_type == "llm_chain_extract":
            if not self.llm_config:
                raise ValueError(
                    "llm_config is required for llm_chain_extract compressor"
                )

            try:
                llm = self.llm_config.instantiate()
            except Exception as e:
                raise ValueError(f"Failed to instantiate LLM: {e}")

            compressor = LLMChainExtractor.from_llm(llm)

        elif self.compressor_type == "llm_chain_filter":
            if not self.llm_config:
                raise ValueError(
                    "llm_config is required for llm_chain_filter compressor"
                )

            try:
                llm = self.llm_config.instantiate()
            except Exception as e:
                raise ValueError(f"Failed to instantiate LLM: {e}")

            compressor = LLMChainFilter.from_llm(llm)

        else:
            raise ValueError(f"Unsupported compressor_type: {self.compressor_type}")

        return ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=base_retriever
        )
