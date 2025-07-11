#!/usr/bin/env python
"""Test to verify agents can be added AFTER graph compilation.

This is a critical test to ensure the dynamic supervisor design works correctly.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from langgraph.graph import END, START, StateGraph

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Mock classes to simulate the real system
class MockAgent:
    """Simulated agent."""

    def __init__(self, name: str):
        self.name = name

    async def process(self, state: dict) -> dict:
        """Process state and return updated state."""
        messages = state.get("messages", [])
        messages.append(f"Processed by {self.name}")
        return {"messages": messages, "last_agent": self.name}


class DynamicGraphManager:
    """Manages a LangGraph that can be modified after compilation."""

    def __init__(self):
        self.agents: dict[str, MockAgent] = {}
        self.graph: StateGraph | None = None
        self.compiled_graph = None
        self.is_compiled = False

    def add_agent(self, agent: MockAgent) -> bool:
        """Add an agent to the system."""
        logger.info(f"\n📌 Adding agent: {agent.name}")
        logger.info(f"   Current compiled state: {self.is_compiled}")

        # Add to registry
        self.agents[agent.name] = agent

        # If already compiled, we need to rebuild
        if self.is_compiled:
            logger.info("   ⚠️  Graph already compiled - need to rebuild!")
            return self._rebuild_graph()
        logger.info("   ✅ Agent added (graph not yet compiled)")
        return True

    def build_initial_graph(self) -> None:
        """Build the initial graph structure."""
        logger.info("\n🔨 Building initial graph...")

        # Create state graph
        self.graph = StateGraph(dict)

        # Add supervisor node
        async def supervisor(state: dict) -> dict:
            """Route to appropriate agent based on state."""
            messages = state.get("messages", [])
            last_message = messages[-1] if messages else ""

            # Simple routing logic
            if "math" in str(last_message).lower() and "math_agent" in self.agents:
                state["next"] = "math_agent"
            elif (
                "write" in str(last_message).lower() and "writing_agent" in self.agents
            ):
                state["next"] = "writing_agent"
            elif self.agents:
                # Default to first available agent
                state["next"] = next(iter(self.agents.keys()))
            else:
                state["next"] = END

            return state

        self.graph.add_node("supervisor", supervisor)
        self.graph.set_entry_point("supervisor")

        # Add existing agents
        for agent_name, agent in self.agents.items():
            self._add_agent_to_graph(agent_name, agent)

        # Add routing from supervisor
        def route_supervisor(state: dict) -> str:
            return state.get("next", END)

        destinations = [*list(self.agents.keys()), END]
        self.graph.add_conditional_edges(
            "supervisor", route_supervisor, {dest: dest for dest in destinations}
        )

        logger.info(f"   ✅ Initial graph built with {len(self.agents)} agents")

    def _add_agent_to_graph(self, agent_name: str, agent: MockAgent) -> None:
        """Add a single agent node to the graph."""

        async def agent_node(state: dict) -> dict:
            return await agent.process(state)

        self.graph.add_node(agent_name, agent_node)
        # Route back to supervisor after agent
        self.graph.add_edge(agent_name, "supervisor")

    def compile(self) -> None:
        """Compile the graph."""
        logger.info("\n📦 Compiling graph...")

        if not self.graph:
            self.build_initial_graph()

        self.compiled_graph = self.graph.compile()
        self.is_compiled = True

        logger.info(f"   ✅ Graph compiled with agents: {list(self.agents.keys())}")

    def _rebuild_graph(self) -> bool:
        """Rebuild the graph with new agents."""
        logger.info("\n🔄 Rebuilding graph with new agents...")

        try:
            # Create new graph from scratch
            old_compiled = self.compiled_graph

            # Reset and rebuild
            self.graph = None
            self.is_compiled = False

            # Build new graph with all current agents
            self.build_initial_graph()

            # Recompile
            self.compiled_graph = self.graph.compile()
            self.is_compiled = True

            logger.info(
                f"   ✅ Graph rebuilt successfully with {len(self.agents)} agents"
            )
            return True

        except Exception as e:
            logger.exception(f"   ❌ Failed to rebuild graph: {e}")
            # Restore old graph
            self.compiled_graph = old_compiled
            return False

    async def run(self, message: str) -> dict:
        """Run the graph with a message."""
        if not self.compiled_graph:
            raise RuntimeError("Graph not compiled!")

        initial_state = {"messages": [message]}
        result = await self.compiled_graph.ainvoke(initial_state)
        return result


async def test_dynamic_addition():
    """Test the complete flow of dynamic agent addition."""
    # Create manager
    manager = DynamicGraphManager()

    # Step 1: Add initial agent and compile
    writing_agent = MockAgent("writing_agent")
    manager.add_agent(writing_agent)

    manager.compile()

    # Test with initial setup
    result1 = await manager.run("Write me a story")
    assert "writing_agent" in str(result1), "Writing agent should handle this"

    # Step 4: Add new agent AFTER compilation
    math_agent = MockAgent("math_agent")
    manager.add_agent(math_agent)

    # Test with new agent
    result2 = await manager.run("Calculate 2+2")
    assert "math_agent" in str(result2), "Math agent should handle this"

    # Add another agent
    research_agent = MockAgent("research_agent")
    manager.add_agent(research_agent)

    # Final test

    # Test each type
    await manager.run("Write something")
    await manager.run("Do some math")

    return True


if __name__ == "__main__":

    asyncio.run(test_dynamic_addition())
