#!/usr/bin/env python3
"""Test in a fresh process to avoid prepared statement issues."""

import os
import subprocess
import sys

# Create the actual test script
test_script = """
import os
import asyncio
from datetime import datetime
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
import psycopg

async def run_test():
    thread_id = f"fresh_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    print(f"Thread ID: {thread_id}")

    # Create and run agent
    try:
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Fresh Test")

        result = agent.run(
            {'messages': [HumanMessage(content="Test message for Supabase.")]},
            config={'configurable': {'thread_id': thread_id}}
        )
        print("✅ Agent completed")
    except Exception as e:
        print(f"❌ Agent error: {e}")
        return None

    # Wait and check
    await asyncio.sleep(2)

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    async with await psycopg.AsyncConnection.connect(conn_string) as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                (thread_id,)
            )
            count = (await cur.fetchone())[0]
            print(f"Checkpoint writes: {count}")
            return thread_id if count > 0 else None

result = asyncio.run(run_test())
if result:
    print(f"✅ SUCCESS! Data written for thread: {result}")
else:
    print("❌ FAILED")
"""

# Write test script
with open("_temp_test.py", "w") as f:
    f.write(test_script)


# Run in subprocess
try:
    result = subprocess.run(
        [sys.executable, "_temp_test.py"],
        check=False, capture_output=True,
        text=True,
        env={**os.environ},
    )


    if result.stderr and "prepared statement" not in result.stderr:

    # Clean up
    os.remove("_temp_test.py")

except Exception as e:
    pass
