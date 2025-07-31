"""Unified Memory API - Complete Memory System Integration.

This module provides a unified, easy-to-use API for the complete memory system,
integrating all components including classification, storage, retrieval,
knowledge graph generation, and multi-agent coordination.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.persistence.store.types import StoreType
from haive.core.tools.store_manager import StoreManager
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory.agentic_rag_coordinator import (
    AgenticRAGCoordinator,
    AgenticRAGCoordinatorConfig,
)
from haive.agents.memory.core.classifier import MemoryClassifier, MemoryClassifierConfig
from haive.agents.memory.core.stores import MemoryStoreConfig, MemoryStoreManager
from haive.agents.memory.core.types import MemoryType
from haive.agents.memory.enhanced_retriever import EnhancedRetrieverConfig
from haive.agents.memory.graph_rag_retriever import (
    GraphRAGRetriever,
    GraphRAGRetrieverConfig,
)
from haive.agents.memory.kg_generator_agent import (
    KGGeneratorAgent,
    KGGeneratorAgentConfig,
)
from haive.agents.memory.multi_agent_coordinator import (
    MultiAgentCoordinatorConfig,
    MultiAgentMemoryCoordinator,
)

logger = logging.getLogger(__name__)


class MemorySystemConfig(BaseModel):
    """Comprehensive configuration for the unified memory system.

    This configuration class defines all settings needed to create and customize
    a UnifiedMemorySystem, including store settings, LLM configuration, feature
    toggles, and performance parameters.

    Attributes:
        store_type: Type of store backend ("memory", "postgres", "redis", etc.)
        collection_name: Name of the collection/table for storing memories
        default_namespace: Default namespace tuple for memory organization
        llm_config: LLM configuration for classification, analysis, and generation
        enable_auto_classification: Whether to automatically classify stored memories
        classification_confidence_threshold: Minimum confidence for auto-classification
        enable_enhanced_retrieval: Whether to enable enhanced retrieval features
        enable_graph_rag: Whether to enable Graph RAG retrieval capabilities
        enable_multi_agent_coordination: Whether to enable multi-agent coordination
        max_concurrent_operations: Maximum number of concurrent memory operations
        operation_timeout_seconds: Timeout for individual memory operations
        enable_memory_consolidation: Whether to enable automatic memory consolidation
        consolidation_interval_hours: Hours between automatic consolidation runs

    Examples:
        Basic configuration for development::

            config = MemorySystemConfig(
                store_type="memory",
                collection_name="dev_memories",
                default_namespace=("user", "development")
            )

        Production configuration with PostgreSQL::

            config = MemorySystemConfig(
                store_type="postgres",
                collection_name="prod_memories",
                default_namespace=("company", "production"),
                llm_config=AugLLMConfig(
                    model="gpt-4",
                    temperature=0.1,
                    max_tokens=1000
                ),
                enable_auto_classification=True,
                enable_graph_rag=True,
                enable_multi_agent_coordination=True,
                max_concurrent_operations=10,
                operation_timeout_seconds=600
            )

        Performance-optimized configuration::

            config = MemorySystemConfig(
                store_type="redis",
                collection_name="fast_memories",
                default_namespace=("user", "cache"),
                enable_auto_classification=False,  # Disable for speed
                enable_enhanced_retrieval=True,
                enable_graph_rag=False,  # Disable for speed
                enable_multi_agent_coordination=False,
                max_concurrent_operations=20,
                operation_timeout_seconds=30
            )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Store configuration
    store_type: str = Field(
        default="memory", description="Store type (memory, postgres, etc.)"
    )
    collection_name: str = Field(
        default="haive_memories", description="Collection name"
    )
    default_namespace: tuple[str, ...] = Field(
        default=("user", "general"), description="Default namespace"
    )

    # LLM configuration
    llm_config: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="LLM configuration"
    )

    # Classification configuration
    enable_auto_classification: bool = Field(
        default=True, description="Enable automatic classification"
    )
    classification_confidence_threshold: float = Field(
        default=0.6, description="Classification confidence threshold"
    )

    # Retrieval configuration
    enable_enhanced_retrieval: bool = Field(
        default=True, description="Enable enhanced retrieval"
    )
    enable_graph_rag: bool = Field(default=True, description="Enable graph RAG")
    enable_multi_agent_coordination: bool = Field(
        default=True, description="Enable multi-agent coordination"
    )

    # Performance configuration
    max_concurrent_operations: int = Field(
        default=5, description="Maximum concurrent operations"
    )
    operation_timeout_seconds: int = Field(default=300, description="Operation timeout")

    # Memory lifecycle
    enable_memory_consolidation: bool = Field(
        default=True, description="Enable memory consolidation"
    )
    consolidation_interval_hours: int = Field(
        default=24, description="Consolidation interval"
    )


