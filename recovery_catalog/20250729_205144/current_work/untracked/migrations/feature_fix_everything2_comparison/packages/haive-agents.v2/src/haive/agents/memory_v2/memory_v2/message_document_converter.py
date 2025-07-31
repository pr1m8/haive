"""Message to Document Converter for Memory V2 System.

This module converts conversation messages into timestamped documents
following LangChain patterns for long-term memory agents and graph construction.

Based on: https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/
"""

import logging
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from .memory_state_original import EnhancedMemoryItem, ImportanceLevel

logger = logging.getLogger(__name__)


class MessageMetadata(BaseModel):
    """Enhanced metadata for message-based documents."""

    # Core message info
    message_id: str = Field(default_factory=lambda: str(uuid4()))
    message_type: str = Field(...)  # "human", "ai", "system"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Conversation context
    conversation_id: str | None = Field(default=None)
    user_id: str | None = Field(default=None)
    session_id: str | None = Field(default=None)
    turn_number: int = Field(default=0)

    # Content analysis
    content_length: int = Field(default=0)
    estimated_tokens: int = Field(default=0)
    language: str = Field(default="en")

    # Memory relevance
    memory_importance: ImportanceLevel = Field(default=ImportanceLevel.MEDIUM)
    contains_personal_info: bool = Field(default=False)
    contains_technical_info: bool = Field(default=False)
    contains_temporal_info: bool = Field(default=False)

    # Extraction flags
    needs_entity_extraction: bool = Field(default=True)
    needs_sentiment_analysis: bool = Field(default=True)
    processed_for_memory: bool = Field(default=False)


class TimestampedDocument(Document):
    """Document with enhanced timestamp and metadata for memory retrieval."""

    def __init__(self, page_content: str, metadata: dict[str, Any] = None):
        """Initialize with enhanced metadata."""
        if metadata is None:
            metadata = {}

        # Ensure timestamp exists
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.now(UTC).isoformat()

        # Ensure document ID exists
        if "doc_id" not in metadata:
            metadata["doc_id"] = str(uuid4())

        super().__init__(page_content=page_content, metadata=metadata)

    @property
    def timestamp(self) -> datetime:
        """Get timestamp as datetime object."""
        timestamp_str = self.metadata.get("timestamp")
        if isinstance(timestamp_str, str):
            return datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        if isinstance(timestamp_str, datetime):
            return timestamp_str
        return datetime.now(UTC)

    @property
    def age_hours(self) -> float:
        """Get document age in hours."""
        now = datetime.now(UTC)
        return (now - self.timestamp).total_seconds() / 3600

    @property
    def age_days(self) -> float:
        """Get document age in days."""
        return self.age_hours / 24


