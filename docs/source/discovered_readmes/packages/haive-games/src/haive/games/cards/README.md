# Haive Games: Cards Module

## Overview

The Cards module provides a comprehensive foundation for card-based games within the Haive framework. It includes implementations of common card types, decks, and game mechanics that can be shared across various card games like Poker, Blackjack, and Bridge. This module serves as both a standalone utility for card manipulation and as a building block for more complex card game implementations.

## Key Features

- **Standard Card Deck**: Full implementation of standard 52-card deck with optional jokers
- **Card Representation**: Flexible card objects with suit, rank, and value properties
- **Deck Operations**: Shuffling, drawing, dealing, and deck management
- **Hand Evaluation**: Card combination evaluation for various game types
- **Specialized Decks**: Support for non-standard decks and custom card types
- **Serialization**: JSON serialization for game state persistence
- **Visualization**: Text and Unicode representations of cards and hands

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.cards import Deck, Card, Hand

# Create a standard deck
deck = Deck.standard_deck()

# Shuffle the deck
deck.shuffle()

# Deal a poker hand
poker_hand = Hand([deck.draw() for _ in range(5)])

# Check for a flush
has_flush = poker_hand.is_flush()

# Display the hand
print(poker_hand)  # "A` K` Q` J` 10`"

# Evaluate poker hand
hand_type, hand_value = poker_hand.evaluate_poker()
print(f"Hand type: {hand_type}")  # "Hand type: ROYAL_FLUSH"
```

## Components

### Card

Represents a single playing card with rank, suit, and value.

```python
from haive.games.cards import Card, Suit, Rank

# Create cards
ace_of_spades = Card(rank=Rank.ACE, suit=Suit.SPADES)
ten_of_hearts = Card(rank=Rank.TEN, suit=Suit.HEARTS)

# Compare cards
is_higher = ace_of_spades > ten_of_hearts  # True

# Card properties
print(ace_of_spades.rank)  # Rank.ACE
print(ace_of_spades.suit)  # Suit.SPADES
print(ace_of_spades.value)  # 14 (numeric value for comparisons)

# String representation
print(str(ace_of_spades))  # "A`"
print(ace_of_spades.long_name)  # "Ace of Spades"
```

### Deck

Collection of cards with operations for manipulation.

```python
from haive.games.cards import Deck, Card

# Create a standard 52-card deck
deck = Deck.standard_deck()

# Shuffle the deck
deck.shuffle()

# Draw a card
card = deck.draw()
print(card)  # "Ke" (or any random card)

# Check remaining cards
print(len(deck))  # 51

# Peek at top card without drawing
top_card = deck.peek()

# Deal multiple cards
hand = deck.deal(5)
print(hand)  # [Card, Card, Card, Card, Card]

# Reset and reshuffle
deck.reset()
deck.shuffle()
print(len(deck))  # 52 again
```

### Hand

Collection of cards held by a player with evaluation logic.

```python
from haive.games.cards import Hand, Card, Suit, Rank

# Create a hand
hand = Hand([
    Card(Rank.ACE, Suit.SPADES),
    Card(Rank.KING, Suit.SPADES),
    Card(Rank.QUEEN, Suit.SPADES),
    Card(Rank.JACK, Suit.SPADES),
    Card(Rank.TEN, Suit.SPADES)
])

# Evaluate the hand
hand_type, hand_value = hand.evaluate_poker()
print(hand_type)  # "ROYAL_FLUSH"

# Sort the hand
hand.sort()
print(hand)  # "10` J` Q` K` A`"

# Check for specific combinations
is_flush = hand.is_flush()  # True
is_straight = hand.is_straight()  # True
is_full_house = hand.is_full_house()  # False

# Add card to hand
hand.add_card(Card(Rank.NINE, Suit.SPADES))
print(len(hand))  # 6
```

### SpecializedDeck

Customized deck implementations for various card games.

```python
from haive.games.cards import SpecializedDeck, Card, Suit, Rank

# Create a Euchre deck (9-A in 4 suits)
euchre_deck = SpecializedDeck.euchre_deck()
print(len(euchre_deck))  # 24

# Create a Pinochle deck (9-A in 4 suits, duplicated)
pinochle_deck = SpecializedDeck.pinochle_deck()
print(len(pinochle_deck))  # 48

# Create a Tarot deck
tarot_deck = SpecializedDeck.tarot_deck()
print(len(tarot_deck))  # 78

# Create a custom deck
custom_ranks = [Rank.ACE, Rank.KING, Rank.QUEEN]
custom_suits = [Suit.HEARTS, Suit.DIAMONDS]
custom_deck = SpecializedDeck.custom_deck(ranks=custom_ranks, suits=custom_suits)
print(len(custom_deck))  # 6
```

## Usage Patterns

### Poker Hand Evaluation

```python
from haive.games.cards import Deck, Hand, PokerHandType

# Create a deck and draw a poker hand
deck = Deck.standard_deck()
deck.shuffle()
hand = Hand([deck.draw() for _ in range(5)])

