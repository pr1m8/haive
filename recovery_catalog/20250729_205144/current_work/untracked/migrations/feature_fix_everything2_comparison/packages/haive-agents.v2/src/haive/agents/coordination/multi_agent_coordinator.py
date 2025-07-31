"""Multi-Agent Memory Coordinator using MetaStateSchema patterns.

This module provides a comprehensive coordinator that orchestrates multiple memory
agents using the MetaStateSchema pattern for proper state management and agent
composition.
"""

import asyncio
import logging
from datetime import datetime
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory.agentic_rag_coordinator import (
    AgenticRAGCoordinator,
    AgenticRAGCoordinatorConfig,
    Optional,
    from,
    import,
    typing,
)
from haive.agents.memory.core.classifier import MemoryClassifier
from haive.agents.memory.core.stores import MemoryStoreManager
from haive.agents.memory.core.types import MemoryType
from haive.agents.memory.kg_generator_agent import (
    KGGeneratorAgent,
    KGGeneratorAgentConfig,
)
from haive.agents.simple import SimpleAgent

logger = logging.getLogger(__name__)


class MemoryTask(BaseModel):
    """Represents a memory-related task for multi-agent coordination.

    A MemoryTask encapsulates a specific memory operation (store, retrieve, analyze, etc.)
    that can be executed by the multi-agent coordinator system. It contains all necessary
    information for task routing, execution, and result tracking.

    Attributes:
        id: Unique identifier for the task, used for tracking and coordination
        type: Type of memory operation (store, retrieve, analyze, generate_kg, etc.)
        query: Natural language description of the task or query content
        parameters: Dictionary of task-specific parameters and configuration
        priority: Task priority level (1=highest, 10=lowest) for execution ordering
        namespace: Memory namespace to operate within (e.g., ("user", "personal"))
        memory_types: Specific memory types to target (semantic, episodic, etc.)
        status: Current task status (pending, routing, executing, completed, failed)
        assigned_agent: Name of the agent assigned to execute this task
        result: Task execution result (populated after completion)
        error: Error message if task execution failed
        created_at: UTC timestamp when the task was created
        started_at: UTC timestamp when task execution started
        completed_at: UTC timestamp when task execution completed

    Examples:
        Creating a memory storage task::

            task = MemoryTask(
                id="store_001",
                type="store_memory",
                query="Store information about Python programming",
                parameters={"content": "Python is a programming language"},
                priority=3,
                namespace=("user", "learning")
            )

        Creating a retrieval task::

            task = MemoryTask(
                id="retrieve_001",
                type="retrieve_memories",
                query="Find information about machine learning",
                parameters={"limit": 10, "use_graph_rag": True},
                priority=1,
                memory_types=[MemoryType.SEMANTIC, MemoryType.EPISODIC]
            )

        Creating an analysis task::

            task = MemoryTask(
                id="analyze_001",
                type="analyze_memory",
                query="Analyze patterns in my learning history",
                parameters={"analysis_type": "pattern_detection"},
                priority=2
            )

        Creating a knowledge graph generation task::

            task = MemoryTask(
                id="kg_001",
                type="generate_knowledge_graph",
                query="Build knowledge graph from recent memories",
                parameters={"max_memories": 100, "confidence_threshold": 0.7},
                priority=4,
                namespace=("user", "work")
            )
    """

    id: str = Field(..., description="Unique task identifier")
    type: str = Field(...,
                      description="Task type (store, retrieve, analyze, etc.)")
    query: str = Field(..., description="Task query or description")

    # Task parameters
    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Task-specific parameters"
    )
    priority: int = Field(
        default=5,
        ge=1,
        le=10,
        description="Task priority (1=highest, 10=lowest)")

    # Execution context
    namespace: tuple[str, ...] | None = Field(
        default=None, description="Memory namespace"
    )
    memory_types: list[MemoryType] | None = Field(
        default=None, description="Target memory types"
    )

    # Task state
    status: str = Field(default="pending", description="Task status")
    assigned_agent: Optional[str] = Field(
        default=None, description="Assigned agent name")
    result: Optional[Any] = Field(default=None, description="Task result")
    error: Optional[str] = Field(
        default=None,
        description="Error message if failed")

    # Timing
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Task creation time"
    )
    started_at: Optional[datetime] = Field(
        default=None, description="Task start time")
    completed_at: Optional[datetime] = Field(
        default=None, description="Task completion time"
    )


class MemoryAgentCapabilities(BaseModel):
    """Describes the capabilities and characteristics of a memory agent.

    This model defines what a memory agent can do, its performance characteristics,
    and specializations. It's used by the multi-agent coordinator for intelligent
    task routing and load balancing.

    Attributes:
        agent_name: Unique identifier for the agent
        agent_type: Class or type name of the agent (e.g., "KGGeneratorAgent")
        can_store_memories: Whether the agent can store new memories
        can_retrieve_memories: Whether the agent can retrieve existing memories
        can_analyze_memories: Whether the agent can analyze memory content
        can_generate_knowledge_graph: Whether the agent can build knowledge graphs
        can_coordinate_retrieval: Whether the agent can coordinate retrieval strategies
        supported_memory_types: List of memory types the agent can handle
        typical_latency_ms: Expected response time in milliseconds
        max_concurrent_tasks: Maximum number of concurrent tasks the agent can handle
        specialization: List of agent specializations and strengths

    Examples:
        KG Generator Agent capabilities::

            kg_capabilities = MemoryAgentCapabilities(
                agent_name="kg_generator",
                agent_type="KGGeneratorAgent",
                can_analyze_memories=True,
                can_generate_knowledge_graph=True,
                supported_memory_types=[
                    MemoryType.SEMANTIC,
                    MemoryType.EPISODIC,
                    MemoryType.CONTEXTUAL
                ],
                typical_latency_ms=2000,
                max_concurrent_tasks=2,
                specialization=[
                    "entity_extraction",
                    "relationship_discovery",
                    "graph_construction"
                ]
            )

        Agentic RAG Coordinator capabilities::

            rag_capabilities = MemoryAgentCapabilities(
                agent_name="agentic_rag",
                agent_type="AgenticRAGCoordinator",
                can_retrieve_memories=True,
                can_coordinate_retrieval=True,
                supported_memory_types=list(MemoryType),  # Supports all types
                typical_latency_ms=1500,
                max_concurrent_tasks=3,
                specialization=[
                    "strategy_selection",
                    "result_fusion",
                    "intelligent_retrieval"
                ]
            )

        Memory Store Agent capabilities::

            store_capabilities = MemoryAgentCapabilities(
                agent_name="memory_store",
                agent_type="MemoryStoreAgent",
                can_store_memories=True,
                can_retrieve_memories=True,
                supported_memory_types=list(MemoryType),
                typical_latency_ms=500,
                max_concurrent_tasks=5,
                specialization=[
                    "memory_storage",
                    "basic_retrieval",
                    "memory_management"
                ]
            )
    """

    agent_name: str = Field(..., description="Agent name")
    agent_type: str = Field(..., description="Agent type/class")

    # Capabilities
    can_store_memories: bool = Field(
        default=False, description="Can store memories")
    can_retrieve_memories: bool = Field(
        default=False, description="Can retrieve memories"
    )
    can_analyze_memories: bool = Field(
        default=False, description="Can analyze memories"
    )
    can_generate_knowledge_graph: bool = Field(
        default=False, description="Can generate knowledge graphs"
    )
    can_coordinate_retrieval: bool = Field(
        default=False, description="Can coordinate retrieval strategies"
    )

    # Supported memory types
    supported_memory_types: list[MemoryType] = Field(
        default_factory=list, description="Supported memory types"
    )

    # Performance characteristics
    typical_latency_ms: float = Field(
        default=1000, description="Typical response latency"
    )
    max_concurrent_tasks: int = Field(
        default=1, description="Maximum concurrent tasks")

    # Specialization
    specialization: list[str] = Field(
        default_factory=list, description="Agent specializations"
    )


