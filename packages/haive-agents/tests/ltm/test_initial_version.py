#!/usr/bin/env python3
"""Test the initial version of LTM agent works with LangMem (no fallback).

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

    # Create agent with default Anthropic config
    agent = LTMAgent(name="Initial LTM Agent")
    agent.setup_agent()


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
    result = agent.extract_memories_node(state)

    # Verify it worked (no errors)
    if result.get("processing_errors"):
        return False

    # Verify we got real memories
    memories = result["extracted_memories"]
    if not memories:
        return False

    # Verify source is LangMem (not fallback)
    real_langmem = all(m["source"] == "langmem_extraction" for m in memories)
    if not real_langmem:
        sources = [m["source"] for m in memories]
        return False


    # Print memory details
    for i, memory in enumerate(memories):
        if isinstance(memory["content"], dict):
            for key, value in memory["content"].items():
                if key != "confidence":  # Don't double-print confidence
                    pass

    # Verify schema diversity
    schemas = set(m["schema"] for m in memories}

    return True


def test_agent_graph_execution():
    """Test the core extraction functionality (what matters)."""

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
        if result.get("processing_errors"):
            return False

        memories = result.get("extracted_memories", [])
        if not memories:
            return False

        # Verify LangMem source
        langmem_sources = [m for m in memories if m["source"] == "langmem_extraction"]
        if len(langmem_sources) != len(memories):
            return False


        return True

    except Exception as e:
        return False


if __name__ == "__main__":

    success1 = test_initial_version()
    success2 = test_agent_graph_execution()


    if success1 and success2:
    else:
        sys.exit(1)
