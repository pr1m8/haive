"""Demo 08: RAG Agent.

Tests: BaseRAGAgent and SimpleRAGAgent
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig


async def main():
    print("=" * 60)
    print("Demo 08: RAG Agent")
    print("=" * 60)

    # Test BaseRAGAgent
    try:
        from haive.agents.rag.base.agent import BaseRAGAgent
        print("[OK] BaseRAGAgent imported")
    except ImportError as e:
        print(f"[BROKEN] BaseRAGAgent import: {e}")
        return

    try:
        # BaseRAGAgent expects a retriever/vectorstore engine, not AugLLMConfig
        rag = BaseRAGAgent(name="rag_demo")  # uses default InMemory VectorStoreConfig
        print(f"[OK] BaseRAGAgent instantiated: {rag.name}")
    except Exception as e:
        print(f"[BROKEN] BaseRAGAgent instantiation: {e}")

    # Test SimpleRAGAgent
    try:
        from haive.agents.rag.simple.agent import SimpleRAGAgent
        print("[OK] SimpleRAGAgent imported")
    except ImportError as e:
        print(f"[BROKEN] SimpleRAGAgent import: {e}")
        return

    try:
        simple_rag = SimpleRAGAgent(name="simple_rag_demo")  # uses defaults
        print(f"[OK] SimpleRAGAgent instantiated: {simple_rag.name}")
    except Exception as e:
        print(f"[BROKEN] SimpleRAGAgent instantiation: {e}")

    # NOTE: RAG agents need a vector store / documents to actually run
    print("\n[INFO] RAG agents require vector store setup to run arun()")
    print("       Skipping arun test - would need document ingestion first")
    print("\n[OK] RAG agent demo complete (import + instantiate)")


if __name__ == "__main__":
    asyncio.run(main())