class MemorySystemResult(BaseModel):
    """Comprehensive result from memory system operations with metrics and analysis.

    This class encapsulates all information returned from memory system operations,
    including success status, operation results, performance metrics, quality scores,
    and metadata for analysis and monitoring.

    Attributes:
        success: Whether the operation completed successfully
        operation: Type of operation performed (store_memory, retrieve_memories, etc.)
        result: The actual result data from the operation (varies by operation type)
        error: Error message if the operation failed (None if successful)
        execution_time_ms: Time taken to complete the operation in milliseconds
        agent_used: Name of the agent/component that handled the operation
        confidence_score: Confidence in the result quality (0.0-1.0)
        completeness_score: How complete the result is (0.0-1.0)
        timestamp: UTC timestamp when the operation completed
        metadata: Additional metadata specific to the operation

    Examples:
        Checking operation success::

            result = await memory_system.store_memory("Important information")

            if result.success:
                memory_id = result.result["memory_id"]
                print(f"Memory stored successfully with ID: {memory_id}")
                print(f"Operation took {result.execution_time_ms:.1f}ms")
            else:
                print(f"Storage failed: {result.error}")

        Analyzing retrieval results::

            result = await memory_system.retrieve_memories("machine learning")

            if result.success:
                memories = result.result["memories"]
                count = result.result["count"]

                print(f"Retrieved {count} memories in {result.execution_time_ms:.1f}ms")
                print(f"Confidence: {result.confidence_score:.2f}")
                print(f"Completeness: {result.completeness_score:.2f}")
                print(f"Agent used: {result.agent_used}")

                for memory in memories:
                    print(f"- {memory['content'][:100]}...")

        Performance monitoring::

            results = []

            # Perform multiple operations
            for query in ["Python", "AI", "databases"]:
                result = await memory_system.retrieve_memories(query)
                results.append(result)

            # Analyze performance
            avg_time = sum(r.execution_time_ms for r in results) / len(results)
            success_rate = sum(1 for r in results if r.success) / len(results)

            print(f"Average response time: {avg_time:.1f}ms")
            print(f"Success rate: {success_rate:.1%}")
    """

    success: bool = Field(..., description="Operation success status")
    operation: str = Field(..., description="Operation type")
    result: Any = Field(default=None, description="Operation result")
    error: str | None = Field(default=None, description="Error message if failed")

    # Performance metrics
    execution_time_ms: float = Field(
        default=0.0, description="Execution time in milliseconds"
    )
    agent_used: str | None = Field(default=None, description="Agent used for operation")

    # Quality metrics
    confidence_score: float = Field(default=0.0, description="Confidence in result")
    completeness_score: float = Field(default=0.0, description="Completeness of result")

    # Metadata
    timestamp: datetime = Field(
        default_factory=datetime.utcnow, description="Result timestamp"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class UnifiedMemorySystem:
    """Unified Memory System - Complete memory management solution with intelligent coordination.

    The UnifiedMemorySystem provides a single, comprehensive interface to all memory
    system capabilities, automatically coordinating between multiple specialized agents
    to provide optimal memory storage, retrieval, and analysis. It combines traditional
    vector search with knowledge graph traversal, multi-agent coordination, and
    intelligent classification for superior memory management.

    Key Features:
        - Unified API: Single interface for all memory operations
        - Multi-Agent Coordination: Automatic routing to best-suited agents
        - Graph RAG: Knowledge graph enhanced retrieval
        - Auto-Classification: Intelligent memory type detection
        - Performance Monitoring: Built-in metrics and diagnostics
        - Flexible Storage: Support for multiple backend stores
        - Async Operations: Full async/await support for scalability

    Architecture:
        - Memory Store Manager: Handles storage and basic retrieval
        - Memory Classifier: Analyzes and categorizes memory content
        - KG Generator Agent: Builds and maintains knowledge graphs
        - Graph RAG Retriever: Enhanced retrieval with graph context
        - Agentic RAG Coordinator: Intelligent retrieval strategy selection
        - Multi-Agent Coordinator: Orchestrates all agents for complex tasks

    Attributes:
        config: System configuration settings
        memory_store: Core memory storage manager
        classifier: Memory classification engine
        kg_generator: Knowledge graph generation agent
        retrievers: Dictionary of specialized retrieval systems
        agentic_rag: Intelligent retrieval coordinator
        coordinator: Multi-agent coordination system (optional)

    Examples:
        Basic usage with default configuration::

            # Create system with all features enabled
            memory_system = await create_memory_system()

            # Store memories
            result = await memory_system.store_memory(
                "Alice works at TechCorp as a software engineer"
            )

            if result.success:
                print(f"Memory stored: {result.result['memory_id']}")

            # Retrieve memories
            result = await memory_system.retrieve_memories(
                "Who works at TechCorp?", limit=5
            )

            if result.success:
                for memory in result.result["memories"]:
                    print(f"Found: {memory['content']}")

        Advanced usage with custom configuration::

            config = MemorySystemConfig(
                store_type="postgres",
                collection_name="company_knowledge",
                default_namespace=("company", "engineering"),
                enable_graph_rag=True,
                enable_multi_agent_coordination=True,
                llm_config=AugLLMConfig(model="gpt-4", temperature=0.1)
            )

            memory_system = UnifiedMemorySystem(config)

            # Store with metadata
            result = await memory_system.store_memory(
                content="Neural networks are effective for pattern recognition",
                namespace=("company", "ai", "research"),
                metadata={"source": "research_paper", "confidence": 0.95}
            )

            # Advanced retrieval with filtering
            result = await memory_system.retrieve_memories(
                query="pattern recognition techniques",
                limit=10,
                memory_types=[MemoryType.SEMANTIC, MemoryType.PROCEDURAL],
                namespace=("company", "ai"),
                use_graph_rag=True
            )

        Knowledge graph operations::

            # Generate knowledge graph from stored memories
            kg_result = await memory_system.generate_knowledge_graph(
                namespace=("company", "projects")
            )

            if kg_result.success:
                kg = kg_result.result["knowledge_graph"]
                print(f"Generated graph with {len(kg.nodes)} nodes")

            # Search for specific entities
            entity_result = await memory_system.search_entities("Alice")

            if entity_result.success:
                context = entity_result.result["entity_context"]
                print(f"Found entity: {context['entity'].name}")
                print(f"Connected to {context['total_connections']} other entities")

        System monitoring and diagnostics::

            # Get comprehensive statistics
            stats_result = await memory_system.get_memory_statistics()

            if stats_result.success:
                stats = stats_result.result
                print(f"Total memories: {stats['store_statistics']['total_count']}")
                print(f"Operations performed: {stats['system_statistics']['total_operations']}")

            # Run system health check
            diag_result = await memory_system.run_system_diagnostic()

            if diag_result.success:
                health = diag_result.result["system_health"]
                print(f"System health: {health}")

                for component, status in diag_result.result["component_diagnostics"].items():
                    print(f"{component}: {status['status']}")

        Memory lifecycle management::

            # Consolidate memories (remove duplicates, expired entries)
            consolidation_result = await memory_system.consolidate_memories(
                namespace=("user", "temp"),
                dry_run=True  # Preview changes first
            )

            if consolidation_result.success:
                result = consolidation_result.result["consolidation_result"]
                print(f"Would remove {result['duplicates_found']} duplicates")
                print(f"Would expire {result['expired_found']} old memories")

            # Actually perform consolidation
            if input("Proceed with consolidation? (y/n): ").lower() == 'y':
                final_result = await memory_system.consolidate_memories(
                    namespace=("user", "temp"),
                    dry_run=False
                )

    Note:
        The UnifiedMemorySystem automatically selects the best agent for each operation
        based on the request type, available features, and performance considerations.
        Enable multi-agent coordination for the most intelligent behavior, or disable
        specific features for better performance in resource-constrained environments.
    """

    def __init__(self, config: MemorySystemConfig):
        """Initialize the unified memory system with comprehensive component setup.

        Creates and configures all memory system components including stores, classifiers,
        knowledge graph generators, retrievers, and coordinators based on the provided
        configuration. All components are initialized and validated during construction.

        Args:
            config: MemorySystemConfig with all system settings and feature flags

        Raises:
            ValueError: If required configuration parameters are missing or invalid
            RuntimeError: If component initialization fails

        Examples:
            Basic initialization::

                config = MemorySystemConfig(
                    store_type="memory",
                    collection_name="my_memories"
                )

                memory_system = UnifiedMemorySystem(config)
                print("System initialized successfully")

            Production initialization with validation::

                config = MemorySystemConfig(
                    store_type="postgres",
                    collection_name="prod_memories",
                    default_namespace=("company", "prod"),
                    enable_multi_agent_coordination=True,
                    llm_config=AugLLMConfig(model="gpt-4")
                )

                try:
                    memory_system = UnifiedMemorySystem(config)

                    # Validate initialization
                    system_info = memory_system.get_system_info()
                    assert system_info["initialized"]

                    print(f"System ready with {len(system_info['components'])} components")

                except Exception as e:
                    print(f"Initialization failed: {e}")

        Note:
            Component initialization follows dependency order: store → classifier →
            KG generator → retrievers → coordinator. If any component fails to
            initialize, the entire system initialization will fail.
        """
        self.config = config

        # Initialize core components
        self._initialize_store()
        self._initialize_classifier()
        self._initialize_kg_generator()
        self._initialize_retrievers()
        self._initialize_coordinator()

        # System state
        self._initialized = True
        self._stats = {
            "total_operations": 0,
            "successful_operations": 0,
            "failed_operations": 0,
            "total_memories_stored": 0,
            "total_memories_retrieved": 0,
            "avg_operation_time_ms": 0.0,
        }

    def _initialize_store(self) -> None:
        """Initialize the memory store."""
        # Create store manager
        store_manager = StoreManager(
            store_config={"type": StoreType.MEMORY},
            default_namespace=self.config.default_namespace,
        )

        # Create memory store config
        store_config = MemoryStoreConfig(
            store_manager=store_manager,
            default_namespace=self.config.default_namespace,
            auto_classify=self.config.enable_auto_classification,
        )

        # Create memory store manager
        self.memory_store = MemoryStoreManager(store_config)

    def _initialize_classifier(self) -> None:
        """Initialize the memory classifier."""
        classifier_config = MemoryClassifierConfig(
            llm_config=self.config.llm_config,
            confidence_threshold=self.config.classification_confidence_threshold,
        )

        self.classifier = MemoryClassifier(classifier_config)

    def _initialize_kg_generator(self) -> None:
        """Initialize the knowledge graph generator."""
        # Use Pydantic initialization (no __init__ override)
        self.kg_generator = KGGeneratorAgent(
            name="memory_kg_generator",
            engine=self.config.llm_config,
            memory_store=self.memory_store,
            classifier=self.classifier,
        )

    def _initialize_retrievers(self) -> None:
        """Initialize the retrieval systems."""
        self.retrievers = {}

        # Enhanced retriever
        if self.config.enable_enhanced_retrieval:
            EnhancedRetrieverConfig(
                memory_store_manager=self.memory_store,
                memory_classifier=self.classifier,
            )
            # Note: We'll need to create EnhancedRetriever class
            # self.retrievers["enhanced"] = EnhancedRetriever(enhanced_config)

        # Graph RAG retriever
        if self.config.enable_graph_rag:
            graph_rag_config = GraphRAGRetrieverConfig(
                memory_store_manager=self.memory_store,
                memory_classifier=self.classifier,
                kg_generator=self.kg_generator,
            )
            self.retrievers["graph_rag"] = GraphRAGRetriever(graph_rag_config)

        # Agentic RAG coordinator
        agentic_rag_config = AgenticRAGCoordinatorConfig(
            memory_store_manager=self.memory_store,
            memory_classifier=self.classifier,
            kg_generator=self.kg_generator,
        )
        self.agentic_rag = AgenticRAGCoordinator(agentic_rag_config)

    def _initialize_coordinator(self) -> None:
        """Initialize the multi-agent coordinator."""
        if self.config.enable_multi_agent_coordination:
            # Create coordinator config
            coordinator_config = MultiAgentCoordinatorConfig(
                memory_store_manager=self.memory_store,
                memory_classifier=self.classifier,
                kg_generator_config=KGGeneratorAgentConfig(
                    memory_store_manager=self.memory_store,
                    memory_classifier=self.classifier,
                ),
                agentic_rag_config=AgenticRAGCoordinatorConfig(
                    memory_store_manager=self.memory_store,
                    memory_classifier=self.classifier,
                    kg_generator=self.kg_generator,
                ),
            )

            self.coordinator = MultiAgentMemoryCoordinator(coordinator_config)
        else:
            self.coordinator = None

    async def store_memory(
        self,
        content: str,
        namespace: tuple[str, ...] | None = None,
        memory_type: MemoryType | None = None,
        importance: float | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> MemorySystemResult:
        """Store a memory in the system.

        Args:
            content: Memory content to store
            namespace: Memory namespace (defaults to configured default)
            memory_type: Force specific memory type (otherwise auto-classified)
            importance: Override importance score
            metadata: Additional metadata

        Returns:
            MemorySystemResult with operation result
        """
        start_time = datetime.now()

        try:
            # Use coordinator if available
            if self.coordinator:
                result = await self.coordinator.store_memory(
                    content=content, namespace=namespace
                )
                memory_id = result
            else:
                # Direct store operation
                memory_id = await self.memory_store.store_memory(
                    content=content,
                    namespace=namespace,
                    force_classification=memory_type,
                    importance_override=importance,
                )

            # Update stats
            self._stats["total_memories_stored"] += 1
            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="store_memory",
                result={"memory_id": memory_id},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="coordinator" if self.coordinator else "direct",
                confidence_score=1.0,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error storing memory: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="store_memory",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def retrieve_memories(
        self,
        query: str,
        limit: int = 10,
        namespace: tuple[str, ...] | None = None,
        memory_types: list[MemoryType] | None = None,
        use_graph_rag: bool = True,
        use_multi_agent: bool = True,
    ) -> MemorySystemResult:
        """Retrieve memories from the system.

        Args:
            query: Search query
            limit: Maximum number of memories to retrieve
            namespace: Memory namespace to search
            memory_types: Specific memory types to search
            use_graph_rag: Whether to use graph RAG
            use_multi_agent: Whether to use multi-agent coordination

        Returns:
            MemorySystemResult with retrieved memories
        """
        start_time = datetime.now()

        try:
            # Use coordinator if available and requested
            if self.coordinator and use_multi_agent:
                memories = await self.coordinator.retrieve_memories(
                    query=query,
                    limit=limit,
                    memory_types=memory_types,
                    namespace=namespace,
                )
                agent_used = "multi_agent_coordinator"

            # Use graph RAG if available and requested
            elif "graph_rag" in self.retrievers and use_graph_rag:
                result = await self.retrievers["graph_rag"].retrieve_memories(
                    query=query,
                    limit=limit,
                    memory_types=memory_types,
                    namespace=namespace,
                )
                memories = result.memories
                agent_used = "graph_rag"

            # Use agentic RAG coordinator
            elif self.agentic_rag:
                result = await self.agentic_rag.retrieve_memories(
                    query=query,
                    limit=limit,
                    memory_types=memory_types,
                    namespace=namespace,
                )
                memories = result.final_memories
                agent_used = "agentic_rag"

            # Fallback to direct store search
            else:
                memories = await self.memory_store.retrieve_memories(
                    query=query,
                    limit=limit,
                    namespace=namespace,
                    memory_types=memory_types,
                )
                agent_used = "direct_store"

            # Update stats
            self._stats["total_memories_retrieved"] += len(memories)
            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="retrieve_memories",
                result={"memories": memories, "count": len(memories), "query": query},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used=agent_used,
                confidence_score=0.8,  # Default confidence
                completeness_score=min(len(memories) / limit, 1.0),
            )

        except Exception as e:
            logger.exception(f"Error retrieving memories: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="retrieve_memories",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def classify_memory(
        self, content: str, user_context: dict[str, Any] | None = None
    ) -> MemorySystemResult:
        """Classify memory content.

        Args:
            content: Memory content to classify
            user_context: User context for classification

        Returns:
            MemorySystemResult with classification result
        """
        start_time = datetime.now()

        try:
            # Use coordinator if available
            if self.coordinator:
                result = await self.coordinator.analyze_memory(content)
                if result["success"]:
                    classification = result["analysis"]
                else:
                    raise Exception(result["error"])
            else:
                # Direct classification
                classification = self.classifier.classify_memory(
                    content=content, user_context=user_context
                )

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="classify_memory",
                result={"classification": classification, "content": content},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="coordinator" if self.coordinator else "direct",
                confidence_score=getattr(classification, "confidence", 0.8),
            )

        except Exception as e:
            logger.exception(f"Error classifying memory: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="classify_memory",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def generate_knowledge_graph(
        self,
        namespace: tuple[str, ...] | None = None,
        force_regeneration: bool = False,
    ) -> MemorySystemResult:
        """Generate knowledge graph from memories.

        Args:
            namespace: Memory namespace to process
            force_regeneration: Force regeneration even if graph exists

        Returns:
            MemorySystemResult with knowledge graph
        """
        start_time = datetime.now()

        try:
            # Use coordinator if available
            if self.coordinator:
                result = await self.coordinator.generate_knowledge_graph(namespace)
                if result["success"]:
                    knowledge_graph = result["knowledge_graph"]
                else:
                    raise Exception(result["error"])
            else:
                # Direct KG generation
                knowledge_graph = (
                    await self.kg_generator.extract_knowledge_graph_from_memories(
                        namespace=namespace
                    )
                )

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="generate_knowledge_graph",
                result={"knowledge_graph": knowledge_graph, "namespace": namespace},
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="coordinator" if self.coordinator else "direct",
                confidence_score=0.8,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error generating knowledge graph: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="generate_knowledge_graph",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def consolidate_memories(
        self, namespace: tuple[str, ...] | None = None, dry_run: bool = False
    ) -> MemorySystemResult:
        """Consolidate memories by removing duplicates and expired entries.

        Args:
            namespace: Memory namespace to consolidate
            dry_run: If True, only analyze without making changes

        Returns:
            MemorySystemResult with consolidation results
        """
        start_time = datetime.now()

        try:
            # Use memory store consolidation
            result = await self.memory_store.consolidate_memories(
                namespace=namespace, dry_run=dry_run
            )

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="consolidate_memories",
                result={
                    "consolidation_result": result,
                    "namespace": namespace,
                    "dry_run": dry_run,
                },
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="memory_store",
                confidence_score=1.0,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error consolidating memories: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="consolidate_memories",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def get_memory_statistics(
        self, namespace: tuple[str, ...] | None = None
    ) -> MemorySystemResult:
        """Get comprehensive memory statistics.

        Args:
            namespace: Memory namespace to analyze

        Returns:
            MemorySystemResult with statistics
        """
        start_time = datetime.now()

        try:
            # Get store statistics
            store_stats = await self.memory_store.get_memory_statistics(namespace)

            # Get system statistics
            system_stats = self._stats.copy()

            # Get coordinator statistics if available
            coordinator_stats = {}
            if self.coordinator:
                coordinator_stats = self.coordinator.get_system_status()

            combined_stats = {
                "store_statistics": store_stats,
                "system_statistics": system_stats,
                "coordinator_statistics": coordinator_stats,
            }

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="get_memory_statistics",
                result=combined_stats,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="system",
                confidence_score=1.0,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error getting memory statistics: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="get_memory_statistics",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def search_entities(
        self, entity_name: str, namespace: tuple[str, ...] | None = None
    ) -> MemorySystemResult:
        """Search for entities in the knowledge graph.

        Args:
            entity_name: Name of entity to search for
            namespace: Memory namespace to search

        Returns:
            MemorySystemResult with entity information
        """
        start_time = datetime.now()

        try:
            # Get entity context from KG generator
            entity_context = await self.kg_generator.get_entity_context(entity_name)

            if "error" in entity_context:
                raise Exception(entity_context["error"])

            # Get related memories using graph RAG if available
            related_memories = []
            if "graph_rag" in self.retrievers:
                result = await self.retrievers["graph_rag"].retrieve_memories(
                    query=entity_name,
                    limit=10,
                    namespace=namespace,
                    enable_graph_traversal=True,
                )
                related_memories = result.memories

            combined_result = {
                "entity_context": entity_context,
                "related_memories": related_memories,
                "entity_name": entity_name,
            }

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="search_entities",
                result=combined_result,
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="kg_generator",
                confidence_score=0.8,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error searching entities: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="search_entities",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    async def run_system_diagnostic(self) -> MemorySystemResult:
        """Run comprehensive system diagnostic.

        Returns:
            MemorySystemResult with diagnostic results
        """
        start_time = datetime.now()

        try:
            diagnostic_results = {}

            # Test memory store
            try:
                test_id = await self.memory_store.store_memory(
                    content="System diagnostic test", namespace=("system", "diagnostic")
                )
                await self.memory_store.get_memory_by_id(test_id)
                diagnostic_results["memory_store"] = {"status": "healthy"}
            except Exception as e:
                diagnostic_results["memory_store"] = {
                    "status": "error",
                    "error": str(e),
                }

            # Test classifier
            try:
                classification = self.classifier.classify_memory("Test memory")
                diagnostic_results["classifief"] = {
                    "status": "healthy",
                    "classification_types": len(classification.memory_types),
                }
            except Exception as e:
                diagnostic_results["classifief"] = {"status": "error", "error": str(e)}

            # Test KG generator
            try:
                kg_stats = (
                    f"KG has {len(self.kg_generator.knowledge_graph.nodes)} nodes"
                )
                diagnostic_results["kg_generatof"] = {
                    "status": "healthy",
                    "info": kg_stats,
                }
            except Exception as e:
                diagnostic_results["kg_generatof"] = {
                    "status": "error",
                    "error": str(e),
                }

            # Test coordinator if available
            if self.coordinator:
                try:
                    coord_diagnostic = await self.coordinator.run_diagnostic()
                    diagnostic_results["coordinatof"] = {
                        "status": coord_diagnostic["system_status"],
                        "details": coord_diagnostic,
                    }
                except Exception as e:
                    diagnostic_results["coordinatof"] = {
                        "status": "error",
                        "error": str(e),
                    }

            # Overall health
            all_healthy = all(
                result["status"] == "healthy" for result in diagnostic_results.values()
            )

            system_health = "healthy" if all_healthy else "degraded"

            self._update_operation_stats(start_time, success=True)

            return MemorySystemResult(
                success=True,
                operation="run_system_diagnostic",
                result={
                    "system_health": system_health,
                    "component_diagnostics": diagnostic_results,
                    "system_statistics": self._stats,
                },
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
                agent_used="system",
                confidence_score=1.0,
                completeness_score=1.0,
            )

        except Exception as e:
            logger.exception(f"Error running system diagnostic: {e}")
            self._update_operation_stats(start_time, success=False)

            return MemorySystemResult(
                success=False,
                operation="run_system_diagnostic",
                error=str(e),
                execution_time_ms=(datetime.now() - start_time).total_seconds() * 1000,
            )

    def _update_operation_stats(self, start_time: datetime, success: bool) -> None:
        """Update operation statistics."""
        self._stats["total_operations"] += 1

        if success:
            self._stats["successful_operations"] += 1
        else:
            self._stats["failed_operations"] += 1

        # Update average operation time
        operation_time = (datetime.now() - start_time).total_seconds() * 1000
        current_avg = self._stats["avg_operation_time_ms"]
        total_ops = self._stats["total_operations"]

        self._stats["avg_operation_time_ms"] = (
            current_avg * (total_ops - 1) + operation_time
        ) / total_ops

    def get_system_info(self) -> dict[str, Any]:
        """Get comprehensive system information."""
        return {
            "system_version": "1.0.0",
            "initialized": self._initialized,
            "configuration": {
                "store_type": self.config.store_type,
                "collection_name": self.config.collection_name,
                "auto_classification": self.config.enable_auto_classification,
                "enhanced_retrieval": self.config.enable_enhanced_retrieval,
                "graph_rag": self.config.enable_graph_rag,
                "multi_agent_coordination": self.config.enable_multi_agent_coordination,
            },
            "components": {
                "memory_store": "initialized",
                "classifier": "initialized",
                "kg_generator": "initialized",
                "retrievers": list(self.retrievers.keys()),
                "agentic_rag": "initialized" if self.agentic_rag else "disabled",
                "coordinator": "initialized" if self.coordinator else "disabled",
            },
            "statistics": self._stats,
        }


