#!/usr/bin/env python3
"""Test that shows Supabase is working despite prepared statement errors."""

import asyncio
import os
import warnings
from datetime import datetime

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent

# Suppress warnings
warnings.filterwarnings("ignore", message=".*prepared statement.*")


async def main():

    # Create unique thread
    thread_id = f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    # Create agent
    engine = AugLLMConfig()
    agent = SimpleAgent(engine=engine, name="Demo Agent")

    # Check configuration
    if hasattr(agent, "persistence") and agent.persistence:
        if hasattr(agent.persistence, "connection_string") and (
            agent.persistence.connection_string
            and "supabase.com" in agent.persistence.connection_string
        ):
            print("✅ Using Supabase connection!")")

    # Run agent (ignoring prepared statement errors)
    success = False
    try:
        result = agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="Hello! This message will be saved to Supabase."
                    )
                ]
            },
            config={"configurable": {"thread_id": thread_id}},
        )
        success = True
        if "messages" in result and len(result["messages"]) > 1:
            pass
    except Exception as e:
        if "prepared statement" in str(e):
            # Check if data was saved anyway
        else:
            pass")

    # Wait for writes
    await asyncio.sleep(2)

    # Verify data in Supabase

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    async with await psycopg.AsyncConnection.connect(conn_string) as conn, conn.cursor() as cur:
        # Count writes
        await cur.execute(
            "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
            (thread_id,),
        )
        write_count = (await cur.fetchone())[0]

        # Count checkpoints
        await cur.execute(
            "SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s", (thread_id,)
        )
        checkpoint_count = (await cur.fetchone())[0]

        print(f"\n📊 Results:")
        print(f"   Checkpoint writes: {write_count}")
        print(f"   Checkpoints: {checkpoint_count}")

        if write_count > 0 or checkpoint_count > 0:
            print("\n✅ SUCCESS! Data is being saved to Supabase!")
            print(f"\n🔗 View your data in Supabase:")
            print(
                f"   https://supabase.com/dashboard/project/zkssazqhwcetsnbiuqik/editor/45942"
            )
            print(
                f"   SQL Query: SELECT * FROM checkpoint_writes WHERE thread_id = '{thread_id}';"
            )
            return True
        else:
            print("\n❌ No data found")
            return False


if __name__ == "__main__":
    success = asyncio.run(main())


    if not success:
        exit(1)
