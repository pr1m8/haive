"""Engine configurations for the Tree of Thoughts agent.

This module defines specialized engine configurations for candidate generation,
evaluation, and selection in the Tree of Thoughts algorithm.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from haive.agents.reasoning_and_critique.tot.models import (
    CandidateEvaluation,
    CandidateGeneration,
)

# =============================
# Default Prompts
# =============================

# Generator prompt
generator_system_message = SystemMessage(
    content="""You are an expert problem solver working on a Tree of Thoughts approach.
Your task is to generate diverse and creative candidate solutions for the problem.
Explore different approaches and reasoning pathways.

Return your response as a structured output with reasoning and multiple candidate solutions."""
)

generator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", generator_system_message.content),
        MessagesPlaceholder(variable_name="history"),
        (
            "user",
            """Problem: {problem}

{seed_info}

Generate {expansion_count} different candidate solutions.""",
        ),
    ]
)

# Evaluator prompt
evaluator_system_message = SystemMessage(
    content="""You are an expert evaluator working on a Tree of Thoughts approach.
Your task is to evaluate a candidate solution and provide a score between 0 and 1.
Be critical and analytical in your assessment.

Return your response as a structured output with a numerical score between 0 and 1
and detailed feedback explaining the score."""
)

evaluator_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", evaluator_system_message.content),
        MessagesPlaceholder(variable_name="history"),
        (
            "user",
            """Problem: {problem}

Candidate Solution:
{candidate}

Evaluate this solution and provide a numerical score between 0 and 1, where:
- 0 means completely incorrect or irrelevant
- 1 means perfect solution

Your evaluation:""",
        ),
    ]
)

# =============================
# Pre-configured Engine Configs
# =============================

# Generator engine with default parameters
generator_aug_llm_config = AugLLMConfig(
    name="tot_generator",
    description="Generates candidate solutions for tree of thoughts",
    prompt_template=generator_prompt,
    structured_output_model=CandidateGeneration,
)

# Evaluator engine with default parameters
evaluator_aug_llm_config = AugLLMConfig(
    name="tot_evaluator",
    description="Evaluates candidate solutions for tree of thoughts",
    prompt_template=evaluator_prompt,
    structured_output_model=CandidateEvaluation,
)
