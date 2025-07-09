"""
NeuralDB Retriever implementation for the Haive framework.

This module provides a configuration class for the NeuralDB retriever,
which uses ThirdAI's NeuralDB for fast neural search without GPUs.
NeuralDB provides efficient neural information retrieval with CPU-only
inference and training capabilities.

The NeuralDBRetriever works by:
1. Using ThirdAI's NeuralDB engine for neural search
2. Performing efficient CPU-based neural retrieval
3. Supporting fast training and inference
4. Enabling neural search without GPU requirements

This retriever is particularly useful when:
- Need neural search without GPU infrastructure
- Want fast CPU-based neural retrieval
- Building cost-effective neural search systems
- Need efficient training on CPU
- Using ThirdAI's NeuralDB platform

The implementation integrates with LangChain's NeuralDBRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.NEURAL_DB)
class NeuralDBRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for NeuralDB retriever in the Haive framework.

    This retriever uses ThirdAI's NeuralDB to provide fast neural search
    without requiring GPU infrastructure, enabling efficient CPU-based retrieval.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always NEURAL_DB).
        api_key (Optional[SecretStr]): ThirdAI API key (auto-resolved from THIRDAI_API_KEY).
        model_path (Optional[str]): Path to the NeuralDB model file.
        k (int): Number of documents to retrieve.
        documents (List[Document]): Documents to index for retrieval.
        training_steps (int): Number of training steps for the model.

    Examples:
        >>> from haive.core.engine.retriever import NeuralDBRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="Machine learning enables computers to learn"),
        ...     Document(page_content="Deep learning is a subset of machine learning"),
        ...     Document(page_content="Neural networks are inspired by the brain")
        ... ]
        >>>
        >>> # Create the NeuralDB retriever config
        >>> config = NeuralDBRetrieverConfig(
        ...     name="neuraldb_retriever",
        ...     documents=docs,
        ...     k=5,
        ...     training_steps=100
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("neural network learning")
        >>>
        >>> # Example with pre-trained model
        >>> pretrained_config = NeuralDBRetrieverConfig(
        ...     name="pretrained_neuraldb_retriever",
        ...     model_path="./my_neuraldb_model.pkl",
        ...     documents=docs,
        ...     k=3
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.NEURAL_DB, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="ThirdAI API key (auto-resolved from THIRDAI_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="thirdai", description="Provider name for API key resolution"
    )

    # Model configuration
    model_path: Optional[str] = Field(
        default=None,
        description="Path to the NeuralDB model file (if using pre-trained model)",
    )

    # Documents to index
    documents: List[Document] = Field(
        default_factory=list, description="Documents to index for NeuralDB retrieval"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    # Training parameters
    training_steps: int = Field(
        default=100,
        ge=1,
        le=10000,
        description="Number of training steps for the NeuralDB model",
    )

    learning_rate: float = Field(
        default=0.001, ge=0.0001, le=0.1, description="Learning rate for training"
    )

    # NeuralDB specific parameters
    chunk_size: int = Field(
        default=1000, ge=100, le=4000, description="Size of text chunks for processing"
    )

    chunk_overlap: int = Field(
        default=100, ge=0, le=500, description="Overlap between text chunks"
    )

    # Advanced parameters
    batch_size: int = Field(
        default=32, ge=1, le=256, description="Batch size for training and inference"
    )

    max_length: int = Field(
        default=512,
        ge=128,
        le=2048,
        description="Maximum sequence length for processing",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for NeuralDB retriever."""
        return {
            "query": (str, Field(description="Neural search query for NeuralDB")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for NeuralDB retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents from NeuralDB search"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a NeuralDB retriever from this configuration.

        Returns:
            NeuralDBRetriever: Instantiated retriever ready for neural search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import NeuralDBRetriever
        except ImportError:
            raise ImportError(
                "NeuralDBRetriever requires langchain-community and thirdai packages. "
                "Install with: pip install langchain-community thirdai"
            )

        # Get API key using SecureConfigMixin (if needed)
        api_key = self.get_api_key()

        # Prepare configuration
        config = {"k": self.k}

        # Add API key if available
        if api_key:
            config["thirdai_key"] = api_key

        # Handle model path or documents
        if self.model_path:
            # Load from pre-trained model
            config["model_path"] = self.model_path
        else:
            # Train from documents
            if not self.documents:
                raise ValueError(
                    "NeuralDBRetriever requires either a model_path or documents for training."
                )

            config["documents"] = self.documents
            config["training_steps"] = self.training_steps
            config["learning_rate"] = self.learning_rate
            config["chunk_size"] = self.chunk_size
            config["chunk_overlap"] = self.chunk_overlap

        # Add advanced parameters
        config["batch_size"] = self.batch_size
        config["max_length"] = self.max_length

        return NeuralDBRetriever(**config)
