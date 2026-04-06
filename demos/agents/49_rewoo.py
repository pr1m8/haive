"""Demo 49: ReWOO Agent.

Tests: ReWOO - Reasoning WithOut Observation
Plans all steps upfront, executes in parallel, synthesizes answer.
Only 2 LLM calls total (plan + solve).
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 49: ReWOO - Reasoning WithOut Observation")
    print("=" * 60)

    from haive.agents.planning.rewoo.agent import ReWOOAgent

    agent = ReWOOAgent(name="rewoo_demo", tools=[])
    print(f"[OK] Created: {type(agent).__name__}")

    g = agent.compile()
    print(f"[OK] Compiled: {type(g).__name__}")
    print(f"[OK] Nodes: {list(g.get_graph().nodes.keys())}")

    print("\n[OK] ReWOO demo complete")


if __name__ == "__main__":
    asyncio.run(main())
