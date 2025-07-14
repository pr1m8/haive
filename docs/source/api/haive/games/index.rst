Haive Games
===========

Comprehensive game environments for AI agents with LLM integration.

.. grid:: 1 2 2 3
   :gutter: 3

   .. grid-item-card:: 🎯 **Board Games**
      :link: board_games
      :link-type: doc
      
      Chess, Checkers, Go, Reversi
      
   .. grid-item-card:: 🃏 **Card Games**
      :link: card_games
      :link-type: doc
      
      Poker, Blackjack, UNO
      
   .. grid-item-card:: 🧩 **Puzzle Games**
      :link: puzzle_games
      :link-type: doc
      
      Sudoku, Wordle, 2048
      
   .. grid-item-card:: 🎭 **Social Deduction**
      :link: social_games
      :link-type: doc
      
      Mafia, Among Us, Clue
      
   .. grid-item-card:: 🏰 **Strategy Games**
      :link: strategy_games
      :link-type: doc
      
      Risk, Monopoly, Battleship
      
   .. grid-item-card:: 🎮 **Game Framework**
      :link: framework
      :link-type: doc
      
      Base classes and utilities

Quick Start
-----------

Play a game with simple API:

.. code-block:: python

   from haive.games.connect4.api import play_connect4_simple
   
   # Play GPT-4 vs Claude
   result = play_connect4_simple(
       red_model="openai:gpt-4o",
       yellow_model="anthropic:claude-3-5-sonnet"
   )
   print(f"Winner: {result.winner}")

Tournament Mode
---------------

Run tournaments between different models:

.. code-block:: python

   from haive.games.tournament_tools import TournamentRunner
   
   tournament = TournamentRunner(
       games=["chess", "checkers", "connect4"],
       player1="gpt-4o",
       player2="claude-3-opus",
       rounds_per_game=5
   )
   results = tournament.run()

Featured Games
--------------

**Most Complete Implementations:**

1. **Tic Tac Toe** - Rich UI, analysis features, comprehensive testing
2. **Chess** - Full rules, python-chess backend, position analysis
3. **Connect4** - Configurable agents, API support, tournament ready
4. **Mafia** - Multi-agent discussion, complex social dynamics
5. **Among Us** - Task system, voting, impostor detection

Game Architecture
-----------------

All games follow a consistent pattern:

.. code-block:: text

   GameAgent (extends haive.core.Agent)
   ├── GameConfig (configuration)
   ├── GameState (state management)
   ├── GameStateManager (rules & logic)
   └── LLM Engines (player intelligence)

Example Game Implementation
---------------------------

.. code-block:: python

   from haive.games.base import GameAgent, GameConfig, GameState
   
   class MyGameAgent(GameAgent[MyGameState]):
       """Custom game implementation."""
       
       def setup_workflow(self):
           # Build LangGraph state machine
           builder = StateGraph(MyGameState)
           
           # Add game nodes
           builder.add_node("player_move", self.handle_move)
           builder.add_node("check_winner", self.check_winner)
           
           # Connect workflow
           builder.add_edge("player_move", "check_winner")
           builder.set_entry_point("player_move")
           
           return builder.compile()

Available Games (24 Total)
--------------------------

**Board Games (8)**
   - Chess, Checkers, Go, Reversi/Othello
   - Mancala, Fox and Geese, Tic-Tac-Toe, Connect4

**Card Games (5)**
   - Texas Hold'em, Blackjack, BS (Bluffing), UNO, Poker variants

**Single Player (11)**
   - Wordle, Sudoku, 2048, Minesweeper, Flow Free
   - Rubik's Cube, Towers of Hanoi, Crossword, Logic Grid
   - Word Search, Solitaire

**Multi-Player Strategy (6)**
   - Risk, Monopoly, Dominoes, Battleship
   - Mafia, Among Us

**Other Games (3)**
   - Clue/Cluedo, Mastermind, Nim, Debate

.. toctree::
   :maxdepth: 3
   :caption: Game Categories
   :hidden:
   
   board_games
   card_games
   puzzle_games
   social_games
   strategy_games
   framework

Module Path
-----------

.. code-block:: python

   import haive.games
   # Specific games
   from haive.games.chess import ChessAgent
   from haive.games.connect4 import Connect4Agent
   
   # APIs
   from haive.games.connect4.api import play_connect4_simple

API Reference
-------------

.. autosummary::
   :toctree: generated
   :recursive:
   :caption: Haive Games API
   
   haive.games