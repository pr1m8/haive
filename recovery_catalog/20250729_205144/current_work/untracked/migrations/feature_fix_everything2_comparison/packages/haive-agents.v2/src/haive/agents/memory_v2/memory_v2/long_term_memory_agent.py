"""Long-Term Memory Agent following LangChain patterns.

This implementation follows the LangChain long-term memory agent documentation:
https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/

Key features:
1. Load memories first approach
2. Semantic memory retrieval across conversations
3. Text and structured knowledge storage
4. Time-weighted retrieval
5. ReactAgent tool integration

Architecture:
- BaseRAGAgent for memory retrieval
- SimpleRAGAgent for memory-enhanced responses
- Memory extraction and storage pipeline
- Cross-conversation persistence
"""

import asyncio
import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any
from uuid import uuid4

from haive.core.engine.vectorstore import VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.rag.base.agent import BaseRAGAgent

# Import the fixed SimpleRAG components
from haive.agents.rag.simple.agent import SimpleRAGAgent

logger = logging.getLogger(__name__)


class MemoryEntry(BaseModel):
    """Individual memory entry with timestamp and metadata."""

    model_config = ConfigDict(str_strip_whitespace=True)

    # Core fields
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str = Field(..., description="Memory content")
    memory_type: str = Field(
        default="text", description="Type: text, knowledge_triple, preference"
    )

    # Temporal information
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = Field(default=None)
    last_accessed: datetime | None = Field(default=None)

    # Context information
    conversation_id: str | None = Field(default=None)
    user_id: str | None = Field(default=None)
    session_id: str | None = Field(default=None)

    # Semantic information
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    tags: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Access tracking
    access_count: int = Field(default=0)
    relevance_scores: dict[str, float] = Field(default_factory=dict)

    def mark_accessed(self, query: str = None, relevance: float = None):
        """Mark memory as accessed."""
        self.access_count += 1
        self.last_accessed = datetime.now(UTC)
        if query and relevance:
            self.relevance_scores[query] = relevance

    def to_document(self) -> Document:
        """Convert to LangChain Document for RAG."""
        return Document(
            page_content=self.content,
            metadata={
                "memory_id": self.id,
                "memory_type": self.memory_type,
                "created_at": self.created_at.isoformat(),
                "importance": self.importance,
                "tags": self.tags,
                "conversation_id": self.conversation_id,
                "user_id": self.user_id,
                "access_count": self.access_count,
                **self.metadata,
            },
        )


class KnowledgeTriple(BaseModel):
    """Structured knowledge in (subject, predicate, object) format."""

    subject: str = Field(..., description="Subject entity")
    predicate: str = Field(..., description="Relationship/predicate")
    object: str = Field(..., description="Object entity")
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    source: str = Field(default="conversation")

    def to_memory_entry(self, **kwargs) -> MemoryEntry:
        """Convert to MemoryEntry."""
        content = f"{self.subject} {self.predicate} {self.object}"
        return MemoryEntry(
            content=content,
            memory_type="knowledge_triple",
            metadata={
                "subject": self.subject,
                "predicate": self.predicate,
                "object": self.object,
                "confidence": self.confidence,
                "source": self.source,
            },
            importance=self.confidence,
            **kwargs,
        )


