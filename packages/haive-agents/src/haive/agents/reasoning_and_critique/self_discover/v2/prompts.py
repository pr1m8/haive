# src/haive/agents/self_discovery/prompts.py
"""
Prompt templates for Self-Discovery reasoning system.
"""

from langchain_core.prompts import ChatPromptTemplate

# Select reasoning modules prompt
select_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at selecting appropriate reasoning modules for problem-solving tasks.

Your job is to analyze the given task and select the most crucial reasoning modules that would help solve it effectively.

Consider the nature of the task, its complexity, and what types of thinking would be most beneficial.""",
        ),
        (
            "human",
            """Select several reasoning modules that are crucial to utilize in order to solve the given task:

All reasoning module descriptions:
{reasoning_modules}

Task: {task_description}

Select several modules that are crucial for solving the task above. Explain your selection briefly.""",
        ),
    ]
)


# Adapt modules prompt
adapt_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at adapting reasoning strategies to specific tasks.

Your job is to take the selected reasoning modules and rephrase/specify each one so that it directly addresses the given task.

Make each adaptation concrete and actionable for the specific problem at hand.""",
        ),
        (
            "human",
            """Rephrase and specify each reasoning module so that it better helps solving the task:

SELECTED module descriptions:
{selected_modules}

Task: {task_description}

Adapt each reasoning module description to better solve the task. Make them specific and actionable.""",
        ),
    ]
)


# Structure reasoning prompt
structured_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at creating structured reasoning plans.

Your job is to operationalize the adapted reasoning modules into a clear, step-by-step plan that can be followed to solve the task.

Create a JSON structure that defines the reasoning steps without actually solving the problem.""",
        ),
        (
            "human",
            """Operationalize the reasoning modules into a step-by-step reasoning plan in JSON format:

Here's an example:

Example task:
If you follow these instructions, do you return to the starting point? Always face forward. Take 1 step backward. Take 9 steps left. Take 2 steps backward. Take 6 steps forward. Take 4 steps forward. Take 4 steps backward. Take 3 steps right.

Example reasoning structure:
{{
    "Position after instruction 1": "",
    "Position after instruction 2": "",
    "Position after instruction n": "",
    "Is final position the same as starting position": ""
}}

Adapted module descriptions:
{adapted_modules}

Task: {task_description}

Implement a reasoning structure for solvers to follow step-by-step and arrive at correct answer.

Note: do NOT actually arrive at a conclusion in this pass. Your job is to generate a PLAN so that in the future you can fill it out and arrive at the correct conclusion for tasks like this.""",
        ),
    ]
)


# Final reasoning prompt
reasoning_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert problem solver who follows structured reasoning plans.

Your job is to use the provided reasoning structure to solve the given task step by step.

Fill in each step with specific reasoning and arrive at the correct answer.""",
        ),
        (
            "human",
            """Follow the step-by-step reasoning plan in JSON to correctly solve the task. Fill in the values following the keys by reasoning specifically about the task given. Do not simply rephrase the keys.

Reasoning Structure:
{reasoning_structure}

Task: {task_description}

Work through each step carefully and provide the final answer.""",
        ),
    ]
)
