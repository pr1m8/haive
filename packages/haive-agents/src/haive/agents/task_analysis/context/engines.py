# src/haive/agents/task_analysis/context/engine.py

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.task_analysis.context.models import (
    ContextDomain,
    ContextFlow,
    ContextRequirement,
)
from haive.agents.task_analysis.context.prompts import (
    CONTEXT_ANALYSIS_PROMPT,
    CONTEXT_FLOW_PROMPT,
    CONTEXT_OPTIMIZATION_PROMPT,
    DOMAIN_EXPERTISE_PROMPT,
)

# Main context analysis engine
ContextAnalyzerEngine = AugLLMConfig(
    name="context_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=CONTEXT_ANALYSIS_PROMPT,
    structured_output_model=ContextRequirement,
    system_message="You are a context requirements analyst specializing in information flow.",
)

# Context flow mapping engine
ContextFlowEngine = AugLLMConfig(
    name="context_flow_mapper",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=CONTEXT_FLOW_PROMPT,
    structured_output_model=ContextFlow,
    system_message="You analyze how context flows between tasks and integration points.",
)

# Context optimization engine
ContextOptimizerEngine = AugLLMConfig(
    name="context_optimizer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=CONTEXT_OPTIMIZATION_PROMPT,
    structured_output_model=None,  # Returns optimization plan text
    system_message="You optimize context loading and caching strategies.",
)

# Domain expertise analyzer
DomainExpertiseEngine = AugLLMConfig(
    name="domain_expertise_analyzer",
    llm_config=AzureLLMConfig(
        model="gpt-4o",
    ),
    prompt_template=DOMAIN_EXPERTISE_PROMPT,
    structured_output_model=ContextDomain,
    system_message="You identify and categorize knowledge domain requirements.",
)
