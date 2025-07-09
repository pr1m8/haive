Games Showcase
==============

Beautiful, interactive game environments with intelligent AI opponents.

.. raw:: html

    <div class="agent-showcase-grid">
        
        <!-- Board Games -->
        <div class="showcase-section">
            <h2 class="section-title">♟️ Board Games</h2>
            <div class="agent-cards-grid">
                
                <div class="agent-card" onclick="window.open('demos/chess-demo.html', '_blank')">
                    <div class="agent-icon">♟️</div>
                    <h3>Chess</h3>
                    <p>Play interactive chess against AI opponents of varying skill levels</p>
                    <div class="agent-features">
                        <span class="feature">Strategy</span>
                        <span class="feature">AI Opponent</span>
                    </div>
                </div>
                
                <div class="agent-card" onclick="window.open('demos/checkers-demo.html', '_blank')">
                    <div class="agent-icon">🔴</div>
                    <h3>Checkers</h3>
                    <p>Strategic board game with jumping captures and AI strategy</p>
                    <div class="agent-features">
                        <span class="feature">Jumping</span>
                        <span class="feature">Captures</span>
                    </div>
                </div>
                
                <div class="agent-card" onclick="window.open('demos/mancala-demo.html', '_blank')">
                    <div class="agent-icon">🟤</div>
                    <h3>Mancala</h3>
                    <p>Ancient counting game with strategic depth and AI planning</p>
                    <div class="agent-features">
                        <span class="feature">Ancient</span>
                        <span class="feature">Counting</span>
                    </div>
                </div>
                
            </div>
        </div>
        
        <!-- Quick Games -->
        <div class="showcase-section">
            <h2 class="section-title">⚡ Quick Games</h2>
            <div class="agent-cards-grid">
                
                <div class="agent-card" onclick="window.open('demos/tictactoe-demo.html', '_blank')">
                    <div class="agent-icon">⭕</div>
                    <h3>Tic Tac Toe</h3>
                    <p>Quick 3x3 strategy game with perfect AI opponent</p>
                    <div class="agent-features">
                        <span class="feature">Perfect AI</span>
                        <span class="feature">Quick</span>
                    </div>
                </div>
                
                <div class="agent-card" onclick="window.open('demos/connect4-demo.html', '_blank')">
                    <div class="agent-icon">🎯</div>
                    <h3>Connect 4</h3>
                    <p>Classic connection game with strategic depth</p>
                    <div class="agent-features">
                        <span class="feature">Connection</span>
                        <span class="feature">Strategy</span>
                    </div>
                </div>
                
            </div>
        </div>
        
        <!-- Card & Social Games -->
        <div class="showcase-section">
            <h2 class="section-title">🃏 Card & Social Games</h2>
            <div class="agent-cards-grid">
                
                <div class="agent-card" onclick="window.open('demos/poker-demo.html', '_blank')">
                    <div class="agent-icon">🃏</div>
                    <h3>Poker (Hold'em)</h3>
                    <p>Texas Hold'em with betting, bluffing, and AI psychology</p>
                    <div class="agent-features">
                        <span class="feature">Bluffing</span>
                        <span class="feature">Psychology</span>
                    </div>
                </div>
                
                <div class="agent-card" onclick="window.open('demos/among_us-demo.html', '_blank')">
                    <div class="agent-icon">🚀</div>
                    <h3>Among Us</h3>
                    <p>Social deduction game with intelligent AI crewmates and imposters</p>
                    <div class="agent-features">
                        <span class="feature">Deduction</span>
                        <span class="feature">Social</span>
                    </div>
                </div>
                
                <div class="agent-card" onclick="window.open('demos/clue-demo.html', '_blank')">
                    <div class="agent-icon">🕵️</div>
                    <h3>Clue</h3>
                    <p>Mystery deduction game with logical reasoning and AI detective work</p>
                    <div class="agent-features">
                        <span class="feature">Mystery</span>
                        <span class="feature">Logic</span>
                    </div>
                </div>
                
            </div>
        </div>
        
        <!-- Economic Games -->
        <div class="showcase-section">
            <h2 class="section-title">💰 Economic Games</h2>
            <div class="agent-cards-grid">
                
                <div class="agent-card" onclick="window.open('demos/monopoly-demo.html', '_blank')">
                    <div class="agent-icon">🏨</div>
                    <h3>Monopoly</h3>
                    <p>Economic strategy with AI negotiation and property trading</p>
                    <div class="agent-features">
                        <span class="feature">Trading</span>
                        <span class="feature">Negotiation</span>
                    </div>
                </div>
                
            </div>
        </div>
        
    </div>

    <link rel="stylesheet" href="../_static/showcase.css">
    <script src="../_static/showcase.js"></script>

Game Categories
---------------

For detailed API documentation of all games, see :doc:`../api/haive-games`.

Quick Start
-----------

.. code-block:: python

   from haive.games.tic_tac_toe import TicTacToeGame
   from haive.games.tic_tac_toe.agent import TicTacToeAgent
   
   # Create game and agents
   game = TicTacToeGame()
   agent1 = TicTacToeAgent(name="Player 1", symbol="X")
   agent2 = TicTacToeAgent(name="Player 2", symbol="O")
   
   # Play!
   winner = await game.run(agent1, agent2)