class MultiAgentCoordinatorConfig(BaseModel):
    """Configuration for Multi-Agent Memory Coordinator.

    This configuration class defines all parameters needed to create and configure
    a MultiAgentMemoryCoordinator, including agent configurations, coordination settings,
    and performance parameters.

    Attributes:
        name: Unique identifier for the coordinator instance
        memory_store_manager: Manager for memory storage and retrieval operations
        memory_classifier: Classifier for analyzing memory content and types
        kg_generator_config: Configuration for the knowledge graph generator agent
        agentic_rag_config: Configuration for the agentic RAG coordinator agent
        max_concurrent_tasks: Maximum number of tasks that can execute simultaneously
        task_timeout_seconds: Maximum time (in seconds) a task can run before timing out
        enable_agent_communication: Whether to enable communication between agents
        coordinator_llm: LLM configuration for the coordinator's decision-making
        routing_strategy: Strategy for routing tasks to agents (capability_based, load_balanced, etc.)
        enable_task_decomposition: Whether to enable breaking complex tasks into subtasks
        enable_caching: Whether to enable result caching for performance
        cache_ttl_seconds: Time-to-live for cached results in seconds
        persistence: Persistence configuration passed to sub-agents

    Examples:
        Basic configuration::

            config = MultiAgentCoordinatorConfig(
                name="my_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                kg_generator_config=kg_config,
                agentic_rag_config=rag_config,
                max_concurrent_tasks=3,
                task_timeout_seconds=180
            )

        Advanced configuration with custom settings::

            config = MultiAgentCoordinatorConfig(
                name="advanced_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                kg_generator_config=kg_config,
                agentic_rag_config=rag_config,

                # Coordination settings
                max_concurrent_tasks=10,
                task_timeout_seconds=600,
                enable_agent_communication=True,

                # Coordinator LLM
                coordinator_llm=AugLLMConfig(
                    model="gpt-4",
                    temperature=0.2,
                    max_tokens=1000
                ),

                # Task routing
                routing_strategy="capability_based",
                enable_task_decomposition=True,

                # Performance
                enable_caching=True,
                cache_ttl_seconds=7200,  # 2 hours

                # Persistence
                persistence=False  # Disable for testing
            )

        Production configuration::

            config = MultiAgentCoordinatorConfig(
                name="production_coordinator",
                memory_store_manager=store_manager,
                memory_classifier=classifier,
                kg_generator_config=kg_config,
                agentic_rag_config=rag_config,

                # High-performance settings
                max_concurrent_tasks=20,
                task_timeout_seconds=900,
                enable_agent_communication=True,

                # Optimized coordinator
                coordinator_llm=AugLLMConfig(
                    model="gpt-4-turbo",
                    temperature=0.1,
                    max_tokens=2000
                ),

                # Advanced routing
                routing_strategy="load_balanced",
                enable_task_decomposition=True,

                # Production caching
                enable_caching=True,
                cache_ttl_seconds=3600
            )
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core configuration
    name: str = Field(
        default="multi_agent_coordinator",
        description="Coordinator name")
    memory_store_manager: MemoryStoreManager = Field(
        ..., description="Memory store manager"
    )
    memory_classifier: MemoryClassifier = Field(
        ..., description="Memory classifier")

    # Agent configurations
    kg_generator_config: KGGeneratorAgentConfig = Field(
        ..., description="KG generator configuration"
    )
    agentic_rag_config: AgenticRAGCoordinatorConfig = Field(
        ..., description="Agentic RAG configuration"
    )

    # Coordination configuration
    max_concurrent_tasks: int = Field(
        default=5, description="Maximum concurrent tasks")
    task_timeout_seconds: int = Field(
        default=300, description="Task timeout in seconds"
    )
    enable_agent_communication: bool = Field(
        default=True, description="Enable inter-agent communication"
    )

    # LLM configuration
    coordinator_llm: AugLLMConfig = Field(
        default_factory=AugLLMConfig, description="Coordinator LLM"
    )

    # Task routing configuration
    routing_strategy: str = Field(
        default="capability_based", description="Task routing strategy"
    )
    enable_task_decomposition: bool = Field(
        default=True, description="Enable complex task decomposition"
    )

    # Performance configuration
    enable_caching: bool = Field(
        default=True,
        description="Enable result caching")
    cache_ttl_seconds: int = Field(
        default=3600, description="Cache TTL in seconds")

    # Persistence configuration
    persistence: Any = Field(
        default=None, description="Persistence configuration for agents"
    )


class MultiAgentMemoryCoordinator:
    """Orchestrates multiple memory agents using MetaStateSchema patterns.

    The MultiAgentMemoryCoordinator is the central orchestrator for the memory system,
    managing a collection of specialized memory agents and intelligently routing tasks
    based on agent capabilities, performance characteristics, and current load.

    This coordinator provides:
    - Intelligent task routing based on agent capabilities
    - Load balancing across multiple agents
    - Task decomposition for complex operations
    - Performance monitoring and optimization
    - Fault tolerance and error handling
    - Agent communication and coordination

    Attributes:
        config: Configuration object containing all coordinator settings
        memory_store: Memory store manager for direct storage operations
        classifier: Memory classifier for content analysis
        coordinator_llm: LLM runnable for coordinator decision-making
        meta_agents: Dictionary of agents wrapped in MetaStateSchema
        agent_capabilities: Dictionary mapping agent names to their capabilities
        task_queue: List of pending tasks waiting for execution
        active_tasks: Dictionary of currently executing tasks
        completed_tasks: Dictionary of completed tasks with results
        performance_metrics: Dictionary tracking system performance metrics

    Examples:
        Basic coordinator usage::

            # Create coordinator
            coordinator = MultiAgentMemoryCoordinator(config)

            # Store memory
            result = await coordinator.store_memory(
                "I learned about machine learning algorithms today"
            )

            # Retrieve memories
            memories = await coordinator.retrieve_memories(
                query="machine learning",
                limit=5
            )

            # Analyze memory content
            analysis = await coordinator.analyze_memory(
                "Complex analysis of learning patterns"
            )

        Advanced task execution::

            # Create custom task
            task = MemoryTask(
                id="complex_analysis",
                type="analyze_and_graph",
                query="Analyze learning patterns and build knowledge graph",
                parameters={
                    "analysis_depth": "comprehensive",
                    "graph_confidence": 0.8
                },
                priority=1
            )

            # Execute task
            result = await coordinator.execute_task(task)

            # Check task status
            if result.status == "completed":
                print(f"Task completed: {result.result}")
            else:
                print(f"Task failed: {result.error}")

        System monitoring::

            # Get system status
            status = coordinator.get_system_status()
            print(f"Total agents: {status['total_agents']}")
            print(f"Active tasks: {status['active_tasks']}")

            # Run diagnostic
            diagnostic = await coordinator.run_diagnostic()
            if diagnostic["system_status"] == "healthy":
                print("System is healthy")
            else:
                print("System issues detected")

        Performance monitoring::

            # Get performance metrics
            metrics = coordinator.performance_metrics
            print(f"Total tasks: {metrics['total_tasks']}")
            print(f"Success rate: {metrics['successful_tasks'] / metrics['total_tasks'] * 100:.1f}%")
            print(f"Average latency: {metrics['avg_latency_ms']:.1f}ms")
    """

    def __init__(self, config: MultiAgentCoordinatorConfig) -> None:
        """Initialize the multi-agent coordinator.

        Sets up the coordinator with the provided configuration, initializes
        all managed agents, and prepares the task management system.

        Args:
            config: MultiAgentCoordinatorConfig containing all coordinator settings

        Examples:
            Basic initialization::

                config = MultiAgentCoordinatorConfig(
                    memory_store_manager=store_manager,
                    memory_classifier=classifier,
                    kg_generator_config=kg_config,
                    agentic_rag_config=rag_config
                )

                coordinator = MultiAgentMemoryCoordinator(config)

            Advanced initialization with custom settings::

                config = MultiAgentCoordinatorConfig(
                    name="production_coordinator",
                    memory_store_manager=store_manager,
                    memory_classifier=classifier,
                    kg_generator_config=kg_config,
                    agentic_rag_config=rag_config,
                    max_concurrent_tasks=10,
                    task_timeout_seconds=600,
                    enable_caching=True
                )

                coordinator = MultiAgentMemoryCoordinator(config)
        """
        self.config = config
        self.memory_store = config.memory_store_manager
        self.classifier = config.memory_classifier

        # Setup coordinator LLM
        self.coordinator_llm = config.coordinator_llm.create_runnable()

        # Initialize agents with MetaStateSchema
        self.meta_agents: dict[str, MetaStateSchema] = {}
        self.agent_capabilities: dict[str, MemoryAgentCapabilities] = {}

        # Task management
        self.task_queue: list[MemoryTask] = []
        self.active_tasks: dict[str, MemoryTask] = {}
        self.completed_tasks: dict[str, MemoryTask] = {}

        # Performance tracking
        self.performance_metrics = {
            "total_tasks": 0,
            "successful_tasks": 0,
            "failed_tasks": 0,
            "avg_latency_ms": 0.0,
            "agent_utilization": {},
        }

        # Setup agents
        self._setup_agents()

        # Setup prompts
        self._setup_prompts()

    def _setup_agents(self) -> None:
        """Setup and wrap agents with MetaStateSchema.
        """
        # 1. KG Generator Agent
        kg_agent = KGGeneratorAgent(self.config.kg_generator_config)
        # Set persistence if configured
        if hasattr(
                self.config,
                "persistence") and self.config.persistence is not None:
            kg_agent.persistence = self.config.persistence
        kg_meta_state = MetaStateSchema.from_agent(
            agent=kg_agent,
            initial_state={"ready": True, "kg_ready": False},
            graph_context={"agent_type": "kg_generator"},
        )
        self.meta_agents["kg_generator"] = kg_meta_state

        self.agent_capabilities["kg_generator"] = MemoryAgentCapabilities(
            agent_name="kg_generator",
            agent_type="KGGeneratorAgent",
            can_analyze_memories=True,
            can_generate_knowledge_graph=True,
            supported_memory_types=[
                MemoryType.SEMANTIC,
                MemoryType.EPISODIC,
                MemoryType.CONTEXTUAL,
            ],
            typical_latency_ms=2000,
            specialization=[
                "entity_extraction",
                "relationship_discovery",
                "graph_construction",
            ],
        )

        # 2. Agentic RAG Coordinator
        rag_coordinator = AgenticRAGCoordinator(self.config.agentic_rag_config)
        # Set persistence if configured
        if hasattr(
                self.config,
                "persistence") and self.config.persistence is not None:
            rag_coordinator.persistence = self.config.persistence
        rag_meta_state = MetaStateSchema.from_agent(
            agent=rag_coordinator,
            initial_state={"ready": True, "strategies_loaded": True},
            graph_context={"agent_type": "agentic_rag"},
        )
        self.meta_agents["agentic_rag"] = rag_meta_state

        self.agent_capabilities["agentic_rag"] = MemoryAgentCapabilities(
            agent_name="agentic_rag",
            agent_type="AgenticRAGCoordinator",
            can_retrieve_memories=True,
            can_coordinate_retrieval=True,
            supported_memory_types=list(MemoryType),
            typical_latency_ms=1500,
            max_concurrent_tasks=3,
            specialization=[
                "strategy_selection",
                "result_fusion",
                "intelligent_retrieval",
            ],
        )

        # 3. Memory Store Manager (wrapped as agent)
        store_meta_state = MetaStateSchema.from_agent(
            agent=self._create_store_agent(),
            initial_state={"ready": True, "store_connected": True},
            graph_context={"agent_type": "memory_store"},
        )
        self.meta_agents["memory_store"] = store_meta_state

        self.agent_capabilities["memory_store"] = MemoryAgentCapabilities(
            agent_name="memory_store",
            agent_type="MemoryStoreAgent",
            can_store_memories=True,
            can_retrieve_memories=True,
            supported_memory_types=list(MemoryType),
            typical_latency_ms=500,
            max_concurrent_tasks=5,
            specialization=[
                "memory_storage",
                "basic_retrieval",
                "memory_management"],
        )

        # 4. Memory Classifier (wrapped as agent)
        classifier_meta_state = MetaStateSchema.from_agent(
            agent=self._create_classifier_agent(),
            initial_state={"ready": True, "models_loaded": True},
            graph_context={"agent_type": "memory_classifier"},
        )
        self.meta_agents["memory_classifier"] = classifier_meta_state

        self.agent_capabilities["memory_classifier"] = MemoryAgentCapabilities(
            agent_name="memory_classifier",
            agent_type="MemoryClassifierAgent",
            can_analyze_memories=True,
            supported_memory_types=list(MemoryType),
            typical_latency_ms=800,
            max_concurrent_tasks=3,
            specialization=[
                "memory_classification",
                "intent_analysis",
                "metadata_extraction",
            ],
        )

    def _create_store_agent(self) -> SimpleAgent:
        """Create a simple agent wrapper for memory store operations.
        """
        # Create a simple agent that wraps store operations
        store_agent = SimpleAgent(
            name="memory_store_agent",
            engine=AugLLMConfig(temperature=0.1),
            system_message="""You are a memory store agent. You help users store and retrieve memories.

