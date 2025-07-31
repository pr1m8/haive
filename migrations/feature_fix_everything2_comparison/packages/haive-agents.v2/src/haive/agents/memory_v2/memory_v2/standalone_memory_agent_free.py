"""Standalone memory agent using only free resources (no API keys required).

This implementation shows how to build a functional memory agent without
relying on paid APIs like OpenAI or Anthropic.
"""

import asyncio
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from haive.agents.memory_v2.memory_state_original import (
    EnhancedMemoryItem,
    ImportanceLevel,
    MemoryState,
    MemoryType,
)


class FreeMemoryAgent:
    """Memory agent using free embeddings and local storage.

    This agent provides:
    - Memory storage with embeddings (using HuggingFace)
    - Similarity-based retrieval
    - Persistent storage to disk
    - No API keys required
    """

    def __init__(
        self,
        user_id: str,
        storage_path: str | None = None,
        embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
        k_memories: int = 5,
    ):
        """Initialize the free memory agent.

        Args:
            user_id: User identifier
            storage_path: Path to store memories (uses temp if None)
            embedding_model: HuggingFace model name for embeddings
            k_memories: Number of memories to retrieve
        """
        self.user_id = user_id
        self.k_memories = k_memories

        # Set up storage path
        if storage_path:
            self.storage_path = Path(storage_path)
        else:
            self.storage_path = Path(tempfile.mkdtemp()) / f"memory_{user_id}"
        self.storage_path.mkdir(parents=True, exist_ok=True)

        # Initialize embeddings (free, no API key)
        print(f"Initializing {embedding_model} embeddings...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=embedding_model,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": False},
        )

        # Initialize or load vector store
        self.vector_store_path = self.storage_path / "vector_store"
        self.vector_store = self._initialize_vector_store()

        # Initialize memory state
        self.memory_state = MemoryState(user_id=user_id)

        print(f"✅ FreeMemoryAgent initialized for user: {user_id}")

    def _initialize_vector_store(self) -> FAISS:
        """Initialize or load the vector store."""
        if self.vector_store_path.exists():
            try:
                print(f"Loading existing vector store from {self.vector_store_path}")
                return FAISS.load_local(
                    str(self.vector_store_path),
                    self.embeddings,
                    allow_dangerous_deserialization=True,
                )
            except Exception as e:
                print(f"Failed to load vector store: {e}")

        # Create new vector store with initial document
        print("Creating new vector store...")
        initial_doc = Document(
            page_content="Memory system initialized",
            metadata={"type": "system", "timestamp": datetime.now().isoformat()},
        )
        return FAISS.from_documents([initial_doc], self.embeddings)

    def add_memory(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.CONVERSATIONAL,
        importance: ImportanceLevel = ImportanceLevel.MEDIUM,
        metadata: dict[str, Any] | None = None,
    ) -> str:
        """Add a new memory.

        Args:
            content: Memory content
            memory_type: Type of memory
            importance: Importance level
            metadata: Optional metadata

        Returns:
            Memory ID
        """
        # Create enhanced memory item
        memory = EnhancedMemoryItem(
            content=content,
            memory_type=memory_type,
            importance=importance,
            user_id=self.user_id,
            metadata=metadata or {},
        )

        # Add to memory state
        self.memory_state.add_memory_item(memory)

        # Create document for vector store
        doc_metadata = {
            "memory_id": memory.id,
            "type": memory_type.value,
            "importance": importance.value,
            "timestamp": memory.created_at.isoformat(),
            "user_id": self.user_id,
        }
        if metadata:
            doc_metadata.update(metadata)

        doc = Document(page_content=content, metadata=doc_metadata)

        # Add to vector store
        self.vector_store.add_documents([doc])

        # Save vector store
        self.save()

        print(f"✅ Added memory: {memory.id} - {content[:50]}...")
        return memory.id

    def search_memories(
        self,
        query: str,
        k: int | None = None,
        memory_type: MemoryType | None = None,
        importance: ImportanceLevel | None = None,
    ) -> list[dict[str, Any]]:
        """Search memories using similarity search.

        Args:
            query: Search query
            k: Number of results (uses k_memories if None)
            memory_type: Filter by memory type
            importance: Filter by importance

        Returns:
            List of memory results with scores
        """
        k = k or self.k_memories

        # Build filter
        filter_dict = {"user_id": self.user_id}
        if memory_type:
            filter_dict["type"] = memory_type.value
        if importance:
            filter_dict["importance"] = importance.value

        # Search with filter
        results = self.vector_store.similarity_search_with_score(
            query, k=k, filter=filter_dict
        )

        # Format results
        formatted_results = []
        for doc, score in results:
            formatted_results.append(
                {
                    "content": doc.page_content,
                    "score": float(score),
                    "metadata": doc.metadata,
                    "memory_id": doc.metadata.get("memory_id"),
                    "type": doc.metadata.get("type"),
                    "importance": doc.metadata.get("importance"),
                    "timestamp": doc.metadata.get("timestamp"),
                }
            )

        return formatted_results

    def get_relevant_context(self, query: str, k: int | None = None) -> str:
        """Get relevant context for a query.

        Args:
            query: Query to find context for
            k: Number of memories to include

        Returns:
            Formatted context string
        """
        memories = self.search_memories(query, k)

        if not memories:
            return "No relevant memories found."

        # Format memories as context
        context_parts = ["Relevant memories:"]
        for i, memory in enumerate(memories, 1):
            timestamp = memory.get("timestamp", "")
            if timestamp:
                try:
                    dt = datetime.fromisoformat(timestamp)
                    timestamp = dt.strftime("%Y-%m-%d %H:%M")
                except:
                    pass

            context_parts.append(
                f"{i}. [{memory.get('type', 'unknown')}] "
                f"{memory['content']} "
                f"(importance: {memory.get('importance', 'unknown')}, "
                f"time: {timestamp})"
            )

        return "\n".join(context_parts)

    def save(self):
        """Save the vector store to disk."""
        self.vector_store.save_local(str(self.vector_store_path))
        print(f"💾 Saved vector store to {self.vector_store_path}")

    def get_stats(self) -> dict[str, Any]:
        """Get memory statistics."""
        return {
            "total_memories": self.memory_state.stats.total_memories,
            "memories_by_type": dict(self.memory_state.stats.memories_by_type),
            "memories_by_importance": dict(
                self.memory_state.stats.memories_by_importance
            ),
            "storage_path": str(self.storage_path),
            "vector_store_size": len(self.vector_store.docstore._dict),
        }

    async def process_input(self, user_input: str) -> str:
        """Process user input - store if it's information, retrieve if it's a question.

        Args:
            user_input: User's input text

        Returns:
            Response string
        """
        # Simple heuristic: questions vs statements
        is_question = (
            any(
                user_input.lower().strip().startswith(word)
                for word in [
                    "who",
                    "what",
                    "where",
                    "when",
                    "why",
                    "how",
                    "is",
                    "are",
                    "do",
                    "does",
                    "can",
                    "could",
                    "tell me",
                ]
            )
            or "?" in user_input
        )

        if is_question:
            # Retrieve relevant memories
            context = self.get_relevant_context(user_input)
            return f"Based on my memories:\n\n{context}"
        # Store as new memory
        # Determine type and importance based on content
        memory_type = MemoryType.CONVERSATIONAL
        importance = ImportanceLevel.MEDIUM

        # Simple classification
        if any(
            word in user_input.lower()
            for word in ["important", "critical", "urgent", "remember"]
        ):
            importance = ImportanceLevel.HIGH

        if any(
            word in user_input.lower()
            for word in ["fact", "is a", "are", "works", "located"]
        ):
            memory_type = MemoryType.FACTUAL

        memory_id = self.add_memory(
            user_input, memory_type=memory_type, importance=importance
        )

        return f"I've stored that in my memory (ID: {memory_id}). Type: {memory_type.value}, Importance: {importance.value}"


