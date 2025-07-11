"""Test the full dynamic supervisor flow with agent creation and registry."""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.registry import EngineRegistry
from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.dynamic_supervisor_agent import (
    create_supervisor_agent,
)
from haive.agents.simple.agent import SimpleAgent


async def create_new_agent_from_registry(
    agent_type: str, description: str
) -> SimpleAgent:
    """Create a new agent using the engine registry."""

    # Create engine configuration
    engine_name = f"{agent_type}_engine"
    engine = AugLLMConfig(
        name=engine_name,
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message=f"You are a {description}. Help users with {agent_type} related tasks.",
    )

    # Register in engine registry
    registry = EngineRegistry.get_instance()
    registry.register_engine(engine_name, engine)

    # Create agent
    agent = SimpleAgent(
        name=f"{agent_type}_agent", engine=engine, description=description
    )

    return agent


async def add_agent_to_state(
    state: SupervisorStateWithTools, agent: SimpleAgent, description: str
) -> SupervisorStateWithTools:
    """Add a new agent to the supervisor state."""
    agent_info = AgentInfo(
        agent=agent, name=agent.name, description=description, active=True
    )

    # Add to agents dict
    state.agents[agent.name] = agent_info
    state.active_agents.add(agent.name)

    # Sync the dynamic choice model
    state.sync_agents()

    return state


async def test_full_dynamic_flow():
    """Test the complete dynamic supervisor flow."""

    # Create supervisor with no predefined agents
    supervisor = create_supervisor_agent("dynamic_supervisor")

    # Start with empty state
    initial_state = SupervisorStateWithTools(
        messages=[
            HumanMessage(
                content="I need to analyze some code and also translate text to French"
            )
        ],
        agents={},  # Start empty!
        active_agents=set(),
    )


    # Test 1: Request something that needs a new agent

    try:
        # This should show that no agents are available
        result1 = await supervisor.arun(
            initial_state.model_dump(), debug=True  # Show full execution trace
        )

        for i, msg in enumerate(result1.get("messages", [])):
            pass

    except Exception as e:
        pass")

    # Test 2: Add code analysis agent dynamically

    code_agent = await create_new_agent_from_registry(
        "code_analysis", "Expert code analyzer and reviewer"
    )

    # Add to state
    updated_state = await add_agent_to_state(
        initial_state, code_agent, "Expert code analyzer and reviewer"
    )

    # Test with code analysis task
    updated_state.messages = [
        HumanMessage(
            content="Please analyze this Python function: def factorial(n): return 1 if n <= 1 else n * factorial(n-1)"
        )
    ]

    try:
        result2 = await supervisor.arun(updated_state.model_dump(), debug=True)

        if result2.get("agent_response"):
            pass

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 3: Add translation agent and test multi-agent workflow

    translation_agent = await create_new_agent_from_registry(
        "translation", "Expert language translator for multiple languages"
    )

    # Add translation agent
    updated_state = await add_agent_to_state(
        updated_state, translation_agent, "Expert language translator"
    )

    # Test with translation task
    updated_state.messages = [
        HumanMessage(content="Translate 'Hello, how are you today?' to French")
    ]

    try:
        result3 = await supervisor.arun(updated_state.model_dump(), debug=True)

        if result3.get("agent_response"):
            pass

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 4: Complex task requiring decision between multiple agents

    # Task that could go to either agent
    updated_state.messages = [
        HumanMessage(
            content="I have some Python code comments in French that need to be analyzed"
        )
    ]

    try:
        result4 = await supervisor.arun(updated_state.model_dump(), debug=True)


    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 5: Show final state


    # Show engine registry
    registry = EngineRegistry.get_instance()
    for name in registry._engines:
        pass")



if __name__ == "__main__":
    asyncio.run(test_full_dynamic_flow())
