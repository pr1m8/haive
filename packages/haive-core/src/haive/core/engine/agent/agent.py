"""
Agent - Base class for all agent implementations in the Haive framework.

This module provides the core agent architecture with consistent schema handling,
execution flows, persistence management, and extensibility through patterns.
All agent implementations conform to the protocol interfaces for consistent API access.
"""

from __future__ import annotations

import asyncio
import json
import logging
import os
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Generator
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
)

from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph
from pydantic import BaseModel

# Haive core imports
from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.agent.config import AgentConfig

# Import protocol definitions
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.persistence.handlers import (
    ensure_async_pool_open,
    ensure_pool_open,
    prepare_merged_input,
    register_async_thread_if_needed,
    register_thread_if_needed,
    setup_async_checkpointer,
    setup_checkpointer,
)
from haive.core.persistence.types import CheckpointerMode
from haive.core.schema.schema_composer import SchemaComposer
from haive.core.utils.pydantic_utils import ensure_json_serializable

# Rich UI imports - handle gracefully if not available
try:
    from rich.console import Console
    from rich.live import Live
    from rich.logging import RichHandler
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.progress import (
        BarColumn,
        Progress,
        SpinnerColumn,
        TaskProgressColumn,
        TextColumn,
    )
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.traceback import install as install_rich_traceback
    from rich.tree import Tree

    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

# Set up logging
logger = logging.getLogger(__name__)

# Agent registry maps config classes to agent classes
AGENT_REGISTRY: Dict[Type[AgentConfig], Type[Agent]] = {}


def register_agent(config_class: Type[AgentConfig]):
    """Register an agent class with its configuration class."""

    def decorator(agent_class: Type[Agent]):
        AGENT_REGISTRY[config_class] = agent_class
        # Set reference to config class on agent class
        agent_class.config_class = config_class
        logger.info(
            f"Registered agent class {agent_class.__name__} for config {config_class.__name__}"
        )
        return agent_class

    return decorator


TConfig = TypeVar("TConfig", bound="AgentConfig")  # Required
TIn = TypeVar("TIn")  # Defaults to Any in practice
TOut = TypeVar("TOut")  # Defaults to Any in practice
TState = TypeVar("TState", bound=Optional[BaseModel])  # Defaults to None in practice


