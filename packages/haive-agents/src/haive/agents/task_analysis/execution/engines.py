# src/haive/agents/task_analysis/execution/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.execution.models import (
    ExecutionPlan,
    JoinPoint,
    ResourceAllocation,
)
from haive.agents.task_analysis.execution.prompts import (
    EXECUTION_PLANNING_PROMPT,
    JOIN_POINT_STRATEGY_PROMPT,
    PHASE_OPTIMIZATION_PROMPT,
    RESOURCE_ALLOCATION_PROMPT,
)

# Main execution planning engine
ExecutionPlannerEngine = AugLLMConfig(
    name="execution_planner",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=EXECUTION_PLANNING_PROMPT,
    structured_output_model=ExecutionPlan,
    system_message="You are an execution planning expert specializing in task scheduling.",
)

# Phase optimization engine
PhaseOptimizerEngine = AugLLMConfig(
    name="phase_optimizer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=PHASE_OPTIMIZATION_PROMPT,
    structured_output_model=None,  # Returns optimized phase text
    system_message="You optimize execution phases for maximum efficiency.",
)

# Join point strategy engine
JoinPointStrategyEngine = AugLLMConfig(
    name="join_point_strategist",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=JOIN_POINT_STRATEGY_PROMPT,
    structured_output_model=JoinPoint,
    system_message="You design strategies for combining parallel execution results.",
)

# Resource allocation engine
ResourceAllocatorEngine = AugLLMConfig(
    name="resource_allocator",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=RESOURCE_ALLOCATION_PROMPT,
    structured_output_model=ResourceAllocation,
    system_message="You optimize resource allocation across task execution phases.",
)
