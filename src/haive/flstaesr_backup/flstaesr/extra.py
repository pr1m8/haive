
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
