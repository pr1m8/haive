# src/haive/agents/task_analysis/agent.py

import logging
from typing import Any, Literal

from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from langgraph.graph import END, START
from langgraph.types import Command, Send
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.task_analysis.analysis.engines import (
    FeasibilityAssessorEngine,
    IntegratedAnalyzerEngine,
    OptimizationRecommenderEngine,
)

# Import models
from haive.agents.task_analysis.base.models import TaskNode
from haive.agents.task_analysis.complexity.engines import (
    ComplexityAssessorEngine,
    ComplexityFactorsEngine,
)
from haive.agents.task_analysis.complexity.models import ComplexityVector
from haive.agents.task_analysis.context.engines import (
    ContextAnalyzerEngine,
)

# Import all engines
from haive.agents.task_analysis.decomposer.engines import (
    RecursiveDecomposerEngine,
    TaskDecomposerEngine,
    TaskValidationEngine,
)
from haive.agents.task_analysis.execution.engines import (
    ExecutionPlannerEngine,
    JoinPointStrategyEngine,
)
from haive.agents.task_analysis.execution.models import ExecutionPlan
from haive.agents.task_analysis.tree.engines import (
    TreeStructureAnalyzerEngine,
)
from haive.agents.task_analysis.tree.models import TaskTree

logger = logging.getLogger(__name__)

# ============================================================================
# ROUTING FUNCTIONS (same as before)
# ============================================================================


def route_after_decomposition(state: dict[str, Any]) -> str:
    """Route after initial decomposition."""
    task_node = state.get("task_node")

    if not task_node:
        return "validate_decomposition"

    # Check if we need recursive decomposition
    needs_expansion = any(
        subtask.can_expand
        for subtask in task_node.subtasks
        if hasattr(subtask, "can_expand")
    )

    if needs_expansion and state.get("current_depth", 0) < state.get("max_depth", 3):
        return "recursive_decompose"

    # Validate first
    if not state.get("validation_complete"):
        return "validate_decomposition"

    # Then parallel analysis
    return "parallel_analysis"


def route_after_validation(state: dict[str, Any]) -> str:
    """Route after validation."""
    validation_result = state.get("validation_result", {})

    if validation_result.get("needs_redecomposition"):
        return "decompose_task"

    if validation_result.get("needs_expansion"):
        return "recursive_decompose"

    return "parallel_analysis"


def route_after_analysis(state: dict[str, Any]) -> str:
    """Route after parallel analysis completes."""
    # Check if all analyses are complete
    has_complexity = state.get("complexity_vector") is not None
    has_context = state.get("context_requirement") is not None
    has_tree_analysis = state.get("tree_analysis") is not None

    if not (has_complexity and has_context and has_tree_analysis):
        # Should not happen with proper Send usage
        return "integrate_analysis"

    # Check complexity score
    complexity = state.get("complexity_vector")
    if complexity and complexity.total_score() > 7:
        return "optimization"

    return "execution_planning"


def route_final_decision(state: dict[str, Any]) -> str:
    """Make final routing decision."""
    execution_plan = state.get("execution_plan")
    integrated_analysis = state.get("integrated_analysis")

    if not execution_plan:
        return "__end__"

    # Check if optimization needed
    if execution_plan.optimization_opportunities:
        return "optimization"

    # Check if feasibility assessment needed
    if not state.get("feasibility_assessed"):
        return "feasibility_assessment"

    return "__end__"


# ============================================================================
# NODE FUNCTIONS (same as before)
# ============================================================================


