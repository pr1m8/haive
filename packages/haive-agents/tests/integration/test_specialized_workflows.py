#!/usr/bin/env python3
"""Test script for specialized RAG workflows."""

import asyncio

from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


async def test_flare():
    """Test FLARE workflow."""
    agent = FLAREAgent(name="flare_test")

    # Test with a query that should trigger uncertainty
    result = await agent.ainvoke(
        {
            "query": "What are the latest developments in quantum computing and how might they affect cryptography in the next decade?"
        }
    )

    return result


async def test_dynamic_rag():
    """Test Dynamic RAG with add/remove retrievers."""
    agent = DynamicRAGAgent(name="dynamic_rag_test")

    # Test with a query that might benefit from multiple retrievers
    result = await agent.ainvoke(
        {"query": "Compare the economic policies of the US and China in 2023"}
    )

    return result


async def test_debate_rag():
    """Test Debate RAG system."""
    # Create with custom positions
    agent = DebateRAGAgent(
        name="debate_rag_test",
        debate_positions=["Optimistic", "Pessimistic", "Balanced"],
    )

    # Test with a debatable topic
    result = await agent.ainvoke(
        {"query": "Is artificial intelligence more beneficial or harmful to society?"}
    )

    for _position, _args in result.get("arguments_by_position", {}).items():
        pass
    for _position, _evidence in result.get("evidence_by_position", {}).items():
        pass

    return result


async def test_adaptive_threshold():
    """Test Adaptive Threshold RAG."""
    agent = AdaptiveThresholdRAGAgent(name="adaptive_threshold_test")

    # Test with a query that might need threshold adjustment
    result = await agent.ainvoke(
        {
            "query": "Explain the technical details of transformer architecture in neural networks"
        }
    )

    return result


async def main():
    """Run all tests."""
    try:
        # Test FLARE
        await test_flare()

    except Exception:
        import traceback

        traceback.print_exc()

    try:
        # Test Dynamic RAG
        await test_dynamic_rag()

    except Exception:
        import traceback

        traceback.print_exc()

    try:
        # Test Debate RAG
        await test_debate_rag()

    except Exception:
        import traceback

        traceback.print_exc()

    try:
        # Test Adaptive Threshold
        await test_adaptive_threshold()

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
