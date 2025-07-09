#!/usr/bin/env python3
"""Simple test script for specialized RAG workflows"""

from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


def test_workflow_instantiation():
    """Test that workflows can be instantiated"""
    print("Testing workflow instantiation...")

    try:
        # Test FLARE
        flare = FLAREAgent(name="flare_test")
        print("✓ FLARE Agent created successfully")
        print(f"  - Agents: {[agent.name for agent in flare.agents]}")
        print(f"  - Execution mode: {flare.execution_mode}")
        print(f"  - State schema: {flare.state_schema.__name__}")

    except Exception as e:
        print(f"✗ FLARE Agent failed: {e}")

    print()

    try:
        # Test Dynamic RAG
        dynamic = DynamicRAGAgent(name="dynamic_test")
        print("✓ Dynamic RAG Agent created successfully")
        print(f"  - Agents: {[agent.name for agent in dynamic.agents]}")
        print(f"  - Execution mode: {dynamic.execution_mode}")
        print(f"  - State schema: {dynamic.state_schema.__name__}")

    except Exception as e:
        print(f"✗ Dynamic RAG Agent failed: {e}")

    print()

    try:
        # Test Debate RAG
        debate = DebateRAGAgent(
            name="debate_test", debate_positions=["Pro", "Con", "Neutral"]
        )
        print("✓ Debate RAG Agent created successfully")
        print(f"  - Agents: {[agent.name for agent in debate.agents]}")
        print(f"  - Execution mode: {debate.execution_mode}")
        print(f"  - State schema: {debate.state_schema.__name__}")
        print(
            f"  - Debate positions: {getattr(debate, '_debate_positions', 'NOT SET')}"
        )

    except Exception as e:
        print(f"✗ Debate RAG Agent failed: {e}")

    print()

    try:
        # Test Adaptive Threshold
        adaptive = AdaptiveThresholdRAGAgent(name="adaptive_test")
        print("✓ Adaptive Threshold RAG Agent created successfully")
        print(f"  - Agents: {[agent.name for agent in adaptive.agents]}")
        print(f"  - Execution mode: {adaptive.execution_mode}")
        print(f"  - State schema: {adaptive.state_schema.__name__}")

    except Exception as e:
        print(f"✗ Adaptive Threshold RAG Agent failed: {e}")


def test_state_schemas():
    """Test state schema fields"""
    print("\n\nTesting state schemas...")

    from haive.agents.rag.multi_agent_rag.specialized_workflows import (
        DebateRAGState,
        DynamicRAGState,
        FLAREState,
    )

    # Test FLARE State
    print("\nFLARE State fields:")
    flare_state = FLAREState()
    for field in [
        "current_generation",
        "uncertainty_tokens",
        "active_retrieval_points",
        "generation_segments",
        "confidence_scores",
        "retrieval_triggers",
    ]:
        print(f"  - {field}: {getattr(flare_state, field, 'NOT FOUND')}")

    # Test Dynamic RAG State
    print("\nDynamic RAG State fields:")
    dynamic_state = DynamicRAGState()
    for field in [
        "active_retrievers",
        "retriever_performance",
        "document_sources",
        "retriever_configurations",
        "adaptive_threshold",
    ]:
        print(f"  - {field}: {getattr(dynamic_state, field, 'NOT FOUND')}")

    # Test Debate RAG State
    print("\nDebate RAG State fields:")
    debate_state = DebateRAGState()
    for field in [
        "debate_positions",
        "arguments_by_position",
        "evidence_by_position",
        "debate_rounds",
        "synthesis_attempts",
        "consensus_reached",
        "final_answer",
    ]:
        print(f"  - {field}: {getattr(debate_state, field, 'NOT FOUND')}")


def test_agent_schemas():
    """Test individual agent output schemas"""
    print("\n\nTesting agent output schemas...")

    # Create FLARE agent and check its sub-agents
    flare = FLAREAgent(name="flare_test")
    print("\nFLARE Agent sub-agents:")
    for agent in flare.agents:
        print(f"\n  {agent.name}:")
        if hasattr(agent, "output_schema") and agent.output_schema:
            for key, value in agent.output_schema.items():
                print(f"    - {key}: {value}")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Specialized RAG Workflows (Simple)")
    print("=" * 60)

    test_workflow_instantiation()
    test_state_schemas()
    test_agent_schemas()

    print("\n" + "=" * 60)
    print("Simple tests completed!")
    print("=" * 60)
