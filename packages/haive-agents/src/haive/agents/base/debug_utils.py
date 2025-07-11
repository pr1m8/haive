"""Debug utilities for agent execution with Rich UI.

Provides comprehensive debugging and logging capabilities for agent execution,
particularly focused on runnable config and recursion limit issues.
"""

import logging
from typing import Any

from langchain_core.runnables import RunnableConfig
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

# Global console for debugging
debug_console = Console()

# Debug logger that can be controlled
debug_logger = logging.getLogger("haive.agent.debug")


class AgentDebugger:
    """Rich UI debugger for agent execution."""

    def __init__(self, agent_name: str = "Agent", enabled: bool = False):
        self.agent_name = agent_name
        self.enabled = enabled
        self.console = Console()

    def enable(self):
        """Enable debugging output."""
        self.enabled = True
        debug_logger.setLevel(logging.DEBUG)

    def disable(self):
        """Disable debugging output."""
        self.enabled = False
        debug_logger.setLevel(logging.WARNING)

    def log_runnable_config(self, config: RunnableConfig, context: str = ""):
        """Log runnable config with rich formatting."""
        if not self.enabled:
            return

        # Create a tree view of the config
        tree = Tree(
            f"[bold blue]🔧 Runnable Config{' - ' + context if context else ''}"
        )

        # Top level items
        for key, value in config.items():
            if key == "configurable":
                configurable_tree = tree.add("[yellow]configurable[/yellow]")
                for config_key, config_value in value.items():
                    if config_key == "recursion_limit":
                        color = "green" if config_value and config_value > 0 else "red"
                        configurable_tree.add(
                            f"[{color}]recursion_limit: {config_value}[/{color}]"
                        )
                    elif config_key == "thread_id":
                        configurable_tree.add(
                            f"[cyan]thread_id: {config_value[:8]}...[/cyan]"
                            if config_value
                            else "[red]thread_id: None[/red]"
                        )
                    elif config_key == "engine_configs":
                        engine_tree = configurable_tree.add(
                            "[magenta]engine_configs[/magenta]"
                        )
                        if isinstance(config_value, dict):
                            for engine_id, engine_config in config_value.items():
                                engine_tree.add(
                                    f"[white]{engine_id}: {len(engine_config)} params[/white]"
                                )
                        else:
                            engine_tree.add(
                                f"[red]Invalid engine_configs: {type(config_value)}[/red]"
                            )
                    else:
                        configurable_tree.add(
                            f"[white]{config_key}: {str(config_value)[:50]}{'...' if len(str(config_value)) > 50 else ''}[/white]"
                        )
            elif key == "recursion_limit":
                color = "green" if value and value > 0 else "red"
                tree.add(f"[{color}]TOP-LEVEL recursion_limit: {value}[/{color}]")
            else:
                tree.add(
                    f"[white]{key}: {str(value)[:50]}{'...' if len(str(value)) > 50 else ''}[/white]"
                )

        self.console.print(
            Panel(tree, title=f"[bold]{self.agent_name}[/bold]", border_style="blue")
        )

    def log_recursion_limit_flow(
        self, step: str, recursion_limit: Any, source: str = ""
    ):
        """Track recursion limit through the execution flow."""
        if not self.enabled:
            return

        color = "green" if recursion_limit and recursion_limit > 0 else "red"
        icon = "✅" if recursion_limit and recursion_limit > 0 else "❌"

        text = Text()
        text.append(f"{icon} {step}: ", style="bold")
        text.append(f"recursion_limit={recursion_limit}", style=color)
        if source:
            text.append(f" (from {source})", style="dim")

        self.console.print(
            Panel(
                text,
                title=f"[bold]{self.agent_name} - Recursion Limit Flow[/bold]",
                border_style="yellow",
            )
        )

    def log_config_preparation(
        self,
        base_config: RunnableConfig | None,
        runtime_config: RunnableConfig,
        thread_id: str | None,
        kwargs: dict[str, Any],
    ):
        """Log the config preparation process."""
        if not self.enabled:
            return

        table = Table(
            title=f"{self.agent_name} - Config Preparation",
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Source", style="cyan")
        table.add_column("recursion_limit", justify="center")
        table.add_column("thread_id", style="dim")
        table.add_column("Other Keys")

        # Base config
        base_recursion = "None"
        base_thread = "None"
        base_keys = "None"
        if base_config:
            base_recursion = str(base_config.get("recursion_limit", "None"))
            base_thread = str(
                base_config.get("configurable", {}).get("thread_id", "None")
            )
            base_keys = ", ".join(
                [k for k in base_config if k not in ["recursion_limit", "configurable"]]
            )

        table.add_row(
            "base_config",
            base_recursion,
            base_thread[:8] + "..." if len(base_thread) > 8 else base_thread,
            base_keys,
        )

        # Runtime config
        runtime_recursion = str(runtime_config.get("recursion_limit", "None"))
        runtime_thread = str(
            runtime_config.get("configurable", {}).get("thread_id", "None")
        )
        runtime_keys = ", ".join(
            [k for k in runtime_config if k not in ["recursion_limit", "configurable"]]
        )
        table.add_row(
            "runtime_config",
            runtime_recursion,
            runtime_thread[:8] + "..." if len(runtime_thread) > 8 else runtime_thread,
            runtime_keys,
        )

        # Configurable recursion limit
        configurable_recursion = str(
            runtime_config.get("configurable", {}).get("recursion_limit", "None")
        )
        table.add_row("configurable.recursion_limit", configurable_recursion, "-", "-")

        # Kwargs
        kwargs_recursion = str(kwargs.get("recursion_limit", "None"))
        kwargs_thread = str(kwargs.get("thread_id", "None"))
        kwargs_keys = ", ".join(
            [
                k
                for k in kwargs
                if k not in ["recursion_limit", "thread_id", "debug", "config"]
            ]
        )
        table.add_row("kwargs", kwargs_recursion, kwargs_thread, kwargs_keys)

        self.console.print(table)

    def log_agent_execution_start(self, input_data: Any, config: RunnableConfig):
        """Log the start of agent execution."""
        if not self.enabled:
            return

        panel_content = []

        # Input info
        if hasattr(input_data, "messages"):
            panel_content.append(f"📨 Messages: {len(input_data.messages)}")
        elif isinstance(input_data, dict):
            panel_content.append(f"📦 Dict with keys: {list(input_data.keys())}")
        else:
            panel_content.append(f"📄 Input type: {type(input_data).__name__}")

        # Config info
        recursion_limit = config.get("recursion_limit", "Not set")
        panel_content.append(f"🔄 Recursion limit: {recursion_limit}")

        thread_id = config.get("configurable", {}).get("thread_id", "Not set")
        panel_content.append(
            f"🧵 Thread ID: {thread_id[:8]}..."
            if thread_id != "Not set"
            else "🧵 Thread ID: Not set"
        )

        content = "\n".join(panel_content)
        self.console.print(
            Panel(
                content,
                title=f"[bold green]🚀 Starting {self.agent_name} Execution[/bold green]",
                border_style="green",
            )
        )


# Global debugger instance
_global_debugger: AgentDebugger | None = None


def get_agent_debugger(agent_name: str = "Agent") -> AgentDebugger:
    """Get or create agent debugger."""
    global _global_debugger
    if _global_debugger is None:
        _global_debugger = AgentDebugger(agent_name)
    else:
        _global_debugger.agent_name = agent_name
    return _global_debugger


def enable_agent_debugging():
    """Enable global agent debugging."""
    debug_logger.setLevel(logging.DEBUG)
    if not debug_logger.handlers:
        handler = RichHandler(rich_tracebacks=True, show_path=False)
        handler.setFormatter(logging.Formatter("%(message)s"))
        debug_logger.addHandler(handler)
    debug_logger.info("🐛 Agent debugging enabled")


def disable_agent_debugging():
    """Disable global agent debugging."""
    debug_logger.setLevel(logging.WARNING)
    debug_logger.info("🔇 Agent debugging disabled")


def debug_runnable_config(
    config: RunnableConfig, context: str = "", agent_name: str = "Agent"
):
    """Quick function to debug a runnable config."""
    debugger = get_agent_debugger(agent_name)
    if debug_logger.level <= logging.DEBUG:
        debugger.enabled = True
        debugger.log_runnable_config(config, context)
