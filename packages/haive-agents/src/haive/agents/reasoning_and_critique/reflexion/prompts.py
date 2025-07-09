import datetime

from agents.reflexion.models import AnswerQuestion, ReviseAnswer
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# from haive_agents.reflexion.responder_with_retries import ResponderWithRetries


actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are {role}.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. Recommend search queries to research information and improve your answer.""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "user",
            "\n\n<system>Reflect on the user's original question and the"
            " actions taken thus far. Respond using the {function_name} function.</reminder>",
        ),
    ]
).partial(
    role="expert researcher",
    time=lambda: datetime.datetime.now().isoformat(),
)

initial_answer_chain = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer.",
    function_name=AnswerQuestion.__name__,
)  # | llm.bind_tools(tools=[AnswerQuestion])
# validator = PydanticToolsParser(tools=[AnswerQuestion])


revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""


revision_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
)  # | llm.bind_tools(tools=[ReviseAnswer])
# revision_validator = PydanticToolsParser(tools=[ReviseAnswer])

# revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)
