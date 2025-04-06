from typing import Dict, Any
from langgraph.types import Command
from langgraph.graph import END
from src.haive.core.engine.agent.agent import Agent, register_agent
from src.haive.games.battleship.models import ShipPlacement, MoveCommand, GamePhase, ShipPlacementWrapper
from src.haive.games.battleship.state import BattleshipState
from src.haive.games.battleship.state_manager import BattleshipStateManager
from src.haive.games.battleship.config import BattleshipAgentConfig
from src.haive.core.graph.GraphBuilder import DynamicGraph
import time
import json


@register_agent(BattleshipAgentConfig)
class BattleshipAgent(Agent[BattleshipAgentConfig]):
    def __init__(self, config: BattleshipAgentConfig):
        self.state_manager = BattleshipStateManager()
        self.engines = config.engines  # Store reference to engines
        super().__init__(config)

    def ensure_state(self, state: Any) -> BattleshipState:
        """Ensure that state is a proper BattleshipState instance."""
        if isinstance(state, dict):
            return BattleshipState(**state)
        return state if isinstance(state, BattleshipState) else BattleshipState(**state)

    def setup_workflow(self):
        """Set up the workflow for the Battleship game."""
        gb = DynamicGraph(components=[self.config.engines], state_schema=self.config.state_schema)

        # Register nodes
        gb.add_node("initialize_game", self.initialize_game)
        gb.add_node("place_ships_player1", self.place_ships_player1)
        gb.add_node("place_ships_player2", self.place_ships_player2)
        gb.add_node("player1_move", self.player1_move)
        gb.add_node("player2_move", self.player2_move)
        
        # Add check nodes to separate player turns
        gb.add_node("check_game_over", self.check_game_over)
        gb.add_node("switch_to_player1", self.switch_to_player1)
        gb.add_node("switch_to_player2", self.switch_to_player2)

        # Setup phase
        gb.add_edge("initialize_game", "place_ships_player1")
        gb.add_edge("place_ships_player1", "place_ships_player2")

        if self.config.enable_analysis:
            # Add analysis nodes
            gb.add_node("player1_analysis", self.player1_analysis)
            gb.add_node("player2_analysis", self.player2_analysis)

            # Completely sequential flow to avoid state conflicts
            gb.add_edge("place_ships_player2", "player1_analysis")
            gb.add_edge("player1_analysis", "player1_move")
            gb.add_edge("player1_move", "check_game_over")
            
            # Route based on game over check
            gb.add_conditional_edges(
                "check_game_over",
                lambda state: "END" if self.ensure_state(state).is_game_over() else "switch_to_player2",
                {"END": END, "switch_to_player2": "switch_to_player2"}
            )
            
            # Player 2's turn after the switch
            gb.add_edge("switch_to_player2", "player2_analysis")
            gb.add_edge("player2_analysis", "player2_move")
            gb.add_edge("player2_move", "check_game_over")
            
            # Add the player 1 switch to connect back to player 1
            gb.add_conditional_edges(
                "switch_to_player1",
                lambda state: "END" if self.ensure_state(state).is_game_over() else "player1_analysis",
                {"END": END, "player1_analysis": "player1_analysis"}
            )
        else:
            # Simple flow without analysis
            gb.add_edge("place_ships_player2", "player1_move")
            gb.add_edge("player1_move", "check_game_over")
            
            # Route based on game over check
            gb.add_conditional_edges(
                "check_game_over",
                lambda state: "END" if self.ensure_state(state).is_game_over() else "switch_to_player2",
                {"END": END, "switch_to_player2": "switch_to_player2"}
            )
            
            # Player 2's turn
            gb.add_edge("switch_to_player2", "player2_move")
            gb.add_edge("player2_move", "check_game_over")
            
            # Return to player 1
            gb.add_conditional_edges(
                "switch_to_player1",
                lambda state: "END" if self.ensure_state(state).is_game_over() else "player1_move",
                {"END": END, "player1_move": "player1_move"}
            )

        self.graph = gb.build()

    def check_game_over(self, state: Dict[str, Any]) -> Command:
        """Check if the game is over."""
        state_obj = self.ensure_state(state)
        
        # Check if the game is over
        if state_obj.is_game_over():
            # Update winner if not already set
            if not state_obj.winner:
                state_obj.winner = (
                    "player1" if state_obj.player2_state.board.all_ships_sunk() else "player2"
                )
            state_obj.game_phase = GamePhase.ENDED
            return Command(update=state_obj.model_dump(), goto=END)
        
        # Continue to the switch node
        return Command(update=state_obj.model_dump(), goto="switch_to_player2")

    def switch_to_player1(self, state: Dict[str, Any]) -> Command:
        """Switch to player 1's turn."""
        state_obj = self.ensure_state(state)
        
        # Check if the game is over (double-check)
        if state_obj.is_game_over():
            # Update winner if not already set
            if not state_obj.winner:
                state_obj.winner = (
                    "player1" if state_obj.player2_state.board.all_ships_sunk() else "player2"
                )
            state_obj.game_phase = GamePhase.ENDED
            return Command(update=state_obj.model_dump(), goto=END)
        
        # Switch to player 1
        state_obj.current_player = "player1"
        
        # If enable_analysis is True, go to player1_analysis, otherwise to player1_move
        next_node = "player1_analysis" if self.config.enable_analysis else "player1_move"
        
        return Command(update=state_obj.model_dump(), goto=next_node)

    def switch_to_player2(self, state: Dict[str, Any]) -> Command:
        """Switch to player 2's turn."""
        state_obj = self.ensure_state(state)
        
        # Check if the game is over (double-check)
        if state_obj.is_game_over():
            # Update winner if not already set
            if not state_obj.winner:
                state_obj.winner = (
                    "player1" if state_obj.player2_state.board.all_ships_sunk() else "player2"
                )
            state_obj.game_phase = GamePhase.ENDED
            return Command(update=state_obj.model_dump(), goto=END)
        
        # Switch to player 2
        state_obj.current_player = "player2"
        
        # If enable_analysis is True, go to player2_analysis, otherwise to player2_move
        next_node = "player2_analysis" if self.config.enable_analysis else "player2_move"
        
        return Command(update=state_obj.model_dump(), goto=next_node)

    def analyze_position(self, state: Dict[str, Any], player: str) -> Command:
        """Common method for analyzing positions."""
        try:
            state_obj = self.ensure_state(state)
            
            # Check if game is in playing phase
            if state_obj.game_phase != GamePhase.PLAYING:
                # Skip analysis and go directly to the player's move
                return Command(update=state_obj.model_dump(), goto=f"{player}_move")
            
            # Get the appropriate engine
            engine_key = f"{player}_analyzer"
            engine = self.engines.get(engine_key)
            if not engine:
                print(f"WARNING: Missing analyzer engine: {engine_key}")
                return Command(update=state_obj.model_dump(), goto=f"{player}_move")

            # Get public state for the player
            public_state = state_obj.get_public_state_for_player(player)
            
            # Invoke the engine
            result = engine.invoke(public_state)
            
            # Handle different possible result formats
            if isinstance(result, dict) and "analysis" in result:
                analysis = result["analysis"]
            elif hasattr(result, "analysis"):
                analysis = result.analysis
            else:
                analysis = str(result)
            
            # Update the state with the analysis
            updated_state = self.state_manager.add_analysis(state_obj, player, analysis)
            
            return Command(update=updated_state.model_dump(), goto=f"{player}_move")
        except Exception as e:
            # Detailed error logging
            import traceback
            print(f"FULL ERROR for {player} analysis:")
            traceback.print_exc()
            
            # Update error message but don't stop the game
            state_obj.error_message = f"Analysis error for {player}: {str(e)}"
            return Command(update=state_obj.model_dump(), goto=f"{player}_move")

    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize a new game."""
        new_state = self.state_manager.initialize()
        return Command(update=new_state.model_dump(), goto="place_ships_player1")

    def place_ships_player1(self, state: Dict[str, Any]) -> Command:
        """Place ships for player 1."""
        return self.place_ships(state, "player1")

    def place_ships_player2(self, state: Dict[str, Any]) -> Command:
        """Place ships for player 2."""
        return self.place_ships(state, "player2")

    def place_ships(self, state: Dict[str, Any], player: str) -> Command:
        """Common method for ship placement."""
        state_obj = self.ensure_state(state)
        player_state = state_obj.get_player_state(player)
        occupied_positions = []  # Start with empty list for first player
        
        # For the second player, get occupied positions from the first player
        if player == "player2" and state_obj.player1_state.has_placed_ships:
            occupied_positions = state_obj.player1_state.board.get_occupied_positions()
        
        # Get the appropriate engine
        engine_key = f"{player}_ship_placement"
        engine = self.engines.get(engine_key)
        if not engine:
            raise ValueError(f"Missing engine: {engine_key}")

        try:
            # Invoke the engine
            result = engine.invoke({"occupied_positions": occupied_positions})
            
            # Handle different possible return types
            placements = []
            if isinstance(result, ShipPlacementWrapper):
                # If it's a ShipPlacementWrapper instance
                placements = result.placements
            elif hasattr(result, "placements"):
                # If it's another structured output with placements attribute
                placements = result.placements
            elif isinstance(result, dict) and "placements" in result:
                # If it's a dictionary with placements key
                placements_data = result["placements"]
                for placement_data in placements_data:
                    if isinstance(placement_data, ShipPlacement):
                        placements.append(placement_data)
                    elif isinstance(placement_data, dict):
                        placements.append(ShipPlacement(**placement_data))
            elif isinstance(result, list):
                # If it's directly a list of placements
                for placement_data in result:
                    if isinstance(placement_data, ShipPlacement):
                        placements.append(placement_data)
                    elif isinstance(placement_data, dict):
                        placements.append(ShipPlacement(**placement_data))
            
            if not placements:
                print(f"WARNING: No valid placements found in LLM response, raw result: {result}")
                state_obj.error_message = f"Failed to generate valid ship placements for {player}"
                return Command(update=state_obj.model_dump(), goto="initialize_game")
            
            # Update the state with the placements
            updated_state = self.state_manager.place_ships(state_obj, player, placements)
            
            # Determine next step
            next_node = "place_ships_player2" if player == "player1" else (
                "player1_analysis" if self.config.enable_analysis else "player1_move"
            )
            
            return Command(update=updated_state.model_dump(), goto=next_node)
        except Exception as e:
            import traceback
            print(f"Ship placement error for {player}: {e}")
            traceback.print_exc()
            # Update error message
            state_obj.error_message = f"Ship placement error for {player}: {str(e)}"
            return Command(update=state_obj.model_dump(), goto="initialize_game")

    def player1_move(self, state: Dict[str, Any]) -> Command:
        """Make a move for player 1."""
        return self.make_move(state, "player1", "check_game_over")

    def player2_move(self, state: Dict[str, Any]) -> Command:
        """Make a move for player 2."""
        return self.make_move(state, "player2", "check_game_over")

    def make_move(self, state: Dict[str, Any], player: str, next_node: str = "check_game_over") -> Command:
        """Common method for making moves."""
        state_obj = self.ensure_state(state)
        
        # Check if it's the player's turn and game is in playing phase
        if state_obj.current_player != player or state_obj.game_phase != GamePhase.PLAYING:
            return Command(update=state_obj.model_dump(), goto=next_node)

        # Get the appropriate engine
        engine_key = f"{player}_move"
        engine = self.engines.get(engine_key)
        if not engine:
            raise ValueError(f"Missing engine: {engine_key}")

        try:
            # Get public state for the player
            public_state = state_obj.get_public_state_for_player(player)
            
            # Invoke the engine
            result = engine.invoke(public_state)
            
            # Handle different possible return types
            if isinstance(result, MoveCommand):
                move_command = result
            elif isinstance(result, dict) and "row" in result and "col" in result:
                move_command = MoveCommand(row=result["row"], col=result["col"])
            else:
                print(f"WARNING: Invalid move format returned by LLM: {result}")
                # Fallback to a valid move (first available position)
                move_command = self._find_valid_move(state_obj, player)
                
            # Update the state with the move
            updated_state = self.state_manager.make_move(state_obj, player, move_command)
            
            return Command(update=updated_state.model_dump(), goto=next_node)
        except Exception as e:
            import traceback
            print(f"Move error for {player}: {e}")
            traceback.print_exc()
            # Update error message but don't stop the game
            state_obj.error_message = f"Move error for {player}: {str(e)}"
            return Command(update=state_obj.model_dump(), goto=next_node)
            
    def _find_valid_move(self, state: BattleshipState, player: str) -> MoveCommand:
        """Find a valid move when the LLM fails to provide one."""
        opponent = state.get_opponent(player)
        opponent_state = state.get_player_state(opponent)
        player_state = state.get_player_state(player)
        
        # Get all previously attacked positions
        attacked = set((c.row, c.col) for c in player_state.board.attacks)
        
        # First, check for partially hit ships and target adjacent cells
        for hit in player_state.board.successful_hits:
            # Try adjacent positions
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_row, new_col = hit.row + dx, hit.col + dy
                # Check if position is valid and not already attacked
                if 0 <= new_row < 10 and 0 <= new_col < 10 and (new_row, new_col) not in attacked:
                    return MoveCommand(row=new_row, col=new_col)
        
        # Try all positions on the board
        for row in range(10):
            for col in range(10):
                if (row, col) not in attacked:
                    return MoveCommand(row=row, col=col)
                    
        # If all positions have been attacked (shouldn't happen), return a random one
        import random
        return MoveCommand(row=random.randint(0, 9), col=random.randint(0, 9))

    def player1_analysis(self, state: Dict[str, Any]) -> Command:
        """Analyze position for player 1."""
        return self.analyze_position(state, "player1", "player1_move")

    def player2_analysis(self, state: Dict[str, Any]) -> Command:
        """Analyze position for player 2."""
        return self.analyze_position(state, "player2", "player2_move")

    def analyze_position(self, state: Dict[str, Any], player: str, next_node: str) -> Command:
        """Common method for analyzing positions."""
        try:
            state_obj = self.ensure_state(state)
            
            # Check if game is in playing phase
            if state_obj.game_phase != GamePhase.PLAYING:
                # Skip analysis and go directly to the player's move
                return Command(update=state_obj.model_dump(), goto=next_node)
            
            # Get the appropriate engine
            engine_key = f"{player}_analyzer"
            engine = self.engines.get(engine_key)
            if not engine:
                print(f"WARNING: Missing analyzer engine: {engine_key}")
                return Command(update=state_obj.model_dump(), goto=next_node)

            # Get public state for the player
            public_state = state_obj.get_public_state_for_player(player)
            
            # Invoke the engine
            result = engine.invoke(public_state)
            
            # Handle different possible result formats
            if isinstance(result, dict) and "analysis" in result:
                analysis = result["analysis"]
            elif hasattr(result, "analysis"):
                analysis = result.analysis
            else:
                analysis = str(result)
            
            # Update the state with the analysis
            updated_state = self.state_manager.add_analysis(state_obj, player, analysis)
            
            return Command(update=updated_state.model_dump(), goto=next_node)
        except Exception as e:
            # Detailed error logging
            import traceback
            print(f"FULL ERROR for {player} analysis:")
            traceback.print_exc()
            
            # Update error message but don't stop the game
            state_obj.error_message = f"Analysis error for {player}: {str(e)}"
            return Command(update=state_obj.model_dump(), goto=next_node)

    def check_game_status(self, state: Dict[str, Any]) -> Command:
        """Check the game status after a move."""
        state_obj = self.ensure_state(state)
        
        # Check if the game is over
        if state_obj.is_game_over():
            # Update winner if not already set
            if not state_obj.winner:
                state_obj.winner = (
                    "player1" if state_obj.player2_state.board.all_ships_sunk() else "player2"
                )
            state_obj.game_phase = GamePhase.ENDED
            return Command(update=state_obj.model_dump(), goto=END)

        # Switch player
        next_player = "player2" if state_obj.current_player == "player1" else "player1"
        state_obj.current_player = next_player
        
        # Determine next step based on current player and analysis settings
        if self.config.enable_analysis:
            next_step = f"{next_player}_analysis"
        else:
            next_step = f"{next_player}_move"
        
        return Command(update=state_obj.model_dump(), goto=next_step)

    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """Run the game with optional visualization."""
        if not self.app:
            self.compile()
            
        if visualize:
            try:
                final_state = None
                step_number = 0
                # Use self.runnable_config for proper configuration
                for step in self.app.stream({}, stream_mode="values", debug=self.config.debug, config=self.runnable_config):
                    step_number += 1
                    print(f"\n--- GAME STATE (Step {step_number}) ---")
                    print(f"Turn: {step.get('current_player')}")
                    print(f"Phase: {step.get('game_phase')}")
                    print(f"Winner: {step.get('winner', 'None')}")
                    
                    # Display error if any
                    if step.get('error_message'):
                        print(f"\n[ERROR] {step.get('error_message')}")
                    
                    # If in playing phase, show board stats
                    if step.get('game_phase') == 'playing':
                        try:
                            # Try to get hit stats safely
                            p1_state = step.get('player1_state', {})
                            p2_state = step.get('player2_state', {})
                            p1_board = p1_state.get('board', {})
                            p2_board = p2_state.get('board', {})
                            
                            p1_hits = len(p1_board.get('successful_hits', []))
                            p2_hits = len(p2_board.get('successful_hits', []))
                            p1_sunk = len(p1_board.get('sunk_ships', []))
                            p2_sunk = len(p2_board.get('sunk_ships', []))
                            
                            print(f"\nPlayer 1 Hits: {p1_hits}, Ships Sunk: {p1_sunk}")
                            print(f"Player 2 Hits: {p2_hits}, Ships Sunk: {p2_sunk}")
                            
                            # Show last move if available
                            move_history = step.get('move_history', [])
                            if move_history:
                                last_player, last_outcome = move_history[-1]
                                print(f"Last Move: {last_player} -> {last_outcome}")
                        except Exception as stats_error:
                            print(f"Error showing stats: {stats_error}")
                    
                    # Show ship placement in setup phase
                    if step.get('game_phase') == 'setup':
                        p1_state = step.get('player1_state', {})
                        p2_state = step.get('player2_state', {})
                        print(f"Player 1 placed ships: {p1_state.get('has_placed_ships', False)}")
                        print(f"Player 2 placed ships: {p2_state.get('has_placed_ships', False)}")
                    
                    time.sleep(0.5)
                    final_state = step
                
                # Show final game state
                if final_state and final_state.get('game_phase') == 'ended':
                    winner = final_state.get('winner', 'None')
                    print(f"\n🎮 GAME OVER! Winner: {winner} 🎮")
                
                return final_state
            except Exception as e:
                import traceback
                print(f"Game run error: {e}")
                traceback.print_exc()
                return {}
        
        # Non-visualized run
        return self.run({}, config=self.runnable_config)