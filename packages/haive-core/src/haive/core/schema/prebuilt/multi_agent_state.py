"""Multi-agent state with hierarchical agent management and recompilation support.

This module provides a state schema for managing multiple agents without schema
flattening, maintaining hierarchical access with proper typing for the graph API.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

from pydantic import Field, computed_field, field_validator, model_validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

from haive.core.schema.prebuilt.tool_state import ToolState

if TYPE_CHECKING:
    from haive.agents.base import Agent

# Rich console for debug visualization
console = Console()


class MultiAgentState(ToolState):
    """State schema for multi-agent systems with hierarchical management.

    This schema extends ToolState to provide multi-agent coordination while
    maintaining type safety and hierarchical access patterns. Unlike traditional
    approaches that flatten agent schemas, this maintains each agent's schema
    independently while providing coordinated execution.

    Key features:
    - Agents stored as first-class fields (agents IN the state)
    - No schema flattening - each agent maintains its own schema
    - Hierarchical state management with isolated agent states
    - Recompilation tracking for dynamic agent updates
    - Tool routing inherited from ToolState
    - Token usage tracking inherited from MessagesStateWithTokenUsage

    The schema supports both list and dict initialization of agents, automatically
    converting lists to dicts keyed by agent name for consistent access.

    Example:
        ```python
        from haive.core.schema.prebuilt import MultiAgentState
        from haive.agents.simple import SimpleAgent

        # Create agents
        planner = SimpleAgent(name="planner")
        executor = SimpleAgent(name="executor")

        # Initialize with list (converted to dict)
        state = MultiAgentState(agents=[planner, executor])

        # Or initialize with dict
        state = MultiAgentState(agents={
            "plan": planner,
            "exec": executor
        })

        # Access agents hierarchically
        planner_state = state.get_agent_state("plan")
        state.update_agent_state("plan", {"current_plan": "..."})

        # Mark for recompilation
        state.mark_agent_for_recompile("plan")
        ```
    """

    # ========================================================================
    # AGENT MANAGEMENT
    # ========================================================================

    # Agents can be passed as list or dict
    agents: list["Agent"] | dict[str, "Agent"] = Field(
        default_factory=dict,
        description="Agent instances contained in this state (not flattened)",
    )

    # Hierarchical state management - each agent has isolated state
    agent_states: dict[str, dict[str, Any]] = Field(
        default_factory=dict,
        description="Isolated state for each agent, preserving their schemas",
    )

    # ========================================================================
    # EXECUTION TRACKING
    # ========================================================================

    active_agent: str | None = Field(
        default=None, description="Currently executing agent name"
    )

    agent_outputs: dict[str, Any] = Field(
        default_factory=dict, description="Outputs from each agent execution"
    )

    agent_execution_order: list[str] = Field(
        default_factory=list,
        description="Order of agent execution for sequential coordination",
    )

    # ========================================================================
    # RECOMPILATION SUPPORT
    # ========================================================================

    agents_needing_recompile: set[str] = Field(
        default_factory=set, description="Agent names that need graph recompilation"
    )

    recompile_count: int = Field(
        default=0, description="Total number of recompilations performed"
    )

    recompile_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of recompilation events"
    )

    # ========================================================================
    # VALIDATORS
    # ========================================================================

    @field_validator("agents", mode="before")
    @classmethod
    def convert_agents_to_dict(
        cls, v: list["Agent"] | dict[str, "Agent"]
    ) -> dict[str, "Agent"]:
        """Convert list of agents to dict keyed by agent name.

        This allows flexible initialization while maintaining consistent
        internal representation for hierarchical access.
        """
        if isinstance(v, list):
            # Convert list to dict using agent names
            agent_dict = {}
            for agent in v:
                if not hasattr(agent, "name"):
                    raise ValueError(f"Agent {agent} must have a 'name' attribute")
                agent_dict[agent.name] = agent
            return agent_dict
        return v

    @model_validator(mode="after")
    def setup_agent_hierarchy(self) -> "MultiAgentState":
        """Initialize agent hierarchy and sync engines.

        This validator:
        1. Initializes empty state for each agent
        2. Syncs engines from agents to parent state with namespacing
        3. Sets up execution order if not provided
        4. Validates agent compatibility
        """
        if isinstance(self.agents, dict):
            for agent_name, agent in self.agents.items():
                # Initialize empty state for each agent if not exists
                if agent_name not in self.agent_states:
                    self.agent_states[agent_name] = {}

                # Sync engines from agents to parent state with namespacing
                # This allows the graph to access agent engines hierarchically
                if hasattr(agent, "engines") and agent.engines:
                    for engine_name, engine in agent.engines.items():
                        namespaced_name = f"{agent_name}.{engine_name}"
                        self.engines[namespaced_name] = engine

                        # Also add without namespace for compatibility
                        if engine_name not in self.engines:
                            self.engines[engine_name] = engine

                # Add main engine if available
                if hasattr(agent, "engine") and agent.engine:
                    self.engines[f"{agent_name}.main"] = agent.engine
                    if "main" not in self.engines:
                        self.engines["main"] = agent.engine

            # Set default execution order if not provided
            if not self.agent_execution_order and self.agents:
                self.agent_execution_order = list(self.agents.keys())

        return self

    # ========================================================================
    # AGENT STATE MANAGEMENT
    # ========================================================================

    def get_agent_state(self, agent_name: str) -> dict[str, Any]:
        """Get isolated state for a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent's isolated state dictionary
        """
        return self.agent_states.get(agent_name, {})

    def update_agent_state(self, agent_name: str, updates: dict[str, Any]) -> None:
        """Update isolated state for a specific agent.

        Args:
            agent_name: Name of the agent
            updates: State updates to apply
        """
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = {}
        self.agent_states[agent_name].update(updates)

    def set_active_agent(self, agent_name: str) -> None:
        """Set the currently active agent.

        Args:
            agent_name: Name of the agent to activate
        """
        if agent_name not in self.agents:
            raise ValueError(f"Agent '{agent_name}' not found in agents")
        self.active_agent = agent_name

    # ========================================================================
    # RECOMPILATION MANAGEMENT
    # ========================================================================

    def mark_agent_for_recompile(
        self, agent_name: str, reason: str | None = None
    ) -> None:
        """Mark an agent as needing recompilation.

        Args:
            agent_name: Name of the agent
            reason: Optional reason for recompilation
        """
        self.agents_needing_recompile.add(agent_name)

        # Add to history
        self.recompile_history.append(
            {
                "agent_name": agent_name,
                "reason": reason or "Manual recompilation request",
                "timestamp": __import__("datetime").datetime.now().isoformat(),
                "resolved": False,
            }
        )

    def resolve_agent_recompile(self, agent_name: str) -> None:
        """Mark agent recompilation as resolved.

        Args:
            agent_name: Name of the agent
        """
        self.agents_needing_recompile.discard(agent_name)
        self.recompile_count += 1

        # Update history
        for entry in reversed(self.recompile_history):
            if entry["agent_name"] == agent_name and not entry.get("resolved"):
                entry["resolved"] = True
                entry["resolved_at"] = __import__("datetime").datetime.now().isoformat()
                break

    def get_agents_needing_recompile(self) -> set[str]:
        """Get set of agents that need recompilation.

        Returns:
            Set of agent names needing recompilation
        """
        return self.agents_needing_recompile.copy()

    # ========================================================================
    # COMPUTED PROPERTIES
    # ========================================================================

    @computed_field
    @property
    def agent_count(self) -> int:
        """Number of agents in the state."""
        return len(self.agents) if isinstance(self.agents, dict) else 0

    @computed_field
    @property
    def has_active_agent(self) -> bool:
        """Whether there is an active agent."""
        return self.active_agent is not None

    @computed_field
    @property
    def needs_any_recompile(self) -> bool:
        """Whether any agent needs recompilation."""
        return len(self.agents_needing_recompile) > 0

    # ========================================================================
    # UTILITY METHODS
    # ========================================================================

    def get_agent(self, agent_name: str) -> Optional["Agent"]:
        """Get an agent by name.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent instance or None if not found
        """
        if isinstance(self.agents, dict):
            return self.agents.get(agent_name)
        return None

    def get_agent_output(self, agent_name: str) -> Any:
        """Get the output from a specific agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Agent's output or None if not executed
        """
        return self.agent_outputs.get(agent_name)

    def record_agent_output(self, agent_name: str, output: Any) -> None:
        """Record output from an agent execution.

        Args:
            agent_name: Name of the agent
            output: Output to record
        """
        self.agent_outputs[agent_name] = output

    # ========================================================================
    # DEBUG VISUALIZATION METHODS
    # ========================================================================

    def display_debug_info(self, title: str = "MultiAgentState Debug") -> None:
        """Display comprehensive debug information with rich visualization."""
        debug_tree = Tree(f"🔍 {title}", style="bold blue")

        # 1. Agent Overview
        agent_overview = debug_tree.add("👥 Agent Overview", style="bold green")
        self._add_agent_overview(agent_overview)

        # 2. State Hierarchy
        state_hierarchy = debug_tree.add("📊 State Hierarchy", style="bold yellow")
        self._add_state_hierarchy(state_hierarchy)

        # 3. Execution Status
        execution_status = debug_tree.add("🏃 Execution Status", style="bold cyan")
        self._add_execution_status(execution_status)

        # 4. Engine Management
        engine_mgmt = debug_tree.add("⚙️ Engine Management", style="bold magenta")
        self._add_engine_management(engine_mgmt)

        # 5. Recompilation Status
        recompile_status = debug_tree.add("🔄 Recompilation Status", style="bold red")
        self._add_recompilation_status(recompile_status)

        # Display in panel
        console.print(Panel(debug_tree, border_style="blue", expand=False))
        console.print()

    def _add_agent_overview(self, branch: Tree) -> None:
        """Add agent overview information."""
        if isinstance(self.agents, dict):
            # Agent count and types
            branch.add(f"📊 Total Agents: {len(self.agents)}")

            # List each agent with details
            for name, agent in self.agents.items():
                agent_type = type(agent).__name__
                has_state = name in self.agent_states and bool(self.agent_states[name])
                has_output = name in self.agent_outputs

                status_indicators = []
                if name == self.active_agent:
                    status_indicators.append("🟢 Active")
                if has_state:
                    status_indicators.append("📊 Has State")
                if has_output:
                    status_indicators.append("📤 Has Output")
                if name in self.agents_needing_recompile:
                    status_indicators.append("🔄 Needs Recompile")

                status_str = (
                    " | ".join(status_indicators) if status_indicators else "⏸️ Idle"
                )
                branch.add(f"{name} ({agent_type}) - {status_str}")

    def _add_state_hierarchy(self, branch: Tree) -> None:
        """Add state hierarchy information."""
        # Global state fields
        global_fields = [
            f
            for f in self.model_fields
            if f not in ["agents", "agent_states", "agent_outputs"]
        ]
        global_branch = branch.add(f"🌍 Global Fields ({len(global_fields)})")
        for field in global_fields[:5]:  # Show first 5
            value = getattr(self, field, None)
            if isinstance(value, list):
                global_branch.add(f"📋 {field}: [{len(value)} items]")
            elif isinstance(value, dict):
                global_branch.add(f"📁 {field}: {{{len(value)} keys}}")
            else:
                value_str = (
                    str(value)[:30] + "..." if len(str(value)) > 30 else str(value)
                )
                global_branch.add(f"📝 {field}: {value_str}")

        # Agent states
        if self.agent_states:
            states_branch = branch.add(f"🤖 Agent States ({len(self.agent_states)})")
            for agent_name, state in self.agent_states.items():
                state_branch = states_branch.add(f"{agent_name} ({len(state)} fields)")
                for key, value in list(state.items())[:3]:  # Show first 3 fields
                    if isinstance(value, list):
                        state_branch.add(f"📋 {key}: [{len(value)} items]")
                    elif isinstance(value, dict):
                        state_branch.add(f"📁 {key}: {{{len(value)} keys}}")
                    else:
                        value_str = (
                            str(value)[:20] + "..."
                            if len(str(value)) > 20
                            else str(value)
                        )
                        state_branch.add(f"📝 {key}: {value_str}")

    def _add_execution_status(self, branch: Tree) -> None:
        """Add execution status information."""
        # Active agent
        if self.active_agent:
            branch.add(f"⭐ Active Agent: {self.active_agent}")
        else:
            branch.add("⏸️ No Active Agent")

        # Execution order
        if self.agent_execution_order:
            order_branch = branch.add(
                f"📋 Execution Order ({len(self.agent_execution_order)})"
            )
            for i, agent_name in enumerate(self.agent_execution_order):
                status = (
                    "✅ Completed" if agent_name in self.agent_outputs else "⏳ Pending"
                )
                order_branch.add(f"{i+1}. {agent_name} - {status}")

        # Agent outputs
        if self.agent_outputs:
            outputs_branch = branch.add(f"📤 Agent Outputs ({len(self.agent_outputs)})")
            for agent_name, output in self.agent_outputs.items():
                if isinstance(output, dict) and "error" in output:
                    outputs_branch.add(f"❌ {agent_name}: Error - {output['error']}")
                elif isinstance(output, dict):
                    outputs_branch.add(f"✅ {agent_name}: {len(output)} fields")
                else:
                    output_str = (
                        str(output)[:30] + "..."
                        if len(str(output)) > 30
                        else str(output)
                    )
                    outputs_branch.add(f"✅ {agent_name}: {output_str}")

    def _add_engine_management(self, branch: Tree) -> None:
        """Add engine management information."""
        if hasattr(self, "engines") and self.engines:
            engines_branch = branch.add(f"⚙️ Engines ({len(self.engines)})")

            # Group engines by type
            agent_engines = {}
            global_engines = {}

            for name, engine in self.engines.items():
                if "." in name:
                    agent_name = name.split(".")[0]
                    if agent_name not in agent_engines:
                        agent_engines[agent_name] = []
                    agent_engines[agent_name].append(name)
                else:
                    global_engines[name] = engine

            # Show agent engines
            if agent_engines:
                agent_eng_branch = engines_branch.add("🤖 Agent Engines")
                for agent_name, engine_names in agent_engines.items():
                    agent_eng_branch.add(f"{agent_name}: {len(engine_names)} engines")

            # Show global engines
            if global_engines:
                global_eng_branch = engines_branch.add("🌍 Global Engines")
                for name, engine in global_engines.items():
                    engine_type = type(engine).__name__
                    global_eng_branch.add(f"{name} ({engine_type})")
        else:
            branch.add("⚙️ No Engines Configured")

    def _add_recompilation_status(self, branch: Tree) -> None:
        """Add recompilation status information."""
        # Recompilation count
        branch.add(f"🔢 Total Recompiles: {self.recompile_count}")

        # Agents needing recompilation
        if self.agents_needing_recompile:
            needs_branch = branch.add(
                f"🔄 Needs Recompile ({len(self.agents_needing_recompile)})"
            )
            for agent_name in self.agents_needing_recompile:
                needs_branch.add(f"⚠️ {agent_name}")
        else:
            branch.add("✅ No Agents Need Recompilation")

        # Recent recompilation history
        if self.recompile_history:
            recent_count = min(3, len(self.recompile_history))
            history_branch = branch.add(f"📜 Recent History (last {recent_count})")

            for entry in self.recompile_history[-recent_count:]:
                agent_name = entry.get("agent_name", "Unknown")
                reason = entry.get("reason", "No reason")
                resolved = entry.get("resolved", False)
                status = "✅ Resolved" if resolved else "🔄 Pending"
                history_branch.add(f"{agent_name}: {reason} - {status}")

    def create_agent_table(self) -> Table:
        """Create a rich table showing agent status."""
        table = Table(title="🤖 Multi-Agent State Overview")
        table.add_column("Agent Name", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("State Fields", style="yellow")
        table.add_column("Has Output", style="blue")
        table.add_column("Needs Recompile", style="red")

        if isinstance(self.agents, dict):
            for name, agent in self.agents.items():
                agent_type = type(agent).__name__

                # Status
                if name == self.active_agent:
                    status = "🟢 Active"
                elif name in self.agent_outputs:
                    status = "✅ Completed"
                else:
                    status = "⏸️ Idle"

                # State fields count
                state_count = len(self.agent_states.get(name, {}))

                # Has output
                has_output = "✅" if name in self.agent_outputs else "❌"

                # Needs recompile
                needs_recompile = (
                    "⚠️ Yes" if name in self.agents_needing_recompile else "✅ No"
                )

                table.add_row(
                    name,
                    agent_type,
                    status,
                    str(state_count),
                    has_output,
                    needs_recompile,
                )

        return table

    def display_agent_table(self) -> None:
        """Display the agent status table."""
        table = self.create_agent_table()
        console.print(table)
        console.print()
