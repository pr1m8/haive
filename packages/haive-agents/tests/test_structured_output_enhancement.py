"""Test Structured Output Enhancement Pattern.

Tests the new modular approach where any agent can be enhanced with structured
output by appending a SimpleAgent with appropriate Pydantic models.
"""

from typing import List

import pytest
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document

from haive.agents.rag.hyde.enhanced_agent import (
    EnhancedHyDERAGAgent,
    create_enhanced_hyde_agent,
    demonstrate_enhancement_vs_traditional,
)
from haive.agents.rag.models import FusionResult, HyDEResult
from haive.agents.rag.utils.structured_output_enhancer import (
    RAGEnhancementFactory,
    StructuredOutputEnhancer,
    create_fusion_enhancer,
    create_hyde_enhancer,
)


class TestStructuredOutputEnhancer:
    """Test the structured output enhancement utility."""

    @pytest.fixture
    def sample_documents(self) -> list[Document]:
        """Create sample documents for testing."""
        return [
            Document(
                page_content="Machine learning is a subset of AI that uses algorithms to learn patterns from data.",
                metadata={"source": "ml_intro", "topic": "machine_learning"},
            ),
            Document(
                page_content="Neural networks are computational models inspired by biological neural networks.",
                metadata={"source": "nn_overview", "topic": "neural_networks"},
            ),
            Document(
                page_content="Deep learning uses multiple layers to model complex patterns in data.",
                metadata={"source": "dl_guide", "topic": "deep_learning"},
            ),
        ]

    @pytest.fixture
    def test_llm_config(self) -> AzureLLMConfig:
        """Create test LLM configuration."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="https://test-endpoint.openai.azure.com/",
            api_key="test-api-key",
            api_version="2024-02-15-preview",
        )

    def test_structured_output_enhancer_creation(self):
        """Test creating structured output enhancers."""
        # Test HyDE enhancer
        hyde_enhancer = create_hyde_enhancer()
        assert hyde_enhancer.output_model == HyDEResult

        # Test Fusion enhancer
        fusion_enhancer = create_fusion_enhancer()
        assert fusion_enhancer.output_model == FusionResult

        # Test custom enhancer
        from pydantic import BaseModel, Field

        class CustomModel(BaseModel):
            result: str = Field(description="Custom result")
            confidence: float = Field(description="Confidence score")

        custom_enhancer = StructuredOutputEnhancer(CustomModel)
        assert custom_enhancer.output_model == CustomModel

    def test_format_instructions_generation(self):
        """Test that format instructions are generated correctly."""
        hyde_enhancer = create_hyde_enhancer()
        format_instructions = hyde_enhancer.create_format_instructions()

        # Should contain model field information
        assert "hypothetical_doc" in format_instructions
        assert "refined_query" in format_instructions
        assert "confidence" in format_instructions

    def test_enhancement_prompt_creation(self):
        """Test prompt template creation for enhancement."""
        hyde_enhancer = create_hyde_enhancer()

        prompt = hyde_enhancer.create_enhancement_prompt(
            context_prompt="Generate hypothetical documents", include_state_context=True
        )

        # Check prompt structure
        assert len(prompt.messages) == 2
        assert "Generate hypothetical documents" in str(prompt.messages[0])
        assert "{query}" in str(prompt.messages[1])
        assert "{context}" in str(prompt.messages[1])

    def test_enhancement_agent_creation(self, test_llm_config):
        """Test creating enhancement agents."""
        hyde_enhancer = create_hyde_enhancer()

        enhancement_agent = hyde_enhancer.create_enhancement_agent(
            llm_config=test_llm_config,
            context_prompt="Generate structured HyDE analysis",
        )

        # Verify agent structure
        assert enhancement_agent is not None
        assert hasattr(enhancement_agent, "engine")
        assert enhancement_agent.engine.structured_output_model == HyDEResult
        assert enhancement_agent.engine.output_key == "hyderesult_result"

    def test_agent_sequence_enhancement(self, test_llm_config):
        """Test enhancing a sequence of agents."""
        hyde_enhancer = create_hyde_enhancer()

        # Mock base agents (empty list for testing)
        base_agents = []

        enhanced_agents = hyde_enhancer.enhance_agent_sequence(
            agents=base_agents,
            llm_config=test_llm_config,
            context_prompt="Enhance with HyDE analysis",
        )

        # Should have one more agent than input
        assert len(enhanced_agents) == len(base_agents) + 1

        # Last agent should be the enhancement agent
        enhancement_agent = enhanced_agents[-1]
        assert enhancement_agent.engine.structured_output_model == HyDEResult

    def test_rag_enhancement_factory(self, test_llm_config):
        """Test the RAG enhancement factory."""
        # Test different enhancement types
        enhancement_types = ["hyde", "fusion", "speculative", "memory"]

        for enhancement_type in enhancement_types:
            enhanced_agents = RAGEnhancementFactory.enhance_simple_rag(
                llm_config=test_llm_config, enhancement_type=enhancement_type
            )

            assert len(enhanced_agents) >= 1
            # Last agent should have appropriate structured output
            enhancement_agent = enhanced_agents[-1]
            assert enhancement_agent.engine.structured_output_model is not None


class TestEnhancedHyDEAgent:
    """Test the Enhanced HyDE RAG Agent implementation."""

    @pytest.fixture
    def sample_documents(self) -> list[Document]:
        """Create sample documents for testing."""
        return [
            Document(
                page_content="Machine learning algorithms learn patterns from training data.",
                metadata={"source": "ml_basics"},
            ),
            Document(
                page_content="Neural networks consist of interconnected nodes processing information.",
                metadata={"source": "nn_fundamentals"},
            ),
        ]

    @pytest.fixture
    def test_llm_config(self) -> AzureLLMConfig:
        """Create test LLM configuration."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="https://test-endpoint.openai.azure.com/",
            api_key="test-api-key",
        )

    def test_enhanced_hyde_agent_creation(self, sample_documents, test_llm_config):
        """Test creating Enhanced HyDE agents with both patterns."""
        # Test enhancement pattern
        enhanced_agent = create_enhanced_hyde_agent(
            documents=sample_documents,
            llm_config=test_llm_config,
            use_enhancement_pattern=True,
        )

        assert enhanced_agent is not None
        assert (
            len(enhanced_agent.agents) == 4
        )  # Base + Enhancement + Retriever + Answer

        # Test traditional pattern
        traditional_agent = create_enhanced_hyde_agent(
            documents=sample_documents,
            llm_config=test_llm_config,
            use_enhancement_pattern=False,
        )

        assert traditional_agent is not None
        assert len(traditional_agent.agents) == 3  # Generator + Retriever + Answer

    def test_enhanced_hyde_agent_structure(self, sample_documents, test_llm_config):
        """Test the structure of Enhanced HyDE agents."""
        agent = EnhancedHyDERAGAgent.from_documents(
            documents=sample_documents,
            llm_config=test_llm_config,
            use_enhancement_pattern=True,
        )

        # Verify agent sequence
        agents = agent.agents
        assert len(agents) == 4

        # Check agent names
        agent_names = [a.name for a in agents]
        assert "Base HyDE Generator" in agent_names
        assert "HyDE Structure Enhancer" in agent_names
        assert "Enhanced HyDE Retriever" in agent_names
        assert "Answer Generator" in agent_names

    def test_enhanced_retriever_adaptive_behavior(
        self, sample_documents, test_llm_config
    ):
        """Test that the enhanced retriever adapts to different input patterns."""
        from haive.agents.rag.hyde.enhanced_agent import EnhancedHyDERetriever

        retriever = EnhancedHyDERetriever(
            documents=sample_documents, name="Test Retriever"
        )

        # Build graph to access the retrieval function
        graph = retriever.build_graph()
        assert graph is not None
        assert "adaptive_retrieve" in graph.nodes

    def test_pattern_comparison_demo(self):
        """Test the pattern comparison demonstration."""
        demo_result = demonstrate_enhancement_vs_traditional()

        assert "enhanced" in demo_result
        assert "traditional" in demo_result
        assert "pattern_benefits" in demo_result

        # Verify both agents were created
        enhanced_agent = demo_result["enhanced"]
        traditional_agent = demo_result["traditional"]

        assert enhanced_agent is not None
        assert traditional_agent is not None
        assert len(enhanced_agent.agents) > len(traditional_agent.agents)