class LongTermMemoryStore:
    """Persistent storage for long-term memories."""

    def __init__(self, storage_path: str = "./memory_store"):
        """Initialize memory store."""
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(exist_ok=True)
        self.memories: dict[str, MemoryEntry] = {}
        self.knowledge_triples: dict[str, KnowledgeTriple] = {}

        # Load existing memories
        self._load_memories()

    def add_memory(self, memory: MemoryEntry) -> None:
        """Add memory to store."""
        self.memories[memory.id] = memory
        self._save_memory(memory)

    def add_knowledge_triple(self, triple: KnowledgeTriple, **kwargs) -> MemoryEntry:
        """Add knowledge triple as memory."""
        memory = triple.to_memory_entry(**kwargs)
        self.add_memory(memory)
        self.knowledge_triples[memory.id] = triple
        return memory

    def get_memories(self, user_id: str = None, limit: int = None) -> list[MemoryEntry]:
        """Get memories, optionally filtered by user."""
        memories = list(self.memories.values())

        if user_id:
            memories = [m for m in memories if m.user_id == user_id]

        # Sort by importance and recency
        memories.sort(key=lambda m: (m.importance, m.created_at), reverse=True)

        if limit:
            memories = memories[:limit]

        return memories

    def search_memories(
        self, query: str, user_id: str = None, limit: int = 5
    ) -> list[MemoryEntry]:
        """Simple text search in memories."""
        query_lower = query.lower()
        matches = []

        for memory in self.memories.values():
            if user_id and memory.user_id != user_id:
                continue

            if query_lower in memory.content.lower():
                memory.mark_accessed(query, 1.0)  # Simple relevance
                matches.append(memory)

        # Sort by relevance and importance
        matches.sort(key=lambda m: (m.importance, m.access_count), reverse=True)
        return matches[:limit]

    def _save_memory(self, memory: MemoryEntry) -> None:
        """Save individual memory to file."""
        memory_file = self.storage_path / f"{memory.id}.json"
        with open(memory_file, "w") as f:
            json.dump(memory.model_dump(), f, default=str, indent=2)

    def _load_memories(self) -> None:
        """Load memories from storage."""
        for memory_file in self.storage_path.glob("*.json"):
            try:
                with open(memory_file) as f:
                    data = json.load(f)
                    memory = MemoryEntry(**data)
                    self.memories[memory.id] = memory
            except Exception as e:
                logger.warning(f"Failed to load memory {memory_file}: {e}")


