# src/haive/core/ui/interactive_ui.py

import importlib
import inspect
import json

from haive_core.config.runnable import RunnableConfigManager
from haive_core.engine.base import Engine, EngineRegistry, EngineType
from haive_core.graph.dynamic_graph_builder import DynamicGraph
from rich.markdown import Markdown
from rich.prompt import Confirm, Prompt
from rich.syntax import Syntax
from rich.table import Table

from .debug_interface import HaiveDebugger


class HaiveInteractiveUI:
    """Interactive UI for testing and debugging Haive framework components.

    Provides a REPL-like interface for:
    - Exploring available components
    - Testing engines in isolation
    - Building and testing simple graphs
    - Inspecting configs and states
    - Running benchmarks
    """

    def __init__(self, debugger: HaiveDebugger | None = None):
        """Initialize the interactive UI."""
        self.debugger = debugger or HaiveDebugger()
        self.console = self.debugger.console
        self.registry = EngineRegistry.get_instance()
        self.current_state = {}
        self.components = {}
        self.history = []

    def start(self):
        """Start the interactive UI."""
        self.console.print("[bold green]Haive Framework Interactive UI[/bold green]")
        self.console.print("Type 'help' to see available commands")

        # Main REPL loop
        while True:
            try:
                command = Prompt.ask("\n[bold blue]haive[/bold blue]").strip()
                self.history.append(command)

                if command.lower() in ["exit", "quit", "q"]:
                    break
                if command.lower() == "help":
                    self._show_help()
                elif command.lower() == "components":
                    self._list_components()
                elif command.lower().startswith("inspect "):
                    component_name = command[8:].strip()
                    self._inspect_component(component_name)
                elif command.lower().startswith("test "):
                    component_name = command[5:].strip()
                    self._test_component(component_name)
                elif command.lower().startswith("create "):
                    self._create_component(command[7:].strip())
                elif command.lower().startswith("graph "):
                    self._handle_graph_command(command[6:].strip())
                elif command.lower() == "state":
                    self._show_state()
                elif command.lower().startswith("config "):
                    self._handle_config_command(command[7:].strip())
                elif command.lower().startswith("benchmark "):
                    self._benchmark_component(command[10:].strip())
                elif command.lower() == "history":
                    self._show_history()
                elif command.lower().startswith("load "):
                    self._load_module(command[5:].strip())
                elif command.lower().startswith("save "):
                    self._save_component(command[5:].strip())
                elif command.lower() == "clear":
                    self.console.clear()
                else:
                    self.console.print(
                        "[yellow]Unknown command. Type 'help' for available commands.[/yellow]"
                    )
            except Exception as e:
                self.console.print(f"[bold red]Error: {e!s}[/bold red]")
                import traceback

                self.console.print(traceback.format_exc())

    def _show_help(self):
        """Show help information."""
        help_md = """
        # Haive Interactive UI Commands

        ## General Commands
        - `help` - Show this help information
        - `exit`, `quit`, `q` - Exit the interactive UI
        - `clear` - Clear the console
        - `history` - Show command history

        ## Component Commands
        - `components` - List available components
        - `inspect <name>` - Inspect a component
        - `test <name>` - Test a component
        - `create <type> <name>` - Create a new component
        - `benchmark <name> [iterations]` - Benchmark a component
        - `save <name> <file>` - Save a component to a file
        - `load <module>` - Load a module with components

        ## Graph Commands
        - `graph create <name>` - Create a new graph
        - `graph add <graph> <node> <engine>` - Add a node to a graph
        - `graph connect <graph> <source> <target>` - Connect nodes
        - `graph compile <name>` - Compile a graph
        - `graph run <name> <input>` - Run a graph
        - `graph visualize <name>` - Visualize a graph

        ## Config Commands
        - `config create <name>` - Create a new config
        - `config add <config> <key> <value>` - Add a parameter to a config
        - `config show <name>` - Show a config
        - `config use <component> <config>` - Use a config with a component

        ## State Commands
        - `state` - Show the current state
        """

        self.console.print(Markdown(help_md))

    def _list_components(self):
        """List available components."""
        # Show engines from registry
        table = Table(title="Available Engines")
        table.add_column("Type", style="green")
        table.add_column("Name", style="blue")
        table.add_column("ID", style="yellow")

        for engine_type in EngineType:
            engines = self.registry.get_all(engine_type)
            for name, engine in engines.items():
                engine_id = getattr(engine, "id", "N/A")
                table.add_row(engine_type.value, name, str(engine_id))

        self.console.print(table)

        # Show other components
        if self.components:
            table = Table(title="Created Components")
            table.add_column("Type", style="green")
            table.add_column("Name", style="blue")

            for name, component in self.components.items():
                component_type = type(component).__name__
                table.add_row(component_type, name)

            self.console.print(table)

    def _inspect_component(self, name: str):
        """Inspect a component by name."""
        # Check registry first
        component = None

        # Try to find in registry
        for engine_type in EngineType:
            if component := self.registry.get(engine_type, name):
                break

        # Try local components if not found
        if not component and name in self.components:
            component = self.components[name]

        if not component:
            self.console.print(f"[red]Component '{name}' not found.[/red]")
            return

        # Inspect using debugger
        if isinstance(component, Engine):
            self.debugger.display_engine(component)
        elif isinstance(component, DynamicGraph):
            self.debugger.display_graph(component)
        else:
            # Generic inspection
            self.console.print(
                f"[bold]Component: {name} ({type(component).__name__})[/bold]"
            )

            # Get attributes
            attrs = {
                key: value
                for key, value in component.__dict__.items()
                if not key.startswith("_")
            }

            # Display in table
            table = Table(title=f"Attributes for {name}")
            table.add_column("Attribute", style="cyan")
            table.add_column("Value", style="green")
            table.add_column("Type", style="yellow")

            for attr_name, attr_value in attrs.items():
                value_str = str(attr_value)
                if len(value_str) > 50:
                    value_str = value_str[:47] + "..."

                table.add_row(attr_name, value_str, type(attr_value).__name__)

            self.console.print(table)

    def _test_component(self, name: str):
        """Test a component by name."""
        # Find component
        component = None

        # Try to find in registry
        for engine_type in EngineType:
            if component := self.registry.get(engine_type, name):
                break

        # Try local components if not found
        if not component and name in self.components:
            component = self.components[name]

        if not component:
            self.console.print(f"[red]Component '{name}' not found.[/red]")
            return

        # Test based on component type
        if isinstance(component, Engine):
            self._test_engine(component)
        elif isinstance(component, DynamicGraph):
            self._test_graph(component)
        else:
            self.console.print(
                f"[yellow]Don't know how to test component type: {type(component).__name__}[/yellow]"
            )

    def _test_engine(self, engine):
        """Test an engine component."""
        self.console.print(
            f"[bold]Testing Engine: {engine.name} ({engine.engine_type.value})[/bold]"
        )

        # Get test input
        if hasattr(engine, "derive_input_schema"):
            input_schema = engine.derive_input_schema()
            self.console.print(f"[blue]Input Schema: {input_schema.__name__}[/blue]")

            # Show fields
            if hasattr(input_schema, "model_fields"):
                # Pydantic v2
                for name, field in input_schema.model_fields.items():
                    self.console.print(f"  {name}: {field.annotation}")

        # Prompt for input
        test_input = Prompt.ask("[bold]Test input[/bold]")

        # Try to parse as JSON
        try:
            input_data = json.loads(test_input)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            input_data = test_input

        # Create runtime config
        config = RunnableConfigManager.create(thread_id="test-session")

        # Time execution
        with self.debugger.timer(f"test_{engine.name}"):
            try:
                # If invokable, use invoke
                if hasattr(engine, "invoke"):
                    result = engine.invoke(input_data, config)

                    # Display result
                    self.console.print("[bold green]Result:[/bold green]")
                    if isinstance(result, dict | list):
                        result_json = json.dumps(result, indent=2, default=str)
                        self.console.print(Syntax(result_json, "json"))
                    else:
                        self.console.print(str(result))
                else:
                    # Just instantiate
                    instance = engine.instantiate(config)
                    self.console.print(
                        f"[bold green]Instantiated: {type(instance).__name__}[/bold green]"
                    )
            except Exception as e:
                self.console.print(f"[bold red]Error: {e!s}[/bold red]")

    def _test_graph(self, graph):
        """Test a graph component."""
        self.console.print(f"[bold]Testing Graph: {graph.name}[/bold]")

        # Check if compiled
        if not hasattr(graph, "app") or graph.app is None:
            if Confirm.ask("Graph is not compiled. Compile now?", default=True):
                try:
                    graph.compile()
                    self.console.print("[green]Graph compiled successfully.[/green]")
                except Exception as e:
                    self.console.print(f"[red]Error compiling graph: {e!s}[/red]")
                    return
            else:
                return

        # Get test input
        test_input = Prompt.ask("[bold]Test input[/bold]")

        # Try to parse as JSON
        try:
            input_data = json.loads(test_input)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            input_data = test_input

        # Create runtime config
        config = RunnableConfigManager.create(thread_id="test-session")

        # Time execution
        with self.debugger.timer(f"test_{graph.name}"):
            try:
                # Run graph
                result = graph.app.invoke(input_data, config)

                # Display result
                self.console.print("[bold green]Result:[/bold green]")
                if isinstance(result, dict | list):
                    result_json = json.dumps(result, indent=2, default=str)
                    self.console.print(Syntax(result_json, "json"))
                else:
                    self.console.print(str(result))

                # Update state
                self.current_state = result
            except Exception as e:
                self.console.print(f"[bold red]Error: {e!s}[/bold red]")

    def _create_component(self, command):
        """Create a new component."""
        parts = command.split()
        if len(parts) < 2:
            self.console.print(
                "[red]Invalid command. Usage: create <type> <name> [params...][/red]"
            )
            return

        comp_type = parts[0].lower()
        comp_name = parts[1]

        if comp_type == "graph":
            # Create a graph
            self._create_graph(comp_name)
        elif comp_type == "config":
            # Create a config
            self._create_config(comp_name)
        else:
            self.console.print(f"[red]Unknown component type: {comp_type}[/red]")

    def _create_graph(self, name):
        """Create a new graph component."""
        # Import components
        from haive_core.graph.dynamic_graph_builder import DynamicGraph

        # Prompt for components
        component_list = Prompt.ask(
            "[bold]Enter comma-separated component names to include[/bold]", default=""
        )

        # Find components
        components = []
        if component_list:
            for comp_name in component_list.split(","):
                comp_name = comp_name.strip()

                # Try to find in registry
                component = None
                for engine_type in EngineType:
                    if component := self.registry.get(engine_type, comp_name):
                        break

                # Try local components if not found
                if not component and comp_name in self.components:
                    component = self.components[comp_name]

                if component:
                    components.append(component)
                else:
                    self.console.print(
                        f"[yellow]Warning: Component '{comp_name}' not found, skipping.[/yellow]"
                    )

        # Create graph
        try:
            graph = DynamicGraph(name=name, components=components)
            self.components[name] = graph
            self.console.print(
                f"[green]Created graph '{name}' with {len(components)} components.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error creating graph: {e!s}[/red]")

    def _create_config(self, name):
        """Create a new config component."""
        # Create empty config
        config = RunnableConfigManager.create(thread_id=f"config-{name}")
        self.components[name] = config
        self.console.print(f"[green]Created config '{name}'.[/green]")

    def _handle_graph_command(self, command):
        """Handle graph-related commands."""
        parts = command.split()
        if not parts:
            self.console.print("[red]Invalid graph command.[/red]")
            return

        subcommand = parts[0].lower()

        if subcommand == "create":
            if len(parts) < 2:
                self.console.print("[red]Usage: graph create <name>[/red]")
                return
            self._create_graph(parts[1])
        elif subcommand == "add":
            if len(parts) < 4:
                self.console.print(
                    "[red]Usage: graph add <graph> <node> <engine>[/red]"
                )
                return
            self._add_graph_node(parts[1], parts[2], parts[3])
        elif subcommand == "connect":
            if len(parts) < 4:
                self.console.print(
                    "[red]Usage: graph connect <graph> <source> <target>[/red]"
                )
                return
            self._connect_graph_nodes(parts[1], parts[2], parts[3])
        elif subcommand == "compile":
            if len(parts) < 2:
                self.console.print("[red]Usage: graph compile <name>[/red]")
                return
            self._compile_graph(parts[1])
        elif subcommand == "run":
            if len(parts) < 3:
                self.console.print("[red]Usage: graph run <name> <input>[/red]")
                return
            self._run_graph(parts[1], " ".join(parts[2:]))
        elif subcommand == "visualize":
            if len(parts) < 2:
                self.console.print("[red]Usage: graph visualize <name>[/red]")
                return
            self._visualize_graph(parts[1])
        else:
            self.console.print(f"[red]Unknown graph subcommand: {subcommand}[/red]")

    def _add_graph_node(self, graph_name, node_name, engine_name):
        """Add a node to a graph."""
        # Find graph
        if graph_name not in self.components:
            self.console.print(f"[red]Graph '{graph_name}' not found.[/red]")
            return

        graph = self.components[graph_name]
        if not isinstance(graph, DynamicGraph):
            self.console.print(f"[red]Component '{graph_name}' is not a graph.[/red]")
            return

        # Find engine
        engine = None
        for engine_type in EngineType:
            if engine := self.registry.get(engine_type, engine_name):
                break

        if not engine and engine_name in self.components:
            engine = self.components[engine_name]

        if not engine:
            self.console.print(f"[red]Engine '{engine_name}' not found.[/red]")
            return

        # Add node to graph
        try:
            graph.add_node(node_name, engine)
            self.console.print(
                f"[green]Added node '{node_name}' to graph '{graph_name}'.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error adding node: {e!s}[/red]")

    def _connect_graph_nodes(self, graph_name, source, target):
        """Connect nodes in a graph."""
        # Find graph
        if graph_name not in self.components:
            self.console.print(f"[red]Graph '{graph_name}' not found.[/red]")
            return

        graph = self.components[graph_name]
        if not isinstance(graph, DynamicGraph):
            self.console.print(f"[red]Component '{graph_name}' is not a graph.[/red]")
            return

        # Add edge to graph
        try:
            graph.add_edge(source, target)
            self.console.print(
                f"[green]Connected '{source}' to '{target}' in graph '{graph_name}'.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error connecting nodes: {e!s}[/red]")

    def _compile_graph(self, graph_name):
        """Compile a graph."""
        # Find graph
        if graph_name not in self.components:
            self.console.print(f"[red]Graph '{graph_name}' not found.[/red]")
            return

        graph = self.components[graph_name]
        if not isinstance(graph, DynamicGraph):
            self.console.print(f"[red]Component '{graph_name}' is not a graph.[/red]")
            return

        # Compile graph
        try:
            with self.debugger.timer(f"compile_{graph_name}"):
                graph.compile()
            self.console.print(
                f"[green]Graph '{graph_name}' compiled successfully.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error compiling graph: {e!s}[/red]")

    def _run_graph(self, graph_name, input_str):
        """Run a compiled graph."""
        # Find graph
        if graph_name not in self.components:
            self.console.print(f"[red]Graph '{graph_name}' not found.[/red]")
            return

        graph = self.components[graph_name]
        if not isinstance(graph, DynamicGraph):
            self.console.print(f"[red]Component '{graph_name}' is not a graph.[/red]")
            return

        # Check if compiled
        if not hasattr(graph, "app") or graph.app is None:
            if Confirm.ask("Graph is not compiled. Compile now?", default=True):
                try:
                    graph.compile()
                    self.console.print("[green]Graph compiled successfully.[/green]")
                except Exception as e:
                    self.console.print(f"[red]Error compiling graph: {e!s}[/red]")
                    return
            else:
                return

        # Parse input
        try:
            input_data = json.loads(input_str)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            input_data = input_str

        # Create runtime config
        config = RunnableConfigManager.create(thread_id=f"run-{graph_name}")

        # Run graph
        try:
            with self.debugger.timer(f"run_{graph_name}"):
                result = graph.app.invoke(input_data, config)

            # Display result
            self.console.print("[bold green]Result:[/bold green]")
            if isinstance(result, dict | list):
                result_json = json.dumps(result, indent=2, default=str)
                self.console.print(Syntax(result_json, "json"))
            else:
                self.console.print(str(result))

            # Update state
            self.current_state = result
        except Exception as e:
            self.console.print(f"[red]Error running graph: {e!s}[/red]")

    def _visualize_graph(self, graph_name):
        """Visualize a graph."""
        # Find graph
        if graph_name not in self.components:
            self.console.print(f"[red]Graph '{graph_name}' not found.[/red]")
            return

        graph = self.components[graph_name]
        if not isinstance(graph, DynamicGraph):
            self.console.print(f"[red]Component '{graph_name}' is not a graph.[/red]")
            return

        # Visualize graph
        try:
            # Use debugger to visualize
            self.debugger.display_graph(graph, visualize=True)
        except Exception as e:
            self.console.print(f"[red]Error visualizing graph: {e!s}[/red]")

    def _handle_config_command(self, command):
        """Handle config-related commands."""
        parts = command.split()
        if not parts:
            self.console.print("[red]Invalid config command.[/red]")
            return

        subcommand = parts[0].lower()

        if subcommand == "create":
            if len(parts) < 2:
                self.console.print("[red]Usage: config create <name>[/red]")
                return
            self._create_config(parts[1])
        elif subcommand == "add":
            if len(parts) < 4:
                self.console.print(
                    "[red]Usage: config add <config> <key> <value>[/red]"
                )
                return
            self._add_config_param(parts[1], parts[2], " ".join(parts[3:]))
        elif subcommand == "show":
            if len(parts) < 2:
                self.console.print("[red]Usage: config show <name>[/red]")
                return
            self._show_config(parts[1])
        elif subcommand == "use":
            if len(parts) < 3:
                self.console.print("[red]Usage: config use <component> <config>[/red]")
                return
            self._use_config(parts[1], parts[2])
        else:
            self.console.print(f"[red]Unknown config subcommand: {subcommand}[/red]")

    def _add_config_param(self, config_name, key, value_str):
        """Add a parameter to a config."""
        # Find config
        if config_name not in self.components:
            self.console.print(f"[red]Config '{config_name}' not found.[/red]")
            return

        config = self.components[config_name]

        # Parse value
        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            value = value_str

        # Add parameter
        try:
            if "configurable" not in config:
                config["configurable"] = {}

            config["configurable"][key] = value
            self.console.print(
                f"[green]Added parameter '{key}' to config '{config_name}'.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error adding parameter: {e!s}[/red]")

    def _show_config(self, config_name):
        """Show a config."""
        # Find config
        if config_name not in self.components:
            self.console.print(f"[red]Config '{config_name}' not found.[/red]")
            return

        config = self.components[config_name]

        # Display config
        self.console.print(f"[bold]Config: {config_name}[/bold]")
        config_json = json.dumps(config, indent=2, default=str)
        self.console.print(Syntax(config_json, "json"))

    def _use_config(self, component_name, config_name):
        """Use a config with a component."""
        # Find component
        component = None
        for engine_type in EngineType:
            if component := self.registry.get(engine_type, component_name):
                break

        if not component and component_name in self.components:
            component = self.components[component_name]

        if not component:
            self.console.print(f"[red]Component '{component_name}' not found.[/red]")
            return

        # Find config
        if config_name not in self.components:
            self.console.print(f"[red]Config '{config_name}' not found.[/red]")
            return

        config = self.components[config_name]

        # Use config with component
        try:
            if hasattr(component, "invoke"):
                # Prompt for input
                test_input = Prompt.ask("[bold]Test input[/bold]")

                # Try to parse as JSON
                try:
                    input_data = json.loads(test_input)
                except json.JSONDecodeError:
                    # Not JSON, treat as string
                    input_data = test_input

                # Invoke component with config
                with self.debugger.timer(f"invoke_{component_name}"):
                    result = component.invoke(input_data, config)

                # Display result
                self.console.print("[bold green]Result:[/bold green]")
                if isinstance(result, dict | list):
                    result_json = json.dumps(result, indent=2, default=str)
                    self.console.print(Syntax(result_json, "json"))
                else:
                    self.console.print(str(result))
            else:
                self.console.print(
                    "[yellow]Component does not support invoke method.[/yellow]"
                )
        except Exception as e:
            self.console.print(f"[red]Error using config: {e!s}[/red]")

    def _show_state(self):
        """Show the current state."""
        if not self.current_state:
            self.console.print("[yellow]No state available.[/yellow]")
            return

        # Use debugger to display state
        self.debugger.display_state(self.current_state)

    def _benchmark_component(self, command):
        """Benchmark a component."""
        parts = command.split()
        if not parts:
            self.console.print("[red]Invalid benchmark command.[/red]")
            return

        component_name = parts[0]
        iterations = 3  # Default iterations

        if len(parts) > 1:
            try:
                iterations = int(parts[1])
            except ValueError:
                self.console.print(
                    "[yellow]Invalid iteration count, using default (3).[/yellow]"
                )

        # Find component
        component = None
        for engine_type in EngineType:
            if component := self.registry.get(engine_type, component_name):
                break

        if not component and component_name in self.components:
            component = self.components[component_name]

        if not component:
            self.console.print(f"[red]Component '{component_name}' not found.[/red]")
            return

        # Benchmark based on component type
        if isinstance(component, Engine):
            self._benchmark_engine(component, iterations)
        elif isinstance(component, DynamicGraph):
            self._benchmark_graph(component, iterations)
        else:
            self.console.print(
                f"[yellow]Don't know how to benchmark component type: {type(component).__name__}[/yellow]"
            )

    def _benchmark_engine(self, engine, iterations):
        """Benchmark an engine component."""
        self.console.print(
            f"[bold]Benchmarking Engine: {engine.name} ({engine.engine_type.value})[/bold]"
        )

        # Get test input
        test_input = Prompt.ask("[bold]Test input[/bold]")

        # Try to parse as JSON
        try:
            input_data = json.loads(test_input)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            input_data = test_input

        # Create runtime config
        config = RunnableConfigManager.create(thread_id="benchmark-session")

        # Run benchmark
        with self.debugger.benchmark(f"engine_{engine.name}", iterations):
            try:
                if hasattr(engine, "invoke"):
                    for _ in range(iterations):
                        engine.invoke(input_data, config)
                else:
                    for _ in range(iterations):
                        engine.instantiate(config)
            except Exception as e:
                self.console.print(f"[red]Error during benchmark: {e!s}[/red]")

    def _benchmark_graph(self, graph, iterations):
        """Benchmark a graph component."""
        self.console.print(f"[bold]Benchmarking Graph: {graph.name}[/bold]")

        # Check if compiled
        if not hasattr(graph, "app") or graph.app is None:
            if Confirm.ask("Graph is not compiled. Compile now?", default=True):
                try:
                    graph.compile()
                    self.console.print("[green]Graph compiled successfully.[/green]")
                except Exception as e:
                    self.console.print(f"[red]Error compiling graph: {e!s}[/red]")
                    return
            else:
                return

        # Get test input
        test_input = Prompt.ask("[bold]Test input[/bold]")

        # Try to parse as JSON
        try:
            input_data = json.loads(test_input)
        except json.JSONDecodeError:
            # Not JSON, treat as string
            input_data = test_input

        # Create runtime config
        config = RunnableConfigManager.create(thread_id="benchmark-session")

        # Run benchmark
        with self.debugger.benchmark(f"graph_{graph.name}", iterations):
            try:
                for _ in range(iterations):
                    graph.app.invoke(input_data, config)
            except Exception as e:
                self.console.print(f"[red]Error during benchmark: {e!s}[/red]")

    def _show_history(self):
        """Show command history."""
        if not self.history:
            self.console.print("[yellow]No command history.[/yellow]")
            return

        self.console.print("[bold]Command History:[/bold]")
        for i, cmd in enumerate(self.history):
            self.console.print(f"{i+1}: {cmd}")

    def _load_module(self, module_path):
        """Load a module with components."""
        try:
            # Import module
            module = importlib.import_module(module_path)
            self.console.print(f"[green]Loaded module {module_path}[/green]")

            # Look for engines to register
            engines_found = 0

            for _name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, Engine) and obj != Engine:
                    # Try to instantiate and register
                    try:
                        engine = obj()
                        engine.register()
                        engines_found += 1
                    except Exception:
                        pass

            self.console.print(
                f"[green]Found and registered {engines_found} engines.[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error loading module: {e!s}[/red]")

    def _save_component(self, command):
        """Save a component to a file."""
        parts = command.split()
        if len(parts) < 2:
            self.console.print("[red]Usage: save <name> <file>[/red]")
            return

        component_name = parts[0]
        file_path = parts[1]

        # Find component
        component = None
        for engine_type in EngineType:
            if component := self.registry.get(engine_type, component_name):
                break

        if not component and component_name in self.components:
            component = self.components[component_name]

        if not component:
            self.console.print(f"[red]Component '{component_name}' not found.[/red]")
            return

        # Save component
        try:
            # Convert to dict
            if hasattr(component, "to_dict"):
                data = component.to_dict()
            elif hasattr(component, "model_dump"):
                # Pydantic v2
                data = component.model_dump()
            elif hasattr(component, "dict"):
                # Pydantic v1
                data = component.dict()
            else:
                self.console.print("[red]Component cannot be serialized.[/red]")
                return

            # Save to file
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2, default=str)

            self.console.print(
                f"[green]Component '{component_name}' saved to {file_path}[/green]"
            )
        except Exception as e:
            self.console.print(f"[red]Error saving component: {e!s}[/red]")
