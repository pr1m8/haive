#!/usr/bin/env python3
"""Simple test to check if RAG agents can be imported and created."""

import os
import sys

# Add the source paths
sys.path.insert(0, os.path.join(os.getcwd(), "src"))


def test_imports():
    """Test if we can import the basic classes."""
    print("Testing imports...")

    try:
        from langchain_core.documents import Document

        print("✅ langchain_core.documents imported")
    except ImportError as e:
        print(f"❌ langchain_core.documents failed: {e}")
        return False

    try:
        from haive.agents.rag.simple.agent import SimpleRAGAgent

        print("✅ SimpleRAGAgent imported")
    except ImportError as e:
        print(f"❌ SimpleRAGAgent failed: {e}")
        return False

    return True


def test_simple_creation():
    """Test if we can create a SimpleRAGAgent."""
    print("\nTesting SimpleRAGAgent creation...")

    try:
        from langchain_core.documents import Document

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        # Create test documents
        docs = [
            Document(page_content="Python is a programming language."),
            Document(page_content="Machine learning uses algorithms."),
        ]

        # Try to create the agent (without LLM config)
        agent = SimpleRAGAgent.from_documents(documents=docs)
        print(f"✅ SimpleRAGAgent created with {len(agent.agents)} agents")
        print(f"   Agent names: {[a.name for a in agent.agents]}")
        return True

    except Exception as e:
        print(f"❌ SimpleRAGAgent creation failed: {e}")
        return False


if __name__ == "__main__":
    print("=== RAG Agent Simple Test ===\n")

    # Test 1: Imports
    if not test_imports():
        print("❌ Import test failed - stopping")
        sys.exit(1)

    # Test 2: Creation
    if not test_simple_creation():
        print("❌ Creation test failed")
        sys.exit(1)

    print("\n✅ Basic tests passed!")
    print("Note: Full execution tests require LLM configuration.")
