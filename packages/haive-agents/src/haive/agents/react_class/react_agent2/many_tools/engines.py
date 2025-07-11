from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from haive.agents.react_class.react_agent2.many_tools.models import QueryForTools

tool_query_system_messagege = SystemMessage(
    "Given this conversation, generate a query for additional tools. "
    "The query should be a short string containing what type of information "
    "is needed. If no further information is needed, "
    "set more_information_needed False and populate a blank string for the query."
)
tool_query_prompt_template = ChatPromptTemplate.from_messages(
    [tool_query_system_messagege, MessagesPlaceholder(variable_name="messages")]
)
tool_query_builder_aug_llm_config = AugLLMConfig(
    prompt_template=tool_query_prompt_template,
    structured_output_model=QueryForTools,
)
