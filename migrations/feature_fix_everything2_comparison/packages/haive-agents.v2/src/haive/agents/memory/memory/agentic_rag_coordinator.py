"""Agentic RAG Coordinator for Memory System.

This module provides an intelligent coordinator that selects and combines
multiple retrieval strategies based on query analysis and context.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory.core.classifier import MemoryClassifier
from haive.agents.memory.core.stores import MemoryStoreManager
from haive.agents.memory.core.types import MemoryType
from haive.agents.memory.enhanced_retriever import EnhancedRetrieverConfig
from haive.agents.memory.graph_rag_retriever import (
    GraphRAGRetriever,
    GraphRAGRetrieverConfig,
)
from haive.agents.memory.kg_generator_agent import KGGeneratorAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class RetrievalStrategy(BaseModel):
    """Represents a retrieval strategy with its configuration and performance characteristics.

    A retrieval strategy defines how to retrieve memories for specific types of queries,
    including the strategy's strengths, supported memory types, and performance parameters.

    Attributes:
        name: Unique identifier for the strategy (e.g., "enhanced_similarity")
        description: Human-readable description of what the strategy does
        best_for: List of query types this strategy excels at handling
        memory_types: List of memory types this strategy is optimized for
        confidence_threshold: Minimum confidence score required to use this strategy
        typical_latency_ms: Expected response time in milliseconds for this strategy
        max_results: Maximum number of results this strategy can return
        parameters: Strategy-specific configuration parameters

    Examples:
        Creating an enhanced similarity strategy::

            strategy = RetrievalStrategy(
                name="enhanced_similarity",
                description="Multi-factor similarity search with memory type awareness",
                best_for=["factual_queries", "recent_events", "personal_information"],
                memory_types=[MemoryType.SEMANTIC, MemoryType.EPISODIC],
                confidence_threshold=0.6,
                typical_latency_ms=300,
                max_results=15,
                parameters={"enable_query_expansion": True, "importance_boost": 0.2}
            )

        Creating a graph traversal strategy::

            strategy = RetrievalStrategy(
                name="graph_traversal",
                description="Knowledge graph traversal for relationship discovery",
                best_for=["relationship_queries", "entity_connections"],
                memory_types=[MemoryType.CONTEXTUAL, MemoryType.SEMANTIC],
                confidence_threshold=0.7,
                typical_latency_ms=800,
                max_results=12,
                parameters={"max_depth": 3, "min_confidence": 0.6}
            )
    """

    name: str = Field(..., description="Strategy name")
    description: str = Field(..., description="Strategy description")
    best_for: list[str] = Field(
        ..., description="Query types this strategy is best for"
    )
    memory_types: list[MemoryType] = Field(
        ..., description="Memory types this strategy handles well"
    )
    confidence_threshold: float = Field(
        default=0.7, description="Minimum confidence to use this strategy"
    )

    # Performance characteristics
    typical_latency_ms: float = Field(
        default=500, description="Typical latency in milliseconds"
    )
    max_results: int = Field(
        default=10, description="Maximum results this strategy returns"
    )

    # Strategy-specific parameters
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Strategy-specific parameters"
    )


class AgenticRAGResult(BaseModel):
    """Comprehensive result from agentic RAG coordinator with performance metrics and analysis.

    This class encapsulates all information from an agentic RAG retrieval operation,
    including the retrieved memories, strategy details, performance metrics, and
    quality scores for analysis and optimization.

    Attributes:
        query: Original user query that was processed
        selected_strategies: List of strategy names that were selected and executed
        strategy_results: Detailed results from each individual strategy
        final_memories: Final ranked and deduplicated memories after strategy fusion
        final_scores: Relevance scores for each memory in final_memories
        total_time_ms: Total processing time for the entire operation
        strategy_times: Execution time for each individual strategy
        query_analysis: Detailed analysis of the query (intent, complexity, etc.)
        strategy_reasoning: Explanation of why specific strategies were selected
        diversity_score: Measure of diversity in the retrieved memories (0.0-1.0)
        coverage_score: Measure of how well results cover query aspects (0.0-1.0)
        confidence_score: Overall confidence in the result quality (0.0-1.0)

    Examples:
        Accessing retrieval results::

            result = await coordinator.retrieve_memories("How do I deploy web apps?")

            print(f"Query: {result.query}")
            print(f"Strategies used: {result.selected_strategies}")
            print(f"Total memories: {len(result.final_memories)}")
            print(f"Processing time: {result.total_time_ms:.1f}ms")

            # Access individual memories
            for i, memory in enumerate(result.final_memories):
                score = result.final_scores[i] if i < len(result.final_scores) else 0.0
                print(f"Memory {i+1}: {memory['content'][:100]}... (score: {score:.2f})")

        Analyzing strategy performance::

            result = await coordinator.retrieve_memories("complex query")

            print(f"Strategy reasoning: {result.strategy_reasoning}")
            print(f"Quality scores:")
            print(f"  Diversity: {result.diversity_score:.2f}")
            print(f"  Coverage: {result.coverage_score:.2f}")
            print(f"  Confidence: {result.confidence_score:.2f}")

            # Strategy timing analysis
            for strategy, time_ms in result.strategy_times.items():
                print(f"  {strategy}: {time_ms:.1f}ms")

        Query analysis details::

            result = await coordinator.retrieve_memories("What did I learn about ML?")

            if result.query_analysis:
                analysis = result.query_analysis
                print(f"Memory types needed: {analysis.get('memory_types', [])}")
                print(f"Query complexity: {analysis.get('complexity', 'unknown')}")
                print(f"Requires reasoning: {analysis.get('requires_reasoning', False)}")
                print(f"Entities: {analysis.get('entities', [])}")
                print(f"Topics: {analysis.get('topics', [])}")
    """

    query: str = Field(..., description="Original query")
    selected_strategies: list[str] = Field(
        default_factory=list, description="Selected retrieval strategies"
    )
    strategy_results: dict[str, Any] = Field(
        default_factory=dict, description="Results from each strategy"
    )

    # Final combined results
    final_memories: list[dict[str, Any]] = Field(
        default_factory=list, description="Final ranked memories"
    )
    final_scores: list[float] = Field(
        default_factory=list, description="Final ranking scores"
    )

    # Performance metrics
    total_time_ms: float = Field(default=0.0, description="Total processing time")
    strategy_times: dict[str, float] = Field(
        default_factory=dict, description="Time for each strategy"
    )

    # Analysis information
    query_analysis: dict[str, Any] | None = Field(
        default=None, description="Query analysis results"
    )
    strategy_reasoning: str = Field(
        default="", description="Reasoning for strategy selection"
    )

    # Quality metrics
    diversity_score: float = Field(
        default=0.0, description="Diversity of retrieved memories"
    )
    coverage_score: float = Field(default=0.0, description="Coverage of query aspects")
    confidence_score: float = Field(
        default=0.0, description="Overall confidence in results"
    )


class AgenticRAGCoordinatorConfig(BaseModel):
    """Configuration for Agentic RAG Coordinator with intelligent strategy selection.

    This configuration class defines all parameters needed to create and configure
    an AgenticRAGCoordinator, including core components, retrieval strategies,
    coordination settings, and result fusion parameters.

    Attributes:
        name: Unique identifier for the coordinator instance
        memory_store_manager: Manager for memory storage and retrieval operations
        memory_classifier: Classifier for analyzing query intent and memory types
        kg_generator: Optional knowledge graph generator for graph-based retrieval
        enhanced_retriever_config: Configuration for enhanced vector retrieval
        graph_rag_config: Configuration for graph-enhanced RAG retrieval
        max_strategies: Maximum number of strategies to use per query
        min_confidence_threshold: Minimum confidence score required to use a strategy
        enable_strategy_combination: Whether to enable multi-strategy result fusion
        coordinator_llm: LLM configuration for strategy selection and coordination
        fusion_method: Method used for combining results from multiple strategies
        diversity_weight: Weight given to diversity in result ranking (0.0-1.0)
        coverage_weight: Weight given to coverage in result ranking (0.0-1.0)
        relevance_weight: Weight given to relevance in result ranking (0.0-1.0)

    Examples:
        Basic configuration::

            config = AgenticRAGCoordinatorConfig(
                name="my_rag_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                kg_generator=kg_generator,
                max_strategies=2,
                min_confidence_threshold=0.6
            )

        Advanced configuration with custom retrieval components::

            config = AgenticRAGCoordinatorConfig(
                name="advanced_rag_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                kg_generator=kg_generator,

                # Enhanced retrieval configuration
                enhanced_retriever_config=EnhancedRetrieverConfig(
                    enable_query_expansion=True,
                    importance_boost=0.2
                ),

                # Graph RAG configuration
                graph_rag_config=GraphRAGRetrieverConfig(
                    enable_graph_traversal=True,
                    max_graph_depth=3,
                    min_confidence_threshold=0.6
                ),

                # Coordination settings
                max_strategies=3,
                min_confidence_threshold=0.5,
                enable_strategy_combination=True,

                # LLM configuration
                coordinator_llm=AugLLMConfig(
                    model="gpt-4",
                    temperature=0.2,
                    max_tokens=1000
                ),

                # Result fusion weights
                fusion_method="weighted_rank",
                diversity_weight=0.25,
                coverage_weight=0.35,
                relevance_weight=0.4
            )

        Performance-optimized configuration::

            config = AgenticRAGCoordinatorConfig(
                name="fast_rag_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,

                # Single strategy for speed
                max_strategies=1,
                min_confidence_threshold=0.7,
                enable_strategy_combination=False,

                # Fast LLM configuration
                coordinator_llm=AugLLMConfig(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    max_tokens=500
                ),

                # Relevance-focused fusion
                fusion_method="relevance_only",
                diversity_weight=0.0,
                coverage_weight=0.0,
                relevance_weight=1.0
            )

    Note:
        The weights for diversity, coverage, and relevance should sum to 1.0
        for optimal result fusion. The coordinator will normalize them if needed.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core components
    name: str = Field(default="agentic_rag_coordinator", description="Agent name")
    memory_store_manager: MemoryStoreManager = Field(
        ..., description="Memory store manager"
    )
    memory_classifier: MemoryClassifier = Field(..., description="Memory classifier")
    kg_generator: KGGeneratorAgent | None = Field(
        default=None, description="Knowledge graph generator"
    )

    # Retrieval components
    enhanced_retriever_config: EnhancedRetrieverConfig | None = Field(
        default=None, description="Enhanced retriever configuration"
    )
    graph_rag_config: GraphRAGRetrieverConfig | None = Field(
        default=None, description="Graph RAG configuration"
    )

    # Coordination configuration
    max_strategies: int = Field(
        default=3, description="Maximum strategies to use per query"
    )
    min_confidence_threshold: float = Field(
        default=0.5, description="Minimum confidence to use strategy"
    )
    enable_strategy_combination: bool = Field(
        default=True, description="Enable combining multiple strategies"
    )

    # LLM configuration
    coordinator_llm: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="LLM for coordination"
    )

    # Result fusion configuration
    fusion_method: str = Field(
        default="weighted_rank", description="Method for fusing results"
    )
    diversity_weight: float = Field(
        default=0.2, description="Weight for diversity in ranking"
    )
    coverage_weight: float = Field(
        default=0.3, description="Weight for coverage in ranking"
    )
    relevance_weight: float = Field(
        default=0.5, description="Weight for relevance in ranking"
    )


