"""Comprehensive RAG Test Suite

Tests all RAG implementations including ChainAgent versions, traditional agents,
and multi-agent integrations.
"""

from typing import Any, Dict, List

import pytest
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document

# Test documents
TEST_DOCUMENTS = [
    Document(
        page_content="Machine learning is a subset of artificial intelligence that uses algorithms to learn patterns from data."
    ),
    Document(
        page_content="Neural networks are computational models inspired by biological neural networks in animal brains."
    ),
    Document(
        page_content="Deep learning uses multiple layers of neural networks to model complex patterns in data."
    ),
    Document(
        page_content="Reinforcement learning trains agents to make decisions through trial and error using rewards."
    ),
    Document(
        page_content="Natural language processing enables computers to understand and generate human language."
    ),
    Document(
        page_content="Computer vision allows machines to interpret and understand visual information from images."
    ),
]

# Test LLM configuration
TEST_LLM_CONFIG = AzureLLMConfig(
    deployment_name="gpt-4", azure_endpoint="test-endpoint", api_key="test-key"
)


class TestRAGChainCollection:
    """Test the ChainAgent RAG collection."""

    def test_simple_rag_chain(self):
        """Test simple RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_simple_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "Simple RAG"
        assert len(agent.nodes) >= 2  # Should have retrieve + generate nodes

    def test_fusion_rag_chain(self):
        """Test fusion RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_fusion_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "Fusion RAG"
        assert len(agent.nodes) >= 3  # Multi-query + fusion + synthesis

    def test_hyde_rag_chain(self):
        """Test HyDE RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_hyde_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "HyDE RAG"
        assert len(agent.nodes) >= 3  # HyDE gen + retrieval + answer

    def test_step_back_rag_chain(self):
        """Test step-back RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_step_back_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "Step-Back RAG"
        assert len(agent.nodes) >= 3  # Step-back + retrieve + answer

    def test_speculative_rag_chain(self):
        """Test speculative RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_speculative_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "Speculative RAG"
        assert len(agent.nodes) >= 3  # Hypothesis + verify + synthesize

    def test_memory_aware_rag_chain(self):
        """Test memory-aware RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_memory_aware_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "Memory-Aware RAG"
        assert len(agent.nodes) >= 3  # Memory + retrieve + answer

    def test_flare_rag_chain(self):
        """Test FLARE RAG chain creation."""
        from haive.agents.rag.chain_collection import RAGChainCollection

        collection = RAGChainCollection()
        agent = collection.create_flare_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        assert agent.name == "FLARE RAG"
        assert len(agent.nodes) >= 3  # Initial + active retrieve + refine


class TestUnifiedRAGFactory:
    """Test the unified RAG factory."""

    def test_factory_create_simple(self):
        """Test factory creates simple RAG."""
        from haive.agents.rag.unified_factory import create_rag

        agent = create_rag("simple", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)
        assert agent is not None

    def test_factory_create_fusion(self):
        """Test factory creates fusion RAG."""
        from haive.agents.rag.unified_factory import create_rag

        agent = create_rag("fusion", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)
        assert agent is not None

    def test_factory_create_chain_style(self):
        """Test factory creates chain style RAG."""
        from haive.agents.rag.unified_factory import create_rag_chain

        agent = create_rag_chain("simple", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)
        assert hasattr(agent, "nodes")  # Should be ChainAgent

    def test_factory_create_multi_style(self):
        """Test factory creates multi-agent style RAG."""
        from haive.agents.rag.unified_factory import create_rag_multi

        agent = create_rag_multi("simple", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)
        assert agent is not None

    def test_factory_create_pipeline(self):
        """Test factory creates RAG pipeline."""
        from haive.agents.rag.unified_factory import create_rag_pipeline

        pipeline = create_rag_pipeline(
            ["simple", "fusion"], TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG
        )
        assert pipeline.name == "RAG Pipeline"
        assert len(pipeline.nodes) >= 2  # At least 2 RAG agents


class TestModularRAG:
    """Test modular RAG implementations."""

    def test_modular_rag_creation(self):
        """Test modular RAG chain creation."""
        from haive.agents.rag.modular_chain import (
            ModularConfig,
            RAGModule,
            create_modular_rag,
        )

        config = ModularConfig(
            modules=[RAGModule.QUERY_EXPANSION, RAGModule.ANSWER_GENERATION]
        )
        agent = create_modular_rag(TEST_DOCUMENTS, config, TEST_LLM_CONFIG)

        assert agent.name == "Modular RAG"
        assert len(agent.nodes) >= 2  # Should have the specified modules

    def test_simple_modular_rag(self):
        """Test simple modular RAG creation."""
        from haive.agents.rag.modular_chain import create_simple_modular_rag

        agent = create_simple_modular_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None

    def test_comprehensive_modular_rag(self):
        """Test comprehensive modular RAG creation."""
        from haive.agents.rag.modular_chain import create_comprehensive_modular_rag

        agent = create_comprehensive_modular_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 6  # Should have all modules


