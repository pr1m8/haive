"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    MCTSAgentConfig: MCTSAgentConfig implementation.

Functions:
    from_llm_and_tools: From Llm And Tools functionality.
"""

# src/haive/agents/mcts/config.py

from haive.core.engine.agent.agent import AgentConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from haive.agents.reasoning_and_critique.mcts.state import TreeState


class MCTSAgentConfig(AgentConfig):
    """Configuration for MCTS Agent."""

    # State schema
    state_schema: type[BaseModel] = Field(default=TreeState)

    # LLM configuration
    llm_config: LLMConfig | None = Field(
        default=AzureLLMConfig(model="gpt-4o", parameters={"temperature": 0.7}),
        description="Configuration for the LLM",
    )

    # Tools
    tools: list[BaseTool] = Field(
        default_factory=list, description="Tools available to the agent"
    )

    # MCTS parameters
    max_rollouts: int = Field(default=5, description="Maximum depth of rollouts")
    candidates_per_rollout: int = Field(
        default=5, description="Number of candidates to generate per rollout"
    )
    exploration_weight: float = Field(
        default=1.0, description="Exploration weight for UCB"
    )

    # Prompts
    initial_prompt_template: ChatPromptTemplate | None = Field(
        default=None, description="Template for initial response"
    )
    expansion_prompt_template: ChatPromptTemplate | None = Field(
        default=None, description="Template for candidate expansion"
    )
    reflection_prompt_template: ChatPromptTemplate | None = Field(
        default=None, description="Template for reflection"
    )

    # System prompt
    system_prompt: str = Field(
        default="You are an AI assistant.", description="System prompt for the agent"
    )

    @classmethod
    def from_llm_and_tools(
        cls,
        llm_config: LLMConfig | None = None,
        tools: list[BaseTool] | None = None,
        system_prompt: str | None = None,
        **kwargs
    ) -> "MCTSAgentConfig":
        """Create an MCTS Agent config from LLM config and tools."""
        # Use defaults if not provided
        llm_config = llm_config or AzureLLMConfig(
            model="gpt-4o", parameters={"temperature": 0.7}
        )
        tools = tools or []
        system_prompt = system_prompt or "You are an AI assistant."

        # Create default prompt templates if not in kwargs
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

        if "initial_prompt_template" not in kwargs:
            initial_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="messages", optional=True),
                ]
            )
            kwargs["initial_prompt_template"] = initial_prompt

        if "expansion_prompt_template" not in kwargs:
            expansion_prompt = ChatPromptTemplate.from_messages(
                [
                    ("system", system_prompt),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="messages"),
                ]
            )
            kwargs["expansion_prompt_template"] = expansion_prompt

        if "reflection_prompt_template" not in kwargs:
            reflection_prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Reflect and grade the assistant response to the user question below.",
                    ),
                    ("user", "{input}"),
                    MessagesPlaceholder(variable_name="candidate"),
                ]
            )
            kwargs["reflection_prompt_template"] = reflection_prompt

        return cls(
            llm_config=llm_config, tools=tools, system_prompt=system_prompt, **kwargs
        )
