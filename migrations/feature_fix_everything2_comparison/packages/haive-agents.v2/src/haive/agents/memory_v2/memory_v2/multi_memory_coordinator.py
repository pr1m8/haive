"""Multi-Memory Agent Coordinator - Orchestrates all memory systems.

This is the top-level coordinator that manages all memory agents:
- SimpleMemoryAgent (pre-hook system)
- ReactMemoryAgent (tool-based memory)
- LongTermMemoryAgent (persistent memory)
- GraphMemoryAgent (structured knowledge)
- AdvancedRAGMemoryAgent (multi-stage retrieval)

The coordinator intelligently routes operations to the most appropriate
memory system and can combine results from multiple systems.
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.memory_v2.advanced_rag_memory_agent import (
    AdvancedRAGConfig,
    AdvancedRAGMemoryAgent,
)
from haive.agents.memory_v2.graph_memory_agent import (
    GraphMemoryAgent,
    GraphMemoryConfig,
)
from haive.agents.memory_v2.long_term_memory_agent import LongTermMemoryAgent
from haive.agents.memory_v2.react_memory_agent import ReactMemoryAgent
from haive.agents.memory_v2.simple_memory_agent import SimpleMemoryAgent
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class MemorySystemType(str, Enum):
    """Available memory system types."""

    SIMPLE = "simple"  # Pre-hook based memory
    REACT = "react"  # Tool-based memory management
    LONGTERM = "longterm"  # Cross-conversation persistence
    GRAPH = "graph"  # Structured knowledge graphs
    ADVANCED_RAG = "rag"  # Multi-stage retrieval
    ALL = "all"  # Use all systems


class CoordinationMode(str, Enum):
    """Memory coordination modes."""

    INTELLIGENT = "intelligent"  # AI-powered routing
    EXPLICIT = "explicit"  # User specifies system
    PARALLEL = "parallel"  # Query all systems
    HIERARCHICAL = "hierarchical"  # Try systems in order
    CONSENSUS = "consensus"  # Combine multiple systems


@dataclass
class MultiMemoryConfig:
    """Configuration for Multi-Memory Coordinator."""

    # User identification
    user_id: str = "default_user"

    # LLM configuration
    engine: AugLLMConfig | None = None

    # System enablement
    enable_simple: bool = True
    enable_react: bool = True
    enable_longterm: bool = True
    enable_graph: bool = False  # Requires Neo4j
    enable_advanced_rag: bool = True

    # Coordination settings
    default_mode: CoordinationMode = CoordinationMode.INTELLIGENT
    parallel_timeout: float = 30.0  # Seconds
    consensus_threshold: int = 2  # Minimum systems for consensus

    # Memory system configurations
    simple_config: dict[str, Any] | None = None
    react_config: dict[str, Any] | None = None
    longterm_config: dict[str, Any] | None = None
    graph_config: GraphMemoryConfig | None = None
    rag_config: AdvancedRAGConfig | None = None

    # Storage paths
    base_storage_path: str | None = None

    def __post_init__(self):
        if self.engine is None:
            self.engine = AugLLMConfig(temperature=0.7)


class MultiMemoryCoordinator:
    """Coordinates multiple memory systems for comprehensive memory management.

    This coordinator provides:
    - Intelligent routing to appropriate memory systems
    - Parallel querying across multiple systems
    - Result combination and synthesis
    - Memory system analytics and optimization
    - Cross-system memory migration
    """

    def __init__(self, config: MultiMemoryConfig):
        self.config = config
        self.logger = logger

        # Initialize enabled memory systems
        self.memory_systems: dict[MemorySystemType, Any] = {}
        self._init_memory_systems()

        # Initialize coordination components
        self.router = self._create_router()
        self.synthesizer = self._create_synthesizer()

        # Track operations
        self.operation_history: list[dict[str, Any]] = []

    def _init_memory_systems(self):
        """Initialize all enabled memory systems."""
        if self.config.enable_simple:
            self._init_simple_memory()

        if self.config.enable_react:
            self._init_react_memory()

        if self.config.enable_longterm:
            self._init_longterm_memory()

        if self.config.enable_graph:
            self._init_graph_memory()

        if self.config.enable_advanced_rag:
            self._init_advanced_rag_memory()

        self.logger.info(
            f"Initialized {len(self.memory_systems)} memory systems: {list(self.memory_systems.keys())}"
        )

    def _init_simple_memory(self):
        """Initialize simple memory agent."""
        try:
            config = self.config.simple_config or {}
            agent = SimpleMemoryAgent(
                name="simple_memory",
                engine=self.config.engine,
                user_id=self.config.user_id,
                **config,
            )
            self.memory_systems[MemorySystemType.SIMPLE] = agent
            self.logger.info("Simple memory system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize simple memory: {e}")

    def _init_react_memory(self):
        """Initialize React memory agent."""
        try:
            config = self.config.react_config or {}
            storage_path = None
            if self.config.base_storage_path:
                storage_path = f"{self.config.base_storage_path}/react_memory"

            agent = ReactMemoryAgent(
                name="react_memory",
                engine=self.config.engine,
                user_id=self.config.user_id,
                memory_store_path=storage_path,
                **config,
            )
            self.memory_systems[MemorySystemType.REACT] = agent
            self.logger.info("React memory system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize react memory: {e}")

    def _init_longterm_memory(self):
        """Initialize long-term memory agent."""
        try:
            config = self.config.longterm_config or {}
            agent = LongTermMemoryAgent(
                user_id=self.config.user_id, llm_config=self.config.engine, **config
            )
            self.memory_systems[MemorySystemType.LONGTERM] = agent
            self.logger.info("Long-term memory system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize long-term memory: {e}")

    def _init_graph_memory(self):
        """Initialize graph memory agent."""
        try:
            if self.config.graph_config:
                graph_config = self.config.graph_config
            else:
                graph_config = GraphMemoryConfig(
                    user_id=self.config.user_id, llm_config=self.config.engine
                )

            agent = GraphMemoryAgent(graph_config)
            self.memory_systems[MemorySystemType.GRAPH] = agent
            self.logger.info("Graph memory system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize graph memory: {e}")

    def _init_advanced_rag_memory(self):
        """Initialize advanced RAG memory agent."""
        try:
            if self.config.rag_config:
                rag_config = self.config.rag_config
            else:
                storage_path = None
                if self.config.base_storage_path:
                    storage_path = f"{self.config.base_storage_path}/rag_memory"

                rag_config = AdvancedRAGConfig(
                    user_id=self.config.user_id,
                    memory_store_path=storage_path,
                    llm_config=self.config.engine,
                )

            agent = AdvancedRAGMemoryAgent(rag_config)
            self.memory_systems[MemorySystemType.ADVANCED_RAG] = agent
            self.logger.info("Advanced RAG memory system initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize advanced RAG memory: {e}")

    def _create_router(self) -> ReactAgent:
        """Create intelligent memory system router."""

        @tool
        def analyze_memory_operation(
            content: str, operation_type: str = "query"
        ) -> str:
            """Analyze content to determine best memory systems.

            Args:
                content: Content to analyze
                operation_type: "store", "query", or "update"

            Returns: Comma-separated list of recommended systems
            """
            content_lower = content.lower()
            systems = []

            # Structured knowledge indicators → Graph
            if any(
                indicator in content_lower
                for indicator in [
                    "works at",
                    "knows",
                    "located in",
                    "relationship",
                    "connected to",
                    "part of",
                    "belongs to",
                    "entity",
                ]
            ):
                if MemorySystemType.GRAPH in self.memory_systems:
                    systems.append("graph")

            # Complex queries → Advanced RAG
            if operation_type == "query":
                complexity_indicators = [
                    "how",
                    "why",
                    "explain",
                    "relationship",
                    "compare",
                    "analyze",
                    "implications",
                    "impact",
                    "consequences",
                ]
                if any(ind in content_lower for ind in complexity_indicators):
                    if MemorySystemType.ADVANCED_RAG in self.memory_systems:
                        systems.append("rag")

            # Tool-based operations → React
            if any(
                indicator in content_lower
                for indicator in [
                    "search",
                    "find",
                    "list",
                    "update",
                    "delete",
                    "store",
                    "remember",
                    "forget",
                ]
            ):
                if MemorySystemType.REACT in self.memory_systems:
                    systems.append("react")

            # Important/persistent content → Long-term
            if any(
                indicator in content_lower
                for indicator in [
                    "important",
                    "critical",
                    "always",
                    "never forget",
                    "permanent",
                    "long-term",
                    "persistent",
                ]
            ):
                if MemorySystemType.LONGTERM in self.memory_systems:
                    systems.append("longterm")

            # Token management → Simple
            if any(
                indicator in content_lower
                for indicator in [
                    "summarize",
                    "compress",
                    "manage context",
                    "token",
                    "memory limit",
                ]
            ):
                if MemorySystemType.SIMPLE in self.memory_systems:
                    systems.append("simple")

            # Default recommendations
            if not systems:
                # Default for queries
                if operation_type == "query":
                    if MemorySystemType.ADVANCED_RAG in self.memory_systems:
                        systems.append("rag")
                    elif MemorySystemType.REACT in self.memory_systems:
                        systems.append("react")

                # Default for storage
                elif operation_type == "store":
                    if MemorySystemType.REACT in self.memory_systems:
                        systems.append("react")
                    if MemorySystemType.LONGTERM in self.memory_systems:
                        systems.append("longterm")

            return ",".join(systems) if systems else "all"

        @tool
        def determine_coordination_mode(query: str, available_systems: str) -> str:
            """Determine best coordination mode for the query.

            Returns: intelligent, parallel, hierarchical, or consensus
            """
            systems = available_systems.split(",")

            # Use parallel for comprehensive queries
            if any(
                word in query.lower()
                for word in ["everything", "all", "comprehensive", "complete"]
            ):
                return "parallel"

            # Use consensus for important decisions
            if (
                any(
                    word in query.lower()
                    for word in ["important", "critical", "decision", "verify"]
                )
                and len(systems) >= 2
            ):
                return "consensus"

            # Use hierarchical for specific system preferences
            if len(systems) > 1:
                return "hierarchical"

            return "intelligent"

        router = ReactAgent(
            name="memory_router",
            engine=self.config.engine,
            tools=[analyze_memory_operation, determine_coordination_mode],
            system_message=f"""You are an intelligent memory system router for user {self.config.user_id}.

