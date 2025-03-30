# src/haive/agents/agent_games/framework/factory.py

"""Factory module for creating game agents.

This module provides a factory class for creating game agents with standardized
workflows and configurations. It simplifies the process of creating new game
agents by providing a flexible, composable pattern.

Example:
    >>> # Create a new chess agent
    >>> chess_agent = GameAgentFactory.create_game_agent(
    ...     name="ChessAgent",
    ...     state_schema=ChessState,
    ...     state_manager=ChessStateManager,
    ...     enable_analysis=True
    ... )
    >>> 
    >>> # Create a standard workflow
    >>> graph = StateGraph()
    >>> graph = GameAgentFactory.create_standard_workflow(graph)

Typical usage:
    - Use create_game_agent to generate new game agent classes
    - Use create_standard_workflow to set up game workflows
    - Customize agents with analysis, custom nodes, and edges
"""

from typing import Dict, List, Any, Optional, Union, Type, Callable, TypeVar, Generic
from pydantic import BaseModel
from src.haive.core.engine.agent.agent import Agent, AgentConfig, register_agent
from src.haive.core.engine.aug_llm import AugLLMConfig, compose_runnable
from src.haive.core.graph.NodeFactory import create_node_function
from src.haive.core.graph.GraphBuilder import DynamicGraph
from langgraph.graph import StateGraph
from langgraph.constants import START, END

from src.haive.games.framework.base import GameAgent, GameConfig, GameState, GameStateManager

# Type variable for generic state
T = TypeVar('T', bound=BaseModel)

