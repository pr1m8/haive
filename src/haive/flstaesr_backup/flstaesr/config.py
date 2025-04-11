from typing import Type, List
from pydantic import BaseModel, Field
#from src.haive.agents.flstaesr.state import RAGAgentSchema
#from src.haive.agents.flstaesr.models import DocumentLoaderRegistry, TextSplitterRegistry, DocumentTransformerRegistry, DocumentAnnotatorRegistry, EmbeddingsConfig, VectorStoreProvider
#from src.haive.agents.flstaesr.agent import FLSTAESRAgent
from src.haive.core.engine.agent.agent import AgentConfig
#from src.haive.agents.flstaesr.fetch.models import DocumentLoaderRegistry, TextSplitterRegistry, DocumentTransformerRegistry, DocumentAnnotatorRegistry, EmbeddingsConfig, VectorStoreProvider
from src.haive.agents.flstaesr.fetch.models import DocumentSource
from langchain_core.documents import Document
from typing import Any, Dict, Optional
from src.haive.core.models.vectorstore.base import VectorStoreConfig

# RAG Agent Schema
class RAGAgentSchema(BaseModel):
    """Schema for RAG agent state."""
    messages: List[Any] = Field(default_factory=list, description="Messages in the conversation")
    query: str = Field(default="", description="Current user query")
    context: List[str] = Field(default_factory=list, description="Retrieved context")
    sources: List[Dict[str, Any]] = Field(default_factory=list, description="Source information")
    documents: List[Document] = Field(default_factory=list, description="Loaded documents")
    document_sources: List[DocumentSource] = Field(default_factory=list, description="Original document sources")
    splits: List[Document] = Field(default_factory=list, description="Split documents")
    transformed_splits: List[Document] = Field(default_factory=list, description="Transformed document splits")
    annotated_splits: List[Document] = Field(default_factory=list, description="Annotated document splits")
    vectorstore: Optional[Any] = Field(default=None, description="Vector store for embeddings")
    vector_store_config: Optional[VectorStoreConfig] = Field(default=None, description="Vector store configuration")
    error: Optional[str] = Field(default=None, description="Error message if any")
    current_step: str = Field(default="route", description="Current processing step")
    retrieval_method: Optional[str] = Field(default=None, description="Method used for retrieval")
    retriever: Optional[Any] = Field(default=None, description="Retriever object")

class FLSTAESRAgentConfig(AgentConfig):
    """Configuration for the FLSTAESR RAG Agent."""
    state_schema: Type[BaseModel] = Field(default=RAGAgentSchema, description="State schema for the agent")
    search_engines: List[str] = Field(default_factory=lambda: ["tavily"], description="Search engines to use")
    document_loader_registry: Type[DocumentLoaderRegistry] = Field(default=DocumentLoaderRegistry, description="Registry for document loaders")
    text_splitter_registry: Type[TextSplitterRegistry] = Field(default=TextSplitterRegistry, description="Registry for text splitters")
    document_transformer_registry: Type[DocumentTransformerRegistry] = Field(default=DocumentTransformerRegistry, description="Registry for document transformers")
    document_annotator_registry: Type[DocumentAnnotatorRegistry] = Field(default=DocumentAnnotatorRegistry, description="Registry for document annotators")
    embedding_model: EmbeddingsConfig = Field(default=EmbeddingsConfig(), description="Embedding model to use")
    vector_store_provider: VectorStoreProvider = Field(default=VectorStoreProvider.FAISS, description="Vector store provider to use")
    vector_store_path: str = Field(default="vector_store", description="Path to the vector store")
    chunk_size: int = Field(default=1000, description="Default chunk size for text splitting")
    chunk_overlap: int = Field(default=100, description="Default chunk overlap for text splitting")
    