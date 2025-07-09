"""
Rephrase Query Retriever implementation for the Haive framework.

This module provides a configuration class for the Rephrase Query retriever,
which reformulates user queries using an LLM to improve retrieval performance
by creating more effective search queries.

The RePhraseQueryRetriever works by:
1. Taking the user's original query as input
2. Using an LLM to rephrase the query for better search effectiveness
3. Running the rephrased query against the base retriever
4. Returning documents found using the improved query

This retriever is particularly useful when:
- User queries are poorly formulated or ambiguous
- Need to improve search effectiveness through query optimization
- Building systems that need to handle natural language queries better
- Want to bridge the gap between user intent and retrieval effectiveness

The implementation integrates with LangChain's RePhraseQueryRetriever while
providing a consistent Haive configuration interface with LLM integration.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.REPHRASE_QUERY)
class RePhraseQueryRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Rephrase Query retriever in the Haive framework.

    This retriever reformulates user queries using an LLM to improve retrieval
    performance by creating more effective search queries.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always REPHRASE_QUERY).
        base_retriever (BaseRetrieverConfig): The underlying retriever to query with rephrased query.
        llm_config (AugLLMConfig): LLM configuration for query rephrasing.
        prompt_template (Optional[str]): Custom prompt template for rephrasing.

    Examples:
        >>> from haive.core.engine.retriever import RePhraseQueryRetrieverConfig
        >>> from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
        >>> from haive.core.engine.aug_llm import AugLLMConfig
        >>>
        >>> # Create base retriever and LLM config
        >>> base_config = VectorStoreRetrieverConfig(name="base", vectorstore_config=vs_config)
        >>> llm_config = AugLLMConfig(model_name="gpt-3.5-turbo", provider="openai")
        >>>
        >>> # Create rephrase query retriever
        >>> config = RePhraseQueryRetrieverConfig(
        ...     name="rephrase_retriever",
        ...     base_retriever=base_config,
        ...     llm_config=llm_config
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning stuff")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.REPHRASE_QUERY, description="The type of retriever"
    )

    # Core configuration
    base_retriever: BaseRetrieverConfig = Field(
        ..., description="Base retriever configuration to query with rephrased query"
    )

    llm_config: AugLLMConfig = Field(
        ..., description="LLM configuration for query rephrasing"
    )

    # Prompt customization
    prompt_template: Optional[str] = Field(
        default=None,
        description="Custom prompt template for rephrasing (uses default if None)",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Rephrase Query retriever."""
        return {
            "query": (
                str,
                Field(description="Original query to be rephrased and searched"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Rephrase Query retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved using the rephrased query",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Rephrase Query retriever from this configuration.

        Returns:
            RePhraseQueryRetriever: Instantiated retriever ready for query rephrasing retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers.re_phraser import RePhraseQueryRetriever
        except ImportError:
            raise ImportError(
                "RePhraseQueryRetriever requires langchain package. "
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

        # Create the rephrase query retriever
        kwargs = {
            "retriever": base_retriever,
            "llm_chain": llm,
        }

        # Add custom prompt if provided
        if self.prompt_template:
            try:
                from langchain.prompts import PromptTemplate

                prompt = PromptTemplate(
                    input_variables=["question"], template=self.prompt_template
                )
                kwargs["prompt"] = prompt
            except ImportError:
                raise ImportError(
                    "Custom prompt templates require langchain package. "
                    "Install with: pip install langchain"
                )

        return RePhraseQueryRetriever.from_llm(**kwargs)
