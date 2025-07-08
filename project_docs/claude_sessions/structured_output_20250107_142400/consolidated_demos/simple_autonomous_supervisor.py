#!/usr/bin/env python3
"""Simple demo showing how a supervisor can autonomously create agents."""

import logging

from haive.agents.experiments.dynamic_supervisor import DynamicSupervisorAgent
from haive.agents.simple.agent import SimpleAgent
from langchain_core.tools import tool

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def add_self_modification_tool(supervisor: DynamicSupervisorAgent):
    """Add a tool that lets the supervisor create new agents."""

    @tool
    def create_specialized_agent(
        agent_name: str, agent_purpose: str, agent_expertise: str
    ) -> str:
        """Create a new specialized agent and add it to the supervisor.

        Args:
            agent_name: Internal name for the agent (e.g., 'coding_agent')
            agent_purpose: What the agent does (e.g., 'writes and debugs code')
            agent_expertise: The agent's system prompt/expertise

        Returns:
            Confirmation message
        """
        try:
            # Add the new agent to supervisor's registry
            supervisor.add_agent_to_registry(
                name=agent_name,
                description=agent_purpose,
                agent_class=SimpleAgent,
                config={
                    "name": agent_name.replace("_", " ").title(),
                    "system_message": agent_expertise,
                },
            )

            return f"✅ Successfully created {agent_name}! You can now use 'handoff_to_{agent_name}' to delegate tasks to this agent."

        except Exception as e:
            return f"❌ Error creating agent: {e!s}"}"

    # Add this tool to the supervisor
    supervisor.tools.append(create_specialized_agent)

    # Update system message to explain the capability
    supervisor.system_message = """You are an autonomous supervisor that can create specialized agents as needed.

When you receive a task:
1. First check if you have a suitable agent using 'list_agents'
2. If no suitable agent exists, create one using 'create_specialized_agent'
3. Then delegate the task using the appropriate 'handoff_to_X' tool

For example:
- For coding tasks → create a coding_agent
- For writing tasks → create a writing_age  
- For data analysis → create a data_agent

Always think about what type of specialist would best handle the task."""


def demo():
    """Demonstrate autonomous agent creation."""

    # Create supervisor
    supervisor = DynamicSupervisorAgent(name="Autonomous Supervisor", debug=True)

    # Add self-modification capability
    add_self_modification_tool(supervisor)

    for tool in supervisor.tools:
        if tool.name in ["list_agents", "create_specialized_agent", "end_supervision"]:
            pass



    # Save the configuration
    config = {
        "supervisor_name": supervisor.name,
        "total_tools": len(supervisor.tools),
        "self_modification_enabled": True,
        "initial_agents": list(supervisor.agent_registry.list_agents().keys()),
    }

    with open("/tmp/autonomous_supervisor_config.json", "w") as f:
        import json

        json.dump(config, f, indent=2)


    return supervisor


if __name__ == "__main__":
    supervisor = demo()


