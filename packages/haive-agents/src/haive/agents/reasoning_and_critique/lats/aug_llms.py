from agents.lats.models import Reflection
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

REFLECTION_PROMPT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Reflect and grade the assistant response to the user question below.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="candidate"),
    ]
)
reflection_output_parser = PydanticToolsParser(tools=[Reflection])

reflection_llm_config = AugLLMConfig(
    name="reflection_chain",
    prompt_template=REFLECTION_PROMPT_TEMPLATE,
    # output_parser=reflection_output_parser)
    structured_output_model=Reflection,
)


prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an AI assistant.",
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="messages", optional=True),
    ]
)
from langchain.chat_models import BaseChatModel

a = BaseChatModel
parser = JsonOutputToolsParser(return_id=True)
initial_answer_llm_config = AugLLMConfig(
    name="initial_answer_chain", prompt_template=prompt_template, output_parser=parser
)
