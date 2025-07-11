"""
Base state schemas with clear inheritance hierarchy.

This module provides a cleaner inheritance structure for state schemas,
separating concerns between different types of agents and workflows.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, PrivateAttr

if TYPE_CHECKING:
    from haive.core.engine.base import Engine
    from haive.core.graph import BaseGraph


# ============================================================================
# BASE STATE SCHEMAS
# ============================================================================


class MinimalState(BaseModel):
    """
    Absolute minimal state - just data, no engines or agents.

    Use this for simple data transformations, validations, or workflows
    that don't need LLM or other engine capabilities.
    """

    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Metadata for tracking and debugging"
    )

    class Config:
        arbitrary_types_allowed = True


class MessagingState(MinimalState):
    """
    State that includes message handling.

    For workflows that need conversation/message tracking but not
    necessarily LLM capabilities (e.g., routing, logging, monitoring).
    """

    messages: List[BaseMessage] = Field(
        default_factory=list, description="Message history"
    )

    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the conversation."""
        self.messages.append(message)

    def get_last_message(self) -> Optional[BaseMessage]:
        """Get the most recent message."""
        return self.messages[-1] if self.messages else None


class EngineState(MessagingState):
    """
    State that can hold engines (serializable components).

    This is the base for states that need engines but aren't
    necessarily "agents" in the LLM sense.
    """

    engines: Dict[str, Union["Engine", Dict[str, Any]]] = Field(
        default_factory=dict, description="Registry of engines (serializable)"
    )

    # Track which engines are currently active/loaded
    _loaded_engines: Dict[str, "Engine"] = PrivateAttr(default_factory=dict)

    def register_engine(
        self, name: str, engine: Union["Engine", Dict[str, Any]]
    ) -> None:
        """Register an engine (can be serialized dict or instance)."""
        self.engines[name] = engine

        # If it's an actual engine instance, track it
        if not isinstance(engine, dict):
            self._loaded_engines[name] = engine

    def get_engine(self, name: str) -> Optional["Engine"]:
        """Get an engine, deserializing if needed."""
        if name in self._loaded_engines:
            return self._loaded_engines[name]

        engine_data = self.engines.get(name)
        if engine_data is None:
            return None

        # If it's already an engine, return it
        if not isinstance(engine_data, dict):
            self._loaded_engines[name] = engine_data
            return engine_data

        # TODO: Deserialize engine from dict
        # This would use engine registry/factory pattern
        return None

    def serialize_engines(self) -> None:
        """Ensure all engines are in serialized form."""
        for name, engine in self._loaded_engines.items():
            if hasattr(engine, "model_dump"):
                self.engines[name] = engine.model_dump()


class ToolState(EngineState):
    """
    State that includes tool management.

    For workflows that use tools but might not have a primary LLM
    (e.g., pure tool orchestration, data processing pipelines).
    """

    tools: List[Any] = Field(default_factory=list, description="Available tools")

    tool_routes: Dict[str, str] = Field(
        default_factory=dict, description="Tool routing configuration"
    )

    tool_results: Dict[str, Any] = Field(
        default_factory=dict, description="Results from tool executions"
    )


# ============================================================================
# AGENT STATE SCHEMAS
# ============================================================================


class AgentState(ToolState):
    """
    State for a single agent with a primary engine (usually LLM).

    This is the base for traditional agents that have a main
    decision-making engine.
    """

    # Primary engine (for backward compatibility and convenience)
    engine: Optional[Union["Engine", Dict[str, Any]]] = Field(
        default=None, description="Primary/main engine for this agent"
    )

    # Agent configuration
    agent_name: str = Field(default="agent", description="Name of this agent")

    agent_type: str = Field(
        default="base",
        description="Type of agent (llm, retriever, tool_executor, etc.)",
    )

    @property
    def primary_engine(self) -> Optional["Engine"]:
        """Get the primary engine."""
        if self.engine is not None:
            if isinstance(self.engine, dict):
                # TODO: Deserialize
                return None
            return self.engine

        # Try to find a main/primary engine in engines dict
        for name in ["main", "primary", self.agent_type]:
            engine = self.get_engine(name)
            if engine:
                return engine

        # Return first available engine
        if self.engines:
            return self.get_engine(next(iter(self.engines)))

        return None


