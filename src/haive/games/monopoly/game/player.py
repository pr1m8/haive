from typing import List
from src.haive.games.monopoly.game.property import Property

class Player:
    """Represents a player in the game."""
    def __init__(self, name: str, index: int, starting_cash: int = 1500):
        self.name = name
        self.index = index
        self.cash = starting_cash
        self.position = 0  # Position on the board
        self.properties: List[int] = []  # List of property positions owned
        self.jail_cards = 0  # Number of "Get Out of Jail Free" cards
        self.in_jail = False
        self.jail_turns = 0  # Number of turns spent in jail
        self.bankruptcy_status = False  # Whether the player is bankrupt
        
    def own_property(self, property_position: int) -> None:
        """Add a property to this player's properties."""
        if property_position not in self.properties:
            self.properties.append(property_position)
    
    def lose_property(self, property_position: int) -> None:
        """Remove a property from this player's properties."""
        if property_position in self.properties:
            self.properties.remove(property_position)
    
    def pay(self, amount: int) -> bool:
        """
        Pay an amount from the player's cash.
        
        Args:
            amount: Amount to pay
            
        Returns:
            True if the payment was successful, False if player can't afford it
        """
        if amount <= 0:
            return True
            
        if self.cash >= amount:
            self.cash -= amount
            return True
        return False
    
    def receive(self, amount: int) -> None:
        """
        Receive an amount of cash.
        
        Args:
            amount: Amount to receive
        """
        if amount > 0:
            self.cash += amount
    
    def net_worth(self, board_properties: List[Property]) -> int:
        """
        Calculate the player's net worth including property values.
        
        Args:
            board_properties: List of all properties on the board
            
        Returns:
            The player's total net worth
        """
        # Cash value
        worth = self.cash
        
        # Add property values
        for prop_pos in self.properties:
            prop = next((p for p in board_properties if p.position == prop_pos), None)
            if prop:
                if not prop.is_mortgaged:
                    worth += prop.price  # Full property value
                    worth += prop.houses * prop.house_cost  # House value
                else:
                    worth += prop.mortgage_value  # Mortgaged value
        
        return worth