class MessageDocumentConverter:
    """Converts conversation messages into timestamped documents for memory storage."""

    def __init__(
        self,
        conversation_id: str | None = None,
        user_id: str | None = None,
        session_id: str | None = None,
    ):
        """Initialize converter with context."""
        self.conversation_id = conversation_id or f"conv_{uuid4()}"
        self.user_id = user_id
        self.session_id = session_id or f"session_{uuid4()}"
        self.turn_counter = 0

        logger.info(
            f"Initialized MessageDocumentConverter for conversation {self.conversation_id}"
        )

    def convert_message(self, message: BaseMessage) -> TimestampedDocument:
        """Convert single message to timestamped document.

        Args:
            message: LangChain message to convert

        Returns:
            TimestampedDocument with rich metadata
        """
        self.turn_counter += 1

        # Determine message type
        message_type = self._get_message_type(message)

        # Extract content
        content = self._extract_content(message)

        # Analyze content for metadata
        content_analysis = self._analyze_content(content, message_type)

        # Create enhanced metadata
        message_metadata = MessageMetadata(
            message_type=message_type,
            conversation_id=self.conversation_id,
            user_id=self.user_id,
            session_id=self.session_id,
            turn_number=self.turn_counter,
            content_length=len(content),
            estimated_tokens=len(content.split()) * 1.3,  # Rough token estimate
            **content_analysis,
        )

        # Create document metadata
        doc_metadata = {
            **message_metadata.model_dump(),
            "timestamp": message_metadata.timestamp.isoformat(),
            "source": "conversation_message",
            "conversation_context": f"{self.conversation_id}:turn_{self.turn_counter}",
        }

        # Create timestamped document
        doc = TimestampedDocument(page_content=content, metadata=doc_metadata)

        logger.debug(
            f"Converted {message_type} message to document: {len(content)} chars, turn {self.turn_counter}"
        )

        return doc

    def convert_messages(
        self, messages: list[BaseMessage]
    ) -> list[TimestampedDocument]:
        """Convert multiple messages to timestamped documents.

        Args:
            messages: List of messages to convert

        Returns:
            List of TimestampedDocuments
        """
        documents = []

        for message in messages:
            doc = self.convert_message(message)
            documents.append(doc)

        logger.info(
            f"Converted {len(messages)} messages to {len(documents)} timestamped documents"
        )

        return documents

    def create_conversation_summary_document(
        self, messages: list[BaseMessage], summary: str
    ) -> TimestampedDocument:
        """Create summary document from conversation.

        Args:
            messages: Original messages
            summary: Generated summary text

        Returns:
            TimestampedDocument containing the summary
        """
        # Analyze summary importance
        importance = self._determine_summary_importance(messages, summary)

        metadata = {
            "message_type": "conversation_summary",
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "turn_number": len(messages),
            "original_message_count": len(messages),
            "summary_length": len(summary),
            "memory_importance": importance.value,
            "contains_personal_info": self._contains_personal_info(summary),
            "contains_technical_info": self._contains_technical_info(summary),
            "processed_for_memory": True,
            "source": "conversation_summary",
            "doc_type": "summary",
        }

        return TimestampedDocument(page_content=summary, metadata=metadata)

    def create_memory_document(
        self, memory_item: EnhancedMemoryItem
    ) -> TimestampedDocument:
        """Convert memory item to timestamped document.

        Args:
            memory_item: Memory item to convert

        Returns:
            TimestampedDocument for memory storage
        """
        metadata = {
            "message_type": "extracted_memory",
            "memory_id": memory_item.id,
            "memory_type": memory_item.memory_type.value,
            "importance": memory_item.importance.value,
            "confidence": memory_item.confidence,
            "tags": memory_item.tags,
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "source": memory_item.source,
            "access_count": memory_item.access_count,
            "doc_type": "memory",
            "processed_for_memory": True,
        }

        return TimestampedDocument(page_content=memory_item.content, metadata=metadata)

    def _get_message_type(self, message: BaseMessage) -> str:
        """Determine message type from LangChain message."""
        if isinstance(message, HumanMessage):
            return "human"
        if isinstance(message, AIMessage):
            return "ai"
        if isinstance(message, SystemMessage):
            return "system"
        return "unknown"

    def _extract_content(self, message: BaseMessage) -> str:
        """Extract content from message."""
        if hasattr(message, "content") and message.content:
            return str(message.content)
        return str(message)

    def _analyze_content(self, content: str, message_type: str) -> dict[str, Any]:
        """Analyze content for metadata extraction."""
        content.lower()

        analysis = {
            "contains_personal_info": self._contains_personal_info(content),
            "contains_technical_info": self._contains_technical_info(content),
            "contains_temporal_info": self._contains_temporal_info(content),
            "memory_importance": self._determine_importance(content, message_type),
        }

        return analysis

    def _contains_personal_info(self, content: str) -> bool:
        """Check if content contains personal information."""
        personal_indicators = [
            "i am",
            "my name",
            "i work",
            "i live",
            "i like",
            "i prefer",
            "my job",
            "my role",
            "my company",
            "my team",
            "my family",
            "i enjoy",
            "i love",
            "i hate",
            "i dislike",
            "my hobby",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in personal_indicators)

    def _contains_technical_info(self, content: str) -> bool:
        """Check if content contains technical information."""
        technical_indicators = [
            "code",
            "programming",
            "algorithm",
            "database",
            "api",
            "framework",
            "python",
            "javascript",
            "sql",
            "server",
            "deployment",
            "architecture",
            "bug",
            "error",
            "debug",
            "performance",
            "optimization",
            "scalability",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in technical_indicators)

    def _contains_temporal_info(self, content: str) -> bool:
        """Check if content contains time-sensitive information."""
        temporal_indicators = [
            "today",
            "tomorrow",
            "yesterday",
            "next week",
            "last week",
            "meeting",
            "deadline",
            "due date",
            "schedule",
            "appointment",
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "january",
            "february",
            "march",
            "april",
            "may",
            "june",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in temporal_indicators)

    def _determine_importance(self, content: str, message_type: str) -> ImportanceLevel:
        """Determine importance level of content."""
        content_lower = content.lower()

        # Critical indicators
        critical_words = [
            "urgent",
            "critical",
            "important",
            "asap",
            "emergency",
            "deadline",
        ]
        if any(word in content_lower for word in critical_words):
            return ImportanceLevel.CRITICAL

        # High importance indicators
        high_words = ["decision", "meeting", "project", "launch", "release", "problem"]
        if any(word in content_lower for word in high_words) or len(content) > 200:
            return ImportanceLevel.HIGH

        # Low importance indicators
        low_words = ["hello", "hi", "thanks", "okay", "yes", "no"]
        if any(word in content_lower for word in low_words) and len(content) < 50:
            return ImportanceLevel.LOW

        # Default to medium
        return ImportanceLevel.MEDIUM

    def _determine_summary_importance(
        self, messages: list[BaseMessage], summary: str
    ) -> ImportanceLevel:
        """Determine importance of conversation summary."""
        # Longer conversations tend to be more important
        if len(messages) > 20:
            return ImportanceLevel.HIGH
        if len(messages) > 10:
            return ImportanceLevel.MEDIUM

        # Summary with key information is important
        if len(summary) > 500 or any(
            word in summary.lower() for word in ["decision", "project", "important"]
        ):
            return ImportanceLevel.HIGH

        return ImportanceLevel.MEDIUM


