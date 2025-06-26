# Haive Games: Poker Module

## Overview

The Poker module provides a comprehensive implementation of Texas Hold'em poker for AI agents. It features complete game state management, hand evaluation, betting logic, and strategic decision-making through LLM-based agents. This module enables AI agents to play realistic poker games with reasoning about probabilities, bluffing, and opponent modeling.

## Key Features

- **Complete Texas Hold'em Rules**: Fully implemented poker rules including betting rounds, hand evaluation, and showdown logic
- **Multi-Agent Support**: Designed for multiple players with different strategies
- **State Management**: Comprehensive game state tracking with full history
- **LLM-Based Decision Making**: Sophisticated agent reasoning for poker strategy
- **Betting Logic**: Complete betting system with raises, calls, checks, and folds
- **Hand Evaluation**: Accurate poker hand ranking and comparison
- **Visualization**: Tools for rendering game state and player actions
- **Configurable Parameters**: Adjustable blinds, stack sizes, and game variants

## Installation

This module is part of the `haive-games` package. Install the full package with:

```bash
pip install haive-games
```

## Quick Start

```python
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure the game
config = PokerAgentConfig(
    player_names=["Alice", "Bob", "Charlie", "Dave"],
    starting_chips=1000,
    small_blind=5,
    big_blind=10,
    llm_config=AugLLMConfig(
        system_message="You are playing Texas Hold'em poker. Make strategic decisions based on your cards, the community cards, and betting patterns.",
        temperature=0.7  # Higher temperature for more varied play styles
    )
)

# Create and run the game
agent = PokerAgent(config)
result = agent.run()

# View results
print(f"Winner: {result.winner}")
print(f"Final chip counts: {result.chip_counts}")
print(f"Hands played: {result.num_hands}")
```

## Components

### PokerAgent

Main agent class that orchestrates the poker game.

```python
from haive.games.poker import PokerAgent, PokerAgentConfig

# Create a custom configuration
config = PokerAgentConfig(
    player_names=["Player 1", "Player 2", "Player 3", "Player 4"],
    starting_chips=1000,
    small_blind=5,
    big_blind=10,
    max_raises=3,
    hand_limit=20
)

# Create the agent
agent = PokerAgent(config)

# Run a full game
result = agent.run()
```

### PokerState

Game state representation for poker.

```python
from haive.games.poker import PokerState, Card, Player

# Examine a game state
state = PokerState(
    players=[
        Player(id="p1", name="Alice", chips=950, hand=[Card("Ah"), Card("Kh")], is_active=True),
        Player(id="p2", name="Bob", chips=1050, hand=[Card("Jc"), Card("Jd")], is_active=True),
    ],
    community_cards=[Card("Qh"), Card("Th"), Card("2s")],
    pot=100,
    current_player_idx=0,
    dealer_idx=1,
    phase="flop",
    min_bet=20
)

# Check if a player has a flush draw
has_flush_draw = state.players[0].has_flush_draw(state.community_cards)
```

### PokerStateManager

Handles game logic, state transitions, and rule enforcement.

```python
from haive.games.poker import PokerStateManager, PokerAgentConfig, PlayerAction

# Create a state manager
config = PokerAgentConfig(player_names=["Alice", "Bob"])
state_manager = PokerStateManager(config)

# Initialize a new hand
state = state_manager.initialize_state()

# Process a player action
action = PlayerAction(
    player_id="p1",
    action_type="raise",
    amount=40
)
new_state = state_manager.apply_action(state, action)

# Check if the hand is over
is_hand_over = state_manager.is_hand_over(new_state)
```

## Game Structure

A poker game consists of multiple hands, each following this structure:

1. **Setup**: Deal cards to players, post blinds
2. **Pre-flop**: First betting round
3. **Flop**: Deal 3 community cards, betting round
4. **Turn**: Deal 4th community card, betting round
5. **River**: Deal 5th community card, final betting round
6. **Showdown**: Compare hands and determine winner
7. **Payout**: Distribute pot to winner(s)

Each betting round follows this pattern:

1. Each active player chooses an action (fold, check, call, or raise)
2. Round continues until all active players have put the same amount in the pot
3. Move to next phase when betting is complete

## Usage Patterns

### Custom Player Decision Making

```python
from haive.games.poker import PokerAgent, PlayerObservation, AgentDecision
from haive.core.engine.aug_llm import AugLLMConfig, compose_runnable

class CustomPokerAgent(PokerAgent):
    def __init__(self, config):
        super().__init__(config)

        # Create specialized decision engines
        self.tight_engine = compose_runnable(AugLLMConfig(
            system_message="You are a tight-conservative poker player who only plays premium hands.",
            temperature=0.2
        ))

        self.loose_engine = compose_runnable(AugLLMConfig(
            system_message="You are a loose-aggressive poker player who bluffs frequently.",
            temperature=0.8
        ))

    def get_player_decision(self, state, player_id):
        # Create player observation
        observation = self.create_player_observation(state, player_id)

        # Choose engine based on player position
        player_idx = self.get_player_idx(state, player_id)
        if player_idx % 2 == 0:  # Even positions play tight
            engine = self.tight_engine
        else:  # Odd positions play loose
            engine = self.loose_engine

        # Get decision from engine
        response = engine.invoke(self.format_observation(observation))

        # Parse decision
        return self.parse_decision(response, observation)
```

