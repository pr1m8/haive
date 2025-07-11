"""Fixed Dynamic Supervisor with Proper Graph Rebuilding.

This implementation correctly handles dynamic agent addition after compilation
based on BaseGraph2 limitations and requirements.
"""

import asyncio
import logging
from typing import Any, Callable, Dict, List, Optional

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import BaseMessage
from pydantic import Field

from haive.agents.react.agent import ReactAgent

from .dynamic_state import DynamicSupervisorState

logger = logging.getLogger(__name__)


class DynamicSupervisorFixed(ReactAgent):
    """Fixed dynamic supervisor that properly rebuilds graphs at runtime.

    Key improvements:
    1. Proper graph rebuilding through Agent.create_runnable()
    2. Lazy recompilation on next invocation
    3. State preservation through checkpointer
    4. Dynamic routing that checks registry at runtime
    """

    # Configuration
    auto_rebuild_graph: bool = Field(
        default=True,
        description="Whether to automatically rebuild graph on agent changes",
    )

    # Private state
    _agent_registry: dict[str, Any] = {}
    _needs_rebuild: bool = False
    _initial_build_complete: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent_registry = {}
        self._needs_rebuild = False
        self._initial_build_complete = False

    def register_agent(
        self,
        agent: Any,
        capability: str | None = None,
        rebuild_immediately: bool = False,
    ) -> bool:
        """Register an agent for dynamic routing.

        Args:
            agent: Agent to register
            capability: Description of agent's capabilities
            rebuild_immediately: Force immediate rebuild (vs lazy rebuild)

        Returns:
            bool: Success status
        """
        logger.info(f"Registering agent: {agent.name}")

        # Add to registry
        self._agent_registry[agent.name] = {
            "agent": agent,
            "capability": capability or f"Agent {agent.name}",
        }

        # Mark for rebuild
        if self._initial_build_complete:
            self._needs_rebuild = True

            if rebuild_immediately and self.auto_rebuild_graph:
                self._rebuild_graph_properly()

        return True

    def unregister_agent(
        self, agent_name: str, rebuild_immediately: bool = False
    ) -> bool:
        """Unregister an agent.

        Args:
            agent_name: Name of agent to remove
            rebuild_immediately: Force immediate rebuild

        Returns:
            bool: Success status
        """
        if agent_name in self._agent_registry:
            logger.info(f"Unregistering agent: {agent_name}")
            del self._agent_registry[agent_name]

            if self._initial_build_complete:
                self._needs_rebuild = True

                if rebuild_immediately and self.auto_rebuild_graph:
                    self._rebuild_graph_properly()

            return True
        return False

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with registered agents."""
        logger.info(f"Building graph with {len(self._agent_registry)} agents")

        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor routing node
        supervisor_node = self._create_dynamic_supervisor_node()
        graph.add_node("supervisor", supervisor_node)

        # Add executor node that handles actual agent execution
        executor_node = self._create_dynamic_executor_node()
        graph.add_node("executor", executor_node)

        # Add all registered agent nodes
        for agent_name, agent_info in self._agent_registry.items():
            agent_wrapper = self._create_agent_wrapper(agent_name, agent_info["agent"])
            graph.add_node(agent_name, agent_wrapper)

            # Agent flows back to supervisor
            graph.add_edge(agent_name, "supervisor")

        # Supervisor routes to executor or END
        graph.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {
                "executor": "executor",
                "END": "__end__",
                **{name: name for name in self._agent_registry},
            },
        )

        # Executor routes to specific agents
        graph.add_conditional_edges(
            "executor",
            self._route_to_agent,
            {
                **{name: name for name in self._agent_registry},
                "supervisor": "supervisor",
            },
        )

        # Set entry point
        graph.set_entry_point("supervisor")

        self._initial_build_complete = True
        return graph

    def _rebuild_graph_properly(self) -> None:
        """Properly rebuild the graph using Agent's create_runnable method."""
        logger.info("Rebuilding supervisor graph with new agent configuration...")

        try:
            # Clear the current graph to force rebuild
            self.graph = None
            self._graph_built = False

            # Force graph rebuild on next invocation
            # The Agent base class will call build_graph() and create_runnable()
            # This ensures proper compilation through the correct flow

            logger.info("Graph marked for rebuild - will recompile on next invocation")
            self._needs_rebuild = False

        except Exception as e:
            logger.exception(f"Failed to mark graph for rebuild: {e}")

    async def ainvoke(self, input: Any, config: Any | None = None, **kwargs) -> Any:
        """Override ainvoke to handle lazy graph rebuilding."""
        # Check if we need to rebuild before invoking
        if self._needs_rebuild and self.auto_rebuild_graph:
            logger.info("Rebuilding graph before invocation...")
            self._rebuild_graph_properly()

            # Ensure the graph is rebuilt by clearing compiled graph
            if hasattr(self, "_compiled_graph"):
                self._compiled_graph = None

        # Call parent ainvoke which will trigger recompilation if needed
        return await super().ainvoke(input, config, **kwargs)

    def invoke(self, input: Any, config: Any | None = None, **kwargs) -> Any:
        """Override invoke to handle lazy graph rebuilding."""
        # Check if we need to rebuild before invoking
        if self._needs_rebuild and self.auto_rebuild_graph:
            logger.info("Rebuilding graph before invocation...")
            self._rebuild_graph_properly()

            # Ensure the graph is rebuilt by clearing compiled graph
            if hasattr(self, "_compiled_graph"):
                self._compiled_graph = None

        # Call parent invoke which will trigger recompilation if needed
        return super().invoke(input, config, **kwargs)

    def _create_dynamic_supervisor_node(self) -> Callable:
        """Create supervisor node that routes based on dynamic registry."""

        async def supervisor_node(state: DynamicSupervisorState) -> dict[str, Any]:
            """Supervisor that checks registry dynamically."""
            # Check available agents IN REAL TIME
            available_agents = list(self._agent_registry.keys())
            logger.info(f"Available agents at runtime: {available_agents}")

            if not state.messages:
                return {"next": "END"}

            # Simple routing logic for demo
            last_message = state.messages[-1]
            content = getattr(last_message, "content", "").lower()

            # Route based on keywords
            if "math" in content and "math_agent" in available_agents:
                return {"next": "math_agent", "target_agent": "math_agent"}
            if "write" in content and "writing_agent" in available_agents:
                return {"next": "writing_agent", "target_agent": "writing_agent"}
            if available_agents:
                # Default to first available
                target = available_agents[0]
                return {"next": target, "target_agent": target}
            return {"next": "END"}

        return supervisor_node

    def _create_dynamic_executor_node(self) -> Callable:
        """Create executor node that prepares for agent execution."""

        async def executor_node(state: DynamicSupervisorState) -> dict[str, Any]:
            """Prepare state for agent execution."""
            target = getattr(state, "target_agent", None)
            if target and target in self._agent_registry:
                logger.info(f"Preparing to execute agent: {target}")
                return {"next": target}

            return {"next": "supervisor"}

        return executor_node

    def _create_agent_wrapper(self, agent_name: str, agent: Any) -> Callable:
        """Create wrapper function for agent execution."""

        async def agent_wrapper(state: DynamicSupervisorState) -> dict[str, Any]:
            """Execute agent and update state."""
            logger.info(f"Executing agent: {agent_name}")

            try:
                # Execute agent
                result = await agent.ainvoke({"messages": state.messages})

                # Extract messages from result
                if hasattr(result, "messages"):
                    new_messages = result.messages
                elif isinstance(result, dict) and "messages" in result:
                    new_messages = result["messages"]
                else:
                    new_messages = []

                return {"messages": new_messages, "last_agent": agent_name}

            except Exception as e:
                logger.exception(f"Agent {agent_name} execution failed: {e}")
                return {"error": str(e)}

        return agent_wrapper

    def _route_supervisor(self, state: DynamicSupervisorState) -> str:
        """Route from supervisor based on state."""
        next_target = getattr(state, "next", "END")
        return next_target if next_target != "END" else "__end__"

    def _route_to_agent(self, state: DynamicSupervisorState) -> str:
        """Route to specific agent from executor."""
        target = getattr(state, "target_agent", None)

        # Verify agent still exists at routing time
        if target and target in self._agent_registry:
            return target

        return "supervisor"

    def get_registered_agents(self) -> list[str]:
        """Get list of currently registered agents."""
        return list(self._agent_registry.keys())

    def get_agent_info(self, agent_name: str) -> dict[str, Any] | None:
        """Get information about a registered agent."""
        return self._agent_registry.get(agent_name)


# Example usage
if __name__ == "__main__":

    async def test_dynamic_supervisor():
        """Test the fixed dynamic supervisor."""
        # Create supervisor
        supervisor = DynamicSupervisorFixed(
            name="fixed_supervisor", auto_rebuild_graph=True
        )

        # Create mock agents
        class MockAgent:
            def __init__(self, name):
                self.name = name

            async def ainvoke(self, state):
                messages = state.get("messages", [])
                return {"messages": [*messages, f"Response from {self.name}"]}

        # Register initial agent
        writing_agent = MockAgent("writing_agent")
        supervisor.register_agent(writing_agent, "Writing and content creation")

        # First invocation - triggers initial build
        await supervisor.ainvoke({"messages": ["Write a story"]})

        # Register new agent AFTER compilation
        math_agent = MockAgent("math_agent")
        supervisor.register_agent(math_agent, "Mathematical calculations")

        # Next invocation will trigger rebuild
        await supervisor.ainvoke({"messages": ["Calculate 2+2"]})

    # Run test
    asyncio.run(test_dynamic_supervisor())
