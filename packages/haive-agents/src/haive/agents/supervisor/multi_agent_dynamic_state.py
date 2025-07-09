"""Enhanced Multi-Agent State with Dynamic Agent Management.

This module extends the DynamicSupervisorState to include multi-agent coordination
capabilities, agent registry management, and dynamic choice model integration.
"""

import time
from typing import Any, Dict, List, Optional, Set, Union
from uuid import uuid4

from haive.core.common.models.dynamic_choice_model import DynamicChoiceModel
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, computed_field

from haive.agents.supervisor.dynamic_state import (
    AgentExecutionConfig,
    AgentExecutionResult,
    DynamicSupervisorState,
    SupervisorDecision,
)


class AgentRegistryState(BaseModel):
    """State for dynamic agent registry management."""

    # Registry management
    available_agents: Dict[str, str] = Field(
        default_factory=dict, description="Map of agent names to their types"
    )
    agent_capabilities: Dict[str, str] = Field(
        default_factory=dict,
        description="Map of agent names to capability descriptions",
    )
    agent_tools: Dict[str, List[str]] = Field(
        default_factory=dict, description="Map of agent names to their tool lists"
    )

    # Dynamic choice model state
    choice_model_options: List[str] = Field(
        default_factory=list, description="Current options in the choice model"
    )
    choice_model_version: int = Field(
        default=0, description="Version counter for choice model updates"
    )

    # Agent addition/removal tracking
    pending_agent_additions: List[Dict[str, Any]] = Field(
        default_factory=list, description="Agents pending addition to registry"
    )
    pending_agent_removals: List[str] = Field(
        default_factory=list, description="Agent names pending removal from registry"
    )

    # Tool-to-agent mapping for dynamic routing
    tool_to_agent_mapping: Dict[str, str] = Field(
        default_factory=dict, description="Map of tool names to owning agent names"
    )

    # Agent request tracking
    agent_change_requests: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of agent change requests"
    )
    last_agent_change: Optional[float] = Field(
        default=None, description="Timestamp of last agent registry change"
    )

    def add_agent_to_registry(
        self, agent_name: str, agent_type: str, capability: str, tools: List[str] = None
    ) -> None:
        """Add agent to registry state."""
        self.available_agents[agent_name] = agent_type
        self.agent_capabilities[agent_name] = capability
        if tools:
            self.agent_tools[agent_name] = tools
            # Update tool mapping
            for tool in tools:
                self.tool_to_agent_mapping[tool] = agent_name

        self.last_agent_change = time.time()
        self._update_choice_model_options()

    def remove_agent_from_registry(self, agent_name: str) -> bool:
        """Remove agent from registry state."""
        if agent_name not in self.available_agents:
            return False

        # Remove from all mappings
        self.available_agents.pop(agent_name, None)
        self.agent_capabilities.pop(agent_name, None)

        # Remove tools mapping
        if agent_name in self.agent_tools:
            tools = self.agent_tools.pop(agent_name)
            for tool in tools:
                self.tool_to_agent_mapping.pop(tool, None)

        self.last_agent_change = time.time()
        self._update_choice_model_options()
        return True

    def _update_choice_model_options(self) -> None:
        """Update choice model options based on current agents."""
        self.choice_model_options = list(self.available_agents.keys())
        self.choice_model_version += 1

    def get_agent_for_tool(self, tool_name: str) -> Optional[str]:
        """Get the agent that owns a specific tool."""
        return self.tool_to_agent_mapping.get(tool_name)

    def get_tools_for_agent(self, agent_name: str) -> List[str]:
        """Get tools owned by a specific agent."""
        return self.agent_tools.get(agent_name, [])

    def add_agent_change_request(
        self, request_type: str, agent_name: str, details: Dict[str, Any] = None
    ) -> None:
        """Track agent change requests."""
        request = {
            "type": request_type,  # "add", "remove", "update"
            "agent_name": agent_name,
            "timestamp": time.time(),
            "details": details or {},
        }
        self.agent_change_requests.append(request)


