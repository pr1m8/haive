"""
Monopoly agent implementation using LangGraph.

This module provides the agent implementation for the Monopoly game,
following the same pattern as the chess agent.
"""

from typing import Dict, Any, List, Optional, Tuple, Literal, Union
from pydantic import BaseModel, Field
import copy
import time
import uuid
import os
import logging
import random

from langgraph.graph import StateGraph, END
from langgraph.types import Command, RetryPolicy
from langchain_core.runnables import Runnable
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage

from haive.core.engine.agent.agent import register_agent, Agent
from haive.games.monopoly.models import TurnDecision, PropertyAction, MoveAction, StrategyAnalysis, PlayerInfo, PropertyInfo, DiceInfo
from haive.games.monopoly.state import MonopolyState
from haive.games.monopoly.config import MonopolyAgentConfig

# Set up logging
logger = logging.getLogger(__name__)

@register_agent(MonopolyAgentConfig)
class MonopolyAgent(Agent[MonopolyAgentConfig]):
    """
    Monopoly agent implementation using LangGraph.
    
    This agent manages a Monopoly game with multiple players, including:
        - Game state tracking
        - Move validation and execution
        - Property management decisions
        - Strategic analysis
        - Turn management
    """
    
    def __init__(self, config: MonopolyAgentConfig=MonopolyAgentConfig()):
        """Initialize the Monopoly agent."""
        super().__init__(config)
        self.engines = {}
        
        # Ensure engines are properly set up
        for key, engine_config in config.engines.items():
            # Check if it's a dictionary and convert to AugLLMConfig if needed
            if isinstance(engine_config, dict):
                from haive.core.engine.aug_llm import AugLLMConfig
                engine_obj = AugLLMConfig(**engine_config)
                self.engines[key] = engine_obj.create_runnable()
            else:
                # It's already an AugLLMConfig object
                self.engines[key] = engine_config.create_runnable()
            
            if self.engines[key] is None:
                raise ValueError(f"Failed to create engine for {key}")
        
        # Setup retry policies
        self.retry_policy = RetryPolicy(
            max_attempts=3,
            initial_interval=1.0,
            backoff_factor=2.0,
            max_interval=10.0,
            jitter=True
        )
    
    def setup_workflow(self):
        """
        Set up the workflow graph for the Monopoly game.
        
        This method:
            1. Adds nodes for game actions (initialize, move, property management)
            2. Connects nodes with edges based on game flow
            3. Handles conditional routing based on game status
            4. Configures subgraphs for player decisions
        """
        # Add core nodes
        self.graph.add_node("initialize_game", self.initialize_game)
        self.graph.add_node("analyze_strategy", self.analyze_strategy)
        self.graph.add_node("decide_turn_actions", self.decide_turn_actions)
        self.graph.add_node("execute_move", self.execute_move)
        self.graph.add_node("manage_properties", self.manage_properties)
        self.graph.add_node("check_game_status", self.check_game_status)
        self.graph.add_node("end_player_turn", self.end_player_turn)
        
        # Set up entry point
        self.graph.set_entry_point("initialize_game")
        
        # Connect nodes for main flow
        self.graph.add_edge("initialize_game", "analyze_strategy")
        self.graph.add_edge("analyze_strategy", "decide_turn_actions")
        
        # Add conditional edges based on decision
        self.graph.add_conditional_edges(
            "decide_turn_actions",
            self.route_action,
            {
                "move": "execute_move",
                "manage_properties": "manage_properties",
                "end_turn": "end_player_turn",
                "game_over": END
            }
        )
        
        # Connect move execution to property management
        self.graph.add_edge("execute_move", "check_game_status")
        
        # Add conditional edges from check_game_status
        self.graph.add_conditional_edges(
            "check_game_status",
            self.route_after_move,
            {
                "continue": "manage_properties",
                "end_turn": "end_player_turn",
                "game_over": END
            }
        )
        
        # Connect property management to decision node
        self.graph.add_edge("manage_properties", "decide_turn_actions")
        
        # Connect end turn to analyze strategy (for next player)
        self.graph.add_edge("end_player_turn", "analyze_strategy")
    
    def run_research(self, state: MonopolyState) -> Dict[str, Any]:
        """
        Run a Monopoly game simulation from the given state.
        
        Args:
            state: Starting game state
            
        Returns:
            Final game state
        """
        # Ensure we have at least two players to start with
        if not state.players or len(state.players) < 2:
            # Initialize with two default players if none provided
            state.players = [
                PlayerInfo(
                    name="Player 1", 
                    index=0,
                    position=0,
                    cash=1500,
                    total_wealth=1500,
                    properties_owned=[]
                ),
                PlayerInfo(
                    name="Player 2", 
                    index=1,
                    position=0,
                    cash=1500,
                    total_wealth=1500,
                    properties_owned=[]
                )
            ]
            print("🎮 Initialized game with two default players")
        
        # Print initialization message
        print("\n💰 Initializing Monopoly game...")
        
        # Run strategy analysis to start
        return self.analyze_strategy(state.model_dump())
    
    def initialize_game(self, state: Union[Dict[str, Any], MonopolyState]) -> Dict[str, Any]:
        """
        Initialize a new Monopoly game.
        
        Args:
            state: Initial state data (may be empty)
            
        Returns:
            Initialized game state
        """
        # Create full state from input
        if isinstance(state, MonopolyState):
            state_obj = state
        else:
            state_obj = MonopolyState(**state)
        
        # Create a new state if no players
        if not state_obj.players or len(state_obj.players) < 2:
            # Add two players
            state_obj.players = [
                PlayerInfo(
                    name="Player 1", 
                    index=0,
                    position=0,
                    cash=1500,
                    total_wealth=1500,
                    properties_owned=[]
                ),
                PlayerInfo(
                    name="Player 2", 
                    index=1,
                    position=0,
                    cash=1500,
                    total_wealth=1500,
                    properties_owned=[]
                )
            ]
            
            # Add some properties (simplified)
            initial_properties = {
                "Mediterranean Avenue": PropertyInfo(
                    name="Mediterranean Avenue",
                    color="brown",
                    position=1,
                    cost=60,
                    rent_values=[2, 10, 30, 90, 160, 250],
                    rent=2,
                    mortgage_value=30,
                    owner=None,
                    houses=0,
                    is_mortgaged=False
                ),
                "Baltic Avenue": PropertyInfo(
                    name="Baltic Avenue",
                    color="brown",
                    position=3,
                    cost=60,
                    rent_values=[4, 20, 60, 180, 320, 450],
                    rent=4,
                    mortgage_value=30,
                    owner=None,
                    houses=0,
                    is_mortgaged=False
                )
            }
            
            state_obj.properties = initial_properties
            state_obj.recent_events = ["Game initialized"]
            
        # Return the state dict
        return state_obj.model_dump()
    
    def analyze_strategy(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the current game state and determine strategy.
        
        Args:
            state: Current game state
            
        Returns:
            Updated state with strategic analysis
        """
        print("\n🧠 Analyzing game strategy...")
        
        # Handle both dict and MonopolyState inputs
        if isinstance(state, MonopolyState):
            state_obj = state
        else:
            state_obj = MonopolyState(**state)
        
        # Get the strategy analysis engine
        strategy_engine = self.engines.get("strategy")
        if not strategy_engine:
            error_msg = "Missing engine for strategy analysis"
            print(f"❌ {error_msg}")
            return {"error_message": error_msg}
        
        try:
            # Get current player
            current_player = state_obj.get_current_player()
            opponent = state_obj.get_opponent()
            
            # Prepare context for LLM
            context = {
                "turn": state_obj.current_player_index,
                "current_round": len(state_obj.recent_events) // 2,  # Approximate round count
                "current_player_cash": current_player.cash,
                "current_player_wealth": current_player.total_wealth,
                "board_representation": self._get_board_representation(state_obj),
                "player_properties": self._get_property_summary(state_obj, current_player.index),
                "opponent_properties": self._get_property_summary(state_obj, opponent.index),
                "recent_events": "\n".join(state_obj.recent_events[-5:])
            }
            
            # Get strategy analysis from LLM
            analysis_result = strategy_engine.invoke(context)
            
            # Log analysis
            print(f"📊 Strategy analysis: {analysis_result.analysis[:100]}...")
            
            # Add analysis to state
            new_state = state_obj.model_dump()
            new_state["strategy_analysis"] = analysis_result.model_dump()
            
            return new_state
            
        except Exception as e:
            error_msg = f"Error in strategy analysis: {str(e)}"
            print(f"❌ {error_msg}")
            return state
    
    def decide_turn_actions(self, state: Dict[str, Any]) -> Command:
        """
        Decide what actions to take for the current turn.
        
        Args:
            state: Current game state
            
        Returns:
            Command with decision and next step
        """
        print("\n🎲 Deciding turn actions...")
        
        # Handle both dict and MonopolyState inputs
        if isinstance(state, MonopolyState):
            state_obj = state
        else:
            state_obj = MonopolyState(**state)
        print(state_obj)
        print(self.engines)
        # Get the turn decision engine
        turn_engine = self.engines.get("turn_decision")
        if not turn_engine:
            error_msg = "Missing engine for turn decision"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg}, goto="end_turn")
        
        try:
            # Get current player
            current_player = state_obj.get_current_player()
            opponent = state_obj.get_opponent()
            
            # Prepare context for LLM
            context = {
                "turn": state_obj.current_player_index,
                "current_player_cash": current_player.cash,
                "current_player_wealth": current_player.total_wealth,
                "current_position": current_player.position,
                "current_location": self._get_location_name(current_player.position),
                "in_jail": current_player.is_in_jail,
                "has_rolled": state_obj.has_rolled,
                "board_representation": self._get_board_representation(state_obj),
                "player_properties": self._get_property_summary(state_obj, current_player.index),
                "opponent_properties": self._get_property_summary(state_obj, opponent.index),
                "legal_moves": self._get_legal_moves(state_obj),
                "available_property_actions": self._get_property_actions(state_obj),
                "recent_events": "\n".join(state_obj.recent_events[-5:]),
            }
            
            # Add strategy analysis if available
            if hasattr(state_obj, "strategy_analysis") and state_obj.strategy_analysis:
                context["strategy_analysis"] = state_obj.strategy_analysis.analysis
            elif isinstance(state, dict) and "strategy_analysis" in state and state["strategy_analysis"]:
                context["strategy_analysis"] = state["strategy_analysis"].get("analysis", "No analysis available")
            else:
                context["strategy_analysis"] = "No analysis available"
            
            # Get turn decision from LLM
            turn_decision = turn_engine.invoke(context)
            
            # Log decision
            print(f"🎯 Turn decision: {turn_decision.reasoning[:100]}...")
            
            # Determine next step based on decision
            next_step = "end_turn"  # Default
            
            # Check if there's a move action
            if turn_decision.move_action:
                next_step = "move"
            # Check if there are property actions
            elif turn_decision.property_actions:
                next_step = "manage_properties"
            # Check if ending turn
            elif turn_decision.end_turn:
                next_step = "end_turn"
            
            # Update state with decision
            return Command(
                update={"turn_decision": turn_decision.model_dump()},
                goto=next_step
            )
            
        except Exception as e:
            error_msg = f"Error in turn decision: {str(e)}"
            print(f"❌ {error_msg}")
            return Command(update={"error_message": error_msg}, goto="end_turn")
    
    def execute_move(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a player's move on the board.
        
        Args:
            state: Current game state
            
        Returns:
            Updated state after executing the move
        """
        # Convert to state object if needed
        if isinstance(state, dict):
            state_obj = MonopolyState(**state)
        else:
            state_obj = state
            
        print(f"\n🎲 Executing move for Player {state_obj.current_player_index + 1}...")
        
        # Get the current player
        current_player = state_obj.get_current_player()
        
        # Get turn decision
        turn_decision = state_obj.turn_decision
        if not turn_decision:
            print("❌ No turn decision found")
            return state_obj.model_dump()
        
        # Extract move action
        move_action = None
        if hasattr(turn_decision, "move_action") and turn_decision.move_action:
            move_action = turn_decision.move_action
        elif isinstance(turn_decision, dict) and "move_action" in turn_decision and turn_decision["move_action"]:
            move_action = turn_decision["move_action"]
        
        if not move_action:
            print("❌ No valid move action found")
            return state_obj.model_dump()
        
        # Extract action type
        action_type = None
        if isinstance(move_action, dict):
            action_type = move_action.get("action_type")
        else:
            action_type = getattr(move_action, "action_type", None)
        
        # If we need to roll dice
        if action_type == "roll":
            # Check if dice are already rolled
            if not state_obj.dice:
                # Roll the dice
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                
                # Create proper DiceInfo object if available
                try:
                    state_obj.dice = DiceInfo(values=(dice1, dice2), sum=dice1 + dice2)
                except Exception:
                    # Fallback to simple list if DiceInfo is not available or has different structure
                    state_obj.dice = [dice1, dice2]
                    
                print(f"🎲 Rolled {dice1} and {dice2} (sum: {dice1 + dice2})")
            
            # Calculate total steps
            if hasattr(state_obj.dice, "sum"):
                steps = state_obj.dice.sum
            elif hasattr(state_obj.dice, "values") and isinstance(state_obj.dice.values, tuple):
                steps = sum(state_obj.dice.values)
            else:
                # Assume it's a list
                steps = sum(state_obj.dice)
                
            current_position = current_player.position
            
            # Fix: Handle wrapping around the board (passing GO)
            new_position = (current_position + steps) % 40  # Wrap around at 40
            
            # Check if passing GO (not in jail and moved forward past position 39)
            passes_go = current_position > new_position and not current_player.is_in_jail
            
            # Update player position
            state_obj.players[state_obj.current_player_index].position = new_position
            
            # Handle passing GO
            if passes_go:
                # Add $200 for passing GO
                state_obj.players[state_obj.current_player_index].cash += 200
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} passed GO and collected $200")
                print(f"💵 Player {state_obj.current_player_index + 1} passed GO and collected $200")
            
            print(f"🚶 Moved from position {current_position} to position {new_position}")
            state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} moved from position {current_position} to position {new_position}")
            
            # Update has_rolled flag
            state_obj.has_rolled = True
        
        # Handle pay to exit jail
        elif action_type == "pay_to_exit_jail":
            if current_player.is_in_jail:
                # Pay $50 to exit jail
                if current_player.cash >= 50:
                    state_obj.players[state_obj.current_player_index].cash -= 50
                    state_obj.players[state_obj.current_player_index].is_in_jail = False
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} paid $50 to get out of jail")
                    print(f"💵 Paid $50 to get out of jail")
                else:
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} cannot pay $50 to get out of jail")
                    print(f"❌ Insufficient funds to pay jail fine")
            else:
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to pay to exit jail but is not in jail")
                print("❌ Not in jail, cannot pay to exit")
        
        # Handle roll for double to exit jail
        elif action_type == "roll_for_double":
            if current_player.is_in_jail:
                # Roll dice
                dice1 = random.randint(1, 6)
                dice2 = random.randint(1, 6)
                state_obj.dice = [dice1, dice2]
                print(f"🎲 Rolled {dice1} and {dice2}")
                
                # Check if rolled doubles
                if dice1 == dice2:
                    state_obj.players[state_obj.current_player_index].is_in_jail = False
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} rolled doubles and got out of jail")
                    print("🎉 Rolled doubles! You're out of jail")
                    
                    # Move player according to dice roll
                    steps = dice1 + dice2
                    current_position = current_player.position
                    new_position = (current_position + steps) % 40
                    state_obj.players[state_obj.current_player_index].position = new_position
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} moved to position {new_position}")
                    print(f"🚶 Moved to position {new_position}")
                else:
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} failed to roll doubles and remains in jail")
                    print("❌ Not doubles, still in jail")
                    
                # Update has_rolled flag
                state_obj.has_rolled = True
            else:
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to roll for double but is not in jail")
                print("❌ Not in jail, cannot roll for double")
        
        else:
            print(f"❌ Unknown move action: {action_type}")
            state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried an unknown move action: {action_type}")
        
        # Check if landed on a property
        new_position = current_player.position
        property_at_position = None
        
        # Look for property at the current position
        for prop_name, prop in state_obj.properties.items():
            if prop.position == new_position:
                property_at_position = prop
                break
        
        if property_at_position:
            print(f"🏠 Landed on property: {property_at_position.name}")
            
            # Handle property landing logic
            if property_at_position.owner is None:
                # Property is unowned
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} landed on unowned property {property_at_position.name}")
                print(f"💰 {property_at_position.name} is unowned and available for purchase (${property_at_position.cost})")
            
            elif property_at_position.owner != state_obj.current_player_index:
                # Property is owned by another player - pay rent
                if not property_at_position.is_mortgaged:
                    # Calculate rent
                    rent_amount = self._calculate_rent(state_obj, property_at_position.name)
                    
                    # Pay rent if player has enough cash
                    if current_player.cash >= rent_amount:
                        # Update cash for both players
                        state_obj.players[state_obj.current_player_index].cash -= rent_amount
                        state_obj.players[property_at_position.owner].cash += rent_amount
                        
                        state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} paid ${rent_amount} rent to Player {property_at_position.owner + 1}")
                        print(f"💵 Paid ${rent_amount} rent to Player {property_at_position.owner + 1}")
                    else:
                        # Handle insufficient funds (bankruptcy)
                        state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} cannot pay ${rent_amount} rent and is bankrupt")
                        print(f"⚠️ Cannot pay ${rent_amount} rent - player is bankrupt")
                        if hasattr(state_obj.players[state_obj.current_player_index], "bankruptcy_status"):
                            state_obj.players[state_obj.current_player_index].bankruptcy_status = True
                        else:
                            # Backwards compatibility with older PlayerInfo model
                            state_obj.players[state_obj.current_player_index].bankrupt = True
                else:
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} landed on mortgaged property {property_at_position.name} - no rent paid")
                    print(f"📝 Property is mortgaged - no rent paid")
            else:
                # Player owns this property
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} landed on their own property {property_at_position.name}")
                print(f"🏡 You own this property")
        
        return state_obj.model_dump()
    
    def manage_properties(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Manage properties (buy, sell, mortgage, etc).
        
        Args:
            state: Current game state
            
        Returns:
            Updated state after property management
        """
        # Convert to state object if needed
        if isinstance(state, dict):
            state_obj = MonopolyState(**state)
        else:
            state_obj = state
            
        print("\n🏠 Managing properties...")
        
        # Get the current player
        current_player = state_obj.get_current_player()
        
        # Get turn decision
        turn_decision = state_obj.turn_decision
        if not turn_decision:
            print("❌ No turn decision found")
            return state_obj.model_dump()
        
        # Handle the property action
        property_actions = []
        if hasattr(turn_decision, "property_actions") and turn_decision.property_actions:
            property_actions = turn_decision.property_actions
        elif isinstance(turn_decision, dict) and "property_actions" in turn_decision:
            property_actions = turn_decision["property_actions"]
        
        if not property_actions:
            print("❌ No property actions specified")
            return state_obj.model_dump()
        
        # Process each property action
        for property_action in property_actions:
            # Get the property being managed
            if isinstance(property_action, dict):
                property_name = property_action.get("property_name")
                action = property_action.get("action_type")
            else:
                property_name = getattr(property_action, "property_name", None)
                action = getattr(property_action, "action_type", None)
            
            if not property_name or property_name not in state_obj.properties:
                print(f"❌ Invalid property: {property_name}")
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to manage invalid property: {property_name}")
                continue
                
            property_obj = state_obj.properties[property_name]
            
            # BUY property
            if action == "buy":
                # Check if property is unowned
                if property_obj.owner is not None:
                    print(f"❌ Cannot buy {property_name} - already owned by Player {property_obj.owner + 1}")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to buy {property_name}, but it's already owned")
                    continue
                
                # Check if player has enough money
                if current_player.cash < property_obj.cost:
                    print(f"❌ Cannot buy {property_name} - insufficient funds (need ${property_obj.cost}, have ${current_player.cash})")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to buy {property_name}, but has insufficient funds")
                    continue
                
                # Buy the property
                state_obj.properties[property_name].owner = current_player.index
                state_obj.players[current_player.index].cash -= property_obj.cost
                
                if not hasattr(state_obj.players[current_player.index], "properties_owned"):
                    state_obj.players[current_player.index].properties_owned = []
                    
                state_obj.players[current_player.index].properties_owned.append(property_name)
                
                print(f"✅ Bought {property_name} for ${property_obj.cost}")
                state_obj.recent_events.append(f"Player {current_player.index + 1} bought {property_name} for ${property_obj.cost}")
            
            # BUILD house
            elif action == "build":
                # Check if player owns the property
                if property_obj.owner != current_player.index:
                    print(f"❌ Cannot build on {property_name} - not owned by current player")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to build on {property_name}, but doesn't own it")
                    continue
                
                # Check if property has max houses
                if property_obj.houses >= 5:  # 5 houses = hotel
                    print(f"❌ Cannot build on {property_name} - already has maximum improvements")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to build on {property_name}, but it already has maximum improvements")
                    continue
                
                # Calculate house cost (simplified)
                house_cost = self._get_house_cost(property_obj.color)
                
                # Check if player has enough money
                if current_player.cash < house_cost:
                    print(f"❌ Cannot build on {property_name} - insufficient funds (need ${house_cost}, have ${current_player.cash})")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to build on {property_name}, but has insufficient funds")
                    continue
                
                # Buy the house
                state_obj.properties[property_name].houses += 1
                state_obj.players[current_player.index].cash -= house_cost
                
                # Determine if this is a house or hotel
                if property_obj.houses == 5:
                    print(f"✅ Built a hotel on {property_name} for ${house_cost}")
                    state_obj.recent_events.append(f"Player {current_player.index + 1} built a hotel on {property_name} for ${house_cost}")
                else:
                    print(f"✅ Built a house on {property_name} for ${house_cost} (now {property_obj.houses} houses)")
                    state_obj.recent_events.append(f"Player {current_player.index + 1} built a house on {property_name} for ${house_cost}")
            
            # SELL house
            elif action == "sell":
                # Check if player owns the property
                if property_obj.owner != current_player.index:
                    print(f"❌ Cannot sell house from {property_name} - not owned by current player")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to sell house from {property_name}, but doesn't own it")
                    continue
                
                # Check if property has houses
                if property_obj.houses <= 0:
                    print(f"❌ Cannot sell house from {property_name} - no houses to sell")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to sell house from {property_name}, but there are no houses")
                    continue
                
                # Calculate house cost (simplified)
                house_cost = self._get_house_cost(property_obj.color)
                sell_value = house_cost // 2  # Houses sell for half their cost
                
                # Sell the house
                state_obj.properties[property_name].houses -= 1
                state_obj.players[current_player.index].cash += sell_value
                
                # Determine if this was a hotel or house
                was_hotel = property_obj.houses == 4
                if was_hotel:
                    print(f"✅ Sold a hotel from {property_name} for ${sell_value}")
                    state_obj.recent_events.append(f"Player {current_player.index + 1} sold a hotel from {property_name} for ${sell_value}")
                else:
                    print(f"✅ Sold a house from {property_name} for ${sell_value} (now {property_obj.houses} houses)")
                    state_obj.recent_events.append(f"Player {current_player.index + 1} sold a house from {property_name} for ${sell_value}")
            
            # MORTGAGE property
            elif action == "mortgage":
                # Check if player owns the property
                if property_obj.owner != current_player.index:
                    print(f"❌ Cannot mortgage {property_name} - not owned by current player")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to mortgage {property_name}, but doesn't own it")
                    continue
                
                # Check if property is already mortgaged
                if property_obj.is_mortgaged:
                    print(f"❌ Cannot mortgage {property_name} - already mortgaged")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to mortgage {property_name}, but it's already mortgaged")
                    continue
                
                # Check if property has buildings
                if property_obj.houses > 0:
                    print(f"❌ Cannot mortgage {property_name} - has buildings")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to mortgage {property_name}, but it has buildings")
                    continue
                
                # Calculate mortgage value
                mortgage_value = property_obj.cost // 2
                
                # Mortgage the property
                state_obj.properties[property_name].is_mortgaged = True
                state_obj.players[current_player.index].cash += mortgage_value
                
                print(f"✅ Mortgaged {property_name} for ${mortgage_value}")
                state_obj.recent_events.append(f"Player {current_player.index + 1} mortgaged {property_name} for ${mortgage_value}")
            
            # UNMORTGAGE property
            elif action == "unmortgage":
                # Check if player owns the property
                if property_obj.owner != current_player.index:
                    print(f"❌ Cannot unmortgage {property_name} - not owned by current player")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to unmortgage {property_name}, but doesn't own it")
                    continue
                
                # Check if property is mortgaged
                if not property_obj.is_mortgaged:
                    print(f"❌ Cannot unmortgage {property_name} - not mortgaged")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to unmortgage {property_name}, but it's not mortgaged")
                    continue
                
                # Calculate unmortgage cost (mortgage value + 10% interest)
                mortgage_value = property_obj.cost // 2
                unmortgage_cost = mortgage_value + (mortgage_value // 10)
                
                # Check if player has enough money
                if current_player.cash < unmortgage_cost:
                    print(f"❌ Cannot unmortgage {property_name} - insufficient funds (need ${unmortgage_cost}, have ${current_player.cash})")
                    state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried to unmortgage {property_name}, but has insufficient funds")
                    continue
                
                # Unmortgage the property
                state_obj.properties[property_name].is_mortgaged = False
                state_obj.players[current_player.index].cash -= unmortgage_cost
                
                print(f"✅ Unmortgaged {property_name} for ${unmortgage_cost}")
                state_obj.recent_events.append(f"Player {current_player.index + 1} unmortgaged {property_name} for ${unmortgage_cost}")
            
            else:
                print(f"❌ Unknown property action: {action}")
                state_obj.recent_events.append(f"Player {state_obj.current_player_index + 1} tried unknown property action: {action}")
        
        return state_obj.model_dump()
    
    def _calculate_rent(self, state: MonopolyState, property_name: str) -> int:
        """Calculate the rent for a given property."""
        property_obj = state.properties.get(property_name)
        if not property_obj:
            return 0
            
        # Get base rent based on number of houses
        house_count = property_obj.houses
        
        # Access rent values correctly
        rent_values = []
        if hasattr(property_obj, "rent_values"):
            rent_values = property_obj.rent_values
        else:
            # Fallback to single rent value
            return property_obj.rent
        
        # Get the appropriate rent value based on houses
        if house_count < len(rent_values):
            base_rent = rent_values[house_count]
        else:
            # Fallback if rent array is incomplete
            base_rent = rent_values[-1] if rent_values else property_obj.rent
        
        # Check if player owns all properties in the group (monopoly)
        if house_count == 0:  # Only apply monopoly bonus for undeveloped properties
            owner = property_obj.owner
            color_group = getattr(property_obj, "color", None)
            if owner is not None and color_group:
                properties_in_group = [p for p_name, p in state.properties.items() 
                                      if getattr(p, "color", None) == color_group]
                if all(p.owner == owner for p in properties_in_group):
                    # Double rent for monopoly
                    base_rent *= 2
        
        return base_rent
    
    def _get_house_cost(self, property_group: str) -> int:
        """Get the cost of a house for a property group."""
        # House costs by property group/color
        house_costs = {
            "Brown": 50,
            "Light Blue": 50,
            "Pink": 100,
            "Purple": 100,
            "Orange": 100,
            "Red": 150,
            "Yellow": 150,
            "Green": 200,
            "Dark Blue": 200,
            # Color aliases
            "brown": 50,
            "light blue": 50,
            "light_blue": 50,
            "pink": 100,
            "purple": 100,
            "orange": 100,
            "red": 150,
            "yellow": 150,
            "green": 200,
            "dark blue": 200,
            "dark_blue": 200
        }
        
        return house_costs.get(property_group, 100)  # Default to 100
    
    def check_game_status(self, state: Dict[str, Any]) -> Command:
        """
        Check if game can continue or should end.
        
        Args:
            state: Current game state
            
        Returns:
            Command with routing decision
        """
        print("\n🔍 Checking game status...")
        
        # Handle both dict and MonopolyState inputs
        if isinstance(state, MonopolyState):
            state_obj = state
        else:
            state_obj = MonopolyState(**state)
        
        # Check for bankruptcy
        any_bankruptcy = False
        for player in state_obj.players:
            if player.bankruptcy_status:
                any_bankruptcy = True
                print(f"💔 Player {player.index + 1} is bankrupt")
        
        if any_bankruptcy:
            print("🏁 Game over due to bankruptcy")
            return Command(update={}, goto="game_over")
        
        # Check max turns (could add this to config)
        if len(state_obj.recent_events) > 100:  # Simple limit
            print("🏁 Game over due to turn limit")
            return Command(update={}, goto="game_over")
        
        # Determine if should continue to property management
        turn_decision = state.get("turn_decision", {})
        property_actions = turn_decision.get("property_actions", [])
        
        if property_actions:
            return Command(update={}, goto="continue")
        else:
            # No more actions, end turn
            return Command(update={}, goto="end_turn")
    
    def end_player_turn(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """
        End the current player's turn and switch to the next player.
        
        Args:
            state: Current game state
            
        Returns:
            Updated state for next player
        """
        print("\n⏭️ Ending player turn...")
        
        # Handle both dict and MonopolyState inputs
        if isinstance(state, MonopolyState):
            state_obj = state
        else:
            state_obj = MonopolyState(**state)
        
        # Clone state for updates
        new_state = copy.deepcopy(state_obj.model_dump())
        
        # Get current player
        current_player = state_obj.get_current_player()
        
        # Switch to next player - protect against empty players list
        if len(state_obj.players) > 0:
            next_player_index = (current_player.index + 1) % len(state_obj.players)
            new_state["current_player_index"] = next_player_index
            
            # Add event
            new_state["recent_events"].append(
                f"Player {current_player.index + 1} ended turn, now Player {next_player_index + 1}'s turn"
            )
            
            print(f"👉 Switched to Player {next_player_index + 1}")
        else:
            # If no players, keep the current player index
            next_player_index = state_obj.current_player_index
            new_state["recent_events"].append("No players available, turn ended")
            print("⚠️ No players available to switch to")
        
        # Reset dice and has_rolled flag
        new_state["dice"] = None
        new_state["has_rolled"] = False
        
        # Clear turn decision
        if "turn_decision" in new_state:
            del new_state["turn_decision"]
        
        return new_state
    
    def route_action(self, state: Dict[str, Any]) -> str:
        """Route to the next action based on the turn decision."""
        # Convert to state object if needed
        if isinstance(state, dict):
            state_obj = MonopolyState(**state)
        else:
            state_obj = state
            
        # Get the turn decision
        if hasattr(state_obj, "turn_decision") and state_obj.turn_decision:
            turn_decision = state_obj.turn_decision
        elif isinstance(state, dict) and "turn_decision" in state and state["turn_decision"]:
            turn_decision = state["turn_decision"]
        else:
            print("⚠️ No turn decision found, defaulting to end_turn")
            return "end_turn"
        
        # Determine next action based on turn_decision structure
        # First check if move_action exists and has priority
        if isinstance(turn_decision, dict):
            # Dict-based turn decision
            if "move_action" in turn_decision and turn_decision["move_action"]:
                return "move"
            elif "property_actions" in turn_decision and turn_decision["property_actions"]:
                return "manage_properties"
            elif "end_turn" in turn_decision and turn_decision["end_turn"]:
                return "end_turn"
        else:
            # Object-based turn decision
            if hasattr(turn_decision, "move_action") and turn_decision.move_action:
                return "move"
            elif hasattr(turn_decision, "property_actions") and turn_decision.property_actions:
                return "manage_properties"
            elif hasattr(turn_decision, "end_turn") and turn_decision.end_turn:
                return "end_turn"
        
        # Fallback to end_turn if no clear action found
        print("⚠️ No clear action determined, defaulting to end_turn")
        return "end_turn"
            
    def route_after_move(self, state: Dict[str, Any]) -> str:
        """Route after a move based on the game state."""
        # Convert to state object if needed
        if isinstance(state, dict):
            state_obj = MonopolyState(**state)
        else:
            state_obj = state
            
        # Check if any player is bankrupt
        for player in state_obj.players:
            if player.bankrupt:
                return "game_over"
                
        # Default to continue
        return "continue"
    
    # Helper methods
    def _get_property(self, state: MonopolyState, property_name: str):
        """Get a property by name."""
        if property_name in state.properties:
            return state.properties[property_name]
        elif property_name in state.special_cards:
            return state.special_cards[property_name]
        return None
    
    def _get_location_name(self, position: int) -> str:
        """Get location name from position."""
        # This would be replaced with actual game board data
        locations = [
            "Go", "Mediterranean Avenue", "Community Chest", "Baltic Avenue",
            "Income Tax", "Reading Railroad", "Oriental Avenue", "Chance",
            "Vermont Avenue", "Connecticut Avenue", "Jail/Just Visiting", "St. Charles Place",
            "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad",
            "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue",
            "Free Parking", "Kentucky Avenue", "Chance", "Indiana Avenue",
            "Illinois Avenue", "B&O Railroad", "Atlantic Avenue", "Ventnor Avenue",
            "Water Works", "Marvin Gardens", "Go To Jail", "Pacific Avenue",
            "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue", "Short Line",
            "Chance", "Park Place", "Luxury Tax", "Boardwalk"
        ]
        
        if 0 <= position < len(locations):
            return locations[position]
        return f"Position {position}"
    
    def _get_board_representation(self, state: MonopolyState) -> str:
        """Get a simple text representation of the board."""
        board = "Game Board:\n"
        
        # Add player positions
        player_positions = {}
        for player in state.players:
            position = player.position
            if position not in player_positions:
                player_positions[position] = []
            player_positions[position].append(f"P{player.index+1}")
        
        # Generate board layout
        for i in range(40):
            location_name = self._get_location_name(i)
            players = ", ".join(player_positions.get(i, []))
            owner = ""
            
            # Check if property has an owner
            for prop in state.properties.values():
                if prop.position == i and prop.owner is not None:
                    owner = f" (P{prop.owner+1}"
                    if prop.houses > 0:
                        owner += f", {prop.houses} houses"
                    if prop.is_mortgaged:
                        owner += ", mortgaged"
                    owner += ")"
            
            board += f"{i}: {location_name}{owner}"
            if players:
                board += f" [{players}]"
            board += "\n"
        
        return board
    
    def _get_property_summary(self, state: MonopolyState, player_index: int) -> str:
        """Get a summary of properties for a player."""
        player_properties = []
        
        # Check regular properties
        for prop_name, prop in state.properties.items():
            if prop.owner == player_index:
                status = f"{prop.color} property"
                if prop.houses > 0:
                    status += f", {prop.houses} houses"
                if prop.is_mortgaged:
                    status += ", mortgaged"
                player_properties.append(f"{prop_name}: {status}")
        
        # Check special cards (railroads, utilities)
        for card_name, card in state.special_cards.items():
            if card.owner == player_index:
                status = f"{card.card_type}"
                if card.card_type == "railroad":
                    status += f", rent: ${card.rent}"
                elif card.card_type == "utility":
                    status += f", rent multiplier"
                player_properties.append(f"{card_name}: {status}")
        
        if not player_properties:
            return "No properties owned"
        
        return "\n".join(player_properties)
    
    def _get_legal_moves(self, state: MonopolyState) -> str:
        """Get a summary of legal moves for the current player."""
        current_player = state.get_current_player()
        
        # Start with an empty list of legal moves
        legal_moves = []
        
        # Check if player has already rolled
        if not state.has_rolled:
            legal_moves.append("roll: Roll the dice to move")
        
        # Check if player is in jail
        if current_player.is_in_jail:
            legal_moves.append("pay_to_exit_jail: Pay $50 to get out of jail")
            legal_moves.append("roll_for_double: Try to roll a double to get out of jail")
        
        # Always can end turn (though this might not be a good idea in some cases)
        legal_moves.append("end_turn: End your turn")
        
        if not legal_moves:
            return "No legal moves available"
        
        return "\n".join(legal_moves)
    
    def _get_property_actions(self, state: MonopolyState) -> str:
        """Get a summary of available property actions for the current player."""
        current_player = state.get_current_player()
        
        # Start with an empty list of property actions
        property_actions = []
        
        # Check current position for buyable property
        position = current_player.position
        
        # Check if can buy the current property
        for prop_name, prop in state.properties.items():
            if prop.position == position and prop.owner is None:
                property_actions.append(f"buy: Buy {prop_name} for ${prop.cost}")
        
        # Check owned properties for building/selling/mortgaging
        for prop_name, prop in state.properties.items():
            if prop.owner == current_player.index:
                # Check if can build (would need to check monopoly, but simplifying here)
                can_build = not prop.is_mortgaged and prop.houses < 5
                if can_build:
                    house_cost = int(prop.cost / 5)
                    property_actions.append(f"build: Build house on {prop_name} for ${house_cost}")
                
                # Check if can sell houses
                if prop.houses > 0:
                    house_value = int(prop.cost / 10)
                    property_actions.append(f"sell: Sell house from {prop_name} for ${house_value}")
                
                # Check if can mortgage
                if not prop.is_mortgaged and prop.houses == 0:
                    property_actions.append(f"mortgage: Mortgage {prop_name} for ${prop.mortgage_value}")
                
                # Check if can unmortgage
                if prop.is_mortgaged:
                    unmortgage_cost = int(prop.mortgage_value * 1.1)
                    property_actions.append(f"unmortgage: Unmortgage {prop_name} for ${unmortgage_cost}")
        
        # Also check special properties (railroads, utilities)
        for card_name, card in state.special_cards.items():
            if card.owner == current_player.index:
                # Special properties can only be mortgaged or unmortgaged
                if not card.is_mortgaged:
                    property_actions.append(f"mortgage: Mortgage {card_name} for ${card.mortgage_value}")
                else:
                    unmortgage_cost = int(card.mortgage_value * 1.1)
                    property_actions.append(f"unmortgage: Unmortgage {card_name} for ${unmortgage_cost}")
        
        if not property_actions:
            return "No property actions available"
        
        return "\n".join(property_actions)