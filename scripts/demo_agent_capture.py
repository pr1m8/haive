#!/usr/bin/env python3
"""Demo script showing agent capture and documentation generation.

This script demonstrates how to:
1. Capture agent execution with visualization
2. Generate documentation pages automatically
3. Create interactive showcase content

Run with: python scripts/demo_agent_capture.py
"""

import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))
sys.path.insert(0, str(project_root / "packages" / "haive-agents" / "src"))

try:
    from haive.core.utils.agent_capture import capture_agent_run, visualize_agent_graph
    from haive.core.utils.doc_agent_showcase import (
        batch_document_agents,
        create_agent_showcase_page,
    )

    # Import some example agents (these may not exist yet, so we'll mock them)
    try:
        from haive.agents.react_class.react_agent import ReactAgent
        from haive.agents.simple import SimpleAgent
    except ImportError:

        class MockAgent:
            """Mock agent for demonstration purposes."""

            def __init__(self, name="MockAgent"):
                self.name = name
                self.__class__.__name__ = name
                self.__class__.__module__ = f"haive.mock.{name.lower()}"

            def run(self, input_data):
                """Mock run method."""
                return {"result": f"Processed: {input_data}", "status": "success"}

            def stream(self, input_data, **kwargs):
                """Mock stream method."""
                steps = [
                    {
                        "messages": [
                            {"content": "Starting processing", "type": "system"}
                        ]
                    },
                    {"node": "input_processor", "content": input_data},
                    {"node": "main_logic", "content": {"processing": True}},
                    {
                        "messages": [
                            {"content": f"Processed: {input_data}", "type": "result"}
                        ]
                    },
                ]
                yield from steps

            def visualize_graph(self, output_path=None):
                """Mock visualization method."""
                if output_path:
                    # Create a simple placeholder file
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    Path(output_path).write_text("Mock graph visualization")
                    return output_path
                return None

        def SimpleAgent():
            return MockAgent("SimpleAgent")
        def ReactAgent():
            return MockAgent("ReactAgent")

except ImportError as e:
    sys.exit(1)


def setup_logging():
    """Setup logging for the demo."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def demo_single_agent_capture():
    """Demonstrate capturing a single agent run."""

    # Create agent
    agent = SimpleAgent()

    # Example input
    example_input = {
        "task": "Analyze the benefits of renewable energy",
        "context": "climate change discussion",
        "max_length": 500,
    }

    # Capture the run
    run = capture_agent_run(
        agent,
        example_input,
        agent_name="SimpleAnalysisAgent",
        capture_dir="docs/captures",
    )


    return run


def demo_agent_documentation():
    """Demonstrate generating agent documentation."""

    # Create agents
    simple_agent = SimpleAgent()
    react_agent = ReactAgent()

    # Define examples
    simple_example = {
        "question": "What are the key components of a sustainable energy system?",
        "context": "renewable energy research",
    }

    react_example = {
        "task": "Research the latest developments in solar panel technology",
        "tools_required": ["web_search", "pdf_analysis"],
        "max_iterations": 5,
    }

    # Generate documentation pages

    simple_page = create_agent_showcase_page(
        simple_agent,
        simple_example,
        agent_name="SimpleAnalysisAgent",
        description="A straightforward agent for content analysis and summarization",
        example_description="Analyzing renewable energy components",
    )

    react_page = create_agent_showcase_page(
        react_agent,
        react_example,
        agent_name="ReactResearchAgent",
        description="A research agent using ReAct pattern with tool integration",
        example_description="Researching solar panel technology developments",
    )


    return [simple_page, react_page]


def demo_batch_documentation():
    """Demonstrate batch documentation generation."""

    # Define multiple agents with their examples
    agents_and_examples = [
        (
            SimpleAgent(),
            {"query": "Explain quantum computing principles", "format": "beginner"},
            {
                "agent_name": "QuantumExplainerAgent",
                "description": "Agent specializing in quantum computing education",
            },
        ),
        (
            ReactAgent(),
            {"research_topic": "climate change solutions", "depth": "comprehensive"},
            {
                "agent_name": "ClimateResearchAgent",
                "description": "Comprehensive climate change research agent",
            },
        ),
        (
            SimpleAgent(),
            {"text": "Lorem ipsum dolor sit amet...", "task": "summarize"},
            {
                "agent_name": "TextSummarizerAgent",
                "description": "Fast text summarization agent",
            },
        ),
    ]


    # Generate batch documentation
    generated_files = batch_document_agents(agents_and_examples)

    for file_path in generated_files:
        pass

    return generated_files


def demo_visualization():
    """Demonstrate agent graph visualization."""

    agents = [(SimpleAgent(), "SimpleAgent"), (ReactAgent(), "ReactAgent")]


    for agent, name in agents:
        graph_path = visualize_agent_graph(
            agent, output_path=f"docs/captures/{name}_demo_graph.png"
        )

        if graph_path:
            pass")
        else:
            passe}")


def main():
    """Run all demos."""
    setup_logging()


    try:
        # Demo 1: Single agent capture
        demo_single_agent_capture()

        # Demo 2: Documentation generation
        demo_agent_documentation()

        # Demo 3: Batch documentation
        demo_batch_documentation()

        # Demo 4: Visualization
        demo_visualization()


    except Exception as e:
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
