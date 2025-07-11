#!/usr/bin/env python3
"""Test LTM Agent fallback functionality without API calls.

Run with: poetry run python packages/haive-agents/tests/ltm/test_fallback_only.py
"""

import logging
import sys

from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.ltm.agent import LTMAgent, LTMState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_fallback_extraction():
    """Test fallback extraction mechanism."""
    # Create agent that will trigger fallback due to quota/API issues
    # (We know from previous test that API quota is exceeded)
    agent = LTMAgent(name="Fallback Test Agent")
    agent.setup_agent()

    # Create test conversation
    state = LTMState(
        messages=[
            HumanMessage(content="Hi! I'm Sarah and I love science fiction books."),
            AIMessage(
                content="Nice to meet you, Sarah! I'll remember your interest in sci-fi."
            ),
            HumanMessage(content="I'm also a vegetarian and prefer Italian food."),
            AIMessage(
                content="Got it! Vegetarian with a preference for Italian cuisine."
            ),
        ]
    )

    # Test extraction - should trigger fallback
    result = agent.extract_memories_node(state)

    # Verify fallback worked
    assert "extracted_memories" in result
    memories = result["extracted_memories"]

    # Verify fallback characteristics
    fallback_memories = [m for m in memories if m["source"] == "fallback_extraction"]
    assert len(fallback_memories) > 0, "Should have fallback memories"

    # Check quality is capped for fallback
    assert result["extraction_quality"] <= 0.5, "Fallback quality should be capped"

    return result


def test_quality_calculation_standalone():
    """Test quality calculation without API calls."""
    agent = LTMAgent(name="Quality Test Agent")

    # Test different quality scenarios
    messages = [HumanMessage(content=f"Message {i}") for i in range(10)]

    # High quality: good ratio and diversity
    high_quality_memories = [
        {"memory_id": "mem_1", "schema": "Memory", "confidence": 0.9},
        {"memory_id": "mem_2", "schema": "UserPreference", "confidence": 0.9},
        {"memory_id": "mem_3", "schema": "FactualMemory", "confidence": 0.9},
        {"memory_id": "mem_4", "schema": "ConversationalMemory", "confidence": 0.9},
    ]

    # Medium quality: decent ratio, less diversity
    medium_quality_memories = [
        {"memory_id": "mem_1", "schema": "Memory", "confidence": 0.7},
        {"memory_id": "mem_2", "schema": "Memory", "confidence": 0.7},
    ]

    # Low quality: poor ratio
    low_quality_memories = [
        {"memory_id": "mem_1", "schema": "Memory", "confidence": 0.5}
    ]

    high_score = agent._calculate_extraction_quality(high_quality_memories, messages)
    medium_score = agent._calculate_extraction_quality(
        medium_quality_memories, messages
    )
    low_score = agent._calculate_extraction_quality(low_quality_memories, messages)

    # Verify quality ordering
    assert high_score >= medium_score >= low_score, "Quality scores should be ordered"
    assert (
        0.0 <= low_score <= medium_score <= high_score <= 1.0
    ), "Scores should be in [0,1] range"


def test_memory_schemas():
    """Test memory schema imports."""
    try:
        from haive.agents.ltm.memory_schemas import (
            DEFAULT_MEMORY_SCHEMAS,
            FactualMemory,
            Memory,
            UserPreference,
        )

        # Test creating instances
        Memory(content="Test memory content")
        UserPreference(
            category="food", preference="pizza", context="user mentioned loving pizza"
        )
        FactualMemory(fact="Paris is the capital of France", domain="geography")

        assert len(DEFAULT_MEMORY_SCHEMAS) > 0, "Should have default schemas"

    except Exception:
        raise


if __name__ == "__main__":

    try:
        test_memory_schemas()
        test_quality_calculation_standalone()
        test_fallback_extraction()

    except Exception:
        import traceback

        traceback.print_exc()
        sys.exit(1)
