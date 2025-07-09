"""Dynamic Executor Node for Dynamic Supervisor.

This node dynamically executes agents by name, properly handling state extraction
and merging based on the EngineNode/AgentNode patterns.
"""

import logging
from typing import Any, Dict, Optional, Union

from langchain_core.messages import BaseMessage
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class DynamicExecutorNode:
    """Node that dynamically executes agents by name with proper state handling."""

    def __init__(self, agent_registry: Dict[str, Any]):
        """Initialize with agent registry.

        Args:
            agent_registry: Dictionary mapping agent names to agent instances
        """
        self.agent_registry = agent_registry

    async def __call__(
        self,
        state: Union[Dict[str, Any], BaseModel],
        config: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the targeted agent with proper state extraction.

        This follows the pattern from AgentNode:
        1. Get target agent name from state
        2. Extract fields for agent's state schema
        3. Execute agent
        4. Merge results back
        """
        logger.info("=" * 60)
        logger.info("DYNAMIC EXECUTOR NODE")
        logger.info("=" * 60)

        # Convert state to dict if needed
        if isinstance(state, BaseModel):
            state_dict = state.model_dump()

            # Preserve actual BaseMessage objects (critical!)
            if hasattr(state, "messages"):
                messages = getattr(state, "messages")
                if hasattr(messages, "root"):
                    state_dict["messages"] = messages.root
                else:
                    state_dict["messages"] = list(messages)
        else:
            state_dict = state

        # Get target agent name
        target_agent_name = state_dict.get("target_agent", state_dict.get("next_agent"))

        if not target_agent_name:
            logger.error("No target agent specified in state")
            return {"error": "No target agent specified"}

        logger.info(f"Target agent: {target_agent_name}")

        # Get agent from registry
        agent = self.agent_registry.get(target_agent_name)

        if not agent:
            logger.error(f"Agent '{target_agent_name}' not found in registry")
            return {"error": f"Agent '{target_agent_name}' not found"}

        logger.info(f"Found agent: {type(agent).__name__}")

        try:
            # Prepare agent input based on agent's state schema
            agent_input = self._prepare_agent_input(agent, state_dict)

            # Execute agent
            logger.info(f"Executing agent {target_agent_name}...")

            # Check if agent has async invoke
            if hasattr(agent, "ainvoke"):
                result = await agent.ainvoke(agent_input, config)
            elif hasattr(agent, "invoke"):
                result = agent.invoke(agent_input, config)
            else:
                # Try calling directly
                result = await agent(agent_input, config)

            logger.info(f"Agent execution complete")

            # Process result
            update = self._process_agent_result(result, state_dict, target_agent_name)

            return update

        except Exception as e:
            logger.error(f"Error executing agent {target_agent_name}: {e}")
            import traceback

            traceback.print_exc()

            return {
                "error": str(e),
                "last_agent": target_agent_name,
                "agent_execution_failed": True,
            }

    def _prepare_agent_input(self, agent: Any, state: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare input for agent based on its state schema.

        Following AgentNode pattern:
        - Use agent's own state schema
        - Extract only fields the agent expects
        - Preserve message objects
        """
        logger.info("Preparing agent input...")

        # If agent has state_schema, use it
        if hasattr(agent, "state_schema") and agent.state_schema:
            logger.info(f"Using agent's state schema: {agent.state_schema.__name__}")

            agent_input = {}

            # Extract fields the agent expects
            for field_name in agent.state_schema.model_fields:
                if field_name in state:
                    agent_input[field_name] = state[field_name]
                    logger.debug(f"  Extracted field: {field_name}")

            # Ensure engines if needed
            if (
                "engines" in agent.state_schema.model_fields
                and "engines" not in agent_input
            ):
                if "engines" in state:
                    agent_input["engines"] = state["engines"]
                elif hasattr(agent, "engines"):
                    agent_input["engines"] = agent.engines
                else:
                    agent_input["engines"] = {}

            return agent_input

        # Fallback: common agent fields
        logger.info("No state schema, using common fields")

        agent_input = {}

        # Always include messages if present
        if "messages" in state:
            agent_input["messages"] = state["messages"]
            logger.info(f"  Included {len(state['messages'])} messages")

        # Include other common fields
        common_fields = ["query", "context", "documents", "tools", "engines"]
        for field in common_fields:
            if field in state:
                agent_input[field] = state[field]
                logger.debug(f"  Included field: {field}")

        # If agent needs full state (like multi-agents), give it
        if hasattr(agent, "requires_full_state") and agent.requires_full_state:
            logger.info("Agent requires full state")
            return state

        return agent_input

    def _process_agent_result(
        self, result: Any, state: Dict[str, Any], agent_name: str
    ) -> Dict[str, Any]:
        """Process agent result and create state update.

        Following EngineNode pattern for result wrapping.
        """
        logger.info("Processing agent result...")
        logger.info(f"Result type: {type(result).__name__}")

        update = {"last_agent": agent_name, "agent_execution_complete": True}

        # If result is already a dict with state updates
        if isinstance(result, dict):
            logger.info("Result is dict, merging updates")
            update.update(result)

            # Log what we're updating
            for key in result:
                if key == "messages" and isinstance(result[key], list):
                    logger.info(f"  Updating messages: {len(result[key])} items")
                else:
                    logger.debug(f"  Updating {key}")

        # If result has messages attribute
        elif hasattr(result, "messages"):
            logger.info("Result has messages attribute")
            update["messages"] = result.messages

        # If result is a BaseMessage
        elif isinstance(result, BaseMessage):
            logger.info("Result is a BaseMessage, appending to messages")
            current_messages = state.get("messages", [])
            update["messages"] = current_messages + [result]

        # If result is a string (raw response)
        elif isinstance(result, str):
            logger.info("Result is string, creating AIMessage")
            from langchain_core.messages import AIMessage

            current_messages = state.get("messages", [])
            update["messages"] = current_messages + [AIMessage(content=result)]

        # Store raw result for inspection
        update["last_agent_result"] = result

        return update


def create_dynamic_executor_node(agent_registry: Dict[str, Any]) -> DynamicExecutorNode:
    """Factory function to create a dynamic executor node.

    Args:
        agent_registry: Dictionary mapping agent names to agent instances

    Returns:
        DynamicExecutorNode instance
    """
    return DynamicExecutorNode(agent_registry)
