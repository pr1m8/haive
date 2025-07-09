#!/usr/bin/env python3
"""
Debug Supervisor Demo - Simple demonstration with debug=True

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
    """Simple demonstration of supervisor with debug=True"""
    print("🚀 DYNAMIC SUPERVISOR DEBUG DEMO")
    print("=" * 50)

    # Create supervisor with debug enabled
    print("\n1. Creating supervisor with debug=True...")
    registry = create_test_registry()
    supervisor = DynamicSupervisorAgent(
        name="Debug Demo Supervisor",
        agent_registry=registry,
        debug=True,  # This enables debug mode
    )

    print(f"✅ Created: {supervisor.name}")
    print(f"🔧 Initial tools: {len(supervisor.tools)}")

    # Show initial tools
    print("\n2. Initial Tools:")
    for i, tool in enumerate(supervisor.tools, 1):
        print(f"   {i}. {tool.name}")
        print(f"      Description: {tool.description}")

    # Show agent registry
    print("\n3. Agent Registry:")
    agents = supervisor.agent_registry.list_agents()
    for name, info in agents.items():
        print(f"   • {name}: {info['description']}")
        print(f"     Capabilities: {', '.join(info['capabilities'])}")

    # Demonstrate dynamic tool addition
    print("\n4. Adding new agent dynamically...")
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

    print(f"🔧 Tools after addition: {len(supervisor.tools)}")

    # Show new tools
    print("\n5. Updated Tools:")
    handoff_tools = [t for t in supervisor.tools if t.name.startswith("handoff_to_")]
    for tool in handoff_tools:
        print(f"   • {tool.name}")

    # Test list_agents tool
    print("\n6. Testing list_agents tool...")
    list_tool = next(t for t in supervisor.tools if t.name == "list_agents")
    result = list_tool.invoke({})
    print("Result:")
    print(result)

    # Show state schema
    print("\n7. State Schema Information:")
    state_schema = supervisor.state_schema
    print(f"   Schema class: {state_schema.__name__}")
    print(f"   Fields: {list(state_schema.model_fields.keys())}")

    print("\n✅ Demo completed successfully!")
    print(
        f"Final stats: {len(supervisor.tools)} tools, {len(supervisor.agent_registry.list_agents())} agents"
    )

    return supervisor


if __name__ == "__main__":
    supervisor = demo_supervisor_with_debug()

    # Save the supervisor state for review
    print("\n📝 Saving supervisor details for review...")

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

    print("Supervisor Details:")
    for key, value in details.items():
        print(f"  {key}: {value}")
