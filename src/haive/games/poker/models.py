"""Core data models for the Poker game implementation.

This module defines the fundamental data structures and models used in the poker game,
including:
    - Card suits and values
    - Hand rankings and game phases
    - Player actions and states
    - Game state tracking
    - Decision models for LLM output

The models use Pydantic for validation and serialization, ensuring type safety
and consistent data structures throughout the game.

Example:
    >>> from poker.models import Card, Suit, CardValue
    >>> 
    >>> # Create a card
    >>> ace_of_spades = Card(suit=Suit.SPADES, value=CardValue.ACE)
    >>> print(ace_of_spades)  # Shows "Ace of spades"
"""

from enum import Enum
from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field

# Enums for card suits and values
class Suit(str, Enum):
    """Card suit enumeration.
    
    Represents the four standard playing card suits. Inherits from str.Enum
    for easy serialization and string comparison.

    Attributes:
        HEARTS (str): Hearts suit
        DIAMONDS (str): Diamonds suit
        CLUBS (str): Clubs suit
        SPADES (str): Spades suit
    """
    HEARTS = "hearts"
    DIAMONDS = "diamonds"
    CLUBS = "clubs"
    SPADES = "spades"

class CardValue(int, Enum):
    """Card value enumeration.
    
    Represents standard playing card values from 2 to Ace. Inherits from int.Enum
    for numeric comparison (e.g., King > Queen). Ace is highest by default (14)
    but can be treated as 1 in certain contexts (e.g., A-2-3-4-5 straight).

    Attributes:
        TWO (int): Value 2
        THREE (int): Value 3
        ...
        KING (int): Value 13
        ACE (int): Value 14 (or 1 in some contexts)
    """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14  # Ace can also be 1 in some contexts

# Enum for poker hand rankings
class HandRank(int, Enum):
    """Poker hand ranking enumeration.
    
    Represents the standard poker hand rankings from high card to royal flush.
    Inherits from int.Enum for easy comparison of hand strengths.

    Attributes:
        HIGH_CARD (int): Highest card in hand
        PAIR (int): Two cards of same value
        TWO_PAIR (int): Two different pairs
        THREE_OF_A_KIND (int): Three cards of same value
        STRAIGHT (int): Five sequential cards
        FLUSH (int): Five cards of same suit
        FULL_HOUSE (int): Three of a kind plus a pair
        FOUR_OF_A_KIND (int): Four cards of same value
        STRAIGHT_FLUSH (int): Sequential cards of same suit
        ROYAL_FLUSH (int): A-K-Q-J-10 of same suit
    """
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8
    ROYAL_FLUSH = 9

# Enum for game phases
class GamePhase(str, Enum):
    """Poker game phase enumeration.
    
    Represents the different phases of a Texas Hold'em poker game.
    Inherits from str.Enum for easy serialization and comparison.

    Attributes:
        SETUP (str): Initial game setup
        PREFLOP (str): Before community cards
        FLOP (str): First three community cards
        TURN (str): Fourth community card
        RIVER (str): Fifth community card
        SHOWDOWN (str): Hand comparison
        GAME_OVER (str): Game completed
    """
    SETUP = "setup"
    PREFLOP = "preflop"
    FLOP = "flop"
    TURN = "turn"
    RIVER = "river"
    SHOWDOWN = "showdown"
    GAME_OVER = "game_over"

# Enum for player actions
class PlayerAction(str, Enum):
    """Player action enumeration.
    
    Represents the possible actions a player can take during their turn.
    Inherits from str.Enum for easy serialization and comparison.

    Attributes:
        FOLD (str): Give up hand
        CHECK (str): Pass action when no bet to call
        CALL (str): Match current bet
        BET (str): Place initial bet
        RAISE (str): Increase current bet
        ALL_IN (str): Bet all remaining chips
    """
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALL_IN = "all_in"

