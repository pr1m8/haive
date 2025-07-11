#!/usr/bin/env python3
"""Simple test to check if RAG agents can be imported and created."""

import os
import sys

# Add the source paths
sys.path.insert(0, os.path.join(os.getcwd(), "src"))


def test_imports():
    """Test if we can import the basic classes."""
    try:
        from langchain_core.documents import Document

    except ImportError:
        return False

    try:
        from haive.agents.rag.simple.agent import SimpleRAGAgent

    except ImportError:
        return False

    return True


def test_simple_creation():
    """Test if we can create a SimpleRAGAgent."""
    try:
        from langchain_core.documents import Document

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        # Create test documents
        docs = [
            Document(page_content="Python is a programming language."),
            Document(page_content="Machine learning uses algorithms."),
        ]

        # Try to create the agent (without LLM config)
        SimpleRAGAgent.from_documents(documents=docs)
        return True

    except Exception:
        return False


if __name__ == "__main__":

    # Test 1: Imports
    if not test_imports():
        sys.exit(1)

    # Test 2: Creation
    if not test_simple_creation():
        sys.exit(1)
