Board Games
===========

Classic board games with AI opponents.

Chess
-----

Full chess implementation with advanced features:

.. code-block:: python

   from haive.games.chess import ChessAgent, ChessConfig
   
   config = ChessConfig(
       white_player="openai:gpt-4o",
       black_player="anthropic:claude-3-opus",
       enable_analysis=True,
       max_moves=100
   )
   
   agent = ChessAgent(config)
   result = agent.run()

Features:
- Complete chess rules (castling, en passant, promotion)
- Position analysis with python-chess
- PGN export/import
- Move validation and legal move generation

Checkers
--------

American checkers with king promotion:

.. code-block:: python

   from haive.games.checkers import CheckersAgent
   
   agent = CheckersAgent(
       player1_model="gpt-4",
       player2_model="claude-3"
   )
   result = await agent.arun()

Go
--

Ancient territorial control game:

.. code-block:: python

   from haive.games.go import GoAgent, GoConfig
   
   config = GoConfig(
       board_size=19,  # 9x9, 13x13, or 19x19
       komi=7.5,       # Compensation for white
       time_limit=300  # Seconds per move
   )

Reversi/Othello
---------------

Piece flipping strategy:

.. code-block:: python

   from haive.games.reversi import ReversiAgent
   
   agent = ReversiAgent(
       enable_hints=True,
       show_valid_moves=True
   )

Connect4
--------

Drop pieces to connect four:

.. code-block:: python

   from haive.games.connect4.api import play_connect4_simple
   
   # Simple API
   result = play_connect4_simple(
       red_model="gpt-4o-mini",
       yellow_model="claude-3-haiku"
   )
   
   # Advanced configuration
   from haive.games.connect4 import Connect4Agent
   agent = Connect4Agent(
       analysis_depth=3,
       enable_minimax=True
   )

Tic-Tac-Toe
-----------

Classic game with Rich UI:

.. code-block:: python

   from haive.games.tic_tac_toe import TicTacToeAgent
   
   agent = TicTacToeAgent(
       enable_analysis=True,
       ui_enabled=True  # Rich terminal UI
   )

Mancala
-------

Seed sowing game:

.. code-block:: python

   from haive.games.mancala import MancalaAgent
   
   agent = MancalaAgent(
       variant="kalah",  # or "oware"
       seeds_per_house=4
   )

Fox and Geese
-------------

Asymmetric strategy game:

.. code-block:: python

   from haive.games.fox_and_geese import FoxAndGeeseAgent
   
   agent = FoxAndGeeseAgent(
       fox_player="gpt-4",
       geese_player="claude-3",
       ui_enabled=True  # Rich UI
   )

Common Features
---------------

All board games support:
- Save/load game states
- Move history and replay
- AI vs AI, AI vs Human, Human vs Human
- Configurable thinking time
- Position evaluation
- Rich terminal UI (select games)