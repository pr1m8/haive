"""
Integration module for connecting the Monopoly agent to the existing game.

This module provides:
    - Functions to connect the agent to the game
    - State extraction helpers
    - Decision execution utility
"""

import os
import sys
import time
import uuid
import logging
from typing import Dict, Any, Optional, Callable

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.haive.games.monopoly.agent import MonopolyAgent
from src.haive.games.monopoly.config import MonopolyAgentConfig
from src.haive.games.monopoly.state_manager import MonopolyStateManager
from src.haive.core.engine.agent.persistence.memory_config import MemoryCheckpointerConfig

def setup_monopoly_agent(
    player_index: int = 1,
    model: str = "gpt-4o",
    temperature: float = 0.7,
    debug: bool = False
) -> MonopolyAgent:
    """
    Set up a Monopoly agent integrated with the existing game.
    
    Args:
        player_index: Index of the player to control (0-based)
        model: LLM model to use
        temperature: Temperature for generation
        debug: Enable debug logging
        
    Returns:
        Configured MonopolyAgent instance
    """
    logger.info(f"Setting up Monopoly agent for player {player_index + 1}")
    
    # Create thread ID
    thread_id = f"monopoly_game_{uuid.uuid4().hex[:8]}"
    
    # Create agent config
    config = MonopolyAgentConfig.create_default(
        name=f"monopoly_agent_{thread_id}",
        model=model,
        temperature=temperature,
        debug=debug,
        persistence=MemoryCheckpointerConfig()
    )
    
    # Initialize the agent
    agent = MonopolyAgent(config=config)
    
    # Create state manager
    state_manager = MonopolyStateManager(max_events=10)
    
    # Store references as agent attributes for later use
    agent.state_manager = state_manager
    agent.player_index = player_index
    agent.thread_id = thread_id
    
    # Patch the game to use the agent
    _patch_game_for_agent(agent, player_index)
    
    logger.info(f"Monopoly agent initialized with thread ID: {thread_id}")
    return agent

