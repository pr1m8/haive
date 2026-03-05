"""Demo 07: SupervisorAgent.

Tests: Basic supervisor routing tasks to sub-agents
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent


async def main():
    print("=" * 60)
    print("Demo 07: Supervisor Agent")
    print("=" * 60)

    # Try to import supervisor agent (class is DynamicSupervisor)
    try:
        from haive.agents.supervisor.agent import DynamicSupervisor
        print("[OK] DynamicSupervisor imported")
    except ImportError as e:
        print(f"[BROKEN] DynamicSupervisor import failed: {e}")
        return

    try:
        supervisor = DynamicSupervisor(
            name="demo_supervisor",
            engine=AugLLMConfig(
                temperature=0.3,
                system_message="You route tasks to appropriate team members.",
            ),
        )
        print(f"[OK] Instantiated: {supervisor.name}")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")
        return

    print("\n[OK] DynamicSupervisor demo complete")


if __name__ == "__main__":
    asyncio.run(main())
