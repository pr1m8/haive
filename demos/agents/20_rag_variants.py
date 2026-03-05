"""Demo 20: RAG Agent Variants.

Tests: Import of all RAG agent types
"""

import asyncio
import importlib
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 20: RAG Agent Variants")
    print("=" * 60)

    rag_modules = [
        ("adaptive", "haive.agents.rag.adaptive.agent"),
        ("adaptive_rag", "haive.agents.rag.adaptive_rag.agent"),
        ("adaptive_tools", "haive.agents.rag.adaptive_tools.agent"),
        ("agentic", "haive.agents.rag.agentic.agent"),
        ("agentic_router", "haive.agents.rag.agentic_router.agent"),
        ("corrective", "haive.agents.rag.corrective.agent"),
        ("db_rag/graph_db", "haive.agents.rag.db_rag.graph_db.agent"),
        ("db_rag/sql_rag", "haive.agents.rag.db_rag.sql_rag.agent"),
        ("document_grading", "haive.agents.rag.document_grading.agent"),
        ("dynamic", "haive.agents.rag.dynamic.agent"),
        ("filtered", "haive.agents.rag.filtered.agent"),
        ("flare", "haive.agents.rag.flare.agent"),
        ("fusion", "haive.agents.rag.fusion.agent"),
        ("hallucination_grading", "haive.agents.rag.hallucination_grading.agent"),
        ("hyde", "haive.agents.rag.hyde.agent"),
        ("llm_rag", "haive.agents.rag.llm_rag.agent"),
        ("memory_aware", "haive.agents.rag.memory_aware.agent"),
        ("multi_query", "haive.agents.rag.multi_query.agent"),
        ("multi_strategy", "haive.agents.rag.multi_strategy.agent"),
        ("query_decomposition", "haive.agents.rag.query_decomposition.agent"),
        ("query_planning", "haive.agents.rag.query_planning.agent"),
        ("self_corr", "haive.agents.rag.self_corr.agent"),
        ("self_reflective", "haive.agents.rag.self_reflective.agent"),
        ("self_route", "haive.agents.rag.self_route.agent"),
        ("simple/enhanced_v3", "haive.agents.rag.simple.enhanced_v3.agent"),
        ("speculative", "haive.agents.rag.speculative.agent"),
        ("step_back", "haive.agents.rag.step_back.agent"),
        ("typed", "haive.agents.rag.typed.agent"),
    ]

    ok = broken = 0
    for name, module_path in rag_modules:
        try:
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if "Agent" in c and not c.startswith("_")]
            print(f"  [OK] {name:<25} {classes[:2]}")
            ok += 1
        except Exception as e:
            print(f"  [XX] {name:<25} {type(e).__name__}: {str(e)[:60]}")
            broken += 1

    print(f"\n  RAG variants: {ok}/{ok+broken} OK")
    print("\n[OK] RAG variants demo complete")


if __name__ == "__main__":
    asyncio.run(main())
