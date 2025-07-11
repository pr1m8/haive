# src/haive/agents/conversation/round_robin.py
"""Round-robin conversation agent where each participant speaks in turn."""

from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.logging.rich_logger import LogLevel, get_logger
from pydantic import Field

from haive.agents.conversation.base.agent import BaseConversationAgent
from haive.agents.conversation.base.state import ConversationState
from haive.agents.simple.agent import SimpleAgent

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class RoundRobinConversation(BaseConversationAgent):
    """Round-robin conversation where each agent speaks in a fixed order.

    Each participant gets exactly one turn per round, with the order
    maintained throughout the conversation.
    """

    mode: Literal["round_robin"] = Field(default="round_robin")

    # Round-robin specific settings
    skip_unavailable: bool = Field(
        default=True, description="Skip speakers who are unavailable instead of ending"
    )
    announce_speaker: bool = Field(
        default=False, description="Announce who is speaking next"
    )

    def select_speaker(self, state: ConversationState) -> dict[str, Any]:
        """Select the next speaker in round-robin order."""
        speakers = state.speakers
        current_speaker = state.current_speaker
        round_number = state.round_number

        if not speakers:
            logger.warning("No speakers available")
            return {"current_speaker": None, "conversation_ended": True}

        # Determine next speaker
        if current_speaker is None:
            # First speaker
            next_speaker = speakers[0]
            new_round = 0
        else:
            try:
                current_idx = speakers.index(current_speaker)
                next_idx = (current_idx + 1) % len(speakers)
                next_speaker = speakers[next_idx]

                # Increment round when we wrap back to first speaker
                new_round = round_number + (1 if next_idx == 0 else 0)
            except ValueError:
                # Current speaker not in list, start over
                logger.warning(
                    f"Current speaker {current_speaker} not in speakers list"
                )
                next_speaker = speakers[0]
                new_round = round_number

        update = {"current_speaker": next_speaker, "round_number": new_round}

        # Add announcement if enabled
        if self.announce_speaker and next_speaker:
            from langchain_core.messages import SystemMessage

            announcement = SystemMessage(content=f"[Now speaking: {next_speaker}]")
            update["messages"] = [announcement]

        return update

    def _custom_initialization(self, state: ConversationState) -> dict[str, Any]:
        """Add round-robin specific initialization."""
        return {
            "skip_unavailable": self.skip_unavailable,
            "announce_speaker": self.announce_speaker,
        }

    def _prepare_agent_input(
        self, state: ConversationState, agent_name: str
    ) -> dict[str, Any]:
        """Prepare input with round context."""
        base_input = super()._prepare_agent_input(state, agent_name)

        # Add round information to the context
        if state.round_number > 0:
            from langchain_core.messages import SystemMessage

            round_msg = SystemMessage(
                content=f"[Round {state.round_number + 1} of {state.max_rounds}]"
            )

            # Insert at beginning of messages
            messages = [round_msg, *base_input.get("messages", [])]
            base_input["messages"] = messages

        return base_input

    @classmethod
    def create_simple(
        cls,
        participants: list[str],
        topic: str = "General discussion",
        max_rounds: int = 3,
        system_message_template: str | None = None,
        **kwargs,
    ):
        """Create a simple round-robin conversation with auto-generated agents.

        Args:
            participants: List of participant names
            topic: Conversation topic
            max_rounds: Maximum number of rounds
            system_message_template: Template for system messages (use {name} for participant name)
            **kwargs: Additional arguments for the conversation

        Returns:
            Configured RoundRobinConversation
        """
        if not system_message_template:
            system_message_template = (
                "You are {name}, a thoughtful participant in a round-robin discussion. "
                "Keep your responses concise (2-3 sentences) and relevant to the topic."
            )

        # Create agents for each participant
        agents = {}
        for name in participants:
            engine = AugLLMConfig(
                name=f"{name.lower()}_engine",
                system_message=system_message_template.format(name=name),
                temperature=0.7,
            )
            agents[name] = SimpleAgent(name=f"{name}_agent", engine=engine)

        return cls(
            participant_agents=agents, topic=topic, max_rounds=max_rounds, **kwargs
        )

    def __repr__(self) -> str:
        participant_names = list(self.participant_agents.keys())
        return (
            f"RoundRobinConversation("
            f"participants={participant_names}, "
            f"topic='{self.topic}', "
            f"max_rounds={self.max_rounds})"
        )