class WorkflowState(AgentState):
    """
    State for workflow agents that can modify their own execution graph.

    This enables meta-programming where agents can inspect and modify
    their own workflow based on results.
    """

    # The workflow graph (serializable)
    graph: Optional[Dict[str, Any]] = Field(
        default=None, description="Serialized workflow graph"
    )

    # Execution state
    current_node: Optional[str] = Field(
        default=None, description="Current node in execution"
    )

    execution_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of node executions"
    )

    # Graph modification flags
    graph_modified: bool = Field(
        default=False, description="Whether graph has been modified"
    )

    _compiled_graph: Optional["BaseGraph"] = PrivateAttr(default=None)

    def modify_graph(self, modifications: Dict[str, Any]) -> None:
        """Apply modifications to the workflow graph."""
        if self.graph is None:
            self.graph = {}

        # Apply modifications
        self.graph.update(modifications)
        self.graph_modified = True
        self._compiled_graph = None  # Invalidate compiled version

    def get_compiled_graph(self) -> Optional["BaseGraph"]:
        """Get compiled graph, recompiling if needed."""
        if self._compiled_graph is None and self.graph:
            # TODO: Compile from serialized graph
            pass
        return self._compiled_graph


class MetaAgentState(WorkflowState):
    """
    State for meta-agents that can spawn and manage other agents.

    This is for advanced scenarios where agents create and coordinate
    other agents dynamically.
    """

    # Sub-agents managed by this meta-agent
    sub_agents: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Serialized sub-agent states"
    )

    # Sub-agent results
    sub_agent_results: Dict[str, Any] = Field(
        default_factory=dict, description="Results from sub-agent executions"
    )

    # Coordination state
    coordination_strategy: str = Field(
        default="sequential",
        description="How to coordinate sub-agents (sequential, parallel, dynamic)",
    )

    active_sub_agents: List[str] = Field(
        default_factory=list, description="Currently active sub-agents"
    )

    def spawn_sub_agent(
        self, name: str, agent_type: str, initial_state: Optional[Dict[str, Any]] = None
    ) -> None:
        """Spawn a new sub-agent."""
        self.sub_agents[name] = {
            "agent_type": agent_type,
            "state": initial_state or {},
            "status": "created",
        }

    def update_sub_agent_result(self, name: str, result: Any) -> None:
        """Update results from a sub-agent."""
        self.sub_agent_results[name] = result
        if name in self.sub_agents:
            self.sub_agents[name]["status"] = "completed"


# ============================================================================
# MULTI-AGENT STATE SCHEMAS
# ============================================================================


class MultiAgentState(MessagingState):
    """
    State for multi-agent systems with proper isolation.

    This provides a clean separation between shared state and
    per-agent private state.
    """

    # Shared state accessible by all agents
    shared_context: Dict[str, Any] = Field(
        default_factory=dict, description="Context shared across all agents"
    )

    # Per-agent states (isolated)
    agent_states: Dict[str, AgentState] = Field(
        default_factory=dict, description="Isolated state for each agent"
    )

    # Routing and coordination
    routing: Dict[str, Any] = Field(
        default_factory=dict, description="Routing and coordination info"
    )

    def get_agent_state(self, agent_name: str) -> AgentState:
        """Get or create state for an agent."""
        if agent_name not in self.agent_states:
            self.agent_states[agent_name] = AgentState(agent_name=agent_name)
        return self.agent_states[agent_name]

    def broadcast_to_agents(self, data: Dict[str, Any]) -> None:
        """Broadcast data to all agents via shared context."""
        self.shared_context.update(data)

    def collect_agent_results(self) -> Dict[str, Any]:
        """Collect results from all agents."""
        results = {}
        for name, state in self.agent_states.items():
            if hasattr(state, "tool_results"):
                results[name] = state.tool_results
        return results