def parallel_analysis_orchestrator(
    state: dict[str, Any],
) -> Command[Literal["complexity_assessment", "context_analysis", "tree_analysis"]]:
    """Orchestrate parallel analysis using Send."""
    task_node = state["task_node"]
    task_tree = TaskTree(task_node)

    # Prepare data for each analysis
    tree_summary = task_tree.get_analysis_summary()

    # Create Send objects for parallel execution
    sends = []

    # Send to complexity assessment
    sends.append(
        Send(
            "complexity_assessment",
            {
                **state,
                "task_details": task_node.description,
                "depth": tree_summary["max_depth"],
                "breadth": len(task_tree.get_parallel_groups()),
                "total_nodes": tree_summary["total_tasks"],
                "dependency_count": len(task_node.dependencies),
                "has_cycles": False,
                "task_tree_summary": str(task_node),
                "parallel_count": len(task_tree.get_parallel_groups()),
                "join_points": tree_summary["join_points"],
                "critical_path_length": tree_summary["critical_path_length"],
            },
        )
    )

    # Send to context analysis
    sends.append(
        Send(
            "context_analysis",
            {
                **state,
                "task_description": task_node.description,
                "task_type": task_node.task_type.value,
                "domain": state.get("domain", "general"),
                "subtask_list": "\n".join(
                    [f"- {st.name}" for st in task_node.subtasks]
                ),
                "dependencies": str(task_node.dependencies),
            },
        )
    )

    # Send to tree structure analysis
    sends.append(
        Send(
            "tree_analysis",
            {
                **state,
                "tree_visualization": str(task_tree),
                "max_depth": tree_summary["max_depth"],
                "max_breadth": len(task_tree.get_parallel_groups()),
                "total_nodes": tree_summary["total_tasks"],
                "leaf_nodes": len([n for n in task_node.get_all_steps()]),
                "balance_factor": 0.8,  # Simplified
            },
        )
    )

    return Command(goto=sends)


def join_analyses(
    state: dict[str, Any],
) -> Command[Literal["execution_planning", "optimization", "integrate_analysis"]]:
    """Join parallel analyses and route next."""
    # All analyses should be complete at this point
    next_node = route_after_analysis(state)
    return Command(update={"analyses_complete": True}, goto=next_node)  # type: ignore


def recursive_expansion_orchestrator(
    state: dict[str, Any],
) -> Command[Literal["recursive_decompose", "validate_decomposition"]]:
    """Orchestrate recursive decomposition."""
    task_node = state["task_node"]

    # Find expandable subtasks
    expandable_tasks = [
        subtask
        for subtask in task_node.subtasks
        if isinstance(subtask, TaskNode) and subtask.can_expand
    ]

    if not expandable_tasks:
        return Command(goto="validate_decomposition")

    # Take first expandable task
    task_to_expand = expandable_tasks[0]

    # Send to recursive decomposer
    return Command(
        update={
            "parent_task_name": task_node.name,
            "parent_context": task_node.description,
            "task_description": task_to_expand.description,
            "expansion_reason": task_to_expand.expansion_hints or "Needs more detail",
            "current_depth": state.get("current_depth", 0) + 1,
            "inherited_constraints": [],
        },
        goto="recursive_decompose",
    )


# ============================================================================
# MAIN AGENT CLASS
# ============================================================================


