# src/haive/agents/task_analysis/analysis/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.analysis.prompts import (
    FEASIBILITY_ASSESSMENT_PROMPT,
    INTEGRATED_ANALYSIS_PROMPT,
    OPTIMIZATION_RECOMMENDATIONS_PROMPT,
)

# Integrated analysis engine
IntegratedAnalyzerEngine = AugLLMConfig(
    name="integrated_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=INTEGRATED_ANALYSIS_PROMPT,
    structured_output_model=None,  # Returns comprehensive analysis
    system_message="You integrate multiple analysis dimensions into comprehensive insights.",
)

# Feasibility assessment engine
FeasibilityAssessorEngine = AugLLMConfig(
    name="feasibility_assessor",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=FEASIBILITY_ASSESSMENT_PROMPT,
    structured_output_model=None,  # Returns feasibility assessment
    system_message="You assess overall task feasibility based on comprehensive analysis.",
)

# Optimization recommendations engine
OptimizationRecommenderEngine = AugLLMConfig(
    name="optimization_recommender",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=OPTIMIZATION_RECOMMENDATIONS_PROMPT,
    structured_output_model=None,  # Returns optimization recommendations
    system_message="You generate optimization recommendations from task analysis.",
)
