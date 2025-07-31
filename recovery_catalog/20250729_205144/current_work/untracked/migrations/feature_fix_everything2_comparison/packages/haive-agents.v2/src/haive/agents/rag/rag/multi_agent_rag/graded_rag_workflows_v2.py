"""Graded RAG Workflows V2 - Using Enhanced State Schemas.

This version uses state schemas with built-in configuration support,
providing a cleaner approach to managing agent-specific parameters.
"""

from typing import Any

from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.rag.multi_agent_rag.enhanced_state_schemas import (
    GradedRAGState,
    StateConfigMixin,
)
from haive.agents.rag.multi_agent_rag.grading_components import (
    create_answer_grader,
    create_document_grader,
    create_hallucination_grader,
    create_priority_ranker,
    create_query_analyzer,
)
from haive.agents.simple import SimpleAgent


class FullyGradedRAGAgentV2(MultiAgent, StateConfigMixin):
    """Fully Graded RAG V2 - Uses enhanced state schema with configuration support."""

    def __init__(self, relevance_threshold: float = 0.5, **kwargs):
        # Create agents
        query_analyzer = create_query_analyzer("query_analyzer")

        retriever = SimpleAgent(
            name="retriever",
            instructions="""
            Retrieve documents based on the query and analysis.
            Use the state's relevance_threshold and max_documents configuration.
            """,
            output_schema={
                "documents": "List[str]",
                "retrieval_strategy": "str",
                "num_retrieved": "int",
            },
        )

        document_grader = create_document_grader("document_relevance_grader")
        priority_ranker = create_priority_ranker("document_priority_ranker")

        filter_agent = SimpleAgent(
            name="document_filter",
            instructions="""
            Filter documents based on relevance grades and priority ranking.
            Use the relevance_threshold from state configuration.
            Respect max_documents limit from state.
            """,
            output_schema={
                "filtered_documents": "List[str]",
                "num_filtered": "int",
                "filter_stats": "Dict[str, Any]",
            },
        )

        answer_generator = SimpleAgent(
            name="graded_answer_generator",
            instructions="""
            Generate answer using filtered documents.
            Consider grading_criteria from state configuration.
            """,
            output_schema={
                "answer": "str",
                "sources_used": "List[str]",
                "confidence": "float",
            },
        )

        answer_grader = create_answer_grader("answer_quality_grader")
        hallucination_grader = create_hallucination_grader("hallucination_detector")

        synthesis_agent = SimpleAgent(
            name="grade_synthesis",
            instructions="""
            Synthesize all grading information.
            Use grading_weights from state configuration if available.
            """,
            output_schema={
                "overall_score": "float",
                "meets_threshold": "bool",
                "summary": "stf",
            },
        )

        agents = [
            query_analyzer,
            retriever,
            document_grader,
            priority_ranker,
            filter_agent,
            answer_generator,
            answer_grader,
            hallucination_grader,
            synthesis_agent,
        ]

        # Initialize with enhanced state schema
        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

        # Store initial configuration as private attribute
        self._initial_config = {
            "relevance_threshold": relevance_threshold,
            "workflow_type": "fully_graded_rag",
        }

    def build_custom_graph(self) -> Any:
        """Build the custom graph with state initialization."""
        # In a real implementation, you would initialize state here
        # For now, return None to use default
        return

    async def ainvoke(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Override to inject configuration into state."""
        # Ensure state has our configuration
        if "relevance_threshold" not in inputs:
            inputs["relevance_threshold"] = self._initial_config["relevance_threshold"]
        if "workflow_type" not in inputs:
            inputs["workflow_type"] = self._initial_config["workflow_type"]

        return await super().ainvoke(inputs)


class MultiCriteriaGradedRAGAgentV2(MultiAgent, StateConfigMixin):
    """Multi-Criteria Graded RAG V2 - Configuration stored in state schema."""

    def __init__(self, grading_criteria: list[str] | None = None, **kwargs):
        if grading_criteria is None:
            grading_criteria = [
                "relevance",
                "accuracy",
                "completeness",
                "clarity",
                "authority",
            ]

        multi_criteria_grader = SimpleAgent(
            name="multi_criteria_grader",
            instructions="""
            Grade documents using criteria from state.grading_criteria.
            Apply weights from state.grading_weights if available.
            """,
            output_schema={
                "document_id": "str",
                "criteria_scores": "Dict[str, float]",
                "composite_score": "float",
            },
        )

        perspective_aggregator = SimpleAgent(
            name="perspective_aggregator",
            instructions="""
            Aggregate grades considering state.grading_criteria priorities.
            Use state.config for any additional parameters.
            """,
            output_schema={
                "aggregated_scores": "Dict[str, float]",
                "recommendations": "List[str]",
            },
        )

        balanced_generator = SimpleAgent(
            name="balanced_answer_generator",
            instructions="""
            Generate answer balancing all criteria from state.grading_criteria.
            """,
            output_schema={"answer": "str", "criteria_addressed": "Dict[str, bool]"},
        )

        agents = [multi_criteria_grader, perspective_aggregator, balanced_generator]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

        self._initial_config = {
            "grading_criteria": grading_criteria,
            "workflow_type": "multi_criteria_graded_rag",
        }

    async def ainvoke(self, inputs: dict[str, Any]) -> dict[str, Any]:
        """Override to inject configuration."""
        if "grading_criteria" not in inputs:
            inputs["grading_criteria"] = self._initial_config["grading_criteria"]
        if "workflow_type" not in inputs:
            inputs["workflow_type"] = self._initial_config["workflow_type"]

        return await super().ainvoke(inputs)


# Example of how to use with specialized workflows
class FLAREAgentV2Example(MultiAgent, StateConfigMixin):
    """FLARE Agent V2 example using enhanced state schema."""

    def __init__(
        self,
        uncertainty_threshold: float = 0.3,
        max_retrieval_rounds: int = 3,
        **kwargs,
    ):
        from haive.agents.rag.multi_agent_rag.enhanced_state_schemas import FLAREState

        # Create a simple agent for example
        monitor = SimpleAgent(
            name="monitor",
            instructions="Monitor for uncertainty",
            output_schema={"uncertainty": "bool"},
        )

        super().__init__(
            agents=[monitor],
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=FLAREState,
            **kwargs,
        )

        self._initial_config = {
            "uncertainty_threshold": uncertainty_threshold,
            "max_retrieval_rounds": max_retrieval_rounds,
            "workflow_type": "flare",
        }

    def build_custom_graph(self) -> Any:
        """Build custom graph."""
        return


# Helper function to create properly configured agents
def create_graded_rag_agent(
    workflow_type: str = "fully_graded",
    relevance_threshold: float = 0.5,
    grading_criteria: list[str] | None = None,
    **kwargs,
) -> MultiAgent:
    """Factory function to create graded RAG agents with proper configuration."""
    if workflow_type == "fully_graded":
        return FullyGradedRAGAgentV2(relevance_threshold=relevance_threshold, **kwargs)
    if workflow_type == "multi_criteria":
        return MultiCriteriaGradedRAGAgentV2(
            grading_criteria=grading_criteria, **kwargs
        )
    raise ValueError(f"Unknown workflow type: {workflow_type}")


# Example usage showing the clean interface
if __name__ == "__main__":
    # Create agent with configuration
    agent = create_graded_rag_agent(
        workflow_type="fully_graded", relevance_threshold=0.7, name="production_rag"
    )

    # Configuration is stored in state, not agent
    # When invoking, state will have all configuration
    result = agent.invoke(
        {
            "query": "What is quantum computing?",
            # Can override configuration per-invocation
            "relevance_threshold": 0.8,
            "max_documents": 5,
        }
    )
