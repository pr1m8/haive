"""Prompts for the Self-Discover Selector Agent."""

from langchain_core.prompts import PromptTemplate

SELECTOR_SYSTEM_MESSAGE = """You are an expert problem analyst specializing in selecting optimal reasoning strategies.

Your role is to analyze complex problems and identify the most relevant cognitive approaches from a comprehensive set of reasoning modules. You excel at understanding problem structures and matching them with appropriate analytical frameworks."""


SELECTOR_PROMPT = PromptTemplate(
    input_variables=["available_modules", "task_description"],
    template="""Analyze the following task and select the most relevant reasoning modules to solve it effectively.

AVAILABLE REASONING MODULES:
{available_modules}

TASK TO SOLVE:
{task_description}

Please select 3-5 reasoning modules that would be most effective for solving this task.

For each selected module:
1. Identify the module by its number and name
2. Explain specifically why this module is relevant for THIS task
3. Describe how it will contribute to finding a solution
4. Consider how it complements other selected modules

Focus on:
- Problem-specific relevance
- Complementary approaches that work well together
- Coverage of different aspects of the problem
- Practical applicability to the task

Your selection should form a comprehensive toolkit for addressing all aspects of the task.""",
)
