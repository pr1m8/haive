from agents.reflexion.models import AnswerQuestion, ReviseAnswer

# from langchain_core.tools import PydanticToolsParser
from agents.reflexion.prompts import actor_prompt_template
from haive.core.engine.aug_llm import AugLLMConfig

initial_answer_prompt = actor_prompt_template.partial(
    first_instruction="Provide a detailed 1000 word essay.",
    function_name=AnswerQuestion.__name__,
)
initial_answer_chain_config = AugLLMConfig(
    tools=[AnswerQuestion], prompt_template=initial_answer_prompt, name="responder"
)


revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""


revision_prompt = actor_prompt_template.partial(
    first_instruction=revise_instructions,
    function_name=ReviseAnswer.__name__,
)
revision_chain_config = AugLLMConfig(
    tools=[ReviseAnswer], prompt_template=revision_prompt, name="revisior"
)
