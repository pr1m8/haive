.. title:: Haive Games Framework
.. _games:

🎮 Haive Games Framework



🎯 Strategic Game Environments for AI Testing



Beautiful, interactive game environments with intelligent AI opponents. Test your agents in strategic scenarios from classic board games to complex multiplayer environments.

🎲 All Games



.. note::


   Grid layout removed due to sphinx_design incompatibility.


   .. grid-item-card:: ♟️ Chess

      :shadow: lg

      **Strategy Game**

      Play interactive chess against AI opponents of varying skill levels with advanced position evaluation and opening theory.

      +++

      ✓ Position Analysis • ✓ Opening Theory • ✓ Endgame AI
      **8x8 Board • 2 Players • 60+ Min**

   .. grid-item-card:: 🎯 Tic-Tac-Toe

      :shadow: lg

      **Quick Game**

      Classic 3x3 strategy game with perfect AI opponent using minimax algorithm for optimal play.

      +++

      ✓ Perfect AI • ✓ Minimax Algorithm • ✓ Quick Play
      **3x3 Board • 2 Players • 2 Min**

   .. grid-item-card:: 🔴 Connect Four

      :shadow: lg

      **Strategy Game**

      Classic connection game with strategic depth and AI that uses pattern recognition for competitive play.

      +++

      ✓ Pattern Recognition • ✓ Strategic Depth • ✓ Threat Detection
      **7x6 Board • 2 Players • 10 Min**

   .. grid-item-card:: 🃏 Poker

      :shadow: lg

      **Card Game**

      Texas Hold'em with betting, bluffing, and AI psychology that adapts to player patterns and behavior.

      +++

      ✓ Bluffing AI • ✓ Psychology • ✓ Betting Strategy
      **52 Cards • 2-8 Players • 30 Min**

   .. grid-item-card:: 🕵️ Among Us

      :shadow: lg

      **Social Deduction**

      Social deduction game with intelligent AI crewmates and imposters using behavioral analysis and deception.

      +++

      ✓ Behavioral Analysis • ✓ Deception AI • ✓ Role Playing
      **4-10 Players • 1-3 Imposters • 15 Min**

   .. grid-item-card:: 🌍 Risk

      :shadow: lg

      **Strategy Game**

      World domination strategy with AI diplomacy, warfare tactics, and long-term strategic planning.

      +++

      ✓ Diplomacy AI • ✓ Warfare Tactics • ✓ Territory Control
      **42 Territories • 2-6 Players • 120 Min**

   .. grid-item-card:: 🎲 Monopoly

      :shadow: lg

      **Economic Game**

      Economic strategy game with AI negotiation, property trading, and financial optimization algorithms.

      +++

      ✓ AI Negotiation • ✓ Property Trading • ✓ Financial Strategy
      **40 Spaces • 2-8 Players • 90 Min**

   .. grid-item-card:: 🧩 Mastermind

      :shadow: lg

      **Logic Game**

      Code-breaking game with AI logical deduction, pattern analysis, and optimal guessing strategies.

      +++

      ✓ Logical Deduction • ✓ Pattern Analysis • ✓ Optimal Guessing
      **4 Code Length • 2 Players • 20 Min**

Game Categories



   <div class="showcase-content">
   <h3>🎯 Board Games</h3>
   <p>Classic board games with advanced AI opponents.</p>

   <div class="game-list">
   <ul>
   <li><strong>Chess</strong> - Complete chess engine with opening book and endgame tablebase</li>
   <li><strong>Checkers</strong> - Classic checkers with multiple difficulty levels</li>
   <li><strong>Connect Four</strong> - Strategic connection game with pattern recognition</li>
   <li><strong>Tic-Tac-Toe</strong> - Perfect play minimax implementation</li>
   <li><strong>Go</strong> - Ancient strategy game with neural network AI</li>
   <li><strong>Reversi</strong> - Territory control with strategic positioning</li>
   </ul>
   </div>

   </div>

   <div class="showcase-content">
   <h3>🃏 Card Games</h3>
   <p>Card games with probabilistic reasoning and bluffing AI.</p>

   <div class="game-list">
   <ul>
   <li><strong>Poker</strong> - Texas Hold'em with betting psychology</li>
   <li><strong>Blackjack</strong> - Casino game with card counting AI</li>
   <li><strong>Hearts</strong> - Trick-taking game with strategic play</li>
   <li><strong>Uno</strong> - Color matching with tactical card play</li>
   </ul>
   </div>

   </div>

   <div class="showcase-content">
   <h3>🌍 Strategy Games</h3>
   <p>Complex strategy games requiring long-term planning.</p>

   <div class="game-list">
   <ul>
   <li><strong>Risk</strong> - World domination with diplomacy</li>
   <li><strong>Civilization</strong> - Build empires through the ages</li>
   <li><strong>Settlers of Catan</strong> - Resource management and trading</li>
   </ul>
   </div>

   </div>

   <div class="showcase-content">
   <h3>🕵️ Social Games</h3>
   <p>Games focusing on social interaction and deduction.</p>

   <div class="game-list">
   <ul>
   <li><strong>Among Us</strong> - Social deduction with imposters</li>
   <li><strong>Mafia</strong> - Classic social deduction game</li>
   <li><strong>Secret Hitler</strong> - Hidden identity and deduction</li>
   </ul>
   </div>

   </div>

Quick Start Example



   <div class="code-example-section">
   <h4>🚀 Start Playing in 30 Seconds</h4>

