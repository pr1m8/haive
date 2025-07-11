r"""Base conversation state with automatic round tracking via reducers.

This module defines the ConversationState class, which is the foundational state schema
for all conversation types. It extends MessagesState with specialized tracking for
conversation rounds, speaker history, and flow management using reducer-based automatic
state updates.

The state uses Pydantic for validation and reducer functions for automatic field updates,
allowing for elegant tracking of conversation progress without complex manual state management.
This approach ensures consistent state evolution and provides rich computed properties for
conversation analysis and control.

Key Features:
    - Automatic message accumulation (inherited from MessagesState)
    - Turn count tracking with automatic incrementation via reducers
    - Speaker history with automatic appending and chronological tracking
    - Round calculation based on turn count and speaker count
    - Computed properties for conversation progress and remaining speakers
    - Rich progress tracking with percentage completion and round analysis
    - Automatic termination detection based on round limits

Architecture:
    The ConversationState extends MessagesState and adds conversation-specific fields
    with reducer functions that automatically update state as conversations progress.
    Computed properties provide real-time analysis of conversation state without
    manual tracking or complex state management.

Usage Patterns:
    Basic state creation::\n

        state = ConversationState(
            speakers=["Alice", "Bob", "Charlie"],
            topic="Future of AI",
            max_rounds=5
        )

        # Automatic progress tracking
        print(f"Round {state.round_number}, Turn {state.turn_count}")
        print(f"Progress: {state.conversation_progress:.1%}")

    State updates via reducers::\n

        # Turn count automatically increments
        state = state.model_copy(update={"turn_count": 1})

        # Speaker history automatically appends
        state = state.model_copy(update={"speaker_history": ["Alice"]})

        # Computed properties automatically update
        print(f"Remaining speakers: {state.remaining_speakers_this_round}")

Examples:
    See the base conversation examples for comprehensive usage patterns.

Version: 1.0.0
Author: Haive Team
License: MIT
"""

from __future__ import annotations

import operator
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from haive.core.logging.rich_logger import LogLevel, get_logger
from haive.core.schema.prebuilt.messages_state import MessagesState
from pydantic import Field, computed_field
from typing_extensions import TypeAlias

if TYPE_CHECKING:
    pass

