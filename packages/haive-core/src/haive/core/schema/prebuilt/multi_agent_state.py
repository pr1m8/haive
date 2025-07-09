"""Multi-agent state with hierarchical agent management and recompilation support.

This module provides a state schema for managing multiple agents without schema
flattening, maintaining hierarchical access with proper typing for the graph API.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union
from pydantic import Field, field_validator, model_validator, computed_field

from haive.core.schema.prebuilt.tool_state import ToolState

if TYPE_CHECKING:
    from haive.agents.base import Agent


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
    agents: Union[List["Agent"], Dict[str, "Agent"]] = Field(
        default_factory=dict,
        description="Agent instances contained in this state (not flattened)"
    )
    
    # Hierarchical state management - each agent has isolated state
    agent_states: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Isolated state for each agent, preserving their schemas"
    )
    
    # ========================================================================
    # EXECUTION TRACKING
    # ========================================================================
    
    active_agent: Optional[str] = Field(
        default=None,
        description="Currently executing agent name"
    )
    
    agent_outputs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Outputs from each agent execution"
    )
    
    agent_execution_order: List[str] = Field(
        default_factory=list,
        description="Order of agent execution for sequential coordination"
    )
    
    # ========================================================================
    # RECOMPILATION SUPPORT
    # ========================================================================
    
    agents_needing_recompile: Set[str] = Field(
        default_factory=set,
        description="Agent names that need graph recompilation"
    )
    
    recompile_count: int = Field(
        default=0,
        description="Total number of recompilations performed"
    )
    
    recompile_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of recompilation events"
    )
    
    # ========================================================================
    # VALIDATORS
    # ========================================================================
    
    @field_validator("agents", mode="before")
    @classmethod
    def convert_agents_to_dict(cls, v: Union[List["Agent"], Dict[str, "Agent"]]) -> Dict[str, "Agent"]:
        """Convert list of agents to dict keyed by agent name.
        
        This allows flexible initialization while maintaining consistent
        internal representation for hierarchical access.
        """
        if isinstance(v, list):
            # Convert list to dict using agent names
            agent_dict = {}
            for agent in v:
                if not hasattr(agent, 'name'):
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
                        # Namespace: agent_name.engine_name
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
    
    def get_agent_state(self, agent_name: str) -> Dict[str, Any]:
        """Get isolated state for a specific agent.
        
        Args:
            agent_name: Name of the agent
            
        Returns:
            Agent's isolated state dictionary
        """
        return self.agent_states.get(agent_name, {})
    
    def update_agent_state(self, agent_name: str, updates: Dict[str, Any]) -> None:
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
    
    def mark_agent_for_recompile(self, agent_name: str, reason: Optional[str] = None) -> None:
        """Mark an agent as needing recompilation.
        
        Args:
            agent_name: Name of the agent
            reason: Optional reason for recompilation
        """
        self.agents_needing_recompile.add(agent_name)
        
        # Add to history
        self.recompile_history.append({
            "agent_name": agent_name,
            "reason": reason or "Manual recompilation request",
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "resolved": False
        })
    
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
    
    def get_agents_needing_recompile(self) -> Set[str]:
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