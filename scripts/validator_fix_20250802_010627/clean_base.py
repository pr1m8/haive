"""Clean multi-agent base following proper Agent patterns."""

from haive.agents.base.agent import Agent
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from langgraph.graph import END, START
from pydantic import Field, model_validator


class CleanMultiAgent(Agent):
    """Clean multi-agent following base Agent patterns.

    This properly follows the base Agent class patterns:
    - Uses agents field similar to engines field
    - Lets base agent handle schema generation
    - Implements setup_agent() and build_graph() properly
    """

    # Agents field - similar to engines field in base Agent
    agents: list[Agent] | dict[str, Agent] = Field(
        default_factory=list,
        description="Agents to coordinate - similar to engines field",
    )

    # Execution mode
    execution_mode: str = Field(
        default="sequential",
        description="How to execute agents: sequential, parallel, conditional",
    )

    @model_validator(mode="after")
    def normalize_agents(cls) -> "CleanMultiAgent":
        """Normalize agents similar to how base Agent normalizes engines."""
        if isinstance(self.agents, list):
            # Convert list to dict using agent names - similar to engine
            # normalization
            agent_dict = {}
            for agent in self.agents:
                if not hasattr(agent, "name"):
                    raise ValueError(f"Agent {agent} must have 'name' attribute")
                agent_dict[agent.name] = agent
            self.agents = agent_dict

        return self

    def setup_agent(self) -> None:
        """Setup hook - let base agent handle schema generation."""
        # Set state schema to MultiAgentState if not provided
        if not self.state_schema:
            self.state_schema = MultiAgentState
            self.use_prebuilt_base = True

        # Add agents to engines dict for schema generation
        if isinstance(self.agents, dict):
            for agent_name, agent in self.agents.items():
                # Add agent's engines to our engines dict with namespacing
                if hasattr(agent, "engines") and agent.engines:
                    for engine_name, engine in agent.engines.items():
                        namespaced_name = f"{agent_name}.{engine_name}"
                        self.engines[namespaced_name] = engine

    def build_graph(self) -> BaseGraph:
        """Build graph using AgentNodeV3 properly."""
        # Create graph - base agent will provide the state schema
        graph = BaseGraph(name=f"{self.name}_graph")

        if not isinstance(self.agents, dict):
            raise ValueError("Agents must be normalized to dict")

        # Add each agent using AgentNodeV3Config
        for agent_name, agent in self.agents.items():
            node_config = AgentNodeV3Config(
                name=f"agent_{agent_name}",
                agent_name=agent_name,
                agent=agent,
                project_state=True,
                extract_from_container=True,
                update_container_state=True,
            )
            graph.add_node(f"agent_{agent_name}", node_config)

        # Build edges based on execution mode
        if self.execution_mode == "sequential":
            self._build_sequential_edges(graph)
        else:
            raise NotImplementedError(f"Mode {self.execution_mode} not implemented")

        return graph

    def _build_sequential_edges(self, graph: BaseGraph):
        """Build sequential execution edges."""
        agent_names = list(self.agents.keys())

        # Connect START to first agent
        graph.add_edge(START, f"agent_{agent_names[0]}")

        # Connect agents in sequence
        for i in range(len(agent_names) - 1):
            graph.add_edge(f"agent_{agent_names[i]}", f"agent_{agent_names[i + 1]}")

        # Connect last agent to END
        graph.add_edge(f"agent_{agent_names[-1]}", END)
