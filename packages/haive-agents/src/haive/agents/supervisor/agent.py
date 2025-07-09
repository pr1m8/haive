"""Haive Supervisor Agent Implementation.

A ReactAgent-based supervisor that manages multiple specialized agents using
state-driven prompts and generic routing nodes, following LangGraph patterns
but adapted to Haive's architecture.
"""

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Union

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor.registry import AgentRegistry

logger = logging.getLogger(__name__)
console = Console()


class SupervisorState(BaseModel):
    """Extended state for supervisor operations."""

    # Core messaging (inherited from base state)
    messages: List[Any] = Field(default_factory=list)

    # Supervisor-specific fields
    registered_agents: Dict[str, Any] = Field(
        default_factory=dict, description="Available agents"
    )
    routing_decision: Optional[str] = Field(None, description="Last routing decision")
    routing_timestamp: Optional[float] = Field(
        None, description="When routing occurred"
    )
    target_agent: Optional[str] = Field(None, description="Current target agent")
    last_agent: Optional[str] = Field(None, description="Previously active agent")
    conversation_complete: bool = Field(
        False, description="Whether conversation is done"
    )

    # Task tracking
    task_keywords: List[str] = Field(
        default_factory=list, description="Detected task types"
    )
    task_complexity: str = Field("Simple", description="Estimated complexity")


