# Cards Agent Examples

Real examples and outputs from the cards agent.

## cards_README

**Source**: `packages/haive-games/src/haive/games/cards/README.md`

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
print(ace_of_spades.r

... (truncated)


---