# Evaluate the poker hand
hand_type, hand_value = hand.evaluate_poker()

# Check for specific hand types
if hand_type == PokerHandType.STRAIGHT_FLUSH:
    print("Straight flush!")
elif hand_type == PokerHandType.FOUR_OF_A_KIND:
    print("Four of a kind!")
# ...and so on

# Compare two poker hands
other_hand = Hand([deck.draw() for _ in range(5)])
other_type, other_value = other_hand.evaluate_poker()

if hand_value > other_value:
    print("First hand wins!")
elif hand_value < other_value:
    print("Second hand wins!")
else:
    print("It's a tie!")
```

### Card Game Implementation

```python
from haive.games.cards import Deck, Hand, Card
from haive.games.framework import GameState, GameAgent
from typing import List
from pydantic import Field

# Define game state
class BlackjackState(GameState):
    dealer_hand: Hand = Field(default_factory=Hand)
    player_hands: List[Hand] = Field(default_factory=list)
    deck: Deck = Field(default_factory=Deck.standard_deck)
    current_player: int = Field(default=0)
    phase: str = Field(default="betting")  # betting, player_turn, dealer_turn, payout

    def hand_value(self, hand: Hand) -> int:
        """Calculate the value of a blackjack hand."""
        value = sum(card.blackjack_value() for card in hand.cards)
        # Handle aces
        ace_count = sum(1 for card in hand.cards if card.rank == Rank.ACE)
        while value > 21 and ace_count > 0:
            value -= 10  # Change an ace from 11 to 1
            ace_count -= 1
        return value

    def is_bust(self, hand: Hand) -> bool:
        """Check if a hand is bust (over 21)."""
        return self.hand_value(hand) > 21

    def is_blackjack(self, hand: Hand) -> bool:
        """Check if a hand is a blackjack."""
        return len(hand) == 2 and self.hand_value(hand) == 21

# Create a blackjack agent
class BlackjackAgent(GameAgent):
    def initialize_game(self):
        # Create initial state
        state = BlackjackState()

        # Shuffle the deck
        state.deck.shuffle()

        # Deal initial cards
        state.player_hands = [Hand([state.deck.draw(), state.deck.draw()])]
        state.dealer_hand = Hand([state.deck.draw(), state.deck.draw()])

        return state

    def player_turn(self, state):
        # Get player decision (hit or stand)
        decision = self.get_player_decision(state)

        # Process decision
        if decision == "hit":
            # Deal another card
            card = state.deck.draw()
            state.player_hands[state.current_player].add_card(card)

            # Check for bust
            if state.is_bust(state.player_hands[state.current_player]):
                # Move to next player or dealer turn
                state.current_player += 1
                if state.current_player >= len(state.player_hands):
                    state.phase = "dealer_turn"
        else:  # stand
            # Move to next player or dealer turn
            state.current_player += 1
            if state.current_player >= len(state.player_hands):
                state.phase = "dealer_turn"

        return state
```

### Custom Card Representations

```python
from haive.games.cards import Card, Suit, Rank

# Create a custom card renderer
class CardRenderer:
    def __init__(self, unicode=True, color=True):
        self.unicode = unicode
        self.color = color

    def render_card(self, card: Card) -> str:
        """Render a card as a string with optional Unicode and color."""
        if not self.unicode:
            # ASCII representation
            rank_str = str(card.rank.value) if card.rank.value <= 10 else card.rank.name[0]
            suit_str = card.suit.name[0]
            return f"{rank_str}{suit_str}"

        # Unicode representation
        rank_symbol = {
            Rank.ACE: "A",
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "10",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K"
        }[card.rank]

        suit_symbol = {
            Suit.SPADES: "`",
            Suit.HEARTS: "e",
            Suit.DIAMONDS: "f",
            Suit.CLUBS: "c"
        }[card.suit]

        if not self.color:
            return f"{rank_symbol}{suit_symbol}"

        # Add color
        color_code = "\033[30m"  # Black
        if card.suit in [Suit.HEARTS, Suit.DIAMONDS]:
            color_code = "\033[31m"  # Red

        reset_code = "\033[0m"
        return f"{color_code}{rank_symbol}{suit_symbol}{reset_code}"

    def render_hand(self, hand, delimiter=" "):
        """Render a full hand with the given delimiter."""
        return delimiter.join(self.render_card(card) for card in hand)

# Use the renderer
renderer = CardRenderer(unicode=True, color=True)
hand = Hand([
    Card(Rank.ACE, Suit.HEARTS),
    Card(Rank.KING, Suit.CLUBS),
    Card(Rank.QUEEN, Suit.DIAMONDS)
])

