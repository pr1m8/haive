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
    print(f"Node received {len(state.agents)} agents")
    for agent_info in state.agents:
        print(f"  - {agent_info.name}: {agent_info.active}")
    return {}


async def test_agent_storage():
    """Test storing agents in state with PostgreSQL checkpointer."""
    print("🔧 Testing agent storage in state...\n")

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
    print("1. Creating state with agents...")
    state = SupervisorState()
    state.messages = [HumanMessage(content="Test message")]
    state.add_agent("search_agent", search_agent, "Search specialist", active=True)
    state.add_agent("simple_agent", simple_agent, "Simple assistant", active=False)

    print(f"\n2. State created with {len(state.agents)} agents")

    # Build a simple graph
    graph = StateGraph(SupervisorState)
    graph.add_node("test", test_node)
    graph.add_edge(START, "test")
    graph.add_edge("test", END)

    # Test with in-memory (should work)
    print("\n3. Testing with in-memory checkpointer...")
    from langgraph.checkpoint.memory import MemorySaver

    memory_app = graph.compile(checkpointer=MemorySaver())

    try:
        result = await memory_app.ainvoke(
            state, {"configurable": {"thread_id": "test1"}}
        )
        print("✅ In-memory checkpointer works!")
    except Exception as e:
        print(f"❌ In-memory failed: {e}")

    # Test with PostgreSQL (might fail)
    print("\n4. Testing with PostgreSQL checkpointer...")
    try:
        db_url = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/haive")
        conn = psycopg.connect(db_url)

        checkpointer = PostgresSaver(conn)
        postgres_app = graph.compile(checkpointer=checkpointer)

        result = await postgres_app.ainvoke(
            state, {"configurable": {"thread_id": "test2"}}
        )
        print("✅ PostgreSQL checkpointer works!")

        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL failed: {type(e).__name__}: {e}")
        import traceback

        traceback.print_exc()

    print("\n5. Testing direct serialization...")
    import ormsgpack

    try:
        # Test model_dump
        state_dict = state.model_dump()
        serialized = ormsgpack.packb(state_dict)
        print(f"✅ state.model_dump() is serializable ({len(serialized)} bytes)")

        # Check what's in the agents field
        print("\n6. Checking serialized agent data:")
        for i, agent_data in enumerate(state_dict.get("agents", [])):
            print(f"   Agent {i}: {list(agent_data.keys())}")
            print(f"     - name: {agent_data.get('name')}")
            print(f"     - agent field: {agent_data.get('agent', 'NOT PRESENT')}")
            print(f"     - metadata: {agent_data.get('agent_metadata')}")
    except Exception as e:
        print(f"❌ Serialization failed: {e}")


if __name__ == "__main__":
    asyncio.run(test_agent_storage())