# Card model
class Card(BaseModel):
    """Playing card model.
    
    Represents a standard playing card with suit and value.
    Provides methods for numeric value comparison.

    Attributes:
        suit (Suit): Card's suit
        value (CardValue): Card's value

    Example:
        >>> card = Card(suit=Suit.HEARTS, value=CardValue.ACE)
        >>> print(card)  # Shows "Ace of hearts"
        >>> print(card.numeric_value)  # Shows 14
    """
    suit: Suit = Field(description="The suit of the card")
    value: CardValue = Field(description="The value of the card")
    
    def __str__(self) -> str:
        """String representation of the card."""
        return f"{self.value.name.capitalize()} of {self.suit.value}"

    @property
    def numeric_value(self) -> int:
        """Get numeric value of card (2-14, with Ace being 14)."""
        return self.value.value

    @property
    def numeric_value_low(self) -> int:
        """Get numeric value treating Ace as 1.
        
        Used for A-2-3-4-5 straight calculations.
        """
        return 1 if self.value == CardValue.ACE else self.value.value

# Hand model (combination of cards a player has)
class Hand(BaseModel):
    """Playing hand model.
    
    Represents a collection of cards held by a player or on the board.
    Limited to 7 cards maximum (2 hole cards + 5 community cards).

    Attributes:
        cards (List[Card]): List of cards in the hand

    Example:
        >>> hand = Hand(cards=[
        ...     Card(suit=Suit.HEARTS, value=CardValue.ACE),
        ...     Card(suit=Suit.HEARTS, value=CardValue.KING)
        ... ])
        >>> print(hand)  # Shows "Ace of hearts, King of hearts"
    """
    cards: List[Card] = Field(
        default_factory=list,
        max_length=7,
        description="The cards in the hand"
    )

    def __str__(self) -> str:
        """String representation of the hand."""
        return ", ".join(str(card) for card in self.cards)

# Player model
class Player(BaseModel):
    """Player model for poker game.
    
    Represents a player in the game, tracking their cards, chips, and game status.
    Includes betting information and position at the table.

    Attributes:
        id (str): Unique identifier for the player
        name (str): Display name of the player
        chips (int): Current chip count, defaults to 1000
        hand (Hand): Player's hole cards
        is_active (bool): Whether player is still in current hand
        is_all_in (bool): Whether player has gone all-in
        current_bet (int): Amount bet in current round
        total_bet (int): Total amount bet in current hand
        position (int): Position at table (0 = dealer)

    Example:
        >>> player = Player(
        ...     id="p1",
        ...     name="Alice",
        ...     chips=1000,
        ...     position=0
        ... )
        >>> print(player)  # Shows "Player Alice ($1000)"
    """
    id: str = Field(description="The unique identifier for the player")
    name: str = Field(description="The name of the player")
    chips: int = Field(default=1000, description="The number of chips the player has")
    hand: Hand = Field(default_factory=Hand, description="The cards the player has in their hand")
    is_active: bool = Field(default=True, description="Whether the player is still in the game")
    is_all_in: bool = Field(default=False, description="Whether the player is all in")
    current_bet: int = Field(default=0, description="The amount of chips the player has bet or raised")
    total_bet: int = Field(default=0, description="The total amount of chips the player has bet")
    position: int = Field(default=0, description="The position of the player in the game")

    def __str__(self) -> str:
        """String representation of the player."""
        return f"Player {self.name} (${self.chips})"

# Action model for tracking player actions
class ActionRecord(BaseModel):
    """Record of a player's action.
    
    Tracks a single action taken by a player during the game,
    including the type of action, amount (if any), and game phase.

    Attributes:
        player_id (str): ID of player who took action
        action (PlayerAction): Type of action taken
        amount (int): Chips bet/raised, if applicable
        phase (GamePhase): Game phase when action occurred

    Example:
        >>> record = ActionRecord(
        ...     player_id="p1",
        ...     action=PlayerAction.RAISE,
        ...     amount=100,
        ...     phase=GamePhase.FLOP
        ... )
    """
    player_id: str = Field(description="The unique identifier for the player")
    action: PlayerAction = Field(description="The action taken by the player")
    amount: int = Field(default=0, description="The amount of chips the player bet or raised")
    phase: GamePhase = Field(description="The phase of the game when the action was taken")

# Hand ranking result
class HandRanking(BaseModel):
    """Poker hand ranking result.
    
    Represents the evaluation of a player's best possible hand,
    including rank, high cards for tiebreakers, and description.

    Attributes:
        player_id (str): ID of player whose hand was ranked
        rank (HandRank): Type of hand (pair, flush, etc.)
        high_cards (List[CardValue]): Cards used for tiebreaking
        description (str): Human-readable hand description

    Example:
        >>> ranking = HandRanking(
        ...     player_id="p1",
        ...     rank=HandRank.FLUSH,
        ...     high_cards=[CardValue.ACE, CardValue.KING],
        ...     description="Ace-high flush"
        ... )
    """
    player_id: str = Field(description="The unique identifier for the player")
    rank: HandRank = Field(description="The rank of the hand")
    high_cards: List[CardValue] = Field(default_factory=list, description="The highest cards in the hand")
    description: str = Field(default="", description="The description of the hand")