print(renderer.render_hand(hand))  # Colored Unicode representation
```

## Google-Style Docstrings

Here are examples of Google-style docstrings used in the module:

```python
def evaluate_poker(self) -> Tuple[PokerHandType, int]:
    """Evaluates a 5-card poker hand.

    Determines the best poker hand type and a numerical value for comparison.
    Hand must contain exactly 5 cards for standard poker hand evaluation.

    Returns:
        A tuple containing:
            - The poker hand type (PokerHandType enum)
            - A numerical value for comparison (higher is better)

    Raises:
        ValueError: If the hand does not contain exactly 5 cards.

    Examples:
        >>> hand = Hand([
        ...     Card(Rank.ACE, Suit.SPADES),
        ...     Card(Rank.KING, Suit.SPADES),
        ...     Card(Rank.QUEEN, Suit.SPADES),
        ...     Card(Rank.JACK, Suit.SPADES),
        ...     Card(Rank.TEN, Suit.SPADES)
        ... ])
        >>> hand_type, value = hand.evaluate_poker()
        >>> hand_type
        PokerHandType.ROYAL_FLUSH
        >>> value
        9000  # Base value for royal flush
    """
    # Implementation...
```

```python
class Deck:
    """A collection of playing cards with standard deck operations.

    This class represents a deck of playing cards with operations for
    shuffling, drawing, dealing, and managing cards. It can be used to
    create standard 52-card decks or customized decks for specific games.

    Attributes:
        cards: List of Card objects in the deck.
        original_cards: A copy of the initial cards for resetting.

    Examples:
        >>> deck = Deck.standard_deck()
        >>> deck.shuffle()
        >>> hand = deck.deal(5)
        >>> print(len(deck))
        47
    """

    def __init__(self, cards: List[Card] = None):
        """Initializes a Deck with optional initial cards.

        Args:
            cards: Optional list of cards to initialize the deck with.
                  If None, an empty deck is created.
        """
        # Implementation...

    def shuffle(self, seed: Optional[int] = None) -> None:
        """Shuffles the cards in the deck.

        Args:
            seed: Optional random seed for reproducible shuffling.

        Examples:
            >>> deck = Deck.standard_deck()
            >>> deck.shuffle(seed=42)  # Reproducible shuffle
        """
        # Implementation...
```

## Integration with Other Modules

### Integration with Poker Module

```python
from haive.games.cards import Deck, Card, Hand
from haive.games.poker import PokerStateManager, PokerConfig, PokerPhase

# Create a poker state manager
config = PokerConfig(
    player_names=["Alice", "Bob", "Charlie", "Dave"],
    starting_chips=1000,
    small_blind=5,
    big_blind=10
)
state_manager = PokerStateManager(config)

# Initialize poker state
state = state_manager.initialize_state()

# Use the cards module to manage the deck and deal cards
deck = Deck.standard_deck()
deck.shuffle()

# Deal hole cards to players
for player in state.players:
    player.hand = Hand([deck.draw(), deck.draw()])

# Deal community cards based on game phase
if state.phase == PokerPhase.FLOP:
    state.community_cards = [deck.draw() for _ in range(3)]
elif state.phase == PokerPhase.TURN:
    state.community_cards.append(deck.draw())
elif state.phase == PokerPhase.RIVER:
    state.community_cards.append(deck.draw())

# Evaluate hands at showdown
if state.phase == PokerPhase.SHOWDOWN:
    for player in state.players:
        combined_hand = Hand(player.hand.cards + state.community_cards)
        player.hand_type, player.hand_value = combined_hand.evaluate_poker()
```

### Integration with AI Decision Making

```python
from haive.games.cards import Hand, Card, Rank, Suit
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

# Create a poker hand evaluator engine
poker_engine = compose_runnable(AugLLMConfig(
    system_message="""
    You are a poker hand analyzer. Evaluate poker hands and provide strategic advice
    based on the cards, community cards, position, and betting history.
    """,
    temperature=0.2
))

# Example hand evaluation
hole_cards = Hand([Card(Rank.ACE, Suit.HEARTS), Card(Rank.ACE, Suit.SPADES)])
community_cards = Hand([
    Card(Rank.KING, Suit.HEARTS),
    Card(Rank.QUEEN, Suit.HEARTS),
    Card(Rank.JACK, Suit.DIAMONDS)
])

# Generate evaluation prompt
prompt = f"""
Your hole cards: {hole_cards}
Community cards: {community_cards}
Position: Button
Players remaining: 3
Pot size: 150 chips
Your stack: 850 chips

What is your hand strength and what action would you recommend?
"""

# Get analysis from the LLM
analysis = poker_engine.invoke(prompt)
print(analysis)
```

## Best Practices

- **Card Immutability**: Keep Card objects immutable to prevent state inconsistencies
- **Random Seeding**: Use explicit random seeds during testing for reproducibility
- **Hand Validation**: Validate hand sizes for game-specific evaluations
- **Consistent Comparisons**: Ensure consistent comparison semantics across card games
- **Efficient Evaluation**: Optimize hand evaluation algorithms for performance
- **Clear Representations**: Provide clear string representations for debugging
- **Customization Support**: Design for extensibility with game-specific card behaviors

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/cards).

## Related Modules

- **haive.games.poker**: Texas Hold'em implementation using the cards module
- **haive.games.blackjack**: Blackjack implementation using the cards module
- **haive.games.framework**: Core framework integrated with card game implementations
