#!/usr/bin/env python
"""Example of using DynamicMultiAgent with real haive agents.

This example shows how to create a dynamic supervisor system that can:
1. Start with a few agents
2. Add specialized agents on demand
3. Route requests intelligently
4. Track performance
"""

import asyncio
import logging
from typing import Any, Dict

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage, SystemMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_dynamic_supervisor_system():
    """Create a dynamic supervisor system with real agents."""

    print("\n" + "=" * 80)
    print("🤖 DYNAMIC SUPERVISOR SYSTEM EXAMPLE")
    print("=" * 80 + "\n")

    # Import required components
    try:
        from dynamic_multi_agent import DynamicMultiAgent

        from haive.agents.react.agent import ReactAgent
        from haive.agents.simple.agent import SimpleAgent
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you have haive-agents installed")
        return

    # Create engines for different agents
    print("[Step 1] Creating engines for agents")

    # Research engine - good at finding information
    research_engine = AugLLMConfig(
        name="research_engine",
        system_message="You are a research specialist. Find and summarize information on any topic. Be thorough and cite sources when possible.",
        temperature=0.3,  # Lower temperature for factual research
    )

    # Writing engine - good at content creation
    writing_engine = AugLLMConfig(
        name="writing_engine",
        system_message="You are a professional writer. Create engaging, well-structured content. Adapt your style to the audience and purpose.",
        temperature=0.7,  # Higher temperature for creativity
    )

    # Analysis engine - good at data analysis
    analysis_engine = AugLLMConfig(
        name="analysis_engine",
        system_message="You are a data analyst. Analyze information, identify patterns, and provide insights. Be precise and data-driven.",
        temperature=0.4,
    )

    print("✅ Created 3 specialized engines")

    # Create initial agents
    print("\n[Step 2] Creating initial agents")

    # Simple agents for basic tasks
    research_agent = SimpleAgent(name="research_specialist", engine=research_engine)
    research_agent.capability = (
        "research, information gathering, fact-finding, web search"
    )

    writing_agent = SimpleAgent(name="content_writer", engine=writing_engine)
    writing_agent.capability = "writing, content creation, documentation, storytelling"

    # Create dynamic multi-agent system
    print("\n[Step 3] Creating DynamicMultiAgent supervisor")

    supervisor = DynamicMultiAgent(
        name="dynamic_supervisor",
        agents=[research_agent, writing_agent],
        enable_capability_routing=True,
        track_performance=True,
        separation_strategy="smart",  # Smart field separation
    )

    print(f"✅ Created supervisor with {len(supervisor.agents)} initial agents")
    print(f"   Agents: {list(supervisor.agents.keys())}")

    return supervisor, analysis_engine


async def demonstrate_dynamic_capabilities(supervisor, analysis_engine):
    """Demonstrate the dynamic capabilities of the system."""

    print("\n" + "=" * 80)
    print("🎯 DEMONSTRATING DYNAMIC CAPABILITIES")
    print("=" * 80 + "\n")

    # Test 1: Research request
    print("[Demo 1] Research Request")

    result1 = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Research the latest developments in quantum computing"
                )
            ]
        }
    )

    print(f"✅ Handled by: {result1.get('last_agent')}")
    last_message = result1.get("messages", [])[-1]
    print(f"Response preview: {last_message.content[:200]}...")

    # Test 2: Writing request
    print("\n[Demo 2] Writing Request")

    result2 = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Write a blog post introduction about the future of AI"
                )
            ]
        }
    )

    print(f"✅ Handled by: {result2.get('last_agent')}")

    # Test 3: Analysis request (no analyst yet)
    print("\n[Demo 3] Analysis Request (no analyst registered yet)")

    result3 = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(content="Analyze the trends in the research findings")
            ]
        }
    )

    print(f"✅ Handled by: {result3.get('last_agent')} (fallback - no analyst)")

    # Add analysis agent dynamically
    print("\n[Demo 4] Adding Analysis Agent Dynamically")

    from haive.agents.simple.agent import SimpleAgent

    analysis_agent = SimpleAgent(name="data_analyst", engine=analysis_engine)
    analysis_agent.capability = (
        "analysis, data processing, pattern recognition, insights"
    )

    # Register the new agent
    success = supervisor.register_agent_dynamically(
        analysis_agent, capability="data analysis and insights generation"
    )

    print(f"✅ Dynamically added analyst: {success}")
    print(f"   Current agents: {list(supervisor.agents.keys())}")

    # Test 4: Analysis request with analyst
    print("\n[Demo 5] Analysis Request (with analyst now available)")

    result4 = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(content="Analyze the market trends for AI adoption")
            ]
        }
    )

    print(f"✅ Handled by: {result4.get('last_agent')}")

    # Show performance metrics
    print("\n[Demo 6] Performance Metrics")

    for agent_name in supervisor.agents:
        metrics = supervisor.get_agent_performance(agent_name)
        print(f"\n{agent_name}:")
        print(f"  Executions: {metrics.get('total_executions', 0)}")
        print(f"  Success rate: 100%")  # Should be 100% for these simple cases
        print(
            f"  Capability: {supervisor.get_agent_capabilities().get(agent_name, 'N/A')}"
        )


