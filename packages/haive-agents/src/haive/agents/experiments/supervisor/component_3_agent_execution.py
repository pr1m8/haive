"""Component 3: Agent execution node that mirrors tool_node pattern."""

import logging
from typing import Any, Dict, Optional

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)

logger = logging.getLogger(__name__)


class AgentExecutionNode:
    """Agent execution node that mirrors the tool_node pattern.

    Key insight: Just like tool_node reads from engine.tools at runtime,
    this node reads from state.agents at runtime to execute any agent.
    """

    def __init__(self, name: str = "agent_execution"):
        self.name = name

    def __call__(self, state: SupervisorStateWithTools) -> dict[str, Any]:
        """Execute agent based on state routing - mirrors tool_node pattern.

        This is the core pattern that enables dynamic supervisor:
        1. Read state.next_agent (like tool_node reads tool name from state)
        2. Get agent from state.agents[agent_name] (like tool_node gets tool from engine.tools)
        3. Execute agent.arun(state.agent_task) (like tool_node executes tool)
        4. Return response (like tool_node returns tool result)
        """
        logger.info(f"🎯 Agent Execution Node: {self.name}")

        # 1. Get routing from state (like tool_node gets tool name)
        agent_name = state.next_agent
        task = state.agent_task

        logger.info(f"  Target agent: {agent_name}")
        logger.info(f"  Task: {task[:100]}...")

        # 2. Validate agent exists in state
        if not agent_name or agent_name not in state.agents:
            error_msg = f"Agent '{agent_name}' not found in state.agents"
            logger.error(f"❌ {error_msg}")
            available = list(state.agents.keys())
            logger.info(f"  Available agents: {available}")

            return {
                "agent_response": f"Error: {error_msg}. Available: {available}",
                "next_agent": None,
                "agent_task": "",
            }

        # 3. Get agent from state (like tool_node gets tool from engine.tools)
        agent_info = state.agents[agent_name]

        # Handle both AgentInfo objects and dict representations
        if isinstance(agent_info, dict):
            logger.info("  Agent info type: dict")
            agent = agent_info.get("agent") or agent_info["agent"]
            is_active = agent_info.get("active", True)
        else:
            logger.info(f"  Agent info type: {type(agent_info).__name__}")
            agent = agent_info.get_agent()
            is_active = agent_info.is_active()

        logger.info(f"  Agent type: {type(agent) if agent else 'None'}")
        logger.info(f"  Agent active: {is_active}")

        # 4. Check if agent is active
        if not is_active:
            logger.warning(f"⚠️ Agent '{agent_name}' is inactive")
            return {
                "agent_response": f"Agent '{agent_name}' is currently inactive",
                "next_agent": None,
                "agent_task": "",
            }

        try:
            # 5. Execute agent with task (like tool_node executes tool)
            logger.info(f"🚀 Executing agent '{agent_name}'...")

            # Use sync execution
            if hasattr(agent, "run"):
                result = agent.run(task)
            elif hasattr(agent, "invoke"):
                # For sync execution, we need to provide proper input format
                if hasattr(agent, "state_schema"):
                    # Create proper state for agent
                    agent_input = agent.state_schema(
                        messages=[{"role": "user", "content": task}]
                    )
                    result = agent.invoke(agent_input)
                else:
                    # Simple string input
                    result = agent.invoke({"input": task})
            else:
                raise AttributeError(
                    f"Agent {agent_name} has no 'arun' or 'invoke' method"
                )

            logger.info(f"✅ Agent '{agent_name}' completed successfully")
            logger.info(f"  Result type: {type(result).__name__}")

            # Extract response from result
            if isinstance(result, dict):
                # Look for common response fields
                response = (
                    result.get("output")
                    or result.get("response")
                    or result.get("answer")
                    or str(result)
                )
            elif isinstance(result, str):
                response = result
            else:
                response = str(result)

            # 6. Return state update (like tool_node returns tool result)
            return {
                "agent_response": response,
                "next_agent": None,  # Clear routing after execution
                "agent_task": "",  # Clear task after execution
                # Could also add metadata about execution
                "last_executed_agent": agent_name,
                "execution_success": True,
            }

        except Exception as e:
            logger.exception(f"❌ Error executing agent '{agent_name}': {e}")
            logger.exception("Full traceback:")

            # Return error state
            return {
                "agent_response": f"Error executing {agent_name}: {e!s}",
                "next_agent": None,
                "agent_task": "",
                "last_executed_agent": agent_name,
                "execution_success": False,
                "execution_error": str(e),
            }

    def __str__(self):
        return f"AgentExecutionNode({self.name})"

    def __repr__(self):
        return self.__str__()


# Convenience function for creating node
def create_agent_execution_node(name: str = "agent_execution") -> AgentExecutionNode:
    """Create an agent execution node."""
    return AgentExecutionNode(name=name)


# Sync version for non-async contexts
class SyncAgentExecutionNode:
    """Synchronous version of agent execution node."""

    def __init__(self, name: str = "agent_execution"):
        self.name = name

    def __call__(self, state: SupervisorStateWithTools) -> dict[str, Any]:
        """Sync version - calls agents using invoke instead of arun."""
        logger.info(f"🎯 Sync Agent Execution Node: {self.name}")

        agent_name = state.next_agent
        task = state.agent_task

        if not agent_name or agent_name not in state.agents:
            return {
                "agent_response": f"Agent '{agent_name}' not found",
                "next_agent": None,
                "agent_task": "",
            }

        agent_info = state.agents[agent_name]
        agent = agent_info.get_agent()

        if not agent_info.is_active():
            return {
                "agent_response": f"Agent '{agent_name}' is inactive",
                "next_agent": None,
                "agent_task": "",
            }

        try:
            # Sync execution using invoke
            if hasattr(agent, "invoke"):
                # Try to create proper input for agent
                if hasattr(agent, "state_schema"):
                    try:
                        # Create state with messages
                        agent_input = {"messages": [{"role": "user", "content": task}]}
                        result = agent.invoke(agent_input)
                    except Exception:
                        # Fallback to simple input
                        result = agent.invoke({"input": task})
                else:
                    result = agent.invoke({"input": task})
            else:
                return {
                    "agent_response": f"Agent {agent_name} not invokable",
                    "next_agent": None,
                    "agent_task": "",
                }

            # Extract response
            if isinstance(result, dict):
                response = result.get("output") or result.get("response") or str(result)
            else:
                response = str(result)

            return {
                "agent_response": response,
                "next_agent": None,
                "agent_task": "",
                "last_executed_agent": agent_name,
                "execution_success": True,
            }

        except Exception as e:
            logger.exception(f"Error executing {agent_name}: {e}")
            return {
                "agent_response": f"Error: {e!s}",
                "next_agent": None,
                "agent_task": "",
                "execution_error": str(e),
            }
