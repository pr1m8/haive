# experiments/dynamic_supervisor.py

"""Dynamic Supervisor Agent Experiment.

This module contains experimental implementation of a dynamic supervisor
that can select and execute agents based on runtime decisions.
"""

import logging
from typing import Any, Dict, List, Optional, Set, Type

from haive.core.schema.prebuilt.messages_state import MessagesState
from pydantic import BaseModel, Field, computed_field

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


# ============================================================================
# STATE SCHEMA
# ============================================================================


class SupervisorState(MessagesState):
    """State schema for dynamic supervisor agent."""

    # Agent registry information
    agent_registry: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Registry of available agents with their metadata",
    )

    # Current execution state
    current_agent_name: str | None = Field(
        default=None, description="Name of the currently selected agent"
    )

    current_task: str | None = Field(
        default=None, description="Current task being executed"
    )

    # Execution tracking
    execution_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of agent executions with results"
    )

    completed_agents: set[str] = Field(
        default_factory=set, description="Set of agents that have completed their tasks"
    )

    # Task status
    task_complete: bool = Field(
        default=False, description="Whether the overall task is complete"
    )

    max_iterations: int = Field(
        default=10, description="Maximum number of agent iterations"
    )

    current_iteration: int = Field(default=0, description="Current iteration count")

    @computed_field
    @property
    def available_agents(self) -> list[str]:
        """Get list of available agent names from registry."""
        return list(self.agent_registry.keys())

    @computed_field
    @property
    def is_at_max_iterations(self) -> bool:
        """Check if we've reached the maximum iteration limit."""
        return self.current_iteration >= self.max_iterations


# ============================================================================
# AGENT REGISTRY
# ============================================================================


class AgentRegistryEntry(BaseModel):
    """Registry entry for an agent."""

    name: str = Field(description="Unique name for the agent")
    description: str = Field(description="What this agent does")
    agent_class: type[Agent] = Field(description="Agent class to instantiate")
    config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for agent instantiation"
    )
    capabilities: list[str] = Field(
        default_factory=list, description="List of capabilities this agent has"
    )

    model_config = {"arbitrary_types_allowed": True}


class AgentRegistry:
    """Registry for managing available agents."""

    def __init__(self):
        self._registry: dict[str, AgentRegistryEntry] = {}
        self._instances: dict[str, Agent] = {}  # Cache

    def register(
        self,
        name: str,
        description: str,
        agent_class: type[Agent],
        config: Dict[str, Any] | None = None,
        capabilities: list[str] | None = None,
    ) -> None:
        """Register an agent with the registry."""
        entry = AgentRegistryEntry(
            name=name,
            description=description,
            agent_class=agent_class,
            config=config or {},
            capabilities=capabilities or [],
        )
        self._registry[name] = entry
        logger.info(f"Registered agent: {name}")

    def unregister(self, name: str) -> None:
        """Remove an agent from the registry."""
        if name in self._registry:
            del self._registry[name]
            if name in self._instances:
                del self._instances[name]
            logger.info(f"Unregistered agent: {name}")

    def list_agents(self) -> dict[str, dict[str, Any]]:
        """List all registered agents with their metadata."""
        return {
            name: {
                "description": entry.description,
                "capabilities": entry.capabilities,
            }
            for name, entry in self._registry.items()
        }

    def instantiate_agent(self, name: str) -> Agent | None:
        """Instantiate an agent from the registry."""
        entry = self._registry.get(name)
        if not entry:
            logger.error(f"Agent '{name}' not found in registry")
            return None

        # Check cache first
        if name in self._instances:
            return self._instances[name]

        try:
            agent = entry.agent_class(**entry.config)
            self._instances[name] = agent
            return agent
        except Exception as e:
            logger.exception(f"Failed to instantiate agent '{name}': {e}")
            return None

    def to_state_format(self) -> dict[str, dict[str, Any]]:
        """Convert registry to format suitable for SupervisorState."""
        return {
            name: {
                "description": entry.description,
                "capabilities": entry.capabilities,
                "class_name": entry.agent_class.__name__,
            }
            for name, entry in self._registry.items()
        }


# ============================================================================
# DYNAMIC TOOLS FOR AGENT EXECUTION
# ============================================================================

from typing import Annotated

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.prebuilt import InjectedState


