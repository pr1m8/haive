# src/haive/core/engine/retriever.py

"""Retriever engine implementation for the Haive framework.

This module provides a flexible and extensible interface for document retrieval in the Haive framework.
It includes base classes and implementations for various retriever types, with a focus on vector
store-based retrieval.

The module supports different retriever types through a plugin architecture, allowing easy extension
with new retriever implementations while maintaining a consistent interface.

Classes:
    RetrieverConfig: Base configuration class for all retrievers
    VectorStoreRetrieverConfig: Configuration for vector store-based retrievers

Functions:
    create_retriever_config: Factory function for creating retriever configurations
    create_retriever_from_vectorstore: Helper to create a retriever from a vector store

Example:
    Basic usage of creating a vector store retriever:
    ```python
    from haive.core.engine.retriever import VectorStoreRetrieverConfig
    from haive.core.engine.vectorstore import VectorStoreConfig

    # Create vector store config
    vs_config = VectorStoreConfig(...)

    # Create retriever config
    retriever_config = VectorStoreRetrieverConfig(
        name="my_retriever",
        vector_store_config=vs_config,
        k=4
    )

    # Create and use the retriever
    retriever = retriever_config.instantiate()
    docs = retriever.get_relevant_documents("query")
    ```
"""
import importlib
import logging
import pkgutil
import sys
from typing import Any, ClassVar, Dict, Optional, Sequence, Tuple, Type, Union

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, ConfigDict, Field, field_validator

from haive.core.engine.base import EngineType, InvokableEngine
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig

logger = logging.getLogger(__name__)


# Input and output schemas as BaseModels
class RetrieverInput(BaseModel):
    """Schema for retriever input."""

    query: str = Field(description="Query string for retrieval")
    k: Optional[int] = Field(
        default=None, description="Number of documents to retrieve"
    )
    filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Filter criteria for retrieval"
    )
    search_type: Optional[str] = Field(
        default=None, description="Type of search to perform"
    )
    score_threshold: Optional[float] = Field(
        default=None, description="Minimum similarity score threshold"
    )

    model_config = ConfigDict(extra="allow")


class RetrieverOutput(BaseModel):
    """Schema for retriever output."""

    retrieved_documents: Optional[Sequence[Document]] = Field(
        default_factory=list, description="Retrieved documents"
    )

    model_config = ConfigDict(extra="allow")

    @field_validator("retrieved_documents", mode="before")
    @classmethod
    def validate_documents(cls, v):
        """Validate that the documents are a list."""
        if v is None:
            return []
        return v


