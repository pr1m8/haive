import os
import uuid
import logging
from typing import Dict, Any, List, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MonopolyAgent:
    """
    A simplified agent for playing Monopoly.
    
    This agent works directly with the game without complex package structures.
    """
    
    def __init__(self, player_index=1, model="gpt-4o", temperature=0.7, debug=False):
        """
        Initialize the Monopoly agent.
        
        Args:
            player_index: Index of the player to control (0 or 1)
            model: LLM model to use
            temperature: Temperature for the LLM
            debug: Enable debug logging
        """
        self.player_index = player_index
        self.model = model
        self.temperature = temperature
        self.debug = debug
        self.game_id = str(uuid.uuid4())[:8]
        
        # Initialize the state manager
        self.state_manager = MonopolyStateManager()
        
        # Set up the LLM
        self.llm = self._setup_llm()
        
        # Decision history
        self.decision_history = []
        
        # UI dashboard (if connected)
        self.dashboard = None
        
        logger.info(f"Initialized MonopolyAgent for player {player_index + 1}")
    
    def _setup_llm(self):
        """Set up the LLM to use for decision making."""
        try:
            # Try to import OpenAI
            from langchain_openai import ChatOpenAI
            
            return ChatOpenAI(
                model=self.model,
                temperature=self.temperature
            )
        except ImportError:
            logger.warning("Could not import OpenAI, falling back to fake LLM")
            
            # Create a fake LLM for testing
            class FakeLLM:
                def invoke(self, prompt):
                    return {
                        "move_action": {"action_type": "roll", "reasoning": "Need to move forward"},
                        "property_actions": [],
                        "end_turn": True,
                        "reasoning": "This is a fake LLM response for testing"
                    }
            
            return FakeLLM()
    
    def run(self, game_state):
        """
        Run the agent on the current game state.
        
        Args:
            game_state: Current game state dictionary
            
        Returns:
            Decision dictionary
        """
        if self.debug:
            logger.info(f"Running agent for player {self.player_index + 1}")
        
        # Extract state using the state manager
        monopoly_state = self.state_manager.extract_state(game_state)
        
        # Get the current player
        current_player = monopoly_state.get_current_player()
        
        # Check if it's our turn
        if current_player.index != self.player_index:
            if self.debug:
                logger.info(f"Not our turn (current player: {current_player.index + 1})")
            return {
                "turn_decision": {
                    "move_action": None,
                    "property_actions": [],
                    "end_turn": False,
                    "reasoning": "Not our turn"
                }
            }
        
        # Create decision prompt
        prompt = self._create_decision_prompt(monopoly_state)
        
        # Get decision from LLM
        if self.debug:
            logger.info("Getting decision from LLM")
        
        try:
            # Get decision from LLM
            llm_response = self.llm.invoke(prompt)
            
            # Process LLM response
            if isinstance(llm_response, str):
                # Simple string response, convert to structured format
                decision = {
                    "move_action": {"action_type": "roll", "reasoning": llm_response},
                    "property_actions": [],
                    "end_turn": True,
                    "reasoning": llm_response
                }
            else:
                # Structured response (depends on LLM implementation)
                decision = llm_response
            
            # Store the decision
            self.decision_history.append(decision)
            
            # Update dashboard if available
            if self.dashboard:
                self.dashboard.add_decision({"turn_decision": decision})
            
            return {"turn_decision": decision}
        
        except Exception as e:
            logger.error(f"Error getting decision from LLM: {e}")
            
            # Return a default decision
            default_decision = {
                "move_action": {"action_type": "roll", "reasoning": "Error occurred"},
                "property_actions": [],
                "end_turn": True,
                "reasoning": f"Error occurred: {e}"
            }
            
            return {"turn_decision": default_decision}
    
    def _create_decision_prompt(self, state):
        """
        Create a prompt for the LLM to make a decision.
        
        Args:
            state: Extracted game state
            
        Returns:
            Prompt string
        """
        # Get current player info
        current_player = state.get_current_player()
        
        # Get opponent info
        opponent = state.get_opponent()
        
        # Get property info
        property_summary = self.state_manager.generate_property_ownership_summary()
        
        # Create the prompt
        prompt = f"""
You are playing Monopoly as Player {current_player.index + 1}.

CURRENT GAME STATE:
- Cash: ${current_player.cash}
- Properties: {', '.join(current_player.properties_owned) if current_player.properties_owned else 'None'}
- Position: {current_player.position}
- In Jail: {'Yes' if current_player.is_in_jail else 'No'}
- Has Rolled: {'Yes' if state.has_rolled else 'No'}

OPPONENT INFORMATION:
- Opponent Cash: ${opponent.cash}
- Opponent Properties: {', '.join(opponent.properties_owned) if opponent.properties_owned else 'None'}

PROPERTY OWNERSHIP:
{property_summary}

DECISION OPTIONS:
1. Move Actions:
   - roll: Roll the dice to move
   - pay_to_exit_jail: Pay to get out of jail

2. Property Actions:
   - buy: Buy the property you landed on
   - build: Build houses on a property
   - sell: Sell houses from a property
   - mortgage: Mortgage a property
   - unmortgage: Unmortgage a property

3. Turn Management:
   - end_turn: End your turn

What decision do you want to make? Provide a structured response with these components:
1. move_action: An action to move (or null if none)
2. property_actions: A list of property actions (or empty if none)
3. end_turn: Whether to end your turn (true/false)
4. reasoning: Your strategic reasoning
"""
        
        return prompt
    
    def connect_dashboard(self, dashboard):
        """
        Connect a dashboard to the agent.
        
        Args:
            dashboard: Dashboard object
        """
        self.dashboard = dashboard
        logger.info("Connected dashboard to agent")
    
    def update_settings(self, temperature=None, model=None):
        """
        Update agent settings.
        
        Args:
            temperature: New temperature value
            model: New model name
        """
        if temperature is not None:
            self.temperature = temperature
            
        if model is not None:
            self.model = model
            
        # Reinitialize the LLM
        self.llm = self._setup_llm()
        
        logger.info(f"Updated agent settings: model={self.model}, temperature={self.temperature}")


