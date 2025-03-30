from typing import Dict, Any, List
import time
from langgraph.types import Command
from src.haive.games.framework.base import GameAgent
from src.haive.games.single_player.wordle.models import WordConnectionsState, WordConnectionsMove, WordConnectionsPlayerDecision, WordConnectionsAnalysis
from src.haive.games.single_player.wordle.state_manager import WordConnectionsStateManager
from src.haive.games.single_player.wordle.config import WordConnectionsAgentConfig
from src.haive.core.engine.agent.agent import register_agent

@register_agent(WordConnectionsAgentConfig)
class WordConnectionsAgent(GameAgent[WordConnectionsAgentConfig]):
    """Agent for playing the Word Connections game."""
    
    def __init__(self, config: WordConnectionsAgentConfig = WordConnectionsAgentConfig()):
        """Initialize the Word Connections agent."""
        super().__init__(config)
        self.state_manager = WordConnectionsStateManager
    
    def prepare_move_context(self, state: WordConnectionsState, player: str) -> Dict[str, Any]:
        """Prepare context for move generation."""
        # Format recent moves for display
        formatted_move_history = []
        for move in state.move_history[-5:]:  # Last 5 moves
            formatted_move_history.append(f"{move}")
        
        # Initialize player analysis
        player_analysis = {}
        
        # Get analysis if available
        if player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]
        
        # Prepare the context
        return Command(update={
            "board": state.board_string,
            "turn": state.turn,
            "player": player,
            "move_history": formatted_move_history,
            "player_analysis": player_analysis,
            "player1_score": state.player1_score,
            "player2_score": state.player2_score
        })
    
    def extract_move(self, response: WordConnectionsPlayerDecision) -> WordConnectionsMove:
        """Extract move from engine response."""
        return response.move
    
    def make_player1_move(self, state: WordConnectionsState) -> Command:
        """Make a move for player1."""
        return self.make_move(state, "player1")
    
    def make_player2_move(self, state: WordConnectionsState) -> Command:
        """Make a move for player2."""
        return self.make_move(state, "player2")
    
    def prepare_analysis_context(self, state: WordConnectionsState, player: str) -> Dict[str, Any]:
        """Prepare context for position analysis."""
        # Format recent moves for display
        formatted_move_history = []
        for move in state.move_history[-5:]:  # Last 5 moves
            formatted_move_history.append(f"{move}")
            
        return {
            "board": state.board_string,
            "turn": state.turn,
            "player": player,
            "move_history": formatted_move_history,
            "player1_score": state.player1_score,
            "player2_score": state.player2_score
        }
    
    def analyze_player1(self, state: WordConnectionsState) -> Command:
        """Analyze position for player1."""
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: WordConnectionsState) -> Command:
        """Analyze position for player2."""
        return self.analyze_position(state, "player2")
    
    def should_continue_game(self, state: WordConnectionsState) -> bool:
        """Check if the game should continue."""
        return state.game_status == "ongoing"
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Visualize the current game state."""
        # Create a WordConnectionsState from the dict
        game_state = WordConnectionsState(**state)
        
        print("\n" + "=" * 60)
        print(f"🎮 Word Connections Game")
        if game_state.game_source == "nyt":
            print(f"📅 NYT Connections {game_state.game_date}")
        print(f"📌 Status: {game_state.game_status.upper()}")
        print(f"🏆 Categories found: {len(game_state.discovered_groups)}/4")
        print("=" * 60)
        
        # Print the board
        print("\n" + game_state.board_string)
        
        # Print last move if available
        if game_state.move_history:
            last_move = game_state.move_history[-1]
            print(f"\n📝 Last Move: {last_move}")
        
        # Print analysis if available
        if game_state.analysis_history:
            last_analysis = game_state.analysis_history[-1]
            print(f"\n🔍 Analysis:")
            
            # Print potential groups
            if "potential_groups" in last_analysis and last_analysis["potential_groups"]:
                print("\nPotential Groups:")
                for i, group in enumerate(last_analysis["potential_groups"][:3]):
                    if "category" in group and "words" in group:
                        print(f"{i+1}. {group['category']}: {', '.join(group['words'])}")
            
            # Print difficult words
            if "difficult_words" in last_analysis and last_analysis["difficult_words"]:
                print("\nAmbiguous Words:")
                print(", ".join(last_analysis["difficult_words"][:8]))
            
            # Print strategy
            if "strategy" in last_analysis and last_analysis["strategy"]:
                print("\nStrategy:")
                strategy = last_analysis["strategy"]
                if len(strategy) > 150:
                    print(f"{strategy[:150]}...")
                else:
                    print(strategy)
        
        # Game outcome
        if game_state.game_status != "ongoing":
            if game_state.game_status == "victory":
                print("\n🎉 Congratulations! You've solved all categories!")
            elif game_state.game_status == "defeat":
                print("\n❌ Game over! You've run out of attempts.")
                
                # Show remaining categories
                if len(game_state.discovered_groups) < len(game_state.categories):
                    print("\nRemaining categories were:")
                    for category, words in game_state.categories.items():
                        if category not in game_state.discovered_groups:
                            print(f"- {category}: {', '.join(words)}")
        
        # Add a short delay for readability
        time.sleep(0.5)