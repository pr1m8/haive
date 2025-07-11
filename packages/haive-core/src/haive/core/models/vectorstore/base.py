from __future__ import annotations

from enum import Enum
from typing import Any

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field

from haive.core.models.embeddings.base import (
    BaseEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
)


class VectorStoreProvider(str, Enum):
    """Enumeration of supported vector store providers."""

    Chroma = "Chroma"
    vs_FAISS = "FAISS"
    Pinecone = "Pinecone"
    Weaviate = "Weaviate"
    Zilliz = "Zilliz"
    Milvus = "Milvus"
    Qdrant = "Qdrant"
    InMemory = "InMemory"


class VectorStoreConfig(BaseModel):
    """Configuration model for a vector store."""

    name: str | None = Field(default=None)
    embedding_model: BaseEmbeddingConfig = Field(
        default=HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
        description="The embedding model to use for the vector store",
    )
    vector_store_provider: VectorStoreProvider = Field(
        default=VectorStoreProvider.vs_FAISS,
        description="The type of vector store to use",
    )
    vector_store_path: str = Field(
        default="vector_store", description="The path to the vector store"
    )
    vector_store_kwargs: dict[str, Any] = Field(
        default_factory=dict, description="Optional kwargs for the vector store"
    )
    documents: list[Document] = Field(
        default_factory=list, description="The raw documents to store"
    )
    docstore_path: str = Field(
        default="docstore", description="Where to store raw and processed documents"
    )

    def add_document(self, document: Document):
        """Add a single document to the vector store config."""
        self.documents.append(document)

    def create_vectorstore(self, async_mode: bool = False):
        """Create a vector store instance from this configuration."""
        # Dynamically select the backend
        if self.vector_store_provider == VectorStoreProvider.Chroma:
            from langchain_community.vectorstores import Chroma

            vs = Chroma
        elif self.vector_store_provider == VectorStoreProvider.vs_FAISS:
            from langchain_community.vectorstores import FAISS

            vs = FAISS
        elif self.vector_store_provider == VectorStoreProvider.Pinecone:
            from langchain_community.vectorstores import Pinecone

            vs = Pinecone
        elif self.vector_store_provider == VectorStoreProvider.Weaviate:
            from langchain_community.vectorstores import Weaviate

            vs = Weaviate
        elif self.vector_store_provider == VectorStoreProvider.Zilliz:
            from langchain_community.vectorstores import Zilliz

            vs = Zilliz
        elif self.vector_store_provider == VectorStoreProvider.Milvus:
            from langchain_community.vectorstores import Milvus

            vs = Milvus
        elif self.vector_store_provider == VectorStoreProvider.Qdrant:
            from langchain_community.vectorstores import Qdrant

            vs = Qdrant
        elif self.vector_store_provider == VectorStoreProvider.InMemory:
            from langchain_core.vectorstores import InMemoryVectorStore

            vs = InMemoryVectorStore
        else:
            raise ValueError(
                f"Unsupported vector store type: {self.vector_store_provider}"
            )

        # Instantiate the vector store with appropriate embedding model
        if async_mode:
            return vs.afrom_documents(
                self.documents,
                self.embedding_model.instantiate(),
                **self.vector_store_kwargs,
            )
        return vs.from_documents(
            self.documents,
            self.embedding_model.instantiate(),
            **self.vector_store_kwargs,
        )

    def create_retriever(self, async_mode: bool = False):
        """Create a retriever from the vector store."""
        vectorstore = self.create_vectorstore(async_mode=async_mode)
        return vectorstore.as_retriever()

    @classmethod
    def create_vs_config_from_documents(
        cls,
        documents: list[Document],
        embedding_model: BaseEmbeddingConfig = HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
        **kwargs,
    ) -> VectorStoreConfig:
        """Create a VectorStoreConfig from a list of documents."""
        config = cls(documents=documents, embedding_model=embedding_model, **kwargs)
        return config

    @classmethod
    def create_vs_from_documents(
        cls,
        documents: list[Document],
        embedding_model: BaseEmbeddingConfig = HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        ),
        **kwargs,
    ) -> VectorStoreConfig:
        """Create a VectorStore from a list of documents."""
        config = cls.create_vs_config_from_documents(
            documents, embedding_model, **kwargs
        )
        return config.create_vectorstore()


# Shorthand creator if needed elsewhere
def create_vectorstore(config: VectorStoreConfig, async_mode: bool = False):
    return config.create_vectorstore(async_mode=async_mode)


def create_retriever(config: VectorStoreConfig, async_mode: bool = False):
    return config.create_retriever(async_mode=async_mode)


def create_vs_config_from_documents(
    documents: list[Document],
    embedding_model: BaseEmbeddingConfig = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-mpnet-base-v2"
    ),
    **kwargs,
) -> VectorStoreConfig:
    return VectorStoreConfig.create_vs_config_from_documents(
        documents, embedding_model, **kwargs
    )


def create_vs_from_documents(
    documents: list[Document],
    embedding_model: BaseEmbeddingConfig = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-mpnet-base-v2"
    ),
    **kwargs,
) -> VectorStore:
    return VectorStoreConfig.create_vs_from_documents(
        documents, embedding_model, **kwargs
    )


def create_retriever_from_documents(
    documents: list[Document],
    embedding_model: BaseEmbeddingConfig = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-mpnet-base-v2"
    ),
    **kwargs,
) -> BaseRetriever:
    return VectorStoreConfig.create_vs_from_documents(
        documents, embedding_model, **kwargs
    ).create_retriever()
