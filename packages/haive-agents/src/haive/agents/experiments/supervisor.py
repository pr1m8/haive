import operator
from enum import Enum
from typing import Annotated, List, Protocol, runtime_checkable

from haive.core.common.mixins.getter_mixin import GetterMixin
from haive.core.engine.aug_llm import AugLLMConfig

# ============================================================================
# REACT AGENT
# ============================================================================
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langgraph.graph import END
from pydantic import (
    BaseModel,
    Field,
    computed_field,
    field_serializer,
    field_validator,
    model_validator,
)

from haive.agents.base.agent import Agent
from haive.agents.react.agent import ReactAgent

# from haive.agents.rag.base.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


@tool
def add(a: int, b: int) -> int:
    """returns the sum of two numbers"""
    return a + b


class Plan(BaseModel):
    steps: List[str] = Field(description="list of steps")


add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")
simple_agent = SimpleAgent(engine=plan_aug)
react_agent = ReactAgent(engine=add_aug)
from langgraph_supervisor import (
    create_forward_message_tool,
    create_handoff_tool,
    create_supervisor,
)


class MultiAgentState(BaseModel, GetterMixin):
    agents: List[Agent] = Field(default_factory=[])
    selected_agents: Annotated[List[Agent], operator.add] = Field(default_factory=[])

    @computed_field
    def selected_agent(self) -> Agent:
        return selected_agents[-1] if selected_agents else None


def temp_node(state):
    selected_agent = state.get("selected_agent")
    agent = agent.create_runnable()
    result = agent.run(input_payload)


from langgraph.graph import END, START, StateGraph

base_graph = StateGraph(state_schema=MultiAgentState)
base_graph.add_node(temp_node)
base_graph.set_entry_point("temp_node")
base_graph.set_finish_point("temp_node")
base_graph.compile()
