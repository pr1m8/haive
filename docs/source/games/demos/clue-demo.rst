Clue (Cluedo) Demo
==================

Mystery deduction game to solve the murder

.. raw:: html

   <div class="game-demo-container">
   <!-- Game Overview -->

.. raw:: html

   <div class="game-overview-card">

.. raw:: html

   <div class="game-header">

.. raw:: html

   <div class="game-icon">🔍</div>

.. raw:: html

   <div>
   <h2>Clue (Cluedo)</h2>
   <p class="game-complexity">Complexity: High</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="game-stats">

.. raw:: html

   <div class="stat">
   <label>Board Size:</label>
   <span>Mansion layout</span>
   </div>

.. raw:: html

   <div class="stat">
   <label>Players:</label>
   <span>2-4</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="game-features">
   <span class="feature-tag">Deduction</span>
   <span class="feature-tag">Movement</span>
   <span class="feature-tag">Accusations</span>
   <span class="feature-tag">Note-taking</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Playable Game Interface -->

.. raw:: html

   <div class="game-interface">

.. raw:: html

   <div class="game-controls">
   <h3>Play Clue (Cluedo)</h3>

.. raw:: html

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="clue-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

.. raw:: html

   <button onclick="startGame('clue')" class="start-game-btn">

                    Start New Game
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="clue-board" class="game-board">
   <!-- Game board will be rendered here -->

.. raw:: html

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Clue (Cluedo)</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="game-status">

.. raw:: html

   <div id="clue-status" class="status-display">

                       Ready to play
.. raw:: html

   </div>

.. raw:: html

   <div id="clue-moves" class="moves-history">
   <!-- Move history will appear here -->
   </div>

.. raw:: html

   </div>
   </div>

.. raw:: html

   <!-- Live Game Stream -->

.. raw:: html

   <div class="game-streaming">
   <h3>Live Game Visualization</h3>

.. raw:: html

   <div class="streaming-indicator">

                   Live Stream
.. raw:: html

   </div>

.. raw:: html

   <div class="game-state-display">

.. raw:: html

   <pre id="clue-state">

       ╔═══════╦═══════╦═══════╦═══════╗
       ║ Study ║Hallway║ Hall  ║Lounge ║
       ║   P1  ║       ║       ║   P2  ║
       ╠═══════╬═══════╬═══════╬═══════╣
       ║Library║Billiard║Dining ║       ║
       ║       ║  Room  ║ Room  ║Passage║
       ╠═══════╬═══════╬═══════╬═══════╣
       ║Conserv║Ballroom║Kitchen║       ║
       ║   P3  ║   P4   ║  P5   ║  P6   ║
       ╚═══════╩═══════╩═══════╩═══════╝


   Current Player: Miss Scarlet
   Location: Study
   Cards in hand: 3
   Suggestions made: 2

.. raw:: html

   </pre>
   </div>

.. raw:: html

   <div class="move-history">
   <h4>Recent Activity</h4>

.. raw:: html

   <div id="clue-moves-stream">

.. raw:: html

   <div class="move">Game initialized...</div>

.. raw:: html

   <div class="move">Waiting for players...</div>
   </div>

.. raw:: html

   </div>
   </div>
   </div>

Rules & Strategy
----------------

**How to Play:**

Learn the rules and strategies for Clue (Cluedo).

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example
------------

.. code-block:: python

    from haive.games.clue import Clue(Cluedo)Game
    from haive.agents.simple import SimpleAgent

    # Create game
    game = Clue(Cluedo)Game()

    # Create AI players
    player1 = SimpleAgent(name="Player1")
    player2 = SimpleAgent(name="AI_Player", difficulty="advanced")

    # Play game
    winner = game.play(player1, player2)
    print(f"Winner: {winner}")

    See Also
    --------

    - :doc:`/api/haive/games/index` - Games API documentation
    - :doc:`/guides/game-development` - Creating custom games
    - :doc:`/examples/game-agents` - More game examples