class LongTermMemoryAgent:
    """Long-term memory agent following LangChain patterns.

    This agent implements the "load memories first" approach:
    1. Load relevant memories from storage
    2. Use BaseRAGAgent for semantic memory retrieval
    3. Enhanced response generation with memory context
    4. Extract and store new memories from conversation

    Examples:
        Basic usage::

            agent = LongTermMemoryAgent(user_id="user123")
            await agent.initialize()

            # Memory-enhanced conversation
            response = await agent.run("What do you remember about my work?")

        With specific LLM config::

            llm_config = AzureLLMConfig(deployment_name="gpt-4", ...)
            agent = LongTermMemoryAgent(
                user_id="user123",
                llm_config=llm_config
            )
    """

    def __init__(
        self,
        user_id: str,
        llm_config: LLMConfig | None = None,
        storage_path: str = "./memory_store",
        embedding_model: str = "sentence-transformers/all-mpnet-base-v2",
        vector_store_provider: VectorStoreProvider = VectorStoreProvider.FAISS,
        name: str = "long_term_memory_agent",
    ):
        """Initialize long-term memory agent."""
        self.user_id = user_id
        self.name = name
        self.llm_config = llm_config

        # Initialize memory store
        self.memory_store = LongTermMemoryStore(storage_path)

        # Vector store configuration
        self.embedding_model = HuggingFaceEmbeddingConfig(model=embedding_model)
        self.vector_store_provider = vector_store_provider

        # Agents (initialized in setup)
        self.memory_retriever: BaseRAGAgent | None = None
        self.memory_enhanced_agent: SimpleRAGAgent | None = None
        self._initialized = False

        logger.info(f"Created LongTermMemoryAgent for user {user_id}")

    async def initialize(self) -> None:
        """Initialize memory retrieval and enhanced response agents."""
        if self._initialized:
            return

        # Step 1: Load memories for this user
        user_memories = self.memory_store.get_memories(user_id=self.user_id, limit=100)
        logger.info(f"Loaded {len(user_memories)} memories for user {self.user_id}")

        # Step 2: Convert memories to documents for RAG
        memory_documents = [memory.to_document() for memory in user_memories]

        # Add placeholder if no memories
        if not memory_documents:
            placeholder = Document(
                page_content="No previous memories stored for this user.",
                metadata={"memory_type": "system", "user_id": self.user_id},
            )
            memory_documents.append(placeholder)

        # Step 3: Create memory retriever using BaseRAGAgent
        self.memory_retriever = BaseRAGAgent.from_documents(
            documents=memory_documents,
            embedding_model=self.embedding_model,
            vector_store_provider=self.vector_store_provider,
            name=f"{self.name}_retriever",
        )

        # Step 4: Create memory-enhanced response agent using fixed SimpleRAGAgent
        self.memory_enhanced_agent = SimpleRAGAgent.from_documents(
            documents=memory_documents,
            llm_config=self.llm_config,
            name=f"{self.name}_enhanced",
        )

        self._initialized = True
        logger.info(
            f"✅ Initialized LongTermMemoryAgent with {len(memory_documents)} memory documents"
        )

    async def run(self, query: str, extract_memories: bool = True) -> dict[str, Any]:
        """Run memory-enhanced conversation.

        This implements the "load memories first" pattern:
        1. Retrieve relevant memories using BaseRAGAgent
        2. Generate enhanced response using SimpleRAGAgent with memory context
        3. Extract and store new memories from the interaction
        """
        await self.initialize()

        # Step 1: Retrieve relevant memories
        memory_result = await self.memory_retriever.arun({"query": query})
        retrieved_memories = memory_result.get("retrieved_documents", [])

        # Step 2: Generate memory-enhanced response
        enhanced_result = await self.memory_enhanced_agent.arun({"query": query})
        response = enhanced_result.get("answer", "No response generated")

        # Step 3: Extract and store new memories (if enabled)
        if extract_memories:
            await self._extract_and_store_memories(query, response)

        # Step 4: Update memory access patterns
        for doc in retrieved_memories:
            memory_id = doc.metadata.get("memory_id")
            if memory_id and memory_id in self.memory_store.memories:
                self.memory_store.memories[memory_id].mark_accessed(query, 1.0)

        return {
            "response": response,
            "retrieved_memories": len(retrieved_memories),
            "memory_context": [doc.page_content for doc in retrieved_memories[:3]],
            "user_id": self.user_id,
        }

    async def add_conversation(self, messages: list[BaseMessage]) -> list[MemoryEntry]:
        """Add conversation and extract memories."""
        extracted_memories = []

        for message in messages:
            content = (
                str(message.content) if hasattr(message, "content") else str(message)
            )

            # Extract different types of memories using simple heuristics
            # In production, use LLM-based extraction
            memories = self._extract_memories_from_content(content)

            for memory_data in memories:
                memory = MemoryEntry(
                    content=memory_data["content"],
                    memory_type=memory_data["type"],
                    importance=memory_data["importance"],
                    user_id=self.user_id,
                    conversation_id=str(uuid4()),
                    tags=memory_data.get("tags", []),
                )

                self.memory_store.add_memory(memory)
                extracted_memories.append(memory)

        # Refresh agents with new memories if needed
        if extracted_memories:
            await self._refresh_agents()

        logger.info(
            f"Extracted {len(extracted_memories)} memories from {len(messages)} messages"
        )
        return extracted_memories

    def _extract_memories_from_content(self, content: str) -> list[dict[str, Any]]:
        """Extract memories from content using heuristics."""
        content_lower = content.lower()
        memories = []

        # Factual information patterns
        if any(
            pattern in content_lower
            for pattern in ["i am", "i work", "my name", "i live"]
        ):
            memories.append(
                {
                    "content": content,
                    "type": "factual",
                    "importance": 0.8,
                    "tags": ["personal", "factual"],
                }
            )

        # Preference patterns
        elif any(
            pattern in content_lower
            for pattern in ["i prefer", "i like", "i dislike", "i love", "i hate"]
        ):
            memories.append(
                {
                    "content": content,
                    "type": "preference",
                    "importance": 0.6,
                    "tags": ["preference"],
                }
            )

        # Important events or decisions
        elif any(
            pattern in content_lower
            for pattern in ["decided", "planning", "meeting", "deadline"]
        ):
            memories.append(
                {
                    "content": content,
                    "type": "event",
                    "importance": 0.7,
                    "tags": ["event", "planning"],
                }
            )

        return memories

    async def _extract_and_store_memories(self, query: str, response: str) -> None:
        """Extract memories from query and response."""
        # Extract from user query
        query_memories = self._extract_memories_from_content(query)
        for memory_data in query_memories:
            memory = MemoryEntry(
                content=memory_data["content"],
                memory_type=memory_data["type"],
                importance=memory_data["importance"],
                user_id=self.user_id,
                tags=memory_data.get("tags", []),
            )
            self.memory_store.add_memory(memory)

    async def _refresh_agents(self) -> None:
        """Refresh agents with updated memories."""
        # Get updated memories
        user_memories = self.memory_store.get_memories(user_id=self.user_id, limit=100)
        memory_documents = [memory.to_document() for memory in user_memories]

        # Recreate agents
        self.memory_retriever = BaseRAGAgent.from_documents(
            documents=memory_documents,
            embedding_model=self.embedding_model,
            vector_store_provider=self.vector_store_provider,
            name=f"{self.name}_retriever",
        )

        self.memory_enhanced_agent = SimpleRAGAgent.from_documents(
            documents=memory_documents,
            llm_config=self.llm_config,
            name=f"{self.name}_enhanced",
        )

    def get_memory_summary(self) -> dict[str, Any]:
        """Get summary of stored memories."""
        user_memories = self.memory_store.get_memories(user_id=self.user_id)

        return {
            "user_id": self.user_id,
            "total_memories": len(user_memories),
            "memory_types": list(set(m.memory_type for m in user_memories)),
            "most_accessed": sorted(
                user_memories, key=lambda m: m.access_count, reverse=True
            )[:3],
            "recent_memories": sorted(
                user_memories, key=lambda m: m.created_at, reverse=True
            )[:3],
            "storage_path": str(self.memory_store.storage_path),
        }

    # ReactAgent tool integration
    @classmethod
    def as_memory_tool(cls, user_id: str, **config_kwargs):
        """Create memory tool for ReactAgent integration."""

        @tool(
            name="long_term_memory", description="Search and recall long-term memories"
        )
        async def memory_tool(query: str) -> str:
            """Search long-term memory for relevant information."""
            agent = cls(user_id=user_id, **config_kwargs)
            await agent.initialize()

            result = await agent.run(query, extract_memories=False)

            memory_context = result.get("memory_context", [])
            if memory_context:
                return "Relevant memories found:\n" + "\n".join(
                    f"- {mem}" for mem in memory_context
                )
            return "No relevant memories found."

        return memory_tool


