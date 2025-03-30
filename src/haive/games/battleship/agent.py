from src.haive.core.engine.agent.agent import Agent, register_agent
from langgraph.types import Command
from langgraph.constants import START, END
from typing import Optional, Dict, Tuple, List, Any, Literal
from src.haive.games.battleship.state import BattleshipGameState
from src.haive.games.battleship.state_manager import BattleshipGameStateManager
from src.haive.games.battleship.models import (
    PREBUILT_SHIPS, 
    BattleshipPlacement,
    BattleshipPlayerDecision,
    BattleshipAnalysis,
    Ship,
    Coordinates,
    BattleshipMoveModel
)
src.haive.core.engine.aug_llm import compose_runnable
from src.haive.games.battleship.config import BattleshipAgentConfig


@register_agent(BattleshipAgentConfig)
class BattleshipAgent(Agent[BattleshipAgentConfig]):
    def __init__(self, config: BattleshipAgentConfig):
        super().__init__(config)
        

    def setup_workflow(self):
        """Sets up the Battleship game workflow."""
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("place_ships_p1", self.player_1_ship_placement)
        self.graph.add_node("place_ships_p2", self.player_2_ship_placement)
        self.graph.add_node("player1_move", self.player_1_move)
        self.graph.add_node("player2_move", self.player_2_move)
        self.graph.add_node("check_game_status", self.check_game_status)

        if self.config.enable_analysis:
            self.graph.add_node("player1_analysis", self.player_1_analysis)
            self.graph.add_node("player2_analysis", self.player_2_analysis)

        # Workflow edges
        self.graph.add_edge(START, "initialize_game")
        self.graph.add_edge("initialize_game", "place_ships_p1")
        self.graph.add_edge("place_ships_p1", "place_ships_p2")
        #self.graph.add_node("end_game", self.end_game)
        if self.config.enable_analysis:
            # Set up flow with analysis
            self.graph.add_edge("place_ships_p2", "player1_analysis")
            self.graph.add_edge("player1_analysis", "player1_move")
            #self.graph.add_edge("player1_move", "check_game_status")
            self.graph.add_edge("player1_move", "check_game_status")
        
            self.graph.add_edge("player2_analysis", "player2_move")
            # Similar for player2
            self.graph.add_edge("player2_move", "check_game_status")
            
            # After status check, either continue to player1 or end game
            
            
        else:
            # Set up flow without analysis
            self.graph.add_edge("place_ships_p2", "player1_move")
            self.graph.add_edge("player1_move", "check_game_status")
           
            self.graph.add_edge("player2_move", "check_game_status")

    def initialize_game(self, state: Optional[BattleshipGameState] = None) -> Command:
        """Starts a new game with empty boards."""
        game_state = BattleshipGameStateManager.initialize()
        return Command(update=game_state.model_dump())

    #
    # 1) Ship Placement
    #
    def place_ship(self, state: BattleshipGameState, player: str) -> Command:
        """Places ships for a player using the LLM."""
        print(f"Placing ships for {player}...")
        private_state = getattr(state, f"{player}_private").model_copy()
        private_state.board.ships.clear()  # Ensure fresh placements

        placed_positions = set()
        for ship in PREBUILT_SHIPS:
            ship_name = ship.name
            ship_size = ship.size
            valid_placement = False
            attempts = 0

            while not valid_placement and attempts < 10:
                placement_input = {
                    "board_size": state.board_size,
                    "ship_name": ship_name,
                    "occupied_positions": [{"row": pos[0], "col": pos[1]} for pos in placed_positions]
                }

                # Get ship placement from LLM
                ship_placement: BattleshipPlacement = self.engines[f"{player}_ship_placement"].invoke(placement_input)

                if not ship_placement.coordinates:
                    attempts += 1
                    continue

                proposed_positions = {(c.row, c.col) for c in ship_placement.coordinates}
                
                # Validate placement
                if len(proposed_positions) == ship_size and private_state.board.is_valid_placement(proposed_positions):
                    # ✅ Register the ship correctly
                    new_ship = Ship(name=ship_name, size=ship_size, coordinates=list(ship_placement.coordinates))
                    private_state.board.ships.append(new_ship)
                    placed_positions.update(proposed_positions)
                    valid_placement = True
                    print(f"Successfully placed {ship_name} for {player} at {[c.to_tuple() for c in ship_placement.coordinates]}")

            if not valid_placement:
                raise ValueError(f"Failed to place {ship_name} for {player} after {attempts} attempts")

        return Command(update={f"{player}_private": private_state.model_dump()})

    #
    # 2) Move Execution
    #
    def make_move(self, state: BattleshipGameState, player: str) -> Command:
        """Gets the next move from LLM and applies it to the game state."""
        print(f"\n{player}'s turn to move...")
        opponent = "player2" if player == "player1" else "player1"

        # Debug current turn
        print(f"DEBUG: Current turn in state: {state.turn}")
        print(f"DEBUG: Expected player moving: {player}")
        
        # Validate it's actually this player's turn
        if state.turn != player:
            print(f"WARNING: Turn mismatch! State says it's {state.turn}'s turn but trying to move as {player}")
            # Return current state without changes
            return Command(update=state.model_dump())
        
        # Get player and opponent boards
        player_private = getattr(state, f"{player}_private").model_copy()
        opponent_private = getattr(state, f"{opponent}_private").model_copy()

        # Prepare hit/miss data as coordinate tuples for the LLM
        player_hits = [hit.to_tuple() for hit in player_private.board.hits]
        player_misses = [miss.to_tuple() for miss in player_private.board.misses]
        opponent_hits = [hit.to_tuple() for hit in opponent_private.board.hits]
        opponent_misses = [miss.to_tuple() for miss in opponent_private.board.misses]
        
        # Get move from LLM
        move_input = {
            "board_size": state.board_size,
            "your_hits": player_hits,
            "your_misses": player_misses,
            "opponent_hits": opponent_hits,
            "opponent_misses": opponent_misses,
            "your_sunken_ships": player_private.board.sunk_ships,
            "opponent_sunken_ships": opponent_private.board.sunk_ships,
            "strategic_thoughts": player_private.strategic_thoughts if player_private.strategic_thoughts else "",
            "turn": player  # Use current player, not opponent
        }
        
        # Get move decision from LLM
        move_result = self.engines[player].invoke(move_input)
        
        # Ensure we got a valid move object
        if not isinstance(move_result, BattleshipMoveModel):
            print(f"WARNING: Unexpected move result type: {type(move_result)}")
            # Try to convert if needed
            if hasattr(move_result, "move"):
                move = move_result.move
            elif isinstance(move_result, dict) and "row" in move_result and "col" in move_result:
                move = Coordinates(row=move_result["row"], col=move_result["col"])
            else:
                raise ValueError(f"Invalid move format from LLM: {move_result}")
        else:
            move = Coordinates(row=move_result.row, col=move_result.col)
            
        print(f"{player} chose to attack: ({move.row}, {move.col})")

        # Check if move has already been made
        previous_moves = [(c.row, c.col) for c in player_private.board.guesses]
        if (move.row, move.col) in previous_moves:
            print(f"WARNING: {player} tried to attack {(move.row, move.col)} again! Finding a new target...")
            # Find an unguessed position
            for r in range(state.board_size):
                for c in range(state.board_size):
                    if (r, c) not in previous_moves:
                        move = Coordinates(row=r, col=c)
                        print(f"Auto-selecting new target: ({move.row}, {move.col})")
                        break
                if (move.row, move.col) not in previous_moves:
                    break

        # Register attack on opponent's board
        attack_result = opponent_private.board.receive_attack(move.row, move.col)
        
        print(f"Attack result: {attack_result.result}" + 
            (f" (Sunk {attack_result.sunk_ship}!)" if attack_result.sunk_ship else ""))

        # Update the tracking for this player
        player_private.board.guesses.append(move)
        
        # Record hit/miss based on the result
        if attack_result.result == "hit" or attack_result.result == "sunk":
            player_private.board.hits.append(move)
        elif attack_result.result == "miss":
            player_private.board.misses.append(move)
                
        # Update move history
        move_entry = (player, (move.row, move.col), attack_result.result)
        new_move_history = list(state.move_history)
        new_move_history.append(move_entry)
        
        # Set game turn to opponent
        #new_turn = opponent
        #print(f"DEBUG: Switching turn from {player} to {new_turn}")

        # Return updates
        return Command(update={
            f"{player}_private": player_private.model_dump(),
            f"{opponent}_private": opponent_private.model_dump(),
            "move_history": new_move_history,
            #"turn": new_turn,  # Make sure to include turn in the update
        })
        # 3) Analysis
    #
    def analyze_position(self, state: BattleshipGameState, player: str) -> Command:
        """Analyzes the board for the given player."""
        print(f"\nAnalyzing position for {player}...")
        opponent = "player2" if player == "player1" else "player1"
        
        # Get player and opponent boards
        player_private = getattr(state, f"{player}_private").model_copy()
        opponent_private = getattr(state, f"{opponent}_private").model_copy()

        # Prepare hit/miss data as coordinate tuples for the LLM
        player_hits = [hit.to_tuple() for hit in player_private.board.hits]
        player_misses = [miss.to_tuple() for miss in player_private.board.misses]
        opponent_hits = [hit.to_tuple() for hit in opponent_private.board.hits]
        opponent_misses = [miss.to_tuple() for miss in opponent_private.board.misses]
        opponent_turn = opponent
        # Get analysis from LLM
        analysis_input = {
            "board_size": state.board_size,
            "your_hits": player_hits,
            "your_misses": player_misses,
            "opponent_hits": opponent_hits,
            "opponent_misses": opponent_misses,
            "your_sunken_ships": player_private.board.sunk_ships,
            "opponent_sunken_ships": opponent_private.board.sunk_ships,
            "strategic_thoughts": player_private.strategic_thoughts if player_private.strategic_thoughts else "",
            #"turn": opponent_turn
        }
        
        analysis_result = self.engines[f"{player}_analyzer"].invoke(analysis_input)
        
        # Store the analysis in player's strategic thoughts
        if hasattr(analysis_result, "analysis"):
            analysis_text = analysis_result.analysis
        else:
            analysis_text = str(analysis_result)
            
        # Limit strategic thoughts to prevent overflow
        player_private.strategic_thoughts = (player_private.strategic_thoughts or [])
        player_private.strategic_thoughts.append(analysis_text)
        
        # Keep only the last 5 thoughts to avoid state bloat
        if len(player_private.strategic_thoughts) > 5:
            player_private.strategic_thoughts = player_private.strategic_thoughts[-5:]

        return Command(update={f"{player}_private": player_private.model_dump()})

    #
    # 4) Check & Continue
    #
    def check_game_status(self, state: BattleshipGameState) -> Command[Literal["player1_analysis", "player2_analysis", "__end__"]]:
        """Determine if the game should continue or end and update game state."""
        print(f"Determining next step. Game status: {state.game_status}")
        
        # Check if all ships are sunk for either player
        player1_all_sunk = state.player1_private.board.all_ships_sunk()
        player2_all_sunk = state.player2_private.board.all_ships_sunk()
        
        # Create a copy of the state to update
        updated_state = state.model_copy()
        
        # If either player has all ships sunk, game is over
        if player1_all_sunk or player2_all_sunk:
            print("Game over! Updating state and routing to END")
            updated_state.game_status = "ended"
            
            if player1_all_sunk:
                updated_state.game_result = "player2"
                print("Player 2 has won! All Player 1's ships are sunk.")
            else:
                updated_state.game_result = "player1"
                print("Player 1 has won! All Player 2's ships are sunk.")
            goto=END
            # Return Command with updated state and route to END
            return Command(update=updated_state.model_dump(), goto=END)
        else:
            print("Game continues! Routing to next player")
            
            # Switch turn (in case it wasn't already handled in make_move)
            current_turn = state.turn
            updated_state.turn = "player2" if current_turn == "player1" else "player1"
            goto=f"{updated_state.turn}_analysis"
            # For the continue case, let the conditional edge routing handle the destination
            # Just return the updated state
            return Command(update=updated_state.model_dump(),goto=goto)



    # Wrappers for player-specific actions
    #
    def player_1_move(self, state: BattleshipGameState) -> Command:
        return self.make_move(state, "player1")

    def player_2_move(self, state: BattleshipGameState) -> Command:
        return self.make_move(state, "player2")

    def player_1_analysis(self, state: BattleshipGameState) -> Command:
        return self.analyze_position(state, "player1")

    def player_2_analysis(self, state: BattleshipGameState) -> Command:
        return self.analyze_position(state, "player2")

    def player_1_ship_placement(self, state: BattleshipGameState) -> Command:
        return self.place_ship(state, "player1")

    def player_2_ship_placement(self, state: BattleshipGameState) -> Command:
        return self.place_ship(state, "player2")
        
    def get_ship_symbol(self, ship_name: str) -> str:
        """Returns color-coded letters for different ships."""
        ship_symbols = {
            "Carrier": "\033[34mC\033[0m",     # Blue C
            "Battleship": "\033[32mB\033[0m",  # Green B
            "Cruiser": "\033[33mR\033[0m",     # Yellow R
            "Submarine": "\033[35mS\033[0m",   # Purple S
            "Destroyer": "\033[31mD\033[0m"    # Red D
        }
        return ship_symbols.get(ship_name, "?")  # Default to '?' if ship not found
        
    def run(self, **kwargs):
        """Starts the Battleship game and streams updates until the game ends."""
        # Initialize the game
        initial_state = BattleshipGameStateManager.initialize()
        
        # Configure runtime settings
        runtime_config = dict(self.runnable_config)
        runtime_config.setdefault('configurable', {})
        runtime_config['configurable']['recursion_limit'] = 60
        
        # Add any additional keyword arguments to the config
        for key, value in kwargs.items():
            runtime_config[key] = value
        
        print("🏁 Starting Battleship game...")
        print("-" * 60)
        
        try:
            # Stream the game loop
            for step in self.app.stream(
                initial_state.model_dump(), 
                config=runtime_config,
                debug=self.config.debug,
                stream_mode="values"
            ):
                self.display_game_state(step)
                
            # Display final game result
            print("\n" + "=" * 60)
            print("🏆 **Game Over!**")
            if step.get('game_result'):
                print(f"🎖 **Winner:** {step['game_result'].capitalize()}")
            else:
                print("🤝 **Draw!**")
                
        except Exception as e:
            print(f"\n❌ Error during game execution: {str(e)}")
            import traceback
            traceback.print_exc()
            
        return step  # Return the final state

    #
    def display_game_state(self, step: Dict[str, Any]):
        """Prints the current game state in a structured format."""
        if not self.config.visualize_board:
            return
            
        print("\n" + "=" * 60)
        print(f"🔷 **GAME STATE**")
        print(f"🎮 Turn: {step.get('turn', 'Unknown').capitalize()}")
        print(f"📌 Status: {step.get('game_status', 'Unknown')}")

        # Show the last move
        if step.get("move_history") and len(step["move_history"]) > 0:
            last_move = step["move_history"][-1]
            if isinstance(last_move, tuple) and len(last_move) >= 3:
                player, coords, result = last_move
                print(f"📝 Last Move: {player.capitalize()} attacked {coords}, Result: {result}")
            else:
                print(f"📝 Last Move: {last_move}")

        # Player 1's board with their ships
        print(f"\n🛥️  PLAYER 1'S BOARD:")
        if "player1_private" in step and "board" in step["player1_private"]:
            self.visualize_board_with_guesses(step["player1_private"]["board"], is_opponent_view=False)
        else:
            print("Board data unavailable")
        
        # Player 2's board with their ships
        print(f"\n🛥️  PLAYER 2'S BOARD:")
        if "player2_private" in step and "board" in step["player2_private"]:
            self.visualize_board_with_guesses(step["player2_private"]["board"], is_opponent_view=False)
        else:
            print("Board data unavailable")
    def visualize_board_with_guesses(self, board_state: Dict, is_opponent_view: bool = False):
        """
        Visualizes a player's board with appropriate view.
        
        Args:
            board_state: The board state to visualize
            is_opponent_view: If True, shows opponent's board (with player's attacks)
        """
        # Get board size with fallback
        board_size = board_state.get("size", 10)
        
        # Initialize empty board grid
        board_grid = {(r, c): "🟦" for r in range(board_size) for c in range(board_size)}
        
        # Place ships on grid (only if showing player's own board)
        if not is_opponent_view:
            # This is the player's own board, show their ships
            if "ships" in board_state and board_state["ships"]:
                for ship in board_state["ships"]:
                    ship_name = ship.get("name", "Unknown")
                    symbol = self.get_ship_symbol(ship_name)
                    
                    if "coordinates" in ship:
                        for coord in ship["coordinates"]:
                            try:
                                if isinstance(coord, dict) and "row" in coord and "col" in coord:
                                    row, col = coord["row"], coord["col"]
                                    board_grid[(row, col)] = symbol
                            except Exception as e:
                                continue
            
            # For player's own board, guesses from opponent will be shown as hits/misses
            # on the player's ships
            if "guesses" in board_state:
                for guess in board_state.get("guesses", []):
                    try:
                        if isinstance(guess, dict) and "row" in guess and "col" in guess:
                            row, col = guess["row"], guess["col"]
                            # Check if this is a hit on the player's ship
                            if any(
                                any(
                                    c.get("row") == row and c.get("col") == col
                                    for c in ship.get("coordinates", [])
                                )
                                for ship in board_state.get("ships", [])
                            ):
                                board_grid[(row, col)] = "🔥"  # Hit on player's ship
                            else:
                                board_grid[(row, col)] = "❌"  # Miss on player's board
                    except Exception as e:
                        continue
        else:
            # This is opponent's board view (from player's perspective)
            # Show player's hits and misses on opponent's board
            for hit in board_state.get("hits", []):
                try:
                    if isinstance(hit, dict) and "row" in hit and "col" in hit:
                        row, col = hit["row"], hit["col"]
                        board_grid[(row, col)] = "🔥"  # Hit on opponent's ship
                except Exception as e:
                    continue
                    
            for miss in board_state.get("misses", []):
                try:
                    if isinstance(miss, dict) and "row" in miss and "col" in miss:
                        row, col = miss["row"], miss["col"]
                        board_grid[(row, col)] = "❌"  # Miss on opponent's board
                except Exception as e:
                    continue
        
        # Print board
        print("\n   " + "  ".join(str(i) for i in range(board_size)))
        print("   " + "—" * (board_size * 3))
        
        for row in range(board_size):
            row_display = [f"{row} |"]
            for col in range(board_size):
                row_display.append(board_grid.get((row, col), "🟦"))
            print("  ".join(row_display))

        # Print legend
        print("\nLegend:")
        print("🟦 - Empty water      🔥 - Hit      ❌ - Miss")
        print(f"{self.get_ship_symbol('Carrier')} - Carrier (5)    " +
            f"{self.get_ship_symbol('Battleship')} - Battleship (4)    " +
            f"{self.get_ship_symbol('Cruiser')} - Cruiser (3)")
        print(f"{self.get_ship_symbol('Submarine')} - Submarine (3)    " +
            f"{self.get_ship_symbol('Destroyer')} - Destroyer (2)")


bs = BattleshipAgent(BattleshipAgentConfig())
bs.run()