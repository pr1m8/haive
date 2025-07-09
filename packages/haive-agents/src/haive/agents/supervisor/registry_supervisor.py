"""Registry-Based Dynamic Supervisor using DynamicChoiceModel.

The supervisor gets agents from an agent registry instead of creating them.
Uses DynamicChoiceModel for selection and all agents are ReactAgents.
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Union

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import BaseTool
from pydantic import Field, PrivateAttr

from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class AgentRegistry:
    """Registry of available agents that can be added to supervisor."""

    def __init__(self):
        self.available_agents: Dict[str, ReactAgent] = {}
        self.agent_capabilities: Dict[str, str] = {}

    def register_agent(self, agent: ReactAgent, capability: str = None):
        """Register an agent as available."""
        self.available_agents[agent.name] = agent
        self.agent_capabilities[agent.name] = (
            capability or f"General tasks for {agent.name}"
        )
        logger.info(f"Registered {agent.name} in registry")

    def get_agent(self, agent_name: str) -> Optional[ReactAgent]:
        """Get an agent from registry."""
        return self.available_agents.get(agent_name)

    def get_available_agents(self) -> Dict[str, str]:
        """Get available agents with capabilities."""
        return {
            name: self.agent_capabilities.get(name, "General tasks")
            for name in self.available_agents.keys()
        }

    def search_agents_by_capability(self, task_description: str) -> List[str]:
        """Search for agents that might handle the task."""
        task_lower = task_description.lower()
        matches = []

        for agent_name, capability in self.agent_capabilities.items():
            capability_lower = capability.lower()

            # Simple keyword matching
            if any(word in capability_lower for word in task_lower.split()):
                matches.append(agent_name)

        return matches


class AgentRetrievalTool(BaseTool):
    """Tool to retrieve agents from registry based on task needs."""

    name: str = "get_agent_from_registry"
    description: str = """Get a suitable agent from the agent registry for the current task.
    Use this when no currently active agent can handle the request."""

    def __init__(self, registry: AgentRegistry, supervisor, **kwargs):
        super().__init__(**kwargs)
        self.registry = registry
        self.supervisor = supervisor

    def _run(self, task_description: str, agent_type_needed: str = "") -> str:
        """Retrieve agent from registry."""

        logger.info(f"Looking for agent for task: {task_description}")

        # Get agents that might match
        potential_agents = self.registry.search_agents_by_capability(task_description)

        if not potential_agents:
            # Check if we have any available agents
            available = list(self.registry.get_available_agents().keys())
            if available:
                # Take first available as fallback
                agent_name = available[0]
                logger.info(f"No specific match, using fallback: {agent_name}")
            else:
                return "NO_AGENTS_AVAILABLE"
        else:
            # Use best match
            agent_name = potential_agents[0]
            logger.info(f"Found matching agent: {agent_name}")

        # Get the agent from registry
        agent = self.registry.get_agent(agent_name)
        if not agent:
            return f"Agent {agent_name} not found in registry"

        # Add to supervisor's active agents
        self.supervisor._add_agent_to_active(agent)

        return f"Retrieved and activated {agent_name} from registry"


class AgentSelectionTool(BaseTool):
    """Tool that uses DynamicChoiceModel to select from active agents."""

    name: str = "select_active_agent"
    description: str = (
        """Select the best active agent for the current task using the choice model."""
    )

    def __init__(self, choice_model: DynamicChoiceModel, **kwargs):
        super().__init__(**kwargs)
        self.choice_model = choice_model

    def _run(self, task_description: str) -> str:
        """Select from currently active agents."""

        available_options = self.choice_model.option_names

        if not available_options or available_options == ["END"]:
            return "NO_ACTIVE_AGENTS"

        # Simple selection based on task
        task_lower = task_description.lower()

        # Check each option
        for option in available_options:
            if option == "END":
                continue

            option_lower = option.lower()

            # Match agent type to task
            if "research" in option_lower and any(
                word in task_lower for word in ["research", "find", "search"]
            ):
                return option
            elif "code" in option_lower and any(
                word in task_lower for word in ["code", "program", "implement"]
            ):
                return option
            elif "write" in option_lower and any(
                word in task_lower for word in ["write", "create", "draft"]
            ):
                return option
            elif "math" in option_lower and any(
                word in task_lower for word in ["calculate", "math", "solve"]
            ):
                return option
            elif "analy" in option_lower and any(
                word in task_lower for word in ["analyze", "examine", "study"]
            ):
                return option

        # Return first available if no specific match
        non_end_options = [opt for opt in available_options if opt != "END"]
        return non_end_options[0] if non_end_options else "END"


class RegistrySupervisor(ReactAgent):
    """Supervisor that gets agents from a registry using DynamicChoiceModel.

    This supervisor:
    1. Maintains a registry of available agents
    2. Uses DynamicChoiceModel to track active agents
    3. Uses tools to select from active agents or get new ones from registry
    4. All execution agents are ReactAgents
    """

    # Configuration
    max_active_agents: int = Field(default=6, description="Max active agents")

    # Private attributes
    _registry: AgentRegistry = PrivateAttr(default_factory=AgentRegistry)
    _active_agents: Dict[str, ReactAgent] = PrivateAttr(default_factory=dict)
    _choice_model: Optional[DynamicChoiceModel] = PrivateAttr(default=None)

    def setup_agent(self) -> None:
        """Set up supervisor with registry and choice model."""

        # Initialize
        self._registry = AgentRegistry()
        self._active_agents = {}

        # Create choice model
        self._choice_model = DynamicChoiceModel(
            option_names=["END"], option_descriptions=["End the conversation"]
        )

        # Create tools
        self.tools = [
            AgentSelectionTool(self._choice_model),
            AgentRetrievalTool(self._registry, self),
        ]

        # Call parent setup
        super().setup_agent()

        logger.info("✅ Registry supervisor initialized")

    def populate_registry(
        self, agents: List[ReactAgent], capabilities: List[str] = None
    ):
        """Populate the agent registry with available agents."""

        if capabilities and len(capabilities) != len(agents):
            capabilities = None

        for i, agent in enumerate(agents):
            capability = (
                capabilities[i] if capabilities else f"General tasks for {agent.name}"
            )
            self._registry.register_agent(agent, capability)

        logger.info(f"✅ Populated registry with {len(agents)} agents")

    def _add_agent_to_active(self, agent: ReactAgent):
        """Add agent to active roster and update choice model."""

        if len(self._active_agents) >= self.max_active_agents:
            logger.warning("Max active agents reached, cannot add more")
            return False

        self._active_agents[agent.name] = agent
        self._update_choice_model()

        logger.info(f"✅ Added {agent.name} to active agents")
        return True

    def _update_choice_model(self):
        """Update choice model with current active agents."""

        agent_names = list(self._active_agents.keys()) + ["END"]
        descriptions = []

        for name in agent_names:
            if name == "END":
                descriptions.append("End the conversation")
            else:
                capability = self._registry.agent_capabilities.get(
                    name, f"Tasks for {name}"
                )
                descriptions.append(f"Route to {name}: {capability}")

        self._choice_model.option_names = agent_names
        self._choice_model.option_descriptions = descriptions

        logger.info(f"Updated choice model with {len(agent_names)} options")

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with registry integration."""

        logger.info("Building registry supervisor graph")

        graph = BaseGraph(name=f"{self.name}Graph")

        # Add supervisor node
        supervisor_node = self._create_supervisor_node()
        graph.add_node("supervisor", supervisor_node)

        # Add executor node
        executor_node = self._create_executor_node()
        graph.add_node("executor", executor_node)

        # Set entry point
        graph.set_entry_point("supervisor")

        # Routing
        graph.add_conditional_edges(
            "supervisor",
            self._route_from_supervisor,
            {"executor": "executor", "END": "__end__"},
        )

        # Executor loops back
        graph.add_edge("executor", "supervisor")

        logger.info("✅ Built registry supervisor graph")
        return graph

    def _create_supervisor_node(self):
        """Create supervisor node that uses tools for agent management."""

        async def supervisor_node(state: Any) -> Dict[str, Any]:
            """Supervisor uses tools to manage agents."""

            logger.info("=" * 60)
            logger.info("REGISTRY SUPERVISOR")
            logger.info("=" * 60)

            # Extract state
            state_dict = self._extract_state_dict(state)

            # Check completion
            if state_dict.get("is_complete"):
                return {"is_complete": True}

            # Get messages
            messages = state_dict.get("messages", [])
            if not messages:
                return {"is_complete": True}

            # Get last message
            last_message = messages[-1]

            # Avoid loops
            if isinstance(last_message, AIMessage) and state_dict.get("last_agent"):
                human_messages = [m for m in messages if isinstance(m, HumanMessage)]
                if human_messages:
                    last_human_idx = messages.index(human_messages[-1])
                    if last_human_idx < len(messages) - 1:
                        return {"is_complete": True}

            # Analyze request
            content = getattr(last_message, "content", "")

            # Use this supervisor's ReactAgent capabilities to make decisions
            supervisor_input = {
                "messages": [
                    HumanMessage(
                        content=f"""Analyze this request and either:
1. Select an active agent using select_active_agent tool, OR
2. Get a new agent from registry using get_agent_from_registry tool

Request: {content}

Available active agents: {list(self._active_agents.keys())}
Available in registry: {list(self._registry.get_available_agents().keys())}"""
                    )
                ]
            }

            try:
                # Use supervisor's own ReactAgent capabilities
                decision_result = await super().ainvoke(supervisor_input)

                # Parse the decision
                selected_agent = self._parse_decision_result(decision_result)

                if selected_agent and selected_agent != "END":
                    logger.info(f"Selected agent: {selected_agent}")
                    return {
                        "target_agent": selected_agent,
                        "original_request": content,
                        "is_complete": False,
                    }
                else:
                    return {"is_complete": True}

            except Exception as e:
                logger.error(f"Error in supervisor decision: {e}")
                return {"is_complete": True}

        return supervisor_node

    def _create_executor_node(self):
        """Create executor that runs selected ReactAgent."""

        async def executor_node(state: Any) -> Dict[str, Any]:
            """Execute the selected ReactAgent."""

            logger.info("=" * 60)
            logger.info("AGENT EXECUTOR")
            logger.info("=" * 60)

            state_dict = self._extract_state_dict(state)

            target_agent = state_dict.get("target_agent")
            if not target_agent:
                return {"error": "No target agent"}

            logger.info(f"Executing ReactAgent: {target_agent}")

            # Get agent from active agents
            agent = self._active_agents.get(target_agent)
            if not agent:
                logger.error(f"Agent {target_agent} not in active agents")
                return {"error": f"Agent {target_agent} not active"}

            try:
                # Prepare input
                messages = state_dict.get("messages", [])
                agent_input = {"messages": messages}

                # Execute ReactAgent
                result = await agent.ainvoke(agent_input)

                # Return result
                result_messages = result.get("messages", messages)

                return {
                    "messages": result_messages,
                    "last_agent": target_agent,
                    "execution_complete": True,
                }

            except Exception as e:
                logger.error(f"Error executing {target_agent}: {e}")
                return {"error": str(e)}

        return executor_node

    def _parse_decision_result(self, result: Dict[str, Any]) -> Optional[str]:
        """Parse the supervisor's decision result."""

        messages = result.get("messages", [])

        # Look for tool results
        for msg in messages:
            if isinstance(msg, ToolMessage):
                if "select_active_agent" in getattr(msg, "name", ""):
                    agent_name = msg.content
                    if (
                        agent_name != "NO_ACTIVE_AGENTS"
                        and agent_name in self._active_agents
                    ):
                        return agent_name
                elif "get_agent_from_registry" in getattr(msg, "name", ""):
                    # Agent was retrieved, should be in active now
                    # Look for the agent name in the message
                    content = msg.content
                    if "Retrieved and activated" in content:
                        for agent_name in self._active_agents:
                            if agent_name in content:
                                return agent_name

        # Check if we have any active agents as fallback
        if self._active_agents:
            return list(self._active_agents.keys())[0]

        return None

    def _extract_state_dict(self, state: Any) -> Dict[str, Any]:
        """Extract state dict preserving messages."""
        if isinstance(state, dict):
            return state

        state_dict = state.model_dump() if hasattr(state, "model_dump") else {}

        if hasattr(state, "messages"):
            messages = getattr(state, "messages", [])
            if hasattr(messages, "root"):
                state_dict["messages"] = messages.root
            else:
                state_dict["messages"] = list(messages)

        return state_dict

    def _route_from_supervisor(self, state: Any) -> str:
        """Route from supervisor."""
        state_dict = self._extract_state_dict(state)

        if state_dict.get("is_complete"):
            return "END"

        if state_dict.get("target_agent"):
            return "executor"

        return "END"

    # Public interface
    def get_active_agents(self) -> List[str]:
        """Get currently active agents."""
        return list(self._active_agents.keys())

    def get_registry_agents(self) -> Dict[str, str]:
        """Get available agents in registry."""
        return self._registry.get_available_agents()

    def get_choice_model_status(self) -> Dict[str, Any]:
        """Get choice model status."""
        return {
            "options": self._choice_model.option_names if self._choice_model else [],
            "active_agents": len(self._active_agents),
            "registry_agents": len(self._registry.available_agents),
        }