class BaseRetrieverConfig(InvokableEngine[RetrieverInput, RetrieverOutput]):
    """Base configuration for all retriever engines in the Haive framework.

    This class serves as the foundation for all retriever configurations, providing a consistent
    interface for document retrieval operations. It supports automatic discovery and registration
    of retriever implementations through a plugin architecture.

    The registry system allows new retriever types to be created simply by adding a new module
    with a properly decorated class, without having to manually update central registries.

    Attributes:
        engine_type (EngineType): The type of engine (always RETRIEVER).
        retriever_type (RetrieverType): The specific type of retriever to use.
        search_type (str): The type of search to perform ('similarity', 'mmr', etc.).
        search_kwargs (Dict[str, Any]): Additional search parameters.
        k (int): Number of documents to retrieve.
        filter (Optional[Dict[str, Any]]): Optional filter to apply to vector store search.
        _registry (ClassVar[Dict[RetrieverType, Type['RetrieverConfig']]]): Registry for retriever types.

    Example:
        ```python
        from haive.core.engine.retriever import RetrieverConfig, RetrieverType
        from haive.core.engine.vectorstore import VectorStoreConfig

        # Create a basic retriever config
        config = RetrieverConfig(
            name="my_retriever",
            retriever_type=RetrieverType.VECTOR_STORE,
            k=4,
            search_type="similarity"
        )

        # Create and use the retriever
        retriever = config.instantiate()
        docs = retriever.get_relevant_documents("query")
        ```
    """

    engine_type: EngineType = Field(default=EngineType.RETRIEVER)
    retriever_type: RetrieverType = Field(
        description="The type of retriever to use", default=RetrieverType.VECTOR_STORE
    )

    # Common retriever parameters
    search_type: str = Field(
        default="similarity", description="Search type ('similarity', 'mmr', etc.)"
    )
    search_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional search parameters"
    )
    k: int = Field(default=4, description="Number of documents to retrieve")
    filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Filter to apply to vector store search"
    )

    # Schema definitions
    input_schema: Type[BaseModel] = Field(
        default=RetrieverInput,
        description="Input schema for this retriever",
        exclude=True,
    )
    output_schema: Type[BaseModel] = Field(
        default=RetrieverOutput,
        description="Output schema for this retriever",
        exclude=True,
    )

    # Registry for retriever types
    _registry: ClassVar[Dict[RetrieverType, Type["BaseRetrieverConfig"]]] = {}
    _initialized: ClassVar[bool] = False

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("engine_type")
    def validate_engine_type(cls, v):
        """Validate that the engine type is RETRIEVER."""
        if v != EngineType.RETRIEVER:
            raise ValueError("engine_type must be RETRIEVER")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions from the RetrieverInput model.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        fields = {}
        for name, field_info in self.input_schema.model_fields.items():
            fields[name] = (field_info.annotation, field_info.default)
        return fields

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions from the RetrieverOutput model.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        fields = {}
        for name, field_info in self.output_schema.model_fields.items():
            fields[name] = (field_info.annotation, field_info.default)
        return fields

    def create_runnable(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> BaseRetriever:
        """
        Create a retriever with runtime configuration applied.

        This method creates a retriever instance with the current configuration,
        applying any runtime overrides specified in the runnable_config. It extracts
        relevant parameters from the runnable_config, updates the current configuration
        with those parameters, and then creates the retriever instance.

        The method handles common retriever parameters like k (number of results),
        filter, and search_type, ensuring they're properly propagated to the
        retriever instance.

        Args:
            runnable_config (Optional[RunnableConfig]): Runtime configuration containing
                parameter overrides for this execution. This can include parameters like
                k, filter, and search_type in the "configurable" section.

        Returns:
            BaseRetriever: An instantiated retriever with the current configuration
                and any runtime overrides applied.

        Examples:
            >>> config = VectorStoreRetrieverConfig(
            ...     name="my_retriever",
            ...     vector_store_config=vs_config,
            ...     k=4
            ... )
            >>>
            >>> # Create with default configuration
            >>> default_retriever = config.create_runnable()
            >>>
            >>> # Create with runtime overrides
            >>> runtime_config = {
            ...     "configurable": {
            ...         "k": 10,
            ...         "filter": {"metadata.source": "wikipedia"}
            ...     }
            ... }
            >>> custom_retriever = config.create_runnable(runtime_config)
            >>> # This retriever will use k=10 instead of k=4
        """
        # Extract parameters from runnable_config
        params = self.apply_runnable_config(runnable_config)

        # Apply k parameter if specified
        if "k" in params:
            self.k = params["k"]

            # Update search_kwargs if it contains k
            if "k" in self.search_kwargs:
                self.search_kwargs["k"] = params["k"]

        # Apply filter parameter if specified
        if "filter" in params:
            self.filter = params["filter"]

            # Update search_kwargs if it contains filter
            if "filter" in self.search_kwargs:
                self.search_kwargs["filter"] = params["filter"]

        # Apply search_type if specified
        if "search_type" in params:
            self.search_type = params["search_type"]

        # Create the retriever with updated configuration
        return self.instantiate()

    def instantiate(self) -> BaseRetriever:
        """Create the retriever instance.

        Returns:
            Instantiated retriever

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement instantiate method")

    def apply_runnable_config(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> Dict[str, Any]:
        """Extract parameters from runnable_config relevant to this retriever.

        Args:
            runnable_config: Runtime configuration

        Returns:
            Dictionary of relevant parameters
        """
        # Start with common parameters
        params = super().apply_runnable_config(runnable_config)

        if runnable_config and "configurable" in runnable_config:
            configurable = runnable_config["configurable"]

            # Extract retriever-specific parameters
            if "k" in configurable:
                params["k"] = configurable["k"]
            if "search_type" in configurable:
                params["search_type"] = configurable["search_type"]
            if "filter" in configurable:
                params["filter"] = configurable["filter"]

        return params

    @classmethod
    def register(cls, retriever_type: RetrieverType):
        """Register a retriever config implementation.

        Args:
            retriever_type: Type of retriever to register

        Returns:
            Decorator function
        """

        def decorator(subclass):
            logger.debug(
                f"Registering retriever type {retriever_type} with class {subclass.__name__}"
            )
            cls._registry[retriever_type] = subclass
            return subclass

        return decorator

    @classmethod
    def get_config_class(
        cls, retriever_type: RetrieverType
    ) -> Type["BaseRetrieverConfig"]:
        """Get the appropriate config class for the retriever type.

        Args:
            retriever_type: Type of retriever

        Returns:
            Retriever config class
        """
        # Ensure all retriever types are loaded
        cls._ensure_retrievers_loaded()

        if retriever_type not in cls._registry:
            logger.warning(
                f"No registered config for {retriever_type}, using base config"
            )
            return cls
        return cls._registry[retriever_type]

    @classmethod
    def from_retriever_type(
        cls, retriever_type: RetrieverType, **kwargs
    ) -> "BaseRetrieverConfig":
        """Create the appropriate config for the given retriever type.

        Args:
            retriever_type: Type of retriever to create
            **kwargs: Additional parameters for the config

        Returns:
            Configured retriever config
        """
        config_class = cls.get_config_class(retriever_type)
        return config_class(retriever_type=retriever_type, **kwargs)

    @classmethod
    def _ensure_retrievers_loaded(cls):
        """Ensure all retriever implementations are loaded.

        This method automatically imports all modules in the retriever package
        to ensure all retriever implementations are registered.
        """
        if cls._initialized:
            return

        # Get the current module
        current_module = sys.modules[__name__]
        package_name = current_module.__name__

        # Find the parent package
        parent_package = ".".join(package_name.split(".")[:-1])
        retriever_package = f"{parent_package}.retriever"

        try:
            # Import the retriever package
            retriever_pkg = importlib.import_module(retriever_package)

            # Get the package path
            if hasattr(retriever_pkg, "__path__"):
                package_path = retriever_pkg.__path__

                # Discover and import all modules in the package
                for _, name, is_pkg in pkgutil.walk_packages(package_path):
                    if not is_pkg:
                        try:
                            importlib.import_module(f"{retriever_package}.{name}")
                            logger.debug(f"Loaded retriever module: {name}")
                        except ImportError as e:
                            logger.warning(
                                f"Failed to import retriever module {name}: {e}"
                            )

            cls._initialized = True

        except (ImportError, AttributeError) as e:
            logger.warning(f"Failed to load retriever modules: {e}")
            # Continue without loading modules


@BaseRetrieverConfig.register(RetrieverType.VECTOR_STORE)
class VectorStoreRetrieverConfig(BaseRetrieverConfig):
    """Configuration for a vector store-based retriever in the Haive framework.

    This class extends RetrieverConfig to provide specific configuration for vector store-based
    document retrieval. It integrates with various vector stores and supports customizable
    search parameters for efficient document retrieval.

    Attributes:
        vector_store_config (VectorStoreConfig): Configuration for the underlying vector store.
        k (int): Number of documents to retrieve (default: 4).
        search_type (str): Type of search to perform, e.g., 'similarity' or 'mmr' (default: 'similarity').
        search_kwargs (Dict[str, Any]): Additional parameters for the search operation.
        filter (Optional[Dict[str, Any]]): Optional metadata filter for the search.

    Example:
        ```python
        from haive.core.engine.retriever import VectorStoreRetrieverConfig
        from haive.core.engine.vectorstore import VectorStoreConfig

        # Create a vector store config
        vector_store_config = VectorStoreConfig(
            name="my_vectorstore",
            store_type="chroma",
            embedding_config={"model": "sentence-transformers/all-mpnet-base-v2"}
        )

        # Create a vector store retriever config
        retriever_config = VectorStoreRetrieverConfig(
            name="my_retriever",
            vector_store_config=vector_store_config,
            k=4,
            search_type="mmr",
            search_kwargs={"fetch_k": 20, "lambda_mult": 0.5}
        )

        # Create and use the retriever
        retriever = retriever_config.instantiate()
        docs = retriever.get_relevant_documents("query")
        ```
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.VECTOR_STORE, description="The type of retriever"
    )

    # Required vector store configuration
    vector_store_config: VectorStoreConfig = Field(
        ...,  # This makes it required
        description="Configuration for the vector store to retrieve from",
    )

    # Search configuration
    k: int = Field(
        default=4,
        ge=1,  # minimum of 1 document
        description="Number of documents to retrieve",
    )

    search_type: str = Field(
        default="similarity", description="Search type: 'similarity', 'mmr', etc."
    )

    search_kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Additional search parameters"
    )

    filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Filter to apply to vector store search"
    )

    @field_validator("retriever_type")
    def validate_retriever_type(cls, v):
        """Validate that the retriever type is VECTOR_STORE."""
        if v != RetrieverType.VECTOR_STORE:
            raise ValueError("retriever_type must be VECTOR_STORE")
        return v

    def instantiate(self) -> BaseRetriever:
        """
        Create a VectorStoreRetriever instance based on this configuration.

        This method creates a retriever that uses the configured vector store as its
        document source. It sets up the appropriate search parameters based on the
        configuration, including k (number of results), search type, and any filters.

        The method uses the vector_store_config to create the retriever, handling
        all the necessary parameter conversions and applying any specific configuration
        options.

        Returns:
            BaseRetriever: An instantiated VectorStoreRetriever ready for document retrieval.

        Raises:
            ValueError: If the retriever creation fails, with details about the failure.

        Examples:
            >>> config = VectorStoreRetrieverConfig(
            ...     name="product_retriever",
            ...     vector_store_config=vs_config,
            ...     k=5,
            ...     search_type="mmr",
            ...     search_kwargs={"fetch_k": 20, "lambda_mult": 0.7}
            ... )
            >>> retriever = config.instantiate()
            >>> documents = retriever.get_relevant_documents("smartphone with good camera")
        """
        try:
            # Prepare search kwargs
            search_kwargs = {"k": self.k}
            if self.search_kwargs:
                search_kwargs.update(self.search_kwargs)

            # Add filter if provided
            extra_kwargs = {}
            if self.filter:
                search_kwargs["filter"] = self.filter

            # Create retriever
            retriever = self.vector_store_config.create_retriever(
                search_type=self.search_type,
                search_kwargs=search_kwargs,
                # prompt_template=self.prompt_template,
                **extra_kwargs,
            )

            return retriever
        except Exception as e:
            logger.error(f"Error creating retriever: {str(e)}")
            raise ValueError(f"Failed to create retriever: {str(e)}") from e


