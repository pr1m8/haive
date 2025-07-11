# haive/agents/multi/agent_node.py
"""Agent-specific node configurations for multi-agent systems.

This module provides node configurations that properly handle:
- Agent state isolation and merging
- Private state schema management
- Agent coordination through meta state
"""

import logging
from typing import Any, Dict, List, Literal, Optional, Type, Union

from haive.agents.base.agent import Agent
from langchain_core.messages import BaseMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

from haive.core.engine.base import EngineType
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class AgentNodeConfig(EngineNodeConfig):
    """Node configuration specifically for agents in multi-agent systems.

    This extends EngineNodeConfig to:
    - Properly handle agent as the engine
    - Manage private agent state schemas
    - Coordinate through meta state
    - Handle state transformation between global and agent-specific schemas
    """

    # Override engine to be agent
    engine: Agent = Field(description="The agent to execute")

    # Agent-specific fields
    private_state_schema: type[BaseModel] | None = Field(
        default=None, description="Private state schema for this agent"
    )

    # State transformation
    extract_private_state: bool = Field(
        default=True,
        description="Whether to extract agent's private state before execution",
    )
    merge_agent_output: bool = Field(
        default=True, description="Whether to merge agent output back to global state"
    )

    # Meta state tracking
    update_meta_state: bool = Field(
        default=True,
        description="Whether to update meta state with agent execution info",
    )

    def __init__(self, **data):
        """Initialize with agent as engine."""
        # Ensure we have an agent
        if "agent" in data and "engine" not in data:
            data["engine"] = data.pop("agent")

        # Set node type to CALLABLE (agents are callable)
        if "node_type" not in data:
            data["node_type"] = NodeType.CALLABLE

        super().__init__(**data)

    def __call__(
        self,
        state: dict[str, Any] | BaseModel,
        config: RunnableConfig | None = None,
    ) -> dict[str, Any]:
        """Execute the agent with proper state management.

        This method:
        1. Updates meta state to track agent start
        2. Extracts relevant fields for agent's private schema
        3. Executes the agent
        4. Merges results back to global state
        5. Updates meta state with completion info
        """
        logger.info("=" * 80)
        logger.info(f"AGENT NODE EXECUTION: {self.name}")
        logger.info("=" * 80)

        agent = self.engine
        agent_id = getattr(agent, "id", agent.name)
        agent_name = getattr(agent, "name", agent.__class__.__name__)

        logger.info("Step 1: Agent Details")
        logger.info(f"  Agent Name: {agent_name}")
        logger.info(f"  Agent ID: {agent_id}")
        logger.info(f"  Agent Type: {type(agent).__name__}")
        logger.info(
            f"  Has compiled graph: {hasattr(agent, '_app') and agent._app is not None}"
        )

        # Log incoming state
        logger.info("Step 2: Incoming State Analysis")
        logger.info(f"  State type: {type(state).__name__}")

        # Handle both dict and Pydantic model states
        if isinstance(state, dict):
            logger.info(f"  State keys: {list(state.keys())}")
            state_dict = state
        else:
            # It's a Pydantic model, extract actual messages
            logger.info("  State is Pydantic model, extracting messages")
            state_dict = state.model_dump()

            # IMPORTANT: For messages, keep the actual BaseMessage objects, don't serialize them
            if hasattr(state, "messages"):
                original_messages = state.messages
                logger.info(f"INCOMING MESSAGES TYPE: {type(original_messages)}")

                # Get the actual message objects
                if hasattr(original_messages, "root"):
                    # MessageList with root attribute
                    actual_messages = original_messages.root
                    logger.info(f"  Extracted from .root: {type(actual_messages)}")
                elif isinstance(original_messages, list | tuple):
                    # Direct list/tuple of messages
                    actual_messages = list(original_messages)
                    logger.info(f"  Direct list/tuple: {type(actual_messages)}")
                else:
                    # Try to iterate
                    try:
                        actual_messages = list(original_messages)
                        logger.info(f"  Converted to list: {type(actual_messages)}")
                    except:
                        logger.warning(
                            f"Cannot iterate over messages of type {type(original_messages)}"
                        )
                        actual_messages = []

                # Check what we actually got
                logger.info("FINAL MESSAGE TYPES:")
                for i, msg in enumerate(actual_messages):
                    logger.info(
                        f"  Message {i}: {type(msg)} (is BaseMessage: {isinstance(msg, BaseMessage)})"
                    )
                    if isinstance(msg, dict):
                        logger.warning(f"    DICT MESSAGE: {list(msg.keys())}")
                        if "tool_call_id" in msg:
                            logger.info(
                                f"    Dict has tool_call_id: {msg['tool_call_id']}"
                            )
                        else:
                            logger.warning("    Dict missing tool_call_id!")
                    elif hasattr(msg, "tool_call_id"):
                        logger.info(
                            f"    BaseMessage tool_call_id: {getattr(msg, 'tool_call_id', 'None')}"
                        )

                # Keep actual BaseMessage objects - don't serialize them!
                state_dict["messages"] = actual_messages
                logger.info(
                    f"  Extracted {len(actual_messages)} actual message objects"
                )

                # Log message types for debugging
                for i, msg in enumerate(actual_messages):
                    logger.info(f"    Message {i}: {type(msg).__name__}")
                    if isinstance(msg, ToolMessage):
                        logger.info(
                            f"      ToolMessage name: {getattr(msg, 'name', 'None')}"
                        )
                        logger.info(
                            f"      ToolMessage tool_call_id: {getattr(msg, 'tool_call_id', 'None')}"
                        )
                    elif hasattr(msg, "__dict__"):
                        logger.info(f"      Message data: {msg.__dict__}")

            logger.info(f"  State keys: {list(state_dict.keys())}")
            # Update state to be the dict for the rest of the method
            state = state_dict

        for key, value in state_dict.items():
            if isinstance(value, list) and key == "messages":
                logger.info(f"  {key}: {len(value)} messages")
            else:
                value_str = (
                    str(value)[:100] + "..." if len(str(value)) > 100 else str(value)
                )
                logger.info(f"  {key}: {type(value).__name__} = {value_str}")

        # 1. Update meta state - agent starting
        if self.update_meta_state and "meta_state" in state:
            meta_state = state.get("meta_state")
            if meta_state and hasattr(meta_state, "record_agent_start"):
                meta_state.record_agent_start(agent_id, agent_name)

        try:
            # 2. Prepare agent input using agent's own state schema
            logger.info("Step 3: Preparing Agent Input with Agent's Own State Schema")

            # Use agent's own state schema instead of multi-agent composed schema
            if hasattr(agent, "state_schema") and agent.state_schema:
                logger.info(
                    f"  Using agent's own state schema: {agent.state_schema.__name__}"
                )

                # Create agent-specific state from multi-agent state
                agent_state_fields = {}

                # Extract fields that the agent's state schema expects
                for field_name, _field_info in agent.state_schema.model_fields.items():
                    if field_name in state:
                        agent_state_fields[field_name] = state[field_name]
                        logger.debug(
                            f"    Extracted field '{field_name}' for agent state"
                        )

                # IMPORTANT: Ensure engines are included if the agent schema expects them
                if (
                    "engines" in agent.state_schema.model_fields
                    and "engines" not in agent_state_fields
                ):
                    # Use the engines from the parent state if available
                    if state.get("engines"):
                        agent_state_fields["engines"] = state["engines"]
                        logger.debug(
                            f"    Using engines from parent state: {list(state['engines'].keys())}"
                        )
                    elif hasattr(agent, "engines") and agent.engines:
                        # Otherwise use the agent's own engines
                        agent_state_fields["engines"] = agent.engines
                        logger.debug(
                            f"    Using agent's own engines: {list(agent.engines.keys())}"
                        )
                    else:
                        # Empty dict as last resort
                        agent_state_fields["engines"] = {}
                        logger.warning("    No engines found for agent state")

                # Create instance of agent's own state schema
                try:
                    agent_specific_state = agent.state_schema(**agent_state_fields)

                    # Convert to dict for agent input
                    agent_input = agent_specific_state.model_dump()

                    # IMPORTANT: Do NOT override engines with actual engine objects
                    # Keep the serialized version from state to avoid msgpack errors
                    # The engines in agent_input are already properly serialized
                    if agent_input.get("engines"):
                        logger.info(
                            f"    Using serialized engines from state: {list(agent_input['engines'].keys())}"
                        )

                    # IMPORTANT: Also serialize tools to avoid msgpack errors
                    # Tools often contain Pydantic classes in args_schema that can't be serialized
                    if agent_input.get("tools"):
                        serialized_tools = []
                        for tool in agent_input["tools"]:
                            if tool is not None:
                                # Serialize tools to avoid Pydantic class issues
                                if hasattr(tool, "model_dump"):
                                    try:
                                        tool_dict = tool.model_dump(
                                            mode="json", exclude_none=True
                                        )
                                        # Clean up args_schema - it's usually a Pydantic class
                                        if tool_dict.get("args_schema"):
                                            if hasattr(
                                                tool_dict["args_schema"], "__name__"
                                            ):
                                                tool_dict["args_schema"] = (
                                                    f"<PydanticModel:{tool_dict['args_schema'].__name__}>"
                                                )
                                            else:
                                                tool_dict["args_schema"] = None
                                        serialized_tools.append(tool_dict)
                                    except Exception as e:
                                        logger.warning(f"Failed to serialize tool: {e}")
                                        # Fallback: basic tool info
                                        serialized_tools.append(
                                            {
                                                "name": getattr(
                                                    tool, "name", str(tool)
                                                ),
                                                "description": getattr(
                                                    tool, "description", ""
                                                ),
                                                "type": "tool",
                                            }
                                        )
                                else:
                                    # Tool doesn't have model_dump, create basic dict
                                    serialized_tools.append(
                                        {
                                            "name": getattr(tool, "name", str(tool)),
                                            "description": getattr(
                                                tool, "description", ""
                                            ),
                                            "type": "tool",
                                        }
                                    )
                        agent_input["tools"] = serialized_tools
                        logger.info(
                            f"    Serialized {len(serialized_tools)} tools for agent input"
                        )

                    logger.info(
                        "  Created agent-specific state with agent's own tools/schemas"
                    )

                except Exception as e:
                    logger.warning(f"  Could not create agent-specific state: {e}")
                    logger.warning(
                        "  Falling back to prepared input from multi-agent state"
                    )
                    agent_input = self._prepare_agent_input(state, agent)
            else:
                logger.info("  Agent has no state_schema, using prepared input")
                agent_input = self._prepare_agent_input(state, agent)

            logger.info(f"  Final agent input keys: {list(agent_input.keys())}")
            logger.info(f"  Agent input type: {type(agent_input)}")
            logger.info(f"  Is dict: {isinstance(agent_input, dict)}")
            logger.info(f"  Is BaseModel: {isinstance(agent_input, BaseModel)}")

            for key, value in agent_input.items():
                if isinstance(value, list) and key == "messages":
                    logger.info(f"  {key}: {len(value)} messages")
                elif key == "engines" and isinstance(value, dict):
                    logger.info(f"  {key}: dict with {len(value)} engines")
                    for eng_name, eng in value.items():
                        logger.info(
                            f"    - {eng_name}: {type(eng)} (is dict: {isinstance(eng, dict)})"
                        )
                        if hasattr(eng, "tools"):
                            logger.info(
                                f"      Has tools attribute: {len(getattr(eng, 'tools', []))} tools"
                            )
                            for tool in getattr(eng, "tools", [])[
                                :2
                            ]:  # Show first 2 tools
                                logger.info(f"        Tool type: {type(tool)}")
                else:
                    value_str = (
                        str(value)[:100] + "..."
                        if len(str(value)) > 100
                        else str(value)
                    )
                    logger.info(f"  {key}: {type(value).__name__} = {value_str}")

            # 3. Clean agent's engine tools before execution to prevent contamination
            logger.info("Step 4: Cleaning Agent Tools (preventing contamination)")
            original_tools = None
            original_tool_routes = None

            if hasattr(agent, "engine") and agent.engine:
                engine = agent.engine

                # Backup original tools
                if hasattr(engine, "tools"):
                    original_tools = engine.tools.copy() if engine.tools else []
                    logger.info(
                        f"  Original tools: {[getattr(t, 'name', str(t)) for t in original_tools]}"
                    )

                if hasattr(engine, "tool_routes"):
                    original_tool_routes = (
                        engine.tool_routes.copy() if engine.tool_routes else {}
                    )

                # Filter tools to only include legitimate ones (not Pydantic models)
                if hasattr(engine, "tools") and engine.tools:
                    clean_tools = []
                    clean_routes = {}

                    for tool in engine.tools:
                        tool_name = getattr(
                            tool, "name", getattr(tool, "__name__", str(tool))
                        )

                        # Skip Pydantic model classes that shouldn't be in tools
                        if hasattr(tool, "__bases__") and any(
                            "BaseModel" in str(base) for base in tool.__bases__
                        ):
                            logger.info(
                                f"  Filtering OUT Pydantic model from engine tools: {tool_name}"
                            )
                            continue

                        # Skip non-callable items
                        if isinstance(tool, type) and hasattr(tool, "model_fields"):
                            logger.info(
                                f"  Filtering OUT Pydantic model class from engine tools: {tool_name}"
                            )
                            continue

                        # Keep legitimate tools
                        if callable(tool) or hasattr(tool, "invoke"):
                            clean_tools.append(tool)
                            if (
                                original_tool_routes
                                and tool_name in original_tool_routes
                            ):
                                clean_routes[tool_name] = original_tool_routes[
                                    tool_name
                                ]
                            logger.info(f"  Keeping legitimate tool: {tool_name}")

                    # Apply cleaned tools to engine
                    engine.tools = clean_tools
                    if hasattr(engine, "tool_routes"):
                        engine.tool_routes = clean_routes

                    logger.info(
                        f"  Cleaned tools: {[getattr(t, 'name', str(t)) for t in clean_tools]}"
                    )
                    logger.info(f"  Cleaned routes: {list(clean_routes.keys())}")

            # 4. Execute agent with clean tools
            logger.info("Step 5: Executing Agent")
            logger.info(
                f"  Method: {'compiled graph' if hasattr(agent, '_app') and agent._app else 'invoke method'}"
            )

            try:
                # Check if agent has compiled graph
                if hasattr(agent, "_app") and agent._app:
                    # Use compiled graph
                    logger.info("  Using agent's compiled graph (_app)")
                    result = agent._app.invoke(agent_input, config)
                else:
                    # Use agent's invoke method
                    logger.info("  Using agent's invoke method")
                    logger.info(
                        f"  About to invoke agent with input type: {type(agent_input)}"
                    )
                    logger.info(f"  Input is dict: {isinstance(agent_input, dict)}")
                    logger.info(
                        f"  Input is BaseModel: {isinstance(agent_input, BaseModel)}"
                    )
                    if isinstance(agent_input, dict) and "engines" in agent_input:
                        logger.info(
                            f"  Engines in input: {list(agent_input['engines'].keys())}"
                        )
                        for eng_name, eng in agent_input["engines"].items():
                            logger.info(f"    Engine {eng_name} type: {type(eng)}")
                    result = agent.invoke(agent_input, config)
            finally:
                # Restore original tools after execution
                if (
                    original_tools is not None
                    and hasattr(agent, "engine")
                    and agent.engine
                ):
                    agent.engine.tools = original_tools
                    if original_tool_routes is not None and hasattr(
                        agent.engine, "tool_routes"
                    ):
                        agent.engine.tool_routes = original_tool_routes
                    logger.debug("  Restored original tools after execution")

            logger.info("Step 5: Agent Result Analysis")
            logger.info(f"  Result type: {type(result).__name__}")
            if isinstance(result, dict):
                logger.info(f"  Result keys: {list(result.keys())}")
                for key, value in result.items():
                    if isinstance(value, list) and key in [
                        "messages",
                        "retrieved_documents",
                    ]:
                        logger.info(f"  {key}: {len(value)} items")
                    else:
                        value_str = (
                            str(value)[:100] + "..."
                            if len(str(value)) > 100
                            else str(value)
                        )
                        logger.info(f"  {key}: {type(value).__name__}")

            # 4. Process agent output
            logger.info("Step 6: Processing Agent Output")
            state_update = self._process_agent_output(result, state, agent)

            logger.info(f"  State update keys: {list(state_update.keys())}")

            # 5. Update meta state - agent completed
            if self.update_meta_state and "meta_state" in state:
                meta_state = state.get("meta_state")
                if meta_state and hasattr(meta_state, "record_agent_completion"):
                    meta_state.record_agent_completion(agent_id, result)

            logger.info(f"✅ AGENT NODE COMPLETED: {self.name}")
            return state_update

        except Exception as e:
            logger.exception(f"❌ Error executing agent {agent_name}: {e}")
            logger.exception(f"Error type: {type(e).__name__}")
            import traceback

            logger.exception(f"Traceback:\n{traceback.format_exc()}")

            # Update meta state - agent error
            if self.update_meta_state and "meta_state" in state:
                meta_state = state.get("meta_state")
                if meta_state and hasattr(meta_state, "record_agent_error"):
                    meta_state.record_agent_error(agent_id, str(e))

            raise

    def _prepare_agent_input(
        self, state: dict[str, Any], agent: Agent
    ) -> dict[str, Any]:
        """Prepare input for agent execution.

        If agent has a private state schema, extract only relevant fields.
        Otherwise, pass appropriate fields based on agent's input schema.
        """
        logger.debug("=== _prepare_agent_input called ===")
        logger.debug(f"  Agent: {agent.name}")
        logger.debug(f"  Private state schema: {self.private_state_schema}")
        logger.debug(f"  Extract private state: {self.extract_private_state}")
        logger.debug(f"  Has input_schema: {hasattr(agent, 'input_schema')}")
        if hasattr(agent, "input_schema"):
            logger.debug(f"  Input schema type: {type(agent.input_schema)}")
            logger.debug(f"  Input schema: {agent.input_schema}")

        # If we have a private state schema, use it
        if self.private_state_schema and self.extract_private_state:
            logger.debug(f"Using private state extraction for {agent.name}")

            # Create instance of private schema from global state
            relevant_fields = {}
            for field_name in self.private_state_schema.model_fields:
                if field_name in state:
                    relevant_fields[field_name] = state[field_name]

            # Always include messages if available
            if "messages" in state and "messages" not in relevant_fields:
                relevant_fields["messages"] = state["messages"]

            return relevant_fields

        # Otherwise, use agent's input schema or heuristics
        if hasattr(agent, "input_schema") and agent.input_schema:
            logger.debug("Using agent's input_schema")
            logger.debug(
                f"  Input schema fields: {list(agent.input_schema.model_fields.keys())}"
            )

            # Extract fields based on input schema
            input_fields = {}
            for field_name in agent.input_schema.model_fields:
                if field_name in state:
                    input_fields[field_name] = state[field_name]
                    logger.debug(f"  Added field '{field_name}' from state")
                else:
                    logger.debug(f"  Field '{field_name}' not found in state")

            logger.debug(f"  Final input fields: {list(input_fields.keys())}")
            return input_fields

        # Default: pass messages and any fields the agent expects
        default_input = {}

        # Always include messages for agents
        if "messages" in state:
            default_input["messages"] = state["messages"]

        # Include common fields agents might need
        common_fields = ["query", "question", "input", "context", "documents"]
        for field in common_fields:
            if field in state:
                default_input[field] = state[field]

        # If agent has get_input_fields method, use it
        if hasattr(agent, "get_input_fields"):
            try:
                expected_fields = agent.get_input_fields()
                for field_name in expected_fields:
                    if field_name in state:
                        default_input[field_name] = state[field_name]
            except Exception as e:
                logger.debug(f"Could not get input fields from agent: {e}")

        logger.debug(f"  Final default input: {list(default_input.keys())}")
        return default_input if default_input else state

    def _process_agent_output(
        self, result: Any, state: dict[str, Any], agent: Agent
    ) -> dict[str, Any]:
        """Process agent output and merge with global state.

        Handles various output formats and ensures proper state updates.
        """
        # Start with empty update
        state_update = {}

        # Handle different result types
        if isinstance(result, dict):
            # Direct dictionary result
            state_update = result
        elif isinstance(result, BaseModel):
            # Pydantic model result - preserve actual message objects
            state_update = result.model_dump()

            # CRITICAL: If the result has messages, preserve the actual BaseMessage objects
            if hasattr(result, "messages") and result.messages:
                logger.info(
                    f"Preserving {len(result.messages)} actual message objects from agent result"
                )

                # Debug: Check what types the messages actually are
                for i, msg in enumerate(result.messages):
                    logger.info(f"  Result message {i}: {type(msg).__name__}")
                    if isinstance(msg, ToolMessage):
                        logger.info(
                            f"    ToolMessage tool_call_id: {getattr(msg, 'tool_call_id', 'None')}"
                        )
                    elif isinstance(msg, dict):
                        logger.warning(f"    Message is dict, not BaseMessage: {msg}")

                # Keep the actual BaseMessage objects instead of serialized dicts
                state_update["messages"] = result.messages
                logger.info(
                    "STATE UPDATE: Setting messages to actual BaseMessage objects"
                )
                for i, msg in enumerate(result.messages):
                    if hasattr(msg, "tool_call_id"):
                        logger.info(
                            f"  Storing ToolMessage {i} with tool_call_id={getattr(msg, 'tool_call_id', 'None')}"
                        )
        elif isinstance(result, str):
            # String result - check if agent outputs to specific field
            if hasattr(agent, "output_field_name"):
                state_update[agent.output_field_name] = result
            else:
                # Default to agent_output field
                state_update["agent_output"] = result
        elif result is None:
            # No output
            logger.debug(f"Agent {agent.name} returned None")
        else:
            # Unknown type - store as agent_output
            logger.warning(f"Unknown result type from agent: {type(result)}")
            state_update["agent_output"] = result

        # Store agent-specific output in meta state
        if self.update_meta_state and "meta_state" in state:
            agent_id = getattr(agent, "id", agent.name)
            # Store in agent_outputs field
            if "agent_outputs" not in state_update:
                state_update["agent_outputs"] = state.get("agent_outputs", {})
            state_update["agent_outputs"][agent_id] = result

        # Ensure messages are preserved/updated correctly
        if "messages" in state_update and "messages" in state:
            # If both have messages, we need to handle carefully
            existing_messages = state.get("messages", [])
            new_messages = state_update.get("messages", [])

            # Simple approach: if new messages is a complete replacement, use it
            # Otherwise, assume we should append
            if isinstance(new_messages, list) and isinstance(existing_messages, list):
                if len(new_messages) >= len(existing_messages):
                    # Looks like a complete replacement - use new messages as-is
                    state_update["messages"] = new_messages
                else:
                    # Looks like just new messages to append
                    state_update["messages"] = existing_messages + new_messages

        return state_update


