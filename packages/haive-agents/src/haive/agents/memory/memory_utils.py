import datetime
import logging
import uuid
from collections.abc import Callable
from typing import Any

from agents.react.memory.state import KnowledgeTriple, MemoryItem
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

logger = logging.getLogger(__name__)


def get_user_id_from_state(state: dict[str, Any]) -> str:
    """Get the user ID from state or config.

    Args:
        state: Current state

    Returns:
        User ID string
    """
    user_id = state.get("user_id")
    if not user_id:
        # Check if it's in metadata
        metadata = state.get("metadata", {})
        user_id = metadata.get("user_id")

    if not user_id:
        # Generate a random ID
        user_id = f"user_{uuid.uuid4().hex[:8]}"

    return user_id


def create_memory_vectorstore(embedding_model: Embeddings | None = None) -> VectorStore:
    """Create a vector store for storing memories.

    Args:
        embedding_model: Optional embedding model

    Returns:
        Vector store instance
    """
    from langchain_community.vectorstores import FAISS
    from langchain_openai import OpenAIEmbeddings

    # Use provided embedding model or create a new one
    embeddings = embedding_model or OpenAIEmbeddings()

    # Create an empty FAISS index
    return FAISS.from_documents([], embeddings)


def save_unstructured_memories(
    memories: list[str | MemoryItem], vector_store: VectorStore, user_id: str
) -> list[str]:
    """Save unstructured memories to vector store.

    Args:
        memories: List of memory strings or MemoryItem objects
        vector_store: Vector store for storage
        user_id: User ID to associate with memories

    Returns:
        List of saved memory contents
    """
    documents = []
    saved_memories = []

    timestamp = datetime.datetime.now().isoformat()

    for memory in memories:
        if isinstance(memory, str):
            # Convert string to MemoryItem
            memory_item = MemoryItem(
                content=memory,
                source="conversation",
                timestamp=timestamp,
                metadata={"user_id": user_id},
            )
            content = memory
        elif isinstance(memory, MemoryItem):
            memory_item = memory
            if not memory_item.timestamp:
                memory_item.timestamp = timestamp
            if "user_id" not in memory_item.metadata:
                memory_item.metadata["user_id"] = user_id
            content = memory_item.content
        else:
            # Skip invalid memory types
            logger.warning(f"Skipping invalid memory type: {type(memory)}")
            continue

        # Create document
        document = Document(
            page_content=content,
            metadata={
                "user_id": user_id,
                "timestamp": memory_item.timestamp,
                "source": memory_item.source,
                **memory_item.metadata,
            },
        )
        documents.append(document)
        saved_memories.append(content)

    # Add documents to vector store
    if documents:
        vector_store.add_documents(documents)
        logger.info(f"Saved {len(documents)} memories for user {user_id}")

    return saved_memories


def save_structured_memories(
    memories: list[dict[str, Any] | KnowledgeTriple],
    vector_store: VectorStore,
    user_id: str,
) -> list[dict[str, Any]]:
    """Save structured memories (knowledge triples) to vector store.

    Args:
        memories: List of knowledge triples
        vector_store: Vector store for storage
        user_id: User ID to associate with memories

    Returns:
        List of saved triple dictionaries
    """
    documents = []
    saved_triples = []

    timestamp = datetime.datetime.now().isoformat()

    for memory in memories:
        if isinstance(memory, dict) and all(
            k in memory for k in ["subject", "predicate", "object_"]
        ):
            # Convert dict to KnowledgeTriple
            triple_dict = memory
            triple = KnowledgeTriple(
                subject=triple_dict["subject"],
                predicate=triple_dict["predicate"],
                object_=triple_dict["object_"],
                confidence=triple_dict.get("confidence", 1.0),
                source=triple_dict.get("source", "conversation"),
                timestamp=triple_dict.get("timestamp", timestamp),
                metadata=triple_dict.get("metadata", {"user_id": user_id}),
            )
        elif isinstance(memory, KnowledgeTriple):
            triple = memory
            if not triple.timestamp:
                triple.timestamp = timestamp
            if "user_id" not in triple.metadata:
                triple.metadata["user_id"] = user_id
        else:
            # Skip invalid memory types
            logger.warning(f"Skipping invalid memory type: {type(memory)}")
            continue

        # Create a string representation of the triple
        triple_str = f"{triple.subject} {triple.predicate} {triple.object_}"

        # Create document
        document = Document(
            page_content=triple_str,
            metadata={
                "user_id": user_id,
                "timestamp": triple.timestamp,
                "source": triple.source,
                "subject": triple.subject,
                "predicate": triple.predicate,
                "object": triple.object_,  # Use object instead of object_ for compatibility
                "confidence": triple.confidence,
                **triple.metadata,
            },
        )
        documents.append(document)
        saved_triples.append(triple.dict())

    # Add documents to vector store
    if documents:
        vector_store.add_documents(documents)
        logger.info(f"Saved {len(documents)} structured memories for user {user_id}")

    return saved_triples


def retrieve_memories(
    query: str,
    vector_store: VectorStore,
    user_id: str,
    limit: int = 5,
    filter_fn: Callable[[Document], bool] | None = None,
) -> list[str]:
    """Retrieve relevant memories from vector store.

    Args:
        query: Query string
        vector_store: Vector store containing memories
        user_id: User ID to filter memories
        limit: Maximum number of memories to retrieve
        filter_fn: Optional custom filter function

    Returns:
        List of relevant memory strings
    """
    # Default filter by user ID
    if filter_fn is None:
        filter_fn = lambda doc: doc.metadata.get("user_id") == user_id

    try:
        # Search for relevant documents
        documents = vector_store.similarity_search(query, k=limit, filter=filter_fn)

        # Extract memory strings
        memory_strings = [doc.page_content for doc in documents]

        logger.info(f"Retrieved {len(memory_strings)} memories for user {user_id}")
        return memory_strings

    except Exception as e:
        logger.error(f"Error retrieving memories: {e}")
        return []


def create_memory_tools(vector_store: VectorStore):
    """Create memory tools for saving and retrieving memories.

    Args:
        vector_store: Vector store for memory storage/retrieval

    Returns:
        Dictionary of memory tool functions
    """
    from langchain_core.tools import tool

    @tool
    def save_memory(memory: str, user_id: str) -> str:
        """Save an unstructured memory for later retrieval."""
        save_unstructured_memories([memory], vector_store, user_id)
        return f"Memory saved: {memory}"

    @tool
    def save_structured_memory(
        subject: str, predicate: str, object_: str, user_id: str
    ) -> str:
        """Save a structured memory as a knowledge triple."""
        triple = {
            "subject": subject,
            "predicate": predicate,
            "object_": object_,
            "metadata": {"user_id": user_id},
        }
        save_structured_memories([triple], vector_store, user_id)
        return f"Structured memory saved: {subject} {predicate} {object_}"

    @tool
    def recall_memories(query: str, user_id: str, limit: int = 5) -> list[str]:
        """Recall relevant memories for the query."""
        return retrieve_memories(query, vector_store, user_id, limit)

    return {
        "save_memory": save_memory,
        "save_structured_memory": save_structured_memory,
        "recall_memories": recall_memory,
    }
