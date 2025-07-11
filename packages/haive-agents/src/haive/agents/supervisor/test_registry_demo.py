#!/usr/bin/env python
"""Demo of Registry Supervisor behavior without requiring API keys."""

import asyncio
import logging
from typing import Any, Dict, List

from langchain_core.messages import AIMessage, HumanMessage

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class MockEngine:
    """Mock engine that simulates responses without API calls."""

    def __init__(self, name: str, response_template: str):
        self.name = name
        self.response_template = response_template
        self.call_count = 0

    async def ainvoke(self, input_data: dict[str, Any], config=None) -> dict[str, Any]:
        """Mock async invoke."""
        self.call_count += 1

        messages = input_data.get("messages", [])
        last_message = messages[-1] if messages else None
        content = getattr(last_message, "content", "")

        # Generate mock response
        response_content = self.response_template.format(
            request=content[:50], call_num=self.call_count
        )

        response = AIMessage(content=response_content)
        return {"messages": [*messages, response]}


class MockReactAgent:
    """Mock ReactAgent for demonstration."""

    def __init__(self, name: str, engine: MockEngine, tools: list = None):
        self.name = name
        self.engine = engine
        self.tools = tools or []
        self.execution_count = 0

    async def ainvoke(self, input_data: dict[str, Any], config=None) -> dict[str, Any]:
        """Mock agent execution."""
        self.execution_count += 1

        # Simulate agent processing
        result = await self.engine.ainvoke(input_data, config)

        logger.info(f"🤖 {self.name} executed (count: {self.execution_count})")
        return result


async def create_mock_agents():
    """Create mock ReactAgents for demonstration."""

    # Research agent
    research_engine = MockEngine(
        "research_engine",
        "🔍 Research findings for '{request}': Based on my analysis, here are the key insights... (execution #{call_num})",
    )
    research_agent = MockReactAgent("research_agent", research_engine)

    # Coding agent
    coding_engine = MockEngine(
        "coding_engine",
        "💻 Code implementation for '{request}':\n```python\ndef solution():\n    # Implementation here\n    pass\n```\n(execution #{call_num})",
    )
    coding_agent = MockReactAgent("coding_agent", coding_engine)

    # Writing agent
    writing_engine = MockEngine(
        "writing_engine",
        "✍️ Written content for '{request}': Here's a well-crafted response that addresses your needs... (execution #{call_num})",
    )
    writing_agent = MockReactAgent("writing_agent", writing_engine)

    return [research_agent, coding_agent, writing_agent]


class MockRegistrySupervisor:
    """Simplified mock of the registry supervisor to demonstrate behavior."""

    def __init__(self, name: str):
        self.name = name
        self.registry_agents = {}
        self.active_agents = {}
        self.choice_model_options = ["END"]
        self.execution_log = []

    def populate_registry(
        self, agents: list[MockReactAgent], capabilities: list[str] = None
    ):
        """Populate registry with agents."""
        for i, agent in enumerate(agents):
            capability = (
                capabilities[i]
                if capabilities and i < len(capabilities)
                else f"General tasks for {agent.name}"
            )
            self.registry_agents[agent.name] = {
                "agent": agent,
                "capability": capability,
            }


    def _update_choice_model(self):
        """Update choice model with active agents."""
        self.choice_model_options = [*list(self.active_agents.keys()), "END"]

    def _select_agent_from_registry(self, task: str) -> str:
        """Simulate agent selection from registry."""
        task_lower = task.lower()

        # Check if we need to get an agent from registry
        for agent_name, agent_info in self.registry_agents.items():
            capability = agent_info["capability"].lower()

            # Simple matching
            if "research" in capability and any(
                word in task_lower for word in ["research", "find", "search"]
            ):
                return agent_name
            elif "writing" in capability and any(
                word in task_lower for word in ["write", "create", "draft"]
            ):
                return agent_name

        # Return first available as fallback
        return next(iter(self.registry_agents.keys())) if self.registry_agents else None

    def _select_from_active(self, task: str) -> str:
        """Select from currently active agents."""
        if not self.active_agents:
            return None

        task_lower = task.lower()

        # Check active agents
        for agent_name in self.active_agents:
            if "research" in agent_name and any(
                word in task_lower for word in ["research", "find"]
            ):
                return agent_name
            elif "writing" in agent_name and any(
                word in task_lower for word in ["write", "create"]
            ):
                return agent_name

        # Return first active
        return next(iter(self.active_agents.keys()))

    async def ainvoke(self, input_data: dict[str, Any]) -> dict[str, Any]:
        """Simulate supervisor execution."""
        messages = input_data.get("messages", [])
        if not messages:
            return {"messages": messages, "error": "No messages"}

        last_message = messages[-1]
        task = getattr(last_message, "content", "")


        # Step 1: Try to use active agent
        selected_agent = self._select_from_active(task)

        if selected_agent:
            pass")
        else:
            # Step 2: Get agent from registry
            registry_agent = self._select_agent_from_registry(task)

            if registry_agent:

                # Add to active
                agent_info = self.registry_agents[registry_agent]
                self.active_agents[registry_agent] = agent_info["agent"]
                self._update_choice_model()

                selected_agent = registry_agent
            else:
                return {"messages": messages, "error": "No agent available"}

        # Step 3: Execute the agent
        agent = self.active_agents[selected_agent]

        result = await agent.ainvoke(input_data)

        # Log execution
        self.execution_log.append(
            {
                "task": task,
                "agent": selected_agent,
                "was_active": selected_agent in self.active_agents,
            }
        )

        result["last_agent"] = selected_agent
        result["execution_complete"] = True

        return result

    def get_status(self) -> dict[str, Any]:
        """Get current status."""
        return {
            "registry_agents": list(self.registry_agents.keys()),
            "active_agents": list(self.active_agents.keys()),
            "choice_model_options": self.choice_model_options,
            "execution_count": len(self.execution_log),
        }


async def demo_registry_supervisor():
    """Demonstrate the registry supervisor behavior."""

    # Create mock agents
    agents = await create_mock_agents()

    # Create supervisor
    supervisor = MockRegistrySupervisor("demo_supervisor")

    # Populate registry
    supervisor.populate_registry(
        agents,
        capabilities=[
            "research, information gathering, analysis",
            "coding, programming, software development",
            "writing, content creation, documentation",
        ],
    )

    # Show initial status
    status = supervisor.get_status()
    for key, value in status.items():
        pass

    # Test 1: Research request

    result1 = await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Research the latest AI developments")]}
    )


    # Show response
    messages = result1.get("messages", [])
    if messages:
        last_msg = messages[-1]

    # Show updated status
    status = supervisor.get_status()
    for key, value in status.items():
        pass

    # Test 2: Coding request

    result2 = await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Write Python code for binary search")]}
    )


    # Show response
    messages = result2.get("messages", [])
    if messages:
        last_msg = messages[-1]

    # Test 3: Another research request (should use existing)

    result3 = await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Find information about quantum computing")]}
    )


    # Test 4: Writing request

    result4 = await supervisor.ainvoke(
        {"messages": [HumanMessage(content="Write a blog post about remote work")]}
    )


    # Final status

    status = supervisor.get_status()
    for key, value in status.items():
        pass

    # Show execution log
    for i, log_entry in enumerate(supervisor.execution_log, 1):
        pass

    # Show agent execution counts
    for agent_name in supervisor.active_agents:
        agent = supervisor.active_agents[agent_name]




if __name__ == "__main__":

    asyncio.run(demo_registry_supervisor())
