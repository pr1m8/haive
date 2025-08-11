#!/usr/bin/env python3
"""Comprehensive documentation and visualization generator for haive-games.

This script generates:
1. Agent graph visualizations (PNG) for each game
2. Example runs with state history
3. Comprehensive documentation with visual references
4. Game-specific documentation with usage examples

Usage:
    python generate_game_docs.py [--game GAME_NAME] [--output-dir DIR]
"""

# Standard library imports
import argparse
import logging
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any

# Third-party imports
try:
    import matplotlib.pyplot as plt
    import networkx as nx
    from PIL import Image, ImageDraw, ImageFont
except ImportError as e:
    print(f"Missing required dependencies: {e}")
    print("Install with: pip install matplotlib networkx pillow")
    sys.exit(1)

# Local imports
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class GameDocumentationGenerator:
    """Generates comprehensive documentation for all haive games."""

    def __init__(self, output_dir: str = "docs/generated"):
        """Initialize the documentation generator.

        Args:
            output_dir: Directory to save generated documentation
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        self.graphs_dir = self.output_dir / "graphs"
        self.examples_dir = self.output_dir / "examples"
        self.state_history_dir = self.output_dir / "state_history"

        for dir_path in [self.graphs_dir, self.examples_dir, self.state_history_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.games = self._discover_games()
        logger.info(f"Discovered {len(self.games)} games: {list(self.games.keys())}")

    def _discover_games(self) -> dict[str, dict[str, Any]]:
        """Discover all available games in the haive-games package."""
        games_dir = Path("src/haive/games")
        games = {}

        if not games_dir.exists():
            logger.error(f"Games directory not found: {games_dir}")
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
                }
                logger.debug(f"Found game: {game_name}")
            else:
                logger.debug(f"Skipping {game_name} - no agent.py found")

        return games

    def generate_agent_graph(self, game_name: str) -> Path | None:
        """Generate agent graph visualization for a specific game.

        Args:
            game_name: Name of the game to generate graph for

        Returns:
            Path to generated PNG file, or None if failed
        """
        logger.info(f"Generating graph for {game_name}")

        try:
            # Import the game agent
            agent_module = self._import_game_agent(game_name)
            if not agent_module:
                return None

            # Try to get the agent class
            agent_class = self._get_agent_class(agent_module, game_name)
            if not agent_class:
                return None

            # Try to instantiate and get graph
            graph_data = self._extract_agent_graph(agent_class, game_name)
            if not graph_data:
                return None

            # Generate visualization
            output_path = self.graphs_dir / f"{game_name}_agent_graph.png"
            self._create_graph_visualization(graph_data, output_path, game_name)

            logger.info(f"Generated graph: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate graph for {game_name}: {e}")
            logger.debug(traceback.format_exc())
            return None

    def _import_game_agent(self, game_name: str) -> Any | None:
        """Import the agent module for a game."""
        try:
            module_name = f"haive.games.{game_name}.agent"
            module = __import__(module_name, fromlist=[""])
            return module
        except ImportError as e:
            logger.warning(f"Could not import {game_name} agent: {e}")
            return None

    def _get_agent_class(self, module: Any, game_name: str) -> Any | None:
        """Get the main agent class from a module."""
        # Common agent class name patterns
        possible_names = [
            f"{game_name.title()}Agent",
            f"{game_name.title().replace('_', '')}Agent",
            f"{game_name.upper()}Agent",
            "Agent",
            "GameAgent",
        ]

        for name in possible_names:
            if hasattr(module, name):
                agent_class = getattr(module, name)
                logger.debug(f"Found agent class: {name} for {game_name}")
                return agent_class

        # Try to find any class ending in 'Agent'
        for attr_name in dir(module):
            if attr_name.endswith("Agent") and not attr_name.startswith("_"):
                agent_class = getattr(module, attr_name)
                if callable(agent_class):  # Check if it's a class
                    logger.debug(f"Found agent class: {attr_name} for {game_name}")
                    return agent_class

        logger.warning(f"No agent class found for {game_name}")
        return None

    def _extract_agent_graph(
        self, agent_class: Any, game_name: str
    ) -> dict[str, Any] | None:
        """Extract graph structure from an agent class."""
        try:
            # Try to instantiate the agent with minimal config
            agent = self._create_agent_instance(agent_class, game_name)
            if not agent:
                return None

            # Try to extract graph information
            graph_info = self._get_graph_info(agent)
            return graph_info

        except Exception as e:
            logger.warning(f"Could not extract graph for {game_name}: {e}")
            return self._create_fallback_graph(game_name)

    def _create_agent_instance(self, agent_class: Any, game_name: str) -> Any | None:
        """Create an agent instance with default configuration."""
        try:
            # Try with no arguments
            return agent_class()
        except Exception:
            try:
                # Try to find and use a config class
                config_class = self._find_config_class(game_name)
                if config_class:
                    config = config_class()
                    return agent_class(config)
            except Exception:
                pass

        logger.debug(f"Could not instantiate agent for {game_name}")
        return None

    def _find_config_class(self, game_name: str) -> Any | None:
        """Find the configuration class for a game."""
        try:
            config_module_name = f"haive.games.{game_name}.config"
            config_module = __import__(config_module_name, fromlist=[""])

            # Common config class patterns
            possible_names = [
                f"{game_name.title()}Config",
                f"{game_name.title().replace('_', '')}Config",
                f"{game_name.title()}AgentConfig",
                "Config",
                "AgentConfig",
            ]

            for name in possible_names:
                if hasattr(config_module, name):
                    return getattr(config_module, name)

        except ImportError:
            pass

        return None

    def _get_graph_info(self, agent: Any) -> dict[str, Any]:
        """Extract graph information from an agent instance."""
        graph_info = {"nodes": [], "edges": [], "type": "unknown"}

        # Check if agent has a graph attribute (LangGraph)
        if hasattr(agent, "graph"):
            graph = agent.graph
            if hasattr(graph, "nodes"):
                graph_info["nodes"] = list(graph.nodes.keys())
                graph_info["type"] = "langgraph"

            if hasattr(graph, "edges"):
                edges = []
                for edge in graph.edges:
                    if hasattr(edge, "source") and hasattr(edge, "target"):
                        edges.append((edge.source, edge.target))
                graph_info["edges"] = edges

        # Check for workflow methods (common pattern)
        workflow_methods = [
            method
            for method in dir(agent)
            if method.startswith(("handle_", "process_", "execute_"))
        ]

        if workflow_methods:
            graph_info["workflow_methods"] = workflow_methods
            if not graph_info["nodes"]:
                graph_info["nodes"] = workflow_methods
                graph_info["type"] = "workflow"

        # Check for state management
        if hasattr(agent, "state_manager"):
            graph_info["has_state_manager"] = True

        return graph_info

    def _create_fallback_graph(self, game_name: str) -> dict[str, Any]:
        """Create a fallback graph structure for games without extractable graphs."""
        return {
            "nodes": ["initialize", "process_move", "update_state", "check_end"],
            "edges": [
                ("initialize", "process_move"),
                ("process_move", "update_state"),
                ("update_state", "check_end"),
                ("check_end", "process_move"),
            ],
            "type": "fallback",
            "game": game_name,
        }

    def _create_graph_visualization(
        self, graph_data: dict[str, Any], output_path: Path, game_name: str
    ):
        """Create a PNG visualization of the graph."""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))

        # Create NetworkX graph
        G = nx.DiGraph()

        # Add nodes
        nodes = graph_data.get("nodes", [])
        G.add_nodes_from(nodes)

        # Add edges
        edges = graph_data.get("edges", [])
        if edges:
            G.add_edges_from(edges)
        else:
            # Create a default flow if no edges
            if len(nodes) > 1:
                for i in range(len(nodes) - 1):
                    G.add_edge(nodes[i], nodes[i + 1])
                # Add loop back
                if len(nodes) > 2:
                    G.add_edge(nodes[-1], nodes[1])

        # Choose layout
        if len(nodes) <= 6:
            pos = nx.spring_layout(G, k=2, iterations=50)
        else:
            pos = nx.kamada_kawai_layout(G)

        # Draw the graph
        nx.draw_networkx_nodes(
            G, pos, node_color="lightblue", node_size=3000, alpha=0.8, ax=ax
        )
        nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", ax=ax)
        nx.draw_networkx_edges(
            G,
            pos,
            edge_color="gray",
            arrows=True,
            arrowsize=20,
            width=2,
            alpha=0.7,
            ax=ax,
        )

        # Set title and styling
        graph_type = graph_data.get("type", "unknown")
        ax.set_title(
            f"{game_name.title()} Agent Graph ({graph_type})",
            fontsize=16,
            fontweight="bold",
            pad=20,
        )
        ax.axis("off")

        # Add metadata
        metadata_text = f"Nodes: {len(nodes)}\nEdges: {len(edges)}\nType: {graph_type}"
        ax.text(
            0.02,
            0.98,
            metadata_text,
            transform=ax.transAxes,
            verticalalignment="top",
            bbox={"boxstyle": "round", "facecolor": "wheat", "alpha": 0.8},
        )

        plt.tight_layout()
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        plt.close()

    def generate_example_run(self, game_name: str) -> Path | None:
        """Generate an example run with state history for a game.

        Args:
            game_name: Name of the game

        Returns:
            Path to generated example file
        """
        logger.info(f"Generating example run for {game_name}")

        try:
            example_content = self._create_example_content(game_name)
            output_path = self.examples_dir / f"{game_name}_example.py"

            with open(output_path, "w") as f:
                f.write(example_content)

            logger.info(f"Generated example: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Failed to generate example for {game_name}: {e}")
            return None

    def _create_example_content(self, game_name: str) -> str:
        """Create example run content for a game."""
        template = f'''#!/usr/bin/env python3
"""Example run for {game_name.title()} game with state history logging.

