"""Gamified Debate Agent - Modern Implementation.

This module implements a gamified debate using the modern conversation agent
pattern from haive-agents, providing proper topic handling and state management
without the deprecated DynamicGraph system.
"""

import logging
from typing import Any, Literal

from haive.agents.conversation.debate.agent import DebateConversation
from haive.agents.conversation.debate.state import DebateState
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GameDebateAgent(DebateConversation):
    """Gamified debate agent with scoring and tournament features.

    This agent extends the conversation debate system with game-like features:
    - Scoring system for arguments and rebuttals
    - Tournament bracket support
    - Performance statistics tracking
    - Ranking and leaderboard capabilities

    """

    # Mode identifier
    mode: Literal["game_debate"] = Field(
        default="game_debate", description="Game debate mode identifier"
    )

    # CRITICAL: Explicitly declare state schema type
    state_schema: type[BaseModel] = Field(
        default=DebateState, description="State schema class to use for this agent"
    )

    # Game-specific configuration
    scoring_enabled: bool = Field(
        default=True, description="Whether to enable argument scoring"
    )

    points_per_argument: int = Field(
        default=10, ge=1, le=50, description="Base points awarded per argument"
    )

    points_per_rebuttal: int = Field(
        default=15, ge=1, le=50, description="Base points awarded per rebuttal"
    )

    bonus_for_evidence: int = Field(
        default=5, ge=0, le=20, description="Bonus points for citing evidence"
    )

    penalty_for_repetition: int = Field(
        default=3, ge=0, le=10, description="Point penalty for repetitive arguments"
    )

    # Tournament features
    tournament_mode: bool = Field(
        default=False, description="Whether this is a tournament match"
    )

    match_id: str | None = Field(
        default=None, description="Unique identifier for tournament match"
    )

    bracket_position: str | None = Field(
        default=None, description="Position in tournament bracket (e.g., 'semifinal_1')"
    )

    # Performance tracking
    track_performance: bool = Field(
        default=True, description="Whether to track detailed performance metrics"
    )

    save_replay: bool = Field(
        default=True, description="Whether to save debate replay for analysis"
    )

    @model_validator(mode="after")
    @classmethod
    def validate_game_setup(cls) -> "GameDebateAgent":
        """Validate game configuration."""
        # Ensure state schema is set
        if not self.state_schema or self.state_schema != DebateState:
            self.state_schema = DebateState

        # Validate tournament settings
        if self.tournament_mode and not self.match_id:
            logger.warning("Tournament mode enabled but no match_id provided")

        return self

    def setup_agent(self) -> None:
        """Setup the game debate agent with proper state schema."""
        # Force DebateState as the state schema
        self.state_schema = DebateState

        # Enable schema generation from engines
        self.set_schema = True

        # Call parent setup
        super().setup_agent()

        logger.debug(
            f"GameDebateAgent setup complete with state schema: {self.state_schema}"
        )

    def _custom_initialization(self, state: DebateState) -> dict[str, Any]:
        """Initialize game-specific state fields."""
        # Get base debate initialization from DebateConversation
        base_init = super()._custom_initialization(state)

        # Add game-specific fields
        game_fields = {
            # Scoring system
            "player_scores": dict.fromkeys((self.debate_positions or {}).keys(), 0),
            "argument_scores": {},  # Track individual argument scores
            "rebuttal_scores": {},  # Track individual rebuttal scores
            "bonus_points": dict.fromkeys((self.debate_positions or {}).keys(), 0),
            "penalty_points": dict.fromkeys((self.debate_positions or {}).keys(), 0),
            # Performance metrics
            "response_times": {},  # Track response speed if available
            "argument_quality": {},  # Quality assessments
            "consistency_scores": {},  # Position consistency tracking
            # Tournament features
            "match_metadata": {
                "match_id": self.match_id,
                "bracket_position": self.bracket_position,
                "tournament_mode": self.tournament_mode,
            },
            # Game state
            "game_phase": "starting",  # starting, playing, scoring, complete
            "round_scores": [],  # Score progression by round
            "mvp_candidate": None,  # Most valuable player candidate
        }

        # Merge with base initialization
        base_init.update(game_fields)
        return base_init

    def _create_initial_message(self) -> BaseMessage:
        """Create the gamified debate introduction message."""
        positions = self.debate_positions if self.debate_positions is not None else {}
        positions_str = (
            "\n".join(
                [f"  🎯 {name}: {position}" for name, position in positions.items()]
            )
            if positions
            else "No positions assigned yet"
        )

        # Build game structure description
        game_features = []
        if self.scoring_enabled:
            game_features.append(
                f"📊 Scoring: {self.points_per_argument} pts per argument, {
                    self.points_per_rebuttal
                } pts per rebuttal"
            )
            if self.bonus_for_evidence > 0:
                game_features.append(
                    f"💎 Evidence Bonus: +{self.bonus_for_evidence} pts for citing sources"
                )
            if self.penalty_for_repetition > 0:
                game_features.append(
                    f"⚠️ Repetition Penalty: -{self.penalty_for_repetition} pts for redundant arguments"
                )

        if self.tournament_mode:
            game_features.append(
                f"🏆 Tournament Match: {self.bracket_position or 'Competition'}"
            )
            if self.match_id:
                game_features.append(f"🆔 Match ID: {self.match_id}")

        game_features_str = (
            "\n".join(game_features) if game_features else "Standard debate rules"
        )

        # Tournament-specific title
        title = (
            "🎮 Welcome to the Gamified Debate Tournament!"
            if self.tournament_mode
            else "🎮 Welcome to the Gamified Debate!"
        )

        return HumanMessage(
            content=f"""{title}

📋 **Topic**: {self.topic}

👥 **Players and Positions**:
{positions_str}

🎯 **Game Features**:
{game_features_str}

📜 **How to Win**:
• Make compelling, well-researched arguments
• Counter your opponent's points effectively
• Cite evidence and sources for bonus points
• Stay consistent with your position
• Engage with respect and intellectual honesty

🎲 **Let the game begin!** {next(iter(positions.keys())) if positions else "Players"}, present your opening move!"""
        )

    def process_response(self, state: DebateState) -> Command:
        """Process response with game scoring logic."""
        # Get base processing first
        try:
            base_updates = super().process_response(state)
            updates = (
                base_updates.update
                if hasattr(base_updates, "update") and base_updates.update
                else {}
            )
        except AttributeError as e:
            # Handle token usage tracking issues gracefully
            if "token_usage" in str(e):
                logger.warning(f"Token usage tracking not available: {e}")
                updates = {}
            else:
                raise

        if not state.current_speaker or not state.messages:
            return Command(update=updates)

        # Get last message for scoring
        last_msg = state.messages[-1]
        if not isinstance(last_msg, AIMessage) or not hasattr(last_msg, "name"):
            return Command(update=updates)

        speaker = last_msg.name
        content = str(last_msg.content)
        phase = getattr(state, "current_phase", "arguments")

        # Apply game scoring if enabled
        if self.scoring_enabled and speaker in (self.debate_positions or {}):
            score_updates = self._calculate_argument_score(
                content, speaker, phase, state
            )
            updates.update(score_updates)

        # Update game phase
        game_phase_updates = self._update_game_phase(state)
        updates.update(game_phase_updates)

        return Command(update=updates)

    def _calculate_argument_score(
        self, content: str, speaker: str, phase: str, state: DebateState
    ) -> dict[str, Any]:
        """Calculate and assign scores for arguments/rebuttals."""
        updates = {}
        base_score = 0
        bonus = 0
        penalty = 0

        # Base points by phase
        if phase == "arguments":
            base_score = self.points_per_argument
        elif phase == "rebuttals":
            base_score = self.points_per_rebuttal
        elif phase in ["opening", "closing"]:
            base_score = self.points_per_argument  # Same as regular argument

        # Evidence bonus detection
        if self.bonus_for_evidence > 0 and self._has_evidence(content):
            bonus += self.bonus_for_evidence

        # Repetition penalty detection
        if self.penalty_for_repetition > 0 and self._is_repetitive(
            content, speaker, state
        ):
            penalty += self.penalty_for_repetition

        # Calculate final score
        final_score = max(0, base_score + bonus - penalty)

        # Update player scores
        current_scores = getattr(state, "player_scores", {})
        current_scores[speaker] = current_scores.get(speaker, 0) + final_score
        updates["player_scores"] = current_scores

        # Track detailed scoring
        argument_scores = getattr(state, "argument_scores", {})
        if speaker not in argument_scores:
            argument_scores[speaker] = []

        argument_scores[speaker].append(
            {
                "content_preview": (
                    content[:100] + "..." if len(content) > 100 else content
                ),
                "base_score": base_score,
                "bonus": bonus,
                "penalty": penalty,
                "final_score": final_score,
                "phase": phase,
            }
        )
        updates["argument_scores"] = argument_scores

        # Update bonus and penalty tracking
        if bonus > 0:
            bonus_points = getattr(state, "bonus_points", {})
            bonus_points[speaker] = bonus_points.get(speaker, 0) + bonus
            updates["bonus_points"] = bonus_points

        if penalty > 0:
            penalty_points = getattr(state, "penalty_points", {})
            penalty_points[speaker] = penalty_points.get(speaker, 0) + penalty
            updates["penalty_points"] = penalty_points

        logger.debug(
            f"Scored {speaker}: {final_score} pts (base: {base_score}, bonus: {bonus}, penalty: {penalty})"
        )

        return updates

    def _has_evidence(self, content: str) -> bool:
        """Detect if content cites evidence or sources."""
        evidence_indicators = [
            "according to",
            "research shows",
            "studies indicate",
            "data suggests",
            "statistics show",
            "source:",
            "citation:",
            "reference:",
            "www.",
            "http",
            ".com",
            ".org",
            ".edu",
            "published in",
            "journal",
            "university",
            "institute",
            "report",
            "survey",
        ]

        content_lower = content.lower()
        return any(indicator in content_lower for indicator in evidence_indicators)

    def _is_repetitive(self, content: str, speaker: str, state: DebateState) -> bool:
        """Detect if content is repetitive of previous arguments."""
        # Get previous arguments from this speaker
        previous_args = getattr(state, "arguments_made", {}).get(speaker, [])

        if len(previous_args) < 2:  # Need at least 2 arguments to check repetition
            return False

        # Simple repetition check - could be enhanced with NLP similarity
        content_words = set(content.lower().split())

        for prev_arg in previous_args[-2:]:  # Check last 2 arguments
            prev_words = set(str(prev_arg).lower().split())
            # If more than 70% word overlap, consider repetitive
            overlap = len(content_words & prev_words) / max(len(content_words), 1)
            if overlap > 0.7:
                return True

        return False

    def _update_game_phase(self, state: DebateState) -> dict[str, Any]:
        """Update game phase based on debate progress."""
        updates = {}
        current_game_phase = getattr(state, "game_phase", "starting")

        # Transition logic
        if current_game_phase == "starting" and len(getattr(state, "messages", [])) > 1:
            updates["game_phase"] = "playing"
        elif current_game_phase == "playing" and getattr(
            state, "should_end_debate", False
        ):
            updates["game_phase"] = "scoring"
        elif current_game_phase == "scoring" and getattr(
            state, "conversation_ended", False
        ):
            updates["game_phase"] = "complete"

        return updates

    def conclude_conversation(self, state: DebateState) -> Command:
        """Create gamified conclusion with scores and winner declaration."""
        # Get base conclusion
        base_conclusion = super().conclude_conversation(state)
        base_updates = (
            base_conclusion.update if hasattr(base_conclusion, "update") else {}
        )

        # Calculate final scores and determine winner
        final_scores = getattr(state, "player_scores", {})
        winner = (
            max(final_scores.items(), key=lambda x: x[1])[0] if final_scores else None
        )

        # Build gamified summary
        summary_parts = [
            "🏁 **GAME OVER** - Debate Tournament Match Complete!",
            f"📋 Topic: '{self.topic}'",
            "",
            "🏆 **FINAL SCORES:**",
        ]

        # Display scores
        sorted_scores = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)
        for rank, (player, score) in enumerate(sorted_scores, 1):
            position = getattr(state, "debate_positions", {}).get(player, "Unknown")
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉"
            summary_parts.append(f"  {medal} {player} ({position}): {score} points")

        # Add detailed scoring breakdown
        if self.scoring_enabled:
            summary_parts.extend(["", "📊 **SCORING BREAKDOWN:**"])
            for player in final_scores:
                bonus = getattr(state, "bonus_points", {}).get(player, 0)
                penalty = getattr(state, "penalty_points", {}).get(player, 0)

                breakdown = f"  • {player}:"
                if bonus > 0:
                    breakdown += f" +{bonus} bonus"
                if penalty > 0:
                    breakdown += f" -{penalty} penalty"
                summary_parts.append(breakdown)

        # Tournament information
        if self.tournament_mode:
            summary_parts.extend(
                [
                    "",
                    "🏆 **TOURNAMENT INFO:**",
                    f"  • Match ID: {self.match_id or 'Unknown'}",
                    f"  • Bracket: {self.bracket_position or 'Unknown'}",
                    f"  • Advancing Player: {winner or 'TBD'}",
                ]
            )

        # Add performance stats
        if self.track_performance:
            summary_parts.extend(
                [
                    "",
                    "📈 **PERFORMANCE STATS:**",
                    f"  • Total Rounds: {len(getattr(state, 'phase_transitions', []))}",
                    f"  • Arguments Made: {getattr(state, 'total_arguments', 0)}",
                    f"  • Rebuttals Given: {getattr(state, 'total_rebuttals', 0)}",
                ]
            )

        conclusion_msg = SystemMessage(content="\n".join(summary_parts))

        # Update with game completion
        game_updates = {
            "messages": [conclusion_msg],
            "conversation_ended": True,
            "current_phase": "complete",
            "game_phase": "complete",
            "debate_winner": winner,
            "final_scores": final_scores,
        }

        base_updates.update(game_updates)
        return Command(update=base_updates)

    @classmethod
    def create_tournament_match(
        cls,
        topic: str,
        player_a: tuple[str, str],  # (name, position)
        player_b: tuple[str, str],  # (name, position)
        match_id: str,
        bracket_position: str = "tournament",
        **kwargs,
    ) -> "GameDebateAgent":
        """Create a tournament debate match."""

        name_a, pos_a = player_a
        name_b, pos_b = player_b

        # Create competitive agents
        agents = {}

        # Player A
        engine_a = AugLLMConfig(
            name=f"{name_a.lower()}_tournament_engine",
            system_message=(
                f"🎮 TOURNAMENT MODE ACTIVATED 🎮\n\n"
                f"You are {name_a} competing in a formal debate tournament.\n"
                f"Topic: '{topic}'\n"
                f"Your Position: {pos_a}\n\n"
                "WINNING STRATEGY:\n"
                "• Make 2-3 strong, evidence-backed arguments\n"
                "• Counter opponent's points decisively\n"
                "• Cite sources for bonus points\n"
                "• Maintain logical consistency\n"
                "• Be respectful but competitive\n\n"
                "This is a scored competition - give your best performance!"
            ),
            temperature=0.6,  # Slightly more focused for competition
        )
        agents[name_a] = SimpleAgent(
            name=f"{name_a}_tournament_agent", engine=engine_a, state_schema=DebateState
        )

        # Player B
        engine_b = AugLLMConfig(
            name=f"{name_b.lower()}_tournament_engine",
            system_message=(
                f"🎮 TOURNAMENT MODE ACTIVATED 🎮\n\n"
                f"You are {name_b} competing in a formal debate tournament.\n"
                f"Topic: '{topic}'\n"
                f"Your Position: {pos_b}\n\n"
                "WINNING STRATEGY:\n"
                "• Make 2-3 strong, evidence-backed arguments\n"
                "• Counter opponent's points decisively\n"
                "• Cite sources for bonus points\n"
                "• Maintain logical consistency\n"
                "• Be respectful but competitive\n\n"
                "This is a scored competition - give your best performance!"
            ),
            temperature=0.6,
        )
        agents[name_b] = SimpleAgent(
            name=f"{name_b}_tournament_agent", engine=engine_b, state_schema=DebateState
        )

        # Create tournament match
        tournament_kwargs = {
            "name": f"TournamentMatch_{match_id}",
            "participant_agents": agents,
            "topic": topic,
            "debate_positions": {name_a: pos_a, name_b: pos_b},
            "tournament_mode": True,
            "match_id": match_id,
            "bracket_position": bracket_position,
            "arguments_per_side": 3,
            "enable_opening_statements": True,
            "enable_closing_statements": True,
            "state_schema": DebateState,
        }

        # Merge with provided kwargs, avoiding conflicts
        for key, value in kwargs.items():
            if key not in tournament_kwargs:
                tournament_kwargs[key] = value

        return cls(**tournament_kwargs)

    def __repr__(self) -> str:
        """String representation of the game debate agent."""
        mode_str = "Tournament" if self.tournament_mode else "Game"
        positions = ", ".join(
            [
                f"{name}={pos[:15]}..."
                for name, pos in (self.debate_positions or {}).items()
            ]
        )
        return (
            f"{mode_str}DebateAgent(topic='{self.topic}', "
            f"positions=[{positions}], "
            f"scoring={self.scoring_enabled})"
        )
