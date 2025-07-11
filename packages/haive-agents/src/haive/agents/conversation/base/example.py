#!/usr/bin/env python3
"""Base Conversation Agent Example.

This example demonstrates how to create custom conversation agents by extending
the BaseConversationAgent class and implementing core conversation patterns.
"""

import asyncio
import operator
from typing import Any, Dict, List, Optional

from haive.core.exceptions import ConversationError
from haive.core.logging import get_logger
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import Field

from haive.agents.conversation.base import (
    BaseConversationAgent,
    ConversationState,
    create_conversation_state,
    get_conversation_progress,
)
from haive.agents.simple import SimpleAgent

logger = get_logger(__name__)


class CustomConversationState(ConversationState):
    """Extended conversation state with quality tracking."""

    # Custom fields for tracking conversation quality
    quality_scores: list[float] = Field(default_factory=list)
    engagement_level: float = Field(default=0.5)
    sentiment_scores: dict[str, float] = Field(default_factory=dict)

    # Custom reducers for automatic updates
    __reducer_fields__ = {
        **ConversationState.__reducer_fields__,
        "quality_scores": operator.add,  # Append quality scores
    }

    @property
    def average_quality(self) -> float:
        """Calculate average conversation quality."""
        if not self.quality_scores:
            return 0.0
        return sum(self.quality_scores) / len(self.quality_scores)


class CustomConversationAgent(BaseConversationAgent[CustomConversationState]):
    """Custom conversation agent demonstrating extension patterns.

    This example shows how to:
    - Implement custom speaker selection logic
    - Add conversation quality assessment
    - Handle errors gracefully
    - Track custom metrics
    """

    def __init__(self, *args, **kwargs):
        """Initialize with custom configuration."""
        super().__init__(*args, **kwargs)
        self.speaker_preferences = {}
        self.conversation_metrics = {
            "total_words": 0,
            "average_response_length": 0,
            "engagement_scores": [],
        }

    def select_next_speaker(self, state: CustomConversationState) -> str | None:
        """Custom speaker selection with engagement-based prioritization.

        Selects speakers based on:
        1. Who hasn't spoken in the current round
        2. Engagement level preferences
        3. Balanced participation
        """
        # Check if we have remaining speakers this round
        if state.remaining_speakers_this_round:
            # If engagement is high, prioritize active participants
            if state.engagement_level > 0.7:
                # Sort by recent activity (those who spoke more recently)
                recent_speakers = state.speaker_history[-len(state.speakers) :]
                active_remaining = [
                    s
                    for s in state.remaining_speakers_this_round
                    if s in recent_speakers
                ]
                if active_remaining:
                    return active_remaining[0]

            # Default: return first remaining speaker
            return state.remaining_speakers_this_round[0]

        # Round complete or no speakers
        return None

    def should_end_conversation(self, state: CustomConversationState) -> bool:
        """Enhanced termination logic with quality considerations.

        Ends conversation if:
        - Round limit reached
        - Quality drops below threshold
        - Engagement is too low
        - Explicit end flag set
        """
        # Check standard termination conditions
        if state.should_end_by_rounds or state.conversation_ended:
            return True

        # Check quality threshold
        if state.quality_scores and state.average_quality < 0.3:
            logger.warning("Ending conversation due to low quality")
            return True

        # Check engagement threshold
        if state.engagement_level < 0.2 and state.turn_count > 5:
            logger.warning("Ending conversation due to low engagement")
            return True

        # Check message count limit
        if len(state.messages) > 50:
            logger.info("Ending conversation due to message limit")
            return True

        return False

    async def execute_agent(
        self, agent: Any, input_data: str, state: CustomConversationState
    ) -> str:
        """Execute agent with quality assessment and error handling."""
        try:
            # Execute the agent
            response = await super().execute_agent(agent, input_data, state)

            # Assess response quality (simplified example)
            quality_score = self._assess_response_quality(response)

            # Update metrics
            self.conversation_metrics["total_words"] += len(response.split())
            self.conversation_metrics["engagement_scores"].append(quality_score)

            # Update state with quality score
            state.quality_scores.append(quality_score)

            # Adjust engagement based on quality
            if quality_score > 0.7:
                state.engagement_level = min(1.0, state.engagement_level + 0.1)
            elif quality_score < 0.3:
                state.engagement_level = max(0.0, state.engagement_level - 0.1)

            return response

        except TimeoutError:
            logger.exception(f"Agent {agent.name} timed out")
            return f"[{agent.name} is taking time to respond...]"
        except Exception as e:
            logger.exception(f"Error executing agent {agent.name}: {e}")
            raise ConversationError(f"Failed to execute agent: {e}")

    def _assess_response_quality(self, response: str) -> float:
        """Simplified quality assessment based on response characteristics.

        In a real implementation, this could use:
        - Sentiment analysis
        - Relevance scoring
        - Coherence metrics
        - Fact checking
        """
        # Simple heuristics for demonstration
        score = 0.5  # Base score

        # Length bonus (not too short, not too long)
        word_count = len(response.split())
        if 10 <= word_count <= 50:
            score += 0.2
        elif word_count < 5:
            score -= 0.2
        elif word_count > 100:
            score -= 0.1

        # Question engagement (contains questions)
        if "?" in response:
            score += 0.1

        # Politeness indicators
        polite_words = ["please", "thank you", "appreciate", "kindly"]
        if any(word in response.lower() for word in polite_words):
            score += 0.1

        # Negative indicators
        negative_words = ["hate", "stupid", "awful", "terrible"]
        if any(word in response.lower() for word in negative_words):
            score -= 0.2

        return max(0.0, min(1.0, score))

    def get_conversation_summary(self) -> dict[str, Any]:
        """Generate comprehensive conversation summary."""
        state = self.get_state()

        # Calculate final metrics
        avg_response_length = (
            self.conversation_metrics["total_words"] / state.turn_count
            if state.turn_count > 0
            else 0
        )

        return {
            "basic_info": {
                "topic": state.topic,
                "participants": state.speakers,
                "total_turns": state.turn_count,
                "total_rounds": state.round_number,
                "progress": f"{state.conversation_progress:.1%}",
            },
            "quality_metrics": {
                "average_quality": state.average_quality,
                "final_engagement": state.engagement_level,
                "quality_trend": (
                    "improving"
                    if len(state.quality_scores) > 1
                    and state.quality_scores[-1] > state.quality_scores[0]
                    else "declining"
                ),
            },
            "conversation_metrics": {
                "total_words": self.conversation_metrics["total_words"],
                "average_response_length": avg_response_length,
                "message_count": len(state.messages),
            },
            "termination_reason": self._get_termination_reason(state),
        }

    def _get_termination_reason(self, state: CustomConversationState) -> str:
        """Determine why the conversation ended."""
        if state.should_end_by_rounds:
            return "Round limit reached"
        if state.conversation_ended:
            return "Explicit termination"
        if state.average_quality < 0.3:
            return "Low conversation quality"
        if state.engagement_level < 0.2:
            return "Low engagement level"
        if len(state.messages) > 50:
            return "Message limit reached"
        return "Natural conclusion"