# Example usage
if __name__ == "__main__":
    import asyncio

    async def test_registry_supervisor():
        """Test the registry supervisor."""

        print("\n" + "=" * 80)
        print("🧪 TESTING REGISTRY SUPERVISOR")
        print("=" * 80 + "\n")

        # Create some ReactAgents for the registry
        from haive.core.engine.aug_llm import AugLLMConfig

        # Research agent
        research_engine = AugLLMConfig(
            name="research_engine",
            system_message="You are a research specialist. Find and analyze information.",
            temperature=0.3,
        )
        research_agent = ReactAgent(
            name="research_agent", engine=research_engine, tools=[]
        )

        # Coding agent
        coding_engine = AugLLMConfig(
            name="coding_engine",
            system_message="You are a software developer. Write clean, efficient code.",
            temperature=0.4,
        )
        coding_agent = ReactAgent(name="coding_agent", engine=coding_engine, tools=[])

        # Create supervisor
        supervisor = RegistrySupervisor(name="registry_supervisor")

        # Populate registry
        supervisor.populate_registry(
            agents=[research_agent, coding_agent],
            capabilities=[
                "research, information gathering, analysis",
                "coding, programming, software development",
            ],
        )

        print(f"Registry agents: {supervisor.get_registry_agents()}")
        print(f"Active agents: {supervisor.get_active_agents()}")

        # Test 1: Research request
        print("\n[Test 1] Research request")
        result1 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Research machine learning trends")]}
        )

        print(f"Active agents after test 1: {supervisor.get_active_agents()}")

        # Test 2: Coding request
        print("\n[Test 2] Coding request")
        result2 = await supervisor.ainvoke(
            {"messages": [HumanMessage(content="Write Python code for sorting")]}
        )

        print(f"Active agents after test 2: {supervisor.get_active_agents()}")
        print(f"Choice model: {supervisor.get_choice_model_status()}")

        print("\n✅ Registry supervisor test complete!")

    asyncio.run(test_registry_supervisor())
