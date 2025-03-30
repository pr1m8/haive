import logging
from typing import Dict, Any, List, Optional, Tuple
from collections import deque

from src.haive.games.monopoly.models import PlayerInfo, PropertyInfo, SpecialCardInfo
from src.haive.games.monopoly.state import MonopolyState
from src.haive.core.models.llm.base import LLMConfig, AzureLLMConfig


# Set up logging
logger = logging.getLogger(__name__)

class MonopolyStateManager:
    """
    Manages the state of the Monopoly game.
    
    This class:
    - Extracts state from game objects
    - Provides helper methods for getting location info
    - Manages event history
    - Creates property ownership summaries
    """
    
    def __init__(self, max_events: int = 5):
        """
        Initialize the state manager.
        
        Args:
            max_events: Maximum number of events to track in history
        """
        self.max_events = max_events
        self.recent_events = deque(maxlen=max_events)
        self._location_info = {}
        self._property_info = {}
        
        # Default location info
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
    
    def add_event(self, event: str):
        """Add an event to the recent events history."""
        logger.debug(f"Adding event: {event}")
        self.recent_events.append(event)
    
    def get_recent_events(self) -> List[str]:
        """Get the recent events history."""
        return list(self.recent_events)
    
    def extract_state(self, game_objects: Dict[str, Any]) -> MonopolyState:
        """
        Extract the current state from the Monopoly game objects.
        
        Args:
            game_objects: Dictionary containing game objects
        
        Returns:
            MonopolyState object
        """
        try:
            # Extract player information
            players = []
            player_list = game_objects.get("player", [])
            
            for i, player_obj in enumerate(player_list):
                try:
                    if hasattr(player_obj, "cash"):
                        # Extract properties owned
                        properties_owned = []
                        if hasattr(player_obj, "properties"):
                            properties = getattr(player_obj, "properties")
                            if isinstance(properties, list):
                                properties_owned = properties
                            elif isinstance(properties, dict):
                                properties_owned = list(properties.keys())
                        
                        player_info = PlayerInfo(
                            name=f"Player {i+1}",
                            index=i,
                            position=player_obj.place if hasattr(player_obj, "place") else (0, 0),
                            cash=player_obj.cash,
                            total_wealth=player_obj.total_wealth if hasattr(player_obj, "total_wealth") else player_obj.cash,
                            properties_owned=properties_owned,
                            is_in_jail=getattr(player_obj, "released", 1) == 0,
                            jail_cards=getattr(player_obj, "jail_cards", 0),
                            railways_owned=getattr(player_obj, "no_of_railways", 0),
                            bankruptcy_status=getattr(player_obj, "bankruptcy_status", False)
                        )
                        players.append(player_info)
                except Exception as e:
                    logger.error(f"Error extracting player {i} info: {e}")
            
            # If no players found, create default ones
            if not players:
                players = [
                    PlayerInfo(
                        name="Player 1",
                        index=0,
                        position=(0, 0),
                        cash=15000,
                        total_wealth=15000,
                        properties_owned=[],
                        is_in_jail=False,
                        jail_cards=0,
                        railways_owned=0,
                        bankruptcy_status=False
                    ),
                    PlayerInfo(
                        name="Player 2",
                        index=1,
                        position=(0, 0),
                        cash=15000,
                        total_wealth=15000,
                        properties_owned=[],
                        is_in_jail=False,
                        jail_cards=0,
                        railways_owned=0,
                        bankruptcy_status=False
                    )
                ]
            
            # Extract property information
            properties = {}
            property_dict = game_objects.get("_property", {})
            
            for prop_name, prop_obj in property_dict.items():
                try:
                    if hasattr(prop_obj, "cost"):
                        rent_values = []
                        # Try to extract rent values if available
                        for i in range(6):  # 0-5 houses/hotel
                            attr_name = f"rent{i}"
                            if hasattr(prop_obj, attr_name):
                                rent_values.append(getattr(prop_obj, attr_name))
                        
                        property_info = PropertyInfo(
                            name=prop_name,
                            color=getattr(prop_obj, "color", "unknown"),
                            position=getattr(prop_obj, "position", (0, 0)),
                            cost=prop_obj.cost,
                            rent_values=rent_values,
                            rent=getattr(prop_obj, "rent", rent_values[0] if rent_values else 0),
                            mortgage_value=getattr(prop_obj, "mortgage", prop_obj.cost // 2),
                            owner=getattr(prop_obj, "owner", None),
                            houses=getattr(prop_obj, "no_of_houses", 0),
                            is_mortgaged=getattr(prop_obj, "is_mortgaged", False)
                        )
                        properties[prop_name] = property_info
                        
                        # Store for location info
                        self._property_info[prop_name] = property_info
                except Exception as e:
                    logger.error(f"Error extracting property {prop_name} info: {e}")
            
            # Extract special card information
            special_cards = {}
            special_dict = game_objects.get("sproperty", {})
            
            for card_name, card_obj in special_dict.items():
                try:
                    if hasattr(card_obj, "cost"):
                        card_type = "railroad" if "railroad" in card_name.lower() else "utility"
                        special_card_info = SpecialCardInfo(
                            name=card_name,
                            card_type=card_type,
                            position=getattr(card_obj, "position", (0, 0)),
                            cost=card_obj.cost,
                            rent=getattr(card_obj, "rent", 0),
                            mortgage_value=getattr(card_obj, "mortgage", card_obj.cost // 2),
                            owner=getattr(card_obj, "owner", None)
                        )
                        special_cards[card_name] = special_card_info
                except Exception as e:
                    logger.error(f"Error extracting special card {card_name} info: {e}")
            
            # Get current player index
            current_player_index = game_objects.get("player_index", 0)
            
            # Check if player has rolled
            has_rolled = game_objects.get("rollonce", 0) == 1
            
            # Update location info with property details
            self._update_location_info(properties)
            
            # Create and return the state
            return MonopolyState(
                properties=properties,
                special_cards=special_cards,
                players=players,
                current_player_index=current_player_index,
                dice=None,  # We don't have this information yet
                community_chest_drawn=None,  # We don't have this information yet
                chance_drawn=None,  # We don't have this information yet
                has_rolled=has_rolled,
                recent_events=list(self.recent_events)
            )
            
        except Exception as e:
            logger.error(f"Error extracting state: {e}")
            
            # Return a minimal valid state
            return MonopolyState(
                players=[
                    PlayerInfo(
                        name="Player 1",
                        index=0,
                        position=(0, 0),
                        cash=15000,
                        total_wealth=15000
                    ),
                    PlayerInfo(
                        name="Player 2",
                        index=1,
                        position=(0, 0),
                        cash=15000,
                        total_wealth=15000
                    )
                ],
                current_player_index=game_objects.get("player_index", 0),
                has_rolled=game_objects.get("rollonce", 0) == 1,
                recent_events=list(self.recent_events)
            )
            
    def _update_location_info(self, properties: Dict[str, PropertyInfo]) -> None:
        """Update location info with property details."""
        for prop_name, prop_info in properties.items():
            if prop_name in self._location_info:
                owned_str = ""
                if prop_info.owner is not None:
                    owned_str = f", owned by Player {prop_info.owner + 1}"
                
                houses_str = ""
                if prop_info.houses > 0:
                    houses_str = f", has {prop_info.houses} houses"
                
                self._location_info[prop_name] = f"{prop_info.color} property, costs ${prop_info.cost}{owned_str}{houses_str}"
    
    def get_location_info(self) -> str:
        """
        Get information about the current location.
        
        Returns:
            Description of the current location
        """
        if not self._location_info:
            self._init_default_location_info()
        
        # Create a formatted string with all location info
        info_str = "Location Information:\n"
        for name, desc in self._location_info.items():
            info_str += f"- {name}: {desc}\n"
        
        return info_str
    
    def get_properties_by_country(self, color_group: str) -> List[PropertyInfo]:
        """
        Get all properties in a specific color group.
        
        Args:
            color_group: Name of the color group
            
        Returns:
            List of matching PropertyInfo objects
        """
        return [
            prop for prop in self._property_info.values() 
            if prop.color == color_group
        ]
    
    def can_build_house(self, player_idx: int, property_name: str) -> bool:
        """
        Check if a player can build a house on a property.
        
        Args:
            player_idx: Index of the player
            property_name: Name of the property
            
        Returns:
            True if a house can be built
        """
        # Get property info
        prop = self._property_info.get(property_name)
        if not prop:
            return False
            
        # Check if player owns the property
        if prop.owner != player_idx:
            return False
            
        # Check if property is mortgaged
        if prop.is_mortgaged:
            return False
            
        # Check house limit (maximum 5 - where 5 means a hotel)
        if prop.houses >= 5:
            return False
            
        # Get all properties in the same color group
        color_props = self.get_properties_by_country(prop.color)
        
        # Check if player owns all properties in the group
        if not all(p.owner == player_idx for p in color_props):
            return False
            
        # Check even building rule
        min_houses = min(p.houses for p in color_props)
        
        # Can only build if this property has the minimum houses in its group
        return prop.houses == min_houses
    
    def can_sell_house(self, player_idx: int, property_name: str) -> bool:
        """
        Check if a player can sell a house from a property.
        
        Args:
            player_idx: Index of the player
            property_name: Name of the property
            
        Returns:
            True if a house can be sold
        """
        # Get property info
        prop = self._property_info.get(property_name)
        if not prop:
            return False
            
        # Check if player owns the property
        if prop.owner != player_idx:
            return False
            
        # Check if property has houses
        if prop.houses <= 0:
            return False
            
        # Get all properties in the same color group
        color_props = self.get_properties_by_country(prop.color)
        
        # Check even building rule
        max_houses = max(p.houses for p in color_props)
        
        # Can only sell if this property has the maximum houses in its group
        return prop.houses == max_houses
    
    def can_mortgage(self, player_idx: int, property_name: str) -> bool:
        """
        Check if a player can mortgage a property.
        
        Args:
            player_idx: Index of the player
            property_name: Name of the property
            
        Returns:
            True if the property can be mortgaged
        """
        # Get property info
        prop = self._property_info.get(property_name)
        if not prop:
            return False
            
        # Check if player owns the property
        if prop.owner != player_idx:
            return False
            
        # Check if property is already mortgaged
        if prop.is_mortgaged:
            return False
            
        # Check if property has houses (must sell houses first)
        if prop.houses > 0:
            return False
            
        return True
    
    def can_unmortgage(self, player_idx: int, property_name: str, player_cash: int) -> bool:
        """
        Check if a player can unmortgage a property.
        
        Args:
            player_idx: Index of the player
            property_name: Name of the property
            player_cash: Player's current cash
            
        Returns:
            True if the property can be unmortgaged
        """
        # Get property info
        prop = self._property_info.get(property_name)
        if not prop:
            return False
            
        # Check if player owns the property
        if prop.owner != player_idx:
            return False
            
        # Check if property is mortgaged
        if not prop.is_mortgaged:
            return False
            
        # Calculate unmortgage cost (mortgage value + 10%)
        unmortgage_cost = int(prop.mortgage_value * 1.1)
        
        # Check if player has enough cash
        return player_cash >= unmortgage_cost
    
    def generate_property_ownership_summary(self) -> str:
        """
        Generate a summary of property ownership for the game.
        
        Returns:
            String summary of property ownership
        """
        property_groups = {}
        
        # Group properties by color/country
        for prop_name, prop_info in self._property_info.items():
            group = prop_info.color
            if group not in property_groups:
                property_groups[group] = []
            
            owner_str = "Unowned"
            if prop_info.owner is not None:
                owner_str = f"Player {prop_info.owner + 1}"
            
            houses_str = ""
            if prop_info.houses > 0:
                houses_str = f" ({prop_info.houses} houses)"
            
            property_groups[group].append(f"{prop_name}: {owner_str}{houses_str}")
        
        # Generate the summary
        summary_lines = [f"Property Ownership Summary:"]
        
        for group, properties in property_groups.items():
            summary_lines.append(f"\n{group}:")
            for prop in properties:
                summary_lines.append(f"  - {prop}")
        
        return "\n".join(summary_lines)