# Convenience factory functions


def create_retriever_config(
    retriever_type: Union[RetrieverType, str],
    name: str,
    description: Optional[str] = None,
    **kwargs,
) -> BaseRetrieverConfig:
    """
    Factory function to create the appropriate retriever configuration.

    This function serves as a central factory for creating retriever configurations
    of any type supported by the system. It automatically determines the correct
    configuration class based on the provided retriever type and initializes it
    with the specified parameters.

    The function handles dynamic loading of retriever implementations and converts
    string-based retriever types to the appropriate enum values.

    Args:
        retriever_type (Union[RetrieverType, str]): Type of retriever to create,
            either as a RetrieverType enum value or a string matching an enum value.
        name (str): Name identifier for this retriever instance, used for referencing
            and debugging.
        description (Optional[str]): Optional human-readable description of the
            retriever's purpose.
        **kwargs: Additional parameters specific to the retriever type, such as
            vector_store_config for VectorStoreRetriever, k for number of results, etc.

    Returns:
        BaseRetrieverConfig: The appropriate retriever configuration object for
            the specified type, properly initialized with the provided parameters.

    Examples:
        >>> from haive.core.engine.retriever import create_retriever_config, RetrieverType
        >>> from haive.core.engine.vectorstore import VectorStoreConfig
        >>>
        >>> # Create a vector store config
        >>> vs_config = VectorStoreConfig(name="docs")
        >>>
        >>> # Create a vector store retriever config
        >>> vs_retriever = create_retriever_config(
        ...     retriever_type=RetrieverType.VECTOR_STORE,
        ...     name="doc_retriever",
        ...     description="Retrieves relevant documents from the vector store",
        ...     vector_store_config=vs_config,
        ...     k=5
        ... )
        >>>
        >>> # Create a multi-query retriever config using string type
        >>> mq_retriever = create_retriever_config(
        ...     retriever_type="MultiQueryRetriever",
        ...     name="multi_query_retriever",
        ...     base_retriever=vs_retriever,
        ...     llm_config=llm_config
        ... )
    """
    # Ensure all retrievers are loaded
    BaseRetrieverConfig._ensure_retrievers_loaded()

    # Convert string to enum if needed
    if isinstance(retriever_type, str):
        retriever_type = RetrieverType(retriever_type)

    # Create the configuration with common parameters
    config_params = {"name": name, "description": description, **kwargs}

    # Create and return the appropriate configuration using the registry
    return BaseRetrieverConfig.from_retriever_type(retriever_type, **config_params)


