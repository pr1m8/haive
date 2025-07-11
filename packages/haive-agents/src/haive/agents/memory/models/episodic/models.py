import re
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from haive.agents.memory.models.base import BaseMemoryModel
from haive.agents.memory.models.episodic.mixins import (
    PerformanceMetrics,
    TaskExecution,
    TemporalMixin,
)


class EpisodicMemory(BaseMemoryModel, TemporalMixin):
    """Sophisticated episodic memory for learning from experiences."""

    __memory_type__ = "episodic"
    __validation_level__ = "enterprise"

    user_id: str = Field(..., description="Associated user ID")
    session_id: str = Field(..., description="Session identifier")

    # Task context
    task_execution: TaskExecution = Field(..., description="Execution details")
    performance_metrics: PerformanceMetrics = Field(default_factory=PerformanceMetrics)

    # Learning data
    user_input: str = Field(
        ..., min_length=1, max_length=5000, description="Original user input"
    )
    agent_response: str = Field(
        ..., min_length=1, max_length=10000, description="Agent response"
    )
    outcome_classification: Literal[
        "success", "partial_success", "failure", "error"
    ] = Field(default="success", description="Outcome classification")

    # Context and environment
    environmental_context: dict[str, Any] = Field(
        default_factory=dict, description="Execution environment"
    )
    feedback_received: str | None = Field(None, description="User feedback")
    lessons_learned: list[str] = Field(
        default_factory=list, description="Extracted lessons"
    )

    # Similarity and clustering
    similarity_cluster: str | None = Field(None, description="Similarity cluster ID")
    temporal_weight: float = Field(default=1.0, description="Temporal relevance weight")

    @field_validator("user_input", "agent_response")
    @classmethod
    def validate_content_safety(cls, v: str) -> str:
        """Basic content safety validation."""
        if not v.strip():
            raise ValueError("Content cannot be empty")

        # Basic PII detection (simplified)
        pii_patterns = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN pattern
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # Email
        ]

        for pattern in pii_patterns:
            if re.search(pattern, v):
                # In production, you might want to mask or handle PII differently
                pass  # For now, just detect

        return v.strip()

    @model_validator(mode="after")
    def validate_episodic_consistency(self) -> "EpisodicMemory":
        """Validate episodic memory consistency."""
        # Performance metrics should align with outcome
        if (
            self.outcome_classification == "success"
            and self.performance_metrics.success_rate < 0.5
        ):
            self.performance_metrics.success_rate = 0.8  # Auto-correct for consistency

        elif (
            self.outcome_classification == "failure"
            and self.performance_metrics.success_rate > 0.5
        ):
            self.performance_metrics.success_rate = 0.2

        # Auto-extract lessons from feedback
        if self.feedback_received and not self.lessons_learned:
            self.lessons_learned = self._extract_lessons_from_feedback()

        return self

    def _extract_lessons_from_feedback(self) -> list[str]:
        """Extract actionable lessons from user feedback."""
        if not self.feedback_received:
            return []

        # Simple lesson extraction (could be enhanced with NLP)
        lessons = []
        feedback_lower = self.feedback_received.lower()

        if "too long" in feedback_lower or "verbose" in feedback_lower:
            lessons.append("Keep responses more concise")

        if "not clear" in feedback_lower or "confusing" in feedback_lower:
            lessons.append("Improve response clarity")

        if "helpful" in feedback_lower or "good" in feedback_lower:
            lessons.append("Continue current approach")

        return lessons

    def calculate_learning_value(self) -> float:
        """Calculate the learning value of this episodic memory."""
        base_value = self.performance_metrics.success_rate

        # Boost value for complex tasks
        complexity_boost = self.performance_metrics.complexity_score * 0.05

        # Reduce value for very old memories
        temporal_factor = self.calculate_temporal_relevance()

        # Boost for memories with explicit feedback
        feedback_boost = 0.2 if self.feedback_received else 0.0

        return (
            min(base_value + complexity_boost + feedback_boost, 1.0) * temporal_factor
        )
