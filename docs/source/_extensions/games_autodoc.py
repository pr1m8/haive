"""Enhanced Sphinx extension for automatic game documentation generation.

This extension recognizes the consistent patterns in haive-games and
creates better documentation that respects the structure and nuances of
each game.
"""

from pathlib import Path
import re

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.application import Sphinx
from sphinx.util.docutils import SphinxDirective


class GameCategory:
    """Represents a category of games with consistent patterns."""

    def __init__(self, name: str, description: str, icon: str = "🎮"):
        self.name = name
        self.description = description
        self.icon = icon
        self.games: list[GameInfo] = []


class GameInfo:
    """Information about a specific game implementation."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.title = self._extract_title()
        self.description = self._extract_description()
        self.quality_level = self._assess_quality()
        self.has_readme = (path / "README.md").exists()
        self.has_example = (path / "example.py").exists()
        self.has_ui = (path / "ui.py").exists()
        self.components = self._scan_components()

    def _extract_title(self) -> str:
        """Extract game title from README or directory name."""
        readme_path = self.path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, encoding="utf-8") as f:
                    first_line = f.readline().strip()
                    if first_line.startswith("#"):
                        # Extract title from markdown header
                        title = first_line.lstrip("#").strip()
                        # Clean up common patterns
                        title = re.sub(r"^(Haive Games?:?\s*)?", "", title)
                        title = re.sub(r"\s*(Module|Game|Implementation)$", "",
                                       title)
                        return title
            except Exception:
                pass

        # Fallback: prettify directory name
        return self.name.replace("_", " ").title()

    def _extract_description(self) -> str:
        """Extract game description from README."""
        readme_path = self.path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, encoding="utf-8") as f:
                    content = f.read()

                    # Look for overview section
                    overview_match = re.search(
                        r"## Overview\s*\n\s*(.+?)(?=\n##|\n\n|\Z)",
                        content,
                        re.DOTALL | re.IGNORECASE,
                    )
                    if overview_match:
                        desc = overview_match.group(1).strip()
                        # Clean up and truncate
                        desc = re.sub(r"\n+", " ", desc)
                        desc = re.sub(r"\s+", " ", desc)
                        if len(desc) > 200:
                            desc = desc[:200] + "..."
                        return desc

                    # Fallback: look for description after title
                    lines = content.split("\n")
                    for i, line in enumerate(lines):
                        if line.strip().startswith("#") and i + 1 < len(lines):
                            next_line = lines[i + 1].strip()
                            if next_line and not next_line.startswith("#"):
                                # Check next few lines for description
                                desc_lines = []
                                for j in range(i + 1, min(i + 5, len(lines))):
                                    if lines[j].strip(
                                    ) and not lines[j].startswith("#", ):
                                        desc_lines.append(lines[j].strip())
                                    elif desc_lines:
                                        break
                                if desc_lines:
                                    desc = " ".join(desc_lines)
                                    if len(desc) > 200:
                                        desc = desc[:200] + "..."
                                    return desc
            except Exception:
                pass

        # Fallback description
        return f"AI-powered {self.title} game implementation with LLM agents."

    def _assess_quality(self) -> str:
        """Assess the quality/completeness level of the game."""
        score = 0

        # Check for key files
        if (self.path / "README.md").exists():
            score += 2
        if (self.path / "agent.py").exists():
            score += 2
        if (self.path / "example.py").exists():
            score += 1
        if (self.path / "ui.py").exists():
            score += 1
        if (self.path / "models.py").exists():
            score += 1
        if (self.path / "config.py").exists():
            score += 1
        if (self.path / "state.py").exists():
            score += 1

        # Check README quality
        readme_path = self.path / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, encoding="utf-8") as f:
                    content = f.read()
                    # Look for comprehensive sections
                    if len(content) > 5000:  # Substantial documentation
                        score += 2
                    elif len(content) > 2000:
                        score += 1

                    # Look for specific quality indicators
                    if "## Quick Start" in content or "## Installation" in content:
                        score += 1
                    if "## Examples" in content or "## Usage" in content:
                        score += 1
                    if "## API Reference" in content:
                        score += 1
            except Exception:
                pass

        # Determine quality level
        if score >= 8:
            return "excellent"
        if score >= 6:
            return "good"
        if score >= 4:
            return "basic"
        return "minimal"

    def _scan_components(self) -> dict[str, bool]:
        """Scan for standard game components."""
        components = {}

        standard_files = [
            "agent.py",
            "config.py",
            "state.py",
            "models.py",
            "engines.py",
            "example.py",
            "ui.py",
            "utils.py",
        ]

        for file_name in standard_files:
            components[file_name.replace(".py", "")] = (self.path /
                                                        file_name).exists()

        return components


class GameCategorizer:
    """Categorizes games into logical groups."""

    CATEGORIES = {
        "board_games":
        GameCategory(
            "Board Games",
            "Classic board games with strategic depth",
            "♟️",
        ),
        "card_games":
        GameCategory(
            "Card Games",
            "Traditional and modern card games",
            "🃏",
        ),
        "single_player":
        GameCategory(
            "Single Player Games",
            "Puzzle and single-player challenges",
            "🧩",
        ),
        "social_deduction":
        GameCategory(
            "Social Deduction",
            "Games involving deception and social reasoning",
            "🎭",
        ),
        "strategy_games":
        GameCategory(
            "Strategy Games",
            "Complex strategic and tactical games",
            "🏰",
        ),
        "arcade_games":
        GameCategory(
            "Arcade Games",
            "Fast-paced action and reaction games",
            "🕹️",
        ),
        "other_games":
        GameCategory(
            "Other Games",
            "Miscellaneous and experimental games",
            "🎲",
        ),
    }

    # Game name patterns for categorization
    GAME_PATTERNS = {
        "board_games": [
            "chess",
            "checkers",
            "go",
            "reversi",
            "othello",
            "tic_tac_toe",
            "tictactoe",
            "connect4",
            "mancala",
            "fox_and_geese",
            "backgammon",
        ],
        "card_games": [
            "poker",
            "hold_em",
            "holdem",
            "blackjack",
            "bs",
            "uno",
            "solitaire",
            "hearts",
            "spades",
            "bridge",
        ],
        "single_player": [
            "wordle",
            "sudoku",
            "2048",
            "twenty_fourty_eight",
            "minesweeper",
            "mine_sweeper",
            "flow_free",
            "rubiks",
            "towers_of_hanoi",
            "crossword",
            "word_search",
            "solitaire",
        ],
        "social_deduction": [
            "mafia",
            "among_us",
            "clue",
            "cluedo",
            "werewolf",
            "secret_hitler",
            "resistance",
        ],
        "strategy_games": [
            "risk",
            "monopoly",
            "dominoes",
            "battleship",
            "civilization",
            "settlers",
            "catan",
        ],
        "arcade_games": [
            "pacman",
            "tetris",
            "snake",
            "pong",
            "asteroids",
            "space_invaders",
            "breakout",
        ],
    }

    @classmethod
    def categorize_game(cls, game_name: str) -> str:
        """Categorize a game based on its name."""
        game_name_lower = game_name.lower()

        for category, patterns in cls.GAME_PATTERNS.items():
            if any(pattern in game_name_lower for pattern in patterns):
                return category

        return "other_games"


class GameDocumentationGenerator:
    """Generates enhanced documentation for games."""

    def __init__(self, games_path: Path):
        self.games_path = games_path
        self.categories = GameCategorizer.CATEGORIES.copy()
        self._scan_games()

    def _scan_games(self):
        """Scan the games directory and categorize games."""
        if not self.games_path.exists():
            return

        for item in self.games_path.iterdir():
            if item.is_dir() and not item.name.startswith(("_", ".")):
                # Skip utility directories
                if item.name in [
                        "core",
                        "framework",
                        "base",
                        "base_v2",
                        "common",
                        "utils",
                        "api",
                ]:
                    continue

                game_info = GameInfo(item)
                category_name = GameCategorizer.categorize_game(item.name)

                if category_name in self.categories:
                    self.categories[category_name].games.append(game_info)

    def generate_category_index(self, category: GameCategory) -> str:
        """Generate RST content for a game category."""
        if not category.games:
            return ""

        lines = []
        lines.append(f"{category.icon} {category.name}")
        lines.append("=" * len(lines[-1]))
        lines.append("")
        lines.append(category.description)
        lines.append("")

        # Sort games by quality level and name
        quality_order = {"excellent": 0, "good": 1, "basic": 2, "minimal": 3}
        sorted_games = sorted(
            category.games,
            key=lambda g: (quality_order.get(g.quality_level, 4), g.title),
        )

        # Create game grid
        lines.append(".. grid:: 1 2 2 3")
        lines.append("   :gutter: 3")
        lines.append("")

        for game in sorted_games:
            quality_emoji = {
                "excellent": "⭐",
                "good": "✅",
                "basic": "🔧",
                "minimal": "🚧",
            }.get(game.quality_level, "❓")

            lines.append(
                f"   .. grid-item-card:: {quality_emoji} **{game.title}**")
            if game.has_readme:
                lines.append(f"      :link: {game.name}/index")
                lines.append("      :link-type: doc")
            lines.append("      ")
            lines.append(f"      {game.description}")

            # Add component indicators
            components = []
            if game.has_example:
                components.append("📖 Examples")
            if game.has_ui:
                components.append("🎨 Rich UI")
            if game.quality_level == "excellent":
                components.append("📚 Complete Docs")

            if components:
                lines.append("      ")
                lines.append(f"      *{' • '.join(components)}*")

            lines.append("      ")

        lines.append("")

        # Add quick start section
        if any(g.has_example for g in sorted_games):
            lines.append("Quick Examples")
            lines.append("-" * 14)
            lines.append("")

            for game in sorted_games[:3]:  # Show top 3 examples
                if game.has_example:
                    lines.append(f"**{game.title}**")
                    lines.append("")
                    lines.append(".. code-block:: python")
                    lines.append("")
                    lines.append(
                        f"   from haive.games.{
                            game.name} import {
                            game.title.replace(
                                ' ',
                                '')}Agent",
                    )
                    lines.append("   ")
                    lines.append(
                        f"   agent = {game.title.replace(' ', '')}Agent()")
                    lines.append("   result = agent.run()")
                    lines.append("")

        # Add toctree for individual games
        lines.append(".. toctree::")
        lines.append("   :maxdepth: 2")
        lines.append("   :hidden:")
        lines.append("")

        for game in sorted_games:
            if game.has_readme:
                lines.append(f"   {game.name}/index")

        lines.append("")

        return "\n".join(lines)

    def generate_main_index(self) -> str:
        """Generate the main games index with improved organization."""
        lines = []
        lines.append("🎮 Haive Games")
        lines.append("==============")
        lines.append("")
        lines.append(
            "Comprehensive game environments for AI agents with LLM integration.",
        )
        lines.append("")

        # Count games by quality
        all_games = []
        for category in self.categories.values():
            all_games.extend(category.games)

        quality_counts = {}
        for game in all_games:
            quality_counts[game.quality_level] = quality_counts.get(
                game.quality_level, 0) + 1

        lines.append(".. note::")
        lines.append("")
        lines.append(
            f"   **{len(all_games)} games available** across {len([c for c in self.categories.values() if c.games])} categories",
        )

        if quality_counts:
            quality_info = []
            if quality_counts.get("excellent", 0) > 0:
                quality_info.append(
                    f"⭐ {quality_counts['excellent']} excellent")
            if quality_counts.get("good", 0) > 0:
                quality_info.append(f"✅ {quality_counts['good']} good")
            if quality_counts.get("basic", 0) > 0:
                quality_info.append(f"🔧 {quality_counts['basic']} basic")
            if quality_counts.get("minimal", 0) > 0:
                quality_info.append(f"🚧 {quality_counts['minimal']} minimal")

            if quality_info:
                lines.append("   ")
                lines.append(f"   Quality levels: {' • '.join(quality_info)}")

        lines.append("")

        # Category overview grid
        lines.append("Game Categories")
        lines.append("---------------")
        lines.append("")
        lines.append(".. grid:: 1 2 2 3")
        lines.append("   :gutter: 3")
        lines.append("")

        for category_name, category in self.categories.items():
            if category.games:
                lines.append(
                    f"   .. grid-item-card:: {category.icon} **{category.name}**",
                )
                lines.append(f"      :link: {category_name}")
                lines.append("      :link-type: doc")
                lines.append("      ")
                lines.append(f"      {category.description}")
                lines.append("      ")
                lines.append(f"      *{len(category.games)} games available*")
                lines.append("      ")

        lines.append("")

        # Featured games (excellent quality)
        excellent_games = [
            g for g in all_games if g.quality_level == "excellent"
        ]
        if excellent_games:
            lines.append("⭐ Featured Games")
            lines.append("----------------")
            lines.append("")
            lines.append(
                "These games have comprehensive documentation, examples, and full feature sets:", )
            lines.append("")

            for game in excellent_games[:5]:  # Top 5 featured
                lines.append(f"* **{game.title}** - {game.description}")

            lines.append("")

        # Quick start
        lines.append("🚀 Quick Start")
        lines.append("--------------")
        lines.append("")
        lines.append(".. code-block:: python")
        lines.append("")
        lines.append("   # Play any game with simple setup")
        lines.append("   from haive.games.tic_tac_toe import TicTacToeAgent")
        lines.append("   ")
        lines.append("   agent = TicTacToeAgent()")
        lines.append("   result = agent.run()")
        lines.append('   print(f"Game result: {result}")')
        lines.append("")

        # Add toctree
        lines.append(".. toctree::")
        lines.append("   :maxdepth: 2")
        lines.append("   :caption: Game Categories")
        lines.append("   :hidden:")
        lines.append("")

        for category_name, category in self.categories.items():
            if category.games:
                lines.append(f"   {category_name}")

        lines.append("")

        # API reference
        lines.append("📚 API Reference")
        lines.append("----------------")
        lines.append("")
        lines.append(".. autosummary::")
        lines.append("   :toctree: generated")
        lines.append("   :recursive:")
        lines.append("   :caption: Haive Games API")
        lines.append("   ")
        lines.append("   haive.games")
        lines.append("")

        return "\n".join(lines)


class GamesAutoDocDirective(SphinxDirective):
    """Custom directive for automatic games documentation."""

    has_content = False
    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        "games-path": directives.path,
        "category": directives.unchanged,
        "format": directives.unchanged,
    }

    def run(self):
        """Generate games documentation."""
        env = self.state.document.settings.env

        # Get games path
        if "games-path" in self.options:
            games_path = Path(self.options["games-path"])
        else:
            # Default path relative to project root
            games_path = (Path(env.srcdir).parent.parent / "packages" /
                          "haive-games" / "src" / "haive" / "games")

        if not games_path.exists():
            error_node = nodes.error()
            error_node += nodes.paragraph(
                text=f"Games path not found: {games_path}")
            return [error_node]

        # Generate documentation
        generator = GameDocumentationGenerator(games_path)

        if "category" in self.options:
            # Generate specific category
            category_name = self.options["category"]
            if category_name in generator.categories:
                content = generator.generate_category_index(
                    generator.categories[category_name], )
            else:
                content = f"Category '{category_name}' not found."
        else:
            # Generate main index
            content = generator.generate_main_index()

        # Parse the generated RST content
        container = nodes.container()
        self.state.nested_parse(
            self.state.document.reporter.stringlist.from_string(content),
            self.content_offset,
            container,
        )

        return [container]


def setup(app: Sphinx):
    """Setup the Sphinx extension."""
    app.add_directive("games-autodoc", GamesAutoDocDirective)

    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
