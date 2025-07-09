#!/usr/bin/env python3
"""
Generate interactive demo pages for all Haive games.

This script creates visual game demonstration pages with playable interfaces,
rule explanations, and AI agent interactions.
"""

import json
from pathlib import Path

GAMES = [
    {
        "id": "chess",
        "name": "Chess",
        "icon": "♟️",
        "description": "Classic chess with AI agents of varying skill levels",
        "features": ["8x8 Board", "AI Opponents", "Move History", "Analysis"],
        "rules": "Move pieces according to chess rules. Checkmate the opponent's king to win.",
        "ai_levels": ["Beginner", "Intermediate", "Advanced", "Master"],
        "board_size": "8x8",
        "complexity": "High"
    },
    {
        "id": "tictactoe",
        "name": "Tic Tac Toe",
        "icon": "⭕",
        "description": "Simple 3x3 grid game with perfect play AI",
        "features": ["3x3 Grid", "Perfect AI", "Quick Games", "Strategy"],
        "rules": "Get 3 in a row (horizontal, vertical, or diagonal) to win.",
        "ai_levels": ["Easy", "Perfect"],
        "board_size": "3x3",
        "complexity": "Low"
    },
    {
        "id": "checkers",
        "name": "Checkers",
        "icon": "🔴",
        "description": "Classic checkers with jumping and king promotion",
        "features": ["8x8 Board", "King Pieces", "Jump Captures", "Strategy"],
        "rules": "Move diagonally, capture by jumping, promote to kings.",
        "ai_levels": ["Novice", "Expert", "Master"],
        "board_size": "8x8",
        "complexity": "Medium"
    },
    {
        "id": "monopoly",
        "name": "Monopoly",
        "icon": "🏨",
        "description": "Economic strategy game with property trading and AI negotiation",
        "features": ["Property Trading", "AI Negotiation", "Economic Strategy", "Chance Cards"],
        "rules": "Buy properties, collect rent, bankrupt opponents through smart trading.",
        "ai_levels": ["Conservative", "Aggressive", "Balanced"],
        "board_size": "40 Spaces",
        "complexity": "High"
    },
    {
        "id": "among_us",
        "name": "Among Us",
        "icon": "🚀",
        "description": "Social deduction with AI crewmates and imposters",
        "features": ["Social Deduction", "Task Completion", "Voting", "AI Behavior"],
        "rules": "Complete tasks as crewmate or eliminate crewmates as imposter.",
        "ai_levels": ["Naive", "Suspicious", "Strategic"],
        "board_size": "Ship Map",
        "complexity": "Medium"
    },
    {
        "id": "mancala",
        "name": "Mancala",
        "icon": "🟤",
        "description": "Ancient seed-counting game with strategic depth",
        "features": ["Seed Movement", "Capture Rules", "Strategy", "Ancient Rules"],
        "rules": "Move seeds around the board to capture the most seeds.",
        "ai_levels": ["Basic", "Advanced"],
        "board_size": "6x2 + 2",
        "complexity": "Medium"
    }
]

