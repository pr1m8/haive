"""Demo 10: PlanAndExecuteAgent.

Tests: Plan and Execute agent pattern (V2 - newer pattern)
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 10: PlanAndExecuteAgent")
    print("=" * 60)

    try:
        from haive.agents.planning.plan_and_execute.simple import PlanAndExecuteAgent
        print("[OK] PlanAndExecuteAgent (simple/v2) imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        agent = PlanAndExecuteAgent.create(name="demo_plan_execute")
        print(f"[OK] Instantiated via create()")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")
        return

    print("\n[OK] PlanAndExecuteAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