# Pot model
class Pot(BaseModel):
    """Poker pot model.
    
    Represents a pot of chips in the game, tracking both the amount
    and which players are eligible to win it (for side pots).

    Attributes:
        amount (int): Total chips in the pot
        eligible_players (List[str]): IDs of players who can win

    Example:
        >>> pot = Pot(
        ...     amount=500,
        ...     eligible_players=["p1", "p2", "p3"]
        ... )
    """
    amount: int = Field(default=0, description="The amount of chips in the pot")
    eligible_players: List[str] = Field(default_factory=list, description="The players who are eligible to win the pot")

# Texas Hold'em specific
class PokerGameState(BaseModel):
    """Texas Hold'em poker game state.
    
    Comprehensive model of the current game state, including all player
    information, community cards, betting status, and game progression.

    Attributes:
        players (List[Player]): All players in the game
        active_players (List[str]): IDs of players still in hand
        dealer_position (int): Position of dealer button
        current_player_idx (int): Index of player to act
        community_cards (List[Card]): Shared cards on board
        deck (List[Card]): Remaining cards in deck
        phase (GamePhase): Current game phase
        pots (List[Pot]): Main pot and side pots
        current_bet (int): Amount to call
        small_blind (int): Small blind amount
        big_blind (int): Big blind amount
        min_raise (int): Minimum raise amount
        action_history (List[ActionRecord]): Record of all actions
        last_aggressor (Optional[str]): ID of last betting/raising player
        hand_rankings (Dict[str, HandRanking]): Final hand evaluations
        winners (List[str]): IDs of hand winners
        round_complete (bool): Whether betting round is finished

    Example:
        >>> state = PokerGameState(
        ...     players=[Player(id="p1", name="Alice")],
        ...     small_blind=5,
        ...     big_blind=10
        ... )
    """
    players: List[Player] = Field(default_factory=list, description="The players in the game")
    active_players: List[str] = Field(default_factory=list, description="The players who are still in the game")
    dealer_position: int = Field(default=0, description="The position of the dealer")
    current_player_idx: int = Field(default=0, description="The index of the current player")    
    community_cards: List[Card] = Field(default_factory=list, max_length=5, description="The community cards on the table")
    deck: List[Card] = Field(default_factory=list, max_length=52, description="The deck of cards in the game")
    phase: GamePhase = Field(default=GamePhase.SETUP, description="The current phase of the game")
    pots: List[Pot] = Field(default_factory=lambda: [Pot()], description="The pots in the game")
    current_bet: int = Field(default=0, description="The current bet amount")
    small_blind: int = Field(default=5, description="The small blind amount")
    big_blind: int = Field(default=10, description="The big blind amount")
    min_raise: int = Field(default=10, description="The minimum raise amount")
    action_history: List[ActionRecord] = Field(default_factory=list, description="The history of actions taken by the players")
    last_aggressor: Optional[str] = Field(default=None, description="The last player to make a bet or raise")
    hand_rankings: Dict[str, HandRanking] = Field(default_factory=dict, description="The rankings of the hands of each player")
    winners: List[str] = Field(default_factory=list, description="The players who won the game")
    round_complete: bool = Field(default=False, description="Whether the current round is complete")

    @property
    def active_player_count(self) -> int:
        """Get the number of active players in the game."""
        return len(self.active_players)

    

