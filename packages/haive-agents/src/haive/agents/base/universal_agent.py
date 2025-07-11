"""Universal Agent - Simplified base class for all agent types.

This module provides a simplified Agent base class that maintains familiar
naming while providing clear type-based capabilities and proper separation
of concerns through agent types rather than complex inheritance hierarchies.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any

from haive.core.engine.base.agent_types import AgentType, get_agent_capabilities
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from langchain_core.runnables import RunnableConfig
from langgraph.graph.graph import CompiledGraph
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class Agent(BaseModel, ABC):
    """Universal base class for all agent types in the Haive framework.

    All components that can be executed as graphs are "Agents" but have
    different types that determine their capabilities:

    - REASONING: LLM-based agents that can reason and use tools
    - RETRIEVER: Agents that retrieve information from data sources
    - LOADER: Agents that load data from various sources
    - PROCESSOR: Agents that transform and process data
    - PIPELINE: Agents that chain processing operations
    - WORKFLOW: Agents that orchestrate multiple other agents
    - CHAIN: Agents that execute other agents sequentially

    The agent_type field determines what capabilities and methods are
    available to each agent instance.
    """

    # Core identification
    name: str = Field(description="Human-readable name for this agent")

    # Agent type classification
    agent_type: AgentType = Field(
        description="Type of agent that determines available capabilities"
    )

    # Schema definitions
    state_schema: type[StateSchema] | type[BaseModel] | dict[str, Any] | None = Field(
        default=None, description="Schema defining the state structure for this agent"
    )
    input_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, description="Schema for input validation (optional)"
    )
    output_schema: type[BaseModel] | dict[str, Any] | None = Field(
        default=None, description="Schema for output validation (optional)"
    )

    # Optional metadata
    description: str | None = Field(
        default=None, description="Optional description of agent functionality"
    )

    # Runtime configuration
    runnable_config: RunnableConfig | None = Field(
        default=None, description="Default runtime configuration for execution"
    )

    # Debug and visualization
    verbose: bool = Field(
        default=False, description="Enable verbose logging during execution"
    )

    @abstractmethod
    def build_graph(self) -> BaseGraph:
        """Build the graph representation for this agent.

        This method must be implemented by all agent subclasses to define
        how the agent should be represented as a graph structure.

        Returns:
            BaseGraph: The graph representation of this agent
        """

    def compile(self, **kwargs) -> CompiledGraph:
        """Compile this agent to an executable LangGraph instance.

        Args:
            **kwargs: Additional compilation arguments

        Returns:
            CompiledGraph: Executable LangGraph instance
        """
        graph = self.build_graph()
        return graph.compile(**kwargs)

    def invoke(self, input_data: Any, config: dict[str, Any] | None = None) -> Any:
        """Invoke the agent with input data.

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

    # Type checking methods
    def is_reasoning_agent(self) -> bool:
        """Check if this agent has reasoning capabilities."""
        from haive.core.engine.base.agent_types import is_reasoning_agent

        return is_reasoning_agent(self.agent_type)

    def is_processing_agent(self) -> bool:
        """Check if this agent is for deterministic processing."""
        from haive.core.engine.base.agent_types import is_processing_agent

        return is_processing_agent(self.agent_type)

    def is_orchestration_agent(self) -> bool:
        """Check if this agent orchestrates other agents."""
        from haive.core.engine.base.agent_types import is_orchestration_agent

        return is_orchestration_agent(self.agent_type)

    def get_capabilities(self) -> dict[str, bool]:
        """Get capabilities available to this agent."""
        return get_agent_capabilities(self.agent_type)

    def can_reason(self) -> bool:
        """Check if agent can perform reasoning operations."""
        return self.get_capabilities().get("reasoning", False)

    def can_process_batch(self) -> bool:
        """Check if agent supports batch processing."""
        return self.get_capabilities().get("batch_processing", False)

    def can_orchestrate(self) -> bool:
        """Check if agent can orchestrate other agents."""
        return self.get_capabilities().get("orchestration", False)

    # Capability-based method routing
    def __getattr__(self, name: str) -> Any:
        """Route method calls based on agent capabilities.

        This allows agents to have type-specific methods that are only
        available when the agent type supports those capabilities.
        """
        capabilities = self.get_capabilities()

        # Reasoning-specific methods
        if name in ["reason", "use_tool", "get_available_tools"]:
            if not capabilities.get("reasoning"):
                raise AttributeError(
                    f"'{self.__class__.__name__}' agent (type: {self.agent_type}) "
                    f"does not support reasoning method '{name}'"
                )

        # Processing-specific methods
        elif name in ["process", "batch_process", "get_performance_metrics"]:
            if not capabilities.get("batch_processing"):
                raise AttributeError(
                    f"'{self.__class__.__name__}' agent (type: {self.agent_type}) "
                    f"does not support processing method '{name}'"
                )

        # Orchestration-specific methods
        elif name in ["orchestrate", "add_agent", "remove_agent"]:
            if not capabilities.get("orchestration"):
                raise AttributeError(
                    f"'{self.__class__.__name__}' agent (type: {self.agent_type}) "
                    f"does not support orchestration method '{name}'"
                )

        # Default behavior for unknown attributes
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")

    def __str__(self) -> str:
        """String representation of the agent."""
        return (
            f"{self.__class__.__name__}(name='{self.name}', type='{self.agent_type}')"
        )

    def __repr__(self) -> str:
        """Detailed string representation of the agent."""
        capabilities = list(k for k, v in self.get_capabilities().items() if v]
        return (
            f"{self.__class__.__name__}("
            f"name='{self.name}', "
            f"type='{self.agent_type}', "
            f"capabilities={capabilities})"
        )
