#!/usr/bin/env python3
"""Demo of static supervisor with ReactAgent inheritance and state sync."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import logging

from haive.agents.experiments.static_supervisor_with_sync import (
    StaticSupervisor,
    SupervisorReactState,
)
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent
from langchain_core.messages import HumanMessage

# Configure detailed logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


# Mock engine for testing
class MockEngine:
    """Mock engine that shows what would be executed."""

    def __init__(self, name: str, system_message: str = ""):
        self.name = name
        self.system_message = system_message
        self.tools = []

    def invoke(self, messages):
        """Simulate engine response."""
        # Simulate different responses based on system message
        if "research" in self.system_message.lower():
            return {"content": "Research findings: Information about the topic..."}
        if "code" in self.system_message.lower():
            return {"content": "def solution():\n    return 'Code implementation'"}
        # For supervisor, show decision process
        return {
            "content": "I'll help you with that task. Let me check available agents.",
            "tool_calls": [{"name": "list_agents", "id": "call_1", "args": {}}],
        }


async def demonstrate_static_supervisor():
    """Show how the static supervisor works with state synchronization."""
    # Create supervisor with mock engine
    supervisor_engine = MockEngine(
        name="supervisor_engine", system_message="You are a task routing supervisor"
    )

    # Note: In real usage, you'd use AugLLMEngine
    supervisor = StaticSupervisor(name="task_supervisor", engine=supervisor_engine)

    # Create and register agents

    research_agent = SimpleAgent(
        name="research_agent",
        engine=MockEngine(
            name="research_engine", system_message="You are a research assistant"
        ),
    )

    coding_agent = ReactAgent(
        name="coding_agent",
        engine=MockEngine(
            name="coding_engine", system_message="You are a Python coding expert"
        ),
    )

    # Register agents - triggers model validator
    supervisor.register_agent(
        name="research_agent",
        description="Handles research and information gathering",
        agent=research_agent,
    )

    supervisor.register_agent(
        name="coding_agent",
        description="Handles code generation and debugging",
        agent=coding_agent,
    )

    state = supervisor.get_state()

    # Show serialization works
    for _name, entry in state.registered_agents.items():
        entry.get_agent()

    # Demonstrate tool node execution

    # Simulate state with tool call
    test_state = SupervisorReactState(
        messages=[
            HumanMessage(content="Write Python code to sort a list"),
            # Simulate AI response with tool call
            type(
                "AIMessage",
                (),
                {
                    "content": "I'll hand this off to the coding agent",
                    "tool_calls": [
                        {
                            "name": "coding_agent",
                            "id": "call_123",
                            "args": {"task": "Write Python code to sort a list"},
                        }
                    ],
                },
            )(),
        ],
        registered_agents=state.registered_agents,
        handoff_tools=state.handoff_tools,
    )

    # Execute tool node
    supervisor._execute_tool_or_agent(test_state)


if __name__ == "__main__":
    asyncio.run(demonstrate_static_supervisor())
