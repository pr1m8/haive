"""Agent protocols - Protocol definitions for Agent capabilities.

This module defines protocol interfaces that describe the expected
functionality of Agent classes in the Haive framework. These protocols
enable runtime type checking and promote consistent interfaces across
different agent implementations.
"""

from collections.abc import AsyncGenerator, Generator
from typing import Any, Dict, Optional, Protocol, TypeVar, runtime_checkable

from langchain_core.runnables import RunnableConfig

# Define type variables for input and output
TIn = TypeVar("TIn")
TOut = TypeVar("TOut")
TState = TypeVar("TState")


@runtime_checkable
class AgentProtocol(Protocol[TIn, TOut, TState]):
    """Protocol defining the core functionality of an Agent.

    This protocol specifies the minimum interface requirements for
    Agent implementations in the Haive framework.
    """

    @property
    def app(self) -> Any:
        """Return the compiled agent application."""
        ...

    def run(
        self,
        input_data: TIn,
        thread_id: str | None = None,
        debug: bool = True,
        config: RunnableConfig | None = None,
        **kwargs
    ) -> TOut:
        """Synchronously run the agent with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            debug: Whether to enable debug mode
            config: Optional runtime configuration
            **kwargs: Additional runtime configuration

        Returns:
            Output from the agent
        """
        ...

    async def arun(
        self,
        input_data: TIn,
        thread_id: str | None = None,
        config: RunnableConfig | None = None,
        **kwargs
    ) -> TOut:
        """Asynchronously run the agent with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
            **kwargs: Additional runtime configuration

        Returns:
            Output from the agent
        """
        ...

    def compile(self) -> None:
        """Compile the agent's workflow graph."""
        ...

    def setup_workflow(self) -> None:
        """Set up the workflow graph for this agent."""
        ...


@runtime_checkable
class StreamingAgentProtocol(Protocol[TIn, TOut]):
    """Protocol defining streaming functionality for Agents.

    This protocol extends the core agent functionality with
    streaming capabilities for real-time outputs.
    """

    def stream(
        self,
        input_data: TIn,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        debug: bool = True,
        **kwargs
    ) -> Generator[dict[str, Any], None, None]:
        """Stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Yields:
            State updates during execution
        """
        ...

    async def astream(
        self,
        input_data: TIn,
        thread_id: str | None = None,
        stream_mode: str = "values",
        config: RunnableConfig | None = None,
        **kwargs
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Asynchronously stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            **kwargs: Additional runtime configuration

        Yields:
            Async iterator of state updates during execution
        """
        ...


@runtime_checkable
class PersistentAgentProtocol(Protocol):
    """Protocol defining persistence functionality for Agents.

    This protocol specifies methods related to state persistence
    and thread management in agents.
    """

    def save_state_history(self, runnable_config: RunnableConfig | None = None) -> bool:
        """Save the current agent state to a JSON file.

        Args:
            runnable_config: Optional runnable configuration

        Returns:
            True if successful, False otherwise
        """
        ...

    def inspect_state(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> None:
        """Inspect the current state of the agent.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
        """
        ...

    def reset_state(
        self, thread_id: str | None = None, config: RunnableConfig | None = None
    ) -> bool:
        """Reset the agent's state for a thread.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration

        Returns:
            True if successful, False otherwise
        """
        ...


@runtime_checkable
class VisualizationAgentProtocol(Protocol):
    """Protocol defining visualization capabilities for Agents.

    This protocol specifies methods related to graph visualization
    and debugging.
    """

    def visualize_graph(self, output_path: str | None = None) -> None:
        """Generate and save a visualization of the agent's graph.

        Args:
            output_path: Optional custom path for visualization output
        """
        ...


@runtime_checkable
class ExtensibilityAgentProtocol(Protocol):
    """Protocol defining pattern-based extensibility for Agents.

    This protocol specifies methods related to pattern application
    and graph modification.
    """

    def apply_pattern(self, pattern_name: str, **kwargs) -> None:
        """Apply a graph pattern to the agent's workflow.

        Args:
            pattern_name: Name of the pattern to apply
            **kwargs: Pattern-specific parameters
        """
        ...


# Combined protocol for comprehensive agent capabilities
@runtime_checkable
class FullAgentProtocol(
    AgentProtocol,
    StreamingAgentProtocol,
    PersistentAgentProtocol,
    VisualizationAgentProtocol,
    ExtensibilityAgentProtocol,
    Protocol,
):
    """Protocol combining all agent capabilities.

    This protocol represents a fully-featured agent with all available
    capabilities in the Haive framework.
    """


# Type assertions to verify that Agent class implements protocols
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from haive.core.engine.agent.agent import Agent

    def assert_agent_protocols(agent_class: type[Agent]):
        """Assert that Agent class implements all protocols."""
        assert issubclass(
            agent_class, AgentProtocol
        ), "Agent must implement AgentProtocol"
        assert issubclass(
            agent_class, StreamingAgentProtocol
        ), "Agent must implement StreamingAgentProtocol"
        assert issubclass(
            agent_class, PersistentAgentProtocol
        ), "Agent must implement PersistentAgentProtocol"
        assert issubclass(
            agent_class, VisualizationAgentProtocol
        ), "Agent must implement VisualizationAgentProtocol"
        assert issubclass(
            agent_class, ExtensibilityAgentProtocol
        ), "Agent must implement ExtensibilityAgentProtocol"
        assert issubclass(
            agent_class, FullAgentProtocol
        ), "Agent must implement FullAgentProtocol"
