#!/usr/bin/env python3
"""Generate demo pages for ALL games in the haive-games package."""

import os
from pathlib import Path

# Game configurations with proper display names and descriptions
GAMES = {
    "battleship": {
        "name": "Battleship",
        "icon": "🚢",
        "description": "Naval strategy game with hidden ship placement",
        "complexity": "Medium",
        "board": "10x10 grids",
        "features": ["Ship placement", "Strategic guessing", "Hit tracking", "AI opponents"],
        "state": """  A B C D E F G H I J        A B C D E F G H I J
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
X=Hit, O=Miss, ?=Unknown"""
    },
    "clue": {
        "name": "Clue (Cluedo)",
        "icon": "🔍",
        "description": "Mystery deduction game to solve the murder",
        "complexity": "High",
        "board": "Mansion layout",
        "features": ["Deduction", "Movement", "Accusations", "Note-taking"],
        "state": """╔═══════╦═══════╦═══════╦═══════╗
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
Suggestions made: 2"""
    },
    "connect4": {
        "name": "Connect Four",
        "icon": "🔴",
        "description": "Drop discs to connect four in a row",
        "complexity": "Low",
        "board": "7x6 grid",
        "features": ["Gravity mechanics", "Strategic placement", "Quick games", "AI levels"],
        "state": """┌─┬─┬─┬─┬─┬─┬─┐
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

Turn: Red | Moves: 9"""
    },
    "debate": {
        "name": "Debate",
        "icon": "💬",
        "description": "AI agents engage in structured debates",
        "complexity": "High",
        "board": "N/A",
        "features": ["Arguments", "Rebuttals", "Judging", "Topics"],
        "state": """Topic: "AI will create more jobs than it eliminates"

PRO (Agent A): Opening Statement
"AI augments human capabilities, creating new industries..."

CON (Agent B): Opening Statement  
"Historical automation has consistently reduced employment..."

Round: 1/3 | Phase: Rebuttals
Time remaining: 45s"""
    },
    "dominoes": {
        "name": "Dominoes",
        "icon": "🁯",
        "description": "Classic tile-matching game",
        "complexity": "Medium",
        "board": "Chain layout",
        "features": ["Tile matching", "Strategic blocking", "Scoring", "Multiple variants"],
        "state": """Current Chain:
[2|5]─[5|5]─[5|3]─[3|1]─[1|6]─[6|6]─[6|4]

Player 1 Hand: 7 tiles
Player 2 Hand: 5 tiles
Boneyard: 12 tiles

Last Play: P2 played [6|4]
Current Turn: Player 1"""
    },
    "fox_and_geese": {
        "name": "Fox and Geese",
        "icon": "🦊",
        "description": "Asymmetric strategy game",
        "complexity": "Medium",
        "board": "Cross-shaped",
        "features": ["Asymmetric play", "Capture mechanics", "Strategic movement", "Classic rules"],
        "state": """    . G .
    G G G
. . G G G . .
G G G F G G G
. . G G G . .
    G G G
    . G .

F = Fox, G = Goose
Fox Turn | Geese captured: 2"""
    },
    "go": {
        "name": "Go",
        "icon": "⚫",
        "description": "Ancient strategic board game",
        "complexity": "Very High",
        "board": "19x19 grid",
        "features": ["Territory control", "Capture", "Ko rule", "Handicap system"],
        "state": """   A B C D E F G H J
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
Turn: Black | Move: 45"""
    },
    "hold_em": {
        "name": "Texas Hold'em",
        "icon": "🃏",
        "description": "Popular poker variant",
        "complexity": "High",
        "board": "N/A",
        "features": ["Betting", "Bluffing", "Hand rankings", "Tournament play"],
        "state": """Community Cards: [A♠] [K♦] [Q♦] [10♣] [?]

Pot: $450
Current Bet: $100

Player 1: [?][?] | Stack: $980 | Action: Call
Player 2: [?][?] | Stack: $1200 | Action: Raise $200
Player 3: FOLDED
Player 4: [?][?] | Stack: $750 | Action: ?

Phase: Turn | To call: $100"""
    },
    "mafia": {
        "name": "Mafia",
        "icon": "🕵️",
        "description": "Social deduction party game",
        "complexity": "Medium",
        "board": "N/A",
        "features": ["Role playing", "Deduction", "Voting", "Special abilities"],
        "state": """Day 3 - Discussion Phase

Alive Players:
- Player 1 (?)
- Player 3 (?)
- Player 5 (?)
- Player 7 (?)
- Player 8 (?)

Eliminated:
- Player 2 (Villager) - Night 1
- Player 4 (Detective) - Voted Day 2
- Player 6 (Villager) - Night 2

Time until vote: 2:30"""
    },
    "mastermind": {
        "name": "Mastermind",
        "icon": "🎯",
        "description": "Code-breaking logic game",
        "complexity": "Medium",
        "board": "N/A",
        "features": ["Deduction", "Pattern recognition", "Feedback system", "Limited guesses"],
        "state": """Secret Code: [?][?][?][?]

Guess History:
1. [R][B][G][Y] → ●●○○
2. [B][R][Y][G] → ●○○
3. [B][G][R][Y] → ●●●○
4. [B][G][Y][R] → ●●●●

● = Correct position
○ = Correct color, wrong position

Guesses remaining: 6"""
    },
    "nim": {
        "name": "Nim",
        "icon": "🎮",
        "description": "Mathematical strategy game",
        "complexity": "Low",
        "board": "N/A",
        "features": ["Perfect strategy", "Multiple variants", "Quick games", "Mathematical basis"],
        "state": """Heap A: ||||| (5)
Heap B: ||| (3)
Heap C: |||||||| (8)
Heap D: || (2)

Last move: Player 1 took 3 from Heap C
Current turn: Player 2

Classic rules: Take any number from one heap
Goal: Force opponent to take last object"""
    },
    "poker": {
        "name": "Poker",
        "icon": "♠️",
        "description": "Classic card game with multiple variants",
        "complexity": "High",
        "board": "N/A",
        "features": ["Multiple variants", "Betting", "Hand rankings", "Tournaments"],
        "state": """5-Card Draw

Your Hand: [K♠][K♥][7♦][7♣][A♠]

Pot: $320
Current Bet: $50

Actions:
- Player 1: Bet $50
- Player 2: Call $50
- Player 3: Fold
- You: ?

Draw Phase | Cards to exchange: ?"""
    },
    "reversi": {
        "name": "Reversi (Othello)",
        "icon": "⚪",
        "description": "Disc-flipping strategy game",
        "complexity": "Medium",
        "board": "8x8 grid",
        "features": ["Disc flipping", "Corner strategy", "Mobility", "Endgame counting"],
        "state": """  A B C D E F G H
1 . . . . . . . .
2 . . . . . . . .
3 . . . ● . . . .
4 . . ● ● ● . . .
5 . . . ● ○ . . .
6 . . . . . . . .
7 . . . . . . . .
8 . . . . . . . .

Black: 5 | White: 1
Turn: White
Valid moves: C5, E3, E5"""
    },
    "risk": {
        "name": "Risk",
        "icon": "🗺️",
        "description": "Global domination strategy game",
        "complexity": "High",
        "board": "World map",
        "features": ["Territory control", "Army management", "Dice battles", "Alliances"],
        "state": """North America: P1 (12 armies)
South America: P2 (8 armies)
Europe: P3 (15 armies)
Africa: P1 (10 armies)
Asia: P4 (22 armies)
Australia: P2 (6 armies)

Current Phase: Reinforcement
Player 1 Turn
Armies to place: 7
Cards in hand: 2"""
    },
    "tic_tac_toe": {
        "name": "Tic Tac Toe",
        "icon": "❌",
        "description": "Classic 3x3 grid game",
        "complexity": "Low",
        "board": "3x3 grid",
        "features": ["Simple rules", "Perfect play", "Quick games", "Learning aid"],
        "state": """     |     |     
  X  |  O  |     
_____|_____|_____
     |     |     
     |  X  |     
_____|_____|_____
     |     |     
     |     |  O  
     |     |     

Turn: X | Move: 5"""
    }
}

