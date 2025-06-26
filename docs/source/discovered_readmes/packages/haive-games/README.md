# Haive Games - AI Game Environments

## Overview

Haive Games provides 40+ game environments designed for testing, training, and benchmarking AI agents. These environments range from simple puzzles to complex strategy games, offering standardized interfaces for agent development and evaluation.

## Why Games for AI?

Games provide:

- **Controlled Environments**: Clear rules and objectives
- **Measurable Performance**: Scores, wins, efficiency metrics
- **Progressive Difficulty**: From simple to complex challenges
- **Strategy Testing**: Evaluate planning and decision-making
- **Multi-Agent Scenarios**: Competition and cooperation

## Game Categories

### 1. Classic Board Games

**Chess**

- Full chess engine with legal move validation
- Multiple difficulty levels
- Position analysis and evaluation
- Opening book and endgame tables

**Checkers**

- Standard and international rules
- Jump detection and king mechanics
- Minimax AI opponents

**Go**

- 9x9, 13x13, and 19x19 boards
- Ko rule enforcement
- Territory scoring
- Handicap system

**Reversi (Othello)**

- Strategic position evaluation
- Corner and edge strategy
- Mobility analysis

**Fox and Geese**

- Traditional asymmetric hunt game with rich terminal UI
- Fox (🦊) tries to capture geese while geese (🪿) try to trap the fox
- State management, move validation, and win condition detection
- Fixed implementation that works reliably

```bash
# Run with fixed state handling (recommended)
python src/haive/games/fox_and_geese/fixed_runner.py --delay 0.5 --debug

# Run with original implementation (requires LLM API access)
python src/haive/games/fox_and_geese/example.py
```

### 2. Strategy Games

**Risk**

- World domination gameplay
- Dice rolling mechanics
- Territory management
- Alliance formation

**Battleship**

- Ship placement strategies
- Probability-based targeting
- Pattern recognition

**Mancala**

- Capture mechanics
- Lookahead strategies
- Endgame optimization

**Connect 4**

- Column selection strategy
- Win detection
- Threat analysis

### 3. Card Games

