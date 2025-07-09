import logging
from enum import Enum
from typing import Any, ClassVar, Dict, Optional, Type, Union

from langchain_core.retrievers import BaseRetriever
from pydantic import BaseModel, Field

from haive.core.models.vectorstore.base import VectorStoreConfig

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.CRITICAL)


class RetrieverType(str, Enum):
    """The type of retriever to use."""

    # Base vector store retrievers
    VECTOR_STORE = "VectorStoreRetriever"

    # Advanced retrieval strategies
    TIME_WEIGHTED = "TimeWeightedVectorStoreRetriever"
    MULTI_QUERY = "MultiQueryRetriever"
    MULTI_VECTOR = "MultiVectorRetriever"
    PARENT_DOCUMENT = "ParentDocumentRetriever"
    SELF_QUERY = "SelfQueryRetriever"
    CONTEXTUAL_COMPRESSION = "ContextualCompressionRetriever"
    REPHRASE_QUERY = "RePhraseQueryRetriever"

    # Ensemble methods
    MERGER = "MergerRetriever"
    ENSEMBLE = "EnsembleRetriever"

    # Sparse retrievers
    SPARSE = "SparseRetriever"
    KNN = "KNNRetriever"
    TFIDF = "TFIDFRetriever"
    BM25 = "BM25Retriever"
    SVM = "SVMRetriever"

    # Specific implementations
    ELASTICSEARCH = "ElasticsearchRetriever"
    FAISS = "FAISSRetriever"
    IN_MEMORY = "InMemoryRetriever"
    PINECONE = "PineconeRetriever"
    QDRANT = "QdrantRetriever"
    GOLDEN = "GoldenRetriever"

    # Graph-based retrievers
    NEO4J = "Neo4jRetriever"
    KNOWLEDGE_GRAPH = "KnowledgeGraphRetriever"


class RetrieverConfig(BaseModel):
    """Base configuration for all retrievers."""

    retriever_type: RetrieverType = Field(description="The type of retriever to use")
    name: str = Field(description="Name identifier for this retriever configuration")
    description: Optional[str] = Field(
        default=None, description="Description of this retriever"
    )

    # Common retriever parameters
    search_type: str = Field(
        default="similarity", description="Search type ('similarity', 'mmr', etc.)"
    )
    search_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional search parameters"
    )
    k: int = Field(default=4, description="Number of documents to retrieve")

    # Core functionality
    _registry: ClassVar[Dict[RetrieverType, Type["RetrieverConfig"]]] = {}

    def instantiate(self) -> BaseRetriever:
        """Create the retriever instance based on configuration."""
        raise NotImplementedError("Subclasses must implement instantiate method")

    @classmethod
    def register(cls, retriever_type: RetrieverType):
        """Decorator to register retriever config implementations."""

        def decorator(subclass):
            cls._registry[retriever_type] = subclass
            return subclass

        return decorator

    @classmethod
    def get_config_class(cls, retriever_type: RetrieverType) -> Type["RetrieverConfig"]:
        """Get the appropriate config class for the retriever type."""
        if retriever_type not in cls._registry:
            logger.warning(
                f"No registered config for {retriever_type}, using base config"
            )
            return cls
        return cls._registry[retriever_type]

    @classmethod
    def from_retriever_type(
        cls, retriever_type: RetrieverType, **kwargs
    ) -> "RetrieverConfig":
        """Create the appropriate config for the given retriever type."""
        config_class = cls.get_config_class(retriever_type)
        return config_class(retriever_type=retriever_type, **kwargs)


def create_retriever_config(
    retriever_type: Union[RetrieverType, str],
    name: str,
    description: Optional[str] = None,
    vector_store_config: Optional[VectorStoreConfig] = None,
    llm_config: Optional[Any] = None,
    **kwargs,
) -> RetrieverConfig:
    """
    Factory function to create appropriate retriever configuration.

    Args:
        retriever_type: Type of retriever to create
        name: Name identifier for this retriever
        description: Description of the retriever
        vector_store_config: Configuration for vector store (if needed)
        llm_config: Configuration for LLM (if needed)
        **kwargs: Additional parameters specific to retriever type

    Returns:
        Appropriate retriever configuration object
    """
    # Convert string to enum if needed
    if isinstance(retriever_type, str):
        retriever_type = RetrieverType(retriever_type)

    # Create the configuration with common parameters
    config_params = {"name": name, "description": description, **kwargs}

    # Add specific parameters based on retriever type
    if retriever_type in [
        RetrieverType.VECTOR_STORE,
        RetrieverType.TIME_WEIGHTED,
        RetrieverType.MULTI_QUERY,
        RetrieverType.SELF_QUERY,
    ]:
        if vector_store_config:
            config_params["vector_store_config"] = vector_store_config

    if retriever_type in [RetrieverType.MULTI_QUERY, RetrieverType.REPHRASE_QUERY]:
        if llm_config:
            config_params["llm_config"] = llm_config

    # Create and return the appropriate configuration
    return RetrieverConfig.from_retriever_type(retriever_type, **config_params)