This example demonstrates:
1. Agent initialization
2. Game execution with move tracking
3. State history saving for documentation
4. Comprehensive logging of game progression

Generated on: {datetime.now().isoformat()}
"""

# Standard library imports
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

# Third-party imports
from langgraph.types import Command

# Local imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from haive.games.{game_name}.agent import *
    from haive.games.{game_name}.models import *
    from haive.games.{game_name}.state import *
except ImportError as e:
    print(f"Could not import {game_name} components: {{e}}")
    print("Make sure the game is properly installed and configured.")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class {game_name.title()}ExampleRunner:
    """Example runner for {game_name.title()} game with comprehensive state tracking."""

    def __init__(self):
        """Initialize the example runner."""
        self.state_history = []
        self.move_count = 0
        self.start_time = datetime.now()

    def save_state_history(self, output_dir: str = "state_history"):
        """Save complete state history to JSON file."""
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"{game_name}_example_run_{{timestamp}}.json"
        filepath = Path(output_dir) / filename

        history_data = {{
            "game": "{game_name}",
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.now().isoformat(),
            "total_moves": self.move_count,
            "state_history": self.state_history
        }}

        with open(filepath, 'w') as f:
            json.dump(history_data, f, indent=2, default=str)

        logger.info(f"State history saved to: {{filepath}}")
        return filepath

    def log_state(self, state: Any, move_description: str = ""):
        """Log current state to history."""
        self.move_count += 1

        state_entry = {{
            "move_number": self.move_count,
            "timestamp": datetime.now().isoformat(),
            "description": move_description,
            "state": self._serialize_state(state)
        }}

        self.state_history.append(state_entry)
        logger.info(f"Move {{self.move_count}}: {{move_description}}")

    def _serialize_state(self, state: Any) -> Dict[str, Any]:
        """Serialize state to JSON-compatible format."""
        if hasattr(state, 'model_dump'):
            return state.model_dump()
        elif hasattr(state, 'dict'):
            return state.dict()
        elif isinstance(state, dict):
            return state
        else:
            return str(state)

    def run_example(self):
        """Run a complete example game."""
        logger.info("Starting {game_name.title()} example run")

        try:
            # Initialize agent (this will vary by game)
            agent = self._initialize_agent()
            if not agent:
                logger.error("Failed to initialize agent")
                return

            # Run example game
            self._run_game_loop(agent)

            # Save results
            self.save_state_history()

            logger.info("Example run completed successfully")

        except Exception as e:
            logger.error(f"Example run failed: {{e}}")
            import traceback
            logger.error(traceback.format_exc())

    def _initialize_agent(self):
        """Initialize the game agent with default configuration."""
        try:
            # Try different initialization patterns
            # Pattern 1: No config required
            try:
                agent = {game_name.title()}Agent()
                logger.info("Agent initialized without config")
                return agent
            except Exception:
                pass

            # Pattern 2: Config class available
            try:
                config_class = globals().get(f'{game_name.title()}Config') or globals().get(f'{game_name.title()}AgentConfig')
                if config_class:
                    config = config_class()
                    agent = {game_name.title()}Agent(config)
                    logger.info("Agent initialized with default config")
                    return agent
            except Exception:
                pass

            logger.warning("Could not initialize agent with standard patterns")
            return None

        except Exception as e:
            logger.error(f"Agent initialization failed: {{e}}")
            return None

    def _run_game_loop(self, agent):
        """Run the main game loop with state tracking."""
        logger.info("Starting game loop")

        # Initialize game state
        initial_state = {{}}
        self.log_state(initial_state, "Game initialized")

        # Run a few example moves (this is game-specific)
        for move_num in range(1, 6):  # 5 example moves
            try:
                # This is a simplified example - real games would have proper move logic
                result = agent.invoke(initial_state)

                if isinstance(result, Command) and result.update:
                    initial_state.update(result.update)
                    self.log_state(initial_state, f"Move {{move_num}} completed")
                else:
                    self.log_state(initial_state, f"Move {{move_num}} - no state change")

                # Check for game end conditions (game-specific)
                if self._check_game_end(initial_state):
                    self.log_state(initial_state, "Game ended")
                    break

            except Exception as e:
                logger.warning(f"Move {{move_num}} failed: {{e}}")
                self.log_state(initial_state, f"Move {{move_num}} failed: {{e}}")
                break

        logger.info(f"Game loop completed after {{self.move_count}} moves")

    def _check_game_end(self, state: Dict[str, Any]) -> bool:
        """Check if game has ended (game-specific logic)."""
        # This is a placeholder - each game would have its own end conditions
        return state.get('game_over', False) or self.move_count >= 10


def main():
    """Main function to run the example."""
    print(f"\\n{"=" * 60}")
    print(f"{game_name.upper()} GAME EXAMPLE RUN")
    print(f"{"=" * 60}")

    runner = {game_name.title()}ExampleRunner()
    runner.run_example()

    print(f"\\n{"=" * 60}")
    print("EXAMPLE RUN COMPLETED")
    print(f"Check state_history/ directory for detailed logs")
    print(f"{"=" * 60}\\n")


if __name__ == "__main__":
    main()
'''
        return template

    def generate_all_documentation(self):
        """Generate complete documentation for all games."""
        logger.info("Starting comprehensive documentation generation")

        results = {"graphs": {}, "examples": {}, "total_games": len(self.games)}

        # Generate for each game
        for game_name in self.games:
            logger.info(f"Processing {game_name}...")

            # Generate graph visualization
            graph_path = self.generate_agent_graph(game_name)
            results["graphs"][game_name] = str(graph_path) if graph_path else None

            # Generate example run
            example_path = self.generate_example_run(game_name)
            results["examples"][game_name] = str(example_path) if example_path else None

        # Generate master index
        self._generate_master_index(results)

        logger.info("Documentation generation completed!")
        logger.info(f"Output directory: {self.output_dir}")

        return results

    def _generate_master_index(self, results: dict[str, Any]):
        """Generate master index documentation."""
        index_content = self._create_master_index_content(results)
        index_path = self.output_dir / "README.md"

        with open(index_path, "w") as f:
            f.write(index_content)

        logger.info(f"Master index created: {index_path}")

    def _create_master_index_content(self, results: dict[str, Any]) -> str:
        """Create master index markdown content."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        content = f"""# Haive Games Documentation

