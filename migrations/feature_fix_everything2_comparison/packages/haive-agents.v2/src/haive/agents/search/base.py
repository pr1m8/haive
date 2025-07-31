"""Base classes for search agents.

This module provides the foundation for all search agents in the memory system, with
common functionality for memory integration, tool management, and structured outputs.
"""

from abc import ABC, abstractmethod
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import Tool
from pydantic import BaseModel, Field

from haive.agents.memory.core.types import MemoryType
from haive.agents.react.agent import ReactAgent


class SearchResponse(BaseModel):
    """Base response model for all search agents."""

    query: str = Field(..., description="The original search query")
    response: str = Field(..., description="The search response content")
    sources: list[str] = Field(
        default_factory=list, description="Source URLs or references"
    )
    confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Confidence score"
    )
    search_type: str = Field(..., description="Type of search performed")
    processing_time: float = Field(
        default=0.0, description="Time taken to process in seconds"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class BaseSearchAgent(ReactAgent, ABC):
    """Abstract base class for all search agents.

    Provides common functionality for memory integration, tool management, and
    structured output formatting for search operations.
    """

    def __init__(
        self,
        name: str,
        engine: AugLLMConfig,
        search_tools: list[Tool] | None = None,
        **kwargs,
    ):
        """Initialize the search agent.

        Args:
            name: Unique identifier for the agent
            engine: LLM configuration for the agent
            search_tools: Optional list of search tools to use
            **kwargs: Additional arguments passed to parent class
        """
        # Initialize with ReactAgent capabilities
        super().__init__(name=name, engine=engine, **kwargs)

        # Add search tools if provided
        if search_tools:
            if hasattr(self, "tools") and self.tools is not None:
                self.tools.extend(search_tools)
            else:
                self.tools = search_tools

    @abstractmethod
    def get_response_model(self) -> type[SearchResponse]:
        """Get the structured response model for this search agent."""

    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt template for this search agent."""

    @abstractmethod
    def get_search_instructions(self) -> str:
        """Get specific search instructions for this agent type."""

    def format_search_context(self, query: str, context: dict[str, Any]) -> str:
        """Format search context for the agent.

        Args:
            query: The user's search query
            context: Additional context including memory, preferences, etc.

        Returns:
            Formatted context string for the agent
        """
        context_parts = [f"Query: {query}"]

        # Add memory context if available
        if "memory_context" in context:
            memory_items = context["memory_context"]
            if memory_items:
                context_parts.append("Relevant Memory:")
                for item in memory_items[:3]:  # Limit to top 3
                    context_parts.append(f"- {item}")

        # Add user preferences if available
        if "preferences" in context:
            prefs = context["preferences"]
            if prefs:
                context_parts.append(f"User Preferences: {prefs}")

        # Add search history if available
        if "search_history" in context:
            history = context["search_history"]
            if history:
                context_parts.append("Recent Searches:")
                for search in history[-2:]:  # Last 2 searches
                    context_parts.append(f"- {search}")

        return "\n".join(context_parts)

    def extract_memory_items(self, query: str, response: str) -> list[dict[str, Any]]:
        """Extract memory items from search interaction.

        Args:
            query: The search query
            response: The search response

        Returns:
            List of memory items to store
        """
        memory_items = []

        # Store the search interaction as episodic memory
        memory_items.append(
            {
                "type": MemoryType.EPISODIC,
                "content": f"Search: {query} -> {response[:200]}...",
                "metadata": {
                    "query": query,
                    "response_length": len(response),
                    "search_type": self.__class__.__name__,
                },
            }
        )

        # Extract semantic facts from response (basic extraction)
        if "fact:" in response.lower() or "according to" in response.lower():
            memory_items.append(
                {
                    "type": MemoryType.SEMANTIC,
                    "content": response[:500],  # First 500 chars as semantic knowledge
                    "metadata": {"source": "search_response", "query": query},
                }
            )

        return memory_items

    async def process_search(
        self,
        query: str,
        context: dict[str, Any] | None = None,
        save_to_memory: bool = True,
    ) -> SearchResponse:
        """Process a search query with memory integration.

        Args:
            query: The search query
            context: Optional context including memory and preferences
            save_to_memory: Whether to save results to memory

        Returns:
            Structured search response
        """
        import time

        start_time = time.time()

        # Get relevant memory context
        if context is None:
            context = {}

        # Note: Memory functionality would be added here when memory system is available
        # For now, we'll use basic context

        # Format the search context
        formatted_context = self.format_search_context(query, context)

        # Build the prompt
        system_prompt = self.get_system_prompt()
        search_instructions = self.get_search_instructions()

        full_prompt = f"{system_prompt}\n\n{search_instructions}\n\n{formatted_context}"

        # Execute the search
        response = await self.arun(full_prompt)

        # Calculate processing time
        processing_time = time.time() - start_time

        # Create structured response
        response_model = self.get_response_model()
        structured_response = response_model(
            query=query,
            response=response,
            sources=[],  # Will be populated by subclasses
            confidence=0.8,  # Default confidence
            search_type=self.__class__.__name__,
            processing_time=processing_time,
            metadata=context,
        )

        # Save to memory if requested
        if save_to_memory:
            # Note: Memory saving would be implemented when memory system is available
            pass

        return structured_response
