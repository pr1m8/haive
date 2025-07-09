"""Base Agent Module - Core abstractions for Haive agents.

This module provides the base agent class and related utilities for building
intelligent agents in the Haive framework. It properly exports the Agent class
from the agent.py module, along with supporting types and utilities.

Key Components:
    * Classes: Agent (from agent.py), GenericAgent
    * Mixins: ExecutionMixin, StateMixin, SerializationMixin
    * Types: AgentInput, AgentOutput, AgentState

Example:
    Basic usage::

        from haive.agents.base import Agent
        from haive.core.graph.state_graph.base_graph2 import BaseGraph

        class MyAgent(Agent):
            def setup_agent(self):
                # Custom setup logic
                pass

            def build_graph(self) -> BaseGraph:
                # Build and return the agent's workflow graph
                return my_graph

        # Create agent with configuration
        agent = MyAgent(
            name="my_agent",
            engine=my_llm_engine,
            config=AgentConfig(
                persistence=PostgresCheckpointerConfig(),
                runnable_config={
                    "configurable": {
                        "recursion_limit": 100
                    }
                }
            )
        )

        result = agent.invoke(input_data)

See Also:
    :mod:`haive.agents.base.agent`: Main Agent implementation
    :mod:`haive.agents.base.generic_agent`: Generic typed agent
    :mod:`haive.agents.base.mixins`: Agent capability mixins
"""

# Re-export the correct Agent class from agent.py
from .agent import Agent
from .generic_agent import GenericAgent

# Re-export mixins for convenience
from .mixins import ExecutionMixin, PersistenceMixin, StateMixin
from .serialization_mixin import SerializationMixin
from .types import AgentInput, AgentOutput, AgentState

__all__ = [
    "Agent",
    "GenericAgent",
    "AgentInput",
    "AgentOutput",
    "AgentState",
    "ExecutionMixin",
    "StateMixin",
    "PersistenceMixin",
    "SerializationMixin",
]
