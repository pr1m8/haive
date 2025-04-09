from src.haive.games.mastermind.config import MastermindConfig
from src.haive.games.mastermind.models import MastermindGuess, MastermindAnalysis, ColorCode
from src.haive.games.mastermind.state import MastermindState
from src.haive.games.mastermind.state_manager import MastermindStateManager
from src.haive.games.framework.base.agent import GameAgent
from src.haive.core.graph.GraphBuilder import DynamicGraph
from typing import Dict, Any, List, Optional
import time 
from src.haive.core.engine.agent.agent import register_agent
from langgraph.types import Command

@register_agent(MastermindConfig)
class MastermindAgent(GameAgent[MastermindConfig]):
    """Agent for playing Mastermind.

    This class implements the Mastermind game agent, which uses language models
    to generate guesses and analyze positions in the game.
    """
    
    def __init__(self, config: MastermindConfig = MastermindConfig()):
        """Initialize the Mastermind agent.

        Args:
            config (MastermindConfig): The configuration for the Mastermind game.
        """
        
        self.state_manager = MastermindStateManager
        #self.engines = config.aug_llm_configs
        super().__init__(config)
        
        # Check for version updates
        self.check_version_update()
    def check_version_update(self) -> None:
        """Check if the game version is up to date.
        
        Compares the version in the config with the latest version in the config module.
        Logs a warning if they don't match.
        """
        if self.config.version != VERSION:
            print(f"⚠️ Warning: Running Mastermind version {self.config.version}, but latest is {VERSION}")
            print("   Consider updating to the latest version for bug fixes and improvements.")
            # Update the version in the config
            self.config.version = VERSION
    def initialize_game(self, state: Dict[str, Any]) -> Command:
        """Initialize the Mastermind game.

        If a secret code is not already configured, this method uses the codemaker engine
        to generate one. It then constructs the initial game state with the given parameters.

        Args:
            state (Dict[str, Any]): Initial state dictionary (unused here but required for interface).

        Returns:
            Command: Initialization command containing the new game state.
        """
        # If secret code is not provided, generate it using LLM
        secret_code = self.config.secret_code
        if not secret_code:
            # Use the codemaker engine to generate a code
            codemaker_engine = self.engines["codemaker"]#.create_runnable()
            secret_code = codemaker_engine.invoke({})
        
        # Initialize the game state
        game_state = self.state_manager.initialize(
            codemaker=self.config.codemaker,
            colors=self.config.colors,
            code_length=self.config.code_length,
            max_turns=self.config.max_turns,
            secret_code=secret_code
        )
        
        return Command(update=game_state.model_dump() if hasattr(game_state, "model_dump") else game_state.dict())
    
    def prepare_guess_context(self, state: MastermindState, player: str) -> Dict[str, Any]:
        """Build input context for the guess engine.

        Includes the current board string, turn info, past guesses with feedback,
        and any previous analysis by the current codebreaker.

        Args:
            state (MastermindState): Current game state.
            player (str): The guessing player ('player1' or 'player2').

        Returns:
            Dict[str, Any]: Context dictionary for guess generation.
        """
        # Format guess history
        guess_history = []
        for i, (guess, feedback) in enumerate(zip(state.guesses, state.feedback)):
            guess_str = f"Turn {i+1}: {', '.join(guess.colors)}"
            feedback_str = f"🎯 {feedback.correct_position}, 🔄 {feedback.correct_color}"
            guess_history.append(f"{guess_str} → {feedback_str}")
        
        # Get player's analysis if available
        player_analysis = None
        if player == "player1" and state.player1_analysis:
            player_analysis = state.player1_analysis[-1]
        elif player == "player2" and state.player2_analysis:
            player_analysis = state.player2_analysis[-1]
        
        if not player_analysis:
            player_analysis = "No previous analysis available."
        
        # Prepare the context
        return {
            "board_string": state.board_string,
            "current_turn_number": state.current_turn_number,
            "max_turns": state.max_turns,
            "guess_history": "\n".join(guess_history),
            "player_analysis": player_analysis
        }
    
    def prepare_analysis_context(self, state: MastermindState, player: str) -> Dict[str, Any]:
        """Build input context for position analysis engine.

        Includes history of guesses with feedback and turn metadata.

        Args:
            state (MastermindState): Current game state.
            player (str): The analyzing player ('player1' or 'player2').

        Returns:
            Dict[str, Any]: Context dictionary for analysis.
        """

        # Format guess history
        guess_history = []
        for i, (guess, feedback) in enumerate(zip(state.guesses, state.feedback)):
            guess_str = f"Turn {i+1}: {', '.join(guess.colors)}"
            feedback_str = f"🎯 {feedback.correct_position}, 🔄 {feedback.correct_color}"
            guess_history.append(f"{guess_str} → {feedback_str}")
        
        # Prepare the context
        return {
            "current_turn_number": state.current_turn_number,
            "max_turns": state.max_turns,
            "guess_history": "\n".join(guess_history)
        }
    
    def extract_guess(self, response: Any) -> MastermindGuess:
        """Extract a structured MastermindGuess object from the engine response.

        Args:
            response (Any): Response from the guess engine.

        Returns:
            MastermindGuess: Parsed guess object.
        """
        # The response should already be a MastermindGuess object
        return response
    
    def make_player1_guess(self, state: MastermindState) -> Command:
        """Handle player1's guess if they are the codebreaker.

        Returns immediately if player1 is the codemaker.

        Args:
            state (MastermindState): Current game state.

        Returns:
            Command: Updated game state after the guess or passthrough if not allowed.
        """
        if state.codemaker == "player1":
            # Player1 is the codemaker, not the guesser
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        return self.make_guess(state, "player1")
    
    def make_player2_guess(self, state: MastermindState) -> Command:
        """Handle player2's guess if they are the codebreaker.

        Returns immediately if player2 is the codemaker.

        Args:
            state (MastermindState): Current game state.

        Returns:
            Command: Updated game state after the guess or passthrough if not allowed.
        """
        if state.codemaker == "player2":
            # Player2 is the codemaker, not the guesser
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        return self.make_guess(state, "player2")
    
    def make_guess(self, state: MastermindState, player: str) -> Command:
        """Invoke the appropriate guess engine and apply the resulting move.

        Skips if it is not the player's turn or the game is no longer ongoing.

        Args:
            state (MastermindState): Current game state.
            player (str): 'player1' or 'player2'.

        Returns:
            Command: Updated game state with the new guess applied.
        """

        # Check if it's the player's turn
        if state.turn != player:
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Check if game is over
        if state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for the guess
        context = self.prepare_guess_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_guesser"
        engine = self.engines[engine_key]#.create_runnable()
        
        # Generate guess
        guess = engine.invoke(context)
        
        # Apply the guess
        new_state = self.state_manager.apply_move(state, guess)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def analyze_player1(self, state: MastermindState) -> Command:
        """Run analysis for player1 if they are the codebreaker.

        Args:
            state (MastermindState): Current game state.

        Returns:
            Command: Updated state with appended analysis or passthrough.
        """

        if state.codemaker == "player1":
            # Player1 is the codemaker, not the codebreaker
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        return self.analyze_position(state, "player1")
    
    def analyze_player2(self, state: MastermindState) -> Command:
        """Run analysis for player2 if they are the codebreaker.

        Args:
            state (MastermindState): Current game state.

        Returns:
            Command: Updated state with appended analysis or passthrough.
        """
        if state.codemaker == "player2":
            # Player2 is the codemaker, not the codebreaker
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        return self.analyze_position(state, "player2")
    
    def analyze_position(self, state: MastermindState, player: str) -> Command:
        """Invoke the analysis engine to evaluate the current position.

        Args:
            state (MastermindState): Current game state.
            player (str): 'player1' or 'player2'.

        Returns:
            Command: Updated state including the newly generated analysis.
        """

        if not self.config.enable_analysis:
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Skip analysis if game is over
        if state.game_status != "ongoing":
            return Command(update=state.model_dump() if hasattr(state, "model_dump") else state.dict())
        
        # Prepare context for analysis
        context = self.prepare_analysis_context(state, player)
        
        # Select the appropriate engine
        engine_key = f"{player}_analyzer"
        engine = self.engines[engine_key]#.create_runnable()
        
        # Generate analysis
        analysis = engine.invoke(context)
        
        # Update state with analysis
        new_state = self.state_manager.add_analysis(state, player, analysis)
        
        # Return the updated state
        return Command(update=new_state.model_dump() if hasattr(new_state, "model_dump") else new_state.dict())
    
    def visualize_state(self, state: Dict[str, Any]) -> None:
        """Print a visual summary of the current game state.

        Shows the board, guesses, codemaker, game status, and most recent analysis.

        Args:
            state (Dict[str, Any]): The state dictionary to render.
        """
        if not self.config.visualize:
            return
            
        # Create a MastermindState from the dict
        game_state = MastermindState(**state)
        
        print("\n" + "=" * 50)
        print(f"🎮 Game: Mastermind v{self.config.version}")
        print(f"📊 Turn: {game_state.current_turn_number}/{game_state.max_turns}")
        print(f"🎭 Codemaker: {game_state.codemaker}, Codebreaker: {'player2' if game_state.codemaker == 'player1' else 'player1'}")
        print(f"📝 Status: {game_state.game_status}")
        
        # Only show secret code if game is over
        if game_state.game_status != "ongoing":
            print(f"🔑 Secret Code: {', '.join(game_state.secret_code)}")
        
        print("=" * 50)
        
        # Print the board with all guesses and feedback
        if game_state.guesses:
            print("\n" + game_state.board_string)
        else:
            print("\nNo guesses yet.")
        
        # Print analysis if available
        codebreaker = "player2" if game_state.codemaker == "player1" else "player1"
        if codebreaker == "player1" and game_state.player1_analysis:
            last_analysis = game_state.player1_analysis[-1]
            print(f"\n🔍 Codebreaker's Analysis:")
            print(f"Possible combinations: {last_analysis['possible_combinations']}")
            print(f"High probability colors: {', '.join(last_analysis['high_probability_colors'])}")
            print(f"Strategy: {last_analysis['strategy']}")
            #print(f"Recommended next guess: {', '.join(last_analysis['recommended_guess'])}")
            print(f"Confidence: {last_analysis['confidence']}/10")
            
        elif codebreaker == "player2" and game_state.player2_analysis:
            last_analysis = game_state.player2_analysis[-1]
            print(f"\n🔍 Codebreaker's Analysis:")
            print(f"Possible combinations: {last_analysis['possible_combinations']}")
            print(f"High probability colors: {', '.join(last_analysis['high_probability_colors'])}")
            # Only print the full analysis dictionary for debugging if needed
            # print(last_analysis)
            print(f"Strategy: {last_analysis['strategy']}")
            #print(f"Recommended next guess: {', '.join(last_analysis['recommended_guess'])}")
            print(f"Confidence: {last_analysis['confidence']}/10")
        
        # Add a short delay for readability
        time.sleep(0.5)
    
    def setup_workflow(self) -> None:
        """Set up the game workflow.

        Creates a dynamic graph with nodes for game initialization, guess making,
        and analysis. Adds edges between nodes based on the codemaker's role.
        """
        # Create a graph builder
        builder = DynamicGraph(state_schema=self.state_schema)
        
        # Add nodes for the main game flow
        builder.add_node("initialize", self.initialize_game)
        builder.add_node("player1_guess", self.make_player1_guess)
        builder.add_node("player2_guess", self.make_player2_guess)
        builder.add_node("analyze_player1", self.analyze_player1)
        builder.add_node("analyze_player2", self.analyze_player2)
        
        # Determine the workflow based on who is the codemaker
        if self.config.codemaker == "player1":
            # Player1 is codemaker, Player2 is codebreaker
            builder.add_edge("initialize", "player2_guess")
            builder.add_edge("player2_guess", "analyze_player2")
            builder.add_edge("analyze_player2", "player2_guess")  # Loop back to player2's turn
        else:
            # Player2 is codemaker, Player1 is codebreaker
            builder.add_edge("initialize", "player1_guess")
            builder.add_edge("player1_guess", "analyze_player1")
            builder.add_edge("analyze_player1", "player1_guess")  # Loop back to player1's turn
        
        # Build the graph
        self.graph = builder.build()
        
    def run_game(self, visualize: bool = True) -> Dict[str, Any]:
        """Run the full Mastermind game, optionally visualizing each step.

        Args:
            visualize (bool): Whether to visualize the game state.

        Returns:
            Dict[str, Any]: Final game state after completion.
        """
        # Determine or generate the secret code
        if self.config.secret_code:
            secret_code = self.config.secret_code
        else:
            response = self.engines["codemaker"].invoke({})
            print(f"[DEBUG] Codemaker engine response: {response!r}")

            if isinstance(response, dict) and "code" in response:
                secret_code = response["code"]
            elif isinstance(response, ColorCode):
                secret_code = response.code
            elif hasattr(response, "code") and isinstance(response.code, list):
                secret_code = response.code
            elif isinstance(response, tuple) and len(response) == 2 and isinstance(response[1], list):
                secret_code = response[1]
            elif isinstance(response, list) and all(isinstance(c, str) for c in response):
                secret_code = response
            else:
                raise ValueError(f"Invalid codemaker response: {response}")

        # Initialize game state
        initial_state = MastermindStateManager.initialize(
            codemaker=self.config.codemaker,
            colors=self.config.colors,
            code_length=self.config.code_length,
            max_turns=self.config.max_turns,
            secret_code=secret_code
        )

        # Run the game
        if visualize:
            # Store the last seen state to prevent infinite loops
            last_state = None
            final_state = None
            
            for step in self.stream(initial_state, stream_mode="values", debug=True):
                self.visualize_state(step)
                
                # Create a MastermindState to check for game completion
                current_state = MastermindState(**step)
                
                # Break the loop if the game is over
                if current_state.game_status != "ongoing":
                    final_state = step
                    break
                
                # Detect if we're stuck in an infinite loop by comparing with last state
                if last_state:
                    # If we've seen the same guesses twice, we might be in a loop
                    if (len(current_state.guesses) == len(last_state.guesses) and 
                        len(current_state.guesses) > 0 and 
                        len(last_state.guesses) > 0):
                        # Check if max turns reached
                        if len(current_state.guesses) >= current_state.max_turns:
                            print("\n⚠️ Maximum turns reached. Ending game.")
                            # Force game to end with codemaker win
                            current_state.game_status = f"{current_state.codemaker}_win"
                            current_state.winner = current_state.codemaker
                            final_state = current_state.model_dump()
                            break
                
                # Update last state
                last_state = current_state
            
            return final_state if final_state else step
        else:
            return super().run(initial_state)

a=MastermindAgent()
a.run_game(visualize=True)