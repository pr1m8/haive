# ============================================================================
# AGENT NODE CONFIG V2 - WITH SCHEMA SUPPORT
# ============================================================================

import logging
from typing import Any, Dict, List, Literal, Optional, Type, TypeVar, Union

from haive.agents.base.agent import Agent
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

logger = logging.getLogger(__name__)
console = Console()

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class AgentNodeConfig(BaseNodeConfig[TInput, TOutput]):
    """Schema-aware node configuration for agents in multi-agent systems.

    This node properly handles:
    - Agent execution with type-safe state management
    - Schema transformation between global and agent-specific schemas
    - Private state isolation
    - Message preservation and proper routing

    Input Schema Requirements:
    - Must have 'messages' field (List[BaseMessage])
    - May have agent-specific fields based on agent's requirements

    Output Schema:
    - Updated messages
    - Agent-specific outputs
    - Optional metadata updates
    """

    node_type: NodeType = Field(
        default=NodeType.AGENT, description="Node type for agents"
    )

    # The agent to execute
    agent: Agent = Field(description="The agent to execute")

    # Schema handling
    agent_state_schema: type[BaseModel] | None = Field(
        default=None,
        description="Agent's expected state schema (if different from global)",
        exclude=True,
    )

    # Field mapping
    shared_fields: list[str] = Field(
        default_factory=lambda: ["messages"],
        description="Fields to share between global and agent state",
    )

    agent_fields: dict[str, str] | None = Field(
        default=None, description="Mapping of global_field -> agent_field names"
    )

    # Output handling
    output_field: str | None = Field(
        default=None, description="Field to store agent's primary output"
    )

    preserve_messages: bool = Field(
        default=True, description="Whether to preserve message objects (not serialize)"
    )

    # Metadata tracking
    track_execution: bool = Field(
        default=True, description="Whether to track execution in metadata"
    )

    metadata_field: str = Field(
        default="agent_metadata", description="Field to store execution metadata"
    )

    @model_validator(mode="after")
    def validate_agent_schema(self) -> "AgentNodeConfig":
        """Extract agent's state schema if not provided."""
        if not self.agent_state_schema and hasattr(self.agent, "state_schema"):
            self.agent_state_schema = self.agent.state_schema
        return self

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get input fields based on agent's requirements."""
        fields = []

        # Always need messages
        fields.append(StandardFields.messages(use_enhanced=True))

        # Add agent-specific fields if we know the schema
        if self.agent_state_schema:
            for field_name, field_info in self.agent_state_schema.model_fields.items():
                if field_name not in ["messages"]:  # Avoid duplicates
                    fields.append(
                        FieldDefinition(
                            name=field_name,
                            field_type=field_info.annotation,
                            default=field_info.default,
                            description=field_info.description
                            or f"Agent field: {field_name}",
                            source=f"agent:{self.agent.name}",
                        )
                    )

        return fields

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get output fields based on agent's outputs."""
        fields = []

        # Messages are always output
        fields.append(StandardFields.messages(use_enhanced=True))

        # Add output field if specified
        if self.output_field:
            fields.append(
                FieldDefinition(
                    name=self.output_field,
                    field_type=Optional[Any],
                    default=None,
                    description=f"Output from agent {self.agent.name}",
                )
            )

        # Add metadata field
        fields.append(
            FieldDefinition(
                name=self.metadata_field,
                field_type=Optional[dict[str, Any]],
                default=None,
                description="Agent execution metadata",
            )
        )

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute the agent with proper state management."""
        logger.info(f"{'='*60}")
        logger.info(f"AGENT NODE V2: {self.name}")
        logger.info(f"Agent: {self.agent.name}")
        logger.info(f"{'='*60}")

        try:
            # Extract state for agent
            agent_input = self._prepare_agent_input(state)

            # Track execution start
            metadata = self._track_start(state) if self.track_execution else {}

            # Execute agent
            logger.info(f"Executing agent with {len(agent_input)} fields")

            # Check if agent has compiled graph
            if hasattr(self.agent, "_app") and self.agent._app:
                logger.debug("Using agent's compiled graph")
                result = self.agent._app.invoke(agent_input, config)
            else:
                logger.debug("Using agent's invoke method")
                result = self.agent.invoke(agent_input, config)

            # Process output
            state_update = self._process_agent_output(result, state)

            # Track execution end
            if self.track_execution:
                metadata = self._track_end(metadata, result)
                state_update[self.metadata_field] = metadata

            logger.info(f"✅ Agent completed with {len(state_update)} field updates")

            return Command(update=state_update, goto=self._get_goto_node())

        except Exception as e:
            logger.exception(f"❌ Agent execution failed: {e}")

            # Track error
            if self.track_execution:
                metadata = self._track_error(e)
                return Command(
                    update={self.metadata_field: metadata}, goto=self._get_goto_node()
                )

            raise

    def _prepare_agent_input(self, state: StateLike) -> dict[str, Any]:
        """Prepare input for agent based on schema requirements."""
        agent_input = {}

        # If agent has specific schema, extract those fields
        if self.agent_state_schema:
            logger.debug(
                f"Using agent's state schema: {self.agent_state_schema.__name__}"
            )

            # Extract fields that exist in both state and agent schema
            for field_name, _field_info in self.agent_state_schema.model_fields.items():
                # Check field mapping
                source_field = field_name
                if self.agent_fields and field_name in self.agent_fields:
                    source_field = self.agent_fields[field_name]

                # Extract from state
                if hasattr(state, source_field):
                    value = getattr(state, source_field)

                    # Special handling for messages to preserve objects
                    if field_name == "messages" and self.preserve_messages:
                        value = self._extract_message_objects(value)

                    agent_input[field_name] = value
                    logger.debug(
                        f"Extracted field '{field_name}' from '{source_field}'"
                    )
                elif hasattr(state, "get") and state.get(source_field) is not None:
                    agent_input[field_name] = state.get(source_field)
                    logger.debug(f"Extracted field '{field_name}' from state dict")

        else:
            # No specific schema - extract shared fields
            logger.debug("No agent schema - extracting shared fields")

            for field in self.shared_fields:
                if hasattr(state, field):
                    value = getattr(state, field)

                    # Special handling for messages
                    if field == "messages" and self.preserve_messages:
                        value = self._extract_message_objects(value)

                    agent_input[field] = value
                elif hasattr(state, "get"):
                    agent_input[field] = state.get(field)

        # Convert to dict if it's a Pydantic model
        if isinstance(agent_input, BaseModel):
            # But preserve message objects
            messages = (
                agent_input.messages if hasattr(agent_input, "messages") else None
            )
            agent_input = agent_input.model_dump()
            if messages and self.preserve_messages:
                agent_input["messages"] = messages

        return agent_input

    def _extract_message_objects(self, messages: Any) -> list[BaseMessage]:
        """Extract actual BaseMessage objects from various containers."""
        if hasattr(messages, "root"):
            # MessageList with root attribute
            return messages.root
        if isinstance(messages, list | tuple):
            # Already a list
            return list(messages)
        # Try to iterate
        try:
            return list(messages)
        except:
            logger.warning(f"Cannot extract messages from {type(messages)}")
            return []

    def _process_agent_output(self, result: Any, state: StateLike) -> dict[str, Any]:
        """Process agent output and prepare state update."""
        state_update = {}

        # Handle different result types
        if isinstance(result, dict):
            state_update = result.copy()
        elif isinstance(result, BaseModel):
            # Preserve message objects if present
            if hasattr(result, "messages") and self.preserve_messages:
                messages = result.messages
                state_update = result.model_dump()
                state_update["messages"] = messages
            else:
                state_update = result.model_dump()
        elif isinstance(result, str) and self.output_field:
            state_update[self.output_field] = result
        elif result is not None:
            # Store in output field or default location
            field = self.output_field or f"{self.agent.name}_output"
            state_update[field] = result

        # Ensure messages are preserved correctly
        if "messages" in state_update and self.preserve_messages:
            messages = state_update["messages"]
            if not all(isinstance(m, BaseMessage) for m in messages):
                logger.warning("Some messages are not BaseMessage objects")

        return state_update

    def _track_start(self, state: StateLike) -> dict[str, Any]:
        """Track agent execution start."""
        return {
            "agent_name": self.agent.name,
            "start_time": logger.time(),
            "input_message_count": len(self._get_messages_from_state(state)),
        }

    def _track_end(self, metadata: dict[str, Any], result: Any) -> dict[str, Any]:
        """Track agent execution end."""
        metadata["end_time"] = logger.time()
        metadata["duration_ms"] = metadata["end_time"] - metadata["start_time"]

        # Track output stats
        if isinstance(result, dict) and "messages" in result:
            metadata["output_message_count"] = len(result["messages"])

        metadata["status"] = "completed"
        return metadata

    def _track_error(self, error: Exception) -> dict[str, Any]:
        """Track agent execution error."""
        return {
            "agent_name": self.agent.name,
            "status": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
        }

    def _get_messages_from_state(self, state: StateLike) -> list[BaseMessage]:
        """Extract messages from state."""
        if hasattr(state, "messages"):
            return self._extract_message_objects(state.messages)
        if hasattr(state, "get"):
            messages = state.get("messages", [])
            return self._extract_message_objects(messages)
        return []

    def _get_goto_node(self) -> str:
        """Get the node to go to after agent execution."""
        return self.command_goto or "coordinator"


# ============================================================================
# COORDINATOR NODE CONFIG
# ============================================================================


class CoordinatorNodeConfig(BaseNodeConfig[TInput, TOutput]):
    """Coordinator node for managing multi-agent execution patterns.

    Handles:
    - Fan-out for parallel execution
    - Result aggregation
    - Agent sequencing
    - Execution tracking
    """

    node_type: NodeType = Field(
        default=NodeType.COORDINATOR, description="Coordinator node type"
    )

    agents: list[Agent] = Field(description="Agents to coordinate")

    mode: Literal["fanout", "aggregate", "sequence"] = Field(
        description="Coordination mode"
    )

    # Aggregation settings
    aggregation_field: str = Field(
        default="agent_results", description="Field to store aggregated results"
    )

    preserve_individual: bool = Field(
        default=True, description="Whether to preserve individual agent outputs"
    )

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Coordinator needs messages and potentially agent results."""
        fields = [StandardFields.messages(use_enhanced=True)]

        if self.mode == "aggregate":
            fields.append(
                FieldDefinition(
                    name=self.aggregation_field,
                    field_type=Optional[dict[str, Any]],
                    default_factory=dict,
                    description="Individual agent results to aggregate",
                )
            )

        return fields

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Coordinator outputs depend on mode."""
        fields = [StandardFields.messages(use_enhanced=True)]

        if self.mode == "aggregate":
            fields.append(
                FieldDefinition(
                    name="aggregated_result",
                    field_type=Optional[Any],
                    default=None,
                    description="Aggregated result from all agents",
                )
            )

        return fields

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute coordination logic."""
        if self.mode == "fanout":
            return self._handle_fanout(state, config)
        if self.mode == "aggregate":
            return self._handle_aggregate(state, config)
        if self.mode == "sequence":
            return self._handle_sequence(state, config)
        raise ValueError(f"Unknown coordination mode: {self.mode}")

    def _handle_fanout(self, state: StateLike, config: ConfigLike | None) -> Command:
        """Prepare for parallel agent execution."""
        logger.info(f"Fanning out to {len(self.agents)} agents")

        # Just mark ready for parallel execution
        # The graph structure handles the actual parallel routing
        return Command(
            update={"coordination_stage": "fanout"}, goto=self._get_goto_node()
        )

    def _handle_aggregate(self, state: StateLike, config: ConfigLike | None) -> Command:
        """Aggregate results from parallel agents."""
        logger.info("Aggregating agent results")

        # Get individual results
        if hasattr(state, self.aggregation_field):
            results = getattr(state, self.aggregation_field)
        else:
            results = (
                state.get(self.aggregation_field, {}) if hasattr(state, "get") else {}
            )

        # Perform aggregation based on result types
        aggregated = self._aggregate_results(results)

        return Command(
            update={
                "aggregated_result": aggregated,
                "coordination_stage": "aggregated",
            },
            goto=self._get_goto_node(),
        )

    def _handle_sequence(self, state: StateLike, config: ConfigLike | None) -> Command:
        """Handle sequential agent execution tracking."""
        # This is more of a tracking node - actual sequencing is in graph structure
        current_index = state.get("agent_index", 0) if hasattr(state, "get") else 0

        return Command(
            update={"agent_index": current_index + 1, "coordination_stage": "sequence"},
            goto=self._get_goto_node(),
        )

    def _aggregate_results(self, results: dict[str, Any]) -> Any:
        """Aggregate results from multiple agents."""
        if not results:
            return None

        # If all results are dicts, merge them
        if all(isinstance(r, dict) for r in results.values()):
            aggregated = {}
            for agent_name, result in results.items():
                if self.preserve_individual:
                    aggregated[agent_name] = result
                else:
                    aggregated.update(result)
            return aggregated

        # If all results are lists, concatenate
        if all(isinstance(r, list) for r in results.values()):
            aggregated = []
            for result in results.values():
                aggregated.extend(result)
            return aggregated

        # Mixed types - preserve structure
        return results

    def _get_goto_node(self) -> str:
        """Get next node based on coordination mode."""
        if self.mode == "fanout":
            # Go to first agent or parallel split
            return self.command_goto or "parallel_split"
        if self.mode == "aggregate":
            # Continue to next stage
            return self.command_goto or "next"
        return self.command_goto or "next"


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_agent_node(
    agent: Agent,
    name: str | None = None,
    shared_fields: list[str] | None = None,
    **kwargs,
) -> AgentNodeConfig:
    """Create an agent node configuration."""
    if not name:
        name = f"agent_{agent.name}"

    return AgentNodeConfig(
        name=name, agent=agent, shared_fields=shared_fields or ["messages"], **kwargs
    )


def create_coordinator_node(
    agents: list[Agent],
    mode: Literal["fanout", "aggregate", "sequence"],
    name: str | None = None,
    **kwargs,
) -> CoordinatorNodeConfig:
    """Create a coordinator node configuration."""
    if not name:
        name = f"coordinator_{mode}"

    return CoordinatorNodeConfig(name=name, agents=agents, mode=mode, **kwargs)