class GameAgentFactory:
    """Factory for creating game agents using a flexible, composable pattern.
    
    This factory class provides methods for creating game agents and their
    workflows. It simplifies the process of creating new game agents by:
    1. Generating workflow nodes from a standardized template
    2. Using DynamicGraph for simplified graph building
    3. Supporting consistent extension patterns for analysis and custom workflows
    
    The factory supports:
    - Creation of game agent classes with standard methods
    - Configuration of analysis steps and custom nodes
    - Flexible workflow definition with conditional edges
    - Registration of agents with their configs
    
    Example:
        >>> # Create a new chess agent
        >>> chess_agent = GameAgentFactory.create_game_agent(
        ...     name="ChessAgent",
        ...     state_schema=ChessState,
        ...     state_manager=ChessStateManager
        ... )
        >>> 
        >>> # Create an instance with custom config
        >>> agent = chess_agent(ChessConfig())
    """
    
    @staticmethod
    def create_game_agent(
        name: str,
        state_schema: Type[GameState],
        state_manager: Type[GameStateManager],
        player1_name: str = "player1",
        player2_name: str = "player2",
        enable_analysis: bool = True,
        aug_llm_configs: Optional[Dict[str, AugLLMConfig]] = None,
        custom_nodes: Optional[Dict[str, Callable]] = None,
        custom_edges: Optional[List[Dict[str, Any]]] = None,
        conditional_edges: Optional[Dict[str, Dict[str, Any]]] = None
    ) -> Type[Agent]:
        """Create a new game agent class with a complete workflow.
        
        This method generates a new game agent class with all necessary methods
        and workflow configuration. It creates both the agent class and its
        corresponding config class.
        
        Args:
            name (str): Name of the agent class.
            state_schema (Type[GameState]): The game state schema class.
            state_manager (Type[GameStateManager]): The game state manager class.
            player1_name (str, optional): Name for player 1. Defaults to "player1".
            player2_name (str, optional): Name for player 2. Defaults to "player2".
            enable_analysis (bool, optional): Whether to enable analysis steps. Defaults to True.
            aug_llm_configs (Optional[Dict[str, AugLLMConfig]], optional): LLM configurations. Defaults to None.
            custom_nodes (Optional[Dict[str, Callable]], optional): Custom node functions. Defaults to None.
            custom_edges (Optional[List[Dict[str, Any]]], optional): Custom edges. Defaults to None.
            conditional_edges (Optional[Dict[str, Dict[str, Any]]], optional): Conditional edges. Defaults to None.
            
        Returns:
            Type[Agent]: A new agent class with all methods and workflow configured.
            
        Example:
            >>> # Create a chess agent with analysis
            >>> chess_agent = GameAgentFactory.create_game_agent(
            ...     name="ChessAgent",
            ...     state_schema=ChessState,
            ...     state_manager=ChessStateManager,
            ...     enable_analysis=True,
            ...     aug_llm_configs={
            ...         "player1": player1_config,
            ...         "player2": player2_config
            ...     }
            ... )
        """
        # Create agent config class
        config_class = type(
            f"{name}Config",
            (GameConfig,),
            {
                "state_schema": state_schema,
                "aug_llm_configs": aug_llm_configs or {},
                "enable_analysis": enable_analysis,
                "visualize": True,
                
                # Add a classmethod for default config
                "default_config": classmethod(lambda cls: cls(
                    state_schema=state_schema,
                    aug_llm_configs=aug_llm_configs or {},
                    enable_analysis=enable_analysis,
                    visualize=True
                ))
            }
        )
        
        # Define methods for the agent class
        def __init__(self, config):
            # Initialize as GameAgent
            GameAgent.__init__(self, config)
            self.state_manager = state_manager
        
        def make_player1_move(self, state):
            return self.make_move(state, player1_name)
            
        def make_player2_move(self, state):
            return self.make_move(state, player2_name)
            
        def analyze_player1(self, state):
            return self.analyze_position(state, player1_name)
            
        def analyze_player2(self, state):
            return self.analyze_position(state, player2_name)

        def setup_workflow(self):
            # Use DynamicGraph to build the workflow
            graph_builder = DynamicGraph(
                components=[self.config.engine],
                state_schema=self.config.state_schema
            )
            
            # Add core nodes
            graph_builder.add_node("initialize_game", self.initialize_game)
            graph_builder.add_node("player1_move", self.make_player1_move)
            graph_builder.add_node("player2_move", self.make_player2_move)
            
            # Add any custom nodes
            if custom_nodes:
                for node_name, node_func in custom_nodes.items():
                    graph_builder.add_node(node_name, node_func)
            
            # Add analysis nodes if enabled
            if self.config.enable_analysis:
                graph_builder.add_node("player1_analysis", self.analyze_player1)
                graph_builder.add_node("player2_analysis", self.analyze_player2)
                
                # Set up flow with analysis
                graph_builder.add_edge(START, "initialize_game")
                graph_builder.add_edge("initialize_game", "player1_analysis")
                graph_builder.add_edge("player1_analysis", "player1_move")
                
                graph_builder.add_conditional_edge(
                    "player1_move",
                    self.should_continue_game,
                    {True: "player2_analysis", False: END}
                )
                
                graph_builder.add_edge("player2_analysis", "player2_move")
                
                graph_builder.add_conditional_edge(
                    "player2_move",
                    self.should_continue_game,
                    {True: "player1_analysis", False: END}
                )
            else:
                # Simplified flow without analysis
                graph_builder.add_edge(START, "initialize_game")
                graph_builder.add_edge("initialize_game", "player1_move")
                
                graph_builder.add_conditional_edge(
                    "player1_move",
                    self.should_continue_game,
                    {True: "player2_move", False: END}
                )
                
                graph_builder.add_conditional_edge(
                    "player2_move",
                    self.should_continue_game,
                    {True: "player1_move", False: END}
                )
            
            # Add any custom edges
            if custom_edges:
                for edge in custom_edges:
                    graph_builder.add_edge(edge["source"], edge["target"])
            
            # Add any custom conditional edges
            if conditional_edges:
                for source, conditions in conditional_edges.items():
                    graph_builder.add_conditional_edge(
                        source,
                        conditions["condition"],
                        conditions["routes"]
                    )
            
            # Build the graph
            self.graph = graph_builder.build()
        
        # Create and register the agent class
        agent_class = type(
            name,
            (GameAgent,),
            {
                "__init__": __init__,
                "make_player1_move": make_player1_move,
                "make_player2_move": make_player2_move,
                "analyze_player1": analyze_player1,
                "analyze_player2": analyze_player2,
                "setup_workflow": setup_workflow
            }
        )
        
        # Register the agent with its config
        register_agent(config_class)(agent_class)
        
        return agent_class
    
    @staticmethod
    def create_standard_workflow(graph: StateGraph, enable_analysis: bool = True) -> StateGraph:
        """Add a standard game workflow to an existing graph.
        
        This method creates the typical workflow for a turn-based game with
        two players, optionally including analysis steps. It modifies the
        provided graph by adding nodes and edges for the standard game flow.
        
        Args:
            graph (StateGraph): The state graph to modify.
            enable_analysis (bool, optional): Whether to include analysis steps.
                Defaults to True.
            
        Returns:
            StateGraph: The modified graph with standard workflow added.
            
        Example:
            >>> # Create a basic graph and add standard workflow
            >>> graph = StateGraph()
            >>> graph = GameAgentFactory.create_standard_workflow(
            ...     graph,
            ...     enable_analysis=True
            ... )
        """
        # Set up the workflow based on whether analysis is enabled
        if enable_analysis:
            graph.add_node("player1_analysis", lambda state: state)
            graph.add_node("player2_analysis", lambda state: state)
            
            # Standard flow with analysis
            graph.add_edge(START, "initialize_game")
            graph.add_edge("initialize_game", "player1_analysis")
            graph.add_edge("player1_analysis", "player1_move")
            
            graph.add_conditional_edges(
                "player1_move",
                lambda state: state.game_status == "ongoing",
                {
                    True: "player2_analysis",
                    False: END
                }
            )
            
            graph.add_edge("player2_analysis", "player2_move")
            
            graph.add_conditional_edges(
                "player2_move",
                lambda state: state.game_status == "ongoing",
                {
                    True: "player1_analysis",
                    False: END
                }
            )
        else:
            # Simplified flow without analysis
            graph.add_edge(START, "initialize_game")
            graph.add_edge("initialize_game", "player1_move")
            
            graph.add_conditional_edges(
                "player1_move",
                lambda state: state.game_status == "ongoing",
                {
                    True: "player2_move",
                    False: END
                }
            )
            
            graph.add_conditional_edges(
                "player2_move",
                lambda state: state.game_status == "ongoing",
                {
                    True: "player1_move",
                    False: END
                }
            )
            
        return graph