Available operations:
- Store new memories with automatic classification
- Retrieve memories based on queries
- Update existing memories
- Delete memories
- Get memory statistics

Always provide clear, helpful responses about memory operations.""",
            # Pass persistence settings from config if available
            persistence=getattr(self.config, "persistence", None),
        )

        return store_agent

    def _create_classifier_agent(self) -> SimpleAgent:
        """Create a simple agent wrapper for memory classification.
        """
        classifier_agent = SimpleAgent(
            name="memory_classifier_agent",
            engine=AugLLMConfig(temperature=0.1),
            system_message="""You are a memory classification agent. You analyze and classify memories.

Available operations:
- Classify memory content into types
- Analyze query intent
- Extract entities and topics
- Assess memory importance
- Provide classification reasoning

Always provide detailed analysis and classification results.""",
            # Pass persistence settings from config if available
            persistence=getattr(self.config, "persistence", None),
        )

        return classifier_agent

    def _setup_prompts(self) -> None:
        """Setup prompts for task routing and coordination.
        """
        self.task_routing_prompt = PromptTemplate(
            template="""You are an expert task router for a multi-agent memory system. Analyze the task and route it to the most appropriate agent.

TASK: {task_description}
TASK TYPE: {task_type}
PARAMETERS: {task_parameters}