def generate_game_demo(game_key, game_info):
    """Generate RST content for a game demo page."""
    
    features_list = "\n".join([f'                <span class="feature-tag">{feature}</span>' for feature in game_info["features"]])
    
    content = f"""{game_info["name"]} Demo
{'=' * (len(game_info["name"]) + 5)}

{game_info["description"]}

.. raw:: html

    <div class="game-demo-container">
        <!-- Game Overview -->
        <div class="game-overview-card">
            <div class="game-header">
                <div class="game-icon">{game_info["icon"]}</div>
                <div>
                    <h2>{game_info["name"]}</h2>
                    <p class="game-complexity">Complexity: {game_info["complexity"]}</p>
                </div>
            </div>

            <div class="game-stats">
                <div class="stat">
                    <label>Board Size:</label>
                    <span>{game_info["board"]}</span>
                </div>
                <div class="stat">
                    <label>Players:</label>
                    <span>2-4</span>
                </div>
            </div>

            <div class="game-features">
{features_list}
            </div>
        </div>

        <!-- Playable Game Interface -->
        <div class="game-interface">
            <div class="game-controls">
                <h3>Play {game_info["name"]}</h3>
                <div class="ai-selection">
                    <label>AI Difficulty:</label>
                    <select id="{game_key}-ai-level">
                        <option value="beginner">Beginner</option>
                        <option value="intermediate">Intermediate</option>
                        <option value="advanced">Advanced</option>
                        <option value="master">Master</option>
                    </select>
                </div>
                <button onclick="startGame('{game_key}')" class="start-game-btn">
                    Start New Game
                </button>
            </div>

            <div id="{game_key}-board" class="game-board">
                <!-- Game board will be rendered here -->
                <div class="board-placeholder">
                    <p>Click "Start New Game" to begin playing {game_info["name"]}</p>
                </div>
            </div>

            <div class="game-status">
                <div id="{game_key}-status" class="status-display">
                    Ready to play
                </div>
                <div id="{game_key}-moves" class="moves-history">
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
                <pre id="{game_key}-state">
{game_info["state"]}
                </pre>
            </div>
            <div class="move-history">
                <h4>Recent Activity</h4>
                <div id="{game_key}-moves-stream">
                    <div class="move">Game initialized...</div>
                    <div class="move">Waiting for players...</div>
                </div>
            </div>
        </div>
    </div>

Rules & Strategy
----------------

**How to Play:**

Learn the rules and strategies for {game_info["name"]}.

**AI Opponents:**

- **Beginner**: Perfect for learning the game
- **Intermediate**: Provides a moderate challenge
- **Advanced**: Strong strategic play
- **Master**: Expert-level AI

Code Example
------------

.. code-block:: python

    from haive.games.{game_key} import {game_info["name"].replace(" ", "")}Game
    from haive.agents.simple import SimpleAgent

    # Create game
    game = {game_info["name"].replace(" ", "")}Game()

    # Create AI players
    player1 = SimpleAgent(name="Player1")
    player2 = SimpleAgent(name="AI_Player", difficulty="advanced")

    # Play game
    winner = game.play(player1, player2)
    print(f"Winner: {{winner}}")

See Also
--------

- :doc:`/api/haive/games/index` - Games API documentation
- :doc:`/guides/game-development` - Creating custom games
- :doc:`/examples/game-agents` - More game examples
"""
    
    return content

