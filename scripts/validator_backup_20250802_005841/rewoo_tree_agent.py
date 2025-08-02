"""ReWOO Tree-based Planning Agent with Parallelizable Execution.

This agent implements the ReWOO (Reasoning without Observation) methodology
with tree-based planning for parallelizable execution. It features:

- Hierarchical tree planning with recursive decomposition
- Parallelizable node execution with proper dependencies
- Tool aliasing and forced tool choice
- Structured output models with field validators
- Plan-and-execute pattern with dynamic recompilation
- LLM Compiler inspired parallelization

Reference:
- ReWOO: https://langchain-ai.github.io/langgraph/tutorials/rewoo/rewoo/#solver
- LLM Compiler: https://langchain-ai.github.io/langgraph/tutorials/llm-compiler/LLMCompiler/
"""

import asyncio
import logging
import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langgraph.types import Command
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

logger = logging.getLogger(__name__)


class TaskType(str, Enum):
    """Types of tasks in the planning tree."""

    RESEARCH = "research"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    EXECUTION = "execution"
    VALIDATION = "validation"
    PLANNING = "planning"


class TaskStatus(str, Enum):
    """Status of tasks in the planning tree."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


class TaskPriority(str, Enum):
    """Priority levels for tasks."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ToolAlias(BaseModel):
    """Tool alias configuration for forced tool choice."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    alias: str = Field(
        ..., description="The alias name for the tool", min_length=1, max_length=50
    )

    actual_tool: str = Field(
        ..., description="The actual tool name to execute", min_length=1, max_length=50
    )

    force_choice: bool = Field(
        default=True, description="Whether to force this tool choice"
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict, description="Default parameters for the tool"
    )

    @field_validator("alias")
    @classmethod
    def validate_alias(cls, v: str) -> str:
        """Validate alias format."""
        if not v.replace("_", "").isalnum():
            raise ValueError("Alias must be alphanumeric with underscores")
        return v


class PlanNode(BaseModel):
    """A node in the planning tree representing a task."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Identity
    id: str = Field(
        ..., description="Unique identifier for the node", min_length=1, max_length=100
    )

    name: str = Field(
        ...,
        description="Human-readable name for the task",
        min_length=1,
        max_length=200,
    )

    # Task details
    task_type: TaskType = Field(
        default=TaskType.EXECUTION, description="Type of task this node represents"
    )

    description: str = Field(
        ...,
        description="Detailed description of the task",
        min_length=1,
        max_length=1000,
    )

    # Status and metadata
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, description="Current status of the task"
    )

    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, description="Priority level of the task"
    )

    # Execution details
    agent_name: str | None = Field(
        default=None, description="Name of the agent to execute this task"
    )

    tool_alias: str | None = Field(
        default=None, description="Tool alias to use for execution"
    )

    expected_output: str | None = Field(
        default=None, description="Expected output format or type"
    )

    # Tree structure
    parent_id: str | None = Field(default=None, description="ID of the parent node")

    children_ids: list[str] = Field(
        default_factory=list, description="List of child node IDs"
    )

    # Dependencies
    dependencies: list[str] = Field(
        default_factory=list, description="List of node IDs this task depends on"
    )

    dependent_nodes: list[str] = Field(
        default_factory=list, description="List of node IDs that depend on this task"
    )

    # Execution results
    result: Any | None = Field(
        default=None, description="Result of executing this task"
    )

    error: str | None = Field(default=None, description="Error message if task failed")

    # Timing
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the task was created"
    )

    started_at: datetime | None = Field(
        default=None, description="When the task started execution"
    )

    completed_at: datetime | None = Field(
        default=None, description="When the task completed"
    )

    # Parallelization metadata
    parallelizable: bool = Field(
        default=True, description="Whether this task can be executed in parallel"
    )

    estimated_duration: float | None = Field(
        default=None, description="Estimated execution time in seconds"
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate node ID format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Node ID must be alphanumeric with underscores and hyphens"
            )
        return v

    @model_validator(mode="after")
    @classmethod
    def validate_dependencies(cls) -> "PlanNode":
        """Validate dependency relationships."""
        # Cannot depend on itself
        if self.id in self.dependencies:
            raise ValueError("Node cannot depend on itself")

        # Cannot be both parent and dependency
        if self.parent_id and self.parent_id in self.dependencies:
            raise ValueError("Node cannot depend on its parent")

        return self

    def add_child(self, child_id: str) -> None:
        """Add a child node."""
        if child_id not in self.children_ids:
            self.children_ids.append(child_id)

    def add_dependency(self, dependency_id: str) -> None:
        """Add a dependency."""
        if dependency_id not in self.dependencies:
            self.dependencies.append(dependency_id)

    def can_execute(self, completed_nodes: set[str]) -> bool:
        """Check if this node can be executed given completed nodes."""
        if self.status != TaskStatus.PENDING:
            return False

        # All dependencies must be completed
        return all(dep_id in completed_nodes for dep_id in self.dependencies)

    def mark_started(self) -> None:
        """Mark the task as started."""
        self.status = TaskStatus.IN_PROGRESS
        self.started_at = datetime.now()

    def mark_completed(self, result: Any = None) -> None:
        """Mark the task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()
        if result is not None:
            self.result = result

    def mark_failed(self, error: str) -> None:
        """Mark the task as failed."""
        self.status = TaskStatus.FAILED
        self.error = error
        self.completed_at = datetime.now()


class PlanTree(BaseModel):
    """A tree structure representing the complete execution plan."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Tree metadata
    id: str = Field(
        ...,
        description="Unique identifier for the plan tree",
        min_length=1,
        max_length=100,
    )

    name: str = Field(
        ...,
        description="Human-readable name for the plan",
        min_length=1,
        max_length=200,
    )

    description: str = Field(
        ...,
        description="Description of what this plan accomplishes",
        min_length=1,
        max_length=1000,
    )

    # Tree structure
    nodes: dict[str, PlanNode] = Field(
        default_factory=dict, description="Dictionary of all nodes in the tree"
    )

    root_id: str | None = Field(default=None, description="ID of the root node")

    # Execution metadata
    created_at: datetime = Field(
        default_factory=datetime.now, description="When the plan was created"
    )

    total_nodes: int = Field(default=0, description="Total number of nodes in the tree")

    completed_nodes: int = Field(default=0, description="Number of completed nodes")

    failed_nodes: int = Field(default=0, description="Number of failed nodes")

    # Parallelization data
    execution_levels: list[list[str]] = Field(
        default_factory=list,
        description="Nodes organized by execution level for parallelization",
    )

    max_parallelism: int = Field(
        default=4, description="Maximum number of parallel executions", ge=1, le=16
    )

    @field_validator("id")
    @classmethod
    def validate_id(cls, v: str) -> str:
        """Validate plan tree ID format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Plan tree ID must be alphanumeric with underscores and hyphens"
            )
        return v

    def add_node(self, node: PlanNode) -> None:
        """Add a node to the tree."""
        self.nodes[node.id] = node
        self.total_nodes = len(self.nodes)

        # Update parent-child relationships
        if node.parent_id and node.parent_id in self.nodes:
            self.nodes[node.parent_id].add_child(node.id)

        # Set as root if no parent
        if node.parent_id is None and self.root_id is None:
            self.root_id = node.id

    def get_node(self, node_id: str) -> PlanNode | None:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def get_ready_nodes(self) -> list[PlanNode]:
        """Get nodes that are ready for execution."""
        completed_ids = {
            node_id
            for node_id, node in self.nodes.items()
            if node.status == TaskStatus.COMPLETED
        }

        ready_nodes = []
        for node in self.nodes.values():
            if node.can_execute(completed_ids):
                ready_nodes.append(node)

        return ready_nodes

    def get_parallelizable_nodes(self) -> list[list[PlanNode]]:
        """Get nodes organized by parallelizable execution levels."""
        levels = []
        processed = set()

        while len(processed) < len(self.nodes):
            level_nodes = []

            for node in self.nodes.values():
                if node.id in processed:
                    continue

                # Check if all dependencies are processed
                deps_ready = all(dep_id in processed for dep_id in node.dependencies)

                if deps_ready and node.parallelizable:
                    level_nodes.append(node)

            if not level_nodes:
                # Find any remaining nodes (break circular dependencies)
                for node in self.nodes.values():
                    if node.id not in processed:
                        level_nodes.append(node)
                        break

            levels.append(level_nodes)
            processed.update(node.id for node in level_nodes)

        return levels

    def mark_node_completed(self, node_id: str, result: Any = None) -> None:
        """Mark a node as completed."""
        if node_id in self.nodes:
            self.nodes[node_id].mark_completed(result)
            self.completed_nodes = sum(
                1 for node in self.nodes.values() if node.status == TaskStatus.COMPLETED
            )

    def mark_node_failed(self, node_id: str, error: str) -> None:
        """Mark a node as failed."""
        if node_id in self.nodes:
            self.nodes[node_id].mark_failed(error)
            self.failed_nodes = sum(
                1 for node in self.nodes.values() if node.status == TaskStatus.FAILED
            )

    def get_completion_percentage(self) -> float:
        """Get the completion percentage of the plan."""
        if self.total_nodes == 0:
            return 0.0
        return (self.completed_nodes / self.total_nodes) * 100.0

    def is_complete(self) -> bool:
        """Check if the entire plan is complete."""
        return self.completed_nodes == self.total_nodes

    def has_failures(self) -> bool:
        """Check if there are any failed nodes."""
        return self.failed_nodes > 0


class ReWOOTreePlannerOutput(BaseModel):
    """Structured output for the ReWOO tree planner."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Plan metadata
    plan_id: str = Field(
        ...,
        description="Unique identifier for the generated plan",
        min_length=1,
        max_length=100,
    )

    plan_name: str = Field(
        ...,
        description="Human-readable name for the plan",
        min_length=1,
        max_length=200,
    )

    # Planning analysis
    problem_analysis: str = Field(
        ...,
        description="Analysis of the problem and requirements",
        min_length=10,
        max_length=2000,
    )

    approach_strategy: str = Field(
        ...,
        description="High-level strategy for solving the problem",
        min_length=10,
        max_length=1000,
    )

    # Tree structure
    plan_tree: PlanTree = Field(
        ..., description="The complete planning tree with all nodes"
    )

    # Execution metadata
    estimated_duration: float = Field(
        default=0.0, description="Estimated total execution time in seconds", ge=0.0
    )

    parallelization_factor: float = Field(
        default=1.0,
        description="Factor by which parallelization improves performance",
        ge=1.0,
        le=10.0,
    )

    # Tool usage
    required_tools: list[str] = Field(
        default_factory=list, description="List of tools required for execution"
    )

    tool_aliases: dict[str, ToolAlias] = Field(
        default_factory=dict, description="Tool aliases for forced tool choice"
    )

    # Risk assessment
    risk_factors: list[str] = Field(
        default_factory=list, description="Identified risk factors in the plan"
    )

    fallback_strategies: list[str] = Field(
        default_factory=list,
        description="Fallback strategies if parts of the plan fail",
    )

    @field_validator("plan_id")
    @classmethod
    def validate_plan_id(cls, v: str) -> str:
        """Validate plan ID format."""
        if not v.replace("_", "").replace("-", "").isalnum():
            raise ValueError(
                "Plan ID must be alphanumeric with underscores and hyphens"
            )
        return v

    @model_validator(mode="after")
    @classmethod
    def validate_consistency(cls) -> "ReWOOTreePlannerOutput":
        """Validate consistency between plan components."""
        # Plan tree ID should match plan ID
        if self.plan_tree.id != self.plan_id:
            raise ValueError("Plan tree ID must match plan ID")

        # Required tools should include all tool aliases
        alias_tools = {alias.actual_tool for alias in self.tool_aliases.values()}
        missing_tools = alias_tools - set(self.required_tools)
        if missing_tools:
            raise ValueError(f"Required tools missing aliases: {missing_tools}")

        return self