AVAILABLE AGENTS:
{agent_capabilities}

ROUTING CRITERIA:
1. Agent capabilities must match task requirements
2. Consider agent specialization and performance
3. Balance load across agents
4. Prefer agents with relevant experience
5. Consider task complexity and urgency

TASK ROUTING OPTIONS:
- single_agent: Route to one agent
- multi_agent: Route to multiple agents (parallel)
- sequential: Route to agents in sequence
- decompose: Break task into subtasks

FORMAT: Return a JSON object with:
{{
    "routing_decision": "single_agent",
    "primary_agent": "agent_name",
    "secondary_agents": ["agent2", "agent3"],
    "execution_strategy": "parallel",
    "reasoning": "Why this routing was chosen",
    "estimated_time_ms": 1500,
    "confidence": 0.9
}}

Route the task now:""",
            input_variables=[
                "task_description",
                "task_type",
                "task_parameters",
                "agent_capabilities",
            ],
        )

        self.task_decomposition_prompt = PromptTemplate(
            template="""You are an expert at decomposing complex memory tasks into smaller, manageable subtasks.

COMPLEX TASK: {task_description}
TASK COMPLEXITY: {task_complexity}
AVAILABLE AGENTS: {available_agents}

DECOMPOSITION RULES:
1. Break down into 3-7 subtasks maximum
2. Each subtask should be assignable to a single agent
3. Define clear dependencies between subtasks
4. Ensure subtasks cover the full scope of the original task
5. Consider parallel execution opportunities

FORMAT: Return a JSON object with:
{{
    "subtasks": [
        {{
            "id": "subtask_1",
            "description": "Clear task description",
            "assigned_agent": "agent_name",
            "dependencies": ["subtask_0"],
            "priority": 1,
            "estimated_time_ms": 800
        }}
    ],
    "execution_plan": {{
        "parallel_groups": [["subtask_1", "subtask_2"], ["subtask_3"]],
        "total_estimated_time_ms": 2500
    }},
    "reasoning": "Why this decomposition was chosen"
}}

