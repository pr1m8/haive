"""RAG-based Memory Agent using BaseRAGAgent with advanced retrievers.

This module provides memory-capable agents built on BaseRAGAgent with:
1. Time-weighted retrieval for temporal memory access
2. Multi-modal memory storage (conversation, preferences, facts)
3. Knowledge graph-enhanced retrieval
4. Real-time memory updates and ingestion
5. Vector store persistence across different backends

All built using BaseRAGAgent as the foundation with custom retrievers.
"""

import asyncio
import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.vectorstore import VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, ConfigDict, Field

# Import BaseRAGAgent and related components
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent

from .memory_state_original import (
    EnhancedMemoryItem,
    ImportanceLevel,
    MemoryType,
)

# Import our memory components
from .message_document_converter import MessageDocumentConverter
from .time_weighted_retriever import TimeWeightConfig, TimeWeightedRetriever

# Import KG components if available
try:
    from haive.agents.document_modifiers.kg.kg_base.models import GraphTransformer
    from haive.agents.document_modifiers.kg.kg_map_merge.models import (
        EntityNode,
        EntityRelationship,
        KnowledgeGraph,
    )

    KG_AVAILABLE = True
except ImportError:
    # Fallback: disable KG features
    GraphTransformer = None
    EntityNode = None
    EntityRelationship = None
    KnowledgeGraph = None
    KG_AVAILABLE = False

logger = logging.getLogger(__name__)


