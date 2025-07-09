"""
Self-Query Retriever implementation for the Haive framework.

This module provides a configuration class for the Self-Query retriever,
which enables natural language queries to be converted into structured queries
that can filter on document metadata and perform semantic similarity search.

The SelfQueryRetriever works by:
1. Using an LLM to parse natural language queries into structured components
2. Extracting filter conditions for metadata (date, category, etc.)
3. Extracting the semantic search query component
4. Performing both metadata filtering and vector similarity search
5. Returning documents that match both criteria

This retriever is particularly useful when:
- Documents have rich metadata that should be queryable
- Need to combine semantic search with structured filtering
- Users want to query both content and attributes naturally
- Building systems that need precise control over search scope

The implementation integrates with LangChain's SelfQueryRetriever while
providing a consistent Haive configuration interface with metadata schema support.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.SELF_QUERY)
class SelfQueryRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Self-Query retriever in the Haive framework.

    This retriever converts natural language queries into structured queries
    that can filter on document metadata and perform semantic similarity search.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always SELF_QUERY).
        vectorstore_config (VectorStoreConfig): Vector store for semantic search.
        llm_config (AugLLMConfig): LLM for parsing natural language queries.
        document_content_description (str): Description of document content for LLM.
        metadata_field_info (List[Dict]): Metadata fields that can be filtered on.
        k (int): Number of documents to return.

    Examples:
        >>> from haive.core.engine.retriever import SelfQueryRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> # Create vector store and LLM configs
        >>> vs_config = ChromaVectorStoreConfig(name="docs", collection_name="documents")
        >>> llm_config = AugLLMConfig(model_name="gpt-3.5-turbo", provider="openai")
        >>>
        >>> # Define metadata schema
        >>> metadata_fields = [
        ...     {
        ...         "name": "genre",
        ...         "description": "The genre of the movie",
        ...         "type": "string"
        ...     }
        ... ]
        >>>
        >>> # Create self-query retriever
        >>> config = SelfQueryRetrieverConfig(
        ...     name="self_query_retriever",
        ...     vectorstore_config=vs_config,
        ...     llm_config=llm_config,
        ...     document_content_description="Movie reviews and summaries",
        ...     metadata_field_info=metadata_fields,
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("action movies from the 1990s")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.SELF_QUERY, description="The type of retriever"
    )

    # Core configuration
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Vector store configuration for semantic search"
    )

    llm_config: AugLLMConfig = Field(
        ..., description="LLM configuration for parsing natural language queries"
    )

    # Content description for LLM context
    document_content_description: str = Field(
        ...,
        min_length=10,
        description="Description of the document content to help LLM understand the domain",
    )

    # Metadata schema definition
    metadata_field_info: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="List of metadata fields that can be filtered on",
    )

    # Retrieval parameters
    k: int = Field(default=4, ge=1, le=100, description="Number of documents to return")

    @validator("metadata_field_info", each_item=True)
    def validate_metadata_field_info(cls, v):
        """Validate metadata field info structure."""
        required_keys = {"name", "description", "type"}
        if not isinstance(v, dict):
            raise ValueError("Each metadata field info must be a dictionary")

        missing_keys = required_keys - set(v.keys())
        if missing_keys:
            raise ValueError(
                f"Metadata field info missing required keys: {missing_keys}"
            )

        valid_types = {"string", "integer", "float", "boolean"}
        if v["type"] not in valid_types:
            raise ValueError(
                f"Metadata field type must be one of {valid_types}, got {v['type']}"
            )

        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Self-Query retriever."""
        return {
            "query": (
                str,
                Field(
                    description="Natural language query with potential metadata filters"
                ),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Self-Query retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents matching both semantic and metadata criteria",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Self-Query retriever from this configuration.

        Returns:
            SelfQueryRetriever: Instantiated retriever ready for self-query retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.chains.query_constructor.base import AttributeInfo
            from langchain.retrievers import SelfQueryRetriever
        except ImportError:
            raise ImportError(
                "SelfQueryRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate the vector store
        try:
            vectorstore = self.vectorstore_config.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate vector store: {e}")

        # Instantiate the LLM
        try:
            llm = self.llm_config.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate LLM: {e}")

        # Convert metadata field info to AttributeInfo objects
        metadata_field_info = []
        for field_info in self.metadata_field_info:
            attr_info = AttributeInfo(
                name=field_info["name"],
                description=field_info["description"],
                type=field_info["type"],
            )
            metadata_field_info.append(attr_info)

        return SelfQueryRetriever.from_llm(
            llm=llm,
            vectorstore=vectorstore,
            document_contents=self.document_content_description,
            metadata_field_info=metadata_field_info,
            search_kwargs={"k": self.k},
        )