# Player observation (what a player can see)
class PlayerObservation(BaseModel):
    """Player's view of the game state.
    
    Represents what a specific player can observe about the current game
    state, hiding information they shouldn't have access to (e.g., other
    players' hole cards).

    Attributes:
        player_id (str): ID of observing player
        hand (Hand): Player's hole cards
        chips (int): Player's chip count
        position (int): Player's position at table
        position_name (str): Name of position (e.g., "Button")
        community_cards (List[Card]): Shared cards on board
        visible_players (List[Dict[str, Any]]): Observable player info
        phase (GamePhase): Current game phase
        current_bet (int): Amount to call
        pot_sizes (List[int]): Sizes of all pots
        recent_actions (List[ActionRecord]): Recent action history
        min_raise (int): Minimum raise amount
        is_active (bool): Whether player is in hand
        is_current_player (bool): Whether it's player's turn

    Example:
        >>> obs = PlayerObservation(
        ...     player_id="p1",
        ...     hand=Hand(cards=[ace_of_spades, king_of_hearts]),
        ...     position=0,
        ...     position_name="Button"
        ... )
    """
    player_id: str = Field(description="The unique identifier for the player")
    hand: Hand = Field(description="The cards the player has in their hand")
    chips: int = Field(description="The number of chips the player has")
    position: int = Field(description="The position of the player in the game")
    position_name: str = Field(description="The name of the player's position")
    community_cards: List[Card] = Field(description="The community cards on the table")
    visible_players: List[Dict[str, Any]] = Field(description="The players that are still in the game")
    phase: GamePhase = Field(description="The current phase of the game")
    current_bet: int = Field(description="The current bet amount")
    pot_sizes: List[int] = Field(description="The sizes of the pots in the game")
    recent_actions: List[ActionRecord] = Field(description="The recent actions taken by the players")
    min_raise: int = Field(description="The minimum raise amount for the current bet")
    is_active: bool = Field(description="Whether the player is still in the game")
    is_current_player: bool = Field(description="Whether the player is the current player")

# Agent decision

class AgentDecision(BaseModel):
    """Agent's decision in the game.
    
    Represents a decision made by an AI agent, including the action,
    bet amount (if any), and reasoning behind the decision.

    Attributes:
        action (PlayerAction): Chosen action
        amount (int): Bet/raise amount if applicable
        reasoning (str): Explanation of decision

    Example:
        >>> decision = AgentDecision(
        ...     action=PlayerAction.RAISE,
        ...     amount=100,
        ...     reasoning="Strong hand, building pot"
        ... )
        >>> print(decision)  # Shows decision details
    """
    action: PlayerAction = Field(description="The action the player is taking")
    amount: int = Field(default=0, description="The amount of chips the player is betting or raising")
    reasoning: str = Field(description="The reasoning behind the player's decision")

    def __str__(self):
        """String representation of the decision."""
        return f"Decision: {self.action.value} (${self.amount}) - {self.reasoning}"

# Agent decision schema
class AgentDecisionSchema(BaseModel):
    """Schema for LLM decision output.
    
    Defines the expected structure for decisions generated by the language
    model, ensuring consistent and valid output format.

    Attributes:
        action (PlayerAction): Type of action to take
        amount (int): Chips to bet/raise
        reasoning (str): Explanation of decision

    Example:
        >>> schema = AgentDecisionSchema(
        ...     action=PlayerAction.CALL,
        ...     amount=50,
        ...     reasoning="Good pot odds with drawing hand"
        ... )
    """
    action: PlayerAction = Field(description="The action taken by the player")
    amount: int = Field(default=0, description="Amount of chips for bet/raise")
    reasoning: str = Field(description="The reasoning behind the decision")

    class Config:
        json_schema_extra= {
            "example": {
                "action": "raise",
                "amount": 100,
                "reasoning": "Raising to build the pot with a strong hand"
            }
        }

# Game result for record-keeping
class GameResult(BaseModel):
    """Poker game result record.
    
    Stores the final outcome of a completed game, including winners,
    chip counts, and hand rankings.

    Attributes:
        winners (List[str]): IDs of winning players
        final_chips (Dict[str, int]): Final chip counts by player
        hand_rankings (Dict[str, HandRanking]): Final hand evaluations
        total_hands_played (int): Number of hands completed

    Example:
        >>> result = GameResult(
        ...     winners=["p1"],
        ...     final_chips={"p1": 2000, "p2": 0},
        ...     hand_rankings={"p1": ace_high_flush},
        ...     total_hands_played=1
        ... )
    """
    winners: List[str] = Field(description="The players who won the game")
    final_chips: Dict[str, int] = Field(description="The final number of chips each player has")
    hand_rankings: Dict[str, HandRanking] = Field(description="The rankings of the hands of each player")   
    total_hands_played: int = Field(description="The total number of hands played in the game")
