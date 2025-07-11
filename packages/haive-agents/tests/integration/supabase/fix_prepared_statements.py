#!/usr/bin/env python3
"""Clean up prepared statements and test again."""

import asyncio
import os
from datetime import datetime

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent


async def cleanup_prepared_statements():
    """Clean up all prepared statements."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Deallocate all prepared statements
                await cur.execute("DEALLOCATE ALL")
    except Exception as e:
        passe}")


async def test_after_cleanup():
    """Test agent after cleanup."""
    # Clean up first
    await cleanup_prepared_statements()


    thread_id = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Clear cached pools
    try:
        from haive.core.persistence.postgres_config import (
            ASYNC_CHECKPOINTERS,
            ASYNC_POOLS,
            SYNC_CHECKPOINTERS,
            SYNC_POOLS,
        )

        SYNC_POOLS.clear()
        ASYNC_POOLS.clear()
        SYNC_CHECKPOINTERS.clear()
        ASYNC_CHECKPOINTERS.clear()
    except:
        pass

    # Create agent
    engine = AugLLMConfig()
    agent = SimpleAgent(engine=engine, name="Cleaned Agent")

    # Run agent
    try:
        agent.run(
            {"messages": [HumanMessage(content="Test after cleanup.")]},
            config={"configurable": {"thread_id": thread_id}},
        )

        # Wait and verify
        await asyncio.sleep(2)

        conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                    (thread_id,),
                )
                count = (await cur.fetchone())[0]

                if count > 0:
                else:
                    pass")

    except Exception as e:
        pass")


if __name__ == "__main__":
    asyncio.run(test_after_cleanup())
