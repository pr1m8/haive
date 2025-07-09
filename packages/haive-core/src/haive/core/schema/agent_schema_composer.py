"""Agent Schema Composer for the Haive Framework.

This module provides the AgentSchemaComposer class, which extends SchemaComposer
with agent-specific functionality for building dynamic state schemas from multiple
agents. It handles intelligent field separation, message preservation, and
multi-agent coordination patterns.

The AgentSchemaComposer is the cornerstone of multi-agent state management in Haive,
enabling seamless composition of schemas with proper field sharing, reducers, and
engine I/O mappings while preserving critical message fields like tool_call_id.

Example:
    Basic usage for composing schemas from agents::

        from haive.core.schema.agent_schema_composer import AgentSchemaComposer
        from haive.agents.react.agent import ReactAgent
        from haive.agents.simple.agent import SimpleAgent

        # Create agents with their engines
        react_agent = ReactAgent(name="Calculator", engine=calc_engine)
        simple_agent = SimpleAgent(name="Planner", engine=plan_engine)

        # Compose schema from agents
        MultiAgentState = AgentSchemaComposer.from_agents(
            agents=[react_agent, simple_agent],
            name="MultiAgentState",
            separation="smart",  # Intelligent field separation
            build_mode=BuildMode.SEQUENCE  # Sequential execution
        )

        # Create state instance
        state = MultiAgentState()
        # state.messages will use preserve_messages_reducer automatically

Attributes:
    logger: Module-level logger for debugging schema composition
    BuildMode: Enum defining execution patterns for multi-agent systems

Note:
    This module uses a custom message reducer (preserve_messages_reducer) instead
    of LangGraph's default to prevent loss of fields like tool_call_id in
    ToolMessage objects during multi-agent execution.
"""

import logging
from enum import Enum
from typing import TYPE_CHECKING, Any, Dict, List, Literal, Optional, Set, Tuple, Type

from langchain_core.messages import AnyMessage, BaseMessage

from haive.core.schema.schema_composer import SchemaComposer
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)

# Import Agent only for type checking to break circular dependency
if TYPE_CHECKING:
    from haive.agents.base.agent import Agent

# Import preserve_messages_reducer
from haive.core.schema.preserve_messages_reducer import preserve_messages_reducer


# Helper function for message reducer - now uses preserve_messages_reducer
def add_messages(
    current_msgs: List[AnyMessage], new_msgs: List[AnyMessage]
) -> List[AnyMessage]:
    """Combine message lists while preserving BaseMessage objects.

    This function uses preserve_messages_reducer to maintain all fields in
    BaseMessage objects, including tool_call_id which is critical for
    multi-agent tool coordination.

    Args:
        current_msgs: Existing messages in the state
        new_msgs: New messages to add to the state

    Returns:
        Combined list of messages with BaseMessage objects preserved intact

    Example:
        >>> from langchain_core.messages import ToolMessage
        >>> tool_msg = ToolMessage(content="Result", tool_call_id="123")
        >>> messages = add_messages([], [tool_msg])
        >>> messages[0].tool_call_id  # Preserved!
        '123'
    """
    return preserve_messages_reducer(current_msgs, new_msgs)


class BuildMode(str, Enum):
    """Build modes for agent schema composition.

    Defines execution patterns for multi-agent systems, determining how
    agents are orchestrated and how their fields are composed.

    Attributes:
        PARALLEL: All agents execute independently with separate state spaces
        SEQUENCE: Agents execute in order, with state flowing between them
        HIERARCHICAL: Parent-child relationships with supervisor patterns
        CUSTOM: User-defined execution mode requiring custom implementation
    """

    PARALLEL = "parallel"  # All agents execute independently
    SEQUENCE = "sequence"  # Agents execute in sequence
    HIERARCHICAL = "hierarchical"  # Parent-child relationships
    CUSTOM = "custom"  # User-defined mode