**Generated on:** {timestamp}
**Total Games:** {results["total_games"]}

This documentation provides comprehensive coverage of all games in the haive-games package, including agent graph visualizations, example runs, and state history tracking.

## 📊 Agent Graph Visualizations

Each game includes a visual representation of its agent workflow:

"""

        # Add graph links
        for game_name, graph_path in results["graphs"].items():
            if graph_path:
                rel_path = Path(graph_path).relative_to(self.output_dir)
                content += (
                    f"- **{game_name.title()}**: ![{game_name} graph]({rel_path})\n"
                )
            else:
                content += f"- **{game_name.title()}**: ⚠️ Graph generation failed\n"

        content += """
## 🎮 Example Runs

Each game includes a comprehensive example with state history tracking:

"""

        # Add example links
        for game_name, example_path in results["examples"].items():
            if example_path:
                rel_path = Path(example_path).relative_to(self.output_dir)
                content += f"- **{game_name.title()}**: [`{game_name}_example.py`]({rel_path})\n"
            else:
                content += f"- **{game_name.title()}**: ⚠️ Example generation failed\n"

        content += """
## 📁 Directory Structure

```
docs/generated/
├── README.md                 # This file
├── graphs/                   # Agent graph visualizations (PNG)
│   ├── chess_agent_graph.png
│   ├── go_agent_graph.png
│   └── ...
├── examples/                 # Example run scripts
│   ├── chess_example.py
│   ├── go_example.py
│   └── ...
└── state_history/          # Generated state histories (JSON)
    ├── chess_example_run_*.json
    ├── go_example_run_*.json
    └── ...
```