**Poker (Texas Hold'em)**

- Betting strategies
- Hand evaluation
- Bluff detection
- Pot odds calculation

**Blackjack**

- Basic strategy implementation
- Card counting capabilities
- Betting systems
- Multiple hands support

**UNO**

- Color/number matching
- Special card handling
- Strategic card holding

**BS (Bluff)**

- Deception strategies
- Probability calculation
- Opponent modeling

### 4. Social Deduction Games

**Among Us**

- Task completion
- Impostor detection
- Voting strategies
- Information gathering

**Mafia**

- Role-based gameplay with villagers, mafia, detective and doctor roles
- Day/night cycles with phase transitions
- Social deduction mechanics
- LLM-powered decision making

```bash
# Run with fixed state handling (recommended)
python src/haive/games/mafia/fixed_runner.py --players 5 --days 1 --debug

# Run with original implementation (requires LLM API access)
python src/haive/games/mafia/example.py --players 5 --days 1 --debug
```

**Clue**

- Deductive reasoning
- Information tracking
- Hypothesis testing
- Strategic questioning

### 5. Single-Player Puzzles

**Sudoku**

- Constraint satisfaction
- Multiple difficulty levels
- Hint generation
- Solution validation

**Crossword**

- Natural language processing
- Clue interpretation
- Letter pattern matching
- Word database integration

**Wordle**

- Word guessing optimization
- Letter frequency analysis
- Pattern elimination
- Optimal guess strategies

**2048**

- Tile merging strategies
- Corner strategies
- Lookahead planning
- Score optimization

**Rubik's Cube**

- 3D manipulation
- Algorithm learning
- Pattern recognition
- Solve optimization

**Minesweeper**

- Probability calculation
- Safe move detection
- Pattern recognition
- Optimal flagging

### 6. Economic Games

**Monopoly**

- Property investment strategies
- Trading negotiations
- Cash flow management
- Risk assessment
- Auction strategies

### 7. Word Games

**Word Search**

- Pattern detection
- Efficient searching
- Direction handling

**Logic Grid Puzzles**

- Constraint satisfaction
- Clue processing
- Deduction chains

## Game Features

### Standardized Interface

```python
from haive.games import ChessGame

# All games share common interface
game = ChessGame()
state = game.reset()

while not game.is_terminal():
    actions = game.get_legal_actions()
    action = agent.select_action(state, actions)
    state, reward, done = game.step(action)
```

### Multi-Agent Support

```python
from haive.games import PokerGame

game = PokerGame(num_players=4)
game.add_agent(agent1, position=0)
game.add_agent(agent2, position=1)
game.add_agent(human_player, position=2)
game.add_agent(agent3, position=3)

results = game.play_full_game()
```

### Visualization

```python
# Built-in visualization for all games
game.render()  # Console output
game.render_gui()  # Graphical interface
game.save_replay("game_replay.json")
```

### Metrics & Analysis

```python
from haive.games.metrics import GameAnalyzer

analyzer = GameAnalyzer(game)
stats = analyzer.analyze_game()
# Returns: win rate, average score, decision time, etc.
```

## Agent Development

### Basic Game Agent

```python
from haive.games.base import GameAgent

class MyChessAgent(GameAgent):
    def select_action(self, state, legal_actions):
        # Your strategy here
        return self.evaluate_best_move(state, legal_actions)
```

### Learning Agents

```python
from haive.games.learners import RLGameAgent

# Reinforcement learning agent
agent = RLGameAgent(
    game_type="chess",
    algorithm="ppo",
    training_episodes=10000
)
```

### Tournament System

```python
from haive.games.tournament import Tournament

tournament = Tournament(
    game="poker",
    participants=[agent1, agent2, agent3, agent4],
    rounds=100
)

results = tournament.run()
```

## Benchmarking

### Performance Metrics

- **Win Rate**: Against various opponents
- **ELO Rating**: Skill level estimation
- **Decision Time**: Speed of play
- **Strategy Diversity**: Move variety
- **Learning Curve**: Improvement over time

### Leaderboards

```python
from haive.games.leaderboard import GlobalLeaderboard

leaderboard = GlobalLeaderboard("chess")
leaderboard.submit_agent(your_agent)
ranking = leaderboard.get_ranking()
```

## Advanced Features

### Game Variants

```python
# Many games support variants
game = ChessGame(variant="chess960")  # Fischer Random
game = PokerGame(variant="omaha")
game = CheckersGame(variant="international")
```

### Difficulty Scaling

```python
# Adaptive difficulty
game = SudokuGame(difficulty="adaptive")
game.adjust_to_player_skill(agent)
```

### State Serialization

```python
# Save and restore game states
state = game.get_state()
saved_state = game.serialize_state()

# Later...
game.load_state(saved_state)
```

### Parallel Games

```python
from haive.games import ParallelGameRunner

runner = ParallelGameRunner()
results = runner.run_many([
    (ChessGame(), agent1, agent2),
    (GoGame(), agent3, agent4),
    (PokerGame(), [agent5, agent6, agent7])
])
```

## Use Cases

### 1. Agent Testing

- Benchmark new algorithms
- Compare strategies
- Identify weaknesses

### 2. Research

- Study emergent behaviors
- Test game theory concepts
- Explore multi-agent dynamics

### 3. Education

- Teach AI concepts
- Demonstrate strategies
- Interactive learning

### 4. Competition

- Agent tournaments
- Skill progression
- Community challenges

## Getting Started

```python
from haive.games import GameEnvironment, available_games

# List all available games
print(available_games())

# Create any game
game = GameEnvironment.create("chess")

# Or use specific game class
from haive.games.chess import ChessGame
game = ChessGame()

# Play with your agent
from haive.agents import SimpleAgent
agent = SimpleAgent()

game.play_against(agent)
```

## Best Practices

1. **Start Simple**: Begin with tic-tac-toe or connect4
2. **Use Provided Baselines**: Compare against included AI
3. **Log Everything**: Built-in game logging
4. **Test Robustness**: Try edge cases
5. **Measure Consistently**: Use standard metrics
6. **Share Results**: Contribute to leaderboards

_Note: Each game includes tutorials, strategy guides, and example agents. Games are optimized for both learning and high-performance agent development._
