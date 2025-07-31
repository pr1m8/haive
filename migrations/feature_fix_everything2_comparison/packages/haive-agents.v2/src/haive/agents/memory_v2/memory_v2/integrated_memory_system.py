"""Integrated Memory System combining Graph, Vector, and Time-based memory.

This system shows how to use multiple memory strategies together:
1. GraphMemoryAgent for structured knowledge and relationships
2. ReactMemoryAgent for flexible tool-based memory management
3. LongTermMemoryAgent for persistent cross-conversation memory
"""

import asyncio
import json
from datetime import datetime
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.memory_v2.graph_memory_agent import (
    GraphMemoryAgent,
    GraphMemoryConfig,
    GraphMemoryMode,
)
from haive.agents.memory_v2.long_term_memory_agent import LongTermMemoryAgent
from haive.agents.memory_v2.react_memory_agent import ReactMemoryAgent
from haive.agents.multi.simple.agent import SimpleMultiAgent
from haive.agents.react.agent import ReactAgent


class MemorySystemMode(str, Enum):
    """Modes for the integrated memory system."""

    STRUCTURED = "structured"  # Use graph memory for structured data
    CONVERSATIONAL = "conversational"  # Use React memory for conversations
    PERSISTENT = "persistent"  # Use long-term memory
    INTELLIGENT = "intelligent"  # System chooses best approach
    HYBRID = "hybrid"  # Use multiple systems together