class Agent(Generic[TConfig], ABC):
    """
    Base agent architecture class for all agent implementations.

    Type Parameters:
        TConfig: Type of agent configuration
        TIn: Type of input data (defaults to Any)
        TOut: Type of output data (defaults to Any)
        TState: Type of state data (defaults to Optional[BaseModel])
    """

    def __init__(
        self, config: TConfig, verbose: bool = False, rich_logging: bool = True
    ):
        """
        Initialize the agent with its configuration.

        Args:
            config: Agent configuration
            verbose: Whether to enable verbose logging
            rich_logging: Whether to use rich UI for logging and debugging
        """
        self.config = config
        self.verbose = verbose
        self.rich_logging = rich_logging and RICH_AVAILABLE
        self._async_context_managers = {}  # Store async context managers
        self._async_checkpointer = None  # Async checkpointer instance
        self._checkpoint_mode = getattr(config, "checkpoint_mode", "sync")
        self._async_setup_pending = False  # Track if async setup is pending

        self._async_setup_task = None  # Store async setup task

        # Set up rich UI if available and requested
        if self.rich_logging:
            self._setup_rich_ui()

        # Configure logging
        self._setup_logging()

        # Print agent initialization banner
        self._log_agent_init()

        logger.info(f"Initializing agent: {config.name}")

        # Clear initialization order to prevent confusion
        # 1. Setup output directories
        self._setup_directories()

        # 2. Setup schemas first (needed for everything else)
        self._setup_schemas()

        # 3. Setup engines (needed for graph building)
        self._initialize_engines()

        # 4. Setup persistence (needed for compilation)
        if config.checkpoint_mode == "sync":
            self._setup_persistence()
        else:
            # Check if we're already in an event loop
            try:
                asyncio.get_running_loop()
                # We're in an event loop, so we need to handle this differently
                # Set up a basic sync checkpointer as fallback and mark async setup as pending
                self._setup_persistence()  # Set up sync fallback first
                self._async_setup_pending = True
                self._async_setup_task = None
                logger.warning(
                    "Agent initialized in async context with async checkpoint mode. "
                    "Call await agent._complete_async_setup() before using the agent."
                )
            except RuntimeError:
                # No event loop running, safe to use asyncio.run()
                asyncio.run(self._asetup_persistence())
                self._async_setup_pending = False

        # 5. Setup runtime configuration
        self._setup_runtime_config()

        # Now we have all prerequisites to build the graph
        self._create_graph_builder()

        # Create the state graph with the proper schemas
        self.graph = StateGraph(
            input=self.input_schema,
            output=self.output_schema,
            state_schema=self.state_schema,
            config_schema=self.config,
        )

        # Allow subclass to set up workflow
        logger.info(f"Setting up workflow for {config.name}")
        self.setup_workflow()

        # Process node configurations if provided
        self._process_node_configs()

        # Compile the graph
        self.compile()

        # Apply patterns after compilation if configured
        self._apply_configured_patterns()

        # Generate visualization if requested
        if getattr(self.config, "visualize", True) and hasattr(self, "graph"):
            self.visualize_graph()

        self._log_agent_ready()

    def set_traceback_mode(self, mode: str = "minimal"):
        """Control traceback verbosity.

        Args:
            mode: 'minimal', 'normal', or 'verbose'
        """
        if not RICH_AVAILABLE:
            return

        if mode == "minimal":
            install_rich_traceback(show_locals=False, max_frames=3)
        elif mode == "normal":
            install_rich_traceback(show_locals=False, max_frames=10)
        elif mode == "verbose":
            install_rich_traceback(show_locals=True, max_frames=20)
        else:
            install_rich_traceback(show_locals=False, max_frames=5)

    def debug_simple(self, message: str, data: Any = None):
        """Simple debug output without full traceback."""
        if self.verbose:
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(f"[bold yellow]DEBUG:[/bold yellow] {message}")
                if data is not None:
                    self.console.print(f"[dim]{data}[/dim]")
            else:
                logger.debug(f"DEBUG: {message}")
                if data is not None:
                    logger.debug(f"  Data: {data}")

    def _setup_rich_ui(self):
        """Configure rich UI for debugging."""
        if not RICH_AVAILABLE:
            logger.warning(
                "Rich UI requested but rich library not installed. Install with: pip install rich"
            )
            return

        # Install rich traceback handler with minimal output
        install_rich_traceback(show_locals=False, max_frames=5)

        # Set up console
        self.console = Console(record=True, width=120)

        # Create a logger console (can be different from main console)
        self.log_console = Console(stderr=True, width=100)

        # Create debug console for detailed output
        self.debug_console = Console(width=120)

        # Show initialization banner
        self.console.print(
            Panel.fit(
                f"[bold blue]Haive Agent: [green]{getattr(self.config, 'name', 'Unnamed')}[/green][/bold blue]",
                border_style="blue",
                title="Initializing",
                subtitle=f"v{getattr(self.config, 'version', '1.0.0')}",
            )
        )

    def _setup_logging(self):
        """Configure logging with rich or standard handlers."""
        # Get the agent's logger
        agent_logger = logging.getLogger(__name__)

        # Set level based on verbosity
        log_level = logging.DEBUG if self.verbose else logging.INFO
        agent_logger.setLevel(log_level)

        # Clear existing handlers
        if agent_logger.handlers:
            agent_logger.handlers.clear()

        if self.rich_logging and RICH_AVAILABLE:
            # Add rich handler
            rich_handler = RichHandler(
                console=getattr(self, "log_console", Console(stderr=True)),
                rich_tracebacks=True,
                markup=True,
                show_time=True,
                show_path=False,
            )
            rich_handler.setLevel(log_level)
            agent_logger.addHandler(rich_handler)

            # Set format for rich handler
            rich_format = logging.Formatter("%(message)s")
            rich_handler.setFormatter(rich_format)

            # Set parent logger to avoid duplicate logs
            agent_logger.propagate = False
        else:
            # Add standard handler
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            handler.setLevel(log_level)
            agent_logger.addHandler(handler)

        # Set related loggers to appropriate level
        for module in [
            "haive.core.graph",
            "haive.core.engine",
            "haive.core.schema",
            "haive.core.graph.node",
            "haive.core.persistence",
            "haive.core.engine.aug_llm",
        ]:
            module_logger = logging.getLogger(module)
            module_logger.setLevel(log_level)

            # Apply rich handler to module loggers if available
            if self.rich_logging and RICH_AVAILABLE:
                # Remove existing handlers
                if module_logger.handlers:
                    module_logger.handlers.clear()

                module_logger.addHandler(rich_handler)
                module_logger.propagate = False

    def _log_agent_init(self):
        """Display rich initialization information."""
        if not self.rich_logging or not RICH_AVAILABLE:
            return

        # Create a table for agent configuration
        table = Table(
            title=f"[bold]Agent Configuration: [green]{self.config.name}[/green][/bold]"
        )
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="green")

        # Add configuration details
        for key, value in self.config.__dict__.items():
            if key.startswith("_"):
                continue

            # Format complex objects
            if isinstance(value, dict):
                value_str = f"{len(value)} items"
            elif isinstance(value, list):
                value_str = f"{len(value)} entries"
            elif isinstance(value, BaseModel):
                value_str = f"{type(value).__name__}"
            elif callable(value):
                value_str = f"<function {value.__name__}>"
            else:
                value_str = str(value)

            # Truncate long values
            if len(value_str) > 50:
                value_str = value_str[:47] + "..."

            table.add_row(key, value_str)

        self.console.print(table)

    def _log_agent_ready(self):
        """Display rich ready notification."""
        if not self.rich_logging or not RICH_AVAILABLE:
            return

        self.console.print(
            Panel.fit(
                f"[bold green]Agent {self.config.name} Ready[/bold green]\n"
                f"[cyan]Workflow nodes:[/cyan] {len(self.graph.nodes) if hasattr(self.graph, 'nodes') else 0}\n"
                f"[cyan]Schema fields:[/cyan] {len(self.state_schema.model_fields) if hasattr(self.state_schema, 'model_fields') else 0}\n"
                f"[cyan]Persistence:[/cyan] {type(self.checkpointer).__name__}\n"
                f"[cyan]Checkpoint mode:[/cyan] {self._checkpoint_mode}\n"
                f"[cyan]Runnable config:[/cyan] {self.config.runnable_config}",
                border_style="green",
                title="Agent Ready",
                subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
        )

    def _setup_directories(self):
        """Set up directories for outputs and artifacts."""
        # Ensure output directory exists
        Path(self.config.output_dir).mkdir(parents=True, exist_ok=True)

        # Set up state history directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.state_history_dir = Path(self.config.output_dir) / "state_history"
        self.state_history_dir.mkdir(exist_ok=True)
        self.state_filename = (
            self.state_history_dir / f"{self.config.name}_{timestamp}.json"
        )

        # Set up graphs directory
        self.graphs_dir = Path(self.config.output_dir) / "graphs"
        self.graphs_dir.mkdir(exist_ok=True)
        self.graph_image_path = self.graphs_dir / f"{self.config.name}_{timestamp}.png"

        # Set up debug logs directory
        self.debug_dir = Path(self.config.output_dir) / "debug_logs"
        self.debug_dir.mkdir(exist_ok=True)
        self.debug_log_path = self.debug_dir / f"{self.config.name}_{timestamp}.log"

        if self.rich_logging and RICH_AVAILABLE:
            if hasattr(self, "console"):
                self.console.print(
                    f"[blue]Created output directories in:[/blue] {self.config.output_dir}"
                )

        logger.debug(f"Output directories set up for {self.config.name}")

    def _setup_schemas(self):
        """Set up state, input, and output schemas with rich debugging."""
        if self.rich_logging and RICH_AVAILABLE:
            # Create schema setup progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[bold blue]Setting up schemas...[/bold blue]"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console,
            ) as progress:
                state_task = progress.add_task("Setting up state schema...", total=100)
                input_task = progress.add_task(
                    "Setting up input schema...", total=100, start=False
                )
                output_task = progress.add_task(
                    "Setting up output schema...", total=100, start=False
                )

                # Process state schema
                if (
                    hasattr(self.config, "state_schema")
                    and self.config.state_schema is not None
                ):
                    progress.update(
                        state_task,
                        advance=20,
                        description="[bold blue]Building state schema from config...[/bold blue]",
                    )

                    if isinstance(self.config.state_schema, dict):
                        # Build from dictionary definition
                        logger.debug(
                            f"Building state schema from dictionary for {self.config.name}"
                        )
                        schema_composer = SchemaComposer(
                            name=f"{self.config.name}State"
                        )

                        # Progress through fields
                        field_count = len(self.config.state_schema)
                        for _i, (field_name, field_info) in enumerate(
                            self.config.state_schema.items()
                        ):
                            progress.update(state_task, advance=60 / field_count)

                            if isinstance(field_info, tuple):
                                # (type, default) format
                                field_type, default_value = field_info
                                schema_composer.add_field(
                                    field_name, field_type, default=default_value
                                )
                            elif isinstance(field_info, dict):
                                # Dict with parameters
                                field_type = field_info.pop("type", Any)
                                schema_composer.add_field(
                                    field_name, field_type, **field_info
                                )
                            else:
                                # Just a type
                                schema_composer.add_field(field_name, field_info)

                        progress.update(
                            state_task,
                            advance=20,
                            description="[bold blue]Building state schema class...[/bold blue]",
                        )
                        self.state_schema = schema_composer.build()
                    else:
                        # Use provided class
                        progress.update(
                            state_task,
                            advance=80,
                            description="[bold blue]Using provided state schema...[/bold blue]",
                        )
                        logger.debug(
                            f"Using provided state schema for {self.config.name}"
                        )
                        self.state_schema = self.config.state_schema
                else:
                    # Derive from components
                    progress.update(
                        state_task,
                        advance=50,
                        description="[bold blue]Deriving state schema from components...[/bold blue]",
                    )
                    logger.debug(f"Deriving state schema for {self.config.name}")
                    self.state_schema = self.config.derive_schema()
                    progress.update(state_task, advance=30)

                progress.update(
                    state_task,
                    completed=100,
                    description="[bold green]State schema setup complete[/bold green]",
                )
                progress.start_task(input_task)

                # Process input schema
                if (
                    hasattr(self.config, "input_schema")
                    and self.config.input_schema is not None
                ):
                    progress.update(
                        input_task,
                        advance=20,
                        description="[bold blue]Building input schema from config...[/bold blue]",
                    )

                    if isinstance(self.config.input_schema, dict):
                        # Build from dictionary
                        logger.debug(f"Building input schema for {self.config.name}")
                        schema_composer = SchemaComposer(
                            name=f"{self.config.name}Input"
                        )

                        # Progress through fields
                        field_count = len(self.config.input_schema)
                        for _i, (field_name, field_info) in enumerate(
                            self.config.input_schema.items()
                        ):
                            progress.update(input_task, advance=60 / field_count)

                            if isinstance(field_info, tuple):
                                field_type, default_value = field_info
                                schema_composer.add_field(
                                    field_name, field_type, default=default_value
                                )
                            elif isinstance(field_info, dict):
                                field_type = field_info.pop("type", Any)
                                schema_composer.add_field(
                                    field_name, field_type, **field_info
                                )
                            else:
                                schema_composer.add_field(field_name, field_info)

                        progress.update(
                            input_task,
                            advance=20,
                            description="[bold blue]Building input schema class...[/bold blue]",
                        )
                        self.input_schema = schema_composer.build()
                    else:
                        # Use provided class
                        progress.update(
                            input_task,
                            advance=80,
                            description="[bold blue]Using provided input schema...[/bold blue]",
                        )
                        logger.debug(
                            f"Using provided input schema for {self.config.name}"
                        )
                        self.input_schema = self.config.input_schema
                else:
                    # Derive using config's derivation method
                    progress.update(
                        input_task,
                        advance=80,
                        description="[bold blue]Deriving input schema...[/bold blue]",
                    )
                    logger.debug(f"Deriving input schema for {self.config.name}")
                    self.input_schema = self.config.derive_input_schema()

                progress.update(
                    input_task,
                    completed=100,
                    description="[bold green]Input schema setup complete[/bold green]",
                )
                progress.start_task(output_task)

                # Process output schema
                if (
                    hasattr(self.config, "output_schema")
                    and self.config.output_schema is not None
                ):
                    progress.update(
                        output_task,
                        advance=20,
                        description="[bold blue]Building output schema from config...[/bold blue]",
                    )

                    if isinstance(self.config.output_schema, dict):
                        # Build from dictionary
                        logger.debug(f"Building output schema for {self.config.name}")
                        schema_composer = SchemaComposer(
                            name=f"{self.config.name}Output"
                        )

                        # Progress through fields
                        field_count = len(self.config.output_schema)
                        for _i, (field_name, field_info) in enumerate(
                            self.config.output_schema.items()
                        ):
                            progress.update(output_task, advance=60 / field_count)

                            if isinstance(field_info, tuple):
                                field_type, default_value = field_info
                                schema_composer.add_field(
                                    field_name, field_type, default=default_value
                                )
                            elif isinstance(field_info, dict):
                                field_type = field_info.pop("type", Any)
                                schema_composer.add_field(
                                    field_name, field_type, **field_info
                                )
                            else:
                                schema_composer.add_field(field_name, field_info)

                        progress.update(
                            output_task,
                            advance=20,
                            description="[bold blue]Building output schema class...[/bold blue]",
                        )
                        self.output_schema = schema_composer.build()
                    else:
                        # Use provided class
                        progress.update(
                            output_task,
                            advance=80,
                            description="[bold blue]Using provided output schema...[/bold blue]",
                        )
                        logger.debug(
                            f"Using provided output schema for {self.config.name}"
                        )
                        self.output_schema = self.config.output_schema
                else:
                    # Derive using config's derivation method
                    progress.update(
                        output_task,
                        advance=80,
                        description="[bold blue]Deriving output schema...[/bold blue]",
                    )
                    logger.debug(f"Deriving output schema for {self.config.name}")
                    self.output_schema = self.config.derive_output_schema()

                progress.update(
                    output_task,
                    completed=100,
                    description="[bold green]Output schema setup complete[/bold green]",
                )

            # Print schema details
            self._debug_print_schemas()
        else:
            # Non-rich implementation
            # Process state schema
            if (
                hasattr(self.config, "state_schema")
                and self.config.state_schema is not None
            ):
                if isinstance(self.config.state_schema, dict):
                    # Build from dictionary definition
                    logger.debug(
                        f"Building state schema from dictionary for {self.config.name}"
                    )
                    schema_composer = SchemaComposer(name=f"{self.config.name}State")
                    for field_name, field_info in self.config.state_schema.items():
                        if isinstance(field_info, tuple):
                            field_type, default_value = field_info
                            schema_composer.add_field(
                                field_name, field_type, default=default_value
                            )
                        elif isinstance(field_info, dict):
                            field_type = field_info.pop("type", Any)
                            schema_composer.add_field(
                                field_name, field_type, **field_info
                            )
                        else:
                            schema_composer.add_field(field_name, field_info)
                    self.state_schema = schema_composer.build()
                else:
                    # Use provided class
                    logger.debug(f"Using provided state schema for {self.config.name}")
                    self.state_schema = self.config.state_schema
            else:
                # Derive from components
                logger.debug(f"Deriving state schema for {self.config.name}")
                self.state_schema = self.config.derive_schema()

            # Process input schema
            if (
                hasattr(self.config, "input_schema")
                and self.config.input_schema is not None
            ):
                if isinstance(self.config.input_schema, dict):
                    # Build from dictionary
                    logger.debug(f"Building input schema for {self.config.name}")
                    schema_composer = SchemaComposer(name=f"{self.config.name}Input")
                    for field_name, field_info in self.config.input_schema.items():
                        if isinstance(field_info, tuple):
                            field_type, default_value = field_info
                            schema_composer.add_field(
                                field_name, field_type, default=default_value
                            )
                        elif isinstance(field_info, dict):
                            field_type = field_info.pop("type", Any)
                            schema_composer.add_field(
                                field_name, field_type, **field_info
                            )
                        else:
                            schema_composer.add_field(field_name, field_info)
                    self.input_schema = schema_composer.build()
                else:
                    # Use provided class
                    logger.debug(f"Using provided input schema for {self.config.name}")
                    self.input_schema = self.config.input_schema
            else:
                # Derive using config's derivation method
                logger.debug(f"Deriving input schema for {self.config.name}")
                self.input_schema = self.config.derive_input_schema()

            # Process output schema
            if (
                hasattr(self.config, "output_schema")
                and self.config.output_schema is not None
            ):
                if isinstance(self.config.output_schema, dict):
                    # Build from dictionary
                    logger.debug(f"Building output schema for {self.config.name}")
                    schema_composer = SchemaComposer(name=f"{self.config.name}Output")
                    for field_name, field_info in self.config.output_schema.items():
                        if isinstance(field_info, tuple):
                            field_type, default_value = field_info
                            schema_composer.add_field(
                                field_name, field_type, default=default_value
                            )
                        elif isinstance(field_info, dict):
                            field_type = field_info.pop("type", Any)
                            schema_composer.add_field(
                                field_name, field_type, **field_info
                            )
                        else:
                            schema_composer.add_field(field_name, field_info)
                    self.output_schema = schema_composer.build()
                else:
                    # Use provided class
                    logger.debug(f"Using provided output schema for {self.config.name}")
                    self.output_schema = self.config.output_schema
            else:
                # Derive using config's derivation method
                logger.debug(f"Deriving output schema for {self.config.name}")
                self.output_schema = self.config.derive_output_schema()

        logger.debug(f"Schemas set up successfully for {self.config.name}")

    def _debug_print_schemas(self):
        """Print schema details using rich UI."""
        if not self.rich_logging or not RICH_AVAILABLE:
            return

        # Create a table for all schemas
        schema_table = Table(title="[bold]Schema Definitions[/bold]")
        schema_table.add_column("Schema", style="cyan")
        schema_table.add_column("Field", style="green")
        schema_table.add_column("Type", style="magenta")
        schema_table.add_column("Default", style="yellow")

        # Helper to extract field info
        def extract_field_info(schema):
            fields = {}
            if hasattr(schema, "model_fields"):
                # Pydantic v2
                for name, field in schema.model_fields.items():
                    fields[name] = {"type": field.annotation, "default": field.default}
            elif hasattr(schema, "__fields__"):
                # Pydantic v1
                for name, field in schema.__fields__.items():
                    fields[name] = {"type": field.type_, "default": field.default}
            return fields

        # Add state schema
        state_fields = extract_field_info(self.state_schema)
        for field_name, info in state_fields.items():
            type_str = str(info["type"]).replace("typing.", "")
            default_str = str(info["default"])
            if len(default_str) > 30:
                default_str = default_str[:27] + "..."
            schema_table.add_row("State", field_name, type_str, default_str)

        # Add input schema if different from state
        if self.input_schema != self.state_schema:
            input_fields = extract_field_info(self.input_schema)
            for field_name, info in input_fields.items():
                type_str = str(info["type"]).replace("typing.", "")
                default_str = str(info["default"])
                if len(default_str) > 30:
                    default_str = default_str[:27] + "..."
                schema_table.add_row("Input", field_name, type_str, default_str)

        # Add output schema if different from state
        if (
            self.output_schema != self.state_schema
            and self.output_schema != self.input_schema
        ):
            output_fields = extract_field_info(self.output_schema)
            for field_name, info in output_fields.items():
                type_str = str(info["type"]).replace("typing.", "")
                default_str = str(info["default"])
                if len(default_str) > 30:
                    default_str = default_str[:27] + "..."
                schema_table.add_row("Output", field_name, type_str, default_str)

        # Print the table
        self.console.print(schema_table)

        # Show shared schema notice if needed
        if self.input_schema == self.state_schema:
            self.console.print(
                "[yellow]Note:[/yellow] Input schema is using the state schema"
            )
        if self.output_schema == self.state_schema:
            self.console.print(
                "[yellow]Note:[/yellow] Output schema is using the state schema"
            )

    def _initialize_engines(self):
        """Initialize all engines from configuration with rich UI."""
        self.engines = {}

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            engine_table = Table(title="[bold]Engine Initialization[/bold]")
            engine_table.add_column("Name", style="cyan")
            engine_table.add_column("Type", style="green")
            engine_table.add_column("ID", style="yellow")
            engine_table.add_column("Model", style="magenta")
            engine_table.add_column("Status", style="blue")

            # Initialize main engine if present
            if hasattr(self.config, "engine") and self.config.engine is not None:
                engine_name = "main"
                engine_type = getattr(self.config.engine, "engine_type", "unknown")
                engine_id = getattr(self.config.engine, "id", "not-set")
                engine_model = getattr(
                    self.config.engine,
                    "model",
                    getattr(self.config.engine, "model_name", "unknown"),
                )

                with self.console.status(
                    "[bold blue]Initializing main engine...[/bold blue]"
                ):
                    self.engine = self.config.engine
                    self.engines[engine_name] = self.engine

                engine_table.add_row(
                    engine_name,
                    str(engine_type),
                    str(engine_id),
                    str(engine_model),
                    "[green]✓[/green]",
                )

            # Initialize additional engines
            for name, engine_config in getattr(self.config, "engines", {}).items():
                engine_type = getattr(engine_config, "engine_type", "unknown")
                engine_id = getattr(engine_config, "id", "not-set")
                engine_model = getattr(
                    engine_config,
                    "model",
                    getattr(engine_config, "model_name", "unknown"),
                )

                with self.console.status(
                    f"[bold blue]Initializing engine '{name}'...[/bold blue]"
                ):
                    self.engines[name] = engine_config

                engine_table.add_row(
                    name,
                    str(engine_type),
                    str(engine_id),
                    str(engine_model),
                    "[green]✓[/green]",
                )

            # Process any subagent engines
            if hasattr(self.config, "subagents") and self.config.subagents:
                for name, subagent_config in self.config.subagents.items():
                    with self.console.status(
                        f"[bold blue]Processing subagent '{name}'...[/bold blue]"
                    ):
                        # We'll store the config for now, actual instantiation happens later
                        self.engines[f"subagent:{name}"] = subagent_config

                    engine_table.add_row(
                        f"subagent:{name}",
                        "agent",
                        getattr(subagent_config, "id", "not-set"),
                        getattr(subagent_config, "name", "unknown"),
                        "[green]✓[/green]",
                    )

            self.console.print(engine_table)
            self.console.print(
                f"[green]Successfully initialized {len(self.engines)} engines[/green]"
            )
        else:
            # Initialize main engine if present
            if hasattr(self.config, "engine") and self.config.engine is not None:
                engine_name = "main"
                logger.debug(f"Initializing main engine for {self.config.name}")
                self.engine = self.config.engine
                self.engines[engine_name] = self.engine
                logger.debug(
                    f"Main engine initialized: {getattr(self.engine, 'name', 'unknown')}"
                )

            # Initialize additional engines
            for name, engine_config in getattr(self.config, "engines", {}).items():
                logger.debug(f"Initializing engine '{name}' for {self.config.name}")
                self.engines[name] = engine_config
                logger.debug(
                    f"Engine '{name}' initialized: {getattr(self.engines[name], 'name', 'unknown')}"
                )

            # Process any subagent engines
            if hasattr(self.config, "subagents") and self.config.subagents:
                for name, subagent_config in self.config.subagents.items():
                    logger.debug(f"Processing subagent '{name}' for {self.config.name}")
                    self.engines[f"subagent:{name}"] = subagent_config

        logger.debug(f"Initialized {len(self.engines)} engines for {self.config.name}")

    def _setup_persistence(self):
        """Set up synchronous persistence with proper checkpointer."""
        # Determine checkpoint mode
        if hasattr(self.config, "checkpoint_mode"):
            self._checkpoint_mode = self.config.checkpoint_mode
        elif hasattr(self.config, "persistence") and hasattr(
            self.config.persistence, "mode"
        ):
            # Use mode from persistence config if available
            self._checkpoint_mode = (
                "async"
                if self.config.persistence.mode == CheckpointerMode.ASYNC
                else "sync"
            )

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                "[bold blue]Setting up synchronous persistence...[/bold blue]"
            ):
                # Set up standard synchronous checkpointer
                self.checkpointer = setup_checkpointer(self.config)

                # Add store if configured
                self.store = None
                if getattr(self.config, "add_store", False):
                    from langgraph.store.base import BaseStore

                    self.store = BaseStore()

            # Show persistence info
            persistence_type = type(self.checkpointer).__name__
            if "Postgres" in persistence_type:
                status_color = "blue"
                status_icon = "🐘"  # PostgreSQL elephant
            elif "Memory" in persistence_type:
                status_color = "yellow"
                status_icon = "💾"  # Memory icon
            else:
                status_color = "green"
                status_icon = "📦"  # Generic storage

            self.console.print(
                f"[bold]Persistence:[/bold] {status_icon} [{status_color}]{persistence_type}[/{status_color}] "
                f"[dim](sync mode)[/dim]"
            )

            if hasattr(self, "store") and self.store:
                self.console.print("[bold]Store:[/bold] ✅ Enabled")
        else:
            # Standard synchronous checkpointer setup
            self.checkpointer = setup_checkpointer(self.config)
            logger.debug(
                f"Synchronous checkpointer set up for {self.config.name}: {type(self.checkpointer).__name__}"
            )

            # Add store if configured
            self.store = None
            if getattr(self.config, "add_store", False):
                from langgraph.store.base import BaseStore

                self.store = BaseStore()
                logger.debug("BaseStore added to agent")

    async def _asetup_persistence(self):
        """Set up asynchronous persistence with proper checkpointer."""
        # Determine checkpoint mode
        if hasattr(self.config, "checkpoint_mode"):
            self._checkpoint_mode = self.config.checkpoint_mode
        elif hasattr(self.config, "persistence") and hasattr(
            self.config.persistence, "mode"
        ):
            # Use mode from persistence config if available
            self._checkpoint_mode = (
                "async"
                if self.config.persistence.mode == CheckpointerMode.ASYNC
                else "sync"
            )

        # Set the mode to async explicitly
        self._checkpoint_mode = "async"

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                "[bold blue]Setting up asynchronous persistence...[/bold blue]"
            ) as status:
                # Initialize async resources
                self._async_checkpointer = None
                self._async_context_managers = {}

                # Always set up a synchronous checkpointer as fallback
                self.checkpointer = setup_checkpointer(self.config)

                # Create the async checkpointer
                try:
                    self._async_checkpointer = await setup_async_checkpointer(
                        self.config
                    )
                    status.update(
                        "[bold blue]Async checkpointer created successfully[/bold blue]"
                    )

                    # Verify it's actually an async checkpointer
                    if hasattr(self._async_checkpointer, "__class__"):
                        checkpointer_name = self._async_checkpointer.__class__.__name__
                        if "Async" not in checkpointer_name:
                            self.console.print(
                                f"[bold yellow]Warning: Expected async checkpointer but got {checkpointer_name}[/bold yellow]"
                            )
                            logger.warning(
                                f"Expected async checkpointer but got {checkpointer_name}"
                            )
                        else:
                            logger.info(
                                f"Successfully created async checkpointer: {checkpointer_name}"
                            )

                except (NotImplementedError, AttributeError) as e:
                    self.console.print(
                        f"[bold yellow]Async checkpointer not supported: {e}[/bold yellow]"
                    )
                    self.console.print(
                        "[yellow]Using synchronous checkpointer for async operations[/yellow]"
                    )
                    logger.warning(f"Async checkpointer not supported: {e}")
                    logger.info(
                        "Will use synchronous checkpointer for async operations"
                    )
                    self._async_checkpointer = None
                except Exception as e:
                    self.console.print(
                        f"[bold red]Error creating async checkpointer: {e}[/bold red]"
                    )
                    self.console.print(
                        "[yellow]Falling back to synchronous checkpointer[/yellow]"
                    )
                    logger.error(f"Failed to create async checkpointer: {e}")
                    logger.warning("Falling back to synchronous checkpointer")
                    self._async_checkpointer = None

                # Add store if configured
                self.store = None
                if getattr(self.config, "add_store", False):
                    from langgraph.store.base import BaseStore

                    self.store = BaseStore()

            # Show persistence info
            persistence_type = type(
                self._async_checkpointer or self.checkpointer
            ).__name__
            if "Postgres" in persistence_type:
                status_color = "blue"
                status_icon = "🐘"  # PostgreSQL elephant
            elif "Memory" in persistence_type:
                status_color = "yellow"
                status_icon = "💾"  # Memory icon
            else:
                status_color = "green"
                status_icon = "📦"  # Generic storage

            self.console.print(
                f"[bold]Async Persistence:[/bold] {status_icon} [{status_color}]{persistence_type}[/{status_color}] "
                f"[dim](async mode)[/dim]"
            )

            if hasattr(self, "store") and self.store:
                self.console.print("[bold]Store:[/bold] ✅ Enabled")
        else:
            # Initialize async resources
            self._async_checkpointer = None
            self._async_context_managers = {}

            # Always set up a synchronous checkpointer as fallback
            self.checkpointer = setup_checkpointer(self.config)

            # Create the async checkpointer
            try:
                self._async_checkpointer = await setup_async_checkpointer(self.config)

                # Verify it's actually an async checkpointer
                if hasattr(self._async_checkpointer, "__class__"):
                    checkpointer_name = self._async_checkpointer.__class__.__name__
                    if "Async" not in checkpointer_name:
                        logger.warning(
                            f"Expected async checkpointer but got {checkpointer_name}"
                        )
                    else:
                        logger.info(
                            f"Successfully created async checkpointer: {checkpointer_name}"
                        )

                logger.info(
                    f"Async checkpointer created successfully for {self.config.name}"
                )
            except Exception as e:
                logger.error(f"Failed to create async checkpointer: {e}")
                logger.warning("Falling back to synchronous checkpointer")

            # Add store if configured
            self.store = None
            if getattr(self.config, "add_store", False):
                from langgraph.store.base import BaseStore

                self.store = BaseStore()
                logger.debug("BaseStore added to agent")

    async def _get_async_checkpointer(self):
        """
        Get async checkpointer instance, creating it if necessary.

        Returns:
            Async checkpointer instance
        """
        # Check if we already have a live async checkpointer
        if (
            hasattr(self, "_async_checkpointer")
            and self._async_checkpointer is not None
        ):
            checkpointer_name = self._async_checkpointer.__class__.__name__
            logger.debug(f"Using existing async checkpointer: {checkpointer_name}")
            return self._async_checkpointer

        logger.info("Creating new async checkpointer...")

        try:
            # Get the persistence config
            if hasattr(self.config, "persistence"):
                persistence_config = self.config.persistence

                # Use create_async_checkpointer if available
                if hasattr(persistence_config, "create_async_checkpointer"):
                    logger.info("Creating async checkpointer from persistence config")
                    self._async_checkpointer = (
                        await persistence_config.create_async_checkpointer()
                    )

                    # Verify the checkpointer type
                    if self._async_checkpointer:
                        checkpointer_name = self._async_checkpointer.__class__.__name__
                        logger.info(f"Created async checkpointer: {checkpointer_name}")
                        if "Async" not in checkpointer_name:
                            logger.warning(
                                f"Expected async checkpointer but got {checkpointer_name}"
                            )

                    return self._async_checkpointer
        except Exception as e:
            logger.error(
                f"Error creating async checkpointer from persistence config: {e}"
            )

        # Fall back to using the setup function
        try:
            from haive.core.persistence.handlers import setup_async_checkpointer

            logger.info("Creating async checkpointer using setup_async_checkpointer")
            self._async_checkpointer = await setup_async_checkpointer(self.config)

            # Verify the checkpointer type
            if self._async_checkpointer:
                checkpointer_name = self._async_checkpointer.__class__.__name__
                logger.info(
                    f"Created async checkpointer via setup function: {checkpointer_name}"
                )
                if "Async" not in checkpointer_name:
                    logger.warning(
                        f"Expected async checkpointer but got {checkpointer_name}"
                    )

            return self._async_checkpointer
        except Exception as e:
            logger.error(f"Error setting up async checkpointer: {e}")
            raise RuntimeError(f"Failed to create async checkpointer: {e}")

    async def _cleanup_async_resources(self):
        """Clean up any active async context managers."""
        # Clean up each async context manager
        for context_id, (cm, _ctx) in list(self._async_context_managers.items()):
            try:
                # Exit the context manager
                await cm.__aexit__(None, None, None)
                logger.debug(f"Closed async context manager {context_id}")
            except Exception as e:
                logger.error(f"Error closing async context manager {context_id}: {e}")

            # Remove from active managers
            del self._async_context_managers[context_id]

        # Clear the active checkpointer
        self._async_checkpointer = None
        self._async_ctx = None
        self._async_checkpointer_cm = None

    async def _complete_async_setup(self):
        """Complete async setup that was deferred during initialization."""
        if not self._async_setup_pending:
            return  # Already completed or not needed

        try:
            # Set up the async persistence (this will create _async_checkpointer)
            await self._asetup_persistence()
            self._async_setup_pending = False

            # Verify we got an async checkpointer
            if hasattr(self, "_async_checkpointer") and self._async_checkpointer:
                checkpointer_name = self._async_checkpointer.__class__.__name__
                if "Async" in checkpointer_name:
                    logger.info(
                        f"Async setup completed successfully with {checkpointer_name}"
                    )
                else:
                    logger.warning(
                        f"Expected async checkpointer but got {checkpointer_name}"
                    )
            else:
                logger.warning(
                    "Async setup completed but no async checkpointer was created"
                )

            # Note: We keep the sync checkpointer as fallback, but async operations
            # will use the _async_checkpointer when available
        except Exception as e:
            logger.error(f"Error completing async setup: {e}")
            # Don't raise - keep the sync checkpointer as fallback
            self._async_setup_pending = False
            logger.warning(
                "Falling back to sync checkpointer due to async setup failure"
            )

    def _setup_runtime_config(self):
        """Set up default runtime configuration."""
        # Initialize runnable_config from config or create default
        if hasattr(self.config, "runnable_config") and self.config.runnable_config:
            self.runnable_config = self.config.runnable_config
        else:
            self.runnable_config = RunnableConfigManager.create(
                thread_id=str(uuid.uuid4())
            )

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            # Display the runtime configuration
            runtime_md = "## Runtime Configuration\n\n"
            runtime_md += "```json\n"
            runtime_md += json.dumps(self.runnable_config, indent=2, default=str)
            runtime_md += "\n```"

            self.console.print(Markdown(runtime_md))

        logger.debug(f"Runtime configuration set up for {self.config.name}")

    def _create_graph_builder(self):
        """Create the DynamicGraph builder with proper schemas."""
        # Get all components for DynamicGraph
        components = list(self.engines.values())

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                "[bold blue]Creating graph builder...[/bold blue]"
            ) as status:
                # Create DynamicGraph with fully resolved schemas
                status.update("[bold blue]Setting up DynamicGraph...[/bold blue]")
                self.graph_builder = DynamicGraph(
                    name=self.config.name,
                    description=getattr(
                        self.config, "description", f"Agent {self.config.name}"
                    ),
                    components=components,
                    # Pass fully resolved schemas
                    state_schema=self.state_schema,
                    input_schema=self.input_schema,
                    output_schema=self.output_schema,
                    default_runnable_config=self.runnable_config,
                    debug=self.verbose,
                )

            # Show graph info
            self.console.print(
                "[bold]Graph builder:[/bold] [green]Created successfully[/green]"
            )
        else:
            # Create DynamicGraph with fully resolved schemas
            logger.debug(f"Creating DynamicGraph for {self.config.name}")
            self.graph_builder = DynamicGraph(
                name=self.config.name,
                description=getattr(
                    self.config, "description", f"Agent {self.config.name}"
                ),
                components=components,
                # Pass fully resolved schemas
                state_schema=self.state_schema,
                input_schema=self.input_schema,
                output_schema=self.output_schema,
                default_runnable_config=self.runnable_config,
                debug=self.verbose,
            )
            logger.debug(f"DynamicGraph created for {self.config.name}")

        # Initial graph structure will be built in setup_workflow
        self._app = None

    def _process_node_configs(self):
        """Process node configurations from config."""
        node_configs = getattr(self.config, "node_configs", {})
        if not node_configs:
            return

        logger.debug(f"Processing {len(node_configs)} node configurations")

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                f"[bold blue]Processing {len(node_configs)} node configurations...[/bold blue]"
            ) as status:
                for node_name, node_config in node_configs.items():
                    status.update(
                        f"[bold blue]Adding node '{node_name}'...[/bold blue]"
                    )

                    # Create node in graph builder
                    engine = node_config.engine
                    command_goto = node_config.command_goto
                    input_mapping = node_config.input_mapping
                    output_mapping = node_config.output_mapping

                    self.graph_builder.add_node(
                        name=node_name,
                        engine=engine,
                        command_goto=command_goto,
                        input_mapping=input_mapping,
                        output_mapping=output_mapping,
                    )

            self.console.print(
                f"[green]Added {len(node_configs)} nodes from configuration[/green]"
            )
        else:
            for node_name, node_config in node_configs.items():
                logger.debug(f"Adding node '{node_name}' from configuration")

                # Create node in graph builder
                engine = node_config.engine
                command_goto = node_config.command_goto
                input_mapping = node_config.input_mapping
                output_mapping = node_config.output_mapping

                self.graph_builder.add_node(
                    name=node_name,
                    engine=engine,
                    command_goto=command_goto,
                    input_mapping=input_mapping,
                    output_mapping=output_mapping,
                )

        logger.debug("Finished processing node configurations")

    def _apply_configured_patterns(self):
        """Apply patterns configured in the agent config."""
        patterns = getattr(self.config, "patterns", [])
        if not patterns:
            return

        # Get ordered pattern list
        ordered_patterns = sorted(
            [p for p in patterns if p.enabled],
            key=lambda p: (p.order is None, p.order or 999999),
        )

        if not ordered_patterns:
            return

        logger.debug(f"Applying {len(ordered_patterns)} patterns from configuration")

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                f"[bold blue]Applying {len(ordered_patterns)} patterns...[/bold blue]"
            ) as status:
                for pattern_config in ordered_patterns:
                    pattern_name = pattern_config.name
                    status.update(
                        f"[bold blue]Applying pattern '{pattern_name}'...[/bold blue]"
                    )

                    # Get pattern parameters
                    pattern_params = pattern_config.parameters.copy()

                    # Update with global parameters
                    if hasattr(self.config, "pattern_parameters"):
                        global_params = self.config.pattern_parameters.get(
                            pattern_name, {}
                        )
                        for key, value in global_params.items():
                            if key not in pattern_params:
                                pattern_params[key] = value

                    # Apply the pattern
                    try:
                        self.apply_pattern(pattern_name, **pattern_params)
                        self.config.mark_pattern_applied(pattern_name)
                    except Exception as e:
                        self.console.print(
                            f"[bold red]Error applying pattern '{pattern_name}': {e}[/bold red]"
                        )

            self.console.print(
                f"[green]Applied {len(ordered_patterns)} patterns from configuration[/green]"
            )
        else:
            for pattern_config in ordered_patterns:
                pattern_name = pattern_config.name
                logger.debug(f"Applying pattern '{pattern_name}' from configuration")

                # Get pattern parameters
                pattern_params = pattern_config.parameters.copy()

                # Update with global parameters
                if hasattr(self.config, "pattern_parameters"):
                    global_params = self.config.pattern_parameters.get(pattern_name, {})
                    for key, value in global_params.items():
                        if key not in pattern_params:
                            pattern_params[key] = value

                # Apply the pattern
                try:
                    self.apply_pattern(pattern_name, **pattern_params)
                    self.config.mark_pattern_applied(pattern_name)
                except Exception as e:
                    logger.error(f"Error applying pattern '{pattern_name}': {e}")

        logger.debug("Finished applying patterns from configuration")

    @abstractmethod
    def setup_workflow(self) -> None:
        """
        Set up the workflow graph for this agent.

        This method must be implemented by concrete agent classes to define
        the agent's workflow structure.
        """
        pass

    @property
    def app(self) -> Any:
        """Return the compiled agent application."""
        if not hasattr(self, "_app") or self._app is None:
            self.compile()
        return self._app

    def compile(self) -> None:
        """Compile the workflow graph into an executable app."""
        logger.info(f"Compiling graph for {self.config.name}")

        if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
            with self.console.status(
                "[bold blue]Compiling workflow graph...[/bold blue]"
            ) as status:
                # Build graph if not already built
                if not hasattr(self, "graph") or self.graph is None:
                    status.update(
                        "[bold blue]Building graph from builder...[/bold blue]"
                    )
                    self.graph = self.graph_builder.build()

                # Make sure checkpointer tables are set up if needed
                if hasattr(self.checkpointer, "setup"):
                    try:
                        # Ensure connection is open
                        status.update(
                            "[bold blue]Setting up checkpointer tables...[/bold blue]"
                        )
                        ensure_pool_open(self.checkpointer)

                        # Set up tables
                        self.checkpointer.setup()
                    except Exception as e:
                        self.console.print(
                            f"[bold red]Error setting up checkpointer tables: {e}[/bold red]"
                        )

                # Compile the graph
                status.update(
                    "[bold blue]Compiling graph with checkpointer...[/bold blue]"
                )
                start_time = time.time()
                self._app = self.graph.compile(
                    checkpointer=self.checkpointer, store=self.store
                )
                compile_time = time.time() - start_time

            # Show compilation result
            self.console.print(
                f"[bold green]Graph compiled successfully[/bold green] in {compile_time:.2f} seconds"
            )

            # Get node count
            node_count = len(self.graph.nodes) if hasattr(self.graph, "nodes") else 0
            self.console.print(f"[bold]Graph nodes:[/bold] {node_count}")
        else:
            # Build graph if not already built
            if not hasattr(self, "graph") or self.graph is None:
                logger.debug("Building graph from graph_builder")
                self.graph = self.graph_builder.build()

            # Make sure checkpointer tables are set up if needed
            if hasattr(self.checkpointer, "setup"):
                try:
                    # Ensure connection is open
                    ensure_pool_open(self.checkpointer)

                    # Set up tables
                    logger.debug("Setting up checkpointer tables")
                    self.checkpointer.setup()
                    logger.debug("Checkpointer tables set up successfully")
                except Exception as e:
                    logger.error(f"Error setting up checkpointer tables: {e}")

            # Compile the graph
            logger.debug("Compiling graph with checkpointer")
            self._app = self.graph.compile(
                checkpointer=self.checkpointer, store=self.store
            )

        logger.info(f"Graph compiled successfully for {self.config.name}")

    def visualize_graph(self, output_path: Optional[str] = None) -> None:
        """
        Generate and save a visualization of the agent's graph.

        Args:
            output_path: Optional custom path for visualization output
        """
        from haive.core.config.constants import GRAPH_IMAGES_DIR

        if not output_path:
            # Use default path if none provided
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            if not os.path.exists(GRAPH_IMAGES_DIR):
                os.makedirs(GRAPH_IMAGES_DIR, exist_ok=True)
            output_path = os.path.join(
                GRAPH_IMAGES_DIR, f"{self.config.name}_{timestamp}.png"
            )

        logger.debug(f"Visualizing graph for {self.config.name}")

        try:
            # Check if we have a compiled graph
            if hasattr(self, "app") and self.app:
                # Generate the Mermaid diagram PNG with xray for detailed visualization
                png_data = self.app.get_graph(xray=True).draw_mermaid_png()

                # Ensure directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Save the PNG data
                with open(output_path, "wb") as f:
                    f.write(png_data)

                logger.info(f"Graph visualization saved to: {output_path}")

            # Fall back to graph builder visualization if available
            elif hasattr(self, "graph_builder") and hasattr(
                self.graph_builder, "visualize_graph"
            ):
                try:
                    self.graph_builder.visualize_graph(output_path)
                    logger.info(f"Graph visualization saved to: {output_path}")
                except Exception as e:
                    logger.warning(f"Error using graph builder visualization: {e}")
                    logger.warning("Graph visualization requires compilation first")
            else:
                logger.warning("Unable to visualize graph: No compiled graph available")
                logger.warning("Compile the graph first with compile() method")
        except Exception as e:
            logger.error(f"Error visualizing graph: {e}")

    def apply_pattern(self, pattern_name: str, **kwargs) -> None:
        """
        Apply a graph pattern to the agent's workflow.

        Args:
            pattern_name: Name of the pattern to apply
            **kwargs: Pattern-specific parameters
        """
        if not hasattr(self, "graph_builder") or not self.graph_builder:
            logger.error("Cannot apply pattern: Graph builder is not set up")
            raise RuntimeError("Graph builder is not set up.")

        try:
            logger.info(f"Applying pattern '{pattern_name}' to {self.config.name}")

            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                with self.console.status(
                    f"[bold blue]Applying pattern '{pattern_name}'...[/bold blue]"
                ):
                    self.graph_builder.apply_pattern(pattern_name, **kwargs)

                    # Mark graph as needing rebuild
                    self.graph = None
                    self._app = None

                self.console.print(
                    f"[bold green]Pattern '{pattern_name}' applied successfully[/bold green]"
                )
            else:
                self.graph_builder.apply_pattern(pattern_name, **kwargs)

                # Mark graph as needing rebuild
                self.graph = None
                self._app = None

                logger.info(f"Pattern '{pattern_name}' applied successfully")

            # Mark pattern as applied in config
            if hasattr(self.config, "mark_pattern_applied"):
                self.config.mark_pattern_applied(pattern_name)

        except Exception as e:
            logger.error(f"Error applying pattern '{pattern_name}': {e}")
            raise RuntimeError(f"Failed to apply pattern '{pattern_name}': {e}") from e

    def _prepare_input(self, input_data: Any) -> Any:
        """
        Prepare input for the agent based on the input schema.

        Args:
            input_data: Input in various formats

        Returns:
            Processed input compatible with the graph
        """
        # Use the input schema to prepare the input correctly
        input_schema = self.input_schema

        # Handle simple string input
        if isinstance(input_data, str):
            # If we have a schema, look for text fields to populate
            if input_schema:
                # Get schema fields
                schema_fields = {}
                if hasattr(input_schema, "model_fields"):
                    # Pydantic v2
                    schema_fields = input_schema.model_fields
                elif hasattr(input_schema, "__fields__"):
                    # Pydantic v1
                    schema_fields = input_schema.__fields__

                # Create input dictionary
                prepared_input = {}

                # Detect message field and populate if found
                if "messages" in schema_fields:
                    prepared_input["messages"] = [HumanMessage(content=input_data)]

                # Populate common text fields with input string
                for field_name in ["input", "query", "question", "text", "content"]:
                    if field_name in schema_fields:
                        prepared_input[field_name] = input_data

                # If no matches, use first field or create minimal dict
                if not prepared_input:
                    if schema_fields:
                        # Use first field
                        first_field = next(iter(schema_fields))
                        prepared_input[first_field] = input_data
                    else:
                        # Minimal fallback
                        prepared_input = {"input": input_data}

                # Create instance or return dict
                try:
                    result = input_schema(**prepared_input)
                    logger.debug(
                        f"Created input schema instance with {len(prepared_input)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(f"Error creating input schema instance: {e}")
                    return prepared_input
            else:
                # No schema - create standard input with messages
                return {"messages": [HumanMessage(content=input_data)]}

        # Handle list of strings
        elif isinstance(input_data, list) and all(
            isinstance(item, str) for item in input_data
        ):
            # If we have a schema, look for appropriate fields to populate
            if input_schema:
                # Get schema fields
                schema_fields = {}
                if hasattr(input_schema, "model_fields"):
                    # Pydantic v2
                    schema_fields = input_schema.model_fields
                elif hasattr(input_schema, "__fields__"):
                    # Pydantic v1
                    schema_fields = input_schema.__fields__

                # Create input dictionary
                prepared_input = {}

                # Create messages from strings
                if "messages" in schema_fields:
                    prepared_input["messages"] = [
                        HumanMessage(content=text) for text in input_data
                    ]

                # Join strings for other text fields
                joined_text = "\n".join(input_data)
                for field_name in ["input", "query", "question", "text", "content"]:
                    if field_name in schema_fields:
                        prepared_input[field_name] = joined_text

                # Use list directly for list fields
                for field_name, field_info in schema_fields.items():
                    field_type = str(
                        getattr(
                            field_info, "annotation", getattr(field_info, "type_", "")
                        )
                    )
                    if (
                        "list" in field_type.lower()
                        and field_name not in prepared_input
                    ):
                        prepared_input[field_name] = input_data

                # If no matches, use first field or create minimal dict
                if not prepared_input:
                    if schema_fields:
                        # Use first field
                        first_field = next(iter(schema_fields))
                        prepared_input[first_field] = input_data
                    else:
                        # Minimal fallback
                        prepared_input = {"input": input_data}

                # Create instance or return dict
                try:
                    result = input_schema(**prepared_input)
                    logger.debug(
                        f"Created input schema instance with {len(prepared_input)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(f"Error creating input schema instance: {e}")
                    return prepared_input
            else:
                # No schema - create standard input with messages
                return {"messages": [HumanMessage(content=text) for text in input_data]}

        # Handle dictionary input
        elif isinstance(input_data, dict):
            # If we have a schema, use it to validate
            if input_schema:
                # Handle messages specially if they're strings
                if "messages" in input_data and isinstance(
                    input_data["messages"], list
                ):
                    # Convert string messages to HumanMessages if needed
                    messages = input_data["messages"]
                    for i, msg in enumerate(messages):
                        if isinstance(msg, str):
                            messages[i] = HumanMessage(content=msg)

                # Create instance or return dict
                try:
                    result = input_schema(**input_data)
                    logger.debug(
                        f"Created input schema instance from dict with {len(input_data)} fields"
                    )
                    return result
                except Exception as e:
                    logger.warning(
                        f"Error creating input schema instance from dict: {e}"
                    )
                    return input_data
            else:
                # No schema - return dict as is
                return input_data

        # Handle BaseModel input
        elif isinstance(input_data, BaseModel):
            # If input is already a BaseModel, check if we need to convert
            if input_schema and not isinstance(input_data, input_schema):
                # Convert to dict first
                if hasattr(input_data, "model_dump"):
                    # Pydantic v2
                    data_dict = input_data.model_dump()
                else:
                    # Pydantic v1
                    data_dict = input_data.dict()

                # Create instance
                try:
                    result = input_schema(**data_dict)
                    logger.debug("Converted BaseModel to input schema instance")
                    return result
                except Exception as e:
                    logger.warning(f"Error converting BaseModel to input schema: {e}")
                    return input_data
            else:
                # Already correct type or no schema
                return input_data

        # Other types - convert to string and handle
        else:
            # Convert to string and handle recursively
            logger.warning(
                f"Unsupported input type {type(input_data).__name__}, converting to string"
            )
            return self._prepare_input(str(input_data))

    def _prepare_runnable_config(
        self,
        thread_id: Optional[str] = None,
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> RunnableConfig:
        """
        Prepare a runnable config with thread ID and other parameters.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
            **kwargs: Additional configuration parameters

        Returns:
            Prepared runnable configuration
        """
        # Start with the agent's base config
        base_config = getattr(self, "runnable_config", None)

        # Create new config with thread_id if provided, otherwise merge with existing
        if thread_id:
            # If thread_id is explicitly provided, use it as the primary ID
            runtime_config = RunnableConfigManager.create(
                thread_id=thread_id, user_id=kwargs.pop("user_id", None)
            )

            # Merge with base config if available
            if base_config:
                runtime_config = RunnableConfigManager.merge(
                    base_config, runtime_config
                )

            # Merge with provided config if available
            if config:
                runtime_config = RunnableConfigManager.merge(runtime_config, config)
        elif config:
            # Start with provided config and merge with base
            if base_config:
                runtime_config = RunnableConfigManager.merge(base_config, config)
            else:
                runtime_config = config
        else:
            # Use base config or create new one
            if base_config:
                runtime_config = base_config
            else:
                runtime_config = RunnableConfigManager.create()

        # Ensure configurable section exists
        if "configurable" not in runtime_config:
            runtime_config["configurable"] = {}

        # Ensure thread_id exists
        if "thread_id" not in runtime_config["configurable"]:
            runtime_config["configurable"]["thread_id"] = str(uuid.uuid4())

        # Add debug flag if specified
        if "debug" in kwargs:
            runtime_config["configurable"]["debug"] = kwargs.pop("debug")

        # Add save_history flag if specified
        if "save_history" in kwargs:
            runtime_config["configurable"]["save_history"] = kwargs.pop("save_history")

        # Add checkpoint_mode flag if needed
        runtime_config["configurable"]["checkpoint_mode"] = kwargs.pop(
            "checkpoint_mode", self._checkpoint_mode
        )

        # Add other kwargs
        for key, value in kwargs.items():
            if key.startswith("configurable_"):
                # Handle configurable_ prefix for convenience
                param_name = key.replace("configurable_", "")
                runtime_config["configurable"][param_name] = value
            elif key == "configurable" and isinstance(value, dict):
                # Merge configurable dict
                for k, v in value.items():
                    runtime_config["configurable"][k] = v
            elif key == "engine_configs" and isinstance(value, dict):
                # Setup engine_configs section if not present
                if "engine_configs" not in runtime_config["configurable"]:
                    runtime_config["configurable"]["engine_configs"] = {}

                # Merge engine configs
                for engine_id, engine_params in value.items():
                    if (
                        engine_id
                        not in runtime_config["configurable"]["engine_configs"]
                    ):
                        runtime_config["configurable"]["engine_configs"][engine_id] = {}
                    runtime_config["configurable"]["engine_configs"][engine_id].update(
                        engine_params
                    )
            else:
                # Add to top level
                runtime_config[key] = value

        if (
            self.rich_logging
            and RICH_AVAILABLE
            and self.verbose
            and hasattr(self, "debug_console")
        ):
            # Log the runtime config in debug mode
            self.debug_console.print("[bold]Runtime Config:[/bold]")
            config_json = json.dumps(runtime_config, indent=2, default=str)
            self.debug_console.print(
                Syntax(config_json, "json", theme="monokai", line_numbers=True)
            )

        return runtime_config

    def _process_output(self, output_data: Any) -> Any:
        """
        Process and validate output data.

        Args:
            output_data: Raw output data from the graph

        Returns:
            Processed output data
        """
        # Use the output schema to validate if available
        if (
            hasattr(self, "output_schema")
            and self.output_schema
            and not isinstance(output_data, self.output_schema)
        ):
            # Try to instantiate with schema
            try:
                # Convert dict-like objects to proper form
                if isinstance(output_data, dict):
                    data_dict = output_data
                elif hasattr(output_data, "model_dump"):
                    # Pydantic v2
                    data_dict = output_data.model_dump()
                elif hasattr(output_data, "dict"):
                    # Pydantic v1
                    data_dict = output_data.dict()
                else:
                    # Fallback - create from dict members
                    data_dict = {}
                    for key, value in output_data.__dict__.items():
                        if not key.startswith("_"):
                            data_dict[key] = value

                # Create instance
                result = self.output_schema(**data_dict)
                logger.debug("Validated output with schema")
                return result
            except Exception as e:
                logger.warning(f"Error validating output with schema: {e}")
                return output_data

        # No schema or already correct type
        return output_data

    def run(
        self,
        input_data: TIn,
        thread_id: Optional[str] = None,
        debug: bool = None,
        config: Optional[RunnableConfig] = None,
        **kwargs,
    ) -> TOut:
        """
        Synchronously run the agent with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            debug: Whether to enable debug mode
            config: Optional runtime configuration
            **kwargs: Additional runtime configuration

        Returns:
            Output from the agent
        """
        # Default debug to verbose if not specified
        if debug is None:
            debug = self.verbose

        # Prepare input data in correct format
        processed_input = self._prepare_input(input_data)

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, debug=debug, **kwargs
        )

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # Set up tracing for rich UI if available
        if self.rich_logging and RICH_AVAILABLE and debug and hasattr(self, "console"):
            self.console.print(
                Panel.fit(
                    f"[bold blue]Running Agent: [green]{self.config.name}[/green][/bold blue]\n"
                    f"[cyan]Thread ID:[/cyan] {thread_id}",
                    border_style="blue",
                    title="Execution Started",
                    subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

            # Show processed input
            self.console.print("[bold cyan]Processed Input:[/bold cyan]")
            if isinstance(processed_input, dict):
                input_json = json.dumps(processed_input, indent=2, default=str)
                self.console.print(Syntax(input_json, "json", theme="monokai"))
            elif isinstance(processed_input, BaseModel):
                if hasattr(processed_input, "model_dump"):
                    input_json = json.dumps(
                        processed_input.model_dump(), indent=2, default=str
                    )
                else:
                    input_json = json.dumps(
                        processed_input.dict(), indent=2, default=str
                    )
                self.console.print(Syntax(input_json, "json", theme="monokai"))
            else:
                self.console.print(str(processed_input))

        # Set up checkpointer if using persistence
        start_time = time.time()

        # Register thread if needed
        if self.checkpointer and thread_id:
            register_thread_if_needed(self.checkpointer, thread_id)

        # Get previous state if available
        previous_state = None
        try:
            if self.checkpointer and thread_id:
                # Get last state for this thread
                previous_state = self.app.get_state(runtime_config)

                if previous_state and debug:
                    logger.debug(f"Retrieved previous state for thread {thread_id}")
                    if (
                        self.rich_logging
                        and RICH_AVAILABLE
                        and hasattr(self, "console")
                    ):
                        self.console.print(
                            "[bold cyan]Previous State Found.[/bold cyan]"
                        )
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input with previous state if available
        if previous_state:
            try:
                full_input = prepare_merged_input(
                    processed_input,
                    previous_state,
                    runtime_config,
                    self.input_schema,
                    self.state_schema,
                )
                logger.debug("Merged input with previous state")

                # Update processed input for running
                processed_input = full_input
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Run the agent
        try:
            logger.debug(processed_input)
            logger.debug(runtime_config)
            logger.debug(input_data)
            print("--------------------------------")
            print(processed_input)
            print(runtime_config)
            print(input_data)
            print("--------------------------------")
            logger.debug(f"Attempting to invoke app with input data: {processed_input}")
            processed_input = (
                processed_input.model_dump()
                if hasattr(processed_input, "model_dump")
                else processed_input
            )
            result = self.app.invoke(processed_input, runtime_config, debug=debug)
            logger.debug("Agent execution completed successfully")
            print(result)
            # Process the result if needed
            output = self._process_output(result)

            # Save state history if configured
            if runtime_config["configurable"].get(
                "save_history", getattr(self.config, "save_history", True)
            ):
                self.save_state_history(runtime_config)

            # Show debug info if enabled
            if (
                self.rich_logging
                and RICH_AVAILABLE
                and debug
                and hasattr(self, "console")
            ):
                execution_time = time.time() - start_time

                # Show output
                self.console.print("[bold cyan]Output:[/bold cyan]")
                if isinstance(output, dict):
                    output_json = json.dumps(output, indent=2, default=str)
                    self.console.print(Syntax(output_json, "json", theme="monokai"))
                elif isinstance(output, BaseModel):
                    if hasattr(output, "model_dump"):
                        output_json = json.dumps(
                            output.model_dump(), indent=2, default=str
                        )
                    else:
                        output_json = json.dumps(output.dict(), indent=2, default=str)
                    self.console.print(Syntax(output_json, "json", theme="monokai"))
                else:
                    self.console.print(str(output))

                # Show completion message
                self.console.print(
                    Panel.fit(
                        f"[bold green]Execution Completed[/bold green]\n"
                        f"[cyan]Execution Time:[/cyan] {execution_time:.2f} seconds",
                        border_style="green",
                        title="Agent Execution",
                        subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

            return output

        except Exception as e:
            logger.error(f"Error during agent execution: {e}")

            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    Panel.fit(
                        f"[bold red]Execution Error:[/bold red] {str(e)}",
                        border_style="red",
                        title="Agent Execution Failed",
                    )
                )

            raise

    async def arun(
        self,
        input_data: TIn,
        thread_id: Optional[str] = None,
        config: Optional[RunnableConfig] = None,
        debug: bool = None,
        **kwargs,
    ) -> TOut:
        """
        Asynchronously run the agent with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Returns:
            Output from the agent
        """
        # Complete async setup if pending
        if self._async_setup_pending:
            await self._complete_async_setup()

        # Default debug to verbose if not specified
        if debug is None:
            debug = self.verbose

        # Prepare input data in correct format
        processed_input = self._prepare_input(input_data)

        # Check if async checkpoint_mode is requested
        checkpoint_mode = kwargs.get("checkpoint_mode", self._checkpoint_mode)
        is_async_mode = checkpoint_mode == "async"

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id,
            config=config,
            debug=debug,
            checkpoint_mode=checkpoint_mode,
            **kwargs,
        )

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # Set up tracing for rich UI if available
        if self.rich_logging and RICH_AVAILABLE and debug and hasattr(self, "console"):
            self.console.print(
                Panel.fit(
                    f"[bold blue]Running Agent Async: [green]{self.config.name}[/green][/bold blue]\n"
                    f"[cyan]Thread ID:[/cyan] {thread_id}\n"
                    f"[cyan]Checkpoint Mode:[/cyan] {checkpoint_mode}",
                    border_style="blue",
                    title="Async Execution Started",
                    subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

        # Set up checkpointer if using persistence
        start_time = time.time()

        try:
            # Use appropriate persistence setup based on mode
            if is_async_mode:
                # Set up async persistence if not already done
                if (
                    not hasattr(self, "_async_checkpointer")
                    or self._async_checkpointer is None
                ):
                    await self._asetup_persistence()

                # Register thread if needed for async checkpointer
                if self._async_checkpointer and thread_id:
                    await register_async_thread_if_needed(
                        self._async_checkpointer, thread_id
                    )

                # Get previous state if available using async checkpointer
                previous_state = None
                try:
                    # Log the checkpointer being used
                    if self._async_checkpointer:
                        checkpointer_name = self._async_checkpointer.__class__.__name__
                        logger.info(
                            f"Using async checkpointer for graph compilation: {checkpointer_name}"
                        )
                        if "Async" not in checkpointer_name:
                            logger.error(
                                f"ERROR: Expected async checkpointer but got {checkpointer_name}"
                            )
                    else:
                        logger.error("ERROR: No async checkpointer available!")

                    # Create async app with the async checkpointer
                    async_app = self.graph.compile(
                        checkpointer=self._async_checkpointer, store=self.store
                    )

                    # Verify the compiled app's checkpointer
                    if hasattr(async_app, "checkpointer") and async_app.checkpointer:
                        app_checkpointer_name = (
                            async_app.checkpointer.__class__.__name__
                        )
                        logger.info(
                            f"Compiled app using checkpointer: {app_checkpointer_name}"
                        )
                        if "Async" not in app_checkpointer_name:
                            logger.error(
                                f"ERROR: App compiled with sync checkpointer: {app_checkpointer_name}"
                            )

                    previous_state = await async_app.get_state(runtime_config)

                    if previous_state and debug:
                        logger.debug(f"Retrieved previous state for thread {thread_id}")
                except Exception as e:
                    logger.warning(f"Error retrieving previous state: {e}")

                # Prepare merged input with previous state if available
                if previous_state:
                    try:
                        full_input = prepare_merged_input(
                            processed_input,
                            previous_state,
                            runtime_config,
                            self.input_schema,
                            self.state_schema,
                        )
                        logger.debug("Merged input with previous state")

                        # Update processed input for running
                        processed_input = full_input
                    except Exception as e:
                        logger.warning(f"Error merging with previous state: {e}")

                # Use ainvoke with async app
                try:
                    # Log execution details
                    logger.info(
                        f"Executing async app with checkpointer: {async_app.checkpointer.__class__.__name__ if hasattr(async_app, 'checkpointer') and async_app.checkpointer else 'None'}"
                    )

                    # Run with async app and async checkpointer
                    result = await async_app.ainvoke(
                        processed_input, runtime_config, debug=debug
                    )
                    logger.debug("Agent async execution completed successfully")

                    # Process the result
                    output = self._process_output(result)

                    # Save state history if configured
                    if runtime_config["configurable"].get(
                        "save_history", getattr(self.config, "save_history", True)
                    ):
                        await self.save_state_history_async(runtime_config)

                    return output
                except Exception as e:
                    # Log error and re-raise
                    logger.error(
                        f"Error in async invocation using async checkpointer: {e}"
                    )
                    raise
            else:
                # Standard sync mode with async function wrapper

                # Register thread if needed
                if self.checkpointer and thread_id:
                    register_thread_if_needed(self.checkpointer, thread_id)

                # Get previous state if available
                previous_state = None
                try:
                    if self.checkpointer and thread_id:
                        # Get last state for this thread
                        previous_state = self.app.get_state(runtime_config)

                        if previous_state and debug:
                            logger.debug(
                                f"Retrieved previous state for thread {thread_id}"
                            )
                except Exception as e:
                    logger.warning(f"Error retrieving previous state: {e}")

                # Prepare merged input with previous state if available
                if previous_state:
                    try:
                        full_input = prepare_merged_input(
                            processed_input,
                            previous_state,
                            runtime_config,
                            self.input_schema,
                            self.state_schema,
                        )
                        logger.debug("Merged input with previous state")

                        # Update processed input for running
                        processed_input = full_input
                    except Exception as e:
                        logger.warning(f"Error merging with previous state: {e}")

                # Use ainvoke if available
                if hasattr(self.app, "ainvoke"):
                    result = await self.app.ainvoke(processed_input, runtime_config)
                else:
                    # Fall back to threaded execution
                    loop = asyncio.get_event_loop()
                    result = await loop.run_in_executor(
                        None, lambda: self.app.invoke(processed_input, runtime_config)
                    )

                logger.debug("Agent async execution completed successfully")

                # Process the result if needed
                output = self._process_output(result)

                # Save state history if configured
                if runtime_config["configurable"].get(
                    "save_history", getattr(self.config, "save_history", True)
                ):
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, lambda: self.save_state_history(runtime_config)
                    )

                # Return the result
                return output

        except Exception as e:
            logger.error(f"Error during async agent execution: {e}")

            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    Panel.fit(
                        f"[bold red]Async Execution Error:[/bold red] {str(e)}",
                        border_style="red",
                        title="Agent Execution Failed",
                    )
                )

            raise
        finally:
            # Show debug info if enabled
            if (
                self.rich_logging
                and RICH_AVAILABLE
                and debug
                and hasattr(self, "console")
            ):
                execution_time = time.time() - start_time

                # Show completion message
                self.console.print(
                    Panel.fit(
                        f"[bold green]Async Execution Completed[/bold green]\n"
                        f"[cyan]Execution Time:[/cyan] {execution_time:.2f} seconds\n"
                        f"[cyan]Checkpoint Mode:[/cyan] {checkpoint_mode}",
                        border_style="green",
                        title="Agent Async Execution",
                        subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

            # Clean up async resources if we created them
            if (
                is_async_mode
                and hasattr(self, "_async_checkpointer")
                and self._async_checkpointer is not None
            ):
                try:
                    await self._cleanup_async_resources()
                except Exception as e:
                    logger.error(f"Error cleaning up async resources: {e}")

    def stream(
        self,
        input_data: TIn,
        thread_id: Optional[str] = None,
        stream_mode: str = "values",
        config: Optional[RunnableConfig] = None,
        debug: bool = None,
        **kwargs,
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Yields:
            State updates during execution
        """
        # Default debug to verbose if not specified
        if debug is None:
            debug = self.verbose

        # Prepare input data in correct format
        processed_input = self._prepare_input(input_data)

        # Add stream_mode to runtime config
        kwargs["stream_mode"] = stream_mode

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config, debug=debug, **kwargs
        )
        if self.config.runnable_config is not None:
            recursion_limit = self.config.runnable_config["configurable"].get(
                "recursion_limit", 25
            )
            kwargs["recursion_limit"] = recursion_limit

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # Set up tracing for rich UI if available
        if self.rich_logging and RICH_AVAILABLE and debug and hasattr(self, "console"):
            self.console.print(
                Panel.fit(
                    f"[bold blue]Streaming Agent: [green]{self.config.name}[/green][/bold blue]\n"
                    f"[cyan]Thread ID:[/cyan] {thread_id}\n"
                    f"[cyan]Stream Mode:[/cyan] {stream_mode}",
                    border_style="blue",
                    title="Streaming Started",
                    subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

        # Set up checkpointer if using persistence
        start_time = time.time()

        # Register thread if needed
        if self.checkpointer and thread_id:
            register_thread_if_needed(self.checkpointer, thread_id)

        # Get previous state if available
        previous_state = None
        try:
            if self.checkpointer and thread_id:
                # Get last state for this thread
                previous_state = self.app.get_state(runtime_config)

                if previous_state and debug:
                    logger.debug(f"Retrieved previous state for thread {thread_id}")
        except Exception as e:
            logger.warning(f"Error retrieving previous state: {e}")

        # Prepare merged input with previous state if available
        if previous_state:
            try:
                full_input = prepare_merged_input(
                    processed_input,
                    previous_state,
                    runtime_config,
                    self.input_schema,
                    self.state_schema,
                )
                logger.debug("Merged input with previous state")

                # Update processed input for running
                processed_input = full_input
            except Exception as e:
                logger.warning(f"Error merging with previous state: {e}")

        # Stream execution
        try:
            # Create generator to stream results
            stream_gen = self.app.stream(processed_input, runtime_config)

            # Track the final result for state saving
            final_result = None

            # Process stream chunks
            chunk_count = 0
            for chunk in stream_gen:
                chunk_count += 1

                # Save the final chunk for state saving
                final_result = chunk

                # Process the chunk if needed
                processed_chunk = self._process_stream_chunk(chunk, stream_mode)

                # Debug if enabled
                if (
                    self.rich_logging
                    and RICH_AVAILABLE
                    and debug
                    and hasattr(self, "debug_console")
                ):
                    # Only log every few chunks to avoid overwhelming output
                    if chunk_count % 5 == 0 or chunk_count < 3:
                        chunk_type = type(chunk).__name__
                        self.debug_console.print(
                            f"[dim]Stream chunk {chunk_count} ({chunk_type})[/dim]"
                        )

                # Yield the processed chunk
                yield processed_chunk

            # Save state history if configured and we have a final result
            if (
                runtime_config["configurable"].get(
                    "save_history", getattr(self.config, "save_history", True)
                )
                and final_result is not None
            ):
                self.save_state_history(runtime_config)

            # Show debug info if enabled
            if (
                self.rich_logging
                and RICH_AVAILABLE
                and debug
                and hasattr(self, "console")
            ):
                execution_time = time.time() - start_time

                # Show completion message
                self.console.print(
                    Panel.fit(
                        f"[bold green]Streaming Completed[/bold green]\n"
                        f"[cyan]Execution Time:[/cyan] {execution_time:.2f} seconds\n"
                        f"[cyan]Total Chunks:[/cyan] {chunk_count}",
                        border_style="green",
                        title="Agent Streaming",
                        subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

        except Exception as e:
            logger.error(f"Error during streaming execution: {e}")

            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    Panel.fit(
                        f"[bold red]Streaming Error:[/bold red] {str(e)}",
                        border_style="red",
                        title="Agent Streaming Failed",
                    )
                )

            raise

    def _process_stream_chunk(self, chunk: Any, stream_mode: str) -> Dict[str, Any]:
        """
        Process a stream chunk based on stream mode.

        Args:
            chunk: The raw stream chunk
            stream_mode: Stream mode (values, updates, debug, etc.)

        Returns:
            Processed stream chunk
        """
        # Process based on stream mode
        if stream_mode == "custom":
            # Return custom chunks as-is
            return chunk
        elif stream_mode == "values":
            # Return the entire state values
            if isinstance(chunk, dict) and "values" in chunk:
                return chunk["values"]
            return chunk
        elif stream_mode == "updates":
            # Return just the updates
            if isinstance(chunk, dict) and "updates" in chunk:
                return chunk["updates"]
            elif isinstance(chunk, dict) and "node" in chunk:
                return chunk
            return chunk
        elif stream_mode == "messages":
            # Extract and return just the messages for token streaming
            if isinstance(chunk, dict):
                if "values" in chunk and "messages" in chunk["values"]:
                    return {"messages": chunk["values"]["messages"]}
                elif "updates" in chunk and "messages" in chunk["updates"]:
                    return {"messages": chunk["updates"]["messages"]}
                elif "messages" in chunk:
                    return {"messages": chunk["messages"]}

            # Default fallback
            return chunk
        else:
            # Debug mode or unknown - return everything
            return chunk

    async def astream(
        self,
        input_data: TIn,
        thread_id: Optional[str] = None,
        stream_mode: str = "values",
        config: Optional[RunnableConfig] = None,
        debug: bool = None,
        **kwargs,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Asynchronously stream agent execution with input data.

        Args:
            input_data: Input data for the agent
            thread_id: Optional thread ID for persistence
            stream_mode: Stream mode (values, updates, debug, etc.)
            config: Optional runtime configuration
            debug: Whether to enable debug mode
            **kwargs: Additional runtime configuration

        Yields:
            Async iterator of state updates during execution
        """
        # Complete async setup if pending
        if self._async_setup_pending:
            await self._complete_async_setup()

        # Default debug to verbose if not specified
        if debug is None:
            debug = self.verbose

        # Prepare input data in correct format
        processed_input = self._prepare_input(input_data)

        # Add stream_mode to runtime config
        kwargs["stream_mode"] = stream_mode

        # Check if async checkpoint_mode is requested
        checkpoint_mode = kwargs.get("checkpoint_mode", self._checkpoint_mode)
        is_async_mode = checkpoint_mode == "async"

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id,
            config=config,
            debug=debug,
            checkpoint_mode=checkpoint_mode,
            **kwargs,
        )

        # Extract thread_id for persistence
        thread_id = runtime_config["configurable"].get("thread_id")

        # Set up tracing for rich UI if available
        if self.rich_logging and RICH_AVAILABLE and debug and hasattr(self, "console"):
            self.console.print(
                Panel.fit(
                    f"[bold blue]Async Streaming Agent: [green]{self.config.name}[/green][/bold blue]\n"
                    f"[cyan]Thread ID:[/cyan] {thread_id}\n"
                    f"[cyan]Stream Mode:[/cyan] {stream_mode}\n"
                    f"[cyan]Checkpoint Mode:[/cyan] {checkpoint_mode}",
                    border_style="blue",
                    title="Async Streaming Started",
                    subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
            )

        # Set up checkpointer if using persistence
        start_time = time.time()

        try:
            # Use appropriate approach based on checkpoint mode
            if is_async_mode:
                # Get or create async checkpointer
                async_checkpointer = await self._get_async_checkpointer()

                # Register thread if needed
                await register_async_thread_if_needed(async_checkpointer, thread_id)

                # Get previous state if available
                previous_state = None
                try:
                    # Use app with async checkpointer
                    # We need to recompile with the async checkpointer
                    async_app = self.graph.compile(
                        checkpointer=async_checkpointer, store=self.store
                    )
                    previous_state = async_app.get_state(runtime_config)

                    if previous_state and debug:
                        logger.debug(f"Retrieved previous state for thread {thread_id}")
                except Exception as e:
                    logger.warning(f"Error retrieving previous state: {e}")

                # Prepare merged input with previous state if available
                if previous_state:
                    try:
                        full_input = prepare_merged_input(
                            processed_input,
                            previous_state,
                            runtime_config,
                            self.input_schema,
                            self.state_schema,
                        )
                        logger.debug("Merged input with previous state")

                        # Update processed input for running
                        processed_input = full_input
                    except Exception as e:
                        logger.warning(f"Error merging with previous state: {e}")

                # Use astream if available
                if hasattr(async_app, "astream"):
                    stream_gen = async_app.astream(processed_input, runtime_config)
                else:
                    # Fall back to sync streaming via async wrapper
                    sync_gen = async_app.stream(processed_input, runtime_config)

                    # Convert sync generator to async generator
                    async def async_wrapper():
                        for chunk in sync_gen:
                            yield chunk

                    stream_gen = async_wrapper()

                # Track the final result for state saving
                final_result = None

                # Process stream chunks
                chunk_count = 0
                async for chunk in stream_gen:
                    chunk_count += 1

                    # Save the final chunk for state saving
                    final_result = chunk

                    # Process the chunk if needed
                    processed_chunk = self._process_stream_chunk(chunk, stream_mode)

                    # Debug if enabled
                    if (
                        self.rich_logging
                        and RICH_AVAILABLE
                        and debug
                        and hasattr(self, "debug_console")
                    ):
                        # Only log every few chunks to avoid overwhelming output
                        if chunk_count % 5 == 0 or chunk_count < 3:
                            chunk_type = type(chunk).__name__
                            self.debug_console.print(
                                f"[dim]Async stream chunk {chunk_count} ({chunk_type})[/dim]"
                            )

                    # Yield the processed chunk
                    yield processed_chunk

                # Save state history if configured and we have a final result
                if (
                    runtime_config["configurable"].get(
                        "save_history", getattr(self.config, "save_history", True)
                    )
                    and final_result is not None
                ):
                    # Run in executor to avoid blocking
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, lambda: self.save_state_history(runtime_config)
                    )
            else:
                # Standard sync mode with async wrapper

                # Register thread if needed
                if self.checkpointer and thread_id:
                    register_thread_if_needed(self.checkpointer, thread_id)

                # Get previous state if available
                previous_state = None
                try:
                    if self.checkpointer and thread_id:
                        # Get last state for this thread
                        previous_state = self.app.get_state(runtime_config)

                        if previous_state and debug:
                            logger.debug(
                                f"Retrieved previous state for thread {thread_id}"
                            )
                except Exception as e:
                    logger.warning(f"Error retrieving previous state: {e}")

                # Prepare merged input with previous state if available
                if previous_state:
                    try:
                        full_input = prepare_merged_input(
                            processed_input,
                            previous_state,
                            runtime_config,
                            self.input_schema,
                            self.state_schema,
                        )
                        logger.debug("Merged input with previous state")

                        # Update processed input for running
                        processed_input = full_input
                    except Exception as e:
                        logger.warning(f"Error merging with previous state: {e}")

                # Create async generator to stream results
                if hasattr(self.app, "astream"):
                    stream_gen = self.app.astream(processed_input, runtime_config)
                else:
                    # Fall back to sync streaming via async wrapper
                    sync_gen = self.app.stream(processed_input, runtime_config)

                    # Convert sync generator to async generator
                    async def async_wrapper():
                        for chunk in sync_gen:
                            yield chunk

                    stream_gen = async_wrapper()

                # Track the final result for state saving
                final_result = None

                # Process stream chunks
                chunk_count = 0
                async for chunk in stream_gen:
                    chunk_count += 1

                    # Save the final chunk for state saving
                    final_result = chunk

                    # Process the chunk if needed
                    processed_chunk = self._process_stream_chunk(chunk, stream_mode)

                    # Debug if enabled
                    if (
                        self.rich_logging
                        and RICH_AVAILABLE
                        and debug
                        and hasattr(self, "debug_console")
                    ):
                        # Only log every few chunks to avoid overwhelming output
                        if chunk_count % 5 == 0 or chunk_count < 3:
                            chunk_type = type(chunk).__name__
                            self.debug_console.print(
                                f"[dim]Async stream chunk {chunk_count} ({chunk_type})[/dim]"
                            )

                    # Yield the processed chunk
                    yield processed_chunk

                # Save state history if configured and we have a final result
                if (
                    runtime_config["configurable"].get(
                        "save_history", getattr(self.config, "save_history", True)
                    )
                    and final_result is not None
                ):
                    # Run in executor to avoid blocking
                    loop = asyncio.get_event_loop()
                    await loop.run_in_executor(
                        None, lambda: self.save_state_history(runtime_config)
                    )

        except Exception as e:
            logger.error(f"Error during async streaming execution: {e}")

            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    Panel.fit(
                        f"[bold red]Async Streaming Error:[/bold red] {str(e)}",
                        border_style="red",
                        title="Agent Async Streaming Failed",
                    )
                )

            raise

        finally:
            # Show debug info if enabled
            if (
                self.rich_logging
                and RICH_AVAILABLE
                and debug
                and hasattr(self, "console")
            ):
                execution_time = time.time() - start_time

                # Show completion message
                self.console.print(
                    Panel.fit(
                        f"[bold green]Async Streaming Completed[/bold green]\n"
                        f"[cyan]Execution Time:[/cyan] {execution_time:.2f} seconds\n"
                        f"[cyan]Checkpoint Mode:[/cyan] {checkpoint_mode}",
                        border_style="green",
                        title="Agent Async Streaming",
                        subtitle=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    )
                )

    def save_state_history(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> bool:
        """
        Save the current agent state to a JSON file.

        Args:
            runnable_config: Optional runnable configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.app:
            logger.error("Cannot save state history: Workflow graph not compiled")
            return False

        # Use provided runnable config or default
        runnable_config = runnable_config or self.runnable_config

        try:
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                with self.console.status(
                    "[bold blue]Saving state history...[/bold blue]"
                ):
                    # Get state from app
                    state_json = self.app.get_state(runnable_config)

                    if not state_json:
                        self.console.print(
                            "[bold yellow]No state history available[/bold yellow]"
                        )
                        return False

                    # Ensure state is JSON serializable
                    state_json = ensure_json_serializable(state_json)

                    # Save to file
                    with open(self.state_filename, "w", encoding="utf-8") as f:
                        json.dump(state_json, f, indent=4)

                self.console.print(
                    f"[bold green]State history saved to:[/bold green] {self.state_filename}"
                )
            else:
                # Get state from app
                state_json = self.app.get_state(runnable_config)

                if not state_json:
                    logger.warning(f"No state history available for {self.config.name}")
                    return False

                # Ensure state is JSON serializable
                state_json = ensure_json_serializable(state_json)

                # Save to file
                with open(self.state_filename, "w", encoding="utf-8") as f:
                    json.dump(state_json, f, indent=4)

                logger.info(f"State history saved to: {self.state_filename}")

            return True
        except Exception as e:
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    f"[bold red]Error saving state history: {e}[/bold red]"
                )
            else:
                logger.error(f"Error saving state history: {e}")
            return False

    async def save_state_history_async(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> bool:
        """
        Asynchronously save the current agent state to a JSON file.

        Args:
            runnable_config: Optional runnable configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.app:
            logger.error("Cannot save state history: Workflow graph not compiled")
            return False

        # Use provided runnable config or default
        runnable_config = runnable_config or self.runnable_config

        try:
            # Run the synchronous save operation in a thread to make it async
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, lambda: self.save_state_history(runnable_config)
            )

            return result
        except Exception as e:
            logger.error(f"Error saving state history asynchronously: {e}")
            return False

    def inspect_state(
        self, thread_id: Optional[str] = None, config: Optional[RunnableConfig] = None
    ) -> None:
        """
        Inspect the current state of the agent.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
        """
        if not self.app:
            logger.error("Cannot inspect state: Workflow graph not compiled")
            return

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config
        )

        try:
            # Get current state
            state = self.app.get_state(runtime_config)

            if not state:
                logger.warning("No state available")
                if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                    self.console.print("[bold yellow]No state available[/bold yellow]")
                return

            # Extract thread ID from config
            thread_id = runtime_config["configurable"].get("thread_id", "unknown")

            # Log the state
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(
                    Panel.fit(
                        f"[bold]State Inspection for Thread: [cyan]{thread_id}[/cyan][/bold]",
                        border_style="blue",
                    )
                )

                # Handle different state formats
                if hasattr(state, "values"):
                    # StateSnapshot format
                    values = state.values
                    metadata = getattr(state, "metadata", {})
                    created_at = getattr(state, "created_at", "unknown")

                    # Print values
                    self.console.print("[bold]State Values:[/bold]")
                    value_json = json.dumps(ensure_json_serializable(values), indent=2)
                    self.console.print(Syntax(value_json, "json", theme="monokai"))

                    # Print metadata if available
                    if metadata:
                        self.console.print("\n[bold]Metadata:[/bold]")
                        metadata_json = json.dumps(
                            ensure_json_serializable(metadata), indent=2
                        )
                        self.console.print(
                            Syntax(metadata_json, "json", theme="monokai")
                        )

                    # Print creation time
                    self.console.print(f"\n[bold]Created At:[/bold] {created_at}")

                elif isinstance(state, dict):
                    # Dictionary format
                    self.console.print("[bold]State Dictionary:[/bold]")
                    state_json = json.dumps(ensure_json_serializable(state), indent=2)
                    self.console.print(Syntax(state_json, "json", theme="monokai"))

                else:
                    # Unknown format
                    self.console.print(
                        f"[bold]State (Type: {type(state).__name__}):[/bold]"
                    )
                    self.console.print(str(state))
            else:
                # Standard logging
                logger.info(f"State inspection for thread {thread_id}")

                # Handle different state formats
                if hasattr(state, "values"):
                    # StateSnapshot format
                    values = state.values
                    metadata = getattr(state, "metadata", {})
                    created_at = getattr(state, "created_at", "unknown")

                    logger.info(f"State values: {values}")
                    if metadata:
                        logger.info(f"Metadata: {metadata}")
                    logger.info(f"Created at: {created_at}")

                elif isinstance(state, dict):
                    # Dictionary format
                    logger.info(f"State dictionary: {state}")

                else:
                    # Unknown format
                    logger.info(f"State (Type: {type(state).__name__}): {state}")

        except Exception as e:
            logger.error(f"Error inspecting state: {e}")
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(f"[bold red]Error inspecting state: {e}[/bold red]")

    async def inspect_state_async(
        self, thread_id: Optional[str] = None, config: Optional[RunnableConfig] = None
    ) -> None:
        """
        Asynchronously inspect the current state of the agent.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration
        """
        if not self.app:
            logger.error("Cannot inspect state: Workflow graph not compiled")
            return

        try:
            # Run in a thread pool to make it async
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None, lambda: self.inspect_state(thread_id, config)
            )
        except Exception as e:
            logger.error(f"Error in async state inspection: {e}")

    def reset_state(
        self, thread_id: Optional[str] = None, config: Optional[RunnableConfig] = None
    ) -> bool:
        """
        Reset the agent's state for a thread.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration

        Returns:
            True if successful, False otherwise
        """
        if not self.checkpointer:
            logger.warning("Cannot reset state: No checkpointer configured")
            return False

        # Prepare runtime configuration
        runtime_config = self._prepare_runnable_config(
            thread_id=thread_id, config=config
        )

        # Extract thread ID from config
        thread_id = runtime_config["configurable"].get("thread_id", None)
        if not thread_id:
            logger.warning("Cannot reset state: No thread ID provided")
            return False

        try:
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                with self.console.status(
                    f"[bold blue]Resetting state for thread {thread_id}...[/bold blue]"
                ):
                    # Connect to checkpointer
                    ensure_pool_open(self.checkpointer)

                    # Reset state based on checkpointer type
                    if hasattr(self.checkpointer, "delete"):
                        # Use delete method if available
                        self.checkpointer.delete(thread_id)
                    elif hasattr(self.checkpointer, "conn") and self.checkpointer.conn:
                        # Try database approach
                        conn = self.checkpointer.conn
                        with conn.connection() as db_conn:
                            with db_conn.cursor() as cursor:
                                # Delete all records for this thread ID
                                cursor.execute(
                                    "DELETE FROM checkpoints WHERE thread_id = %s",
                                    (thread_id,),
                                )

                self.console.print(
                    f"[bold green]State reset successfully for thread {thread_id}[/bold green]"
                )
            else:
                # Connect to checkpointer
                ensure_pool_open(self.checkpointer)

                # Reset state based on checkpointer type
                if hasattr(self.checkpointer, "delete"):
                    # Use delete method if available
                    self.checkpointer.delete(thread_id)
                elif hasattr(self.checkpointer, "conn") and self.checkpointer.conn:
                    # Try database approach
                    conn = self.checkpointer.conn
                    with conn.connection() as db_conn:
                        with db_conn.cursor() as cursor:
                            # Delete all records for this thread ID
                            cursor.execute(
                                "DELETE FROM checkpoints WHERE thread_id = %s",
                                (thread_id,),
                            )

                logger.info(f"State reset successfully for thread {thread_id}")

            return True
        except Exception as e:
            logger.error(f"Error resetting state: {e}")
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(f"[bold red]Error resetting state: {e}[/bold red]")
            return False

    async def reset_state_async(
        self, thread_id: Optional[str] = None, config: Optional[RunnableConfig] = None
    ) -> bool:
        """
        Asynchronously reset the agent's state for a thread.

        Args:
            thread_id: Optional thread ID for persistence
            config: Optional runtime configuration

        Returns:
            True if successful, False otherwise
        """
        # Check for async mode
        checkpoint_mode = getattr(self, "_checkpoint_mode", "sync")
        is_async_mode = checkpoint_mode == "async"

        if (
            is_async_mode
            and hasattr(self, "_async_checkpointer")
            and self._async_checkpointer
        ):
            # Use async checkpointer directly

            # Prepare runtime configuration
            runtime_config = self._prepare_runnable_config(
                thread_id=thread_id, config=config
            )

            # Extract thread ID from config
            thread_id = runtime_config["configurable"].get("thread_id", None)
            if not thread_id:
                logger.warning("Cannot reset state: No thread ID provided")
                return False

            try:
                # Connect to checkpointer
                await ensure_async_pool_open(self._async_checkpointer)

                # Reset state based on checkpointer type
                if hasattr(self._async_checkpointer, "delete"):
                    # Use delete method if available
                    await self._async_checkpointer.delete(thread_id)
                elif (
                    hasattr(self._async_checkpointer, "conn")
                    and self._async_checkpointer.conn
                ):
                    # Try database approach
                    conn = self._async_checkpointer.conn
                    async with conn.connection() as db_conn:
                        async with db_conn.cursor() as cursor:
                            # Delete all records for this thread ID
                            await cursor.execute(
                                "DELETE FROM checkpoints WHERE thread_id = %s",
                                (thread_id,),
                            )

                logger.info(f"State reset successfully for thread {thread_id} (async)")
                return True

            except Exception as e:
                logger.error(f"Error resetting state asynchronously: {e}")
                return False
        else:
            # Use thread pool for async operation with sync checkpointer
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, lambda: self.reset_state(thread_id, config)
                )
                return result
            except Exception as e:
                logger.error(f"Error in async state reset: {e}")
                return False

    def load_from_state(
        self, state_data: Union[Dict[str, Any], str], thread_id: Optional[str] = None
    ) -> bool:
        """
        Load agent state from a saved state file or dictionary.

        Args:
            state_data: Dictionary or path to JSON file containing state data
            thread_id: Optional thread ID for persistence

        Returns:
            True if successful, False otherwise
        """
        if not self.checkpointer:
            logger.warning("Cannot load state: No checkpointer configured")
            return False

        # Generate thread ID if not provided
        if not thread_id:
            thread_id = str(uuid.uuid4())

        # Load state from string path if provided
        if isinstance(state_data, str) and os.path.exists(state_data):
            try:
                with open(state_data, "r") as f:
                    state_data = json.load(f)
            except Exception as e:
                logger.error(f"Error loading state file: {e}")
                return False

        # Ensure state is a dictionary
        if not isinstance(state_data, dict):
            logger.error(f"Invalid state data type: {type(state_data)}")
            return False

        try:
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                with self.console.status(
                    f"[bold blue]Loading state for thread {thread_id}...[/bold blue]"
                ):
                    # Connect to checkpointer
                    ensure_pool_open(self.checkpointer)

                    # Create runtime config with thread ID
                    runtime_config = self._prepare_runnable_config(thread_id=thread_id)

                    # Process state based on its format
                    if "values" in state_data:
                        # Handle StateSnapshot-like dict
                        values = state_data["values"]

                        # Use checkpoint save mechanism
                        if hasattr(self.app, "app"):
                            # If app is a wrapper
                            config = runtime_config.copy()
                            self.app.app.checkpoint_save(thread_id, values, config)
                        elif hasattr(self.app, "checkpoint_save"):
                            # Direct access
                            config = runtime_config.copy()
                            self.app.checkpoint_save(thread_id, values, config)
                        elif hasattr(self.checkpointer, "save"):
                            # Use checkpointer directly
                            self.checkpointer.save(thread_id, values)
                        else:
                            # Fallback approach
                            raise NotImplementedError(
                                "No checkpoint save mechanism available"
                            )
                    else:
                        # Assume the entire dict is the state
                        if hasattr(self.app, "app"):
                            # If app is a wrapper
                            config = runtime_config.copy()
                            self.app.app.checkpoint_save(thread_id, state_data, config)
                        elif hasattr(self.app, "checkpoint_save"):
                            # Direct access
                            config = runtime_config.copy()
                            self.app.checkpoint_save(thread_id, state_data, config)
                        elif hasattr(self.checkpointer, "save"):
                            # Use checkpointer directly
                            self.checkpointer.save(thread_id, state_data)
                        else:
                            # Fallback approach
                            raise NotImplementedError(
                                "No checkpoint save mechanism available"
                            )

                self.console.print(
                    f"[bold green]State loaded successfully for thread {thread_id}[/bold green]"
                )
            else:
                # Connect to checkpointer
                ensure_pool_open(self.checkpointer)

                # Create runtime config with thread ID
                runtime_config = self._prepare_runnable_config(thread_id=thread_id)

                # Process state based on its format
                if "values" in state_data:
                    # Handle StateSnapshot-like dict
                    values = state_data["values"]

                    # Use checkpoint save mechanism
                    if hasattr(self.app, "app"):
                        # If app is a wrapper
                        config = runtime_config.copy()
                        self.app.app.checkpoint_save(thread_id, values, config)
                    elif hasattr(self.app, "checkpoint_save"):
                        # Direct access
                        config = runtime_config.copy()
                        self.app.checkpoint_save(thread_id, values, config)
                    elif hasattr(self.checkpointer, "save"):
                        # Use checkpointer directly
                        self.checkpointer.save(thread_id, values)
                    else:
                        # Fallback approach
                        raise NotImplementedError(
                            "No checkpoint save mechanism available"
                        )
                else:
                    # Assume the entire dict is the state
                    if hasattr(self.app, "app"):
                        # If app is a wrapper
                        config = runtime_config.copy()
                        self.app.app.checkpoint_save(thread_id, state_data, config)
                    elif hasattr(self.app, "checkpoint_save"):
                        # Direct access
                        config = runtime_config.copy()
                        self.app.checkpoint_save(thread_id, state_data, config)
                    elif hasattr(self.checkpointer, "save"):
                        # Use checkpointer directly
                        self.checkpointer.save(thread_id, state_data)
                    else:
                        # Fallback approach
                        raise NotImplementedError(
                            "No checkpoint save mechanism available"
                        )

                logger.info(f"State loaded successfully for thread {thread_id}")

            return True
        except Exception as e:
            logger.error(f"Error loading state: {e}")
            if self.rich_logging and RICH_AVAILABLE and hasattr(self, "console"):
                self.console.print(f"[bold red]Error loading state: {e}[/bold red]")
            return False

    async def load_from_state_async(
        self, state_data: Union[Dict[str, Any], str], thread_id: Optional[str] = None
    ) -> bool:
        """
        Asynchronously load agent state from a saved state file or dictionary.

        Args:
            state_data: Dictionary or path to JSON file containing state data
            thread_id: Optional thread ID for persistence

        Returns:
            True if successful, False otherwise
        """
        # Check for async mode
        checkpoint_mode = getattr(self, "_checkpoint_mode", "sync")
        is_async_mode = checkpoint_mode == "async"

        if is_async_mode and hasattr(self, "_get_async_checkpointer"):
            try:
                # Get async checkpointer
                async_checkpointer = await self._get_async_checkpointer()

                # Generate thread ID if not provided
                if not thread_id:
                    thread_id = str(uuid.uuid4())

                # Load state from string path if provided
                if isinstance(state_data, str) and os.path.exists(state_data):
                    try:
                        with open(state_data, "r") as f:
                            state_data = json.load(f)
                    except Exception as e:
                        logger.error(f"Error loading state file: {e}")
                        return False

                # Ensure state is a dictionary
                if not isinstance(state_data, dict):
                    logger.error(f"Invalid state data type: {type(state_data)}")
                    return False

                # Create runtime config with thread ID
                self._prepare_runnable_config(thread_id=thread_id)

                # Process state based on its format
                if "values" in state_data:
                    # Handle StateSnapshot-like dict
                    values = state_data["values"]

                    # Use checkpoint save mechanism
                    if hasattr(async_checkpointer, "save"):
                        # Use checkpointer directly
                        await async_checkpointer.save(thread_id, values)
                    else:
                        # Fallback to sync approach in thread
                        await asyncio.get_event_loop().run_in_executor(
                            None, lambda: self.load_from_state(state_data, thread_id)
                        )
                else:
                    # Assume the entire dict is the state
                    if hasattr(async_checkpointer, "save"):
                        # Use checkpointer directly
                        await async_checkpointer.save(thread_id, state_data)
                    else:
                        # Fallback to sync approach in thread
                        await asyncio.get_event_loop().run_in_executor(
                            None, lambda: self.load_from_state(state_data, thread_id)
                        )

                logger.info(f"State loaded successfully for thread {thread_id} (async)")
                return True

            except Exception as e:
                logger.error(f"Error loading state asynchronously: {e}")
                return False
        else:
            # Use thread pool for async operation with sync checkpointer
            try:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, lambda: self.load_from_state(state_data, thread_id)
                )
                return result
            except Exception as e:
                logger.error(f"Error in async state loading: {e}")
                return False

    def __del__(self):
        """Clean up resources when the agent is deleted."""
        # Clean up async resources if needed
        if hasattr(self, "_async_context_managers") and self._async_context_managers:
            try:
                # We can't use async functions in __del__, so we just log a warning
                logger.warning(
                    "Agent destroyed with active async contexts. Resources may not be properly cleaned up."
                )
            except:
                pass