def create_dynamic_handoff_tool(supervisor_instance, agent_name: str):
    """Create a handoff tool for a specific agent."""

    @tool
    def handoff_to_agent(task: str, state: Annotated[dict, InjectedState]) -> str:
        """Transfer control to the specified agent.

        Args:
            task: The specific task for the agent to handle

        Returns:
            Result from the agent execution
        """
        try:
            # Get agent from registry
            agent = supervisor_instance.agent_registry.instantiate_agent(agent_name)
            if not agent:
                return f"Error: Agent '{agent_name}' not found in registry"

            # Update supervisor state
            if hasattr(state, "current_agent_name"):
                state["current_agent_name"] = agent_name
                state["current_task"] = task

            # Create input for the agent
            agent_input = {
                "messages": [*state.get("messages", []), HumanMessage(content=task)]
            }

            # Execute the agent
            result = agent.invoke(agent_input)

            # Extract the response
            if hasattr(result, "messages") and result.messages:
                last_message = result.messages[-1]
                if hasattr(last_message, "content"):
                    response = last_message.content
                else:
                    response = str(last_message)
            else:
                response = str(result)

            # Update execution history
            if hasattr(state, "execution_history"):
                state["execution_history"] = [*state.get("execution_history", []), {"agent_name": agent_name, "task": task, "result": response, "success": True}]

            return f"Agent {agent_name} completed task. Result: {response}"

        except Exception as e:
            error_msg = f"Error executing {agent_name}: {e!s}"

            # Update execution history with error
            if hasattr(state, "execution_history"):
                state["execution_history"] = [*state.get("execution_history", []), {"agent_name": agent_name, "task": task, "result": None, "success": False, "error": str(e)}]

            return error_msg

    # Set the tool name dynamically
    handoff_to_agent.name = f"handoff_to_{agent_name}"
    return handoff_to_agent


def create_forward_message_tool(supervisor_name: str = "supervisor"):
    """Create a tool to forward agent messages."""

    @tool
    def forward_message(from_agent: str, state: Annotated[dict, InjectedState]) -> str:
        """Forward the latest message from a specific agent to the user.

        Args:
            from_agent: Name of the agent whose message to forward

        Returns:
            The forwarded message content
        """
        try:
            # Look for the latest message from the specified agent
            messages = state.get("messages", [])

            # Find the most recent message from this agent
            target_message = None
            for msg in reversed(messages):
                if (hasattr(msg, "name") and msg.name == from_agent) or (
                    hasattr(msg, "additional_kwargs")
                    and msg.additional_kwargs.get("agent_name") == from_agent
                ):
                    target_message = msg
                    break

            if not target_message:
                return f"No message found from agent '{from_agent}'"

            # Forward the message content
            content = (
                target_message.content
                if hasattr(target_message, "content")
                else str(target_message)
            )

            return f"Forwarding from {from_agent}: {content}"

        except Exception as e:
            return f"Error forwarding message from {from_agent}: {e!s}"

    forward_message.name = "forward_message"
    return forward_message


def create_list_agents_tool(supervisor_instance):
    """Create a tool to list available agents."""

    @tool
    def list_agents() -> str:
        """List all available agents in the registry.

        Returns:
            Description of available agents and their capabilities
        """
        try:
            agents = supervisor_instance.agent_registry.list_agents()

            if not agents:
                return "No agents currently available in the registry."

            result = "Available agents:\n"
            for name, info in agents.items():
                result += f"\n• {name}: {info['description']}"
                if info.get("capabilities"):
                    result += f"\n  Capabilities: {', '.join(info['capabilities'])}"

            return result

        except Exception as e:
            return f"Error listing agents: {e!s}"

    list_agents.name = "list_agents"
    return list_agents


# ============================================================================
# DYNAMIC SUPERVISOR AGENT
# ============================================================================


