"""State models for the supervisor system.

This module defines the core state schemas and models used by supervisors
to manage agents, tools, and execution context.
"""

import json
import pickle
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel, ConfigDict, Field, model_validator


class AgentMetadata(BaseModel):
    """Metadata about a registered agent."""

    name: str
    description: str
    capabilities: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    last_used: datetime | None = None
    usage_count: int = 0
    performance_score: float = 1.0  # 0-1 score for agent performance
    tags: list[str] = Field(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SerializedAgent(BaseModel):
    """Container for a serialized agent with metadata."""

    metadata: AgentMetadata
    agent_class: str  # Full class path for reconstruction
    agent_module: str  # Module path
    serialized_data: bytes  # Pickled agent instance
    config_json: str  # JSON serialized config for inspection

    @classmethod
    def from_agent(cls, agent: Any, metadata: AgentMetadata) -> "SerializedAgent":
        """Create from an agent instance."""
        # Get class info
        agent_class = f"{agent.__class__.__module__}.{agent.__class__.__name__}"
        agent_module = agent.__class__.__module__

        # Serialize agent
        serialized_data = pickle.dumps(agent)

        # Try to extract config for inspection
        config_json = "{}"
        if hasattr(agent, "config"):
            try:
                config_json = json.dumps(
                    agent.config.dict() if hasattr(agent.config, "dict") else {}
                )
            except:
                config_json = str(agent.config)

        return cls(
            metadata=metadata,
            agent_class=agent_class,
            agent_module=agent_module,
            serialized_data=serialized_data,
            config_json=config_json,
        )

    def get_agent(self) -> Any:
        """Deserialize and return the agent."""
        return pickle.loads(self.serialized_data)

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ToolMapping(BaseModel):
    """Maps tools to their source agents and categories."""

    tool_name: str
    agent_name: str | None = None  # Source agent if applicable
    category: str = "general"  # general, handoff, control, utility
    description: str
    is_dynamic: bool = False  # Whether tool was dynamically created

    model_config = ConfigDict(arbitrary_types_allowed=True)


class ExecutionContext(BaseModel):
    """Current execution context for the supervisor."""

    current_agent: str | None = None
    current_task: str | None = None
    execution_stack: list[str] = Field(default_factory=list)  # Call stack
    start_time: datetime | None = None
    total_steps: int = 0

    model_config = ConfigDict(arbitrary_types_allowed=True)


class SupervisorState(StateSchema):
    """Base state schema for supervisors with full tracking."""

    # Core conversation state
    messages: list[BaseMessage] = Field(default_factory=list)

    # Agent registry
    agents: dict[str, SerializedAgent] = Field(
        default_factory=dict, description="Registry of available agents"
    )

    # Tool management
    tools: dict[str, BaseTool] = Field(
        default_factory=dict, description="Available tools mapped by name"
    )

    tool_mappings: dict[str, ToolMapping] = Field(
        default_factory=dict, description="Metadata about each tool"
    )

    # Execution tracking
    execution_context: ExecutionContext = Field(
        default_factory=ExecutionContext, description="Current execution state"
    )

    # Results and history
    last_result: Any | None = None
    execution_history: list[dict[str, Any]] = Field(default_factory=list)

    # Configuration
    auto_sync_tools: bool = Field(
        default=True, description="Whether to automatically sync tools with agents"
    )

    max_history_size: int = Field(
        default=100, description="Maximum execution history entries to keep"
    )

    @model_validator(mode="after")
    def sync_tools_if_enabled(self) -> "SupervisorState":
        """Sync tools with agents if auto-sync is enabled."""
        if not self.auto_sync_tools:
            return self

        # Track which tools should exist
        expected_tools = set()

        # Add handoff tools for each agent
        for agent_name in self.agents:
            tool_name = f"handoff_to_{agent_name}"
            expected_tools.add(tool_name)

            # Create tool mapping if missing
            if tool_name not in self.tool_mappings:
                self.tool_mappings[tool_name] = ToolMapping(
                    tool_name=tool_name,
                    agent_name=agent_name,
                    category="handoff",
                    description=f"Hand off task to {agent_name}",
                    is_dynamic=True,
                )

        # Clean up orphaned tool mappings
        mappings_to_remove = []
        for tool_name, mapping in self.tool_mappings.items():
            if mapping.category == "handoff" and mapping.is_dynamic:
                if tool_name not in expected_tools:
                    mappings_to_remove.append(tool_name)

        for tool_name in mappings_to_remove:
            del self.tool_mappings[tool_name]
            # Note: Actual tool removal happens in the supervisor

        return self

    @model_validator(mode="after")
    def trim_history_if_needed(self) -> "SupervisorState":
        """Keep execution history within size limits."""
        if len(self.execution_history) > self.max_history_size:
            # Keep most recent entries
            self.execution_history = self.execution_history[-self.max_history_size :]
        return self

    def add_execution_record(self, record: dict[str, Any]) -> None:
        """Add a record to execution history."""
        record["timestamp"] = datetime.utcnow().isoformat()
        self.execution_history.append(record)

    def get_agent_by_name(self, name: str) -> Any | None:
        """Get deserialized agent by name."""
        if name in self.agents:
            return self.agents[name].get_agent()
        return None

    def register_agent(self, agent: Any, metadata: AgentMetadata) -> None:
        """Register a new agent."""
        serialized = SerializedAgent.from_agent(agent, metadata)
        self.agents[metadata.name] = serialized

    def update_agent_usage(self, agent_name: str) -> None:
        """Update usage statistics for an agent."""
        if agent_name in self.agents:
            self.agents[agent_name].metadata.last_used = datetime.utcnow()
            self.agents[agent_name].metadata.usage_count += 1

    model_config = ConfigDict(arbitrary_types_allowed=True)


class DynamicSupervisorState(SupervisorState):
    """Extended state for dynamic supervisors that can create agents."""

    # Agent creation configuration
    agent_templates: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Templates for creating new agents"
    )

    # Dynamic capabilities
    can_create_agents: bool = Field(
        default=True, description="Whether supervisor can create new agents"
    )

    creation_history: list[dict[str, Any]] = Field(
        default_factory=list, description="History of agent creations"
    )

    # Resource limits
    max_agents: int = Field(default=10, description="Maximum number of agents allowed")

    @model_validator(mode="after")
    def enforce_agent_limit(self) -> "DynamicSupervisorState":
        """Ensure we don't exceed agent limits."""
        if len(self.agents) > self.max_agents:
            # Remove least recently used agents
            agents_by_usage = sorted(
                self.agents.items(),
                key=lambda x: x[1].metadata.last_used or datetime.min,
                reverse=True,
            )

            # Keep only the most recent ones
            self.agents = dict(agents_by_usage[: self.max_agents])

        return self

    def add_agent_template(self, name: str, template: dict[str, Any]) -> None:
        """Add a template for agent creation."""
        self.agent_templates[name] = template

    def record_agent_creation(
        self, agent_name: str, template_used: str | None = None
    ) -> None:
        """Record that an agent was created."""
        self.creation_history.append(
            {
                "agent_name": agent_name,
                "template_used": template_used,
                "created_at": datetime.utcnow().isoformat(),
                "total_agents": len(self.agents),
            }
        )

    model_config = ConfigDict(arbitrary_types_allowed=True)
