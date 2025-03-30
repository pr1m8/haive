

def run_interactive_game(agent: SinglePlayerGameAgent, commands: List[str] = None):
    """Run an interactive single-player game.
    
    Args:
        agent: The game agent
        commands: Optional list of commands to execute (for testing)
    """
    # Initialize the game
    print(f"\n🎮 Starting Single-Player Game in {agent.config.game_mode.value} mode")
    print("=" * 60)
    
    # Initialize the game state
    state_dict = agent.initialize_game({}).update
    
    # Create a proper state object
    state = agent.config.state_schema(**state_dict)
    
    # Auto-analyze if enabled
    if agent.config.auto_analyze:
        analyze_command = agent.analyze_position(state)
        if analyze_command.update:
            for key, value in analyze_command.update.items():
                setattr(state, key, value)
    
    # Main game loop
    game_over = False
    command_index = 0
    
    while not game_over:
        # Visualize the current state
        agent.visualize_state(state.dict())
        
        # Check for game over
        if state.game_status != "ongoing":
            game_over = True
            break
        
        # Get user input or next command
        if commands and command_index < len(commands):
            command = commands[command_index]
            command_index += 1
            print(f"\nCommand: {command}")
        else:
            command = input("\nEnter command: ").strip()
            
        if command.lower() == "quit":
            print("Exiting game...")
            break
            
        if command.lower() == "auto":
            # Make an automatic move
            move_command = agent.make_player_move(state)
            if move_command.update:
                for key, value in move_command.update.items():
                    setattr(state, key, value)
                    
            # Auto-analyze if enabled
            if agent.config.auto_analyze:
                analyze_command = agent.analyze_position(state)
                if analyze_command.update:
                    for key, value in analyze_command.update.items():
                        setattr(state, key, value)
        elif command.lower() == "hint":
            # Get a hint
            hint_command = agent.get_hint(state)
            if hint_command.update:
                for key, value in hint_command.update.items():
                    setattr(state, key, value)
        elif command.lower() == "analyze":
            # Analyze the position
            analyze_command = agent.analyze_position(state)
            if analyze_command.update:
                for key, value in analyze_command.update.items():
                    setattr(state, key, value)
        else:
            # Process game-specific command
            command_result = agent.interactive_command(state, command)
            if command_result.update:
                for key, value in command_result.update.items():
                    setattr(state, key, value)
    
    print("\n✅ Game Complete!")
    
    # Save state history
    agent.save_state_history()


def run_auto_game(agent: SinglePlayerGameAgent):
    """Run a fully automated single-player game.
    
    Args:
        agent: The game agent
    """
    # Initialize the game
    print(f"\n🎮 Starting Automated Single-Player Game")
    print("=" * 60)
    
    # Initialize the game state
    state_dict = agent.initialize_game({}).update
    
    # Stream through the game steps
    for step in agent.app.stream(
        state_dict, 
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
    
    print("\n✅ Game Complete!")
    
    # Save state history
    agent.save_state_history()

