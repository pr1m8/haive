"""Pro Search Agent implementation.

Provides deep, contextual search with user preferences and advanced reasoning.
Similar to Perplexity's Pro Search feature that goes deeper and considers user context.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import Tool

from haive.agents.memory.search.base import BaseSearchAgent, SearchResponse
from haive.agents.memory.search.pro_search.models import (
    ContextualInsight,
    ProSearchResponse,
    SearchRefinement,
)

logger = logging.getLogger(__name__)


class ProSearchAgent(BaseSearchAgent):
    """Agent for deep, contextual search with user preferences.

    Provides comprehensive search responses that consider user context,
    preferences, and search history. Performs query refinement and
    multi-step reasoning for more accurate results.

    Features:
    - Query refinement and expansion
    - User preference integration
    - Contextual insights from memory
    - Multi-step reasoning process
    - Follow-up question generation
    - Depth-based search levels

    Examples:
        Basic usage::

            agent = ProSearchAgent(
                name="pro_search",
                engine=AugLLMConfig(temperature=0.3)
            )

            response = await agent.process_search(
                "How can I improve my productivity?",
                context={"domain": "software_development"}
            )

        With custom depth level::

            response = await agent.process_pro_search(
                "What are the best practices for ML deployment?",
                depth_level=4,
                use_preferences=True
            )
    """

    def __init__(
        self,
        name: str = "pro_search_agent",
        engine: AugLLMConfig | None = None,
        search_tools: list[Tool] | None = None,
        **kwargs,
    ):
        """Initialize the Pro Search Agent.

        Args:
            name: Agent identifier
            engine: LLM configuration (defaults to optimized settings)
            search_tools: Optional search tools
            **kwargs: Additional arguments passed to parent
        """
        # Default engine optimized for pro search
        if engine is None:
            engine = AugLLMConfig(
                temperature=0.3,  # Balanced creativity and consistency
                max_tokens=800,  # Longer responses for depth
                system_message=self.get_system_prompt(),
            )

        super().__init__(name=name, engine=engine, search_tools=search_tools, **kwargs)

        logger.info(f"Initialized ProSearchAgent: {name}")

    def get_response_model(self) -> type[SearchResponse]:
        """Get the response model for pro search."""
        return ProSearchResponse

    def get_system_prompt(self) -> str:
        """Get the system prompt for pro search operations."""
        return """You are a Pro Search Assistant designed to provide deep, contextual, and personalized search responses.

Your role is to:
1. Understand user intent beyond surface-level queries
2. Consider user preferences, context, and search history
3. Provide comprehensive, well-reasoned responses
4. Refine queries for better results
5. Generate contextual insights and follow-up questions
6. Adapt depth and detail based on user needs

Core Capabilities:
- Query refinement and expansion
- Multi-step reasoning process
- User preference integration
- Contextual memory utilization
- Evidence-based responses
- Interactive follow-up generation

Response Guidelines:
- Provide detailed, well-structured answers (400-800 words)
- Include reasoning steps and thought process
- Consider user's expertise level and preferences
- Cite relevant sources and evidence
- Suggest related questions and next steps
- Maintain conversational and helpful tone

Example Interaction:
User: "How can I improve my productivity?"
Pro Search Process:
1. Analyze query intent (seeking actionable productivity advice)
2. Check user preferences (structured approach, tech-savvy)
3. Refine query (evidence-based productivity strategies for professionals)
4. Generate comprehensive response with personalized recommendations
5. Provide follow-up questions based on user context

Remember: Depth, context, and personalization are key to pro search excellence."""

    def get_search_instructions(self) -> str:
        """Get specific search instructions for pro search."""
        return """PRO SEARCH INSTRUCTIONS:

1. QUERY ANALYSIS & REFINEMENT:
   - Identify core intent and implicit needs
   - Check for ambiguity or multiple interpretations
   - Refine query based on user context and preferences
   - Document refinement reasoning

2. CONTEXT INTEGRATION:
   - Retrieve relevant user preferences from memory
   - Consider search history and patterns
   - Identify user's expertise level and domain
   - Apply contextual insights to search strategy

