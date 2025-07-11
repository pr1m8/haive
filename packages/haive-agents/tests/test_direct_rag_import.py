"""Direct test of new RAG workflow implementations without going through broken __init__.py."""

import os
import sys

import pytest

# Add the source directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def test_memory_rag_agent():
    """Test SimpleRAGWithMemoryAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import (
        MemoryRAGState,
        SimpleRAGWithMemoryAgent,
    )

    # Test state creation
    state = MemoryRAGState(query="test query")
    assert state.query == "test query"
    assert state.conversation_history == []
    assert state.previous_queries == []

    # Test agent creation
    agent = SimpleRAGWithMemoryAgent(name="test_memory_rag")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "memory_context_agent"


def test_self_rag_agent():
    """Test SelfRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import (
        SelfRAGAgent,
        SelfRAGState,
    )

    # Test state creation
    state = SelfRAGState(query="test query")
    assert state.query == "test query"
    assert state.reflection_tokens == []
    assert state.needs_retrieval

    # Test agent creation
    agent = SelfRAGAgent(name="test_self_rag")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "retrieval_checker"


def test_multi_query_rag_agent():
    """Test MultiQueryRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import (
        MultiQueryRAGAgent,
        MultiQueryRAGState,
    )

    # Test state creation
    state = MultiQueryRAGState(query="test query")
    assert state.query == "test query"
    assert state.generated_queries == []
    assert state.query_results == {}

    # Test agent creation
    agent = MultiQueryRAGAgent(name="test_multi_query")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "query_expander"


def test_rag_fusion_agent():
    """Test RAGFusionAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import RAGFusionAgent

    # Test agent creation
    agent = RAGFusionAgent(name="test_fusion")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[1].name == "fusion_ranker"


def test_step_back_rag_agent():
    """Test StepBackPromptingRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import (
        StepBackPromptingRAGAgent,
    )

    # Test agent creation
    agent = StepBackPromptingRAGAgent(name="test_step_back")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "step_back_agent"


def test_query_decomposition_rag_agent():
    """Test QueryDecompositionRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.additional_workflows import (
        QueryDecompositionRAGAgent,
    )

    # Test agent creation
    agent = QueryDecompositionRAGAgent(name="test_decomposition")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "decomposition_agent"


def test_graph_rag_agent():
    """Test GraphRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.advanced_workflows import (
        GraphRAGAgent,
        GraphRAGState,
    )

    # Test state creation
    state = GraphRAGState(query="test query")
    assert state.query == "test query"
    assert state.knowledge_graph == {}
    assert state.graph_entities == []

    # Test agent creation
    agent = GraphRAGAgent(name="test_graph_rag")
    assert agent is not None
    assert len(agent.agents) == 4
    assert agent.agents[0].name == "entity_extractor"


def test_agentic_graph_rag_agent():
    """Test AgenticGraphRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.advanced_workflows import AgenticGraphRAGAgent

    # Test agent creation
    agent = AgenticGraphRAGAgent(name="test_agentic_graph")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[1].name == "routing_agent"


def test_speculative_rag_agent():
    """Test SpeculativeRAGAgent can be imported and created."""
    from haive.agents.rag.multi_agent_rag.advanced_workflows import SpeculativeRAGAgent

    # Test agent creation
    agent = SpeculativeRAGAgent(name="test_speculative")
    assert agent is not None
    assert len(agent.agents) == 3
    assert agent.agents[0].name == "hypothesis_generator"


def test_all_advanced_agents():
    """Test all advanced RAG agents can be imported."""
    from haive.agents.rag.multi_agent_rag.advanced_workflows import (
        AgenticRAGRouterAgent,
        QueryPlanningAgenticRAGAgent,
        SelfReflectiveAgenticRAGAgent,
        SelfRouteRAGAgent,
    )

    # Just test they can be created
    router = AgenticRAGRouterAgent(name="test_router")
    planner = QueryPlanningAgenticRAGAgent(name="test_planner")
    reflective = SelfReflectiveAgenticRAGAgent(name="test_reflective")
    self_route = SelfRouteRAGAgent(name="test_self_route")

    assert all([router, planner, reflective, self_route])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