# Type aliases for better API clarity
SpeakerName: TypeAlias = str
SpeakerList: TypeAlias = list[SpeakerName]
ConversationTopic: TypeAlias = str
ConversationMode: TypeAlias = str
RoundNumber: TypeAlias = int
TurnCount: TypeAlias = int
ProgressPercentage: TypeAlias = float

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class ConversationState(MessagesState):
    r"""Base conversation state schema with automatic tracking and progress calculations.

    This state schema extends MessagesState with specialized fields and reducers for
    tracking multi-agent conversations. It provides automatic management of turns,
    rounds, speaker history, and conversation progress through a combination of
    Pydantic fields, reducers, and computed properties.

    The state uses reducer functions for automatic field updates. When a turn is taken,
    the turn_count and speaker_history are automatically updated through reducers,
    allowing for clean state updates without manual tracking complexity.

    Attributes:
        messages (List[BaseMessage]): Conversation messages (inherited from MessagesState)
        current_speaker (Optional[SpeakerName]): The currently active speaker
        speakers (SpeakerList): List of all participant speaker names
        turn_count (TurnCount): Total number of speaking turns taken (auto-incremented)
        max_rounds (int): Maximum number of conversation rounds allowed
        topic (Optional[ConversationTopic]): The conversation topic or subject
        conversation_ended (bool): Flag indicating if conversation is complete
        mode (ConversationMode): Conversation mode identifier (e.g., "round_robin", "debate")
        speaker_history (SpeakerList): Chronological history of speakers (auto-appended)

    Computed Properties:
        round_number (RoundNumber): Current round number calculated from turns and speakers
        current_round_speakers (SpeakerList): Speakers who have spoken in current round
        remaining_speakers_this_round (SpeakerList): Speakers yet to speak in current round
        should_end_by_rounds (bool): Whether round limit has been reached
        turns_per_round (int): Number of turns in a complete round
        conversation_progress (ProgressPercentage): Progress from 0.0 to 1.0

    Reducer Functions:
        turn_count: operator.add - Auto-increment turns when state is updated
        speaker_history: operator.add - Append new speakers to chronological history
        messages: inherited from MessagesState - Accumulate conversation messages

    Examples:
        Basic usage with automatic tracking::\n

            state = ConversationState(
                speakers=["Alice", "Bob", "Charlie"],
                topic="Future of AI",
                max_rounds=5
            )

            # State automatically tracks progress
            print(f"Round {state.round_number}, Turn {state.turn_count}")
            print(f"Progress: {state.conversation_progress:.1%}")

        State updates via reducers::\n

            # Turn count automatically increments
            new_state = state.model_copy(update={"turn_count": 1})

            # Speaker history automatically appends
            new_state = new_state.model_copy(update={"speaker_history": ["Alice"]})

            # Computed properties automatically update
            print(f"Remaining: {new_state.remaining_speakers_this_round}")

    Note:
        This state uses reducer functions for automatic field updates. The reducers
        ensure consistent state evolution without manual tracking complexity, making
        it easier to build robust conversation orchestration systems.
    """

    # Track conversation flow with type hints
    current_speaker: SpeakerName | None = Field(
        default=None, description="The currently active speaker in the conversation"
    )
    speakers: SpeakerList = Field(
        default_factory=list, description="List of all participant speaker names"
    )

    # Use reducer for automatic round counting
    turn_count: TurnCount = Field(
        default=0,
        description="Total number of turns taken (auto-incremented via reducer)",
    )

    max_rounds: int = Field(
        default=10, description="Maximum number of conversation rounds allowed", gt=0
    )

    # Conversation metadata with type hints
    topic: ConversationTopic | None = Field(
        default=None, description="The conversation topic or subject matter"
    )
    conversation_ended: bool = Field(
        default=False, description="Flag indicating if conversation is complete"
    )
    mode: ConversationMode = Field(
        default="round_robin",
        description="Conversation mode identifier (e.g., 'round_robin', 'debate')",
    )

    # Speaker history for tracking with type hints
    speaker_history: SpeakerList = Field(
        default_factory=list,
        description="Chronological history of speakers in order (auto-appended)",
    )

    # Add reducers for automatic tracking with proper type annotations
    __reducer_fields__: dict[str, Any] = {
        **MessagesState.__reducer_fields__,  # Inherit messages reducer
        "turn_count": operator.add,  # Auto-increment turns
        "speaker_history": operator.add,  # Append to history
    }

    @computed_field
    @property
    def round_number(self) -> RoundNumber:
        r"""Compute current round based on turn count and number of speakers.

        Calculates the current round number using turn count and speaker count.
        Returns 0 if no speakers or no turns have been taken.

        Returns:
            Current round number (1-based indexing)

        Examples:
            With 3 speakers and 7 turns taken::\n

                # Round 1: turns 1-3, Round 2: turns 4-6, Round 3: turn 7
                round_number = (7 - 1) // 3 + 1 = 3
        """
        if not self.speakers or self.turn_count == 0:
            return 0
        # Calculate rounds based on turns and speaker count
        return (self.turn_count - 1) // len(self.speakers) + 1

    @computed_field
    @property
    def current_round_speakers(self) -> SpeakerList:
        r"""Get list of speakers who have already spoken in current round.

        Analyzes the speaker history to determine which speakers have taken
        turns in the current round, based on round boundaries.

        Returns:
            List of speaker names who have spoken in the current round

        Examples:
            With 3 speakers in round 2, turn 5::\n

                # Round 1: speakers 0-2, Round 2: speakers 3-4
                current_round_speakers = speaker_history[3:5]
        """
        if not self.speakers or self.round_number == 0:
            return []

        # Calculate based on speaker history
        start_idx = (self.round_number - 1) * len(self.speakers)
        end_idx = start_idx + (
            self.turn_count % len(self.speakers) or len(self.speakers)
        )

        return self.speaker_history[start_idx:end_idx]

    @computed_field
    @property
    def remaining_speakers_this_round(self) -> SpeakerList:
        r"""Get speakers who haven't spoken yet in current round.

        Determines which speakers from the participant list have not yet
        taken their turn in the current round.

        Returns:
            List of speaker names who have not yet spoken in current round

        Examples:
            With speakers ["Alice", "Bob", "Charlie"] and current speakers ["Alice"]::\n

                remaining_speakers_this_round = ["Bob", "Charlie"]
        """
        if not self.speakers:
            return []

        current_speakers = set(self.current_round_speakers)
        return [s for s in self.speakers if s not in current_speakers]

    @computed_field
    @property
    def should_end_by_rounds(self) -> bool:
        r"""Check if conversation should end based on round limit.

        Determines if the conversation has reached or exceeded the maximum
        number of rounds and should be terminated.

        Returns:
            True if round limit has been reached or exceeded

        Examples:
            With max_rounds=5 and current round 5::\n

                should_end_by_rounds = True  # Conversation should end
        """
        return self.round_number >= self.max_rounds

    @computed_field
    @property
    def turns_per_round(self) -> int:
        r"""Calculate expected turns per round.

        Determines the number of turns that constitute a complete round
        based on the number of speakers.

        Returns:
            Number of turns in a complete round (equals number of speakers)

        Examples:
            With 3 speakers::\n

                turns_per_round = 3  # Each speaker gets one turn per round
        """
        return len(self.speakers) if self.speakers else 1

    @computed_field
    @property
    def conversation_progress(self) -> ProgressPercentage:
        r"""Calculate conversation progress as percentage.

        Computes the progress of the conversation as a percentage from 0.0 to 1.0
        based on the current round number and maximum rounds.

        Returns:
            Progress from 0.0 to 1.0 (0% to 100%)

        Examples:
            With max_rounds=5 and current round 3::\n

                conversation_progress = 3 / 5 = 0.6  # 60% complete
        """
        if self.max_rounds == 0:
            return 1.0
        return min(1.0, self.round_number / self.max_rounds)
