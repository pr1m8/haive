#!/usr/bin/env python
"""Comprehensive test suite for DynamicMultiAgent."""

import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Test Agents
class ResearchAgent:
    """Test research agent."""

    def __init__(self, name: str = "research_agent"):
        self.name = name
        self.capability = "research, information gathering, web search, fact-finding"
        self.execution_count = 0
        self.state_schema = TestAgentState  # Simple state schema

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute research task."""
        self.execution_count += 1

        messages = state.get("messages", [])
        last_msg = messages[-1] if messages else None
        content = getattr(last_msg, "content", "")

        # Simulate research
        response = AIMessage(
            content=f"🔍 Research findings for '{content[:50]}...': "
            f"Found {self.execution_count * 5} relevant sources. "
            f"Key insights: [Data point 1, Data point 2, Data point 3]"
        )

        return {"messages": [*messages, response]}


class WritingAgent:
    """Test writing agent."""

    def __init__(self, name: str = "writing_agent"):
        self.name = name
        self.capability = "writing, content creation, documentation, storytelling"
        self.execution_count = 0
        self.state_schema = TestAgentState

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute writing task."""
        self.execution_count += 1

        messages = state.get("messages", [])

        response = AIMessage(
            content=f"✍️ Written content (Draft #{self.execution_count}): "
            f"Here's a professionally crafted response addressing your request. "
            f"[Paragraph 1] [Paragraph 2] [Conclusion]"
        )

        return {"messages": [*messages, response]}