class CoordinatorNodeConfig(NodeConfig):
    """Coordinator node for parallel agent execution.

    Handles fan-out and aggregation of parallel agent execution.
    """

    node_type: NodeType = Field(
        default=NodeType.CALLABLE, description="Coordinator is a callable node"
    )

    agents: list[Agent] = Field(description="Agents to coordinate")

    mode: Literal["fanout", "aggregate"] = Field(description="Coordination mode")

    def __call__(
        self, state: dict[str, Any], config: RunnableConfig | None = None
    ) -> dict[str, Any] | list[dict[str, Any]]:
        """Execute coordination logic.

        For fanout: Returns list of states for each agent
        For aggregate: Combines results from all agents
        """
        if self.mode == "fanout":
            # Create individual states for each agent
            logger.info("Fanning out to parallel agents")

            # Mark agents as ready for parallel execution
            if "meta_state" in state:
                meta_state = state.get("meta_state")
                if meta_state and hasattr(meta_state, "update_workflow_stage"):
                    meta_state.update_workflow_stage("parallel_execution")

            # For now, just return the state - the graph edges handle routing
            # In the future, we can use Send commands with proper annotations
            return state

        if self.mode == "aggregate":
            # Aggregate results from parallel execution
            logger.info("Aggregating results from parallel agents")

            # The state should have agent_outputs populated
            if "agent_outputs" in state:
                logger.debug(f"Found outputs from {len(state['agent_outputs'])} agents")

            # Update workflow stage
            if "meta_state" in state:
                meta_state = state.get("meta_state")
                if meta_state and hasattr(meta_state, "update_workflow_stage"):
                    meta_state.update_workflow_stage("aggregation_complete")

            return state

        raise ValueError(f"Unknown coordination mode: {self.mode}")


# Update engine_node.py to route agents to AgentNodeConfig
def create_node_for_engine(
    engine: Agent | Any, name: str, **kwargs
) -> AgentNodeConfig | EngineNodeConfig:
    """Factory function to create appropriate node config for an engine/agent.

    Routes agents to AgentNodeConfig, others to EngineNodeConfig.
    """
    # Check if it's an agent
    if isinstance(engine, Agent) or (
        hasattr(engine, "engine_type") and engine.engine_type == EngineType.AGENT
    ):
        return AgentNodeConfig(name=name, engine=engine, **kwargs)
    return EngineNodeConfig(name=name, engine=engine, **kwargs)
