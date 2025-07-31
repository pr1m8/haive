"""Aug_Llms core module.

This module provides aug llms functionality for the Haive framework.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.utils.parser_utils import parse_reasoning_modules_to_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from haive.agents.reasoning_and_critique.self_discover.models import (
    AdaptedModules,
    Plan,
)

reasoning_prompt = """
Step {step_id}: {step_description}

Task Context: {task_description}

Relevant Reasoning Modules:
{reasoning_modules}

Perform step {step_id} based on the provided reasoning structure. Ensure clarity and logical deduction.
"""
step_reasoning_prompt_template = PromptTemplate(template=reasoning_prompt)
step_reasoning_chain = AugLLMConfig(
    name="step_reasoning_executor",
    prompt_template=step_reasoning_prompt_template,
    output_parser=StrOutputParser(),
)
reasoning_modules_instance = ReasoningModules()  # ✅ Create an instance


select_prompt_template = PromptTemplate(
    template="""
Select several reasoning modules that are crucial to utilize in order to solve the given task:

All reasoning module descriptions:
{reasoning_modules}

Task: {task_description}

Select several modules that are crucial for solving the task above:
"""
)
select_prompt_template = select_prompt_template.partial(
    reasoning_modules=parse_reasoning_modules_to_string(
        reasoning_modules_instance.modules
    )
)
select_chain = AugLLMConfig(
    name="select",
    prompt_template=select_prompt_template,
    structured_output_model=ReasoningModules,
)


adapt_template = """
Rephrase and specify each reasoning module so that it better helps solving the task:

SELECTED module descriptions:
{selected_modules}

Task: {task_description}

Adapt each reasoning module description to better solve the task:
"""
adapt_prompt_template = PromptTemplate(template=adapt_template)
adapt_chain = AugLLMConfig(
    name="adapt",
    prompt_template=adapt_prompt_template,
    structured_output_model=AdaptedModules,
)


structured_template_prompt = """
Operationalize the reasoning modules into a step-by-step reasoning plan in JSON format:

Here's an example:

Example Plan:
{{
    "id": 1,
    "name": "Example Plan",
    "status": "not_started",
    "tasks": [
        {{
            "id": 1,
            "description": "Analyze the problem thoroughly.",
            "status": "in_progress",
            "reasoning_modules": [
                {{
                    "name": "Critical Thinking",
                    "description": "Analyze the problem from different perspectives, questioning assumptions, and evaluating evidence or information."
                }},
                {{
                    "name": "Systems Thinking",
                    "description": "Consider the problem as part of a larger system and understand interconnected elements."
                }}
            ],
            "subtasks": [
                {{
                    "id": 2,
                    "description": "Break down the problem into smaller parts.",
                    "status": "not_started",
                    "reasoning_modules": [
                        {{
                            "name": "Problem Decomposition",
                            "description": "How can I break down this problem into smaller, more manageable parts?"
                        }}
                    ],
                    "subtasks": []
                }}
            ]
        }}
    ]
}}

Adapted module description:
{adapted_modules}

Task: {task_description}

Implement a reasoning structure for solvers to follow step-by-step and arrive at the correct answer.

Note: do NOT actually arrive at a conclusion in this pass. Your job is to generate a PLAN so that in the future you can fill it out and arrive at the correct conclusion for tasks like this.
"""
structured_template = PromptTemplate(template=structured_template_prompt)
structured_chain = AugLLMConfig(
    name="structured_reasoning_planner",
    prompt_template=structured_template,
    structured_output_model=Plan,
)
