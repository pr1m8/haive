from collections.abc import Sequence
from typing import Any

from haive.agents.base.agent import Agent
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.schema_composer import SchemaComposer
from langgraph.graph import END, START
from pydantic import BaseModel, Field, model_validator


class SequentialAgent(Agent):
    """Sequential agent that executes multiple agents in sequence."""

    name: str = Field(default="Sequential Agent")
    agents: Sequence[Agent | Any] = Field(
        ..., description="List of agents to execute sequentially"
    )
    state_schema: type[BaseModel] | None = Field(default=None)
    smart_compose: bool = Field(
        default=True, description="Whether to use smart composition"
    )

    @model_validator(mode="before")
    def validate_agents(cls, values) -> Any:
        """Validate that agents are Agent instances or convertible."""
        if isinstance(values, dict) and "agents" in values:
            agents = values["agents"]
            validated_agents = []
            for i, agent in enumerate(agents):
                if hasattr(agent, "build_graph") and hasattr(agent, "invoke"):
                    validated_agents.append(agent)
                else:
                    raise ValueError(
                        f"Agent at index {i} is not a valid Agent instance"
                    )
            values["agents"] = validated_agents
        return values

    @model_validator(mode="after")
    def set_state_schema(self) -> "SequentialAgent":
        self.input_schema = SchemaComposer.from_components(
            [self.agents[0].engine]
        ).derive_input_schema()
        self.state_schema = SchemaComposer.from_components(
            [agent.engine for agent in self.agents]
        )
        return self

    @model_validator(mode="after")
    def validate_non_empty_agents(self) -> "SequentialAgent":
        """Ensure we have at least one agent."""
        if not self.agents or len(self.agents) == 0:
            raise ValueError("SequentialAgent requires at least one agent")
        return self

    def build_graph(self) -> BaseGraph:
        """Build the sequential graph connecting agents in order."""
        graph = BaseGraph(name=getattr(self, "name", "sequential_agent"))
        node_names = []
        for i, agent in enumerate(self.agents):
            if hasattr(agent, "name") and agent.name:
                node_name = agent.name
            elif hasattr(agent, "id") and agent.id:
                node_name = agent.id
            else:
                node_name = f"agent_{i}"
            original_name = node_name
            counter = 1
            while node_name in node_names:
                node_name = f"{original_name}_{counter}"
                counter += 1
            node_names.append(node_name)
            engine_node = EngineNodeConfig(name=node_name, engine=agent)
            graph.add_node(node_name, engine_node)
        for i in range(len(node_names)):
            if i == 0:
                graph.add_edge(START, node_names[i])
            if i == len(node_names) - 1:
                graph.add_edge(node_names[i], END)
            else:
                graph.add_edge(node_names[i], node_names[i + 1])
        return graph


def build_graph(agents: Sequence[Agent]) -> BaseGraph:
    """Build a sequential graph from a list of agents."""
    sequential_agent = SequentialAgent(agents=agents)
    return sequential_agent.build_graph()


def set_state_schema(agents: Sequence[Agent]) -> type[BaseModel] | None:
    """Set state schema for a list of agents."""
    sequential_agent = SequentialAgent(agents=agents)
    return sequential_agent.state_schema


def validate_agents(agents: Sequence[Agent]) -> bool:
    """Validate that all items are valid agents."""
    try:
        SequentialAgent(agents=agents)
        return True
    except ValueError:
        return False


def validate_non_empty_agents(agents: Sequence[Agent]) -> bool:
    """Validate that agents list is not empty."""
    return bool(agents)