### Custom Poker Variants

```python
from haive.games.poker import PokerStateManager, PokerState, Card

class OmahaStateManager(PokerStateManager):
    """State manager for Omaha poker variant."""

    def deal_cards(self, state):
        """Deal 4 cards to each player instead of 2."""
        new_state = state.model_copy(deep=True)
        deck = self.create_deck()

        for player in new_state.players:
            # Deal 4 cards in Omaha
            player.hand = [deck.pop() for _ in range(4)]

        return new_state

    def evaluate_hand(self, player_hand, community_cards):
        """Evaluate using Omaha rules (must use exactly 2 hole cards and 3 community)."""
        best_hand = None
        best_value = -1

        # Try all combinations of 2 hole cards
        for hole_combo in itertools.combinations(player_hand, 2):
            # Try all combinations of 3 community cards
            for comm_combo in itertools.combinations(community_cards, 3):
                # Combine to form a 5-card hand
                hand = list(hole_combo) + list(comm_combo)
                value = self.evaluate_five_card_hand(hand)

                if value > best_value:
                    best_value = value
                    best_hand = hand

        return best_hand, best_value
```

### Game Analysis and Visualization

```python
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.games.poker.ui import PokerVisualizer

# Run a game
config = PokerAgentConfig(player_names=["Alice", "Bob", "Charlie", "Dave"])
agent = PokerAgent(config)
result = agent.run()

# Create a visualizer
visualizer = PokerVisualizer()

# Generate game summary
summary = visualizer.generate_game_summary(result)
print(summary)

# Visualize a specific hand
hand_viz = visualizer.visualize_hand(result.hand_histories[0])
print(hand_viz)

# Generate statistics
stats = visualizer.generate_statistics(result)
print(f"VPIP percentages: {stats['vpip']}")
print(f"Average pot size: {stats['avg_pot_size']}")
print(f"Biggest pot: {stats['biggest_pot']}")
```

## Integration with Other Modules

### Integration with Tournament System

```python
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.games.tournament import TournamentManager

# Create tournament configuration
tournament_config = {
    "num_players": 9,
    "starting_chips": 1000,
    "blind_schedule": [
        {"level": 1, "small_blind": 5, "big_blind": 10, "duration": 20},
        {"level": 2, "small_blind": 10, "big_blind": 20, "duration": 20},
        {"level": 3, "small_blind": 25, "big_blind": 50, "duration": 20},
    ],
    "payout_structure": [0.5, 0.3, 0.2]  # 50% to 1st, 30% to 2nd, 20% to 3rd
}

# Create tournament manager
tournament = TournamentManager(
    game_class=PokerAgent,
    game_config_class=PokerAgentConfig,
    tournament_config=tournament_config
)

# Run tournament
results = tournament.run()
```

### Integration with Agent Configuration System

```python
from haive.games.poker import PokerAgent, PokerAgentConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Create different player personalities
player_personalities = [
    AugLLMConfig(
        name="tight_aggressive",
        system_message="You are a tight-aggressive poker player. You play few hands but play them strongly.",
        temperature=0.3
    ),
    AugLLMConfig(
        name="loose_passive",
        system_message="You are a loose-passive poker player. You play many hands but rarely raise.",
        temperature=0.6
    ),
    AugLLMConfig(
        name="maniac",
        system_message="You are a maniac poker player. You play almost any hand and frequently raise and re-raise.",
        temperature=0.9
    ),
    AugLLMConfig(
        name="rock",
        system_message="You are a rock poker player. You only play premium hands and fold everything else.",
        temperature=0.1
    )
]

# Create game with mixed player types
config = PokerAgentConfig(
    player_names=["Alice", "Bob", "Charlie", "Dave"],
    player_llm_configs=player_personalities,
    starting_chips=1000,
    small_blind=5,
    big_blind=10
)

# Run game with varied player types
agent = PokerAgent(config)
result = agent.run()
```

## Best Practices

- **Decision Prompting**: Design clear, structured prompts for agent decision making
- **State Observation**: Provide only information that would be available to a real player
- **Strategic Variety**: Use temperature and system messages to create varied playing styles
- **Handling Randomness**: Use consistent seed values for reproducible results in testing
- **Game Analysis**: Collect and analyze statistics to evaluate agent performance
- **Error Handling**: Implement robust handling of invalid actions
- **Visualization**: Use visualization tools to understand game flow and agent decisions

## API Reference

For full API details, see the [documentation](https://docs.haive.ai/games/poker).

## Related Modules

- **haive.games.framework**: Core framework used by the poker implementation
- **haive.games.cards**: Card utilities shared across card games
- **haive.core.engine**: Engine components used by poker agents
