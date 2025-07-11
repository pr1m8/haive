import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator, model_validator

from haive.agents.ltm.memory_schemas import UserPreference
from haive.agents.memory.models.base import BaseMemoryModel
from haive.agents.memory.models.semantic.mixins import TemporalMixin, UserContextMixin


class SemanticMemory(BaseMemoryModel, UserContextMixin, TemporalMixin):
    """Advanced semantic memory with comprehensive user modeling."""

    __memory_type__ = "semantic"
    __validation_level__ = "enterprise"

    user_id: str = Field(
        ..., min_length=1, max_length=100, description="User identifier"
    )

    # Core semantic data
    personality_profile: PersonalityTraits = Field(default_factory=PersonalityTraits)
    preferences: UserPreference = Field(default_factory=UserPreferences)
    factual_knowledge: dict[str, Any] = Field(
        default_factory=dict, description="Structured factual data"
    )

    # Advanced semantic features
    concept_graph: dict[str, list[str]] = Field(
        default_factory=dict, description="Concept relationships"
    )
    belief_system: dict[str, float] = Field(
        default_factory=dict, description="Belief strengths (0-1)"
    )
    temporal_weight: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Temporal relevance weight"
    )

    # Semantic search optimization
    embedding_vector: list[float] | None = Field(None, description="Semantic embedding")
    semantic_keywords: list[str] = Field(
        default_factory=list, description="Optimized keywords"
    )

    @field_validator("user_id")
    @classmethod
    def validate_user_id(cls, v: str) -> str:
        """Enhanced user ID validation."""
        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "User ID must contain only alphanumeric characters, hyphens, and underscores"
            )
        return v.lower()

    @field_validator("concept_graph")
    @classmethod
    def validate_concept_graph(cls, v: dict[str, list[str]]) -> dict[str, list[str]]:
        """Validate concept graph structure."""
        for concept, related in v.items():
            if len(related) > 50:
                raise ValueError(f"Concept '{concept}' has too many relations (max 50)")

            # Ensure no self-references
            if concept in related:
                related.remove(concept)

        return v

    @model_validator(mode="after")
    def validate_semantic_consistency(self) -> "SemanticMemory":
        """Advanced semantic consistency validation."""
        # Validate belief system consistency
        for belief, strength in self.belief_system.items():
            if not 0.0 <= strength <= 1.0:
                raise ValueError(
                    f"Belief strength for '{belief}' must be between 0.0 and 1.0"
                )

        # Auto-generate semantic keywords from factual knowledge
        if not self.semantic_keywords and self.factual_knowledge:
            self.semantic_keywords = self._extract_keywords(self.factual_knowledge)

        return self

    def _extract_keywords(self, data: dict[str, Any]) -> list[str]:
        """Extract semantic keywords from factual knowledge."""
        keywords = []
        for key, value in data.items():
            keywords.append(key.lower())
            if isinstance(value, str):
                # Simple keyword extraction (could be enhanced with NLP)
                words = re.findall(r"\b[a-zA-Z]+\b", value.lower())
                keywords.extend([w for w in words if len(w) > 3])

        return list(set(keywords))[:20]  # Limit to 20 keywords

    def get_context_summary(self) -> str:
        """Generate comprehensive context summary."""
        return f"""
        User: {self.user_id}
        Communication Style: {self.personality_profile.communication_style}
        Expertise: {', '.join(self.personality_profile.expertise_areas[:3])}
        Recent Activity: {self.access_count} interactions
        Temporal Relevance: {self.calculate_temporal_relevance():.2f}
        Key Interests: {', '.join(self.preferences.topics_of_interest[:3])}
        """

    def update_context(self, new_data: dict[str, Any]) -> None:
        """Intelligently update contextual information."""
        for key, value in new_data.items():
            if key in ["personality_traits", "communication_style"]:
                # Update personality profile
                if hasattr(self.personality_profile, key):
                    setattr(self.personality_profile, key, value)
            elif key in ["preferences", "privacy_level"]:
                # Update preferences
                if hasattr(self.preferences, key):
                    setattr(self.preferences, key, value)
            else:
                # Add to factual knowledge
                self.factual_knowledge[key] = value

        # Re-extract keywords
        self.semantic_keywords = self._extract_keywords(self.factual_knowledge)
