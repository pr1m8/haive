from agents.rewoo.models import RewooPlan
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

system_prompt = """You are a planning agent that creates detailed, structured plans.
Your role is to break down tasks into specific, actionable steps using available tools.
Each step must be precise, properly numbered, and include evidence collection.
You must maintain proper sequencing of steps and ensure evidence references are correctly formatted.
Evidence references are critical for linking collected information to the plan.
Every step MUST include an `evidence_ref` starting with #E, even if no external tool is used."""
user_prompt = """Create a detailed plan for the following task. Your response must be valid JSON matching this structure:
{{
    "task": "task description",
    "steps": [
        {{
            "step_number": 1,
            "description": "detailed step description",
            "tool": "tool_name",
            "tool_input": "specific input",
            "evidence_ref": "#E1"
        }}
    ]
}}

Available Tools:
{tools}

Rules:
- Steps must be numbered sequentially starting at 1
- Each step must use exactly one tool
- Evidence references must be #E1, #E2, etc.
- Tool inputs must be specific and detailed
- Later steps can reference evidence from earlier steps using #E[number]

Task: {task}

{format_instructions}"""

messages = [("system", system_prompt), ("user", user_prompt)]

planning_output_parser = PydanticOutputParser(pydantic_object=RewooPlan)
planning_prompt = ChatPromptTemplate.from_messages(messages).partial(
    format_instructions=planning_output_parser.get_format_instructions()
)

SOLVE_PROMPT_TEMPLATE = PromptTemplate(
    """Solve the following task or problem. To solve the problem, we have made step-by-step Plan and \
        retrieved corresponding Evidence to each Plan. Use them with caution since long evidence might \
        contain irrelevant information.

        {step}

        Now solve the question or task according to provided Evidence above. Respond with the answer
        directly with no extra words.

        Task: {task}
        Response:"""
)
