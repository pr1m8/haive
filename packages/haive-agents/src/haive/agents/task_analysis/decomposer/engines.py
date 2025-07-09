# src/haive/agents/task_analysis/decomposer/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.base.models import TaskNode
from haive.agents.task_analysis.decomposer.prompts import (
    RECURSIVE_DECOMPOSITION_PROMPT,
    TASK_DECOMPOSITION_PROMPT,
    TASK_VALIDATION_PROMPT,
)

# Main decomposer engine
TaskDecomposerEngine = AugLLMConfig(
    name="task_decomposer",
    # llm_config=AzureLLMConfig(model="gpt-4o", temperature=0.3, max_tokens=3000),
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=TASK_DECOMPOSITION_PROMPT,
    structured_output_model=TaskNode,
    system_message="You are an expert at hierarchical task decomposition and work breakdown structures.",
)

# Recursive decomposer for expanding nodes
RecursiveDecomposerEngine = AugLLMConfig(
    name="recursive_decomposer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=RECURSIVE_DECOMPOSITION_PROMPT,
    structured_output_model=TaskNode,
    system_message="You specialize in recursive task decomposition, maintaining context across levels.",
)

# Validation engine
TaskValidationEngine = AugLLMConfig(
    name="task_validator",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=TASK_VALIDATION_PROMPT,
    structured_output_model=None,  # Returns text feedback
    system_message="You validate task decompositions for completeness and correctness.",
)
