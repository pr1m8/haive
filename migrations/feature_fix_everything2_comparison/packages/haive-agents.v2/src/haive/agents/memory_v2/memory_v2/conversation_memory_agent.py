"""Conversation Memory Agent using BaseRAGAgent.

This module provides conversation memory storage and retrieval using BaseRAGAgent
with semantic search over conversation history and optional time-weighting.
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from haive.core.engine.vectorstore import VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, ConfigDict, Field

# Import BaseRAGAgent components
from haive.agents.rag.base.agent import BaseRAGAgent

logger = logging.getLogger(__name__)


class MessageDocumentConverter:
    """Convert messages to documents for RAG storage."""

    def __init__(self, user_id: str = None, conversation_id: str = None):
        """Initialize converter."""
        self.user_id = user_id
        self.conversation_id = conversation_id or f"conv_{uuid4()}"
        self.turn_counter = 0

    def convert_message(self, message: BaseMessage) -> Document:
        """Convert single message to document."""
        self.turn_counter += 1

        # Determine message type
        if isinstance(message, HumanMessage):
            msg_type = "human"
        elif isinstance(message, AIMessage):
            msg_type = "ai"
        else:
            msg_type = "system"

        # Extract content
        content = str(message.content) if hasattr(message, "content") else str(message)

        # Create document with rich metadata
        return Document(
            page_content=content,
            metadata={
                "message_type": msg_type,
                "conversation_id": self.conversation_id,
                "user_id": self.user_id,
                "turn_number": self.turn_counter,
                "timestamp": datetime.now(UTC).isoformat(),
                "content_length": len(content),
                "source": "conversation",
            },
        )

    def convert_messages(self, messages: list[BaseMessage]) -> list[Document]:
        """Convert multiple messages to documents."""
        return [self.convert_message(msg) for msg in messages]


class ConversationMemoryConfig(BaseModel):
    """Configuration for ConversationMemoryAgent."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Vector store configuration
    vector_store_provider: VectorStoreProvider = Field(
        default=VectorStoreProvider.FAISS
    )
    embedding_model: HuggingFaceEmbeddingConfig = Field(
        default_factory=lambda: HuggingFaceEmbeddingConfig(
            model="sentence-transformers/all-mpnet-base-v2"
        )
    )

    # Memory-specific settings
    max_memories_per_query: int = Field(default=5)
    similarity_threshold: float = Field(default=0.7)

    # Time weighting (for future integration)
    enable_time_weighting: bool = Field(default=False)
    time_decay_rate: float = Field(default=0.01)
    recency_weight: float = Field(default=0.3)


