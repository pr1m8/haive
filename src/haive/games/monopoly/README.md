# Monopoly LLM Agent

This package provides an LLM-based agent that can play the Monopoly game. It integrates with the existing Monopoly code to provide intelligent decision-making through large language models.

## Architecture

The agent is designed with a clean separation of concerns:

1. **Models**: Data models representing game state and agent decisions
2. **Prompts**: LLM prompts for different decision types
3. **State Manager**: Extracts and manages game state
4. **Agent**: Core decision-making logic using LangGraph
5. **Integration**: Connects the agent to the existing game code

## Features

- **Strategic Decision Making**: The agent analyzes the game state to make strategic decisions
- **Property Management**: Buys, builds, sells, and mortgages properties based on strategy
- **Jail Handling**: Makes intelligent decisions to get out of jail
- **Adaptive Play**: Adapts strategy based on opponent actions and game state

## How to Use

1. **Installation**:

   ```bash
   # Clone the repository with the Monopoly code
   git clone https://github.com/AniketSanghi/Monopoly-game.git
   
   # Copy the agent folder into the repository
   cp -r monopoly_agent/ Monopoly-game/
   ```

2. **Using the Agent**:

   ```python
   # Import the setup function
   from monopoly_agent.integration import setup_monopoly_agent
   
   # Setup the agent for player 1 (index 1)
   agent_integration = setup_monopoly_agent(player_index=1)
   
   # Run the game normally
   mainboard.mainscreen()
   ```

## Agent Decision Process

1. The agent extracts the current game state from the Monopoly game objects
2. It analyzes the state to develop a strategic understanding
3. Based on this analysis, it decides on actions for the current turn
4. These actions are then executed through the patched button handler

## Customization

You can customize the agent by modifying:

- **Prompts**: Change the prompts in `prompts.py` to adjust decision-making style
- **Configuration**: Adjust the agent configuration in `config.py`
- **Models**: Extend the models in `models.py` to add new capabilities

## Example Usage

See `example.py` for a full example of setting up and running the agent.

## Requirements

- The original Monopoly game code
- Python 3.7+
- pygame
- pydantic
- langchain
- langgraph

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
