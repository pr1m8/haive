# src/haive/core/engine/vectorstore.py

"""Vector store engine implementation for the Haive framework.

This module provides a comprehensive interface for working with vector stores in the Haive framework.
It includes configuration models and utilities for creating, managing, and interacting with various
vector store backends.

Attributes:
    VectorStoreProvider (Enum): Supported vector store providers (Chroma, FAISS, Pinecone, etc.)

Classes:
    VectorStoreConfig: Main configuration class for vector stores
    VectorStoreProvider: Enumeration of supported vector store providers
    VectorStoreProviderRegistry: Registry for extending supported providers

Example:
    Basic usage of creating a vector store:
    ```python
    from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
    from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig

    # Create a vector store config
    config = VectorStoreConfig(
        name="my_vectorstore",
        documents=[Document(page_content="Hello world")],
        vector_store_provider=VectorStoreProvider.FAISS,
        embedding_model=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

    # Create the vector store
    vectorstore = config.create_vectorstore()
    ```

    Registering a custom vector store provider:
    ```python
    from haive.core.engine.vectorstore import VectorStoreProviderRegistry

    # Direct registration with a class
    class MyVectorStore(VectorStore):
        # Implementation of VectorStore methods
        ...

    VectorStoreProviderRegistry.register_provider("MyCustomStore", MyVectorStore)

    # Or with a factory function for lazy loading
    def get_my_vectorstore_class():
        from my_package.vectorstore import MyOtherVectorStore
        return MyOtherVectorStore

    VectorStoreProviderRegistry.register_provider_factory("MyOtherStore", get_my_vectorstore_class)

    # Now you can use these custom providers
    config = VectorStoreConfig(
        name="custom_vectorstore",
        vector_store_provider="MyCustomStore"
    )
    ```

    TODO: Need to seperate and implement the registry system, similar to retrievers and add base.
"""

from __future__ import annotations

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableConfig
from langchain_core.vectorstores import VectorStore
from pydantic import ConfigDict, Field, field_validator

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.models.embeddings.base import (
    BaseEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
)

logger = logging.getLogger(__name__)


class VectorStoreProvider(str, Enum):
    """
    Enumeration of supported vector store providers.

    This enum defines the built-in vector store providers supported by the Haive framework.
    Each provider corresponds to a specific vector database implementation with its own
    features, capabilities, and requirements.

    The enum can be dynamically extended at runtime using the extend() method
    or through the VectorStoreProviderRegistry, allowing for custom providers
    without modifying the core code.

    Attributes:
        CHROMA (str): Chroma vector database
        FAISS (str): Facebook AI Similarity Search
        PINECONE (str): Pinecone managed vector database
        WEAVIATE (str): Weaviate vector database
        ZILLIZ (str): Zilliz cloud vector database
        MILVUS (str): Milvus vector database
        QDRANT (str): Qdrant vector database
        IN_MEMORY (str): In-memory vector store (for testing/development)
        PGVECTOR (str): PostgreSQL with pgvector extension
        ELASTICSEARCH (str): Elasticsearch vector search
        REDIS (str): Redis vector database
        SUPABASE (str): Supabase vector store
        MONGODB_ATLAS (str): MongoDB Atlas vector search
        AZURE_SEARCH (str): Azure Cognitive Search
        OPENSEARCH (str): OpenSearch vector search
        CASSANDRA (str): Apache Cassandra vector store
        CLICKHOUSE (str): ClickHouse vector database
        TYPESENSE (str): Typesense vector search
        LANCEDB (str): LanceDB vector database
        NEO4J (str): Neo4j vector search

    Examples:
        >>> from haive.core.engine.vectorstore import VectorStoreProvider
        >>> # Using an enum value
        >>> provider = VectorStoreProvider.FAISS
        >>> str(provider)
        'FAISS'
        >>> # Checking if a value is in the enum
        >>> "Chroma" in [p.value for p in VectorStoreProvider]
        True
    """

    CHROMA = "Chroma"
    FAISS = "FAISS"
    PINECONE = "Pinecone"
    WEAVIATE = "Weaviate"
    ZILLIZ = "Zilliz"
    MILVUS = "Milvus"
    QDRANT = "Qdrant"
    IN_MEMORY = "InMemory"
    PGVECTOR = "PGVector"
    ELASTICSEARCH = "Elasticsearch"
    REDIS = "Redis"
    SUPABASE = "Supabase"
    MONGODB_ATLAS = "MongoDBAtlas"
    AZURE_SEARCH = "AzureSearch"
    OPENSEARCH = "OpenSearch"
    CASSANDRA = "Cassandra"
    CLICKHOUSE = "ClickHouse"
    TYPESENSE = "Typesense"
    LANCEDB = "LanceDB"
    NEO4J = "Neo4j"

    @classmethod
    def extend(cls, name: str, value: str) -> None:
        """
        Extend the enum with a new provider value.

        Args:
            name: The enum member name (e.g., 'MY_PROVIDER')
            value: The string value (e.g., 'MyProvider')

        Note:
            This is a workaround to extend an Enum at runtime. For proper type
            hinting, use the VectorStoreProviderRegistry instead.
        """
        cls._member_map_[name] = value
        cls._value2member_map_[value] = cls._member_map_[name]


