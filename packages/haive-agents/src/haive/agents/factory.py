from typing import Any

from agents.simple.config import SimpleAgentConfig
from agents.simple.state import SimpleAgentState
from haive.core.engine.agent.persistence.base import MemoryCheckpointerConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


def create_simple_agent(
    name: str,
    system_message: str = "You are a helpful assistant",
    model: str = "gpt-4o",
    use_chat_history: bool = True,
    persistence_config: Any | None = None,
    **kwargs,
) -> SimpleAgentConfig:
    """Factory function to create a SimpleAgent configuration.

    Args:
        name: Name for the agent
        system_message: System message/instructions for the agent
        model: Model to use (default: gpt-4o)
        use_chat_history: Whether to use chat history
        persistence_config: Optional persistence configuration
        **kwargs: Additional parameters for SimpleAgentConfig

    Returns:
        Configured SimpleAgentConfig
    """
    # Create prompt template with system message and messages placeholder
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    # Create LLM engine
    llm_engine = AugLLMConfig(
        name=f"{name}_llm",
        model=model,
        system_message=system_message,
        prompt_template=prompt,
    )

    # Set up default persistence if not provided
    if persistence_config is None:
        persistence_config = MemoryCheckpointerConfig()

    # Create and return the agent config
    return SimpleAgentConfig(
        name=name,
        engine=llm_engine,
        state_schema=SimpleAgentState,
        use_chat_history=use_chat_history,
        persistence=persistence_config,
        **kwargs,
    ).build_agent()
