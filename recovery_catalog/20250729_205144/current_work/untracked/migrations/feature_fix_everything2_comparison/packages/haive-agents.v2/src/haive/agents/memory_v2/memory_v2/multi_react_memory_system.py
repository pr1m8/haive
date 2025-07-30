"""Multi-ReactAgent Memory System with specialized agents.

This advanced example shows how to coordinate multiple ReactAgents,
each with specialized memory responsibilities.
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.memory_v2.react_memory_agent import ReactMemoryAgent
from haive.agents.multi.simple.agent import SimpleMultiAgent
from haive.agents.react.agent import ReactAgent


class MemoryType(str, Enum):
    """Types of specialized memory."""

    EPISODIC = "episodic"  # Personal experiences and events
    SEMANTIC = "semantic"  # Facts and general knowledge
    PROCEDURAL = "procedural"  # Skills and how-to knowledge
    WORKING = "working"  # Current context and active tasks


class MultiReactMemorySystem:
    """Coordinate multiple specialized ReactAgents for comprehensive memory management.

    This system uses:
    - Episodic Memory Agent: Personal experiences, events, conversations
    - Semantic Memory Agent: Facts, concepts, general knowledge
    - Procedural Memory Agent: Skills, procedures, how-to knowledge
    - Working Memory Agent: Current context, active tasks, short-term goals
    - Memory Router Agent: Determines which memory system to use
    """

    def __init__(
        self,
        user_id: str = "default_user",
        engine: AugLLMConfig | None = None,
        memory_base_path: str | None = None,
    ):
        self.user_id = user_id
        self.engine = engine or AugLLMConfig(temperature=0.7)
        self.memory_base_path = memory_base_path or f"./memories/{user_id}"

        # Initialize specialized memory agents
        self.memory_agents = self._initialize_memory_agents()

        # Create memory router agent
        self.router_agent = self._create_router_agent()

        # Create coordinator multi-agent
        self.coordinator = self._create_coordinator()

    def _initialize_memory_agents(self) -> dict[MemoryType, ReactMemoryAgent]:
        """Initialize specialized memory agents."""
        agents = {}

        # Episodic Memory Agent - with time weighting for recency
        agents[MemoryType.EPISODIC] = ReactMemoryAgent(
            name="episodic_memory_agent",
            engine=self.engine,
            user_id=self.user_id,
            memory_store_path=(
                f"{self.memory_base_path}/episodic" if self.memory_base_path else None
            ),
            k=5,
            use_time_weighting=True,
            decay_rate=0.01,  # Slower decay for personal experiences
        )

        # Semantic Memory Agent - no time weighting, facts don't decay
        agents[MemoryType.SEMANTIC] = ReactMemoryAgent(
            name="semantic_memory_agent",
            engine=self.engine,
            user_id=self.user_id,
            memory_store_path=(
                f"{self.memory_base_path}/semantic" if self.memory_base_path else None
            ),
            k=5,
            use_time_weighting=False,  # Facts don't decay over time
        )

        # Procedural Memory Agent - slight time weighting for skill updates
        agents[MemoryType.PROCEDURAL] = ReactMemoryAgent(
            name="procedural_memory_agent",
            engine=self.engine,
            user_id=self.user_id,
            memory_store_path=(
                f"{self.memory_base_path}/procedural" if self.memory_base_path else None
            ),
            k=3,
            use_time_weighting=True,
            decay_rate=0.005,  # Very slow decay for skills
        )

        # Working Memory Agent - high time weighting for current context
        agents[MemoryType.WORKING] = ReactMemoryAgent(
            name="working_memory_agent",
            engine=self.engine,
            user_id=self.user_id,
            memory_store_path=(
                f"{self.memory_base_path}/working" if self.memory_base_path else None
            ),
            k=10,  # More items in working memory
            use_time_weighting=True,
            decay_rate=0.1,  # Fast decay for working memory
        )

        return agents

    def _create_router_agent(self) -> ReactAgent:
        """Create router agent that determines which memory system to use."""

        @tool
        def route_memory_query(query: str) -> str:
            """Determine which memory system(s) should handle a query.

            Returns: Comma-separated list of memory types (episodic,semantic,procedural,working)
            """
            query_lower = query.lower()

            routes = []

            # Episodic memory indicators
            if any(
                word in query_lower
                for word in [
                    "remember when",
                    "last time",
                    "experience",
                    "conversation",
                    "told me",
                    "we discussed",
                    "personal",
                    "my day",
                    "happened",
                ]
            ):
                routes.append(MemoryType.EPISODIC.value)

            # Semantic memory indicators
            if any(
                word in query_lower
                for word in [
                    "fact",
                    "definition",
                    "what is",
                    "explain",
                    "concept",
                    "general knowledge",
                    "information about",
                    "meaning of",
                ]
            ):
                routes.append(MemoryType.SEMANTIC.value)

            # Procedural memory indicators
            if any(
                word in query_lower
                for word in [
                    "how to",
                    "steps",
                    "procedure",
                    "skill",
                    "technique",
                    "method",
                    "way to",
                    "process",
                    "tutorial",
                ]
            ):
                routes.append(MemoryType.PROCEDURAL.value)

            # Working memory indicators
            if any(
                word in query_lower
                for word in [
                    "current",
                    "now",
                    "today",
                    "active",
                    "working on",
                    "task",
                    "goal",
                    "context",
                    "just",
                    "recent",
                ]
            ):
                routes.append(MemoryType.WORKING.value)

            # Default to episodic if no clear indicators
            if not routes:
                routes.append(MemoryType.EPISODIC.value)

            return ",".join(routes)

        @tool
        def classify_memory_for_storage(content: str) -> str:
            """Classify memory content to determine storage location.

            Returns: Memory type (episodic, semantic, procedural, or working)
            """
            content_lower = content.lower()

            # Check for procedural content
            if any(
                word in content_lower
                for word in [
                    "how to",
                    "steps:",
                    "procedure",
                    "1.",
                    "first,",
                    "then",
                    "finally",
                    "method",
                    "technique",
                ]
            ):
                return MemoryType.PROCEDURAL.value

            # Check for semantic content
            if any(
                word in content_lower
                for word in [
                    "is defined as",
                    "means",
                    "fact:",
                    "always",
                    "never",
                    "all",
                    "every",
                    "general rule",
                    "principle",
                ]
            ):
                return MemoryType.SEMANTIC.value

            # Check for working memory content
            if any(
                word in content_lower
                for word in [
                    "currently",
                    "right now",
                    "today",
                    "this moment",
                    "active task",
                    "working on",
                    "in progress",
                ]
            ):
                return MemoryType.WORKING.value

            # Default to episodic
            return MemoryType.EPISODIC.value

        router_agent = ReactAgent(
            name="memory_router",
            engine=self.engine,
            tools=[route_memory_query, classify_memory_for_storage],
            system_message="""You are a memory routing specialist. Your job is to:
