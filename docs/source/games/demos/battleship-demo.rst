Battleship Demo
===============

Naval strategy game with hidden ship placement

.. raw:: html

    <div class="game-demo-container">
        <!-- Game Overview -->
        <div class="game-overview-card">
            <div class="game-header">
                <div class="game-icon">🚢</div>
                <div>
                    <h2>Battleship</h2>
                    <p class="game-complexity">Complexity: Medium</p>
                </div>
            </div>

            <div class="game-stats">
                <div class="stat">
                    <label>Board Size:</label>
                    <span>10x10 grids</span>
                </div>
                <div class="stat">
                    <label>Players:</label>
                    <span>2-4</span>
                </div>
            </div>

            <div class="game-features">
                <span class="feature-tag">Ship placement</span>
                <span class="feature-tag">Strategic guessing</span>
                <span class="feature-tag">Hit tracking</span>
                <span class="feature-tag">AI opponents</span>
            </div>
        </div>

        <!-- Playable Game Interface -->
        <div class="game-interface">
            <div class="game-controls">
                <h3>Play Battleship</h3>
                <div class="ai-selection">
                    <label>AI Difficulty:</label>
                    <select id="battleship-ai-level">
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="master">Master</option>
                    </select>
                </div>
                <button onclick="startGame('battleship')" class="start-game-btn">
                    Start New Game
                </button>
            </div>

            <div id="battleship-board" class="game-board">
                <!-- Game board will be rendered here -->
                <div class="board-placeholder">
                    <p>Click "Start New Game" to begin playing Battleship</p>
                </div>
            </div>

            <div class="game-status">
                <div id="battleship-status" class="status-display">
                    Ready to play
                </div>
                <div id="battleship-moves" class="moves-history">
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
                <pre id="battleship-state">
  A B C D E F G H I J        A B C D E F G H I J
  1 . . . . . . . . . .        1 . . . . . . . . . .
  2 . . S S S . . . . .        2 . . ? ? ? . . . . .
  3 . . . . . . . . . .        3 . . . . . . . . . .
  4 . B . . . . . . . .        4 . X . . . . . . . .
  5 . B . . . . . . . .        5 . O . . . . . . . .
  6 . B . . D D . . . .        6 . ? . . ? ? . . . .
  7 . B . . . . . . . .        7 . ? . . . . . . . .
  8 . . . . . . . . . .        8 . . . . . . . . . .
  9 . . . . . . . C C C        9 . . . . . . . ? ? ?
 10 . . . . . . . . . .       10 . . . . . . . . . .

Your Fleet | Enemy Waters
S=Submarine, B=Battleship, D=Destroyer, C=Cruiser
X=Hit, O=Miss, ?=Unknown
                </pre>
            </div>
            <div class="move-history">
                <h4>Recent Activity</h4>
                <div id="battleship-moves-stream">
                    <div class="move">Game initialized...</div>
                    <div class="move">Waiting for players...</div>
                </div>
            </div>
        </div>
    </div>

Rules & Strategy
----------------

**How to Play:**

Learn the rules and strategies for Battleship.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example
------------

.. code-block:: python

    from haive.games.battleship import BattleshipGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = BattleshipGame()

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
