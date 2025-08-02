from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class UserContextMixin:
    """Mixin for user-specific context management."""

    def get_context_summary(self) -> str:
        """Generate contextual summary."""
        raise NotImplementedError

    def update_context(self, new_data: dict[str, Any]) -> None:
        """Update contextual information."""
        raise NotImplementedError


class TemporalMixin:
    """Mixin for temporal memory management."""

    @field_validator("temporal_weight")
    @classmethod
    def validate_temporal_weight(cls, v: float) -> float:
        """Validate temporal decay weight."""
        if not 0.0 <= v <= 1.0:
            raise ValueError("Temporal weight must be between 0.0 and 1.0")
        return v

    def calculate_temporal_relevance(self) -> float:
        """Calculate temporal relevance based on age and access patterns."""
        age_days = (datetime.now() - self.created_at).days
        decay_factor = 0.95**age_days  # Exponential decay
        access_boost = min(self.access_count * 0.1, 0.5)  # Cap access boost
        return min(decay_factor + access_boost, 1.0)


class PersonalityTraits(BaseModel):
    """Sophisticated personality modeling."""

    communication_style: Literal[
        "formal", "casual", "technical", "friendly", "direct"
    ] = Field(default="friendly", description="Preferred communication style")
    expertise_areas: list[str] = Field(
        default_factory=list, description="Known expertise areas"
    )
    interaction_preferences: dict[str, Any] = Field(
        default_factory=dict, description="Interaction preferences"
    )
    cultural_context: str | None = Field(
        None, description="Cultural background context"
    )
    language_preferences: list[str] = Field(
        default_factory=lambda: ["English"], description="Preferred languages"
    )

    @field_validator("expertise_areas")
    @classmethod
    def validate_expertise(cls, v: list[str]) -> list[str]:
        """Validate and normalize expertise areas."""
        if len(v) > 15:
            raise ValueError("Maximum 15 expertise areas allowed")

        return [area.strip().title() for area in v if area.strip()]

    @model_validator(mode="after")
    @classmethod
    def validate_personality_consistency(cls) -> "PersonalityTraits":
        """Ensure personality traits are consistent."""
        if (
            self.communication_style == "technical"
            and "Technology" not in self.expertise_areas
        ):
            # Auto-add technology expertise for technical communication style
            self.expertise_areas.append("Technology")

        return self


class UserPreferences(BaseModel):
    """Enhanced user preferences with validation."""

    notification_settings: dict[str, bool] = Field(default_factory=dict)
    privacy_level: Literal["public", "private", "restricted"] = Field(default="private")
    data_retention_days: int = Field(default=365, ge=1, le=3650)  # 1 day to 10 years
    preferred_response_length: Literal["brief", "moderate", "detailed"] = Field(
        default="moderate"
    )
    topics_of_interest: list[str] = Field(default_factory=list)
    avoided_topics: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    @classmethod
    def validate_topic_consistency(cls) -> "UserPreferences":
        """Ensure no overlap between interested and avoided topics."""
        interest_set = set(self.topics_of_interest)
        avoided_set = set(self.avoided_topics)

        overlap = interest_set & avoided_set
        if overlap:
            raise ValueError(
                f"Topics cannot be both interesting and avoided: {overlap}"
            )

        return self
