#!/usr/bin/env python3
"""Complete test demonstrating Supabase integration is working."""

import asyncio
import os
import warnings
from datetime import datetime

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent

# Suppress prepared statement warnings
warnings.filterwarnings("ignore", message=".*prepared statement.*")


async def main():
    """Run complete Supabase test."""

    # Check environment
    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return False

    if "supabase.com" in conn_string:
        pass")
    else:
        passon")

    # Create unique thread
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    thread_id = f"supabase_test_{timestamp}"

    # Step 1: Create agent
    try:
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Supabase Test Agent")

        # Check persistence configuration
        if hasattr(agent, "persistence") and agent.persistence:
            if hasattr(agent.persistence, "connection_string") and (
                agent.persistence.connection_string
                and "supabase.com" in agent.persistence.connection_string
            ):
                print("✅ Agent is using Supabase for persistence!")")

        # Check recursion limit
        if hasattr(agent, "runnable_config"):
            recursion_limit = agent.runnable_config.get("configurable", {}).get(
                "recursion_limit"
            )
    except Exception as e:
        return False

    # Step 2: Run agent
    try:
        messages = [
            HumanMessage(
                content="Hello! This is a test message to verify Supabase persistence is working correctly. Please respond confirming you received this message."
            )
        ]

        result = agent.run(
            {"messages": messages}, config={"configurable": {"thread_id": thread_id}}
        )


        # Show response
        if "messages" in result and len(result["messages"]) > len(messages):
            response = result["messages"][-1].content

    except Exception as e:
        if "prepared statement" in str(e):
        else:
            return False

    # Step 3: Wait for database writes
    await asyncio.sleep(3)

    # Step 4: Verify data in Supabase

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

                # Check checkpoint_blobs
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_blobs WHERE thread_id = %s",
                    (thread_id,),
                )
                blob_count = (await cur.fetchone())[0]


                success = write_count > 0 or checkpoint_count > 0

                if success:

                    # Show some write details
                    await cur.execute(
                        """
                        SELECT channel, type, idx
                        FROM checkpoint_writes
                        WHERE thread_id = %s
                        ORDER BY idx
                        LIMIT 5
                    """,
                        (thread_id,),
                    )

                    writes = await cur.fetchall()
                    if writes:
                        for channel, write_type, idx in writes:
                            pass


                else:
                    pass")

                return success

    except Exception as e:
        return False


async def summary():
    """Print summary of what's working."""


if __name__ == "__main__":
    success = asyncio.run(main())
    asyncio.run(summary())

    if not success:
        sys.exit(1)