def create_retriever_from_vectorstore(
    vector_store_config: VectorStoreConfig, **kwargs
) -> BaseRetriever:
    """
    Create a retriever directly from a vector store configuration.

    This convenience function creates a VectorStoreRetrieverConfig and instantiates
    a retriever from it in a single operation. It's a shortcut for the common case
    of creating a retriever from an existing vector store configuration.

    Args:
        vector_store_config (VectorStoreConfig): Configuration for the vector store
            that will be used as the retrieval source. This contains information about
            the documents, embedding model, and vector store provider.
        **kwargs: Additional parameters for the retriever, such as k (number of results),
            search_type ("similarity", "mmr", etc.), filter, or search_kwargs.

    Returns:
        BaseRetriever: An instantiated retriever ready for document retrieval.

    Examples:
        >>> from haive.core.engine.retriever import create_retriever_from_vectorstore
        >>> from haive.core.engine.vectorstore import VectorStoreConfig
        >>>
        >>> # Create a vector store config
        >>> vs_config = VectorStoreConfig(
        ...     name="product_catalog",
        ...     documents=[Document(page_content="iPhone 13: The latest smartphone")],
        ...     vector_store_provider="FAISS"
        ... )
        >>>
        >>> # Create a retriever directly
        >>> retriever = create_retriever_from_vectorstore(
        ...     vector_store_config=vs_config,
        ...     k=3,
        ...     search_type="mmr",
        ...     search_kwargs={"fetch_k": 10, "lambda_mult": 0.5}
        ... )
        >>>
        >>> # Use the retriever
        >>> docs = retriever.get_relevant_documents("smartphone")
    """
    # Create retriever config
    retriever_config = VectorStoreRetrieverConfig(
        name=f"retriever_{vector_store_config.name}",
        vector_store_config=vector_store_config,
        **kwargs,
    )

    # Instantiate retriever
    return retriever_config.instantiate()


# Automatically load all retriever implementations
BaseRetrieverConfig._ensure_retrievers_loaded()
