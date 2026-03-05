"""Demo 18: Document Loader Agents.

Tests: DocumentLoaderAgent variants
"""
import asyncio
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

async def main():
    print("=" * 60)
    print("Demo 18: Document Loader Agents")
    print("=" * 60)

    agents = [
        ("BaseDocumentLoaderAgent", "haive.agents.document_loader.base.agent"),
        ("DirectoryDocumentLoaderAgent", "haive.agents.document_loader.directory.agent"),
        ("FileDocumentLoaderAgent", "haive.agents.document_loader.file.agent"),
        ("WebDocumentLoaderAgent", "haive.agents.document_loader.web.agent"),
    ]

    for name, module_path in agents:
        try:
            import importlib
            mod = importlib.import_module(module_path)
            # Find the first class that looks like an agent
            classes = [c for c in dir(mod) if "Agent" in c or "Loader" in c]
            if classes:
                print(f"[OK] {module_path} imported - classes: {classes[:3]}")
            else:
                print(f"[OK] {module_path} imported (no Agent class found)")
        except Exception as e:
            print(f"[BROKEN] {module_path}: {type(e).__name__}: {str(e)[:80]}")

    print("\n[OK] Document loader agents demo complete")

if __name__ == "__main__":
    asyncio.run(main())
