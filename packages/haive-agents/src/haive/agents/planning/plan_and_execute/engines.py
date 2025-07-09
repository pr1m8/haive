from agents.plan_and_execute.models import Act, Plan
from haive.core.engine.aug_llm import AugLLMConfig
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

EXECUTOR_PROMPT = """You are a helpful assistant"""
EXECUTOR_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", EXECUTOR_PROMPT),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
PLANNER_PROMPT = """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps."""
PLANNER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            PLANNER_PROMPT,
        ),
        ("placeholder", "{messages}"),
    ]
)
planner_aug_llm_config = AugLLMConfig(
    name="planner",
    prompt_template=PLANNER_PROMPT_TEMPLATE,
    structured_output_model=Plan,
)
REPLANNER_PROMPT = """For the given objective, come up with a simple step by step plan. \
This plan should involve individual tasks, that if executed correctly will yield the correct answer. Do not add any superfluous steps. \
The result of the final step should be the final answer. Make sure that each step has all the information needed - do not skip steps.

Your objective was this:
{input}

Your original plan was this:
{plan}

You have currently done the follow steps:
{past_steps}

Update your plan accordingly. If no more steps are needed and you can return to the user, then respond with that. Otherwise, fill out the plan. Only add steps to the plan that still NEED to be done. Do not return previously done steps as part of the plan.
"""

REPLANNER_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        ("system", REPLANNER_PROMPT),
        ("placeholder", "{messages}"),
    ]
)

replanner_aug_llm_config = AugLLMConfig(
    name="replanner",
    prompt_template=REPLANNER_PROMPT_TEMPLATE,
    structured_output_model=Act,
)
