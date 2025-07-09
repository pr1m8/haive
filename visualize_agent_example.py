#!/usr/bin/env python3
"""
Agent Graph Visualization Script

This script helps you run example.py files and visualize their agent graphs.
It can automatically discover examples, run them, and generate visualizations.

Usage:
    python visualize_agent_example.py --help
    python visualize_agent_example.py simple  # Run simple agent example
    python visualize_agent_example.py multi   # Run multi-agent example
    python visualize_agent_example.py --list  # List all available examples
    python visualize_agent_example.py --discover react  # Find react examples
"""

import argparse
import ast
import importlib.util
import inspect
import logging
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add the packages to path
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-core" / "src"))
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-agents" / "src"))

from haive.core.graph.state_graph.graph_visualizer import GraphVisualizer
from haive.core.graph.utils.mermaid_visualizer import MermaidVisualizer, visualize_graph
from haive.core.utils.visualize_graph_utils import render_and_display_graph

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ExampleDiscoverer:
    """Discovers and analyzes example.py files in the codebase."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.examples = {}
        self.discover_examples()
    
    def discover_examples(self):
        """Discover all example.py files in the codebase."""
        logger.info("Discovering example.py files...")
        
        # Search for example.py files
        example_files = list(self.base_path.rglob("**/example.py"))
        
        for example_file in example_files:
            try:
                # Extract module info
                relative_path = example_file.relative_to(self.base_path)
                module_name = str(relative_path.parent).replace(os.sep, ".")
                
                # Skip if it's not in a haive package
                if "haive" not in module_name:
                    continue
                
                # Extract the agent/component type
                if "src/haive/agents" in str(example_file):
                    category = "agents"
                    # Extract agent type (e.g., simple, multi, react)
                    parts = str(relative_path).split(os.sep)
                    agent_type = None
                    for i, part in enumerate(parts):
                        if part == "agents" and i + 1 < len(parts):
                            agent_type = parts[i + 1]
                            break
                    
                elif "src/haive/games" in str(example_file):
                    category = "games"
                    # Extract game type
                    parts = str(relative_path).split(os.sep)
                    agent_type = None
                    for i, part in enumerate(parts):
                        if part == "games" and i + 1 < len(parts):
                            agent_type = parts[i + 1]
                            break
                            
                elif "src/haive/prebuilt" in str(example_file):
                    category = "prebuilt"
                    parts = str(relative_path).split(os.sep)
                    agent_type = None
                    for i, part in enumerate(parts):
                        if part == "prebuilt" and i + 1 < len(parts):
                            agent_type = parts[i + 1]
                            break
                else:
                    category = "other"
                    agent_type = "unknown"
                
                # Analyze the example file
                analysis = self.analyze_example_file(example_file)
                
                key = f"{category}_{agent_type}" if agent_type else f"{category}_unknown"
                self.examples[key] = {
                    "file_path": example_file,
                    "category": category,
                    "agent_type": agent_type,
                    "module_name": module_name,
                    "analysis": analysis
                }
                
            except Exception as e:
                logger.warning(f"Failed to analyze {example_file}: {e}")
        
        logger.info(f"Found {len(self.examples)} example files")
    
    def analyze_example_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze an example file to understand its structure."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the AST
            tree = ast.parse(content)
            
            analysis = {
                "functions": [],
                "classes": [],
                "imports": [],
                "main_functions": [],
                "agent_creations": [],
                "graph_methods": []
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    analysis["functions"].append(node.name)
                    if node.name == "main" or "main" in node.name:
                        analysis["main_functions"].append(node.name)
                
                elif isinstance(node, ast.ClassDef):
                    analysis["classes"].append(node.name)
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        analysis["imports"].append(alias.name)
                
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        analysis["imports"].append(node.module)
                
                elif isinstance(node, ast.Call):
                    # Look for agent creations
                    if hasattr(node.func, 'id') and 'Agent' in str(node.func.id):
                        analysis["agent_creations"].append(str(node.func.id))
                    
                    # Look for graph methods
                    if hasattr(node.func, 'attr'):
                        if node.func.attr in ['build_graph', 'compile', 'invoke', 'run', 'arun']:
                            analysis["graph_methods"].append(node.func.attr)
            
            return analysis
            
        except Exception as e:
            logger.warning(f"Failed to analyze AST for {file_path}: {e}")
            return {"error": str(e)}
    
    def list_examples(self, category: Optional[str] = None) -> List[str]:
        """List available examples, optionally filtered by category."""
        if category:
            return [key for key in self.examples.keys() if key.startswith(category)]
        return list(self.examples.keys())
    
    def get_example_info(self, example_key: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific example."""
        return self.examples.get(example_key)