class HierarchicalAgentState(MultiAgentState):
    """
    State for hierarchical agent systems (parent-child relationships).
    """

    # Parent agent reference
    parent_agent: Optional[str] = Field(
        default=None, description="Name of parent agent"
    )

    # Child agents
    child_agents: List[str] = Field(
        default_factory=list, description="Names of child agents"
    )

    # Aggregation strategy
    aggregation_strategy: str = Field(
        default="merge",
        description="How to aggregate child results (merge, select_best, vote, etc.)",
    )

    def add_child_agent(self, agent_name: str) -> None:
        """Add a child agent."""
        if agent_name not in self.child_agents:
            self.child_agents.append(agent_name)
            self.get_agent_state(agent_name)  # Ensure state exists

    def aggregate_child_results(self) -> Dict[str, Any]:
        """Aggregate results from child agents based on strategy."""
        child_results = {
            name: self.agent_states[name].tool_results
            for name in self.child_agents
            if name in self.agent_states
        }

        if self.aggregation_strategy == "merge":
            # Simple merge
            aggregated = {}
            for results in child_results.values():
                aggregated.update(results)
            return aggregated
        elif self.aggregation_strategy == "select_best":
            # TODO: Implement selection logic
            return (
                child_results.get(self.child_agents[0], {}) if self.child_agents else {}
            )
        else:
            return child_results


# ============================================================================
# SPECIALIZED STATES
# ============================================================================


class ToolExecutorState(ToolState):
    """
    Specialized state for pure tool execution workflows.

    No LLM needed - just tool orchestration based on rules or configs.
    """

    execution_plan: List[Dict[str, Any]] = Field(
        default_factory=list, description="Plan for tool execution"
    )

    current_step: int = Field(default=0, description="Current step in execution plan")

    def add_execution_step(self, tool_name: str, inputs: Dict[str, Any]) -> None:
        """Add a step to the execution plan."""
        self.execution_plan.append(
            {"tool": tool_name, "inputs": inputs, "status": "pending"}
        )

    def mark_step_complete(self, result: Any) -> None:
        """Mark current step as complete with result."""
        if self.current_step < len(self.execution_plan):
            self.execution_plan[self.current_step]["status"] = "complete"
            self.execution_plan[self.current_step]["result"] = result
            self.current_step += 1


class DataProcessingState(EngineState):
    """
    State for data processing workflows.

    Focuses on data transformation engines rather than LLMs.
    """

    input_data: Any = Field(default=None, description="Input data to process")

    processed_data: Any = Field(default=None, description="Processed output data")

    processing_stages: List[str] = Field(
        default_factory=list, description="Stages of processing to apply"
    )

    stage_results: Dict[str, Any] = Field(
        default_factory=dict, description="Results from each processing stage"
    )


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_agent_state(
    agent_type: str, with_workflow: bool = False, with_meta: bool = False
) -> Type[AgentState]:
    """
    Factory to create appropriate agent state class.

    Args:
        agent_type: Type of agent (llm, tool_executor, data_processor, etc.)
        with_workflow: Whether agent can modify its workflow
        with_meta: Whether agent can spawn sub-agents

    Returns:
        Appropriate state class
    """
    if with_meta:
        return MetaAgentState
    elif with_workflow:
        return WorkflowState
    elif agent_type == "tool_executor":
        return ToolExecutorState
    elif agent_type == "data_processor":
        return DataProcessingState
    else:
        return AgentState


def create_multi_agent_state(hierarchical: bool = False) -> Type[MultiAgentState]:
    """
    Factory to create appropriate multi-agent state class.

    Args:
        hierarchical: Whether agents have parent-child relationships

    Returns:
        Appropriate state class
    """
    if hierarchical:
        return HierarchicalAgentState
    else:
        return MultiAgentState