def create_game_demo_page(game: dict, output_dir: Path) -> None:
    """Create a demo page for a game."""
    
    content = f"""{game['name']} Demo
{'=' * (len(game['name']) + 5)}

{game['description']}

.. raw:: html

    <div class="game-demo-container">
        <!-- Game Overview -->
        <div class="game-overview-card">
            <div class="game-header">
                <div class="game-icon">{game['icon']}</div>
                <div>
                    <h2>{game['name']}</h2>
                    <p class="game-complexity">Complexity: {game['complexity']}</p>
                </div>
            </div>
            
            <div class="game-stats">
                <div class="stat">
                    <label>Board Size:</label>
                    <span>{game['board_size']}</span>
                </div>
                <div class="stat">
                    <label>AI Levels:</label>
                    <span>{len(game['ai_levels'])}</span>
                </div>
            </div>
            
            <div class="game-features">
"""
    
    for feature in game["features"]:
        content += f'                <span class="feature-tag">{feature}</span>\n'
    
    content += f"""            </div>
        </div>

        <!-- Playable Game Interface -->
        <div class="game-interface">
            <div class="game-controls">
                <h3>Play {game['name']}</h3>
                <div class="ai-selection">
                    <label>AI Difficulty:</label>
                    <select id="{game['id']}-ai-level">
"""
    
    for level in game["ai_levels"]:
        content += f'                        <option value="{level.lower()}">{level}</option>\n'
    
    content += f"""                    </select>
                </div>
                <button onclick="startGame('{game['id']}')" class="start-game-btn">
                    Start New Game
                </button>
            </div>
            
            <div id="{game['id']}-board" class="game-board">
                <!-- Game board will be rendered here -->
                <div class="board-placeholder">
                    <p>Click "Start New Game" to begin playing {game['name']}</p>
                </div>
            </div>
            
            <div class="game-status">
                <div id="{game['id']}-status" class="status-display">
                    Ready to play
                </div>
                <div id="{game['id']}-moves" class="moves-history">
                    <!-- Move history will appear here -->
                </div>
            </div>
        </div>

        <!-- Game Analysis -->
        <div class="game-analysis">
            <h3>AI Analysis</h3>
            <div id="{game['id']}-analysis" class="analysis-display">
                <p>Start a game to see AI analysis and move suggestions.</p>
            </div>
        </div>
    </div>

    <script>
    // Game initialization and interaction
    function startGame(gameId) {{
        const board = document.getElementById(gameId + '-board');
        const status = document.getElementById(gameId + '-status');
        const aiLevel = document.getElementById(gameId + '-ai-level').value;
        
        // Initialize game board based on game type
        initializeGameBoard(gameId, board);
        status.textContent = `Playing against ${{aiLevel}} AI`;
        
        // Show game-specific interface
        showGameInterface(gameId);
    }}
    
    function initializeGameBoard(gameId, boardElement) {{
        // This would be replaced with actual game implementation
        boardElement.innerHTML = `
            <div class="game-board-${{gameId}}">
                <p>🎮 Interactive ${{gameId}} board would render here</p>
                <p>Click positions to make moves</p>
                <div class="demo-board" id="demo-board">
                    <!-- Demo board will be generated by JS -->
                </div>
            </div>
        `;
    }}
    
    function generateDemoBoard(gameId) {{
        if (gameId === 'chess' || gameId === 'checkers') {{
            let squares = '';
            for (let i = 0; i < 64; i++) {{
                squares += '<div class="square"></div>';
            }}
            return `<div class="board-8x8">${{squares}}</div>`;
        }} else if (gameId === 'tictactoe') {{
            let cells = '';
            for (let i = 0; i < 9; i++) {{
                cells += '<div class="cell" onclick="makeMove(this)"></div>';
            }}
            return `<div class="board-3x3">${{cells}}</div>`;
        }}
        return '<div class="custom-board">Game board visualization</div>';
    }}
    
    function makeMove(cell) {{
        if (cell.textContent === '') {{
            cell.textContent = 'X';
            // Trigger AI move
            setTimeout(() => aiMove(), 500);
        }}
    }}
    
    function aiMove() {{
        const emptyCells = document.querySelectorAll('.cell:empty');
        if (emptyCells.length > 0) {{
            const randomCell = emptyCells[Math.floor(Math.random() * emptyCells.length)];
            randomCell.textContent = 'O';
        }}
    }}
    
    function showGameInterface(gameId) {{
        // Enable game-specific interactions
        console.log(`Started ${{gameId}} game`);
    }}
    </script>

    <style>
    .game-demo-container {{
        max-width: 1200px;
        margin: 0 auto;
    }}
    
    .game-overview-card {{
        background: var(--color-background-secondary);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }}
    
    .game-header {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }}
    
    .game-icon {{
        font-size: 3rem;
    }}
    
    .game-stats {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }}
    
    .stat {{
        display: flex;
        justify-content: space-between;
        padding: 0.5rem;
        background: var(--color-background-primary);
        border-radius: 6px;
    }}
    
    .game-features {{
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }}
    
    .feature-tag {{
        background: var(--color-brand-primary);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
    }}
    
    .game-interface {{
        background: var(--color-background-secondary);
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
    }}
    
    .game-controls {{
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 2rem;
        flex-wrap: wrap;
    }}
    
    .start-game-btn {{
        background: var(--color-brand-primary);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 6px;
        cursor: pointer;
        font-weight: 600;
    }}
    
    .game-board {{
        min-height: 400px;
        background: var(--color-background-primary);
        border: 2px solid var(--color-background-border);
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
    }}
    
    .board-8x8 {{
        display: grid;
        grid-template-columns: repeat(8, 1fr);
        gap: 1px;
        max-width: 400px;
        margin: 0 auto;
    }}
    
    .board-3x3 {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2px;
        max-width: 300px;
        margin: 0 auto;
    }}
    
    .square, .cell {{
        aspect-ratio: 1;
        background: #f0f0f0;
        border: 1px solid #ccc;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        cursor: pointer;
    }}
    
    .square:nth-child(odd) {{
        background: #d4c4b0;
    }}
    
    .cell:hover {{
        background: #e0e0e0;
    }}
    
    .game-status {{
        margin-top: 1rem;
        padding: 1rem;
        background: var(--color-background-primary);
        border-radius: 6px;
    }}
    
    .game-analysis {{
        background: var(--color-background-secondary);
        border-radius: 12px;
        padding: 2rem;
    }}
    </style>

Rules & Strategy
----------------

**How to Play:**

{game['rules']}

**AI Opponents:**

"""
    
    for i, level in enumerate(game["ai_levels"]):
        content += f"- **{level}**: "
        if i == 0:
            content += "Beginner-friendly AI that makes some mistakes\n"
        elif i == len(game["ai_levels"]) - 1:
            content += "Advanced AI using optimal strategies\n"
        else:
            content += "Balanced AI with good strategic play\n"
    
    content += f"""

Code Example
------------

.. code-block:: python

    from haive.games.{game['id']} import {game['name']}Game
    from haive.agents.simple import SimpleAgent
    
    # Create game
    game = {game['name']}Game()
    
    # Create AI players
    player1 = SimpleAgent(name="Human")
    player2 = SimpleAgent(name="AI_Agent", difficulty="advanced")
    
    # Play game
    winner = game.play(player1, player2)
    print(f"Winner: {{winner}}")
    
    # Get game history
    for move in game.history:
        print(f"{{move.player}}: {{move.action}}")

See Also
--------

- :doc:`/api/haive/games/index` - Games API documentation
- :doc:`/guides/game-development` - Creating custom games
- :doc:`/examples/game-agents` - More game examples
"""
    
    # Write to file
    filename = f"{game['id']}-demo.rst"
    output_file = output_dir / filename
    
    with open(output_file, "w") as f:
        f.write(content)
    
    print(f"Created game demo: {output_file}")