class DynamicSupervisorAgent(ReactAgent):
    """Dynamic supervisor that selects and executes agents at runtime.

    This agent inherits from ReactAgent to get the looping behavior needed
    for continuous agent selection and execution. It dynamically creates
    handoff tools for each agent in the registry.
    """

    # Override state schema
    state_schema: type[SupervisorState] = SupervisorState

    # Agent registry
    agent_registry: AgentRegistry = Field(default_factory=AgentRegistry)

    def setup_agent(self):
        """Setup supervisor with dynamic agent tools."""
        # Create dynamic tools based on registry
        self.tools = self._create_dynamic_tools()

        # Set system message for supervisor role
        self.system_message = self._create_system_message()

        # Initialize the registry in the state if needed
        self._sync_registry_to_state()

        super().setup_agent()

    def _create_dynamic_tools(self):
        """Create tools dynamically based on agent registry."""
        tools = []

        # Always include these core tools
        tools.extend(
            [
                create_list_agents_tool(self),
                create_forward_message_tool("supervisor"),
                self._create_end_supervision_tool(),
            ]
        )

        # Create handoff tools for each registered agent
        for agent_name in self.agent_registry.list_agents():
            handoff_tool = create_dynamic_handoff_tool(self, agent_name)
            tools.append(handoff_tool)

        return tools

    def _create_system_message(self):
        """Create system message with available agents."""
        agents = self.agent_registry.list_agents()

        base_message = """You are a dynamic supervisor agent that coordinates multiple specialized agents.

Your role is to:
1. Understand the user's request
2. Select the most appropriate agent for the task using handoff tools
3. Review results and decide next steps
4. Continue until the task is complete

Available tools:
- list_agents: See all available agents and their capabilities
- handoff_to_[agent_name]: Transfer control to a specific agent with a task
- forward_message: Forward an agent's response to the user
- end_supervision: Complete the supervision when task is done
"""

        if agents:
            base_message += "\nAvailable agents:\n"
            for name, info in agents.items():
                base_message += f"• {name}: {info['description']}\n"

        base_message += "\nAlways think step by step and explain your reasoning."

        return base_message

    def _sync_registry_to_state(self):
        """Sync agent registry to state format."""
        # This will be used when the state is created

    def _create_end_supervision_tool(self):
        """Create tool for ending supervision."""

        @tool
        def end_supervision(final_result: str) -> str:
            """End the supervision process with a final result.

            Args:
                final_result: The final result to return to the user

            Returns:
                Confirmation message
            """
            return f"Supervision complete. Final result: {final_result}"

        end_supervision.name = "end_supervision"
        return end_supervision

    def add_agent_to_registry(
        self,
        name: str,
        description: str,
        agent_class: type[Agent],
        config: Dict[str, Any] | None = None,
    ):
        """Dynamically add an agent to the registry and update tools."""
        self.agent_registry.register(name, description, agent_class, config)

        # Recreate tools to include the new agent
        self.tools = self._create_dynamic_tools()

        # Update system message
        self.system_message = self._create_system_message()

        logger.info(f"Added agent '{name}' to supervisor registry")

    def remove_agent_from_registry(self, name: str):
        """Dynamically remove an agent from the registry and update tools."""
        self.agent_registry.unregister(name)

        # Recreate tools without the removed agent
        self.tools = self._create_dynamic_tools()

        # Update system message
        self.system_message = self._create_system_message()

        logger.info(f"Removed agent '{name}' from supervisor registry")

    def _prepare_input(self, input_data: Any) -> Any:
        """Prepare input data and sync registry to state."""
        prepared = super()._prepare_input(input_data)

        # Ensure prepared is a dict
        if hasattr(prepared, "model_dump"):
            prepared_dict = prepared.model_dump()
        elif isinstance(prepared, dict):
            prepared_dict = prepared
        else:
            prepared_dict = {"messages": []}

        # Sync registry to state
        prepared_dict["agent_registry"] = self.agent_registry.to_state_format()

        return prepared_dict


# ============================================================================
# TEST/DEMO FUNCTIONS
# ============================================================================


def create_test_registry() -> AgentRegistry:
    """Create a test registry with some mock agents."""
    registry = AgentRegistry()

    # We'll use SimpleAgent as a base for testing
    from haive.agents.simple.agent import SimpleAgent

    registry.register(
        name="research_agent",
        description="Searches for information and conducts research",
        agent_class=SimpleAgent,
        capabilities=["web_search", "analysis", "summarization"],
    )

    registry.register(
        name="math_agent",
        description="Performs mathematical calculations and analysis",
        agent_class=SimpleAgent,
        capabilities=["arithmetic", "algebra", "statistics"],
    )

    return registry


def test_supervisor_basic():
    """Basic test of supervisor functionality."""
    # Create supervisor with test registry
    registry = create_test_registry()

    supervisor = DynamicSupervisorAgent(name="Test Supervisor", agent_registry=registry)


    return supervisor


def test_dynamic_tools():
    """Test dynamic tool creation and handoff functionality."""

    # Create supervisor
    registry = create_test_registry()
    supervisor = DynamicSupervisorAgent(
        name="Dynamic Test Supervisor", agent_registry=registry
    )

    # Check tools were created
    for tool in supervisor.tools:
        pass

    # Test list_agents tool
    list_tool = next(t for t in supervisor.tools if t.name == "list_agents")
    agents_result = list_tool.invoke({})

    # Test adding a new agent dynamically
    from haive.agents.simple.agent import SimpleAgent

    supervisor.add_agent_to_registry(
        name="calculator_agent",
        description="Performs complex mathematical calculations",
        agent_class=SimpleAgent,
        config={"name": "Calculator Agent"},
    )


    # Verify handoff tool was created
    handoff_tools = [t for t in supervisor.tools if t.name.startswith("handoff_to_")]

    # Test the new handoff tool
    calc_handoff = next(
        t for t in supervisor.tools if t.name == "handoff_to_calculator_agent"
    )

    return supervisor


def test_supervisor_workflow():
    """Test a complete supervisor workflow."""

    supervisor = test_dynamic_tools()

    # Create a mock state for testing
    test_state = {
        "messages": [],
        "agent_registry": supervisor.agent_registry.to_state_format(),
        "current_agent_name": None,
        "current_task": None,
        "execution_history": [],
    }

    # Test handoff functionality
    research_handoff = next(
        t for t in supervisor.tools if t.name == "handoff_to_research_agent"
    )

    try:
        # This would normally be called by the graph, but we'll test directly
        result = research_handoff.invoke(
            {"task": "Research the latest developments in AI", "_state": test_state}
        )
    except Exception as e:

    return supervisor


if __name__ == "__main__":
    # Run comprehensive tests

    # Basic test
    supervisor = test_supervisor_basic()

    # Dynamic tools test
    supervisor = test_dynamic_tools()

    # Workflow test
    supervisor = test_supervisor_workflow()

