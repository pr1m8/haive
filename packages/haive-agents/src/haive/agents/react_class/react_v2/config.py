"""Configuration for the ReactAgent."""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import BaseTool, StructuredTool, Tool
from pydantic import BaseModel, Field, field_validator

from haive.agents.react_class.react_v2.state import ReactAgentState
from haive.agents.simple.config import SimpleAgentConfig

logger = logging.getLogger(__name__)

ToolsInput = Union[
    list[BaseTool | StructuredTool | Tool | type[BaseModel] | Callable],
    dict[
        str,
        BaseTool
        | StructuredTool
        | Tool
        | type[BaseModel]
        | Callable
        | list[BaseTool | StructuredTool | Tool | type[BaseModel] | Callable],
    ],
]


class ReactAgentConfig(SimpleAgentConfig):
    """Configuration for a React agent that can use tools and follow ReAct reasoning pattern."""

    tools: ToolsInput = Field(
        default_factory=list,
        description="Tools available to the agent. Can be a list or a dict mapping node names to tools.",
    )

    tool_choice: str | None = Field(
        default=None, description="Force the agent to use a specific tool."
    )

    max_iterations: int = Field(
        default=10, description="Maximum number of iterations for the agent."
    )

    max_retries: int = Field(
        default=3, description="Maximum number of retries for tool execution failures."
    )

    retry_delay: float = Field(
        default=0.5, description="Delay between retry attempts in seconds."
    )

    parallel_tool_execution: bool = Field(
        default=False, description="Whether to execute multiple tool calls in parallel."
    )

    # Add missing fields for structured output
    use_structured_output_node: bool = Field(
        default=False,
        description="Whether to use a structured output node for final responses.",
    )

    structured_output_model: type[BaseModel] | None = Field(
        default=None, description="Pydantic model class for structured output."
    )

    # Override state schema with react-specific schema
    state_schema: type[BaseModel] = Field(
        default=ReactAgentState, description="Schema for the agent state."
    )

    agent_node_name: str = Field(
        default="agent", description="Name for the agent (LLM) node"
    )

    tools_node_prefix: str = Field(
        default="tool_", description="Prefix for auto-generated tool node names"
    )

    @classmethod
    def from_tools(
        cls,
        tools: ToolsInput,
        model: str = "gpt-4o",
        system_prompt: str | None = None,
        name: str | None = None,
        temperature: float = 0.7,
        parallel_tool_execution: bool = False,
        max_iterations: int = 10,
        max_retries: int = 3,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig with tools from scratch.

        Args:
            tools: Tools to use (list or dict)
            model: Model name to use
            system_prompt: Optional system prompt
            name: Optional agent name
            temperature: Temperature for generation
            parallel_tool_execution: Whether to execute tools in parallel
            max_iterations: Maximum number of reasoning iterations
            max_retries: Maximum number of retries for tool failures
            **kwargs: Additional kwargs for the config

        Returns:
            ReactAgentConfig instance
        """
        # Create default system prompt if not provided
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant with access to tools. "
                "Use these tools to answer the user's questions when needed. "
                "Think step by step to determine which tools to use and in what order."
            )

        # Create LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create prompt template with tool descriptions
        messages = [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Flatten tools to a list for AugLLMConfig if it's a dict
        flat_tools = []
        if isinstance(tools, dict):
            for tool_set in tools.values():
                if isinstance(tool_set, list | tuple):
                    flat_tools.extend(tool_set)
                else:
                    flat_tools.append(tool_set)
        else:
            flat_tools = tools

        # Create AugLLMConfig
        aug_llm = AugLLMConfig(
            name=f"{name or 'react'}_llm",
            llm_config=llm_config,
            prompt_template=prompt_template,
            tools=flat_tools,  # Add tools to AugLLMConfig
        )

        # Update kwargs with tools and settings
        kwargs.update(
            {
                "tools": tools,
                "engine": aug_llm,
                "system_prompt": system_prompt,
                "parallel_tool_execution": parallel_tool_execution,
                "max_iterations": max_iterations,
                "max_retries": max_retries,
            }
        )

        # Create config
        return cls(
            name=name or f"react_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            **kwargs,
        )

    @classmethod
    def with_structured_output(
        cls,
        model_class: type[BaseModel],
        tools: ToolsInput,
        system_prompt: str | None = None,
        name: str | None = None,
        parallel_tool_execution: bool = False,
        **kwargs,
    ) -> "ReactAgentConfig":
        """Create a ReactAgentConfig with structured output and tools.

        Args:
            model_class: Pydantic model class for structured output
            tools: Tools to use (list or dict)
            system_prompt: Optional system prompt
            name: Optional agent name
            parallel_tool_execution: Whether to execute tools in parallel
            **kwargs: Additional kwargs for the config

        Returns:
            ReactAgentConfig instance
        """
        # Create default system prompt if not provided
        if system_prompt is None:
            system_prompt = (
                "You are a helpful assistant with access to tools. "
                "Use these tools to answer the user's questions when needed. "
                "Think step by step to determine which tools to use and in what order. "
                "Your final response must be formatted according to the specified structure."
            )

        # Add additional parameters for structured output
        kwargs.update(
            {
                "structured_output_model": model_class,
                "use_structured_output_node": True,
                "parallel_tool_execution": parallel_tool_execution,
            }
        )

        # Use from_tools to create the config
        config = cls.from_tools(
            tools=tools,
            system_prompt=system_prompt,
            name=name or f"structured_react_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            **kwargs,
        )

        return config

    @field_validator("tools")
    def validate_tools(self, v):
        """Validate that tools are properly configured."""
        if not v:
            logger.warning("No tools provided for ReactAgent")
        return v
