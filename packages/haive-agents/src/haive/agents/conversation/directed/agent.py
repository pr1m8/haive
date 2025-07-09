# src/haive/agents/conversation/directed/agent.py
"""Directed conversation agent where participants respond to mentions and direct questions.
Uses structured output models for robust speaker selection and interaction tracking.
"""

import re
from enum import Enum
from typing import Any, Literal

from haive.core.logging.rich_logger import LogLevel, get_logger
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from pydantic import BaseModel, Field

from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.directed.state import DirectedState

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class MentionType(str, Enum):
    """Types of mentions detected in messages."""

    DIRECT_MENTION = "direct_mention"  # @name
    NAME_REFERENCE = "name_reference"  # "name," or "name:"
    QUESTION_TARGET = "question_target"  # "What do you think, name?"
    NO_MENTION = "no_mention"


class SpeakerMention(BaseModel):
    """Structured representation of a speaker mention."""

    speaker_name: str = Field(description="Name of the mentioned speaker")
    mention_type: MentionType = Field(description="Type of mention detected")
    confidence: float = Field(
        default=1.0, description="Confidence in the mention detection"
    )
    context: str | None = Field(default=None, description="Context around the mention")


class SpeakerSelectionResult(BaseModel):
    """Structured output for speaker selection logic."""

    next_speaker: str | None = Field(default=None, description="Next speaker to talk")
    pending_speakers: list[str] = Field(
        default_factory=list, description="Queue of speakers waiting to talk"
    )
    mentioned_speakers: list[str] = Field(
        default_factory=list, description="All speakers mentioned in last message"
    )
    selection_reason: str = Field(
        default="", description="Reason for speaker selection"
    )
    confidence: float = Field(default=1.0, description="Confidence in the selection")


class InteractionPattern(BaseModel):
    """Track interaction patterns between speakers."""

    from_speaker: str = Field(description="Speaker who mentioned others")
    to_speaker: str = Field(description="Speaker who was mentioned")
    mention_count: int = Field(default=1, description="Number of mentions")
    mention_types: list[MentionType] = Field(
        default_factory=list, description="Types of mentions used"
    )


class DirectedConversationConfig(BaseModel):
    """Configuration for directed conversation behavior."""

    mention_patterns: list[str] = Field(
        default_factory=lambda: ["@{name}", "{name},", "{name}:", "ask {name}"],
        description="Patterns to detect mentions (use {name} as placeholder)",
    )
    fallback_to_round_robin: bool = Field(
        default=True, description="Use round-robin if no one is mentioned"
    )
    max_silence_turns: int = Field(
        default=3, description="Max turns before forcing someone to speak"
    )
    allow_self_selection: bool = Field(
        default=True, description="Allow agents to volunteer to speak"
    )
    avoid_self_mentions: bool = Field(
        default=True,
        description="Prevent speakers from being selected based on self-mentions",
    )
    prioritize_least_active: bool = Field(
        default=True, description="Prioritize speakers who haven't spoken recently"
    )


