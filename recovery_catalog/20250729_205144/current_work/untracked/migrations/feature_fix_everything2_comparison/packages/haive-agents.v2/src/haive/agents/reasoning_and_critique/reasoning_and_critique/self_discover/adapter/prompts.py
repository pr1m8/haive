"""Prompts for the Self-Discover Adapter Agent."""

from langchain_core.prompts import PromptTemplate

ADAPTER_SYSTEM_MESSAGE = """You are an expert at adapting abstract reasoning frameworks to specific problem contexts.

Your role is to take selected reasoning modules and transform them into concrete, actionable steps tailored to the specific task at hand. You excel at bridging the gap between general cognitive strategies and practical application."""


ADAPTER_PROMPT = PromptTemplate(
    input_variables=["selected_modules", "task_description"],
    template="""Adapt the following reasoning modules to be specifically applicable to the given task.

SELECTED REASONING MODULES:
{selected_modules}

TASK TO SOLVE:
{task_description}

For each selected module, create a task-specific adaptation that:

1. PRESERVES the core reasoning approach of the module
2. TRANSLATES abstract concepts into concrete, task-relevant steps
3. PROVIDES specific questions or checkpoints to guide thinking
4. IDENTIFIES what insights or outcomes to expect

Your adaptations should:
- Be concrete and actionable, not abstract
- Include specific steps or questions relevant to THIS task
- Show clear connection to the task requirements
- Work together as an integrated approach

Transform each module from a general framework into a specific tool for solving this particular problem.
""",
)
