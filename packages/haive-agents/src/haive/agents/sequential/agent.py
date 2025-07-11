# SEQUENTIAL AGENT
# ============================================================================

from collections.abc import Sequence
from typing import Any

from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from langgraph.graph import END, START
from pydantic import BaseModel, Field, model_validator

from haive.agents.base.agent import Agent


class SequentialAgent(Agent):
    """Sequential agent that executes multiple agents in sequence."""

    name: str = Field(default="Sequential Agent")

    # Use Union[Agent, Any] to be more permissive, or use forward reference
    agents: Sequence[Agent | Any] = Field(
        ..., description="List of agents to execute sequentially"
    )
    state_schema: type[BaseModel] | None = Field(default=None)
    smart_compose: bool = Field(
        default=True, description="Whether to use smart composition"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_agents(cls, values):
        """Validate that agents are Agent instances or convertible."""
        if isinstance(values, dict) and "agents" in values:
            agents = values["agents"]

            # Validate each agent
            validated_agents = []
            for i, agent in enumerate(agents):
                # Check if it's already an Agent instance
                if hasattr(agent, "build_graph") and hasattr(agent, "invoke"):
                    validated_agents.append(agent)
                else:
                    raise ValueError(
                        f"Agent at index {i} is not a valid Agent instance"
                    )

            values["agents"] = validated_agents

        return values

    @model_validator(mode="after")
    def set_state_schema(self):
        self.input_schema = SchemaComposer.from_components(
            [self.agents[0].engine]
        ).derive_input_schema()
        self.state_schema = SchemaComposer.from_components(
            [agent.engine for agent in self.agents]
        )
        return self

    @model_validator(mode="after")
    def validate_non_empty_agents(self):
        """Ensure we have at least one agent."""
        if not self.agents or len(self.agents) == 0:
            raise ValueError("SequentialAgent requires at least one agent")
        return self

    def build_graph(self) -> BaseGraph:
        """Build the sequential graph connecting agents in order."""
        # Create the graph
        graph = BaseGraph(name=getattr(self, "name", "sequential_agent"))

        node_names = []

        # Add each agent as a node
        for i, agent in enumerate(self.agents):
            # Generate node name
            if hasattr(agent, "name") and agent.name:
                node_name = agent.name
            elif hasattr(agent, "id") and agent.id:
                node_name = agent.id
            else:
                node_name = f"agent_{i}"

            # Ensure unique node names
            original_name = node_name
            counter = 1
            while node_name in node_names:
                node_name = f"{original_name}_{counter}"
                counter += 1

            node_names.append(node_name)

            # Create engine node config - the agent itself is the engine
            engine_node = EngineNodeConfig(name=node_name, engine=agent)
            graph.add_node(node_name, engine_node)

        # Connect the nodes in sequence
        for i in range(len(node_names)):
            if i == 0:
                # First node connects from START
                graph.add_edge(START, node_names[i])

            if i == len(node_names) - 1:
                # Last node connects to END
                graph.add_edge(node_names[i], END)
            else:
                # Connect to next node
                graph.add_edge(node_names[i], node_names[i + 1])

        return graph
