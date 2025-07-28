#!/usr/bin/env python3
"""Comprehensive MultiAgent examples demonstrating all features.

This example showcases the unified MultiAgent implementation with various
patterns including sequential, parallel, and conditional routing.

ALL EXAMPLES USE REAL COMPONENTS - NO MOCKS.
"""

import asyncio
from typing import Any

from haive.agents.multi.clean import MultiAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig


# Example 1: Basic Sequential Execution
async def example_sequential():
    """Demonstrate basic sequential agent execution."""
    print("🔄 Example 1: Sequential Execution")
    print("-" * 50)

    # Create agents with real LLM configurations
    analyzer = SimpleAgent(name="analyzer", engine=AugLLMConfig(temperature=0.3))
    summarizer = SimpleAgent(name="summarizer", engine=AugLLMConfig(temperature=0.5))
    reporter = SimpleAgent(name="reporter", engine=AugLLMConfig(temperature=0.7))

    # Create multi-agent (natural list syntax)
    multi_agent = MultiAgent(agents=[analyzer, summarizer, reporter])

    print(f"Created MultiAgent with {len(multi_agent.agents)} agents")
    print(f"Execution mode: {multi_agent.execution_mode}")
    print(f"Agents: {list(multi_agent.agents.keys())}")

    # Execute (commented out for demo - would make real LLM calls)

    print("✅ Sequential execution setup complete\n")


# Example 2: Conditional Routing
async def example_conditional_routing():
    """Demonstrate conditional routing based on message content."""
    print("🔀 Example 2: Conditional Routing")
    print("-" * 50)

    # Create specialized agents
    classifier = SimpleAgent(name="classifier", engine=AugLLMConfig(temperature=0.2))
    billing_agent = SimpleAgent(name="billing", engine=AugLLMConfig(temperature=0.3))
    technical_agent = SimpleAgent(
        name="technical", engine=AugLLMConfig(temperature=0.3)
    )
    general_agent = SimpleAgent(name="general", engine=AugLLMConfig(temperature=0.4))

    # Create multi-agent with entry point
    multi_agent = MultiAgent(
        agents=[classifier, billing_agent, technical_agent, general_agent],
        entry_point="classifier",
    )

    # Add conditional routing function
    def route_by_category(state: dict[str, Any]) -> str:
        """Route based on message category."""
        # In real implementation, this would analyze the classifier's output
        messages = state.get("messages", [])
        if messages:
            content = str(messages[-1]).lower()
            if "billing" in content or "payment" in content:
                return "billing"
            if "technical" in content or "bug" in content:
                return "technical"
        return "general"

    multi_agent.add_conditional_routing(
        "classifief",
        route_by_category,
        {"billing": "billing", "technical": "technical", "general": "general"},
    )

    print(f"Created routing system with entry point: {multi_agent.entry_point}")
    print(f"Routing configuration: {multi_agent.branches}")

    # Test graph building
    graph = multi_agent.build_graph()
    print(f"Graph built successfully: {graph.name}")

    print("✅ Conditional routing setup complete\n")


# Example 3: Parallel Processing
async def example_parallel_processing():
    """Demonstrate parallel agent processing with convergence."""
    print("⚡ Example 3: Parallel Processing")
    print("-" * 50)

    # Create processing agents
    data_processor = SimpleAgent(name="data_proc", engine=AugLLMConfig(temperature=0.3))
    image_processor = SimpleAgent(
        name="image_proc", engine=AugLLMConfig(temperature=0.3)
    )
    text_processor = SimpleAgent(name="text_proc", engine=AugLLMConfig(temperature=0.3))
    aggregator = SimpleAgent(name="aggregator", engine=AugLLMConfig(temperature=0.5))

    multi_agent = MultiAgent(
        agents=[data_processor, image_processor, text_processor, aggregator]
    )

    # Configure parallel processing
    multi_agent.add_parallel_group(
        ["data_proc", "image_proc", "text_proc"], next_agent="aggregator"
    )

    print("Created parallel processing system")
    print(f"Parallel group: {multi_agent.branches}")

    # Test graph building
    graph = multi_agent.build_graph()
    print(f"Graph built successfully: {graph.name}")

    print("✅ Parallel processing setup complete\n")


