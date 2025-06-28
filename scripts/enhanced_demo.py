#!/usr/bin/env python3
"""Enhanced demonstration of the complete agent capture and analysis system.

This script showcases all the enhanced features:
- Auto-discovery of real agents
- Performance analysis and benchmarking
- Interactive visualizations
- Comprehensive documentation generation
"""

import logging
import sys
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "packages" / "haive-core" / "src"))

from haive.core.utils.agent_capture import capture_agent_run
from haive.core.utils.doc_agent_showcase import AgentDocumentationGenerator
from haive.core.utils.interactive_visualization import InteractiveGraphGenerator
from haive.core.utils.performance_analysis import PerformanceAnalyzer

logger = logging.getLogger(__name__)


def demo_performance_analysis():
    """Demonstrate performance analysis capabilities."""

    # Create mock agent for analysis
    class PerformanceTestAgent:
        def __init__(self, name="PerformanceAgent"):
            self.name = name
            self.__class__.__name__ = name

        def run(self, input_data):
            import time

            time.sleep(0.1)  # Simulate processing
            return {"result": f"Processed: {input_data}", "performance": "optimized"}

        def stream(self, input_data, **kwargs):
            import time

            steps = [
                {"step": "initialization", "content": input_data},
                {"step": "processing", "content": {"status": "analyzing"}},
                {"step": "optimization", "content": {"method": "enhanced"}},
                {"step": "validation", "content": {"checks": "passed"}},
                {"step": "output", "content": {"result": f"Enhanced: {input_data}"}},
            ]
            for step in steps:
                time.sleep(0.02)  # Simulate step processing
                yield step

    agent = PerformanceTestAgent()

    # Capture a run
    run = capture_agent_run(
        agent,
        {"query": "Analyze system performance", "complexity": "high"},
        agent_name="PerformanceAgent",
        capture_dir="docs/captures",
    )

    # Analyze performance
    analyzer = PerformanceAnalyzer()
    analysis = analyzer.analyze_single_run(run.dict())


    if analysis["summary"]["strengths"]:
        pass}")

    if analysis["summary"]["areas_for_improvement"]:
        pass

    return run, analysis


def demo_interactive_visualization(run_data, analysis):
    """Demonstrate interactive visualization generation."""

    # Generate interactive visualization
    viz_generator = InteractiveGraphGenerator()

    html_path = viz_generator.generate_interactive_graph(
        run_data.dict(), output_filename="enhanced_demo_interactive.html"
    )


    return html_path


def demo_benchmarking():
    """Demonstrate agent benchmarking capabilities."""

    # Create agent for benchmarking
    class BenchmarkAgent:
        def __init__(self, efficiency=1.0):
            self.efficiency = efficiency
            self.__class__.__name__ = "BenchmarkAgent"

        def run(self, input_data):
            import time

            # Simulate variable performance
            base_time = 0.05
            actual_time = base_time / self.efficiency
            time.sleep(actual_time)

            return {
                "result": f"Benchmark result for: {input_data}",
                "efficiency": self.efficiency,
                "processing_time": actual_time,
            }

        def stream(self, input_data, **kwargs):
            yield {"step": "start", "content": input_data}
            yield {"step": "process", "content": {"efficiency": self.efficiency}}
            result = self.run(input_data)
            yield {"step": "complete", "content": result}

    # Test different efficiency levels
    agents = [
        BenchmarkAgent(efficiency=0.8),  # Slower agent
        BenchmarkAgent(efficiency=1.2),  # Faster agent
        BenchmarkAgent(efficiency=1.0),  # Baseline agent
    ]

    test_cases = [
        {"task": "Simple processing", "complexity": "low"},
        {"task": "Complex analysis", "complexity": "high"},
        {"task": "Optimization task", "complexity": "medium"},
    ]


    analyzer = PerformanceAnalyzer()
    benchmark_results = []

    for i, agent in enumerate(agents):

        # Run benchmark
        results = analyzer.benchmark_agent(agent, test_cases, iterations=2)
        benchmark_results.append(results)

        summary = results["summary"]

    # Compare results
    for i, results in enumerate(benchmark_results):
        summary = results["summary"]

    return benchmark_results


def demo_enhanced_documentation():
    """Demonstrate enhanced documentation generation."""

    # Create sophisticated agent
    class DocumentationAgent:
        def __init__(self):
            self.__class__.__name__ = "DocumentationAgent"

        def run(self, input_data):
            return {
                "analysis": f"Comprehensive analysis of: {input_data}",
                "insights": ["Key insight 1", "Key insight 2", "Key insight 3"],
                "recommendations": ["Optimize X", "Improve Y", "Monitor Z"],
                "confidence": 0.95,
            }

        def stream(self, input_data, **kwargs):
            steps = [
                {"step": "input_validation", "content": input_data},
                {
                    "step": "data_analysis",
                    "content": {"methods": ["statistical", "ml"]},
                },
                {"step": "insight_generation", "content": {"insights_found": 3}},
                {"step": "recommendation_engine", "content": {"recommendations": 3}},
                {"step": "confidence_scoring", "content": {"confidence": 0.95}},
                {"step": "output_formatting", "content": {"format": "structured"}},
            ]
            yield from steps

        def visualize_graph(self, output_path=None):
            if output_path:
                Path(output_path).parent.mkdir(parents=True, exist_ok=True)
                Path(output_path).write_text("Enhanced documentation agent graph")
                return output_path
            return None

    agent = DocumentationAgent()

    # Generate enhanced documentation

    doc_generator = AgentDocumentationGenerator()

    # This will now include performance analysis and interactive visualizations
    doc_path = doc_generator.generate_agent_page(
        agent,
        {
            "document": "Advanced AI research paper",
            "analysis_type": "comprehensive",
            "output_format": "structured_insights",
        },
        agent_name="DocumentationAgent",
        description="Advanced agent for document analysis and insight generation",
        example_description="Analyzing an AI research paper for key insights and recommendations",
    )


    return doc_path


def main():
    """Run the complete enhanced demonstration."""
    logging.basicConfig(level=logging.INFO)


    try:
        # Demo 1: Performance Analysis
        run_data, analysis = demo_performance_analysis()

        # Demo 2: Interactive Visualization
        viz_path = demo_interactive_visualization(run_data, analysis)

        # Demo 3: Benchmarking
        benchmark_results = demo_benchmarking()

        # Demo 4: Enhanced Documentation
        doc_path = demo_enhanced_documentation()

        # Summary


        return 0

    except Exception as e:
        logger.exception(f"Enhanced demo failed: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