3. MULTI-STEP REASONING:
   - Break down complex queries into components
   - Follow logical reasoning chain
   - Consider multiple perspectives and approaches
   - Document each reasoning step

4. COMPREHENSIVE RESPONSE:
   - Provide detailed, well-structured answers
   - Include multiple viewpoints when relevant
   - Add practical examples and applications
   - Structure with clear headings and bullet points

5. FOLLOW-UP GENERATION:
   - Generate 2-4 relevant follow-up questions
   - Consider user's likely next steps
   - Provide questions that deepen understanding
   - Include both clarifying and exploratory questions

6. QUALITY ASSESSMENT:
   - Rate confidence based on source quality
   - Consider completeness of response
   - Identify any gaps or limitations
   - Suggest areas for further exploration

Process each query with thoroughness and attention to user context."""

    def refine_query(self, query: str, context: dict[str, Any]) -> SearchRefinement:
        """Refine the search query based on context and preferences.

        Args:
            query: Original search query
            context: Context including user preferences and history

        Returns:
            Search refinement with improved query
        """
        # Analyze query for refinement opportunities
        refined_query = query
        refinement_reason = "Original query used as-is"

        # Add domain context if available
        if "domain" in context:
            domain = context["domain"]
            refined_query = f"{query} in {domain}"
            refinement_reason = f"Added domain context: {domain}"

        # Add expertise level context
        if "experience_level" in context:
            level = context["experience_level"]
            if level == "beginner":
                refined_query = f"{refined_query} for beginners"
            elif level == "advanced":
                refined_query = f"{refined_query} advanced techniques"
            refinement_reason += f", adapted for {level} level"

        # Add preference-based refinements
        if "preferred_sources" in context:
            sources = context["preferred_sources"]
            if "academic" in sources:
                refined_query = f"{refined_query} research-based evidence"
                refinement_reason += ", emphasized academic sources"

        return SearchRefinement(
            original_query=query,
            refined_query=refined_query,
            refinement_reason=refinement_reason,
        )

    def extract_contextual_insights(
        self, query: str, context: dict[str, Any]
    ) -> list[ContextualInsight]:
        """Extract contextual insights from available context.

        Args:
            query: Search query
            context: Available context

        Returns:
            List of contextual insights
        """
        insights = []

        # Memory-based insights
        if "memory_context" in context:
            memory_items = context["memory_context"]
            if memory_items:
                insights.append(
                    ContextualInsight(
                        insight=f"Found {len(memory_items)} related items in search history",
                        relevance_score=0.8,
                        source_type="memory",
                    )
                )

        # Preference insights
        if "preferences" in context:
            prefs = context["preferences"]
            if prefs:
                insights.append(
                    ContextualInsight(
                        insight=f"Applied user preferences: {', '.join(prefs.keys())}",
                        relevance_score=0.9,
                        source_type="preferences",
                    )
                )

        # Domain insights
        if "domain" in context:
            domain = context["domain"]
            insights.append(
                ContextualInsight(
                    insight=f"Search contextualized for {domain} domain",
                    relevance_score=0.7,
                    source_type="context",
                )
            )

        return insights

    def generate_reasoning_steps(
        self, query: str, context: dict[str, Any]
    ) -> list[str]:
        """Generate reasoning steps for the search process.

        Args:
            query: Search query
            context: Available context

        Returns:
            List of reasoning steps
        """
        steps = []

        steps.append(f"Analyzed query: '{query}' for intent and scope")

        if context.get("memory_context"):
            steps.append("Retrieved relevant context from user's search history")

        if context.get("preferences"):
            steps.append("Applied user preferences to customize search approach")

        if context.get("domain"):
            steps.append(f"Contextualized search for {context['domain']} domain")

        steps.append("Structured comprehensive response with evidence and examples")

        return steps

    def generate_follow_up_questions(
        self, query: str, response: str, context: dict[str, Any]
    ) -> list[str]:
        """Generate relevant follow-up questions.

        Args:
            query: Original search query
            response: Search response
            context: Available context

        Returns:
            List of follow-up questions
        """
        follow_ups = []

        # Query type-based follow-ups
        if "how to" in query.lower():
            follow_ups.append("What challenges might you face when implementing this?")
            follow_ups.append("Would you like specific tools or resources to help?")

        if "best practices" in query.lower():
            follow_ups.append(
                "Are there particular constraints or requirements in your situation?"
            )
            follow_ups.append(
                "Would you like examples of how others have implemented these practices?"
            )

        if "comparison" in query.lower() or "vs" in query.lower():
            follow_ups.append(
                "Which specific criteria are most important for your decision?"
            )
            follow_ups.append("Would you like detailed pros and cons for each option?")

        # Context-based follow-ups
        if context.get("domain"):
            domain = context["domain"]
            follow_ups.append(
                f"Are there {domain}-specific considerations I should address?"
            )

        # Generic useful follow-ups
        follow_ups.append("What would you like to explore next about this topic?")
        follow_ups.append("Are there any aspects that need more clarification?")

        return follow_ups[:4]  # Limit to 4 follow-ups

    async def process_pro_search(
        self,
        query: str,
        context: dict[str, Any] | None = None,
        depth_level: int = 3,
        use_preferences: bool = True,
        generate_follow_ups: bool = True,
        include_reasoning: bool = True,
        save_to_memory: bool = True,
    ) -> ProSearchResponse:
        """Process a pro search query with advanced features.

        Args:
            query: Search query
            context: Optional context
            depth_level: Search depth (1-5)
            use_preferences: Whether to use user preferences
            generate_follow_ups: Whether to generate follow-up questions
            include_reasoning: Whether to include reasoning steps
            save_to_memory: Whether to save to memory

        Returns:
            Pro search response
        """
        import time

        start_time = time.time()

        logger.info(f"Processing pro search: {query} (depth={depth_level})")

        if context is None:
            context = {}

        # Note: Memory context would be loaded here when memory system is available
        # For now, we'll use basic context

        # Apply user preferences if requested
        if use_preferences:
            # This would typically load from a user preference store
            context["preferences"] = {
                "learning_style": "structured",
                "preferred_sources": ["academic", "research-based"],
                "format_preference": "detailed_explanations",
            }

        # Refine query based on context
        refinement = self.refine_query(query, context)

        # Extract contextual insights
        insights = self.extract_contextual_insights(query, context)

        # Generate reasoning steps
        reasoning_steps = []
        if include_reasoning:
            reasoning_steps = self.generate_reasoning_steps(query, context)

        # Get base response with refined query
        base_response = await super().process_search(
            refinement.refined_query, context, save_to_memory
        )

        # Generate follow-up questions
        follow_ups = []
        if generate_follow_ups:
            follow_ups = self.generate_follow_up_questions(
                query, base_response.response, context
            )

        # Calculate processing time
        processing_time = time.time() - start_time

        # Create pro search response
        response = ProSearchResponse(
            query=query,
            response=base_response.response,
            sources=base_response.sources,
            confidence=base_response.confidence,
            search_type="ProSearch",
            processing_time=processing_time,
            refinements=[refinement],
            contextual_insights=insights,
            user_preferences_applied=context.get("preferences", {}),
            reasoning_steps=reasoning_steps,
            follow_up_questions=follow_ups,
            depth_level=depth_level,
            metadata=base_response.metadata,
        )

        logger.info(f"Pro search completed in {processing_time:.2f}s")

        return response

    async def process_search(
        self,
        query: str,
        context: dict[str, Any] | None = None,
        save_to_memory: bool = True,
    ) -> ProSearchResponse:
        """Process a search query with default pro search settings.

        Args:
            query: Search query
            context: Optional context
            save_to_memory: Whether to save to memory

        Returns:
            Pro search response
        """
        return await self.process_pro_search(
            query=query,
            context=context,
            depth_level=3,
            use_preferences=True,
            generate_follow_ups=True,
            include_reasoning=True,
            save_to_memory=save_to_memory,
        )
