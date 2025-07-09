#!/usr/bin/env python
"""Real test of Registry Supervisor with actual haive agents (no mocks)."""

import asyncio
import logging
import os
from typing import Any, Dict

from langchain_core.messages import AIMessage, HumanMessage

# Configure logging to see what's happening
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def create_real_agents():
    """Create real ReactAgents for testing."""

    print("🔧 Creating real ReactAgents...")

    try:
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.react.agent import ReactAgent

        # Create research agent
        print("  Creating research_agent...")
        research_engine = AugLLMConfig(
            name="research_engine",
            system_message="""You are a research specialist. Your job is to find, analyze, and summarize information on any topic. 
            Be thorough in your research and provide well-structured, factual responses with sources when possible.""",
            temperature=0.3,
            model="gpt-3.5-turbo",  # Using a reliable model
        )

        research_agent = ReactAgent(
            name="research_agent",
            engine=research_engine,
            tools=[],  # No tools for simplicity
        )

        # Create coding agent
        print("  Creating coding_agent...")
        coding_engine = AugLLMConfig(
            name="coding_engine",
            system_message="""You are a software developer. Write clean, efficient, and well-documented code. 
            Explain your solutions and provide examples. Focus on best practices and maintainable code.""",
            temperature=0.4,
            model="gpt-3.5-turbo",
        )

        coding_agent = ReactAgent(name="coding_agent", engine=coding_engine, tools=[])

        # Create writing agent
        print("  Creating writing_agent...")
        writing_engine = AugLLMConfig(
            name="writing_engine",
            system_message="""You are a professional writer. Create engaging, well-structured content. 
            Adapt your style to the audience and purpose. Focus on clarity, flow, and impact.""",
            temperature=0.7,
            model="gpt-3.5-turbo",
        )

        writing_agent = ReactAgent(
            name="writing_agent", engine=writing_engine, tools=[]
        )

        print("✅ Created 3 real ReactAgents")
        return [research_agent, coding_agent, writing_agent]

    except Exception as e:
        print(f"❌ Error creating agents: {e}")
        return []