class AgentGraphVisualizer:
    """Visualizes agent graphs from example runs."""
    
    def __init__(self, output_dir: str = "./graph_visualizations"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
    def run_example_and_visualize(self, example_key: str, discoverer: ExampleDiscoverer):
        """Run an example and visualize its agent graph."""
        example_info = discoverer.get_example_info(example_key)
        if not example_info:
            logger.error(f"Example '{example_key}' not found")
            return
            
        logger.info(f"Running example: {example_key}")
        logger.info(f"File: {example_info['file_path']}")
        
        try:
            # Import the example module
            spec = importlib.util.spec_from_file_location(
                f"example_{example_key}", 
                example_info['file_path']
            )
            example_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(example_module)
            
            # Look for agents and graphs to visualize
            self.extract_and_visualize_graphs(example_module, example_key, example_info)
            
        except Exception as e:
            logger.error(f"Failed to run example {example_key}: {e}")
            logger.exception("Full traceback:")
    
    def extract_and_visualize_graphs(self, module: Any, example_key: str, example_info: Dict[str, Any]):
        """Extract agent graphs from a module and visualize them."""
        graphs_found = []
        
        # Look for functions that create agents
        for name in dir(module):
            obj = getattr(module, name)
            
            # Skip private/internal attributes
            if name.startswith('_'):
                continue
                
            # Check if it's a function that might create agents
            if callable(obj) and hasattr(obj, '__name__'):
                try:
                    # Try to call functions that look like they create agents
                    if any(keyword in name.lower() for keyword in ['create', 'build', 'setup', 'demo', 'example']):
                        logger.info(f"Trying to call function: {name}")
                        
                        # Get function signature
                        sig = inspect.signature(obj)
                        
                        # Only call functions with no required parameters
                        if len(sig.parameters) == 0 or all(p.default != inspect.Parameter.empty for p in sig.parameters.values()):
                            result = obj()
                            
                            # Check if result has a graph
                            if hasattr(result, 'graph') and result.graph:
                                graphs_found.append({
                                    'name': f"{example_key}_{name}",
                                    'graph': result.graph,
                                    'agent': result,
                                    'source': f"function_{name}"
                                })
                            
                            # Check if result has build_graph method
                            elif hasattr(result, 'build_graph'):
                                try:
                                    graph = result.build_graph()
                                    if graph:
                                        graphs_found.append({
                                            'name': f"{example_key}_{name}_built",
                                            'graph': graph,
                                            'agent': result,
                                            'source': f"function_{name}_build_graph"
                                        })
                                except Exception as e:
                                    logger.warning(f"Failed to build graph for {name}: {e}")
                            
                            # Check if result can be compiled
                            elif hasattr(result, 'compile'):
                                try:
                                    compiled = result.compile()
                                    if hasattr(compiled, 'graph') and compiled.graph:
                                        graphs_found.append({
                                            'name': f"{example_key}_{name}_compiled",
                                            'graph': compiled.graph,
                                            'agent': result,
                                            'source': f"function_{name}_compile"
                                        })
                                except Exception as e:
                                    logger.warning(f"Failed to compile graph for {name}: {e}")
                
                except Exception as e:
                    logger.warning(f"Failed to call function {name}: {e}")
            
            # Check if it's already an agent or has a graph
            elif hasattr(obj, 'graph') and obj.graph:
                graphs_found.append({
                    'name': f"{example_key}_{name}",
                    'graph': obj.graph,
                    'agent': obj,
                    'source': f"direct_{name}"
                })
        
        # Visualize all found graphs
        if graphs_found:
            logger.info(f"Found {len(graphs_found)} graphs to visualize")
            for graph_info in graphs_found:
                self.visualize_graph(graph_info, example_key)
        else:
            logger.warning(f"No graphs found in example {example_key}")
            
            # Try to run main function if it exists
            if hasattr(module, 'main'):
                logger.info("Trying to run main function to look for graphs...")
                try:
                    result = module.main()
                    if hasattr(result, 'graph'):
                        self.visualize_graph({
                            'name': f"{example_key}_main",
                            'graph': result.graph,
                            'agent': result,
                            'source': "main_function"
                        }, example_key)
                except Exception as e:
                    logger.warning(f"Failed to run main function: {e}")
    
    def visualize_graph(self, graph_info: Dict[str, Any], example_key: str):
        """Visualize a single graph using multiple visualization methods."""
        graph = graph_info['graph']
        name = graph_info['name']
        
        logger.info(f"Visualizing graph: {name}")
        
        # Create output directory for this example
        example_dir = self.output_dir / example_key
        example_dir.mkdir(exist_ok=True)
        
        try:
            # Method 1: GraphVisualizer (most comprehensive)
            logger.info("Generating visualization with GraphVisualizer...")
            html_path = example_dir / f"{name}_graph_visualizer.html"
            
            mermaid_code = GraphVisualizer.generate_mermaid(
                graph,
                include_subgraphs=True,
                theme="base",
                direction="TB",
                debug=True
            )
            
            # Save mermaid code
            mermaid_path = example_dir / f"{name}_graph_visualizer.mmd"
            with open(mermaid_path, 'w') as f:
                f.write(mermaid_code)
            
            # Display the graph (creates HTML and optionally PNG)
            GraphVisualizer.display_graph(
                graph,
                output_path=str(html_path),
                include_subgraphs=True,
                save_png=True,
                title=f"Agent Graph: {name}",
                debug=True
            )
            
            logger.info(f"GraphVisualizer output saved to: {html_path}")
            
        except Exception as e:
            logger.error(f"GraphVisualizer failed for {name}: {e}")
        
        try:
            # Method 2: MermaidVisualizer
            logger.info("Generating visualization with MermaidVisualizer...")
            html_path = example_dir / f"{name}_mermaid_visualizer.html"
            
            visualizer = MermaidVisualizer(graph)
            visualizer.render_to_file(
                output_file=str(html_path),
                open_browser=False,
                include_legend=True
            )
            
            logger.info(f"MermaidVisualizer output saved to: {html_path}")
            
        except Exception as e:
            logger.error(f"MermaidVisualizer failed for {name}: {e}")
        
        try:
            # Method 3: Basic visualization
            logger.info("Generating basic visualization...")
            png_path = example_dir / f"{name}_basic.png"
            
            render_and_display_graph(
                graph,
                output_dir=str(example_dir),
                output_name=f"{name}_basic.png"
            )
            
            logger.info(f"Basic visualization saved to: {png_path}")
            
        except Exception as e:
            logger.error(f"Basic visualization failed for {name}: {e}")
        
        # Generate debug information
        try:
            debug_info = GraphVisualizer.debug_graph_structure(graph)
            debug_path = example_dir / f"{name}_debug_info.json"
            
            import json
            with open(debug_path, 'w') as f:
                json.dump(debug_info, f, indent=2, default=str)
            
            logger.info(f"Debug info saved to: {debug_path}")
            
        except Exception as e:
            logger.error(f"Debug info generation failed for {name}: {e}")


def main():
    """Main CLI interface."""
    parser = argparse.ArgumentParser(description="Visualize agent graphs from example.py files")
    parser.add_argument("example", nargs="?", help="Example key to run (e.g., 'simple', 'multi', 'agents_simple')")
    parser.add_argument("--list", action="store_true", help="List all available examples")
    parser.add_argument("--discover", metavar="PATTERN", help="Discover examples matching pattern")
    parser.add_argument("--category", help="Filter examples by category (agents, games, prebuilt)")
    parser.add_argument("--output-dir", default="./graph_visualizations", help="Output directory for visualizations")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize components
    discoverer = ExampleDiscoverer()
    visualizer = AgentGraphVisualizer(args.output_dir)
    
    if args.list:
        # List all examples
        examples = discoverer.list_examples(args.category)
        print(f"\nAvailable examples ({len(examples)} found):")
        for example in sorted(examples):
            info = discoverer.get_example_info(example)
            print(f"  {example:30} - {info['file_path']}")
        return
    
    if args.discover:
        # Find examples matching pattern
        examples = discoverer.list_examples()
        matches = [ex for ex in examples if args.discover.lower() in ex.lower()]
        print(f"\nExamples matching '{args.discover}' ({len(matches)} found):")
        for example in sorted(matches):
            info = discoverer.get_example_info(example)
            print(f"  {example:30} - {info['file_path']}")
        return
    
    if not args.example:
        # Show available examples and exit
        examples = discoverer.list_examples()
        print(f"\nPlease specify an example to run. Available examples ({len(examples)} found):")
        for example in sorted(examples):
            info = discoverer.get_example_info(example)
            print(f"  {example:30} - {info['file_path']}")
        print(f"\nUsage: python {sys.argv[0]} <example_key>")
        print(f"Example: python {sys.argv[0]} agents_simple")
        return
    
    # Try to find the example (allow partial matches)
    examples = discoverer.list_examples()
    matches = [ex for ex in examples if args.example.lower() in ex.lower()]
    
    if not matches:
        print(f"Example '{args.example}' not found.")
        print("Available examples:")
        for example in sorted(examples):
            print(f"  {example}")
        return
    
    if len(matches) > 1:
        print(f"Multiple matches found for '{args.example}':")
        for match in sorted(matches):
            print(f"  {match}")
        print("Please be more specific.")
        return
    
    # Run the example
    example_key = matches[0]
    print(f"Running example: {example_key}")
    
    visualizer.run_example_and_visualize(example_key, discoverer)
    
    print(f"\nVisualization complete! Check the output directory: {args.output_dir}")


if __name__ == "__main__":
    main()