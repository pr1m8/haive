"""
Agent for playing Connect 4.

This module defines the Connect 4 agent, which uses language models
to generate moves and analyze positions in the game.
"""
from typing import Dict, Any, List
from langgraph.types import Command
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.connect4.models import Connect4Move,Connect4PlayerDecision
from src.haive.games.connect4.state_manager import Connect4StateManager
from src.haive.games.connect4.config import Connect4AgentConfig
from src.haive.games.connect4.state import Connect4State
import time
import copy
from src.haive.core.engine.agent.agent import register_agent
@register_agent(Connect4AgentConfig)
class Connect4Agent(GameAgent[Connect4AgentConfig]):
    """Agent for playing Connect 4.

    This class implements the Connect 4 agent, which uses language models
    to generate moves and analyze positions in the game.
    """
    
    def __init__(self, config: Connect4AgentConfig):
        super().__init__(config)
        #print(self.engines)
        self.state_manager = Connect4StateManager
    
    def prepare_move_context(self, state: Connect4State, player: str) -> Dict[str, Any]:
        """Prepare context for move generation.

        This method prepares the context for move generation by formatting
        the legal moves and getting the player's last analysis.
        """
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = [f"Column {move.column}" for move in legal_moves]

        # Get player's last analysis (if available)
        player_analysis = None
        if player == "red" and state.red_analysis:
            player_analysis = state.red_analysis[-10:]
        elif player == "yellow" and state.yellow_analysis:
            player_analysis = state.yellow_analysis[-10:]

        # Calculate threats
        threats = self._calculate_threats(state, player)
        
        # ✅ Extract winning/blocking threats explicitly
        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "legal_moves": formatted_legal_moves,
            "move_history": [f"{i+1}. {state.turn}: Column {move.column}" for i, move in enumerate(state.move_history[-5:])],
            "player_analysis": player_analysis,
            "threats_winning_moves": threats["winning_moves"],  # Explicitly named
            "threats_blocking_moves": threats["blocking_moves"],  # Explicitly named
        }

    def _calculate_threats(self, state: Connect4State, player: str) -> Dict[str, List[int]]:
        """Calculate immediate threats and opportunities.

        This method calculates the immediate threats and opportunities
        for the given player in the current game state.
        """
        opponent = "yellow" if player == "red" else "red"
        
        player_winning_moves = []
        opponent_winning_moves = []

        for col in range(7):
            if state.is_column_full(col):
                continue

            row = state.get_next_row(col)

            # ✅ Check if this move wins for the player
            temp_state = copy.deepcopy(state)
            temp_state.board[row][col] = player
            if self.state_manager._check_win(temp_state, row, col):
                player_winning_moves.append(col)

            # ✅ Check if this move blocks opponent's win
            temp_state = copy.deepcopy(state)
            temp_state.board[row][col] = opponent
            if self.state_manager._check_win(temp_state, row, col):
                opponent_winning_moves.append(col)

        return {
            "winning_moves": player_winning_moves,
            "blocking_moves": opponent_winning_moves,
        }

        
    def prepare_analysis_context(self, state: Connect4State, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis with correct variables.

        This method prepares the context for position analysis by calculating
        threats and formatting the required fields.
        """
        threats = self._calculate_threats(state, player)

        # ✅ Ensure all required fields exist
        
        columns_usage = [sum(1 for row in state.board if row[col] is not None) for col in range(7)]
        threats_winning_moves = threats.get("winning_moves", [])
        threats_blocking_moves = threats.get("blocking_moves", [])

        return {
            "board": state.board_string,
            "turn": state.turn,
            "color": player,
            "move_history": [f"{i+1}. {state.turn}: Column {move.column}" for i, move in enumerate(state.move_history[-5:])],
            "threats_winning_moves": threats_winning_moves,
            "threats_blocking_moves": threats_blocking_moves,
            "columns_usage": columns_usage  # ✅ Now the model gets what it expects!
        }



    def extract_move(self, response: Connect4PlayerDecision) -> Connect4Move:
        """Extract move from engine response.

        This method extracts the move from the engine response.
        """
        return response.move
    
    def make_player1_move(self, state: Connect4State) -> Command:
        """Make a move for the red player.

        This method makes a move for the red player in the current game state.
        """
        return self.make_move(state, "red")
    
    def make_player2_move(self, state: Connect4State) -> Command:
        """Make a move for the yellow player.

        This method makes a move for the yellow player in the current game state.
        """
        return self.make_move(state, "yellow")
    
    def analyze_player1(self, state: Connect4State) -> Command:
        """Analyze position for the red player.

        This method analyzes the position for the red player in the current game state.
        """
        return self.analyze_position(state, "red")
    
    def analyze_player2(self, state: Connect4State) -> Command:
        """Analyze position for the yellow player.

        This method analyzes the position for the yellow player in the current game state.
        """
        return self.analyze_position(state, "yellow")
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state with better formatting and insights.

        This method visualizes the current game state with better formatting
        and insights. It displays the current player, game status, board,
        last move, and analysis from the previous turn.
        """
        # Create a Connect4State from the dict
        connect4_state = Connect4State(**state)

        print("\n" + "=" * 60)
        print(f"🎮 Current Player: {connect4_state.turn.upper()}")
        print(f"📌 Game Status: {connect4_state.game_status.upper()}")
        print("=" * 60)

        # 🎲 Display the board
        print("\n" + connect4_state.board_string)
        
        # 📝 Show last move if available
        if connect4_state.move_history:
            last_move = connect4_state.move_history[-1]
            player = "red" if len(connect4_state.move_history) % 2 == 1 else "yellow"
            print(f"\n📝 **Last Move:** {player.upper()} played in column {last_move.column}")

        # 🔍 **Show analysis from the previous turn**
        analysis = None
        analysis_color = None

        if connect4_state.red_analysis and connect4_state.turn == "yellow":
            analysis = connect4_state.red_analysis[-1]
            analysis_color = "Red"
        elif connect4_state.yellow_analysis and connect4_state.turn == "red":
            analysis = connect4_state.yellow_analysis[-1]
            analysis_color = "Yellow"

        if analysis:
            print(f"\n🔍 **{analysis_color} Analysis:**")
            print(f"   - 📈 Position Score: {analysis.get('position_score', 'N/A')}")
            print(f"   - 🎯 Center Control: {analysis.get('center_control', 'N/A')}/10")
            print(f"   - 🎯 Suggested Columns: {', '.join(map(str, analysis.get('suggested_columns', [])))}")
            print(f"   - ⚡ Winning Chances: {analysis.get('winning_chances', 'N/A')}%")

            # 🔺 Threat Analysis
            threats = analysis.get('threats', {})
            print("\n⚠️ **Threats:**")
            print(f"   - 🔴 Winning Moves: {', '.join(map(str, threats.get('winning_moves', []))) or 'None'}")
            print(f"   - 🛑 Blocking Moves: {', '.join(map(str, threats.get('blocking_moves', []))) or 'None'}")

        # Short delay for readability
        time.sleep(0.5)
