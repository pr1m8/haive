"""
Controller for the Clue game.

This module provides the game controller that manages the state and flow of the Clue game.
"""
from typing import List, Dict, Optional, Set
import random
from dataclasses import dataclass, field

from src.haive.games.clue.models import (
    ClueSolution, ClueGuess, ClueResponse, ClueHypothesis,
    ValidSuspect, ValidWeapon, ValidRoom, 
    ClueCard, GameStatus
)
from src.haive.games.clue.engines import clue_engines
from src.haive.core.engine.aug_llm import AugLLMEngine

@dataclass
class CluePlayer:
    """Represents a player in the Clue game."""
    name: str
    cards: List[ClueCard] = field(default_factory=list)
    player_engine: Optional[AugLLMEngine] = None
    analysis_engine: Optional[AugLLMEngine] = None

@dataclass
class ClueGameState:
    """Represents the state of a Clue game."""
    solution: ClueSolution
    players: List[CluePlayer]
    current_player_index: int = 0
    current_turn: int = 1
    max_turns: int = 20
    guess_history: List[tuple[ClueGuess, ClueResponse]] = field(default_factory=list)
    status: GameStatus = GameStatus.IN_PROGRESS
    winner: Optional[str] = None

class ClueGameController:
    """Controller for the Clue game."""
    
    def __init__(self, player_names: List[str], max_turns: int = 20):
        """Initialize a new Clue game.
        
        Args:
            player_names: Names of the players
            max_turns: Maximum number of turns before the game ends
        """
        self.player_names = player_names
        self.max_turns = max_turns
        self.game_state = self._setup_game()
        
    def _setup_game(self) -> ClueGameState:
        """Set up a new game with shuffled cards and solution."""
        # Create solution
        suspects = list(ValidSuspect)
        weapons = list(ValidWeapon)
        rooms = list(ValidRoom)
        
        # Select random solution elements
        solution_suspect = random.choice(suspects)
        solution_weapon = random.choice(weapons)
        solution_room = random.choice(rooms)
        
        solution = ClueSolution(
            suspect=solution_suspect,
            weapon=solution_weapon,
            room=solution_room
        )
        
        # Remove solution cards from deck
        suspects.remove(solution_suspect)
        weapons.remove(solution_weapon)
        rooms.remove(solution_room)
        
        # Create deck with remaining cards
        deck: List[ClueCard] = []
        deck.extend(suspects)
        deck.extend(weapons)
        deck.extend(rooms)
        
        # Shuffle the deck
        random.shuffle(deck)
        
        # Create players with engines
        players = []
        for i, name in enumerate(self.player_names):
            engine_prefix = f"player{i+1}"
            player = CluePlayer(
                name=name,
                cards=[],
                player_engine=AugLLMEngine(clue_engines[f"{engine_prefix}_player"]),
                analysis_engine=AugLLMEngine(clue_engines[f"{engine_prefix}_analyzer"])
            )
            players.append(player)
        
        # Deal cards to players
        cards_per_player = len(deck) // len(players)
        for i, player in enumerate(players):
            start_idx = i * cards_per_player
            end_idx = (i + 1) * cards_per_player if i < len(players) - 1 else len(deck)
            player.cards = deck[start_idx:end_idx]
        
        return ClueGameState(
            solution=solution,
            players=players,
            max_turns=self.max_turns
        )
    
    def get_game_state(self) -> ClueGameState:
        """Get the current game state."""
        return self.game_state
    
    def make_guess(self, player_idx: int, guess: ClueGuess) -> ClueResponse:
        """Process a player's guess and return the response.
        
        Args:
            player_idx: Index of the player making the guess
            guess: The guess made by the player
            
        Returns:
            A response indicating whether the guess was correct or which player refuted it
        """
        if self.game_state.status != GameStatus.IN_PROGRESS:
            raise ValueError("Game is not in progress")
            
        if player_idx != self.game_state.current_player_index:
            raise ValueError("Not this player's turn")
        
        # Check if the guess matches the solution
        if (guess.suspect == self.game_state.solution.suspect and
            guess.weapon == self.game_state.solution.weapon and
            guess.room == self.game_state.solution.room):
            
            # Player wins
            self.game_state.status = GameStatus.FINISHED
            self.game_state.winner = self.game_state.players[player_idx].name
            
            response = ClueResponse(
                responding_player=None,
                is_correct=True,
                refuting_card=None
            )
            
            self.game_state.guess_history.append((guess, response))
            return response
        
        # Check if any player can refute the guess
        next_player_idx = (player_idx + 1) % len(self.game_state.players)
        current_idx = next_player_idx
        
        while current_idx != player_idx:
            current_player = self.game_state.players[current_idx]
            refuting_cards: List[ClueCard] = []
            
            # Check if player has any of the cards in the guess
            if guess.suspect in current_player.cards:
                refuting_cards.append(guess.suspect)
            if guess.weapon in current_player.cards:
                refuting_cards.append(guess.weapon)
            if guess.room in current_player.cards:
                refuting_cards.append(guess.room)
            
            if refuting_cards:
                # Player refutes with a random matching card
                refuting_card = random.choice(refuting_cards)
                
                response = ClueResponse(
                    responding_player=current_player.name,
                    is_correct=False,
                    refuting_card=refuting_card
                )
                
                self.game_state.guess_history.append((guess, response))
                
                # Move to next player for next turn
                self.game_state.current_player_index = (self.game_state.current_player_index + 1) % len(self.game_state.players)
                self.game_state.current_turn += 1
                
                # Check if max turns reached
                if self.game_state.current_turn > self.game_state.max_turns:
                    self.game_state.status = GameStatus.FINISHED
                    self.game_state.winner = None  # No winner if max turns reached
                
                return response
            
            # Move to next player
            current_idx = (current_idx + 1) % len(self.game_state.players)
        
        # No player could refute
        response = ClueResponse(
            responding_player=None,
            is_correct=False,
            refuting_card=None
        )
        
        self.game_state.guess_history.append((guess, response))
        
        # Move to next player for next turn
        self.game_state.current_player_index = (self.game_state.current_player_index + 1) % len(self.game_state.players)
        self.game_state.current_turn += 1
        
        # Check if max turns reached
        if self.game_state.current_turn > self.game_state.max_turns:
            self.game_state.status = GameStatus.FINISHED
            self.game_state.winner = None  # No winner if max turns reached
        
        return response
    
    def generate_board_string(self) -> str:
        """Generate a string representation of the game board."""
        # A simple representation for now
        return "Clue Game Board\n" + "-" * 20
    
    def get_player_view(self, player_idx: int) -> Dict:
        """Get the game state from a specific player's point of view.
        
        Args:
            player_idx: Index of the player
            
        Returns:
            A dictionary with the game state visible to the player
        """
        player = self.game_state.players[player_idx]
        
        return {
            "board_string": self.generate_board_string(),
            "current_turn_number": self.game_state.current_turn,
            "max_turns": self.game_state.max_turns,
            "player_cards": player.cards,
            "guess_history": self.game_state.guess_history,
            "is_your_turn": player_idx == self.game_state.current_player_index,
            "game_status": self.game_state.status,
            "winner": self.game_state.winner
        }
    
    async def generate_ai_guess(self, player_idx: int) -> ClueGuess:
        """Generate a guess using the player's AI engine.
        
        Args:
            player_idx: Index of the AI player
            
        Returns:
            The generated guess
        """
        player = self.game_state.players[player_idx]
        if not player.player_engine:
            raise ValueError(f"Player {player.name} does not have a player engine")
        
        player_view = self.get_player_view(player_idx)
        
        # Use the AI engine to generate a guess
        result = await player.player_engine.arun(**player_view)
        guess = result["guess"]
        
        # Make sure the returned value is a ClueGuess
        if not isinstance(guess, ClueGuess):
            raise ValueError(f"AI engine returned {type(guess)} instead of ClueGuess")
        
        return guess
    
    async def generate_ai_analysis(self, player_idx: int) -> ClueHypothesis:
        """Generate an analysis using the player's AI analysis engine.
        
        Args:
            player_idx: Index of the AI player
            
        Returns:
            The generated analysis
        """
        player = self.game_state.players[player_idx]
        if not player.analysis_engine:
            raise ValueError(f"Player {player.name} does not have an analysis engine")
        
        player_view = self.get_player_view(player_idx)
        
        # Use the AI engine to generate an analysis
        result = await player.analysis_engine.arun(**player_view)
        analysis = result["analysis"]
        
        # Make sure the returned value is a ClueHypothesis
        if not isinstance(analysis, ClueHypothesis):
            raise ValueError(f"AI engine returned {type(analysis)} instead of ClueHypothesis")
        
        return analysis 