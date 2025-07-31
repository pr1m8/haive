"""MultiAgent showcase - demonstrates all routing patterns.

This example shows how to use the unified MultiAgent implementation
with various routing patterns including sequential, conditional,
parallel, and complex workflows.
"""

import asyncio
from typing import Any

from haive.agents.multi.clean import MultiAgent
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool


# Create some example tools
@tool
def calculator(expression: str) -> str:
    """Calculate mathematical expressions."""
    try:
        return str(eval(expression))
    except:
        return "Invalid expression"


@tool
def word_counter(text: str) -> str:
    """Count words in text."""
    return f"Word count: {len(text.split())}"


async def example_1_sequential():
    """Example 1: Simple sequential execution."""
    # Create agents
    analyzer = SimpleAgent(name="analyzer", engine=AugLLMConfig())
    summarizer = SimpleAgent(name="summarizer", engine=AugLLMConfig())

    # Create multi-agent (automatically sequential)
    multi_agent = MultiAgent(agents=[analyzer, summarizer])

    # Execute
    await multi_agent.arun("Analyze this: AI is transforming software development")


async def example_2_conditional_routing():
    """Example 2: Conditional routing based on input."""
    # Create specialized agents
    classifier = SimpleAgent(name="classifier", engine=AugLLMConfig())
    math_expert = ReactAgent(
        name="math_expert", engine=AugLLMConfig(), tools=[calculator]
    )
    text_expert = ReactAgent(
        name="text_expert", engine=AugLLMConfig(), tools=[word_counter]
    )

    # Create multi-agent with entry point
    multi_agent = MultiAgent(
        agents=[classifier, math_expert, text_expert], entry_point="classifier"
    )

    # Add conditional routing
    def route_by_content(state: dict[str, Any]) -> str:
        # Simple routing logic - in practice would analyze state properly
        messages = state.get("messages", [])
        if messages and any("calculate" in str(m).lower() for m in messages):
            return "math"
        return "text"

    multi_agent.add_conditional_routing(
        "classifier", route_by_content, {"math": "math_expert", "text": "text_expert"}
    )

    # Test math path
    await multi_agent.arun("Please calculate 15 * 23 + 10")

    # Test text path
    await multi_agent.arun("Count the words in this sentence")


async def example_3_parallel_execution():
    """Example 3: Parallel execution with convergence."""
    # Create parallel processors
    data_analyzer = SimpleAgent(name="data_analyzer", engine=AugLLMConfig())
    sentiment_analyzer = SimpleAgent(name="sentiment_analyzer", engine=AugLLMConfig())
    keyword_extractor = SimpleAgent(name="keyword_extractor", engine=AugLLMConfig())
    report_writer = SimpleAgent(name="report_writer", engine=AugLLMConfig())

    # Create multi-agent
    multi_agent = MultiAgent(
        agents=[data_analyzer, sentiment_analyzer, keyword_extractor, report_writer]
    )

    # Configure parallel group with convergence
    multi_agent.add_parallel_group(
        ["data_analyzer", "sentiment_analyzer", "keyword_extractor"],
        next_agent="report_writer",
    )

    # Execute - analyzers run in parallel, then report writer
    await multi_agent.arun(
        "Analyze this customer feedback: The product is amazing but shipping was slow"
    )


async def example_4_complex_workflow():
    """Example 4: Complex workflow with mixed patterns."""
    # Create a customer support workflow
    intake = SimpleAgent(name="intake", engine=AugLLMConfig())
    classifier = SimpleAgent(name="classifier", engine=AugLLMConfig())
    urgent_handler = SimpleAgent(name="urgent", engine=AugLLMConfig())
    billing_specialist = SimpleAgent(name="billing", engine=AugLLMConfig())
    tech_specialist = ReactAgent(
        name="technical", engine=AugLLMConfig(), tools=[calculator]
    )
    quality_checker = SimpleAgent(name="quality", engine=AugLLMConfig())
    resolver = SimpleAgent(name="resolver", engine=AugLLMConfig())

    # Create multi-agent system
    support_system = MultiAgent(
        agents=[
            intake,
            classifier,
            urgent_handler,
            billing_specialist,
            tech_specialist,
            quality_checker,
            resolver,
        ],
        entry_point="intake",
    )

    # Build the workflow
    # 1. Intake -> Classifier
    support_system.add_edge("intake", "classifier")

    # 2. Classifier routes based on priority and type
    def route_ticket(state: dict[str, Any]) -> str:
        # Simplified routing logic
        messages = str(state.get("messages", [])).lower()
        if "urgent" in messages or "emergency" in messages:
            return "urgent"
        if "bill" in messages or "payment" in messages:
            return "billing"
        if "error" in messages or "bug" in messages:
            return "technical"
        return "billing"  # default

    support_system.add_conditional_routing(
        "classifier",
        route_ticket,
        {"urgent": "urgent", "billing": "billing", "technical": "technical"},
    )

    # 3. All specialists go to quality check
    support_system.add_edge("urgent", "quality")
    support_system.add_edge("billing", "quality")
    support_system.add_edge("technical", "quality")

    # 4. Quality check to resolver
    support_system.add_edge("quality", "resolver")

    # Execute workflow
    await support_system.arun(
        "URGENT: My account was charged twice and I'm getting error messages!"
    )


async def example_5_direct_edges():
    """Example 5: Direct edge routing for explicit control."""
    # Create validation pipeline
    input_validator = SimpleAgent(name="validator", engine=AugLLMConfig())
    data_processor = ReactAgent(
        name="processor", engine=AugLLMConfig(), tools=[calculator]
    )
    output_formatter = SimpleAgent(name="formatter", engine=AugLLMConfig())

    # Create multi-agent with explicit flow
    pipeline = MultiAgent(
        agents=[input_validator, data_processor, output_formatter],
        entry_point="validator",
    )

    # Define explicit flow
    pipeline.add_edge("validator", "processor")
    pipeline.add_edge("processor", "formatter")

    # Execute pipeline
    await pipeline.arun("Process this data: calculate 100 * 25 and format nicely")


async def main():
    """Run all examples."""
    # Run examples
    await example_1_sequential()
    await example_2_conditional_routing()
    await example_3_parallel_execution()
    await example_4_complex_workflow()
    await example_5_direct_edges()


if __name__ == "__main__":
    asyncio.run(main())
