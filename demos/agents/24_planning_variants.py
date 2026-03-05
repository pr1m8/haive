"""Demo 24: Planning Agent Variants.

Tests: LLM Compiler, ReWOO, Plan-Execute V3
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 24: Planning Agent Variants")
    print("=" * 60)

    planning_modules = [
        ("llm_compiler", "haive.agents.planning.llm_compiler.agent"),
        ("llm_compiler_v3", "haive.agents.planning.llm_compiler_v3.agent"),
        ("plan_and_execute", "haive.agents.planning.plan_and_execute.agent"),
        ("plan_and_execute/v2", "haive.agents.planning.plan_and_execute.v2.agent"),
        ("plan_execute_v3", "haive.agents.planning.plan_execute_v3.agent"),
        ("rewoo_v3", "haive.agents.planning.rewoo_v3.agent"),
        ("p_and_e", "haive.agents.planning.p_and_e.agent"),
    ]

    ok = broken = 0
    for name, module_path in planning_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c or "Planner" in c or "Compiler" in c]
            print(f"  [OK] {name:<25} {[c for c in classes if not c.startswith('_')][:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<25} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  Planning variants: {ok}/{ok+broken} OK")
    print("\n[OK] Planning variants demo complete")


if __name__ == "__main__":
    asyncio.run(main())
