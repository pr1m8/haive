#!/usr/bin/env python3
"""Debug Supervisor Demo - Simple demonstration with debug=True.

This shows the dynamic supervisor working with detailed debug output.
"""

import asyncio
import logging

from haive.agents.experiments.dynamic_supervisor import (
    DynamicSupervisorAgent,
    create_test_registry,
)

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def demo_supervisor_with_debug():
    """Simple demonstration of supervisor with debug=True."""

    # Create supervisor with debug enabled
    registry = create_test_registry()
    supervisor = DynamicSupervisorAgent(
        name="Debug Demo Supervisor",
        agent_registry=registry,
        debug=True,  # This enables debug mode
    )


    # Show initial tools
    for i, tool in enumerate(supervisor.tools, 1):

    # Show agent registry
    agents = supervisor.agent_registry.list_agents()
    for name, info in agents.items():

    # Demonstrate dynamic tool addition
    from haive.agents.simple.agent import SimpleAgent

    supervisor.add_agent_to_registry(
        name="writing_agent",
        description="Creative writing and content generation specialist",
        agent_class=SimpleAgent,
        config={
            "name": "Writing Agent",
            "system_message": "You are a creative writing assistant.",
        },
    )


    # Show new tools
    handoff_tools = [t for t in supervisor.tools if t.name.startswith("handoff_to_")]
    for tool in handoff_tools:
        pass")

    # Test list_agents tool
    list_tool = next(t for t in supervisor.tools if t.name == "list_agents")
    result = list_tool.invoke({})

    # Show state schema
    state_schema = supervisor.state_schema


    return supervisor


if __name__ == "__main__":
    supervisor = demo_supervisor_with_debug()

    # Save the supervisor state for review

    details = {
        "supervisor_name": supervisor.name,
        "debug_enabled": getattr(supervisor, "debug", False),
        "total_tools": len(supervisor.tools),
        "agents_count": len(supervisor.agent_registry.list_agents()),
        "tool_names": [t.name for t in supervisor.tools],
        "agent_names": list(supervisor.agent_registry.list_agents().keys()),
        "state_schema": supervisor.state_schema.__name__,
        "state_fields": list(supervisor.state_schema.model_fields.keys()),
    }

    for key, value in details.items():
        pass
