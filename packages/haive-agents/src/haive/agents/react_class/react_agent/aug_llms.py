from datetime import datetime

from haive.core.engine.aug_llm import AugLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

default_react_system_message = "You are a helpful AI assistant, capable of using tools and escalating tasks as needed. You can invoke tools multiple times if prompted to perform a task, and continue on prompting yourself until the task is done. The cureent date is {}".format(
    datetime.now().strftime("%Y-%m-%d")
)
default_react_prompt_template_config = ChatPromptTemplate(
    messages=[
        ("system", default_react_system_message),
        MessagesPlaceholder(variable_name="messages"),
    ]
)
# print(PromptTemplateFactory(default_react_prompt_template_config).create_prompt())
default_react_tools = [tavily_search_tool]

default_react_llm_runnable_config = AugLLMConfig(
    name="react_agent",
    prompt_template=default_react_prompt_template_config,
    tools=default_react_tools,
)
