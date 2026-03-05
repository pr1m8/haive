"""Demo 21: Reasoning & Critique Agents.

Tests: LATS, Logic, MCTS, Reflexion, ToT (Tree of Thought)
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 21: Reasoning & Critique Agents")
    print("=" * 60)

    reasoning_modules = [
        ("lats", "haive.agents.reasoning_and_critique.lats.agent"),
        ("logic", "haive.agents.reasoning_and_critique.logic.agent"),
        ("mcts", "haive.agents.reasoning_and_critique.mcts.agent"),
        ("reflection", "haive.agents.reasoning_and_critique.reflection.agent"),
        ("reflexion", "haive.agents.reasoning_and_critique.reflexion.agent"),
        ("self_discover", "haive.agents.reasoning_and_critique.self_discover.agent"),
        ("self_discover/adapter", "haive.agents.reasoning_and_critique.self_discover.adapter.agent"),
        ("self_discover/executor", "haive.agents.reasoning_and_critique.self_discover.executor.agent"),
        ("self_discover/selector", "haive.agents.reasoning_and_critique.self_discover.selector.agent"),
        ("self_discover/structurer", "haive.agents.reasoning_and_critique.self_discover.structurer.agent"),
        ("tot", "haive.agents.reasoning_and_critique.tot.agent"),
    ]

    ok = broken = 0
    for name, module_path in reasoning_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c and not c.startswith("_")]
            print(f"  [OK] {name:<20} {classes[:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<20} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  Reasoning agents: {ok}/{ok+broken} OK")
    print("\n[OK] Reasoning agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
