import logging
from typing import Any

from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from haive.core.models.retriever.base import RetrieverConfig, RetrieverType
from haive.core.models.vectorstore.base import VectorStoreConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@RetrieverConfig.register(RetrieverType.MULTI_QUERY)
class MultiQueryRetrieverConfig(RetrieverConfig):
    """Configuration for multi-query retrievers."""

    vector_store_config: VectorStoreConfig | None = Field(
        default=None, description="Configuration for the vector store"
    )
    llm_config: Any | None = Field(
        default=None, description="Configuration for the LLM"
    )
    query_count: int = Field(
        default=3, description="Number of query variations to generate"
    )

    def instantiate(self) -> BaseRetriever:
        """Create the multi-query retriever."""
        if not self.vector_store_config or not self.llm_config:
            raise ValueError("Both vector_store_config and llm_config are required")

        # Import the specific retriever class
        from langchain_community.retrievers import MultiQueryRetriever

        # Create the vector store
        vector_store = self.vector_store_config.create_vectorstore()
        base_retriever = vector_store.as_retriever(
            search_type=self.search_type, search_kwargs=self.search_kwargs, k=self.k
        )

        # Create the LLM
        llm = self.llm_config.instantiate()

        # Create and return the retriever
        return MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=llm,
            prompt=None,  # Use default prompt
            parser_key="queries",
            num_queries=self.query_count,
        )
