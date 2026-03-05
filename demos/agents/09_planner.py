"""Demo 09: BasePlannerAgent.

Tests: Strategic planning agent
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.planning.base.agents.planner import BasePlannerAgent


async def main():
    print("=" * 60)
    print("Demo 09: BasePlannerAgent")
    print("=" * 60)

    planner = BasePlannerAgent(name="planner_demo")
    print(f"[OK] Instantiated: {planner.name}")

    print("\n--- Running arun ---")
    try:
        result = await planner.arun({
            "objective": "Create a simple Python CLI tool",
            "available_tools": "Python, pip, click library",
            "time_constraints": "1 day",
            "complexity_level": "low",
            "domain_focus": "software development",
            "additional_context": "For personal use, no need for tests initially",
        })
        print(f"Result type: {type(result)}")
        print(f"Result: {str(result)[:400]}")
        print("\n[OK] BasePlannerAgent demo complete")
    except Exception as e:
        print(f"[BROKEN] arun failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
