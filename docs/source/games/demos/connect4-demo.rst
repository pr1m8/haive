Connect Four Demo
=================

Drop discs to connect four in a row

.. raw:: html

    <div class="game-demo-container">
        <!-- Game Overview -->
        <div class="game-overview-card">
            <div class="game-header">
                <div class="game-icon">🔴</div>
                <div>
                    <h2>Connect Four</h2>
                    <p class="game-complexity">Complexity: Low</p>
                </div>
            </div>

            <div class="game-stats">
                <div class="stat">
                    <label>Board Size:</label>
                    <span>7x6 grid</span>
                </div>
                <div class="stat">
                    <label>Players:</label>
                    <span>2-4</span>
                </div>
            </div>

            <div class="game-features">
                <span class="feature-tag">Gravity mechanics</span>
                <span class="feature-tag">Strategic placement</span>
                <span class="feature-tag">Quick games</span>
                <span class="feature-tag">AI levels</span>
            </div>
        </div>

        <!-- Playable Game Interface -->
        <div class="game-interface">
            <div class="game-controls">
                <h3>Play Connect Four</h3>
                <div class="ai-selection">
                    <label>AI Difficulty:</label>
                    <select id="connect4-ai-level">
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="master">Master</option>
                    </select>
                </div>
                <button onclick="startGame('connect4')" class="start-game-btn">
                    Start New Game
                </button>
            </div>

            <div id="connect4-board" class="game-board">
                <!-- Game board will be rendered here -->
                <div class="board-placeholder">
                    <p>Click "Start New Game" to begin playing Connect Four</p>
                </div>
            </div>

            <div class="game-status">
                <div id="connect4-status" class="status-display">
                    Ready to play
                </div>
                <div id="connect4-moves" class="moves-history">
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
                <pre id="connect4-state">
┌─┬─┬─┬─┬─┬─┬─┐
│ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┤
│ │ │ │ │ │ │ │
├─┼─┼─┼─┼─┼─┼─┤
│ │ │🔴│🟡│ │ │ │
├─┼─┼─┼─┼─┼─┼─┤
│ │🔴│🟡│🔴│ │ │ │
├─┼─┼─┼─┼─┼─┼─┤
│🟡│🔴│🟡│🔴│🟡│ │ │
└─┴─┴─┴─┴─┴─┴─┘
 1 2 3 4 5 6 7

Turn: Red | Moves: 9
                </pre>
            </div>
            <div class="move-history">
                <h4>Recent Activity</h4>
                <div id="connect4-moves-stream">
                    <div class="move">Game initialized...</div>
                    <div class="move">Waiting for players...</div>
                </div>
            </div>
        </div>
    </div>

Rules & Strategy
----------------

**How to Play:**

Learn the rules and strategies for Connect Four.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example
------------

.. code-block:: python

    from haive.games.connect4 import ConnectFourGame
    from haive.agents.simple import SimpleAgent

    # Create game
    game = ConnectFourGame()

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
