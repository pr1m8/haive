#!/usr/bin/env python3
"""
Dynamic Supervisor Demo - Shows the working implementation

This demonstrates the dynamic supervisor with real agents, following
the pattern we built in experiments.
"""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.dynamic_supervisor import (
    DynamicSupervisorAgent,
    SupervisorStateWithTools,
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
    print("🚀 DYNAMIC SUPERVISOR DEMO")
    print("=" * 60)

    # Create supervisor
    print("\n1. Creating Dynamic Supervisor...")
    supervisor_engine = AugLLMConfig(
        name="supervisor_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a task supervisor. Route tasks to the best agent.",
    )

    supervisor = DynamicSupervisorAgent(name="coordinator", engine=supervisor_engine)
    print(f"✅ Created supervisor: {supervisor.name}")

    # Create initial state
    print("\n2. Setting up agents...")
    state = supervisor.create_initial_state()
    simple_agent, react_agent = create_agents()

    # Add agents to state
    state.add_agent("assistant", simple_agent, "General purpose assistant")
    state.add_agent("reasoner", react_agent, "Step-by-step reasoning specialist")

    print(f"✅ Added {len(state.agents)} agents")
    print(f"📋 Generated {len(state.generated_tools)} tools:")
    for tool in state.generated_tools:
        print(f"   - {tool}")

    # Show active agents
    print("\n3. Active Agents:")
    for name, desc in state.list_active_agents().items():
        print(f"   • {name}: {desc}")

    # Test handoff tools
    print("\n4. Testing Handoff Tools...")
    tools = state.get_all_tools()

    # Find a handoff tool
    handoff_tool = next(t for t in tools if t.name == "handoff_to_assistant")
    print(f"\n🔧 Testing {handoff_tool.name}...")

    # Note: Can't execute without API keys, but show structure
    print(f"   Tool: {handoff_tool.name}")
    print(f"   Description: {handoff_tool.description}")
    print(f"   Callable: {callable(handoff_tool.func)}")

    # Show dynamic agent management
    print("\n5. Dynamic Agent Management...")

    # Add a new agent
    print("   Adding new agent...")
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
    print(f"   ✅ Now have {len(state.agents)} agents")
    print(
        f"   📋 Generated tools: {[t for t in state.generated_tools if t.startswith('handoff_')]}"
    )

    # Deactivate an agent
    print("\n   Deactivating 'reasoner' agent...")
    state.deactivate_agent("reasoner")
    print(f"   ⏸️  Active agents: {list(state.list_active_agents().keys())}")

    # Remove an agent
    print("\n   Removing 'assistant' agent...")
    state.remove_agent("assistant")
    print(f"   🗑️  Remaining agents: {list(state.agents.keys())}")
    print(
        f"   📋 Updated tools: {[t for t in state.generated_tools if t.startswith('handoff_')]}"
    )

    # Show serialization works
    print("\n6. Testing Serialization...")
    import ormsgpack

    state_dict = state.model_dump()
    print(f"   State fields: {list(state_dict.keys())}")

    # Verify agents are excluded from serialization
    if state.agents:
        agent_name = list(state.agents.keys())[0]
        agent_data = state_dict["agents"][agent_name]
        print(f"   Agent '{agent_name}' data: {list(agent_data.keys())}")
        print(f"   'agent' field excluded: {'agent' not in agent_data}")

    # Serialize
    try:
        serialized = ormsgpack.packb(state_dict)
        print(f"   ✅ Serialization successful! ({len(serialized)} bytes)")
    except Exception as e:
        print(f"   ❌ Serialization failed: {e}")

    print("\n" + "=" * 60)
    print("✅ Demo completed successfully!")
    print("\nKey Points:")
    print("- Handoff tools execute agents directly (no separate node)")
    print("- Agents are excluded from serialization")
    print("- Tools are dynamically generated as agents change")
    print("- Supports different agent types (SimpleAgent, ReactAgent)")


async def demo_supervisor_execution():
    """Demo what execution would look like (requires API keys)."""
    print("\n\n🎯 EXECUTION DEMO (Simulated)")
    print("=" * 60)

    print("\nIn a real execution with API keys:")
    print("1. Supervisor receives task: 'Explain quantum computing simply'")
    print("2. Supervisor analyzes task and available agents")
    print("3. Supervisor calls handoff_to_assistant tool")
    print("4. Tool executes assistant agent directly with the task")
    print("5. Assistant returns explanation")
    print("6. Supervisor returns final result")

    print("\nThe flow is simple:")
    print("User → Supervisor → Handoff Tool → Agent → Result")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(demo_supervisor())
    asyncio.run(demo_supervisor_execution())
