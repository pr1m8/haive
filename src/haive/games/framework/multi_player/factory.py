"""Factory for creating multi-player game agents.

This module provides a factory class for creating multi-player game agents,
automating the creation of game-specific agent classes with proper configuration
and state management.

Example:
    >>> from src.haive.agents.agent_games.framework.multi_player.factory import MultiPlayerGameFactory
    >>> 
    >>> # Create a new chess agent class
    >>> ChessAgent = MultiPlayerGameFactory.create_game_agent(
    ...     name="ChessAgent",
    ...     state_schema=ChessState,hv
    ...     state_manager=ChessStateManager,
    ...     player_roles=["white", "black"],
    ...     aug_llm_configs={
    ...         "white": {"move": white_llm_config},
    ...         "black": {"move": black_llm_config}
    ...     }
    ... )
"""

from typing import Type, Dict, List, Callable
from src.haive.games.framework.multi_player.config import MultiPlayerGameConfig
from src.haive.games.framework.multi_player.state import MultiPlayerGameState
from src.haive.games.framework.multi_player.state_manager import MultiPlayerGameStateManager
from src.haive.games.framework.multi_player.agent import MultiPlayerGameAgent
from src.haive.core.engine.agent.agent import Agent 
from src.haive.core.engine.aug_llm import AugLLMConfig
from src.haive.core.engine.agent.agent import register_agent

class MultiPlayerGameFactory:
    """Factory for creating multi-player game agents.
    
    This class provides static methods for creating game-specific agent
    classes with proper configuration and state management. It handles:
        - Agent class creation with proper inheritance
        - Configuration class creation
        - State management integration
        - Custom method injection
        - Agent registration
    
    Example:
        >>> # Create a new game agent class
        >>> MafiaAgent = MultiPlayerGameFactory.create_game_agent(
        ...     name="MafiaAgent",
        ...     state_schema=MafiaState,
        ...     state_manager=MafiaStateManager,
        ...     player_roles=["villager", "mafia", "detective"],
        ...     aug_llm_configs={
        ...         "villager": {"vote": villager_config},
        ...         "mafia": {"kill": mafia_config},
        ...         "detective": {"investigate": detective_config}
        ...     }
        ... )
    """
    
    @staticmethod
    def create_game_agent(
        name: str,
        state_schema: Type[MultiPlayerGameState],
        state_manager: Type[MultiPlayerGameStateManager],
        player_roles: List[str],
        aug_llm_configs: Dict[str, Dict[str, AugLLMConfig]],
        custom_methods: Dict[str, Callable] = None
    ) -> Type[Agent]:
        """Create a new multi-player game agent class.
        
        This method creates a new agent class with proper configuration,
        state management, and custom methods. The created class is
        automatically registered with the agent registry.
        
        Args:
            name (str): Name of the agent class.
            state_schema (Type[MultiPlayerGameState]): The game state schema class.
            state_manager (Type[MultiPlayerGameStateManager]): The game state manager class.
            player_roles (List[str]): List of player roles.
            aug_llm_configs (Dict[str, Dict[str, AugLLMConfig]]): LLM configurations by role and function.
            custom_methods (Dict[str, Callable], optional): Additional methods for the agent.
        
        Returns:
            Type[Agent]: A new agent class ready for instantiation.
        
        Example:
            >>> # Create a chess agent with custom methods
            >>> ChessAgent = MultiPlayerGameFactory.create_game_agent(
            ...     name="ChessAgent",
            ...     state_schema=ChessState,
            ...     state_manager=ChessStateManager,
            ...     player_roles=["white", "black"],
            ...     aug_llm_configs={
            ...         "white": {"move": white_config},
            ...         "black": {"move": black_config}
            ...     },
            ...     custom_methods={
            ...         "evaluate_position": my_eval_function,
            ...         "get_piece_moves": my_move_generator
            ...     }
            ... )
        """
        # Create agent config class
        config_class = type(
            f"{name}Config",
            (MultiPlayerGameConfig,),
            {
                "state_schema": state_schema,
                "aug_llm_configs": aug_llm_configs,
                "player_roles": player_roles,
                "visualize": True,
                
                # Add a classmethod for default config
                "default_config": classmethod(lambda cls: cls(
                    state_schema=state_schema,
                    aug_llm_configs=aug_llm_configs,
                    player_roles=player_roles,
                    visualize=True
                ))
            }
        )
        
        # Define initialization for the agent class
        def __init__(self, config):
            # Initialize as MultiPlayerGameAgent
            MultiPlayerGameAgent.__init__(self, config)
            self.state_manager = state_manager
        
        # Create base methods dictionary
        methods = {
            "__init__": __init__,
            # Add any other standard methods here
        }
        
        # Add custom methods if provided
        if custom_methods:
            methods.update(custom_methods)
        
        # Create and register the agent class
        agent_class = type(
            name,
            (MultiPlayerGameAgent,),
            methods
        )
        
        # Register the agent with its config
        register_agent(config_class)(agent_class)
        
        return agent_class