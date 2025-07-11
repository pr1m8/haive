"""Simple test for MultiAgentBase approach without dependencies."""

import asyncio
from typing import Literal

from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode


# Test just the routing logic
def simple_route(state) -> Literal["agent_node", "END"]:
    """Simple routing based on messages."""
    if state.get("messages"):
        last_msg = state["messages"][-1]
        if hasattr(last_msg, "content") and "done" in last_msg.content.lower():
            return "END"
    return "agent_node"


async def simple_agent_node(state):
    """Simple agent node that adds a message."""
    return {"messages": [AIMessage(content="Agent processed the task. Done!")]}


async def test_simple_multiagent():
    """Test basic MultiAgentBase functionality."""
    # Create a simple supervisor agent
    supervisor = SimpleAgent(
        name="supervisor",
        engine=AugLLMConfig(
            name="supervisor_engine",
            llm_config=AzureLLMConfig(model="gpt-4o"),
            system_message="You are a simple supervisor.",
        ),
    )

    # Create system with MultiAgentBase
    system = MultiAgentBase(
        agents=[supervisor],
        workflow_nodes={"agent_node": simple_agent_node},
        branches=[(supervisor, simple_route, {"agent_node": "agent_node", "END": END})],
        schema_build_mode=BuildMode.SEQUENCE,
        name="Simple Test System",
    )

    # Build and compile
    graph = system.build_graph()
    compiled = graph.compile()

    # Test with simple input
    initial_state = {"messages": [HumanMessage(content="Process this task")]}

    result = await compiled.ainvoke(initial_state)

    for _i, _msg in enumerate(result.get("messages", [])):
        pass


if __name__ == "__main__":
    asyncio.run(test_simple_multiagent())
