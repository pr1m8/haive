#!/usr/bin/env python3
"""Simple documentation generator for haive-games without external dependencies.

This script generates:
1. Text-based agent architecture diagrams
2. Example run templates for each game
3. Game-specific documentation
4. State history templates

No external dependencies required - uses only Python standard library.
"""

import json
import sys

# Standard library imports
from datetime import datetime
from pathlib import Path
from typing import Any


class SimpleGameDocumentationGenerator:
    """Generates simple documentation without external dependencies."""

    def __init__(self, output_dir: str = "docs/simple_generated"):
        """Initialize the documentation generator."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.architectures_dir = self.output_dir / "architectures"
        self.examples_dir = self.output_dir / "examples"
        self.templates_dir = self.output_dir / "templates"

        for dir_path in [self.architectures_dir, self.examples_dir, self.templates_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.games = self._discover_games()
        print(f"Discovered {len(self.games)} games: {list(self.games.keys())}")

    def _discover_games(self) -> dict[str, dict[str, Any]]:
        """Discover all available games."""
        games_dir = Path("src/haive/games")
        games = {}

        if not games_dir.exists():
            print(f"Games directory not found: {games_dir}")
            return {}

        for game_dir in games_dir.iterdir():
            if not game_dir.is_dir() or game_dir.name.startswith("."):
                continue

            game_name = game_dir.name
            agent_file = game_dir / "agent.py"

            if agent_file.exists():
                games[game_name] = {
                    "path": game_dir,
                    "agent_file": agent_file,
                    "has_agent": True,
                    "complexity": self._assess_complexity(game_dir),
                }

        return games

    def _assess_complexity(self, game_dir: Path) -> str:
        """Assess game complexity based on file structure."""
        files = list(game_dir.glob("*.py"))

        if len(files) >= 8:
            return "high"
        elif len(files) >= 5:
            return "medium"
        else:
            return "low"

    def generate_text_architecture(self, game_name: str) -> Path | None:
        """Generate text-based architecture diagram for a game."""
        print(f"Generating architecture diagram for {game_name}")

        game_info = self.games.get(game_name)
        if not game_info:
            return None

        # Create text-based architecture
        architecture_content = self._create_architecture_text(game_name, game_info)
        output_path = self.architectures_dir / f"{game_name}_architecture.txt"

        with open(output_path, "w") as f:
            f.write(architecture_content)

        print(f"Generated architecture: {output_path}")
        return output_path

    def _create_architecture_text(
        self, game_name: str, game_info: dict[str, Any]
    ) -> str:
        """Create text-based architecture diagram."""
        game_path = game_info["path"]
        complexity = game_info["complexity"]

        # Get file list
        python_files = [
            f.name for f in game_path.glob("*.py") if not f.name.startswith("__")
        ]

        architecture = f"""
# {game_name.upper()} GAME ARCHITECTURE

Generated: {datetime.now().isoformat()}
Complexity: {complexity.upper()}

## File Structure
```
{game_name}/
"""

        for file in sorted(python_files):
            architecture += f"├── {file}\n"

        architecture += """```

## Agent Flow Diagram
```
    ┌─────────────────┐
    │   Game Start    │
    └─────────┬───────┘
              │
    ┌─────────▼───────┐
    │  Initialize     │
    │  Game State     │
    └─────────┬───────┘
              │
    ┌─────────▼───────┐
    │  Process Move   │◄─────┐
    └─────────┬───────┘      │
              │              │
    ┌─────────▼───────┐      │
    │  Validate Move  │      │
    └─────────┬───────┘      │
              │              │
    ┌─────────▼───────┐      │
    │  Update State   │      │
    └─────────┬───────┘      │
              │              │
    ┌─────────▼───────┐      │
    │  Check End      │      │
    └─────────┬───────┘      │
              │              │
              ├──────────────┘
              │ Continue
              │
    ┌─────────▼───────┐
    │   Game Over     │
    └─────────────────┘
```

