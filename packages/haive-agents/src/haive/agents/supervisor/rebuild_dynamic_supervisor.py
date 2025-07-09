"""Dynamic Supervisor with Proper Graph Rebuilding.

This implementation correctly rebuilds the graph when agents are added/removed,
following the Agent base class patterns.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from pydantic import Field, PrivateAttr

from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class RebuildDynamicSupervisor(ReactAgent):
    """Dynamic supervisor that properly rebuilds graphs when agents change.

    Key approach:
    1. Maintain agent registry
    2. When agents are added/removed, clear the graph
    3. Let the Agent base class rebuild on next invocation
    4. Each agent gets its own node in the graph
    """

    # Configuration
    auto_rebuild: bool = Field(
        default=True, description="Auto rebuild on agent changes"
    )

    # Private attributes
    _agent_registry: Dict[str, Any] = PrivateAttr(default_factory=dict)
    _agent_capabilities: Dict[str, str] = PrivateAttr(default_factory=dict)
    _needs_rebuild: bool = PrivateAttr(default=False)

    def register_agent(
        self, agent: Any, capability: str = None, agent_name: str = None
    ) -> bool:
        """Register an agent and mark for rebuild.

        Args:
            agent: Agent instance to register
            capability: Description of agent capabilities
            agent_name: Optional name override

        Returns:
            Success status
        """
        name = agent_name or getattr(agent, "name", agent.__class__.__name__)

        logger.info(f"Registering agent: {name}")

        # Store agent
        self._agent_registry[name] = agent
        self._agent_capabilities[name] = capability or f"Agent {name}"

        # Mark for rebuild
        if self._graph_built:
            logger.info("Marking graph for rebuild due to agent addition")
            self._needs_rebuild = True

            if self.auto_rebuild:
                self._trigger_rebuild()

        logger.info(f"✅ Registered {name} ({len(self._agent_registry)} total agents)")
        return True

    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent and mark for rebuild."""
        if agent_name not in self._agent_registry:
            return False

        logger.info(f"Unregistering agent: {agent_name}")

        del self._agent_registry[agent_name]
        if agent_name in self._agent_capabilities:
            del self._agent_capabilities[agent_name]

        # Mark for rebuild
        if self._graph_built:
            self._needs_rebuild = True

            if self.auto_rebuild:
                self._trigger_rebuild()

        logger.info(
            f"✅ Unregistered {agent_name} ({len(self._agent_registry)} remaining)"
        )
        return True

    def _trigger_rebuild(self):
        """Trigger graph rebuild by clearing current graph.

        This forces the Agent base class to rebuild on next invocation.
        """
        logger.info("Triggering graph rebuild...")

        # Clear the graph - this forces rebuild
        self.graph = None
        self._graph_built = False

        # Clear compiled graph
        if hasattr(self, "_compiled_graph"):
            self._compiled_graph = None

        # Reset rebuild flag
        self._needs_rebuild = False

        logger.info("✅ Graph cleared, will rebuild on next invocation")

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with all registered agents as nodes.

        Graph structure:
        - supervisor: Makes routing decisions
        - agent nodes: One per registered agent
        - Conditional routing from supervisor to agents
        - Agents route back to supervisor
        """
        logger.info(
            f"Building supervisor graph with {len(self._agent_registry)} agents"
        )

        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor node
        supervisor_node = self._create_supervisor_node()
        graph.add_node("supervisor", supervisor_node)
        graph.set_entry_point("supervisor")

        # Add a node for each registered agent
        for agent_name, agent in self._agent_registry.items():
            logger.info(f"Adding node for agent: {agent_name}")

            # Create agent execution node
            agent_node = self._create_agent_node(agent_name, agent)
            graph.add_node(agent_name, agent_node)

            # Agent routes back to supervisor
            graph.add_edge(agent_name, "supervisor")

        # Build routing destinations
        destinations = {
            agent_name: agent_name for agent_name in self._agent_registry.keys()
        }
        destinations["END"] = "__end__"

        # Supervisor routes conditionally
        graph.add_conditional_edges(
            "supervisor", self._route_from_supervisor, destinations
        )

        logger.info(
            f"✅ Graph built with nodes: supervisor + {list(self._agent_registry.keys())}"
        )
        return graph

    def _create_supervisor_node(self):
        """Create supervisor decision node."""

        async def supervisor_node(state: Any) -> Dict[str, Any]:
            """Make routing decision based on current state."""

            logger.info("=" * 60)
            logger.info("SUPERVISOR DECISION NODE")
            logger.info("=" * 60)

            # Extract state
            if hasattr(state, "model_dump"):
                state_dict = state.model_dump()
                if hasattr(state, "messages"):
                    state_dict["messages"] = list(getattr(state, "messages", []))
            else:
                state_dict = state if isinstance(state, dict) else {}

            # Check completion
            if state_dict.get("complete"):
                logger.info("Conversation marked complete")
                return {"next_agent": "END", "complete": True}

            # Get messages
            messages = state_dict.get("messages", [])
            if not messages:
                logger.info("No messages, ending")
                return {"next_agent": "END", "complete": True}

            # Analyze last message
            last_message = messages[-1]

            # Avoid infinite loops - if last was AI and no new human input
            if isinstance(last_message, AIMessage):
                # Find last human message
                human_msgs = [m for m in messages if isinstance(m, HumanMessage)]
                if human_msgs:
                    last_human_idx = messages.index(human_msgs[-1])
                    if last_human_idx < len(messages) - 1:
                        # AI already responded after last human message
                        logger.info("AI already responded, ending")
                        return {"next_agent": "END", "complete": True}

            # Select agent based on content
            content = getattr(last_message, "content", str(last_message))
            selected_agent = self._select_best_agent(content)

            if selected_agent:
                logger.info(f"Selected agent: {selected_agent}")
                return {"next_agent": selected_agent, "complete": False}
            else:
                logger.info("No suitable agent found")
                return {"next_agent": "END", "complete": True}

        return supervisor_node

    def _create_agent_node(self, agent_name: str, agent: Any):
        """Create node for a specific agent with proper state handling."""

        async def agent_node(state: Any) -> Dict[str, Any]:
            """Execute agent with proper state extraction."""

            logger.info(f"=" * 60)
            logger.info(f"AGENT NODE: {agent_name}")
            logger.info(f"=" * 60)

            # Extract state following AgentNode pattern
            if hasattr(state, "model_dump"):
                state_dict = state.model_dump()
                # Preserve BaseMessage objects
                if hasattr(state, "messages"):
                    messages = getattr(state, "messages", [])
                    if hasattr(messages, "root"):
                        state_dict["messages"] = messages.root
                    else:
                        state_dict["messages"] = list(messages)
            else:
                state_dict = state if isinstance(state, dict) else {}

            try:
                # Prepare agent input based on agent's schema
                agent_input = self._prepare_agent_input(agent, state_dict)

                # Execute agent
                logger.info(f"Executing {agent_name}...")

                if hasattr(agent, "ainvoke"):
                    result = await agent.ainvoke(agent_input)
                elif hasattr(agent, "invoke"):
                    result = agent.invoke(agent_input)
                else:
                    result = await agent(agent_input)

                # Process result
                update = self._process_agent_result(result, state_dict, agent_name)

                logger.info(f"✅ {agent_name} execution complete")
                return update

            except Exception as e:
                logger.error(f"Error in {agent_name}: {e}")
                return {"error": str(e), "last_agent": agent_name, "complete": True}

        return agent_node

    def _prepare_agent_input(self, agent: Any, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for agent based on its state schema."""

        # If agent has state_schema, extract only needed fields
        if hasattr(agent, "state_schema") and agent.state_schema:
            logger.info(f"Using agent state schema: {agent.state_schema.__name__}")

            agent_input = {}
            for field_name in agent.state_schema.model_fields:
                if field_name in state:
                    agent_input[field_name] = state[field_name]

            # Ensure engines if needed
            if "engines" in agent.state_schema.model_fields:
                if "engines" not in agent_input and "engines" in state:
                    agent_input["engines"] = state["engines"]
                elif hasattr(agent, "engines"):
                    agent_input["engines"] = agent.engines

            return agent_input

        # Default: common fields
        agent_input = {}

        # Always include messages
        if "messages" in state:
            agent_input["messages"] = state["messages"]

        # Include other common fields
        for field in ["query", "context", "tools", "engines"]:
            if field in state:
                agent_input[field] = state[field]

        return agent_input

    def _process_agent_result(
        self, result: Any, state: Dict[str, Any], agent_name: str
    ) -> Dict[str, Any]:
        """Process agent result into state update."""

        update = {"last_agent": agent_name, "last_agent_success": True}

        # Handle different result types
        if isinstance(result, dict):
            update.update(result)
        elif hasattr(result, "messages"):
            update["messages"] = result.messages
        elif isinstance(result, BaseMessage):
            current_messages = state.get("messages", [])
            update["messages"] = current_messages + [result]
        elif isinstance(result, str):
            from langchain_core.messages import AIMessage

            current_messages = state.get("messages", [])
            update["messages"] = current_messages + [AIMessage(content=result)]

        return update

    def _select_best_agent(self, content: str) -> Optional[str]:
        """Select best agent for the given content."""

        if not self._agent_registry:
            return None

        content_lower = content.lower()

        # Check capabilities
        for agent_name, capability in self._agent_capabilities.items():
            if any(word in content_lower for word in capability.lower().split()):
                return agent_name

        # Check agent names
        for agent_name in self._agent_registry:
            if agent_name.lower() in content_lower:
                return agent_name

        # Default to first agent
        return list(self._agent_registry.keys())[0]

    def _route_from_supervisor(self, state: Any) -> str:
        """Routing function from supervisor."""

        if hasattr(state, "model_dump"):
            state_dict = state.model_dump()
        else:
            state_dict = state if isinstance(state, dict) else {}

        next_agent = state_dict.get("next_agent", "END")

        # Validate agent exists
        if next_agent != "END" and next_agent not in self._agent_registry:
            logger.warning(f"Agent {next_agent} not found, routing to END")
            return "END"

        return next_agent

    async def ainvoke(self, input: Any, config: Optional[Any] = None, **kwargs) -> Any:
        """Override to check for rebuild before invocation."""

        if self._needs_rebuild and self.auto_rebuild:
            logger.info("Rebuilding graph before invocation...")
            self._trigger_rebuild()

        return await super().ainvoke(input, config, **kwargs)

    def invoke(self, input: Any, config: Optional[Any] = None, **kwargs) -> Any:
        """Override to check for rebuild before invocation."""

        if self._needs_rebuild and self.auto_rebuild:
            logger.info("Rebuilding graph before invocation...")
            self._trigger_rebuild()

        return super().invoke(input, config, **kwargs)


# Test it
if __name__ == "__main__":
    import asyncio

    class TestAgent:
        def __init__(self, name: str):
            self.name = name

        async def ainvoke(self, state: Dict[str, Any]) -> Dict[str, Any]:
            messages = state.get("messages", [])
            response = AIMessage(content=f"{self.name}: Processed your request")
            return {"messages": messages + [response]}

    async def test_rebuild_supervisor():
        # Create supervisor
        supervisor = RebuildDynamicSupervisor(name="rebuild_supervisor")

        # Add initial agents
        supervisor.register_agent(TestAgent("research_agent"), "research")
        supervisor.register_agent(TestAgent("writing_agent"), "writing")

        # First invocation - builds graph
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Research something")]}
        )
        print("Result 1:", result1)

        # Add new agent - triggers rebuild on next invoke
        supervisor.register_agent(TestAgent("math_agent"), "calculations")

        # Second invocation - rebuilds graph automatically
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Calculate something")]}
        )
        print("Result 2:", result2)

        print(f"\nRegistered agents: {list(supervisor._agent_registry.keys())}")

    asyncio.run(test_rebuild_supervisor())