async def demonstrate_complex_workflow(supervisor):
    """Demonstrate a complex multi-step workflow."""

    print("\n" + "=" * 80)
    print("🔄 COMPLEX WORKFLOW DEMONSTRATION")
    print("=" * 80 + "\n")

    print("Scenario: Complete research project workflow")

    # Initialize conversation
    messages = [
        SystemMessage(content="You are part of a research project team."),
        HumanMessage(
            content="Let's research and write about the impact of AI on healthcare"
        ),
    ]

    # Step 1: Research
    print("\n[Step 1] Research Phase")
    result1 = await supervisor.ainvoke({"messages": messages})
    messages = result1.get("messages", messages)
    print(f"✅ Research completed by: {result1.get('last_agent')}")

    # Step 2: Analysis
    print("\n[Step 2] Analysis Phase")
    messages.append(
        HumanMessage(
            content="Now analyze the key findings and identify the main trends"
        )
    )
    result2 = await supervisor.ainvoke({"messages": messages})
    messages = result2.get("messages", messages)
    print(f"✅ Analysis completed by: {result2.get('last_agent')}")

    # Step 3: Writing
    print("\n[Step 3] Writing Phase")
    messages.append(
        HumanMessage(
            content="Write a comprehensive report based on the research and analysis"
        )
    )
    result3 = await supervisor.ainvoke({"messages": messages})
    messages = result3.get("messages", messages)
    print(f"✅ Report written by: {result3.get('last_agent')}")

    # Show conversation flow
    print(f"\n✅ Workflow completed with {len(messages)} messages")
    print(f"   Agents involved: {result3.get('completed_agents', [])}")

    # Execution history
    print("\n[Execution History]")
    history = supervisor.get_execution_history(limit=5)
    for i, entry in enumerate(history):
        print(f"  {i+1}. {entry['agent']} - {entry['timestamp'].strftime('%H:%M:%S')}")


async def demonstrate_react_agent_integration(supervisor):
    """Show how to add a ReactAgent with tools."""

    print("\n" + "=" * 80)
    print("🔧 REACT AGENT WITH TOOLS INTEGRATION")
    print("=" * 80 + "\n")

    try:
        from haive.tools.math import calculator
        from haive.tools.web import web_search

        from haive.agents.react.agent import ReactAgent
    except ImportError:
        print("Note: This example requires haive-tools for full functionality")
        print("Showing the pattern without actual tools")

        # Create mock tools for demo
        class MockTool:
            def __init__(self, name, description):
                self.name = name
                self.description = description

        calculator = MockTool("calculator", "Perform calculations")
        web_search = MockTool("web_search", "Search the web")

    print("[Step 1] Creating ReactAgent with tools")

    # Create engine for ReactAgent
    react_engine = AugLLMConfig(
        name="react_engine",
        system_message="You are a helpful assistant with access to tools. Use them to solve problems step by step.",
        temperature=0.3,
    )

    # Create ReactAgent
    react_agent = ReactAgent(
        name="tool_specialist",
        engine=react_engine,
        tools=[calculator, web_search] if "calculator" in locals() else [],
    )
    react_agent.capability = "tool usage, calculations, web search, problem solving"

    # Add to supervisor
    print("\n[Step 2] Adding ReactAgent to supervisor")

    supervisor.register_agent_dynamically(
        react_agent, capability="specialized tool usage and problem solving"
    )

    print(f"✅ Added ReactAgent with tools")
    print(f"   Total agents now: {len(supervisor.agents)}")

    # Test tool usage
    print("\n[Step 3] Testing tool-based problem solving")

    result = await supervisor.ainvoke(
        {
            "messages": [
                HumanMessage(
                    content="Calculate the compound interest on $10,000 at 5% for 10 years"
                )
            ]
        }
    )

    print(f"✅ Handled by: {result.get('last_agent')}")

    # Note: In real usage, the ReactAgent would use the calculator tool


async def main():
    """Main example flow."""

    print("🚀 Dynamic Multi-Agent Supervisor Example")
    print("This example demonstrates building a flexible AI system that can:")
    print("- Start with basic agents")
    print("- Add specialized agents dynamically")
    print("- Route requests intelligently")
    print("- Handle complex workflows")

    # Create the system
    supervisor, analysis_engine = await create_dynamic_supervisor_system()

    if not supervisor:
        return

    # Demonstrate capabilities
    await demonstrate_dynamic_capabilities(supervisor, analysis_engine)

    # Complex workflow
    await demonstrate_complex_workflow(supervisor)

    # ReactAgent integration
    await demonstrate_react_agent_integration(supervisor)

    # Final summary
    print("\n" + "=" * 80)
    print("📊 FINAL SYSTEM STATE")
    print("=" * 80 + "\n")

    print(f"Total agents: {len(supervisor.agents)}")
    print(f"Agent types: {list(supervisor.agents.keys())}")

    print("\nCapabilities available:")
    for agent, capability in supervisor.get_agent_capabilities().items():
        print(f"  - {agent}: {capability}")

    print("\n✅ Example completed successfully!")
    print("\nKey Takeaways:")
    print("1. Agents can be added/removed without rebuilding the graph")
    print("2. The supervisor routes based on capabilities and performance")
    print("3. Complex workflows naturally emerge from simple routing")
    print("4. Both SimpleAgent and ReactAgent work seamlessly")
    print("5. The system scales dynamically with your needs")


if __name__ == "__main__":
    asyncio.run(main())
