"""Proper Dynamic Supervisor using correct state extraction patterns.

This implementation follows the EngineNode/AgentNode patterns for proper
state handling and dynamic agent execution without graph rebuilding.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import Field

from haive.agents.react.agent import ReactAgent

from .dynamic_executor_node import create_dynamic_executor_node
from .dynamic_state import DynamicSupervisorState

logger = logging.getLogger(__name__)


class ProperDynamicSupervisor(ReactAgent):
    """Dynamic supervisor that executes agents without graph rebuilding.

    Key design:
    1. Fixed graph structure: supervisor -> executor -> supervisor
    2. Dynamic agent execution in executor node
    3. Proper state extraction following EngineNode patterns
    4. No graph rebuilding needed - agents are executed dynamically
    """

    # Agent registry - stores actual agent instances
    _agent_registry: Dict[str, Any] = Field(default_factory=dict, exclude=True)

    # Capability descriptions for routing decisions
    _agent_capabilities: Dict[str, str] = Field(default_factory=dict, exclude=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._agent_registry = {}
        self._agent_capabilities = {}

    def register_agent(
        self, agent: Any, capability: str = None, agent_name: str = None
    ) -> bool:
        """Register an agent for dynamic execution.

        Args:
            agent: The agent instance to register
            capability: Description of agent's capabilities
            agent_name: Optional name override (uses agent.name by default)

        Returns:
            bool: Success status
        """
        name = agent_name or getattr(agent, "name", agent.__class__.__name__)

        logger.info(f"Registering agent: {name}")

        # Store agent instance
        self._agent_registry[name] = agent

        # Store capability description
        self._agent_capabilities[name] = capability or f"Agent {name}"

        logger.info(f"✅ Registered agent '{name}' with capability: '{capability}'")
        logger.info(f"   Total registered agents: {len(self._agent_registry)}")

        return True

    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent.

        Args:
            agent_name: Name of agent to remove

        Returns:
            bool: Success status
        """
        if agent_name in self._agent_registry:
            del self._agent_registry[agent_name]
            del self._agent_capabilities[agent_name]
            logger.info(f"✅ Unregistered agent: {agent_name}")
            return True
        return False

    def build_graph(self) -> BaseGraph:
        """Build the fixed supervisor graph structure.

        The graph structure is:
        1. supervisor: Decides which agent to execute
        2. executor: Dynamically executes the chosen agent
        3. Loop back to supervisor or END

        No rebuilding needed when agents are added/removed!
        """
        logger.info("Building dynamic supervisor graph")

        graph = BaseGraph(name=f"{self.name}Graph")

        # Create supervisor decision node
        supervisor_node = self._create_supervisor_node()
        graph.add_node("supervisor", supervisor_node)

        # Create dynamic executor node
        executor_node = create_dynamic_executor_node(self._agent_registry)
        graph.add_node("executor", executor_node)

        # Fixed edges
        graph.set_entry_point("supervisor")

        # Supervisor conditionally routes
        graph.add_conditional_edges(
            "supervisor",
            self._route_supervisor,
            {"executor": "executor", "END": "__end__"},
        )

        # Executor always returns to supervisor
        graph.add_edge("executor", "supervisor")

        logger.info("✅ Graph built with fixed structure")
        return graph

    def _create_supervisor_node(self):
        """Create the supervisor decision node."""

        async def supervisor_node(state: Union[Dict[str, Any], Any]) -> Dict[str, Any]:
            """Supervisor decides which agent to execute next."""

            logger.info("=" * 60)
            logger.info("SUPERVISOR NODE")
            logger.info("=" * 60)

            # Get available agents
            available_agents = list(self._agent_registry.keys())
            logger.info(f"Available agents: {available_agents}")

            if not available_agents:
                logger.info("No agents available, ending conversation")
                return {"complete": True}

            # Convert state to dict if needed
            if hasattr(state, "model_dump"):
                state_dict = state.model_dump()
                # Preserve messages
                if hasattr(state, "messages"):
                    state_dict["messages"] = getattr(state, "messages")
            else:
                state_dict = state if isinstance(state, dict) else {"value": state}

            # Check if we should end
            if state_dict.get("complete") or state_dict.get("agent_execution_failed"):
                logger.info("Conversation complete or execution failed")
                return {"complete": True}

            # Get messages
            messages = state_dict.get("messages", [])

            if not messages:
                logger.info("No messages, ending")
                return {"complete": True}

            # Get last message for routing decision
            last_message = messages[-1]

            # Skip if last message was from an agent (avoid loops)
            if isinstance(last_message, AIMessage) and state_dict.get("last_agent"):
                # Check if user provided new input
                user_messages = [m for m in messages if isinstance(m, HumanMessage)]
                if user_messages:
                    last_user_msg_idx = messages.index(user_messages[-1])
                    if last_user_msg_idx == len(messages) - 1:
                        # Last message is from user, continue
                        pass
                    else:
                        # Last message is from agent, check if we should continue
                        logger.info("Last message was from agent, ending")
                        return {"complete": True}

            # Route based on content
            content = getattr(last_message, "content", str(last_message))
            target_agent = self._select_agent(content, available_agents)

            if target_agent:
                logger.info(f"Selected agent: {target_agent}")
                return {"target_agent": target_agent, "complete": False}
            else:
                logger.info("No suitable agent found")
                return {"complete": True}

        return supervisor_node

    def _select_agent(self, content: str, available_agents: List[str]) -> Optional[str]:
        """Select the best agent for the given content.

        This is a simple implementation - can be enhanced with:
        - LLM-based routing
        - Capability matching
        - Performance metrics
        - Load balancing
        """
        content_lower = content.lower()

        # Simple keyword-based routing for demo
        routing_rules = {
            "research": ["research", "find", "search", "investigate"],
            "writing": ["write", "draft", "compose", "create"],
            "math": ["calculate", "compute", "solve", "equation"],
            "analysis": ["analyze", "examine", "evaluate", "assess"],
            "code": ["code", "program", "implement", "debug"],
            "translate": ["translate", "convert", "localize"],
            "summarize": ["summarize", "summary", "condense", "brief"],
        }

        # Check each agent's name against routing rules
        for agent_name in available_agents:
            agent_lower = agent_name.lower()

            # Direct name match
            for category, keywords in routing_rules.items():
                if category in agent_lower:
                    if any(keyword in content_lower for keyword in keywords):
                        return agent_name

            # Check capability description
            capability = self._agent_capabilities.get(agent_name, "").lower()
            if any(word in content_lower for word in capability.split()):
                return agent_name

        # Default to first available agent
        return available_agents[0] if available_agents else None

    def _route_supervisor(self, state: Union[Dict[str, Any], Any]) -> str:
        """Route from supervisor node."""

        # Convert state if needed
        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        else:
            state_dict = state if isinstance(state, dict) else {}

        if state_dict.get("complete"):
            return "END"

        if state_dict.get("target_agent"):
            return "executor"

        return "END"

    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return list(self._agent_registry.keys())

    def get_agent_capabilities(self) -> Dict[str, str]:
        """Get agent capabilities descriptions."""
        return self._agent_capabilities.copy()


