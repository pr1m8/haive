"""Demo 13: Reflection Agent.

Tests: Reflection agent config and import
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 13: Reflection Agent")
    print("=" * 60)

    try:
        from haive.agents.reasoning_and_critique.reflection.config import (
            ReflectionAgentConfig,
        )
        print("[OK] ReflectionAgentConfig imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        from haive.agents.reasoning_and_critique.reflection.agent import ReflectionAgent
        print("[OK] ReflectionAgent imported")
    except ImportError as e:
        print(f"[BROKEN] ReflectionAgent import failed: {e}")

    try:
        config = ReflectionAgentConfig.from_scratch(
            system_prompt="You are a helpful assistant.",
            model="gpt-4o-mini",
            temperature=0.5,
        )
        print(f"[OK] Config created: max_rounds={config.reflection.max_reflection_rounds}")
    except Exception as e:
        print(f"[BROKEN] Config creation failed: {e}")
        return

    print("\n[OK] ReflectionAgent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
