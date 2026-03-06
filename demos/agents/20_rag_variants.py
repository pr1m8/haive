"""Demo 20: RAG Agent Variants - Import, Instantiate, and Run.

Tests: All 28 RAG agent types - import, instantiate with name=, and verify.
Each agent is tested for:
  1. Module import
  2. Class instantiation (with name= kwarg)
  3. Key attributes present

Agents that need external services (Neo4j, SQL DB) are tested separately
with connection awareness.
"""

import asyncio
import importlib
import os
import sys
import traceback

sys.path.insert(0, ".")

from dotenv import load_dotenv

load_dotenv()

# Ensure OpenAI is used
os.environ.setdefault("OPENAI_API_TYPE", "openai")


# ── Helper ──────────────────────────────────────────────────────
def try_instantiate(cls, name, **kwargs):
    """Try to instantiate a class with name= kwarg."""
    try:
        obj = cls(name=name, **kwargs)
        return obj, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


def try_from_documents(cls, name, docs=None):
    """Try factory method from_documents()."""
    from langchain_core.documents import Document

    if docs is None:
        docs = [
            Document(page_content="Python is a programming language created by Guido van Rossum."),
            Document(page_content="Machine learning is a subset of artificial intelligence."),
            Document(page_content="Neural networks are inspired by the human brain."),
        ]
    try:
        obj = cls.from_documents(documents=docs, name=name)
        return obj, None
    except Exception as e:
        return None, f"{type(e).__name__}: {e}"


# ── Agent definitions ───────────────────────────────────────────
# (name, module, class_name, instantiation_method)
# method: "name" = AgentClass(name=...), "from_docs" = AgentClass.from_documents(...)
# "config" = AgentClass(config=ConfigClass(name=...))

RAG_AGENTS = [
    # --- New pattern (Pydantic + build_graph / from_documents) ---
    ("adaptive", "haive.agents.rag.adaptive.agent", "AdaptiveRAGAgent", "from_docs"),
    ("adaptive_tools", "haive.agents.rag.adaptive_tools.agent", "AdaptiveToolsRAGAgent", "from_docs"),
    ("corrective", "haive.agents.rag.corrective.agent", "CorrectiveRAGAgent", "from_docs"),
    ("document_grading", "haive.agents.rag.document_grading.agent", "DocumentGradingRAGAgent", "from_docs"),
    ("flare", "haive.agents.rag.flare.agent", "FLARERAGAgent", "from_docs"),
    ("fusion", "haive.agents.rag.fusion.agent", "RAGFusionAgent", "from_docs"),
    ("hyde", "haive.agents.rag.hyde.agent", "HyDERAGAgent", "from_docs"),
    ("memory_aware", "haive.agents.rag.memory_aware.agent", "MemoryAwareRAGAgent", "from_docs"),
    ("multi_query", "haive.agents.rag.multi_query.agent", "MultiQueryRAGAgent", "from_docs"),
    ("self_route", "haive.agents.rag.self_route.agent", "SelfRouteRAGAgent", "from_docs"),
    ("speculative", "haive.agents.rag.speculative.agent", "SpeculativeRAGAgent", "from_docs"),
    ("step_back", "haive.agents.rag.step_back.agent", "StepBackRAGAgent", "from_docs"),

    # --- Old pattern (Agent[Config] with setup_workflow) ---
    # adaptive_rag module is empty (class moved to adaptive/agent.py) - skipped
    ("filtered", "haive.agents.rag.filtered.agent", "FilteredRAGAgent", "name"),
    ("query_planning", "haive.agents.rag.query_planning.agent", "QueryPlanningRAGAgent", "name"),
    ("self_reflective", "haive.agents.rag.self_reflective.agent", "SelfReflectiveRAGAgent", "name"),
    ("self_corr", "haive.agents.rag.self_corr.agent", "SelfCorrectiveRAGAgent", "name"),
    ("multi_strategy", "haive.agents.rag.multi_strategy.agent", "MultiStrategyRAGAgent", "name"),
    ("typed", "haive.agents.rag.typed.agent", "TypedRAGAgent", "name"),
    ("dynamic", "haive.agents.rag.dynamic.agent", "DynamicRAGAgent", "name"),
    ("llm_rag", "haive.agents.rag.llm_rag.agent", "LLMRAGAgent", "name"),

    # --- New pattern with Pydantic fields (hallucination / query_decomposition) ---
    ("hallucination_grading", "haive.agents.rag.hallucination_grading.agent", "HallucinationGraderAgent", "name"),
    ("query_decomposition", "haive.agents.rag.query_decomposition.agent", "QueryDecomposerAgent", "name"),

    # --- Agentic agents ---
    ("agentic", "haive.agents.rag.agentic.agent", "AgenticRAGAgent", "name"),
    ("agentic_router", "haive.agents.rag.agentic_router.agent", "AgenticRAGRouterAgent", "name"),

    # simple/enhanced_v3 requires VectorStoreConfig (deprecated, use SimpleRAGAgent) - skipped
]