def _patch_game_for_agent(agent: MonopolyAgent, player_index: int) -> None:
    """
    Patch the game functions to use the agent for decision making.
    
    Args:
        agent: The MonopolyAgent instance
        player_index: The player index to control
    """
    logger.info(f"Patching game for agent to control player {player_index + 1}")
    
    # Try to access the game modules dynamically
    try:
        # We'll use Python's module system to find the game functions
        # This approach assumes the functions are already imported in the current scope
        
        # Store for original functions
        original_functions = {}
        
        # Look for the module that contains the key game functions
        # First, try to find functions directly in main modules
        functions_module = None
        for module_name, module in sys.modules.items():
            if hasattr(module, 'roll') and hasattr(module, 'endturn'):
                functions_module = module
                logger.info(f"Found game functions in module: {module_name}")
                break
        
        if not functions_module:
            # Try to find a module named 'functions'
            if 'functions' in sys.modules:
                functions_module = sys.modules['functions']
                logger.info("Found 'functions' module")
        
        # Check if we found the functions module
        if not functions_module:
            logger.warning("Could not find game functions module")
            return
        
        # Also try to find the module that holds player/game state
        mainboard_module = None
        for module_name, module in sys.modules.items():
            if hasattr(module, 'player_index'):
                mainboard_module = module
                logger.info(f"Found game state in module: {module_name}")
                break
        
        if not mainboard_module:
            # Try to find a module named 'mainboard'
            if 'mainboard' in sys.modules:
                mainboard_module = sys.modules['mainboard']
                logger.info("Found 'mainboard' module")
        
        if not mainboard_module:
            logger.warning("Could not find game state module")
            return
        
        # Store original functions
        if hasattr(functions_module, 'roll'):
            original_functions['roll'] = functions_module.roll
            
            def patched_roll():
                """Patched roll function that uses the agent for decisions."""
                # Get current player index
                current_player_idx = getattr(mainboard_module, 'player_index', -1)
                
                if current_player_idx == player_index:
                    logger.info(f"Agent's turn (Player {player_index + 1})")
                    
                    # Get current game state
                    game_state = _get_game_state()
                    
                    # Use the agent to make a decision
                    decision = _make_agent_decision(agent, game_state)
                    
                    # Execute the decision
                    return _execute_decision(agent, decision, functions_module)
                else:
                    # Not the agent's turn, call original function
                    return original_functions['roll']()
            
            # Replace the original function
            functions_module.roll = patched_roll
            logger.info("Patched 'roll' function")
        
        # Other functions that might need patching for better integration
        if hasattr(functions_module, 'yes'):
            original_functions['yes'] = functions_module.yes
            
            def patched_yes():
                """Patched yes function to log activity."""
                logger.info("Agent choosing 'yes'")
                result = original_functions['yes']()
                agent.state_manager.add_event(f"Player {player_index + 1} chose 'yes'")
                return result
            
            functions_module.yes = patched_yes
            logger.info("Patched 'yes' function")
        
        if hasattr(functions_module, 'no'):
            original_functions['no'] = functions_module.no
            
            def patched_no():
                """Patched no function to log activity."""
                logger.info("Agent choosing 'no'")
                result = original_functions['no']()
                agent.state_manager.add_event(f"Player {player_index + 1} chose 'no'")
                return result
            
            functions_module.no = patched_no
            logger.info("Patched 'no' function")
        
        if hasattr(functions_module, 'build'):
            original_functions['build'] = functions_module.build
            
            def patched_build():
                """Patched build function to log activity."""
                logger.info("Agent building house")
                result = original_functions['build']()
                agent.state_manager.add_event(f"Player {player_index + 1} built a house")
                return result
            
            functions_module.build = patched_build
            logger.info("Patched 'build' function")
        
        if hasattr(functions_module, 'mortgage'):
            original_functions['mortgage'] = functions_module.mortgage
            
            def patched_mortgage():
                """Patched mortgage function to log activity."""
                logger.info("Agent mortgaging property")
                result = original_functions['mortgage']()
                agent.state_manager.add_event(f"Player {player_index + 1} mortgaged a property")
                return result
            
            functions_module.mortgage = patched_mortgage
            logger.info("Patched 'mortgage' function")
        
        if hasattr(functions_module, 'unmortgage'):
            original_functions['unmortgage'] = functions_module.unmortgage
            
            def patched_unmortgage():
                """Patched unmortgage function to log activity."""
                logger.info("Agent unmortgaging property")
                result = original_functions['unmortgage']()
                agent.state_manager.add_event(f"Player {player_index + 1} unmortgaged a property")
                return result
            
            functions_module.unmortgage = patched_unmortgage
            logger.info("Patched 'unmortgage' function")
        
        if hasattr(functions_module, 'endturn'):
            original_functions['endturn'] = functions_module.endturn
            
            def patched_endturn():
                """Patched endturn function to log activity."""
                logger.info("Agent ending turn")
                result = original_functions['endturn']()
                agent.state_manager.add_event(f"Player {player_index + 1} ended turn")
                return result
            
            functions_module.endturn = patched_endturn
            logger.info("Patched 'endturn' function")
        
        logger.info(f"Successfully patched game for agent to control player {player_index + 1}")
        
    except Exception as e:
        logger.error(f"Error patching game for agent: {e}")

def _get_game_state() -> Dict[str, Any]:
    """
    Extract the current game state from the game modules.
    
    Returns:
        Dictionary with game state information
    """
    game_state = {}
    
    try:
        # Look for key game state modules
        for module_name, module in sys.modules.items():
            # Check for player module
            if hasattr(module, 'player') and isinstance(module.player, (list, tuple)):
                game_state['player'] = module.player
            
            # Check for property module
            if hasattr(module, '_property') and isinstance(module._property, dict):
                game_state['_property'] = module._property
            
            # Check for special property module
            if hasattr(module, 'sproperty') and isinstance(module.sproperty, dict):
                game_state['sproperty'] = module.sproperty
            
            # Check for game state variables
            if hasattr(module, 'player_index'):
                game_state['player_index'] = module.player_index
            
            if hasattr(module, 'rollonce'):
                game_state['rollonce'] = module.rollonce
        
        logger.debug("Game state extracted successfully")
        return game_state
    
    except Exception as e:
        logger.error(f"Error getting game state: {e}")
        return {}