Available memory systems:
{', '.join(str(s.value) for s in self.memory_systems.keys())}

Your job is to:
1. Analyze content to determine the best memory systems
2. Choose appropriate coordination modes
3. Ensure optimal memory management

System capabilities:
- simple: Pre-hook token management, summarization
- react: Tool-based flexible memory operations
- longterm: Cross-conversation persistent memory
- graph: Structured knowledge with entities/relationships
- rag: Advanced retrieval with multi-stage processing""",
        )

        return router

    def _create_synthesizer(self) -> ReactAgent:
        """Create result synthesis agent."""
        synthesizer = ReactAgent(
            name="memory_synthesizer",
            engine=self.config.engine,
            tools=[],
            system_message=f"""You are a memory result synthesizer for user {self.config.user_id}.

Your job is to:
1. Combine results from multiple memory systems
2. Resolve conflicts between different sources
3. Provide comprehensive, accurate responses
4. Maintain consistency across systems

When combining results:
- Prioritize more recent information
- Weight results by system reliability
- Highlight conflicting information
- Provide source attribution when helpful""",
        )

        return synthesizer

    async def store_memory(
        self,
        content: str,
        systems: list[MemorySystemType] | None = None,
        mode: CoordinationMode | None = None,
        metadata: dict[str, Any] | None = None,
        importance: str = "normal",
    ) -> dict[str, Any]:
        """Store memory across appropriate systems.

        Args:
            content: Memory content to store
            systems: Specific systems to use (None for intelligent routing)
            mode: Coordination mode
            metadata: Optional metadata
            importance: Importance level

        Returns:
            Storage results from all used systems
        """
        start_time = datetime.now()
        mode = mode or self.config.default_mode

        # Determine target systems
        if systems is None:
            if mode == CoordinationMode.INTELLIGENT:
                routing_result = await self.router.arun(
                    f"Analyze this content for storage: {content}"
                )

                # Extract recommended systems
                systems = []
                for system_type in MemorySystemType:
                    if (
                        system_type.value in routing_result.lower()
                        and system_type in self.memory_systems
                    ):
                        systems.append(system_type)

                if not systems:
                    systems = list(self.memory_systems.keys())[:2]  # Default to first 2
            else:
                systems = list(self.memory_systems.keys())

        # Filter to available systems
        systems = [s for s in systems if s in self.memory_systems]

        # Store in each system
        results = {
            "content": content,
            "systems_used": [],
            "results": {},
            "total_time": 0,
            "errors": [],
        }

        for system_type in systems:
            try:
                system = self.memory_systems[system_type]
                system_result = None

                if system_type == MemorySystemType.SIMPLE:
                    # Simple memory doesn't have direct storage, use run
                    system_result = await system.arun(f"Remember: {content}")

                elif system_type == MemorySystemType.REACT:
                    system_result = await system.arun(
                        f"Store this memory with {importance} importance: {content}",
                        auto_save=True,
                    )

                elif system_type == MemorySystemType.LONGTERM:
                    system_result = await system.run(content, extract_memories=True)

                elif system_type == MemorySystemType.GRAPH:
                    system_result = await system.run(content, auto_store=True)

                elif system_type == MemorySystemType.ADVANCED_RAG:
                    system_result = await system.add_memory(
                        content, metadata, importance
                    )

                if system_result:
                    results["systems_used"].append(system_type.value)
                    results["results"][system_type.value] = system_result

            except Exception as e:
                error_msg = f"Error storing in {system_type.value}: {e!s}"
                results["errors"].append(error_msg)
                self.logger.error(error_msg)

        # Calculate timing
        results["total_time"] = (datetime.now() - start_time).total_seconds()

        # Log operation
        self.operation_history.append(
            {
                "operation": "store",
                "content": content[:100] + "...",
                "systems_used": results["systems_used"],
                "timestamp": start_time.isoformat(),
                "success": len(results["systems_used"]) > 0,
            }
        )

        return results

    async def query_memory(
        self,
        query: str,
        systems: list[MemorySystemType] | None = None,
        mode: CoordinationMode | None = None,
        combine_results: bool = True,
    ) -> dict[str, Any]:
        """Query memory across systems.

        Args:
            query: Query string
            systems: Specific systems to query
            mode: Coordination mode
            combine_results: Whether to combine results

        Returns:
            Query results
        """
        start_time = datetime.now()
        mode = mode or self.config.default_mode

        # Determine systems to query
        if systems is None:
            if mode == CoordinationMode.INTELLIGENT:
                routing_result = await self.router.arun(
                    f"Route this query to appropriate memory systems: {query}"
                )

                systems = []
                for system_type in MemorySystemType:
                    if (
                        system_type.value in routing_result.lower()
                        and system_type in self.memory_systems
                    ):
                        systems.append(system_type)

                if not systems:
                    systems = list(self.memory_systems.keys())[:3]  # Default
            elif mode == CoordinationMode.PARALLEL:
                systems = list(self.memory_systems.keys())
            else:
                systems = list(self.memory_systems.keys())[:2]  # Default

        # Filter to available systems
        systems = [s for s in systems if s in self.memory_systems]

        # Query systems
        results = {
            "query": query,
            "systems_queried": [],
            "individual_results": {},
            "combined_result": None,
            "total_time": 0,
            "errors": [],
        }

        # Execute queries
        if mode == CoordinationMode.PARALLEL:
            # Query all systems in parallel
            tasks = []
            for system_type in systems:
                task = self._query_single_system(system_type, query)
                tasks.append(task)

            try:
                system_results = await asyncio.wait_for(
                    asyncio.gather(*tasks, return_exceptions=True),
                    timeout=self.config.parallel_timeout,
                )

                for i, system_result in enumerate(system_results):
                    system_type = systems[i]
                    if isinstance(system_result, Exception):
                        results["errors"].append(
                            f"{system_type.value}: {system_result!s}"
                        )
                    else:
                        results["systems_queried"].append(system_type.value)
                        results["individual_results"][system_type.value] = system_result

            except TimeoutError:
                results["errors"].append(
                    f"Parallel query timeout after {self.config.parallel_timeout}s"
                )

        else:
            # Query systems sequentially
            for system_type in systems:
                try:
                    system_result = await self._query_single_system(system_type, query)
                    results["systems_queried"].append(system_type.value)
                    results["individual_results"][system_type.value] = system_result

                    # In hierarchical mode, stop after first successful result
                    if mode == CoordinationMode.HIERARCHICAL and system_result:
                        break

                except Exception as e:
                    error_msg = f"Error querying {system_type.value}: {e!s}"
                    results["errors"].append(error_msg)
                    self.logger.error(error_msg)

        # Combine results if requested
        if combine_results and len(results["individual_results"]) > 1:
            try:
                results["combined_result"] = await self._combine_query_results(
                    query, results["individual_results"]
                )
            except Exception as e:
                results["errors"].append(f"Error combining results: {e!s}")
        elif len(results["individual_results"]) == 1:
            # Single result, use as combined
            results["combined_result"] = list(results["individual_results"].values())[0]

        # Calculate timing
        results["total_time"] = (datetime.now() - start_time).total_seconds()

        # Log operation
        self.operation_history.append(
            {
                "operation": "query",
                "query": query,
                "systems_queried": results["systems_queried"],
                "timestamp": start_time.isoformat(),
                "success": len(results["systems_queried"]) > 0,
            }
        )

        return results

    async def _query_single_system(
        self, system_type: MemorySystemType, query: str
    ) -> Any:
        """Query a single memory system."""
        system = self.memory_systems[system_type]

        if system_type == MemorySystemType.SIMPLE:
            return await system.arun(query)

        if system_type == MemorySystemType.REACT:
            return await system.arun(f"Search memories: {query}", auto_save=False)

        if system_type == MemorySystemType.LONGTERM:
            result = await system.run(query, extract_memories=False)
            return result.get("response", result)

        if system_type == MemorySystemType.GRAPH:
            result = await system.query_graph(query, query_type="natural")
            return result.get("answer", result)

        if system_type == MemorySystemType.ADVANCED_RAG:
            result = await system.query_memory(query)
            return result.get("answer", result)

        return str(system)  # Fallback

    async def _combine_query_results(
        self, query: str, individual_results: dict[str, Any]
    ) -> str:
        """Combine results from multiple memory systems."""
        synthesis_prompt = f"""Query: {query}

