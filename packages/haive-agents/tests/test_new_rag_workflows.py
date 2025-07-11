"""Test suite for new RAG workflow implementations."""

import pytest


class TestBasicRAGWorkflows:
    """Test basic RAG workflow implementations."""

    def test_import_workflows(self):
        """Test that we can import the new RAG workflows."""
        try:
            from haive.agents.rag.multi_agent_rag.additional_workflows import (
                MultiQueryRAGAgent,
                QueryDecompositionRAGAgent,
                RAGFusionAgent,
                SelfRAGAgent,
                SimpleRAGWithMemoryAgent,
                StepBackPromptingRAGAgent,
            )

            assert True  # Import succeeded
        except ImportError as e:
            pytest.fail(f"Failed to import additional workflows: {e}")

    def test_import_advanced_workflows(self):
        """Test that we can import the advanced RAG workflows."""
        try:
            from haive.agents.rag.multi_agent_rag.advanced_workflows import (
                AgenticGraphRAGAgent,
                AgenticRAGRouterAgent,
                GraphRAGAgent,
                QueryPlanningAgenticRAGAgent,
                SelfReflectiveAgenticRAGAgent,
                SelfRouteRAGAgent,
                SpeculativeRAGAgent,
            )

            assert True  # Import succeeded
        except ImportError as e:
            pytest.fail(f"Failed to import advanced workflows: {e}")

    def test_state_schemas(self):
        """Test that we can import the state schemas."""
        try:
            from haive.agents.rag.multi_agent_rag.additional_workflows import (
                MemoryRAGState,
                MultiQueryRAGState,
                SelfRAGState,
            )
            from haive.agents.rag.multi_agent_rag.advanced_workflows import (
                AgenticRAGState,
                GraphRAGState,
            )

            assert True  # Import succeeded
        except ImportError as e:
            pytest.fail(f"Failed to import state schemas: {e}")


if __name__ == "__main__":
    pytest.main([__file__])