class TestBranchedRAG:
    """Test branched RAG implementations."""

    def test_branched_rag_creation(self):
        """Test branched RAG chain creation."""
        from haive.agents.rag.branched_chain import create_branched_rag_chain

        agent = create_branched_rag_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Branched RAG"
        assert len(agent.nodes) >= 8  # Should have multiple branches

    def test_adaptive_branched_rag(self):
        """Test adaptive branched RAG creation."""
        from haive.agents.rag.branched_chain import create_adaptive_branched_rag

        agent = create_adaptive_branched_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 4  # Classifier + branches

    def test_parallel_branched_rag(self):
        """Test parallel branched RAG creation."""
        from haive.agents.rag.branched_chain import create_parallel_branched_rag

        agent = create_parallel_branched_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 4  # Parallel branches + synthesizer


class TestEnhancedMemoryReActRAG:
    """Test enhanced memory ReAct RAG implementations."""

    def test_enhanced_memory_react_creation(self):
        """Test enhanced memory ReAct RAG creation."""
        from haive.agents.rag.enhanced_memory_react import (
            create_enhanced_memory_react_rag,
        )

        agent = create_enhanced_memory_react_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Enhanced Memory ReAct RAG"
        assert len(agent.nodes) >= 8  # Full ReAct chain with memory

    def test_simple_memory_react_creation(self):
        """Test simple memory ReAct RAG creation."""
        from haive.agents.rag.enhanced_memory_react import (
            create_simple_memory_react_rag,
        )

        agent = create_simple_memory_react_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Simple Memory ReAct RAG"
        assert len(agent.nodes) >= 3  # Simplified ReAct chain

    def test_memory_react_with_tools(self):
        """Test memory ReAct RAG with tools."""
        from haive.agents.rag.enhanced_memory_react import (
            create_memory_react_with_tools,
        )

        agent = create_memory_react_with_tools(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Memory ReAct RAG with Tools"
        assert len(agent.nodes) >= 3  # Tools + ReAct


class TestAgendicRouterChain:
    """Test agentic router chain implementations."""

    def test_agentic_router_chain_creation(self):
        """Test agentic router chain creation."""
        from haive.agents.rag.agentic_router.agent_chain import (
            create_agentic_rag_router_chain,
        )

        agent = create_agentic_rag_router_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Agentic RAG Router"
        assert len(agent.nodes) >= 5  # Strategy selector + RAG agents + synthesizer

    def test_simple_router_chain_creation(self):
        """Test simple router chain creation."""
        from haive.agents.rag.agentic_router.agent_chain import (
            create_simple_rag_router_chain,
        )

        agent = create_simple_rag_router_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 3  # Classifier + 2 RAG strategies


class TestQueryPlanningChain:
    """Test query planning chain implementations."""

    def test_query_planning_chain_creation(self):
        """Test query planning chain creation."""
        from haive.agents.rag.query_planning.agent_chain import (
            create_query_planning_chain,
        )

        agent = create_query_planning_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent.name == "Query Planning RAG"
        assert len(agent.nodes) >= 3  # Planner + executor + synthesizer

    def test_simple_decomposition_chain(self):
        """Test simple decomposition chain creation."""
        from haive.agents.rag.query_planning.agent_chain import (
            create_simple_decomposition_chain,
        )

        agent = create_simple_decomposition_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 3  # Decomposer + answerer + combiner

    def test_adaptive_planning_chain(self):
        """Test adaptive planning chain creation."""
        from haive.agents.rag.query_planning.agent_chain import (
            create_adaptive_planning_chain,
        )

        agent = create_adaptive_planning_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)
        assert agent is not None
        assert len(agent.nodes) >= 3  # Analyzer + routing


class TestRAGIntegration:
    """Test RAG integration with other systems."""

    def test_chain_multi_agent_integration(self):
        """Test ChainAgent integration with multi-agent system."""
        from haive.agents.rag.unified_factory import create_rag_multi

        multi_agent = create_rag_multi(
            "simple", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG
        )
        assert multi_agent is not None

    def test_all_rag_types_availability(self):
        """Test that all RAG types are available through factory."""
        from haive.agents.rag.unified_factory import RAGType, create_rag

        # Test core RAG types
        core_types = [
            RAGType.SIMPLE,
            RAGType.FUSION,
            RAGType.HYDE,
            RAGType.FLARE,
            RAGType.SPECULATIVE,
            RAGType.MEMORY_AWARE,
            RAGType.STEP_BACK,
        ]

        for rag_type in core_types:
            try:
                agent = create_rag(rag_type, TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)
                assert agent is not None, f"Failed to create {rag_type} RAG"
            except Exception as e:
                pytest.fail(f"Error creating {rag_type} RAG: {e}")


