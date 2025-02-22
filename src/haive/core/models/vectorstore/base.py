from pydantic import BaseModel, Field, field_validator
from src.haive.core.models.embeddings import EmbeddingModelConfig
from langchain_core.documents import Document
from typing import List, Dict, Any
from enum import Enum

# Define the Enum for vector store providers
class VectorStoreProvider(str, Enum):
    """Enumeration of supported vector store providers."""
    Chroma = "Chroma"
    vs_FAISS = "FAISS"
    Pinecone = "Pinecone"
    Weaviate = "Weaviate"
    Zilliz = "Zilliz"
    Milvus = "Milvus"
    Qdrant = "Qdrant"

class VectorStoreConfig(BaseModel):
    """Configuration model for the vector store.

    Attributes:
        name (str): The name of the vector store.
        embedding_model (EmbeddingsConfig): The embedding model to use for the vector store.
        vector_store_provider (VectorStoreProvider): The type of vector store to use.
        vector_store_path (str): The path to the vector store.
        vector_store_kwargs (Dict[str, Any]): The kwargs to pass to the vector store.
        documents (List[Document]): The documents to store in the vector store.
        docstore_path (str): The path to the document store.
    """
    name: str
    embedding_model: EmbeddingModelConfig = Field(description="The embedding model to use for the vector store", default=EmbeddingModelConfig())
    vector_store_provider: VectorStoreProvider = Field(description="The type of vector store to use", default=VectorStoreProvider.Chroma)
    vector_store_path: str = Field(description="The path to the vector store", default="vector_store")
    vector_store_kwargs: Dict[str, Any] = Field(description="The kwargs to pass to the vector store", default_factory=dict)
    documents: List[Document] = Field(description="The documents to store in the vector store", default_factory=list)
    docstore_path: str = Field(description="The path to the document store", default="docstore")
    
    @field_validator("vector_store_provider")
    def validate_vector_store_provider(cls, v: VectorStoreProvider):
        """Validate the vector store provider.

        Args:
            cls: The class itself.
            v (VectorStoreProvider): The value to validate.

        Raises:
            ValueError: If the vector store provider is unsupported.

        Returns:
            VectorStoreProvider: The validated vector store provider.
        """
        if v not in VectorStoreProvider:
            raise ValueError(f"Unsupported vector store type: {v}")
        return v
    
    @field_validator("documents")
    def add_documents(cls, documents: List[Document], values):
        """Add documents to the vector store configuration.

        Args:
            cls: The class itself.
            documents (List[Document]): The documents to add.
            values: The current values of the model.

        Returns:
            List[Document]: The updated list of documents.
        """
        values['documents'].extend(documents)
        return values['documents']
    
    def add_document(self, document: Document):
        """Add a single document to the vector store configuration.

        Args:
            document (Document): The document to add.
        """
        self.documents.append(document)
    
    @classmethod
    def create_vector_store(cls, config: 'VectorStoreConfig', async_mode: bool = True):
        """Create a vector store based on the configuration.

        Args:
            cls: The class itself.
            config (VectorStoreConfig): The configuration for the vector store.
            async_mode (bool): Whether to create the vector store in async mode.

        Returns:
            The created vector store instance.

        Raises:
            ValueError: If the vector store provider is unsupported.
        """
        if config.vector_store_provider == VectorStoreProvider.Chroma:
            from langchain_community.vectorstores import Chroma
            vs = Chroma
        elif config.vector_store_provider == VectorStoreProvider.vs_FAISS:
            from langchain_community.vectorstores import FAISS
            vs = FAISS
        elif config.vector_store_provider == VectorStoreProvider.Pinecone:
            from langchain_community.vectorstores import Pinecone
            vs = Pinecone
        elif config.vector_store_provider == VectorStoreProvider.Weaviate:
            from langchain_community.vectorstores import Weaviate
            vs = Weaviate
        elif config.vector_store_provider == VectorStoreProvider.Zilliz:
            from langchain_community.vectorstores import Zilliz
            vs = Zilliz
        elif config.vector_store_provider == VectorStoreProvider.Milvus:
            from langchain_community.vectorstores import Milvus
            vs = Milvus
        elif config.vector_store_provider == VectorStoreProvider.Qdrant:
            from langchain_community.vectorstores import Qdrant
            vs = Qdrant
        else:
            raise ValueError(f"Unsupported vector store type: {config.vector_store_provider}")

        if async_mode:
            vector_store = vs.afrom_documents(config.documents, config.embedding_model.model_name, **config.vector_store_kwargs)
        else:
            vector_store = vs.from_documents(config.documents, config.embedding_model.model_name, **config.vector_store_kwargs)
        
        return vector_store
    
    @classmethod
    def create_retriever(cls, vector_store: Any):
        """Create a retriever from a vector store.

        Args:
            cls: The class itself.
            vector_store: The vector store to create the retriever from.
        """
        return cls.create_vector_store(vector_store.as_retriever())