"""Flexible multi-agent state that doesn't force messages or tools.

This module provides flexible state schemas for multi-agent systems without forcing
specific fields like messages or tools.
"""

from typing import TYPE_CHECKING, Any, Optional, Self

from pydantic import Field, field_validator, model_validator
from typing_extensions import TypedDict

from haive.core.schema.state_schema import StateSchema

if TYPE_CHECKING:
    from haive.agents.base import Agent


class MinimalMultiAgentState(TypedDict):
    """Minimal state for multi-agent coordination - no forced fields."""

    current_agent: str | None
    completed_agents: list[str]
    final_result: Any | None
    error: str | None


class FlexibleMultiAgentState(StateSchema):
    """Flexible multi-agent state without forcing messages or tools.

    This state schema provides:
    - No forced inheritance from ToolState or MessagesState
    - Flexible agent storage (list or dict)
    - Hierarchical state management
    - Private state passing support
    - No schema flattening

    Example:
        ```python
        # Create with minimal fields
        state = FlexibleMultiAgentState(
            agents=[planner, executor]
        )

        # Or with custom shared context
        state = FlexibleMultiAgentState(
            agents={"plan": planner, "exec": executor},
            shared_context={"task": "analyze data"}
        )
        ```
    """

    # ========================================================================
    # AGENT MANAGEMENT - Core fields
    # ========================================================================

    agents: list["Agent"] | dict[str, "Agent"] = Field(
        default_factory=dict, description="Agent instances - can be list or dict"
    )

    agent_states: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Isolated state for each agent"
    )

    # ========================================================================
    # COORDINATION FIELDS - Optional
    # ========================================================================

    current_agent: str | None = Field(
        default=None, description="Currently executing agent"
    )

    completed_agents: list[str] = Field(
        default_factory=list, description="Agents that have completed execution"
    )

    agent_outputs: dict[str, Any] = Field(
        default_factory=dict, description="Outputs from each agent"
    )

    # ========================================================================
    # FLEXIBLE SHARED CONTEXT - Optional
    # ========================================================================

    shared_context: dict[str, Any] = Field(
        default_factory=dict,
        description="Shared context between agents - completely flexible",
    )

    # Optional error tracking
    error: str | None = Field(default=None, description="Error message if any")

    # Optional final result
    final_result: Any | None = Field(
        default=None, description="Final result from multi-agent execution"
    )

    # ========================================================================
    # STATE TRANSFER CONFIGURATION
    # ========================================================================

    state_transfers: dict[str, dict[str, str]] = Field(
        default_factory=dict,
        description="Configuration for state transfers between agents",
    )

    # ========================================================================
    # VALIDATORS
    # ========================================================================

    @field_validator("agents", mode="before")
    @classmethod
    def normalize_agents(
        cls, v: list["Agent"] | dict[str, "Agent"]
    ) -> dict[str, "Agent"]:
        """Convert list to dict for consistent access."""
        if isinstance(v, list):
            agent_dict = {}
            for agent in v:
                if not hasattr(agent, "name"):
                    raise ValueError(f"Agent {agent} must have 'name' attribute")
                agent_dict[agent.name] = agent
            return agent_dict
        return v

    @model_validator(mode="after")
    def initialize_agent_states(self) -> Self:
        """Initialize empty states for each agent."""
        if isinstance(self.agents, dict):
            for agent_name in self.agents:
                if agent_name not in self.agent_states:
                    self.agent_states[agent_name] = {}
        return self

    # ========================================================================
    # STATE MANAGEMENT METHODS
    # ========================================================================

    def get_agent_state(self, agent_name: str) -> dict[str, Any]:
        """Get state for specific agent."""
        return self.agent_states.get(agent_name, {})

    def update_agent_state(self, agent_name: str, updates: dict[str, Any]) -> None:
        """Update state for specific agent."""
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = {}
        self.agent_states[agent_name].update(updates)

    def get_agent(self, agent_name: str) -> Optional["Agent"]:
        """Get agent by name."""
        if isinstance(self.agents, dict):
            return self.agents.get(agent_name)
        return None

    def record_agent_output(self, agent_name: str, output: Any) -> None:
        """Record output from agent execution."""
        self.agent_outputs[agent_name] = output
        if agent_name not in self.completed_agents:
            self.completed_agents.append(agent_name)

    def set_current_agent(self, agent_name: str) -> None:
        """Set currently executing agent."""
        self.current_agent = agent_name

    def apply_state_transfer(self, from_agent: str, to_agent: str) -> None:
        """Apply configured state transfers between agents."""
        transfer_key = f"{from_agent}->{to_agent}"
        if transfer_key in self.state_transfers:
            transfers = self.state_transfers[transfer_key]
            from_state = self.get_agent_state(from_agent)
            to_updates = {}

            for from_field, to_field in transfers.items():
                if from_field in from_state:
                    to_updates[to_field] = from_state[from_field]

            if to_updates:
                self.update_agent_state(to_agent, to_updates)


class ContainerMultiAgentState(FlexibleMultiAgentState):
    """Container pattern with additional organization features.

    Extends flexible state with:
    - Execution order tracking
    - Agent metadata
    - Recompilation support
    """

    agent_execution_order: list[str] = Field(
        default_factory=list, description="Order of agent execution"
    )

    agent_metadata: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Metadata about each agent"
    )

    recompilation_needed: bool = Field(
        default=False, description="Whether graph recompilation is needed"
    )

    @model_validator(mode="after")
    def setup_execution_order(self) -> Self:
        """Set default execution order if not provided."""
        if not self.agent_execution_order and isinstance(self.agents, dict):
            self.agent_execution_order = list(self.agents.keys())
        return self
