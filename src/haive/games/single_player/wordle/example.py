from src.haive.games.single_player.wordle.agent import WordConnectionsAgent
from src.haive.games.single_player.wordle.config import WordConnectionsAgentConfig
from src.haive.games.single_player.wordle.state_manager import WordConnectionsStateManager
import time
import random

def run_word_connections_game(source="internal", categories=None, auto_analyze=True):
    """Run a Word Connections game with visualization.
    
    Args:
        source (str): Source of game data ('internal' or 'nyt')
        categories (List[str], optional): Specific categories to use
        auto_analyze (bool): Whether to automatically analyze before each move
    """
    # Create agent with appropriate config
    config = WordConnectionsAgentConfig(
        enable_analysis=auto_analyze,
        visualize=True,
        auto_submit=False,
        source=source
    )
    
    if categories:
        config.categories = categories
        
    agent = WordConnectionsAgent(config)
    
    # Run the game
    print("\n🎮 Starting Word Connections Game")
    print("=" * 60)
    print("Game Rules:")
    print("1. Find groups of 4 words that form a category")
    print("2. Each category has a difficulty level (yellow: easiest, purple: hardest)")
    print("3. You have 4 incorrect attempts before the game ends")
    print("4. The goal is to find all 4 categories")
    print("=" * 60)
    
    # Initialize the game
    game_state = agent.initialize_game({})
    
    # Stream through the game steps
    for step in agent.app.stream(
        game_state, 
        config=agent.runnable_config,
        debug=True,
        stream_mode="values"
    ):
        # Visualize the game state
        agent.visualize_state(step)
        
        # Check for errors
        if step.get("error_message"):
            print(f"\n❌ Error: {step['error_message']}")
        
        # Check for game over
        if step.get("game_status") != "ongoing":
            break
    
    # Save game history
    agent.save_state_history()
    print("\n✅ Game Complete!")

def run_interactive_word_connections_game(source="internal", categories=None):
    """Run an interactive version of Word Connections where the user makes selections.
    
    Args:
        source (str): Source of game data ('internal' or 'nyt')
        categories (List[str], optional): Specific categories to use
    """
    # Create agent with config
    config = WordConnectionsAgentConfig(
        enable_analysis=True,
        visualize=True,
        auto_submit=False,
        source=source
    )
    
    if categories:
        config.categories = categories
        
    agent = WordConnectionsAgent(config)
    
    # Run the game
    print("\n🎮 Starting Word Connections Game - Interactive Mode")
    print("=" * 60)
    print("Game Rules:")
    print("1. Find groups of 4 words that form a category")
    print("2. Each category has a difficulty level (yellow: easiest, purple: hardest)")
    print("3. You have 4 incorrect attempts before the game ends")
    print("4. The goal is to find all 4 categories")
    print("\nInteractive Commands:")
    print("- Enter a number (0-15) to select/deselect a word")
    print("- Type 'submit' to submit your current selection")
    print("- Type 'analyze' to get an analysis of the board")
    print("- Type 'auto' to let the AI make the next move")
    print("- Type 'quit' to exit the game")
    print("=" * 60)
    
    # Initialize the game state
    state = WordConnectionsStateManager.initialize(source=source, categories=categories)
    
    # Main game loop
    game_over = False
    while not game_over:
        # Display the current state
        print("\n" + "=" * 60)
        print(f"🎮 Word Connections Game")
        if state.game_source == "nyt":
            print(f"📅 NYT Connections {state.game_date}")
        print(f"📌 Status: {state.game_status.upper()}")
        print(f"🏆 Categories found: {len(state.discovered_groups)}/4")
        print("=" * 60)
        
        # Print the board
        print("\n" + state.board_string)
        
        # Check for game over
        if state.game_status != "ongoing":
            if state.game_status == "victory":
                print("\n🎉 Congratulations! You've solved all categories!")
            elif state.game_status == "defeat":
                print("\n❌ Game over! You've run out of attempts.")
                
                # Show remaining categories
                if len(state.discovered_groups) < len(state.categories):
                    print("\nRemaining categories were:")
                    for category, words in state.categories.items():
                        if category not in state.discovered_groups:
                            print(f"- {category}: {', '.join(words)}")
            game_over = True
            break
        
        # Get user input
        command = input("\nEnter command (0-15, submit, analyze, auto, quit): ").strip().lower()
        
        if command == "quit":
            print("Exiting game...")
            break
            
        elif command == "submit":
            # Submit current selection
            state = WordConnectionsStateManager.submit_selection(state)
            
        elif command == "analyze":
            # Analyze the position
            analyzer = agent.engines.get("game_analyzer")
            if analyzer:
                try:
                    analysis_context = agent.prepare_analysis_context(state)
                    analysis = analyzer.invoke(analysis_context)
                    analysis_dict = analysis.model_dump() if hasattr(analysis, "model_dump") else analysis.dict()
                    
                    print("\n🔍 Analysis:")
                    
                    # Print potential groups
                    if hasattr(analysis, "potential_groups") and analysis.potential_groups:
                        print("\nPotential Groups:")
                        for i, group in enumerate(analysis.potential_groups[:3]):
                            if "category" in group and "words" in group:
                                print(f"{i+1}. {group['category']}: {', '.join(group['words'])}")
                    
                    # Print difficult words
                    if hasattr(analysis, "difficult_words") and analysis.difficult_words:
                        print("\nAmbiguous Words:")
                        print(", ".join(analysis.difficult_words[:8]))
                    
                    # Print strategy
                    if hasattr(analysis, "strategy") and analysis.strategy:
                        print("\nStrategy:")
                        strategy = analysis.strategy
                        if len(strategy) > 150:
                            print(f"{strategy[:150]}...")
                        else:
                            print(strategy)
                            
                    # Update state with analysis
                    state.analysis_history.append(analysis_dict)
                    
                except Exception as e:
                    print(f"Error in analysis: {e}")
            else:
                print("Analysis engine not available.")
                
        elif command == "auto":
            # Let the AI make a move
            print(agent.engines)
            engine = agent.engines.get("player_move")
            if engine:
                try:
                    print(move_context)
                    print(engine)
                    move_context = agent.prepare_move_context(state)
                    response = engine.invoke(move_context)
                    move = agent.extract_move(response)
                    print(move_context)
                    print(response)
                    print(f"\nAI suggests: {', '.join(move.words)}")
                    print(f"Reasoning: {response.reasoning[:200]}...")
                    
                    confirm = input("Apply this move? (y/n): ").strip().lower()
                    if confirm == "y":
                        state = WordConnectionsStateManager.apply_move(state, move)
                except Exception as e:
                    print(f"Error in AI move: {e}")
            else:
                print("Move engine not available.")
        else:
            # Try to parse as a cell index
            try:
                cell_index = int(command)
                if 0 <= cell_index < 16:
                    state = WordConnectionsStateManager.select_cell(state, cell_index)
                else:
                    print("Invalid cell index. Must be between 0 and 15.")
            except ValueError:
                print("Invalid command.")
    
    print("\n✅ Game Complete!")

if __name__ == "__main__":
    # Choose your game mode
    # Mode 1: Fully automated with AI analysis and moves
    # run_word_connections_game(source="internal")
    
    # Mode 2: Interactive where you select the words
    run_interactive_word_connections_game(source="internal")
    
    # To play today's NYT Connections (requires selenium or playwright):
    # run_interactive_word_connections_game(source="nyt")