Mastermind Demo
===============

Code-breaking logic game

   <div class="game-demo-container">
   <!-- Game Overview -->

   <div class="game-overview-card">

   <div class="game-header">

   <div class="game-icon">🎯</div>

   <div>
   <h2>Mastermind</h2>
   <p class="game-complexity">Complexity: Medium</p>
   </div>

   </div>

   <div class="game-stats">

   <div class="stat">
   <label>Board Size:</label>
   <span>N/A</span>
   </div>

   <div class="stat">
   <label>Players:</label>
   <span>2-4</span>
   </div>

   </div>

   <div class="game-features">
   <span class="feature-tag">Deduction</span>
   <span class="feature-tag">Pattern recognition</span>
   <span class="feature-tag">Feedback system</span>
   <span class="feature-tag">Limited guesses</span>
   </div>

   </div>

   <!-- Playable Game Interface -->

   <div class="game-interface">

   <div class="game-controls">
   <h3>Play Mastermind</h3>

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="mastermind-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

   <button onclick="startGame('mastermind')" class="start-game-btn">

                    Start New Game
   </button>
   </div>

   <div id="mastermind-board" class="game-board">
   <!-- Game board will be rendered here -->

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Mastermind</p>
   </div>

   </div>

   <div class="game-status">

   <div id="mastermind-status" class="status-display">

                       Ready to play
   </div>

   <div id="mastermind-moves" class="moves-history">
   <!-- Move history will appear here -->
   </div>

   </div>
   </div>

   <!-- Live Game Stream -->

   <div class="game-streaming">
   <h3>Live Game Visualization</h3>

   <div class="streaming-indicator">

                   Live Stream
   </div>

   <div class="game-state-display">

   <pre id="mastermind-state">

       Secret Code: [?][?][?][?]


   Guess History:
   1. [R][B][G][Y] → ●●○○
   2. [B][R][Y][G] → ●○○
   3. [B][G][R][Y] → ●●●○
   4. [B][G][Y][R] → ●●●●

   ● = Correct position
   ○ = Correct color, wrong position

   Guesses remaining: 6

   </pre>
   </div>

   <div class="move-history">
   <h4>Recent Activity</h4>

   <div id="mastermind-moves-stream">

   <div class="move">Game initialized...</div>

   <div class="move">Waiting for players...</div>
   </div>

   </div>
   </div>
   </div>

Rules & Strategy
----------------

**How to Play:*

Learn the rules and strategies for Mastermind.

**AI Opponents:*

- **Beginner*: Perfect for learning the game
- **Intermediate*: Provides a moderate challenge
- **Advanced*: Strong strategic play
- **Master*: Expert-level AI

Code Example
------------

.. code-block:: python

    # Code example here

    from haive.games.mastermind import MastermindGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = MastermindGame()

    # Create AI players
    player1 = SimpleAgent(name="Player1")
    player2 = SimpleAgent(name="AI_Player", difficulty="advanced")

    # Play game
    winner = game.play(player1, player2)
    print(f"Winner: {winner}")

    See Also

--------

    - :doc:`/api/haive/games/index - Games API documentation`
    - :doc:`/guides/game-development - Creating custom games`
    - :doc:`/examples/game-agents - More game examples`
