# Additional retriever configurations
import logging
from typing import Any

from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from haive.core.models.retriever.base import RetrieverConfig, RetrieverType
from haive.core.models.vectorstore.base import VectorStoreConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@RetrieverConfig.register(RetrieverType.PARENT_DOCUMENT)
class ParentDocumentRetrieverConfig(RetrieverConfig):
    """Configuration for parent document retrievers."""

    vector_store_config: VectorStoreConfig | None = Field(
        default=None, description="Configuration for the vector store"
    )
    parent_document_store_config: dict[str, Any] | None = Field(
        default=None, description="Configuration for the parent document store"
    )
    child_splitter_config: dict[str, Any] | None = Field(
        default=None, description="Configuration for the text splitter for children"
    )

    def instantiate(self) -> BaseRetriever:
        """Create the parent document retriever."""
        from langchain.retrievers import ParentDocumentRetriever
        from langchain.storage import InMemoryStore
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        # Create the vector store
        vector_store = self.vector_store_config.create_vectorstore()

        # Create the document store
        doc_store = InMemoryStore()  # Default, but can be customized

        # Create the child splitter
        child_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        )

        # Create and return the retriever
        return ParentDocumentRetriever(
            vectorstore=vector_store, docstore=doc_store, child_splitter=child_splitter
        )
