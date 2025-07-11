"""Configuration for the ReactAgent - a tool-using agent with ReAct pattern.

This module defines the configuration class for ReactAgent, which implements the
ReAct (Reasoning and Acting) pattern for tool-using agents.
"""

import logging
from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.state_schema import StateSchema
from langchain_core.tools import BaseTool
from langgraph.pregel import RetryPolicy
from pydantic import Field, model_validator

# Setup logging
logger = logging.getLogger(__name__)


class ReactAgentConfig(AgentConfig):
    """Configuration for a ReAct agent with tool integration.

    This agent implements the Reasoning+Acting pattern:
    1. Reasoning about what to do based on the input
    2. Acting by using tools when necessary
    3. Observing the results and continuing the process
    """

    # Required engine for reasoning
    engine: AugLLMConfig = Field(description="The LLM engine to use for reasoning")

    # Tools available to the agent
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools that the agent can use"
    )

    # Optional schemas
    state_schema: type[StateSchema] | None = Field(
        default=None,
        description="Schema for agent state (auto-derived if not provided)",
    )

    # Node names
    reasoning_node_name: str = Field(
        default="reasoning", description="Name for the reasoning node"
    )

    tool_node_name: str = Field(
        default="tools", description="Name for the tool execution node"
    )

    # System prompts
    system_prompt: str = Field(
        default=(
            "You are a helpful assistant with access to tools. "
            "When you need information or need to perform an action, use the appropriate tool. "
            "First think about what you need to accomplish, then select the right tool for the task."
        ),
        description="System prompt for the agent",
    )

    # Retry policies
    reasoning_retry: RetryPolicy | None = Field(
        default=None, description="Retry policy for reasoning node"
    )

    tool_retry: RetryPolicy | None = Field(
        default=None, description="Retry policy for tool execution node"
    )

    # Maximum iterations
    max_iterations: int = Field(
        default=10, description="Maximum number of reasoning-tool cycles"
    )

    # Visualization
    visualize: bool = Field(default=True, description="Whether to visualize the graph")

    # Tool configuration
    include_tool_names_in_prompt: bool = Field(
        default=True,
        description="Whether to explicitly include tool names in the system prompt",
    )

    model_config = {"arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def setup_defaults(self):
        """Set up default retry policies if not provided."""
        if self.reasoning_retry is None:
            self.reasoning_retry = RetryPolicy(
                initial_interval=1.0,
                backoff_factor=2.0,
                max_interval=16.0,
                max_attempts=3,
                jitter=True,
            )

        if self.tool_retry is None:
            self.tool_retry = RetryPolicy(
                initial_interval=0.5,
                backoff_factor=1.5,
                max_interval=8.0,
                max_attempts=2,
                jitter=True,
            )

        # Update system prompt with tool information if requested
        if self.include_tool_names_in_prompt and self.tools:
            tool_names = [f"- {tool.name}: {tool.description}" for tool in self.tools]
            tool_section = "\n\nYou have access to the following tools:\n" + "\n".join(
                tool_names
            )
            self.system_prompt += tool_section

        return self

    def get_tool_schemas(self) -> dict[str, Any]:
        """Get the input and output schemas for all tools.

        Returns:
            Dictionary mapping tool names to their schemas
        """
        tool_schemas = {}

        for tool in self.tools:
            schema_info = {"description": tool.description}

            # Get input schema
            if hasattr(tool, "args_schema"):
                schema_info["input_schema"] = tool.args_schema

            # Try to extract return type if possible
            if hasattr(tool, "return_type"):
                schema_info["return_type"] = tool.return_type

            tool_schemas[tool.name] = schema_info

        return tool_schemas

    def get_tools_by_name(self) -> dict[str, BaseTool]:
        """Get a dictionary mapping tool names to tools.

        Returns:
            Dictionary mapping tool names to tool instances
        """
        return {tool.name: tool for tool in self.tools}

    def build_agent(self):
        """Build and return a ReactAgent instance.

        Returns:
            Configured ReactAgent
        """
        from haive.agents.react_class.react_v3.agent import ReactAgent

        return ReactAgent(self)