1. Determine which memory systems should handle queries
2. Classify new memories for appropriate storage
3. Ensure efficient memory organization

Memory types:
- episodic: Personal experiences, events, conversations
- semantic: Facts, definitions, general knowledge
- procedural: Skills, procedures, how-to knowledge
- working: Current context, active tasks, temporary information""",
        )

        return router_agent

    def _create_coordinator(self) -> SimpleMultiAgent:
        """Create coordinator multi-agent."""
        # Convert memory agents to dict for SimpleMultiAgent
        agents_dict = {
            memory_type.value: agent.agent  # Use the underlying ReactAgent
            for memory_type, agent in self.memory_agents.items()
        }

        # Add router agent
        agents_dict["router"] = self.router_agent

        coordinator = SimpleMultiAgent(
            name="memory_coordinator",
            engine=self.engine,
            agents=agents_dict,
            mode="sequential",  # Process in sequence
        )

        return coordinator

    async def process_query(self, query: str) -> dict[str, Any]:
        """Process a query using the appropriate memory systems.

        Args:
            query: User query

        Returns:
            Dictionary with response and metadata
        """
        # First, determine which memory systems to use
        routing_result = await self.router_agent.arun(
            f"Route this query to appropriate memory systems: {query}"
        )

        # Extract memory types from routing result
        memory_types = []
        for memory_type in MemoryType:
            if memory_type.value in routing_result.lower():
                memory_types.append(memory_type)

        # Query each relevant memory system
        results = {}
        for memory_type in memory_types:
            agent = self.memory_agents[memory_type]
            result = await agent.arun(query, auto_save=False)
            results[memory_type.value] = result

        # Combine results
        combined_response = self._combine_memory_results(results, query)

        return {
            "response": combined_response,
            "memory_systems_used": [mt.value for mt in memory_types],
            "timestamp": datetime.now().isoformat(),
            "user_id": self.user_id,
        }

    async def store_memory(
        self, content: str, memory_type: MemoryType | None = None
    ) -> str:
        """Store a memory in the appropriate system.

        Args:
            content: Memory content to store
            memory_type: Optional specific memory type, otherwise auto-classified

        Returns:
            Confirmation message
        """
        # Determine memory type if not specified
        if not memory_type:
            classification = await self.router_agent.arun(
                f"Classify this memory for storage: {content}"
            )

            # Extract memory type
            for mt in MemoryType:
                if mt.value in classification.lower():
                    memory_type = mt
                    break

            if not memory_type:
                memory_type = MemoryType.EPISODIC  # Default

        # Store in appropriate system
        agent = self.memory_agents[memory_type]
        result = await agent.arun(f"Store this memory: {content}", auto_save=False)

        return f"Memory stored in {memory_type.value} system: {result}"

    async def consolidate_memories(self) -> str:
        """Consolidate memories across systems (move from working to long-term)."""
        # Get working memories
        working_memories = await self.memory_agents[MemoryType.WORKING].arun(
            "List all recent memories", auto_save=False
        )

        # Process each working memory for consolidation
        consolidation_prompt = f"""Review these working memories and determine which should be:
