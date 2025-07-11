"""Multi-Query Retriever implementation for the Haive framework.

This module provides a configuration class for the Multi-Query retriever,
which generates multiple query variations to improve retrieval coverage
and find more relevant documents for complex or ambiguous queries.

The MultiQueryRetriever works by:
1. Using an LLM to generate multiple query variations from the original query
2. Running each generated query against the base retriever
3. Collecting and deduplicating all retrieved documents
4. Returning the combined set of unique documents

This retriever is particularly useful when:
- Dealing with complex or ambiguous user queries
- Need to improve recall by finding documents with different phrasings
- User queries might miss relevant documents due to vocabulary mismatch
- Building systems that need comprehensive document coverage

The implementation integrates with LangChain's MultiQueryRetriever while
providing a consistent Haive configuration interface with LLM integration.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.MULTI_QUERY)
class MultiQueryRetrieverConfig(BaseRetrieverConfig):
    """Configuration for Multi-Query retriever in the Haive framework.

    This retriever generates multiple query variations using an LLM to improve
    retrieval coverage and find more relevant documents for complex queries.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always MULTI_QUERY).
        base_retriever (BaseRetrieverConfig): The underlying retriever to query with variations.
        llm_config (AugLLMConfig): LLM configuration for generating query variations.
        num_queries (int): Number of query variations to generate.
        include_original (bool): Whether to include the original query in the set.

    Examples:
        >>> from haive.core.engine.retriever import MultiQueryRetrieverConfig
        >>> from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> # Create base retriever and LLM config
        >>> base_config = VectorStoreRetrieverConfig(name="base", vectorstore_config=vs_config)
        >>> llm_config = AugLLMConfig(model_name="gpt-3.5-turbo", provider="openai")
        >>>
        >>> # Create multi-query retriever
        >>> config = MultiQueryRetrieverConfig(
        ...     name="multi_query_retriever",
        ...     base_retriever=base_config,
        ...     llm_config=llm_config,
        ...     num_queries=3,
        ...     include_original=True
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.MULTI_QUERY, description="The type of retriever"
    )

    # Core configuration
    base_retriever: BaseRetrieverConfig = Field(
        ..., description="Base retriever configuration to query with variations"
    )

    llm_config: AugLLMConfig = Field(
        ..., description="LLM configuration for generating query variations"
    )

    # Query generation parameters
    num_queries: int = Field(
        default=3, ge=1, le=10, description="Number of query variations to generate"
    )

    include_original: bool = Field(
        default=True, description="Whether to include the original query in the set"
    )

    # Query prompt customization
    query_prompt_template: str | None = Field(
        default=None,
        description="Custom prompt template for query generation (uses default if None)",
    )

    @validator("num_queries")
    def validate_num_queries(self, v):
        """Ensure reasonable number of queries."""
        if v < 1:
            raise ValueError("num_queries must be at least 1")
        if v > 10:
            raise ValueError("num_queries should not exceed 10 for performance reasons")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Multi-Query retriever."""
        return {
            "query": (
                str,
                Field(description="Original query to generate variations from"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Multi-Query retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved from all query variations",
                ),
            ),
        }

    def instantiate(self):
        """Create a Multi-Query retriever from this configuration.

        Returns:
            MultiQueryRetriever: Instantiated retriever ready for multi-query retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers.multi_query import MultiQueryRetriever
        except ImportError:
            raise ImportError(
                "MultiQueryRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate the base retriever
        try:
            base_retriever = self.base_retriever.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate base retriever: {e}")

        # Instantiate the LLM
        try:
            llm = self.llm_config.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate LLM: {e}")

        # Create the multi-query retriever
        kwargs = {
            "retriever": base_retriever,
            "llm_chain": llm,
            "include_original": self.include_original,
        }

        # Add custom prompt if provided
        if self.query_prompt_template:
            try:
                from langchain.prompts import PromptTemplate

                prompt = PromptTemplate(
                    input_variables=["question"], template=self.query_prompt_template
                )
                kwargs["prompt"] = prompt
            except ImportError:
                raise ImportError(
                    "Custom prompt templates require langchain package. "
                    "Install with: pip install langchain"
                )

        return MultiQueryRetriever.from_llm(**kwargs)
