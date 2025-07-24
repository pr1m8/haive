Game Demos
==========

Interactive game demonstrations with playable interfaces and AI opponents.

.. raw:: html

    <div class="games-hero">
        <h2>🎮 Play Against AI</h2>
        <p>Experience our game environments with intelligent AI opponents of varying skill levels.</p>
    </div>

.. grid:: 2 2 3 3
   :gutter: 3

   .. grid-item-card:: ♟️ Chess
      :link: chess-demo
      :link-type: doc
      :class-card: game-demo-card

      Classic chess with AI agents of varying skill levels

   .. grid-item-card:: ⭕ Tic Tac Toe
      :link: tictactoe-demo
      :link-type: doc
      :class-card: game-demo-card

      Simple 3x3 grid game with perfect play AI

   .. grid-item-card:: 🔴 Checkers
      :link: checkers-demo
      :link-type: doc
      :class-card: game-demo-card

      Classic checkers with jumping and king promotion

   .. grid-item-card:: 🏨 Monopoly
      :link: monopoly-demo
      :link-type: doc
      :class-card: game-demo-card

      Economic strategy game with property trading and AI negotiation

   .. grid-item-card:: 🚀 Among Us
      :link: among_us-demo
      :link-type: doc
      :class-card: game-demo-card

      Social deduction with AI crewmates and imposters

   .. grid-item-card:: 🟤 Mancala
      :link: mancala-demo
      :link-type: doc
      :class-card: game-demo-card

      Ancient seed-counting game with strategic depth



.. toctree::
   :maxdepth: 1
   :caption: Game Demonstrations
   :hidden:

   chess-demo
   tictactoe-demo
   checkers-demo
   monopoly-demo
   among_us-demo
   mancala-demo


.. raw:: html

    <style>
    .games-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
    }

    .games-hero h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .game-demo-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .game-demo-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    </style>

Features
--------

All game demos include:

- **🎮 Interactive Interface**: Click to play directly in your browser
- **🤖 AI Opponents**: Multiple difficulty levels with differents
- **📊 Move Analysis**: See AI reasoning and move suggestions
- **📈 Game History**: Track moves and analyze gameplay
- **🎯 Strategy Tips**: Learn optimal play techniques

Getting Started
---------------

1. **Choose a Game**: Click any game card above
2. **Select AI Level**: Pick difficulty from beginner to master
3. **Start Playing**: Make moves by clicking the board
4. **Learn Strategy**: Watch AI analysis and improve your play

Each game includes detailed rules, strategy guides, and code examples for building your own game agents.
