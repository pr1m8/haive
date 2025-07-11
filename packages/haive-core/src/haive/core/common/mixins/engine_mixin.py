"""Engine management mixin for tracking and accessing Haive engines.

This module provides a sophisticated mixin for managing different types of
engines within the Haive framework. It enables tracking engines by name and type,
collecting usage statistics, and provides rich visualization capabilities.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins import EngineStateMixin
    from haive.core.engine.llm import LLMEngine

    class MyState(EngineStateMixin, BaseModel):
        # Other fields
        pass

    # Create state and add engines
    state = MyState()

    # Add an LLM engine
    llm = LLMEngine(name="my_llm", model="gpt-4", provider="openai")
    state.add_engine(llm)

    # Later, retrieve the engine
    retrieved_llm = state.get_engine("my_llm")

    # Get all LLM engines
    all_llms = state.get_llms()

    # Display engine information
    state.display_engines()
    ```
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table
from rich.tree import Tree

from haive.core.engine.base import Engine, EngineType

logger = logging.getLogger(__name__)


class EngineStateMixin(BaseModel):
    """Mixin providing comprehensive engine management capabilities with validation.

    This mixin allows StateSchema to manage engines by name and type, providing
    rich access patterns, performance tracking, and debugging capabilities.

    The mixin maintains multiple indexes for efficient access:
    - By name: Fast lookup of specific engines
    - By type: Group engines by their type (LLM, Retriever, etc.)

    It also tracks metadata about engines including access patterns and
    performance metrics, and provides rich visualization for debugging.

    Attributes:
        engines: Dictionary of engines indexed by name.
        engines_by_type: Dictionary of engines organized by type.
        engine_metadata: Dictionary containing additional metadata for each engine.
    """

    # Main storage - using proper field names (no leading underscore)
    engines: dict[str, Engine] = Field(
        default_factory=dict, description="Engines indexed by name"
    )
    engines_by_type: dict[EngineType, list[Engine]] = Field(
        default_factory=lambda: {engine_type: [] for engine_type in EngineType},
        description="Engines organized by type for quick access",
    )

    # Track engine metadata and relationships
    engine_metadata: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Additional metadata for each engine"
    )

    # Private attributes for internal tracking
    _engine_access_log: list[dict[str, Any]] = PrivateAttr(default_factory=list)
    _engine_performance_metrics: dict[str, dict[str, float]] = PrivateAttr(
        default_factory=dict
    )

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    @model_validator(mode="after")
    def validate_and_organize_engines(self) -> "EngineStateMixin":
        """Ensure engines are properly organized by type and validated.

        This validator rebuilds the engines_by_type index to ensure consistency
        and initializes metadata for any engines that don't have it yet.

        Returns:
            Self with validated engine organization.
        """
        # Rebuild engines_by_type to ensure consistency
        self.engines_by_type = {engine_type: [] for engine_type in EngineType}

        for name, engine in self.engines.items():
            if not isinstance(engine, Engine):
                logger.warning(f"Object '{name}' is not an Engine instance")
                continue

            engine_type = engine.engine_type
            if engine not in self.engines_by_type[engine_type]:
                self.engines_by_type[engine_type].append(engine)

            # Initialize metadata if not present
            if name not in self.engine_metadata:
                self.engine_metadata[name] = {
                    "added_at": datetime.now().isoformat(),
                    "access_count": 0,
                    "last_accessed": None,
                    "performance": {
                        "total_calls": 0,
                        "total_time": 0.0,
                        "avg_time": 0.0,
                    },
                }

        return self

    # ===== Engine Management Methods =====

    def add_engine(self, engine: Engine, name: str | None = None) -> None:
        """Add an engine to the state with automatic organization by type.

        This method adds an engine to both the main engines dictionary and the
        type-based index. It also initializes metadata tracking for the engine.

        Args:
            engine: The engine to add.
            name: Optional name override (defaults to engine.name).
        """
        engine_name = name or engine.name
        self.engines[engine_name] = engine

        # Add to type index
        if engine not in self.engines_by_type[engine.engine_type]:
            self.engines_by_type[engine.engine_type].append(engine)

        # Update metadata
        self.engine_metadata[engine_name] = {
            "added_at": datetime.now().isoformat(),
            "access_count": 0,
            "last_accessed": None,
            "original_name": engine.name,
            "type": engine.engine_type.value,
            "performance": {"total_calls": 0, "total_time": 0.0, "avg_time": 0.0},
        }

        logger.debug(f"Added engine '{engine_name}' of type {engine.engine_type}")

    def get_engine(self, name: str) -> Engine | None:
        """Get an engine by name with access logging.

        This method retrieves an engine by name and updates access metrics
        including access count, timestamp, and performance data.

        Args:
            name: Engine name.

        Returns:
            Engine if found, None otherwise.
        """
        import time

        start_time = time.time()

        engine = self.engines.get(name)

        if engine:
            # Update access metadata
            if name in self.engine_metadata:
                self.engine_metadata[name]["access_count"] += 1
                self.engine_metadata[name]["last_accessed"] = datetime.now().isoformat()

                # Update performance metrics
                elapsed = time.time() - start_time
                perf = self.engine_metadata[name]["performance"]
                perf["total_calls"] += 1
                perf["total_time"] += elapsed
                perf["avg_time"] = perf["total_time"] / perf["total_calls"]

            # Log access
            self._engine_access_log.append(
                {
                    "engine": name,
                    "timestamp": datetime.now().isoformat(),
                    "operation": "get_engine",
                    "duration_ms": (time.time() - start_time) * 1000,
                }
            )

        return engine

    def get_engines_by_type(self, engine_type: EngineType) -> list[Engine]:
        """Get all engines of a specific type.

        Args:
            engine_type: The engine type to filter by.

        Returns:
            List of engines of the specified type.
        """
        return self.engines_by_type.get(engine_type, [])

    def get_all_engines(self) -> dict[str, Engine]:
        """Get all engines as a dictionary.

        Returns:
            Dictionary of all engines by name.
        """
        return self.engines.copy()

    # ===== Specialized Getters =====

    def get_llms(self) -> list[Engine]:
        """Get all LLM/AugLLM engines.

        Returns:
            List of LLM engines.
        """
        return self.get_engines_by_type(EngineType.LLM)

    def get_retrievers(self) -> list[Engine]:
        """Get all retriever engines.

        Returns:
            List of retriever engines.
        """
        return self.get_engines_by_type(EngineType.RETRIEVER)

    def get_agents(self) -> list[Engine]:
        """Get all agent engines.

        Returns:
            List of agent engines.
        """
        return self.get_engines_by_type(EngineType.AGENT)

    def get_vector_stores(self) -> list[Engine]:
        """Get all vector store engines.

        Returns:
            List of vector store engines.
        """
        return self.get_engines_by_type(EngineType.VECTOR_STORE)

    def get_tools(self) -> list[Engine]:
        """Get all tool engines.

        Returns:
            List of tool engines.
        """
        return self.get_engines_by_type(EngineType.TOOL)

    def get_embeddings(self) -> list[Engine]:
        """Get all embeddings engines.

        Returns:
            List of embeddings engines.
        """
        return self.get_engines_by_type(EngineType.EMBEDDINGS)

    # ===== Engine Manipulation =====

    def update_engine(self, name: str, **kwargs) -> None:
        """Update engine attributes dynamically.

        This method allows updating specific attributes of an engine
        by providing them as keyword arguments.

        Args:
            name: Engine name.
            **kwargs: Attributes to update.

        Raises:
            ValueError: If the engine is not found.
        """
        engine = self.get_engine(name)
        if not engine:
            raise ValueError(f"Engine '{name}' not found")

        for key, value in kwargs.items():
            if hasattr(engine, key):
                setattr(engine, key, value)
                logger.debug(f"Updated engine '{name}' attribute '{key}' to '{value}'")
            else:
                logger.warning(f"Engine '{name}' has no attribute '{key}'")

    def change_provider(self, name: str, provider: str) -> None:
        """Change the provider of an LLM engine.

        This is a convenience method specifically for changing the
        provider of an engine (e.g., switching from 'openai' to 'anthropic').

        Args:
            name: Engine name.
            provider: New provider name.

        Raises:
            ValueError: If the engine is not found.
        """
        engine = self.get_engine(name)
        if not engine:
            raise ValueError(f"Engine '{name}' not found")

        if hasattr(engine, "provider"):
            old_provider = getattr(engine, "provider", "unknown")
            engine.provider = provider
            logger.info(
                f"Changed engine '{name}' provider from '{old_provider}' to '{provider}'"
            )
        else:
            logger.warning(f"Engine '{name}' does not have a provider attribute")

    def get_engine_tools(self, name: str) -> list[Any]:
        """Get tools from an engine (for agents/LLMs with tools).

        This method tries to extract tools from an engine by checking
        various attribute names where tools might be stored.

        Args:
            name: Engine name.

        Returns:
            List of tools if available, empty list otherwise.
        """
        engine = self.get_engine(name)
        if not engine:
            return []

        # Try different attributes where tools might be stored
        for attr in ["tools", "tool_instances", "available_tools", "tool_configs"]:
            if hasattr(engine, attr):
                tools = getattr(engine, attr)
                if isinstance(tools, list):
                    return tools
                if tools is not None:
                    return [tools]

        return []

    def get_engine_routes(self, name: str) -> dict[str, str]:
        """Get tool routes from an engine.

        This method tries to extract routing information from an engine
        by checking various attribute names where routes might be stored.

        Args:
            name: Engine name.

        Returns:
            Dictionary of routes if available, empty dict otherwise.
        """
        engine = self.get_engine(name)
        if not engine:
            return {}

        # Try different attributes where routes might be stored
        for attr in ["tool_routes", "routes", "routing_table", "tool_routing"]:
            if hasattr(engine, attr):
                routes = getattr(engine, attr)
                if isinstance(routes, dict):
                    return routes

        return {}

    def remove_engine(self, name: str) -> bool:
        """Remove an engine from the state.

        This method removes an engine from both the main engines dictionary
        and the type-based index, as well as removing its metadata.

        Args:
            name: Engine name to remove.

        Returns:
            True if removed, False if not found.
        """
        if name not in self.engines:
            return False

        engine = self.engines[name]

        # Remove from main storage
        del self.engines[name]

        # Remove from type index
        if engine in self.engines_by_type[engine.engine_type]:
            self.engines_by_type[engine.engine_type].remove(engine)

        # Remove metadata
        if name in self.engine_metadata:
            del self.engine_metadata[name]

        logger.info(f"Removed engine '{name}'")
        return True

    # ===== Rich UI Display Methods =====

    def display_engines(
        self, show_metadata: bool = False, show_performance: bool = False
    ) -> None:
        """Display all engines in a rich tree view organized by type.

        This method creates a rich visual representation of engines
        organized by type, with optional metadata and performance information.

        Args:
            show_metadata: Whether to show additional metadata.
            show_performance: Whether to show performance metrics.
        """
        console = Console()

        # Create tree view by type
        tree = Tree("🔧 [bold cyan]Engines[/bold cyan]")

        # LLMs
        if llms := self.get_llms():
            llm_branch = tree.add(f"🤖 [bold yellow]LLMs[/bold yellow] ({len(llms)})")
            for llm in llms:
                llm_info = f"[green]{llm.name}[/green]"
                if hasattr(llm, "model"):
                    llm_info += f" [dim]({llm.model})[/dim]"
                if hasattr(llm, "provider"):
                    llm_info += f" [blue]{llm.provider}[/blue]"

                node = llm_branch.add(llm_info)

                if show_metadata and llm.name in self.engine_metadata:
                    meta = self.engine_metadata[llm.name]
                    node.add(f"[dim]Access count: {meta.get('access_count', 0)}[/dim]")
                    node.add(
                        f"[dim]Last accessed: {meta.get('last_accessed', 'Never')}[/dim]"
                    )

                if show_performance and llm.name in self.engine_metadata:
                    perf = self.engine_metadata[llm.name].get("performance", {})
                    node.add(
                        f"[dim]Avg response time: {perf.get('avg_time', 0):.3f}s[/dim]"
                    )

        # Retrievers
        if retrievers := self.get_retrievers():
            ret_branch = tree.add(
                f"🔍 [bold magenta]Retrievers[/bold magenta] ({len(retrievers)})"
            )
            for ret in retrievers:
                ret_info = f"[green]{ret.name}[/green]"
                if hasattr(ret, "retriever_type"):
                    ret_info += f" [dim]({ret.retriever_type})[/dim]"
                ret_branch.add(ret_info)

        # Agents
        if agents := self.get_agents():
            agent_branch = tree.add(f"🎯 [bold red]Agents[/bold red] ({len(agents)})")
            for agent in agents:
                agent_info = f"[green]{agent.name}[/green]"
                if hasattr(agent, "engines"):
                    agent_info += f" [dim]({len(agent.engines)} sub-engines)[/dim]"
                elif hasattr(agent, "components"):
                    agent_info += f" [dim]({len(agent.components)} components)[/dim]"
                agent_branch.add(agent_info)

        # Vector Stores
        if vector_stores := self.get_vector_stores():
            vs_branch = tree.add(
                f"💾 [bold blue]Vector Stores[/bold blue] ({len(vector_stores)})"
            )
            for vs in vector_stores:
                vs_info = f"[green]{vs.name}[/green]"
                if hasattr(vs, "vector_store_provider"):
                    vs_info += f" [dim]({vs.vector_store_provider})[/dim]"
                vs_branch.add(vs_info)

        # Tools
        if tools := self.get_tools():
            tool_branch = tree.add(f"🔨 [bold green]Tools[/bold green] ({len(tools)})")
            for tool in tools:
                tool_info = f"[green]{tool.name}[/green]"
                if hasattr(tool, "description"):
                    tool_info += f" [dim]{tool.description[:50]}...[/dim]"
                tool_branch.add(tool_info)

        # Embeddings
        if embeddings := self.get_embeddings():
            emb_branch = tree.add(
                f"📊 [bold cyan]Embeddings[/bold cyan] ({len(embeddings)})"
            )
            for emb in embeddings:
                emb_info = f"[green]{emb.name}[/green]"
                if hasattr(emb, "model"):
                    emb_info += f" [dim]({emb.model})[/dim]"
                emb_branch.add(emb_info)

        console.print(tree)

        # Show summary statistics
        total_engines = len(self.engines)
        console.print(f"\n[bold]Total Engines:[/bold] {total_engines}")

        if show_metadata or show_performance:
            # Show top accessed engines
            sorted_by_access = sorted(
                self.engine_metadata.items(),
                key=lambda x: x[1].get("access_count", 0),
                reverse=True,
            )[:5]

            if sorted_by_access and sorted_by_access[0][1].get("access_count", 0) > 0:
                console.print("\n[bold]Top Accessed Engines:[/bold]")
                for name, meta in sorted_by_access:
                    if meta.get("access_count", 0) > 0:
                        console.print(f"  {name}: {meta['access_count']} accesses")

    def display_engine_details(self, name: str) -> None:
        """Display detailed information about a specific engine.

        This method creates a rich visual representation of all the details
        for a specific engine, including its configuration, metadata,
        and performance metrics.

        Args:
            name: Engine name.
        """
        console = Console()

        engine = self.get_engine(name)
        if not engine:
            console.print(f"[red]Engine '{name}' not found[/red]")
            return

        # Create detailed panel
        details = Table(show_header=False, box=None, padding=(0, 1))
        details.add_column(style="bold cyan", width=20)
        details.add_column()

        # Basic info
        details.add_row("Name:", engine.name)
        details.add_row("Type:", engine.engine_type.value)
        details.add_row("ID:", engine.id)

        # Type-specific info
        if hasattr(engine, "model"):
            details.add_row("Model:", str(engine.model))
        if hasattr(engine, "provider"):
            details.add_row("Provider:", str(engine.provider))
        if hasattr(engine, "temperature"):
            details.add_row("Temperature:", str(engine.temperature))
        if hasattr(engine, "retriever_type"):
            details.add_row("Retriever Type:", str(engine.retriever_type))
        if hasattr(engine, "vector_store_provider"):
            details.add_row("Vector Store:", str(engine.vector_store_provider))

        # Tools info
        tools = self.get_engine_tools(name)
        if tools:
            details.add_row("Tools:", f"{len(tools)} available")
            for i, tool in enumerate(tools[:3]):
                tool_name = getattr(tool, "name", f"Tool {i+1}")
                details.add_row("", f"  - {tool_name}")
            if len(tools) > 3:
                details.add_row("", f"  ... and {len(tools) - 3} more")

        # Routes info
        routes = self.get_engine_routes(name)
        if routes:
            details.add_row("Routes:", f"{len(routes)} defined")
            for route_name, route_target in list(routes.items())[:3]:
                details.add_row("", f"  {route_name} → {route_target}")
            if len(routes) > 3:
                details.add_row("", f"  ... and {len(routes) - 3} more")

        # Metadata
        if name in self.engine_metadata:
            meta = self.engine_metadata[name]
            details.add_row("", "")  # Spacer
            details.add_row("[bold]Metadata[/bold]", "")
            details.add_row("Added At:", meta.get("added_at", "Unknown")[:19])
            details.add_row("Access Count:", str(meta.get("access_count", 0)))
            details.add_row(
                "Last Accessed:",
                (
                    meta.get("last_accessed", "Never")[:19]
                    if meta.get("last_accessed")
                    else "Never"
                ),
            )

            # Performance metrics
            if "performance" in meta:
                perf = meta["performance"]
                details.add_row("", "")  # Spacer
                details.add_row("[bold]Performance[/bold]", "")
                details.add_row("Total Calls:", str(perf.get("total_calls", 0)))
                details.add_row("Avg Time:", f"{perf.get('avg_time', 0):.3f}s")

        panel = Panel(
            details, title=f"[bold]Engine: {name}[/bold]", border_style="cyan"
        )

        console.print(panel)

        # Show configuration if available
        if hasattr(engine, "model_dump"):
            config_data = engine.model_dump(exclude={"id", "name", "engine_type"})
            if config_data:
                config_json = json.dumps(config_data, indent=2)
                syntax = Syntax(config_json, "json", theme="monokai", line_numbers=True)
                console.print("\n[bold]Configuration:[/bold]")
                console.print(syntax)

    def debug_engine_access(self, limit: int = 10) -> None:
        """Show debug information about engine access patterns.

        This method displays access statistics and a recent access log
        to help with debugging engine usage patterns and performance.

        Args:
            limit: Maximum number of access log entries to show.
        """
        console = Console()

        console.print("[bold cyan]Engine Access Debug Info[/bold cyan]\n")

        # Access statistics table
        stats_table = Table(title="Access Statistics")
        stats_table.add_column("Engine", style="cyan")
        stats_table.add_column("Type", style="magenta")
        stats_table.add_column("Access Count", justify="right")
        stats_table.add_column("Last Accessed")
        stats_table.add_column("Avg Time (ms)", justify="right")

        for name, metadata in sorted(
            self.engine_metadata.items(),
            key=lambda x: x[1].get("access_count", 0),
            reverse=True,
        ):
            engine = self.engines.get(name)
            if engine:
                perf = metadata.get("performance", {})
                stats_table.add_row(
                    name,
                    engine.engine_type.value,
                    str(metadata.get("access_count", 0)),
                    (
                        metadata.get("last_accessed", "Never")[:19]
                        if metadata.get("last_accessed")
                        else "Never"
                    ),
                    (
                        f"{perf.get('avg_time', 0) * 1000:.1f}"
                        if perf.get("avg_time", 0) > 0
                        else "-"
                    ),
                )

        console.print(stats_table)

        # Recent access log
        if self._engine_access_log:
            console.print(f"\n[bold]Recent Access Log[/bold] (last {limit} entries):")

            log_table = Table()
            log_table.add_column("Timestamp", style="dim")
            log_table.add_column("Engine", style="cyan")
            log_table.add_column("Operation")
            log_table.add_column("Duration (ms)", justify="right")

            for entry in self._engine_access_log[-limit:]:
                log_table.add_row(
                    entry["timestamp"][:19],
                    entry["engine"],
                    entry["operation"],
                    f"{entry.get('duration_ms', 0):.1f}",
                )

            console.print(log_table)

    def get_engine_summary(self) -> dict[str, Any]:
        """Get a summary of all engines.

        This method generates a summary of engine statistics including
        counts by type, access patterns, and performance information.

        Returns:
            Dictionary with engine statistics.
        """
        summary = {
            "total_engines": len(self.engines),
            "engines_by_type": {
                engine_type.value: len(self.get_engines_by_type(engine_type))
                for engine_type in EngineType
            },
            "most_accessed": None,
            "least_accessed": None,
            "total_accesses": 0,
        }

        if self.engine_metadata:
            # Find most and least accessed
            sorted_by_access = sorted(
                self.engine_metadata.items(), key=lambda x: x[1].get("access_count", 0)
            )

            if sorted_by_access:
                least = sorted_by_access[0]
                most = sorted_by_access[-1]

                summary["least_accessed"] = {
                    "name": least[0],
                    "count": least[1].get("access_count", 0),
                }
                summary["most_accessed"] = {
                    "name": most[0],
                    "count": most[1].get("access_count", 0),
                }

                # Total accesses
                summary["total_accesses"] = sum(
                    meta.get("access_count", 0)
                    for meta in self.engine_metadata.values()
                )

        return summary