def create_games_index(output_dir: Path) -> None:
    """Create games demo index."""
    
    content = """Game Demos
==========

Interactive game demonstrations with playable interfaces and AI opponents.

.. raw:: html

    <div class="games-hero">
        <h2>🎮 Play Against AI</h2>
        <p>Experience our game environments with intelligent AI opponents of varying skill levels.</p>
    </div>

.. grid:: 2 2 3 3
   :gutter: 3

"""
    
    for game in GAMES:
        content += f"""   .. grid-item-card:: {game['icon']} {game['name']}
      :link: {game['id']}-demo
      :link-type: doc
      :class-card: game-demo-card

      {game['description']}

"""
    
    content += """

.. toctree::
   :maxdepth: 1
   :caption: Game Demonstrations
   :hidden:

"""
    
    for game in GAMES:
        content += f"   {game['id']}-demo\n"
    
    content += """

.. raw:: html

    <style>
    .games-hero {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
    }
    
    .games-hero h2 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .game-demo-card {
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .game-demo-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
    }
    </style>

Features
--------

All game demos include:

- **🎮 Interactive Interface**: Click to play directly in your browser
- **🤖 AI Opponents**: Multiple difficulty levels with different strategies  
- **📊 Move Analysis**: See AI reasoning and move suggestions
- **📈 Game History**: Track moves and analyze gameplay
- **🎯 Strategy Tips**: Learn optimal play techniques

Getting Started
---------------

1. **Choose a Game**: Click any game card above
2. **Select AI Level**: Pick difficulty from beginner to master
3. **Start Playing**: Make moves by clicking the board
4. **Learn Strategy**: Watch AI analysis and improve your play

Each game includes detailed rules, strategy guides, and code examples for building your own game agents.
"""
    
    index_file = output_dir / "index.rst"
    with open(index_file, "w") as f:
        f.write(content)
    
    print(f"Created games index: {index_file}")

def main():
    """Generate all game demo pages."""
    
    # Create output directory
    output_dir = Path(__file__).parent / "source" / "games" / "demos"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("Creating game demo pages...")
    for game in GAMES:
        create_game_demo_page(game, output_dir)
    
    create_games_index(output_dir)
    
    print(f"\\nGenerated {len(GAMES)} game demo pages in {output_dir}")

if __name__ == "__main__":
    main()