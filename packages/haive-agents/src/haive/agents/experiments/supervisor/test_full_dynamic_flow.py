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
    print(f"\n🔧 Creating new {agent_type} agent...")

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
    print(f"✅ Registered engine: {engine_name}")

    # Create agent
    agent = SimpleAgent(
        name=f"{agent_type}_agent", engine=engine, description=description
    )

    print(f"✅ Created agent: {agent.name}")
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

    print(f"✅ Added {agent.name} to supervisor state")
    return state


async def test_full_dynamic_flow():
    """Test the complete dynamic supervisor flow."""
    print("\n" + "=" * 60)
    print("🚀 TESTING FULL DYNAMIC SUPERVISOR FLOW")
    print("=" * 60)

    # Create supervisor with no predefined agents
    print("\n1. Creating empty supervisor...")
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

    print(f"✅ Supervisor created with {len(initial_state.agents)} agents")

    # Test 1: Request something that needs a new agent
    print("\n" + "-" * 50)
    print("2. Testing request that needs NEW agents...")
    print("-" * 50)

    try:
        # This should show that no agents are available
        result1 = await supervisor.arun(
            initial_state.model_dump(), debug=True  # Show full execution trace
        )

        print(f"\n📋 Result 1 - No agents available:")
        print(f"Messages: {len(result1.get('messages', []))}")
        for i, msg in enumerate(result1.get("messages", [])):
            print(
                f"  [{i}] {type(msg).__name__}: {msg.content if hasattr(msg, 'content') else msg}"
            )

    except Exception as e:
        print(f"❌ Test 1 failed: {e}")

    # Test 2: Add code analysis agent dynamically
    print("\n" + "-" * 50)
    print("3. Adding code analysis agent dynamically...")
    print("-" * 50)

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

        print(f"\n📋 Result 2 - Code analysis:")
        print(f"Routed to: {result2.get('next_agent')}")
        print(f"Task: {result2.get('agent_task')}")
        if result2.get("agent_response"):
            print(f"Response: {result2['agent_response'][:200]}...")

    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 3: Add translation agent and test multi-agent workflow
    print("\n" + "-" * 50)
    print("4. Adding translation agent and testing multi-step workflow...")
    print("-" * 50)

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

        print(f"\n📋 Result 3 - Translation:")
        print(f"Routed to: {result3.get('next_agent')}")
        print(f"Task: {result3.get('agent_task')}")
        if result3.get("agent_response"):
            print(f"Response: {result3['agent_response']}")

    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 4: Complex task requiring decision between multiple agents
    print("\n" + "-" * 50)
    print("5. Testing complex decision with multiple available agents...")
    print("-" * 50)

    # Task that could go to either agent
    updated_state.messages = [
        HumanMessage(
            content="I have some Python code comments in French that need to be analyzed"
        )
    ]

    try:
        result4 = await supervisor.arun(updated_state.model_dump(), debug=True)

        print(f"\n📋 Result 4 - Complex routing decision:")
        print(f"Available agents: {list(updated_state.agents.keys())}")
        print(f"Routed to: {result4.get('next_agent')}")
        print(
            f"Reasoning: Supervisor chose {result4.get('next_agent')} for the French code analysis task"
        )

    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 5: Show final state
    print("\n" + "-" * 50)
    print("6. Final state summary...")
    print("-" * 50)

    print(f"📊 Final supervisor state:")
    print(f"  - Total agents: {len(updated_state.agents)}")
    print(f"  - Active agents: {len(updated_state.active_agents)}")
    print(f"  - Agent names: {list(updated_state.agents.keys())}")

    # Show engine registry
    registry = EngineRegistry.get_instance()
    print(f"  - Engines in registry: {len(registry._engines)}")
    for name in registry._engines.keys():
        print(f"    • {name}")

    print("\n🎉 DYNAMIC SUPERVISOR FLOW TEST COMPLETE!")


if __name__ == "__main__":
    asyncio.run(test_full_dynamic_flow())
