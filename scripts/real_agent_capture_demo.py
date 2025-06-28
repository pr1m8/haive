#!/usr/bin/env python3
"""Real agent capture demonstration using actual Haive agents.

This script demonstrates the agent capture system with real agents from the codebase.
"""

import logging
import sys
from pathlib import Path

# Add project packages to path
project_root = Path(__file__).parent.parent
core_src = project_root / "packages" / "haive-core" / "src"
agents_src = project_root / "packages" / "haive-agents" / "src"

sys.path.insert(0, str(core_src))
sys.path.insert(0, str(agents_src))

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Demonstrate agent capture with real agents."""
    try:
        # Import capture utilities
        from haive.core.utils.agent_capture import (
            capture_agent_run,
        )
        from haive.core.utils.doc_agent_showcase import create_agent_showcase_page

        # Try to import and test SimpleAgent
        try:
            from haive.agents.simple.agent import SimpleAgent
            from haive.agents.simple.config import SimpleAgentConfig

            # Configure the agent
            config = SimpleAgentConfig()
            agent = SimpleAgent(config=config)

            # Example input for simple agent
            example_input = {
                "user_input": "What are the main benefits of renewable energy?"
            }


            # Capture the run
            run = capture_agent_run(
                agent,
                example_input,
                agent_name="SimpleAgent",
                capture_dir="docs/captures",
            )


            # Generate documentation page

            doc_page = create_agent_showcase_page(
                agent,
                example_input,
                agent_name="SimpleAgent",
                description="A straightforward agent for general question answering and text processing",
                example_description="Answering a question about renewable energy benefits",
            )


        except ImportError as e:
            pass")

        # Try to test ReactAgent
        try:
            from haive.agents.react_class.react_agent.agent import ReactAgent
            from haive.agents.react_class.react_agent.config import ReactAgentConfig


            # Configure the agent
            config = ReactAgentConfig()
            agent = ReactAgent(config=config)

            # Example input for react agent
            example_input = {
                "input": "Research the latest developments in electric vehicle battery technology"
            }


            # Capture the run
            run = capture_agent_run(
                agent,
                example_input,
                agent_name="ReactAgent",
                capture_dir="docs/captures",
            )


            # Generate documentation page

            doc_page = create_agent_showcase_page(
                agent,
                example_input,
                agent_name="ReactAgent",
                description="A research agent implementing the ReAct pattern with tool integration",
                example_description="Researching electric vehicle battery technology",
            )


        except ImportError as e:
            pass")


    except Exception as e:
        logger.exception(f"Demo failed: {e}")


if __name__ == "__main__":
    main()