class DirectedConversation(BaseConversationAgent):
    """Directed conversation where agents respond to mentions and questions.

    Uses structured output models for robust speaker selection and tracking.
    Participants speak when:
    - They are directly mentioned (@name)
    - A question is directed at them
    - They haven't spoken in a while (configurable)
    """

    mode: Literal["directed"] = Field(default="directed")

    # Configuration
    config: DirectedConversationConfig = Field(
        default_factory=DirectedConversationConfig,
        description="Configuration for directed conversation behavior",
    )

    # Internal tracking
    _interaction_history: list[InteractionPattern] = []

    def get_conversation_state_schema(self) -> type:
        """Use extended state schema."""
        return DirectedState

    def select_speaker(self, state: DirectedState) -> dict[str, Any]:
        """Select speaker based on mentions and context using structured models."""
        # Get structured selection result
        selection_result = self._get_speaker_selection(state)

        # Log the selection reasoning
        logger.debug(
            f"Speaker selection: {selection_result.next_speaker} - {selection_result.selection_reason}"
        )

        # Convert to state update
        update = {
            "current_speaker": selection_result.next_speaker,
            "pending_speakers": selection_result.pending_speakers,
            "mentioned_speakers": selection_result.mentioned_speakers,
        }

        # If no speaker selected, mark conversation as ended
        if not selection_result.next_speaker:
            update["conversation_ended"] = True

        return update

    def _get_speaker_selection(self, state: DirectedState) -> SpeakerSelectionResult:
        """Get structured speaker selection result."""
        # Check pending speakers first
        if state.pending_speakers:
            return SpeakerSelectionResult(
                next_speaker=state.pending_speakers[0],
                pending_speakers=state.pending_speakers[1:],
                selection_reason="Selected from pending queue",
            )

        # Extract mentions using structured model
        mentions = self._extract_structured_mentions(state)

        # Filter out self-mentions if configured
        if self.config.avoid_self_mentions and mentions:
            last_speaker = self._get_last_speaker_name(state)
            mentions = [m for m in mentions if m.speaker_name != last_speaker]

        # If we have mentions, use them
        if mentions:
            # Sort by confidence and mention type priority
            sorted_mentions = sorted(
                mentions,
                key=lambda m: (
                    m.confidence,
                    self._get_mention_priority(m.mention_type),
                ),
                reverse=True,
            )

            # Extract unique speaker names in priority order
            mentioned_names = []
            seen = set()
            for mention in sorted_mentions:
                if mention.speaker_name not in seen:
                    mentioned_names.append(mention.speaker_name)
                    seen.add(mention.speaker_name)

            if mentioned_names:
                return SpeakerSelectionResult(
                    next_speaker=mentioned_names[0],
                    pending_speakers=(
                        mentioned_names[1:] if len(mentioned_names) > 1 else []
                    ),
                    mentioned_speakers=mentioned_names,
                    selection_reason=f"Mentioned via {sorted_mentions[0].mention_type.value}",
                    confidence=sorted_mentions[0].confidence,
                )

        # No mentions - use fallback strategy
        if self.config.fallback_to_round_robin:
            return self._select_round_robin_structured(state)
        return self._select_least_active_structured(state)

    def _extract_structured_mentions(
        self, state: DirectedState
    ) -> list[SpeakerMention]:
        """Extract mentions as structured models."""
        if not state.messages:
            return []

        last_message = state.messages[-1]
        if not isinstance(last_message, (AIMessage, BaseMessage)) or not hasattr(
            last_message, "content"
        ):
            return []

        content = str(last_message.content)
        mentions = []

        # Check each speaker for different mention types
        for speaker in state.speakers:
            # Direct mentions (@name)
            if f"@{speaker}" in content:
                mentions.append(
                    SpeakerMention(
                        speaker_name=speaker,
                        mention_type=MentionType.DIRECT_MENTION,
                        confidence=1.0,
                        context=self._extract_context(content, f"@{speaker}"),
                    )
                )
                continue

            # Name references (name, or name:)
            for pattern in [f"{speaker},", f"{speaker}:"]:
                if pattern in content:
                    mentions.append(
                        SpeakerMention(
                            speaker_name=speaker,
                            mention_type=MentionType.NAME_REFERENCE,
                            confidence=0.9,
                            context=self._extract_context(content, pattern),
                        )
                    )
                    break

            # Question targets
            if "?" in content:
                question_patterns = [
                    rf"what (?:do you think|about|is your opinion),?\s*{re.escape(speaker)}\?",
                    rf"{re.escape(speaker)},?\s*what (?:do you think|about)",
                    rf"how (?:about you|do you feel),?\s*{re.escape(speaker)}\?",
                    rf"ask {re.escape(speaker)}",
                ]

                for pattern in question_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        mentions.append(
                            SpeakerMention(
                                speaker_name=speaker,
                                mention_type=MentionType.QUESTION_TARGET,
                                confidence=0.95,
                                context=self._extract_context(content, speaker),
                            )
                        )
                        break

        return mentions

    def _extract_context(
        self, content: str, mention: str, context_size: int = 50
    ) -> str:
        """Extract context around a mention."""
        try:
            idx = content.lower().find(mention.lower())
            if idx == -1:
                return ""

            start = max(0, idx - context_size)
            end = min(len(content), idx + len(mention) + context_size)

            context = content[start:end]
            if start > 0:
                context = "..." + context
            if end < len(content):
                context = context + "..."

            return context
        except Exception:
            return ""

    def _get_mention_priority(self, mention_type: MentionType) -> int:
        """Get priority score for mention type (higher is better)."""
        priorities = {
            MentionType.DIRECT_MENTION: 3,
            MentionType.QUESTION_TARGET: 2,
            MentionType.NAME_REFERENCE: 1,
            MentionType.NO_MENTION: 0,
        }
        return priorities.get(mention_type, 0)

    def _get_last_speaker_name(self, state: DirectedState) -> str | None:
        """Get the name of the last speaker."""
        if not state.messages:
            return None

        for msg in reversed(state.messages):
            if isinstance(msg, AIMessage) and hasattr(msg, "name"):
                return msg.name

        return None

    def _select_round_robin_structured(
        self, state: DirectedState
    ) -> SpeakerSelectionResult:
        """Select next speaker using round-robin."""
        current_speaker = state.current_speaker
        speakers = state.speakers

        if not speakers:
            return SpeakerSelectionResult(
                next_speaker=None, selection_reason="No speakers available"
            )

        if not current_speaker:
            return SpeakerSelectionResult(
                next_speaker=speakers[0], selection_reason="Starting with first speaker"
            )

        try:
            current_idx = speakers.index(current_speaker)
            next_idx = (current_idx + 1) % len(speakers)
            return SpeakerSelectionResult(
                next_speaker=speakers[next_idx],
                selection_reason="Round-robin selection",
            )
        except ValueError:
            return SpeakerSelectionResult(
                next_speaker=speakers[0],
                selection_reason="Current speaker not found, restarting",
            )

    def _select_least_active_structured(
        self, state: DirectedState
    ) -> SpeakerSelectionResult:
        """Select the speaker who has been least active."""
        # Count messages per speaker
        message_count = dict.fromkeys(state.speakers, 0)

        for msg in state.messages:
            if isinstance(msg, AIMessage) and hasattr(msg, "name"):
                if msg.name in message_count:
                    message_count[msg.name] += 1

        # Find speaker with minimum messages
        if message_count:
            least_active = min(message_count.items(), key=lambda x: x[1])
            return SpeakerSelectionResult(
                next_speaker=least_active[0],
                selection_reason=f"Least active speaker (spoke {least_active[1]} times)",
                confidence=0.8,
            )

        return SpeakerSelectionResult(
            next_speaker=state.speakers[0] if state.speakers else None,
            selection_reason="Defaulting to first speaker",
        )

    def process_response(self, state: DirectedState) -> dict[str, Any]:
        """Track interaction patterns using structured models."""
        update = {}

        # Track interactions
        if state.current_speaker and state.mentioned_speakers:
            # Create interaction patterns
            for mentioned in state.mentioned_speakers:
                if mentioned != state.current_speaker:
                    interaction = InteractionPattern(
                        from_speaker=state.current_speaker,
                        to_speaker=mentioned,
                        mention_count=1,
                        mention_types=[MentionType.NAME_REFERENCE],  # Could be enhanced
                    )
                    self._interaction_history.append(interaction)

            # Update interaction count in state
            interaction_count = dict(state.interaction_count)
            if state.current_speaker not in interaction_count:
                interaction_count[state.current_speaker] = {}

            for mentioned in state.mentioned_speakers:
                if mentioned != state.current_speaker:
                    current = interaction_count[state.current_speaker].get(mentioned, 0)
                    interaction_count[state.current_speaker][mentioned] = current + 1

            update["interaction_count"] = interaction_count

        # Clear mentioned speakers
        update["mentioned_speakers"] = []

        return update

    def _prepare_agent_input(
        self, state: DirectedState, agent_name: str
    ) -> dict[str, Any]:
        """Prepare input with mention context."""
        base_input = super()._prepare_agent_input(state, agent_name)

        # Add context about why they're speaking
        if agent_name in state.mentioned_speakers:
            # Find how they were mentioned
            mentions = self._extract_structured_mentions(state)
            agent_mentions = [m for m in mentions if m.speaker_name == agent_name]

            if agent_mentions:
                mention_type = agent_mentions[0].mention_type.value.replace("_", " ")
                context = f"[You were mentioned via {mention_type}. Please respond.]"
            else:
                context = "[You were mentioned in the conversation. Please respond.]"

            mention_msg = SystemMessage(content=context)
            messages = base_input.get("messages", [])

            # Insert before the last message
            if messages:
                messages = messages[:-1] + [mention_msg] + messages[-1:]
            else:
                messages = [mention_msg]
            base_input["messages"] = messages

        return base_input

    @staticmethod
    def _sanitize_name_for_openai(name: str) -> str:
        """Sanitize a name to be compatible with OpenAI's API requirements.

        OpenAI's name field must match the pattern '^[^\\s<|\\\\/>]+$'
        This means no spaces, <, |, \\, /, or >

        Args:
            name: The original name

        Returns:
            Sanitized name safe for OpenAI API
        """
        # Replace spaces with underscores
        sanitized = name.replace(" ", "_")

        # Remove any other forbidden characters
        forbidden_chars = ["<", "|", "\\", "/", ">"]
        for char in forbidden_chars:
            sanitized = sanitized.replace(char, "")

        # Ensure the name is not empty
        if not sanitized:
            sanitized = "User"

        return sanitized

    @classmethod
    def create_classroom(
        cls,
        teacher_name: str = "Teacher",
        student_names: list[str] | None = None,
        topic: str = "Today's lesson",
        config: DirectedConversationConfig | None = None,
        **kwargs,
    ):
        """Create a classroom-style directed conversation.

        Args:
            teacher_name: Name of the teacher
            student_names: List of student names
            topic: Lesson topic
            config: Optional configuration for directed conversation
            **kwargs: Additional conversation arguments
        """
        if student_names is None:
            student_names = ["Alice", "Bob", "Charlie"]

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.simple.agent import SimpleAgent

        # Sanitize all names for OpenAI API
        teacher_name_sanitized = cls._sanitize_name_for_openai(teacher_name)

        # Create teacher agent
        teacher_engine = AugLLMConfig(
            name=f"{teacher_name_sanitized.lower()}_engine",
            system_message=(
                f"You are {teacher_name}, a teacher leading a discussion about {topic}. "
                "Ask questions to specific students using their names. "
                "Provide feedback and guide the discussion. "
                "Make sure to mention student names when asking them questions."
            ),
            temperature=0.6,
        )

        agents = {
            teacher_name_sanitized: SimpleAgent(
                name=f"{teacher_name_sanitized}_agent", engine=teacher_engine
            )
        }

        # Create student agents
        for student in student_names:
            student_sanitized = cls._sanitize_name_for_openai(student)
            student_engine = AugLLMConfig(
                name=f"{student_sanitized.lower()}_engine",
                system_message=(
                    f"You are {student}, a student in class. "
                    "Answer when the teacher asks you questions. "
                    "You can also ask questions or respond to other students. "
                    "Be engaged and thoughtful in your responses."
                ),
                temperature=0.7,
            )
            agents[student_sanitized] = SimpleAgent(
                name=f"{student_sanitized}_agent", engine=student_engine
            )

        # Use provided config or create default
        if config is None:
            config = DirectedConversationConfig(
                mention_patterns=[
                    "@{name}",
                    "{name},",
                    "{name}:",
                    "ask {name}",
                    "{name}?",
                ],
                fallback_to_round_robin=True,
                avoid_self_mentions=True,
                prioritize_least_active=True,
            )

        return cls(
            participant_agents=agents,
            topic=topic,
            config=config,
            **kwargs,
        )

    def _check_custom_end_conditions(
        self, state: DirectedState
    ) -> dict[str, Any] | None:
        """Check if everyone has participated sufficiently."""
        # Count participation
        participation = dict.fromkeys(state.speakers, 0)

        for msg in state.messages:
            if isinstance(msg, AIMessage) and hasattr(msg, "name"):
                if msg.name in participation:
                    participation[msg.name] += 1

        # If everyone has spoken at least once and we've had reasonable discussion
        min_participation = min(participation.values()) if participation else 0
        total_messages = len(state.messages)

        if min_participation >= 2 and total_messages >= len(state.speakers) * 3:
            return {"conversation_ended": True}

        return None