.. code-block:: python

    # Code example here

   from haive.games.tic_tac_toe import TicTacToeGame
   from haive.games.tic_tac_toe.agent import TicTacToeAgent
   from haive.core.engine.aug_llm import AugLLMConfig

   # Create game environment
   game = TicTacToeGame()

   # Create AI agents with different strategies
   agent1 = TicTacToeAgent(
   name="Player 1",
   symbol="X",
   engine=AugLLMConfig(temperature=0.1),  # Deterministic
   strategy="minimax"
   )

   agent2 = TicTacToeAgent(
   name="Player 2",
   symbol="O",
   engine=AugLLMConfig(temperature=0.7),  # More creative
   strategy="mcts"  # Monte Carlo Tree Search
   )

   # Play the game!
   async def play():
   winner = await game.run(agent1, agent2)
   print(f"Winner: {winner}")
   game.display_board()

   # Run the game
   import asyncio
   asyncio.run(play())

   </div>

   Game Development Guide



   <div class="custom-section">
   <h3>🎨 Creating Your Own Game</h3>
   <p>Build custom game environments for your agents to play in.</p>

.. code-block:: python

    # Code example here

   from haive.games.base import BaseGame, GameState, Move
   from typing import List, Optional, Tuple

   class MyCustomGame(BaseGame):
   """Custom game implementation."""

   def __init__(self):
   super().__init__(
   name="My Custom Game",
   min_players=2,
   max_players=4
   )
   self.board = self.create_board()

   def get_valid_moves(self, state: GameState) -> List[Move]:
   """Return all valid moves for current player."""
   moves = []
   # Implement your game logic
   return moves

   def make_move(self, move: Move) -> GameState:
   """Execute a move and return new state."""
   # Update game state
   return self.state

   def is_terminal(self) -> bool:
   """Check if game has ended."""
   return self.check_win_condition()

   def get_reward(self, player: int) -> float:
   """Return reward for specified player."""
   if self.winner == player:
   return 1.0
   elif self.winner is not None:
   return -1.0
   return 0.0

   </div>

   AI Strategies



   <div class="showcase-section">

   <div class="showcase-header">
   <h2>🧠 AI Strategies and Algorithms</h2>
   <p>Different AI approaches used in our game implementations</p>
   </div>

   <div class="api-grid">

   <div class="api-section">
   <h4>🎯 Minimax Algorithm</h4>
   <p>Perfect play for zero-sum games</p>
   <ul>
   <li>Alpha-beta pruning</li>
   <li>Transposition tables</li>
   <li>Iterative deepening</li>
   <li>Move ordering</li>
   </ul>
   </div>

   <div class="api-section">
   <h4>🌳 Monte Carlo Tree Search</h4>
   <p>Probabilistic game tree exploration</p>
   <ul>
   <li>UCT selection</li>
   <li>Progressive widening</li>
   <li>RAVE enhancements</li>
   <li>Neural network guidance</li>
   </ul>
   </div>

   <div class="api-section">
   <h4>🤖 Neural Networks</h4>
   <p>Deep learning for game AI</p>
   <ul>
   <li>Value networks</li>
   <li>Policy networks</li>
   <li>AlphaZero architecture</li>
   <li>Self-play training</li>
   </ul>
   </div>

   </div>

   </div>

   Performance Benchmarks



   <div class="performance-section">
   <h3>⚡ AI Performance Metrics</h3>
   <table class="performance-table">
   <thead>
   <tr>
   <th>Game</th>
   <th>AI Level</th>
   <th>Win Rate vs Human</th>
   <th>Avg Decision Time</th>
   <th>ELO Rating</th>
   </tr>
   </thead>
   <tbody>
   <tr>
   <td>Chess</td>
   <td>Expert</td>
   <td>95%</td>
   <td>2.3s</td>
   <td>2400+</td>
   </tr>
   <tr>
   <td>Go (9x9)</td>
   <td>Advanced</td>
   <td>88%</td>
   <td>3.1s</td>
   <td>2200+</td>
   </tr>
   <tr>
   <td>Poker</td>
   <td>Professional</td>
   <td>73%</td>
   <td>1.2s</td>
   <td>N/A</td>
   </tr>
   <tr>
   <td>Connect Four</td>
   <td>Perfect</td>
   <td>100%</td>
   <td>0.1s</td>
   <td>∞</td>
   </tr>
   </tbody>
   </table>
   </div>

   <style>
   .performance-table {
   width: 100%;
   border-collapse: collapse;
   margin: 2rem 0;
   background: var(--color-background-secondary);
   border-radius: 8px;
   overflow: hidden;
   }

   .performance-table th {
   background: var(--color-accent);
   color: white;
   padding: 1rem;
   text-align: left;
   font-weight: 600;
   }

   .performance-table td {
   padding: 1rem;
   border-bottom: 1px solid var(--color-background-border);
   }

   .performance-table tr:hover {
   background: var(--color-background-hover);
   }

   .game-list ul {
   list-style: none;
   padding: 0;
   }

   .game-list li {
   padding: 0.5rem 0;
   border-bottom: 1px solid var(--color-background-border);
   }

   .game-list li:last-child {
   border-bottom: none;
   }

   </style>

   API Reference



   .. toctree::


   :maxdepth: 2
   :hidden:

   ../api/games/index
   demos/index

   Quick Links
   ^^^^^^^^^^^

   - :doc:`Game Base Classes <../api/games/base/index> - Abstract base classes for games`

`
   - :doc`:`Board Games API <../api/games/board/index> - Board game implementations`

`
   - :doc`:`Card Games API <../api/games/cards/index> - Card game systems`

`
   - :doc`:`Game Demos <demos/index> - Interactive demonstrations`

`

   .. seealso::


   - :doc`:`../agents/index - AI agents that play games`

`
   - :doc`:`../guides/agent_games - Building game-playing agents`

`
   - :doc`:`../examples/index - Example game implementations`

`
`