class IntegratedMemorySystem:
    """Combines multiple memory systems for comprehensive memory management.

    This system intelligently routes memory operations to the most appropriate
    subsystem based on content type and requirements.
    """

    def __init__(
        self,
        user_id: str = "default_user",
        neo4j_config: dict[str, Any] | None = None,
        vector_store_path: str | None = None,
        engine: AugLLMConfig | None = None,
    ):
        self.user_id = user_id
        self.engine = engine or AugLLMConfig(temperature=0.7)

        # Initialize subsystems
        self._init_graph_memory(neo4j_config)
        self._init_react_memory(vector_store_path)
        self._init_longterm_memory()

        # Create memory router
        self.router = self._create_memory_router()

        # Create coordinator agent
        self.coordinator = self._create_coordinator()

    def _init_graph_memory(self, neo4j_config: dict[str, Any] | None):
        """Initialize graph memory for structured knowledge."""
        config = GraphMemoryConfig(
            user_id=self.user_id,
            mode=GraphMemoryMode.FULL,
            llm_config=self.engine,
            **(
                neo4j_config
                or {
                    "neo4j_uri": "bolt://localhost:7687",
                    "neo4j_username": "neo4j",
                    "neo4j_password": "password",
                }
            ),
        )
        self.graph_memory = GraphMemoryAgent(config)

    def _init_react_memory(self, vector_store_path: str | None):
        """Initialize React memory for flexible tool-based management."""
        self.react_memory = ReactMemoryAgent(
            name="react_memory",
            engine=self.engine,
            user_id=self.user_id,
            memory_store_path=vector_store_path,
            k=5,
            use_time_weighting=True,
        )

    def _init_longterm_memory(self):
        """Initialize long-term memory for persistence."""
        self.longterm_memory = LongTermMemoryAgent(
            user_id=self.user_id, llm_config=self.engine, k_memories=10
        )

    def _create_memory_router(self) -> ReactAgent:
        """Create router agent that determines which memory system to use."""

        @tool
        def analyze_memory_type(content: str) -> str:
            """Analyze content to determine the best memory system.

            Returns: structured, conversational, persistent, or hybrid
            """
            content_lower = content.lower()

            # Check for structured data indicators
            structured_indicators = [
                "works at",
                "located in",
                "knows",
                "created by",
                "belongs to",
                "part of",
                "connected to",
                "related to",
            ]
            has_structured = any(ind in content_lower for ind in structured_indicators)

            # Check for conversational indicators
            conversational_indicators = [
                "remember",
                "said",
                "mentioned",
                "discussed",
                "conversation",
                "told me",
                "i think",
                "my opinion",
            ]
            has_conversational = any(
                ind in content_lower for ind in conversational_indicators
            )

            # Check for long-term importance indicators
            persistent_indicators = [
                "important",
                "always",
                "never forget",
                "critical",
                "fundamental",
                "core",
                "essential",
                "permanent",
            ]
            has_persistent = any(ind in content_lower for ind in persistent_indicators)

            # Determine best system
            if has_structured and not has_conversational:
                return "structured"
            if has_conversational and not has_structured:
                return "conversational"
            if has_persistent:
                return "persistent"
            if has_structured and has_conversational:
                return "hybrid"
            return "conversational"  # Default

        @tool
        def route_memory_query(query: str) -> str:
            """Determine which memory systems to query.

            Returns: Comma-separated list of systems to use
            """
            query_lower = query.lower()

            systems = []

            # Graph queries
            if any(
                word in query_lower
                for word in [
                    "who",
                    "what",
                    "where",
                    "connected",
                    "related",
                    "knows",
                    "works",
                    "located",
                ]
            ):
                systems.append("graph")

            # Time-based queries
            if any(
                word in query_lower
                for word in [
                    "recent",
                    "today",
                    "yesterday",
                    "last week",
                    "when",
                    "timeline",
                    "history",
                ]
            ):
                systems.append("react")

            # Persistent memory queries
            if any(
                word in query_lower
                for word in [
                    "always",
                    "important",
                    "remember",
                    "learned",
                    "fact",
                    "knowledge",
                ]
            ):
                systems.append("longterm")

            return ",".join(systems) if systems else "all"

        router = ReactAgent(
            name="memory_router",
            engine=self.engine,
            tools=[analyze_memory_type, route_memory_query],
            system_message="""You are a memory routing specialist. Analyze content and queries to determine
the best memory system(s) to use:
- structured: For entities, relationships, and structured knowledge (Neo4j graph)
- conversational: For dialogue, opinions, and temporal information (React memory)
- persistent: For important facts and long-term knowledge (Long-term memory)
- hybrid: When multiple systems should be used together""",
        )

        return router

    def _create_coordinator(self) -> SimpleMultiAgent:
        """Create coordinator that manages all memory systems."""
        agents = {
            "router": self.router,
            "graph": self.graph_memory.as_tool(self.graph_memory.config),
            "react": self.react_memory.agent,
            "longterm": self.longterm_memory.memory_enhanced_agent,
        }

        coordinator = SimpleMultiAgent(
            name="memory_coordinator",
            engine=self.engine,
            agents=agents,
            mode="sequential",
        )

        return coordinator

    async def store_memory(
        self,
        content: str,
        mode: MemorySystemMode = MemorySystemMode.INTELLIGENT,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Store memory using the appropriate system(s).

        Args:
            content: Memory content to store
            mode: Storage mode
            metadata: Optional metadata

        Returns:
            Storage results from all used systems
        """
        results = {
            "content": content,
            "mode": mode.value,
            "timestamp": datetime.now().isoformat(),
            "systems_used": [],
        }

        if mode == MemorySystemMode.INTELLIGENT:
            # Let router decide
            routing = await self.router.arun(
                f"Analyze this content for memory storage: {content}"
            )

            if "structured" in routing.lower():
                mode = MemorySystemMode.STRUCTURED
            elif "conversational" in routing.lower():
                mode = MemorySystemMode.CONVERSATIONAL
            elif "persistent" in routing.lower():
                mode = MemorySystemMode.PERSISTENT
            elif "hybrid" in routing.lower():
                mode = MemorySystemMode.HYBRID

        # Store based on mode
        if mode in [MemorySystemMode.STRUCTURED, MemorySystemMode.HYBRID]:
            graph_result = await self.graph_memory.run(
                content, mode=GraphMemoryMode.EXTRACT_AND_STORE
            )
            results["graph_storage"] = graph_result
            results["systems_used"].append("graph")

        if mode in [MemorySystemMode.CONVERSATIONAL, MemorySystemMode.HYBRID]:
            react_result = await self.react_memory.arun(
                f"Store this memory: {content}", auto_save=True
            )
            results["react_storage"] = react_result
            results["systems_used"].append("react")

        if mode in [MemorySystemMode.PERSISTENT, MemorySystemMode.HYBRID]:
            longterm_result = await self.longterm_memory.run(
                content, extract_memories=True
            )
            results["longterm_storage"] = longterm_result
            results["systems_used"].append("longterm")

        return results

    async def query_memory(
        self,
        query: str,
        mode: MemorySystemMode = MemorySystemMode.INTELLIGENT,
        combine_results: bool = True,
    ) -> dict[str, Any]:
        """Query memory using appropriate system(s).

        Args:
            query: Query string
            mode: Query mode
            combine_results: Whether to combine results from multiple systems

        Returns:
            Query results
        """
        results = {
            "query": query,
            "mode": mode.value,
            "timestamp": datetime.now().isoformat(),
            "systems_queried": [],
        }

        if mode == MemorySystemMode.INTELLIGENT:
            # Let router decide which systems to query
            routing = await self.router.arun(f"Route this memory query: {query}")
            systems_to_query = routing.lower().split(",")
        else:
            # Map mode to systems
            mode_to_systems = {
                MemorySystemMode.STRUCTURED: ["graph"],
                MemorySystemMode.CONVERSATIONAL: ["react"],
                MemorySystemMode.PERSISTENT: ["longterm"],
                MemorySystemMode.HYBRID: ["graph", "react", "longterm"],
            }
            systems_to_query = mode_to_systems.get(mode, ["all"])

        # Query each system
        all_results = {}

        if "graph" in systems_to_query or "all" in systems_to_query:
            graph_result = await self.graph_memory.query_graph(
                query, query_type="natural"
            )
            all_results["graph"] = graph_result
            results["systems_queried"].append("graph")

        if "react" in systems_to_query or "all" in systems_to_query:
            react_result = await self.react_memory.arun(
                f"Search memories for: {query}", auto_save=False
            )
            all_results["react"] = react_result
            results["systems_queried"].append("react")

        if "longterm" in systems_to_query or "all" in systems_to_query:
            longterm_result = await self.longterm_memory.run(
                query, extract_memories=False
            )
            all_results["longterm"] = longterm_result
            results["systems_queried"].append("longterm")

        if combine_results and len(all_results) > 1:
            # Combine results intelligently
            combined = await self._combine_query_results(query, all_results)
            results["combined_answer"] = combined

        results["individual_results"] = all_results

        return results

    async def _combine_query_results(self, query: str, results: dict[str, Any]) -> str:
        """Combine results from multiple memory systems."""
        # Use a simple agent to synthesize results
        synthesis_prompt = f"""
Query: {query}

Results from different memory systems:

Graph Memory (structured knowledge):
{json.dumps(results.get('graph', {}), indent=2)}

Conversational Memory (recent interactions):
{results.get('react', 'No results')}

Long-term Memory (important facts):
{json.dumps(results.get('longterm', {}), indent=2)}

Synthesize these results into a comprehensive answer.
"""

        synthesizer = SimpleAgent(name="result_synthesizer", engine=self.engine)

        combined = await synthesizer.arun(synthesis_prompt)
        return combined

    async def get_memory_analytics(self) -> dict[str, Any]:
        """Get analytics across all memory systems."""
        analytics = {
            "user_id": self.user_id,
            "timestamp": datetime.now().isoformat(),
            "systems": {},
        }

        # Graph memory stats
        try:
            graph_stats = self.graph_memory.graph.query(
                """
                MATCH (n {user_id: $user_id})
                WITH labels(n) as node_labels, count(n) as count
                RETURN node_labels[0] as type, count
                ORDER BY count DESC
            """,
                {"user_id": self.user_id},
            )

            analytics["systems"]["graph"] = {
                "node_distribution": graph_stats,
                "total_nodes": sum(stat["count"] for stat in graph_stats),
            }
        except:
            analytics["systems"]["graph"] = {"error": "Unable to get stats"}

        # React memory stats
        recent_memories = await self.react_memory.arun(
            "List my 10 most recent memories", auto_save=False
        )
        analytics["systems"]["react"] = {
            "recent_activity": recent_memories[:200] + "..."
        }

        # Long-term memory stats
        analytics["systems"]["longterm"] = {
            "retriever_active": hasattr(self.longterm_memory, "memory_retriever")
        }

        return analytics

    async def consolidate_all_memories(self) -> dict[str, Any]:
        """Consolidate memories across all systems."""
        consolidation_results = {
            "timestamp": datetime.now().isoformat(),
            "systems_consolidated": [],
        }

        # Graph memory consolidation
        graph_consolidation = await self.graph_memory.consolidate_memories()
        consolidation_results["graph"] = graph_consolidation
        consolidation_results["systems_consolidated"].append("graph")

        # Move old conversational memories to long-term
        old_memories = await self.react_memory.arun(
            "Search memories from more than 30 days ago", auto_save=False
        )

        if old_memories and "no memories" not in old_memories.lower():
            # Store in long-term memory
            await self.longterm_memory.run(
                f"Archive of old memories: {old_memories}", extract_memories=True
            )
            consolidation_results["archived_memories"] = True
            consolidation_results["systems_consolidated"].append("react_to_longterm")

        return consolidation_results


# Example usage
async def demo_integrated_memory():
    """Demonstrate the integrated memory system."""
    system = IntegratedMemorySystem(
        user_id="demo_user",
        neo4j_config={
            "neo4j_uri": "bolt://localhost:7687",
            "neo4j_username": "neo4j",
            "neo4j_password": "password",
        },
    )

    print("=== Integrated Memory System Demo ===\n")

    # Store different types of memories
    memories = [
        # Structured knowledge
        "John Smith is the CEO of TechCorp, which is headquartered in San Francisco.",
        # Conversational memory
        "During our conversation, John mentioned he's been with the company for 10 years.",
        # Important fact
        "Important: John's email is john.smith@techcorp.com - always use this for official communication.",
        # Mixed content
        "I met Sarah Johnson at the TechCorp office. She works as CTO and told me about their new AI project.",
        # Time-based memory
        "Yesterday, John and Sarah presented the Q4 roadmap to the board.",
    ]

    print("Storing memories...\n")
    for memory in memories:
        result = await system.store_memory(memory, mode=MemorySystemMode.INTELLIGENT)
        print(f"Stored in: {result['systems_used']}")
        print(f"Content: {memory[:50]}...\n")

    # Query memories in different ways
    queries = [
        "Who are the executives at TechCorp?",
        "What did John mention in our conversation?",
        "What happened yesterday?",
        "What do I know about the AI project?",
        "What is John's contact information?",
    ]

    print("\nQuerying memories...\n")
    for query in queries:
        result = await system.query_memory(query, mode=MemorySystemMode.INTELLIGENT)
        print(f"Query: {query}")
        print(f"Systems used: {result['systems_queried']}")
        if "combined_answer" in result:
            print(f"Answer: {result['combined_answer'][:200]}...")
        print()

    # Get analytics
    print("\nMemory System Analytics:")
    analytics = await system.get_memory_analytics()
    print(json.dumps(analytics, indent=2))

    # Consolidate memories
    print("\nConsolidating memories...")
    consolidation = await system.consolidate_all_memories()
    print(f"Consolidation complete: {consolidation['systems_consolidated']}")


# Advanced example with custom agent
async def create_research_assistant():
    """Create a research assistant with integrated memory."""
    # Initialize memory system
    memory_system = IntegratedMemorySystem(
        user_id="researcher",
        neo4j_config={
            "neo4j_uri": "bolt://localhost:7687",
            "neo4j_username": "neo4j",
            "neo4j_password": "password",
        },
    )

    # Create custom tools using the memory system
    @tool
    async def remember_paper(
        title: str, authors: str, key_findings: str, relevance: str
    ) -> str:
        """Remember details about a research paper."""
        memory_content = f"""
        Research Paper: {title}
        Authors: {authors}
        Key Findings: {key_findings}
        Relevance to our work: {relevance}
        """

        result = await memory_system.store_memory(
            memory_content, mode=MemorySystemMode.HYBRID  # Store in multiple systems
        )

        return (
            f"Stored paper information in {len(result['systems_used'])} memory systems"
        )

    @tool
    async def find_related_papers(topic: str) -> str:
        """Find papers related to a topic from memory."""
        result = await memory_system.query_memory(
            f"Find research papers related to {topic}", mode=MemorySystemMode.HYBRID
        )

        if "combined_answer" in result:
            return result["combined_answer"]
        return "No related papers found in memory"

    @tool
    async def get_research_graph(entity: str) -> str:
        """Get the knowledge graph around a research entity."""
        graph_result = await memory_system.graph_memory.get_memory_subgraph(
            entity, max_depth=2, relationship_types=["AUTHORED", "CITES", "RELATED_TO"]
        )

        return json.dumps(graph_result, indent=2)

    # Create research assistant agent
    research_assistant = ReactAgent(
        name="research_assistant",
        engine=AugLLMConfig(temperature=0.7),
        tools=[remember_paper, find_related_papers, get_research_graph],
        system_message="""You are a research assistant with advanced memory capabilities.
You can remember papers, find related research, and explore knowledge graphs.
Always store important information in memory for future reference.""",
    )

    return research_assistant, memory_system


if __name__ == "__main__":
    # Run demo
    asyncio.run(demo_integrated_memory())
