#!/usr/bin/env python3
"""CLI tool for agent capture and documentation generation.

This tool can be run with poetry run for easy access:
    poetry run python scripts/agent_capture_cli.py demo
    poetry run python scripts/agent_capture_cli.py capture --agent simple --input "test question"
"""

import argparse
import json
import logging
import sys
from pathlib import Path

# Add project paths for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def cmd_demo(args):
    """Run demonstration of agent capture system."""
    print("🤖 Agent Capture System Demo")
    print("=" * 50)
    
    try:
        from haive.core.utils.agent_capture import capture_agent_run
        print("✅ Successfully imported agent capture utilities")
        
        # Create a mock agent for demo
        class DemoAgent:
            def __init__(self, name="DemoAgent"):
                self.name = name
                self.__class__.__name__ = name
                self.__class__.__module__ = f"demo.{name.lower()}"
            
            def run(self, input_data):
                return {"result": f"Demo processed: {input_data}", "status": "success"}
            
            def stream(self, input_data, **kwargs):
                steps = [
                    {"step": "input", "content": input_data},
                    {"step": "processing", "content": {"status": "thinking"}},
                    {"step": "output", "content": {"result": f"Processed: {input_data}"}}
                ]
                for step in steps:
                    yield step
            
            def visualize_graph(self, output_path=None):
                if output_path:
                    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                    Path(output_path).write_text("Demo graph placeholder")
                    return output_path
                return None
        
        # Demo capture
        agent = DemoAgent()
        example_input = {"query": "What is artificial intelligence?"}
        
        print("📸 Capturing demo agent run...")
        run = capture_agent_run(
            agent,
            example_input,
            agent_name="DemoAgent",
            capture_dir="docs/captures"
        )
        
        print(f"✅ Demo completed successfully!")
        print(f"   Run ID: {run.run_id}")
        print(f"   Steps: {len(run.steps)}")
        print(f"   Duration: {run.duration:.2f}s" if run.duration else "   Duration: N/A")
        print(f"   Success: {run.is_successful}")
        
        return 0
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure you're running with poetry run and all dependencies are installed")
        return 1
    except Exception as e:
        logger.exception(f"Demo failed: {e}")
        return 1


def cmd_capture(args):
    """Capture a specific agent run."""
    print(f"📸 Capturing {args.agent} agent...")
    
    try:
        from haive.core.utils.agent_capture import capture_agent_run
        
        # Parse input
        if args.input.startswith('{'):
            input_data = json.loads(args.input)
        else:
            input_data = {"query": args.input}
        
        # TODO: Add logic to load specific agents based on args.agent
        # For now, use demo agent
        class CaptureAgent:
            def __init__(self, agent_type):
                self.agent_type = agent_type
                self.__class__.__name__ = f"{agent_type.title()}Agent"
                self.__class__.__module__ = f"haive.agents.{agent_type}"
            
            def run(self, input_data):
                return {"result": f"{self.agent_type} processed: {input_data}"}
            
            def stream(self, input_data, **kwargs):
                yield {"step": "start", "content": input_data}
                yield {"step": "process", "content": {"thinking": True}}
                yield {"step": "complete", "content": {"result": f"Done: {input_data}"}}
        
        agent = CaptureAgent(args.agent)
        
        run = capture_agent_run(
            agent,
            input_data,
            agent_name=f"{args.agent.title()}Agent",
            capture_dir=args.output_dir
        )
        
        print(f"✅ Capture completed:")
        print(f"   Run ID: {run.run_id}")
        print(f"   Output: {args.output_dir}")
        print(f"   Steps: {len(run.steps)}")
        
        return 0
        
    except Exception as e:
        logger.exception(f"Capture failed: {e}")
        return 1


def cmd_document(args):
    """Generate documentation for captured runs."""
    print(f"📚 Generating documentation...")
    
    try:
        from haive.core.utils.doc_agent_showcase import AgentDocumentationGenerator
        
        generator = AgentDocumentationGenerator(docs_dir=args.docs_dir)
        
        # TODO: Load actual agents and generate docs
        print("✅ Documentation generation not yet implemented for CLI")
        print("   Use the demo scripts for now:")
        print("   poetry run python scripts/demo_agent_capture.py")
        
        return 0
        
    except Exception as e:
        logger.exception(f"Documentation generation failed: {e}")
        return 1


def cmd_list(args):
    """List captured agent runs."""
    capture_dir = Path(args.capture_dir)
    
    if not capture_dir.exists():
        print(f"❌ Capture directory not found: {capture_dir}")
        return 1
    
    captures = list(capture_dir.glob("*.json"))
    
    if not captures:
        print(f"No captures found in {capture_dir}")
        return 0
    
    print(f"📁 Found {len(captures)} captures in {capture_dir}:")
    
    for capture_file in sorted(captures):
        try:
            with open(capture_file) as f:
                data = json.load(f)
            
            agent_name = data.get("agent_name", "Unknown")
            run_id = data.get("run_id", "Unknown")[:8]
            duration = data.get("duration", 0)
            steps = len(data.get("steps", []))
            success = "✅" if data.get("error") is None else "❌"
            
            print(f"   {success} {agent_name} ({run_id}...) - {duration:.2f}s, {steps} steps")
            
        except Exception as e:
            print(f"   ❌ {capture_file.name} - Error reading file: {e}")
    
    return 0


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Haive Agent Capture CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  poetry run python scripts/agent_capture_cli.py demo
  poetry run python scripts/agent_capture_cli.py capture --agent simple --input "test question"
  poetry run python scripts/agent_capture_cli.py list
        """
    )
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logging")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Demo command
    demo_parser = subparsers.add_parser("demo", help="Run demonstration")
    demo_parser.set_defaults(func=cmd_demo)
    
    # Capture command
    capture_parser = subparsers.add_parser("capture", help="Capture agent run")
    capture_parser.add_argument("--agent", required=True, help="Agent type to capture")
    capture_parser.add_argument("--input", required=True, help="Input data (JSON string or plain text)")
    capture_parser.add_argument("--output-dir", default="docs/captures", help="Output directory")
    capture_parser.set_defaults(func=cmd_capture)
    
    # Document command
    doc_parser = subparsers.add_parser("document", help="Generate documentation")
    doc_parser.add_argument("--docs-dir", default="docs/source", help="Documentation directory")
    doc_parser.set_defaults(func=cmd_document)
    
    # List command
    list_parser = subparsers.add_parser("list", help="List captured runs")
    list_parser.add_argument("--capture-dir", default="docs/captures", help="Capture directory")
    list_parser.set_defaults(func=cmd_list)
    
    args = parser.parse_args()
    
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        return 1
    
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())