class ConversationMemoryAgent:
    """Memory agent for conversation history using BaseRAGAgent.

    This agent provides:
    - Semantic search over conversation history
    - Automatic message-to-document conversion
    - Real BaseRAGAgent integration with vector stores
    - Incremental conversation updates
    - Time-weighted retrieval (optional)

    Examples:
        Basic usage::

            agent = ConversationMemoryAgent("user_123")
            await agent.initialize()

            # Add conversation
            messages = [HumanMessage("I work at Google")]
            await agent.add_conversation(messages)

            # Retrieve context
            docs = await agent.retrieve_context("Where do I work?")
    """

    def __init__(
        self,
        config: ConversationMemoryConfig = None,
        name: str = "conversation_memory",
        user_id: str = None,
    ):
        """Initialize conversation memory agent."""
        self.config = config or ConversationMemoryConfig()
        self.name = name
        self.user_id = user_id or f"user_{uuid4()}"

        self.message_converter = MessageDocumentConverter(user_id=self.user_id)
        self._rag_agent: BaseRAGAgent | None = None
        self._documents: list[Document] = []
        self._initialized = False

        logger.info(
            f"Initialized ConversationMemoryAgent: {name} for user {self.user_id}"
        )

    async def initialize(self) -> None:
        """Initialize the underlying RAG agent."""
        if self._initialized:
            return

        if not self._documents:
            # Create initial placeholder document
            placeholder_doc = Document(
                page_content="Conversation memory initialized for usef",
                metadata={
                    "message_type": "system",
                    "user_id": self.user_id,
                    "timestamp": datetime.now(UTC).isoformat(),
                    "source": "system_initialization",
                },
            )
            self._documents.append(placeholder_doc)

        # Create BaseRAGAgent from documents - NO LLM CONFIG NEEDED!
        self._rag_agent = BaseRAGAgent.from_documents(
            documents=self._documents,
            embedding_model=self.config.embedding_model,
            vector_store_provider=self.config.vector_store_provider,
            name=self.name,
        )

        self._initialized = True
        logger.info(f"✅ Initialized BaseRAGAgent for {self.name}")

    async def add_conversation(self, messages: list[BaseMessage]) -> None:
        """Add conversation messages to memory."""
        if not messages:
            return

        # Convert messages to documents
        new_documents = self.message_converter.convert_messages(messages)
        self._documents.extend(new_documents)

        # Update RAG agent if already initialized
        if self._initialized:
            await self._update_vector_store()

        logger.info(f"Added {len(messages)} messages to conversation memory")

    async def retrieve_context(self, query: str, k: int = None) -> list[Document]:
        """Retrieve relevant conversation context using BaseRAGAgent.

        Args:
            query: Search query
            k: Number of documents to retrieve

        Returns:
            List of relevant conversation documents
        """
        await self.initialize()

        if k is None:
            k = self.config.max_memories_per_query

        # Use BaseRAGAgent to retrieve context - this is the magic!
        # BaseRAGAgent only does retrieval, no LLM generation
        result = await self._rag_agent.arun({"query": query})
        retrieved_docs = result.get("retrieved_documents", [])

        # Ensure we return Document objects
        documents = []
        for doc in retrieved_docs[:k]:
            if isinstance(doc, Document):
                documents.append(doc)
            elif isinstance(doc, str):
                # Convert string results to Document
                documents.append(
                    Document(page_content=doc, metadata={"source": "retrieved_content"})
                )

        logger.info(
            f"Retrieved {len(documents)} conversation documents for query: {query}"
        )
        return documents

    async def get_conversation_summary(self) -> dict[str, Any]:
        """Get summary of stored conversations."""
        return {
            "user_id": self.user_id,
            "total_documents": len(self._documents),
            "total_messages": len(
                [
                    d
                    for d in self._documents
                    if d.metadata.get("source") == "conversation"
                ]
            ),
            "conversations": len(
                set(
                    d.metadata.get("conversation_id")
                    for d in self._documents
                    if d.metadata.get("conversation_id")
                )
            ),
            "storage_backend": self.config.vector_store_provider.value,
            "embedding_model": self.config.embedding_model.model,
            "initialized": self._initialized,
        }

    async def _update_vector_store(self) -> None:
        """Update vector store with new documents."""
        try:
            # Recreate the RAG agent with all documents
            # In production, you'd want incremental updates
            self._rag_agent = BaseRAGAgent.from_documents(
                documents=self._documents,
                embedding_model=self.config.embedding_model,
                vector_store_provider=self.config.vector_store_provider,
                name=self.name,
            )
            logger.info(
                f"Updated vector store with {len(self._documents)} total documents"
            )
        except Exception as e:
            logger.error(f"Failed to update vector store: {e}")
            raise

    # Factory method for easy creation
    @classmethod
    def create(
        cls,
        user_id: str = None,
        vector_store_provider: VectorStoreProvider = VectorStoreProvider.FAISS,
        embedding_model: str = "sentence-transformers/all-mpnet-base-v2",
        name: str = "conversation_memory",
    ) -> "ConversationMemoryAgent":
        """Factory method to create ConversationMemoryAgent."""
        config = ConversationMemoryConfig(
            vector_store_provider=vector_store_provider,
            embedding_model=HuggingFaceEmbeddingConfig(model=embedding_model),
        )

        return cls(config=config, name=name, user_id=user_id)


# Standalone demo function
async def demo_conversation_memory():
    """Demo conversation memory agent functionality."""
    print("🚀 Demo: ConversationMemoryAgent with BaseRAGAgent")

    # Create agent
    agent = ConversationMemoryAgent.create(
        user_id="demo_user", name="demo_conversation"
    )

    # Initialize
    await agent.initialize()
    print("✅ Agent initialized")

    # Add conversation
    messages = [
        HumanMessage("Hi, I'm Sarah, a product manager at Spotify"),
        AIMessage("Hello Sarah! Nice to meet you."),
        HumanMessage("I work on recommendation algorithms and love jazz music"),
        AIMessage("That's fascinating! How does your music taste influence your work?"),
        HumanMessage("Jazz teaches me about improvisation and complex patterns"),
    ]

    await agent.add_conversation(messages)
    print(f"✅ Added {len(messages)} messages")

    # Retrieve context
    queries = [
        "Where does Sarah work?",
        "What type of music does Sarah like?",
        "What does Sarah do for work?",
    ]

    for query in queries:
        try:
            docs = await agent.retrieve_context(query, k=2)
            print(f"\n🔍 Query: {query}")
            print(f"📄 Found {len(docs)} relevant documents")

            for i, doc in enumerate(docs, 1):
                content = doc.page_content[:100]
                msg_type = doc.metadata.get("message_type", "unknown")
                print(f"   {i}. [{msg_type}] {content}...")

        except Exception as e:
            print(f"⚠️  Query '{query}' failed: {str(e)[:100]}...")

    # Get summary
    summary = await agent.get_conversation_summary()
    print(f"\n📊 Summary: {summary}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_conversation_memory())
