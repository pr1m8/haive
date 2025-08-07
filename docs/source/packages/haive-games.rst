haive-games
===========

Game environments and agents for AI gameplay.

Overview
--------

The ``haive-games`` package provides a comprehensive collection of game environments and AI agents:

- **Board Games** - Chess, Checkers, Go, Reversi, Tic-Tac-Toe
- **Card Games** - Poker, Blackjack, BS, Uno
- **Strategy Games** - Risk, Battleship, Clue, Monopoly
- **Social Games** - Mafia, Among Us, Debate
- **Puzzle Games** - Sudoku, Wordle, Mastermind, Mancala
- **Single Player** - Minesweeper, 2048, Flow Free, Rubik's Cube

Installation
------------

.. code-block:: bash

   pip install haive-games

Or as part of the full framework:

.. code-block:: bash

   pip install haive

Quick Start
-----------

.. code-block:: python

   from haive.games.chess.agent import ChessAgent
   from haive.games.chess.config import ChessConfig
   
   # Create chess game
   config = ChessConfig(
       player1_model="gpt-4",
       player2_model="claude-3"
   )
   
   agent = ChessAgent(config=config)
   
   # Play game
   result = agent.play_game()

Game Categories
---------------

Board Games
^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Chess
      :link: ../api/games/chess/index
      :link-type: doc

      Classic chess implementation
      
      - Full rules engine
      - UCI notation support
      - AI vs AI/Human
      - Move validation

   .. grid-item-card:: Go
      :link: ../api/games/go/index
      :link-type: doc

      Ancient strategy game
      
      - 19x19, 13x13, 9x9 boards
      - Ko rule handling
      - Territory scoring
      - AI strategy

