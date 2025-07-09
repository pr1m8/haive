"""Test script for Component 4 MultiAgentBase approach."""

import asyncio
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Now import our components
from component_2_tools import SupervisorStateWithTools
from component_3_agent_execution import create_agent_execution_node
from component_4_multiagent_supervisor import (
    create_dynamic_supervisor_system,
    test_multiagent_supervisor,
    test_routing_logic,
)

if __name__ == "__main__":
    print("Running Component 4 MultiAgentBase tests...")

    # Run routing test first
    asyncio.run(test_routing_logic())

    print("\n" + "=" * 80 + "\n")

    # Run full integration test
    asyncio.run(test_multiagent_supervisor())
