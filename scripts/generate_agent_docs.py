#!/usr/bin/env python
"""
Script to generate standardized documentation for agents.

This script can be used in two ways:
1. Process existing state history files to generate documentation
2. Run agents and generate documentation from their outputs

Example usage:
    # Process existing state history files
    poetry run python scripts/generate_agent_docs.py --state-dir /path/to/state/history

    # Run an agent and generate documentation
    poetry run python scripts/generate_agent_docs.py --agent SimpleAgent --prompt "Hello, world!"
"""

import argparse
import glob
import importlib
import json
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parents[1]
sys.path.insert(0, str(project_root))

from src.haive.core.utils.doc_utils import AgentVisualizer, create_agent_example_index


def process_state_history_files(state_dir: str, output_dir: str = None):
    """Process existing state history files to generate documentation."""
    visualizer = AgentVisualizer(output_dir=output_dir)

    # Get all state history files
    state_files = glob.glob(os.path.join(state_dir, "*.json"))

    if not state_files:
        print(f"No state history files found in {state_dir}")
        return

    print(f"Found {len(state_files)} state history files")

    # Process each file
    for state_file in state_files:
        try:
            # Load state history file
            with open(state_file, "r") as f:
                data = json.load(f)

            # Extract metadata and state history
            metadata = data.get("metadata", {})
            state_history = data.get("state_history", [])
            agent_name = metadata.get("agent_name", Path(state_file).stem)

            # Generate graph (if possible)
            graph_path = None

            # Generate documentation page
            doc_path = visualizer.generate_agent_visualization_page(
                agent_name=agent_name,
                agent_description=f"{agent_name} agent example run",
                state_history_path=state_file,
                graph_path=graph_path,
            )

            print(f"Generated documentation for {agent_name} at {doc_path}")

        except Exception as e:
            print(f"Error processing {state_file}: {e}")

    # Create index page
    index_path = create_agent_example_index()
    print(f"Created agent examples index at {index_path}")


def run_agent_and_document(
    agent_name: str, prompt: str, output_dir: str = None, module_path=None
):
    """Run an agent and generate documentation from its output."""
    visualizer = AgentVisualizer(output_dir=output_dir)

    # Create directories if they don't exist
    examples_dir = visualizer.output_dir.parent.parent / "agents" / "examples"
    examples_dir.mkdir(exist_ok=True, parents=True)

    print(f"Will save agent examples to {examples_dir}")

    # Dynamically import the agent class
    try:
        # If module path is provided, try to import directly
        if module_path:
            try:
                module = importlib.import_module(module_path)
                agent_class = getattr(module, agent_name)
            except (ImportError, AttributeError) as e:
                print(f"Error importing {agent_name} from {module_path}: {e}")
                raise
        else:
            # Try importing from haive.agents first
            try:
                module = importlib.import_module(f"haive.agents.{agent_name.lower()}")
                agent_class = getattr(module, agent_name)
            except (ImportError, AttributeError):
                # Try importing from haive.core.engine
                try:
                    module = importlib.import_module("haive.core.engine.agent")
                    agent_class = getattr(module, agent_name)
                except (ImportError, AttributeError):
                    # Try importing from packages directories with proper namespace
                    paths_to_try = [
                        f"haive.agents.{agent_name.lower()}",
                        f"haive.agents.simple.{agent_name.lower()}",
                        f"haive.agents.react.{agent_name.lower()}",
                        f"haive.agents.rag.{agent_name.lower()}",
                        f"haive.agents.conversation.{agent_name.lower()}",
                        # Try src paths
                        f"src.haive.agents.{agent_name.lower()}",
                        f"src.haive.agents.simple.{agent_name.lower()}",
                        f"src.haive.core.engine.agent",
                        # Try direct import
                        "haive.agents",
                        "haive.core.engine",
                    ]

                    for path in paths_to_try:
                        try:
                            module = importlib.import_module(path)
                            agent_class = getattr(module, agent_name)
                            break
                        except (ImportError, AttributeError):
                            continue
                    else:
                        raise ImportError(f"Could not find agent class {agent_name}")

        # Create agent instance
        agent = agent_class()

        # Run agent
        result = agent.invoke(prompt)

        # Get state history and graph
        # Try different ways to access state history
        state_history = getattr(agent, "state_history", None)
        if not state_history:
            if hasattr(agent, "state") and hasattr(agent.state, "history"):
                state_history = agent.state.history
            elif hasattr(agent, "_state_history"):
                state_history = agent._state_history
            elif hasattr(agent, "_history"):
                state_history = agent._history
            else:
                # Create a minimal state history with the result
                state_history = [
                    {"input": prompt, "output": result, "agent_type": agent_name}
                ]

        # Try different ways to access the graph
        graph = getattr(agent, "graph", None)
        if not graph and hasattr(agent, "get_graph"):
            try:
                graph = agent.get_graph()
            except:
                pass

        if not state_history:
            print(f"No state history available for {agent_name}")
            return

        # Save state history
        state_path = visualizer.save_agent_state_history(
            agent_name=agent_name, state_history=state_history
        )

        # Save graph if available
        graph_path = None
        if graph:
            graph_path = visualizer.save_agent_graph(agent_name=agent_name, graph=graph)

        # Generate documentation page
        doc_path = visualizer.generate_agent_visualization_page(
            agent_name=agent_name,
            agent_description=f"{agent_name} agent example run with prompt: '{prompt}'",
            state_history_path=state_path,
            graph_path=graph_path,
        )

        print(f"Generated documentation for {agent_name} at {doc_path}")

        # Create index page
        index_path = create_agent_example_index()
        print(f"Created agent examples index at {index_path}")

    except Exception as e:
        print(f"Error running agent {agent_name}: {e}")