class MonopolyStateManager:
    """
    Manager for extracting and handling Monopoly game state.
    
    This works directly with the game state without complex package dependencies.
    """
    
    def __init__(self, max_events=5):
        """
        Initialize the state manager.
        
        Args:
            max_events: Maximum number of events to track
        """
        self.max_events = max_events
        self.recent_events = []
        self._location_info = {}
        self._property_info = {}
        
        # Initialize default location info
        self._init_default_location_info()
    
    def _init_default_location_info(self):
        """Initialize default location information."""
        self._location_info = {
            "Go": "Collect $2000 as you pass GO",
            "Mediterranean Avenue": "Brown property, cheapest on the board",
            "Community Chest": "Draw a Community Chest card",
            "Baltic Avenue": "Brown property",
            "Income Tax": "Pay $2000",
            "Reading Railroad": "Railroad property",
            "Oriental Avenue": "Light blue property",
            "Chance": "Draw a Chance card",
            "Vermont Avenue": "Light blue property",
            "Connecticut Avenue": "Light blue property",
            "Jail / Just Visiting": "Jail (or just visiting)",
            "St. Charles Place": "Pink property",
            "Electric Company": "Utility property",
            "States Avenue": "Pink property",
            "Virginia Avenue": "Pink property",
            "Pennsylvania Railroad": "Railroad property",
            "St. James Place": "Orange property",
            "Tennessee Avenue": "Orange property",
            "New York Avenue": "Orange property",
            "Free Parking": "Free space, no effect",
            "Kentucky Avenue": "Red property",
            "Indiana Avenue": "Red property",
            "Illinois Avenue": "Red property",
            "B&O Railroad": "Railroad property",
            "Atlantic Avenue": "Yellow property",
            "Ventnor Avenue": "Yellow property",
            "Water Works": "Utility property",
            "Marvin Gardens": "Yellow property",
            "Go To Jail": "Go to Jail",
            "Pacific Avenue": "Green property",
            "North Carolina Avenue": "Green property",
            "Pennsylvania Avenue": "Green property",
            "Short Line": "Railroad property",
            "Park Place": "Blue property",
            "Luxury Tax": "Pay $1000",
            "Boardwalk": "Blue property, most expensive on the board"
        }
    
    def add_event(self, event):
        """
        Add an event to the recent events list.
        
        Args:
            event: Event description
        """
        self.recent_events.append(event)
        if len(self.recent_events) > self.max_events:
            self.recent_events.pop(0)
        
        logger.debug(f"Event: {event}")
    
    def get_recent_events(self):
        """
        Get the list of recent events.
        
        Returns:
            List of event strings
        """
        return self.recent_events
    
    def extract_state(self, game_objects):
        """
        Extract a structured state from the game objects.
        
        Args:
            game_objects: Dictionary of game objects
            
        Returns:
            Structured state dictionary
        """
        try:
            # Extract player information
            players = []
            player_list = game_objects.get("player", [])
            
            for i, player_obj in enumerate(player_list):
                if hasattr(player_obj, "cash"):
                    # Extract properties owned
                    properties_owned = []
                    if hasattr(player_obj, "properties"):
                        properties = getattr(player_obj, "properties")
                        if isinstance(properties, list):
                            properties_owned = properties
                        elif isinstance(properties, dict):
                            properties_owned = list(properties.keys())
                    
                    player_info = {
                        "name": f"Player {i+1}",
                        "index": i,
                        "position": player_obj.place if hasattr(player_obj, "place") else (0, 0),
                        "cash": player_obj.cash,
                        "total_wealth": player_obj.total_wealth if hasattr(player_obj, "total_wealth") else player_obj.cash,
                        "properties_owned": properties_owned,
                        "is_in_jail": getattr(player_obj, "released", 1) == 0,
                        "jail_cards": getattr(player_obj, "jail_cards", 0),
                        "railways_owned": getattr(player_obj, "no_of_railways", 0),
                        "bankruptcy_status": getattr(player_obj, "bankruptcy_status", False)
                    }
                    players.append(player_info)
            
            # If no players found, create default ones
            if not players:
                players = [
                    {
                        "name": "Player 1",
                        "index": 0,
                        "position": (0, 0),
                        "cash": 15000,
                        "total_wealth": 15000,
                        "properties_owned": [],
                        "is_in_jail": False,
                        "jail_cards": 0,
                        "railways_owned": 0,
                        "bankruptcy_status": False
                    },
                    {
                        "name": "Player 2",
                        "index": 1,
                        "position": (0, 0),
                        "cash": 15000,
                        "total_wealth": 15000,
                        "properties_owned": [],
                        "is_in_jail": False,
                        "jail_cards": 0,
                        "railways_owned": 0,
                        "bankruptcy_status": False
                    }
                ]
            
            # Extract property information
            properties = {}
            property_dict = game_objects.get("_property", {})
            
            for prop_name, prop_obj in property_dict.items():
                if hasattr(prop_obj, "cost"):
                    rent_values = []
                    # Try to extract rent values if available
                    for i in range(6):  # 0-5 houses/hotel
                        attr_name = f"rent{i}"
                        if hasattr(prop_obj, attr_name):
                            rent_values.append(getattr(prop_obj, attr_name))
                    
                    property_info = {
                        "name": prop_name,
                        "color": getattr(prop_obj, "color", "unknown"),
                        "position": getattr(prop_obj, "position", (0, 0)),
                        "cost": prop_obj.cost,
                        "rent_values": rent_values,
                        "rent": getattr(prop_obj, "rent", rent_values[0] if rent_values else 0),
                        "mortgage_value": getattr(prop_obj, "mortgage", prop_obj.cost // 2),
                        "owner": getattr(prop_obj, "owner", None),
                        "houses": getattr(prop_obj, "no_of_houses", 0),
                        "is_mortgaged": getattr(prop_obj, "is_mortgaged", False)
                    }
                    properties[prop_name] = property_info
                    
                    # Store for location info
                    self._property_info[prop_name] = property_info
            
            # Extract special card information
            special_cards = {}
            special_dict = game_objects.get("sproperty", {})
            
            for card_name, card_obj in special_dict.items():
                if hasattr(card_obj, "cost"):
                    card_type = "railroad" if "railroad" in card_name.lower() else "utility"
                    special_card_info = {
                        "name": card_name,
                        "card_type": card_type,
                        "position": getattr(card_obj, "position", (0, 0)),
                        "cost": card_obj.cost,
                        "rent": getattr(card_obj, "rent", 0),
                        "mortgage_value": getattr(card_obj, "mortgage", card_obj.cost // 2),
                        "owner": getattr(card_obj, "owner", None)
                    }
                    special_cards[card_name] = special_card_info
            
            # Get current player index
            current_player_index = game_objects.get("player_index", 0)
            
            # Check if player has rolled
            has_rolled = game_objects.get("rollonce", 0) == 1
            
            # Create the state dictionary
            state = {
                "properties": properties,
                "special_cards": special_cards,
                "players": players,
                "current_player_index": current_player_index,
                "dice": None,  # We don't have this information yet
                "community_chest_drawn": None,  # We don't have this information yet
                "chance_drawn": None,  # We don't have this information yet
                "has_rolled": has_rolled,
                "recent_events": self.recent_events.copy()
            }
            
            return state
            
        except Exception as e:
            logger.error(f"Error extracting state: {e}")
            import traceback
            traceback.print_exc()
            
            # Return a minimal valid state
            return {
                "players": [
                    {
                        "name": "Player 1",
                        "index": 0,
                        "position": (0, 0),
                        "cash": 15000,
                        "total_wealth": 15000,
                        "properties_owned": []
                    },
                    {
                        "name": "Player 2",
                        "index": 1,
                        "position": (0, 0),
                        "cash": 15000,
                        "total_wealth": 15000,
                        "properties_owned": []
                    }
                ],
                "current_player_index": game_objects.get("player_index", 0),
                "has_rolled": game_objects.get("rollonce", 0) == 1,
                "recent_events": self.recent_events.copy()
            }
    
    def get_current_player(self, state):
        """
        Get the current player from the state.
        
        Args:
            state: Game state dictionary
            
        Returns:
            Current player information
        """
        if not state or "players" not in state:
            return {
                "name": "Unknown",
                "index": 0,
                "cash": 0,
                "properties_owned": []
            }
        
        current_idx = state.get("current_player_index", 0)
        players = state.get("players", [])
        
        if current_idx < len(players):
            return players[current_idx]
        
        return {
            "name": f"Player {current_idx + 1}",
            "index": current_idx,
            "cash": 0,
            "properties_owned": []
        }
    
    def get_opponent(self, state):
        """
        Get the opponent player from the state.
        
        Args:
            state: Game state dictionary
            
        Returns:
            Opponent player information
        """
        if not state or "players" not in state:
            return {
                "name": "Unknown",
                "index": 1,
                "cash": 0,
                "properties_owned": []
            }
        
        current_idx = state.get("current_player_index", 0)
        players = state.get("players", [])
        
        # Find the first player that isn't the current player
        for player in players:
            if player.get("index") != current_idx:
                return player
        
        # If no other player found, return a default one
        return {
            "name": "Player 2",
            "index": 1,
            "cash": 0,
            "properties_owned": []
        }
    
    def generate_property_ownership_summary(self):
        """
        Generate a summary of property ownership.
        
        Returns:
            String summary of property ownership
        """
        property_groups = {}
        
        # Group properties by color/country
        for prop_name, prop_info in self._property_info.items():
            group = prop_info.get("color", "Unknown")
            if group not in property_groups:
                property_groups[group] = []
            
            owner_str = "Unowned"
            if prop_info.get("owner") is not None:
                owner_str = f"Player {prop_info['owner'] + 1}"
            
            houses_str = ""
            if prop_info.get("houses", 0) > 0:
                houses_str = f" ({prop_info['houses']} houses)"
            
            property_groups[group].append(f"{prop_name}: {owner_str}{houses_str}")
        
        # Generate the summary
        summary_lines = [f"Property Ownership Summary:"]
        
        for group, properties in property_groups.items():
            summary_lines.append(f"\n{group}:")
            for prop in properties:
                summary_lines.append(f"  - {prop}")
        
        return "\n".join(summary_lines)


def setup_monopoly_agent(player_index=1, model="gpt-4o", temperature=0.7, debug=False):
    """
    Set up a Monopoly agent to play the game.
    
    Args:
        player_index: Index of the player to control (0 or 1)
        model: LLM model to use
        temperature: Temperature for the LLM
        debug: Enable debug logging
        
    Returns:
        MonopolyAgent instance
    """
    # Create the agent
    agent = MonopolyAgent(
        player_index=player_index,
        model=model,
        temperature=temperature,
        debug=debug
    )
    
    # Patch the game to use the agent
    _patch_game_for_agent(agent, player_index)
    
    return agent


def _patch_game_for_agent(agent, player_index):
    """
    Patch the Monopoly game to use the agent for the specified player.
    
    Args:
        agent: MonopolyAgent instance
        player_index: Index of the player to control
    """
    try:
        # Try to import Monopoly game modules
        import functions
        import mainboard
        
        # Store original functions
        original_functions = {}
        
        # Patch the roll function
        original_functions['roll'] = functions.roll
        
        def patched_roll():
            """Patched roll function that uses the agent if it's the agent's turn."""
            if mainboard.player_index == player_index:
                logger.info(f"Agent's turn (Player {player_index + 1})")
                
                # Log to UI if available
                if hasattr(agent, 'dashboard') and agent.dashboard:
                    agent.dashboard.add_event(f"Agent's turn (Player {player_index + 1})")
                
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
        
        # Also patch other functions to log events
        if hasattr(functions, 'yes'):
            original_functions['yes'] = functions.yes
            
            def patched_yes():
                result = original_functions['yes']()
                # Log to UI if available
                if hasattr(agent, 'dashboard') and agent.dashboard:
                    agent.dashboard.add_event("Property purchased")
                return result
                
            functions.yes = patched_yes
        
        if hasattr(functions, 'build'):
            original_functions['build'] = functions.build
            
            def patched_build():
                result = original_functions['build']()
                # Log to UI if available
                if hasattr(agent, 'dashboard') and agent.dashboard:
                    agent.dashboard.add_event("House built")
                return result
                
            functions.build = patched_build
        
        if hasattr(functions, 'endturn'):
            original_functions['endturn'] = functions.endturn
            
            def patched_endturn():
                result = original_functions['endturn']()
                # Log to UI if available
                if hasattr(agent, 'dashboard') and agent.dashboard:
                    agent.dashboard.add_event("Turn ended")
                return result
                
            functions.endturn = patched_endturn
        
        logger.info(f"Patched game for agent to control player {player_index + 1}")
        
    except ImportError as e:
        # If direct import doesn't work, try to get the functions from the game state
        logger.warning(f"Could not directly import game functions: {e}")
        logger.info("Will try to access functions from game state when needed")_index == player_index:
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
        
    except ImportError as e:
        # If direct import doesn't work, try to get the functions from the game state
        logger.warning(f"Could not directly import game functions: {e}")
        logger.info("Will try to access functions from game state when needed")


def _get_game_state():
    """
    Get the current game state.
    
    Returns:
        Dictionary of game objects
    """
    try:
        # Try to import directly
        import player
        import mainboard
        import functions
        import firstpage
        import Property
        
        return {
            "_property": Property._property,
            "sproperty": Property.sproperty,
            "player": player.player,
            "player_index": mainboard.player_index,
            "rollonce": mainboard.rollonce,
            "functions": functions,
            "firstpage": firstpage
        }
    except ImportError:
        # If we can't import directly, return an empty state
        logger.warning("Could not import game modules to get state")
        return {}


def _execute_agent_decision(decision):
    """
    Execute the agent's decision.
    
    Args:
        decision: Decision dictionary
    """
    try:
        # Try to import directly
        import functions
        import Property
        
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