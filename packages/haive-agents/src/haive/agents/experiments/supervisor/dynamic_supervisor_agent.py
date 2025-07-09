"""Dynamic Supervisor Agent - A proper Agent implementation for dynamic agent management.

This agent implements the supervisor pattern with:
- supervisor node: decides which agent to execute
- agent_execution node: executes any agent from state (like tool_node pattern)
- Routes: supervisor → (agent_execution | add_agent | END)
"""

import logging
from typing import Any, Literal

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent

# Import our working components
from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    create_agent_execution_node,
)

logger = logging.getLogger(__name__)

# Supervisor system message with dynamic agent list from state
SUPERVISOR_SYSTEM_MESSAGE = """You are an intelligent task supervisor that routes tasks to specialized agents.

Available agents:
{agent_list}

You have access to handoff tools that let you delegate work to the appropriate agents. 
Look at the available tools and use the one that best matches the user's request.

When routing:
- Use handoff tools to transfer work to the right specialist based on their capabilities
- Provide clear task instructions when handing off
- If no agent is suitable, use 'choose_agent' tool to select "END"
- If you need a new agent, provide specifications and context for what's needed

Always respond with:
1. Your routing decision and reasoning
2. The specific task for the selected agent
3. Any additional context or requirements
"""


from haive.agents.simple.agent import SimpleAgent


class DynamicSupervisorAgent(SimpleAgent):
    """Dynamic supervisor agent that extends SimpleAgent.

    Uses SimpleAgent's engine node pattern but modifies routing to handle
    handoff tools that route to agent execution nodes.
    """

    # Override state schema to use our supervisor state
    state_schema_override: type = Field(
        default=SupervisorStateWithTools,
        description="Use supervisor state schema with dynamic agent management",
    )

    def setup_agent(self) -> None:
        """Setup the supervisor - sync state schema and tools."""
        # Call parent setup first
        super().setup_agent()

        # Force use of our supervisor state schema
        self.state_schema = SupervisorStateWithTools
        self.input_schema = SupervisorStateWithTools

    def build_graph(self) -> BaseGraph:
        """Build supervisor graph - extend SimpleAgent graph with agent execution routing."""
        # Build base SimpleAgent graph first
        graph = super().build_graph()

        # Add agent execution node to handle handoff tools
        agent_execution_node = create_agent_execution_node()
        graph.add_node("agent_execution", agent_execution_node)

        # Route agent_execution back to agent_node like ReactAgent does with tools
        graph.add_edge("agent_execution", "agent_node")

        # TODO: Add custom routing logic in tool_node to handle handoff tools
        # Handoff tools should route to agent_execution instead of back to agent_node

        return graph


def create_supervisor_agent(
    name: str = "supervisor", engine=None
) -> DynamicSupervisorAgent:
    """Create a configured supervisor agent."""
    return DynamicSupervisorAgent(
        name=name,
        engine=engine,
        description="Dynamic supervisor agent for routing tasks to specialized agents",
    )