class TaskAnalysisAgent(Agent):
    """Comprehensive task analysis agent that orchestrates multiple analysis engines.

    This agent:
    1. Decomposes tasks hierarchically
    2. Analyzes complexity across multiple dimensions
    3. Identifies parallelization opportunities
    4. Plans execution with resource allocation
    5. Provides integrated analysis and recommendations
    """

    # Configuration
    max_decomposition_depth: int = Field(
        default=4, description="Maximum task decomposition depth"
    )
    enable_recursive_decomposition: bool = Field(
        default=True, description="Enable recursive task expansion"
    )
    parallel_analysis: bool = Field(
        default=True, description="Run analyses in parallel"
    )

    # ========================================================================
    # INITIALIZE ENGINES IN __init__
    # ========================================================================

    def __init__(self, **kwargs):
        """Initialize with engines properly set up."""
        # Initialize engines dict before calling super().__init__
        if "engines" not in kwargs:
            kwargs["engines"] = {
                # Decomposition engines
                "task_decomposer": TaskDecomposerEngine,
                "recursive_decomposer": RecursiveDecomposerEngine,
                "task_validator": TaskValidationEngine,
                # Analysis engines
                "complexity_assessor": ComplexityAssessorEngine,
                "complexity_factors": ComplexityFactorsEngine,
                "context_analyzer": ContextAnalyzerEngine,
                "tree_analyzer": TreeStructureAnalyzerEngine,
                # Planning engines
                "execution_planner": ExecutionPlannerEngine,
                "join_strategist": JoinPointStrategyEngine,
                # Integration engines
                "integrated_analyzer": IntegratedAnalyzerEngine,
                "feasibility_assessor": FeasibilityAssessorEngine,
                "optimizer": OptimizationRecommenderEngine,
            }

        super().__init__(**kwargs)

    # ========================================================================
    # SCHEMA SETUP - USE from_components!
    # ========================================================================

    def setup_agent(self):
        """Set up the agent with schema derived from engines."""
        # Get all engine instances
        engine_instances = list(self.engines.values())

        # Use SchemaComposer.from_components to derive schema automatically
        self.state_schema = SchemaComposer.from_components(
            components=engine_instances,
            name="TaskAnalysisState",
        )

        # Enable schema generation
        self.set_schema = True

    # ========================================================================
    # GRAPH BUILDING (same as before)
    # ========================================================================
    # src/haive/agents/task_analysis/agent.py (only showing the build_graph method fix)

    def build_graph(self) -> BaseGraph:
        """Build the task analysis workflow graph."""
        graph = BaseGraph(name="Task Analysis Workflow")

        # ====================================================================
        # DECOMPOSITION PHASE
        # ====================================================================

        # Initial decomposition
        graph.add_node(
            "decompose_task",
            EngineNodeConfig(
                name="decompose_task", engine=self.engines["task_decomposer"]
            ),
        )
        graph.add_edge(START, "decompose_task")

        # Validation
        graph.add_node(
            "validate_decomposition",
            EngineNodeConfig(
                name="validate_decomposition", engine=self.engines["task_validator"]
            ),
        )

        # Recursive decomposition
        if self.enable_recursive_decomposition:
            graph.add_node(
                "recursive_decompose",
                EngineNodeConfig(
                    name="recursive_decompose",
                    engine=self.engines["recursive_decomposer"],
                ),
            )
            graph.add_node("recursive_orchestrator", recursive_expansion_orchestrator)
            # Add edges for recursive flow
            graph.add_edge("recursive_orchestrator", "recursive_decompose")
            graph.add_edge("recursive_decompose", "validate_decomposition")

        # ====================================================================
        # PARALLEL ANALYSIS PHASE
        # ====================================================================

        # Orchestrator node - THIS NEEDS TO SEND TO THE ANALYSIS NODES
        graph.add_node("parallel_analysis", parallel_analysis_orchestrator)

        # Analysis nodes
        graph.add_node(
            "complexity_assessment",
            EngineNodeConfig(
                name="complexity_assessment", engine=self.engines["complexity_assessor"]
            ),
        )

        graph.add_node(
            "context_analysis",
            EngineNodeConfig(
                name="context_analysis", engine=self.engines["context_analyzer"]
            ),
        )

        graph.add_node(
            "tree_analysis",
            EngineNodeConfig(
                name="tree_analysis", engine=self.engines["tree_analyzer"]
            ),
        )

        # Join node
        graph.add_node("join_analyses", join_analyses)

        # IMPORTANT: Add edges from parallel_analysis to each analysis node
        # These are the Send targets from parallel_analysis_orchestrator
        graph.add_edge("parallel_analysis", "complexity_assessment")
        graph.add_edge("parallel_analysis", "context_analysis")
        graph.add_edge("parallel_analysis", "tree_analysis")

        # Analysis nodes all converge to join
        graph.add_edge("complexity_assessment", "join_analyses")
        graph.add_edge("context_analysis", "join_analyses")
        graph.add_edge("tree_analysis", "join_analyses")

        # ====================================================================
        # PLANNING PHASE
        # ====================================================================

        graph.add_node(
            "execution_planning",
            EngineNodeConfig(
                name="execution_planning", engine=self.engines["execution_planner"]
            ),
        )

        # ====================================================================
        # INTEGRATION PHASE
        # ====================================================================

        graph.add_node(
            "integrate_analysis",
            EngineNodeConfig(
                name="integrate_analysis", engine=self.engines["integrated_analyzer"]
            ),
        )

        graph.add_node(
            "feasibility_assessment",
            EngineNodeConfig(
                name="feasibility_assessment",
                engine=self.engines["feasibility_assessor"],
            ),
        )

        graph.add_node(
            "optimization",
            EngineNodeConfig(name="optimization", engine=self.engines["optimizer"]),
        )

        # ====================================================================
        # EDGES AND ROUTING
        # ====================================================================

        # From decomposition - conditional routing
        graph.add_conditional_edges(
            "decompose_task",
            route_after_decomposition,
            {
                "validate_decomposition": "validate_decomposition",
                "recursive_decompose": (
                    "recursive_orchestrator"
                    if self.enable_recursive_decomposition
                    else "validate_decomposition"
                ),
                "parallel_analysis": "parallel_analysis",
            },
        )

        # From validation - conditional routing
        graph.add_conditional_edges(
            "validate_decomposition",
            route_after_validation,
            {
                "decompose_task": "decompose_task",
                "recursive_decompose": (
                    "recursive_orchestrator"
                    if self.enable_recursive_decomposition
                    else "parallel_analysis"
                ),
                "parallel_analysis": "parallel_analysis",
            },
        )

        # From join to next phase - conditional routing
        graph.add_conditional_edges(
            "join_analyses",
            route_after_analysis,
            {
                "execution_planning": "execution_planning",
                "optimization": "optimization",
                "integrate_analysis": "integrate_analysis",
            },
        )

        # From execution planning to integration
        graph.add_edge("execution_planning", "integrate_analysis")

        # From integration - conditional routing
        graph.add_conditional_edges(
            "integrate_analysis",
            route_final_decision,
            {
                "feasibility_assessment": "feasibility_assessment",
                "optimization": "optimization",
                "__end__": END,
            },
        )

        # From feasibility to END
        graph.add_edge("feasibility_assessment", END)

        # From optimization back to execution planning (optimization loop)
        graph.add_edge("optimization", "execution_planning")

        return graph

    # ========================================================================
    # CONVENIENCE METHODS (same as before)
    # ========================================================================

    def analyze_task(
        self,
        task_description: str,
        domain: str = "general",
        additional_context: str = "",
        max_depth: int | None = None,
    ) -> dict[str, Any]:
        """Analyze a task comprehensively.

        Args:
            task_description: Natural language task description
            domain: Task domain (e.g., "software", "research", "creative")
            additional_context: Any additional context
            max_depth: Maximum decomposition depth (uses default if None)

        Returns:
            Comprehensive analysis results
        """
        return self.invoke(
            {
                "task_description": task_description,
                "domain": domain,
                "additional_context": additional_context,
                "max_depth": max_depth or self.max_decomposition_depth,
            }
        )

    def get_execution_plan(
        self, analysis_result: dict[str, Any]
    ) -> ExecutionPlan | None:
        """Extract execution plan from analysis results."""
        return analysis_result.get("execution_plan")

    def get_complexity_assessment(
        self, analysis_result: dict[str, Any]
    ) -> ComplexityVector | None:
        """Extract complexity assessment from analysis results."""
        return analysis_result.get("complexity_vector")

    def get_recommendations(self, analysis_result: dict[str, Any]) -> list[str]:
        """Extract recommendations from analysis results."""
        return analysis_result.get("recommendations", [])
