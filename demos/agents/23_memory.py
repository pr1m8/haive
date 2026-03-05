"""Demo 23: Memory Agents.

Tests: Memory system agents (long_term_memory, ltm, memory, memory_reorganized)
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 23: Memory Agents")
    print("=" * 60)

    memory_modules = [
        ("long_term_memory", "haive.agents.long_term_memory.agent"),
        ("ltm", "haive.agents.ltm.agent"),
        ("memory", "haive.agents.memory.agent"),
        ("memory/quick_search", "haive.agents.memory.search.quick_search.agent"),
        ("memory/pro_search", "haive.agents.memory.search.pro_search.agent"),
        ("memory/deep_research", "haive.agents.memory.search.deep_research.agent"),
        ("memory_reorg/base", "haive.agents.memory_reorganized.base.agent"),
    ]

    ok = broken = 0
    for name, module_path in memory_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c or "Memory" in c]
            print(f"  [OK] {name:<25} {[c for c in classes if not c.startswith('_')][:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<25} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  Memory agents: {ok}/{ok+broken} OK")
    print("\n[OK] Memory agents demo complete")


if __name__ == "__main__":
    asyncio.run(main())
