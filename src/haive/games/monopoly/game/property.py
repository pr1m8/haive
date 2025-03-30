from typing import List, Optional
from src.haive.games.monopoly.game.types import PropertyType, SpecialSquareType

class Property:
    """Represents a property on the board."""
    def __init__(
        self, 
        name: str, 
        position: int,
        property_type: PropertyType,
        price: int = 0,
        color_group: Optional[str] = None,
        rent_values: Optional[List[int]] = None,
        mortgage_value: Optional[int] = None,
        house_cost: Optional[int] = None,
        special_type: Optional[SpecialSquareType] = None
    ):
        self.name = name
        self.position = position
        self.property_type = property_type
        self.price = price
        self.color_group = color_group
        self.rent_values = rent_values or [0]
        self.mortgage_value = mortgage_value or (price // 2 if price else 0)
        self.house_cost = house_cost or 0
        self.special_type = special_type
        
        # State variables
        self.owner: Optional[int] = None  # Player index who owns this property
        self.houses: int = 0  # Number of houses (5 = hotel)
        self.is_mortgaged: bool = False
    
    def get_rent(self, dice_roll: Optional[int] = None) -> int:
        """
        Calculate the rent for this property.
        
        Args:
            dice_roll: The dice roll (needed for utilities)
            
        Returns:
            The rent amount
        """
        if self.is_mortgaged or self.owner is None:
            return 0
            
        if self.property_type == PropertyType.PROPERTY:
            # Regular property rent based on houses
            house_level = min(self.houses, len(self.rent_values) - 1)
            return self.rent_values[house_level]
            
        elif self.property_type == PropertyType.RAILROAD:
            # Railroad rent based on how many railroads the owner has
            return self.rent_values[0]  # Will be updated by the game engine
            
        elif self.property_type == PropertyType.UTILITY:
            # Utility rent based on dice roll and how many utilities the owner has
            multiplier = self.rent_values[0]  # Will be updated by the game engine
            return (dice_roll or 7) * multiplier  # Default to 7 if no dice roll provided
            
        return 0
    
