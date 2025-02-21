from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import chain as as_runnable
from src.haive.agents.lats.models import Reflection
from langchain_core.messages import AIMessage
from src.haive.core.aug_llm.base import AugLLMConfig,compose_runnable


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

reflection_aug_llm_config = AugLLMConfig(
    name="reflection_chain",
    prompt_template=REFLECTION_PROMPT_TEMPLATE,  
    tools=[Reflection],  # Structured tools as classes
    #tool_kwargs={"Reflection": {"some_param": "value"}},  # Tool instantiation kwargs
    bind_tools_kwargs={"tool_choice": "Reflection"},  # bind_tools kwargs
    bind_tools_config={"run_name": "Reflection"},  # bind_tools config
    output_parser=PydanticToolsParser(tools=[Reflection]),  # Output parser
)