# Example 4: Complex Workflow
async def example_complex_workflow():
    """Demonstrate complex workflow with multiple routing patterns."""
    print("🌊 Example 4: Complex Workflow")
    print("-" * 50)

    # Create comprehensive agent set
    intake = SimpleAgent(name="intake", engine=AugLLMConfig(temperature=0.2))

    # Parallel analysis agents
    risk_analyzer = SimpleAgent(
        name="risk_analyzer", engine=AugLLMConfig(temperature=0.3)
    )
    financial_analyzer = SimpleAgent(
        name="financial_analyzer", engine=AugLLMConfig(temperature=0.3)
    )
    legal_analyzer = SimpleAgent(
        name="legal_analyzer", engine=AugLLMConfig(temperature=0.3)
    )

    # Decision agents
    approver = SimpleAgent(name="approver", engine=AugLLMConfig(temperature=0.4))
    reviewer = SimpleAgent(name="reviewer", engine=AugLLMConfig(temperature=0.4))

    # Final processing
    processor = SimpleAgent(name="processor", engine=AugLLMConfig(temperature=0.5))

    # Create multi-agent system
    multi_agent = MultiAgent(
        agents=[
            intake,
            risk_analyzer,
            financial_analyzer,
            legal_analyzer,
            approver,
            reviewer,
            processor,
        ],
        entry_point="intake",
    )

    # Step 1: Intake routes to parallel analysis
    multi_agent.add_parallel_group(
        ["risk_analyzer", "financial_analyzer", "legal_analyzer"], next_agent="approver"
    )

    # Step 2: Approver makes decision
    def approval_routing(state: dict[str, Any]) -> str:
        """Route based on approval decision."""
        # In real scenario, this would check approval status
        return "processor"  # Simplified for demo

    multi_agent.add_conditional_routing(
        "approvef",
        approval_routing,
        {"approved": "processor", "review": "reviewer", "denied": "processor"},
    )

    # Step 3: Reviewer can send to processor
    multi_agent.add_edge("reviewer", "processor")

    print(f"Created complex workflow with {len(multi_agent.agents)} agents")
    print(f"Entry point: {multi_agent.entry_point}")
    print(f"Routing branches: {len(multi_agent.branches)}")

    # Test graph building
    graph = multi_agent.build_graph()
    print(f"Complex graph built successfully: {graph.name}")

    print("✅ Complex workflow setup complete\n")


# Example 5: Factory Method Usage
async def example_factory_method():
    """Demonstrate factory method for creating MultiAgent instances."""
    print("🏭 Example 5: Factory Method")
    print("-" * 50)

    # Create agents
    agents = []
    for i in range(3):
        agents.append(
            SimpleAgent(name=f"worker_{i}", engine=AugLLMConfig(temperature=0.3))
        )

    # Use factory method
    multi_agent = MultiAgent.create(
        agents=agents, name="assembly_line", execution_mode="sequential"
    )

    print(f"Created via factory: {multi_agent.name}")
    print(f"Execution mode: {multi_agent.execution_mode}")
    print(f"Agents: {list(multi_agent.agents.keys())}")

    print("✅ Factory method demonstration complete\n")


# Example 6: Dynamic Agent Management
async def example_dynamic_management():
    """Demonstrate dynamic agent addition and routing updates."""
    print("⚡ Example 6: Dynamic Agent Management")
    print("-" * 50)

    # Start with basic agents
    agent1 = SimpleAgent(name="stage1", engine=AugLLMConfig())
    agent2 = SimpleAgent(name="stage2", engine=AugLLMConfig())

    multi_agent = MultiAgent(agents=[agent1, agent2])
    print(f"Initial agents: {list(multi_agent.agents.keys())}")

    # Add new agent dynamically
    new_agent = SimpleAgent(name="quality_check", engine=AugLLMConfig())
    multi_agent.agents["quality_check"] = new_agent

    # Update routing
    multi_agent.add_edge("stage1", "quality_check")
    multi_agent.add_edge("quality_check", "stage2")

    print(f"After dynamic addition: {list(multi_agent.agents.keys())}")
    print(f"Routing updates: {multi_agent.branches}")

    print("✅ Dynamic management demonstration complete\n")


# Example 7: Real Execution (Optional)
async def example_real_execution():
    """Demonstrate actual execution with real LLM calls."""
    print("🚀 Example 7: Real Execution (Optional)")
    print("-" * 50)

    # Create simple agents for real execution
    greeter = SimpleAgent(name="greeter", engine=AugLLMConfig(temperature=0.1))
    responder = SimpleAgent(name="responder", engine=AugLLMConfig(temperature=0.3))

    multi_agent = MultiAgent(agents=[greeter, responder])

    try:
        print("Attempting real execution...")
        result = await multi_agent.arun("Hello, please introduce yourself")

        print("✅ Real execution successful!")
        print(f"Result type: {type(result)}")
        print(f"Result preview: {str(result)[:200]}...")

    except Exception as e:
        print(f"⚠️ Real execution failed (expected in some environments): {e}")
        print("This is normal if LLM credentials are not configured.")

    print("✅ Real execution demonstration complete\n")


# Main execution function
async def main():
    """Run all MultiAgent examples."""
    print("🎯 Comprehensive MultiAgent Examples")
    print("=" * 60)
    print()

    # Run all examples
    await example_sequential()
    await example_conditional_routing()
    await example_parallel_processing()
    await example_complex_workflow()
    await example_factory_method()
    await example_dynamic_management()
    await example_real_execution()

    print("🎉 All examples completed successfully!")
    print("\nKey Takeaways:")
    print("- MultiAgent supports natural list initialization")
    print("- Conditional routing enables smart agent selection")
    print("- Parallel processing allows concurrent execution")
    print("- Complex workflows combine multiple patterns")
    print("- Factory methods provide convenient creation")
    print("- Dynamic management enables runtime flexibility")
    print("- Real execution works with properly configured LLMs")


if __name__ == "__main__":
    asyncio.run(main())