# Factory functions for easy creation
def create_long_term_memory_agent(
    user_id: str,
    llm_config: LLMConfig | None = None,
    storage_path: str = "./memory_store",
) -> LongTermMemoryAgent:
    """Factory function to create long-term memory agent."""
    return LongTermMemoryAgent(
        user_id=user_id, llm_config=llm_config, storage_path=storage_path
    )


async def demo_long_term_memory():
    """Demo the long-term memory agent functionality."""
    print("🧠 Demo: Long-Term Memory Agent")

    # Create agent
    agent = create_long_term_memory_agent(user_id="demo_user")

    # Initialize
    await agent.initialize()
    print("✅ Agent initialized")

    # Add some memories through conversation
    messages = [
        HumanMessage("Hi, I'm Sarah and I work as a product manager at Spotify"),
        HumanMessage("I prefer morning meetings and I really love jazz music"),
        HumanMessage("I'm working on improving recommendation algorithms"),
    ]

    extracted = await agent.add_conversation(messages)
    print(f"✅ Extracted {len(extracted)} memories from conversation")

    # Test memory-enhanced queries
    queries = [
        "Where do I work?",
        "What are my preferences for meetings?",
        "What kind of music do I like?",
        "What am I working on?",
    ]

    for query in queries:
        try:
            result = await agent.run(query)
            print(f"\n🔍 Query: {query}")
            print(f"📝 Response: {result['response'][:100]}...")
            print(f"🧠 Retrieved {result['retrieved_memories']} memories")

        except Exception as e:
            print(f"⚠️  Query failed: {str(e)[:100]}...")

    # Get memory summary
    summary = agent.get_memory_summary()
    print("\n📊 Memory Summary:")
    print(f"   Total memories: {summary['total_memories']}")
    print(f"   Memory types: {summary['memory_types']}")

    print("\n✅ Demo completed!")


if __name__ == "__main__":
    asyncio.run(demo_long_term_memory())
