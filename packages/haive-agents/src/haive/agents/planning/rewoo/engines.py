"""Augmented LLM configurations for the ReWOO agent.

This module defines the LLM configurations for the planner and solver
components of the ReWOO agent.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.prompts import ChatPromptTemplate

# Planner prompt template that takes a task and available tools
planner_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful planning assistant that creates detailed step-by-step plans.

Each step should be specific and actionable, using available tools when needed.
You can use the following tools:

{tools}

IMPORTANT: When referring to tools, you MUST use EXACTLY one of the following tool names:
- tavily_search_tool (NOT tavily_search)
- tavily_search_context
- tavily_qna
- tavily_extract
- LLM

For each step, you must include:
1. A clear description of what to do
2. An evidence reference (e.g., #E1, #E2) to track results
3. One or more tool calls that should be used for this step

Your output must be a valid JSON object with a 'steps' list containing:
- step_number: the step number (integer)
- description: a clear description of the step
- evidence_ref: a unique identifier starting with #E (e.g., #E1)
- tool_calls: a list of tool calls to execute, each with 'name' and 'input' fields

Example plan:
```
{{
  "steps": [
    {{
      "step_number": 1,
      "description": "Search for information about langgraph on GitHub",
      "evidence_ref": "#E1",
      "tool_calls": [
        {{
          "name": "tavily_search_tool",
          "input": {{
            "query": "langgraph GitHub repository"
          }}
        }}
      ]
    }},
    {{
      "step_number": 2,
      "description": "Extract key information from the search results",
      "evidence_ref": "#E2",
      "tool_calls": [
        {{
          "name": "LLM",
          "input": "Analyze the search results and extract the most important information about langgraph."
        }}
      ]
    }}
  ]
}}
```

Only include steps that are necessary to complete the task successfully.
""",
        ),
        ("user", "{task}"),
    ]
)

# Solver prompt template that takes a task, step, and evidence
solver_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful assistant that solves tasks using evidence collected in earlier steps.

You will be given:
1. The original task
2. A specific step from the plan
3. Evidence collected for that step

Your job is to:
1. Analyze the evidence
2. Extract relevant information
3. Provide a clear, concise solution for this specific step

Present your answer in a clear, helpful format that directly addresses what was asked in the step.
""",
        ),
        (
            "user",
            """
Task: {task}
Step {step_number}: {step_description}
Evidence: {evidence}

Please analyze this evidence and provide a solution for this step.
""",
        ),
    ]
)

# Initialize AugLLM configurations for planner and solver
# IMPORTANT: We're NOT passing tool instances to the AugLLMConfig
rewoo_aug_llm_config = AugLLMConfig(
    name="rewoo_planner",
    llm_config=AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 4096}
    ),
    prompt_template=planner_prompt,
    # No tools - these will be set in the agent config
    tools=None,
)

solve_aug_llm_config = AugLLMConfig(
    name="rewoo_solver",
    llm_config=AzureLLMConfig(
        model="gpt-4o", parameters={"temperature": 0.7, "max_tokens": 4096}
    ),
    prompt_template=solver_prompt,
    # No tools - these will be set in the agent config
    tools=None,
)
