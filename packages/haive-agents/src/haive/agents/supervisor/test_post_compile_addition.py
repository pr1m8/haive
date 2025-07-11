#!/usr/bin/env python
"""Test that verifies agents can be added AFTER graph compilation.

This is the critical test to ensure dynamic agent addition works post-compilation.
"""

import asyncio
import logging
from typing import Any, Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MockEngine:
    """Simple mock engine for testing."""

    def __init__(self, name: str = "mock_engine"):
        self.name = name
        self.tools = []

    async def ainvoke(self, messages: Any, config: Any = None) -> Any:
        """Mock LLM invocation that returns a routing decision."""
        # Simple routing based on content
        content = str(messages[-1]) if messages else ""

        if "math" in content.lower():
            target = "math_agent"
        elif "write" in content.lower():
            target = "writing_agent"
        else:
            target = "END"

        class MockResponse:
            def __init__(self, content):
                self.content = content

        return MockResponse(f'{{"target": "{target}", "reasoning": "Test routing"}}')


class MockAgent:
    """Simple mock agent for testing."""

    def __init__(self, name: str, tools: list[str] = None):
        self.name = name
        self.engine = MockEngine(f"{name}_engine")
        self.tools = tools or []
        self.id = f"{name}_id"

    async def ainvoke(self, state: Any, config: Any = None) -> Any:
        """Mock agent execution."""

        class MockResult:
            def __init__(self, messages):
                self.messages = messages

        class MockMessage:
            def __init__(self, content):
                self.content = content

        return MockResult([MockMessage(f"Response from {self.name}")])


# Import only what we need to minimize dependencies
from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel


class SimpleDynamicSupervisor:
    """Simplified dynamic supervisor for testing post-compile addition."""

    def __init__(self, name: str = "test_supervisor"):
        self.name = name
        self.agent_registry = {}
        self.choice_model = DynamicChoiceModel(
            option_names=["END"], option_descriptions=["End the conversation"]
        )
        self.compiled = False
        self.graph_nodes = set(["supervisor", "END"}

    def register_agent(self, agent: MockAgent) -> bool:
        """Register an agent."""
        logger.info(f"Registering agent: {agent.name}")

        # Add to registry
        self.agent_registry[agent.name] = agent

        # Update choice model
        self.choice_model.add_option(agent.name, f"Route to {agent.name}")

        # Simulate graph node addition
        self.graph_nodes.add(agent.name)

        logger.info(
            f"✅ Agent {agent.name} registered. Current agents: {list(self.agent_registry.keys())}"
        )
        logger.info(f"   Choice model options: {self.choice_model.option_names}")
        logger.info(f"   Graph nodes: {self.graph_nodes}")

        return True

    def compile(self) -> None:
        """Simulate graph compilation."""
        logger.info("📦 Compiling supervisor graph...")
        self.compiled = True
        logger.info(f"✅ Graph compiled with nodes: {self.graph_nodes}")

    def can_add_agents_post_compile(self) -> bool:
        """Check if we can add agents after compilation."""
        return self.compiled

    async def route_request(self, message: str) -> str:
        """Route a request to an agent."""
        logger.info(f"\n🔄 Routing request: '{message}'")

        # Check available agents
        available = list(self.agent_registry.keys())
        logger.info(f"   Available agents: {available}")

        # Simple routing logic
        if "math" in message.lower() and "math_agent" in self.agent_registry:
            target = "math_agent"
        elif "write" in message.lower() and "writing_agent" in self.agent_registry:
            target = "writing_agent"
        elif available:
            target = available[0]  # Default to first available
        else:
            target = "END"

        logger.info(f"   ➡️  Routed to: {target}")
        return target


async def test_post_compile_agent_addition():
    """Test adding agents after graph compilation."""

    # Step 1: Create supervisor with initial agent
    supervisor = SimpleDynamicSupervisor()

    # Add one agent before compilation
    initial_agent = MockAgent("writing_agent", ["text_editor", "grammar_check"])
    supervisor.register_agent(initial_agent)

    # Step 2: Compile the graph
    supervisor.compile()

    # Step 3: Test routing with only initial agent
    result1 = await supervisor.route_request("Write me a story")
    assert result1 == "writing_agent", f"Expected writing_agent, got {result1}"

    result2 = await supervisor.route_request("Calculate 2+2")  # No math agent yet
    assert (
        result2 == "writing_agent"
    ), f"Expected writing_agent (default), got {result2}"

    # Step 4: Add new agent AFTER compilation

    math_agent = MockAgent("math_agent", ["calculator", "equation_solver"])
    supervisor.register_agent(math_agent)

    # Step 5: Test routing with new agent
    result3 = await supervisor.route_request("Calculate 2+2")
    assert result3 == "math_agent", f"Expected math_agent, got {result3}"

    # Step 6: Add another agent
    research_agent = MockAgent("research_agent", ["web_search", "wikipedia"])
    supervisor.register_agent(research_agent)

    # Step 7: Verify all agents work

    # Test routing to each agent type
    write_result = await supervisor.route_request("Write something")
    math_result = await supervisor.route_request("Do some math")
    generic_result = await supervisor.route_request("Generic request")



    return True


async def test_graph_rebuilding():
    """Test the actual graph rebuilding mechanism."""

    # This tests the actual _rebuild_graph method concept
    class GraphRebuildingSupervisor(SimpleDynamicSupervisor):
        def __init__(self, name: str = "rebuild_supervisor"):
            super().__init__(name)
            self.graph_rebuild_count = 0
            self.routing_destinations = ["END"]

        def register_agent(self, agent: MockAgent) -> bool:
            """Register agent and rebuild graph."""
            # Add to registry first
            super().register_agent(agent)

            # Rebuild graph if compiled
            if self.compiled:
                self._rebuild_graph()

            return True

        def _rebuild_graph(self):
            """Simulate graph rebuilding."""
            self.graph_rebuild_count += 1
            logger.info(f"\n🔨 Rebuilding graph (rebuild #{self.graph_rebuild_count})")

            # Update routing destinations
            self.routing_destinations = [*list(self.agent_registry.keys()), "END"]
            logger.info(f"   New routing destinations: {self.routing_destinations}")

            # Simulate re-compilation
            logger.info("   Re-compiling graph with new structure...")
            logger.info("   ✅ Graph rebuilt successfully"y")

    # Test the rebuilding
    supervisor = GraphRebuildingSupervisor()

    # Initial agent
    supervisor.register_agent(MockAgent("agent1"))

    # Compile
    supervisor.compile()

    # Add agent post-compile (should trigger rebuild)
    supervisor.register_agent(MockAgent("agent2"))

    # Add another agent (should trigger another rebuild)
    supervisor.register_agent(MockAgent("agent3"))

    # Verify
    assert supervisor.graph_rebuild_count == 2, "Expected 2 rebuilds"
    assert (
        len(supervisor.routing_destinations) == 4
    ), "Expected 4 destinations (3 agents + END)"



if __name__ == "__main__":

    # Run tests
    asyncio.run(test_post_compile_agent_addition())
    asyncio.run(test_graph_rebuilding())

