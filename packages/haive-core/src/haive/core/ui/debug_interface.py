# src/haive/core/ui/debug_interface.py

import json
import logging
import os
import time
from contextlib import contextmanager
from typing import Any, Dict

from pydantic import BaseModel
from rich.console import Console
from rich.layout import Layout
from rich.logging import RichHandler
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.traceback import install as install_rich_traceback

# Install rich traceback handler
install_rich_traceback(show_locals=True)

# Set up rich console
console = Console()


class HaiveDebugger:
    """
    Centralized debugging and visualization interface for the Haive framework.

    Provides:
    - Standardized logging setup
    - Component visualization
    - Graph visualization
    - State inspection
    - Performance tracking
    - Error handling
    """

    def __init__(
        self,
        log_level: int = logging.INFO,
        show_timestamps: bool = True,
        log_to_file: bool = False,
        log_file: str = "haive_debug.log",
        rich_traceback: bool = True,
        capture_stdout: bool = False,
    ):
        """Initialize the debugger with configuration options."""
        self.console = Console(record=capture_stdout)
        self.logs = []
        self.timers = {}
        self.execution_traces = []

        # Set up logging
        self._setup_logging(log_level, show_timestamps, log_to_file, log_file)

        # Set up rich traceback if requested
        if rich_traceback:
            install_rich_traceback(show_locals=True, width=self.console.width)

        self.logger = logging.getLogger("haive")
        self.logger.info("Haive Debugger initialized")

    def _setup_logging(self, log_level, show_timestamps, log_to_file, log_file):
        """Set up logging with Rich handler."""
        handlers = []

        # Console handler with Rich formatting
        console_handler = RichHandler(
            console=self.console, show_time=show_timestamps, show_path=False
        )
        handlers.append(console_handler)

        # File handler if requested
        if log_to_file:
            os.makedirs(os.path.dirname(os.path.abspath(log_file)), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                )
            )
            handlers.append(file_handler)

        # Configure root logger
        logging.basicConfig(
            level=log_level, format="%(message)s", datefmt="[%X]", handlers=handlers
        )

    def display_engine(self, engine: Any):
        """Display detailed information about an engine component."""
        if not hasattr(engine, "engine_type"):
            self.console.print("[bold red]Not a valid engine object[/bold red]")
            return

        # Get engine details
        engine_info = {
            "name": getattr(engine, "name", "Unnamed"),
            "id": getattr(engine, "id", None),
            "engine_type": getattr(engine, "engine_type", None),
            "type": type(engine).__name__,
        }

        # Get field info
        if hasattr(engine, "model_fields"):
            # Pydantic v2
            fields = {
                name: str(field.annotation)
                for name, field in engine.model_fields.items()
                if name not in ["engine_type", "name", "id"]
            }
        else:
            fields = {}

        # Create display
        self.console.print(f"[bold blue]{engine_info['type']}[/bold blue]")

        # Engine info table
        table = Table(title=f"Engine: {engine_info['name']}")
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        for key, value in engine_info.items():
            table.add_row(key, str(value))

        # Add fields
        for name, type_info in fields.items():
            value = getattr(engine, name, "N/A")
            if isinstance(value, BaseModel):
                value = "BaseModel(...)"
            elif isinstance(value, dict) and len(value) > 5:
                value = f"dict with {len(value)} items"
            elif isinstance(value, list) and len(value) > 5:
                value = f"list with {len(value)} items"
            table.add_row(f"{name}: {type_info}", str(value)[:50])

        self.console.print(table)

    def display_graph(self, graph: Any, visualize: bool = True):
        """Display information about a graph, with optional visualization."""
        # Extract graph metadata
        metadata = {}
        if hasattr(graph, "extract_metadata"):
            metadata = graph.extract_metadata()
        elif hasattr(graph, "metadata"):
            metadata = graph.metadata

        # Basic graph info
        graph_name = getattr(graph, "name", "Unnamed Graph")
        self.console.print(f"[bold magenta]Graph: {graph_name}[/bold magenta]")

        # Node and edge info
        nodes = []
        edges = []

        if "nodes" in metadata:
            nodes = metadata["nodes"]
        elif hasattr(graph, "nodes"):
            nodes = list(graph.nodes.keys())

        if "edges" in metadata:
            edges = metadata["edges"]
        elif hasattr(graph, "edges"):
            edges = graph.edges

        # Display node and edge info
        nodes_table = Table(title="Nodes")
        nodes_table.add_column("Node Name", style="cyan")

        for node in nodes:
            nodes_table.add_row(str(node))

        edges_table = Table(title="Edges")
        edges_table.add_column("Source", style="cyan")
        edges_table.add_column("Target", style="green")

        for edge in edges:
            if isinstance(edge, tuple) and len(edge) == 2:
                edges_table.add_row(str(edge[0]), str(edge[1]))
            else:
                edges_table.add_row(str(edge), "")

        layout = Layout()
        layout.split_row(
            Layout(nodes_table, name="nodes"), Layout(edges_table, name="edges")
        )

        self.console.print(layout)

        # Generate visualization if requested
        if visualize and hasattr(graph, "visualize"):
            try:
                output_file = f"graph_{graph_name}_{int(time.time())}.png"
                graph.visualize(output_file=output_file)
                self.console.print(
                    f"[bold green]Graph visualization saved to {output_file}[/bold green]"
                )
            except Exception as e:
                self.console.print(
                    f"[bold red]Error generating visualization: {str(e)}[/bold red]"
                )

    def display_state(self, state: Dict[str, Any]):
        """Display the current state of a graph or agent."""
        self.console.print("[bold yellow]Current State:[/bold yellow]")

        # Format and display state
        formatted_state = {}

        for key, value in state.items():
            # Handle special state values
            if key == "messages" and isinstance(value, list):
                formatted_state[key] = f"{len(value)} messages"
            elif isinstance(value, BaseModel):
                formatted_state[key] = f"{type(value).__name__}(...)"
            elif isinstance(value, (list, dict)) and len(str(value)) > 100:
                if isinstance(value, list):
                    formatted_state[key] = f"list with {len(value)} items"
                else:
                    formatted_state[key] = f"dict with {len(value)} keys"
            else:
                formatted_state[key] = value

        # Display as JSON
        state_json = json.dumps(formatted_state, indent=2, default=str)
        state_syntax = Syntax(state_json, "json", theme="monokai", line_numbers=True)

        self.console.print(Panel(state_syntax, title="State"))

    @contextmanager
    def timer(self, name: str):
        """Context manager for timing operations."""
        start_time = time.time()
        try:
            yield
        finally:
            end_time = time.time()
            elapsed = end_time - start_time
            self.timers[name] = elapsed
            self.console.print(
                f"[bold cyan]Timer[/bold cyan] {name}: {elapsed:.4f} seconds"
            )

    def trace_execution(self, enabled: bool = True):
        """
        Decorator to trace function execution for debugging.

        @debugger.trace_execution()
        def my_function(arg1, arg2):
            ...
        """

        def decorator(func):
            if not enabled:
                return func

            def wrapper(*args, **kwargs):
                # Get function info
                func_name = func.__name__
                module_name = func.__module__
                signature = f"{func_name}({', '.join([repr(a) for a in args] + [f'{k}={repr(v)}' for k, v in kwargs.items()])})"

                # Log entry
                self.logger.debug(f"TRACE ENTER: {module_name}.{signature}")

                # Execute function with timing
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    end_time = time.time()
                    elapsed = end_time - start_time

                    # Log success
                    self.logger.debug(
                        f"TRACE EXIT: {module_name}.{func_name} (returned {type(result).__name__}) [{elapsed:.4f}s]"
                    )

                    # Record trace
                    self.execution_traces.append(
                        {
                            "function": f"{module_name}.{func_name}",
                            "args": args,
                            "kwargs": kwargs,
                            "result_type": type(result).__name__,
                            "elapsed": elapsed,
                            "success": True,
                        }
                    )

                    return result
                except Exception as e:
                    end_time = time.time()
                    elapsed = end_time - start_time

                    # Log error
                    self.logger.error(
                        f"TRACE ERROR: {module_name}.{func_name} - {type(e).__name__}: {str(e)} [{elapsed:.4f}s]"
                    )

                    # Record error trace
                    self.execution_traces.append(
                        {
                            "function": f"{module_name}.{func_name}",
                            "args": args,
                            "kwargs": kwargs,
                            "error": f"{type(e).__name__}: {str(e)}",
                            "elapsed": elapsed,
                            "success": False,
                        }
                    )

                    raise

            return wrapper

        return decorator

    def show_performance_summary(self):
        """Display a summary of performance timers."""
        if not self.timers:
            self.console.print("[yellow]No timers recorded yet.[/yellow]")
            return

        table = Table(title="Performance Summary")
        table.add_column("Operation", style="cyan")
        table.add_column("Time (s)", style="green")

        for name, elapsed in sorted(
            self.timers.items(), key=lambda x: x[1], reverse=True
        ):
            table.add_row(name, f"{elapsed:.4f}")

        self.console.print(table)

    def show_trace_summary(self):
        """Display a summary of execution traces."""
        if not self.execution_traces:
            self.console.print("[yellow]No execution traces recorded yet.[/yellow]")
            return

        table = Table(title="Execution Trace Summary")
        table.add_column("Function", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Time (s)", style="blue")

        for trace in self.execution_traces[-20:]:  # Show last 20 traces
            status = (
                "[green]SUCCESS[/green]"
                if trace["success"]
                else f"[red]ERROR: {trace.get('error', 'Unknown')}[/red]"
            )
            table.add_row(trace["function"], status, f"{trace['elapsed']:.4f}")

        self.console.print(table)

    def capture_output(self, func, *args, **kwargs):
        """
        Capture the console output of a function execution.

        Returns both the function result and the captured output.
        """
        with self.console.capture() as capture:
            result = func(*args, **kwargs)

        captured_output = capture.get()
        return result, captured_output

    def watch_object(self, obj, name=None):
        """
        Register an object for tracking changes between operations.
        """
        obj_name = name or type(obj).__name__
        obj_hash = id(obj)

        if hasattr(obj, "model_dump"):
            # Pydantic v2 model
            snapshot = obj.model_dump()
        elif hasattr(obj, "dict"):
            # Pydantic v1 model
            snapshot = obj.dict()
        elif isinstance(obj, dict):
            snapshot = obj.copy()
        elif hasattr(obj, "__dict__"):
            snapshot = obj.__dict__.copy()
        else:
            snapshot = str(obj)

        self.console.print(f"[bold blue]Watching object: {obj_name}[/bold blue]")
        return (obj_hash, obj_name, snapshot)

    def check_watched_object(self, watch_info):
        """
        Check for changes in a watched object.
        """
        obj_hash, obj_name, prev_snapshot = watch_info

        # Try to find the object by its id
        import gc

        for obj in gc.get_objects():
            if id(obj) == obj_hash:
                if hasattr(obj, "model_dump"):
                    # Pydantic v2 model
                    curr_snapshot = obj.model_dump()
                elif hasattr(obj, "dict"):
                    # Pydantic v1 model
                    curr_snapshot = obj.dict()
                elif isinstance(obj, dict):
                    curr_snapshot = obj.copy()
                elif hasattr(obj, "__dict__"):
                    curr_snapshot = obj.__dict__.copy()
                else:
                    curr_snapshot = str(obj)

                # Check for differences
                if curr_snapshot != prev_snapshot:
                    self.console.print(
                        f"[bold yellow]Changes detected in {obj_name}[/bold yellow]"
                    )

                    # If dictionaries, show key differences
                    if isinstance(curr_snapshot, dict) and isinstance(
                        prev_snapshot, dict
                    ):
                        # Keys added
                        added = set(curr_snapshot.keys()) - set(prev_snapshot.keys())
                        if added:
                            self.console.print(
                                f"  [green]Added keys: {', '.join(added)}[/green]"
                            )

                        # Keys removed
                        removed = set(prev_snapshot.keys()) - set(curr_snapshot.keys())
                        if removed:
                            self.console.print(
                                f"  [red]Removed keys: {', '.join(removed)}[/red]"
                            )

                        # Changed values
                        changed = {
                            k: (prev_snapshot[k], curr_snapshot[k])
                            for k in set(prev_snapshot.keys())
                            & set(curr_snapshot.keys())
                            if prev_snapshot[k] != curr_snapshot[k]
                        }
                        if changed:
                            self.console.print("  [yellow]Changed values:[/yellow]")
                            for k, (old, new) in changed.items():
                                self.console.print(f"    {k}: {old} -> {new}")
                    else:
                        self.console.print(f"  Previous: {prev_snapshot}")
                        self.console.print(f"  Current: {curr_snapshot}")

                # Update snapshot for next check
                return (obj_hash, obj_name, curr_snapshot)

        self.console.print(f"[bold red]Object {obj_name} no longer exists[/bold red]")
        return None
