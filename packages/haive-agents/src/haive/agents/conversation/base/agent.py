"""Base conversation agent providing core multi-agent conversation functionality.

This base class handles the orchestration of conversations between multiple agents,
with support for different conversation modes and patterns. It implements the core
graph-based state management system that all conversation types extend.

The BaseConversationAgent provides:

1. A common orchestration flow for all conversation types
2. Agent compilation and execution management
3. Message routing and processing
4. Automatic state tracking via reducers
5. Conversation initialization and conclusion
6. Extension points for specialized conversation behaviors

The conversation flow follows a standard pattern:
initialize → select_speaker → execute_agent → process_response → check_end → conclude

Each conversation type extends this base by implementing the abstract methods,
particularly the `select_speaker` method that defines the conversation pattern.
"""

from abc import abstractmethod
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.logging.rich_logger import LogLevel, get_logger
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field, PrivateAttr, model_validator

from haive.agents.base.agent import Agent
from haive.agents.conversation.base.state import ConversationState
from haive.agents.simple.agent import SimpleAgent

logger = get_logger(__name__)
logger.set_level(LogLevel.WARNING)


class BaseConversationAgent(Agent):
    """Base conversation agent that orchestrates multi-agent conversations.

    This abstract base class provides the core functionality for managing
    conversations between multiple agents, with hooks for customization.

    The BaseConversationAgent implements a graph-based conversation flow
    that all specialized conversation types extend and customize. It handles
    agent compilation, message routing, state tracking, and conversation
    lifecycle management.

    Attributes:
        participant_agents (Dict[str, Union[SimpleAgent, AugLLMConfig]]):
            Mapping of participant names to agent instances or configs.
        topic (str): The conversation topic.
        max_rounds (int): Maximum number of conversation rounds.
        mode (str): Conversation mode identifier (e.g., "round_robin", "debate").
        recursion_limit (int): Maximum recursion depth for agent execution.
        handle_errors (bool): Whether to handle agent execution errors gracefully.
        max_turns_safety (int): Absolute maximum turns as a safety limit.

    Note:
        This is an abstract base class. Concrete conversation types must implement
        at minimum the `select_speaker` method to define their conversation pattern.
    """

    # Agents participating in the conversation
    participant_agents: dict[str, SimpleAgent | AugLLMConfig] = Field(
        default_factory=dict, description="Agent instances or configs by name"
    )

    # Compiled agents cache
    _compiled_agents: dict[str, SimpleAgent] = PrivateAttr(default_factory=dict)

    # Configuration
    topic: str = Field(default="General discussion")
    max_rounds: int = Field(default=10)
    mode: str = Field(default="round_robin", description="Conversation mode")

    # Error handling
    recursion_limit: int = Field(
        default=50, description="Maximum recursion depth for agent execution"
    )
    handle_errors: bool = Field(
        default=True, description="Whether to handle errors gracefully"
    )

    # Safety limits
    max_turns_safety: int = Field(
        default=100, description="Absolute maximum turns as safety limit"
    )

    @model_validator(mode="before")
    @classmethod
    def convert_persistence_boolean(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Convert persistence=True to actual persistence configuration."""
        if not isinstance(values, dict):
            return values

        # Check if persistence is a boolean True
        if values.get("persistence") is True:
            logger.info(
                "Converting persistence=True to PostgreSQL persistence configuration"
            )

            try:
                import os

                from haive.core.persistence.postgres_config import (
                    PostgresCheckpointerConfig,
                )
                from haive.core.persistence.types import (
                    CheckpointerMode,
                    CheckpointStorageMode,
                )

                # Use environment connection string if available (Supabase)
                connection_string = os.getenv("POSTGRES_CONNECTION_STRING")

                if connection_string:
                    # Use Supabase/environment connection string
                    # Create unique pool per conversation to avoid prepared statement conflicts
                    conversation_id = getattr(
                        values.get("agent"), "name", "conversation"
                    )
                    app_name = f"haive_{conversation_id}_{id(values)}"

                    values["persistence"] = PostgresCheckpointerConfig(
                        connection_string=connection_string,
                        mode=CheckpointerMode.SYNC,
                        storage_mode=CheckpointStorageMode.FULL,
                        prepare_threshold=None,  # Disable prepared statements completely
                        auto_commit=True,  # Ensure auto-commit is enabled
                        min_pool_size=1,  # Minimal pool to reduce conflicts
                        max_pool_size=3,  # Small pool for isolation
                        connection_kwargs={
                            "prepare_threshold": None,  # Extra explicit disable
                            "application_name": app_name,  # Unique app name for identification
                            "connect_timeout": 30,  # 30 second connection timeout
                            "keepalives_idle": 600,  # Keep connection alive for 10 minutes
                            "keepalives_interval": 30,  # Send keepalive every 30 seconds
                            "keepalives_count": 3,  # 3 failed keepalives before disconnect
                        },
                    )
                    logger.info(
                        f"Set up PostgreSQL persistence for {app_name} (prepared statements disabled)"
                    )
                else:
                    # Use default local PostgreSQL
                    conversation_id = getattr(
                        values.get("agent"), "name", "conversation"
                    )
                    app_name = f"haive_{conversation_id}_{id(values)}"

                    values["persistence"] = PostgresCheckpointerConfig(
                        mode=CheckpointerMode.SYNC,
                        storage_mode=CheckpointStorageMode.FULL,
                        prepare_threshold=None,  # Disable prepared statements completely
                        auto_commit=True,  # Ensure auto-commit is enabled
                        min_pool_size=1,  # Minimal pool to reduce conflicts
                        max_pool_size=3,  # Small pool for isolation
                        connection_kwargs={
                            "prepare_threshold": None,  # Extra explicit disable
                            "application_name": app_name,  # Unique app name for identification
                            "connect_timeout": 30,  # 30 second connection timeout
                            "keepalives_idle": 600,  # Keep connection alive for 10 minutes
                            "keepalives_interval": 30,  # Send keepalive every 30 seconds
                            "keepalives_count": 3,  # 3 failed keepalives before disconnect
                        },
                    )
                    logger.info("Set up default PostgreSQL persistence")

            except ImportError as e:
                logger.warning(f"PostgreSQL dependencies not available: {e}")
                # Fall back to memory persistence
                try:
                    from haive.core.persistence.memory import MemoryCheckpointerConfig

                    values["persistence"] = MemoryCheckpointerConfig()
                    logger.info("Using memory persistence fallback")
                except ImportError:
                    logger.exception("Could not import MemoryCheckpointerConfig")
                    values["persistence"] = None
            except Exception as e:
                logger.exception(f"Error setting up persistence configuration: {e}")
                values["persistence"] = None

        return values

    def setup_agent(self):
        """Set up the conversation orchestrator.

        This method performs critical initialization steps for the conversation agent:

        1. Configures the state schema for conversation tracking
        2. Creates a default orchestrator engine if none is provided
        3. Compiles all participant agents to ensure they're ready for execution
        4. Sets up persistence if persistence=True was passed

        This method is called automatically during the agent's lifecycle and
        should rarely need to be called directly.

        Returns:
            None
        """
        # Set the state schema
        self.state_schema = self.get_conversation_state_schema()
        self.set_schema = True

        # Ensure we have a default engine for orchestration
        if not self.engine and not self.engines:
            self.engine = self._create_orchestrator_engine()
            self.engines["orchestrator"] = self.engine

        # Compile participant agents
        self._compile_participants()

        super().setup_agent()

    def get_conversation_state_schema(self) -> type:
        """Get the state schema for this conversation type.

        Override in subclasses to provide custom state schemas.
        """
        return ConversationState

    def _create_orchestrator_engine(self) -> AugLLMConfig:
        """Create the default orchestrator engine."""
        return AugLLMConfig(
            name="conversation_orchestrator",
            system_message=f"You are orchestrating a {self.mode} conversation about: {self.topic}",
        )

    def _compile_participants(self):
        """Compile all participant agents."""
        for name, agent_or_config in self.participant_agents.items():
            if isinstance(agent_or_config, AugLLMConfig):
                # Create SimpleAgent from config
                agent = SimpleAgent(name=f"{name}_agent", engine=agent_or_config)
            else:
                agent = agent_or_config

            # Compile the agent
            if not hasattr(agent, "_compiled_graph") or not agent._compiled_graph:
                agent.compile()

            self._compiled_agents[name] = agent

    def build_graph(self) -> BaseGraph:
        """Build the conversation graph."""
        graph = BaseGraph(
            name=f"{self.name}_conversation",
            state_schema=self.get_conversation_state_schema(),
        )

        # Core nodes
        graph.add_node("initialize", self.initialize_conversation)
        graph.add_node("select_speaker", self.select_speaker)
        graph.add_node("execute_agent", self.execute_agent)
        graph.add_node("process_response", self.process_response)
        graph.add_node("check_end", self.check_end)
        graph.add_node("conclude", self.conclude_conversation)

        # Core flow
        graph.add_edge(START, "initialize")
        graph.add_edge("initialize", "select_speaker")
        graph.add_edge("execute_agent", "process_response")
        graph.add_edge("process_response", "check_end")
        graph.add_edge("conclude", END)

        # Conditional routing - select_speaker decides if we continue or end
        def speaker_router(state: Any) -> str:
            """Route based on speaker selection result."""
            # Handle different state types
            if isinstance(state, dict):
                current_speaker = state.get("current_speaker")
                conversation_ended = state.get("conversation_ended", False)
            else:
                current_speaker = getattr(state, "current_speaker", None)
                conversation_ended = getattr(state, "conversation_ended", False)

            if current_speaker is not None and not conversation_ended:
                return "execute_agent"
            return "conclude"

        graph.add_conditional_edges(
            "select_speaker",
            speaker_router,
            {"execute_agent": "execute_agent", "conclude": "conclude"},
        )

        # Check end decides if we go back to select_speaker or conclude
        def end_router(state: Any) -> str:
            """Route based on end check result."""
            # Handle different state types
            if isinstance(state, dict):
                conversation_ended = state.get("conversation_ended", False)
            else:
                conversation_ended = getattr(state, "conversation_ended", False)

            if conversation_ended:
                return "conclude"
            return "select_speaker"

        graph.add_conditional_edges(
            "check_end",
            end_router,
            {"select_speaker": "select_speaker", "conclude": "conclude"},
        )

        # Add custom nodes and edges
        self._add_custom_graph_elements(graph)

        return graph

    def _add_custom_graph_elements(self, graph: BaseGraph):
        """Hook for subclasses to add custom nodes and edges.

        Override this method to extend the graph structure.
        """

    def initialize_conversation(self, state: Any) -> Command:
        """Initialize the conversation."""
        # Get speaker names
        speaker_names = list(self._compiled_agents.keys())

        # Create initial message
        initial_message = self._create_initial_message()

        # Base initialization
        update = {
            "messages": [initial_message],
            "speakers": speaker_names,
            "topic": self.topic,
            "max_rounds": self.max_rounds,
            "round_number": 0,
            "turn_count": 0,
            "mode": self.mode,
            "conversation_ended": False,
            "current_speaker": None,
            "speaker_history": [],
        }

        # Add custom initialization
        custom_init = self._custom_initialization(state)
        update.update(custom_init)

        logger.info(
            f"Initialized conversation with {len(speaker_names)} participants, max_rounds={self.max_rounds}"
        )

        return Command(update=update)

    @abstractmethod
    def select_speaker(self, state: Any) -> Command:
        """Select the next speaker in the conversation.

        This is the primary method that defines the conversation pattern and must
        be implemented by all conversation type subclasses. It determines which
        participant should speak next based on the current conversation state.

        The implementation of this method defines the fundamental behavior of each
        conversation type. For example:
        - Round-robin conversations select speakers in a fixed rotating order
        - Debate conversations select based on debate phase and structure
        - Directed conversations use a moderator to select the next speaker

        Args:
            state (Any): The current conversation state, containing speakers,
                         message history, and conversation metadata.

        Returns:
            Command: A langgraph Command object with state updates. Must include either:
                - update={"current_speaker": speaker_name} to continue conversation
                - update={"current_speaker": None, "conversation_ended": True} to end

        Raises:
            NotImplementedError: If not implemented by a subclass.

        Note:
            This is the core method that differentiates conversation types. Each
            subclass must implement this method to define its unique conversation pattern.
        """
        raise NotImplementedError("Subclasses must implement select_speaker")

    def execute_agent(self, state: Any) -> Command:
        """Execute the current speaker's agent."""
        # Safe state access
        if isinstance(state, dict):
            current_speaker = state.get("current_speaker")
        else:
            current_speaker = getattr(state, "current_speaker", None)

        # Safety check
        if not current_speaker or current_speaker not in self._compiled_agents:
            logger.warning(f"Invalid speaker: {current_speaker}")
            return Command(update={"conversation_ended": True, "current_speaker": None})

        agent = self._compiled_agents[current_speaker]

        # Prepare input for agent
        agent_input = self._prepare_agent_input(state, current_speaker)

        try:
            # Execute agent with recursion limit
            config = {"configurable": {"recursion_limit": self.recursion_limit}}
            result = agent.invoke(agent_input, config)

            # Extract new messages
            new_messages = self._extract_agent_messages(
                result, agent_input.get("messages", [])
            )

            # Add speaker name to messages
            for msg in new_messages:
                if isinstance(msg, AIMessage):
                    msg.name = current_speaker

            logger.debug(f"Agent {current_speaker} executed successfully")

            return Command(
                update={
                    "messages": new_messages,
                    "turn_count": 1,  # Increment by 1 (reducer will add)
                    "speaker_history": [
                        current_speaker
                    ],  # Append speaker (reducer will add)
                }
            )

        except Exception as e:
            if self.handle_errors:
                return self._handle_agent_error(e, current_speaker)
            raise

    def process_response(self, state: Any) -> Command:
        """Process the agent's response.

        Override in subclasses to add custom response processing.
        """
        return Command(update={})

    def check_end(self, state: Any) -> Command:
        """Check if conversation should end."""
        updates = {}

        # Safe state access
        if isinstance(state, dict):
            turn_count = state.get("turn_count", 0)
            round_number = state.get("round_number", 0)
            conversation_ended = state.get("conversation_ended", False)
            max_rounds = state.get("max_rounds", self.max_rounds)
        else:
            turn_count = getattr(state, "turn_count", 0)
            round_number = getattr(state, "round_number", 0)
            conversation_ended = getattr(state, "conversation_ended", False)
            max_rounds = getattr(state, "max_rounds", self.max_rounds)

        logger.debug(
            f"check_end: turn_count={turn_count}, round_number={round_number}, conversation_ended={conversation_ended}"
        )

        # Check if already marked as ended
        if conversation_ended:
            logger.info("Conversation already marked as ended")
            updates["conversation_ended"] = True
            return Command(update=updates)

        # Check round limit
        if round_number >= max_rounds:
            logger.info(f"Max rounds reached: {round_number} >= {max_rounds}")
            updates["conversation_ended"] = True
            return Command(update=updates)

        # Safety check on turn count
        if turn_count > self.max_turns_safety:
            logger.warning(
                f"Safety limit reached: {turn_count} > {self.max_turns_safety}"
            )
            updates["conversation_ended"] = True
            return Command(update=updates)

        # Check custom end conditions
        custom_end = self._check_custom_end_conditions(state)
        if custom_end:
            logger.info("Custom end condition triggered")
            updates.update(custom_end)
            if "conversation_ended" not in updates:
                updates["conversation_ended"] = True
            return Command(update=updates)

        # Continue conversation
        return Command(update=updates)

    def conclude_conversation(self, state: Any) -> Command:
        """Create final conclusion for the conversation."""
        # Safe state access
        if isinstance(state, dict):
            turn_count = state.get("turn_count", 0)
            round_number = state.get("round_number", 0)
            max_rounds = state.get("max_rounds", self.max_rounds)
            conversation_ended = state.get("conversation_ended", False)
        else:
            turn_count = getattr(state, "turn_count", 0)
            round_number = getattr(state, "round_number", 0)
            max_rounds = getattr(state, "max_rounds", self.max_rounds)
            conversation_ended = getattr(state, "conversation_ended", False)

        # Determine reason for ending
        if round_number >= max_rounds:
            reason = f"Reached maximum rounds ({max_rounds})"
        elif turn_count > self.max_turns_safety:
            reason = f"Safety limit reached ({self.max_turns_safety} turns)"
        elif conversation_ended:
            reason = "Conversation completed"
        else:
            reason = "Unknown reason"

        conclusion_msg = SystemMessage(
            content=f"🏁 Conversation ended: {reason}\n"
            f"📊 Total rounds: {round_number}\n"
            f"🔄 Total turns: {turn_count}"
        )

        logger.info(f"Conversation concluded: {reason}")

        return Command(
            update={
                "messages": [conclusion_msg],
                "conversation_ended": True,
                "current_speaker": None,
            }
        )

    # Helper methods

    def _create_initial_message(self) -> BaseMessage:
        """Create the initial conversation message."""
        return HumanMessage(
            content=f"Topic: {self.topic}\nLet's begin our {self.mode} discussion."
        )

    def _custom_initialization(self, state: Any) -> dict[str, Any]:
        """Hook for custom initialization. Override in subclasses."""
        return {}

    def _prepare_agent_input(self, state: Any, agent_name: str) -> dict[str, Any]:
        """Prepare input for an agent. Override for custom behavior."""
        if isinstance(state, dict):
            messages = state.get("messages", [])
        else:
            messages = getattr(state, "messages", [])
        return {"messages": messages}

    def _extract_agent_messages(
        self, result: Any, input_messages: list[BaseMessage]
    ) -> list[BaseMessage]:
        """Extract new messages from agent result."""
        new_messages = []

        if isinstance(result, dict) and "messages" in result:
            result_messages = result.get("messages", [])
            # Get only new messages (after what we sent)
            if len(result_messages) > len(input_messages):
                new_messages = result_messages[len(input_messages) :]
        elif isinstance(result, list):
            # Result might be a list of messages directly
            new_messages = [msg for msg in result if isinstance(msg, BaseMessage)]

        return new_messages

    def _handle_agent_error(self, error: Exception, agent_name: str) -> Command:
        """Handle errors from agent execution."""
        logger.error(f"Error executing agent {agent_name}: {error}")
        error_msg = AIMessage(
            content=f"[Error from {agent_name}]: {error!s}", name=agent_name
        )
        return Command(
            update={
                "messages": [error_msg],
                "turn_count": 1,
                "speaker_history": [agent_name],
            }
        )

    def _check_custom_end_conditions(self, state: Any) -> dict[str, Any] | None:
        """Check custom end conditions. Override in subclasses."""
        return None

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Define input fields."""
        return {"messages": (list[BaseMessage], []), "topic": (str, "")}

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Define output fields."""
        return {
            "messages": (list[BaseMessage], []),
            "round_number": (int, 0),
            "turn_count": (int, 0),
            "conversation_ended": (bool, False),
        }

    # Factory method for easy creation
    @classmethod
    def create(
        cls, participants: dict[str, SimpleAgent | AugLLMConfig], **kwargs
    ) -> "BaseConversationAgent":
        """Create a conversation with participants."""
        return cls(participant_agents=participants, **kwargs)
