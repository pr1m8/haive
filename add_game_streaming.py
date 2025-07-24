#!/usr/bin/env python3
"""Add game streaming content to all game demo pages."""

import os
from pathlib import Path

# Game states for different games
GAME_STATES = {
    "chess": """♜ ♞ ♝ ♛ ♚ ♝ ♞ ♜
♟ ♟ ♟ ♟ ♟ ♟ ♟ ♟
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
♙ ♙ ♙ ♙ ♙ ♙ ♙ ♙
♖ ♘ ♗ ♕ ♔ ♗ ♘ ♖

Turn: White | Move: 1
Status: Game in progress""",
    
    "checkers": """  b   b   b   b
b   b   b   b  
  b   b   b   b
.   .   .   .  
  .   .   .   .
r   r   r   r  
  r   r   r   r
r   r   r   r  

Turn: Red | Pieces: Red 12, Black 12
Status: Game in progress""",
    
    "tictactoe": """     |     |     
  X  |  O  |     
_____|_____|_____
     |     |     
     |  X  |     
_____|_____|_____
     |     |     
     |     |  O  
     |     |     

Turn: X | Move: 5
Status: Game in progress""",
    
    "mancala": """   [4] [4] [4] [4] [4] [4]
[0]                         [0]
   [4] [4] [4] [4] [4] [4]

Player 1: 0 | Player 2: 0
Turn: Player 1
Status: Game in progress""",
    
    "monopoly": """Board Position:
┌─────┬─────┬─────┬─────┬─────┐
│ GO  │ P1  │     │ P2  │ JAIL│
├─────┼─────┴─────┴─────┼─────┤
│     │   MONOPOLY      │     │
│ P3  │     BOARD       │ P4  │
├─────┼─────┬─────┬─────┼─────┤
│     │     │ P5  │     │     │
└─────┴─────┴─────┴─────┴─────┘

P1: $1500 | P2: $1450 | P3: $1600
Turn: Player 1 | Dice: Ready
Status: Game in progress""",
    
    "among_us": """Emergency Meeting Called!

Crewmates: 6
Imposters: 2
Tasks: 45% Complete

Discussion Phase
Time Remaining: 45s

Chat:
Red: "I saw Blue vent in Electrical!"
Blue: "No way, I was doing wires!"
Green: "I was with Yellow in MedBay"

Vote Status: Waiting..."""
}

MOVE_HISTORIES = {
    "chess": """<div class="move">1. e4 e5</div>
                    <div class="move">2. Nf3 Nc6</div>
                    <div class="move">3. Bb5 a6</div>""",
    
    "checkers": """<div class="move">1. Red: c3-d4</div>
                    <div class="move">2. Black: f6-e5</div>
                    <div class="move">3. Red: d4xf6</div>""",
    
    "tictactoe": """<div class="move">1. X: Center (5)</div>
                    <div class="move">2. O: Top-Middle (2)</div>
                    <div class="move">3. X: Bottom-Right (9)</div>""",
    
    "mancala": """<div class="move">1. P1: Pit 3 → 4 seeds</div>
                    <div class="move">2. P2: Pit 5 → 4 seeds</div>
                    <div class="move">3. P1: Pit 1 → 4 seeds</div>""",
    
    "monopoly": """<div class="move">1. P1: Rolled 7, landed on Baltic Ave</div>
                    <div class="move">2. P2: Rolled 5, bought Vermont Ave</div>
                    <div class="move">3. P3: Rolled 12, passed GO</div>""",
    
    "among_us": """<div class="move">1. Emergency Meeting called by Red</div>
                    <div class="move">2. Blue voted for Red</div>
                    <div class="move">3. Green voted for Blue</div>"""
}

def add_streaming_content(file_path, game_name):
    """Add streaming content to a game demo file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Check if streaming content already exists
    if "Live Game Stream" in content or "game-streaming" in content:
        print(f"Skipping {file_path} - already has streaming content")
        return
    
    # Get game state and moves
    state = GAME_STATES.get(game_name, GAME_STATES["chess"])
    moves = MOVE_HISTORIES.get(game_name, MOVE_HISTORIES["chess"])
    
    # Find where to insert the streaming content
    streaming_content = f'''
        <!-- Live Game Stream -->
        <div class="game-streaming">
            <h3>Live Game Visualization</h3>
            <div class="streaming-indicator">
                Live Stream
            </div>
            <div class="game-state-display">
                <pre id="{game_name}-state">
{state}
                </pre>
            </div>
            <div class="move-history">
                <h4>Move History</h4>
                <div id="{game_name}-moves-stream">
                    {moves}
                </div>
            </div>
        </div>'''
    
    # Find the closing div of game-demo-container
    insert_pos = content.rfind("</div>", 0, content.rfind("</div>"))
    
    if insert_pos > 0:
        new_content = content[:insert_pos] + streaming_content + "\n    " + content[insert_pos:]
        
        with open(file_path, 'w') as f:
            f.write(new_content)
        
        print(f"Updated {file_path} with streaming content")
    else:
        print(f"Could not find insertion point in {file_path}")

def main():
    """Process all game demo files."""
    demos_dir = Path("docs/source/games/demos")
    
    # Map of file names to game names
    game_files = {
        "chess-demo.rst": "chess",
        "checkers-demo.rst": "checkers",
        "tictactoe-demo.rst": "tictactoe",
        "mancala-demo.rst": "mancala",
        "monopoly-demo.rst": "monopoly",
        "among_us-demo.rst": "among_us"
    }
    
    for file_name, game_name in game_files.items():
        file_path = demos_dir / file_name
        if file_path.exists():
            add_streaming_content(file_path, game_name)
        else:
            print(f"File not found: {file_path}")

if __name__ == "__main__":
    main()