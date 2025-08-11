Risk Demo



Global domination strategy game

   <div class="game-demo-container">
   <!-- Game Overview -->

   <div class="game-overview-card">

   <div class="game-header">

   <div class="game-icon">🗺️</div>

   <div>
   <h2>Risk</h2>
   <p class="game-complexity">Complexity: High</p>
   </div>

   </div>

   <div class="game-stats">

   <div class="stat">
   <label>Board Size:</label>
   <span>World map</span>
   </div>

   <div class="stat">
   <label>Players:</label>
   <span>2-4</span>
   </div>

   </div>

   <div class="game-features">
   <span class="feature-tag">Territory control</span>
   <span class="feature-tag">Army management</span>
   <span class="feature-tag">Dice battles</span>
   <span class="feature-tag">Alliances</span>
   </div>

   </div>

   <!-- Playable Game Interface -->

   <div class="game-interface">

   <div class="game-controls">
   <h3>Play Risk</h3>

   <div class="ai-selection">
   <label>AI Difficulty:</label>
   <select id="risk-ai-level">
   <option value="beginner">Beginner</option>
   <option value="intermediate">Intermediate</option>
   <option value="advanced">Advanced</option>
   <option value="master">Master</option>
   </select>
   </div>

   <button onclick="startGame('risk')" class="start-game-btn">

                    Start New Game

   </button>
   </div>

   <div id="risk-board" class="game-board">
   <!-- Game board will be rendered here -->

   <div class="board-placeholder">
   <p>Click "Start New Game" to begin playing Risk</p>
   </div>

   </div>

   <div class="game-status">

   <div id="risk-status" class="status-display">

                       Ready to play

   </div>

   <div id="risk-moves" class="moves-history">
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

   <pre id="risk-state">

       North America: P1 (12 armies)
       South America: P2 (8 armies)
       Europe: P3 (15 armies)
       Africa: P1 (10 armies)
       Asia: P4 (22 armies)
       Australia: P2 (6 armies)


   Current Phase: Reinforcement
   Player 1 Turn
   Armies to place: 7
   Cards in hand: 2

   </pre>
   </div>

   <div class="move-history">
   <h4>Recent Activity</h4>

   <div id="risk-moves-stream">

   <div class="move">Game initialized...</div>

   <div class="move">Waiting for players...</div>
   </div>

   </div>
   </div>
   </div>

Rules & Strategy



**How to Play:**

Learn the rules and strategies for Risk.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example



.. code-block:: python

    # Code example here

    from haive.games.risk import RiskGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = RiskGame()

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
