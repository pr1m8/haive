"""Demo 12: Self-Discover SelectorAgent.

Tests: Self-discover reasoning module selection
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig


async def main():
    print("=" * 60)
    print("Demo 12: Self-Discover SelectorAgent")
    print("=" * 60)

    try:
        from haive.agents.reasoning_and_critique.self_discover.selector import SelectorAgent
        print("[OK] SelectorAgent imported")
    except ImportError as e:
        print(f"[BROKEN] Import failed: {e}")
        return

    try:
        selector = SelectorAgent(
            name="selector_demo",
            engine=AugLLMConfig(temperature=0.3),
        )
        print(f"[OK] Instantiated: {selector.name}")
    except Exception as e:
        print(f"[BROKEN] Instantiation failed: {e}")
        return

    print("\n--- Running arun ---")
    try:
        result = await selector.arun({
            "available_modules": (
                "1. Critical Thinking\n"
                "2. Pattern Recognition\n"
                "3. Decomposition\n"
                "4. Analogical Reasoning\n"
                "5. Systems Thinking"
            ),
            "task_description": "Design a recommendation system for an e-commerce platform",
        })
        print(f"Result type: {type(result)}")
        print(f"Result: {str(result)[:300]}")
        print("\n[OK] SelectorAgent demo complete")
    except Exception as e:
        print(f"[BROKEN] arun failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())
