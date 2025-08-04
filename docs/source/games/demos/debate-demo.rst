Debate Demo
===========

AI agents engage in structured debates

.. raw:: html

   <div class="game-demo-container">
   <!-- Game Overview -->

.. raw:: html

   <div class="game-overview-card">

.. raw:: html

   <div class="game-header">

.. raw:: html

   <div class="game-icon">💬</div>

.. raw:: html

   <div>
   <h2>Debate</h2>
   <p class="game-complexity">Complexity: High</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="game-stats">

.. raw:: html

   <div class="stat">
   <label>Board Size:</label>
   <span>N/A</span>
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
   <span class="feature-tag">Arguments</span>
   <span class="feature-tag">Rebuttals</span>
   <span class="feature-tag">Judging</span>
   <span class="feature-tag">Topics</span>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <!-- Playable Game Interface -->

.. raw:: html

   <div class="game-interface">

.. raw:: html

   <div class="game-controls">
   <h3>Play Debate</h3>

.. raw:: html

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="debate-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

.. raw:: html

   <button onclick="startGame('debate')" class="start-game-btn">

                    Start New Game
.. raw:: html

   </button>
   </div>

.. raw:: html

   <div id="debate-board" class="game-board">
   <!-- Game board will be rendered here -->

.. raw:: html

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Debate</p>
   </div>

.. raw:: html

   </div>

.. raw:: html

   <div class="game-status">

.. raw:: html

   <div id="debate-status" class="status-display">

                       Ready to play
.. raw:: html

   </div>

.. raw:: html

   <div id="debate-moves" class="moves-history">
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

   <pre id="debate-state">

       Topic: "AI will create more jobs than it eliminates"


   PRO (Agent A): Opening Statement
   "AI augments human capabilities, creating new industries..."

   CON (Agent B): Opening Statement
   "Historical automation has consistently reduced employment..."

   Round: 1/3 | Phase: Rebuttals
   Time remaining: 45s

.. raw:: html

   </pre>
   </div>

.. raw:: html

   <div class="move-history">
   <h4>Recent Activity</h4>

.. raw:: html

   <div id="debate-moves-stream">

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

Learn the rules and strategies for Debate.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example
------------

.. code-block:: python

    from haive.games.debate import DebateGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = DebateGame()

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
