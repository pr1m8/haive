"""Prompts for the Self-Discover Executor Agent."""

from langchain_core.prompts import PromptTemplate

EXECUTOR_SYSTEM_MESSAGE = """You are an expert at executing complex reasoning processes and synthesizing solutions.

Your role is to systematically work through structured reasoning plans, applying rigorous analysis at each step to arrive at well-founded conclusions. You excel at following logical processes, maintaining objectivity, and producing comprehensive solutions."""


EXECUTOR_PROMPT = PromptTemplate(
    input_variables=["reasoning_structure", "task_description"],
    template="""Execute the following structured reasoning plan to solve the given task.

REASONING STRUCTURE TO FOLLOW:
{reasoning_structure}

TASK TO SOLVE:
{task_description}

Work through each step systematically:

1. FOLLOW the reasoning structure step by step
2. ADDRESS all guiding questions thoroughly for each step
3. DOCUMENT your findings and reasoning at each step
4. BUILD upon previous steps as you progress
5. ASSESS confidence levels throughout the process

For each step, provide:
- Clear findings based on the guiding questions
- Evidence or reasoning supporting your conclusions
- Confidence assessment (0.0-1.0)
- How this step connects to previous and next steps

Finally, synthesize all step results into:
- A comprehensive final solution
- Supporting analysis explaining your reasoning path
- Alternative perspectives you considered
- Practical implementation recommendations
- Assessment of which success criteria were met

Be thorough, objective, and systematic in your execution. Show your work clearly so the reasoning process can be understood and validated.
""",
)
