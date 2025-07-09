"""Agent Node V3 - Hierarchical state projection for multi-agent systems.

This module provides AgentNodeV3 which properly handles state projection
between container states (like MultiAgentState) and individual agent states,
maintaining type safety and hierarchical access patterns.
"""

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from langchain_core.messages import BaseMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

if TYPE_CHECKING:
    from haive.agents.base.agent import Agent

logger = logging.getLogger(__name__)

# Type variables for schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class AgentNodeV3Config(BaseNodeConfig[TInput, TOutput]):
    """
    Agent node configuration with hierarchical state projection support.
    
    This node configuration handles:
    - Execution of agents within container states (like MultiAgentState)
    - State projection from container to agent-specific schema
    - Updates back to the container maintaining hierarchy
    - Recompilation tracking for dynamic agent changes
    
    Key improvements over V2:
    - Works with MultiAgentState and similar container patterns
    - Projects state to exact agent schema (no flattening)
    - Maintains type safety throughout execution
    - Supports dynamic agent lookup from state
    """
    
    node_type: NodeType = Field(
        default=NodeType.AGENT,
        description="Node type for agent execution"
    )
    
    # Agent configuration
    agent_name: str = Field(
        description="Name of agent to execute (key in container's agents dict)"
    )
    
    agent: Optional["Agent"] = Field(
        default=None,
        description="Agent instance (extracted from state if not provided)",
        exclude=True
    )
    
    # Container state handling
    extract_from_container: bool = Field(
        default=True,
        description="Whether to extract agent from container state"
    )
    
    agent_state_field: str = Field(
        default="agent_states",
        description="Field in container holding agent states"
    )
    
    agents_field: str = Field(
        default="agents",
        description="Field in container holding agent instances"
    )
    
    # State projection
    project_state: bool = Field(
        default=True,
        description="Whether to project state to agent's expected schema"
    )
    
    shared_fields: List[str] = Field(
        default_factory=lambda: ["messages"],
        description="Fields to share from container to agent"
    )
    
    # Output handling
    output_mode: str = Field(
        default="merge",
        description="How to handle outputs: 'merge', 'replace', or 'isolate'"
    )
    
    update_container_state: bool = Field(
        default=True,
        description="Whether to update the container's agent_states"
    )
    
    # Recompilation tracking
    track_recompilation: bool = Field(
        default=True,
        description="Whether to track agent recompilation needs"
    )
    
    @model_validator(mode="after")
    def validate_agent_config(self) -> "AgentNodeV3Config":
        """Validate configuration."""
        if not self.agent_name and not self.agent:
            raise ValueError("Either agent_name or agent must be provided")
        return self
    
    def get_default_input_fields(self) -> List[FieldDefinition]:
        """Get input fields based on container expectations."""
        fields = []
        
        # Always need messages
        fields.append(StandardFields.messages(use_enhanced=True))
        
        # Need agent states field
        fields.append(
            FieldDefinition(
                name=self.agent_state_field,
                field_type=Dict[str, Dict[str, Any]],
                default_factory=dict,
                description="Agent states container"
            )
        )
        
        # Need agents field if extracting
        if self.extract_from_container:
            fields.append(
                FieldDefinition(
                    name=self.agents_field,
                    field_type=Dict[str, "Agent"],
                    default_factory=dict,
                    description="Agent instances"
                )
            )
        
        return fields
    
    def get_default_output_fields(self) -> List[FieldDefinition]:
        """Get output fields."""
        fields = []
        
        # Messages are always output
        fields.append(StandardFields.messages(use_enhanced=True))
        
        # Agent states if updating container
        if self.update_container_state:
            fields.append(
                FieldDefinition(
                    name=self.agent_state_field,
                    field_type=Dict[str, Dict[str, Any]],
                    default_factory=dict,
                    description="Updated agent states"
                )
            )
        
        # Agent outputs
        fields.append(
            FieldDefinition(
                name="agent_outputs",
                field_type=Dict[str, Any],
                default_factory=dict,
                description="Agent execution outputs"
            )
        )
        
        return fields
    
    def __call__(
        self,
        state: StateLike,
        config: Optional[ConfigLike] = None
    ) -> Command:
        """Execute agent with hierarchical state projection."""
        logger.info(f"{'='*60}")
        logger.info(f"AGENT NODE V3: {self.name}")
        logger.info(f"Agent: {self.agent_name}")
        logger.info(f"{'='*60}")
        
        try:
            # Get agent instance
            agent = self._get_agent(state)
            if not agent:
                raise ValueError(f"Agent '{self.agent_name}' not found")
            
            # Set active agent if container supports it
            self._set_active_agent(state)
            
            # Project state for agent
            agent_input = self._project_state_for_agent(state, agent)
            
            logger.info(f"Executing agent with {len(agent_input)} fields")
            logger.debug(f"Fields: {list(agent_input.keys())}")
            
            # Execute agent
            if hasattr(agent, "_app") and agent._app:
                logger.debug("Using agent's compiled graph")
                result = agent._app.invoke(agent_input, config)
            else:
                logger.debug("Using agent's invoke method")
                result = agent.invoke(agent_input, config)
            
            # Process output
            state_update = self._process_agent_output(result, state, agent)
            
            # Track recompilation if needed
            if self.track_recompilation:
                self._check_recompilation(state, agent)
            
            logger.info(f"✅ Agent completed with {len(state_update)} field updates")
            
            return Command(update=state_update, goto=self._get_goto_node())
            
        except Exception as e:
            logger.error(f"❌ Agent execution failed: {e}")
            
            # Record error
            error_update = {
                "agent_outputs": {
                    self.agent_name: {
                        "error": str(e),
                        "error_type": type(e).__name__
                    }
                }
            }
            
            # Preserve existing outputs
            if hasattr(state, "agent_outputs"):
                current_outputs = getattr(state, "agent_outputs", {})
                error_update["agent_outputs"] = {**current_outputs, **error_update["agent_outputs"]}
            
            return Command(update=error_update, goto=self._get_goto_node())
    
    def _get_agent(self, state: StateLike) -> Optional["Agent"]:
        """Get agent from state or use provided agent."""
        if self.agent:
            return self.agent
        
        if self.extract_from_container:
            # Extract from container state
            agents = getattr(state, self.agents_field, {})
            if isinstance(agents, dict):
                return agents.get(self.agent_name)
        
        return None
    
    def _set_active_agent(self, state: StateLike) -> None:
        """Set active agent if container supports it."""
        if hasattr(state, "set_active_agent"):
            state.set_active_agent(self.agent_name)
        elif hasattr(state, "active_agent"):
            state.active_agent = self.agent_name
    
    def _project_state_for_agent(
        self,
        state: StateLike,
        agent: "Agent"
    ) -> Dict[str, Any]:
        """Project container state to agent's expected schema.
        
        This is the key method that enables hierarchical state management.
        Each agent gets exactly what it expects, not a flattened global state.
        """
        # Start with agent's isolated state
        agent_states = getattr(state, self.agent_state_field, {})
        agent_state = agent_states.get(self.agent_name, {})
        projected = agent_state.copy()
        
        if not self.project_state:
            return projected
        
        # Add shared fields from container
        for field in self.shared_fields:
            if hasattr(state, field) and field not in projected:
                value = getattr(state, field)
                # Special handling for messages
                if field == "messages":
                    value = self._extract_message_objects(value)
                projected[field] = value
        
        # Project to agent's expected schema if available
        if hasattr(agent, "state_schema") and agent.state_schema:
            expected_schema = agent.state_schema
            
            # Add fields from schema with defaults
            for field_name, field_info in expected_schema.model_fields.items():
                if field_name not in projected:
                    # Check if it's a shared field in the schema
                    schema_shared = getattr(expected_schema, "__shared_fields__", set())
                    if field_name in schema_shared and hasattr(state, field_name):
                        projected[field_name] = getattr(state, field_name)
                    elif field_info.default is not None:
                        projected[field_name] = field_info.default
                    elif field_info.default_factory:
                        projected[field_name] = field_info.default_factory()
            
            # Validate against schema
            try:
                validated = expected_schema(**projected)
                # Return dict but preserve message objects
                messages = projected.get("messages")
                projected = validated.model_dump()
                if messages is not None:
                    projected["messages"] = messages
            except Exception as e:
                logger.warning(f"Schema validation failed, using raw projection: {e}")
        
        return projected
    
    def _extract_message_objects(self, messages: Any) -> List[BaseMessage]:
        """Extract BaseMessage objects from various containers."""
        if hasattr(messages, "root"):
            return messages.root
        elif isinstance(messages, (list, tuple)):
            return list(messages)
        else:
            try:
                return list(messages)
            except:
                logger.warning(f"Cannot extract messages from {type(messages)}")
                return []
    
    def _process_agent_output(
        self,
        result: Any,
        state: StateLike,
        agent: "Agent"
    ) -> Dict[str, Any]:
        """Process agent output and prepare state update."""
        state_update = {}
        
        # Convert result to dict
        if isinstance(result, dict):
            result_dict = result
        elif isinstance(result, BaseModel):
            # Preserve messages
            messages = getattr(result, "messages", None)
            result_dict = result.model_dump()
            if messages is not None:
                result_dict["messages"] = messages
        else:
            result_dict = {"result": result}
        
        # Update agent's isolated state
        if self.update_container_state:
            agent_states = getattr(state, self.agent_state_field, {})
            current_agent_state = agent_states.get(self.agent_name, {})
            
            if self.output_mode == "merge":
                updated_state = {**current_agent_state, **result_dict}
            elif self.output_mode == "replace":
                updated_state = result_dict
            else:  # isolate
                updated_state = current_agent_state
            
            state_update[self.agent_state_field] = {
                **agent_states,
                self.agent_name: updated_state
            }
        
        # Update agent outputs
        current_outputs = getattr(state, "agent_outputs", {})
        state_update["agent_outputs"] = {
            **current_outputs,
            self.agent_name: result_dict
        }
        
        # Update shared fields
        if hasattr(agent, "state_schema"):
            schema_shared = getattr(agent.state_schema, "__shared_fields__", set())
            for field in schema_shared:
                if field in result_dict:
                    state_update[field] = result_dict[field]
        
        # Always update messages if present
        if "messages" in result_dict:
            state_update["messages"] = result_dict["messages"]
        
        return state_update
    
    def _check_recompilation(self, state: StateLike, agent: "Agent") -> None:
        """Check and track recompilation needs."""
        if hasattr(agent, "graph") and hasattr(agent.graph, "needs_recompile"):
            if agent.graph.needs_recompile():
                # Mark for recompilation
                if hasattr(state, "mark_agent_for_recompile"):
                    state.mark_agent_for_recompile(self.agent_name, "Graph needs recompilation")
                elif hasattr(state, "agents_needing_recompile"):
                    state.agents_needing_recompile.add(self.agent_name)
    
    def _get_goto_node(self) -> Optional[str]:
        """Get next node to execute."""
        return self.command_goto


# ============================================================================
# CONVENIENCE FACTORY FUNCTION
# ============================================================================


def create_agent_node_v3(
    agent_name: str,
    agent: Optional["Agent"] = None,
    name: Optional[str] = None,
    **kwargs
) -> AgentNodeV3Config:
    """Create an agent node V3 configuration.
    
    Args:
        agent_name: Name of agent to execute (key in container)
        agent: Optional agent instance (extracted from state if not provided)
        name: Optional node name
        **kwargs: Additional configuration options
        
    Returns:
        AgentNodeV3Config instance
    """
    if not name:
        name = f"agent_{agent_name}"
    
    return AgentNodeV3Config(
        name=name,
        agent_name=agent_name,
        agent=agent,
        **kwargs
    )