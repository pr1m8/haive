"""Memory classification system using LLM-based analysis.

This module provides intelligent classification of memories into types, importance
scoring, and metadata extraction using language models.
"""

import logging
import re
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field

from haive.agents.memory.core.types import (
    MemoryClassificationResult,
    MemoryEntry,
    MemoryImportance,
    MemoryQueryIntent,
    MemoryType,
    Optional,
    Union,
    from,
    import,
    typing,
)

logger = logging.getLogger(__name__)


class MemoryClassifierConfig(BaseModel):
    """Configuration for memory classification system.
    """

    llm_config: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="LLM for classification"
    )
    enable_entity_extraction: bool = Field(
        default=True, description="Extract named entities"
    )
    enable_sentiment_analysis: bool = Field(
        default=True, description="Analyze sentiment"
    )
    enable_topic_modeling: bool = Field(
        default=True, description="Extract topics")

    # Classification thresholds
    importance_threshold_high: float = Field(
        default=0.7, description="Threshold for high importance"
    )
    importance_threshold_critical: float = Field(
        default=0.9, description="Threshold for critical importance"
    )
    confidence_threshold: float = Field(
        default=0.6, description="Minimum confidence for classification"
    )

    # Processing limits
    max_content_length: int = Field(
        default=2000, description="Maximum content length for analysis"
    )
    batch_size: int = Field(
        default=10, description="Batch size for bulk classification"
    )