class ConversationDocumentBatch:
    """Batch processor for converting entire conversations to documents."""

    def __init__(self, conversation_id: str = None, user_id: str = None):
        """Initialize batch processor."""
        self.conversation_id = conversation_id or f"batch_{uuid4()}"
        self.user_id = user_id
        self.converter = MessageDocumentConverter(conversation_id, user_id)

    def process_conversation(
        self,
        messages: list[BaseMessage],
        include_summary: bool = True,
        chunk_size: int = 5,
    ) -> list[TimestampedDocument]:
        """Process entire conversation into documents.

        Args:
            messages: Conversation messages
            include_summary: Whether to create summary documents
            chunk_size: Size of message chunks for processing

        Returns:
            List of all generated documents
        """
        all_documents = []

        # Convert individual messages
        message_docs = self.converter.convert_messages(messages)
        all_documents.extend(message_docs)

        # Create chunk summaries if requested
        if include_summary and len(messages) > chunk_size:
            chunks = [
                messages[i : i + chunk_size]
                for i in range(0, len(messages), chunk_size)
            ]

            for i, chunk in enumerate(chunks):
                chunk_summary = self._create_chunk_summary(chunk, i + 1, len(chunks))
                summary_doc = self.converter.create_conversation_summary_document(
                    chunk, chunk_summary
                )
                all_documents.append(summary_doc)

        logger.info(
            f"Processed conversation: {len(messages)} messages → {len(all_documents)} documents"
        )

        return all_documents

    def _create_chunk_summary(
        self, messages: list[BaseMessage], chunk_num: int, total_chunks: int
    ) -> str:
        """Create summary for a chunk of messages."""
        # Simple extractive summary (in real implementation, use LLM)
        key_messages = []

        for msg in messages:
            content = str(msg.content) if hasattr(msg, "content") else str(msg)
            if len(content) > 50:  # Skip very short messages
                key_messages.append(
                    content[:100] + ("..." if len(content) > 100 else "")
                )

        summary = f"Conversation chunk {chunk_num}/{total_chunks}:\n"
        summary += "\n".join(f"- {msg}" for msg in key_messages[:3])

        return summary


# ============================================================================
# DOCUMENT UTILITIES
# ============================================================================


def extract_documents_by_timeframe(
    documents: list[TimestampedDocument], hours_back: float = 24
) -> list[TimestampedDocument]:
    """Extract documents from specific timeframe.

    Args:
        documents: List of timestamped documents
        hours_back: How many hours back to include

    Returns:
        Filtered list of documents
    """
    cutoff_time = datetime.now(UTC) - pd.Timedelta(hours=hours_back)

    return [doc for doc in documents if doc.timestamp >= cutoff_time]


def sort_documents_by_relevance_and_time(
    documents: list[TimestampedDocument],
    time_weight: float = 0.3,
    recency_decay: float = 0.1,
) -> list[TimestampedDocument]:
    """Sort documents by relevance and recency.

    Args:
        documents: Documents to sort
        time_weight: Weight given to recency (0.0 to 1.0)
        recency_decay: How quickly relevance decays with time

    Returns:
        Sorted documents (most relevant first)
    """

    def score_document(doc: TimestampedDocument) -> float:
        # Base relevance from importance
        importance_scores = {"critical": 1.0, "high": 0.8, "medium": 0.6, "low": 0.4}

        base_score = importance_scores.get(
            doc.metadata.get("importance", "medium"), 0.6
        )

        # Time decay factor
        age_hours = doc.age_hours
        time_factor = max(0.1, 1.0 - (age_hours * recency_decay / 24))

        # Combined score
        return base_score * (1 - time_weight) + time_factor * time_weight

    return sorted(documents, key=score_document, reverse=True)


def create_document_index(documents: list[TimestampedDocument]) -> dict[str, Any]:
    """Create searchable index of documents.

    Args:
        documents: Documents to index

    Returns:
        Index with metadata and statistics
    """
    index = {
        "total_documents": len(documents),
        "by_type": {},
        "by_importance": {},
        "by_usef": {},
        "by_conversation": {},
        "time_range": {},
        "documents": documents,
    }

    if not documents:
        return index

    # Calculate statistics
    for doc in documents:
        # By type
        doc_type = doc.metadata.get("message_type", "unknown")
        index["by_type"][doc_type] = index["by_type"].get(doc_type, 0) + 1

        # By importance
        importance = doc.metadata.get("importance", "medium")
        index["by_importance"][importance] = (
            index["by_importance"].get(importance, 0) + 1
        )

        # By user
        user_id = doc.metadata.get("user_id", "unknown")
        index["by_user"][user_id] = index["by_user"].get(user_id, 0) + 1

        # By conversation
        conv_id = doc.metadata.get("conversation_id", "unknown")
        index["by_conversation"][conv_id] = index["by_conversation"].get(conv_id, 0) + 1

    # Time range
    timestamps = [doc.timestamp for doc in documents]
    if timestamps:
        index["time_range"] = {
            "earliest": min(timestamps).isoformat(),
            "latest": max(timestamps).isoformat(),
            "span_hours": (max(timestamps) - min(timestamps)).total_seconds() / 3600,
        }

    return index