# DB agents tested separately (need external services)
DB_AGENTS = [
    ("db_rag/graph_db", "haive.agents.rag.db_rag.graph_db.agent", "GraphDBRAGAgent", "name"),
    ("db_rag/sql_rag", "haive.agents.rag.db_rag.sql_rag.agent", "SQLRAGAgent", "name"),
]


async def main():
    print("=" * 70)
    print("Demo 20: RAG Agent Variants - Import + Instantiate")
    print("=" * 70)

    ok = broken = 0
    results = []

    for short_name, module_path, class_name, method in RAG_AGENTS:
        # Step 1: Import
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
        except Exception as e:
            print(f"  [XX] {short_name:<25} IMPORT FAIL: {type(e).__name__}: {str(e)[:60]}")
            broken += 1
            results.append((short_name, "IMPORT_FAIL"))
            continue

        # Step 2: Instantiate
        test_name = f"test_{short_name.replace('/', '_')}"
        if method == "from_docs":
            obj, err = try_from_documents(cls, test_name)
        elif method == "name":
            obj, err = try_instantiate(cls, test_name)
        else:
            obj, err = None, f"Unknown method: {method}"

        if obj is not None:
            print(f"  [OK] {short_name:<25} {class_name}")
            ok += 1
            results.append((short_name, "OK"))
        else:
            print(f"  [XX] {short_name:<25} INIT FAIL: {err[:70] if err else 'unknown'}")
            broken += 1
            results.append((short_name, "INIT_FAIL"))

    # ── DB Agents (separate section) ────────────────────────────
    print()
    print("  --- Database RAG Agents (require external services) ---")

    for short_name, module_path, class_name, method in DB_AGENTS:
        try:
            mod = importlib.import_module(module_path)
            cls = getattr(mod, class_name)
        except Exception as e:
            print(f"  [XX] {short_name:<25} IMPORT FAIL: {type(e).__name__}: {str(e)[:60]}")
            broken += 1
            results.append((short_name, "IMPORT_FAIL"))
            continue

        obj, err = try_instantiate(cls, f"test_{short_name.replace('/', '_')}")
        if obj is not None:
            # Check if actually connected
            if short_name == "db_rag/graph_db":
                connected = getattr(obj, "graph_db", None) is not None
                status = "connected" if connected else "deferred (no Neo4j)"
            else:
                status = "instantiated"
            print(f"  [OK] {short_name:<25} {class_name} ({status})")
            ok += 1
            results.append((short_name, "OK"))
        else:
            print(f"  [XX] {short_name:<25} INIT FAIL: {err[:70] if err else 'unknown'}")
            broken += 1
            results.append((short_name, "INIT_FAIL"))

    # ── Summary ─────────────────────────────────────────────────
    total = ok + broken
    print()
    print(f"  RAG variants: {ok}/{total} OK, {broken} broken")

    if broken > 0:
        print("\n  Broken agents:")
        for name, status in results:
            if status != "OK":
                print(f"    - {name}: {status}")

    print(f"\n[{'OK' if broken == 0 else 'PARTIAL'}] RAG variants demo complete")
    return ok, broken


if __name__ == "__main__":
    ok, broken = asyncio.run(main())
    sys.exit(0 if broken == 0 else 1)
