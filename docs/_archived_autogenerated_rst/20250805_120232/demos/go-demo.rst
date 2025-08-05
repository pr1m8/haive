Go Demo



Ancient strategic board game

   <div class="game-demo-container">
   <!-- Game Overview -->

   <div class="game-overview-card">

   <div class="game-header">

   <div class="game-icon">⚫</div>

   <div>
   <h2>Go</h2>
   <p class="game-complexity">Complexity: Very High</p>
   </div>

   </div>

   <div class="game-stats">

   <div class="stat">
   <label>Board Size:</label>
   <span>19x19 grid</span>
   </div>

   <div class="stat">
   <label>Players:</label>
   <span>2-4</span>
   </div>

   </div>

   <div class="game-features">
   <span class="feature-tag">Territory control</span>
   <span class="feature-tag">Capture</span>
   <span class="feature-tag">Ko rule</span>
   <span class="feature-tag">Handicap system</span>
   </div>

   </div>

   <!-- Playable Game Interface -->

   <div class="game-interface">

   <div class="game-controls">
   <h3>Play Go</h3>

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="go-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

   <button onclick="startGame('go')" class="start-game-btn">

                    Start New Game

   </button>
   </div>

   <div id="go-board" class="game-board">
   <!-- Game board will be rendered here -->

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Go</p>
   </div>

   </div>

   <div class="game-status">

   <div id="go-status" class="status-display">

                       Ready to play

   </div>

   <div id="go-moves" class="moves-history">
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

   <pre id="go-state">

       A B C D E F G H J
       9 . . . . . . . . .
       8 . . ○ . . . ● . .
       7 . ○ . . . ● . . .
       6 . . . + . . . . .
       5 . . . . + . . . .
       4 . . . . . . . . .
       3 . . ● . . . ○ . .
       2 . . . . . . . . .
       1 . . . . . . . . .


   Black: 12 captured
   White: 8 captured
   Turn: Black | Move: 45

   </pre>
   </div>

   <div class="move-history">
   <h4>Recent Activity</h4>

   <div id="go-moves-stream">

   <div class="move">Game initialized...</div>

   <div class="move">Waiting for players...</div>
   </div>

   </div>
   </div>
   </div>

Rules & Strategy



**How to Play:**

Learn the rules and strategies for Go.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example



.. code-block:: python

    # Code example here

    from haive.games.go import GoGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = GoGame()

    # Create AI players
    player1 = SimpleAgent(name="Player1")
    player2 = SimpleAgent(name="AI_Player", difficulty="advanced")

    # Play game
    winner = game.play(player1, player2)
    print(f"Winner: {winner}")

    See Also


-------

    - :doc:`/api/haive/games/index - Games API documentation`

`
    - :doc`:`/guides/game-development - Creating custom games`

`
    - :doc`:`/examples/game-agents - More game examples`

`
`
