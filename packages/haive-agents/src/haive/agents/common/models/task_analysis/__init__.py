"""Task Complexity Analysis Module for Haive Agents.

This module provides sophisticated analysis of task complexity including dependency
mapping, parallelization opportunities, solvability assessment, and execution planning.
Uses AutoTree for dynamic dependency graph management and supports complex
task decomposition patterns.

Classes:
    TaskType: Enumeration of different task categories
    DependencyType: Types of dependency relationships
    ComplexityLevel: Overall complexity classifications
    Task: Base task representation with subtasks
    TaskStep: Individual executable steps
    DependencyNode: Dependency relationship modeling
    ComplexityMetrics: Quantitative complexity measurements
    SolvabilityAssessment: Task solvability analysis
    ParallelizationAnalysis: Parallel execution opportunities
    TaskComplexityAnalysis: Complete task analysis results
    TaskComplexityAnalyzer: Main analyzer engine

Example:
    ```python
    from haive.agents.common.models.task_complexity import TaskComplexityAnalyzer

    analyzer = TaskComplexityAnalyzer()

    # Analyze a complex task
    analysis = analyzer.analyze_task(
        "Find the birthday of the most recent Wimbledon winner and calculate
         their age in days, then find the square root of that number"
    )

    print(f"Complexity Level: {analysis.complexity_level}")
    print(f"Parallelizable Steps: {len(analysis.parallelization.parallel_groups)}")
    print(f"Estimated Duration: {analysis.estimated_duration_hours}")

    # Visualize dependency tree
    print(analysis.dependency_tree.visualize())
    ```
"""

from haive.agents.common.models.task_analysis.base import (
    ComplexityLevel,
    ComputationalComplexity,
    DependencyNode,
    DependencyType,
    KnowledgeComplexity,
    ResourceType,
    Task,
    TaskStep,
    TaskType,
    TimeComplexity,
)
from haive.agents.common.models.task_analysis.complexity_metrics import (
    BreadthAnalysis,
    ComplexityMetrics,
    CriticalPathAnalysis,
    DepthAnalysis,
)
from haive.agents.common.models.task_analysis.dependency_tree import (
    DependencyAnalyzer,
    TaskDependencyTree,
)
from haive.agents.common.models.task_analysis.parallelization import (
    ExecutionPhase,
    JoinPoint,
    ParallelGroup,
    ParallelizationAnalysis,
    ParallelizationAnalyzer,
)
from haive.agents.common.models.task_analysis.solvability import (
    BlockerType,
    ResourceRequirement,
    SolvabilityAnalyzer,
    SolvabilityAssessment,
)
from haive.agents.common.models.task_analysis.task_analyzer import (
    TaskComplexityAnalysis,
    TaskComplexityAnalyzer,
)
from haive.agents.common.models.task_analysis.visualization import (
    ComplexityDashboard,
    DependencyGraphRenderer,
    TaskComplexityVisualizer,
)

__all__ = [
    # Base enums and types
    "TaskType",
    "DependencyType",
    "ComplexityLevel",
    "ComputationalComplexity",
    "KnowledgeComplexity",
    "TimeComplexity",
    "ResourceType",
    # Core task models
    "Task",
    "TaskStep",
    "DependencyNode",
    # Analysis components
    "ComplexityMetrics",
    "DepthAnalysis",
    "BreadthAnalysis",
    "CriticalPathAnalysis",
    "SolvabilityAssessment",
    "BlockerType",
    "ResourceRequirement",
    "SolvabilityAnalyzer",
    "ParallelizationAnalysis",
    "ParallelGroup",
    "ExecutionPhase",
    "JoinPoint",
    "ParallelizationAnalyzer",
    # Tree and dependency analysis
    "TaskDependencyTree",
    "DependencyAnalyzer",
    # Main analyzer
    "TaskComplexityAnalysis",
    "TaskComplexityAnalyzer",
    # Visualization
    "TaskComplexityVisualizer",
    "DependencyGraphRenderer",
    "ComplexityDashboard",
]

# Version info
__version__ = "1.0.0"
__author__ = "Haive Framework"