class MultiAgentCoordinationState(BaseModel):
    """State for multi-agent coordination patterns."""

    # Coordination mode
    coordination_mode: str = Field(
        default="supervisor",
        description="Current coordination mode: supervisor, sequential, parallel, swarm",
    )

    # Agent execution queue and history
    execution_queue: List[Dict[str, Any]] = Field(
        default_factory=list, description="Queue of agents/tasks to execute"
    )

    active_executions: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Currently active agent executions"
    )

    # Inter-agent communication
    agent_messages: Dict[str, List[BaseMessage]] = Field(
        default_factory=dict, description="Messages between agents"
    )

    shared_context: Dict[str, Any] = Field(
        default_factory=dict, description="Shared context accessible to all agents"
    )

    # Coordination metadata
    coordination_session_id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique ID for this coordination session",
    )

    coordination_start_time: float = Field(
        default_factory=time.time, description="When coordination session started"
    )

    # Agent handoffs and transitions
    agent_handoffs: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of agent-to-agent handoffs"
    )

    current_active_agent: Optional[str] = Field(
        default=None, description="Currently active agent in coordination"
    )

    def add_to_execution_queue(
        self, agent_name: str, task: Dict[str, Any], priority: int = 1
    ) -> None:
        """Add agent execution to queue."""
        execution = {
            "agent_name": agent_name,
            "task": task,
            "priority": priority,
            "queued_at": time.time(),
            "execution_id": str(uuid4()),
        }
        self.execution_queue.append(execution)
        # Sort by priority (higher first)
        self.execution_queue.sort(key=lambda x: x["priority"], reverse=True)

    def start_agent_execution(self, agent_name: str, execution_id: str) -> None:
        """Mark agent execution as started."""
        execution_info = {
            "started_at": time.time(),
            "status": "active",
            "execution_id": execution_id,
        }
        self.active_executions[agent_name] = execution_info
        self.current_active_agent = agent_name

    def complete_agent_execution(self, agent_name: str) -> None:
        """Mark agent execution as completed."""
        if agent_name in self.active_executions:
            self.active_executions[agent_name]["status"] = "completed"
            self.active_executions[agent_name]["completed_at"] = time.time()

        # Update current active agent
        active_agents = [
            name
            for name, info in self.active_executions.items()
            if info.get("status") == "active"
        ]
        self.current_active_agent = active_agents[0] if active_agents else None

    def add_agent_handoff(
        self,
        from_agent: str,
        to_agent: str,
        reason: str,
        context: Dict[str, Any] = None,
    ) -> None:
        """Record agent handoff."""
        handoff = {
            "from_agent": from_agent,
            "to_agent": to_agent,
            "reason": reason,
            "timestamp": time.time(),
            "context": context or {},
        }
        self.agent_handoffs.append(handoff)