# Example usage
if __name__ == "__main__":
    import asyncio

    class MockAgent:
        """Simple mock agent for testing."""

        def __init__(self, name: str, response_prefix: str = None):
            self.name = name
            self.response_prefix = response_prefix or f"{name} response"

        async def ainvoke(self, state: Dict[str, Any], config=None) -> Dict[str, Any]:
            messages = state.get("messages", [])
            response = AIMessage(
                content=f"{self.response_prefix}: Processed your request"
            )
            return {"messages": messages + [response]}

    async def test_proper_dynamic_supervisor():
        """Test the proper dynamic supervisor."""

        # Create supervisor
        supervisor = ProperDynamicSupervisor(name="proper_supervisor")

        # Register some agents
        supervisor.register_agent(
            MockAgent("research_agent", "🔍 Research"),
            "Research and information gathering",
        )

        supervisor.register_agent(
            MockAgent("writing_agent", "✍️ Writing"), "Content creation and writing"
        )

        # Test execution
        result = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Research AI trends")]}
        )

        print(f"Result: {result}")

        # Add more agents dynamically (no graph rebuild!)
        supervisor.register_agent(
            MockAgent("math_agent", "🧮 Math"), "Mathematical calculations"
        )

        # Test with new agent
        result = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Calculate 15 + 27")]}
        )

        print(f"Result after adding agent: {result}")

    asyncio.run(test_proper_dynamic_supervisor())
