"""Test SimpleAgent v2 with a simple query to identify the exact error."""

import asyncio

from haive.agents.simple.agent_v2 import SimpleAgentV2


try:
    # Create a simple agent without complex models
    agent = SimpleAgentV2(name="test_agent")

    # Try to run with a simple string input
    result = agent.run("Hello, what's 2+2?", debug=True)

except Exception:
    import traceback

    traceback.print_exc()