async def test_free_memory_agent():
    """Test the free memory agent."""
    print("\n🚀 Testing FreeMemoryAgent 🚀\n")

    # Create agent
    agent = FreeMemoryAgent(user_id="test_user")

    # Test data
    test_inputs = [
        # Statements to store
        "Alice Johnson is a senior AI researcher at TechCorp.",
        "Bob Smith works as the CTO of DataCorp.",
        "Important: Meeting with Alice scheduled for Monday at 2 PM.",
        "TechCorp specializes in transformer models and NLP research.",
        "DataCorp is our main technology partner for cloud infrastructure.",
        "Carol Williams is a data scientist specializing in computer vision.",
        # Questions to retrieve
        "Who is Alice?",
        "What companies have we mentioned?",
        "Tell me about the meeting schedule.",
        "What does TechCorp do?",
        "Who works with AI and machine learning?",
    ]

    # Process each input
    for user_input in test_inputs:
        print(f"\n{'='*60}")
        print(f"User: {user_input}")
        response = await agent.process_input(user_input)
        print(f"Agent: {response}")

    # Show statistics
    print(f"\n{'='*60}")
    print("Memory Statistics:")
    stats = agent.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")

    # Test direct search
    print(f"\n{'='*60}")
    print("Direct search test - 'AI researcher':")
    results = agent.search_memories("AI researcher", k=3)
    for i, result in enumerate(results, 1):
        print(f"  {i}. Score: {result['score']:.3f} - {result['content'][:60]}...")

    print("\n✅ FreeMemoryAgent test completed!")


if __name__ == "__main__":
    # Run the test
    asyncio.run(test_free_memory_agent())
