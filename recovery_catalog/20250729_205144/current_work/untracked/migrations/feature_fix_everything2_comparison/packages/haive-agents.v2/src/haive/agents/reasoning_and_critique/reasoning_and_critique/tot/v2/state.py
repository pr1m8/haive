"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    ToTState: ToTState implementation.
    ExpansionState: ExpansionState implementation.

Functions:
    update_candidates: Update Candidates functionality.
    problem: Problem functionality.
    convert_candidates: Convert Candidates functionality.
"""

import operator
from typing import Annotated, Any, Literal

from haive.core.schema.prebuilt.messages_state import MessagesState
from langchain_core.messages import HumanMessage
from pydantic import Field, computed_field, model_validator

from haive.agents.reasoning_and_critique.tot.v2.models import Candidate, ScoredCandidate


def update_candidates(
    existing: list | None = None,
    updates: list | Literal["clear"] | None = None,
) -> list:
    """Custom reducer for candidates."""
    if existing is None:
        existing = []
    if updates is None:
        return existing
    if updates == "clear":
        return []
    # Concatenate the lists
    return existing + updates


class ToTState(MessagesState):
    """Base Tree of Thoughts state."""

    # Problem is derived from messages
    problem_type: str | None = Field(
        default=None, description="Type/category of problem"
    )
    problem_context: dict[str, Any] = Field(
        default_factory=dict, description="Additional problem context"
    )

    # Core fields with proper annotations
    candidates: Annotated[list[Candidate], update_candidates] = Field(
        default_factory=list, description="Current candidates"
    )
    scored_candidates: Annotated[list[ScoredCandidate], update_candidates] = Field(
        default_factory=list, description="Scored candidates"
    )
    selected_candidates: list[ScoredCandidate] = Field(
        default_factory=list, description="Best candidates selected for next iteration"
    )
    all_candidates_history: Annotated[
        list[Candidate | ScoredCandidate], operator.add
    ] = Field(default_factory=list, description="All candidates ever generated")

    # Search parameters
    depth: Annotated[int, operator.add] = Field(default=0, description="Current depth")
    max_depth: int = Field(default=10, description="Maximum search depth")
    beam_size: int = Field(
        default=3, description="Number of candidates to keep after pruning"
    )
    expansion_factor: int = Field(
        default=5, description="Number of candidates to generate per expansion"
    )
    threshold: float = Field(
        default=0.9, description="Score threshold for early termination"
    )

    # Control flow
    should_terminate: bool = Field(
        default=False, description="Whether to terminate search"
    )
    termination_reason: str | None = Field(
        default=None, description="Why search was terminated"
    )
    best_solution: ScoredCandidate | None = Field(
        default=None, description="Best solution found so far"
    )

    # Search strategy
    search_strategy: Literal["breadth_first", "best_first", "adaptive"] = Field(
        default="best_first", description="Search strategy to use"
    )

    # Current candidate being processed (for scoring phase)
    current_candidate_id: str | None = Field(
        default=None, description="ID of candidate being scored"
    )

    # Computed field to extract problem from messages
    @computed_field
    @property
    def problem(self) -> str:
        """Extract the problem from the first human message."""
        for msg in self.messages:
            if isinstance(msg, HumanMessage):
                return msg.content
        return "No problem statement found"

    # Model validators for type conversions
    @model_validator(mode="before")
    @classmethod
    def convert_candidates(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Convert raw candidate data to proper Candidate/ScoredCandidate objects."""
        # Convert candidates
        if "candidates" in data and isinstance(data["candidates"], list):
            converted = []
            for item in data["candidates"]:
                if isinstance(item, dict) and not isinstance(
                    item, Candidate | ScoredCandidate
                ):
                    # Check if it has score to determine type
                    if "score" in item and item["score"] is not None:
                        converted.append(ScoredCandidate(**item))
                    else:
                        converted.append(Candidate(**item))
                elif not isinstance(item, Candidate | ScoredCandidate):
                    # Convert arbitrary objects to candidates
                    converted.append(Candidate(content=item))
                else:
                    converted.append(item)
            data["candidates"] = converted

        # Similar conversion for other candidate fields
        for field in [
            "scored_candidates",
            "selected_candidates",
            "all_candidates_history",
        ]:
            if field in data and isinstance(data[field], list):
                converted = []
                for item in data[field]:
                    if isinstance(item, dict) and not isinstance(
                        item, Candidate | ScoredCandidate
                    ):
                        if "score" in item and item["score"] is not None:
                            converted.append(ScoredCandidate(**item))
                        else:
                            converted.append(Candidate(**item))
                    elif not isinstance(item, Candidate | ScoredCandidate):
                        # Convert to candidate
                        converted.append(Candidate(content=item))
                    else:
                        converted.append(item)
                data[field] = converted

        return data

    # Computed fields for prompt templates
    @computed_field
    @property
    def candidates_for_expansion(self) -> str:
        """Format selected candidates for expansion prompts."""
        if not self.selected_candidates:
            return "No parent candidates - starting fresh generation."

        expansion_context = [
            f"Expanding from {len(self.selected_candidates)} parent candidates:",
            "",
        ]

        for i, candidate in enumerate(self.selected_candidates):
            expansion_context.append(f"Parent {i+1} (Score: {candidate.score:.3f}):")
            expansion_context.append(f"Content: {candidate.get_content_str()}")
            expansion_context.append(f"Feedback: {candidate.feedback}")
            if candidate.scoring_metadata:
                if "strengths" in candidate.scoring_metadata:
                    expansion_context.append(
                        f"Strengths: {', '.join(candidate.scoring_metadata['strengths'])}"
                    )
                if "weaknesses" in candidate.scoring_metadata:
                    expansion_context.append(
                        f"Weaknesses: {', '.join(candidate.scoring_metadata['weaknesses'])}"
                    )
            expansion_context.append("")

        return "\n".join(expansion_context)

    @computed_field
    @property
    def candidate_for_scoring(self) -> str:
        """Format current candidate for scoring prompt."""
        if not self.current_candidate_id:
            return "No candidate to score."

        # Find the candidate by ID
        candidate = self.get_candidate_by_id(self.current_candidate_id)
        if not candidate:
            return f"Candidate {self.current_candidate_id} not found."

        scoring_context = [
            f"Candidate ID: {candidate.id}",
            f"Depth: {candidate.depth}",
            f"Content: {candidate.get_content_str()}",
        ]

        if candidate.parent_id:
            parent = self.get_candidate_by_id(candidate.parent_id)
            if parent:
                scoring_context.append(
                    f"\nDerived from parent: {parent.get_content_str()[:100]}..."
                )

        return "\n".join(scoring_context)

    @computed_field
    @property
    def scored_candidates_summary(self) -> str:
        """Summary of scored candidates for pruning decisions."""
        if not self.scored_candidates:
            return "No candidates have been scored yet."

        sorted_scored = sorted(
            self.scored_candidates, key=lambda c: c.score, reverse=True
        )

        summary = [f"Scored candidates ({len(sorted_scored)} total):", ""]

        for i, candidate in enumerate(sorted_scored):
            summary.append(
                f"{i}. [Score: {candidate.score:.3f}] {candidate.get_content_str()[:100]}..."
            )
            summary.append(f"   Feedback: {candidate.feedback}")
            if i < len(sorted_scored) - 1:
                summary.append("")

        return "\n".join(summary)

    @computed_field
    @property
    def best_candidates_summary(self) -> str:
        """Summary of best candidates found so far."""
        if not self.selected_candidates:
            return "No candidates selected yet."

        sorted_candidates = sorted(
            self.selected_candidates, key=lambda c: c.score or 0, reverse=True
        )

        summary_parts = [f"Top {min(3, len(sorted_candidates))} candidates:"]
        for i, cand in enumerate(sorted_candidates[:3]):
            summary_parts.append(
                f"  {i+1}. Score: {cand.score:.3f} - {cand.get_content_str()[:100]}..."
            )

        return "\n".join(summary_parts)

    @computed_field
    @property
    def search_progress(self) -> str:
        """Current search progress description."""
        progress_parts = [
            "Search Progress:",
            f"  - Depth: {self.depth}/{self.max_depth}",
            f"  - Total candidates explored: {len(self.all_candidates_history)}",
            f"  - Current beam size: {len(self.selected_candidates)}/{self.beam_size}",
        ]

        if self.best_solution:
            progress_parts.append(
                f"  - Best solution score: {self.best_solution.score:.3f}"
            )

        return "\n".join(progress_parts)

    @computed_field
    @property
    def best_score(self) -> float:
        """Best score found so far."""
        if self.best_solution:
            return self.best_solution.score
        return 0.0

    # Helper methods
    def get_candidate_by_id(
        self, candidate_id: str
    ) -> Candidate | ScoredCandidate | None:
        """Find a candidate by ID in any list."""
        # Check all lists
        for c in self.candidates:
            if c.id == candidate_id:
                return c
        for c in self.scored_candidates:
            if c.id == candidate_id:
                return c
        for c in self.selected_candidates:
            if c.id == candidate_id:
                return c
        for c in self.all_candidates_history:
            if c.id == candidate_id:
                return c
        return None


class ExpansionState(ToTState):
    """State for expansion with seed candidate."""

    seed: ScoredCandidate | None = Field(
        default=None, description="Parent candidate to expand from"
    )