class AgentSchemaComposer(SchemaComposer):
    """Enhanced schema composer with agent-specific intelligence.

    Extends SchemaComposer to provide intelligent schema composition from
    agent instances, handling field separation strategies, message preservation,
    and multi-agent coordination patterns. This class is the primary interface
    for building state schemas in multi-agent systems.

    The composer automatically:
    - Extracts fields from agent state schemas and engines
    - Applies intelligent field separation based on usage patterns
    - Preserves engine I/O mappings for proper routing
    - Adds message fields with custom reducers to preserve tool_call_id
    - Includes meta state for agent coordination when needed

    Example:
        >>> # Compose from multiple agents
        >>> schema = AgentSchemaComposer.from_agents(
        ...     agents=[research_agent, writer_agent],
        ...     separation="smart"
        ... )
        >>> state = schema()  # Create state instance
    """

    @classmethod
    def from_agents(
        cls,
        agents: List["Agent"],
        name: Optional[str] = None,
        include_meta: bool = None,  # Auto-detect if None
        separation: str = "smart",  # "smart", "shared", "namespaced"
        build_mode: Optional[BuildMode] = None,  # Build mode for schema generation
    ) -> Type[StateSchema]:
        """Compose a state schema from multiple agents with intelligent defaults.

        This method is the primary entry point for creating multi-agent state schemas.
        It analyzes the provided agents and creates a unified schema with proper
        field sharing, reducers, and engine mappings.

        Args:
            agents: List of agent instances to compose the schema from. Each agent
                should have a state_schema and optionally engines with I/O fields.
            name: Optional name for the composed schema class. If None, generates
                a name based on the agents (e.g., "MultiAgentState").
            include_meta: Whether to include MetaAgentState for coordination. If None,
                auto-detects based on number of agents and meta_state usage.
            separation: Field separation strategy:
                - "smart": Automatically determine sharing based on usage patterns
                - "shared": All fields are shared between agents
                - "namespaced": Each agent's fields get a unique prefix
            build_mode: Execution pattern for the multi-agent system. If None,
                defaults to PARALLEL for single agent, SEQUENCE for multiple.

        Returns:
            A new StateSchema class composed from the agent specifications.

        Raises:
            ValueError: If no agents are provided or if agents have invalid schemas.

        Example:
            >>> # Smart separation with auto-detected build mode
            >>> schema = AgentSchemaComposer.from_agents(
            ...     agents=[agent1, agent2],
            ...     name="CustomMultiState"
            ... )
            >>>
            >>> # Explicit configuration
            >>> schema = AgentSchemaComposer.from_agents(
            ...     agents=[supervisor, worker1, worker2],
            ...     separation="namespaced",
            ...     build_mode=BuildMode.HIERARCHICAL
            ... )

        Note:
            The messages field is always added with preserve_messages_reducer
            to ensure tool_call_id and other fields are maintained across
            agent boundaries.
        """

        # Auto-detect meta state need
        if include_meta is None:
            include_meta = (
                any(hasattr(a, "meta_state") for a in agents) or len(agents) > 1
            )

        # Auto-detect build mode if not specified
        if build_mode is None:
            build_mode = BuildMode.PARALLEL if len(agents) <= 1 else BuildMode.SEQUENCE

        composer = cls(name=name or cls._generate_name(agents))

        # Force messages state for agents
        composer.has_messages = True

        # Check if any agent has tools
        for agent in agents:
            if (
                hasattr(agent, "engine")
                and hasattr(agent.engine, "tools")
                and agent.engine.tools
            ):
                composer.has_tools = True
                break
            if hasattr(agent, "engines"):
                for engine in agent.engines.values():
                    if hasattr(engine, "tools") and engine.tools:
                        composer.has_tools = True
                        break

        # Collect all fields from all agents
        all_fields, engine_io_mappings = cls._collect_all_fields(agents)

        # Apply build mode specific logic
        if build_mode == BuildMode.SEQUENCE:
            cls._apply_sequence_mode(composer, all_fields, agents, engine_io_mappings)
        elif build_mode == BuildMode.PARALLEL:
            # Apply separation strategy for parallel mode
            if separation == "smart":
                cls._apply_smart_separation(composer, all_fields, agents)
            elif separation == "shared":
                cls._apply_shared_separation(composer, all_fields)
            elif separation == "namespaced":
                cls._apply_namespaced_separation(composer, all_fields, agents)
        elif build_mode == BuildMode.HIERARCHICAL:
            cls._apply_hierarchical_mode(composer, all_fields, agents)
        else:
            # Custom mode - use default separation
            if separation == "smart":
                cls._apply_smart_separation(composer, all_fields, agents)
            elif separation == "shared":
                cls._apply_shared_separation(composer, all_fields)
            elif separation == "namespaced":
                cls._apply_namespaced_separation(composer, all_fields, agents)

        # Add implicit fields
        cls._add_implicit_fields(composer, agents, include_meta)

        # Copy engine IO mappings
        for engine_name, mapping in engine_io_mappings.items():
            # Add to composer's engine IO mappings
            composer.engine_io_mappings[engine_name] = mapping.copy()

            # Update input/output fields tracking
            for field_name in mapping["inputs"]:
                composer.input_fields[engine_name].add(field_name)
            for field_name in mapping["outputs"]:
                composer.output_fields[engine_name].add(field_name)

        # Don't copy engines to prevent contamination
        # Each agent will use its own state schema with its own engines
        # This prevents tools from one agent leaking to another
        logger.debug("Skipping engine copying to prevent cross-agent contamination")

        return composer.build()

    @staticmethod
    def _collect_all_fields(
        agents: List["Agent"],
    ) -> Tuple[
        Dict[str, List[Tuple[str, str, Type, Any]]], Dict[str, Dict[str, List[str]]]
    ]:
        """Collect all fields from agents and their engine I/O mappings.

        Extracts field definitions from agent state schemas and engine
        input/output specifications. This comprehensive collection enables
        intelligent field separation and proper engine routing.

        Args:
            agents: List of agents to analyze for field extraction

        Returns:
            Tuple containing:
                - fields_dict: Mapping of field names to their sources and types
                  Format: {field_name: [(agent_id, field_name, type, info)]}
                - engine_io_mappings_dict: Engine routing information
                  Format: {engine_name: {"inputs": [...], "outputs": [...]}}

        Example:
            >>> fields, mappings = AgentSchemaComposer._collect_all_fields([agent1, agent2])
            >>> # fields["messages"] might contain multiple entries if both agents use it
            >>> # mappings["planner_engine"] contains input/output field names

        Note:
            Engine names are prefixed with agent names to avoid collisions
            (e.g., "planner_aug_llm" for aug_llm engine in planner agent).
        """
        fields = {}

        # Also track engine IO mappings in a separate dictionary
        engine_io_mappings = {}

        for agent in agents:
            agent_id = agent.id  # Use ID instead of object for hashability
            agent_name = agent.name

            # From state schema
            if agent.state_schema and hasattr(agent.state_schema, "model_fields"):
                for fname, finfo in agent.state_schema.model_fields.items():
                    if fname not in fields:
                        fields[fname] = []
                    fields[fname].append((agent_id, fname, finfo.annotation, finfo))

                # Extract engine IO mappings from state schema if available
                if hasattr(agent.state_schema, "__engine_io_mappings__"):
                    schema_mappings = getattr(
                        agent.state_schema, "__engine_io_mappings__", {}
                    )

                    # Add prefix to engine names to avoid collisions
                    for engine_name, mapping in schema_mappings.items():
                        prefixed_engine_name = (
                            f"{agent_name.lower().replace(' ', '_')}_{engine_name}"
                        )
                        engine_io_mappings[prefixed_engine_name] = mapping.copy()

            # From engines - using get_input_fields and get_output_fields
            for engine_name, engine in agent.engines.items():
                # Create prefixed engine name
                prefixed_engine_name = (
                    f"{agent_name.lower().replace(' ', '_')}_{engine_name}"
                )

                # Initialize engine mapping if not exists
                if prefixed_engine_name not in engine_io_mappings:
                    engine_io_mappings[prefixed_engine_name] = {
                        "inputs": [],
                        "outputs": [],
                    }

                # Get input fields
                if hasattr(engine, "get_input_fields"):
                    try:
                        input_fields = engine.get_input_fields()
                        for fname, (ftype, fdefault) in input_fields.items():
                            if fname not in fields:
                                fields[fname] = []
                            # Create a mock field info
                            field_info = type(
                                "FieldInfo",
                                (),
                                {"annotation": ftype, "default": fdefault},
                            )()
                            fields[fname].append((agent_id, fname, ftype, field_info))

                            # Add to engine IO mapping
                            if (
                                fname
                                not in engine_io_mappings[prefixed_engine_name][
                                    "inputs"
                                ]
                            ):
                                engine_io_mappings[prefixed_engine_name][
                                    "inputs"
                                ].append(fname)
                    except:
                        pass

                # Get output fields
                if hasattr(engine, "get_output_fields"):
                    try:
                        output_fields = engine.get_output_fields()
                        for fname, (ftype, fdefault) in output_fields.items():
                            if fname not in fields:
                                fields[fname] = []
                            # Create a mock field info
                            field_info = type(
                                "FieldInfo",
                                (),
                                {"annotation": ftype, "default": fdefault},
                            )()
                            fields[fname].append((agent_id, fname, ftype, field_info))

                            # Add to engine IO mapping
                            if (
                                fname
                                not in engine_io_mappings[prefixed_engine_name][
                                    "outputs"
                                ]
                            ):
                                engine_io_mappings[prefixed_engine_name][
                                    "outputs"
                                ].append(fname)
                    except:
                        pass

        # Return the fields and the engine IO mappings
        return fields, engine_io_mappings

    @staticmethod
    def _apply_smart_separation(
        composer: SchemaComposer, all_fields: Dict, agents: List["Agent"]
    ):
        """Apply intelligent field separation based on usage patterns.

        Smart separation automatically determines whether fields should be
        shared or namespaced based on:
        - Number of agents using the field
        - Special field names (e.g., "messages", "shared_*")
        - Field type and purpose

        Args:
            composer: SchemaComposer instance to add fields to
            all_fields: Dictionary of collected fields from all agents
            agents: List of agent instances for context

        Separation Rules:
            - Fields used by multiple agents → shared
            - Fields named "messages" or "meta_state" → always shared
            - Fields prefixed with "shared_" → always shared
            - Fields used by all agents → shared
            - Single-agent fields → namespaced if multiple agents exist

        Example:
            If agent1 and agent2 both have a "context" field, it becomes shared.
            If only agent1 has "tool_results", it becomes "agent1_tool_results"
            in a multi-agent setup.
        """

        # Create agent ID to name mapping
        agent_id_to_name = {agent.id: agent.name for agent in agents}

        for field_name, field_sources in all_fields.items():
            # Check if field appears in multiple agents (using agent IDs)
            unique_agent_ids = set(source[0] for source in field_sources)

            if len(unique_agent_ids) > 1:
                # Field used by multiple agents - share it
                # Use the first occurrence for type info
                _, _, ftype, finfo = field_sources[0]

                # Determine if it should be shared
                should_share = (
                    field_name in ["messages", "meta_state"]
                    or field_name.startswith("shared_")
                    or len(unique_agent_ids) == len(agents)  # All agents use it
                )

                # Handle field info properly
                if hasattr(finfo, "default"):
                    default = finfo.default
                elif hasattr(finfo, "default_factory"):
                    composer.add_field(
                        field_name,
                        ftype,
                        default_factory=finfo.default_factory,
                        shared=should_share,
                    )
                    continue
                else:
                    default = None

                composer.add_field(
                    field_name, ftype, default=default, shared=should_share
                )
            else:
                # Field used by single agent
                agent_id = field_sources[0][0]
                agent_name = agent_id_to_name.get(agent_id, agent_id)
                _, _, ftype, finfo = field_sources[0]

                # Could namespace it
                if len(agents) > 1:
                    namespaced_name = (
                        f"{agent_name.lower().replace(' ', '_')}_{field_name}"
                    )

                    # Handle field info properly
                    if hasattr(finfo, "default_factory"):
                        composer.add_field(
                            namespaced_name,
                            ftype,
                            default_factory=finfo.default_factory,
                            shared=False,
                        )
                    else:
                        composer.add_field(
                            namespaced_name,
                            ftype,
                            default=(
                                finfo.default if hasattr(finfo, "default") else None
                            ),
                            shared=False,
                        )
                else:
                    # Single agent, use as is
                    if hasattr(finfo, "default_factory"):
                        composer.add_field(
                            field_name, ftype, default_factory=finfo.default_factory
                        )
                    else:
                        composer.add_field(
                            field_name,
                            ftype,
                            default=(
                                finfo.default if hasattr(finfo, "default") else None
                            ),
                        )

    @staticmethod
    def _add_implicit_fields(
        composer: SchemaComposer, agents: List["Agent"], include_meta: bool
    ):
        """Add fields that should be implicitly included."""

        # Check if field exists using has_field method or by checking the fields dict
        def field_exists(name: str) -> bool:
            if hasattr(composer, "has_field"):
                return composer.has_field(name)
            elif hasattr(composer, "fields"):
                return name in composer.fields
            elif hasattr(composer, "_field_definitions"):
                return name in composer._field_definitions
            else:
                # Try to access through the model fields if already built
                try:
                    temp_model = composer.build()
                    return name in temp_model.model_fields
                except:
                    return False

        # Always ensure messages field exists
        if not field_exists("messages"):
            composer.add_field(
                "messages",
                List[AnyMessage],
                default_factory=list,
                shared=True,
                reducer=add_messages,
            )

        # Add meta state if needed
        if include_meta and not field_exists("meta_state"):
            # Import here to avoid circular imports
            try:
                from haive.core.schema.meta_agent_state import MetaAgentState

                composer.add_field(
                    "meta_state",
                    MetaAgentState,
                    default_factory=MetaAgentState,
                    shared=True,
                    description="Shared meta state for agent coordination",
                )
            except ImportError:
                # If meta_state module doesn't exist, create a dummy Dict type
                composer.add_field(
                    "meta_state",
                    Dict[str, Any],
                    default_factory=dict,
                    shared=True,
                    description="Shared meta state for agent coordination",
                )

        # Multi-agent coordination fields
        if len(agents) > 1:
            if not field_exists("active_agent_id"):
                composer.add_field(
                    "active_agent_id", Optional[str], default=None, shared=True
                )

            if not field_exists("agent_outputs"):
                composer.add_field(
                    "agent_outputs",
                    Dict[str, Any],
                    default_factory=dict,
                    shared=True,
                    description="Collected outputs from each agent",
                )

    @staticmethod
    def _generate_name(agents: List["Agent"]) -> str:
        """Generate a name for the composed schema."""
        if len(agents) == 1:
            return f"{agents[0].__class__.__name__}State"
        else:
            return "MultiAgentState"

    @staticmethod
    def _apply_shared_separation(composer: SchemaComposer, all_fields: Dict):
        """Apply shared separation - all fields are shared."""
        for field_name, field_sources in all_fields.items():
            # Use first occurrence for type info
            _, _, ftype, finfo = field_sources[0]

            if hasattr(finfo, "default_factory"):
                composer.add_field(
                    field_name,
                    ftype,
                    default_factory=finfo.default_factory,
                    shared=True,
                )
            else:
                composer.add_field(
                    field_name,
                    ftype,
                    default=finfo.default if hasattr(finfo, "default") else None,
                    shared=True,
                )

    @staticmethod
    def _apply_namespaced_separation(
        composer: SchemaComposer, all_fields: Dict, agents: List["Agent"]
    ):
        """Apply namespaced separation - each agent gets its own namespace."""
        # Create agent ID to name mapping
        agent_id_to_name = {agent.id: agent.name for agent in agents}

        for field_name, field_sources in all_fields.items():
            for agent_id, fname, ftype, finfo in field_sources:
                agent_name = agent_id_to_name.get(agent_id, agent_id)
                namespaced_name = f"{agent_name.lower().replace(' ', '_')}_{fname}"

                if hasattr(finfo, "default_factory"):
                    composer.add_field(
                        namespaced_name,
                        ftype,
                        default_factory=finfo.default_factory,
                        shared=False,
                    )
                else:
                    composer.add_field(
                        namespaced_name,
                        ftype,
                        default=finfo.default if hasattr(finfo, "default") else None,
                        shared=False,
                    )

    @staticmethod
    def _apply_sequence_mode(
        composer: SchemaComposer,
        all_fields: Dict,
        agents: List["Agent"],
        engine_io_mappings: Dict[str, Dict[str, List[str]]],
    ):
        """
        Apply sequence mode logic where agents execute in order.

        In sequence mode:
        - First agent's input fields are required
        - Last agent's output fields are the schema output
        - Intermediate fields are optional (as they may be populated by previous agents)
        - Messages field is always shared
        """
        # Create agent ID to index mapping
        agent_id_to_idx = {agent.id: idx for idx, agent in enumerate(agents)}
        agent_id_to_name = {agent.id: agent.name for agent in agents}

        # Process fields based on their position in the sequence
        for field_name, field_sources in all_fields.items():
            # Always share messages field
            if field_name == "messages":
                _, _, ftype, finfo = field_sources[0]
                composer.add_field(
                    field_name,
                    ftype,
                    default_factory=(
                        finfo.default_factory
                        if hasattr(finfo, "default_factory")
                        else list
                    ),
                    shared=True,
                    reducer=add_messages,
                )
                continue

            # Determine which agents use this field
            agent_indices = []
            for agent_id, fname, ftype, finfo in field_sources:
                if agent_id in agent_id_to_idx:
                    agent_indices.append(agent_id_to_idx[agent_id])

            if not agent_indices:
                continue

            min_idx = min(agent_indices)
            max_idx = max(agent_indices)

            # Use first occurrence for type info
            _, _, ftype, finfo = field_sources[0]

            # Determine if field should be required
            is_required = False

            # Check if this is an input field for the first agent
            if min_idx == 0:
                first_agent = agents[0]
                # Check if it's in the first agent's input fields
                for engine_name, mapping in engine_io_mappings.items():
                    if engine_name.startswith(
                        first_agent.name.lower().replace(" ", "_")
                    ):
                        if field_name in mapping.get("inputs", []):
                            is_required = True
                            break

            # Add field with appropriate optionality
            if hasattr(finfo, "default_factory"):
                composer.add_field(
                    field_name,
                    ftype,
                    default_factory=finfo.default_factory,
                    shared=(
                        len(set(agent_indices)) > 1
                    ),  # Share if multiple agents use it
                )
            else:
                # Make intermediate fields optional by providing a default
                default_value = finfo.default if hasattr(finfo, "default") else None
                if not is_required and default_value is None:
                    # Make it optional by wrapping in Optional if not already
                    from typing import Optional as Opt
                    from typing import get_origin

                    if get_origin(ftype) is not Opt:
                        ftype = Opt[ftype]

                composer.add_field(
                    field_name,
                    ftype,
                    default=default_value,
                    shared=(len(set(agent_indices)) > 1),
                )

    @staticmethod
    def _apply_hierarchical_mode(
        composer: SchemaComposer, all_fields: Dict, agents: List["Agent"]
    ):
        """Apply hierarchical mode for parent-child agent relationships."""
        # For now, just use smart separation
        # TODO: Implement proper hierarchical logic
        AgentSchemaComposer._apply_smart_separation(composer, all_fields, agents)
