# src/haive/agents/task_analysis/context/models.py

from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class ContextSize(str, Enum):
    """Size categories for context."""

    MINIMAL = "minimal"  # < 500 tokens
    SMALL = "small"  # 500-2k tokens
    MEDIUM = "medium"  # 2k-10k tokens
    LARGE = "large"  # 10k-50k tokens
    MASSIVE = "massive"  # 50k+ tokens


class ContextFreshness(str, Enum):
    """How recent context needs to be."""

    REALTIME = "realtime"  # Live data needed
    RECENT = "recent"  # Hours to days old
    CURRENT = "current"  # Weeks to months old
    HISTORICAL = "historical"  # Any age acceptable


class ContextDomain(BaseModel):
    """A domain of knowledge required."""

    domain_name: str = Field(..., description="Domain identifier")
    expertise_level: Literal["basic", "intermediate", "advanced", "expert"] = "basic"
    specific_topics: list[str] = Field(default_factory=list)

    # Sources
    preferred_sources: list[str] = Field(default_factory=list)
    required_sources: list[str] = Field(default_factory=list)


class ContextFlow(BaseModel):
    """How context flows between tasks."""

    source_task_id: str
    target_task_id: str

    # What flows
    data_keys: list[str] = Field(default_factory=list)
    transformations: list[str] = Field(default_factory=list)

    # How it flows
    flow_type: Literal["direct", "transformed", "aggregated", "filtered"] = "direct"
    is_required: bool = Field(default=True)


class ContextRequirement(BaseModel):
    """Complete context requirements for a task."""

    # Size and scope
    size: ContextSize = Field(default=ContextSize.MINIMAL)
    estimated_tokens: int | None = None

    # Domains
    domains: list[ContextDomain] = Field(default_factory=list)

    # Freshness
    freshness: ContextFreshness = Field(default=ContextFreshness.CURRENT)

    # Specific requirements
    required_information: list[str] = Field(default_factory=list)
    optional_information: list[str] = Field(default_factory=list)

    # Integration
    integration_points: list[str] = Field(
        default_factory=list, description="Other contexts this must integrate with"
    )

    # Transformations
    preprocessing_steps: list[str] = Field(default_factory=list)
    postprocessing_steps: list[str] = Field(default_factory=list)

    # Constraints
    must_exclude: list[str] = Field(default_factory=list)
    quality_requirements: list[str] = Field(default_factory=list)

    def merge_with(self, other: "ContextRequirement") -> "ContextRequirement":
        """Merge two context requirements."""
        # Take maximum size
        size_order = [
            ContextSize.MINIMAL,
            ContextSize.SMALL,
            ContextSize.MEDIUM,
            ContextSize.LARGE,
            ContextSize.MASSIVE,
        ]
        merged_size = max(self.size, other.size, key=lambda s: size_order.index(s))

        # Take most stringent freshness
        fresh_order = [
            ContextFreshness.HISTORICAL,
            ContextFreshness.CURRENT,
            ContextFreshness.RECENT,
            ContextFreshness.REALTIME,
        ]
        merged_fresh = max(
            self.freshness, other.freshness, key=lambda f: fresh_order.index(f)
        )

        # Merge domains (avoiding duplicates)
        domain_names = {d.domain_name for d in self.domains}
        merged_domains = list(self.domains)
        for domain in other.domains:
            if domain.domain_name not in domain_names:
                merged_domains.append(domain)

        return ContextRequirement(
            size=merged_size,
            estimated_tokens=max(
                self.estimated_tokens or 0, other.estimated_tokens or 0
            ),
            domains=merged_domains,
            freshness=merged_fresh,
            required_information=list(
                set(self.required_information + other.required_information)
            ),
            optional_information=list(
                set(self.optional_information + other.optional_information)
            ),
            integration_points=list(
                set(self.integration_points + other.integration_points)
            ),
            preprocessing_steps=list(
                set(self.preprocessing_steps + other.preprocessing_steps)
            ),
            postprocessing_steps=list(
                set(self.postprocessing_steps + other.postprocessing_steps)
            ),
            must_exclude=list(set(self.must_exclude + other.must_exclude)),
            quality_requirements=list(
                set(self.quality_requirements + other.quality_requirements)
            ),
        )


class ContextAnalysis(BaseModel):
    """Complete context analysis for a task plan."""

    # Overall requirements
    total_context_requirement: ContextRequirement

    # Per-task requirements
    task_contexts: dict[str, ContextRequirement] = Field(default_factory=dict)

    # Context flow
    context_flows: list[ContextFlow] = Field(default_factory=list)

    # Aggregated metrics
    total_estimated_tokens: int = Field(default=0)
    unique_domains: list[str] = Field(default_factory=list)

    # Loading strategy
    loading_strategy: Literal["eager", "lazy", "streaming"] = "lazy"
    caching_strategy: Literal["none", "lru", "full"] = "lru"

    # Risks
    context_risks: list[str] = Field(default_factory=list)
    mitigation_strategies: list[str] = Field(default_factory=list)
