"""Enhanced_Simple_Agent core module.

This module provides enhanced simple agent functionality for the Haive framework.

Classes:
    EnhancedSimpleAgent: EnhancedSimpleAgent implementation.

Functions:
    calculator: Calculator functionality.
    create_default_engine: Create Default Engine functionality.
    setup_agent: Setup Agent functionality.
"""

# src/haive/agents/simple/enhanced_simple_agent.py

"""Enhanced SimpleAgent with engine-focused generics.

This implements SimpleAgent using the enhanced agent pattern with engine generics.
SimpleAgent becomes essentially Agent[AugLLMConfig] as requested.
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from pydantic import Field, model_validator

from haive.agents.base.enhanced_agent import Agent

logger = logging.getLogger(__name__)


# ========================================================================
# ENHANCED SIMPLE AGENT - Clean Agent[AugLLMConfig] implementation
# ========================================================================


class EnhancedSimpleAgent(Agent[AugLLMConfig]):
    """Enhanced SimpleAgent that is essentially Agent[AugLLMConfig].

    This is the cleanest implementation - SimpleAgent is just an Agent
    specialized for AugLLMConfig as its engine type. All the complex
    functionality comes from the base enhanced Agent class.

    The engine-focused generic pattern provides:
    - Type safety: engine is always AugLLMConfig
    - Clean design: SimpleAgent = Agent[AugLLMConfig]
    - Flexibility: Can still use tools, structured output, etc.

    Attributes:
        temperature: LLM temperature (0.0-2.0), synced to engine.
        max_tokens: Maximum tokens for responses, synced to engine.
        system_message: System prompt, synced to engine.
        tools: List of tools available to the agent.

    Examples:
        Basic usage::

            agent = EnhancedSimpleAgent(
                name="assistant",
                temperature=0.7,
                system_message="You are a helpful assistant"
            )
            response = await agent.arun("Hello!")

        With tools::

            from langchain_core.tools import tool

            @tool
            def calculator(expression: str) -> str:
                return str(eval(expression))

            agent = EnhancedSimpleAgent(
                name="math_helper",
                tools=[calculator]
            )
            result = await agent.arun("What is 15 * 23?")
    """

    # ========================================================================
    # SIMPLE AGENT CONVENIENCE FIELDS
    # ========================================================================

    # These sync to the AugLLMConfig engine
    temperature: float | None = Field(
        default=None, ge=0.0, le=2.0, description="LLM temperature (0.0-2.0)"
    )

    max_tokens: int | None = Field(
        default=None, ge=1, description="Maximum tokens for LLM responses"
    )

    system_message: str | None = Field(
        default=None, description="System message for the LLM"
    )

    tools: list[Any] = Field(
        default_factory=list, description="Tools available to the agent"
    )

    # ========================================================================
    # ENGINE SETUP - ENHANCED PATTERN
    # ========================================================================

    @model_validator(mode="before")
    @classmethod
    def create_default_engine(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Create AugLLMConfig engine if not provided."""
        if not isinstance(values, dict):
            return values

        # If no engine provided, create AugLLMConfig
        if "engine" not in values or values["engine"] is None:
            # Extract config from convenience fields
            config_kwargs = {}

            if "temperature" in values and values["temperature"] is not None:
                config_kwargs["temperature"] = values["temperature"]

            if "max_tokens" in values and values["max_tokens"] is not None:
                config_kwargs["max_tokens"] = values["max_tokens"]

            if "system_message" in values and values["system_message"] is not None:
                config_kwargs["system_message"] = values["system_message"]

            if values.get("tools"):
                config_kwargs["tools"] = values["tools"]

            # Create the engine
            values["engine"] = AugLLMConfig(**config_kwargs)

        return values

    def setup_agent(self) -> None:
        """Sync convenience fields to the AugLLMConfig engine."""
        # Ensure we have an engine
        if not self.engine:
            self.engine = AugLLMConfig()

        # Type assertion - we know it's AugLLMConfig
        engine: AugLLMConfig = self.engine

        # Sync fields to engine
        if self.temperature is not None:
            engine.temperature = self.temperature

        if self.max_tokens is not None:
            engine.max_tokens = self.max_tokens

        if self.system_message is not None:
            engine.system_message = self.system_message

        if self.tools:
            engine.tools = self.tools

        # Enable schema generation
        self.set_schema = True

        # Log setup
        if self.verbose:
            logger.info(
                f"EnhancedSimpleAgent setup complete: {self.name} "
                f"(temp={self.temperature}, tools={len(self.tools)})"
            )

    # ========================================================================
    # GRAPH BUILDING - MINIMAL IMPLEMENTATION
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build the simple agent graph."""
        graph = BaseGraph(name=self.name)

        # Add engine node (the heart of SimpleAgent)
        engine_node = EngineNodeConfig(name="agent_node", engine=self.engine)
        graph.add_node("agent_node", engine_node)
        graph.add_edge(START, "agent_node")

        # Add tool node if we have tools
        if self.tools:
            tool_node = ToolNodeConfig(name="tool_node", tools=self.tools)
            graph.add_node("tool_node", tool_node)

            # Conditional routing based on tool calls
            def has_tool_calls(state: dict[str, Any]) -> Literal["tools", "end"]:
                messages = state.get("messages", [])
                if messages:
                    last_msg = messages[-1]
                    if isinstance(last_msg, AIMessage) and last_msg.tool_calls:
                        return "tools"
                return "end"

            graph.add_conditional_edges(
                "agent_node", has_tool_calls, {"tools": "tool_node", "end": END}
            )

            # Tools always return to end
            graph.add_edge("tool_node", END)
        else:
            # No tools - straight to end
            graph.add_edge("agent_node", END)

        return graph

    # ========================================================================
    # TYPE-SAFE ENGINE ACCESS
    # ========================================================================

    def get_aug_llm_config(self) -> AugLLMConfig:
        """Get the AugLLMConfig engine with proper typing.

        This is a type-safe accessor that leverages the generic pattern.

        Returns:
            The AugLLMConfig engine.

        Raises:
            ValueError: If engine is not set.
        """
        if not self.engine:
            raise ValueError("Engine not initialized")
        return self.engine

    def update_temperature(self, temperature: float) -> None:
        """Update temperature on both agent and engine.

        Args:
            temperature: New temperature value (0.0-2.0).
        """
        self.temperature = temperature
        if self.engine:
            self.engine.temperature = temperature

    def update_system_message(self, message: str) -> None:
        """Update system message on both agent and engine.

        Args:
            message: New system message.
        """
        self.system_message = message
        if self.engine:
            self.engine.system_message = message

    def add_tool(self, tool: Any) -> None:
        """Add a tool to the agent.

        Args:
            tool: Tool to add.

        Note:
            Graph rebuild may be needed after adding tools.
        """
        self.tools.append(tool)
        if self.engine:
            if not self.engine.tools:
                self.engine.tools = []
            self.engine.tools.append(tool)


# ========================================================================
# FACTORY FUNCTION - Convenience creator
# ========================================================================


def create_simple_agent(
    name: str = "simple_agent",
    temperature: float = 0.7,
    max_tokens: int | None = None,
    system_message: str | None = None,
    tools: list[Any] | None = None,
    **kwargs,
) -> EnhancedSimpleAgent:
    """Create an enhanced SimpleAgent with common defaults.

    This factory function provides a convenient way to create SimpleAgents
    with sensible defaults.

    Args:
        name: Agent name.
        temperature: LLM temperature (0.0-2.0).
        max_tokens: Maximum response tokens.
        system_message: System prompt.
        tools: List of tools.
        **kwargs: Additional arguments passed to agent.

    Returns:
        Configured EnhancedSimpleAgent instance.

    Example:
        agent = create_simple_agent(
            name="helper",
            temperature=0.5,
            system_message="You are a helpful coding assistant"
        )
    """
    return EnhancedSimpleAgent(
        name=name,
        temperature=temperature,
        max_tokens=max_tokens,
        system_message=system_message,
        tools=tools or [],
        **kwargs,
    )


# ========================================================================
# BACKWARDS COMPATIBILITY
# ========================================================================

# Alias for migration
SimpleAgent = EnhancedSimpleAgent
