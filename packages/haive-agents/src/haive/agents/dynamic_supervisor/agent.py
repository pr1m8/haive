"""Dynamic Supervisor Agent implementation.

This module contains the main DynamicSupervisorAgent class that extends
SimpleAgent to provide dynamic agent management capabilities.

Classes:
    DynamicSupervisorAgent: Main supervisor implementation

Functions:
    create_dynamic_supervisor: Factory function for creating supervisors

Example:
    Creating a dynamic supervisor::

        from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
        from haive.core.engine import AugLLMConfig

        supervisor = DynamicSupervisorAgent(
            name="task_router",
            engine=supervisor_engine,
            enable_agent_builder=True
        )

        # Run with initial agents
        state = supervisor.create_initial_state()
        state.add_agent("search", search_agent, "Search expert")

        result = await supervisor.arun(
            "Find information about Paris and translate to French",
            state=state
        )
"""

import logging
from typing import Any, Dict, List, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import BaseMessage
from pydantic import Field

# Tools handle agent execution directly - no separate node needed
from haive.agents.dynamic_supervisor.prompts import format_supervisor_prompt
from haive.agents.dynamic_supervisor.state import (
    SupervisorState,
    SupervisorStateWithTools,
)
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class DynamicSupervisorAgent(ReactAgent):
    """Dynamic supervisor agent that manages other agents at runtime.

    Extends ReactAgent to get the looping behavior needed for continuous
    agent selection and execution. The supervisor can add, remove, activate,
    and deactivate agents while running, and generates handoff tools dynamically.

    Architecture:
        - Inherits ReactAgent's reasoning + acting loop
        - Tools execute agents directly (no separate node)
        - Uses SupervisorStateWithTools for dynamic tool generation
        - Handoff tools execute agents and return to supervisor loop

    Attributes:
        enable_agent_builder: Whether to include agent request capability
        state_schema_override: Force use of supervisor state schema
        auto_sync_tools: Whether to sync tools automatically

    Example:
        Basic supervisor setup::

            supervisor = DynamicSupervisorAgent(
                name="coordinator",
                engine=AugLLMConfig(
                    model="gpt-4",
                    force_tool_use=True,
                    system_message="Route tasks to appropriate agents"
                )
            )

            # Add agents
            state = supervisor.create_initial_state()
            state.add_agent("coder", code_agent, "Python expert")

            # Run task
            result = await supervisor.arun("Write a Python function", state=state)
    """

    # Configuration
    enable_agent_builder: bool = Field(
        default=False, description="Enable agent request/builder capability"
    )

    state_schema_override: type = Field(
        default=SupervisorStateWithTools,
        description="Use supervisor state schema with dynamic agent management",
    )

    auto_sync_tools: bool = Field(
        default=True, description="Automatically sync tools when state changes"
    )

    def setup_agent(self) -> None:
        """Setup the supervisor with custom state schema.

        Overrides SimpleAgent setup to use SupervisorStateWithTools
        and configure the supervisor-specific settings.
        """
        # Call parent setup first
        super().setup_agent()

        # Force use of supervisor state schema
        self.state_schema = SupervisorStateWithTools
        self.input_schema = SupervisorStateWithTools

        # Update system message if not customized
        if self.engine and not self.system_message:
            # Format with empty agent list initially
            self.engine.system_message = format_supervisor_prompt({})

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with direct agent execution via tools.

        Uses the base ReactAgent graph where handoff tools execute
        agents directly and the ReAct loop handles multi-step coordination.
        No separate agent_execution node needed.

        Returns:
            Configured supervisor graph with ReAct loop
        """
        # Use base ReactAgent graph - provides the looping behavior
        graph = super().build_graph()

        logger.info(f"Built supervisor graph for '{self.name}' with ReAct loop")

        return graph

    def create_initial_state(self) -> SupervisorStateWithTools:
        """Create initial supervisor state.

        Convenience method to create a properly initialized state
        with the supervisor's configuration.

        Returns:
            Initialized supervisor state

        Example:
            Creating initial state::

                state = supervisor.create_initial_state()
                state.add_agent("search", agent, "Search expert")
        """
        state = SupervisorStateWithTools()

        # Add any default agents if configured
        if hasattr(self, "default_agents"):
            for name, (agent, desc) in self.default_agents.items():
                state.add_agent(name, agent, desc)

        return state

    async def arun(
        self,
        input_data: Union[str, Dict[str, Any], List[BaseMessage]],
        state: Optional[SupervisorStateWithTools] = None,
        **kwargs,
    ) -> Any:
        """Run the supervisor asynchronously.

        Extends SimpleAgent.arun to handle supervisor state and
        dynamic tool synchronization.

        Args:
            input_data: Input message(s) or task
            state: Optional supervisor state with agents
            **kwargs: Additional arguments for execution

        Returns:
            Execution result with updated state

        Example:
            Running with state::

                state = supervisor.create_initial_state()
                state.add_agent("math", math_agent, "Math expert")

                result = await supervisor.arun(
                    "Calculate the square root of 144",
                    state=state
                )
        """
        # Create state if not provided
        if state is None:
            state = self.create_initial_state()

        # Sync tools if auto-sync enabled
        if self.auto_sync_tools and hasattr(state, "sync_agents"):
            state.sync_agents()

            # Update supervisor prompt with current agents
            if self.engine:
                self.engine.system_message = format_supervisor_prompt(state.agents)

                # Update engine tools
                tools = state.get_all_tools()
                self.engine.tools = tools

        # Prepare input
        if isinstance(input_data, str):
            # Convert string to state with message
            from langchain_core.messages import HumanMessage

            state.messages.append(HumanMessage(content=input_data))
            input_data = state
        elif isinstance(input_data, list):
            # Add messages to state
            state.messages.extend(input_data)
            input_data = state
        elif isinstance(input_data, dict) and not isinstance(
            input_data, SupervisorStateWithTools
        ):
            # Merge dict into state
            for key, value in input_data.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            input_data = state

        # Run with parent implementation
        return await super().arun(input_data, **kwargs)

    def run(
        self,
        input_data: Union[str, Dict[str, Any], List[BaseMessage]],
        state: Optional[SupervisorStateWithTools] = None,
        **kwargs,
    ) -> Any:
        """Run the supervisor synchronously.

        Synchronous version of arun.

        Args:
            input_data: Input message(s) or task
            state: Optional supervisor state with agents
            **kwargs: Additional arguments for execution

        Returns:
            Execution result with updated state
        """
        # Create async coroutine and run it
        import asyncio

        return asyncio.run(self.arun(input_data, state, **kwargs))

    def add_default_agent(self, name: str, agent: Any, description: str) -> None:
        """Add a default agent that's always available.

        Default agents are automatically added to new states.

        Args:
            name: Agent identifier
            agent: Agent instance
            description: Agent description
        """
        if not hasattr(self, "default_agents"):
            self.default_agents = {}

        self.default_agents[name] = (agent, description)
        logger.info(f"Added default agent '{name}' to supervisor")

    def __repr__(self) -> str:
        """String representation."""
        engine_info = f"model={getattr(self.engine, 'model', 'unknown')}"
        return f"DynamicSupervisorAgent(name='{self.name}', {engine_info})"


def create_dynamic_supervisor(
    name: str = "supervisor",
    model: str = "gpt-4",
    temperature: float = 0.0,
    force_tool_use: bool = True,
    enable_agent_builder: bool = False,
    **kwargs,
) -> DynamicSupervisorAgent:
    """Factory function to create a configured dynamic supervisor.

    Args:
        name: Supervisor name
        model: LLM model to use
        temperature: LLM temperature (0.0 for deterministic)
        force_tool_use: Whether to force tool usage
        enable_agent_builder: Enable agent request capability
        **kwargs: Additional arguments for supervisor

    Returns:
        Configured DynamicSupervisorAgent instance

    Example:
        Quick supervisor creation::

            supervisor = create_dynamic_supervisor(
                name="task_coordinator",
                model="gpt-4",
                enable_agent_builder=True
            )
    """
    from haive.core.models.llm.base import AzureLLMConfig

    # Create engine configuration
    engine = AugLLMConfig(
        name=f"{name}_engine",
        llm_config=AzureLLMConfig(model=model, temperature=temperature),
        force_tool_use=force_tool_use,
        tools=[],  # Tools come from state
        system_message="",  # Set by supervisor
    )

    # Create supervisor
    supervisor = DynamicSupervisorAgent(
        name=name, engine=engine, enable_agent_builder=enable_agent_builder, **kwargs
    )

    return supervisor
