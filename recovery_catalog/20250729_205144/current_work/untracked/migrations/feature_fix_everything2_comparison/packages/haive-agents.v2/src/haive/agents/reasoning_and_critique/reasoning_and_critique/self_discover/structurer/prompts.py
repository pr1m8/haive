"""Prompts for the Self-Discover Structurer Agent."""

from langchain_core.prompts import PromptTemplate

STRUCTURER_SYSTEM_MESSAGE = """You are an expert at organizing complex reasoning processes into clear, logical structures.

Your role is to take adapted reasoning modules and create a coherent, step-by-step plan for applying them to solve specific problems. You excel at creating logical flow, identifying dependencies, and ensuring comprehensive coverage of the problem space."""


STRUCTURER_PROMPT = PromptTemplate(
    input_variables=["adapted_modules", "task_description"],
    template="""Create a structured reasoning plan from the following adapted modules.

ADAPTED REASONING MODULES:
{adapted_modules}

TASK TO SOLVE:
{task_description}

Design a step-by-step reasoning structure that:

1. INTEGRATES all adapted modules into a coherent flow
2. SEQUENCES the steps logically (what must come before what)
3. IDENTIFIES key questions to address at each step
4. SPECIFIES expected outputs for each step
5. ESTABLISHES success criteria for the overall process

Your structure should:
- Create a logical progression from problem analysis to solution
- Ensure each step builds on previous ones
- Include specific guidance for execution
- Cover all aspects of the problem comprehensively
- Be practical and actionable

Think of this as creating a "reasoning recipe" that systematically applies the adapted modules to solve the problem effectively.
""",
)