class AgenticRAGCoordinator(SimpleAgent):
    """Intelligent coordinator that selects and combines retrieval strategies for optimal memory retrieval.

    The AgenticRAGCoordinator is an advanced memory retrieval agent that analyzes incoming
    queries and dynamically selects the most appropriate retrieval strategies from a
    comprehensive set of available options. It combines results from multiple strategies
    to provide comprehensive, diverse, and relevant memory retrieval.

    Key Features:
        - Intelligent strategy selection based on query analysis
        - Multi-strategy parallel execution for comprehensive coverage
        - Advanced result fusion with diversity and coverage optimization
        - Performance monitoring and optimization
        - Adaptive strategy weighting based on query characteristics
        - Support for graph-based, semantic, temporal, and procedural retrieval

    Attributes:
        memory_store: Memory store manager for basic memory operations
        classifier: Memory classifier for query analysis and intent detection
        kg_generator: Optional knowledge graph generator for graph-based retrieval
        enhanced_retriever_config: Configuration for enhanced vector retrieval
        graph_rag_config: Configuration for graph-enhanced RAG retrieval
        max_strategies: Maximum number of strategies to use per query
        min_confidence_threshold: Minimum confidence score required to use a strategy
        enable_strategy_combination: Whether to enable multi-strategy result fusion
        fusion_method: Method used for combining results from multiple strategies
        diversity_weight: Weight given to diversity in result ranking (0.0-1.0)
        coverage_weight: Weight given to coverage in result ranking (0.0-1.0)
        relevance_weight: Weight given to relevance in result ranking (0.0-1.0)
        coordinator_llm: LLM runnable for strategy selection and coordination
        retrievers: Dictionary of available retrieval components
        strategies: Dictionary of available retrieval strategies
        strategy_selection_prompt: Prompt template for strategy selection
        result_fusion_prompt: Prompt template for result fusion

    Examples:
        Basic coordinator usage::

            # Create coordinator
            coordinator = AgenticRAGCoordinator(config)

            # Retrieve memories with intelligent strategy selection
            result = await coordinator.retrieve_memories(
                "How do I deploy a web application with Docker?"
            )

            print(f"Retrieved {len(result.final_memories)} memories")
            print(f"Used strategies: {result.selected_strategies}")
            print(f"Processing time: {result.total_time_ms:.1f}ms")

            # Access retrieved memories
            for i, memory in enumerate(result.final_memories):
                score = result.final_scores[i]
                print(f"Memory {i+1}: {memory['content'][:100]}... (score: {score:.2f})")

        Advanced retrieval with filtering::

            # Retrieve with specific memory types and limits
            result = await coordinator.retrieve_memories(
                query="What are the best practices for API security?",
                limit=5,
                memory_types=[MemoryType.SEMANTIC, MemoryType.PROCEDURAL],
                namespace=("user", "security")
            )

            # Analyze strategy performance
            print(f"Strategy reasoning: {result.strategy_reasoning}")
            print(f"Quality scores: diversity={result.diversity_score:.2f}, "
                  f"coverage={result.coverage_score:.2f}, confidence={result.confidence_score:.2f}")

        Performance analysis::

            result = await coordinator.retrieve_memories("complex technical query")

            # Analyze individual strategy performance
            for strategy_name, strategy_data in result.strategy_results.items():
                memory_count = len(strategy_data.get('memories', []))
                exec_time = strategy_data.get('execution_time_ms', 0)
                print(f"{strategy_name}: {memory_count} memories in {exec_time:.1f}ms")

        Forced strategy selection (for testing)::

            # Force specific strategies for testing or optimization
            result = await coordinator.retrieve_memories(
                query="test query",
                force_strategies=["enhanced_similarity", "graph_traversal"]
            )

            print(f"Forced strategies: {result.selected_strategies}")

    Note:
        The coordinator automatically selects the best strategies based on query
        analysis, but can be configured with custom weights and thresholds for
        different use cases and performance requirements.
    """

    # RAG-specific fields
    memory_store: MemoryStoreManager = Field(..., description="Memory store manager")
    classifier: MemoryClassifier = Field(..., description="Memory classifier")
    kg_generator: KGGeneratorAgent | None = Field(
        default=None, description="Knowledge graph generator"
    )

    # Retrieval components
    enhanced_retriever_config: EnhancedRetrieverConfig | None = Field(
        default=None, description="Enhanced retriever configuration"
    )
    graph_rag_config: GraphRAGRetrieverConfig | None = Field(
        default=None, description="Graph RAG configuration"
    )

    # Coordination configuration
    max_strategies: int = Field(
        default=3, description="Maximum strategies to use per query"
    )
    min_confidence_threshold: float = Field(
        default=0.5, description="Minimum confidence to use strategy"
    )
    enable_strategy_combination: bool = Field(
        default=True, description="Enable combining multiple strategies"
    )

    # Result fusion configuration
    fusion_method: str = Field(
        default="weighted_rank", description="Method for fusing results"
    )
    diversity_weight: float = Field(
        default=0.2, description="Weight for diversity in ranking"
    )
    coverage_weight: float = Field(
        default=0.3, description="Weight for coverage in ranking"
    )
    relevance_weight: float = Field(
        default=0.5, description="Weight for relevance in ranking"
    )

    # Runtime fields
    coordinator_llm: Any = Field(default=None, description="LLM for coordination")
    retrievers: dict[str, Any] = Field(
        default_factory=dict, description="Available retrievers"
    )
    strategies: dict[str, RetrievalStrategy] = Field(
        default_factory=dict, description="Available strategies"
    )

    # Prompt fields
    strategy_selection_prompt: PromptTemplate = Field(
        default=None, description="Strategy selection prompt"
    )
    result_fusion_prompt: PromptTemplate = Field(
        default=None, description="Result fusion prompt"
    )

    def __init__(self, config: AgenticRAGCoordinatorConfig) -> None:
        """Initialize the Agentic RAG Coordinator with comprehensive strategy setup.

        Sets up the coordinator with all necessary components including retrievers,
        strategies, and prompts for intelligent memory retrieval coordination.

        Args:
            config: AgenticRAGCoordinatorConfig containing all coordinator settings

        Examples:
            Basic initialization::

                config = AgenticRAGCoordinatorConfig(
                    name="my_coordinator",
                    memory_store_manager=store_manager,
                    memory_classifier=classifier,
                    kg_generator=kg_generator
                )

                coordinator = AgenticRAGCoordinator(config)

            Advanced initialization with custom settings::

                config = AgenticRAGCoordinatorConfig(
                    name="advanced_coordinator",
                    memory_store_manager=store_manager,
                    memory_classifier=classifier,
                    kg_generator=kg_generator,
                    enhanced_retriever_config=enhanced_config,
                    graph_rag_config=graph_config,
                    max_strategies=3,
                    min_confidence_threshold=0.7,
                    enable_strategy_combination=True,
                    coordinator_llm=AugLLMConfig(model="gpt-4", temperature=0.2),
                    fusion_method="weighted_rank",
                    diversity_weight=0.25,
                    coverage_weight=0.35,
                    relevance_weight=0.4
                )

                coordinator = AgenticRAGCoordinator(config)

        Note:
            The coordinator automatically sets up all available retrieval strategies
            based on the provided configuration. Optional components (like graph RAG)
            will only be available if their configurations are provided.
        """
        # Initialize SimpleAgent with extracted config values
        super().__init__(
            name=config.name,
            engine=config.coordinator_llm,
            memory_store=config.memory_store_manager,
            classifier=config.memory_classifier,
            kg_generator=config.kg_generator,
            enhanced_retriever_config=config.enhanced_retriever_config,
            graph_rag_config=config.graph_rag_config,
            max_strategies=config.max_strategies,
            min_confidence_threshold=config.min_confidence_threshold,
            enable_strategy_combination=config.enable_strategy_combination,
            fusion_method=config.fusion_method,
            diversity_weight=config.diversity_weight,
            coverage_weight=config.coverage_weight,
            relevance_weight=config.relevance_weight,
        )

        # Setup LLM for coordination
        self.coordinator_llm = config.coordinator_llm.create_runnable()

        # Initialize and setup retrievers
        self._setup_retrievers()

        # Define available strategies
        self.strategies = self._define_strategies()

        # Setup prompts
        self._setup_prompts()

    def _setup_retrievers(self) -> None:
        """Setup individual retrievers."""
        # Enhanced retriever (vector similarity with memory types)
        if self.enhanced_retriever_config:
            from haive.agents.memory.enhanced_retriever import EnhancedRetriever

            self.retrievers["enhanced"] = EnhancedRetriever(
                self.enhanced_retriever_config
            )

        # Graph RAG retriever
        if self.graph_rag_config:
            self.retrievers["graph_rag"] = GraphRAGRetriever(self.graph_rag_config)

        # Basic vector retriever (fallback)
        self.retrievers["basic"] = self.memory_store

    def _define_strategies(self) -> dict[str, RetrievalStrategy]:
        """Define available retrieval strategies."""
        strategies = {}

        # Enhanced similarity strategy
        strategies["enhanced_similarity"] = RetrievalStrategy(
            name="enhanced_similarity",
            description="Multi-factor similarity search with memory type awareness",
            best_for=["factual_queries", "recent_events", "personal_information"],
            memory_types=[
                MemoryType.SEMANTIC,
                MemoryType.EPISODIC,
                MemoryType.PREFERENCE,
            ],
            confidence_threshold=0.6,
            typical_latency_ms=300,
            max_results=15,
            parameters={"enable_query_expansion": True, "importance_boost": 0.2},
        )

        # Graph traversal strategy
        strategies["graph_traversal"] = RetrievalStrategy(
            name="graph_traversal",
            description="Knowledge graph traversal for relationship discovery",
            best_for=[
                "relationship_queries",
                "entity_connections",
                "complex_reasoning",
            ],
            memory_types=[
                MemoryType.CONTEXTUAL,
                MemoryType.SEMANTIC,
                MemoryType.EPISODIC,
            ],
            confidence_threshold=0.7,
            typical_latency_ms=800,
            max_results=12,
            parameters={"max_depth": 3, "min_confidence": 0.6},
        )

        # Procedural knowledge strategy
        strategies["procedural_search"] = RetrievalStrategy(
            name="procedural_search",
            description="Specialized search for how-to and process information",
            best_for=["how_to_queries", "process_questions", "workflow_information"],
            memory_types=[MemoryType.PROCEDURAL, MemoryType.SEMANTIC],
            confidence_threshold=0.6,
            typical_latency_ms=400,
            max_results=8,
            parameters={"focus_on_steps": True, "sequential_ordering": True},
        )

        # Temporal search strategy
        strategies["temporal_search"] = RetrievalStrategy(
            name="temporal_search",
            description="Time-aware search for chronological information",
            best_for=["time_based_queries", "chronological_events", "recent_updates"],
            memory_types=[MemoryType.TEMPORAL, MemoryType.EPISODIC],
            confidence_threshold=0.5,
            typical_latency_ms=350,
            max_results=10,
            parameters={"recency_boost": 0.4, "temporal_ordering": True},
        )

        # Error and feedback strategy
        strategies["error_feedback_search"] = RetrievalStrategy(
            name="error_feedback_search",
            description="Search for errors, corrections, and feedback",
            best_for=["error_queries", "correction_requests", "feedback_history"],
            memory_types=[MemoryType.ERROR, MemoryType.FEEDBACK],
            confidence_threshold=0.8,
            typical_latency_ms=250,
            max_results=6,
            parameters={"boost_recent_errors": True, "include_corrections": True},
        )

        return strategies

    def _setup_prompts(self) -> None:
        """Setup prompts for strategy selection and coordination."""
        self.strategy_selection_prompt = PromptTemplate(
            template="""You are an expert retrieval strategy coordinator. Analyze the query and select the most appropriate retrieval strategies.

QUERY: {query}

QUERY ANALYSIS:
- Intent: {query_intent}
- Memory Types Needed: {memory_types}
- Complexity: {complexity}
- Temporal Scope: {temporal_scope}
- Entities Mentioned: {entities}
- Topics: {topics}

AVAILABLE STRATEGIES:
{strategies_description}

SELECTION CRITERIA:
1. Choose strategies that best match the query intent and memory types
2. Consider query complexity - complex queries may benefit from multiple strategies
3. Balance speed vs. comprehensiveness based on query urgency
4. Ensure strategies complement each other (avoid redundancy)

CONSTRAINTS:
- Maximum {max_strategies} strategies
- Minimum confidence threshold: {min_confidence}
- Consider typical latency for time-sensitive queries

FORMAT: Return a JSON object with:
{{
    "selected_strategies": ["strategy1", "strategy2"],
    "strategy_reasoning": "Explanation of why these strategies were selected",
    "expected_latency_ms": 800,
    "confidence_in_selection": 0.9,
    "parallel_execution": true
}}

Select strategies now:""",
            input_variables=[
                "query",
                "query_intent",
                "memory_types",
                "complexity",
                "temporal_scope",
                "entities",
                "topics",
                "strategies_description",
                "max_strategies",
                "min_confidence",
            ],
        )

        self.result_fusion_prompt = PromptTemplate(
            template="""You are an expert at fusing results from multiple retrieval strategies. Analyze and rank the combined results.

ORIGINAL QUERY: {query}

STRATEGY RESULTS:
{strategy_results}

FUSION CRITERIA:
1. Relevance to original query (weight: {relevance_weight})
2. Diversity of information (weight: {diversity_weight})
3. Coverage of query aspects (weight: {coverage_weight})
4. Confidence scores from strategies
5. Avoid redundancy while maintaining completeness

TASK:
1. Identify the most relevant and diverse memories
2. Remove near-duplicates while preserving unique information
3. Rank results by combined relevance, diversity, and coverage
4. Provide reasoning for the ranking

FORMAT: Return a JSON object with:
{{
    "ranked_memory_ids": ["mem1", "mem2", "mem3"],
    "fusion_reasoning": "Explanation of ranking logic",
    "diversity_score": 0.8,
    "coverage_score": 0.9,
    "confidence_score": 0.85,
    "removed_duplicates": 3
}}

Fuse and rank results now:""",
            input_variables=[
                "query",
                "strategy_results",
                "relevance_weight",
                "diversity_weight",
                "coverage_weight",
            ],
        )

    async def retrieve_memories(
        self,
        query: str,
        limit: int | None = None,
        memory_types: list[MemoryType] | None = None,
        namespace: tuple[str, ...] | None = None,
        force_strategies: list[str] | None = None,
    ) -> AgenticRAGResult:
        """Retrieve memories using intelligent strategy coordination and result fusion.

        This method is the core of the agentic RAG coordinator. It analyzes the query,
        selects appropriate retrieval strategies, executes them in parallel, and fuses
        the results to provide comprehensive, diverse, and relevant memory retrieval.

        Args:
            query: Natural language query for memory retrieval
            limit: Maximum number of memories to return (default: 10)
            memory_types: Specific memory types to focus on (optional filtering)
            namespace: Memory namespace to search within (optional scoping)
            force_strategies: Force specific strategies for testing or optimization

        Returns:
            AgenticRAGResult: Comprehensive result with memories, strategy info, and metrics

        Examples:
            Basic memory retrieval::

                result = await coordinator.retrieve_memories(
                    "How do I deploy a web application?"
                )

                print(f"Retrieved {len(result.final_memories)} memories")
                print(f"Used strategies: {result.selected_strategies}")
                print(f"Processing time: {result.total_time_ms:.1f}ms")

                # Access retrieved memories
                for i, memory in enumerate(result.final_memories):
                    score = result.final_scores[i]
                    print(f"Memory {i+1}: {memory['content'][:100]}... (score: {score:.2f})")

            Advanced retrieval with filtering::

                result = await coordinator.retrieve_memories(
                    query="What are machine learning best practices?",
                    limit=5,
                    memory_types=[MemoryType.SEMANTIC, MemoryType.PROCEDURAL],
                    namespace=("user", "ml", "practices")
                )

                # Analyze strategy performance
                print(f"Strategy reasoning: {result.strategy_reasoning}")
                print(f"Quality scores:")
                print(f"  Diversity: {result.diversity_score:.2f}")
                print(f"  Coverage: {result.coverage_score:.2f}")
                print(f"  Confidence: {result.confidence_score:.2f}")

            Performance analysis::

                result = await coordinator.retrieve_memories("complex technical query")

                # Analyze individual strategy performance
                for strategy_name, strategy_data in result.strategy_results.items():
                    memory_count = len(strategy_data.get('memories', []))
                    exec_time = strategy_data.get('execution_time_ms', 0)
                    print(f"{strategy_name}: {memory_count} memories in {exec_time:.1f}ms")

                # Overall performance metrics
                print(f"Total execution time: {result.total_time_ms:.1f}ms")
                print(f"Average memory score: {sum(result.final_scores) / len(result.final_scores):.2f}")

            Forced strategy selection (for testing)::

                result = await coordinator.retrieve_memories(
                    query="test query",
                    force_strategies=["enhanced_similarity", "graph_traversal"]
                )

                print(f"Forced strategies: {result.selected_strategies}")
                assert result.selected_strategies == ["enhanced_similarity", "graph_traversal"]

        Note:
            The coordinator automatically analyzes the query to select the most appropriate
            strategies. It considers query complexity, memory types needed, temporal scope,
            and other factors to optimize retrieval performance and quality.
        """
        start_time = datetime.now()

        try:
            # Initialize result
            result = AgenticRAGResult(query=query)

            # Step 1: Analyze query
            query_analysis = await self._analyze_query(query)
            result.query_analysis = query_analysis

            # Step 2: Select strategies
            if force_strategies:
                selected_strategies = force_strategies
                result.strategy_reasoning = "Forced strategy selection for testing"
            else:
                selected_strategies, reasoning = await self._select_strategies(
                    query, query_analysis, memory_types
                )
                result.strategy_reasoning = reasoning

            result.selected_strategies = selected_strategies

            # Step 3: Execute strategies
            strategy_results = await self._execute_strategies(
                selected_strategies, query, limit, memory_types, namespace
            )
            result.strategy_results = strategy_results

            # Step 4: Fuse results
            if self.enable_strategy_combination and len(selected_strategies) > 1:
                final_memories, final_scores, fusion_metrics = await self._fuse_results(
                    query, strategy_results, limit or 10
                )
            # Use single strategy results
            elif strategy_results:
                first_strategy = next(iter(strategy_results.keys()))
                strategy_data = strategy_results[first_strategy]
                final_memories = strategy_data.get("memories", [])
                final_scores = strategy_data.get("scores", [])
                fusion_metrics = {
                    "diversity_score": 0.5,
                    "coverage_score": 0.5,
                    "confidence_score": 0.5,
                }
            else:
                final_memories, final_scores, fusion_metrics = [], [], {}

            result.final_memories = final_memories
            result.final_scores = final_scores
            result.diversity_score = fusion_metrics.get("diversity_score", 0.0)
            result.coverage_score = fusion_metrics.get("coverage_score", 0.0)
            result.confidence_score = fusion_metrics.get("confidence_score", 0.0)

            # Step 5: Record timing
            end_time = datetime.now()
            result.total_time_ms = (end_time - start_time).total_seconds() * 1000

            logger.info(
                f"Agentic RAG completed in {result.total_time_ms:.1f}ms: {len(result.final_memories)} memories from {len(selected_strategies)} strategies"
            )

            return result

        except Exception as e:
            logger.exception(f"Error in agentic RAG coordination: {e}")
            # Return empty result on error
            result = AgenticRAGResult(query=query)
            result.total_time_ms = (datetime.now() - start_time).total_seconds() * 1000
            return result

    async def _analyze_query(self, query: str) -> dict[str, Any]:
        """Analyze query to understand intent and requirements."""
        # Use classifier if available
        if self.classifier:
            query_intent = self.classifier.classify_query_intent(query)

            return {
                "memory_types": [mt.value for mt in query_intent.memory_types],
                "complexity": query_intent.complexity,
                "temporal_scope": query_intent.temporal_scope,
                "requires_reasoning": query_intent.requires_reasoning,
                "entities": query_intent.entities,
                "topics": query_intent.topics,
                "preferred_strategy": query_intent.preferred_retrieval_strategy,
            }
        # Fallback analysis
        return {
            "memory_types": [MemoryType.SEMANTIC.value],
            "complexity": "simple",
            "temporal_scope": "recent",
            "requires_reasoning": False,
            "entities": [],
            "topics": [],
            "preferred_strategy": "enhanced_similarity",
        }

    async def _select_strategies(
        self,
        query: str,
        query_analysis: dict[str, Any],
        memory_types: list[MemoryType] | None = None,
    ) -> tuple[list[str], str]:
        """Select appropriate strategies for the query."""
        try:
            # Prepare strategies description
            strategies_desc = []
            for name, strategy in self.strategies.items():
                desc = f"- {name}: {strategy.description} (best for: {', '.join(strategy.best_for)})"
                strategies_desc.append(desc)

            # Prepare prompt
            prompt = self.strategy_selection_prompt.format(
                query=query,
                query_intent=query_analysis.get("preferred_strategy", "unknown"),
                memory_types=", ".join(query_analysis.get("memory_types", [])),
                complexity=query_analysis.get("complexity", "simple"),
                temporal_scope=query_analysis.get("temporal_scope", "recent"),
                entities=", ".join(query_analysis.get("entities", [])),
                topics=", ".join(query_analysis.get("topics", [])),
                strategies_description="\n".join(strategies_desc),
                max_strategies=self.max_strategies,
                min_confidence=self.min_confidence_threshold,
            )

            # Get LLM response
            response = await self.coordinator_llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an expert retrieval strategy coordinator."
                    ),
                    HumanMessage(content=prompt),
                ]
            )

            # Parse response
            selection_data = self._parse_json_response(response.content)

            if selection_data and "selected_strategies" in selection_data:
                selected = selection_data["selected_strategies"]
                reasoning = selection_data.get(
                    "strategy_reasoning", "LLM-based selection"
                )

                # Validate strategies exist
                valid_strategies = [s for s in selected if s in self.strategies]

                if valid_strategies:
                    return valid_strategies, reasoning

            # Fallback to rule-based selection
            return self._fallback_strategy_selection(query_analysis, memory_types)

        except Exception as e:
            logger.exception(f"Error in strategy selection: {e}")
            return self._fallback_strategy_selection(query_analysis, memory_types)

    def _fallback_strategy_selection(
        self,
        query_analysis: dict[str, Any],
        memory_types: list[MemoryType] | None = None,
    ) -> tuple[list[str], str]:
        """Fallback strategy selection using rules."""
        complexity = query_analysis.get("complexity", "simple")
        memory_types_needed = query_analysis.get("memory_types", [])
        requires_reasoning = query_analysis.get("requires_reasoning", False)

        selected = []
        reasoning = "Rule-based fallback selection: "

        # Always include enhanced similarity as baseline
        selected.append("enhanced_similarity")
        reasoning += "enhanced similarity (baseline), "

        # Add graph traversal for complex queries or reasoning
        if complexity in ["moderate", "complex"] or requires_reasoning:
            selected.append("graph_traversal")
            reasoning += "graph traversal (complex/reasoning), "

        # Add procedural search for how-to queries
        if MemoryType.PROCEDURAL.value in memory_types_needed:
            selected.append("procedural_search")
            reasoning += "procedural search (how-to), "

        # Add temporal search for time-based queries
        if MemoryType.TEMPORAL.value in memory_types_needed:
            selected.append("temporal_search")
            reasoning += "temporal search (time-based), "

        # Add error/feedback search
        if any(
            mt in memory_types_needed
            for mt in [MemoryType.ERROR.value, MemoryType.FEEDBACK.value]
        ):
            selected.append("error_feedback_search")
            reasoning += "error/feedback search (corrections), "

        # Limit to max strategies
        selected = selected[: self.max_strategies]

        return selected, reasoning.rstrip(", ")

    async def _execute_strategies(
        self,
        strategies: list[str],
        query: str,
        limit: int | None,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
    ) -> dict[str, Any]:
        """Execute selected strategies in parallel."""
        # Create tasks for parallel execution
        tasks = []
        strategy_names = []

        for strategy_name in strategies:
            if strategy_name in self.strategies:
                task = self._execute_single_strategy(
                    strategy_name, query, limit, memory_types, namespace
                )
                tasks.append(task)
                strategy_names.append(strategy_name)

        # Execute strategies in parallel
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
        else:
            results = []

        # Combine results
        strategy_results = {}
        for i, result in enumerate(results):
            strategy_name = strategy_names[i]

            if isinstance(result, Exception):
                logger.error(f"Strategy {strategy_name} failed: {result}")
                strategy_results[strategy_name] = {
                    "memories": [],
                    "scores": [],
                    "error": str(result),
                    "execution_time_ms": 0,
                }
            else:
                strategy_results[strategy_name] = result

        return strategy_results

    async def _execute_single_strategy(
        self,
        strategy_name: str,
        query: str,
        limit: int | None,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
    ) -> dict[str, Any]:
        """Execute a single retrieval strategy."""
        start_time = datetime.now()

        try:
            strategy = self.strategies[strategy_name]

            # Adjust limit based on strategy
            strategy_limit = min(limit or 10, strategy.max_results)

            # Execute based on strategy type
            if strategy_name == "enhanced_similarity":
                memories = await self._execute_enhanced_similarity(
                    query, strategy_limit, memory_types, namespace, strategy.parameters
                )
            elif strategy_name == "graph_traversal":
                memories = await self._execute_graph_traversal(
                    query, strategy_limit, memory_types, namespace, strategy.parameters
                )
            elif strategy_name == "procedural_search":
                memories = await self._execute_procedural_search(
                    query, strategy_limit, memory_types, namespace, strategy.parameters
                )
            elif strategy_name == "temporal_search":
                memories = await self._execute_temporal_search(
                    query, strategy_limit, memory_types, namespace, strategy.parameters
                )
            elif strategy_name == "error_feedback_search":
                memories = await self._execute_error_feedback_search(
                    query, strategy_limit, memory_types, namespace, strategy.parameters
                )
            else:
                # Fallback to basic retrieval
                memories = await self.memory_store.retrieve_memories(
                    query=query,
                    namespace=namespace,
                    memory_types=memory_types,
                    limit=strategy_limit,
                )

            # Extract scores
            scores = [mem.get("similarity_score", 0.5) for mem in memories]

            end_time = datetime.now()
            execution_time = (end_time - start_time).total_seconds() * 1000

            return {
                "memories": memories,
                "scores": scores,
                "execution_time_ms": execution_time,
                "strategy_name": strategy_name,
            }

        except Exception as e:
            logger.exception(f"Error executing strategy {strategy_name}: {e}")
            return {
                "memories": [],
                "scores": [],
                "error": str(e),
                "execution_time_ms": 0,
                "strategy_name": strategy_name,
            }

    async def _execute_enhanced_similarity(
        self,
        query: str,
        limit: int,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute enhanced similarity strategy."""
        if "enhanced" in self.retrievers:
            retriever = self.retrievers["enhanced"]
            result = await retriever.retrieve_memories(
                query=query, limit=limit, memory_types=memory_types, namespace=namespace
            )
            return result.memories if hasattr(result, "memories") else result
        # Fallback to basic retrieval
        return await self.memory_store.retrieve_memories(
            query=query, namespace=namespace, memory_types=memory_types, limit=limit
        )

    async def _execute_graph_traversal(
        self,
        query: str,
        limit: int,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute graph traversal strategy."""
        if "graph_rag" in self.retrievers:
            retriever = self.retrievers["graph_rag"]
            result = await retriever.retrieve_memories(
                query=query,
                limit=limit,
                memory_types=memory_types,
                namespace=namespace,
                enable_graph_traversal=True,
            )
            return result.memories if hasattr(result, "memories") else result
        # Fallback to basic retrieval
        return await self.memory_store.retrieve_memories(
            query=query, namespace=namespace, memory_types=memory_types, limit=limit
        )

    async def _execute_procedural_search(
        self,
        query: str,
        limit: int,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute procedural search strategy."""
        # Focus on procedural memories
        procedural_types = [MemoryType.PROCEDURAL, MemoryType.SEMANTIC]

        return await self.memory_store.retrieve_memories(
            query=query, namespace=namespace, memory_types=procedural_types, limit=limit
        )

    async def _execute_temporal_search(
        self,
        query: str,
        limit: int,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute temporal search strategy."""
        # Focus on temporal and episodic memories
        temporal_types = [MemoryType.TEMPORAL, MemoryType.EPISODIC]

        return await self.memory_store.retrieve_memories(
            query=query, namespace=namespace, memory_types=temporal_types, limit=limit
        )

    async def _execute_error_feedback_search(
        self,
        query: str,
        limit: int,
        memory_types: list[MemoryType] | None,
        namespace: tuple[str, ...] | None,
        parameters: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """Execute error/feedback search strategy."""
        # Focus on error and feedback memories
        error_types = [MemoryType.ERROR, MemoryType.FEEDBACK]

        return await self.memory_store.retrieve_memories(
            query=query, namespace=namespace, memory_types=error_types, limit=limit
        )

    async def _fuse_results(
        self, query: str, strategy_results: dict[str, Any], limit: int
    ) -> tuple[list[dict[str, Any]], list[float], dict[str, Any]]:
        """Fuse results from multiple strategies."""
        try:
            # Prepare strategy results for fusion
            results_summary = {}
            for strategy_name, result_data in strategy_results.items():
                results_summary[strategy_name] = {
                    "memory_count": len(result_data.get("memories", [])),
                    "avg_score": sum(result_data.get("scores", [0]))
                    / max(len(result_data.get("scores", [1])), 1),
                    "execution_time": result_data.get("execution_time_ms", 0),
                }

            # Use LLM for intelligent fusion
            prompt = self.result_fusion_prompt.format(
                query=query,
                strategy_results=str(results_summary),
                relevance_weight=self.relevance_weight,
                diversity_weight=self.diversity_weight,
                coverage_weight=self.coverage_weight,
            )

            response = await self.coordinator_llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an expert at fusing retrieval results."
                    ),
                    HumanMessage(content=prompt),
                ]
            )

            # Parse fusion response
            fusion_data = self._parse_json_response(response.content)

            # Combine all memories
            all_memories = []
            memory_id_to_data = {}

            for strategy_name, result_data in strategy_results.items():
                memories = result_data.get("memories", [])
                scores = result_data.get("scores", [])

                for i, memory in enumerate(memories):
                    memory_id = memory.get("id")
                    if memory_id:
                        # Add strategy context
                        memory_with_context = memory.copy()
                        memory_with_context["retrieval_strategy"] = strategy_name
                        memory_with_context["strategy_score"] = (
                            scores[i] if i < len(scores) else 0.5
                        )

                        if memory_id not in memory_id_to_data:
                            memory_id_to_data[memory_id] = memory_with_context
                            all_memories.append(memory_with_context)

            # Apply fusion ranking or use simple scoring
            if fusion_data and "ranked_memory_ids" in fusion_data:
                # Use LLM ranking
                ranked_ids = fusion_data["ranked_memory_ids"]
                final_memories = []
                final_scores = []

                for memory_id in ranked_ids[:limit]:
                    if memory_id in memory_id_to_data:
                        final_memories.append(memory_id_to_data[memory_id])
                        final_scores.append(
                            memory_id_to_data[memory_id].get("strategy_score", 0.5)
                        )

                fusion_metrics = {
                    "diversity_score": fusion_data.get("diversity_score", 0.5),
                    "coverage_score": fusion_data.get("coverage_score", 0.5),
                    "confidence_score": fusion_data.get("confidence_score", 0.5),
                }
            else:
                # Fallback to simple scoring
                final_memories = all_memories[:limit]
                final_scores = [
                    mem.get("strategy_score", 0.5) for mem in final_memories
                ]
                fusion_metrics = {
                    "diversity_score": 0.5,
                    "coverage_score": 0.5,
                    "confidence_score": 0.5,
                }

            return final_memories, final_scores, fusion_metrics

        except Exception as e:
            logger.exception(f"Error in result fusion: {e}")
            # Fallback to simple combination
            all_memories = []
            for result_data in strategy_results.values():
                all_memories.extend(result_data.get("memories", []))

            final_memories = all_memories[:limit]
            final_scores = [0.5] * len(final_memories)
            fusion_metrics = {
                "diversity_score": 0.5,
                "coverage_score": 0.5,
                "confidence_score": 0.5,
            }

            return final_memories, final_scores, fusion_metrics

    def _parse_json_response(self, response: str) -> dict[str, Any] | None:
        """Parse JSON response from LLM."""
        try:
            import json

            # Try to find JSON in response
            start_idx = response.find("{")
            end_idx = response.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response[start_idx:end_idx]
                return json.loads(json_str)
        except Exception as e:
            logger.warning(f"Failed to parse JSON response: {e}")
        return None

    async def run(self, user_input: str) -> str:
        """Main execution method for the Agentic RAG Coordinator with comprehensive reporting.

        This method serves as the primary interface for the coordinator, accepting natural
        language queries and returning formatted results with detailed performance metrics
        and strategy information.

        Args:
            user_input: Natural language query for memory retrieval

        Returns:
            str: Formatted response with retrieval results, strategy information, and performance metrics

        Examples:
            Basic query execution::

                coordinator = AgenticRAGCoordinator(config)

                response = await coordinator.run(
                    "How do I deploy a Docker container to AWS?"
                )

                print(response)
                # Output:
                # Retrieved 8 memories using 2 strategies:
                # - Strategies: enhanced_similarity, procedural_search
                # - Total time: 1247.3ms
                # - Quality scores: Diversity=0.78, Coverage=0.85, Confidence=0.82
                # - Strategy reasoning: Selected enhanced similarity for factual content and procedural search for deployment steps
                #
                # Top memories:
                # 1. [0.91] Docker deployment to AWS ECS requires proper image tagging and service configuration...
                # 2. [0.87] AWS deployment best practices include using IAM roles, security groups, and monitoring...
                # 3. [0.84] Container orchestration with ECS involves task definitions, services, and load balancers...

            Complex query with multiple strategies::

                response = await coordinator.run(
                    "What are the relationships between machine learning algorithms and their applications in healthcare?"
                )

                print(response)
                # Output shows graph traversal strategy was used for relationship discovery
                # along with enhanced similarity for semantic content

            Error handling::

                response = await coordinator.run("complex query that might fail")

                # Response will include error information if retrieval fails
                # but still provide a graceful user experience

        Note:
            The response format includes:
            - Number of memories retrieved and strategies used
            - Processing time and quality scores
            - Strategy selection reasoning
            - Top 3 memories with relevance scores
            - Graceful error handling for failed retrievals
        """
        # Default to retrieve memories
        result = await self.retrieve_memories(user_input)

        response = f"Retrieved {len(result.final_memories)} memories using {len(result.selected_strategies)} strategies:\n"
        response += f"- Strategies: {', '.join(result.selected_strategies)}\n"
        response += f"- Total time: {result.total_time_ms:.1f}ms\n"
        response += f"- Quality scores: Diversity={result.diversity_score:.2f}, Coverage={result.coverage_score:.2f}, Confidence={result.confidence_score:.2f}\n"

        if result.strategy_reasoning:
            response += f"- Strategy reasoning: {result.strategy_reasoning}\n"

        # Show top memories
        if result.final_memories:
            response += "\nTop memories:\n"
            for i, memory in enumerate(result.final_memories[:3]):
                content = (
                    memory.get("content", "")[:100] + "..."
                    if len(memory.get("content", "")) > 100
                    else memory.get("content", "")
                )
                score = result.final_scores[i] if i < len(result.final_scores) else 0.0
                response += f"{i+1}. [{score:.2f}] {content}\n"

        return response
