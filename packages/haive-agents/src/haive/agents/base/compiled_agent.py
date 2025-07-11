"""CompiledAgent - Agent class based on CompiledStateGraph architecture.

This module provides the new CompiledAgent class that inherits from CompiledStateGraph
while maintaining compatibility with the existing Agent interface. This class represents
the future direction for agent architecture in the Haive framework.
"""

from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any, Literal

from haive.core.engine.base import Engine, EngineType
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.graph.state_graph.compiled_state_graph import CompiledStateGraph
from haive.core.schema.schema_composer import SchemaComposer
from langchain_core.tools import BaseTool
from pydantic import Field, model_validator

# Import mixins for compatibility
from haive.agents.base.mixins.execution_mixin import ExecutionMixin
from haive.agents.base.mixins.persistence_mixin import PersistenceMixin
from haive.agents.base.mixins.state_mixin import StateMixin
from haive.agents.base.serialization_mixin import SerializationMixin

logger = logging.getLogger(__name__)


class CompiledAgent(
    CompiledStateGraph,
    ExecutionMixin,
    StateMixin,
    PersistenceMixin,
    SerializationMixin,
):
    """Agent class based on CompiledStateGraph architecture.

    This class represents LLM-based reasoning agents that can:
    - Reason about problems and make decisions
    - Use tools to interact with external systems
    - Maintain conversation memory and context
    - Coordinate with other agents in multi-agent workflows

    CompiledAgent should be used for components that require:
    - LLM-powered reasoning capabilities
    - Tool usage and coordination
    - Dynamic decision making
    - Conversation and memory management

    Attributes:
        engine: Primary LLM engine for reasoning (required)
        engines: Dictionary of additional engines used by this agent
        tools: List of tools available to this agent
        agent_type: Always EngineType.AGENT for agents
        conversation_memory: Whether to maintain conversation history
        max_iterations: Maximum reasoning iterations before stopping
    """

    # Agent classification
    agent_type: Literal[EngineType.AGENT] = Field(
        default=EngineType.AGENT,
        description="Agent type, always AGENT for reasoning agents",
    )

    # Core engine requirements
    engine: Engine | None = Field(
        default=None,
        description="Primary LLM engine for reasoning (required for agents)",
    )

    engines: dict[str, Engine] = Field(
        default_factory=dict,
        description="Dictionary of additional engines used by this agent",
    )

    # Tool capabilities
    tools: list[BaseTool] = Field(
        default_factory=list, description="List of tools available to this agent"
    )

    # Agent-specific behavior
    conversation_memory: bool = Field(
        default=True, description="Whether to maintain conversation history"
    )

    max_iterations: int = Field(
        default=10, description="Maximum reasoning iterations before stopping"
    )

    # Schema generation control
    set_schema: bool = Field(
        default=True, description="Whether to auto-generate schemas from engines"
    )

    @model_validator(mode="after")
    def validate_agent_requirements(self) -> CompiledAgent:
        """Validate that agent has required LLM capabilities.

        Agents must have an LLM engine for reasoning. This validator ensures
        that the agent is properly configured with reasoning capabilities.
        """
        if not self.engine:
            if not self.engines:
                raise ValueError(
                    "Agents must have at least one engine. "
                    "Provide either 'engine' or 'engines' parameter."
                )
            # If no primary engine, try to find an LLM engine in engines dict
            llm_engines = [
                eng
                for eng in self.engines.values()
                if hasattr(eng, "engine_type") and eng.engine_type == EngineType.LLM
            ]
            if llm_engines:
                self.engine = llm_engines[0]
            else:
                logger.warning(
                    f"Agent {self.name} has no LLM engine. "
                    "Agents should have reasoning capabilities."
                )

        # Set up schemas if requested
        if self.set_schema:
            self._setup_schemas()

        return self

    def _setup_schemas(self) -> None:
        """Generate schemas from available engines.

        This method creates state, input, and output schemas based on the
        engines available to this agent. It uses SchemaComposer for basic
        composition (agents with sub-agents should use AgentSchemaComposer).
        """
        if not self.state_schema:
            engine_list = []
            if self.engine:
                engine_list.append(self.engine)
            engine_list.extend(self.engines.values())

            if engine_list:
                logger.debug(f"Creating schema from {len(engine_list)} engines")
                self.state_schema = SchemaComposer.from_components(
                    components=engine_list, name=f"{self.__class__.__name__}State"
                )
            else:
                logger.debug("No engines found, using basic state schema")
                from haive.core.schema.prebuilt.messages_state import MessagesState

                self.state_schema = MessagesState

    @abstractmethod
    def reason(self, problem: Any, context: dict[str, Any] | None = None) -> Any:
        """Reason about a problem and provide a solution.

        This method must be implemented by all agent subclasses to define
        their reasoning capabilities. The reasoning process may involve:
        - Analyzing the problem
        - Using available tools
        - Making decisions based on context
        - Generating solutions or responses

        Args:
            problem: The problem or input to reason about
            context: Optional context information for reasoning

        Returns:
            Any: The reasoning result or solution

        Raises:
            NotImplementedError: If not implemented by subclass
        """

    async def areason(self, problem: Any, context: dict[str, Any] | None = None) -> Any:
        """Asynchronous version of reason method.

        Default implementation calls the synchronous reason method.
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

    def can_reason(self) -> bool:
        """Check if this agent has reasoning capabilities.

        Returns:
            bool: True if agent has LLM engine for reasoning
        """
        return self.engine is not None

    def get_component_type(self) -> str:
        """Get the component type identifier."""
        return "agent"

    def get_agent_capabilities(self) -> dict[str, Any]:
        """Get information about agent capabilities.

        Returns:
            dict: Information about agent's capabilities
        """
        return {
            "has_reasoning": self.can_reason(),
            "tool_count": len(self.tools),
            "available_tools": self.get_available_tools(),
            "conversation_memory": self.conversation_memory,
            "max_iterations": self.max_iterations,
            "engine_count": len(self.engines) + (1 if self.engine else 0),
        }

    # Backward compatibility methods
    def setup_agent(self) -> None:
        """Hook for subclass-specific setup logic.

        This method is called during initialization and can be overridden
        by subclasses for custom setup logic. Maintained for backward
        compatibility with existing Agent interface.
        """

    def invoke(self, input_data: Any, config: dict[str, Any] | None = None) -> Any:
        """Invoke the agent with input data.

        This method provides the standard invocation interface for agents.
        It compiles the agent's graph and executes it with the provided input.

        Args:
            input_data: Input data for the agent
            config: Optional configuration for execution

        Returns:
            Any: Agent execution result
        """
        compiled_graph = self.compile()
        return compiled_graph.invoke(input_data, config=config)

    async def ainvoke(
        self, input_data: Any, config: dict[str, Any] | None = None
    ) -> Any:
        """Asynchronous invoke method.

        Args:
            input_data: Input data for the agent
            config: Optional configuration for execution

        Returns:
            Any: Agent execution result
        """
        compiled_graph = self.compile()
        return await compiled_graph.ainvoke(input_data, config=config)