## Component Responsibilities
"""

        # Add component descriptions based on common patterns
        if "models.py" in python_files:
            architecture += """
### models.py
- Game data structures (Player, Move, State)
- Pydantic models for validation
- Enums for game constants
"""

        if "state.py" in python_files:
            architecture += """
### state.py
- Game state management
- State transitions
- State validation
"""

        if "state_manager.py" in python_files:
            architecture += """
### state_manager.py
- Game logic implementation
- Move processing
- Rule enforcement
"""

        if "agent.py" in python_files:
            architecture += """
### agent.py
- Main agent implementation
- LangGraph workflow setup
- Agent coordination
"""

        if "config.py" in python_files:
            architecture += """
### config.py
- Game configuration
- Agent settings
- Parameter management
"""

        architecture += """

## Game-Specific Features
"""

        # Add game-specific features based on game type
        game_features = self._get_game_features(game_name)
        for feature in game_features:
            architecture += f"- {feature}\n"

        return architecture

    def _get_game_features(self, game_name: str) -> list[str]:
        """Get game-specific features."""
        feature_map = {
            "chess": [
                "Piece movement validation",
                "Check/checkmate detection",
                "Special moves (castling, en passant)",
                "Turn-based gameplay",
            ],
            "go": [
                "Territory control",
                "Capture logic",
                "Ko rule enforcement",
                "Scoring system",
            ],
            "poker": [
                "Hand evaluation",
                "Betting rounds",
                "Card dealing",
                "Showdown logic",
            ],
            "mafia": [
                "Role-based gameplay",
                "Night/day phases",
                "Voting mechanics",
                "Social deduction",
            ],
            "reversi": [
                "Piece flipping",
                "Valid move calculation",
                "Strategic analysis",
                "Corner control",
            ],
            "tic_tac_toe": [
                "Simple grid management",
                "Win condition checking",
                "Move validation",
            ],
            "connect4": [
                "Column-based movement",
                "Gravity simulation",
                "Line detection",
                "Strategic analysis",
            ],
        }

        return feature_map.get(
            game_name,
            [
                "Standard game mechanics",
                "Move validation",
                "State management",
                "End condition checking",
            ],
        )

    def generate_example_template(self, game_name: str) -> Path | None:
        """Generate example run template for a game."""
        print(f"Generating example template for {game_name}")

        example_content = self._create_example_template(game_name)
        output_path = self.examples_dir / f"{game_name}_example_template.py"

        with open(output_path, "w") as f:
            f.write(example_content)

        print(f"Generated example: {output_path}")
        return output_path

    def _create_example_template(self, game_name: str) -> str:
        """Create example run template."""
        template = f'''#!/usr/bin/env python3
"""Example template for {game_name.title()} game.

This template demonstrates:
1. Basic game setup and initialization
2. Move processing and state updates
3. State history tracking for documentation
4. Game completion handling

Usage:
    python {game_name}_example_template.py