Results from different memory systems:
"""

        for system, result in individual_results.items():
            result_str = str(result)[:500]  # Limit length
            synthesis_prompt += f"\n{system.upper()} Memory:\n{result_str}\n"

        synthesis_prompt += """
Please synthesize these results into a comprehensive, accurate answer.
If there are conflicts, highlight them. If results complement each other, combine them logically.
"""

        combined_result = await self.synthesizer.arun(synthesis_prompt)
        return combined_result

    async def get_system_analytics(self) -> dict[str, Any]:
        """Get analytics across all memory systems."""
        analytics = {
            "coordinatof": {
                "user_id": self.config.user_id,
                "timestamp": datetime.now().isoformat(),
                "enabled_systems": list(self.memory_systems.keys()),
                "operation_history": len(self.operation_history),
                "recent_operations": self.operation_history[-10:],  # Last 10
            },
            "systems": {},
        }

        # Get analytics from each system
        for system_type, system in self.memory_systems.items():
            try:
                if hasattr(system, "get_memory_analytics"):
                    system_analytics = await system.get_memory_analytics()
                elif hasattr(system, "get_analytics"):
                    system_analytics = await system.get_analytics()
                else:
                    system_analytics = {"status": "active", "type": str(type(system))}

                analytics["systems"][system_type.value] = system_analytics

            except Exception as e:
                analytics["systems"][system_type.value] = {
                    "error": str(e),
                    "status": "error",
                }

        return analytics

    async def migrate_memories(
        self,
        from_system: MemorySystemType,
        to_system: MemorySystemType,
        filter_criteria: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Migrate memories between systems."""
        if (
            from_system not in self.memory_systems
            or to_system not in self.memory_systems
        ):
            raise ValueError("Source or target system not available")

        migration_result = {
            "from_system": from_system.value,
            "to_system": to_system.value,
            "migrated_count": 0,
            "errors": [],
            "timestamp": datetime.now().isoformat(),
        }

        # Implementation would depend on specific system APIs
        # This is a placeholder for the migration logic
        self.logger.info(f"Migration from {from_system} to {to_system} completed")

        return migration_result

    @classmethod
    def create_comprehensive_system(
        cls,
        user_id: str,
        enable_graph: bool = False,
        neo4j_config: dict[str, Any] | None = None,
        storage_path: str | None = None,
    ) -> "MultiMemoryCoordinator":
        """Create a comprehensive memory system with all components."""
        # Base configuration
        config = MultiMemoryConfig(
            user_id=user_id,
            enable_graph=enable_graph,
            base_storage_path=storage_path,
            default_mode=CoordinationMode.INTELLIGENT,
        )

        # Add graph config if enabled
        if enable_graph and neo4j_config:
            config.graph_config = GraphMemoryConfig(user_id=user_id, **neo4j_config)

        return cls(config)


