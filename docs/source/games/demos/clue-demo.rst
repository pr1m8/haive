Clue (Cluedo) Demo
==================

Mystery deduction game to solve the murder

.. raw:: html

    <div class="game-demo-container">
        <!-- Game Overview -->
        <div class="game-overview-card">
            <div class="game-header">
                <div class="game-icon">🔍</div>
                <div>
                    <h2>Clue (Cluedo)</h2>
                    <p class="game-complexity">Complexity: High</p>
                </div>
            </div>

            <div class="game-stats">
                <div class="stat">
                    <label>Board Size:</label>
                    <span>Mansion layout</span>
                </div>
                <div class="stat">
                    <label>Players:</label>
                    <span>2-4</span>
                </div>
            </div>

            <div class="game-features">
                <span class="feature-tag">Deduction</span>
                <span class="feature-tag">Movement</span>
                <span class="feature-tag">Accusations</span>
                <span class="feature-tag">Note-taking</span>
            </div>
        </div>

        <!-- Playable Game Interface -->
        <div class="game-interface">
            <div class="game-controls">
                <h3>Play Clue (Cluedo)</h3>
                <div class="ai-selection">
                    <label>AI Difficulty:</label>
                    <select id="clue-ai-level">
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="master">Master</option>
                    </select>
                </div>
                <button onclick="startGame('clue')" class="start-game-btn">
                    Start New Game
                </button>
            </div>

            <div id="clue-board" class="game-board">
                <!-- Game board will be rendered here -->
                <div class="board-placeholder">
                    <p>Click "Start New Game" to begin playing Clue (Cluedo)</p>
                </div>
            </div>

            <div class="game-status">
                <div id="clue-status" class="status-display">
                    Ready to play
                </div>
                <div id="clue-moves" class="moves-history">
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
                </pre>
            </div>
            <div class="move-history">
                <h4>Recent Activity</h4>
                <div id="clue-moves-stream">
                    <div class="move">Game initialized...</div>
                    <div class="move">Waiting for players...</div>
                </div>
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