class SupervisorAgent(ReactAgent):
    """Supervisor agent that manages multiple specialized agents.

    Extends ReactAgent to provide intelligent routing between registered agents
    using state-driven prompts and a generic routing mechanism.
    """

    def __init__(
        self, name: str = "supervisor", engine: Optional[AugLLMConfig] = None, **kwargs
    ):
        """Initialize supervisor agent.

        Args:
            name: Agent name
            engine: LLM engine for routing decisions
            **kwargs: Additional ReactAgent arguments
        """
        # Set default state schema to SupervisorState
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = SupervisorState

        super().__init__(name=name, engine=engine, **kwargs)

        # Initialize agent registry
        self.routing_model = DynamicChoiceModel[str](
            options=[], model_name="SupervisorChoice", include_end=True
        )
        self.agent_registry = AgentRegistry(self.routing_model)

        # Supervisor-specific configuration
        self.delegation_prompt = self._create_delegation_prompt()

        logger.info(f"SupervisorAgent '{name}' initialized")

    def register_agent(
        self, agent: Agent, capability_description: Optional[str] = None
    ) -> bool:
        """Register an agent for supervision.

        Args:
            agent: Agent to register
            capability_description: Description of agent capabilities

        Returns:
            bool: True if registration successful
        """
        success = self.agent_registry.register(agent, capability_description)

        if success:
            # Update delegation prompt with new agents
            self.delegation_prompt = self._create_delegation_prompt()
            console.print(f"[green]✅ Registered agent:[/green] {agent.name}")

        return success

    def unregister_agent(self, agent_name: str) -> bool:
        """Unregister an agent.

        Args:
            agent_name: Name of agent to remove

        Returns:
            bool: True if removal successful
        """
        success = self.agent_registry.unregister(agent_name)

        if success:
            # Update delegation prompt
            self.delegation_prompt = self._create_delegation_prompt()
            console.print(f"[red]❌ Unregistered agent:[/red] {agent_name}")

        return success

    def _create_delegation_prompt(self) -> ChatPromptTemplate:
        """Create prompt template for agent delegation."""

        # Get available agents and capabilities
        available_agents = self.agent_registry.get_available_agents()
        capabilities = self.agent_registry.get_agent_capabilities()

        # Build agent list for prompt
        if available_agents:
            agent_list = []
            for agent_name in available_agents:
                capability = capabilities.get(agent_name, f"Handles {agent_name} tasks")
                agent_list.append(f"- {agent_name}: {capability}")
            agents_text = "\n".join(agent_list)
        else:
            agents_text = "No agents currently available"

        system_prompt = f"""You are a supervisor managing a team of specialized agents. Your job is to analyze incoming requests and delegate them to the most appropriate agent.

Available Agents:
{agents_text}
- END: Use this when the conversation should end or task is complete

Instructions:
1. Analyze the user's request carefully
2. Determine which agent is best suited for the task
3. Respond with ONLY the agent name (e.g., "research_agent" or "END")
4. Choose END if the conversation is complete or no further action is needed

Current agents available: {', '.join(available_agents) if available_agents else 'None'}

Response format: Provide only the agent name or END, nothing else."""

        return ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("placeholder", "{messages}"),
            ]
        )

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with custom routing logic."""

        # Create base graph
        graph = BaseGraph(self.state_schema)

        # Add supervisor node (the LLM decision maker)
        supervisor_node = self._create_supervisor_node()
        graph.add_node("supervisor", supervisor_node)
        graph.add_edge(START, "supervisor")

        # Add routing node (interprets LLM decision and routes)
        routing_node = self._create_routing_node()
        graph.add_node("routing", routing_node)
        graph.add_edge("supervisor", "routing")

        # Add registered agents as nodes
        available_agents = self.agent_registry.get_available_agents()
        for agent_name in available_agents:
            agent_wrapper = self._create_agent_wrapper(agent_name)
            graph.add_node(agent_name, agent_wrapper)
            # Agents return to supervisor after execution
            graph.add_edge(agent_name, "supervisor")

        # Add conditional edges from routing node
        routing_destinations = available_agents + ["__end__"]
        graph.add_conditional_edges(
            "routing", self._routing_condition, routing_destinations
        )

        return graph

    def _create_supervisor_node(self) -> Callable:
        """Create the supervisor LLM node."""

        async def supervisor_node(state: SupervisorState, config=None) -> dict:
            """Supervisor node that makes routing decisions."""

            # Update registered agents in state
            agent_dict = {}
            for agent_name in self.agent_registry.get_available_agents():
                agent = self.agent_registry.get_agent(agent_name)
                if agent:
                    # Store agent reference or metadata
                    agent_dict[agent_name] = {
                        "name": agent_name,
                        "capability": self.agent_registry.get_agent_capability(
                            agent_name
                        ),
                    }

            # Use the delegation prompt
            formatted_prompt = self.delegation_prompt.format_messages(
                messages=state.messages
            )

            # Get LLM response
            if self.main_engine:
                response = await self.main_engine.ainvoke(formatted_prompt, config)

                # Extract routing decision from response
                if isinstance(response, AIMessage):
                    decision = response.content.strip()
                else:
                    decision = str(response).strip()

                # Validate decision
                valid_options = self.agent_registry.get_routing_options()
                if decision not in valid_options:
                    # Try to find a match
                    decision_upper = decision.upper()
                    for option in valid_options:
                        if option.upper() == decision_upper:
                            decision = option
                            break
                    else:
                        # Default to END if no match
                        decision = "END"

                logger.info(f"Supervisor decision: {decision}")

                return {
                    "messages": state.messages
                    + [AIMessage(content=f"Routing to: {decision}")],
                    "registered_agents": agent_dict,
                    "routing_decision": decision,
                    "routing_timestamp": time.time(),
                    "target_agent": decision if decision != "END" else None,
                }

            # Fallback if no engine
            return {"routing_decision": "END", "target_agent": None}

        return supervisor_node

    def _create_routing_node(self) -> Callable:
        """Create the routing node that interprets decisions."""

        def routing_node(state: SupervisorState, config=None) -> dict:
            """Route based on supervisor decision."""

            decision = state.routing_decision

            if not decision:
                decision = "END"

            logger.info(f"Routing to: {decision}")

            return {"routing_decision": decision, "last_agent": state.target_agent}

        return routing_node

    def _create_agent_wrapper(self, agent_name: str) -> Callable:
        """Create wrapper for executing a specific agent."""

        async def agent_wrapper(state: SupervisorState, config=None) -> dict:
            """Execute the target agent and return results."""

            agent = self.agent_registry.get_agent(agent_name)
            if not agent:
                logger.error(f"Agent {agent_name} not found")
                return {
                    "messages": state.messages
                    + [AIMessage(content=f"Error: Agent {agent_name} not available")],
                    "last_agent": agent_name,
                    "target_agent": None,
                }

            try:
                # Create agent state from supervisor state
                agent_state = self._prepare_agent_state(state, agent)

                # Execute agent
                result = await agent.ainvoke(agent_state, config)

                # Extract messages from result
                result_messages = getattr(result, "messages", [])
                if isinstance(result, dict):
                    result_messages = result.get("messages", [])

                # Return updated state
                return {
                    "messages": state.messages + result_messages,
                    "last_agent": agent_name,
                    "target_agent": None,
                    "routing_decision": None,  # Clear for next routing
                }

            except Exception as e:
                logger.error(f"Agent {agent_name} execution failed: {e}")
                return {
                    "messages": state.messages
                    + [
                        AIMessage(
                            content=f"Agent {agent_name} encountered an error: {str(e)}"
                        )
                    ],
                    "last_agent": agent_name,
                    "target_agent": None,
                }

        return agent_wrapper

    def _prepare_agent_state(
        self, supervisor_state: SupervisorState, agent: Agent
    ) -> Any:
        """Prepare state for agent execution."""

        # If agent has specific state schema, try to convert
        if hasattr(agent, "state_schema") and agent.state_schema:
            try:
                # Try to create agent state with messages
                agent_state = agent.state_schema(messages=supervisor_state.messages)
                return agent_state
            except Exception as e:
                logger.warning(f"Could not create specific state for {agent.name}: {e}")

        # Fallback to basic state with messages
        return type("State", (), {"messages": supervisor_state.messages})()

    def _routing_condition(self, state: SupervisorState) -> str:
        """Determine routing destination from state."""
        decision = state.routing_decision

        if decision == "END":
            return "__end__"

        # Validate decision is available
        available_agents = self.agent_registry.get_available_agents()
        if decision in available_agents:
            return decision

        # Default to end if invalid
        return "__end__"

    def get_registered_agents(self) -> List[str]:
        """Get list of registered agent names."""
        return self.agent_registry.get_available_agents()

    def print_supervisor_status(self) -> None:
        """Print comprehensive supervisor status."""

        # Main status table
        table = Table(title="🔧 Supervisor Agent Status")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        table.add_row("Supervisor Name", self.name)
        table.add_row("Registered Agents", str(self.agent_registry.get_agent_count()))
        table.add_row(
            "Routing Options", str(len(self.agent_registry.get_routing_options()))
        )
        table.add_row("Has Engine", str(self.main_engine is not None))

        console.print(table)

        # Show registry details
        self.agent_registry.print_registry_state()

        # Show available routing options
        options_panel = Panel(
            f"Available routing options: {', '.join(self.agent_registry.get_routing_options())}",
            title="🎯 Routing Options",
            style="blue",
        )
        console.print(options_panel)
