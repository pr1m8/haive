from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.rag.base.config import BaseRAGConfig
from haive.agents.rag.self_corr.state import SelfCorrectiveRAGState


class SelfCorrectiveRAGConfig(BaseRAGConfig):
    """Configuration for self-corrective RAG agents that can evaluate and improve their answers.

    This RAG implementation extends the base RAG with:
    1. Answer evaluation to detect hallucinations
    2. Answer correction to fix identified issues
    3. Iterative improvement until quality threshold is met
    """

    # State schema
    state_schema: type = Field(
        default=SelfCorrectiveRAGState,
        description="State schema for self-corrective RAG",
    )

    # LLM Configurations for evaluation and correction
    answer_evaluator_config: AugLLMConfig | None = Field(
        default=None,
        description="Configuration for the LLM that evaluates answer quality",
    )

    answer_corrector_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for the LLM that corrects answers"
    )

    # Document filtering options
    document_filter_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for document filtering"
    )

    relevance_threshold: float = Field(
        default=0.7, description="Threshold for document relevance (0.0 to 1.0)"
    )

    # Correction parameters
    max_correction_iterations: int = Field(
        default=2, description="Maximum number of correction iterations"
    )

    minimum_answer_score: float = Field(
        default=0.8, description="Minimum acceptable answer score (0.0 to 1.0)"
    )