## 🚀 Usage

### Running Examples

Each example can be run independently:

```bash
cd examples/
python chess_example.py
```

### Viewing Graphs

Graph visualizations are saved as high-resolution PNG files in the `graphs/` directory.

### State History

Example runs save detailed state histories in JSON format to the `state_history/` directory. These can be used for:

- Documentation examples
- Testing and validation
- Game replay functionality
- Analysis and debugging

## 🎯 Features

- **Agent Graph Visualization**: Visual representation of game agent workflows
- **Comprehensive Examples**: Full game runs with detailed logging
- **State History Tracking**: Complete game state progression saved to JSON
- **Documentation Integration**: Ready for inclusion in broader documentation
- **Automated Generation**: Systematic coverage of all games

---

*Generated by haive-games documentation system*
"""

        return content


def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(description="Generate haive-games documentation")
    parser.add_argument("--game", help="Generate docs for specific game only")
    parser.add_argument(
        "--output-dir",
        default="docs/generated",
        help="Output directory for generated docs",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    generator = GameDocumentationGenerator(args.output_dir)

    if args.game:
        # Generate for specific game
        if args.game not in generator.games:
            print(
                f"Game '{args.game}' not found. Available games: {list(generator.games.keys())}"
            )
            return 1

        print(f"Generating documentation for {args.game}...")
        graph_path = generator.generate_agent_graph(args.game)
        example_path = generator.generate_example_run(args.game)

        print(f"Graph: {graph_path}")
        print(f"Example: {example_path}")
    else:
        # Generate for all games
        print("Generating documentation for all games...")
        results = generator.generate_all_documentation()

        successful_graphs = sum(1 for path in results["graphs"].values() if path)
        successful_examples = sum(1 for path in results["examples"].values() if path)

        print("\\nCompleted:")
        print(f"- Graphs: {successful_graphs}/{results['total_games']}")
        print(f"- Examples: {successful_examples}/{results['total_games']}")
        print(f"- Output: {generator.output_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