def _make_agent_decision(agent: MonopolyAgent, game_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Use the agent to make a decision based on the current game state.
    
    Args:
        agent: The MonopolyAgent instance
        game_state: The current game state
        
    Returns:
        Decision dictionary
    """
    try:
        # Extract state using state manager
        state = agent.state_manager.extract_state(game_state)
        
        # Run the agent's strategy analysis
        state = agent.analyze_strategy(state)
        
        # Get the turn decision
        result = agent.decide_turn_actions(state)
        
        # Extract the decision
        if hasattr(result, 'update') and 'turn_decision' in result.update:
            decision = result.update['turn_decision']
            return {'turn_decision': decision}
        
        return {'error': 'No decision returned from agent'}
    
    except Exception as e:
        logger.error(f"Error making agent decision: {e}")
        return {'error': str(e)}

def _execute_decision(agent: MonopolyAgent, decision: Dict[str, Any], functions_module) -> Any:
    """
    Execute the agent's decision by calling appropriate game functions.
    
    Args:
        agent: The MonopolyAgent instance
        decision: The decision to execute
        functions_module: Module containing game functions
        
    Returns:
        Result of the executed function
    """
    # Extract turn decision
    turn_decision = decision.get('turn_decision', {})
    
    try:
        # Check for error
        if 'error' in decision:
            logger.error(f"Decision error: {decision['error']}")
            # Default to rolling
            if hasattr(functions_module, 'roll'):
                return functions_module.roll()
            return None
        
        # First, check if move action exists
        move_action = turn_decision.get('move_action', {})
        if move_action:
            action_type = move_action.get('action_type')
            
            if action_type == 'roll' and hasattr(functions_module, 'roll'):
                logger.info("Executing roll action")
                return functions_module.roll()
            
            elif action_type == 'pay_to_exit_jail' and hasattr(functions_module, 'payjail'):
                logger.info("Executing pay jail action")
                return functions_module.payjail()
            
            elif action_type == 'roll_for_double' and hasattr(functions_module, 'roll'):
                logger.info("Executing roll for double action")
                return functions_module.roll()
        
        # If no move action or after move, check for property actions
        property_actions = turn_decision.get('property_actions', [])
        if property_actions:
            # Just execute the first property action for now
            # In a more complex implementation, we would execute all actions
            action = property_actions[0]
            action_type = action.get('action_type')
            property_name = action.get('property_name')
            
            logger.info(f"Executing property action: {action_type} on {property_name}")
            
            # TODO: Set the selected property first if needed
            # This depends on how the game selects properties
            
            if action_type == 'buy' and hasattr(functions_module, 'yes'):
                return functions_module.yes()
            
            elif action_type == 'build' and hasattr(functions_module, 'build'):
                return functions_module.build()
            
            elif action_type == 'sell' and hasattr(functions_module, 'sellhouse'):
                return functions_module.sellhouse()
            
            elif action_type == 'mortgage' and hasattr(functions_module, 'mortgage'):
                return functions_module.mortgage()
            
            elif action_type == 'unmortgage' and hasattr(functions_module, 'unmortgage'):
                return functions_module.unmortgage()
        
        # If no actions or end_turn is true, end the turn
        if turn_decision.get('end_turn', True) and hasattr(functions_module, 'endturn'):
            logger.info("Ending turn")
            return functions_module.endturn()
        
        # Default case - just roll
        if hasattr(functions_module, 'roll'):
            logger.info("No specific action found, defaulting to roll")
            return functions_module.roll()
        
        return None
    
    except Exception as e:
        logger.error(f"Error executing decision: {e}")
        # Try to default to roll
        if hasattr(functions_module, 'roll'):
            return functions_module.roll()
        return None