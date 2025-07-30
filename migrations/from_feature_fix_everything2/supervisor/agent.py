"""Haive Supervisor Agent Implementation.

A clean supervisor that manages multiple specialized agents using
LLM-based routing decisions.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END
from pydantic import BaseModel, Field, field_validator

from haive.agents.base import Agent
from haive.agents.react.agent import ReactAgent

logger = logging.getLogger(__name__)


class SupervisorState(BaseModel):
    """State for supervisor operations."""

    messages: list[Any] = Field(default_factory=list)
    routing_decision: str | None = Field(None, description="Last routing decision")
    target_agent: str | None = Field(None, description="Current target agent")


# Default supervisor prompt
DEFAULT_SUPERVISOR_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a supervisor managing specialized agents.

Available Agents:
{agent_descriptions}

Instructions:
1. Analyze the user's request
2. Determine which agent is best suited
3. Respond with ONLY the agent name or "END" if complete

Decision:""",
        ),
        ("placeholder", "{messages}"),
    ]
)


class SupervisorAgent(ReactAgent):
    """Supervisor agent that routes between multiple specialized agents.

    Extends ReactAgent to leverage its looping behavior for continuous
    routing decisions based on conversation context.
    """

    # ========================================================================
    # SUPERVISOR SPECIFIC FIELDS
    # ========================================================================

    registered_agents: dict[str, Agent] = Field(
        default_factory=dict, description="Registered agents by name"
    )

    agent_descriptions: dict[str, str] = Field(
        default_factory=dict, description="Descriptions of agent capabilities"
    )

    supervisor_prompt: ChatPromptTemplate | None = Field(
        default=None, description="Custom prompt for routing decisions"
    )

    # ========================================================================
    # ENGINE CONFIGURATION
    # ========================================================================

    @field_validator("engine", mode="before")
    @classmethod
    def ensure_supervisor_engine(cls, v):
        """Ensure supervisor has a low-temperature engine for routing."""
        if v is None:
            v = AugLLMConfig(temperature=0.1)
        elif isinstance(v, dict):
            v = AugLLMConfig(**v)
        elif isinstance(v, AugLLMConfig):
            # Set low temperature for consistent routing
            v.temperature = min(v.temperature or 0.7, 0.3)
        return v

    # ========================================================================
    # SETUP
    # ========================================================================

    def setup_agent(self) -> None:
        """Setup supervisor with routing configuration."""
        # Call parent setup
        super().setup_agent()

        # Update prompt template for routing
        if self.engine:
            self.engine.prompt_template = (
                self.supervisor_prompt or self._create_routing_prompt()
            )

    def _create_routing_prompt(self) -> ChatPromptTemplate:
        """Create routing prompt with current agent descriptions."""
        if not self.agent_descriptions:
            descriptions = "No agents registered yet"
        else:
            descriptions = "\n".join(
                [f"- {name}: {desc}" for name, desc in self.agent_descriptions.items()]
            )

        # Use default template with current descriptions
        return DEFAULT_SUPERVISOR_PROMPT.partial(agent_descriptions=descriptions)

    # ========================================================================
    # AGENT REGISTRATION
    # ========================================================================

    def register_agent(self, name: str, agent: Agent, description: str) -> None:
        """Register an agent with the supervisor.

        Args:
            name: Unique name for the agent
            agent: The agent instance
            description: Description of capabilities
        """
        self.registered_agents[name] = agent
        self.agent_descriptions[name] = description

        # Add to engines for state composition
        self.engines[f"agent_{name}"] = agent

        # Update routing prompt
        if self.engine:
            self.engine.prompt_template = self._create_routing_prompt()

        logger.info(f"Registered agent '{name}': {description}")

    def unregister_agent(self, name: str) -> None:
        """Remove an agent from supervision."""
        if name in self.registered_agents:
            del self.registered_agents[name]
            del self.agent_descriptions[name]

            # Remove from engines
            engine_key = f"agent_{name}"
            if engine_key in self.engines:
                del self.engines[engine_key]

            # Update routing prompt
            if self.engine:
                self.engine.prompt_template = self._create_routing_prompt()

            logger.info(f"Unregistered agent '{name}'")

    # ========================================================================
    # GRAPH BUILDING
    # ========================================================================

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph with agent routing."""
        # Start with ReactAgent's graph
        graph = super().build_graph()

        if not self.registered_agents:
            logger.warning(
                "No agents registered, supervisor will only make routing decisions"
            )
            return graph

        # Add routing logic node after agent_node
        def route_to_agent(state: dict[str, Any]) -> str:
            """Route based on supervisor's decision."""
            messages = state.get("messages", [])
            if not messages:
                return END

            last_msg = messages[-1]
            if hasattr(last_msg, "content"):
                decision = last_msg.content.strip().lower()

                # Check for END
                if decision == "end":
                    return END

                # Match agent names
                for agent_name in self.registered_agents:
                    if agent_name.lower() in decision:
                        return f"{agent_name}_node"

            # Default to END if no clear decision
            return END

        # Remove existing edge from agent_node to END/tool_node
        # and add routing instead
        if "agent_node" in graph.nodes:
            # Find and remove outgoing edges from agent_node
            edges_to_remove = []
            for source, target in graph.edges:
                if source == "agent_node":
                    edges_to_remove.append((source, target))

            for edge in edges_to_remove:
                graph.remove_edge(*edge)

            # Add routing node
            graph.add_node("route_decision", route_to_agent)
            graph.add_edge("agent_node", "route_decision")

            # Add agent nodes
            for name, agent in self.registered_agents.items():
                node = AgentNodeV3Config(name=f"{name}_node", agent=agent)
                graph.add_node(f"{name}_node", node)
                # Agent outputs go back to supervisor
                graph.add_edge(f"{name}_node", "agent_node")

            # Add conditional routing
            route_map = {
                END: END,
                **{f"{name}_node": f"{name}_node" for name in self.registered_agents},
            }

            graph.add_conditional_edges("route_decision", route_to_agent, route_map)

        return graph

    # ========================================================================
    # CONVENIENCE METHODS
    # ========================================================================

    @classmethod
    def create_with_agents(
        cls,
        agents: list[tuple[str, Agent, str]],
        name: str = "supervisor",
        engine: AugLLMConfig | None = None,
        **kwargs,
    ) -> "SupervisorAgent":
        """Create supervisor with pre-registered agents.

        Args:
            agents: List of (name, agent, description) tuples
            name: Supervisor name
            engine: Custom engine config
            **kwargs: Additional arguments

        Returns:
            Configured SupervisorAgent

        Example:
            supervisor = SupervisorAgent.create_with_agents([
                ("writer", writer_agent, "Creative writing tasks"),
                ("coder", coder_agent, "Programming tasks"),
                ("analyst", analyst_agent, "Data analysis")
            ])
        """
        supervisor = cls(name=name, engine=engine, **kwargs)

        for agent_name, agent, description in agents:
            supervisor.register_agent(agent_name, agent, description)

        return supervisor