class MultiAgentDynamicSupervisorState(DynamicSupervisorState):
    """Enhanced state combining dynamic supervisor and multi-agent capabilities."""

    # Agent registry management
    agent_registry: AgentRegistryState = Field(
        default_factory=AgentRegistryState, description="Dynamic agent registry state"
    )

    # Multi-agent coordination
    coordination: MultiAgentCoordinationState = Field(
        default_factory=MultiAgentCoordinationState,
        description="Multi-agent coordination state",
    )

    # Dynamic choice model integration
    choice_model_cache: Optional[Dict[str, Any]] = Field(
        default=None, description="Cached choice model configuration"
    )

    # Tool management extensions
    dynamic_tool_routes: Dict[str, str] = Field(
        default_factory=dict, description="Dynamic tool routing configuration"
    )

    tool_usage_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of tool usage across agents"
    )

    # System state flags
    registry_needs_sync: bool = Field(
        default=False, description="Whether agent registry needs synchronization"
    )

    coordination_active: bool = Field(
        default=False, description="Whether multi-agent coordination is active"
    )

    dynamic_routing_enabled: bool = Field(
        default=True, description="Whether dynamic routing is enabled"
    )

    @computed_field
    @property
    def total_registered_agents(self) -> int:
        """Total number of registered agents."""
        return len(self.agent_registry.available_agents)

    @computed_field
    @property
    def total_available_tools(self) -> int:
        """Total number of available tools across all agents."""
        return len(self.agent_registry.tool_to_agent_mapping)

    @computed_field
    @property
    def active_coordination_sessions(self) -> int:
        """Number of active coordination sessions."""
        return len(
            [
                info
                for info in self.coordination.active_executions.values()
                if info.get("status") == "active"
            ]
        )

    def request_agent_addition(
        self,
        agent_name: str,
        agent_type: str,
        capability: str,
        tools: List[str] = None,
        config: Dict[str, Any] = None,
    ) -> str:
        """Request addition of a new agent."""
        request_id = str(uuid4())

        agent_request = {
            "request_id": request_id,
            "agent_name": agent_name,
            "agent_type": agent_type,
            "capability": capability,
            "tools": tools or [],
            "config": config or {},
            "requested_at": time.time(),
        }

        self.agent_registry.pending_agent_additions.append(agent_request)
        self.agent_registry.add_agent_change_request("add", agent_name, agent_request)
        self.registry_needs_sync = True

        return request_id

    def request_agent_removal(self, agent_name: str) -> str:
        """Request removal of an agent."""
        request_id = str(uuid4())

        self.agent_registry.pending_agent_removals.append(agent_name)
        self.agent_registry.add_agent_change_request(
            "remove",
            agent_name,
            {"request_id": request_id, "requested_at": time.time()},
        )
        self.registry_needs_sync = True

        return request_id

    def process_pending_agent_changes(self) -> Dict[str, List[str]]:
        """Process all pending agent additions and removals."""
        results = {"added": [], "removed": [], "failed": []}

        # Process additions
        for request in self.agent_registry.pending_agent_additions:
            try:
                self.agent_registry.add_agent_to_registry(
                    request["agent_name"],
                    request["agent_type"],
                    request["capability"],
                    request.get("tools", []),
                )
                results["added"].append(request["agent_name"])
            except Exception as e:
                results["failed"].append(f"Add {request['agent_name']}: {str(e)}")

        # Process removals
        for agent_name in self.agent_registry.pending_agent_removals:
            try:
                if self.agent_registry.remove_agent_from_registry(agent_name):
                    results["removed"].append(agent_name)
                else:
                    results["failed"].append(f"Remove {agent_name}: not found")
            except Exception as e:
                results["failed"].append(f"Remove {agent_name}: {str(e)}")

        # Clear pending lists
        self.agent_registry.pending_agent_additions.clear()
        self.agent_registry.pending_agent_removals.clear()
        self.registry_needs_sync = False

        return results

    def route_tool_to_agent(self, tool_name: str) -> Optional[str]:
        """Route a tool call to the appropriate agent."""
        agent_name = self.agent_registry.get_agent_for_tool(tool_name)

        if agent_name:
            # Record tool usage
            usage_record = {
                "tool_name": tool_name,
                "agent_name": agent_name,
                "timestamp": time.time(),
                "session_id": self.coordination.coordination_session_id,
            }
            self.tool_usage_history.append(usage_record)

        return agent_name

    def start_coordination_session(self, mode: str = "supervisor") -> str:
        """Start a new multi-agent coordination session."""
        self.coordination.coordination_mode = mode
        self.coordination.coordination_session_id = str(uuid4())
        self.coordination.coordination_start_time = time.time()
        self.coordination_active = True

        return self.coordination.coordination_session_id

    def end_coordination_session(self) -> Dict[str, Any]:
        """End the current coordination session and return summary."""
        session_duration = time.time() - self.coordination.coordination_start_time

        summary = {
            "session_id": self.coordination.coordination_session_id,
            "duration": session_duration,
            "agents_used": list(self.coordination.active_executions.keys()),
            "handoffs": len(self.coordination.agent_handoffs),
            "mode": self.coordination.coordination_mode,
        }

        self.coordination_active = False
        return summary

    def get_coordination_status(self) -> Dict[str, Any]:
        """Get current coordination status."""
        return {
            "active": self.coordination_active,
            "mode": self.coordination.coordination_mode,
            "session_id": self.coordination.coordination_session_id,
            "current_agent": self.coordination.current_active_agent,
            "queue_length": len(self.coordination.execution_queue),
            "active_executions": len(
                [
                    info
                    for info in self.coordination.active_executions.values()
                    if info.get("status") == "active"
                ]
            ),
        }

    def sync_with_choice_model(self, choice_model: DynamicChoiceModel) -> None:
        """Synchronize state with a DynamicChoiceModel."""
        current_options = list(self.agent_registry.available_agents.keys())

        # Update choice model with current agents
        choice_model.options = current_options
        choice_model._regenerate_model()

        # Cache choice model state
        self.choice_model_cache = {
            "options": current_options,
            "version": self.agent_registry.choice_model_version,
            "model_name": choice_model.model_name,
            "synced_at": time.time(),
        }

    def cleanup_old_coordination_data(self, max_history: int = 100) -> None:
        """Clean up old coordination data to prevent memory bloat."""
        # Limit agent handoffs
        if len(self.coordination.agent_handoffs) > max_history:
            self.coordination.agent_handoffs = self.coordination.agent_handoffs[
                -max_history:
            ]

        # Limit tool usage history
        if len(self.tool_usage_history) > max_history:
            self.tool_usage_history = self.tool_usage_history[-max_history:]

        # Limit agent change requests
        if len(self.agent_registry.agent_change_requests) > max_history:
            self.agent_registry.agent_change_requests = (
                self.agent_registry.agent_change_requests[-max_history:]
            )

        # Call parent cleanup
        self.cleanup_old_history(max_history)
