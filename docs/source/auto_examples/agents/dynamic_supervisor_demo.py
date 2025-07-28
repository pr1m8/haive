#!/usr/bin/env python3
"""Dynamic Supervisor Demo - Shows the working implementation.

This demonstrates the dynamic supervisor with real agents, following
the pattern we built in experiments.
"""
"""
"""

import asyncio
import contextlib

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.dynamic_supervisor import (
    DynamicSupervisorAgent,
)
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


def create_agents():
    """Create real agents for the supervisor to manage."""
    # Simple agent for general tasks
    simple_engine = AugLLMConfig(
        name="simple_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a helpful assistant. Answer questions clearly.",
    )
    simple_agent = SimpleAgent(
        name="assistant", engine=simple_engine, description="General purpose assistant"
    )

    # React agent for reasoning
    react_engine = AugLLMConfig(
        name="react_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a reasoning agent. Think step by step.",
    )
    react_agent = ReactAgent(
        name="reasoner",
        engine=react_engine,
        description="Step-by-step reasoning specialist",
    )

    return simple_agent, react_agent


async def demo_supervisor():
    """Demonstrate the dynamic supervisor in action."""
    # Create supervisor
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a task supervisor. Route tasks to the best agent.",
    )

    supervisor = DynamicSupervisorAgent(name="coordinator", engine=supervisor_engine)

    # Create initial state
    state = supervisor.create_initial_state()
    simple_agent, react_agent = create_agents()

    # Add agents to state
    state.add_agent("assistant", simple_agent, "General purpose assistant")
    state.add_agent("reasoner", react_agent, "Step-by-step reasoning specialist")

    for _tool in state.generated_tools:
        pass

    # Show active agents
    for _name, _desc in state.list_active_agents().items():
        pass

    # Test handoff tools
    tools = state.get_all_tools()

    # Find a handoff tool
    next(t for t in tools if t.name == "handoff_to_assistant")

    # Note: Can't execute without API keys, but show structure

    # Show dynamic agent management

    # Add a new agent
    code_engine = AugLLMConfig(
        name="code_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a coding expert. Write clean, efficient code.",
    )
    code_agent = SimpleAgent(
        name="coder",
        engine=code_engine,
        description="Programming and code generation specialist",
    )

    state.add_agent("coder", code_agent, "Programming specialist")

    # Deactivate an agent
    state.deactivate_agent("reasoner")

    # Remove an agent
    state.remove_agent("assistant")

    # Show serialization works
    import ormsgpack

    state_dict = state.model_dump()

    # Verify agents are excluded from serialization
    if state.agents:
        agent_name = next(iter(state.agents.keys()))
        state_dict["agents"][agent_name]

    # Serialize
    with contextlib.suppress(Exception):
        ormsgpack.packb(state_dict)


async def demo_supervisor_execution():
    """Demo what execution would look like (requires API keys)."""


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_supervisor())
    asyncio.run(demo_supervisor_execution())
