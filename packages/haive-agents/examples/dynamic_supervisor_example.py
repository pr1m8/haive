#!/usr/bin/env python3
"""
Dynamic Supervisor Example

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
    print("🤖 Creating Specialized Agents")
    print("=" * 60)

    # Research Agent
    research_engine = AugLLMConfig(
        name="research_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.7),
        system_message="You are a research assistant. Search for information and provide detailed analysis.",
    )
    research_agent = SimpleAgent(name="research_agent", engine=research_engine)
    print("✅ Created research agent")

    # Math Agent
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.0),
        system_message="You are a mathematical expert. Solve calculations and explain mathematical concepts clearly.",
    )
    math_agent = ReactAgent(name="math_agent", engine=math_engine)
    print("✅ Created math agent")

    # Code Agent
    code_engine = AugLLMConfig(
        name="code_engine",
        llm_config=AzureLLMConfig(model=ModelType.GPT_4O_MINI, temperature=0.0),
        system_message="You are a coding expert. Write clean, efficient code and explain programming concepts.",
    )
    code_agent = SimpleAgent(name="code_agent", engine=code_engine)
    print("✅ Created code agent")

    return research_agent, math_agent, code_agent


async def create_supervisor() -> DynamicSupervisorAgent:
    """Create the dynamic supervisor."""
    print("\n🎯 Creating Dynamic Supervisor")
    print("=" * 60)

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

    print(f"✅ Created supervisor: {supervisor.name}")
    return supervisor


async def demonstrate_simple_routing(supervisor: DynamicSupervisorAgent, state):
    """Demonstrate simple task routing to appropriate agents."""
    print("\n" + "=" * 60)
    print("📊 SIMPLE TASK ROUTING")
    print("=" * 60)

    # Task 1: Math question
    print("\n🔢 Task 1: What is the square root of 144?")
    result = await supervisor.arun("What is the square root of 144?", state=state)

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Response: {state.agent_response}")

    # Task 2: Research question
    print("\n🔍 Task 2: What are the latest developments in quantum computing?")
    result = await supervisor.arun(
        "What are the latest developments in quantum computing?", state=state
    )

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Response: {state.agent_response[:200]}...")

    # Task 3: Code question
    print("\n💻 Task 3: Write a Python function to calculate factorial")
    result = await supervisor.arun(
        "Write a Python function to calculate factorial", state=state
    )

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Response: {state.agent_response[:200]}...")


async def demonstrate_multi_step_task(supervisor: DynamicSupervisorAgent, state):
    """Demonstrate a complex multi-step task."""
    print("\n" + "=" * 60)
    print("🔗 MULTI-STEP TASK DEMONSTRATION")
    print("=" * 60)

    print(
        "\n📝 Complex Task: Research Fibonacci sequence, calculate 10th number, write Python function"
    )

    result = await supervisor.arun(
        "Research the Fibonacci sequence, calculate the 10th number, and write a Python function to generate it",
        state=state,
    )

    print("\n📊 Execution Summary:")
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

    print(f"   Agents involved: {', '.join(agent_executions)}")
    print(f"   Total messages: {len(state.messages)}")
    print(f"   Last response: {state.agent_response[:200]}...")


async def demonstrate_dynamic_agent_management(
    supervisor: DynamicSupervisorAgent, state
):
    """Show dynamic agent management capabilities."""
    print("\n" + "=" * 60)
    print("🔧 DYNAMIC AGENT MANAGEMENT")
    print("=" * 60)

    # Add a new agent dynamically
    print("\n➕ Adding translator agent...")
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
    print("✅ Translator agent added")

    # Use the new agent
    print("\n🌍 Task: Translate 'Hello, how are you?' to French")
    result = await supervisor.arun(
        "Translate 'Hello, how are you?' to French", state=state
    )

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Response: {state.agent_response}")

    # Deactivate an agent
    print("\n🚫 Deactivating math agent...")
    state.deactivate_agent("math")
    print("✅ Math agent deactivated")

    # Try to use deactivated agent
    print("\n🔢 Task: Calculate 15 * 23 (with math agent deactivated)")
    result = await supervisor.arun("Calculate 15 * 23", state=state)

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Note: {state.agent_response[:100]}...")

    # Reactivate agent
    print("\n✅ Reactivating math agent...")
    state.activate_agent("math")

    # Use reactivated agent
    print("\n🔢 Task: Now calculate 15 * 23")
    result = await supervisor.arun("Now calculate 15 * 23", state=state)

    print(f"   Last executed agent: {state.last_executed_agent}")
    print(f"   Response: {state.agent_response}")


async def show_execution_summary(state):
    """Show a summary of the execution."""
    print("\n" + "=" * 60)
    print("📊 EXECUTION SUMMARY")
    print("=" * 60)

    # Count agent executions
    agent_executions = {}
    for msg in state.messages:
        if (
            hasattr(msg, "additional_kwargs")
            and msg.additional_kwargs.get("source") == "agent_execution"
        ):
            agent_name = msg.additional_kwargs.get("agent_name", "unknown")
            agent_executions[agent_name] = agent_executions.get(agent_name, 0) + 1

    print("\n🤖 Agent Execution Count:")
    for agent, count in agent_executions.items():
        print(f"   {agent}: {count} executions")

    print(f"\n📝 Total Messages: {len(state.messages)}")
    print(
        f"🔧 Active Agents: {len([a for a, info in state.agents.items() if info.is_active()])}"
    )
    print(
        f"🚫 Inactive Agents: {len([a for a, info in state.agents.items() if not info.is_active()])}"
    )

    # Show available tools
    tools = state.get_all_tools()
    handoff_tools = [t.name for t in tools if t.name.startswith("handoff_to_")]
    print(f"\n🔧 Available Tools: {len(tools)}")
    print(f"   Handoff tools: {', '.join(handoff_tools)}")
    print(
        f"   Other tools: {', '.join([t.name for t in tools if not t.name.startswith('handoff_to_')])}"
    )


async def demonstrate_full_workflow():
    """Complete demonstration of the dynamic supervisor."""
    print("🎭 DYNAMIC SUPERVISOR COMPLETE DEMONSTRATION")
    print("=" * 80)

    # Step 1: Create specialized agents
    research_agent, math_agent, code_agent = await create_specialized_agents()

    # Step 2: Create supervisor
    supervisor = await create_supervisor()

    # Step 3: Initialize state with agents
    print("\n📦 Initializing Supervisor State")
    print("=" * 60)

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

    print(f"✅ Added {len(state.agents)} agents to supervisor")

    # Step 4: Simple routing demonstration
    await demonstrate_simple_routing(supervisor, state)

    # Step 5: Multi-step task demonstration
    await demonstrate_multi_step_task(supervisor, state)

    # Step 6: Dynamic agent management
    await demonstrate_dynamic_agent_management(supervisor, state)

    # Step 7: Show execution summary
    await show_execution_summary(state)

    # Final message
    print("\n" + "=" * 80)
    print("🎉 DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\n💡 Key Takeaways:")
    print("   1. The supervisor automatically routes tasks to appropriate agents")
    print("   2. Agents can be added, removed, and managed dynamically")
    print("   3. Complex multi-step tasks are handled through the ReAct loop")
    print("   4. Each agent execution is tracked with metadata")
    print("\n🚀 The dynamic supervisor is ready for production use!")


async def main():
    """Main execution function."""
    try:
        await demonstrate_full_workflow()
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Note: This example uses mock LLM responses for demonstration
    # In production, ensure you have proper Azure OpenAI credentials configured
    print("\n⚠️  Note: This example requires configured Azure OpenAI credentials")
    print(
        "   Set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT environment variables\n"
    )

    asyncio.run(main())
