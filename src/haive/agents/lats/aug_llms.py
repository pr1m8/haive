from langchain_core.output_parsers.openai_tools import (
    JsonOutputToolsParser,
    PydanticToolsParser,
)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import chain as as_runnable
from src.haive.agents.lats.models import Reflection
from langchain_core.messages import AIMessage
from src.haive.core.aug_llm.base import AugLLMConfig


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
    prompt_template=REFLECTION_PROMPT_TEMPLATE,
    output_parser=reflection_output_parser,
    #llm_config=AzureLLMConfig(model="gpt-4o",parameters={"temperature": 0.7})
    tools=[Reflection],
    
)
reflection_llm_chain = (
    REFLECTION_PROMPT_TEMPLATE
    | llm.bind_tools(tools=[Reflection], tool_choice="Reflection").with_config(
        run_name="Reflection"
    )
    | PydanticToolsParser(tools=[Reflection])
)


@as_runnable
def reflection_chain(inputs) -> Reflection:
    tool_choices = reflection_llm_chain.invoke(inputs)
    reflection = tool_choices[0]
    if not isinstance(inputs["candidate"][-1], AIMessage):
        reflection.found_solution = False
    return reflection