async def main():
    """Demonstrate custom conversation agent usage."""
    # Create participant agents
    alice = SimpleAgent(
        name="Alice",
        model="gpt-4o-mini",
        instructions="You are Alice, a friendly AI assistant interested in technology.",
    )

    bob = SimpleAgent(
        name="Bob",
        model="gpt-4o-mini",
        instructions="You are Bob, a curious learner who asks thoughtful questions.",
    )

    charlie = SimpleAgent(
        name="Charlie",
        model="gpt-4o-mini",
        instructions="You are Charlie, an expert who provides detailed explanations.",
    )

    # Create initial state
    initial_state = CustomConversationState(
        speakers=["Alice", "Bob", "Charlie"],
        topic="The Future of AI in Education",
        max_rounds=3,
        engagement_level=0.7,  # Start with good engagement
    )

    # Create custom conversation agent
    conversation = CustomConversationAgent(
        name="education_discussion",
        participants=[alice, bob, charlie],
        initial_state=initial_state,
    )

    # Run the conversation
    try:
        # Start the conversation
        await conversation.arun(
            "Let's discuss how AI can transform education. "
            "Alice, what are your thoughts on AI-powered personalized learning?"
        )

        # Get final state
        final_state = conversation.get_state()

        # Display conversation messages
        for _i, msg in enumerate(final_state.messages):
            if isinstance(msg, HumanMessage):
                pass
            elif isinstance(msg, AIMessage):
                getattr(msg, "name", "Unknown")

        # Display progress tracking
        progress_info = get_conversation_progress(final_state)
        for _key, _value in progress_info.items():
            pass

        # Display quality metrics

        # Display conversation summary
        summary = conversation.get_conversation_summary()
        for _category, metrics in summary.items():
            if isinstance(metrics, dict):
                for _key, _value in metrics.items():
                    pass
            else:
                pass

    except Exception as e:
        logger.exception(f"Conversation failed: {e}")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