class ReWOOTreeExecutorOutput(BaseModel):
    """Structured output for the ReWOO tree executor."""

    model_config = ConfigDict(
        str_strip_whitespace=True, validate_assignment=True, extra="forbid"
    )

    # Execution metadata
    execution_id: str = Field(
        ...,
        description="Unique identifier for this execution",
        min_length=1,
        max_length=100,
    )

    plan_id: str = Field(
        ..., description="ID of the plan being executed", min_length=1, max_length=100
    )

    # Execution results
    completed_nodes: dict[str, Any] = Field(
        default_factory=dict, description="Results from completed nodes"
    )

    failed_nodes: dict[str, str] = Field(
        default_factory=dict, description="Error messages from failed nodes"
    )

    # Final result
    final_result: Any | None = Field(
        default=None, description="Final aggregated result of the execution"
    )

    # Execution statistics
    total_execution_time: float = Field(
        default=0.0, description="Total execution time in seconds", ge=0.0
    )

    parallel_efficiency: float = Field(
        default=0.0,
        description="Efficiency of parallel execution (0-1)",
        ge=0.0,
        le=1.0,
    )

    nodes_executed: int = Field(default=0, description="Number of nodes executed", ge=0)

    nodes_failed: int = Field(
        default=0, description="Number of nodes that failed", ge=0
    )

    # Success status
    success: bool = Field(
        default=False, description="Whether the execution was successful overall"
    )

    completion_percentage: float = Field(
        default=0.0, description="Percentage of plan completed", ge=0.0, le=100.0
    )


