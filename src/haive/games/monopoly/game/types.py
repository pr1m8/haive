from enum import Enum

class ActionType(str, Enum):
    """Types of actions a player can take."""
    ROLL = "roll"
    BUY = "buy"
    SELL_HOUSE = "sell_house"
    BUILD_HOUSE = "build_house"
    MORTGAGE = "mortgage"
    UNMORTGAGE = "unmortgage"
    END_TURN = "end_turn"
    PAY_JAIL_FEE = "pay_jail_fee"
    USE_JAIL_CARD = "use_jail_card"
    ROLL_FOR_JAIL = "roll_for_jail"
    TRADE = "trade"
    AUCTION = "auction"


class PropertyType(str, Enum):
    """Types of properties on the board."""
    PROPERTY = "property"  # Regular property with houses/hotels
    RAILROAD = "railroad"
    UTILITY = "utility"
    SPECIAL = "special"    # Go, Jail, Free Parking, etc.


class SpecialSquareType(str, Enum):
    """Types of special squares on the board."""
    GO = "go"
    JAIL = "jail"
    FREE_PARKING = "free_parking"
    GO_TO_JAIL = "go_to_jail"
    INCOME_TAX = "income_tax"
    LUXURY_TAX = "luxury_tax"
    CHANCE = "chance"
    COMMUNITY_CHEST = "community_chest"


