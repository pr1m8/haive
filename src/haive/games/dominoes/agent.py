from typing import Dict, Any, List, Union, Literal, Optional
from langgraph.types import Command
from langgraph.graph import END
from src.haive.games.framework.base.agent import GameAgent
from src.haive.games.dominoes.models import DominoMove, DominoesPlayerDecision, DominoTile
from src.haive.games.dominoes.state import DominoesState
from src.haive.games.dominoes.state_manager import DominoesStateManager
from src.haive.games.dominoes.config import DominoesAgentConfig
from src.haive.core.engine.agent.agent import register_agent
from src.haive.core.graph.GraphBuilder import DynamicGraph
import time
import logging

logger = logging.getLogger(__name__)

@register_agent(DominoesAgentConfig)
class DominoesAgent(GameAgent[DominoesAgentConfig]):
    """Agent for playing dominoes."""
    
    def __init__(self, config: Optional[DominoesAgentConfig] = None):
        # Use default config if not provided
        if config is None:
            config = DominoesAgentConfig()
            
        # Set state manager
        self.state_manager = DominoesStateManager
        super().__init__(config)
    
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new Dominoes game.
        
        Args:
            state (Dict[str, Any]): The initial state.
            
        Returns:
            Command: Command with updated state.
        """
        game_state = self.state_manager.initialize()
        return Command(update=game_state, goto="player1_move")
    
    def prepare_move_context(self, state: DominoesState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        legal_moves = self.state_manager.get_legal_moves(state)
        formatted_legal_moves = [str(move) for move in legal_moves]
        
        hand = state.hands[player]
        formatted_hand = [str(tile) for tile in hand]
        
        player_analysis = None
        if player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]
        
        pip_count = sum(tile.left + tile.right for tile in hand)
        
        return {
            "player": player,
            "hand": formatted_hand,
            "pip_count": pip_count,
            "board": state.board_string,
            "open_ends": [state.left_value, state.right_value] if state.board else [],
            "legal_moves": formatted_legal_moves,
            "boneyard_count": len(state.boneyard),
            "opponent_count": {p: len(state.hands[p]) for p in state.players if p != player},
            "move_history": state.move_history[-5:],
            "player_analysis": player_analysis
        }
    
    def make_player1_move(self, state: DominoesState) -> Command:
        """Make a move for player1.
        
        Args:
            state (DominoesState): The current game state.
            
        Returns:
            Command: Command with updated state.
        """
        # Only make a move if it's player1's turn
        if state.turn != "player1":
            # If it's not player1's turn, just pass through the state
            goto = "analyze_player1" if state.turn == "player2" else "player2_move"
            return Command(update=state, goto=goto)
        
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: DominoesState) -> Command:
        """Make a move for player2.
        
        Args:
            state (DominoesState): The current game state.
            
        Returns:
            Command: Command with updated state.
        """
        # Only make a move if it's player2's turn
        if state.turn != "player2":
            # If it's not player2's turn, just pass through the state
            goto = "analyze_player2" if state.turn == "player1" else "player1_move"
            return Command(update=state, goto=goto)
        
        return self.make_move(state, "player2")
    
    def make_move(self, state: DominoesState, player: str) -> Command:
        """Make a move for the specified player.
        
        Args:
            state (DominoesState): The current game state.
            player (str): The player to make the move for.
            
        Returns:
            Command: Command with updated state.
        """
        # Make sure it's the player's turn
        if state.turn != player:
            # If it's not this player's turn, just pass through to the appropriate next node
            goto = f"analyze_{player}"
            return Command(update=state, goto=goto)
        
        # Prepare context for the move
        context = self.prepare_move_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_player"
        engine = self.engines[engine_key]
        
        # Generate move
        try:
            move_decision = engine.invoke(context)
            move = self.extract_move(move_decision)
            
            # Validate the move
            legal_moves = self.state_manager.get_legal_moves(state)
            
            # If move is "pass", it's always valid if returned by get_legal_moves
            if move == "pass" and "pass" in legal_moves:
                updated_state = self.state_manager.apply_move(state, move)
            # Otherwise, need to find a matching legal move
            elif move != "pass":
                # Find matching legal move
                valid_move = None
                for legal_move in legal_moves:
                    if legal_move == "pass":
                        continue
                    
                    # Check if tiles match (regardless of orientation)
                    if ((legal_move.tile.left == move.tile.left and legal_move.tile.right == move.tile.right) or
                        (legal_move.tile.left == move.tile.right and legal_move.tile.right == move.tile.left)) and \
                       legal_move.location == move.location:
                        valid_move = legal_move
                        break
                
                if valid_move:
                    updated_state = self.state_manager.apply_move(state, valid_move)
                else:
                    # If no valid move found, use the first legal move
                    fallback_move = legal_moves[0]
                    updated_state = self.state_manager.apply_move(state, fallback_move)
            else:
                # If an invalid move was provided, use the first legal move
                fallback_move = legal_moves[0]
                updated_state = self.state_manager.apply_move(state, fallback_move)
                
        except Exception as e:
            # If any error occurs, log it and use a fallback move
            logger.error(f"Error making move: {e}")
            legal_moves = self.state_manager.get_legal_moves(state)
            fallback_move = legal_moves[0]
            updated_state = self.state_manager.apply_move(state, fallback_move)
        
        # Return the updated state with conditional goto
        if updated_state.game_status == 'game_over' or 'win' in updated_state.game_status:
            return Command(update=updated_state, goto=END)
        
        # Determine next node based on player
        goto = "analyze_player2" if player == "player1" else "analyze_player1"
        return Command(update=updated_state, goto=goto)
    
    def extract_move(self, response: DominoesPlayerDecision) -> Union[DominoMove, Literal["pass"]]:
        """Extract move from engine response."""
        if response.pass_turn:
            return "pass"
        return response.move
    
    def prepare_analysis_context(self, state: DominoesState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        hand = state.hands[player]
        formatted_hand = [str(tile) for tile in hand]
        
        pip_count = sum(tile.left + tile.right for tile in hand)
        
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
    
    def analyze_player1(self, state: DominoesState) -> Command:
        """Analyze position for player1.
        
        Args:
            state (DominoesState): The current game state.
            
        Returns:
            Command: Command with updated state.
        """
        # Only analyze if it's player1's turn coming up
        if state.turn != "player1":
            return Command(update=state, goto="player1_move")
        
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: DominoesState) -> Command:
        """Analyze position for player2.
        
        Args:
            state (DominoesState): The current game state.
            
        Returns:
            Command: Command with updated state.
        """
        # Only analyze if it's player2's turn coming up
        if state.turn != "player2":
            return Command(update=state, goto="player2_move")
        
        return self.analyze_position(state, "player2")
    
    def analyze_position(self, state: DominoesState, player: str) -> Command:
        """Analyze the current position for the specified player.
        
        Args:
            state (DominoesState): The current game state.
            player (str): The player to analyze the position for.
            
        Returns:
            Command: Command with updated state.
        """
        # Only analyze if it's this player's turn
        if state.turn != player:
            # If it's not this player's turn, skip analysis
            goto = f"{player}_move"
            return Command(update=state, goto=goto)
        
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_analyzer"
        
        try:
            engine = self.engines[engine_key]
            
            # Generate analysis
            analysis = engine.invoke(context)
            
            # Update state with analysis
            updated_state = self.state_manager.update_analysis(state, analysis, player)
        except Exception as e:
            # If any error occurs, log it and skip analysis
            logger.error(f"Error during analysis: {e}")
            updated_state = state
        
        # Return the updated state
        goto = f"{player}_move"
        return Command(update=updated_state, goto=goto)
    
    def check_game_status(self, state: DominoesState) -> str:
        """Check if the game is over.
        
        Args:
            state (DominoesState): The current game state.
            
        Returns:
            str: Next node to go to.
        """
        if state.game_status == 'game_over' or 'win' in state.game_status:
            return END
        
        # Determine next node based on turn
        return "player1_move" if state.turn == "player1" else "player2_move"
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a DominoesState from the dict
        domino_state = DominoesState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Current Player: {domino_state.turn}")
        print(f"📌 Game Status: {domino_state.game_status}")
        print("=" * 50)
        
        # Show the board
        print("\n" + domino_state.board_string)
        
        # Print player hands
        for player in domino_state.players:
            hand = domino_state.hands[player]
            formatted_hand = [str(tile) for tile in hand]
            print(f"\n{player}'s hand: {', '.join(formatted_hand)} (Pip count: {sum(tile.left + tile.right for tile in hand)})")
        
        # Print boneyard
        print(f"\nBoneyard: {len(domino_state.boneyard)} remaining tiles")
        
        # Print last move if available
        if domino_state.move_history:
            print(f"\nLast move: {domino_state.move_history[-1]}")
        
        # Print analysis if available
        if hasattr(domino_state, 'player1_analysis') and domino_state.player1_analysis and domino_state.turn == "player1":
            print(f"\nPlayer 1 Analysis: {domino_state.player1_analysis[-1]}")
        if hasattr(domino_state, 'player2_analysis') and domino_state.player2_analysis and domino_state.turn == "player2":
            print(f"\nPlayer 2 Analysis: {domino_state.player2_analysis[-1]}")
    
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """Run the full game, optionally visualizing each step."""
        if visualize:
            initial_state = self.state_manager.initialize()  # Start with empty state, the initialize node will create the proper state
            try:
                for step in self.app.stream(initial_state, stream_mode="values", debug=True, config=self.runnable_config):
                    self.visualize_state(step)
                    time.sleep(1)  # Add delay for better visualization
                return step
            except Exception as e:
                logger.error(f"Error running game: {e}")
                return {}
        else:
            return self.run({})
    
    def setup_workflow(self) -> None:
        """Set up the game workflow."""
        # Create the graph builder with the state schema
        gb = DynamicGraph(
            components=[self.config],
            state_schema=self.config.state_schema
        )
        
        # Add nodes for the main game flow
        gb.add_node("initialize", self.initialize_game)
        gb.add_node("player1_move", self.make_player1_move)
        gb.add_node("player2_move", self.make_player2_move)
        gb.add_node("analyze_player1", self.analyze_player1)
        gb.add_node("analyze_player2", self.analyze_player2)
        
        # Set up complete graph edges to ensure the workflow can navigate all paths
        gb.add_edge("initialize", "player1_move")
        gb.add_edge("player1_move", "analyze_player2")
        gb.add_edge("analyze_player2", "player2_move")
        gb.add_edge("player2_move", "analyze_player1")
        gb.add_edge("analyze_player1", "player1_move")
        
        # Build the graph
        self.graph = gb.build()
        
        # Store app for later use in run_game
        self.app = self.graph.compile()

# For direct script execution
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    
    # Create and run the game agent
    agent = DominoesAgent()
    agent.run_game(visualize=True)