class ReWOOTreeAgentState(MessagesState):
    """Enhanced state for ReWOO tree agent."""

    # Current planning context
    current_plan: ReWOOTreePlannerOutput | None = None
    current_execution: ReWOOTreeExecutorOutput | None = None

    # Tool management
    available_tools: list[str] = Field(default_factory=list)
    tool_aliases: dict[str, ToolAlias] = Field(default_factory=dict)

    # Recursive planning state
    planning_depth: int = Field(default=0, ge=0, le=10)
    subplan_stack: list[str] = Field(default_factory=list)

    # Parallelization state
    active_executions: dict[str, Any] = Field(default_factory=dict)
    execution_queue: list[str] = Field(default_factory=list)

    # Result aggregation
    node_results: dict[str, Any] = Field(default_factory=dict)
    final_output: Any | None = None


class ReWOOTreeAgent(Agent):
    """ReWOO Tree-based Planning Agent with Parallelizable Execution.

    This agent implements the ReWOO methodology with enhancements:
    - Hierarchical tree planning with recursive decomposition
    - Parallelizable execution with dependency management
    - Tool aliasing for forced tool choice
    - Structured output models with validation
    - LLM Compiler inspired optimizations
    """

    # Tool management
    available_tools: list[BaseTool] = Field(
        default_factory=list, description="Available tools for execution"
    )

    tool_aliases: dict[str, ToolAlias] = Field(
        default_factory=dict, description="Tool aliases for forced choice"
    )

    # Planning configuration
    max_planning_depth: int = Field(
        default=5, description="Maximum depth for recursive planning", ge=1, le=10
    )

    max_parallelism: int = Field(
        default=4, description="Maximum parallel executions", ge=1, le=16
    )

    # Specialized agents
    planner_agent: Agent | None = Field(
        default=None, description="Specialized agent for planning"
    )

    executor_agent: Agent | None = Field(
        default=None, description="Specialized agent for execution"
    )

    def __init__(self, **kwargs) -> None:
        """Initialize ReWOO Tree Agent."""
        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = ReWOOTreeAgentState

        super().__init__(**kwargs)

        # Create specialized agents if not provided
        if self.planner_agent is None:
            self.planner_agent = self._create_planner_agent()

        if self.executor_agent is None:
            self.executor_agent = self._create_executor_agent()

    def _create_planner_agent(self) -> Agent:
        """Create specialized planning agent."""
        planner_prompt = """
        You are a ReWOO Tree Planner. Your task is to analyze a problem and create a detailed execution plan.

        Analysis Framework:
        1. Problem Decomposition: Break down the problem into manageable tasks
        2. Dependency Analysis: Identify task dependencies and parallelizable components
        3. Resource Planning: Determine tools and agents needed
        4. Risk Assessment: Identify potential failures and mitigation strategies
        5. Optimization: Maximize parallelization opportunities

        Task Types:
        - RESEARCH: Information gathering and analysis
        - ANALYSIS: Data processing and evaluation
        - SYNTHESIS: Combining information into insights
        - EXECUTION: Performing actions or operations
        - VALIDATION: Checking results and quality
        - PLANNING: Further decomposition if needed

        Create a structured plan with:
        - Clear task hierarchy
        - Dependency relationships
        - Tool assignments
        - Parallelization opportunities
        - Risk mitigation strategies

        Input: {input}
        Planning Context: {context}
        Available Tools: {tools}
        """

        return SimpleAgent(
            name=f"{self.name}_planner",
            engine=AugLLMConfig(
                prompt_template=planner_prompt,
                temperature=0.3,  # Lower for consistent planning
                structured_output_model=ReWOOTreePlannerOutput,
            ),
        )

    def _create_executor_agent(self) -> Agent:
        """Create specialized execution agent."""
        executor_prompt = """
        You are a ReWOO Tree Executor. Your task is to execute plan nodes efficiently and in parallel.

        Execution Framework:
        1. Dependency Check: Ensure all prerequisites are met
        2. Resource Allocation: Assign tools and agents to tasks
        3. Parallel Execution: Execute independent tasks concurrently
        4. Result Aggregation: Combine results from parallel executions
        5. Error Handling: Manage failures and recovery strategies

        Execution Rules:
        - Always check dependencies before execution
        - Use tool aliases when specified
        - Maximize parallelization opportunities
        - Handle errors gracefully with fallback strategies
        - Aggregate results coherently

        Current Task: {task}
        Available Tools: {tools}
        Dependencies: {dependencies}
        """

        return ReactAgent(
            name=f"{self.name}_executor",
            engine=AugLLMConfig(
                prompt_template=executor_prompt,
                temperature=0.5,  # Moderate for flexible execution
                structured_output_model=ReWOOTreeExecutorOutput,
            ),
            tools=self.available_tools,
        )

    def add_tool_alias(
        self, alias: str, actual_tool: str, force_choice: bool = True, **params
    ) -> None:
        """Add a tool alias for forced tool choice."""
        tool_alias = ToolAlias(
            alias=alias,
            actual_tool=actual_tool,
            force_choice=force_choice,
            parameters=params,
        )
        self.tool_aliases[alias] = tool_alias

    def build_graph(self) -> BaseGraph:
        """Build the execution graph for ReWOO tree agent."""
        graph = BaseGraph(
            name=f"{self.name}_rewoo_graph", state_schema=self.state_schema
        )

        # Add planning node
        graph.add_node("planner", self._planning_node)

        # Add execution coordinator
        graph.add_node("executor", self._execution_coordinator_node)

        # Add result aggregator
        graph.add_node("aggregator", self._result_aggregator_node)

        # Add recursive planning check
        graph.add_node("recursive_check", self._recursive_planning_check_node)

        # Connect nodes
        graph.add_edge("__start__", "planner")
        graph.add_edge("planner", "executor")
        graph.add_edge("executor", "recursive_check")
        graph.add_edge("recursive_check", "aggregator")
        graph.add_edge("aggregator", "__end__")

        # Add recursive edge
        graph.add_edge("recursive_check", "planner")

        return graph

    def _planning_node(self, state: ReWOOTreeAgentState) -> Command:
        """Execute the planning phase."""
        # Get planning depth (default to 0 if not set)
        planning_depth = getattr(state, "planning_depth", 0)
        logger.info(f"🧠 Planning phase for depth {planning_depth}")

        # Prepare planning context
        context = {
            "planning_depth": planning_depth,
            "available_tools": [tool.name for tool in self.available_tools],
            "tool_aliases": self.tool_aliases,
            "max_parallelism": self.max_parallelism,
        }

        # Get the last user message
        user_input = ""
        if state.messages:
            user_input = (
                state.messages[-1].content
                if hasattr(state.messages[-1], "content")
                else str(state.messages[-1])
            )

        # Execute planning
        planner_input = {
            "input": user_input,
            "context": context,
            "tools": [tool.name for tool in self.available_tools],
        }

        try:
            # Run planning synchronously
            plan_result = self.planner_agent.run(planner_input)

            # Ensure we have a ReWOOTreePlannerOutput
            if not isinstance(plan_result, ReWOOTreePlannerOutput):
                # Try to construct from dict or string
                if isinstance(plan_result, dict):
                    plan_result = ReWOOTreePlannerOutput(**plan_result)
                else:
                    # Fallback: create a simple plan
                    plan_result = self._create_fallback_plan(
                        str(plan_result), user_input
                    )

            return Command(
                update={
                    "current_plan": plan_result,
                    "tool_aliases": plan_result.tool_aliases,
                    "messages": [
                        *state.messages,
                        AIMessage(
                            content=f"Created plan: {
                                plan_result.plan_name}"
                        ),
                    ],
                },
                goto="executor",
            )

        except Exception as e:
            logger.exception(f"Planning failed: {e}")
            # Create fallback plan
            fallback_plan = self._create_fallback_plan(str(e), user_input)

            return Command(
                update={
                    "current_plan": fallback_plan,
                    "messages": [
                        *state.messages,
                        AIMessage(content=f"Created fallback plan due to error: {e}"),
                    ],
                },
                goto="executor",
            )

    def _create_fallback_plan(
        self, error_or_result: str, user_input: str
    ) -> ReWOOTreePlannerOutput:
        """Create a fallback plan when planning fails."""
        plan_id = f"fallback_{uuid.uuid4().hex[:8]}"

        # Create a simple single-node plan
        root_node = PlanNode(
            id="root_task",
            name="Execute Request",
            task_type=TaskType.EXECUTION,
            description=f"Execute the user request: {user_input}",
            priority=TaskPriority.HIGH,
            parallelizable=False,
        )

        plan_tree = PlanTree(
            id=plan_id,
            name="Fallback Plan",
            description="Simple fallback plan for execution",
            root_id="root_task",
        )

        plan_tree.add_node(root_node)

        return ReWOOTreePlannerOutput(
            plan_id=plan_id,
            plan_name="Fallback Plan",
            problem_analysis=f"Analysis: {error_or_result}",
            approach_strategy="Execute as single task",
            plan_tree=plan_tree,
            estimated_duration=30.0,
            parallelization_factor=1.0,
            required_tools=[tool.name for tool in self.available_tools],
            tool_aliases=self.tool_aliases,
            risk_factors=["Simple fallback execution"],
            fallback_strategies=["Direct execution without complex planning"],
        )

    def _execution_coordinator_node(self, state: ReWOOTreeAgentState) -> Command:
        """Coordinate the execution of the plan tree."""
        logger.info("⚡ Execution coordination phase")

        if not state.current_plan:
            return Command(
                update={
                    "messages": [
                        *state.messages,
                        AIMessage(content="No plan to execute"),
                    ]
                },
                goto="aggregator",
            )

        plan_tree = state.current_plan.plan_tree

        # Get parallelizable execution levels
        execution_levels = plan_tree.get_parallelizable_nodes()

        # Execute levels in sequence, nodes in parallel
        execution_results = {}

        for level_idx, level_nodes in enumerate(execution_levels):
            logger.info(
                f"📊 Executing level {
                    level_idx +
                    1} with {
                    len(level_nodes)} nodes"
            )

            # Execute nodes in this level (simplified for sync execution)
            level_results = self._execute_nodes_sync(level_nodes, state)
            execution_results.update(level_results)

            # Update plan tree with results
            for node_id, result in level_results.items():
                if isinstance(result, Exception):
                    plan_tree.mark_node_failed(node_id, str(result))
                else:
                    plan_tree.mark_node_completed(node_id, result)

        # Create execution output
        execution_output = ReWOOTreeExecutorOutput(
            execution_id=f"exec_{plan_tree.id}",
            plan_id=plan_tree.id,
            completed_nodes=execution_results,
            failed_nodes={
                node_id: node.error
                for node_id, node in plan_tree.nodes.items()
                if node.status == TaskStatus.FAILED
            },
            nodes_executed=len(execution_results),
            nodes_failed=plan_tree.failed_nodes,
            success=plan_tree.completed_nodes > 0 and plan_tree.failed_nodes == 0,
            completion_percentage=plan_tree.get_completion_percentage(),
        )

        return Command(
            update={
                "current_execution": execution_output,
                "node_results": execution_results,
                "messages": [
                    *state.messages,
                    AIMessage(
                        content=f"Execution completed: {
                            execution_output.completion_percentage:.1f}% success"
                    ),
                ],
            },
            goto="recursive_check",
        )

    def _execute_nodes_sync(
        self, nodes: list[PlanNode], state: ReWOOTreeAgentState
    ) -> dict[str, Any]:
        """Execute nodes synchronously (simplified version)."""
        results = {}

        for node in nodes:
            try:
                logger.info(f"🔧 Executing node: {node.name}")

                # Mark node as started
                node.mark_started()

                # Simple execution using direct tool call or executor
                tool_aliases = getattr(state, "tool_aliases", {})
                if node.tool_alias and node.tool_alias in tool_aliases:
                    # Use specific tool through alias
                    alias_config = state.tool_aliases[node.tool_alias]
                    result = self._execute_with_tool_alias_sync(
                        alias_config, node.description
                    )
                else:
                    # Use general executor agent
                    result = self.executor_agent.run(node.description)

                results[node.id] = result

            except Exception as e:
                logger.exception(f"Node {node.id} failed: {e}")
                results[node.id] = e

        return results

    def _execute_with_tool_alias_sync(
        self, alias_config: ToolAlias, description: str
    ) -> str:
        """Execute a task using a specific tool alias (sync version)."""
        # Find the actual tool
        actual_tool = None
        for tool in self.available_tools:
            if tool.name == alias_config.actual_tool:
                actual_tool = tool
                break

        if not actual_tool:
            raise ValueError(f"Tool not found: {alias_config.actual_tool}")

        # Execute tool synchronously
        try:
            result = actual_tool.run(description)
            return result
        except Exception as e:
            logger.exception(f"Tool execution failed: {e}")
            raise

    async def _execute_parallel_nodes(
        self, nodes: list[PlanNode], state: ReWOOTreeAgentState
    ) -> dict[str, Any]:
        """Execute nodes in parallel with proper coordination."""
        # Create execution tasks
        tasks = []
        for node in nodes:
            task = asyncio.create_task(self._execute_single_node(node, state))
            tasks.append((node.id, task))

        # Wait for all tasks to complete
        results = {}
        for node_id, task in tasks:
            try:
                result = await task
                results[node_id] = result
            except Exception as e:
                logger.exception(f"Node {node_id} failed: {e}")
                results[node_id] = e

        return results

    async def _execute_single_node(
        self, node: PlanNode, state: ReWOOTreeAgentState
    ) -> Any:
        """Execute a single node with proper tool aliasing."""
        logger.info(f"🔧 Executing node: {node.name}")

        # Mark node as started
        node.mark_started()

        # Prepare execution context
        execution_context = {
            "task": node.description,
            "task_type": node.task_type,
            "expected_output": node.expected_output,
            "tool_alias": node.tool_alias,
            "dependencies": [
                state.node_results.get(dep_id)
                for dep_id in node.dependencies
                if dep_id in state.node_results
            ],
        }

        # Execute using executor agent
        try:
            if node.tool_alias and node.tool_alias in state.tool_aliases:
                # Use specific tool through alias
                alias_config = state.tool_aliases[node.tool_alias]
                tool_result = await self._execute_with_tool_alias(
                    alias_config, execution_context
                )
                return tool_result
            # Use general executor agent
            result = await self.executor_agent.arun(execution_context)
            return result

        except Exception as e:
            logger.exception(f"Node execution failed: {e}")
            raise

    async def _execute_with_tool_alias(
        self, alias_config: ToolAlias, context: dict[str, Any]
    ) -> Any:
        """Execute a task using a specific tool alias."""
        # Find the actual tool
        actual_tool = None
        for tool in self.available_tools:
            if tool.name == alias_config.actual_tool:
                actual_tool = tool
                break

        if not actual_tool:
            raise ValueError(f"Tool not found: {alias_config.actual_tool}")

        # Prepare tool input
        tool_input = {**alias_config.parameters, **context}

        # Execute tool
        try:
            result = await actual_tool.arun(tool_input)
            return result
        except Exception as e:
            logger.exception(f"Tool execution failed: {e}")
            raise

    def _recursive_planning_check_node(self, state: ReWOOTreeAgentState) -> Command:
        """Check if recursive planning is needed."""
        logger.info("🔄 Recursive planning check")

        # Get current state values with defaults
        planning_depth = getattr(state, "planning_depth", 0)
        subplan_stack = getattr(state, "subplan_stack", [])

        # Check if we need deeper planning
        if (
            planning_depth < self.max_planning_depth
            and state.current_execution
            and state.current_execution.completion_percentage < 80.0
        ):

            # Identify failed or incomplete nodes that need replanning
            failed_nodes = []
            if state.current_plan:
                failed_nodes = [
                    node
                    for node in state.current_plan.plan_tree.nodes.values()
                    if node.status in [TaskStatus.FAILED, TaskStatus.BLOCKED]
                ]

            if failed_nodes:
                logger.info(
                    f"🔄 Triggering recursive planning for {
                        len(failed_nodes)} failed nodes"
                )

                # Update state for recursive planning
                return Command(
                    update={
                        "planning_depth": planning_depth + 1,
                        "subplan_stack": [*subplan_stack, state.current_plan.plan_id],
                        "messages": [
                            *state.messages,
                            AIMessage(
                                content=f"Initiating recursive planning (depth {
                                    planning_depth + 1})"
                            ),
                        ],
                    },
                    goto="planner",
                )

        # No recursive planning needed
        return Command(goto="aggregator")

    def _result_aggregator_node(self, state: ReWOOTreeAgentState) -> Command:
        """Aggregate results from all executions."""
        logger.info("📊 Result aggregation phase")

        # Aggregate all node results
        final_result = None

        if state.current_execution and state.node_results:
            # Create comprehensive result
            final_result = {
                "plan_summary": {
                    "plan_id": (
                        state.current_plan.plan_id if state.current_plan else "unknown"
                    ),
                    "execution_id": state.current_execution.execution_id,
                    "success": state.current_execution.success,
                    "completion_percentage": state.current_execution.completion_percentage,
                    "nodes_executed": state.current_execution.nodes_executed,
                    "nodes_failed": state.current_execution.nodes_failed,
                },
                "node_results": state.node_results,
                "execution_levels": (
                    state.current_plan.plan_tree.execution_levels
                    if state.current_plan
                    else []
                ),
                "tool_usage": list(state.tool_aliases.keys()),
                "planning_depth": state.planning_depth,
            }

        # Create final response
        response_content = self._format_final_response(final_result, state)

        return Command(
            update={
                "final_output": final_result,
                "messages": [*state.messages, AIMessage(content=response_content)],
            },
            goto="__end__",
        )

    def _format_final_response(
        self, result: dict[str, Any], state: ReWOOTreeAgentState
    ) -> str:
        """Format the final response for the user."""
        if not result:
            return "❌ Execution failed - no results generated"

        plan_summary = result.get("plan_summary", {})

        response = f"""🎯 **ReWOO Tree Execution Complete**

**Plan Summary:**
- Plan ID: {plan_summary.get('plan_id', 'N/A')}
- Success: {'✅' if plan_summary.get('success', False) else '❌'}
- Completion: {plan_summary.get('completion_percentage', 0):.1f}%
- Nodes Executed: {plan_summary.get('nodes_executed', 0)}
- Nodes Failed: {plan_summary.get('nodes_failed', 0)}

**Execution Details:**
- Planning Depth: {result.get('planning_depth', 0)}
- Tools Used: {', '.join(result.get('tool_usage', []))}
- Parallelization: {len(result.get('execution_levels', []))} levels

**Results:**
{self._format_node_results(result.get('node_results', {}))}
"""

        return response

    def _format_node_results(self, node_results: dict[str, Any]) -> str:
        """Format node results for display."""
        if not node_results:
            return "No results available"

        formatted = []
        for node_id, result in node_results.items():
            if isinstance(result, Exception):
                formatted.append(f"- {node_id}: ❌ Error - {result!s}")
            else:
                # Truncate long results
                result_str = str(result)
                if len(result_str) > 200:
                    result_str = result_str[:200] + "..."
                formatted.append(f"- {node_id}: ✅ {result_str}")

        return "\n".join(formatted)
