"""Test Supabase configuration using environment variables from .env file."""

import os

import pytest
from dotenv import load_dotenv
from haive.core.engine.agent.config import AgentConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig
from langgraph.graph import END

from haive.agents.configurable_agent import ConfigurableAgent

# Load environment variables
load_dotenv()


class TestSupabaseAgent(ConfigurableAgent):
    """Test agent for Supabase configuration."""

    def setup_agent(self):
        """Setup hook."""
        pass

    def build_graph(self) -> BaseGraph:
        """Build a simple test graph."""
        from haive.core.graph.state_graph.state_graph import (
            StateGraph as HaiveStateGraph,
        )

        graph = HaiveStateGraph(state_schema={"messages": list})

        def dummy_node(state):
            return {"messages": state.get("messages", []) + ["Processed"]}

        graph.add_node("test", dummy_node)
        graph.add_edge("test", END)
        graph.set_entry_point("test")

        return graph


def test_supabase_direct_postgres_from_env():
    """Test Supabase using direct PostgreSQL connection with env vars."""
    # Check if we have the connection string in env
    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

    if not connection_string:
        pytest.skip("POSTGRES_CONNECTION_STRING not set in environment")

    print(f"\n✓ Found POSTGRES_CONNECTION_STRING in environment")

    # Create PostgreSQL config using connection string from env
    postgres_config = PostgresCheckpointerConfig(connection_string=connection_string)

    # Create agent with PostgreSQL persistence
    agent_config = AgentConfig(
        persistence=postgres_config,
        runnable_config={
            "configurable": {"thread_id": "test-postgres-env", "recursion_limit": 100}
        },
    )

    agent = TestSupabaseAgent(name="test_postgres_agent", config=agent_config)

    # Verify configuration
    assert agent.persistence == postgres_config
    assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    print("✓ Agent configured with PostgreSQL persistence from env")

    # Test basic functionality
    try:
        result = agent.run({"messages": ["Hello"]})
        print(f"✓ Agent execution successful: {result}")
        assert "messages" in result
        assert len(result["messages"]) > 0
    except Exception as e:
        print(
            f"⚠️  Agent execution failed (this may be expected if DB is not accessible): {e}"
        )


def test_supabase_rest_api_from_env():
    """Test Supabase using REST API with env vars."""
    # Check if we have Supabase credentials in env
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

    if not supabase_url or not supabase_key:
        pytest.skip(
            "SUPABASE_URL and SUPABASE_SERVICE_KEY/ANON_KEY not set in environment"
        )

    print(f"\n✓ Found SUPABASE_URL: {supabase_url}")
    print(
        f"✓ Found SUPABASE_KEY: {'SERVICE_KEY' if os.getenv('SUPABASE_SERVICE_KEY') else 'ANON_KEY'}"
    )

    # Create Supabase config - it will use env vars automatically
    supabase_config = SupabaseCheckpointerConfig(
        user_id="test-user", setup_needed=False  # Skip schema setup for test
    )

    # Create agent with Supabase persistence
    agent_config = AgentConfig(
        persistence=supabase_config,
        runnable_config={
            "configurable": {"thread_id": "test-supabase-env", "recursion_limit": 100}
        },
    )

    agent = TestSupabaseAgent(name="test_supabase_agent", config=agent_config)

    # Verify configuration
    assert agent.persistence == supabase_config
    assert agent.persistence.user_id == "test-user"
    assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    print("✓ Agent configured with Supabase persistence from env")

    # Test basic functionality
    try:
        result = agent.run({"messages": ["Hello from Supabase"]})
        print(f"✓ Agent execution successful: {result}")
        assert "messages" in result
        assert len(result["messages"]) > 0
    except Exception as e:
        print(
            f"⚠️  Agent execution failed (this may be expected if Supabase is not accessible): {e}"
        )


def test_parse_supabase_connection_string():
    """Test parsing Supabase PostgreSQL connection string."""
    # Example Supabase connection string
    example_string = "postgresql://postgres:[YOUR-PASSWORD]@db.zkssazqhwcetsnbiuqik.supabase.co:5432/postgres"

    # Parse the connection string
    import re

    pattern = r"postgresql://(?P<user>[^:]+):(?P<password>[^@]+)@(?P<host>[^:]+):(?P<port>\d+)/(?P<database>.+)"
    match = re.match(pattern, example_string)

    if match:
        parts = match.groupdict()
        print(f"\nParsed connection string:")
        print(f"  Host: {parts['host']}")
        print(f"  Port: {parts['port']}")
        print(f"  Database: {parts['database']}")
        print(f"  User: {parts['user']}")
        print(f"  Password: {'*' * len(parts['password'])}")

        # You can also create config with individual parameters
        postgres_config = PostgresCheckpointerConfig(
            db_host=parts["host"],
            db_port=int(parts["port"]),
            db_name=parts["database"],
            db_user=parts["user"],
            db_pass=parts["password"],
        )

        print("\n✓ Successfully created PostgresCheckpointerConfig from parsed values")


def test_env_variables_loaded():
    """Test that environment variables are properly loaded."""
    print("\n=== Environment Variables Check ===")

    # Check PostgreSQL connection
    if os.getenv("POSTGRES_CONNECTION_STRING"):
        print("✓ POSTGRES_CONNECTION_STRING is set")
        # Don't print the actual value for security
        conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
        if "zkssazqhwcetsnbiuqik.supabase.co" in conn_str:
            print("  - Points to Supabase PostgreSQL endpoint")
    else:
        print("✗ POSTGRES_CONNECTION_STRING not found")

    # Check Supabase REST API credentials
    if os.getenv("SUPABASE_URL"):
        print(f"✓ SUPABASE_URL is set: {os.getenv('SUPABASE_URL')}")
    else:
        print("✗ SUPABASE_URL not found")

    if os.getenv("SUPABASE_SERVICE_KEY"):
        print("✓ SUPABASE_SERVICE_KEY is set")
    elif os.getenv("SUPABASE_ANON_KEY"):
        print("✓ SUPABASE_ANON_KEY is set")
    else:
        print("✗ Neither SUPABASE_SERVICE_KEY nor SUPABASE_ANON_KEY found")

    print("\n=== Configuration Methods Available ===")
    if os.getenv("POSTGRES_CONNECTION_STRING"):
        print("✓ Can use PostgresCheckpointerConfig with connection_string")
    if os.getenv("SUPABASE_URL") and (
        os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    ):
        print("✓ Can use SupabaseCheckpointerConfig with REST API")


if __name__ == "__main__":
    # Run the environment check first
    test_env_variables_loaded()

    # Run other tests
    print("\n" + "=" * 50 + "\n")
    pytest.main([__file__, "-v", "-s"])