class VectorStoreConfig(InvokableEngine[Union[str, Dict[str, Any]], List[Document]]):
    """
    Configuration model for a vector store engine.

    VectorStoreConfig provides a consistent interface for creating and using
    vector stores with embeddings. It encapsulates all the configuration needed
    to create and interact with various vector store backends, abstracting away
    provider-specific implementation details.

    This class enables:
    1. Creating vector stores with various providers (FAISS, Chroma, Pinecone, etc.)
    2. Managing documents and embeddings for vector storage
    3. Performing similarity searches with configurable parameters
    4. Creating retrievers that can be used in retrieval chains

    Attributes:
        engine_type (EngineType): The type of engine (always VECTOR_STORE).
        embedding_model (BaseEmbeddingConfig): Configuration for the embedding model.
        vector_store_provider (VectorStoreProvider): The vector store provider to use.
        documents (List[Document]): Documents to store in the vector store.
        vector_store_path (str): Path for storing vector indices on disk.
        docstore_path (str): Path for storing document data.
        k (int): Default number of documents to retrieve in searches.
        score_threshold (Optional[float]): Minimum similarity score for results.
        search_type (str): Search algorithm to use (e.g., "similarity", "mmr").
        vector_store_kwargs (Dict[str, Any]): Additional provider-specific parameters.

    Examples:
        >>> from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
        >>> from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create configuration
        >>> config = VectorStoreConfig(
        ...     name="product_search",
        ...     documents=[Document(page_content="iPhone 13: The latest smartphone from Apple")],
        ...     vector_store_provider=VectorStoreProvider.FAISS,
        ...     embedding_model=HuggingFaceEmbeddingConfig(
        ...         model="sentence-transformers/all-MiniLM-L6-v2"
        ...     ),
        ...     k=5
        ... )
        >>>
        >>> # Create vector store
        >>> vectorstore = config.create_vectorstore()
        >>>
        >>> # Perform similarity search
        >>> results = config.similarity_search("smartphone", k=3)
        >>>
        >>> # Create a retriever
        >>> retriever = config.create_retriever(search_type="mmr")
    """

    engine_type: EngineType = Field(default=EngineType.VECTOR_STORE)

    # Core components
    embedding_model: BaseEmbeddingConfig = Field(
        default_factory=lambda: HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
        description="The embedding model to use for the vector store",
    )
    vector_store_provider: VectorStoreProvider = Field(
        default=VectorStoreProvider.FAISS, description="The type of vector store to use"
    )

    # Content and storage
    documents: List[Document] = Field(
        default_factory=list, description="The raw documents to store"
    )
    vector_store_path: str = Field(
        default="vector_store", description="The path to the vector store"
    )
    docstore_path: str = Field(
        default="docstore", description="Where to store raw and processed documents"
    )

    # Search parameters
    k: int = Field(default=4, description="Default number of documents to retrieve")
    score_threshold: Optional[float] = Field(
        default=None, description="Score threshold for similarity search"
    )
    search_type: str = Field(
        default="similarity", description="Default search type (similarity, mmr, etc.)"
    )

    # Additional configuration
    vector_store_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Optional kwargs for the vector store"
    )

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("engine_type")
    def validate_engine_type(cls, v):
        if v != EngineType.VECTOR_STORE:
            raise ValueError("engine_type must be VECTOR_STORE")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """
        Return input field definitions as field_name -> (type, default) pairs.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        from typing import Any, Dict, Optional

        return {
            "query": (str, ...),
            "k": (Optional[int], None),
            "filter": (Optional[Dict[str, Any]], None),
            "score_threshold": (Optional[float], None),
            "search_type": (Optional[str], None),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """
        Return output field definitions as field_name -> (type, default) pairs.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        return {"documents": (List[Document], [])}

    def add_document(self, document: Document) -> None:
        """Add a single document to the vector store config.

        Args:
            document: Document to add
        """
        self.documents.append(document)

    def add_documents(self, documents: List[Document]) -> None:
        """Add multiple documents to the vector store config.

        Args:
            documents: List of documents to add
        """
        self.documents.extend(documents)

    def create_runnable(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> VectorStore:
        """Create a vector store instance with configuration applied.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            Instantiated vector store
        """
        # Extract config parameters
        params = self.apply_runnable_config(runnable_config)

        # Apply embedding model override if specified
        if "embedding_model" in params:
            return self.get_vectorstore(embedding=params["embedding_model"])

        # Create vector store with existing configuration
        return self.create_vectorstore()

    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        filter: Optional[Dict[str, Any]] = None,
        search_type: Optional[str] = None,
        runnable_config: Optional[RunnableConfig] = None,
    ) -> List[Document]:
        """Perform similarity search with configurable parameters.

        Args:
            query: Query string
            k: Number of documents to retrieve (overrides default)
            score_threshold: Score threshold for filtering results
            filter: Optional filter for the search
            search_type: Search type (similarity, mmr, etc.)
            runnable_config: Optional runtime configuration

        Returns:
            List of retrieved documents
        """
        # Create vector store
        vectorstore = self.create_runnable(runnable_config)

        # Extract search parameters from config
        search_params = {}
        if runnable_config and "configurable" in runnable_config:
            configurable = runnable_config["configurable"]
            if "k" in configurable:
                search_params["k"] = configurable["k"]
            if "score_threshold" in configurable:
                search_params["score_threshold"] = configurable["score_threshold"]
            if "filter" in configurable:
                search_params["filter"] = configurable["filter"]
            if "search_type" in configurable:
                search_type = configurable["search_type"]

        # Override with explicit parameters if provided
        if k is not None:
            search_params["k"] = k
        if score_threshold is not None:
            search_params["score_threshold"] = score_threshold
        if filter is not None:
            search_params["filter"] = filter

        # Use default k if not specified
        if "k" not in search_params:
            search_params["k"] = self.k

        # Use default search type if not specified
        search_type = search_type or self.search_type

        # Perform search based on search type
        if search_type == "similarity":
            return vectorstore.similarity_search(query, **search_params)
        if search_type == "mmr":
            return vectorstore.max_marginal_relevance_search(query, **search_params)
        raise ValueError(f"Unsupported search type: {search_type}")

    def invoke(
        self,
        input_data: Union[str, Dict[str, Any]],
        runnable_config: Optional[RunnableConfig] = None,
    ) -> List[Document]:
        """Invoke the vector store with input data.

        Args:
            input_data: Query string or dictionary with search parameters
            runnable_config: Optional runtime configuration

        Returns:
            List of retrieved documents
        """
        # Handle different input formats
        if isinstance(input_data, str):
            query = input_data
            k = None
            filter = None
            score_threshold = None
            search_type = None
        elif isinstance(input_data, dict):
            query = input_data.get("query", "")
            k = input_data.get("k")
            filter = input_data.get("filter")
            score_threshold = input_data.get("score_threshold")
            search_type = input_data.get("search_type")
        else:
            raise ValueError(f"Unsupported input type: {type(input_data)}")

        # Perform search
        return self.similarity_search(
            query,
            k=k,
            filter=filter,
            score_threshold=score_threshold,
            search_type=search_type,
            runnable_config=runnable_config,
        )

    def create_vectorstore(self, async_mode: bool = False) -> VectorStore:
        """
        Create a vector store instance from this configuration.

        Instantiates a vector store of the configured provider type, using the
        documents and embedding model specified in the configuration. This method
        handles the details of creating the appropriate vector store class,
        initializing it with the correct parameters, and populating it with documents.

        The method supports both synchronous and asynchronous initialization paths,
        and includes special handling for empty document collections.

        Args:
            async_mode (bool): Whether to use async methods for vector store creation.
                Default is False. If True, the method will use asynchronous variants
                of the vector store creation methods if available.

        Returns:
            VectorStore: An instantiated vector store of the configured provider type,
                populated with the configured documents and using the specified embedding model.

        Raises:
            ValueError: If an empty vector store cannot be created with the specified provider.

        Examples:
            >>> config = VectorStoreConfig(
            ...     name="product_catalog",
            ...     vector_store_provider=VectorStoreProvider.FAISS,
            ...     documents=[Document(page_content="Product description...")]
            ... )
            >>> vectorstore = config.create_vectorstore()
            >>>
            >>> # With async mode
            >>> async def create_async():
            ...     return await config.create_vectorstore(async_mode=True)
        """
        # Dynamically select the backend
        vs_cls = self._get_vectorstore_class()

        # Get embedding model
        embedding = self.embedding_model.instantiate()

        # Check if we have documents
        if not self.documents:
            logger.warning(f"Creating empty vector store: {self.name}")

            # Use from_texts with empty list for providers that support it
            if hasattr(vs_cls, "from_texts") or hasattr(vs_cls, "afrom_texts"):
                if async_mode:
                    if hasattr(vs_cls, "afrom_texts"):
                        return vs_cls.afrom_texts(
                            [], embedding, **self.vector_store_kwargs
                        )
                elif hasattr(vs_cls, "from_texts"):
                    return vs_cls.from_texts([], embedding, **self.vector_store_kwargs)

            # Fallback to empty constructor if available
            if hasattr(vs_cls, "__init__"):
                return vs_cls(embedding_function=embedding, **self.vector_store_kwargs)

            raise ValueError("Cannot create empty vector store with this provider")

        # Instantiate the vector store with provided documents
        if async_mode:
            return vs_cls.afrom_documents(
                self.documents, embedding, **self.vector_store_kwargs
            )
        return vs_cls.from_documents(
            self.documents, embedding, **self.vector_store_kwargs
        )

    def _get_vectorstore_class(self) -> Type[VectorStore]:
        """Get the vector store class based on provider.

        Returns:
            VectorStore class
        """
        # Check if provider is in registry first
        provider_class = VectorStoreProviderRegistry.get_provider_class(
            self.vector_store_provider
        )
        if provider_class is not None:
            return provider_class

        # Fall back to built-in providers
        if self.vector_store_provider == VectorStoreProvider.CHROMA:
            from langchain_community.vectorstores import Chroma

            return Chroma

        if self.vector_store_provider == VectorStoreProvider.FAISS:
            from langchain_community.vectorstores import FAISS

            return FAISS

        if self.vector_store_provider == VectorStoreProvider.PINECONE:
            from langchain_community.vectorstores import Pinecone

            return Pinecone

        if self.vector_store_provider == VectorStoreProvider.WEAVIATE:
            from langchain_community.vectorstores import Weaviate

            return Weaviate

        if self.vector_store_provider == VectorStoreProvider.ZILLIZ:
            from langchain_community.vectorstores import Zilliz

            return Zilliz

        if self.vector_store_provider == VectorStoreProvider.MILVUS:
            from langchain_community.vectorstores import Milvus

            return Milvus

        if self.vector_store_provider == VectorStoreProvider.QDRANT:
            from langchain_community.vectorstores import Qdrant

            return Qdrant

        if self.vector_store_provider == VectorStoreProvider.IN_MEMORY:
            from langchain_core.vectorstores import InMemoryVectorStore

            return InMemoryVectorStore

        if self.vector_store_provider == VectorStoreProvider.PGVECTOR:
            from langchain_community.vectorstores import PGVector

            return PGVector

        if self.vector_store_provider == VectorStoreProvider.ELASTICSEARCH:
            from langchain_community.vectorstores import ElasticsearchStore

            return ElasticsearchStore

        if self.vector_store_provider == VectorStoreProvider.REDIS:
            from langchain_community.vectorstores.redis import Redis

            return Redis

        if self.vector_store_provider == VectorStoreProvider.SUPABASE:
            from langchain_community.vectorstores import SupabaseVectorStore

            return SupabaseVectorStore

        if self.vector_store_provider == VectorStoreProvider.MONGODB_ATLAS:
            from langchain_community.vectorstores import MongoDBAtlasVectorSearch

            return MongoDBAtlasVectorSearch

        if self.vector_store_provider == VectorStoreProvider.AZURE_SEARCH:
            from langchain_community.vectorstores import AzureSearch

            return AzureSearch

        if self.vector_store_provider == VectorStoreProvider.OPENSEARCH:
            from langchain_community.vectorstores import OpenSearchVectorSearch

            return OpenSearchVectorSearch

        if self.vector_store_provider == VectorStoreProvider.CASSANDRA:
            from langchain_community.vectorstores import Cassandra

            return Cassandra

        if self.vector_store_provider == VectorStoreProvider.CLICKHOUSE:
            from langchain_community.vectorstores import Clickhouse

            return Clickhouse

        if self.vector_store_provider == VectorStoreProvider.TYPESENSE:
            from langchain_community.vectorstores import Typesense

            return Typesense

        if self.vector_store_provider == VectorStoreProvider.LANCEDB:
            from langchain_community.vectorstores import LanceDB

            return LanceDB

        if self.vector_store_provider == VectorStoreProvider.NEO4J:
            from langchain_community.vectorstores import Neo4jVector

            return Neo4jVector

        raise ValueError(
            f"Unsupported vector store provider: {self.vector_store_provider}"
        )

    def create_retriever(
        self,
        search_type: Optional[str] = None,
        search_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> BaseRetriever:
        """Create a retriever from the vector store.

        Args:
            search_type: Search type (similarity, mmr, etc.)
            search_kwargs: Search parameters
            **kwargs: Additional parameters for the retriever

        Returns:
            Configured retriever
        """
        # Create vector store
        vectorstore = self.create_vectorstore()

        # Set default search kwargs if not provided
        if search_kwargs is None:
            search_kwargs = {"k": self.k}
            if self.score_threshold is not None:
                search_kwargs["score_threshold"] = self.score_threshold

        # Use specified search type or default
        search_type = search_type or self.search_type

        # Create retriever
        return vectorstore.as_retriever(
            search_type=search_type, search_kwargs=search_kwargs, **kwargs
        )

    def get_vectorstore(self, embedding=None, async_mode: bool = False) -> VectorStore:
        """Get the vector store with optional embedding override.

        Args:
            embedding: Optional embedding model override
            async_mode: Whether to use async methods

        Returns:
            Instantiated vector store
        """
        if embedding:
            # Save original embedding
            original_embedding = self.embedding_model
            # Set the provided embedding
            self.embedding_model = embedding
            # Create vector store
            result = self.create_vectorstore(async_mode)
            # Restore original embedding
            self.embedding_model = original_embedding
            return result
        return self.create_vectorstore(async_mode)

    def extract_params(self) -> Dict[str, Any]:
        """
        Extract parameters from this engine for serialization.

        Returns:
            Dictionary of engine parameters
        """
        params = super().extract_params()

        # Add vector store specific parameters
        params.update(
            {
                "k": self.k,
                "search_type": self.search_type,
                "vector_store_provider": self.vector_store_provider,
            }
        )

        if self.score_threshold is not None:
            params["score_threshold"] = self.score_threshold

        return params

    @classmethod
    def create_vs_config_from_documents(
        cls,
        documents: List[Document],
        embedding_model: Optional[BaseEmbeddingConfig] = None,
        **kwargs,
    ) -> "VectorStoreConfig":
        """Create a VectorStoreConfig from a list of documents.

        Args:
            documents: List of documents to include
            embedding_model: Optional embedding model configuration
            **kwargs: Additional parameters for the config

        Returns:
            Configured VectorStoreConfig
        """
        if embedding_model is None:
            embedding_model = HuggingFaceEmbeddingConfig(
                model="sentence-transformers/all-mpnet-base-v2"
            )

        return cls(documents=documents, embedding_model=embedding_model, **kwargs)

    @classmethod
    def create_vs_from_documents(
        cls,
        documents: List[Document],
        embedding_model: Optional[BaseEmbeddingConfig] = None,
        **kwargs,
    ) -> VectorStore:
        """Create a VectorStore from a list of documents.

        Args:
            documents: List of documents to include
            embedding_model: Optional embedding model configuration
            **kwargs: Additional parameters for the config

        Returns:
            Instantiated VectorStore
        """
        config = cls.create_vs_config_from_documents(
            documents, embedding_model, **kwargs
        )
        return config.create_vectorstore()


class VectorStoreProviderRegistry:
    """
    Registry for custom vector store providers.

    This registry allows adding custom vector store providers without modifying
    the core VectorStoreProvider enum. It provides a flexible extension mechanism
    that supports both direct class registration and lazy-loading through factory
    functions, enabling integration with third-party vector store implementations.

    The registry maintains:
    1. A mapping of provider names to vector store classes
    2. A mapping of provider names to factory functions that return vector store classes
    3. Methods to dynamically extend the VectorStoreProvider enum

    This approach allows for runtime extension of the vector store system without
    modifying core code, supporting both built-in and custom provider implementations.

    Class Attributes:
        providers (Dict[Union[str, VectorStoreProvider], Type[VectorStore]]):
            Direct mapping of provider names to vector store classes.
        provider_factories (Dict[Union[str, VectorStoreProvider], Callable[..., Type[VectorStore]]]):
            Mapping of provider names to factory functions.

    Examples:
        >>> from haive.core.engine.vectorstore import VectorStoreProviderRegistry
        >>> from langchain_community.vectorstores import Chroma
        >>>
        >>> # Register a custom vector store class directly
        >>> class MyCustomVectorStore(VectorStore):
        ...     # Implementation...
        ...     pass
        >>>
        >>> VectorStoreProviderRegistry.register_provider("MyCustomStore", MyCustomVectorStore)
        >>>
        >>> # Register a factory function for lazy loading
        >>> def get_special_vector_store():
        ...     # Import and return the class only when needed
        ...     from my_package.vectorstores import SpecialVectorStore
        ...     return SpecialVectorStore
        >>>
        >>> VectorStoreProviderRegistry.register_provider_factory("SpecialStore", get_special_vector_store)
        >>>
        >>> # Use the registered providers
        >>> providers = VectorStoreProviderRegistry.list_providers()
        >>> "MyCustomStore" in providers
        True
    """

    # Use class variables without underscore prefixes for Pydantic compatibility
    providers: Dict[Union[str, VectorStoreProvider], Type[VectorStore]] = {}
    provider_factories: Dict[
        Union[str, VectorStoreProvider], Callable[..., Type[VectorStore]]
    ] = {}

    @classmethod
    def register_provider(
        cls,
        provider_name: Union[str, VectorStoreProvider],
        provider_class: Type[VectorStore],
    ) -> None:
        """
        Register a vector store provider class.

        Args:
            provider_name: Name or enum value for the provider
            provider_class: The VectorStore class to use for this provider
        """
        cls.providers[provider_name] = provider_class

        # If it's a string, try to extend the enum
        if isinstance(provider_name, str) and not any(
            provider.value == provider_name for provider in VectorStoreProvider
        ):
            try:
                enum_name = provider_name.upper().replace(" ", "_")
                VectorStoreProvider.extend(enum_name, provider_name)
                cls.providers[getattr(VectorStoreProvider, enum_name)] = provider_class
            except (AttributeError, ValueError) as e:
                logger.warning(f"Could not extend VectorStoreProvider enum: {e}")

    @classmethod
    def register_provider_factory(
        cls,
        provider_name: Union[str, VectorStoreProvider],
        factory: Callable[..., Type[VectorStore]],
    ) -> None:
        """
        Register a factory function that returns a vector store class.

        Args:
            provider_name: Name or enum value for the provider
            factory: Function that returns a VectorStore class
        """
        cls.provider_factories[provider_name] = factory

        # If it's a string, try to extend the enum
        if isinstance(provider_name, str) and not any(
            provider.value == provider_name for provider in VectorStoreProvider
        ):
            try:
                enum_name = provider_name.upper().replace(" ", "_")
                VectorStoreProvider.extend(enum_name, provider_name)
                cls.provider_factories[getattr(VectorStoreProvider, enum_name)] = (
                    factory
                )
            except (AttributeError, ValueError) as e:
                logger.warning(f"Could not extend VectorStoreProvider enum: {e}")

    @classmethod
    def get_provider_class(
        cls, provider_name: Union[str, VectorStoreProvider]
    ) -> Optional[Type[VectorStore]]:
        """
        Get the vector store class for a provider.

        Args:
            provider_name: Name or enum value for the provider

        Returns:
            VectorStore class if found, None otherwise
        """
        # Check direct registrations first
        if provider_class := cls.providers.get(provider_name):
            return provider_class

        # Check if we have a factory for this provider
        if factory := cls.provider_factories.get(provider_name):
            try:
                provider_class = factory()
                cls.providers[provider_name] = provider_class  # Cache the result
                return provider_class
            except Exception as e:
                logger.error(f"Error creating vector store class from factory: {e}")

        return None

    @classmethod
    def list_providers(cls) -> List[str]:
        """
        List all registered provider names.

        Returns:
            List of provider names
        """
        providers = set()

        # Add enum values
        for provider in VectorStoreProvider:
            providers.add(provider.value)

        # Add string keys
        for provider in list(cls.providers.keys()) + list(
            cls.provider_factories.keys()
        ):
            if isinstance(provider, str):
                providers.add(provider)

        return sorted(providers)


# Shorthand creator functions
def create_vectorstore(
    config: VectorStoreConfig, async_mode: bool = False
) -> VectorStore:
    """Create a vector store from a configuration.

    Args:
        config: Vector store configuration
        async_mode: Whether to use async methods

    Returns:
        Instantiated vector store
    """
    return config.create_vectorstore(async_mode=async_mode)


def create_retriever(config: VectorStoreConfig, **kwargs) -> BaseRetriever:
    """Create a retriever from a vector store configuration.

    Args:
        config: Vector store configuration
        **kwargs: Additional parameters for the retriever

    Returns:
        Configured retriever
    """
    return config.create_retriever(**kwargs)


def create_vs_config_from_documents(
    documents: List[Document],
    embedding_model: Optional[BaseEmbeddingConfig] = None,
    **kwargs,
) -> VectorStoreConfig:
    """Create a VectorStoreConfig from a list of documents.

    Args:
        documents: List of documents to include
        embedding_model: Optional embedding model configuration
        **kwargs: Additional parameters for the config

    Returns:
        Configured VectorStoreConfig
    """
    return VectorStoreConfig.create_vs_config_from_documents(
        documents, embedding_model, **kwargs
    )


def create_vs_from_documents(
    documents: List[Document],
    embedding_model: Optional[BaseEmbeddingConfig] = None,
    **kwargs,
) -> VectorStore:
    """Create a VectorStore from a list of documents.

    Args:
        documents: List of documents to include
        embedding_model: Optional embedding model configuration
        **kwargs: Additional parameters for the config

    Returns:
        Instantiated VectorStore
    """
    return VectorStoreConfig.create_vs_from_documents(
        documents, embedding_model, **kwargs
    )


def create_retriever_from_documents(
    documents: List[Document],
    embedding_model: Optional[BaseEmbeddingConfig] = None,
    **kwargs,
) -> BaseRetriever:
    """Create a retriever directly from documents.

    Args:
        documents: List of documents to include
        embedding_model: Optional embedding model configuration
        **kwargs: Additional parameters for the retriever

    Returns:
        Configured retriever
    """
    config = VectorStoreConfig.create_vs_config_from_documents(
        documents, embedding_model
    )
    return config.create_retriever(**kwargs)