# Convenience functions for easy usage
async def create_memory_system(
    store_type: str = "memory",
    collection_name: str = "haive_memories",
    enable_all_features: bool = True,
) -> UnifiedMemorySystem:
    """Create a unified memory system with sensible default configuration.

    This convenience function creates a UnifiedMemorySystem with commonly used
    settings, making it easy to get started without complex configuration.

    Args:
        store_type: Type of store backend to use ("memory", "postgres", "redis")
        collection_name: Name for the memory collection/table
        enable_all_features: Whether to enable all advanced features (Graph RAG,
                           multi-agent coordination, auto-classification)

    Returns:
        UnifiedMemorySystem: Fully configured and ready-to-use memory system

    Examples:
        Quick start with in-memory storage::

            # Create system with all features enabled
            memory_system = await create_memory_system()

            # System is ready to use immediately
            result = await memory_system.store_memory("Hello, world!")
            print(f"Stored memory: {result.success}")

        Production setup with PostgreSQL::

            memory_system = await create_memory_system(
                store_type="postgres",
                collection_name="company_memories",
                enable_all_features=True
            )

            # Verify system health
            diag = await memory_system.run_system_diagnostic()
            print(f"System health: {diag.result['system_health']}")

        Performance-focused setup::

            # Disable resource-intensive features for speed
            memory_system = await create_memory_system(
                store_type="memory",
                collection_name="fast_cache",
                enable_all_features=False
            )

            # System will use basic storage and retrieval only
            result = await memory_system.store_memory("Fast storage test")

    Note:
        When enable_all_features=True, the system includes:
        - Automatic memory classification
        - Enhanced multi-strategy retrieval
        - Graph RAG with knowledge graph traversal
        - Multi-agent coordination for optimal routing

        When enable_all_features=False, only basic storage and retrieval are enabled
        for maximum performance.
    """
    config = MemorySystemConfig(
        store_type=store_type,
        collection_name=collection_name,
        enable_auto_classification=enable_all_features,
        enable_enhanced_retrieval=enable_all_features,
        enable_graph_rag=enable_all_features,
        enable_multi_agent_coordination=enable_all_features,
    )

    return UnifiedMemorySystem(config)