class MemoryClassifier:
    """LLM-based memory classifier for automatic memory type detection and metadata
    extraction.

    This classifier analyzes memory content to:
    - Determine memory types (semantic, episodic, procedural, etc.)
    - Calculate importance scores
    - Extract entities, topics, and sentiment
    - Provide classification reasoning
    """

    def __init__(self, config: MemoryClassifierConfig = None):
        """Initialize memory classifier with configuration.
        """
        self.config = config or MemoryClassifierConfig()
        self._setup_llm()
        self._setup_classification_prompts()

    def _setup_llm(self) -> None:
        """Setup LLM for classification tasks.
        """
        # Configure LLM for classification
        self.config.llm_config.temperature = (
            0.1  # Low temperature for consistent classification
        )
        self.config.llm_config.max_tokens = (
            1000  # Sufficient for classification response
        )

        # Setup structured output for classification results
        self.config.llm_config.structured_output_model = MemoryClassificationResult
        self.config.llm_config.structured_output_version = "v2"

        self.llm = self.config.llm_config.create_runnable()

    def _setup_classification_prompts(self) -> None:
        """Setup prompts for different classification tasks.
        """
        self.classification_prompt = """You are an expert memory analyst. Analyze the given content and classify it according to cognitive memory types.

MEMORY TYPES:
- SEMANTIC: Facts, concepts, definitions, general knowledge (e.g., "Paris is the capital of France")
- EPISODIC: Specific events, personal experiences, conversations (e.g., "Yesterday I met John at the coffee shop")
- PROCEDURAL: How-to knowledge, processes, workflows (e.g., "To make coffee, first heat water to 200°F")
- CONTEXTUAL: Relationships between entities, social connections (e.g., "John works at Microsoft and knows Sarah")
- PREFERENCE: User likes, dislikes, behavioral patterns (e.g., "I prefer tea over coffee in the morning")
- META: Self-awareness, learning patterns, thoughts about thinking (e.g., "I notice I learn better with examples")
- EMOTIONAL: Feelings, sentiments, emotional context (e.g., "I felt frustrated when the meeting was cancelled")
- TEMPORAL: Time-based patterns, scheduling, temporal relationships (e.g., "I usually exercise at 6 AM")
- ERROR: Mistakes, corrections, error patterns (e.g., "I was wrong about the meeting time")
- FEEDBACK: User corrections, evaluations, reviews (e.g., "That summary was too long, please be more concise")
- SYSTEM: Configuration, settings, system-related information (e.g., "Set notification frequency to daily")

IMPORTANCE LEVELS:
- CRITICAL (0.9-1.0): Essential information that should never be forgotten
- HIGH (0.7-0.9): Important information for long-term retention
- MEDIUM (0.4-0.7): Standard information with moderate importance
- LOW (0.1-0.4): Short-term relevance, may be forgotten over time
- TRANSIENT (0.0-0.1): Temporary information, can be discarded

Your task:
1. Identify ALL applicable memory types (content can have multiple types)
2. Determine importance level and numerical score
3. Extract named entities (people, places, organizations, etc.)
4. Identify key topics/themes
5. Analyze sentiment if applicable (-1.0 to 1.0)
6. Provide reasoning for your classification

Content to analyze: {content}

User context (if available): {user_context}

Conversation context (if available): {conversation_context}"""

        self.query_intent_prompt = """Analyze the user query to understand what type of memory information they're seeking.

MEMORY TYPES TO CONSIDER:
- SEMANTIC: Factual questions, definitions
- EPISODIC: Questions about past events, conversations
- PROCEDURAL: How-to questions, process information
- CONTEXTUAL: Relationship questions, connections
- PREFERENCE: Questions about likes, dislikes, patterns
- META: Self-reflection questions
- EMOTIONAL: Questions about feelings, sentiment
- TEMPORAL: Time-based questions

COMPLEXITY LEVELS:
- simple: Direct factual lookup
- moderate: Requires some reasoning or cross-referencing
- complex: Requires multi-step reasoning or synthesis

TEMPORAL SCOPE:
- recent: Information from recent conversations/interactions
- historical: Information from longer time periods
- all: No time constraints

Query: {query}

Determine:
1. What memory types are most relevant
2. Query complexity level
3. Temporal scope needed
4. Whether reasoning/synthesis is required
5. Entities and topics mentioned
6. Suggested retrieval strategy
"""

    def classify_memory(
        self,
        content: str,
        user_context: dict[str, Any] | None = None,
        conversation_context: dict[str, Any] | None = None,
    ) -> MemoryClassificationResult:
        """Classify a single memory content into types and extract metadata.

        Args:
            content: Memory content to classify
            user_context: Optional user context for classification
            conversation_context: Optional conversation context

        Returns:
            MemoryClassificationResult with types, importance, and metadata
        """
        try:
            # Truncate content if too long
            if len(content) > self.config.max_content_length:
                content = content[: self.config.max_content_length] + "..."
                logger.warning(
                    f"Content truncated to {
                        self.config.max_content_length} characters")

            # Prepare context strings
            user_context_str = str(
                user_context) if user_context else "None provided"
            conversation_context_str = (
                str(conversation_context) if conversation_context else "None provided")

            # Format prompt
            prompt = self.classification_prompt.format(
                content=content,
                user_context=user_context_str,
                conversation_context=conversation_context_str,
            )

            # Get LLM classification
            result = self.llm.invoke(
                {"messages": [{"role": "user", "content": prompt}]}
            )

            # Extract structured result
            if hasattr(result, "content"):
                # Parse structured output if available
                return self._parse_classification_result(
                    result.content, content)
            # Fallback to manual parsing
            return self._fallback_classification(content)

        except Exception as e:
            logger.exception(f"Error classifying memory: {e}")
            return self._fallback_classification(content)

    def classify_query_intent(self, query: str) -> MemoryQueryIntent:
        """Analyze user query to determine memory retrieval intent.

        Args:
            query: User query to analyze

        Returns:
            MemoryQueryIntent with retrieval strategy and parameters
        """
        try:
            prompt = self.query_intent_prompt.format(query=query)

            # Use basic LLM for intent analysis (no structured output needed)
            basic_llm = AugLLMConfig(temperature=0.2).create_runnable()
            result = basic_llm.invoke(
                {"messages": [{"role": "user", "content": prompt}]}
            )

            # Parse intent from response
            return self._parse_query_intent(
                result.content if hasattr(
                    result, "content") else str(result), query)

        except Exception as e:
            logger.exception(f"Error analyzing query intent: {e}")
            return self._fallback_query_intent(query)

    def batch_classify(
        self, contents: list[str], contexts: list[dict[str, Any]] | None = None
    ) -> list[MemoryClassificationResult]:
        """Classify multiple memories in batch for efficiency.

        Args:
            contents: List of memory contents to classify
            contexts: Optional list of contexts for each memory

        Returns:
            List of MemoryClassificationResult for each content
        """
        results = []
        contexts = contexts or [{}] * len(contents)

        # Process in batches
        for i in range(0, len(contents), self.config.batch_size):
            batch_contents = contents[i: i + self.config.batch_size]
            batch_contexts = contexts[i: i + self.config.batch_size]

            batch_results = []
            for content, context in zip(
                    batch_contents, batch_contexts, strict=False):
                result = self.classify_memory(
                    content,
                    context.get("user_context"),
                    context.get("conversation_context"),
                )
                batch_results.append(result)

            results.extend(batch_results)

        return results

    def create_memory_entry(
        self,
        content: str,
        user_context: dict[str, Any] | None = None,
        conversation_context: dict[str, Any] | None = None,
        namespace: Optional[str] = None,
    ) -> MemoryEntry:
        """Create a complete memory entry with automatic classification.

        Args:
            content: Memory content
            user_context: Optional user context
            conversation_context: Optional conversation context
            namespace: Optional memory namespace

        Returns:
            MemoryEntry with full classification and metadata
        """
        # Classify the memory
        classification = self.classify_memory(
            content, user_context, conversation_context
        )

        # Create memory entry
        entry = MemoryEntry(
            content=content,
            memory_types=classification.memory_types,
            importance=classification.importance,
            importance_score=classification.importance_score,
            entities=classification.entities,
            topics=classification.topics,
            sentiment=classification.sentiment,
            confidence=classification.confidence,
            user_context=user_context or {},
            session_context=conversation_context or {},
            namespace=namespace,
        )

        # Calculate initial weight
        entry.calculate_current_weight()

        return entry

    def _parse_classification_result(
        self, llm_response: str, original_content: str
    ) -> MemoryClassificationResult:
        """Parse LLM response into structured classification result.
        """
        try:
            # If structured output worked, this should already be parsed
            # This is a fallback parser for non-structured responses

            # Extract memory types using regex
            memory_types = []
            for memory_type in MemoryType:
                if memory_type.value.upper() in llm_response.upper():
                    memory_types.append(memory_type)

            # Extract importance score
            importance_score = 0.5  # Default
            score_match = re.search(
                r"(?: Union[importance, score])[:\s]+([0-9]*\.?[0-9]+)",
                llm_response.lower())
            if score_match:
                importance_score = min(
                    1.0, max(
                        0.0, float(
                            score_match.group(1))))

            # Determine importance level
            if importance_score >= self.config.importance_threshold_critical:
                importance = MemoryImportance.CRITICAL
            elif importance_score >= self.config.importance_threshold_high:
                importance = MemoryImportance.HIGH
            elif importance_score >= 0.4:
                importance = MemoryImportance.MEDIUM
            elif importance_score >= 0.1:
                importance = MemoryImportance.LOW
            else:
                importance = MemoryImportance.TRANSIENT

            # Extract entities (simple approach)
            entities = self._extract_entities_simple(original_content)

            # Extract topics (simple approach)
            topics = self._extract_topics_simple(original_content)

            return MemoryClassificationResult(
                memory_types=memory_types or [
                    MemoryType.SEMANTIC],  # Default fallback
                importance=importance,
                importance_score=importance_score,
                entities=entities,
                topics=topics,
                confidence=0.7,  # Medium confidence for parsed result
                reasoning="Parsed from LLM response",
            )

        except Exception as e:
            logger.exception(f"Error parsing classification result: {e}")
            return self._fallback_classification(original_content)

    def _fallback_classification(
            self, content: str) -> MemoryClassificationResult:
        """Provide fallback classification when LLM fails.
        """
        # Simple rule-based classification
        memory_types = [MemoryType.SEMANTIC]  # Default to semantic

        # Simple heuristics
        if any(
            word in content.lower()
            for word in ["i", "me", "my", "yesterday", "today", "conversation"]
        ):
            memory_types.append(MemoryType.EPISODIC)

        if any(
            word in content.lower()
            for word in ["how to", "steps", "process", "procedure"]
        ):
            memory_types.append(MemoryType.PROCEDURAL)

        if any(
            word in content.lower()
            for word in ["prefer", "like", "dislike", "favorite"]
        ):
            memory_types.append(MemoryType.PREFERENCE)

        return MemoryClassificationResult(
            memory_types=memory_types,
            importance=MemoryImportance.MEDIUM,
            importance_score=0.5,
            entities=self._extract_entities_simple(content),
            topics=self._extract_topics_simple(content),
            confidence=0.3,  # Low confidence for fallback
            reasoning="Fallback rule-based classification",
        )

    def _parse_query_intent(
        self, llm_response: str, original_query: str
    ) -> MemoryQueryIntent:
        """Parse LLM response for query intent analysis.
        """
        # Simple parsing for now - could be enhanced with structured output
        memory_types = []
        for memory_type in MemoryType:
            if memory_type.value.upper() in llm_response.upper():
                memory_types.append(memory_type)

        # Default complexity analysis
        complexity = "simple"
        if any(
            word in original_query.lower()
            for word in ["analyze", "compare", "relationship", "synthesis"]
        ):
            complexity = "complex"
        elif any(
            word in original_query.lower()
            for word in ["explain", "describe", "tell me about"]
        ):
            complexity = "moderate"

        return MemoryQueryIntent(
            memory_types=memory_types or [
                MemoryType.SEMANTIC],
            complexity=complexity,
            temporal_scope="recent" if "recent" in original_query.lower() else "all",
            requires_reasoning=complexity in [
                "moderate",
                "complex"],
            entities=self._extract_entities_simple(original_query),
            topics=self._extract_topics_simple(original_query),
            preferred_retrieval_strategy=(
                "semantic" if MemoryType.SEMANTIC in memory_types else "episodic"),
        )

    def _fallback_query_intent(self, query: str) -> MemoryQueryIntent:
        """Provide fallback query intent when LLM fails.
        """
        return MemoryQueryIntent(
            memory_types=[MemoryType.SEMANTIC],
            complexity="simple",
            temporal_scope="recent",
            requires_reasoning=False,
            entities=self._extract_entities_simple(query),
            topics=self._extract_topics_simple(query),
            preferred_retrieval_strategy="semantic",
        )

    def _extract_entities_simple(self, text: str) -> list[str]:
        """Simple entity extraction using regex patterns.
        """
        entities = []

        # Extract capitalized words (potential proper nouns)
        capitalized = re.findall(r"\b[A-Z][a-z]+\b", text)
        entities.extend(capitalized)

        # Extract common entity patterns
        email_pattern = f"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{
            2, }\b"
        emails = re.findall(email_pattern, text)
        entities.extend(emails)

        # Remove duplicates while preserving order
        seen = set()
        unique_entities = []
        for entity in entities:
            if entity.lower() not in seen:
                seen.add(entity.lower())
                unique_entities.append(entity)

        return unique_entities[:10]  # Limit to top 10

    def _extract_topics_simple(self, text: str) -> list[str]:
        """Simple topic extraction using key analysis.
        """
        # Common topic keywords
        topic_keywords = {
            "technology": ["computer", "software", "app", "website", "digital", "tech"],
            "business": ["company", "meeting", "project", "client", "work", "office"],
            "personal": [
                "family",
                "friend",
                "home",
                "personal",
                "life",
                "relationship",
            ],
            "health": ["doctor", "medicine", "health", "exercise", "diet", "medical"],
            "education": [
                "school",
                "university",
                "learn",
                "study",
                "education",
                "course",
            ],
            "travel": ["trip", "vacation", "travel", "hotel", "flight", "destination"],
            "food": ["restaurant", "food", "meal", "cook", "recipe", "eat"],
            "entertainment": [
                "movie",
                "music",
                "book",
                "game",
                "show",
                "entertainment",
            ],
        }

        text_lower = text.lower()
        detected_topics = []

        for topic, keywords in topic_keywords.items():
            if any(key in text_lower for key in keywords):
                detected_topics.append(topic)

        return detected_topics