Decompose the task now:""", input_variables=[
                "task_description", "task_complexity", "available_agents"], )

    async def execute_task(self, task: MemoryTask) -> MemoryTask:
        """Execute a memory task using appropriate agents with intelligent routing.

        This method is the core of the multi-agent coordinator, responsible for:
        1. Routing tasks to the most appropriate agent(s)
        2. Executing tasks based on routing decisions
        3. Handling different execution strategies (single, multi, sequential, decomposed)
        4. Updating performance metrics and task status

        Args:
            task: MemoryTask to execute containing query, parameters, and metadata

        Returns:
            MemoryTask: The same task object updated with results, status, and timing

        Raises:
            ValueError: If routing decision is unknown or invalid
            RuntimeError: If task execution fails due to agent errors

        Examples:
            Basic task execution::

                task = MemoryTask(
                    id="simple_task",
                    type="retrieve_memories",
                    query="Find information about Python programming",
                    priority=1
                )

                result_task = await coordinator.execute_task(task)

                if result_task.status == "completed":
                    print(f"Task completed: {result_task.result}")
                else:
                    print(f"Task failed: {result_task.error}")

            Complex task with custom parameters::

                task = MemoryTask(
                    id="complex_analysis",
                    type="analyze_and_graph",
                    query="Analyze learning patterns and build knowledge graph",
                    parameters={
                        "analysis_depth": "comprehensive",
                        "graph_confidence": 0.8,
                        "include_relationships": True
                    },
                    priority=1,
                    namespace=("user", "work")
                )

                result_task = await coordinator.execute_task(task)

                # Check execution details
                print(f"Assigned agent: {result_task.assigned_agent}")
                print(f"Duration: {result_task.completed_at - result_task.started_at}")
                print(f"Result: {result_task.result}")

            Error handling::

                try:
                    result_task = await coordinator.execute_task(task)

                    if result_task.status == "failed":
                        logger.error(f"Task {task.id} failed: {result_task.error}")
                        # Handle failure - maybe retry or use fallback

                except Exception as e:
                    logger.error(f"Unexpected error executing task: {e}")
        """
        task.status = "routing"
        task.started_at = datetime.utcnow()

        try:
            # Step 1: Route task to appropriate agent(s)
            routing_decision = await self._route_task(task)

            # Step 2: Execute based on routing decision
            if routing_decision["routing_decision"] == "single_agent":
                result = await self._execute_single_agent_task(task, routing_decision)
            elif routing_decision["routing_decision"] == "multi_agent":
                result = await self._execute_multi_agent_task(task, routing_decision)
            elif routing_decision["routing_decision"] == "sequential":
                result = await self._execute_sequential_task(task, routing_decision)
            elif routing_decision["routing_decision"] == "decompose":
                result = await self._execute_decomposed_task(task, routing_decision)
            else:
                raise ValueError(
                    f"Unknown routing decision: {
                        routing_decision['routing_decision']}")

            # Step 3: Update task with result
            task.result = result
            task.status = "completed"
            task.completed_at = datetime.utcnow()

            # Update performance metrics
            self._update_performance_metrics(task, success=True)

            return task

        except Exception as e:
            logger.exception(f"Task {task.id} failed: {e}")
            task.error = str(e)
            task.status = "failed"
            task.completed_at = datetime.utcnow()

            # Update performance metrics
            self._update_performance_metrics(task, success=False)

            return task

    async def _route_task(self, task: MemoryTask) -> dict[str, Any]:
        """Route task to appropriate agents using LLM-based intelligent routing.

        This method analyzes the task and uses the coordinator's LLM to determine
        the best routing strategy and agent assignment. It considers agent capabilities,
        specializations, current load, and task requirements.

        Args:
            task: MemoryTask to route containing query, type, and parameters

        Returns:
            Dict[str, Any]: Routing decision containing:
                - routing_decision: Strategy type (single_agent, multi_agent, sequential, decompose)
                - primary_agent: Name of primary agent to handle the task
                - secondary_agents: List of secondary agents (if applicable)
                - execution_strategy: How to execute (single, parallel, sequential)
                - reasoning: Explanation of routing decision
                - estimated_time_ms: Expected execution time
                - confidence: Confidence score (0.0-1.0)

        Examples:
            The returned routing decision format::

                {
                    "routing_decision": "single_agent",
                    "primary_agent": "agentic_rag",
                    "secondary_agents": [],
                    "execution_strategy": "single",
                    "reasoning": "Query requires retrieval expertise",
                    "estimated_time_ms": 1500,
                    "confidence": 0.9
                }

            Multi-agent routing example::

                {
                    "routing_decision": "multi_agent",
                    "primary_agent": "kg_generator",
                    "secondary_agents": ["memory_classifier", "agentic_rag"],
                    "execution_strategy": "parallel",
                    "reasoning": "Complex analysis requires multiple perspectives",
                    "estimated_time_ms": 2500,
                    "confidence": 0.85
                }
        """
        try:
            # Prepare agent capabilities description
            capabilities_desc = []
            for agent_name, capabilities in self.agent_capabilities.items():
                desc = f"- {agent_name}: {
                    capabilities.agent_type} - {
                    ', '.join(
                        capabilities.specialization)}"
                capabilities_desc.append(desc)

            # Create routing prompt
            prompt = self.task_routing_prompt.format(
                task_description=task.query,
                task_type=task.type,
                task_parameters=str(task.parameters),
                agent_capabilities="\n".join(capabilities_desc),
            )

            # Get routing decision from LLM
            response = await self.coordinator_llm.ainvoke(
                [
                    SystemMessage(
                        content="You are an expert task router for multi-agent systems."
                    ),
                    HumanMessage(content=prompt),
                ]
            )

            # Parse routing decision
            routing_decision = self._parse_json_response(response.content)

            if routing_decision and "routing_decision" in routing_decision:
                return routing_decision
            # Fallback to rule-based routing
            return self._fallback_task_routing(task)

        except Exception as e:
            logger.exception(f"Error routing task {task.id}: {e}")
            return self._fallback_task_routing(task)

    def _fallback_task_routing(self, task: MemoryTask) -> dict[str, Any]:
        """Fallback rule-based task routing.
        """
        task_type = task.type.lower()

        if "store" in task_type or "save" in task_type:
            return {
                "routing_decision": "single_agent",
                "primary_agent": "memory_store",
                "secondary_agents": [],
                "execution_strategy": "single",
                "reasoning": "Store tasks go to memory store agent",
                "estimated_time_ms": 500,
                "confidence": 0.8,
            }
        if "retrieve" in task_type or "search" in task_type:
            return {
                "routing_decision": "single_agent",
                "primary_agent": "agentic_rag",
                "secondary_agents": [],
                "execution_strategy": "single",
                "reasoning": "Retrieval tasks go to agentic RAG coordinator",
                "estimated_time_ms": 1500,
                "confidence": 0.8,
            }
        if "analyze" in task_type or "classify" in task_type:
            return {
                "routing_decision": "single_agent",
                "primary_agent": "memory_classifier",
                "secondary_agents": [],
                "execution_strategy": "single",
                "reasoning": "Analysis tasks go to memory classifier",
                "estimated_time_ms": 800,
                "confidence": 0.8,
            }
        if "graph" in task_type or "knowledge" in task_type:
            return {
                "routing_decision": "single_agent",
                "primary_agent": "kg_generator",
                "secondary_agents": [],
                "execution_strategy": "single",
                "reasoning": "Graph tasks go to KG generator",
                "estimated_time_ms": 2000,
                "confidence": 0.8,
            }
        # Default to agentic RAG for unknown tasks
        return {
            "routing_decision": "single_agent",
            "primary_agent": "agentic_rag",
            "secondary_agents": [],
            "execution_strategy": "single",
            "reasoning": "Unknown task type, defaulting to agentic RAG",
            "estimated_time_ms": 1500,
            "confidence": 0.5,
        }

    async def _execute_single_agent_task(
        self, task: MemoryTask, routing_decision: dict[str, Any]
    ) -> Any:
        """Execute task with a single agent.
        """
        agent_name = routing_decision["primary_agent"]
        if agent_name not in self.meta_agents:
            raise ValueError(f"Agent {agent_name} not found")

        meta_state = self.meta_agents[agent_name]
        task.assigned_agent = agent_name
        task.status = "executing"

        # Execute agent with task query
        result = await meta_state.execute_agent(
            input_data={"messages": [{"role": "user", "content": task.query}]},
            update_state=True,
        )

        return result

    async def _execute_multi_agent_task(
        self, task: MemoryTask, routing_decision: dict[str, Any]
    ) -> Any:
        """Execute task with multiple agents in parallel.
        """
        primary_agent = routing_decision["primary_agent"]
        secondary_agents = routing_decision.get("secondary_agents", [])
        all_agents = [primary_agent, *secondary_agents]

        task.assigned_agent = f"multi:{','.join(all_agents)}"
        task.status = "executing"

        # Execute all agents in parallel
        tasks = []
        for agent_name in all_agents:
            if agent_name in self.meta_agents:
                meta_state = self.meta_agents[agent_name]
                task_coro = meta_state.execute_agent(
                    input_data={"messages": [{"role": "user", "content": task.query}]},
                    update_state=True,
                )
                tasks.append(task_coro)

        # Wait for all to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Combine results
        combined_result = {
            "primary_result": results[0] if results else None,
            "secondary_results": results[1:] if len(results) > 1 else [],
            "agents_used": all_agents,
        }

        return combined_result

    async def _execute_sequential_task(
        self, task: MemoryTask, routing_decision: dict[str, Any]
    ) -> Any:
        """Execute task with agents in sequence.
        """
        primary_agent = routing_decision["primary_agent"]
        secondary_agents = routing_decision.get("secondary_agents", [])
        all_agents = [primary_agent, *secondary_agents]

        task.assigned_agent = f"seq:{','.join(all_agents)}"
        task.status = "executing"

        # Execute agents sequentially
        results = []
        current_input = task.query

        for agent_name in all_agents:
            if agent_name in self.meta_agents:
                meta_state = self.meta_agents[agent_name]
                result = await meta_state.execute_agent(
                    input_data={
                        "messages": [{"role": "user", "content": current_input}]
                    },
                    update_state=True,
                )
                results.append(result)

                # Use result as input for next agent
                current_input = str(result)

        return {
            "sequential_results": results,
            "final_result": results[-1] if results else None,
            "agents_used": all_agents,
        }

    async def _execute_decomposed_task(
        self, task: MemoryTask, routing_decision: dict[str, Any]
    ) -> Any:
        """Execute task that has been decomposed into subtasks.
        """
        # This would involve decomposing the task and executing subtasks
        # For now, fall back to single agent execution
        return await self._execute_single_agent_task(
            task,
            {
                "primary_agent": "agentic_rag",
                "secondary_agents": [],
                "execution_strategy": "single",
            },
        )

    def _parse_json_response(self, response: str) -> dict[str, Any] | None:
        """Parse JSON response from LLM.
        """
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

    def _update_performance_metrics(
            self,
            task: MemoryTask,
            success: bool) -> None:
        """Update performance metrics.
        """
        self.performance_metrics["total_tasks"] += 1

        if success:
            self.performance_metrics["successful_tasks"] += 1
        else:
            self.performance_metrics["failed_tasks"] += 1

        # Update latency
        if task.started_at and task.completed_at:
            latency = (task.completed_at -
                       task.started_at).total_seconds() * 1000
            current_avg = self.performance_metrics["avg_latency_ms"]
            total_tasks = self.performance_metrics["total_tasks"]

            # Update rolling average
            self.performance_metrics["avg_latency_ms"] = (
                current_avg * (total_tasks - 1) + latency
            ) / total_tasks

        # Update agent utilization
        if task.assigned_agent:
            agent_key = task.assigned_agent
            if agent_key not in self.performance_metrics["agent_utilization"]:
                self.performance_metrics["agent_utilization"][agent_key] = 0
            self.performance_metrics["agent_utilization"][agent_key] += 1

    async def store_memory(
        self, content: str, namespace: tuple[str, ...] | None = None
    ) -> str:
        """Store a memory using the multi-agent system with intelligent routing.

        This method creates a memory storage task and routes it to the appropriate
        agent (typically the memory store agent). The system automatically handles
        classification, metadata extraction, and storage optimization.

        Args:
            content: The memory content to store (text, structured data, etc.)
            namespace: Optional namespace tuple for organizing memories (e.g., ("user", "work"))

        Returns:
            str: Success message with storage details or error message

        Examples:
            Basic memory storage::

                result = await coordinator.store_memory(
                    "I learned about machine learning algorithms today"
                )
                print(result)  # "Memory stored successfully: {...}"

            Memory with namespace::

                result = await coordinator.store_memory(
                    "Completed project milestone: API integration",
                    namespace=("user", "work", "projects")
                )

            Structured memory storage::

                result = await coordinator.store_memory(
                    json.dumps({
                        "event": "meeting",
                        "participants": ["Alice", "Bob"],
                        "decisions": ["Use React for frontend", "Deploy on AWS"]
                    }),
                    namespace=("user", "work", "meetings")
                )

        Note:
            The system automatically classifies the memory type, extracts metadata,
            and updates relevant knowledge graphs based on the content.
        """
        task = MemoryTask(
            id=f"store_{datetime.utcnow().timestamp()}",
            type="store_memory",
            query=f"Store this memory: {content}",
            parameters={"content": content},
            namespace=namespace,
            priority=5,
        )

        result_task = await self.execute_task(task)

        if result_task.status == "completed":
            return f"Memory stored successfully: {result_task.result}"
        return f"Failed to store memory: {result_task.error}"

    async def retrieve_memories(
        self,
        query: str,
        limit: int = 10,
        memory_types: list[MemoryType] | None = None,
        namespace: tuple[str, ...] | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve memories using the multi-agent system with intelligent routing.

        This method creates a memory retrieval task and routes it to the most appropriate
        agent (typically the agentic RAG coordinator). The system automatically selects
        the best retrieval strategy based on the query characteristics.

        Args:
            query: Natural language query describing what memories to retrieve
            limit: Maximum number of memories to return (default: 10)
            memory_types: Optional list of specific memory types to search within
            namespace: Optional namespace tuple to limit search scope

        Returns:
            List[Dict[str, Any]]: List of memory objects with content, metadata, and relevance scores

        Examples:
            Basic memory retrieval::

                memories = await coordinator.retrieve_memories(
                    "What did I learn about Python programming?"
                )

                for memory in memories:
                    print(f"Content: {memory['content']}")
                    print(f"Relevance: {memory['relevance_score']}")
                    print(f"Timestamp: {memory['timestamp']}")

            Targeted retrieval with filters::

                memories = await coordinator.retrieve_memories(
                    query="machine learning algorithms",
                    limit=5,
                    memory_types=[MemoryType.SEMANTIC, MemoryType.EPISODIC],
                    namespace=("user", "learning")
                )

            Complex query with context::

                memories = await coordinator.retrieve_memories(
                    "Find all meetings where we discussed the API project and show related decisions",
                    limit=20,
                    namespace=("user", "work")
                )

                # System automatically uses graph traversal for complex queries
                for memory in memories:
                    if memory.get('graph_connections'):
                        print(f"Connected entities: {memory['graph_connections']}")

        Note:
            The system automatically:
            - Analyzes query complexity and selects appropriate retrieval strategy
            - Uses vector similarity, graph traversal, or hybrid approaches
            - Applies relevance scoring and ranking
            - Returns structured results with metadata and provenance
        """
        task = MemoryTask(
            id=f"retrieve_{datetime.utcnow().timestamp()}",
            type="retrieve_memories",
            query=query,
            parameters={"limit": limit},
            namespace=namespace,
            memory_types=memory_types,
            priority=3,
        )

        result_task = await self.execute_task(task)

        if result_task.status == "completed":
            # Extract memories from result
            result = result_task.result
            if isinstance(result, dict) and "final_memories" in result:
                return result["final_memories"]
            if isinstance(result, list):
                return result
            return []
        logger.error(f"Failed to retrieve memories: {result_task.error}")
        return []

    async def analyze_memory(self, content: str) -> dict[str, Any]:
        """Analyze memory content using the multi-agent system with specialized routing.

        This method creates a memory analysis task and routes it to the most appropriate
        agent (typically the memory classifier). The system provides comprehensive
        analysis including classification, entity extraction, and importance scoring.

        Args:
            content: The memory content to analyze (text, structured data, etc.)

        Returns:
            Dict[str, Any]: Analysis results containing:
                - analysis: Detailed analysis results from the assigned agent
                - success: Boolean indicating if analysis completed successfully
                - error: Error message if analysis failed

        Examples:
            Basic memory analysis::

                analysis = await coordinator.analyze_memory(
                    "I attended a machine learning conference where I learned about neural networks"
                )

                if analysis["success"]:
                    result = analysis["analysis"]
                    print(f"Memory type: {result.get('memory_type')}")
                    print(f"Entities: {result.get('entities')}")
                    print(f"Importance: {result.get('importance_score')}")
                else:
                    print(f"Analysis failed: {analysis['error']}")

            Complex content analysis::

                analysis = await coordinator.analyze_memory(
                    '''
                    Meeting Notes: Q1 Planning
                    Attendees: Alice (PM), Bob (Engineer), Carol (Designer)
                    Decisions:
                    - Use React for the frontend
                    - Deploy on AWS with auto-scaling
                    - Launch beta by March 15th
                    '''
                )

                if analysis["success"]:
                    result = analysis["analysis"]
                    print(f"Extracted entities: {result.get('entities')}")
                    print(f"Key decisions: {result.get('decisions')}")
                    print(f"Action items: {result.get('action_items')}")
                    print(f"Participants: {result.get('participants')}")

        Note:
            The analysis typically includes:
            - Memory type classification (semantic, episodic, procedural, etc.)
            - Entity extraction (people, organizations, concepts, etc.)
            - Importance and relevance scoring
            - Metadata extraction (dates, locations, etc.)
            - Relationship identification
            - Content summarization
        """
        task = MemoryTask(
            id=f"analyze_{datetime.utcnow().timestamp()}",
            type="analyze_memory",
            query=f"Analyze this memory: {content}",
            parameters={"content": content},
            priority=4,
        )

        result_task = await self.execute_task(task)

        if result_task.status == "completed":
            return {"analysis": result_task.result, "success": True}
        return {"error": result_task.error, "success": False}

    async def generate_knowledge_graph(
        self, namespace: tuple[str, ...] | None = None
    ) -> dict[str, Any]:
        """Generate knowledge graph using the multi-agent system with KG specialization.

        This method creates a knowledge graph generation task and routes it to the
        specialized KG generator agent. The system extracts entities, relationships,
        and builds a comprehensive knowledge graph from stored memories.

        Args:
            namespace: Optional namespace tuple to limit graph generation scope

        Returns:
            Dict[str, Any]: Knowledge graph results containing:
                - knowledge_graph: Generated graph with nodes and relationships
                - success: Boolean indicating if generation completed successfully
                - error: Error message if generation failed

        Examples:
            Basic knowledge graph generation::

                kg_result = await coordinator.generate_knowledge_graph()

                if kg_result["success"]:
                    graph = kg_result["knowledge_graph"]
                    print(f"Nodes: {len(graph.get('nodes', []))}")
                    print(f"Relationships: {len(graph.get('relationships', []))}")

                    # Explore entities
                    for node in graph.get('nodes', []):
                        print(f"Entity: {node['name']} ({node['type']})")

                    # Explore relationships
                    for rel in graph.get('relationships', []):
                        print(f"{rel['source']} -> {rel['target']} ({rel['type']})")
                else:
                    print(f"KG generation failed: {kg_result['error']}")

            Scoped knowledge graph generation::

                kg_result = await coordinator.generate_knowledge_graph(
                    namespace=("user", "work", "projects")
                )

                if kg_result["success"]:
                    graph = kg_result["knowledge_graph"]

                    # Analyze work-related entities
                    work_entities = [
                        node for node in graph.get('nodes', [])
                        if node.get('type') in ['person', 'organization', 'project']
                    ]

                    print(f"Work entities: {len(work_entities)}")

                    # Find project relationships
                    project_rels = [
                        rel for rel in graph.get('relationships', [])
                        if 'project' in rel.get('type', '').lower()
                    ]

                    print(f"Project relationships: {len(project_rels)}")

        Note:
            The knowledge graph typically includes:
            - Entities: People, organizations, concepts, technologies, etc.
            - Relationships: Works_at, uses, knows, creates, etc.
            - Confidence scores for entities and relationships
            - Metadata: Creation timestamps, memory references, etc.
            - Graph statistics: Node counts, relationship types, etc.
        """
        task = MemoryTask(
            id=f"kg_{datetime.utcnow().timestamp()}",
            type="generate_knowledge_graph",
            query="Extract and build knowledge graph from memories",
            parameters={},
            namespace=namespace,
            priority=6,
        )

        result_task = await self.execute_task(task)

        if result_task.status == "completed":
            return {"knowledge_graph": result_task.result, "success": True}
        return {"error": result_task.error, "success": False}

    def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status and health information.

        This method provides a complete overview of the multi-agent system's current
        state, including agent health, performance metrics, and operational status.

        Returns:
            Dict[str, Any]: System status containing:
                - coordinator_status: Overall coordinator status (active, degraded, error)
                - total_agents: Number of managed agents
                - active_tasks: Number of currently executing tasks
                - completed_tasks: Number of completed tasks
                - performance_metrics: System performance statistics
                - agent_status: Individual agent status and health
                - agent_capabilities: Summary of each agent's capabilities

        Examples:
            Basic system status check::

                status = coordinator.get_system_status()

                print(f"Coordinator: {status['coordinator_status']}")
                print(f"Total agents: {status['total_agents']}")
                print(f"Active tasks: {status['active_tasks']}")
                print(f"Success rate: {status['performance_metrics']['successful_tasks'] / status['performance_metrics']['total_tasks'] * 100:.1f}%")

            Detailed agent status::

                status = coordinator.get_system_status()

                for agent_name, agent_info in status['agent_status'].items():
                    print(f"Agent: {agent_name}")
                    print(f"  Type: {agent_info['agent_type']}")
                    print(f"  Status: {agent_info['execution_status']}")
                    print(f"  Executions: {agent_info['execution_count']}")
                    print(f"  Needs recompile: {agent_info['needs_recompile']}")

            Performance monitoring::

                status = coordinator.get_system_status()
                metrics = status['performance_metrics']

                print(f"Total tasks: {metrics['total_tasks']}")
                print(f"Successful: {metrics['successful_tasks']}")
                print(f"Failed: {metrics['failed_tasks']}")
                print(f"Average latency: {metrics['avg_latency_ms']:.1f}ms")

                # Agent utilization
                for agent, count in metrics['agent_utilization'].items():
                    utilization = count / metrics['total_tasks'] * 100
                    print(f"Agent {agent}: {utilization:.1f}% utilization")

        Note:
            This method is synchronous and provides a snapshot of the current system
            state. For continuous monitoring, call this method periodically or use
            the run_diagnostic() method for health checks.
        """
        agent_status = {}
        for agent_name, meta_state in self.meta_agents.items():
            agent_status[agent_name] = {
                "agent_name": meta_state.agent_name,
                "agent_type": meta_state.agent_type,
                "execution_status": meta_state.execution_status,
                "execution_count": meta_state.graph_context.get(
                    "execution_count",
                    0),
                "needs_recompile": meta_state.needs_recompile,
            }

        return {
            "coordinator_status": "active",
            "total_agents": len(self.meta_agents),
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "performance_metrics": self.performance_metrics,
            "agent_status": agent_status,
            "agent_capabilities": {
                name: {
                    "specialization": caps.specialization,
                    "supported_memory_types": [
                        mt.value for mt in caps.supported_memory_types
                    ],
                }
                for name, caps in self.agent_capabilities.items()
            },
        }

    async def run_diagnostic(self) -> dict[str, Any]:
        """Run comprehensive system diagnostic with agent health checks.

        This method performs a complete system diagnostic by testing each agent
        with a simple diagnostic query. It identifies unhealthy agents and provides
        detailed error information for troubleshooting.

        Returns:
            Dict[str, Any]: Diagnostic results containing:
                - system_status: Overall system health (healthy, degraded, critical)
                - agent_diagnostics: Individual agent diagnostic results
                - performance_metrics: Current system performance metrics

        Examples:
            Basic diagnostic check::

                diagnostic = await coordinator.run_diagnostic()

                print(f"System status: {diagnostic['system_status']}")

                if diagnostic['system_status'] != 'healthy':
                    print("Issues detected:")
                    for agent, result in diagnostic['agent_diagnostics'].items():
                        if result['status'] != 'healthy':
                            print(f"  {agent}: {result.get('error', 'Unknown error')}")
                else:
                    print("All agents are healthy")

            Detailed diagnostic analysis::

                diagnostic = await coordinator.run_diagnostic()

                for agent_name, result in diagnostic['agent_diagnostics'].items():
                    print(f"Agent: {agent_name}")
                    print(f"  Status: {result['status']}")

                    if result['status'] == 'healthy':
                        print(f"  Test result: {result.get('test_result', 'N/A')}")
                    else:
                        print(f"  Error: {result.get('error', 'Unknown error')}")

            Performance analysis::

                diagnostic = await coordinator.run_diagnostic()
                metrics = diagnostic['performance_metrics']

                if metrics['total_tasks'] > 0:
                    success_rate = metrics['successful_tasks'] / metrics['total_tasks']
                    print(f"Success rate: {success_rate * 100:.1f}%")

                    if success_rate < 0.9:
                        print("Warning: Low success rate detected")

                    if metrics['avg_latency_ms'] > 5000:
                        print("Warning: High latency detected")

        Note:
            This diagnostic runs a simple test query on each agent to verify basic
            functionality. For production systems, consider running this periodically
            to monitor system health and detect degradation early.
        """
        diagnostic_results = {}

        # Test each agent
        for agent_name, meta_state in self.meta_agents.items():
            try:
                test_result = await meta_state.execute_agent(
                    input_data={
                        "messages": [
                            {"role": "user", "content": "System diagnostic test"}
                        ]
                    },
                    update_state=False,
                )
                diagnostic_results[agent_name] = {
                    "status": "healthy",
                    "test_result": (
                        str(test_result)[:100] + "..."
                        if len(str(test_result)) > 100
                        else str(test_result)
                    ),
                }
            except Exception as e:
                diagnostic_results[agent_name] = {
                    "status": "error", "error": str(e)}

        return {
            "system_status": (
                "healthy"
                if all(r["status"] == "healthy" for r in diagnostic_results.values())
                else "degraded"
            ),
            "agent_diagnostics": diagnostic_results,
            "performance_metrics": self.performance_metrics,
        }
