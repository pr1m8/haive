"""Run all demos and report status.

Usage: poetry run python demos/run_all.py [--dry-run] [--agents-only] [--filter PATTERN]
"""

import asyncio
import importlib
import os
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


DEMO_ORDER = [
    # Priority 1: Core agents
    "agents/01_simple_agent",
    "agents/02_structured_output",
    "agents/03_react_agent",
    "agents/04_multi_sequential",
    "agents/05_multi_parallel",
    "agents/06_dynamic_supervisor",
    "agents/07_supervisor",
    # Priority 2: Specialized agents
    "agents/08_rag_agent",
    "agents/09_planner",
    "agents/10_plan_and_execute",
    "agents/11_structured_output_agent",
    "agents/12_self_discover",
    "agents/13_reflection",
    # Priority 3: Extended agents (import tests)
    "agents/17_conversation",
    "agents/18_document_loader",
    "agents/19_document_modifiers",
    "agents/20_rag_variants",
    "agents/21_reasoning",
    "agents/22_research",
    "agents/23_memory",
    "agents/24_planning_variants",
    # Priority 4: Games
    "games/14_chess",
    "games/15_go",
    "games/25_board_games",
    "games/26_card_games",
    "games/27_single_player",
    # Priority 5: Integrations
    "integrations/16_mcp_agent",
]


async def run_demo(demo_path: str, dry_run: bool = False) -> dict:
    """Run a single demo and capture result."""
    result = {"name": demo_path, "status": "UNKNOWN", "time": 0, "error": None}
    demo_dir = Path(__file__).parent

    module_path = demo_dir / f"{demo_path}.py"
    if not module_path.exists():
        result["status"] = "MISSING"
        result["error"] = f"File not found: {module_path}"
        return result

    if dry_run:
        result["status"] = "SKIP (dry-run)"
        return result

    start = time.time()
    try:
        # Import and run the demo's main function
        spec = importlib.util.spec_from_file_location(
            demo_path.replace("/", "."), str(module_path)
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "main"):
            await module.main()
            result["status"] = "OK"
        else:
            result["status"] = "BROKEN"
            result["error"] = "No main() function"
    except Exception as e:
        result["status"] = "BROKEN"
        result["error"] = f"{type(e).__name__}: {e}"
        traceback.print_exc()
    finally:
        result["time"] = time.time() - start

    return result


async def main():
    dry_run = "--dry-run" in sys.argv
    agents_only = "--agents-only" in sys.argv
    filter_pattern = None
    if "--filter" in sys.argv:
        idx = sys.argv.index("--filter")
        if idx + 1 < len(sys.argv):
            filter_pattern = sys.argv[idx + 1]

    demos = DEMO_ORDER
    if agents_only:
        demos = [d for d in demos if d.startswith("agents/")]
    if filter_pattern:
        demos = [d for d in demos if filter_pattern in d]

    print("=" * 70)
    print(f"  HAIVE DEMOS RUNNER  {'(DRY RUN)' if dry_run else ''}")
    print(f"  Running {len(demos)} demos")
    print("=" * 70)

    results = []
    for demo_path in demos:
        print(f"\n{'─' * 70}")
        print(f"  Running: {demo_path}")
        print(f"{'─' * 70}")
        result = await run_demo(demo_path, dry_run)
        results.append(result)

    # Summary
    print("\n")
    print("=" * 70)
    print("  RESULTS SUMMARY")
    print("=" * 70)

    ok = [r for r in results if r["status"] == "OK"]
    broken = [r for r in results if r["status"] == "BROKEN"]
    other = [r for r in results if r["status"] not in ("OK", "BROKEN")]

    for r in results:
        icon = "OK" if r["status"] == "OK" else "XX" if r["status"] == "BROKEN" else "--"
        time_str = f"{r['time']:.1f}s" if r["time"] > 0 else ""
        error_str = f" | {r['error']}" if r["error"] else ""
        print(f"  [{icon}] {r['name']:<40} {time_str:>6}{error_str}")

    print(f"\n  Passed: {len(ok)}/{len(results)}")
    if broken:
        print(f"  Broken: {len(broken)}")
        for r in broken:
            print(f"    - {r['name']}: {r['error']}")
    if other:
        print(f"  Other:  {len(other)}")

    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