class CodingAgent:
    """Test coding agent."""

    def __init__(self, name: str = "code_agent"):
        self.name = name
        self.capability = "coding, programming, debugging, code review, implementation"
        self.execution_count = 0
        self.state_schema = TestAgentState

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute coding task."""
        self.execution_count += 1

        messages = state.get("messages", [])

        response = AIMessage(
            content=f"💻 Code implementation (v{self.execution_count}):\n"
            f"```python\n"
            f"def solution():\n"
            f"    # Implementation here\n"
            f"    return 'result'\n"
            f"```\n"
            f"Tests passed: ✅"
        )

        return {"messages": [*messages, response]}


class AnalysisAgent:
    """Test analysis agent."""

    def __init__(self, name: str = "analysis_agent"):
        self.name = name
        self.capability = "analysis, data processing, insights, evaluation"
        self.execution_count = 0

    async def ainvoke(self, state: dict[str, Any]) -> dict[str, Any]:
        """Execute analysis task."""
        self.execution_count += 1

        messages = state.get("messages", [])

        response = AIMessage(
            content=f"📊 Analysis Report #{self.execution_count}:\n"
            f"- Pattern detected: [Pattern A]\n"
            f"- Trend analysis: [Upward trend]\n"
            f"- Recommendation: [Action item]\n"
            f"- Confidence: 87%"
        )

        return {"messages": [*messages, response]}


# Test state schema
class TestAgentState(BaseModel):
    """Simple test state schema."""

    messages: list[BaseMessage] = Field(default_factory=list)
    context: str = Field(default="")


async def test_basic_dynamic_multi_agent():
    """Test basic DynamicMultiAgent functionality."""

    # Import our implementation
    try:
        from dynamic_multi_agent import DynamicMultiAgent, create_dynamic_multi_agent
    except ImportError:
        return False

    # Create agents
    research = ResearchAgent()
    writing = WritingAgent()

    # Create dynamic multi-agent
    multi_agent = create_dynamic_multi_agent(
        agents=[research, writing],
        name="test_dynamic_multi",
        enable_capability_routing=True,
        track_performance=True,
    )


    # Test execution

    # Research request
    result1 = await multi_agent.ainvoke(
        {"messages": [HumanMessage(content="Research the latest AI developments")]}
    )


    # Writing request
    result2 = await multi_agent.ainvoke(
        {"messages": [HumanMessage(content="Write a blog post about productivity")]}
    )


    return True


async def test_dynamic_agent_management():
    """Test dynamic agent addition and removal."""

    from dynamic_multi_agent import DynamicMultiAgent

    # Start with minimal agents
    multi_agent = DynamicMultiAgent(
        name="dynamic_test", agents=[ResearchAgent(), WritingAgent()]
    )


    # Test with initial agents
    result1 = await multi_agent.ainvoke(
        {"messages": [HumanMessage(content="Write code to solve this problem")]}
    )

    # Should default to an existing agent since no coding agent

    # Add coding agent dynamically
    coding = CodingAgent()
    success = multi_agent.register_agent_dynamically(
        coding, capability="coding and software development"
    )


    # Test with coding request
    result2 = await multi_agent.ainvoke(
        {
            "messages": [
                HumanMessage(content="Write code to implement a sorting algorithm")
            ]
        }
    )


    # Add analysis agent
    analysis = AnalysisAgent()
    multi_agent.register_agent_dynamically(analysis)

    # Remove writing agent
    removed = multi_agent.unregister_agent_dynamically("writing_agent")

    # Test that writing requests now go elsewhere
    result3 = await multi_agent.ainvoke(
        {"messages": [HumanMessage(content="Write a summary of the findings")]}
    )


    return True


async def test_performance_tracking():
    """Test performance tracking and agent selection."""

    from dynamic_multi_agent import DynamicMultiAgent

    # Create system with performance tracking
    multi_agent = DynamicMultiAgent(
        name="performance_test",
        agents=[ResearchAgent(), WritingAgent(), CodingAgent()],
        track_performance=True,
    )

    # Execute multiple requests

    requests = [
        "Research machine learning trends",
        "Write about AI ethics",
        "Code a neural network",
        "Analyze the research findings",
        "Research quantum computing",
        "Write technical documentation",
    ]

    for i, request in enumerate(requests):
        result = await multi_agent.ainvoke(
            {"messages": [HumanMessage(content=request)]}
        )

    # Check performance metrics

    for agent_name in multi_agent.agents:
        metrics = multi_agent.get_agent_performance(agent_name)

    # Check execution history
    history = multi_agent.get_execution_history(limit=3)
    for entry in history:
        pass

    return True


async def test_capability_routing():
    """Test capability-based routing."""

    from dynamic_multi_agent import DynamicMultiAgent

    # Create agents with specific capabilities
    # Create specialized agents
    agents = [
        ResearchAgent("research_agent"),
        WritingAgent("writing_agent"),
        CodingAgent("python_expert"),
        AnalysisAgent("data_analyst"),
    ]

    multi_agent = DynamicMultiAgent(
        name="capability_test", agents=agents, enable_capability_routing=True
    )

    # Show capabilities
    capabilities = multi_agent.get_agent_capabilities()
    for agent, capability in capabilities.items():
        pass

    # Test routing

    test_cases = [
        ("I need to gather information about blockchain", "research_agent"),
        ("Help me write a compelling story", "writing_agent"),
        ("Debug this Python code for me", "python_expert"),
        ("Analyze these data patterns", "data_analyst"),
        ("Find facts about quantum computing", "research_agent"),
        ("Create documentation for the API", "writing_agent"),
    ]

    correct_routes = 0
    for request, expected_agent in test_cases:
        result = await multi_agent.ainvoke(
            {"messages": [HumanMessage(content=request)]}
        )

        actual_agent = result.get("last_agent")
        is_correct = actual_agent == expected_agent
        correct_routes += is_correct



    return True


async def test_complex_conversation():
    """Test a complex multi-turn conversation."""

    from dynamic_multi_agent import DynamicMultiAgent

    # Create comprehensive system

    multi_agent = DynamicMultiAgent(
        name="conversation_test",
        agents=[ResearchAgent(), WritingAgent(), CodingAgent(), AnalysisAgent()],
        enable_capability_routing=True,
        track_performance=True,
    )

    # Multi-turn conversation

    messages = []

    # Turn 1: Research
    messages.append(HumanMessage(content="Research the latest trends in AI agents"))
    result1 = await multi_agent.ainvoke({"messages": messages})
    messages = result1.get("messages", messages)

    # Turn 2: Analysis
    messages.append(HumanMessage(content="Analyze the key findings from the research"))
    result2 = await multi_agent.ainvoke({"messages": messages})
    messages = result2.get("messages", messages)

    # Turn 3: Coding
    messages.append(
        HumanMessage(content="Write code to implement one of these AI agent patterns")
    )
    result3 = await multi_agent.ainvoke({"messages": messages})
    messages = result3.get("messages", messages)

    # Turn 4: Documentation
    messages.append(HumanMessage(content="Write documentation for the implementation"))
    result4 = await multi_agent.ainvoke({"messages": messages})
    messages = result4.get("messages", messages)

    # Summary

    # Performance after conversation
    for agent_name in multi_agent.agents:
        agent = multi_agent.agents[agent_name]

    return True


async def run_all_tests():
    """Run all test cases."""

    tests = [
        ("Basic Functionality", test_basic_dynamic_multi_agent),
        ("Dynamic Agent Management", test_dynamic_agent_management),
        ("Performance Tracking", test_performance_tracking),
        ("Capability Routing", test_capability_routing),
        ("Complex Conversation", test_complex_conversation),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            success = await test_func()
            results.append((test_name, success))
        except Exception as e:
            import traceback

            traceback.print_exc()
            results.append((test_name, False))

    # Summary

    passed = sum(1 for _, success in results if success)
    total = len(results)

    for test_name, success in results:
        pass'}")


    if passed == total:
        pass.")

    # Key insights


if __name__ == "__main__":
    asyncio.run(run_all_tests())
