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
        from haive.core.utils.agent_capture import capture_agent_run, visualize_agent_graph
        from haive.core.utils.doc_agent_showcase import create_agent_showcase_page
        
        print("🚀 Real Agent Capture Demo")
        print("=" * 50)
        
        # Try to import and test SimpleAgent
        try:
            from haive.agents.simple.agent import SimpleAgent
            from haive.agents.simple.config import SimpleAgentConfig
            
            print("✅ Found SimpleAgent")
            
            # Configure the agent
            config = SimpleAgentConfig()
            agent = SimpleAgent(config=config)
            
            # Example input for simple agent
            example_input = {
                "user_input": "What are the main benefits of renewable energy?"
            }
            
            print("📸 Capturing SimpleAgent execution...")
            
            # Capture the run
            run = capture_agent_run(
                agent,
                example_input,
                agent_name="SimpleAgent",
                capture_dir="docs/captures"
            )
            
            print(f"✅ Captured SimpleAgent run:")
            print(f"   Run ID: {run.run_id}")
            print(f"   Duration: {run.duration:.2f}s" if run.duration else "   Duration: N/A")
            print(f"   Steps: {len(run.steps)}")
            print(f"   Success: {run.is_successful}")
            
            # Generate documentation page
            print("📝 Generating documentation page...")
            
            doc_page = create_agent_showcase_page(
                agent,
                example_input,
                agent_name="SimpleAgent",
                description="A straightforward agent for general question answering and text processing",
                example_description="Answering a question about renewable energy benefits"
            )
            
            print(f"✅ Generated documentation: {doc_page}")
            
        except ImportError as e:
            print(f"❌ Could not import SimpleAgent: {e}")
        
        # Try to test ReactAgent
        try:
            from haive.agents.react_class.react_agent.agent import ReactAgent
            from haive.agents.react_class.react_agent.config import ReactAgentConfig
            
            print("\n✅ Found ReactAgent")
            
            # Configure the agent
            config = ReactAgentConfig()
            agent = ReactAgent(config=config)
            
            # Example input for react agent
            example_input = {
                "input": "Research the latest developments in electric vehicle battery technology"
            }
            
            print("📸 Capturing ReactAgent execution...")
            
            # Capture the run
            run = capture_agent_run(
                agent,
                example_input,
                agent_name="ReactAgent",
                capture_dir="docs/captures"
            )
            
            print(f"✅ Captured ReactAgent run:")
            print(f"   Run ID: {run.run_id}")
            print(f"   Duration: {run.duration:.2f}s" if run.duration else "   Duration: N/A")
            print(f"   Steps: {len(run.steps)}")
            print(f"   Success: {run.is_successful}")
            
            # Generate documentation page
            print("📝 Generating documentation page...")
            
            doc_page = create_agent_showcase_page(
                agent,
                example_input,
                agent_name="ReactAgent",
                description="A research agent implementing the ReAct pattern with tool integration",
                example_description="Researching electric vehicle battery technology"
            )
            
            print(f"✅ Generated documentation: {doc_page}")
            
        except ImportError as e:
            print(f"❌ Could not import ReactAgent: {e}")
        
        print("\n🎉 Demo completed!")
        print("📁 Check docs/captures/ for execution captures")
        print("📁 Check docs/source/agents/ for generated documentation")
        print("\n🏗️ To build docs: poetry run nox -s docs")
        print("🌐 To serve docs: poetry run nox -s serve")
        
    except Exception as e:
        logger.exception(f"Demo failed: {e}")
        print(f"\n❌ Demo failed: {e}")
        print("This might be due to missing dependencies or agent configuration issues.")
        print("Please ensure all Haive packages are properly installed and configured.")


if __name__ == "__main__":
    main()