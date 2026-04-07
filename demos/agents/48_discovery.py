"""Demo 48: Discovery Agent.

Tests: Discovery agent for exploring and cataloging agent capabilities
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 48: Discovery Agent")
    print("=" * 60)

    import haive.agents.discovery as disc
    classes = [c for c in dir(disc) if not c.startswith("_")]
    print(f"[OK] Discovery module: {classes[:5]}")
    print("\n[OK] Discovery demo complete")


if __name__ == "__main__":
    asyncio.run(main())
