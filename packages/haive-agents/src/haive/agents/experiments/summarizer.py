from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import RemoveMessage
from langchain_core.messages.utils import count_tokens_approximately, trim_messages
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import create_react_agent
from langgraph.prebuilt.chat_agent_executor import AgentState
from langmem.short_term import SummarizationNode

from haive.agents.simple import SimpleAgent

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that summarizes text."),
        ("user", "{text}"),
    ]
)
