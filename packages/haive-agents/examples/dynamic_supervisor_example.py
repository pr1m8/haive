#!/usr/bin/env python3
"""Dynamic Supervisor Example.

This example demonstrates the dynamic supervisor agent coordinating
multiple specialized agents to handle complex, multi-step tasks.
"""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, ModelType
from langchain_core.messages import HumanMessage

from haive.agents.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


async def create_specialized_agents():
    """Create specialized agents for different tasks."""
    # Research Agent
    research_engine = AugLLMConfig(
        name="research_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.7),
        system_message="You are a research assistant. Search for information and provide detailed analysis.",
    )
    research_agent = SimpleAgent(name="research_agent", engine=research_engine)

    # Math Agent
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.0),
        system_message="You are a mathematical expert. Solve calculations and explain mathematical concepts clearly.",
    )
    math_agent = ReactAgent(name="math_agent", engine=math_engine)

    # Code Agent
    code_engine = AugLLMConfig(
        name="code_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.0),
        system_message="You are a coding expert. Write clean, efficient code and explain programming concepts.",
    )
    code_agent = SimpleAgent(name="code_agent", engine=code_engine)

    return research_agent, math_agent, code_agent


async def create_supervisor() -> DynamicSupervisorAgent:
    """Create the dynamic supervisor."""
    # Create supervisor engine
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O, temperature=0.0),
        force_tool_use=True,
        system_message="",  # Will be set by supervisor
    )

    # Create supervisor
    supervisor = DynamicSupervisorAgent(
        name="task_coordinator", engine=supervisor_engine, enable_agent_builder=False
    )

    return supervisor


async def demonstrate_simple_routing(supervisor: DynamicSupervisorAgent, state):
    """Demonstrate simple task routing to appropriate agents."""
    # Task 1: Math question
    await supervisor.arun("What is the square root of 144?", state=state)

    # Task 2: Research question
    await supervisor.arun(
        "What are the latest developments in quantum computing?", state=state
    )

    # Task 3: Code question
    await supervisor.arun("Write a Python function to calculate factorial", state=state)


async def demonstrate_multi_step_task(supervisor: DynamicSupervisorAgent, state):
    """Demonstrate a complex multi-step task."""
    await supervisor.arun(
        "Research the Fibonacci sequence, calculate the 10th number, and write a Python function to generate it",
        state=state,
    )

    # Show which agents were involved
    agent_executions = []
    for msg in state.messages:
        if (
            hasattr(msg, "additional_kwargs")
            and msg.additional_kwargs.get("source") == "agent_execution"
        ):
            agent_name = msg.additional_kwargs.get("agent_name", "unknown")
            if agent_name not in agent_executions:
                agent_executions.append(agent_name)


async def demonstrate_dynamic_agent_management(
    supervisor: DynamicSupervisorAgent, state
):
    """Show dynamic agent management capabilities."""
    # Add a new agent dynamically
    translator_engine = AugLLMConfig(
        name="translator_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.3),
        system_message="You are a translation expert. Translate text accurately between languages.",
    )
    translator_agent = SimpleAgent(name="translator_agent", engine=translator_engine)

    state.add_agent(
        "translator",
        translator_agent,
        "Translation expert - translates text between languages",
    )

    # Use the new agent
    await supervisor.arun("Translate 'Hello, how are you?' to French", state=state)

    # Deactivate an agent
    state.deactivate_agent("math")

    # Try to use deactivated agent
    await supervisor.arun("Calculate 15 * 23", state=state)

    # Reactivate agent
    state.activate_agent("math")

    # Use reactivated agent
    await supervisor.arun("Now calculate 15 * 23", state=state)


async def show_execution_summary(state):
    """Show a summary of the execution."""
    # Count agent executions
    agent_executions = {}
    for msg in state.messages:
        if (
            hasattr(msg, "additional_kwargs")
            and msg.additional_kwargs.get("source") == "agent_execution"
        ):
            agent_name = msg.additional_kwargs.get("agent_name", "unknown")
            agent_executions[agent_name] = agent_executions.get(agent_name, 0) + 1

    for _agent, _count in agent_executions.items():
        pass

    # Show available tools
    tools = state.get_all_tools()
    [t.name for t in tools if t.name.startswith("handoff_to_")]


async def demonstrate_full_workflow():
    """Complete demonstration of the dynamic supervisor."""
    # Step 1: Create specialized agents
    research_agent, math_agent, code_agent = await create_specialized_agents()

    # Step 2: Create supervisor
    supervisor = await create_supervisor()

    # Step 3: Initialize state with agents

    state = supervisor.create_initial_state()
    state.add_agent(
        "research",
        research_agent,
        "Research expert - searches for information and provides analysis",
    )
    state.add_agent(
        "math",
        math_agent,
        "Mathematics expert - performs calculations and explains math concepts",
    )
    state.add_agent(
        "code",
        code_agent,
        "Programming expert - writes code and explains programming concepts",
    )

    # Step 4: Simple routing demonstration
    await demonstrate_simple_routing(supervisor, state)

    # Step 5: Multi-step task demonstration
    await demonstrate_multi_step_task(supervisor, state)

    # Step 6: Dynamic agent management
    await demonstrate_dynamic_agent_management(supervisor, state)

    # Step 7: Show execution summary
    await show_execution_summary(state)

    # Final message


async def main():
    """Main execution function."""
    try:
        await demonstrate_full_workflow()
    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Note: This example uses mock LLM responses for demonstration
    # In production, ensure you have proper Azure OpenAI credentials configured

    asyncio.run(main())