def discover_agent_classes():
    """Discover available agent classes in the codebase."""
    agent_classes = []

    # Common agent module paths - update with actual paths in your codebase
    agent_modules = [
        "haive.agents.simple",
        "haive.agents.react",
        "haive.agents.rag",
        "haive.agents.conversation",
        "haive.agents.reasoning_and_critique",
        "haive.agents.task_analysis",
        "haive.agents.document_modifiers",
        "haive.core.engine.agent",
        # Add all possible locations
        "haive.agents",
        "haive.core.engine",
        # Packages locations
        "haive_agents.simple",
        "haive_agents.react",
        "haive_agents.rag",
        # Check if modules exist in src structure too
        "src.haive.agents.simple",
        "src.haive.agents.react",
        "src.haive.agents.rag",
        "src.haive.core.engine.agent",
    ]

    # Try to import each module and find agent classes
    for module_path in agent_modules:
        try:
            module = importlib.import_module(module_path)

            # Look for classes that might be agents
            for attr_name in dir(module):
                if attr_name.endswith("Agent") and not attr_name.startswith("_"):
                    try:
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type):  # Check if it's a class
                            # Check if it has an invoke method
                            if hasattr(attr, "invoke") or "invoke" in dir(attr):
                                agent_classes.append((attr_name, module_path))
                    except Exception as e:
                        print(f"Error checking {attr_name} in {module_path}: {e}")
        except ImportError:
            # Module doesn't exist, just continue
            continue

    return agent_classes


def run_all_agents(
    prompt="Hello, I'd like to learn about artificial intelligence.", output_dir=None
):
    """Run all available agents and generate documentation for each."""
    print("Discovering agent classes...")
    agent_classes = discover_agent_classes()

    if not agent_classes:
        print("No agent classes found.")
        return

    print(f"Found {len(agent_classes)} agent classes.")

    successful = 0
    failed = 0

    for agent_name, module_path in agent_classes:
        print(f"\nTrying to run {agent_name} from {module_path}...")
        try:
            run_agent_and_document(agent_name, prompt, output_dir, module_path)
            successful += 1
        except Exception as e:
            print(f"Failed to run {agent_name}: {e}")
            failed += 1

    # Create index page
    index_path = create_agent_example_index()

    print(
        f"\nRun complete. Successfully documented {successful} agents. Failed: {failed}."
    )
    print(f"Agent examples index created at: {index_path}")


def main():
    """Main function to parse arguments and run the script."""
    parser = argparse.ArgumentParser(description="Generate agent documentation")

    # Add arguments
    parser.add_argument("--state-dir", help="Directory containing state history files")
    parser.add_argument("--agent", help="Agent class name to run")
    parser.add_argument("--prompt", help="Prompt to use when running the agent")
    parser.add_argument("--output-dir", help="Output directory for documentation")
    parser.add_argument("--all", action="store_true", help="Run all available agents")

    # Parse arguments
    args = parser.parse_args()

    # Process state history files
    if args.state_dir:
        process_state_history_files(args.state_dir, args.output_dir)

    # Run all agents
    elif args.all:
        prompt = (
            args.prompt or "Hello, I'd like to learn about artificial intelligence."
        )
        run_all_agents(prompt, args.output_dir)

    # Run specific agent and generate documentation
    elif args.agent and args.prompt:
        run_agent_and_document(args.agent, args.prompt, args.output_dir)

    # Show help if no arguments provided
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
