"""
Enhanced State Schemas with Configuration Support

This module provides state schemas that include configuration fields,
solving the issue of storing agent-specific configuration in a clean way.
"""

from typing import Any, Dict, List, Optional

from haive.core.schema.prebuilt.rag_state import RAGState
from pydantic import Field

from haive.agents.rag.multi_agent_rag.grading_components import (
    AnswerGrade,
    DocumentGrade,
    HallucinationGrade,
)


class ConfigurableRAGState(RAGState):
    """Base RAG state with configuration support"""

    # Configuration fields
    config: Dict[str, Any] = Field(
        default_factory=dict, description="Agent configuration parameters"
    )

    # Common configuration shortcuts
    relevance_threshold: float = Field(
        default=0.5, description="Threshold for document relevance filtering"
    )
    max_documents: int = Field(
        default=10, description="Maximum number of documents to use"
    )

    # Metadata
    agent_name: str = Field(
        default="", description="Name of the agent using this state"
    )
    workflow_type: str = Field(
        default="", description="Type of RAG workflow being executed"
    )


class GradedRAGState(ConfigurableRAGState):
    """RAG state with grading information and configuration"""

    # Query analysis
    query_type: str = ""
    query_complexity: str = ""
    key_entities: List[str] = []

    # Document grading
    document_grades: List[DocumentGrade] = []
    priority_ranking: Dict[str, float] = {}
    filtered_documents: List[str] = []

    # Answer grading
    answer_grade: Optional[AnswerGrade] = None
    hallucination_grade: Optional[HallucinationGrade] = None

    # Pipeline metrics
    overall_score: float = 0.0
    improvement_suggestions: List[str] = []

    # Grading configuration
    grading_criteria: List[str] = Field(
        default_factory=lambda: ["relevance", "accuracy", "completeness"],
        description="Criteria to use for grading",
    )
    grading_weights: Dict[str, float] = Field(
        default_factory=dict, description="Weights for different grading criteria"
    )


class FLAREState(ConfigurableRAGState):
    """FLARE state with configuration support"""

    current_generation: str = ""
    uncertainty_tokens: List[str] = []
    active_retrieval_points: List[int] = []
    generation_segments: List[str] = []
    confidence_scores: List[float] = []
    retrieval_triggers: List[str] = []

    # FLARE configuration
    uncertainty_threshold: float = Field(
        default=0.3, description="Threshold for triggering active retrieval"
    )
    max_retrieval_rounds: int = Field(
        default=3, description="Maximum number of active retrieval rounds"
    )


class DynamicRAGState(ConfigurableRAGState):
    """Dynamic RAG state with configuration support"""

    active_retrievers: Dict[str, Dict[str, Any]] = {}
    retriever_performance: Dict[str, float] = {}
    document_sources: Dict[str, List[str]] = {}
    retriever_configurations: Dict[str, Any] = {}
    adaptive_threshold: float = 0.7

    # Dynamic RAG configuration
    min_retrievers: int = Field(
        default=1, description="Minimum number of active retrievers"
    )
    max_retrievers: int = Field(
        default=5, description="Maximum number of active retrievers"
    )
    performance_threshold: float = Field(
        default=0.6, description="Minimum performance to keep retriever active"
    )


class DebateRAGState(ConfigurableRAGState):
    """Debate RAG state with configuration support"""

    debate_positions: Dict[str, str] = {}
    arguments_by_position: Dict[str, List[str]] = {}
    evidence_by_position: Dict[str, List[str]] = {}
    debate_rounds: int = 0
    synthesis_attempts: List[str] = []
    consensus_reached: bool = False
    final_answer: str = ""
    debate_winner: Optional[str] = None

    # Debate configuration
    position_names: List[str] = Field(
        default_factory=list, description="Names of debate positions"
    )
    max_debate_rounds: int = Field(default=3, description="Maximum rounds of debate")
    require_consensus: bool = Field(
        default=False, description="Whether consensus is required to end debate"
    )
    enable_judge: bool = Field(
        default=False, description="Whether to include a judge for the debate"
    )


class AdaptiveThresholdRAGState(DynamicRAGState):
    """Adaptive threshold state extending Dynamic RAG state"""

    # Additional fields specific to adaptive threshold
    query_complexity_score: float = 0.0
    threshold_adjustments: List[float] = []
    retrieval_rounds: int = 0

    # Adaptive configuration
    initial_threshold: float = Field(
        default=0.7, description="Starting retrieval threshold"
    )
    threshold_step: float = Field(
        default=0.1, description="Amount to adjust threshold by"
    )
    min_threshold: float = Field(default=0.3, description="Minimum allowed threshold")
    max_threshold: float = Field(default=0.95, description="Maximum allowed threshold")


# Helper function to create state with configuration
def create_configured_state(
    state_class: type[ConfigurableRAGState],
    agent_name: str,
    workflow_type: str,
    **config_kwargs
) -> ConfigurableRAGState:
    """Create a state instance with configuration"""
    # Extract fields that belong to the state class
    state_fields = {}
    config_fields = {}

    for key, value in config_kwargs.items():
        if hasattr(state_class, key):
            state_fields[key] = value
        else:
            config_fields[key] = value

    # Create state with direct fields
    state = state_class(
        agent_name=agent_name, workflow_type=workflow_type, **state_fields
    )

    # Add additional config
    state.config.update(config_fields)

    return state


# Example usage in MultiAgent classes
class StateConfigMixin:
    """Mixin to help MultiAgent classes work with configured states"""

    def get_state_config(self, state: ConfigurableRAGState) -> Dict[str, Any]:
        """Extract configuration from state"""
        config = state.config.copy()

        # Add standard fields if they exist
        for field in ["relevance_threshold", "max_documents", "grading_criteria"]:
            if hasattr(state, field):
                config[field] = getattr(state, field)

        return config

    def update_state_config(self, state: ConfigurableRAGState, **updates) -> None:
        """Update configuration in state"""
        for key, value in updates.items():
            if hasattr(state, key):
                setattr(state, key, value)
            else:
                state.config[key] = value