Generated: {datetime.now().isoformat()}
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the project root to Python path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def main():
    """Main example execution."""
    print(f"\\n{"=" * 60}")
    print(f"{game_name.upper()} GAME EXAMPLE")
    print(f"{"=" * 60}")

    # Initialize state history tracking
    state_history = []
    move_count = 0

    try:
        # Import game components
        print("Importing game components...")
        # Note: Actual imports would depend on the specific game structure
        # from haive.games.{game_name}.agent import {game_name.title()}Agent
        # from haive.games.{game_name}.models import *

        print("✅ Game components imported successfully")

        # Initialize game
        print("\\nInitializing game...")
        # agent = {game_name.title()}Agent()
        # initial_state = agent.initialize_game()

        # For template purposes, create a mock initial state
        initial_state = {{
            "game": "{game_name}",
            "players": ["Player1", "Player2"],
            "current_player": "Player1",
            "game_over": False,
            "move_number": 0
        }}

        state_history.append({{
            "move": 0,
            "timestamp": datetime.now().isoformat(),
            "description": "Game initialized",
            "state": initial_state.copy()
        }})

        print(f"✅ Game initialized with {{len(initial_state.get('players', []))}} players")

        # Simulate game moves
        print("\\nStarting game simulation...")
        current_state = initial_state.copy()

        for move_num in range(1, 6):  # Simulate 5 moves
            print(f"\\n--- Move {{move_num}} ---")

            current_player = current_state.get("current_player")
            print(f"Current player: {{current_player}}")

            # Simulate move processing
            # In a real implementation, this would call:
            # move = get_player_move(current_player)
            # result = agent.process_move(current_state, move)
            # current_state = result.update

            # Mock move for template
            mock_move = {{
                "player": current_player,
                "action": f"move_{{move_num}}",
                "timestamp": datetime.now().isoformat()
            }}

            # Update state
            current_state["move_number"] = move_num
            current_state["current_player"] = "Player2" if current_player == "Player1" else "Player1"

            # Check for game end (mock logic)
            if move_num >= 4:
                current_state["game_over"] = True
                current_state["winner"] = "Player1"

            # Record state
            state_history.append({{
                "move": move_num,
                "timestamp": datetime.now().isoformat(),
                "description": f"Move by {{current_player}}",
                "move_details": mock_move,
                "state": current_state.copy()
            }})

            print(f"✅ Move {{move_num}} completed")

            # Check if game ended
            if current_state.get("game_over"):
                winner = current_state.get("winner")
                print(f"\\n🎉 Game Over! Winner: {{winner}}")
                break

        # Save state history
        save_state_history(state_history, game_name)

        print(f"\\n{"=" * 60}")
        print("EXAMPLE COMPLETED SUCCESSFULLY")
        print(f"Total moves: {{len(state_history) - 1}}")
        print(f"Check docs/simple_generated/state_history/ for detailed logs")
        print(f"{"=" * 60}\\n")

    except Exception as e:
        print(f"❌ Error running example: {{e}}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


def save_state_history(history: List[Dict[str, Any]], game_name: str):
    """Save state history to JSON file."""
    # Create state history directory
    history_dir = Path("docs/simple_generated/state_history")
    history_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{{game_name}}_example_{{timestamp}}.json"
    filepath = history_dir / filename

    # Prepare history data
    history_data = {{
        "game": game_name,
        "example_type": "template_simulation",
        "generated_at": datetime.now().isoformat(),
        "total_moves": len(history) - 1,
        "history": history
    }}

    # Save to file
    with open(filepath, 'w') as f:
        json.dump(history_data, f, indent=2, default=str)

    print(f"📁 State history saved: {{filepath}}")


def get_player_move(player: str) -> Dict[str, Any]:
    """Get move from player (placeholder for actual implementation)."""
    # This would contain actual move input logic
    return {{
        "player": player,
        "action": "placeholder_move",
        "timestamp": datetime.now().isoformat()
    }}


if __name__ == "__main__":
    sys.exit(main())
'''
        return template

    def generate_state_history_template(self, game_name: str) -> Path | None:
        """Generate state history template."""
        print(f"Generating state history template for {game_name}")

        template_content = self._create_state_history_template(game_name)
        output_path = self.templates_dir / f"{game_name}_state_template.json"

        with open(output_path, "w") as f:
            f.write(template_content)

        print(f"Generated template: {output_path}")
        return output_path

    def _create_state_history_template(self, game_name: str) -> str:
        """Create state history template."""
        template = {
            "game": game_name,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "template_version": "1.0",
                "description": f"State history template for {game_name} game",
            },
            "initial_state": {
                "game": game_name,
                "players": ["Player1", "Player2"],
                "current_player": "Player1",
                "game_over": False,
                "winner": None,
                "move_number": 0,
            },
            "move_history": [
                {
                    "move_number": 1,
                    "timestamp": "2025-07-05T12:00:00",
                    "player": "Player1",
                    "action": "example_move",
                    "state_after": {
                        "move_number": 1,
                        "current_player": "Player2",
                        "game_over": False,
                    },
                }
            ],
            "final_state": {
                "game": game_name,
                "game_over": True,
                "winner": "Player1",
                "total_moves": 5,
                "end_reason": "normal_completion",
            },
        }

        return json.dumps(template, indent=2)

    def generate_all_documentation(self):
        """Generate all documentation for all games."""
        print("Starting simple documentation generation...")

        results = {
            "architectures": {},
            "examples": {},
            "templates": {},
            "total_games": len(self.games),
        }

        # Generate for each game
        for game_name in self.games:
            print(f"\\nProcessing {game_name}...")

            # Generate architecture diagram
            arch_path = self.generate_text_architecture(game_name)
            results["architectures"][game_name] = str(arch_path) if arch_path else None

            # Generate example template
            example_path = self.generate_example_template(game_name)
            results["examples"][game_name] = str(example_path) if example_path else None

            # Generate state history template
            template_path = self.generate_state_history_template(game_name)
            results["templates"][game_name] = (
                str(template_path) if template_path else None
            )

        # Generate summary index
        self._generate_summary_index(results)

        print("\\n✅ Simple documentation generation completed!")
        print(f"📁 Output directory: {self.output_dir}")

        return results

    def _generate_summary_index(self, results: dict[str, Any]):
        """Generate summary index."""
        index_content = f"""# Simple Game Documentation Index

Generated: {datetime.now().isoformat()}
Total Games: {results["total_games"]}

## Architecture Diagrams (Text-based)

"""

        for game_name, arch_path in results["architectures"].items():
            if arch_path:
                rel_path = Path(arch_path).relative_to(self.output_dir)
                index_content += f"- **{game_name.title()}**: `{rel_path}`\\n"

        index_content += """
## Example Templates

"""

        for game_name, example_path in results["examples"].items():
            if example_path:
                rel_path = Path(example_path).relative_to(self.output_dir)
                index_content += f"- **{game_name.title()}**: `{rel_path}`\\n"

        index_content += """
## State History Templates

"""

        for game_name, template_path in results["templates"].items():
            if template_path:
                rel_path = Path(template_path).relative_to(self.output_dir)
                index_content += f"- **{game_name.title()}**: `{rel_path}`\\n"

        index_content += """
## Usage Instructions

### Running Examples
```bash
# Navigate to examples directory
cd docs/simple_generated/examples/

# Run any example template
python chess_example_template.py
```

### Viewing Architectures
```bash
# View text-based architecture diagrams
cat docs/simple_generated/architectures/chess_architecture.txt
```

### State History
State history files are generated when examples are run and saved to:
`docs/simple_generated/state_history/`

These JSON files contain complete game progression and can be used for:
- Documentation examples
- Test case generation
- Game replay analysis
- Debugging and validation
"""

        index_path = self.output_dir / "INDEX.md"
        with open(index_path, "w") as f:
            f.write(index_content)

        print(f"📝 Summary index created: {index_path}")


def main():
    """Main function."""
    print("🎮 Simple Haive Games Documentation Generator")
    print("=" * 50)

    generator = SimpleGameDocumentationGenerator()
    results = generator.generate_all_documentation()

    successful_architectures = sum(
        1 for path in results["architectures"].values() if path
    )
    successful_examples = sum(1 for path in results["examples"].values() if path)
    successful_templates = sum(1 for path in results["templates"].values() if path)

    print("\\n📊 Generation Summary:")
    print(
        f"- Architecture diagrams: {successful_architectures}/{results['total_games']}"
    )
    print(f"- Example templates: {successful_examples}/{results['total_games']}")
    print(f"- State templates: {successful_templates}/{results['total_games']}")
    print(
        f"- Total files created: {successful_architectures + successful_examples + successful_templates}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
