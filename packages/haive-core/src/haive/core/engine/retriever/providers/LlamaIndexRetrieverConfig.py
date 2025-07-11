"""LlamaIndex Retriever implementation for the Haive framework.

This module provides a configuration class for the LlamaIndex retriever,
which integrates LlamaIndex's retrieval capabilities with LangChain.
LlamaIndex provides a data framework for LLM applications with
sophisticated indexing and retrieval mechanisms.

The LlamaIndexRetriever works by:
1. Using LlamaIndex's retrieval engines
2. Supporting various index types (vector, keyword, graph, etc.)
3. Enabling sophisticated query processing
4. Providing LlamaIndex-specific optimizations

This retriever is particularly useful when:
- Integrating LlamaIndex with LangChain workflows
- Need LlamaIndex's advanced indexing capabilities
- Want to leverage LlamaIndex's query engines
- Building complex retrieval pipelines
- Using LlamaIndex's data connectors

The implementation integrates LlamaIndex retrievers with LangChain while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.LLAMA_INDEX)
class LlamaIndexRetrieverConfig(BaseRetrieverConfig):
    """Configuration for LlamaIndex retriever in the Haive framework.

    This retriever integrates LlamaIndex's retrieval capabilities with LangChain,
    enabling the use of LlamaIndex's sophisticated indexing and query mechanisms.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always LLAMA_INDEX).
        index_path (Optional[str]): Path to a persisted LlamaIndex index.
        documents (List[Document]): Documents to index (if not loading from path).
        k (int): Number of documents to retrieve.
        index_type (str): Type of LlamaIndex index to create.
        similarity_top_k (int): Top-k for similarity search.

    Examples:
        >>> from haive.core.engine.retriever import LlamaIndexRetrieverConfig
        >>> from langchain_core.documents import Document
        >>>
        >>> # Create documents
        >>> docs = [
        ...     Document(page_content="LlamaIndex provides data framework for LLMs"),
        ...     Document(page_content="Vector stores enable semantic search"),
        ...     Document(page_content="Graph indexes capture relationships")
        ... ]
        >>>
        >>> # Create the LlamaIndex retriever config
        >>> config = LlamaIndexRetrieverConfig(
        ...     name="llamaindex_retriever",
        ...     documents=docs,
        ...     k=5,
        ...     index_type="vector",
        ...     similarity_top_k=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("semantic search with vectors")
        >>>
        >>> # Example with graph index
        >>> graph_config = LlamaIndexRetrieverConfig(
        ...     name="llamaindex_graph_retriever",
        ...     documents=docs,
        ...     index_type="knowledge_graph",
        ...     k=3
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.LLAMA_INDEX, description="The type of retriever"
    )

    # Index configuration
    index_path: str | None = Field(
        default=None,
        description="Path to a persisted LlamaIndex index (if loading existing index)",
    )

    documents: list[Document] = Field(
        default_factory=list, description="Documents to index (if creating new index)"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=100, description="Number of documents to retrieve"
    )

    similarity_top_k: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Top-k for similarity search in LlamaIndex",
    )

    # LlamaIndex specific parameters
    index_type: str = Field(
        default="vector",
        description="Type of LlamaIndex index: 'vector', 'keyword', 'knowledge_graph', 'list'",
    )

    chunk_size: int = Field(
        default=1000, ge=100, le=4000, description="Size of text chunks for indexing"
    )

    chunk_overlap: int = Field(
        default=100, ge=0, le=500, description="Overlap between text chunks"
    )

    # Query engine parameters
    response_mode: str = Field(
        default="compact",
        description="Response mode: 'compact', 'refine', 'tree_summarize'",
    )

    # Advanced parameters
    embed_model: str | None = Field(
        default=None,
        description="Embedding model for LlamaIndex (e.g., 'local:BAAI/bge-small-en-v1.5')",
    )

    llm_model: str | None = Field(
        default=None, description="LLM model for LlamaIndex query processing"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for LlamaIndex retriever."""
        return {
            "query": (str, Field(description="Query for LlamaIndex retrieval")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for LlamaIndex retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents from LlamaIndex retrieval",
                ),
            ),
        }

    def instantiate(self):
        """Create a LlamaIndex retriever from this configuration.

        Returns:
            LlamaIndexRetriever: Instantiated retriever ready for LlamaIndex-powered search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.retrievers import LlamaIndexRetriever
        except ImportError:
            raise ImportError(
                "LlamaIndexRetriever requires langchain-community and llama-index packages. "
                "Install with: pip install langchain-community llama-index"
            )

        # Prepare configuration
        config = {"k": self.k}

        # Handle index loading or creation
        if self.index_path:
            # Load from existing index
            config["index_path"] = self.index_path
        else:
            # Create new index from documents
            if not self.documents:
                raise ValueError(
                    "LlamaIndexRetriever requires either index_path or documents."
                )

            config["documents"] = self.documents
            config["index_type"] = self.index_type
            config["chunk_size"] = self.chunk_size
            config["chunk_overlap"] = self.chunk_overlap

        # Add search parameters
        config["similarity_top_k"] = self.similarity_top_k
        config["response_mode"] = self.response_mode

        # Add model configurations
        if self.embed_model:
            config["embed_model"] = self.embed_model

        if self.llm_model:
            config["llm_model"] = self.llm_model

        return LlamaIndexRetriever(**config)
