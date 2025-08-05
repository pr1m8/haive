Nim Demo



Mathematical strategy game

   <div class="game-demo-container">
   <!-- Game Overview -->

   <div class="game-overview-card">

   <div class="game-header">

   <div class="game-icon">🎮</div>

   <div>
   <h2>Nim</h2>
   <p class="game-complexity">Complexity: Low</p>
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
   <span class="feature-tag">Perfect strategy</span>
   <span class="feature-tag">Multiple variants</span>
   <span class="feature-tag">Quick games</span>
   <span class="feature-tag">Mathematical basis</span>
   </div>

   </div>

   <!-- Playable Game Interface -->

   <div class="game-interface">

   <div class="game-controls">
   <h3>Play Nim</h3>

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="nim-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

   <button onclick="startGame('nim')" class="start-game-btn">

                    Start New Game

   </button>
   </div>

   <div id="nim-board" class="game-board">
   <!-- Game board will be rendered here -->

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Nim</p>
   </div>

   </div>

   <div class="game-status">

   <div id="nim-status" class="status-display">

                       Ready to play

   </div>

   <div id="nim-moves" class="moves-history">
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

   <pre id="nim-state">

       Heap A: ||||| (5)
       Heap B: ||| (3)
       Heap C: |||||||| (8)
       Heap D: || (2)


   Last move: Player 1 took 3 from Heap C
   Current turn: Player 2

   Classic rules: Take any number from one heap
   Goal: Force opponent to take last object

   </pre>
   </div>

   <div class="move-history">
   <h4>Recent Activity</h4>

   <div id="nim-moves-stream">

   <div class="move">Game initialized...</div>

   <div class="move">Waiting for players...</div>
   </div>

   </div>
   </div>
   </div>

Rules & Strategy



**How to Play:**

Learn the rules and strategies for Nim.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example



.. code-block:: python

    # Code example here

    from haive.games.nim import NimGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = NimGame()

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
