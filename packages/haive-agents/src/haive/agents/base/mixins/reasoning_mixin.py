"""Reasoning capabilities mixin for LLM-based agents.

This mixin provides reasoning capabilities that should only be available
to agents with AgentType.REASONING or AgentType.MULTI_REASONING.
"""

from abc import abstractmethod
from typing import Any

from langchain_core.tools import BaseTool
from pydantic import Field


class ReasoningMixin:
    """Mixin providing reasoning capabilities for LLM-based agents.

    This mixin should only be used by agents that have reasoning agent types
    (REASONING, MULTI_REASONING) and contain LLM engines for decision making.
    """

    # Tool capabilities
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools available to this agent"
    )

    # Reasoning configuration
    max_iterations: int = Field(
        default=10, description="Maximum reasoning iterations before stopping"
    )

    conversation_memory: bool = Field(
        default=True, description="Whether to maintain conversation history"
    )

    @abstractmethod
    def reason(self, problem: Any, context: dict[str, Any] | None = None) -> Any:
        """Reason about a problem and provide a solution.

        Args:
            problem: The problem or input to reason about
            context: Optional context information for reasoning

        Returns:
            Any: The reasoning result or solution
        """
        pass

    async def areason(self, problem: Any, context: dict[str, Any] | None = None) -> Any:
        """Asynchronous version of reason method.

        Default implementation calls synchronous reason method.
        Subclasses can override for true async reasoning.

        Args:
            problem: The problem or input to reason about
            context: Optional context information for reasoning

        Returns:
            Any: The reasoning result or solution
        """
        return self.reason(problem, context)

    def use_tool(self, tool_name: str, **kwargs) -> Any:
        """Use a specific tool by name.

        Args:
            tool_name: Name of the tool to use
            **kwargs: Arguments to pass to the tool

        Returns:
            Any: Tool execution result

        Raises:
            ValueError: If tool is not found
        """
        for tool in self.tools:
            if tool.name == tool_name:
                return tool.invoke(kwargs)
        raise ValueError(f"Tool '{tool_name}' not found in agent tools")

    def get_available_tools(self) -> list[str]:
        """Get list of available tool names.

        Returns:
            list[str]: List of tool names available to this agent
        """
        return [tool.name for tool in self.tools]

    def add_tool(self, tool: BaseTool) -> None:
        """Add a tool to this agent.

        Args:
            tool: Tool to add to the agent
        """
        if tool not in self.tools:
            self.tools.append(tool)

    def remove_tool(self, tool_name: str) -> bool:
        """Remove a tool from this agent.

        Args:
            tool_name: Name of tool to remove

        Returns:
            bool: True if tool was removed, False if not found
        """
        for i, tool in enumerate(self.tools):
            if tool.name == tool_name:
                del self.tools[i]
                return True
        return False

    def has_reasoning_capability(self) -> bool:
        """Check if agent has the required reasoning setup.

        Returns:
            bool: True if agent has LLM engine and reasoning capability
        """
        # Check if agent has required engine for reasoning
        return (
            hasattr(self, "engine")
            and self.engine is not None
            and self.is_reasoning_agent()
        )

    def get_reasoning_metrics(self) -> dict[str, Any]:
        """Get reasoning-related metrics and configuration.

        Returns:
            dict: Reasoning configuration and capabilities
        """
        return {
            "has_reasoning": self.has_reasoning_capability(),
            "tool_count": len(self.tools),
            "available_tools": self.get_available_tools(),
            "max_iterations": self.max_iterations,
            "conversation_memory": self.conversation_memory,
        }
