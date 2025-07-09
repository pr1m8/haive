# src/haive/agents/conversation/debate/state.py
"""State schema for structured debate conversations with automatic tracking."""

import operator
from typing import Any

from pydantic import Field, computed_field

from haive.agents.conversation.base.state import ConversationState


class DebateState(ConversationState):
    """Extended state schema for debate conversations with automatic tracking.

    Extends ConversationState with debate-specific fields and automatic
    computation of debate progress and statistics.
    """

    # Debate positions and tracking
    debate_positions: dict[str, str] = Field(
        default_factory=dict,
        description="Mapping of participant names to their debate positions",
    )

    # Use reducers for automatic counting
    arguments_made: dict[str, list[str]] = Field(
        default_factory=dict, description="Arguments made by each participant"
    )

    rebuttals: dict[str, list[tuple[str, str]]] = Field(
        default_factory=dict,
        description="Rebuttals as (target_name, rebuttal_summary) tuples",
    )

    # Debate flow control
    opening_statements_complete: bool = Field(
        default=False, description="Whether opening statements phase is done"
    )

    closing_statements_complete: bool = Field(
        default=False, description="Whether closing statements are done"
    )

    current_phase: str = Field(default="opening", description="Current debate phase")

    phase_transitions: list[tuple[str, int]] = Field(
        default_factory=list,
        description="History of phase transitions as (phase_name, turn_number)",
    )

    # Counters with reducers
    total_arguments: int = Field(
        default=0, description="Total arguments made (auto-counted)"
    )

    total_rebuttals: int = Field(
        default=0, description="Total rebuttals made (auto-counted)"
    )

    # Optional scoring and judging
    argument_scores: dict[str, float] = Field(
        default_factory=dict, description="Optional scores for each participant"
    )

    judge_feedback: list[str] = Field(
        default_factory=list, description="Feedback from judge participants"
    )

    debate_winner: str = Field(default="", description="Declared winner of the debate")

    # Configuration
    arguments_per_side: int = Field(
        default=3, description="Required arguments per participant"
    )

    # Extended reducers
    __reducer_fields__ = {
        **ConversationState.__reducer_fields__,
        "total_arguments": operator.add,
        "total_rebuttals": operator.add,
        "phase_transitions": operator.add,
        "judge_feedback": operator.add,
    }

    @computed_field
    @property
    def in_rebuttal_phase(self) -> bool:
        """Check if currently in rebuttal phase."""
        return self.current_phase == "rebuttals"

    @computed_field
    @property
    def all_arguments_complete(self) -> bool:
        """Check if all participants have made required arguments."""
        if not self.debate_positions or self.arguments_per_side == 0:
            return True

        for participant in self.debate_positions:
            if len(self.arguments_made.get(participant, [])) < self.arguments_per_side:
                return False
        return True

    @computed_field
    @property
    def debate_progress(self) -> dict[str, float]:
        """Calculate progress for each participant."""
        progress = {}
        for participant in self.debate_positions:
            args = len(self.arguments_made.get(participant, []))
            progress[participant] = min(1.0, args / self.arguments_per_side)
        return progress

    @computed_field
    @property
    def phase_should_transition(self) -> bool:
        """Check if current phase should transition."""
        if (self.current_phase == "opening" and self.opening_statements_complete) or (
            self.current_phase == "arguments" and self.all_arguments_complete
        ):
            return True
        if (self.current_phase == "rebuttals" and self.all_rebuttals_complete) or (
            self.current_phase == "closing" and self.closing_statements_complete
        ):
            return True
        return False

    @computed_field
    @property
    def all_rebuttals_complete(self) -> bool:
        """Check if rebuttal phase is complete."""
        # Each participant should have at least 1 rebuttal
        for participant in self.debate_positions:
            if len(self.rebuttals.get(participant, [])) < 1:
                return False
        return True

    @computed_field
    @property
    def next_phase(self) -> str | None:
        """Determine what the next phase should be."""
        phase_order = {
            "opening": "arguments",
            "arguments": "rebuttals",
            "rebuttals": "closing",
            "closing": "judging" if self.judge_feedback else "complete",
            "judging": "complete",
        }
        return phase_order.get(self.current_phase)

    @computed_field
    @property
    def debate_statistics(self) -> dict[str, Any]:
        """Get comprehensive debate statistics."""
        return {
            "total_turns": self.turn_count,
            "current_round": self.round_number,
            "phase": self.current_phase,
            "total_arguments": self.total_arguments,
            "total_rebuttals": self.total_rebuttals,
            "arguments_by_participant": {
                p: len(args) for p, args in self.arguments_made.items()
            },
            "rebuttals_by_participant": {
                p: len(rebs) for p, rebs in self.rebuttals.items()
            },
            "progress": self.debate_progress,
            "winner": self.debate_winner or "Undecided",
        }

    @computed_field
    @property
    def should_end_debate(self) -> bool:
        """Check if debate should end based on all conditions."""
        return (
            self.conversation_ended
            or self.current_phase == "complete"
            or self.should_end_by_rounds
            or (self.debate_winner != "" and self.current_phase == "judging")
        )

    def get_participant_summary(self, participant: str) -> dict[str, Any]:
        """Get summary for a specific participant."""
        return {
            "name": participant,
            "position": self.debate_positions.get(participant, "Unknown"),
            "arguments_made": len(self.arguments_made.get(participant, [])),
            "rebuttals_made": len(self.rebuttals.get(participant, [])),
            "score": self.argument_scores.get(participant, 0.0),
            "progress": self.debate_progress.get(participant, 0.0),
        }
