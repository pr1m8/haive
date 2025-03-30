
"""
Monopoly Game Engine - Core implementation optimized for AI agent experimentation.
This module contains the core game rules and state management without UI dependencies.
"""
import random
import logging

from typing import List, Dict, Optional, Tuple, Set, Any, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from src.haive.games.monopoly.game.card import Card
from src.haive.games.monopoly.game.player import Player
from src.haive.games.monopoly.game.property import Property
from src.haive.games.monopoly.game.types import PropertyType, SpecialSquareType, ActionType


class MonopolyGame:
    """
    Core Monopoly game engine without UI dependencies.
    Designed for AI agent experimentation.
    """
    
    # Standard Monopoly board configuration
    DEFAULT_BOARD = [
        # Position, Name, Type, Price, Color Group, [Rent Values], House Cost
        (0, "Go", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.GO),
        (1, "Mediterranean Avenue", PropertyType.PROPERTY, 60, "Brown", [2, 10, 30, 90, 160, 250], 50),
        (2, "Community Chest", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.COMMUNITY_CHEST),
        (3, "Baltic Avenue", PropertyType.PROPERTY, 60, "Brown", [4, 20, 60, 180, 320, 450], 50),
        (4, "Income Tax", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.INCOME_TAX),
        (5, "Reading Railroad", PropertyType.RAILROAD, 200, "Railroad", [25, 50, 100, 200], None),
        (6, "Oriental Avenue", PropertyType.PROPERTY, 100, "Light Blue", [6, 30, 90, 270, 400, 550], 50),
        (7, "Chance", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.CHANCE),
        (8, "Vermont Avenue", PropertyType.PROPERTY, 100, "Light Blue", [6, 30, 90, 270, 400, 550], 50),
        (9, "Connecticut Avenue", PropertyType.PROPERTY, 120, "Light Blue", [8, 40, 100, 300, 450, 600], 50),
        (10, "Jail", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.JAIL),
        (11, "St. Charles Place", PropertyType.PROPERTY, 140, "Pink", [10, 50, 150, 450, 625, 750], 100),
        (12, "Electric Company", PropertyType.UTILITY, 150, "Utility", [4, 10], None),
        (13, "States Avenue", PropertyType.PROPERTY, 140, "Pink", [10, 50, 150, 450, 625, 750], 100),
        (14, "Virginia Avenue", PropertyType.PROPERTY, 160, "Pink", [12, 60, 180, 500, 700, 900], 100),
        (15, "Pennsylvania Railroad", PropertyType.RAILROAD, 200, "Railroad", [25, 50, 100, 200], None),
        (16, "St. James Place", PropertyType.PROPERTY, 180, "Orange", [14, 70, 200, 550, 750, 950], 100),
        (17, "Community Chest", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.COMMUNITY_CHEST),
        (18, "Tennessee Avenue", PropertyType.PROPERTY, 180, "Orange", [14, 70, 200, 550, 750, 950], 100),
        (19, "New York Avenue", PropertyType.PROPERTY, 200, "Orange", [16, 80, 220, 600, 800, 1000], 100),
        (20, "Free Parking", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.FREE_PARKING),
        (21, "Kentucky Avenue", PropertyType.PROPERTY, 220, "Red", [18, 90, 250, 700, 875, 1050], 150),
        (22, "Chance", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.CHANCE),
        (23, "Indiana Avenue", PropertyType.PROPERTY, 220, "Red", [18, 90, 250, 700, 875, 1050], 150),
        (24, "Illinois Avenue", PropertyType.PROPERTY, 240, "Red", [20, 100, 300, 750, 925, 1100], 150),
        (25, "B&O Railroad", PropertyType.RAILROAD, 200, "Railroad", [25, 50, 100, 200], None),
        (26, "Atlantic Avenue", PropertyType.PROPERTY, 260, "Yellow", [22, 110, 330, 800, 975, 1150], 150),
        (27, "Ventnor Avenue", PropertyType.PROPERTY, 260, "Yellow", [22, 110, 330, 800, 975, 1150], 150),
        (28, "Water Works", PropertyType.UTILITY, 150, "Utility", [4, 10], None),
        (29, "Marvin Gardens", PropertyType.PROPERTY, 280, "Yellow", [24, 120, 360, 850, 1025, 1200], 150),
        (30, "Go To Jail", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.GO_TO_JAIL),
        (31, "Pacific Avenue", PropertyType.PROPERTY, 300, "Green", [26, 130, 390, 900, 1100, 1275], 200),
        (32, "North Carolina Avenue", PropertyType.PROPERTY, 300, "Green", [26, 130, 390, 900, 1100, 1275], 200),
        (33, "Community Chest", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.COMMUNITY_CHEST),
        (34, "Pennsylvania Avenue", PropertyType.PROPERTY, 320, "Green", [28, 150, 450, 1000, 1200, 1400], 200),
        (35, "Short Line", PropertyType.RAILROAD, 200, "Railroad", [25, 50, 100, 200], None),
        (36, "Chance", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.CHANCE),
        (37, "Park Place", PropertyType.PROPERTY, 350, "Blue", [35, 175, 500, 1100, 1300, 1500], 200),
        (38, "Luxury Tax", PropertyType.SPECIAL, 0, None, None, None, None, SpecialSquareType.LUXURY_TAX),
        (39, "Boardwalk", PropertyType.PROPERTY, 400, "Blue", [50, 200, 600, 1400, 1700, 2000], 200)
    ]
    
    # Standard Monopoly configuration values
    GO_SALARY = 200
    JAIL_POSITION = 10
    MAX_HOUSES_PER_PROPERTY = 5  # 4 houses + 1 hotel
    JAIL_FEE = 50
    INCOME_TAX = 200  # Or 10% of total value, player's choice
    LUXURY_TAX = 100
    
    def __init__(
        self, 
        player_names: List[str],
        board_config: Optional[List[Tuple]] = None,
        starting_cash: int = 1500,
        max_rounds: int = 100,
        free_parking_money: bool = False,
        auction_properties: bool = True
    ):
        """
        Initialize a new Monopoly game.
        
        Args:
            player_names: List of player names
            board_config: Optional custom board configuration
            starting_cash: Starting cash for each player
            max_rounds: Maximum number of rounds to play
            free_parking_money: Whether Free Parking collects money
            auction_properties: Whether to auction unsold properties
        """
        self.max_players = len(player_names)
        if self.max_players < 2:
            raise ValueError("At least 2 players required")
        
        # Game configuration
        self.max_rounds = max_rounds
        self.free_parking_money = free_parking_money
        self.auction_properties = auction_properties
        self.free_parking_pot = 0

        # Initialize players
        self.players = [
            Player(name, i, starting_cash=starting_cash)
            for i, name in enumerate(player_names)
        ]
        
        # Initialize board
        board_data = board_config or self.DEFAULT_BOARD
        self.properties = []
        
        for pos, name, prop_type, price, color, rents, house_cost, _, special_type in board_data:
            self.properties.append(Property(
                name=name,
                position=pos,
                property_type=prop_type,
                price=price,
                color_group=color,
                rent_values=rents,
                house_cost=house_cost,
                special_type=special_type
            ))
        
        # Initialize deck of cards
        self.chance_cards = self._create_chance_cards()
        self.community_chest_cards = self._create_community_chest_cards()
        random.shuffle(self.chance_cards)
        random.shuffle(self.community_chest_cards)
        
        # Game state
        self.current_player_idx = 0
        self.current_round = 0
        self.doubles_count = 0
        self.last_dice_roll = (0, 0)
        self.properties_to_auction = []
        self.has_rolled = False
        self.game_over = False
        self.winner = None
        self.event_log = []
    
    def _create_chance_cards(self) -> List[Card]:
        """Create the standard Chance cards."""
        return [
            Card("Advance to Go. Collect $200.", "move_to", 0),
            Card("Advance to Illinois Avenue. If you pass Go, collect $200.", "move_to", 24),
            Card("Advance to St. Charles Place. If you pass Go, collect $200.", "move_to", 11),
            Card("Advance to nearest Utility.", "move_to_nearest", "Utility"),
            Card("Advance to nearest Railroad.", "move_to_nearest", "Railroad"),
            Card("Bank pays you dividend of $50.", "collect", 50),
            Card("Get Out of Jail Free.", "jail_card", None),
            Card("Go back 3 spaces.", "move_relative", -3),
            Card("Go to Jail. Go directly to Jail, do not pass Go, do not collect $200.", "go_to_jail", None),
            Card("Make general repairs on all your property. For each house pay $25, for each hotel pay $100.", "pay_repairs", (25, 100)),
            Card("Pay poor tax of $15.", "pay", 15),
            Card("Take a trip to Reading Railroad. If you pass Go, collect $200.", "move_to", 5),
            Card("Take a walk on the Boardwalk. Advance to Boardwalk.", "move_to", 39),
            Card("You have been elected Chairman of the Board. Pay each player $50.", "pay_each", 50),
            Card("Your building loan matures. Collect $150.", "collect", 150),
            Card("You have won a crossword competition. Collect $100.", "collect", 100)
        ]
    
    def _create_community_chest_cards(self) -> List[Card]:
        """Create the standard Community Chest cards."""
        return [
            Card("Advance to Go. Collect $200.", "move_to", 0),
            Card("Bank error in your favor. Collect $200.", "collect", 200),
            Card("Doctor's fee. Pay $50.", "pay", 50),
            Card("From sale of stock you get $50.", "collect", 50),
            Card("Get Out of Jail Free.", "jail_card", None),
            Card("Go to Jail. Go directly to jail, do not pass Go, do not collect $200.", "go_to_jail", None),
            Card("Grand Opera Night. Collect $50 from every player for opening night seats.", "collect_each", 50),
            Card("Holiday fund matures. Receive $100.", "collect", 100),
            Card("Income tax refund. Collect $20.", "collect", 20),
            Card("It is your birthday. Collect $10 from every player.", "collect_each", 10),
            Card("Life insurance matures. Collect $100.", "collect", 100),
            Card("Pay hospital fees of $100.", "pay", 100),
            Card("Pay school fees of $50.", "pay", 50),
            Card("Receive $25 consultancy fee.", "collect", 25),
            Card("You are assessed for street repair. $40 per house, $115 per hotel.", "pay_repairs", (40, 115)),
            Card("You have won second prize in a beauty contest. Collect $10.", "collect", 10),
            Card("You inherit $100.", "collect", 100)
        ]
    
    def log_event(self, event: str) -> None:
        """
        Add an event to the game log.
        
        Args:
            event: Description of the event
        """
        self.event_log.append(event)
        logger.info(event)
    
    def roll_dice(self) -> Tuple[int, int]:
        """
        Roll two dice.
        
        Returns:
            Tuple of (die1, die2)
        """
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.last_dice_roll = (die1, die2)
        
        # Check for doubles
        is_doubles = die1 == die2
        if is_doubles:
            self.doubles_count += 1
        else:
            self.doubles_count = 0
            
        return (die1, die2)
    
    def get_current_player(self) -> Player:
        """
        Get the current player.
        
        Returns:
            Current Player object
        """
        return self.players[self.current_player_idx]
    
    def get_property_at(self, position: int) -> Optional[Property]:
        """
        Get the property at a specific position.
        
        Args:
            position: Board position
            
        Returns:
            Property object or None if not found
        """
        for prop in self.properties:
            if prop.position == position:
                return prop
        return None
    
    def get_properties_by_group(self, color_group: str) -> List[Property]:
        """
        Get all properties in a color group.
        
        Args:
            color_group: Name of the color group
            
        Returns:
            List of Property objects
        """
        return [p for p in self.properties if p.color_group == color_group]
    
    def get_properties_owned_by_player(self, player_idx: int) -> List[Property]:
        """
        Get all properties owned by a player.
        
        Args:
            player_idx: Index of the player
            
        Returns:
            List of Property objects
        """
        return [p for p in self.properties if p.owner == player_idx]
    
    def player_owns_all_in_group(self, player_idx: int, color_group: str) -> bool:
        """
        Check if a player owns all properties in a group.
        
        Args:
            player_idx: Index of the player
            color_group: Name of the color group
            
        Returns:
            True if player owns all properties in the group
        """
        group_properties = self.get_properties_by_group(color_group)
        return all(p.owner == player_idx for p in group_properties)
    
    def can_build_house(self, property_position: int) -> bool:
        """
        Check if a house can be built on a property.
        
        Args:
            property_position: Position of the property
            
        Returns:
            True if a house can be built
        """
        prop = self.get_property_at(property_position)
        if not prop or prop.property_type != PropertyType.PROPERTY:
            return False
            
        # Check ownership
        if prop.owner is None:
            return False
            
        # Check if player owns all properties in the group
        if not self.player_owns_all_in_group(prop.owner, prop.color_group):
            return False
            
        # Check if property is mortgaged
        if prop.is_mortgaged:
            return False
            
        # Check house limit
        if prop.houses >= self.MAX_HOUSES_PER_PROPERTY:
            return False
            
        # Check even building rule
        group_props = self.get_properties_by_group(prop.color_group)
        min_houses = min(p.houses for p in group_props)
        
        # Can only build if this property has the minimum houses in its group
        return prop.houses == min_houses
    
    def can_sell_house(self, property_position: int) -> bool:
        """
        Check if a house can be sold from a property.
        
        Args:
            property_position: Position of the property
            
        Returns:
            True if a house can be sold
        """
        prop = self.get_property_at(property_position)
        if not prop or prop.property_type != PropertyType.PROPERTY:
            return False
            
        # Check if there are houses to sell
        if prop.houses <= 0:
            return False
            
        # Check even building rule
        group_props = self.get_properties_by_group(prop.color_group)
        max_houses = max(p.houses for p in group_props)
        
        # Can only sell if this property has the maximum houses in its group
        return prop.houses == max_houses
    
    def can_mortgage(self, property_position: int) -> bool:
        """
        Check if a property can be mortgaged.
        
        Args:
            property_position: Position of the property
            
        Returns:
            True if the property can be mortgaged
        """
        prop = self.get_property_at(property_position)
        if not prop:
            return False
            
        # Check if already mortgaged
        if prop.is_mortgaged:
            return False
            
        # Check if there are houses (must sell houses first)
        if prop.property_type == PropertyType.PROPERTY and prop.houses > 0:
            return False
            
        # Check if any property in the group has houses (can't mortgage if any have houses)
        if prop.property_type == PropertyType.PROPERTY:
            group_props = self.get_properties_by_group(prop.color_group)
            if any(p.houses > 0 for p in group_props):
                return False
                
        return True
    
    def can_unmortgage(self, property_position: int, player: Player) -> bool:
        """
        Check if a property can be unmortgaged.
        
        Args:
            property_position: Position of the property
            player: Player attempting to unmortgage
            
        Returns:
            True if the property can be unmortgaged
        """
        prop = self.get_property_at(property_position)
        if not prop:
            return False
            
        # Check if mortgaged
        if not prop.is_mortgaged:
            return False
            
        # Check if player has enough money (mortgage value + 10%)
        unmortgage_cost = int(prop.mortgage_value * 1.1)
        return player.cash >= unmortgage_cost
    
    def perform_action(self, action_type: ActionType, player_idx: int, **kwargs) -> bool:
        """
        Perform an action for a player.
        
        Args:
            action_type: Type of action to perform
            player_idx: Index of the player performing the action
            **kwargs: Action-specific parameters
            
        Returns:
            True if the action was successful
        """
        player = self.players[player_idx]
        
        if player.bankruptcy_status:
            self.log_event(f"{player.name} is bankrupt and cannot perform actions.")
            return False
            
        if player_idx != self.current_player_idx:
            self.log_event(f"It's not {player.name}'s turn.")
            return False
        
        if action_type == ActionType.ROLL:
            return self._handle_roll_action(player)
            
        elif action_type == ActionType.BUY:
            property_position = kwargs.get("position", player.position)
            return self._handle_buy_action(player, property_position)
            
        elif action_type == ActionType.SELL_HOUSE:
            property_position = kwargs.get("position")
            return self._handle_sell_house_action(player, property_position)
            
        elif action_type == ActionType.BUILD_HOUSE:
            property_position = kwargs.get("position")
            return self._handle_build_house_action(player, property_position)
            
        elif action_type == ActionType.MORTGAGE:
            property_position = kwargs.get("position")
            return self._handle_mortgage_action(player, property_position)
            
        elif action_type == ActionType.UNMORTGAGE:
            property_position = kwargs.get("position")
            return self._handle_unmortgage_action(player, property_position)
            
        elif action_type == ActionType.END_TURN:
            return self._handle_end_turn_action(player)
            
        elif action_type == ActionType.PAY_JAIL_FEE:
            return self._handle_pay_jail_fee_action(player)
            
        elif action_type == ActionType.USE_JAIL_CARD:
            return self._handle_use_jail_card_action(player)
            
        elif action_type == ActionType.ROLL_FOR_JAIL:
            return self._handle_roll_for_jail_action(player)
            
        elif action_type == ActionType.TRADE:
            other_player_idx = kwargs.get("other_player_idx")
            give_properties = kwargs.get("give_properties", [])
            take_properties = kwargs.get("take_properties", [])
            give_money = kwargs.get("give_money", 0)
            take_money = kwargs.get("take_money", 0)
            return self._handle_trade_action(
                player, other_player_idx, give_properties, take_properties, 
                give_money, take_money
            )
            
        elif action_type == ActionType.AUCTION:
            property_position = kwargs.get("position")
            return self._handle_auction_action(property_position)
            
        return False
    
    def _handle_roll_action(self, player: Player) -> bool:
        """Handle rolling the dice and moving."""
        if self.has_rolled and self.doubles_count == 0:
            self.log_event(f"{player.name} has already rolled this turn.")
            return False
            
        if player.in_jail:
            self.log_event(f"{player.name} is in jail and must pay, use a card, or roll for doubles.")
            return False
        
        # Roll the dice
        die1, die2 = self.roll_dice()
        total = die1 + die2
        is_doubles = die1 == die2
        
        self.log_event(f"{player.name} rolled {die1} and {die2} for a total of {total}.")
        
        # Check for three doubles in a row
        if self.doubles_count >= 3:
            self.log_event(f"{player.name} rolled doubles three times in a row. Go to Jail!")
            return self._send_to_jail(player)
        
        # Move the player
        old_position = player.position
        player.position = (player.position + total) % len(self.properties)
        
        # Check if passed Go
        if player.position < old_position:
            player.receive(self.GO_SALARY)
            self.log_event(f"{player.name} passed Go and collected ${self.GO_SALARY}.")
        
        # Handle landing on the new space
        self._handle_landing(player, player.position)
        
        # Mark as having rolled
        self.has_rolled = True
        
        # If not doubles, player's turn is essentially over after handling the landing
        return True
    
    def _handle_buy_action(self, player: Player, property_position: int) -> bool:
        """Handle buying a property."""
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        # Check if property can be purchased
        if prop.property_type in [PropertyType.SPECIAL]:
            self.log_event(f"{prop.name} cannot be purchased.")
            return False
            
        if prop.owner is not None:
            self.log_event(f"{prop.name} is already owned by {self.players[prop.owner].name}.")
            return False
            
        # Check if player has enough money
        if player.cash < prop.price:
            self.log_event(f"{player.name} does not have enough money to buy {prop.name}.")
            return False
            
        # Buy the property
        player.pay(prop.price)
        prop.owner = player.index
        player.own_property(prop.position)
        
        self.log_event(f"{player.name} bought {prop.name} for ${prop.price}.")
        return True
    
    def _handle_sell_house_action(self, player: Player, property_position: int) -> bool:
        """Handle selling a house from a property."""
        if not property_position:
            self.log_event("No property specified for selling a house.")
            return False
            
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        if prop.owner != player.index:
            self.log_event(f"{player.name} does not own {prop.name}.")
            return False
            
        if not self.can_sell_house(property_position):
            self.log_event(f"Cannot sell a house from {prop.name}.")
            return False
            
        # Sell the house
        prop.houses -= 1
        sell_value = prop.house_cost // 2  # Houses sell for half their cost
        player.receive(sell_value)
        
        house_or_hotel = "hotel" if prop.houses == 4 else "house"
        self.log_event(f"{player.name} sold a {house_or_hotel} from {prop.name} for ${sell_value}.")
        return True
    
    def _handle_build_house_action(self, player: Player, property_position: int) -> bool:
        """Handle building a house on a property."""
        if not property_position:
            self.log_event("No property specified for building a house.")
            return False
            
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        if prop.owner != player.index:
            self.log_event(f"{player.name} does not own {prop.name}.")
            return False
            
        if not self.can_build_house(property_position):
            self.log_event(f"Cannot build a house on {prop.name}.")
            return False
            
        # Check if player has enough money
        if player.cash < prop.house_cost:
            self.log_event(f"{player.name} does not have enough money to build a house on {prop.name}.")
            return False
            
        # Build the house
        player.pay(prop.house_cost)
        prop.houses += 1
        
        house_or_hotel = "hotel" if prop.houses == 5 else "house"
        self.log_event(f"{player.name} built a {house_or_hotel} on {prop.name} for ${prop.house_cost}.")
        return True
    
    def _handle_mortgage_action(self, player: Player, property_position: int) -> bool:
        """Handle mortgaging a property."""
        if not property_position:
            self.log_event("No property specified for mortgaging.")
            return False
            
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        if prop.owner != player.index:
            self.log_event(f"{player.name} does not own {prop.name}.")
            return False
            
        if not self.can_mortgage(property_position):
            self.log_event(f"Cannot mortgage {prop.name}.")
            return False
            
        # Mortgage the property
        prop.is_mortgaged = True
        player.receive(prop.mortgage_value)
        
        self.log_event(f"{player.name} mortgaged {prop.name} for ${prop.mortgage_value}.")
        return True
    
    def _handle_unmortgage_action(self, player: Player, property_position: int) -> bool:
        """Handle unmortgaging a property."""
        if not property_position:
            self.log_event("No property specified for unmortgaging.")
            return False
            
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        if prop.owner != player.index:
            self.log_event(f"{player.name} does not own {prop.name}.")
            return False
            
        if not self.can_unmortgage(property_position, player):
            self.log_event(f"Cannot unmortgage {prop.name}.")
            return False
            
        # Unmortgage the property
        unmortgage_cost = int(prop.mortgage_value * 1.1)
        player.pay(unmortgage_cost)
        prop.is_mortgaged = False
        
        self.log_event(f"{player.name} unmortgaged {prop.name} for ${unmortgage_cost}.")
        return True
    
    def _handle_end_turn_action(self, player: Player) -> bool:
        """Handle ending a player's turn."""
        if not self.has_rolled and not player.in_jail:
            self.log_event(f"{player.name} must roll first.")
            return False
            
        # Reset turn state
        self.has_rolled = False
        
        # If player rolled doubles, they go again
        if self.doubles_count > 0 and self.doubles_count < 3:
            self.log_event(f"{player.name} rolled doubles and gets another turn.")
            return True
            
        # Otherwise, advance to next player
        self._advance_to_next_player()
        return True
    
    def _handle_pay_jail_fee_action(self, player: Player) -> bool:
        """Handle paying the jail fee."""
        if not player.in_jail:
            self.log_event(f"{player.name} is not in jail.")
            return False
            
        if player.cash < self.JAIL_FEE:
            self.log_event(f"{player.name} does not have enough money to pay the jail fee.")
            return False
            
        # Pay the fee
        player.pay(self.JAIL_FEE)
        player.in_jail = False
        player.jail_turns = 0
        
        self.log_event(f"{player.name} paid ${self.JAIL_FEE} to get out of jail.")
        return True
    
    def _handle_use_jail_card_action(self, player: Player) -> bool:
        """Handle using a Get Out of Jail Free card."""
        if not player.in_jail:
            self.log_event(f"{player.name} is not in jail.")
            return False
            
        if player.jail_cards <= 0:
            self.log_event(f"{player.name} does not have a Get Out of Jail Free card.")
            return False
            
        # Use the card
        player.jail_cards -= 1
        player.in_jail = False
        player.jail_turns = 0
        
        self.log_event(f"{player.name} used a Get Out of Jail Free card.")
        return True
    
    def _handle_roll_for_jail_action(self, player: Player) -> bool:
        """Handle rolling for doubles to get out of jail."""
        if not player.in_jail:
            self.log_event(f"{player.name} is not in jail.")
            return False
            
        # Check if this is the third turn in jail
        if player.jail_turns >= 2:
            self.log_event(f"This is {player.name}'s third turn in jail and must pay to get out.")
            return self._handle_pay_jail_fee_action(player)
            
        # Roll the dice
        die1, die2 = self.roll_dice()
        is_doubles = die1 == die2
        
        self.log_event(f"{player.name} rolled {die1} and {die2} attempting to get out of jail.")
        
        if is_doubles:
            # Success! Get out of jail
            player.in_jail = False
            player.jail_turns = 0
            
            # Move the player
            player.position = (player.position + die1 + die2) % len(self.properties)
            
            self.log_event(f"{player.name} rolled doubles and got out of jail!")
            
            # Handle landing on the new space
            self._handle_landing(player, player.position)
            
            # Mark as having rolled
            self.has_rolled = True
            
            return True
        else:
            # Failed to roll doubles
            player.jail_turns += 1
            self.log_event(f"{player.name} failed to roll doubles and remains in jail.")
            
            # Their turn is over
            self.has_rolled = True
            return True
    
    def _handle_trade_action(
        self, 
        player: Player, 
        other_player_idx: int, 
        give_properties: List[int], 
        take_properties: List[int], 
        give_money: int, 
        take_money: int
    ) -> bool:
        """Handle trading between players."""
        # Check if other player exists
        if other_player_idx < 0 or other_player_idx >= len(self.players):
            self.log_event(f"Invalid player index: {other_player_idx}")
            return False
            
        other_player = self.players[other_player_idx]
        
        # Check if other player is bankrupt
        if other_player.bankruptcy_status:
            self.log_event(f"{other_player.name} is bankrupt and cannot trade.")
            return False
            
        # Check if players have enough money
        if player.cash < give_money:
            self.log_event(f"{player.name} does not have enough money for this trade.")
            return False
            
        if other_player.cash < take_money:
            self.log_event(f"{other_player.name} does not have enough money for this trade.")
            return False
            
        # Check if players own the properties they're giving away
        for pos in give_properties:
            prop = self.get_property_at(pos)
            if not prop or prop.owner != player.index:
                self.log_event(f"{player.name} does not own property at position {pos}.")
                return False
                
            # Check if property has houses (must sell houses first)
            if prop.property_type == PropertyType.PROPERTY and prop.houses > 0:
                self.log_event(f"{prop.name} has houses and cannot be traded.")
                return False
        
        for pos in take_properties:
            prop = self.get_property_at(pos)
            if not prop or prop.owner != other_player.index:
                self.log_event(f"{other_player.name} does not own property at position {pos}.")
                return False
                
            # Check if property has houses (must sell houses first)
            if prop.property_type == PropertyType.PROPERTY and prop.houses > 0:
                self.log_event(f"{prop.name} has houses and cannot be traded.")
                return False
        
        # Execute the trade
        # Transfer money
        player.pay(give_money)
        other_player.receive(give_money)
        
        other_player.pay(take_money)
        player.receive(take_money)
        
        # Transfer properties
        for pos in give_properties:
            prop = self.get_property_at(pos)
            prop.owner = other_player.index
            player.lose_property(pos)
            other_player.own_property(pos)
            
        for pos in take_properties:
            prop = self.get_property_at(pos)
            prop.owner = player.index
            other_player.lose_property(pos)
            player.own_property(pos)
            
        self.log_event(f"{player.name} and {other_player.name} completed a trade.")
        return True
    
    def _handle_auction_action(self, property_position: int) -> bool:
        """Handle auctioning a property."""
        prop = self.get_property_at(property_position)
        
        if not prop:
            self.log_event(f"No property at position {property_position}.")
            return False
            
        if prop.owner is not None:
            self.log_event(f"{prop.name} is already owned.")
            return False
            
        # For simplicity, just assign it to the highest bidder at minimum price
        # In a real implementation, this would be a more complex auction process
        
        # Find the player with the most money
        eligible_players = [p for p in self.players if not p.bankruptcy_status and p.cash >= prop.price]
        
        if not eligible_players:
            self.log_event(f"No players can afford {prop.name}.")
            return False
            
        winner = max(eligible_players, key=lambda p: p.cash)
        
        # Assign the property to the winner
        winner.pay(prop.price)
        prop.owner = winner.index
        winner.own_property(prop.position)
        
        self.log_event(f"{winner.name} won the auction for {prop.name} at ${prop.price}.")
        return True
    def _handle_landing(self, player: Player, position: int) -> None:
        """Handle a player landing on a space."""
        prop = self.get_property_at(position)
        
        if not prop:
            self.log_event(f"No property at position {position}.")
            return
            
        self.log_event(f"{player.name} landed on {prop.name}.")
        
        # Handle special squares
        if prop.property_type == PropertyType.SPECIAL:
            self._handle_special_square(player, prop)
            return
            
        # Handle property, railroad, or utility
        if prop.owner is None:
            # Unowned property - can be purchased
            self.log_event(f"{prop.name} is unowned and can be purchased for ${prop.price}.")
            return
            
        if prop.owner == player.index:
            # Player owns this property
            self.log_event(f"{player.name} owns {prop.name}.")
            return
            
        # Another player owns this property - pay rent
        owner = self.players[prop.owner]
        
        if prop.is_mortgaged:
            self.log_event(f"{prop.name} is mortgaged, so no rent is due.")
            return
            
        # Calculate rent
        rent = 0
        
        if prop.property_type == PropertyType.PROPERTY:
            rent = prop.get_rent()
            
        elif prop.property_type == PropertyType.RAILROAD:
            # Count how many railroads the owner has
            railroads_owned = len([p for p in self.properties 
                                   if p.property_type == PropertyType.RAILROAD 
                                   and p.owner == prop.owner])
            
            # Railroad rent increases with more railroads owned
            railroad_index = min(railroads_owned - 1, len(prop.rent_values) - 1)
            rent = prop.rent_values[railroad_index]
            
        elif prop.property_type == PropertyType.UTILITY:
            # Count how many utilities the owner has
            utilities_owned = len([p for p in self.properties 
                                   if p.property_type == PropertyType.UTILITY 
                                   and p.owner == prop.owner])
            
            # Get the multiplier (4 for 1 utility, 10 for 2)
            multiplier = 4 if utilities_owned == 1 else 10
            
            # Rent is dice roll * multiplier
            dice_total = sum(self.last_dice_roll)
            rent = dice_total * multiplier
        
        # Pay the rent
        self.log_event(f"{player.name} pays ${rent} rent to {owner.name}.")
        
        if player.cash < rent:
            # Player can't afford rent - handle bankruptcy
            self._handle_bankruptcy(player, owner, rent)
        else:
            player.pay(rent)
            owner.receive(rent)
    
    def _handle_special_square(self, player: Player, prop: Property) -> None:
        """Handle landing on a special square."""
        if not prop.special_type:
            return
            
        if prop.special_type == SpecialSquareType.GO:
            # Already handled by passing Go
            pass
            
        elif prop.special_type == SpecialSquareType.JAIL:
            # Just visiting
            self.log_event(f"{player.name} is just visiting jail.")
            
        elif prop.special_type == SpecialSquareType.FREE_PARKING:
            # If using house rule, collect money from Free Parking
            if self.free_parking_money and self.free_parking_pot > 0:
                player.receive(self.free_parking_pot)
                self.log_event(f"{player.name} collected ${self.free_parking_pot} from Free Parking!")
                self.free_parking_pot = 0
            else:
                self.log_event(f"{player.name} is taking a break at Free Parking.")
            
        elif prop.special_type == SpecialSquareType.GO_TO_JAIL:
            self._send_to_jail(player)
            
        elif prop.special_type == SpecialSquareType.INCOME_TAX:
            # Pay income tax
            tax_amount = self.INCOME_TAX
            self.log_event(f"{player.name} pays ${tax_amount} in Income Tax.")
            
            if player.cash < tax_amount:
                # Handle bankruptcy to the bank
                self._handle_bankruptcy(player, None, tax_amount)
            else:
                player.pay(tax_amount)
                if self.free_parking_money:
                    self.free_parking_pot += tax_amount
            
        elif prop.special_type == SpecialSquareType.LUXURY_TAX:
            # Pay luxury tax
            tax_amount = self.LUXURY_TAX
            self.log_event(f"{player.name} pays ${tax_amount} in Luxury Tax.")
            
            if player.cash < tax_amount:
                # Handle bankruptcy to the bank
                self._handle_bankruptcy(player, None, tax_amount)
            else:
                player.pay(tax_amount)
                if self.free_parking_money:
                    self.free_parking_pot += tax_amount
            
        elif prop.special_type == SpecialSquareType.CHANCE:
            self._draw_chance_card(player)
            
        elif prop.special_type == SpecialSquareType.COMMUNITY_CHEST:
            self._draw_community_chest_card(player)
    
    def _send_to_jail(self, player: Player) -> bool:
        """Send a player to jail."""
        player.position = self.JAIL_POSITION
        player.in_jail = True
        player.jail_turns = 0
        
        self.log_event(f"{player.name} was sent to jail!")
        
        # Going to jail ends the player's turn
        self.has_rolled = True
        return True
    
    def _draw_chance_card(self, player: Player) -> None:
        """Draw a Chance card."""
        if not self.chance_cards:
            self.log_event("The Chance deck is empty.")
            return
            
        # Draw a card and put it at the bottom of the deck
        card = self.chance_cards.pop(0)
        self.chance_cards.append(card)
        
        self.log_event(f"{player.name} drew a Chance card: {card.text}")
        self._handle_card(player, card)
    
    def _draw_community_chest_card(self, player: Player) -> None:
        """Draw a Community Chest card."""
        if not self.community_chest_cards:
            self.log_event("The Community Chest deck is empty.")
            return
            
        # Draw a card and put it at the bottom of the deck
        card = self.community_chest_cards.pop(0)
        self.community_chest_cards.append(card)
        
        self.log_event(f"{player.name} drew a Community Chest card: {card.text}")
        self._handle_card(player, card)
    
    def _handle_card(self, player: Player, card: Card) -> None:
        """Handle the effects of a card."""
        if card.action == "move_to":
            # Move to a specific position
            old_position = player.position
            player.position = card.value
            
            # Check if passed Go
            if player.position < old_position and card.value != 0:  # Don't pay twice for Go
                player.receive(self.GO_SALARY)
                self.log_event(f"{player.name} passed Go and collected ${self.GO_SALARY}.")
                
            # Handle landing on the new space
            self._handle_landing(player, player.position)
            
        elif card.action == "move_to_nearest":
            # Move to the nearest property of a type
            old_position = player.position
            nearest_pos = self._find_nearest_property(player.position, card.value)
            
            if nearest_pos is not None:
                player.position = nearest_pos
                
                # Check if passed Go
                if player.position < old_position:
                    player.receive(self.GO_SALARY)
                    self.log_event(f"{player.name} passed Go and collected ${self.GO_SALARY}.")
                    
                # Handle landing on the new space
                self._handle_landing(player, player.position)
            
        elif card.action == "move_relative":
            # Move a relative number of spaces
            old_position = player.position
            player.position = (player.position + card.value) % len(self.properties)
            
            # Check if passed Go
            if card.value < 0 and player.position > old_position:
                player.receive(self.GO_SALARY)
                self.log_event(f"{player.name} passed Go and collected ${self.GO_SALARY}.")
                
            # Handle landing on the new space
            self._handle_landing(player, player.position)
            
        elif card.action == "go_to_jail":
            self._send_to_jail(player)
            
        elif card.action == "collect":
            # Collect money from the bank
            player.receive(card.value)
            self.log_event(f"{player.name} collected ${card.value}.")
            
        elif card.action == "pay":
            # Pay money to the bank
            amount = card.value
            self.log_event(f"{player.name} pays ${amount}.")
            
            if player.cash < amount:
                # Handle bankruptcy to the bank
                self._handle_bankruptcy(player, None, amount)
            else:
                player.pay(amount)
                if self.free_parking_money:
                    self.free_parking_pot += amount
            
        elif card.action == "pay_each":
            # Pay money to each player
            amount = card.value
            total = amount * (len(self.players) - 1)
            
            if player.cash < total:
                # Handle bankruptcy
                # For simplicity, just pay what you can evenly
                available = player.cash
                per_player = available // (len(self.players) - 1)
                
                if per_player > 0:
                    for p in self.players:
                        if p.index != player.index and not p.bankruptcy_status:
                            p.receive(per_player)
                    
                    player.pay(per_player * (len(self.players) - 1))
                
                self.log_event(f"{player.name} couldn't afford to pay everyone ${amount}.")
            else:
                for p in self.players:
                    if p.index != player.index and not p.bankruptcy_status:
                        p.receive(amount)
                
                player.pay(total)
                self.log_event(f"{player.name} paid ${amount} to each player.")
            
        elif card.action == "collect_each":
            # Collect money from each player
            amount = card.value
            
            for p in self.players:
                if p.index != player.index and not p.bankruptcy_status:
                    if p.cash < amount:
                        # Handle bankruptcy
                        self._handle_bankruptcy(p, player, amount)
                    else:
                        p.pay(amount)
                        player.receive(amount)
            
            self.log_event(f"{player.name} collected ${amount} from each player.")
            
        elif card.action == "pay_repairs":
            # Pay for repairs
            house_cost, hotel_cost = card.value
            
            # Count houses and hotels
            houses = 0
            hotels = 0
            
            for prop in self.get_properties_owned_by_player(player.index):
                if prop.property_type == PropertyType.PROPERTY:
                    if prop.houses == 5:  # Hotel
                        hotels += 1
                    else:
                        houses += prop.houses
            
            total_cost = (houses * house_cost) + (hotels * hotel_cost)
            
            self.log_event(f"{player.name} must pay ${total_cost} for repairs.")
            
            if player.cash < total_cost:
                # Handle bankruptcy to the bank
                self._handle_bankruptcy(player, None, total_cost)
            else:
                player.pay(total_cost)
                if self.free_parking_money:
                    self.free_parking_pot += total_cost
            
        elif card.action == "jail_card":
            # Receive a Get Out of Jail Free card
            player.jail_cards += 1
            self.log_event(f"{player.name} received a Get Out of Jail Free card.")
    
    def _find_nearest_property(self, position: int, property_type: str) -> Optional[int]:
        """Find the nearest property of a specific type."""
        board_size = len(self.properties)
        
        # Check positions ahead
        for i in range(1, board_size):
            check_pos = (position + i) % board_size
            prop = self.get_property_at(check_pos)
            
            if prop and (
                (property_type == "Railroad" and prop.property_type == PropertyType.RAILROAD) or
                (property_type == "Utility" and prop.property_type == PropertyType.UTILITY)
            ):
                return check_pos
        
        return None
    
    def _handle_bankruptcy(self, player: Player, creditor: Optional[Player], amount: int) -> None:
        """Handle a player going bankrupt."""
        self.log_event(f"{player.name} is bankrupt!")
        
        # Mark player as bankrupt
        player.bankruptcy_status = True
        
        # If the creditor is another player, transfer all assets
        if creditor:
            # Transfer cash
            creditor.receive(player.cash)
            player.cash = 0
            
            # Transfer properties
            for prop in self.get_properties_owned_by_player(player.index):
                prop.owner = creditor.index
                creditor.own_property(prop.position)
                
            # Transfer Get Out of Jail Free cards
            creditor.jail_cards += player.jail_cards
            player.jail_cards = 0
            
            self.log_event(f"{player.name}'s assets were transferred to {creditor.name}.")
        else:
            # Bankrupt to the bank - assets return to the bank
            player.cash = 0
            
            # Return properties to bank
            for prop in self.get_properties_owned_by_player(player.index):
                prop.owner = None
                prop.houses = 0
                prop.is_mortgaged = False
                
            # Return Get Out of Jail Free cards to the bottom of the deck
            # (simplified - just remove them)
            player.jail_cards = 0
            
            self.log_event(f"{player.name}'s assets were returned to the bank.")
        
        # Check if the game is over
        self._check_game_over()
    
    def _advance_to_next_player(self) -> None:
        """Advance to the next player who isn't bankrupt."""
        original_idx = self.current_player_idx
        
        while True:
            self.current_player_idx = (self.current_player_idx + 1) % len(self.players)
            
            # If we've gone through all players and back to the original, break
            if self.current_player_idx == original_idx:
                break
                
            # If this player isn't bankrupt, break
            if not self.players[self.current_player_idx].bankruptcy_status:
                break
        
        # Check if we've completed a round
        if self.current_player_idx == 0:
            self.current_round += 1
            self.log_event(f"Round {self.current_round} completed.")
            
            # Check if we've reached the maximum number of rounds
            if self.current_round >= self.max_rounds:
                self.log_event(f"Maximum number of rounds ({self.max_rounds}) reached.")
                self._end_game()
        
        # Log whose turn it is
        current_player = self.get_current_player()
        self.log_event(f"It's now {current_player.name}'s turn.")
        
        # Reset turn state
        self.doubles_count = 0
        
        # Handle player in jail
        if current_player.in_jail:
            current_player.jail_turns += 1
            self.log_event(f"{current_player.name} is in jail (turn {current_player.jail_turns}).")
            
            # If third turn in jail, force payment
            if current_player.jail_turns >= 3:
                self.log_event(f"This is {current_player.name}'s third turn in jail and must pay to get out.")
                self._handle_pay_jail_fee_action(current_player)
    
    def _check_game_over(self) -> bool:
        """Check if the game is over."""
        # Count non-bankrupt players
        active_players = [p for p in self.players if not p.bankruptcy_status]
        
        # If only one player is left, they're the winner
        if len(active_players) == 1:
            self.game_over = True
            self.winner = active_players[0]
            self.log_event(f"Game over! {self.winner.name} wins!")
            return True
            
        # If all players are bankrupt (unlikely), game is over with no winner
        if len(active_players) == 0:
            self.game_over = True
            self.winner = None
            self.log_event("Game over! All players are bankrupt.")
            return True
            
        return False
    
    def _end_game(self) -> None:
        """End the game due to round limit."""
        self.game_over = True
        
        # Determine winner based on net worth
        active_players = [p for p in self.players if not p.bankruptcy_status]
        
        if active_players:
            self.winner = max(active_players, key=lambda p: p.net_worth(self.properties))
            self.log_event(f"Game over! {self.winner.name} wins with net worth ${self.winner.net_worth(self.properties)}!")
        else:
            self.winner = None
            self.log_event("Game over! All players are bankrupt.")
    
    def get_game_state(self) -> Dict[str, Any]:
        """
        Get the current game state.
        
        Returns:
            Dictionary with the game state
        """
        return {
            "current_player_idx": self.current_player_idx,
            "current_round": self.current_round,
            "doubles_count": self.doubles_count,
            "last_dice_roll": self.last_dice_roll,
            "has_rolled": self.has_rolled,
            "game_over": self.game_over,
            "winner": self.winner.name if self.winner else None,
            "free_parking_pot": self.free_parking_pot,
            "players": [
                {
                    "name": p.name,
                    "index": p.index,
                    "cash": p.cash,
                    "position": p.position,
                    "properties": p.properties.copy(),
                    "jail_cards": p.jail_cards,
                    "in_jail": p.in_jail,
                    "jail_turns": p.jail_turns,
                    "bankruptcy_status": p.bankruptcy_status,
                    "net_worth": p.net_worth(self.properties)
                }
                for p in self.players
            ],
            "properties": [
                {
                    "name": p.name,
                    "position": p.position,
                    "type": p.property_type,
                    "price": p.price,
                    "color_group": p.color_group,
                    "owner": p.owner,
                    "houses": p.houses,
                    "is_mortgaged": p.is_mortgaged,
                    "rent": p.get_rent()
                }
                for p in self.properties
            ],
            "recent_events": self.event_log[-10:] if self.event_log else []
        }
    
    def print_game_state(self) -> None:
        """Print the current game state to the console."""
        print("\n==== MONOPOLY GAME STATE ====")
        print(f"Round: {self.current_round}")
        
        if self.game_over:
            print(f"GAME OVER! Winner: {self.winner.name if self.winner else 'None'}")
        else:
            print(f"Current Player: {self.get_current_player().name}")
            print(f"Last Dice Roll: {self.last_dice_roll}")
        
        print("\nPlayers:")
        for player in self.players:
            status = "BANKRUPT" if player.bankruptcy_status else ""
            jail_status = "IN JAIL" if player.in_jail else ""
            
            print(f"  {player.name}: ${player.cash} - Position: {self.properties[player.position].name} {status} {jail_status}")
            
            # Print properties
            if player.properties:
                props = [self.properties[pos].name for pos in player.properties]
                print(f"    Properties: {', '.join(props)}")
        
        print("\nRecent Events:")
        for event in self.event_log[-5:]:
            print(f"  {event}")
            
        print("============================\n")