class MemoryRAGConfig(BaseModel):
    """Configuration for RAG-based memory agents."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core LLM configuration
    llm_config: AugLLMConfig = Field(default_factory=AugLLMConfig)

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
    memory_collection_name: str = Field(default="user_memories")
    max_memories_per_query: int = Field(default=5)
    similarity_threshold: float = Field(default=0.7)

    # Time weighting configuration
    enable_time_weighting: bool = Field(default=True)
    time_decay_rate: float = Field(default=0.01)  # per hour
    recency_weight: float = Field(default=0.3)  # 30% time, 70% similarity

    # Memory persistence settings
    persistent_storage: bool = Field(default=True)
    storage_path: str | None = Field(default="./memory_store/")

    # Knowledge graph enhancement
    enable_kg_enhancement: bool = Field(default=KG_AVAILABLE)
    kg_node_types: list[str] = Field(
        default=["Person", "Organization", "Concept", "Event", "Location", "Technology"]
    )

    # Memory categorization
    enable_auto_categorization: bool = Field(default=True)
    category_confidence_threshold: float = Field(default=0.8)


class ConversationMemoryAgent:
    """Memory agent for conversation history using BaseRAGAgent."""

    def __init__(self, config: MemoryRAGConfig, name: str = "conversation_memory"):
        """Initialize conversation memory agent."""
        self.config = config
        self.name = name
        self.message_converter = MessageDocumentConverter()
        self._rag_agent: BaseRAGAgent | None = None
        self._documents: list[Document] = []
        self._initialized = False

        logger.info(f"Initialized ConversationMemoryAgent: {name}")

    async def initialize(self) -> None:
        """Initialize the underlying RAG agent."""
        if self._initialized:
            return

        if not self._documents:
            # Create initial empty document to initialize vector store
            placeholder_doc = Document(
                page_content="Initial conversation memory store",
                metadata={
                    "type": "system",
                    "timestamp": datetime.now(UTC).isoformat(),
                    "importance": "low",
                },
            )
            self._documents.append(placeholder_doc)

        # Create BaseRAGAgent from documents
        self._rag_agent = BaseRAGAgent.from_documents(
            documents=self._documents,
            embedding_model=self.config.embedding_model,
            vector_store_provider=self.config.vector_store_provider,
            name=self.name,
        )

        # Replace with time-weighted retriever if enabled
        if self.config.enable_time_weighting:
            time_config = TimeWeightConfig(
                decay_rate=self.config.time_decay_rate,
                recency_weight=self.config.recency_weight,
                k=self.config.max_memories_per_query,
                score_threshold=self.config.similarity_threshold,
            )

            # Get the vector store from the RAG agent
            vector_store = self._rag_agent.retriever_config.vectorstore
            time_retriever = TimeWeightedRetriever(
                vectorstore=vector_store, config=time_config
            )

            # Replace the retriever
            self._rag_agent.retriever_config.retriever = time_retriever

        self._initialized = True
        logger.info(f"Initialized RAG agent for {self.name}")

    async def add_conversation(self, messages: list[BaseMessage]) -> None:
        """Add conversation messages to memory."""
        # Convert messages to timestamped documents
        new_documents = self.message_converter.convert_messages(messages)

        # Convert to regular documents for vector store
        documents = []
        for ts_doc in new_documents:
            doc = Document(page_content=ts_doc.page_content, metadata=ts_doc.metadata)
            documents.append(doc)

        # Add to our document store
        self._documents.extend(documents)

        # Reinitialize RAG agent with new documents if needed
        if self._initialized and len(documents) > 0:
            await self._update_vector_store(documents)

        logger.info(f"Added {len(messages)} messages to conversation memory")

    async def retrieve_conversation_context(
        self, query: str, k: int = None
    ) -> list[Document]:
        """Retrieve relevant conversation context."""
        await self.initialize()

        if k is None:
            k = self.config.max_memories_per_query

        # Use RAG agent to retrieve context
        result = await self._rag_agent.arun({"query": query})
        retrieved_docs = result.get("retrieved_documents", [])

        # Ensure we return Document objects
        documents = []
        for doc in retrieved_docs[:k]:
            if isinstance(doc, Document):
                documents.append(doc)
            elif isinstance(doc, str):
                documents.append(Document(page_content=doc))

        logger.info(
            f"Retrieved {len(documents)} conversation documents for query: {query}"
        )
        return documents

    async def _update_vector_store(self, new_documents: list[Document]) -> None:
        """Update vector store with new documents."""
        try:
            # For now, we recreate the RAG agent with all documents
            # In production, you'd want incremental updates
            self._rag_agent = BaseRAGAgent.from_documents(
                documents=self._documents,
                embedding_model=self.config.embedding_model,
                vector_store_provider=self.config.vector_store_provider,
                name=self.name,
            )
            logger.info(f"Updated vector store with {len(new_documents)} new documents")
        except Exception as e:
            logger.error(f"Failed to update vector store: {e}")


class FactualMemoryAgent:
    """Memory agent for factual information using BaseRAGAgent."""

    def __init__(self, config: MemoryRAGConfig, name: str = "factual_memory"):
        """Initialize factual memory agent."""
        self.config = config
        self.name = name
        self._rag_agent: BaseRAGAgent | None = None
        self._memories: list[EnhancedMemoryItem] = []
        self._initialized = False

        logger.info(f"Initialized FactualMemoryAgent: {name}")

    async def initialize(self) -> None:
        """Initialize the underlying RAG agent."""
        if self._initialized:
            return

        if not self._memories:
            # Create initial placeholder memory
            placeholder_memory = EnhancedMemoryItem(
                content="Initial factual memory store",
                source="system",
                memory_type=MemoryType.FACTUAL,
                importance=ImportanceLevel.LOW,
                tags=["system", "initialization"],
                confidence=1.0,
            )
            self._memories.append(placeholder_memory)

        # Convert memories to documents
        documents = self._memories_to_documents(self._memories)

        # Create BaseRAGAgent
        self._rag_agent = BaseRAGAgent.from_documents(
            documents=documents,
            embedding_model=self.config.embedding_model,
            vector_store_provider=self.config.vector_store_provider,
            name=self.name,
        )

        self._initialized = True
        logger.info(
            f"Initialized factual memory RAG agent with {len(self._memories)} memories"
        )

    async def add_memory(self, memory: EnhancedMemoryItem) -> None:
        """Add a factual memory."""
        self._memories.append(memory)

        if self._initialized:
            # Convert to document and update
            doc = self._memory_to_document(memory)
            await self._update_vector_store([doc])

        logger.info(f"Added factual memory: {memory.content[:50]}...")

    async def add_memories(self, memories: list[EnhancedMemoryItem]) -> None:
        """Add multiple factual memories."""
        self._memories.extend(memories)

        if self._initialized:
            documents = self._memories_to_documents(memories)
            await self._update_vector_store(documents)

        logger.info(f"Added {len(memories)} factual memories")

    async def retrieve_facts(self, query: str, k: int = None) -> list[dict[str, Any]]:
        """Retrieve relevant factual memories."""
        await self.initialize()

        if k is None:
            k = self.config.max_memories_per_query

        # Use RAG agent to retrieve
        result = await self._rag_agent.arun({"query": query})
        retrieved_docs = result.get("retrieved_documents", [])

        # Convert back to memory format
        facts = []
        for doc in retrieved_docs[:k]:
            if isinstance(doc, Document):
                fact = {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "memory_type": doc.metadata.get("memory_type", "factual"),
                    "importance": doc.metadata.get("importance", "medium"),
                    "confidence": doc.metadata.get("confidence", 0.8),
                }
                facts.append(fact)

        logger.info(f"Retrieved {len(facts)} factual memories for: {query}")
        return facts

    def _memory_to_document(self, memory: EnhancedMemoryItem) -> Document:
        """Convert memory item to document."""
        return Document(
            page_content=memory.content,
            metadata={
                "memory_id": memory.id,
                "memory_type": memory.memory_type.value,
                "importance": memory.importance.value,
                "confidence": memory.confidence,
                "tags": memory.tags,
                "source": memory.source,
                "timestamp": memory.created_at.isoformat(),
                "access_count": memory.access_count,
            },
        )

    def _memories_to_documents(
        self, memories: list[EnhancedMemoryItem]
    ) -> list[Document]:
        """Convert multiple memories to documents."""
        return [self._memory_to_document(mem) for mem in memories]

    async def _update_vector_store(self, new_documents: list[Document]) -> None:
        """Update vector store with new documents."""
        try:
            # Recreate with all documents
            all_documents = self._memories_to_documents(self._memories)
            self._rag_agent = BaseRAGAgent.from_documents(
                documents=all_documents,
                embedding_model=self.config.embedding_model,
                vector_store_provider=self.config.vector_store_provider,
                name=self.name,
            )
            logger.info("Updated factual memory store")
        except Exception as e:
            logger.error(f"Failed to update factual memory store: {e}")


class PreferencesMemoryAgent:
    """Memory agent for user preferences using BaseRAGAgent."""

    def __init__(self, config: MemoryRAGConfig, name: str = "preferences_memory"):
        """Initialize preferences memory agent."""
        self.config = config
        self.name = name
        self._rag_agent: SimpleRAGAgent | None = (
            None  # Use SimpleRAGAgent for generation
        )
        self._preferences: list[EnhancedMemoryItem] = []
        self._initialized = False

        logger.info(f"Initialized PreferencesMemoryAgent: {name}")

    async def initialize(self) -> None:
        """Initialize the underlying RAG agent."""
        if self._initialized:
            return

        if not self._preferences:
            # Create placeholder
            placeholder = EnhancedMemoryItem(
                content="Initial preferences store",
                source="system",
                memory_type=MemoryType.PREFERENCE,
                importance=ImportanceLevel.LOW,
                tags=["system"],
                confidence=1.0,
            )
            self._preferences.append(placeholder)

        # Convert to documents
        documents = self._preferences_to_documents(self._preferences)

        # Create SimpleRAGAgent for answer generation
        self._rag_agent = SimpleRAGAgent.from_documents(
            documents=documents,
            llm_config=self.config.llm_config,
            embedding_model=self.config.embedding_model,
            vector_store_provider=self.config.vector_store_provider,
            name=self.name,
        )

        self._initialized = True
        logger.info(
            f"Initialized preferences RAG agent with {len(self._preferences)} preferences"
        )

    async def add_preference(self, preference: EnhancedMemoryItem) -> None:
        """Add a user preference."""
        # Ensure it's marked as preference type
        preference.memory_type = MemoryType.PREFERENCE
        self._preferences.append(preference)

        if self._initialized:
            await self._update_agent()

        logger.info(f"Added preference: {preference.content[:50]}...")

    async def get_preferences_for(self, context: str) -> str:
        """Get relevant preferences and generate summary."""
        await self.initialize()

        query = f"What are the user's preferences related to: {context}"

        # Use SimpleRAGAgent for full RAG pipeline (retrieval + generation)
        result = await self._rag_agent.arun({"query": query})

        # SimpleRAGAgent returns generated answer
        answer = result.get("answer", "No relevant preferences found")
        retrieved_docs = result.get("retrieved_documents", [])

        logger.info(
            f"Generated preference summary for '{context}': {len(retrieved_docs)} docs retrieved"
        )
        return answer

    async def check_preference_conflict(self, new_preference: str) -> dict[str, Any]:
        """Check if new preference conflicts with existing ones."""
        await self.initialize()

        query = (
            f"Does this preference conflict with existing preferences: {new_preference}"
        )
        result = await self._rag_agent.arun({"query": query})

        return {
            "analysis": result.get("answer", "No analysis available"),
            "retrieved_preferences": result.get("retrieved_documents", []),
        }

    def _preferences_to_documents(
        self, preferences: list[EnhancedMemoryItem]
    ) -> list[Document]:
        """Convert preferences to documents."""
        documents = []
        for pref in preferences:
            doc = Document(
                page_content=pref.content,
                metadata={
                    "memory_id": pref.id,
                    "type": "preference",
                    "importance": pref.importance.value,
                    "confidence": pref.confidence,
                    "tags": pref.tags,
                    "timestamp": pref.created_at.isoformat(),
                },
            )
            documents.append(doc)
        return documents

    async def _update_agent(self) -> None:
        """Update the RAG agent with current preferences."""
        try:
            documents = self._preferences_to_documents(self._preferences)
            self._rag_agent = SimpleRAGAgent.from_documents(
                documents=documents,
                llm_config=self.config.llm_config,
                embedding_model=self.config.embedding_model,
                vector_store_provider=self.config.vector_store_provider,
                name=self.name,
            )
            logger.info("Updated preferences RAG agent")
        except Exception as e:
            logger.error(f"Failed to update preferences agent: {e}")


class UnifiedMemoryRAGAgent:
    """Unified memory agent coordinating multiple specialized memory agents."""

    def __init__(self, config: MemoryRAGConfig, user_id: str = None):
        """Initialize unified memory agent."""
        self.config = config
        self.user_id = user_id or f"user_{uuid4()}"

        # Initialize specialized memory agents
        self.conversation_memory = ConversationMemoryAgent(
            config, f"conversation_{self.user_id}"
        )
        self.factual_memory = FactualMemoryAgent(config, f"factual_{self.user_id}")
        self.preferences_memory = PreferencesMemoryAgent(
            config, f"preferences_{self.user_id}"
        )

        # Message converter for conversation processing
        self.message_converter = MessageDocumentConverter(user_id=self.user_id)

        logger.info(f"Initialized UnifiedMemoryRAGAgent for user: {self.user_id}")

    async def initialize(self) -> None:
        """Initialize all memory agents."""
        await asyncio.gather(
            self.conversation_memory.initialize(),
            self.factual_memory.initialize(),
            self.preferences_memory.initialize(),
        )
        logger.info("Initialized all memory agents")

    async def process_conversation(self, messages: list[BaseMessage]) -> dict[str, Any]:
        """Process conversation and extract memories."""
        # Add to conversation memory
        await self.conversation_memory.add_conversation(messages)

        # Extract factual information and preferences (simplified)
        extracted_memories = []
        extracted_preferences = []

        for message in messages:
            content = (
                str(message.content) if hasattr(message, "content") else str(message)
            )

            # Simple heuristics for demo - in production, use LLM extraction
            if any(
                word in content.lower()
                for word in ["i am", "i work", "my name", "my job"]
            ):
                # Factual information
                memory = EnhancedMemoryItem(
                    content=content,
                    source="conversation",
                    memory_type=MemoryType.FACTUAL,
                    importance=ImportanceLevel.HIGH,
                    tags=["personal", "factual"],
                    confidence=0.8,
                )
                extracted_memories.append(memory)

            elif any(
                word in content.lower()
                for word in ["i prefer", "i like", "i dislike", "i hate"]
            ):
                # Preference information
                preference = EnhancedMemoryItem(
                    content=content,
                    source="conversation",
                    memory_type=MemoryType.PREFERENCE,
                    importance=ImportanceLevel.MEDIUM,
                    tags=["preference"],
                    confidence=0.7,
                )
                extracted_preferences.append(preference)

        # Add extracted memories
        if extracted_memories:
            await self.factual_memory.add_memories(extracted_memories)

        if extracted_preferences:
            for pref in extracted_preferences:
                await self.preferences_memory.add_preference(pref)

        return {
            "conversation_messages": len(messages),
            "extracted_facts": len(extracted_memories),
            "extracted_preferences": len(extracted_preferences),
            "status": "processed",
        }

    async def retrieve_context(
        self, query: str, memory_types: list[str] = None
    ) -> dict[str, Any]:
        """Retrieve relevant context from all memory types."""
        if memory_types is None:
            memory_types = ["conversation", "factual", "preferences"]

        results = {}

        # Retrieve from each memory type in parallel
        tasks = []
        if "conversation" in memory_types:
            tasks.append(
                (
                    "conversation",
                    self.conversation_memory.retrieve_conversation_context(query),
                )
            )
        if "factual" in memory_types:
            tasks.append(("factual", self.factual_memory.retrieve_facts(query)))
        if "preferences" in memory_types:
            tasks.append(
                ("preferences", self.preferences_memory.get_preferences_for(query))
            )

        # Execute in parallel
        for memory_type, task in tasks:
            try:
                result = await task
                results[memory_type] = result
            except Exception as e:
                logger.error(f"Failed to retrieve {memory_type} memory: {e}")
                results[memory_type] = []

        return results

    async def get_memory_summary(self) -> dict[str, Any]:
        """Get summary of all stored memories."""
        return {
            "user_id": self.user_id,
            "conversation_documents": len(self.conversation_memory._documents),
            "factual_memories": len(self.factual_memory._memories),
            "preferences": len(self.preferences_memory._preferences),
            "storage_backend": self.config.vector_store_provider.value,
            "embedding_model": self.config.embedding_model.model,
        }

    # Agent-as-tool pattern support
    @classmethod
    def as_tool(cls, name: str = None, description: str = None, **config_kwargs):
        """Convert this agent to a tool for use in other agents."""
        from langchain_core.tools import tool

        if name is None:
            name = "unified_memory"
        if description is None:
            description = "Search and retrieve user memory including conversations, facts, and preferences"

        config = MemoryRAGConfig(**config_kwargs)
        agent = cls(config)

        @tool(name=name, description=description)
        async def memory_tool(query: str) -> str:
            """Search memory and return relevant context."""
            await agent.initialize()
            context = await agent.retrieve_context(query)

            # Format context for tool response
            formatted_context = []

            if "conversation" in context:
                conversations = context["conversation"]
                if conversations:
                    formatted_context.append(
                        f"Recent conversations: {len(conversations)} relevant messages"
                    )

            if "factual" in context:
                facts = context["factual"]
                if facts:
                    fact_contents = [f["content"] for f in facts[:3]]
                    formatted_context.append(f"Known facts: {'; '.join(fact_contents)}")

            if "preferences" in context:
                prefs = context["preferences"]
                if isinstance(prefs, str) and prefs.strip():
                    formatted_context.append(f"User preferences: {prefs}")

            return (
                "\n".join(formatted_context)
                if formatted_context
                else "No relevant memory found"
            )

        return memory_tool


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_conversation_memory_agent(
    vector_store_provider: VectorStoreProvider = VectorStoreProvider.FAISS,
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2",
    enable_time_weighting: bool = True,
    name: str = "conversation_memory",
) -> ConversationMemoryAgent:
    """Factory function to create conversation memory agent."""
    config = MemoryRAGConfig(
        vector_store_provider=vector_store_provider,
        embedding_model=HuggingFaceEmbeddingConfig(model=embedding_model),
        enable_time_weighting=enable_time_weighting,
    )

    return ConversationMemoryAgent(config, name)


def create_factual_memory_agent(
    vector_store_provider: VectorStoreProvider = VectorStoreProvider.FAISS,
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2",
    similarity_threshold: float = 0.7,
    name: str = "factual_memory",
) -> FactualMemoryAgent:
    """Factory function to create factual memory agent."""
    config = MemoryRAGConfig(
        vector_store_provider=vector_store_provider,
        embedding_model=HuggingFaceEmbeddingConfig(model=embedding_model),
        similarity_threshold=similarity_threshold,
    )

    return FactualMemoryAgent(config, name)


def create_unified_memory_agent(
    user_id: str = None,
    llm_config: AugLLMConfig = None,
    vector_store_provider: VectorStoreProvider = VectorStoreProvider.FAISS,
    embedding_model: str = "sentence-transformers/all-mpnet-base-v2",
) -> UnifiedMemoryRAGAgent:
    """Factory function to create unified memory agent."""
    if llm_config is None:
        llm_config = AugLLMConfig()

    config = MemoryRAGConfig(
        llm_config=llm_config,
        vector_store_provider=vector_store_provider,
        embedding_model=HuggingFaceEmbeddingConfig(model=embedding_model),
    )

    return UnifiedMemoryRAGAgent(config, user_id)


# ============================================================================
# PERSISTENT STORAGE VARIANTS
# ============================================================================


def create_postgresql_memory_agent(
    connection_string: str, user_id: str = None, table_name: str = "user_memories"
) -> UnifiedMemoryRAGAgent:
    """Create memory agent with PostgreSQL persistence."""
    # Note: This would need proper PGVectorStoreConfig integration
    config = MemoryRAGConfig(
        vector_store_provider=VectorStoreProvider.POSTGRESQL, persistent_storage=True
    )

    return UnifiedMemoryRAGAgent(config, user_id)


def create_supabase_memory_agent(
    supabase_url: str, supabase_key: str, user_id: str = None
) -> UnifiedMemoryRAGAgent:
    """Create memory agent with Supabase persistence."""
    config = MemoryRAGConfig(
        vector_store_provider=VectorStoreProvider.SUPABASE, persistent_storage=True
    )

    return UnifiedMemoryRAGAgent(config, user_id)


if __name__ == "__main__":
    # Demo usage
    async def demo():
        # Create unified memory agent
        agent = create_unified_memory_agent(user_id="demo_user")
        await agent.initialize()

        # Add some conversation
        messages = [
            HumanMessage(
                content="Hi, I'm Alice and I work as a software engineer at Google"
            ),
            AIMessage(
                content="Nice to meet you Alice! How long have you been at Google?"
            ),
            HumanMessage(
                content="About 3 years now. I prefer morning meetings and I really dislike long emails."
            ),
        ]

        # Process conversation
        result = await agent.process_conversation(messages)
        print(f"Processed: {result}")

        # Retrieve context
        context = await agent.retrieve_context("What do I know about Alice?")
        print(f"Context: {context}")

        # Get summary
        summary = await agent.get_memory_summary()
        print(f"Memory summary: {summary}")

    asyncio.run(demo())


# ============================================================================
# MAIN EXPORT ALIAS
# ============================================================================

# Export UnifiedMemoryRAGAgent as the main RAGMemoryAgent for import compatibility
RAGMemoryAgent = UnifiedMemoryRAGAgent