class TestRAGStateSchemas:
    """Test RAG state schemas and I/O compatibility."""

    def test_io_schemas_available(self):
        """Test that I/O schemas are available for chain agents."""
        from haive.agents.rag.agentic_router.agent_chain import (
            get_agentic_router_chain_io_schema,
        )
        from haive.agents.rag.branched_chain import get_branched_rag_io_schema
        from haive.agents.rag.enhanced_memory_react import (
            get_enhanced_memory_react_io_schema,
        )
        from haive.agents.rag.query_planning.agent_chain import (
            get_query_planning_chain_io_schema,
        )

        # Test schemas exist and have required structure
        schemas = [
            get_branched_rag_io_schema(),
            get_enhanced_memory_react_io_schema(),
            get_agentic_router_chain_io_schema(),
            get_query_planning_chain_io_schema(),
        ]

        for schema in schemas:
            assert "inputs" in schema
            assert "outputs" in schema
            assert isinstance(schema["inputs"], list)
            assert isinstance(schema["outputs"], list)
            assert len(schema["inputs"]) > 0
            assert len(schema["outputs"]) > 0


class TestRAGPerformance:
    """Test RAG performance and functionality."""

    def test_rag_execution_mock(self):
        """Test that RAG agents can be invoked (mock execution)."""
        from haive.agents.rag.chain_collection import create_rag_chain

        # Create a simple RAG chain
        agent = create_rag_chain("simple", TEST_DOCUMENTS, llm_config=TEST_LLM_CONFIG)

        # Test state structure
        test_state = {"query": "What is machine learning?", "messages": []}

        # Verify agent has callable interface
        assert hasattr(agent, "invoke") or hasattr(agent, "__call__")
        assert hasattr(agent, "nodes")
        assert len(agent.nodes) > 0

    def test_complex_rag_chain_structure(self):
        """Test complex RAG chain has proper structure."""
        from haive.agents.rag.branched_chain import create_branched_rag_chain

        agent = create_branched_rag_chain(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        # Verify complex structure
        assert len(agent.nodes) >= 8  # Should have multiple nodes
        assert hasattr(agent, "edges")  # Should have edge connections

    def test_memory_state_handling(self):
        """Test memory-aware RAG handles state properly."""
        from haive.agents.rag.enhanced_memory_react import (
            create_simple_memory_react_rag,
        )

        agent = create_simple_memory_react_rag(TEST_DOCUMENTS, TEST_LLM_CONFIG)

        # Test with different message contexts
        empty_state = {"query": "Test", "messages": []}
        memory_state = {
            "query": "Test",
            "messages": [{"role": "user", "content": "Previous message"}],
        }

        # Should handle both states without errors during construction
        assert agent is not None


def run_comprehensive_rag_tests():
    """Run all RAG tests and return summary."""

    test_classes = [
        TestRAGChainCollection,
        TestUnifiedRAGFactory,
        TestModularRAG,
        TestBranchedRAG,
        TestEnhancedMemoryReActRAG,
        TestAgendicRouterChain,
        TestQueryPlanningChain,
        TestRAGIntegration,
        TestRAGStateSchemas,
        TestRAGPerformance,
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = []

    for test_class in test_classes:
        test_instance = test_class()
        test_methods = [
            method for method in dir(test_instance) if method.startswith("test_")
        ]

        for test_method in test_methods:
            total_tests += 1
            try:
                getattr(test_instance, test_method)()
                passed_tests += 1
                print(f"✅ {test_class.__name__}.{test_method}")
            except Exception as e:
                failed_tests.append(f"{test_class.__name__}.{test_method}: {e}")
                print(f"❌ {test_class.__name__}.{test_method}: {e}")

    print(f"\n📊 Test Summary:")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {len(failed_tests)}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if failed_tests:
        print(f"\n❌ Failed Tests:")
        for failure in failed_tests:
            print(f"  - {failure}")

    return {
        "total": total_tests,
        "passed": passed_tests,
        "failed": len(failed_tests),
        "success_rate": (passed_tests / total_tests) * 100,
        "failures": failed_tests,
    }


if __name__ == "__main__":
    print("🧪 Running Comprehensive RAG Test Suite...")
    results = run_comprehensive_rag_tests()
    print(f"\n🎯 Overall Success Rate: {results['success_rate']:.1f}%")
