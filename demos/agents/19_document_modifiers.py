"""Demo 19: Document Modifier Agents.

Tests: Summarizer, KG, TNT, ComplexExtraction
"""
import asyncio
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

async def main():
    print("=" * 60)
    print("Demo 19: Document Modifier Agents")
    print("=" * 60)

    modules = [
        "haive.agents.document_modifiers.summarizer.iterative_refinement.agent",
        "haive.agents.document_modifiers.summarizer.map_branch.agent",
        "haive.agents.document_modifiers.kg.kg_iterative_refinement.agent",
        "haive.agents.document_modifiers.kg.kg_map_merge.agent",
        "haive.agents.document_modifiers.tnt.agent",
        "haive.agents.document_modifiers.complex_extraction.agent",
    ]

    for module_path in modules:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            classes = [c for c in dir(mod) if not c.startswith("_") and c[0].isupper()]
            print(f"[OK] {module_path.split('.')[-2]}/{module_path.split('.')[-1]} - {classes[:3]}")
        except Exception as e:
            print(f"[BROKEN] {module_path.split('.')[-2]}: {type(e).__name__}: {str(e)[:80]}")

    print("\n[OK] Document modifier agents demo complete")

if __name__ == "__main__":
    asyncio.run(main())
