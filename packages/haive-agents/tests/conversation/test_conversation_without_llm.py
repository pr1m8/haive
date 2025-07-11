#!/usr/bin/env python3
"""Comprehensive test suite for conversation persistence without expensive LLM calls."""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path


def setup_paths():
    """Add required paths for testing."""
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
    )
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src"
    )


async def test_async_postgresql_setup():
    """Test async PostgreSQL configuration and setup."""
    try:

        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
        from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

        connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
        if not connection_string:
            return False

        # Test async config creation
        config_id = id(None)  # Get a unique ID first
        async_config = PostgresCheckpointerConfig(
            connection_string=connection_string,
            mode=CheckpointerMode.ASYNC,  # Set to async mode
            storage_mode=CheckpointStorageMode.FULL,
            prepare_threshold=None,
            min_pool_size=1,
            max_pool_size=3,
            connection_kwargs={
                "prepare_threshold": None,
                "application_name": f"haive_async_test_{config_id}",
            },
        )


        # Test async checkpointer creation
        async_checkpointer = await async_config.create_async_checkpointer()

        # Test basic async operation
        from langgraph.checkpoint.base import empty_checkpoint

        test_checkpoint = empty_checkpoint()
        test_checkpoint["channel_values"] = {
            "async_test": f"working_{datetime.now().isoformat()}"
        }

        test_config = {
            "configurable": {
                "thread_id": f"async_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "checkpoint_ns": "",  # Required for LangGraph PostgreSQL checkpointer
            }
        }

        # This tests async save
        result = await async_checkpointer.aput(test_config, test_checkpoint, {}, {})

        # Close the connection pool properly
        if hasattr(async_checkpointer, "conn") and hasattr(
            async_checkpointer.conn, "close"
        ):
            await async_checkpointer.conn.close()

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_thread_continuation():
    """Test continuing conversations on existing thread IDs."""
    try:

        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.messages import HumanMessage

        from haive.agents.simple.agent import SimpleAgent

        # Create a simple agent with persistence
        agent = SimpleAgent(
            name="ContinuationTestAgent",
            system_message="You are a helpful assistant. Keep responses brief.",
            persistence=True,  # Enable persistence
        )

        agent.compile()

        # Test thread ID for continuation
        thread_id = f"continuation_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        config = {"configurable": {"thread_id": thread_id}}

        # First interaction
        first_input = {
            "messages": [HumanMessage(content="Hello, remember my name is TestUser")]
        }
        first_result = agent.invoke(first_input, config)

        # Second interaction on same thread - should have memory
        second_input = {"messages": [HumanMessage(content="What is my name?")]}
        second_result = agent.invoke(second_input, config)

        # Verify both results have messages
        if "messages" in first_result and "messages" in second_result:
            first_count = len(first_result["messages"])
            second_count = len(second_result["messages"])

            if second_count > first_count:
                return True
            print("⚠️  Thread continuation may not be working - same message count")
            return False
        else:
            return False

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_react_agent_persistence():
    """Test React agent with persistence and tool usage."""
    try:

        from haive.core.engine.aug_llm import AugLLMConfig
        from langchain_core.messages import HumanMessage

        from haive.agents.react.agent import ReactAgent

        # Create React agent with basic tools
        react_agent = ReactAgent(
            name="TestReactAgent",
            system_message="You are a helpful assistant with tools. Keep responses brief.",
            persistence=True,
        )

        react_agent.compile()

        # Test with simple input that doesn't require expensive tool calls
        thread_id = f"react_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        config = {"configurable": {"thread_id": thread_id}}

        test_input = {
            "messages": [HumanMessage(content="What tools do you have available?")]
        }
        result = react_agent.invoke(test_input, config)


        if "messages" in result:
            message_count = len(result["messages"])

            # Check for any errors in the response
            last_message = result["messages"][-1] if result["messages"] else None
            if last_message and hasattr(last_message, "content"):
                if "error" in str(last_message.content).lower():
                    passt}")
                else:
                    pass")

            return True
        print("❌ No messages in result")
        return False

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def check_database_health():
    """Check database connection and recent activity."""
    try:

        import psycopg2
        from psycopg2.extras import RealDictCursor

        conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
        if not conn_str:
            return False

        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Check recent activity
        cursor.execute(
            """
            SELECT
                COUNT(*) as total_checkpoints,
                COUNT(DISTINCT thread_id) as unique_threads,
                MAX(metadata->>'step') as max_step
            FROM checkpoints
            WHERE checkpoint_id::text > (
                SELECT checkpoint_id::text
                FROM checkpoints
                ORDER BY checkpoint_id::text DESC
                OFFSET 100 LIMIT 1
            );
        """
        )

        stats = cursor.fetchone()

        # Check for recent errors
        cursor.execute(
            """
            SELECT COUNT(*) as error_count
            FROM checkpoints
            WHERE checkpoint::text ILIKE '%error%'
            AND checkpoint_id::text > (
                SELECT checkpoint_id::text
                FROM checkpoints
                ORDER BY checkpoint_id::text DESC
                OFFSET 50 LIMIT 1
            );
        """
        )

        error_stats = cursor.fetchone()
        error_count = error_stats["error_count"]

        if error_count > 0:
            passse")
        else:
            pass")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        return False


def create_test_report(results):
    """Create a comprehensive test report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"/home/will/Projects/haive/backend/haive/persistence_test_report_{timestamp}.json"

    report = {
        "timestamp": datetime.now().isoformat(),
        "test_results": results,
        "summary": {
            "total_tests": len(results),
            "passed": sum(1 for r in results.values() if r),
            "failed": sum(1 for r in results.values() if not r),
        },
        "recommendations": [],
    }

    # Add recommendations based on results
    if not results.get("async_postgresql", False):
        report["recommendations"].append("Fix async PostgreSQL configuration")

    if not results.get("thread_continuation", False):
        report["recommendations"].append("Investigate thread continuation issues")

    if not results.get("react_agent", False):
        report["recommendations"].append("Check React agent persistence setup")

    if not results.get("database_health", False):
        report["recommendations"].append("Review database connection and health")

    # Save report
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)

    return report


async def main():
    """Run comprehensive persistence tests."""

    setup_paths()

    # Run all tests
    results = {}

    # Test 1: Async PostgreSQL
    results["async_postgresql"] = await test_async_postgresql_setup()

    # Test 2: Thread continuation
    results["thread_continuation"] = test_thread_continuation()

    # Test 3: React agent persistence
    results["react_agent"] = test_react_agent_persistence()

    # Test 4: Database health
    results["database_health"] = check_database_health()

    # Generate report
    create_test_report(results)

    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"

    overall_status = (
        "✅ ALL TESTS PASSED" if all(results.values()) else "⚠️  SOME TESTS FAILED"
    )

    if not all(results.values()):
        passs")


if __name__ == "__main__":
    asyncio.run(main())
