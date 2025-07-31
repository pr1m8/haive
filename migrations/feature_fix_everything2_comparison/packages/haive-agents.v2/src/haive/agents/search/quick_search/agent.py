"""Quick Search Agent implementation.

Provides fast, basic search responses optimized for speed and concise answers. Similar
to Perplexity's Quick Search feature.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import Tool

from haive.agents.memory.search.base import BaseSearchAgent, SearchResponse
from haive.agents.memory.search.quick_search.models import QuickSearchResponse

logger = logging.getLogger(__name__)


class QuickSearchAgent(BaseSearchAgent):
    """Agent for fast, basic search responses.

    Optimized for speed and concise answers. Provides quick factual responses
    without deep research or complex analysis.

    Features:
    - Fast response times (< 2 seconds target)
    - Concise, direct answers
    - Basic source attribution
    - Memory integration for context
    - Key extraction

    Examples:
        Basic usage::

            agent = QuickSearchAgent(
                name="quick_search",
                engine=AugLLMConfig(temperature=0.1)
            )

            response = await agent.process_search("What is the capital of France?")
            print(response.response)  # "The capital of France is Paris..."

        With custom configuration::

            agent = QuickSearchAgent(
                name="quick_search",
                engine=AugLLMConfig(
                    temperature=0.0,  # Deterministic for facts
                    max_tokens=150    # Keep responses short
                )
            )
    """

    def __init__(
        self,
        name: str = "quick_search_agent",
        engine: AugLLMConfig | None = None,
        search_tools: list[Tool] | None = None,
        **kwargs,
    ):
        """Initialize the Quick Search Agent.

        Args:
            name: Agent identifier
            engine: LLM configuration (defaults to optimized settings)
            search_tools: Optional search tools
            **kwargs: Additional arguments passed to parent
        """
        # Default engine optimized for quick responses
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.1,  # Low temperature for factual consistency
                max_tokens=200,  # Keep responses concise
                system_message=self.get_system_prompt(),
            )

        super().__init__(name=name, engine=engine, search_tools=search_tools, **kwargs)

        logger.info(f"Initialized QuickSearchAgent: {name}")

    def get_response_model(self) -> type[SearchResponse]:
        """Get the response model for quick search."""
        return QuickSearchResponse

    def get_system_prompt(self) -> str:
        """Get the system prompt for quick search operations."""
        return """You are a Quick Search Assistant designed to provide fast, accurate, and concise answers to user queries.

Your role is to:
1. Provide direct, factual answers in 1-3 sentences
2. Focus on the most important information
3. Use clear, simple language
4. Include basic source attribution when possible
5. Avoid unnecessary elaboration or tangents

Response Guidelines:
- Keep answers under 200 characters when possible
- Lead with the most direct answer
- Use factual, authoritative tone
- Include relevant keywords
- Mention uncertainty if information is unclear

Examples:
Query: "What is the capital of Japan?"
Response: "The capital of Japan is Tokyo. It is the largest city in Japan and the seat of government."

Query: "How tall is Mount Everest?"
Response: "Mount Everest is 8,848.86 meters (29,031.7 feet) tall, making it the world's highest mountain peak."

Remember: Speed and accuracy are more important than comprehensive coverage."""

    def get_search_instructions(self) -> str:
        """Get specific search instructions for quick search."""
        return """QUICK SEARCH INSTRUCTIONS:

1. IDENTIFY QUERY TYPE:
   - Factual question (who, what, where, when)
   - Definition request
   - Simple calculation or comparison
   - Basic how-to question

2. PROVIDE DIRECT ANSWER:
   - Start with the most direct response
   - Use 1-3 sentences maximum
   - Include key facts and figures
   - Avoid unnecessary context

3. KEYWORD EXTRACTION:
   - Identify 2-5 key terms from the query
   - Include these in your response naturally
   - Help with searchability and relevance

4. CONFIDENCE ASSESSMENT:
   - High confidence (0.9+): Well-established facts
   - Medium confidence (0.7-0.9): Generally accepted information
   - Low confidence (0.5-0.7): Uncertain or complex topics

5. MEMORY INTEGRATION:
   - Check for related previous searches
   - Use context to improve answers
   - Avoid contradicting recent information

Process the query efficiently and provide a clear, concise response."""

    def extract_keywords(self, query: str) -> list[str]:
        """Extract key terms from the search query.

        Args:
            query: The search query

        Returns:
            List of key terms
        """
        # Simple key extraction (can be enhanced with NLP)
        stop_words = {
            "the",
            "is",
            "at",
            "which",
            "on",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "with",
            "to",
            "for",
            "of",
            "as",
            "by",
            "what",
            "how",
            "when",
            "where",
            "who",
            "why",
        }

        words = query.lower().split()
        keywords = [
            word.strip(".,!?;:")
            for word in words
            if word.strip(".,!?;:") not in stop_words and len(word) > 2
        ]

        return keywords[:5]  # Return top 5 keywords

    def determine_answer_type(self, query: str) -> str:
        """Determine the type of answer needed.

        Args:
            query: The search query

        Returns:
            Answer type classification
        """
        query_lower = query.lower()

        if query_lower.startswith(("what is", "what are", "define")):
            return "definition"
        if query_lower.startswith(("who is", "who was", "who are")):
            return "biographical"
        if query_lower.startswith(("when is", "when was", "when did")):
            return "temporal"
        if query_lower.startswith(("where is", "where was", "where are")):
            return "geographical"
        if query_lower.startswith(("how to", "how do", "how can")):
            return "procedural"
        if query_lower.startswith(("how much", "how many", "how tall", "how long")):
            return "quantitative"
        if query_lower.startswith(("why is", "why do", "why did")):
            return "explanatory"
        return "factual"

    async def process_search(
        self,
        query: str,
        context: dict[str, Any] | None = None,
        save_to_memory: bool = True,
    ) -> QuickSearchResponse:
        """Process a quick search query.

        Args:
            query: The search query
            context: Optional context
            save_to_memory: Whether to save to memory

        Returns:
            Quick search response
        """
        import time

        start_time = time.time()

        logger.info(f"Processing quick search: {query}")

        # Extract keywords and determine answer type
        keywords = self.extract_keywords(query)
        answer_type = self.determine_answer_type(query)

        # Get base response
        base_response = await super().process_search(query, context, save_to_memory)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Create quick search specific response
        response = QuickSearchResponse(
            query=query,
            response=base_response.response,
            sources=base_response.sources,
            confidence=base_response.confidence,
            search_type="QuickSearch",
            processing_time=processing_time,
            answer_type=answer_type,
            keywords=keywords,
            metadata=base_response.metadata,
        )

        logger.info(f"Quick search completed in {processing_time:.2f}s")

        return response

    async def batch_search(self, queries: list[str]) -> list[QuickSearchResponse]:
        """Process multiple quick search queries efficiently.

        Args:
            queries: List of search queries

        Returns:
            List of quick search responses
        """
        import asyncio

        logger.info(f"Processing batch of {len(queries)} quick searches")

        # Process queries concurrently for speed
        tasks = [self.process_search(query) for query in queries]
        responses = await asyncio.gather(*tasks)

        logger.info("Batch processing completed")

        return responses