1. Moved to episodic memory (personal experiences)
2. Moved to semantic memory (facts learned)
3. Moved to procedural memory (skills acquired)
4. Kept in working memory (still active)
5. Discarded (no longer relevant)

Working memories:
{working_memories}

For each memory, indicate the action and destination."""

        consolidation_plan = await self.router_agent.arun(consolidation_prompt)

        # Execute consolidation (simplified for example)
        return f"Memory consolidation complete. Plan: {consolidation_plan}"

    def _combine_memory_results(self, results: dict[str, str], query: str) -> str:
        """Combine results from multiple memory systems."""
        if not results:
            return "No relevant memories found."

        if len(results) == 1:
            return list(results.values())[0]

        # Combine multiple results
        combined = f"Based on searching {len(results)} memory systems:\n\n"

        for memory_type, result in results.items():
            combined += f"From {memory_type} memory:\n{result}\n\n"

        return combined.strip()

    async def get_memory_stats(self) -> dict[str, Any]:
        """Get statistics about memory usage."""
        stats = {
            "user_id": self.user_id,
            "timestamp": datetime.now().isoformat(),
            "memory_systems": {},
        }

        for memory_type, agent in self.memory_agents.items():
            system_stats = await agent.arun(
                "List recent memories and provide a count", auto_save=False
            )
            stats["memory_systems"][memory_type.value] = {
                "recent_activity": system_stats[:200] + "..."  # Truncate
            }

        return stats


# Example usage
async def example_multi_memory_system():
    """Example of using the multi-memory system."""
    system = MultiReactMemorySystem(user_id="alice_doe")

    # Store different types of memories
    print("Storing memories...")

    # Episodic memory
    await system.store_memory(
        "Today I had lunch with Bob at the Italian restaurant downtown. We discussed the new project."
    )

    # Semantic memory
    await system.store_memory(
        "Python is a high-level programming language known for its simplicity and readability."
    )

    # Procedural memory
    await system.store_memory(
        "How to make coffee: 1. Grind beans, 2. Add to filter, 3. Pour hot water, 4. Wait 4 minutes"
    )

    # Working memory
    await system.store_memory(
        "Currently working on the quarterly report, deadline is Friday at 5 PM"
    )

    print("\nQuerying memories...")

    # Query that touches multiple systems
    result1 = await system.process_query(
        "What am I currently working on and when did I last meet with Bob?"
    )
    print(f"Multi-system query: {result1}")

    # Specific procedural query
    result2 = await system.process_query("How do I make coffee?")
    print(f"Procedural query: {result2}")

    # Get memory statistics
    stats = await system.get_memory_stats()
    print(f"\nMemory statistics: {json.dumps(stats, indent=2)}")

    # Consolidate memories
    consolidation = await system.consolidate_memories()
    print(f"\nConsolidation result: {consolidation}")


async def example_advanced_memory_operations():
    """Advanced memory operations example."""
    system = MultiReactMemorySystem(user_id="developer_jane")

    # Store a learning journey
    memories = [
        "Started learning Rust programming language today",
        "Rust has ownership system that prevents memory errors at compile time",
        "Practiced Rust: Created a simple CLI tool for file processing",
        "How to create Rust project: 1. cargo new project_name, 2. Edit Cargo.toml, 3. Write code in src/main.rs",
        "Currently debugging a borrow checker issue in my Rust code",
    ]

    for memory in memories:
        await system.store_memory(memory)
        print(f"Stored: {memory[:50]}...")

    # Complex query spanning multiple memory types
    result = await system.process_query(
        "What have I learned about Rust, what projects have I built, "
        "and what am I currently struggling with?"
    )

    print(f"\nComprehensive query result:\n{result}")


if __name__ == "__main__":
    import asyncio

    # Run examples
    asyncio.run(example_multi_memory_system())
    # asyncio.run(example_advanced_memory_operations())
