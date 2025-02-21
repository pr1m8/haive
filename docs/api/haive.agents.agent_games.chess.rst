Chess Agent Module
================

.. module:: haive.agents.agent_games.chess

.. image:: /_static/module_icons/chess.svg
   :align: right
   :width: 100px

Overview
-------

The Chess Agent module provides a specialized implementation for chess gameplay,
including board state representation, move generation, position evaluation, and
LLM-augmented strategic planning.

Components
---------

The module consists of several key components:

.. grid:: 1 2 2 2
    :gutter: 3
    
    .. grid-item-card:: Agent
        
        Main agent implementation for chess that coordinates the various components.
        
        :class:`~haive.agents.agent_games.chess.agent.ChessAgent`

    .. grid-item-card:: State
        
        Chess-specific state representation with FEN parsing and board management.
        
        :class:`~haive.agents.agent_games.chess.state.ChessState`

    .. grid-item-card:: Models
        
        Data models for chess positions, moves, and evaluation metrics.
        
        :mod:`~haive.agents.agent_games.chess.models`

    .. grid-item-card:: LLM Augmentation
        
        Enhanced language model interfaces for chess strategy and analysis.
        
        :mod:`~haive.agents.agent_games.chess.aug_llms`

Chess Agent
---------

.. autoclass:: haive.agents.agent_games.chess.agent.ChessAgent
   :members:
   :inherited-members:
   :special-members: __init__

State Management
--------------

.. autoclass:: haive.agents.agent_games.chess.state.ChessState
   :members:
   :inherited-members:

Models
-----

.. automodule:: haive.agents.agent_games.chess.models
   :members:
   :undoc-members:

Augmented LLMs
------------

.. automodule:: haive.agents.agent_games.chess.aug_llms
   :members:
   :undoc-members:

Utilities
--------

.. automodule:: haive.agents.agent_games.chess.utils
   :members:
   :undoc-members:

Examples
-------

Basic Usage
~~~~~~~~~~

.. code-block:: python
   :linenos:
   
   from haive.agents.agent_games.chess import ChessAgent
   from haive.agents.agent_games.chess.state import ChessState
   
   # Create a chess agent
   agent = ChessAgent()
   
   # Create an initial state from FEN notation
   state = ChessState.from_fen("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
   
   # Get the next move
   move = agent.get_next_move(state)
   
   # Apply the move to the state
   new_state = state.apply_move(move)
   
   print(f"Move: {move}")
   print(f"New board state:\n{new_state}")

Advanced Analysis
~~~~~~~~~~~~~~~

.. code-block:: python
   :linenos:
   
   from haive.agents.agent_games.chess import ChessAgent
   
   # Create a chess agent with advanced analysis
   agent = ChessAgent(analysis_depth=5)
   
   # Analyze a specific position
   fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
   analysis = agent.analyze_position(fen)
   
   print("Position Analysis:")
   print(f"Evaluation: {analysis['evaluation']}")
   print(f"Best move: {analysis['best_move']}")
   print(f"Strategic assessment: {analysis['strategic_assessment']}")