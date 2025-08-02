"""Meta state schema with embedded agent and graph composition support.

This module provides MetaStateSchema, a specialized state schema for graph-level
agent composition and recompilation management. It focuses on agent lifecycle,
graph coordination, and dynamic recompilation rather than tool routing.

The meta state pattern enables:
- Agent embedding within graph states
- Graph composition and coordination
- Recompilation tracking and management
- Agent lifecycle management
- Dynamic agent modification

Example:
    ```python
    from haive.core.schema.prebuilt.meta_state import MetaStateSchema
    from haive.agents.simple.agent import SimpleAgent

    # Create a contained agent
    inner_agent = SimpleAgent()

    # Create meta state with embedded agent
    meta_state = MetaStateSchema(
        agent=inner_agent,
        agent_state={"initialized": True},
        graph_context={"composition": "nested"}
    )

    # Agent can be executed and recompiled within graph nodes
    result = meta_state.execute_agent()
    ```
"""

from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from typing import TYPE_CHECKING, Any, Self

from haive.core.common.mixins.recompile_mixin import RecompileMixin
from haive.core.schema.state_schema import StateSchema
from pydantic import Field, model_validator

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class MetaStateSchema(StateSchema, RecompileMixin):
    """State schema with embedded agent and graph composition support.

    MetaStateSchema extends StateSchema and RecompileMixin to provide
    graph-level agent composition and recompilation management. It focuses
    on agent lifecycle, graph coordination, and dynamic recompilation.

    Key Features:
        - Agent embedding: Store agents as state fields
        - Graph composition: Coordinate nested agent execution
        - Recompilation tracking: Track when agents need recompilation
        - Agent lifecycle: Manage agent state and execution
        - Dynamic modification: Support runtime agent changes

    Fields:
        agent: The contained agent instance
        graph_context: Graph-level execution context
        agent_state: Current state of the contained agent
        execution_result: Result from agent execution
        composition_metadata: Metadata about graph composition

    The meta state tracks agent changes and manages recompilation
    automatically using the RecompileMixin.
    """

    # Core agent field - the contained agent
    agent: Any | None = Field(
        default=None, description="Contained agent for graph composition"
    )

    # Graph composition context
    graph_context: dict[str, Any] = Field(
        default_factory=dict, description="Graph-level execution context and metadata"
    )

    # Agent state and execution
    agent_state: dict[str, Any] = Field(
        default_factory=dict, description="Current state of the contained agent"
    )

    execution_result: dict[str, Any] | None = Field(
        default=None, description="Result from agent execution"
    )

    # Composition metadata
    composition_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadata about graph composition and coordination",
    )

    # Agent identification
    agent_name: str | None = Field(
        default=None, description="Name/identifier for the contained agent"
    )

    agent_type: str | None = Field(
        default=None, description="Type of the contained agent"
    )

    # Execution status
    execution_status: str = Field(
        default="ready",
        description="Current execution status (ready, running, completed, error)",
    )

    # Define shared fields for graph communication
    __shared_fields__ = ["execution_result", "execution_status", "graph_context"]

    # Define reducers for graph-specific fields
    __reducer_fields__ = {
        # Merge dicts
        "execution_result": lambda a, b: {**(a or {}), **(b or {})},
        # Merge dicts
        "graph_context": lambda a, b: {**(a or {}), **(b or {})},
        # Merge dicts
        "composition_metadata": lambda a, b: {**(a or {}), **(b or {})},
    }

    @model_validator(mode="after")
    @classmethod
    def setup_graph_composition(cls) -> Self:
        """Setup graph composition with the contained agent.

        This validator:
        1. Sets agent metadata (name, type)
        2. Initializes graph context
        3. Sets up recompilation tracking
        4. Initializes composition metadata
        """
        if self.agent is not None:
            # Set agent metadata
            if hasattr(self.agent, "name") and not self.agent_name:
                self.agent_name = self.agent.name

            if hasattr(self.agent, "__class__") and not self.agent_type:
                self.agent_type = self.agent.__class__.__name__

            # Set up graph context
            if not self.graph_context:
                self.graph_context = {
                    "created_at": str(datetime.now()),
                    "agent_class": self.agent_type,
                    "composition_type": "nested",
                }

            # Set up composition metadata
            if not self.composition_metadata:
                self.composition_metadata = {
                    "agent_name": self.agent_name,
                    "agent_type": self.agent_type,
                    "recompilation_supported": hasattr(
                        self.agent, "mark_for_recompile"
                    ),
                }

            # Check if agent needs recompilation
            if hasattr(self.agent, "needs_recompile") and self.agent.needs_recompile:
                self.mark_for_recompile(
                    f"Contained agent {self.agent_name} needs recompilation"
                )

        return self

    def update_agent(self, new_agent: Any) -> None:
        """Update the contained agent and handle recompilation.

        Args:
            new_agent: The new agent to use
        """
        if self.agent != new_agent:
            old_agent_name = self.agent_name
            self.agent = new_agent

            # Update metadata
            if hasattr(new_agent, "name"):
                self.agent_name = new_agent.name
            if hasattr(new_agent, "__class__"):
                self.agent_type = new_agent.__class__.__name__

            # Mark for recompilation due to agent change
            reason = f"Agent changed from {old_agent_name} to {self.agent_name}"
            self.mark_for_recompile(reason)

            # Update composition metadata
            self.composition_metadata.update(
                {
                    "agent_name": self.agent_name,
                    "agent_type": self.agent_type,
                    "last_updated": str(datetime.now()),
                }
            )

    def check_agent_recompilation(self) -> bool:
        """Check if the contained agent needs recompilation.

        Returns:
            True if agent needs recompilation
        """
        if self.agent is None:
            return False

        # Check if agent supports recompilation
        if hasattr(self.agent, "needs_recompile"):
            return self.agent.needs_recompile

        return False

    async def execute_agent(
        self,
        input_data: dict[str, Any] | None = None,
        config: dict[str, Any] | None = None,
        update_state: bool = True,
    ) -> dict[str, Any]:
        """Execute the contained agent with graph-focused execution.

        Args:
            input_data: Input data for the agent (defaults to messages)
            config: Execution configuration
            update_state: Whether to update the meta state with results

        Returns:
            Dictionary containing execution results

        Raises:
            ValueError: If no agent is configured
            RuntimeError: If agent execution fails
        """
        if self.agent is None:
            raise ValueError("No agent configured for execution")

        logger.info(f"Executing contained agent: {self.agent_name or 'unnamed'}")

        # Prepare input from agent state if not provided
        if input_data is None:
            input_data = self.agent_state.copy() if self.agent_state else {}

        # Update execution status
        if update_state:
            self.execution_status = "running"

        try:
            # Check if agent needs recompilation before execution
            if self.check_agent_recompilation():
                logger.info(
                    f"Agent {self.agent_name} needs recompilation before execution"
                )
                self.mark_for_recompile(f"Agent {self.agent_name} needs recompilation")

            # Execute the agent using appropriate method
            if hasattr(self.agent, "arun"):
                # Async execution - pass input_data directly
                result = await self.agent.arun(input_data, **config or {})
            elif hasattr(self.agent, "run"):
                # Sync execution - run in thread to avoid blocking
                result = await asyncio.to_thread(
                    self.agent.run, input_data, **config or {}
                )
            elif hasattr(self.agent, "ainvoke"):
                # Async invoke
                result = await self.agent.ainvoke(input_data, config or {})
            elif hasattr(self.agent, "invoke"):
                # Sync invoke - run in thread
                result = await asyncio.to_thread(
                    self.agent.invoke, input_data, config or {}
                )
            elif callable(self.agent):
                # Callable - run in thread
                result = await asyncio.to_thread(self.agent, input_data)
            else:
                raise RuntimeError(f"Agent {self.agent_type} is not executable")

            # Create execution record
            execution_record = {
                "timestamp": str(datetime.now()),
                "input": input_data,
                "output": result,
                "config": config or {},
                "status": "success",
            }

            if update_state:
                # Update execution result
                self.execution_result = execution_record
                self.execution_status = "completed"

                # Update graph context with execution info
                self.graph_context.update(
                    {
                        "last_execution": execution_record["timestamp"],
                        "execution_count": self.graph_context.get("execution_count", 0)
                        + 1,
                    }
                )

                # Update composition metadata
                self.composition_metadata.update(
                    {
                        "last_execution_status": "success",
                        "last_execution_time": execution_record["timestamp"],
                    }
                )

                # Update agent state with result if available
                if isinstance(result, dict) and "state" in result:
                    self.agent_state.update(result["state"])

            logger.info("Agent execution completed successfully")
            return execution_record

        except Exception as e:
            logger.exception(f"Agent execution failed: {e}")

            # Create error record
            error_record = {
                "timestamp": str(datetime.now()),
                "input": input_data,
                "error": str(e),
                "error_type": type(e).__name__,
                "config": config or {},
                "status": "error",
            }

            if update_state:
                self.execution_result = error_record
                self.execution_status = "error"

                # Update composition metadata with error info
                self.composition_metadata.update(
                    {
                        "last_execution_status": "error",
                        "last_error": str(e),
                        "last_error_time": error_record["timestamp"],
                    }
                )

            raise RuntimeError(f"Agent execution failed: {e}") from e

    def prepare_agent_input(
        self,
        additional_input: dict[str, Any] | None = None,
        include_agent_state: bool = True,
        include_context: bool = True,
    ) -> dict[str, Any]:
        """Prepare input data for agent execution with graph context.

        Args:
            additional_input: Additional input data to include
            include_agent_state: Whether to include agent state
            include_context: Whether to include graph context

        Returns:
            Dictionary with prepared input data
        """
        input_data = {}

        # Include agent state if requested
        if include_agent_state and self.agent_state:
            input_data.update(self.agent_state)

        # Include graph context if requested
        if include_context:
            input_data["graph_context"] = self.graph_context

        # Add additional input
        if additional_input:
            input_data.update(additional_input)

        return input_data

    def get_agent_engine(self, engine_name: str) -> Any | None:
        """Get an engine from the contained agent for graph composition.

        Args:
            engine_name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        if self.agent is None:
            return None

        # Try to get from agent's engines dict
        if (
            hasattr(self.agent, "engines")
            and isinstance(self.agent.engines, dict)
            and engine_name in self.agent.engines
        ):
            return self.agent.engines[engine_name]

        # Try to get main engine if requested
        if engine_name == "main" and hasattr(self.agent, "engine"):
            return self.agent.engine

        return None

    def reset_execution_state(self) -> None:
        """Reset execution state for the contained agent."""
        self.execution_status = "ready"
        self.execution_result = None
        self.agent_state = {}

        # Clear recompilation state
        self.resolve_recompile(success=True)

    def get_execution_summary(self) -> dict[str, Any]:
        """Get a summary of agent execution and graph composition status.

        Returns:
            Dictionary with execution statistics and graph status
        """
        execution_count = self.graph_context.get("execution_count", 0)

        return {
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "current_status": self.execution_status,
            "execution_count": execution_count,
            "last_execution": self.graph_context.get("last_execution"),
            "graph_context": self.graph_context,
            "composition_metadata": self.composition_metadata,
            "recompilation_status": self.get_recompile_status(),
            "needs_recompilation": self.check_agent_recompilation(),
        }

    def clone_with_agent(
        self, new_agent: Any, reset_history: bool = True
    ) -> MetaStateSchema:
        """Create a clone of this meta state with a different agent.

        Args:
            new_agent: The new agent to use
            reset_history: Whether to reset execution history

        Returns:
            New MetaStateSchema instance with the new agent
        """
        # Create a copy of this state
        cloned_data = self.model_dump()

        # Update agent
        cloned_data["agent"] = new_agent

        # Reset execution state if requested
        if reset_history:
            cloned_data["execution_result"] = None
            cloned_data["execution_status"] = "ready"
            cloned_data["agent_state"] = {}
            cloned_data["graph_context"] = {
                "created_at": str(datetime.now()),
                "composition_type": "cloned",
            }

        # Create new instance
        return self.__class__.model_validate(cloned_data)

    @classmethod
    def from_agent(
        cls,
        agent: Any,
        initial_state: dict[str, Any] | None = None,
        graph_context: dict[str, Any] | None = None,
    ) -> MetaStateSchema:
        """Create a MetaStateSchema from an agent for graph composition.

        Args:
            agent: The agent to embed
            initial_state: Initial agent state
            graph_context: Initial graph context

        Returns:
            New MetaStateSchema instance
        """
        return cls(
            agent=agent,
            agent_state=initial_state or {},
            graph_context=graph_context or {},
        )

    def __str__(self) -> str:
        """String representation of the meta state."""
        agent_info = (
            f"{self.agent_type}({self.agent_name})" if self.agent else "No agent"
        )
        status_info = f"status={self.execution_status}"
        execution_info = f"executions={self.graph_context.get('execution_count', 0)}"
        recompile_info = f"needs_recompile={self.needs_recompile}"

        return f"MetaStateSchema(agent={agent_info}, {status_info}, {execution_info}, {recompile_info})"

    def __repr__(self) -> str:
        """Detailed representation of the meta state."""
        return (
            f"MetaStateSchema("
            f"agent={self.agent_type}, "
            f"agent_name='{self.agent_name}', "
            f"status='{self.execution_status}', "
            f"executions={self.graph_context.get('execution_count', 0)}, "
            f"agent_state_keys={list(self.agent_state.keys()) if self.agent_state else []}, "
            f"needs_recompile={self.needs_recompile}"
            f")"
        )
