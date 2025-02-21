Agent Games Package
=================

.. module:: haive.agents.agent_games

.. image:: /_static/module_icons/agent_games.svg
   :align: right
   :width: 100px

Overview
-------

The ``haive.agents.agent_games`` package provides implementations of game-playing agents
across multiple classic strategy games. Each game implementation shares a common architecture
while providing game-specific adaptations.

Supported Games
-------------

.. tab-set::

    .. tab-item:: Chess
        :sync: chess
        
        .. figure:: /_static/game_samples/chess.png
           :width: 300px
           
        Agent implementation for chess with board state management, move generation, 
        and positional evaluation.
        
        :doc:`Chess Agent Documentation <agent_games/chess>`

    .. tab-item:: Go
        :sync: go
        
        .. figure:: /_static/game_samples/go.png
           :width: 300px
           
        Agent implementation for the game of Go (Baduk/Weiqi) with territory analysis
        and complex position evaluation.
        
        :doc:`Go Agent Documentation <agent_games/go>`
        
    .. tab-item:: Checkers
        :sync: checkers
        
        .. figure:: /_static/game_samples/checkers.png
           :width: 300px
           
        Agent implementation for checkers (draughts) with jump detection and king promotion.
        
        :doc:`Checkers Agent Documentation <agent_games/checkers>`

Common Architecture
-----------------

All game agents share a common architecture:

.. mermaid::

   classDiagram
      class BaseGameAgent {
         +state
         +models
         +run(state)
         +evaluate(state)
         +get_next_move(state)
      }
      
      BaseGameAgent <|-- ChessAgent
      BaseGameAgent <|-- GoAgent
      BaseGameAgent <|-- CheckersAgent
      
      class GameState {
         +board
         +current_player
         +move_history
         +is_terminal()
         +get_legal_moves()
         +apply_move(move)
      }
      
      BaseGameAgent --> GameState

Usage Example
-----------

.. code-block:: python
   :linenos:
   
   from haive.agents.agent_games.chess import ChessAgent
   
   # Create a chess agent
   agent = ChessAgent()
   
   # Setup an initial board state (FEN notation)
   initial_state = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
   
   # Get the recommended move
   move = agent.get_next_move(initial_state)
   
   print(f"Recommended move: {move}")

Subpackages
----------

.. toctree::
   :maxdepth: 2
   
   agent_games/base
   agent_games/chess
   agent_games/go
   agent_games/checkers