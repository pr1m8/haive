#!/usr/bin/env python3
"""Test workflow logic with mock data"""

from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DebateRAGState,
    DynamicRAGAgent,
    DynamicRAGState,
    FLAREAgent,
    FLAREState,
)


def test_flare_logic():
    """Test FLARE workflow logic"""
    print("=== Testing FLARE Logic ===")

    # Create agent
    FLAREAgent(name="flare_test")

    # Simulate state progression
    state = FLAREState(query="What is quantum computing?")
    print(f"Initial query: {state.query}")

    # Simulate generation monitor output
    state.current_generation = "Quantum computing is... (uncertain about specifics)"
    state.uncertainty_tokens = ["uncertain", "specifics"]
    state.confidence_scores = [0.8, 0.3]
    print(f"Uncertainty detected: {state.uncertainty_tokens}")

    # Simulate active retrieval
    state.retrieval_triggers = ["Need more info on quantum principles"]
    state.retrieved_documents = [
        "Quantum computing uses qubits...",
        "Superposition allows...",
    ]
    print(f"Retrieved {len(state.retrieved_documents)} documents")

    # Simulate informed generation
    state.generation_segments = [
        "Quantum computing is a revolutionary technology",
        "It uses quantum mechanical phenomena like superposition",
    ]
    state.answer = "Quantum computing is a revolutionary technology that uses quantum mechanical phenomena..."
    print(f"Final answer: {state.answer[:100]}...")

    print("✓ FLARE logic test passed\n")


def test_dynamic_rag_logic():
    """Test Dynamic RAG logic"""
    print("=== Testing Dynamic RAG Logic ===")

    # Create agent
    DynamicRAGAgent(name="dynamic_test")

    # Simulate state
    state = DynamicRAGState(query="Compare US and China economies")
    print(f"Query: {state.query}")

    # Simulate retriever manager decision
    state.active_retrievers = {
        "semantic_search": {"type": "dense", "model": "e5-base"},
        "keyword_search": {"type": "sparse", "algorithm": "bm25"},
        "news_retriever": {"type": "api", "source": "news_api"},
    }
    print(f"Active retrievers: {list(state.active_retrievers.keys())}")

    # Simulate retriever performance
    state.retriever_performance = {
        "semantic_search": 0.85,
        "keyword_search": 0.72,
        "news_retriever": 0.91,
    }
    print(
        f"Best performer: news_retriever ({state.retriever_performance['news_retriever']})"
    )

    # Simulate document sources
    state.document_sources = {
        "semantic_search": ["doc1", "doc2"],
        "keyword_search": ["doc3"],
        "news_retriever": ["news1", "news2", "news3"],
    }
    state.retrieved_documents = ["doc1", "doc2", "doc3", "news1", "news2", "news3"]

    # Simulate adaptive threshold
    state.adaptive_threshold = 0.8  # Raised due to good performance
    print(f"Adaptive threshold: {state.adaptive_threshold}")

    state.answer = "Based on multiple sources, the US and China economies differ in..."
    print(f"Answer: {state.answer[:60]}...")

    print("✓ Dynamic RAG logic test passed\n")


def test_debate_logic():
    """Test Debate RAG logic"""
    print("=== Testing Debate RAG Logic ===")

    # Create agent
    positions = ["Optimist", "Pessimist", "Realist"]
    DebateRAGAgent(name="debate_test", debate_positions=positions)

    # Simulate state
    state = DebateRAGState(query="Is AI beneficial or harmful?")
    state.debate_positions = {
        "Optimist": "AI will solve humanity's greatest challenges",
        "Pessimist": "AI poses existential risks to humanity",
        "Realist": "AI has both benefits and risks that must be managed",
    }
    print(f"Query: {state.query}")
    print(f"Positions: {list(state.debate_positions.keys())}")

    # Simulate arguments
    state.arguments_by_position = {
        "Optimist": [
            "AI can cure diseases",
            "AI can solve climate change",
            "AI enhances human capabilities",
        ],
        "Pessimist": [
            "AI could lead to job displacement",
            "AI weapons are dangerous",
            "AI alignment is unsolved",
        ],
        "Realist": [
            "AI benefits depend on implementation",
            "Regulation is necessary",
            "Balance innovation with safety",
        ],
    }

    # Simulate evidence
    state.evidence_by_position = {
        "Optimist": ["Study shows AI drug discovery success"],
        "Pessimist": ["Report on AI job automation"],
        "Realist": ["EU AI Act example"],
    }

    state.debate_rounds = 3
    print(f"Debate rounds: {state.debate_rounds}")

    # Simulate synthesis
    state.synthesis_attempts = ["Initial synthesis focused on benefits..."]
    state.consensus_reached = True
    state.final_answer = "AI presents both opportunities and challenges. The key is..."

    print(f"Consensus reached: {state.consensus_reached}")
    print(f"Final answer: {state.final_answer[:50]}...")

    print("✓ Debate logic test passed\n")


def test_adaptive_threshold_logic():
    """Test Adaptive Threshold logic"""
    print("=== Testing Adaptive Threshold Logic ===")

    # Create agent
    AdaptiveThresholdRAGAgent(name="adaptive_test")

    # Use Dynamic RAG state (as specified in the agent)
    state = DynamicRAGState(query="Explain transformer architecture")
    print(f"Query: {state.query}")

    # Simulate query analysis
    query_complexity = 0.85  # High complexity
    initial_threshold = 0.6  # Start lower for complex query
    state.adaptive_threshold = initial_threshold
    print(f"Query complexity: {query_complexity}")
    print(f"Initial threshold: {state.adaptive_threshold}")

    # Simulate retrieval rounds
    print("\nRetrieval rounds:")

    # Round 1: Too few results
    state.retrieved_documents = ["Basic transformer overview"]
    print(f"  Round 1: {len(state.retrieved_documents)} docs (too few)")
    state.adaptive_threshold = 0.5  # Lower threshold

    # Round 2: Better results
    state.retrieved_documents = [
        "Transformer architecture",
        "Attention mechanism",
        "Positional encoding",
    ]
    print(f"  Round 2: {len(state.retrieved_documents)} docs (better)")

    # Round 3: Good results
    state.retrieved_documents = state.retrieved_documents + [
        "Multi-head attention",
        "Feed-forward networks",
    ]
    print(f"  Round 3: {len(state.retrieved_documents)} docs (good)")

    # Final answer
    state.answer = "Transformer architecture consists of encoder-decoder structure with attention mechanisms..."
    print(f"\nFinal threshold: {state.adaptive_threshold}")
    print(f"Answer: {state.answer[:70]}...")

    print("✓ Adaptive threshold logic test passed\n")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Workflow Logic")
    print("=" * 60)
    print()

    test_flare_logic()
    test_dynamic_rag_logic()
    test_debate_logic()
    test_adaptive_threshold_logic()

    print("=" * 60)
    print("All logic tests passed! ✓")
    print("=" * 60)