def run_structured_output_enhancement_tests():
    """Run structured output enhancement tests and return results."""
    # Create test instances
    enhancer_test = TestStructuredOutputEnhancer()
    hyde_test = TestEnhancedHyDEAgent()

    # Create fixtures
    sample_docs = [
        Document(
            page_content="Machine learning uses algorithms to learn from data.",
            metadata={"source": "test", "topic": "ml"},
        ),
        Document(
            page_content="Neural networks process information through connections.",
            metadata={"source": "test", "topic": "nn"},
        ),
    ]

    test_llm_config = AzureLLMConfig(
        deployment_name="gpt-4",
        azure_endpoint="https://test.openai.azure.com/",
        api_key="test-key",
    )

    # Run tests
    test_methods = [
        (
            "test_structured_output_enhancer_creation",
            lambda: enhancer_test.test_structured_output_enhancer_creation(),
        ),
        (
            "test_format_instructions_generation",
            lambda: enhancer_test.test_format_instructions_generation(),
        ),
        (
            "test_enhancement_prompt_creation",
            lambda: enhancer_test.test_enhancement_prompt_creation(),
        ),
        (
            "test_enhancement_agent_creation",
            lambda: enhancer_test.test_enhancement_agent_creation(test_llm_config),
        ),
        (
            "test_agent_sequence_enhancement",
            lambda: enhancer_test.test_agent_sequence_enhancement(test_llm_config),
        ),
        (
            "test_rag_enhancement_factory",
            lambda: enhancer_test.test_rag_enhancement_factory(test_llm_config),
        ),
        (
            "test_enhanced_hyde_agent_creation",
            lambda: hyde_test.test_enhanced_hyde_agent_creation(
                sample_docs, test_llm_config
            ),
        ),
        (
            "test_enhanced_hyde_agent_structure",
            lambda: hyde_test.test_enhanced_hyde_agent_structure(
                sample_docs, test_llm_config
            ),
        ),
        (
            "test_enhanced_retriever_adaptive_behavior",
            lambda: hyde_test.test_enhanced_retriever_adaptive_behavior(
                sample_docs, test_llm_config
            ),
        ),
        (
            "test_pattern_comparison_demo",
            lambda: hyde_test.test_pattern_comparison_demo(),
        ),
    ]

    results = {"passed": 0, "failed": 0, "errors": []}

    for method_name, test_func in test_methods:
        try:
            test_func()
            results["passed"] += 1
        except Exception as e:
            results["failed"] += 1
            results["errors"].append(f"{method_name}: {e}")

    return results


if __name__ == "__main__":
    run_structured_output_enhancement_tests()
