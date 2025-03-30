# src/haive/agents/agent_games/dominoes/agent.py

from typing import Dict, Any, List, Union, Literal
from langgraph.types import Command
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.dominoes.models import DominoesState, DominoMove, DominoesPlayerDecision
from src.haive.games.dominoes.state import DominoesStateManager
from src.haive.games.dominoes.config import DominoesAgentConfig
from src.haive.core.engine.agent.agent import register_agent
import time
@register_agent(DominoesAgentConfig)
class DominoesAgent(GameAgent[DominoesState]):
    """Agent for playing dominoes."""
    
    def __init__(self, config: DominoesAgentConfig):
        super().__init__(config)
        self.state_manager = DominoesStateManager
    
    def prepare_move_context(self, state: DominoesState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Get legal moves for player
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = [str(move) for move in legal_moves]
        
        # Format player's hand
        hand = state.hands[player]
        formatted_hand = [str(tile) for tile in hand]
        
        # Get player's analysis if available
        player_analysis = None
        if player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]
        
        # Calculate pip count
        pip_count = sum(tile.left + tile.right for tile in hand)
        
        # Prepare the context for the LLM
        return {
            "player": player,
            "hand": formatted_hand,
            "pip_count": pip_count,
            "board": state.board_string,
            "open_ends": [state.left_value, state.right_value] if state.board else [],
            "legal_moves": formatted_legal_moves,
            "boneyard_count": len(state.boneyard),
            "opponent_count": {p: len(state.hands[p]) for p in state.players if p != player},
            "move_history": state.move_history[-5:],  # Last 5 moves
            "player_analysis": player_analysis
        }
    
    def prepare_analysis_context(self, state: DominoesState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        # Format player's hand
        hand = state.hands[player]
        formatted_hand = [str(tile) for tile in hand]
        
        # Calculate pip count
        pip_count = sum(tile.left + tile.right for tile in hand)
        
        # Get counts of each value in hand
        value_counts = {}
        for i in range(7):  # Values 0-6
            value_counts[i] = sum(1 for tile in hand if tile.left == i or tile.right == i)
        
        return {
            "player": player,
            "hand": formatted_hand,
            "pip_count": pip_count,
            "value_counts": value_counts,
            "board": state.board_string,
            "open_ends": [state.left_value, state.right_value] if state.board else [],
            "boneyard_count": len(state.boneyard),
            "opponent_count": {p: len(state.hands[p]) for p in state.players if p != player},
            "move_history": state.move_history[-5:]  # Last 5 moves
        }
    
    def extract_move(self, response: DominoesPlayerDecision) -> Union[DominoMove, Literal["pass"]]:
        """Extract move from engine response."""
        if response.pass_turn:
            return "pass"
        return response.move
    
    def make_player1_move(self, state: DominoesState) -> Command:
        """Make a move for player 1."""
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: DominoesState) -> Command:
        """Make a move for player 2."""
        return self.make_move(state, "player2")
    
    def analyze_player1(self, state: DominoesState) -> Command:
        """Analyze position for player 1."""
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: DominoesState) -> Command:
        """Analyze position for player 2."""
        return self.analyze_position(state, "player2")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a DominoesState from the dict
        domino_state = DominoesState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {domino_state.turn}")
        print(f"📌 Game Status: {domino_state.game_status}")
        print("=" * 50)
        
        # Print the board
        print("\n" + domino_state.board_string)
        
        # Print player information
        for player in domino_state.players:
            is_current = "➡️ " if player == domino_state.turn else "  "
            hand = domino_state.hands[player]
            
            print(f"\n{is_current} {player}'s Hand ({len(hand)} tiles):")
            print("  " + " ".join([str(tile) for tile in hand]))
            
            # Show score
            print(f"  Score: {domino_state.scores[player]}")
        
        # Print boneyard information
        print(f"\n🎯 Boneyard: {len(domino_state.boneyard)} tiles remaining")
        
        # Print last move if available
        if domino_state.move_history:
            last_move = domino_state.move_history[-1]
            if last_move == "pass":
                print(f"\n📝 Last Move: {domino_state.players[(domino_state.players.index(domino_state.turn) - 1) % len(domino_state.players)]} passed")
            else:
                print(f"\n📝 Last Move: {last_move}")
        
        # Print analyses if available
        if domino_state.player1_analysis and domino_state.turn == "player2":  # Show player1's analysis after their move
            last_analysis = domino_state.player1_analysis[-1]
            print("\n🔍 Player 1's Analysis:")
            print(f"   - Hand Strength: {last_analysis.get('hand_strength', 'N/A')}/10")
            print(f"   - Open Ends: {last_analysis.get('open_ends', 'N/A')}")
            print(f"   - Strategy: {last_analysis.get('suggested_strategy', 'N/A')}")
        
        if domino_state.player2_analysis and domino_state.turn == "player1":  # Show player2's analysis after their move
            last_analysis = domino_state.player2_analysis[-1]
            print("\n🔍 Player 2's Analysis:")
            print(f"   - Hand Strength: {last_analysis.get('hand_strength', 'N/A')}/10")
            print(f"   - Open Ends: {last_analysis.get('open_ends', 'N/A')}")
            print(f"   - Strategy: {last_analysis.get('suggested_strategy', 'N/A')}")
        
        # Add a short delay for readability
        time.sleep(0.5)