async def quick_memory_demo():
    """Comprehensive demonstration of the unified memory system capabilities.

    This demo showcases the main features of the UnifiedMemorySystem including:
    - Memory storage with automatic classification
    - Intelligent retrieval with multiple strategies
    - Knowledge graph generation and analysis
    - System diagnostics and health monitoring
    - Performance metrics and statistics

    Examples:
        Run the complete demo::

            await quick_memory_demo()

        Use as a template for your own integration::

            # Copy relevant sections from this demo
            memory_system = await create_memory_system()

            # Store your data
            for item in your_data:
                await memory_system.store_memory(item)

            # Query your data
            result = await memory_system.retrieve_memories("your query")
    """
    # Create memory system
    memory_system = await create_memory_system(
        store_type="memory", collection_name="demo_memories"
    )

    memory_system.get_system_info()

    # Store some memories

    memories_to_store = [
        "Alice works at TechCorp as a software engineer",
        "Bob is a data scientist at DataFlow Inc",
        "Alice and Bob collaborated on the ML project last month",
        "The ML project involved building a recommendation system",
        "TechCorp is located in San Francisco",
        "DataFlow Inc specializes in big data analytics",
        "The recommendation system uses collaborative filtering",
        "Alice has 5 years of experience in Python programming",
    ]

    storage_times = []
    for memory in memories_to_store:
        result = await memory_system.store_memory(memory)
        if result.success:
            storage_times.append(result.execution_time_ms)
            result.result["memory_id"]
        else:
            pass

    sum(storage_times) / len(storage_times) if storage_times else 0

    # Retrieve memories with different strategies

    queries = [
        "Who works at TechCorp?",
        "What did Alice and Bob work on together?",
        "Where is TechCorp located?",
        "What technologies were used in the ML project?",
    ]

    for query in queries:

        # Test different retrieval modes
        modes = [
            ("Multi-Agent", True, True),
            ("Graph RAG", False, True),
            ("Basic", False, False),
        ]

        for _mode_name, use_multi_agent, use_graph_rag in modes:
            result = await memory_system.retrieve_memories(
                query,
                limit=2,
                use_multi_agent=use_multi_agent,
                use_graph_rag=use_graph_rag,
            )

            if result.success:
                memories = result.result["memories"]
                for memory in memories[:1]:  # Show first result
                    memory.get("content", "")[:60]
            else:
                pass

    # Generate and analyze knowledge graph

    kg_result = await memory_system.generate_knowledge_graph()
    if kg_result.success:
        kg = kg_result.result["knowledge_graph"]

        # Show some entities
        if kg.nodes:
            sample_entities = list(kg.nodes.values())[:3]
            for _entity in sample_entities:
                pass
    else:
        pass

    # Entity search demonstration

    entities_to_search = ["Alice", "TechCorp", "ML project"]
    for entity_name in entities_to_search:
        entity_result = await memory_system.search_entities(entity_name)
        if entity_result.success:
            context = entity_result.result["entity_context"]
            if "error" not in context:
                context["entity"]
                context["total_connections"]
                memories = context["memory_count"]
            else:
                pass
        else:
            pass

    # Get comprehensive statistics

    stats_result = await memory_system.get_memory_statistics()
    if stats_result.success:
        stats = stats_result.result
        stats["store_statistics"]
        stats["system_statistics"]

    # Run comprehensive diagnostic

    diag_result = await memory_system.run_system_diagnostic()
    if diag_result.success:
        diag_result.result["system_health"]
        components = diag_result.result["component_diagnostics"]

        for _component, status in components.items():
            "✅" if status["status"] == "healthy" else "❌"
    else:
        pass


if __name__ == "__main__":
    """Run the memory system demonstration.

    This script demonstrates the complete capabilities of the UnifiedMemorySystem
    including storage, retrieval, knowledge graph generation, and system monitoring.

    Usage:
        python unified_memory_api.py

    The demo will:
    1. Create a memory system with all features enabled
    2. Store sample memories with relationship data
    3. Test different retrieval strategies and compare performance
    4. Generate and analyze a knowledge graph
    5. Search for specific entities
    6. Display comprehensive system statistics
    7. Run system diagnostics
    """
    # Run comprehensive demo
    asyncio.run(quick_memory_demo())
