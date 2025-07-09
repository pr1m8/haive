Games Showcase
==============

Beautiful, interactive game environments with intelligent AI opponents.

Board Games
-----------

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: ♟️ **Chess**
      :class-header: text-center
      :class-body: text-center
      
      Play interactive chess against AI opponents of varying skill levels
      
      :bdg-primary:`Strategy` :bdg-secondary:`AI Opponent`

   .. grid-item-card:: 🔴 **Checkers**
      :class-header: text-center
      :class-body: text-center
      
      Strategic board game with jumping captures and AI strategy
      
      :bdg-primary:`Jumping` :bdg-secondary:`Captures`

   .. grid-item-card:: 🟤 **Mancala**
      :class-header: text-center
      :class-body: text-center
      
      Ancient counting game with strategic depth and AI planning
      
      :bdg-primary:`Ancient` :bdg-secondary:`Counting`

   .. grid-item-card:: ⚫ **Go**
      :class-header: text-center
      :class-body: text-center
      
      Ancient strategy game with territory control and complex AI
      
      :bdg-primary:`Territory` :bdg-secondary:`Complex AI`

   .. grid-item-card:: 🎯 **Reversi**
      :class-header: text-center
      :class-body: text-center
      
      Strategic tile-flipping game with AI pattern recognition
      
      :bdg-primary:`Pattern` :bdg-secondary:`Strategy`

   .. grid-item-card:: 🎲 **Risk**
      :class-header: text-center
      :class-body: text-center
      
      World domination strategy with AI diplomacy and warfare
      
      :bdg-primary:`Diplomacy` :bdg-secondary:`Warfare`

Quick Games
-----------

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: ⭕ **Tic Tac Toe**
      :class-header: text-center
      :class-body: text-center
      
      Quick 3x3 strategy game with perfect AI opponent
      
      :bdg-success:`Perfect AI` :bdg-info:`Quick`

   .. grid-item-card:: 🎯 **Connect 4**
      :class-header: text-center
      :class-body: text-center
      
      Classic connection game with strategic depth
      
      :bdg-success:`Connection` :bdg-info:`Strategy`

   .. grid-item-card:: 🔢 **Nim**
      :class-header: text-center
      :class-body: text-center
      
      Mathematical strategy game with optimal play
      
      :bdg-success:`Math` :bdg-info:`Optimal`

Card & Social Games
-------------------

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: 🃏 **Poker (Hold'em)**
      :class-header: text-center
      :class-body: text-center
      
      Texas Hold'em with betting, bluffing, and AI psychology
      
      :bdg-warning:`Bluffing` :bdg-danger:`Psychology`

   .. grid-item-card:: 🚀 **Among Us**
      :class-header: text-center
      :class-body: text-center
      
      Social deduction game with intelligent AI crewmates and imposters
      
      :bdg-warning:`Deduction` :bdg-danger:`Social`

   .. grid-item-card:: 🕵️ **Clue**
      :class-header: text-center
      :class-body: text-center
      
      Mystery deduction game with logical reasoning and AI detective work
      
      :bdg-warning:`Mystery` :bdg-danger:`Logic`

   .. grid-item-card:: 🎭 **Mafia**
      :class-header: text-center
      :class-body: text-center
      
      Social deduction with AI role-playing and strategic elimination
      
      :bdg-warning:`Role-play` :bdg-danger:`Elimination`

Economic Games
--------------

.. grid:: 1 2 3 3
   :gutter: 3

   .. grid-item-card:: 🏨 **Monopoly**
      :class-header: text-center
      :class-body: text-center
      
      Economic strategy with AI negotiation and property trading
      
      :bdg-light:`Trading` :bdg-dark:`Negotiation`

   .. grid-item-card:: 🎯 **Battleship**
      :class-header: text-center
      :class-body: text-center
      
      Naval strategy with AI pattern recognition and probability
      
      :bdg-light:`Naval` :bdg-dark:`Probability`

   .. grid-item-card:: 🎲 **Dominoes**
      :class-header: text-center
      :class-body: text-center
      
      Tile-based strategy with AI scoring optimization
      
      :bdg-light:`Tiles` :bdg-dark:`Scoring`

   .. grid-item-card:: 🔍 **Mastermind**
      :class-header: text-center
      :class-body: text-center
      
      Code-breaking game with AI logical deduction
      
      :bdg-light:`Deduction` :bdg-dark:`Logic`

Game Categories
---------------

For detailed API documentation of all games, see :doc:`../api/haive-games`.

Quick Start
-----------

.. code-block:: python

   from haive.games.tic_tac_toe import TicTacToeGame
   from haive.games.tic_tac_toe.agent import TicTacToeAgent
   
   # Create game and agents
   game = TicTacToeGame()
   agent1 = TicTacToeAgent(name="Player 1", symbol="X")
   agent2 = TicTacToeAgent(name="Player 2", symbol="O")
   
   # Play!
   winner = await game.run(agent1, agent2)