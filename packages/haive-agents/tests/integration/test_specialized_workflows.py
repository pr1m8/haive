#!/usr/bin/env python3
"""Test script for specialized RAG workflows"""

import asyncio

from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


async def test_flare():
    """Test FLARE workflow"""
    print("\n=== Testing FLARE Agent ===")

    agent = FLAREAgent(name="flare_test")

    # Test with a query that should trigger uncertainty
    result = await agent.ainvoke(
        {
            "query": "What are the latest developments in quantum computing and how might they affect cryptography in the next decade?"
        }
    )

    print(f"Query: {result.get('query')}")
    print(f"Current generation: {result.get('current_generation', '')[:200]}...")
    print(f"Uncertainty tokens: {result.get('uncertainty_tokens', [])}")
    print(f"Retrieval triggers: {result.get('retrieval_triggers', [])}")
    print(f"Final answer: {result.get('answer', '')[:200]}...")
    print(f"Confidence scores: {result.get('confidence_scores', [])}")

    return result


async def test_dynamic_rag():
    """Test Dynamic RAG with add/remove retrievers"""
    print("\n=== Testing Dynamic RAG Agent ===")

    agent = DynamicRAGAgent(name="dynamic_rag_test")

    # Test with a query that might benefit from multiple retrievers
    result = await agent.ainvoke(
        {"query": "Compare the economic policies of the US and China in 2023"}
    )

    print(f"Query: {result.get('query')}")
    print(f"Active retrievers: {list(result.get('active_retrievers', {}).keys())}")
    print(f"Retriever performance: {result.get('retriever_performance', {})}")
    print(f"Document sources: {list(result.get('document_sources', {}).keys())}")
    print(f"Adaptive threshold: {result.get('adaptive_threshold', 0.7)}")
    print(f"Final answer: {result.get('answer', '')[:200]}...")

    return result


async def test_debate_rag():
    """Test Debate RAG system"""
    print("\n=== Testing Debate RAG Agent ===")

    # Create with custom positions
    agent = DebateRAGAgent(
        name="debate_rag_test",
        debate_positions=["Optimistic", "Pessimistic", "Balanced"],
    )

    # Test with a debatable topic
    result = await agent.ainvoke(
        {"query": "Is artificial intelligence more beneficial or harmful to society?"}
    )

    print(f"Query: {result.get('query')}")
    print(f"Debate positions: {list(result.get('debate_positions', {}).keys())}")
    print("Arguments by position:")
    for position, args in result.get("arguments_by_position", {}).items():
        print(f"  {position}: {len(args)} arguments")
    print("Evidence by position:")
    for position, evidence in result.get("evidence_by_position", {}).items():
        print(f"  {position}: {len(evidence)} pieces of evidence")
    print(f"Consensus reached: {result.get('consensus_reached', False)}")
    print(f"Final answer: {result.get('final_answer', '')[:200]}...")

    return result


async def test_adaptive_threshold():
    """Test Adaptive Threshold RAG"""
    print("\n=== Testing Adaptive Threshold RAG Agent ===")

    agent = AdaptiveThresholdRAGAgent(name="adaptive_threshold_test")

    # Test with a query that might need threshold adjustment
    result = await agent.ainvoke(
        {
            "query": "Explain the technical details of transformer architecture in neural networks"
        }
    )

    print(f"Query: {result.get('query')}")
    print(f"Initial threshold: {result.get('adaptive_threshold', 0.7)}")
    print(f"Active retrievers: {list(result.get('active_retrievers', {}).keys())}")
    print(f"Final answer: {result.get('answer', '')[:200]}...")

    return result


async def main():
    """Run all tests"""
    print("Testing Specialized RAG Workflows")
    print("=" * 50)

    try:
        # Test FLARE
        await test_flare()
        print("\n✓ FLARE test completed")

    except Exception as e:
        print(f"\n✗ FLARE test failed: {e}")
        import traceback

        traceback.print_exc()

    try:
        # Test Dynamic RAG
        await test_dynamic_rag()
        print("\n✓ Dynamic RAG test completed")

    except Exception as e:
        print(f"\n✗ Dynamic RAG test failed: {e}")
        import traceback

        traceback.print_exc()

    try:
        # Test Debate RAG
        await test_debate_rag()
        print("\n✓ Debate RAG test completed")

    except Exception as e:
        print(f"\n✗ Debate RAG test failed: {e}")
        import traceback

        traceback.print_exc()

    try:
        # Test Adaptive Threshold
        await test_adaptive_threshold()
        print("\n✓ Adaptive Threshold test completed")

    except Exception as e:
        print(f"\n✗ Adaptive Threshold test failed: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 50)
    print("All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
