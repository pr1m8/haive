"""Meta state schema with embedded agent support.

This module provides MetaStateSchema, a specialized state schema that can contain
an agent as part of its state. This enables sophisticated agent composition patterns
where agents can be nested and executed within other agents.

The meta state pattern allows for:
- Embedding agents as state fields
- Dynamic agent execution within graph nodes
- Agent input/output handling and routing
- Nested agent composition and orchestration
- Context sharing between meta and contained agents

Example:
    ```python
    from haive.core.schema.prebuilt.meta_state import MetaStateSchema
    from haive.agents.simple.agent import SimpleAgent
    from langchain_core.messages import HumanMessage

    # Create a contained agent
    inner_agent = SimpleAgent()

    # Create meta state with embedded agent
    meta_state = MetaStateSchema(
        agent=inner_agent,
        agent_input={"messages": [HumanMessage(content="Hello")]},
        meta_context={"purpose": "nested_execution"}
    )

    # The agent can be executed from within graph nodes
    # using the agent field from the state
    ```
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from langchain_core.messages import BaseMessage
from pydantic import Field, model_validator

from haive.core.schema.prebuilt.messages_state import MessagesState

if TYPE_CHECKING:
    from haive.agents.base.agent import Agent


class MetaStateSchema(MessagesState):
    """State schema with embedded agent support for meta-execution patterns.

    MetaStateSchema extends MessagesState to provide specialized support for
    containing and executing agents within the state itself. This enables
    sophisticated agent composition patterns and nested execution.

    Key Features:
        - Agent embedding: Store agents as state fields
        - Execution context: Manage agent input/output and configuration
        - Engine synchronization: Sync engines from contained agents
        - Context sharing: Share state between meta and contained agents
        - Execution control: Configure how contained agents are executed

    Fields:
        agent: The contained agent instance for meta execution
        agent_input: Input data to pass to the contained agent
        agent_output: Output data received from the contained agent
        agent_config: Configuration for agent execution
        meta_context: Meta-level execution context and metadata
        execution_history: History of agent executions
        agent_state: Current state of the contained agent

    The meta state automatically syncs engines from contained agents and
    provides utilities for agent execution and context management.
    """

    # Core agent field - the contained agent
    agent: Optional[Any] = Field(
        default=None, description="Contained agent for meta execution"
    )

    # Agent execution context
    agent_input: Dict[str, Any] = Field(
        default_factory=dict, description="Input data to pass to the contained agent"
    )

    agent_output: Dict[str, Any] = Field(
        default_factory=dict,
        description="Output data received from the contained agent",
    )

    agent_config: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration for agent execution (debug, thread_id, etc.)",
    )

    # Meta-level context
    meta_context: Dict[str, Any] = Field(
        default_factory=dict, description="Meta-level execution context and metadata"
    )

    # Execution tracking
    execution_history: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="History of agent executions with timestamps and results",
    )

    agent_state: Dict[str, Any] = Field(
        default_factory=dict, description="Current state of the contained agent"
    )

    # Agent identification and metadata
    agent_name: Optional[str] = Field(
        default=None, description="Name/identifier for the contained agent"
    )

    agent_type: Optional[str] = Field(
        default=None, description="Type of the contained agent"
    )

    # Execution results
    last_execution_result: Optional[Dict[str, Any]] = Field(
        default=None, description="Result from the last agent execution"
    )

    execution_status: str = Field(
        default="ready",
        description="Current execution status (ready, running, completed, error)",
    )

    error_info: Optional[Dict[str, Any]] = Field(
        default=None, description="Error information from failed executions"
    )

    # Define shared fields for parent-child communication
    __shared_fields__ = ["messages", "agent_output", "execution_status"]

    # Define reducers for agent-specific fields
    __reducer_fields__ = {
        "messages": "add_messages",  # Use LangGraph's add_messages
        "execution_history": lambda a, b: (a or []) + (b or []),
        "agent_output": lambda a, b: {**(a or {}), **(b or {})},  # Merge dicts
        "meta_context": lambda a, b: {**(a or {}), **(b or {})},  # Merge dicts
    }

    @model_validator(mode="after")
    def setup_agent_integration(self) -> "MetaStateSchema":
        """Setup integration with the contained agent.

        This validator:
        1. Syncs engines from the contained agent
        2. Sets agent metadata (name, type)
        3. Initializes agent state if needed
        4. Sets up execution context
        """
        if self.agent is not None:
            # Set agent metadata
            if hasattr(self.agent, "name") and not self.agent_name:
                self.agent_name = self.agent.name

            if hasattr(self.agent, "__class__") and not self.agent_type:
                self.agent_type = self.agent.__class__.__name__

            # Sync engines from the contained agent
            self._sync_agent_engines()

            # Initialize agent state if needed
            if not self.agent_state and hasattr(self.agent, "state_schema"):
                try:
                    # Get the agent's current state
                    agent_state_instance = self.agent.state_schema()
                    self.agent_state = agent_state_instance.model_dump()
                except Exception as e:
                    # Log but don't fail - agent might not be fully initialized
                    from haive.core.logging.rich_logger import get_logger

                    logger = get_logger(__name__)
                    logger.debug(f"Could not initialize agent state: {e}")

            # Set up default execution context
            if not self.meta_context:
                self.meta_context = {
                    "created_at": str(__import__("datetime").datetime.now()),
                    "agent_class": self.agent_type,
                    "execution_count": 0,
                }

        return self

    def _sync_agent_engines(self) -> None:
        """Sync engines from the contained agent to this state."""
        if self.agent is None:
            return

        from haive.core.logging.rich_logger import get_logger

        logger = get_logger(__name__)

        # Get engines from the agent
        agent_engines = {}

        # Try to get engines from the agent
        if hasattr(self.agent, "engines") and self.agent.engines:
            agent_engines.update(self.agent.engines)
            logger.debug(f"Found {len(self.agent.engines)} engines in agent.engines")

        # Try to get main engine
        if hasattr(self.agent, "engine") and self.agent.engine:
            engine_name = getattr(self.agent.engine, "name", "main")
            agent_engines[engine_name] = self.agent.engine
            logger.debug(f"Added main engine '{engine_name}' from agent")

        # Try to get engines from state schema
        if hasattr(self.agent, "state_schema"):
            try:
                schema_class = self.agent.state_schema
                if hasattr(schema_class, "engines") and schema_class.engines:
                    agent_engines.update(schema_class.engines)
                    logger.debug(
                        f"Found {len(schema_class.engines)} engines in agent state schema"
                    )
            except Exception as e:
                logger.debug(f"Could not access agent state schema engines: {e}")

        # Add agent engines to our engines dict with prefixed names
        for engine_name, engine in agent_engines.items():
            prefixed_name = f"agent_{engine_name}"
            if prefixed_name not in self.engines:
                self.engines[prefixed_name] = engine
                logger.debug(
                    f"Synced agent engine '{engine_name}' as '{prefixed_name}'"
                )

        # Set main engine if we don't have one
        if not self.engine and agent_engines:
            # Prefer 'main' engine, then first available
            if "main" in agent_engines:
                self.engine = agent_engines["main"]
                logger.debug("Set main engine from agent's main engine")
            else:
                first_engine = next(iter(agent_engines.values()))
                self.engine = first_engine
                logger.debug(f"Set main engine from agent's first engine")

    def execute_agent(
        self,
        input_data: Optional[Dict[str, Any]] = None,
        config: Optional[Dict[str, Any]] = None,
        update_state: bool = True,
    ) -> Dict[str, Any]:
        """Execute the contained agent with the given input.

        Args:
            input_data: Input data for the agent (defaults to agent_input)
            config: Execution configuration (defaults to agent_config)
            update_state: Whether to update the meta state with results

        Returns:
            Dictionary containing execution results

        Raises:
            ValueError: If no agent is configured
            RuntimeError: If agent execution fails
        """
        if self.agent is None:
            raise ValueError("No agent configured for execution")

        from haive.core.logging.rich_logger import get_logger

        logger = get_logger(__name__)

        # Use provided input or fall back to agent_input
        execution_input = input_data or self.agent_input
        execution_config = config or self.agent_config

        # Update execution status
        if update_state:
            self.execution_status = "running"
            self.error_info = None

        try:
            logger.info(f"Executing contained agent: {self.agent_name or 'unnamed'}")

            # Execute the agent
            if hasattr(self.agent, "run"):
                # Agent has run method
                result = self.agent.run(execution_input, **execution_config)
            elif hasattr(self.agent, "invoke"):
                # Agent has invoke method
                result = self.agent.invoke(execution_input, execution_config)
            elif callable(self.agent):
                # Agent is callable
                result = self.agent(execution_input)
            else:
                raise RuntimeError(f"Agent {self.agent_type} is not executable")

            # Create execution record
            execution_record = {
                "timestamp": str(__import__("datetime").datetime.now()),
                "input": execution_input,
                "output": result,
                "config": execution_config,
                "status": "success",
            }

            if update_state:
                # Update meta state with results
                self.agent_output = (
                    result if isinstance(result, dict) else {"result": result}
                )
                self.last_execution_result = execution_record
                self.execution_status = "completed"
                self.execution_history.append(execution_record)

                # Update execution count in meta context
                self.meta_context["execution_count"] = (
                    self.meta_context.get("execution_count", 0) + 1
                )
                self.meta_context["last_execution"] = execution_record["timestamp"]

                # Sync messages if the result contains them
                if isinstance(result, dict) and "messages" in result:
                    self.add_messages(result["messages"])

            logger.info(f"Agent execution completed successfully")
            return execution_record

        except Exception as e:
            logger.error(f"Agent execution failed: {e}")

            # Create error record
            error_record = {
                "timestamp": str(__import__("datetime").datetime.now()),
                "input": execution_input,
                "error": str(e),
                "error_type": type(e).__name__,
                "config": execution_config,
                "status": "error",
            }

            if update_state:
                self.error_info = error_record
                self.execution_status = "error"
                self.execution_history.append(error_record)

            raise RuntimeError(f"Agent execution failed: {e}") from e

    def prepare_agent_input(
        self,
        additional_input: Optional[Dict[str, Any]] = None,
        include_messages: bool = True,
        include_context: bool = True,
    ) -> Dict[str, Any]:
        """Prepare input data for agent execution.

        Args:
            additional_input: Additional input data to include
            include_messages: Whether to include messages from this state
            include_context: Whether to include meta context

        Returns:
            Dictionary with prepared input data
        """
        input_data = {}

        # Include messages if requested
        if include_messages and self.messages:
            input_data["messages"] = self.messages

        # Include meta context if requested
        if include_context:
            input_data["meta_context"] = self.meta_context

        # Add agent_input
        input_data.update(self.agent_input)

        # Add additional input
        if additional_input:
            input_data.update(additional_input)

        return input_data

    def get_agent_engine(self, engine_name: str) -> Optional[Any]:
        """Get an engine from the contained agent.

        Args:
            engine_name: Name of the engine to retrieve

        Returns:
            Engine instance if found, None otherwise
        """
        if self.agent is None:
            return None

        # Try to get from agent's engines dict
        if hasattr(self.agent, "engines") and engine_name in self.agent.engines:
            return self.agent.engines[engine_name]

        # Try to get main engine if requested
        if engine_name == "main" and hasattr(self.agent, "engine"):
            return self.agent.engine

        # Try to get from synced engines with prefix
        prefixed_name = f"agent_{engine_name}"
        return self.engines.get(prefixed_name)

    def reset_execution_state(self) -> None:
        """Reset execution state for the contained agent."""
        self.execution_status = "ready"
        self.agent_output = {}
        self.last_execution_result = None
        self.error_info = None
        self.agent_input = {}

    def get_execution_summary(self) -> Dict[str, Any]:
        """Get a summary of agent execution history.

        Returns:
            Dictionary with execution statistics and summary
        """
        total_executions = len(self.execution_history)
        successful_executions = sum(
            1 for record in self.execution_history if record.get("status") == "success"
        )
        failed_executions = total_executions - successful_executions

        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": (
                successful_executions / total_executions if total_executions > 0 else 0
            ),
            "current_status": self.execution_status,
            "agent_name": self.agent_name,
            "agent_type": self.agent_type,
            "last_execution": (
                self.execution_history[-1] if self.execution_history else None
            ),
        }

    def clone_with_agent(
        self, new_agent: Any, reset_history: bool = True
    ) -> "MetaStateSchema":
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
            cloned_data["execution_history"] = []
            cloned_data["agent_output"] = {}
            cloned_data["last_execution_result"] = None
            cloned_data["error_info"] = None
            cloned_data["execution_status"] = "ready"

        # Create new instance
        return self.__class__.model_validate(cloned_data)

    @classmethod
    def from_agent(
        cls,
        agent: Any,
        initial_input: Optional[Dict[str, Any]] = None,
        meta_context: Optional[Dict[str, Any]] = None,
    ) -> "MetaStateSchema":
        """Create a MetaStateSchema from an agent.

        Args:
            agent: The agent to embed
            initial_input: Initial input for the agent
            meta_context: Initial meta context

        Returns:
            New MetaStateSchema instance
        """
        return cls(
            agent=agent,
            agent_input=initial_input or {},
            meta_context=meta_context or {},
        )

    def __str__(self) -> str:
        """String representation of the meta state."""
        agent_info = (
            f"{self.agent_type}({self.agent_name})" if self.agent else "No agent"
        )
        status_info = f"status={self.execution_status}"
        execution_info = f"executions={len(self.execution_history)}"

        return f"MetaStateSchema(agent={agent_info}, {status_info}, {execution_info})"

    def __repr__(self) -> str:
        """Detailed representation of the meta state."""
        return (
            f"MetaStateSchema("
            f"agent={self.agent_type}, "
            f"agent_name='{self.agent_name}', "
            f"status='{self.execution_status}', "
            f"executions={len(self.execution_history)}, "
            f"messages={len(self.messages) if self.messages else 0}"
            f")"
        )
