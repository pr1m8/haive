"""Test if we can store agents in state and serialize it."""

import asyncio
import os

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import END, START, StateGraph

from haive.agents.experiments.supervisor.agent_info import AgentInfo
from haive.agents.experiments.supervisor.supervisor_state import SupervisorState
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


def test_node(state: SupervisorState):
    """Simple test node."""
    for agent_info in state.agents:
        pass
    return {}


async def test_agent_storage():
    """Test storing agents in state with PostgreSQL checkpointer."""

    # Create some agents
    search_engine = AugLLMConfig(
        name="search_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[tavily_search_tool],
        system_message="You are a search specialist.",
    )

    search_agent = ReactAgent(name="search_agent", engine=search_engine)

    simple_engine = AugLLMConfig(
        name="simple_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a simple assistant.",
    )

    simple_agent = SimpleAgent(name="simple_agent", engine=simple_engine)

    # Create state with agents
    state = SupervisorState()
    state.messages = [HumanMessage(content="Test message")]
    state.add_agent("search_agent", search_agent, "Search specialist", active=True)
    state.add_agent("simple_agent", simple_agent, "Simple assistant", active=False)


    # Build a simple graph
    graph = StateGraph(SupervisorState)
    graph.add_node("test", test_node)
    graph.add_edge(START, "test")
    graph.add_edge("test", END)

    # Test with in-memory (should work)
    from langgraph.checkpoint.memory import MemorySaver

    memory_app = graph.compile(checkpointer=MemorySaver())

    try:
        result = await memory_app.ainvoke(
            state, {"configurable": {"thread_id": "test1"}}
        )
    except Exception as e:
        pass")

    # Test with PostgreSQL (might fail)
    try:
        db_url = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/haive")
        conn = psycopg.connect(db_url)

        checkpointer = PostgresSaver(conn)
        postgres_app = graph.compile(checkpointer=checkpointer)

        await postgres_app.ainvoke(
            state, {"configurable": {"thread_id": "test2"}}
        )

        conn.close()
    except Exception as e:
        import traceback

        traceback.print_exc()

    import ormsgpack

    try:
        # Test model_dump
        state_dict = state.model_dump()
        serialized = ormsgpack.packb(state_dict)

        # Check what's in the agents field
        for i, agent_data in enumerate(state_dict.get("agents", [])):
    except Exception as e:
        pass")


if __name__ == "__main__":
    asyncio.run(test_agent_storage())