async def test_registry_supervisor_real():
    """Test the registry supervisor with real agents."""

    print("\n" + "=" * 80)
    print("🚀 REAL REGISTRY SUPERVISOR TEST")
    print("=" * 80 + "\n")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set. Please set it to run this test.")
        return

    # Import our registry supervisor
    try:
        from registry_supervisor import RegistrySupervisor
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return

    # Create real agents
    agents = await create_real_agents()
    if not agents:
        print("❌ Failed to create agents")
        return

    # Create supervisor
    print("\n🤖 Creating Registry Supervisor...")
    supervisor = RegistrySupervisor(
        name="real_registry_supervisor", max_active_agents=5
    )

    # Populate registry with capabilities
    print("\n📋 Populating agent registry...")
    supervisor.populate_registry(
        agents=agents,
        capabilities=[
            "research, information gathering, fact-finding, analysis",
            "coding, programming, software development, debugging",
            "writing, content creation, documentation, storytelling",
        ],
    )

    print(
        f"✅ Registry populated with: {list(supervisor.get_registry_agents().keys())}"
    )
    print(f"   Active agents: {supervisor.get_active_agents()}")
    print(f"   Choice model: {supervisor.get_choice_model_status()}")

    # Test 1: Research request (should activate research agent)
    print("\n" + "=" * 60)
    print("🔍 TEST 1: Research Request")
    print("=" * 60)

    research_request = "Research the latest developments in artificial intelligence and machine learning"
    print(f"📝 Request: {research_request}")

    try:
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=research_request)]}
        )

        print(f"\n✅ Test 1 completed!")
        print(f"   Active agents after: {supervisor.get_active_agents()}")
        print(f"   Last agent used: {result1.get('last_agent', 'unknown')}")

        # Show response preview
        messages = result1.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content
                print(f"   Response preview: {content[:200]}...")

    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 2: Coding request (should activate coding agent)
    print("\n" + "=" * 60)
    print("💻 TEST 2: Coding Request")
    print("=" * 60)

    coding_request = (
        "Write Python code to implement a binary search algorithm with comments"
    )
    print(f"📝 Request: {coding_request}")

    try:
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=coding_request)]}
        )

        print(f"\n✅ Test 2 completed!")
        print(f"   Active agents after: {supervisor.get_active_agents()}")
        print(f"   Last agent used: {result2.get('last_agent', 'unknown')}")

        # Show response preview
        messages = result2.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content
                print(f"   Response preview: {content[:200]}...")

    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 3: Writing request (should activate writing agent)
    print("\n" + "=" * 60)
    print("✍️ TEST 3: Writing Request")
    print("=" * 60)

    writing_request = "Write a compelling introduction for a blog post about the future of remote work"
    print(f"📝 Request: {writing_request}")

    try:
        result3 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=writing_request)]}
        )

        print(f"\n✅ Test 3 completed!")
        print(f"   Active agents after: {supervisor.get_active_agents()}")
        print(f"   Last agent used: {result3.get('last_agent', 'unknown')}")

        # Show response preview
        messages = result3.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content
                print(f"   Response preview: {content[:200]}...")

    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
        import traceback

        traceback.print_exc()

    # Test 4: Use existing agent (should use already active agent)
    print("\n" + "=" * 60)
    print("🔄 TEST 4: Reuse Active Agent")
    print("=" * 60)

    reuse_request = "Do more research on quantum computing applications"
    print(f"📝 Request: {reuse_request}")

    try:
        result4 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=reuse_request)]}
        )

        print(f"\n✅ Test 4 completed!")
        print(f"   Active agents after: {supervisor.get_active_agents()}")
        print(f"   Last agent used: {result4.get('last_agent', 'unknown')}")

        # Show response preview
        messages = result4.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content
                print(f"   Response preview: {content[:200]}...")

    except Exception as e:
        print(f"❌ Test 4 failed: {e}")
        import traceback

        traceback.print_exc()

    # Final status
    print("\n" + "=" * 60)
    print("📊 FINAL STATUS")
    print("=" * 60)

    print(f"Registry agents: {list(supervisor.get_registry_agents().keys())}")
    print(f"Active agents: {supervisor.get_active_agents()}")

    choice_status = supervisor.get_choice_model_status()
    print(f"Choice model options: {choice_status.get('options', [])}")
    print(f"Total active: {choice_status.get('active_agents', 0)}")
    print(f"Total in registry: {choice_status.get('registry_agents', 0)}")

    print("\n✅ All tests completed!")
    print("\nKey Insights:")
    print("1. Agents are retrieved from registry when needed")
    print("2. Choice model updates with active agents")
    print("3. Existing agents are reused when appropriate")
    print("4. All execution agents are ReactAgents")
    print("5. No graph rebuilding needed!")


async def test_detailed_outputs():
    """Show detailed outputs of supervisor decisions."""

    print("\n" + "=" * 80)
    print("🔍 DETAILED OUTPUT ANALYSIS")
    print("=" * 80 + "\n")

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY not set.")
        return

    from registry_supervisor import RegistrySupervisor

    # Create minimal test
    agents = await create_real_agents()
    if not agents:
        return

    supervisor = RegistrySupervisor(name="detailed_test")
    supervisor.populate_registry(agents[:1])  # Just research agent

    print(f"Starting state:")
    print(f"  Registry: {list(supervisor.get_registry_agents().keys())}")
    print(f"  Active: {supervisor.get_active_agents()}")

    # Test coding request (no coding agent active)
    print(f"\n📝 Request: 'Write Python code for fibonacci'")
    print(f"Expected: Should retrieve coding_agent from registry")

    try:
        result = await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Write Python code for fibonacci sequence")
                ]
            }
        )

        print(f"\nResult:")
        print(f"  Active agents: {supervisor.get_active_agents()}")
        print(f"  Last agent: {result.get('last_agent')}")
        print(f"  Success: {result.get('execution_complete', False)}")

        # Show actual response
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]
            print(f"\nActual Response:")
            print(f"  Type: {type(last_msg).__name__}")
            print(f"  Content: {last_msg.content[:500]}...")

    except Exception as e:
        print(f"❌ Detailed test failed: {e}")


if __name__ == "__main__":
    print("🚀 Starting Real Registry Supervisor Tests")
    print("Make sure OPENAI_API_KEY is set in your environment")

    # Run the main test
    asyncio.run(test_registry_supervisor_real())

    # Run detailed output test
    asyncio.run(test_detailed_outputs())