def main():
    """Generate demo pages for all games."""
    demos_dir = Path("docs/source/games/demos")
    demos_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate individual game demos
    for game_key, game_info in GAMES.items():
        if game_key == "tic_tac_toe":
            filename = "tictactoe-demo.rst"  # Special case for existing file
        else:
            filename = f"{game_key}-demo.rst"
        
        filepath = demos_dir / filename
        
        # Skip if already has streaming content
        if filepath.exists():
            with open(filepath, 'r') as f:
                if "Live Game Stream" in f.read():
                    print(f"✓ {filename} already has streaming content")
                    continue
        
        content = generate_game_demo(game_key, game_info)
        
        with open(filepath, 'w') as f:
            f.write(content)
        
        print(f"✓ Generated {filename}")
    
    # Update the games index
    update_games_index()
    
    print("\n✅ All game demos generated!")

def update_games_index():
    """Update the games demos index page."""
    index_content = """Game Demos
==========

Interactive game demonstrations with playable interfaces and AI opponents.

.. grid:: 1 2 3 3
   :gutter: 3

"""
    
    for game_key, game_info in sorted(GAMES.items(), key=lambda x: x[1]["name"]):
        if game_key == "tic_tac_toe":
            link = "tictactoe-demo"
        else:
            link = f"{game_key}-demo"
            
        index_content += f"""   .. grid-item-card:: {game_info["icon"]} {game_info["name"]}
      :link: {link}
      :link-type: doc

      {game_info["description"]}

      **Complexity**: {game_info["complexity"]}

"""
    
    index_content += """

.. toctree::
   :maxdepth: 1
   :hidden:

"""
    
    for game_key in sorted(GAMES.keys()):
        if game_key == "tic_tac_toe":
            index_content += "   tictactoe-demo\n"
        else:
            index_content += f"   {game_key}-demo\n"
    
    with open("docs/source/games/demos/index.rst", 'w') as f:
        f.write(index_content)
    
    print("✓ Updated games demos index")

if __name__ == "__main__":
    main()