# Example usage
async def demo_multi_memory_coordinator():
    """Demonstrate the multi-memory coordinator."""
    coordinator = MultiMemoryCoordinator.create_comprehensive_system(
        user_id="demo_user",
        enable_graph=False,  # Set to True if Neo4j available
        storage_path="./demo_memory_storage",
    )

    print("=== Multi-Memory Coordinator Demo ===\n")

    # Store diverse memories
    memories = [
        ("Alice Johnson is the CEO of TechStartup Inc.", "high"),
        ("I had a great conversation with Alice about the future of AI.", "normal"),
        ("Important: Alice's direct phone number is 555-0123.", "critical"),
        (
            "TechStartup Inc. was founded in 2019 and specializes in machine learning.",
            "high",
        ),
        ("Alice mentioned they're hiring 50 new engineers this quarter.", "normal"),
    ]

    print("Storing memories across multiple systems...\n")
    for content, importance in memories:
        result = await coordinator.store_memory(
            content, importance=importance, mode=CoordinationMode.INTELLIGENT
        )
        print(f"Stored in: {result['systems_used']}")
        print(f"Content: {content[:50]}...\n")

    # Query with different coordination modes
    queries = [
        ("Who is Alice Johnson?", CoordinationMode.INTELLIGENT),
        ("What do I know about TechStartup Inc.?", CoordinationMode.PARALLEL),
        ("What's Alice's contact information?", CoordinationMode.CONSENSUS),
    ]

    print("Querying memories with different coordination modes...\n")
    for query, mode in queries:
        result = await coordinator.query_memory(query, mode=mode)
        print(f"Query: {query}")
        print(f"Mode: {mode.value}")
        print(f"Systems used: {result['systems_queried']}")
        print(f"Answer: {result.get('combined_result', 'No combined result')[:200]}...")
        print(f"Time: {result['total_time']:.2f}s\n")

    # Get analytics
    print("System Analytics:")
    analytics = await coordinator.get_system_analytics()
    print(
        json.dumps(
            {
                "enabled_systems": analytics["coordinator"]["enabled_systems"],
                "total_operations": analytics["coordinator"]["operation_history"],
                "system_status": {
                    k: v.get("status", "active")
                    for k, v in analytics["systems"].items()
                },
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(demo_multi_memory_coordinator())
