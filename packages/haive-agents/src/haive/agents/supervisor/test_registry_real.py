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

    try:
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.react.agent import ReactAgent

        # Create research agent
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
        coding_engine = AugLLMConfig(
            name="coding_engine",
            system_message="""You are a software developer. Write clean, efficient, and well-documented code.
            Explain your solutions and provide examples. Focus on best practices and maintainable code.""",
            temperature=0.4,
            model="gpt-3.5-turbo",
        )

        coding_agent = ReactAgent(name="coding_agent", engine=coding_engine, tools=[])

        # Create writing agent
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

        return [research_agent, coding_agent, writing_agent]

    except Exception as e:
        return []


async def test_registry_supervisor_real():
    """Test the registry supervisor with real agents."""

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        return

    # Import our registry supervisor
    try:
        from registry_supervisor import RegistrySupervisor
    except ImportError as e:
        return

    # Create real agents
    agents = await create_real_agents()
    if not agents:
        return

    # Create supervisor
    supervisor = RegistrySupervisor(
        name="real_registry_supervisor", max_active_agents=5
    )

    # Populate registry with capabilities
    supervisor.populate_registry(
        agents=agents,
        capabilities=[
            "research, information gathering, fact-finding, analysis",
            "coding, programming, software development, debugging",
            "writing, content creation, documentation, storytelling",
        ],
    )


    # Test 1: Research request (should activate research agent)

    research_request = "Research the latest developments in artificial intelligence and machine learning"

    try:
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=research_request)]}
        )


        # Show response preview
        messages = result1.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 2: Coding request (should activate coding agent)

    coding_request = (
        "Write Python code to implement a binary search algorithm with comments"
    )

    try:
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=coding_request)]}
        )


        # Show response preview
        messages = result2.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 3: Writing request (should activate writing agent)

    writing_request = "Write a compelling introduction for a blog post about the future of remote work"

    try:
        result3 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=writing_request)]}
        )


        # Show response preview
        messages = result3.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Test 4: Use existing agent (should use already active agent)

    reuse_request = "Do more research on quantum computing applications"

    try:
        result4 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content=reuse_request)]}
        )


        # Show response preview
        messages = result4.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                content = last_message.content

    except Exception as e:
        import traceback

        traceback.print_exc()

    # Final status


    choice_status = supervisor.get_choice_model_status()



async def test_detailed_outputs():
    """Show detailed outputs of supervisor decisions."""

    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        return

    from registry_supervisor import RegistrySupervisor

    # Create minimal test
    agents = await create_real_agents()
    if not agents:
        return

    supervisor = RegistrySupervisor(name="detailed_test")
    supervisor.populate_registry(agents[:1])  # Just research agent


    # Test coding request (no coding agent active)

    try:
        result = await supervisor.ainvoke(
            {
                "messages": [
                    HumanMessage(content="Write Python code for fibonacci sequence")
                ]
            }
        )


        # Show actual response
        messages = result.get("messages", [])
        if messages:
            last_msg = messages[-1]

    except Exception as e:
        pass")


if __name__ == "__main__":

    # Run the main test
    asyncio.run(test_registry_supervisor_real())

    # Run detailed output test
    asyncio.run(test_detailed_outputs())
