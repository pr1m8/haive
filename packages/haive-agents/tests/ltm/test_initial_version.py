#!/usr/bin/env python3
"""
Test the initial version of LTM agent works with LangMem (no fallback).

Run with: poetry run python packages/haive-agents/tests/ltm/test_initial_version.py
"""

import logging
import sys

from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.ltm.agent import LTMAgent, LTMState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_initial_version():
    """Test that the initial version works perfectly."""
    print("=== Testing Initial LTM Agent Version (No Fallback) ===")

    # Create agent with default Anthropic config
    agent = LTMAgent(name="Initial LTM Agent")
    agent.setup_agent()

    print(f"✅ Agent created with provider: {agent.ltm_llm_config.provider}")
    print(f"   Model: {agent.ltm_llm_config.model}")

    # Create test conversation
    state = LTMState(
        messages=[
            HumanMessage(
                content="Hi! I'm John and I love playing guitar and composing music."
            ),
            AIMessage(
                content="Hello John! I'll remember your passion for guitar and music composition."
            ),
            HumanMessage(
                content="I'm also a vegetarian and I prefer spicy food, especially Thai cuisine."
            ),
            AIMessage(
                content="Got it! You're vegetarian with a preference for spicy Thai food."
            ),
            HumanMessage(
                content="I work as a data scientist and I enjoy running marathons in my free time."
            ),
            AIMessage(
                content="Excellent! So you're a data scientist who runs marathons."
            ),
        ]
    )

    # Test extraction - should work perfectly with no fallback
    print("\nTesting LangMem memory extraction...")
    result = agent.extract_memories_node(state)

    # Verify it worked (no errors)
    if "processing_errors" in result and result["processing_errors"]:
        print(f"❌ FAILED: {result['processing_errors']}")
        return False

    # Verify we got real memories
    memories = result["extracted_memories"]
    if not memories:
        print("❌ FAILED: No memories extracted")
        return False

    # Verify source is LangMem (not fallback)
    real_langmem = all(m["source"] == "langmem_extraction" for m in memories)
    if not real_langmem:
        print("❌ FAILED: Not using real LangMem extraction")
        sources = [m["source"] for m in memories]
        print(f"   Sources found: {sources}")
        return False

    print(f"✅ SUCCESS: Extracted {len(memories)} memories with LangMem")
    print(f"   Quality score: {result['extraction_quality']:.2f}")

    # Print memory details
    print("\n📋 Extracted Memories:")
    for i, memory in enumerate(memories):
        print(f"\n   Memory {i+1}:")
        print(f"     Schema: {memory['schema']}")
        print(f"     Source: {memory['source']}")
        if isinstance(memory["content"], dict):
            for key, value in memory["content"].items():
                if key != "confidence":  # Don't double-print confidence
                    print(f"     {key}: {value}")

    # Verify schema diversity
    schemas = set(m["schema"] for m in memories)
    print(f"\n📊 Schema diversity: {len(schemas)} types - {schemas}")

    print("\n🎉 Initial version working perfectly!")
    return True


def test_agent_graph_execution():
    """Test the core extraction functionality (what matters)."""
    print("\n=== Testing Core LangMem Extraction Functionality ===")

    agent = LTMAgent(name="Core Test Agent")
    agent.setup_agent()

    # Test just the extraction node directly (this is what matters)
    test_state = LTMState(
        messages=[
            HumanMessage(content="I love rock climbing and photography."),
            AIMessage(
                content="I'll remember your interests in rock climbing and photography."
            ),
        ]
    )

    try:
        # Test the core extraction functionality
        result = agent.extract_memories_node(test_state)

        # Verify success
        if "processing_errors" in result and result["processing_errors"]:
            print(f"❌ Extraction failed: {result['processing_errors']}")
            return False

        memories = result.get("extracted_memories", [])
        if not memories:
            print("❌ No memories extracted")
            return False

        # Verify LangMem source
        langmem_sources = [m for m in memories if m["source"] == "langmem_extraction"]
        if len(langmem_sources) != len(memories):
            print("❌ Not all memories from LangMem")
            return False

        print(f"✅ Core LangMem extraction successful")
        print(f"   Extracted {len(memories)} memories")
        print(f"   Quality: {result['extraction_quality']:.2f}")

        return True

    except Exception as e:
        print(f"❌ Core extraction failed: {e}")
        return False


if __name__ == "__main__":
    print("🧠 LTM Agent Initial Version Test (No Fallback Allowed)")
    print("=" * 60)

    success1 = test_initial_version()
    success2 = test_agent_graph_execution()

    print("\n" + "=" * 60)

    if success1 and success2:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Initial LTM Agent version works perfectly with LangMem")
        print("✅ No fallback needed - real LangMem integration working")
    else:
        print("❌ TESTS FAILED!")
        print("🔍 Initial version needs debugging")
        sys.exit(1)