Card Games
^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Poker (Texas Hold'em)
      :link: ../api/games/hold_em/index
      :link-type: doc

      Texas Hold'em poker
      
      - Betting rounds
      - Hand evaluation
      - Bluffing AI
      - Pot management

   .. grid-item-card:: Blackjack
      :link: ../api/games/cards/standard/blackjack/index
      :link-type: doc

      Casino blackjack
      
      - Hit/Stand/Double
      - Card counting
      - Basic strategy
      - Multiple decks

Strategy Games
^^^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Risk
      :link: ../api/games/risk/index
      :link-type: doc

      World domination game
      
      - Territory control
      - Army management
      - Dice battles
      - Alliance system

   .. grid-item-card:: Battleship
      :link: ../api/games/battleship/index
      :link-type: doc

      Naval strategy game
      
      - Ship placement
      - Shot tracking
      - AI targeting
      - Hit detection

Social Games
^^^^^^^^^^^^

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Mafia
      :link: ../api/games/mafia/index
      :link-type: doc

      Social deduction game
      
      - Role assignment
      - Day/Night phases
      - Voting system
      - Deduction AI

   .. grid-item-card:: Debate
      :link: ../api/games/debate/index
      :link-type: doc

      AI debate system
      
      - Topic handling
      - Turn management
      - Judge scoring
      - Argument tracking

Core Game Classes
-----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.base.agent.BaseGameAgent
   haive.games.base.config.BaseGameConfig
   haive.games.base.state.BaseGameState
   haive.games.base.state_manager.BaseStateManager

Board Game Agents
-----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.chess.agent.ChessAgent
   haive.games.checkers.agent.CheckersAgent
   haive.games.go.agent.GoAgent
   haive.games.reversi.agent.ReversiAgent
   haive.games.tic_tac_toe.agent.TicTacToeAgent
   haive.games.connect4.agent.Connect4Agent
   haive.games.mancala.agent.MancalaAgent

Card Game Agents
----------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.hold_em.agent.HoldEmAgent
   haive.games.poker.agent.PokerAgent
   haive.games.cards.standard.blackjack.agent.BlackjackAgent
   haive.games.cards.standard.bs.agent.BSAgent

Strategy Game Agents
--------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.risk.agent.RiskAgent
   haive.games.battleship.agent.BattleshipAgent
   haive.games.clue.agent.ClueAgent
   haive.games.monopoly.agent.MonopolyAgent

Social Game Agents
------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.mafia.agent.MafiaAgent
   haive.games.among_us.agent.AmongUsAgent
   haive.games.debate.agent.DebateAgent
   haive.games.debate_v2.agent.DebateAgentV2

Puzzle Game Agents
------------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/class.rst

   haive.games.single_player.sudoku.SudokuAgent
   haive.games.single_player.wordle.agent.WordleAgent
   haive.games.mastermind.agent.MastermindAgent
   haive.games.nim.agent.NimAgent

Game Utilities
--------------

.. autosummary::
   :toctree: ../api
   :recursive:
   :nosignatures:
   :template: autosummary/function.rst

   haive.games.utils.test_helpers.create_test_game
   haive.games.llm_config_factory.create_llm_config
   haive.games.common.voting_system.VotingSystem

Complete API Reference
----------------------

For the complete API documentation with all game implementations:

.. toctree::
   :maxdepth: 3

   ../api/games/index

Examples
--------

Chess Game with Custom AI
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.games.chess.agent import ChessAgent
   from haive.games.chess.config import ChessConfig
   from haive.core.engine.aug_llm import AugLLMConfig
   
   # Configure players
   config = ChessConfig(
       player1_config=AugLLMConfig(
           model="gpt-4",
           temperature=0.3,
           system_message="You are a chess grandmaster."
       ),
       player2_config=AugLLMConfig(
           model="claude-3",
           temperature=0.5,
           system_message="You play aggressive chess."
       )
   )
   
   # Create and run game
   agent = ChessAgent(config=config)
   result = agent.play_game()
   
   # Display results
   print(f"Winner: {result.winner}")
   print(f"Moves: {result.move_history}")

Poker Tournament
^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.games.hold_em.agent import HoldEmAgent
   from haive.games.hold_em.config import HoldEmConfig
   
   # Multi-player poker setup
   config = HoldEmConfig(
       num_players=6,
       starting_chips=10000,
       blind_structure="tournament"
   )
   
   agent = HoldEmAgent(config=config)
   
   # Run tournament
   tournament_result = agent.run_tournament()

Mafia Game Simulation
^^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.games.mafia.agent import MafiaAgent
   from haive.games.mafia.config import MafiaConfig
   
   # Social deduction setup
   config = MafiaConfig(
       num_players=8,
       roles=["mafia", "mafia", "detective", "doctor", 
              "townsperson", "townsperson", "townsperson", "townsperson"],
       ai_personalities=["aggressive", "defensive", "analytical", "random",
                         "cautious", "leader", "follower", "wildcard"]
   )
   
   agent = MafiaAgent(config=config)
   result = agent.play_game()

Custom Game Creation
^^^^^^^^^^^^^^^^^^^^

.. code-block:: python

   from haive.games.base.agent import BaseGameAgent
   from haive.games.base.config import BaseGameConfig
   from haive.games.base.state import BaseGameState
   
   class MyGameState(BaseGameState):
       """Custom game state."""
       score: int = 0
       moves: List[str] = []
   
   class MyGameConfig(BaseGameConfig):
       """Custom game configuration."""
       difficulty: str = "medium"
   
   class MyGameAgent(BaseGameAgent):
       """Custom game agent."""
       
       def play_turn(self, state: MyGameState) -> str:
           # Implement game logic
           return "move"

Best Practices
--------------

1. **Configure AI appropriately** for each game type
2. **Use structured configs** for game parameters
3. **Implement proper state management** for game history
4. **Test with different AI models** for varied gameplay
5. **Handle game rules** strictly in state managers
6. **Use UI classes** for interactive play

Game Development Guidelines
---------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Guideline
     - Description
   * - **State Management**
     - All game state in dedicated State class
   * - **Move Validation**
     - Validate all moves before applying
   * - **Rule Enforcement**
     - Strict rule checking in StateManager
   * - **AI Strategy**
     - Configurable AI behaviors per game
   * - **Testing**
     - Comprehensive game scenario tests

Related Documentation
---------------------

- :doc:`../guide/games` - Game development guide
- :doc:`../api/games/index` - Complete games API reference
- :doc:`haive-agents` - Agent framework for games
- :doc:`../examples/games` - Game examples and tutorials