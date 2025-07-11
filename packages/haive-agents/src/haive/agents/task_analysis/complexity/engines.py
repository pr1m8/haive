# src/haive/agents/task_analysis/complexity/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.complexity.models import (
    ComplexityFactors,
    ComplexityVector,
)
from haive.agents.task_analysis.complexity.prompts import (
    COMPLEXITY_ASSESSMENT_PROMPT,
    COMPLEXITY_COMPARISON_PROMPT,
    COMPLEXITY_FACTORS_PROMPT,
)

# Main complexity assessment engine
ComplexityAssessorEngine = AugLLMConfig(
    name="complexity_assessor",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=COMPLEXITY_ASSESSMENT_PROMPT,
    structured_output_model=ComplexityVector,
    system_message="You are an expert at multi-dimensional complexity assessment.",
)

# Detailed factors analysis engine
ComplexityFactorsEngine = AugLLMConfig(
    name="complexity_factors_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=COMPLEXITY_FACTORS_PROMPT,
    structured_output_model=ComplexityFactors,
    system_message="You analyze detailed factors contributing to task complexity.",
)

# Comparative analysis engine
ComplexityComparisonEngine = AugLLMConfig(
    name="complexity_comparator",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=COMPLEXITY_COMPARISON_PROMPT,
    structured_output_model=None,  # Returns comparative analysis text
    system_message="You compare task complexities to provide relative assessments.",
)
