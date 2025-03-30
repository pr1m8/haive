"""
Integration module for Monopoly agent and game.

This module connects the agent to the existing Monopoly game code without
requiring complex interface layers.
"""

import logging
import importlib
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_monopoly_agent(player_index: int = 1):
    """
    Set up a Monopoly agent to play the game.
    
    Args:
        player_index: Index of the player to control (0 or 1)
        
    Returns:
        Agent instance
    """
    try:
        # Import the Monopoly agent components
        from src.haive.games.monopoly.agent import MonopolyAgent
        from src.haive.games.monopoly.config import MonopolyAgentConfig
        
        # Create a default configuration
        config = MonopolyAgentConfig.create_default(
            name=f"monopoly_agent_p{player_index + 1}",
            debug=True,
            model="gpt-4o",
            temperature=0.7
        )
        
        # Create the agent
        agent = MonopolyAgent(config)
        logger.info(f"Created Monopoly agent for player {player_index + 1}")
        
        # Patch the game to use the agent
        _patch_game_for_agent(agent, player_index)
        
        return agent
        
    except Exception as e:
        logger.error(f"Error setting up agent: {e}")
        import traceback
        traceback.print_exc()
        return None

def setup_multi_model_agent(player_index: int = 1):
    """
    Set up a Monopoly agent using multiple models.
    
    Args:
        player_index: Index of the player to control (0 or 1)
        
    Returns:
        Agent instance
    """
    try:
        # Import the Monopoly agent components
        from src.haive.games.monopoly.agent import MonopolyAgent
        from src.haive.games.monopoly.config import MonopolyAgentConfig, EngineConfig
        
        # Create engine configurations
        primary_engine = EngineConfig(
            model="gpt-4o",
            provider="azure",
            temperature=0.7
        )
        
        strategy_engine = EngineConfig(
            model="gpt-4o",
            provider="azure",
            temperature=0.8  # Higher temperature for more creative strategy
        )
        
        # Create the agent configuration with multiple models
        config = MonopolyAgentConfig.create_multi_model(
            name=f"monopoly_agent_p{player_index + 1}",
            debug=True,
            primary_engine=primary_engine,
            strategy_engine=strategy_engine
        )
        
        # Create the agent
        agent = MonopolyAgent(config)
        logger.info(f"Created multi-model Monopoly agent for player {player_index + 1}")
        
        # Patch the game to use the agent
        _patch_game_for_agent(agent, player_index)
        
        return agent
        
    except Exception as e:
        logger.error(f"Error setting up multi-model agent: {e}")
        import traceback
        traceback.print_exc()
        return None

def _patch_game_for_agent(agent, player_index: int):
    """
    Patch the Monopoly game to use the agent for the specified player.
    
    Args:
        agent: MonopolyAgent instance
        player_index: Index of the player to control
    """
    try:
        # Import Monopoly game modules
        import monopoly.functions as functions
        import monopoly.mainboard as mainboard
        
        # Store original functions
        original_functions = {}
        
        # Patch the roll function
        original_functions['roll'] = functions.roll
        
        def patched_roll():
            """Patched roll function that uses the agent if it's the agent's turn."""
            if mainboard.player_index == player_index:
                logger.info(f"Agent's turn (Player {player_index + 1})")
                
                # Get the current game state
                game_state = _get_game_state()
                
                # Run the agent
                agent_result = agent.run(game_state)
                
                # Execute the agent's decision
                _execute_agent_decision(agent_result)
                
                return None  # We've handled it
            else:
                # Not the agent's turn, call original function
                return original_functions['roll']()
        
        # Replace the original function
        functions.roll = patched_roll
        
        logger.info(f"Patched game for agent to control player {player_index + 1}")
        
    except Exception as e:
        logger.error(f"Error patching game: {e}")
        import traceback
        traceback.print_exc()

def _get_game_state() -> Dict[str, Any]:
    """
    Get the current game state for the agent.
    
    Returns:
        Dictionary with game state information
    """
    try:
        # Import necessary modules
        import monopoly.player as player
        import monopoly.mainboard as mainboard
        import monopoly.functions as functions
        import monopoly.firstpage as firstpage
        import monopoly.Property as Property
        
        return {
            "_property": Property._property,
            "sproperty": Property.sproperty,
            "player": player.player,
            "player_index": mainboard.player_index,
            "rollonce": mainboard.rollonce,
            "functions": functions,
            "firstpage": firstpage
        }
        
    except Exception as e:
        logger.error(f"Error getting game state: {e}")
        import traceback
        traceback.print_exc()
        return {}

def _execute_agent_decision(decision: Dict[str, Any]):
    """
    Execute the agent's decision.
    
    Args:
        decision: Decision from the agent
    """
    try:
        # Import necessary modules
        import monopoly.functions as functions
        import monopoly.Property as Property
        
        # Extract turn decision
        if "turn_decision" not in decision:
            logger.warning("No turn decision in agent result")
            return
        
        turn_decision = decision["turn_decision"]
        
        # Process move action
        if turn_decision.get("move_action"):
            move_action = turn_decision["move_action"]
            action_type = move_action.get("action_type")
            
            logger.info(f"Executing move action: {action_type}")
            
            if action_type == "roll":
                functions.roll()
            elif action_type == "pay_to_exit_jail":
                # Pay to exit jail (game-specific implementation)
                pass
                
        # Process property actions
        for property_action in turn_decision.get("property_actions", []):
            action_type = property_action.get("action_type")
            property_name = property_action.get("property_name")
            
            logger.info(f"Executing property action: {action_type} on {property_name}")
            
            # Set the target property if needed
            if property_name and hasattr(Property, "_property") and property_name in Property._property:
                Property.temo = Property._property[property_name]
                
                if action_type == "buy":
                    functions.yes()
                elif action_type == "build":
                    functions.build()
                elif action_type == "sell":
                    functions.sellhouse()
                elif action_type == "mortgage":
                    functions.mortgage()
                elif action_type == "unmortgage":
                    functions.unmortgage()
        
        # End turn if requested
        if turn_decision.get("end_turn"):
            logger.info("Ending turn")
            functions.endturn()
                
    except Exception as e:
        logger.error(f"Error executing agent decision: {e}")
        import traceback
        traceback.print_exc()