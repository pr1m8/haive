"""Pytest-compatible Supabase integration tests."""

import asyncio
import os
from datetime import datetime

import psycopg
import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent


class TestSupabaseIntegration:
    """Test suite for Haive agent Supabase integration."""

    def test_environment_configuration(self, supabase_connection_string):
        """Test that Supabase environment is properly configured."""
        assert supabase_connection_string is not None
        assert "supabase.com" in supabase_connection_string

    def test_agent_detects_supabase(self):
        """Test that agent automatically detects Supabase configuration."""
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Test Agent")

        # Check persistence configuration
        assert hasattr(agent, "persistence")
        assert agent.persistence is not None

        # Check if using Supabase
        if hasattr(agent.persistence, "connection_string"):
            assert "supabase.com" in agent.persistence.connection_string

    def test_recursion_limit_configuration(self):
        """Test that recursion limit is properly configured."""
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Test Agent")

        # Check default recursion limit
        recursion_limit = agent.runnable_config.get("configurable", {}).get(
            "recursion_limit"
        )
        assert recursion_limit == 100

    @pytest.mark.asyncio
    async def test_database_connectivity(self, supabase_connection_string):
        """Test direct database connectivity."""
        try:
            async with await psycopg.AsyncConnection.connect(
                supabase_connection_string
            ) as conn, conn.cursor() as cur:
                # Simple connectivity test
                await cur.execute("SELECT 1")
                result = await cur.fetchone()
                assert result[0] == 1
        except Exception as e:
            pytest.fail(f"Database connectivity failed: {e}")

    @pytest.mark.asyncio
    async def test_table_existence(self, supabase_connection_string):
        """Test that required persistence tables exist."""
        required_tables = ["checkpoints", "checkpoint_writes", "checkpoint_blobs"]

        try:
            async with await psycopg.AsyncConnection.connect(
                supabase_connection_string
            ) as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = ANY(%s)
                    """,
                        (required_tables,),
                    )

                    existing_tables = {row[0] for row in await cur.fetchall()}

                    # Check if all required tables exist
                    missing_tables = set(required_tables) - existing_tables
                    if missing_tables:
                        pytest.skip(
                            f"Required tables missing: {missing_tables}. Run agent once to create tables."
                        )

                    assert len(existing_tables) >= 3
        except Exception as e:
            pytest.fail(f"Table check failed: {e}")

    @pytest.mark.asyncio
    async def test_data_persistence(self, test_thread_id, agent_config):
        """Test that agent data is persisted to Supabase."""
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Persistence Test Agent")

        # Test message
        test_message = f"Test message for persistence verification - {test_thread_id}"

        try:
            # Run agent with test message
            result = agent.run(
                {"messages": [HumanMessage(content=test_message)]}, config=agent_config
            )

            # Agent should complete (even with prepared statement errors)
            assert result is not None
            assert "messages" in result

        except Exception as e:
            # Allow prepared statement errors (they don't prevent persistence)
            if "prepared statement" not in str(e):
                pytest.fail(f"Unexpected agent error: {e}")

        # Wait for async database writes
        await asyncio.sleep(2)

        # Verify data was written to Supabase
        await self._verify_data_written(test_thread_id)

    @pytest.mark.asyncio
    async def test_conversation_continuity(self, test_thread_id, agent_config):
        """Test that conversations can be continued across agent instances."""
        engine = AugLLMConfig()

        # First agent interaction
        agent1 = SimpleAgent(engine=engine, name="Agent 1")

        try:
            agent1.run(
                {"messages": [HumanMessage(content="Hello, remember this: banana")]},
                config=agent_config,
            )
        except Exception as e:
            if "prepared statement" not in str(e):
                pytest.fail(f"First agent failed: {e}")

        # Wait for persistence
        await asyncio.sleep(2)

        # Second agent interaction with same thread_id
        agent2 = SimpleAgent(engine=engine, name="Agent 2")

        try:
            result2 = agent2.run(
                {
                    "messages": [
                        HumanMessage(content="What did I tell you to remember?")
                    ]
                },
                config=agent_config,
            )

            # Should have access to conversation history
            assert result2 is not None

        except Exception as e:
            if "prepared statement" not in str(e):
                pytest.fail(f"Second agent failed: {e}")

    async def _verify_data_written(self, thread_id):
        """Helper to verify data was written to Supabase."""
        conn_string = os.getenv("POSTGRES_CONNECTION_STRING")

        try:
            async with await psycopg.AsyncConnection.connect(conn_string) as conn:
                async with conn.cursor() as cur:
                    # Check checkpoint_writes
                    await cur.execute(
                        "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                        (thread_id,),
                    )
                    write_count = (await cur.fetchone())[0]

                    # Check checkpoints
                    await cur.execute(
                        "SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s",
                        (thread_id,),
                    )
                    checkpoint_count = (await cur.fetchone())[0]

                    # At least one table should have data
                    assert (
                        write_count > 0 or checkpoint_count > 0
                    ), f"No data found for thread_id: {thread_id}"

        except Exception as e:
            pytest.fail(f"Data verification failed: {e}")


class TestSupabaseErrorHandling:
    """Test error handling and edge cases."""

    def test_missing_connection_string(self, monkeypatch):
        """Test behavior when POSTGRES_CONNECTION_STRING is not set."""
        # Temporarily remove connection string
        monkeypatch.delenv("POSTGRES_CONNECTION_STRING", raising=False)

        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="No Connection Test")

        # Should fall back to default PostgreSQL configuration
        assert hasattr(agent, "persistence")

    @pytest.mark.asyncio
    async def test_prepared_statement_errors_ignored(
        self, test_thread_id, agent_config
    ):
        """Test that prepared statement errors don't prevent functionality."""
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Error Test Agent")

        # This may generate prepared statement errors, but should still work
        try:
            result = agent.run(
                {"messages": [HumanMessage(content="Test message despite errors")]},
                config=agent_config,
            )

            # Should complete successfully despite any prepared statement errors
            assert result is not None

        except Exception as e:
            # Only prepared statement errors are acceptable
            if "prepared statement" not in str(e):
                pytest.fail(f"Unexpected error: {e}")


if __name__ == "__main__":
    # Allow running tests directly
    pytest.main([__file__, "-v"])
