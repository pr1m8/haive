#!/usr/bin/env python3
"""Example demonstrating Enhanced SimpleAgent with engine-focused generics.

This shows how SimpleAgent is now essentially Agent[AugLLMConfig] with
clean design and type safety.
"""

import asyncio
import os
import sys

# Add the packages to the path
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "../../packages/haive-agents/src"),
)
sys.path.insert(
    0,
    os.path.join(os.path.dirname(__file__), "../../packages/haive-core/src"),
)


async def demonstrate_enhanced_simple_agent():
    """Demonstrate the enhanced SimpleAgent pattern."""
    print("=== Enhanced SimpleAgent Demo ===\n")

    # Import here to show the pattern
    from langchain_core.tools import tool

    from haive.agents.simple.enhanced_simple_agent import (
        EnhancedSimpleAgent,
        create_simple_agent,
    )
    from haive.core.engine.aug_llm import AugLLMConfig

    # 1. Basic Creation - SimpleAgent is just Agent[AugLLMConfig]
    print("1. Basic Enhanced SimpleAgent:")
    agent = EnhancedSimpleAgent(
        name="assistant",
        temperature=0.7,
        system_message="You are a helpful assistant",
    )

    print(f"   Agent: {agent}")
    print(f"   Engine type: {type(agent.engine)}")
    print(f"   Temperature: {agent.temperature}")
    print("")

    # 2. Type-safe engine access
    print("2. Type-safe engine access:")
    aug_config = agent.get_aug_llm_config()  # Returns AugLLMConfig
    print(f"   Engine class: {aug_config.__class__.__name__}")
    print(f"   Has proper typing: {isinstance(aug_config, AugLLMConfig)}")
    print("")

    # 3. With tools - still clean
    print("3. Enhanced SimpleAgent with tools:")

    @tool
    def calculator(expression: str) -> str:
        """Calculate mathematical expressions."""
        try:
            result = eval(expression)
            return f"Result: {result}"
        except BaseException:
            return "Error in calculation"

    math_agent = create_simple_agent(
        name="math_helper",
        temperature=0.1,
        tools=[calculator],
        system_message="You are a math assistant. Use the calculator tool for calculations.",
    )

    print(f"   Agent: {math_agent}")
    print(f"   Tools: {[t.name for t in math_agent.tools]}")
    print("")

    # 4. Dynamic updates maintain sync
    print("4. Dynamic updates with sync:")
    math_agent.update_temperature(0.5)
    print(f"   Agent temperature: {math_agent.temperature}")
    print(f"   Engine temperature: {math_agent.engine.temperature}")
    print(f"   Are synced: {math_agent.temperature == math_agent.engine.temperature}")
    print("")

    # 5. Graph building works
    print("5. Graph building:")
    graph = math_agent.build_graph()
    print(f"   Nodes: {list(graph.nodes.keys())}")
    print(f"   Has tool node: {'tool_node' in graph.nodes}")
    print("")

    # 6. Show the clean inheritance
    print("6. Clean inheritance hierarchy:")
    print("   EnhancedSimpleAgent is Agent[AugLLMConfig]")
    print("   Inherits from enhanced Agent base")
    print("   Engine type is locked to AugLLMConfig")
    print("")

    # 7. Execution would work with real LLM
    print("7. Ready for execution:")
    print("   Would execute with: await agent.arun('Hello!')")
    print("   No mocks needed - uses real AugLLMConfig")
    print("")

    # 8. Benefits of the pattern
    print("8. Benefits of enhanced pattern:")
    print("   - Type safety: engine is always AugLLMConfig")
    print("   - Clean design: SimpleAgent = Agent[AugLLMConfig]")
    print("   - No complexity: All logic in base Agent class")
    print("   - Flexibility: Still supports tools, structured output, etc.")
    print("   - Future-proof: Easy to create Agent[CustomEngine] variants")


def show_pattern_comparison():
    """Show the difference between old and new patterns."""
    print("\n=== Pattern Comparison ===\n")

    print("Old Pattern:")
    print("```python")
    print("class SimpleAgent(Agent):")
    print("    # Inherits from regular Agent")
    print("    # No engine type guarantees")
    print("    # Could have any engine type")
    print("```")
    print("")

    print("New Enhanced Pattern:")
    print("```python")
    print("class EnhancedSimpleAgent(Agent[AugLLMConfig]):")
    print("    # Inherits from Agent with AugLLMConfig generic")
    print("    # Engine is guaranteed to be AugLLMConfig")
    print("    # Type-safe and clean")
    print("```")
    print("")

    print("This makes SimpleAgent literally just Agent[AugLLMConfig]!")


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_enhanced_simple_agent())
    show_pattern_comparison()

    print("\nNext steps:")
    print("1. Apply same pattern to ReactAgent -> Agent[AugLLMConfig] with looping")
    print("2. Create BaseRAGAgent[RetrieverEngine] for RAG-specific agents")
    print("3. Update MultiAgent to use enhanced pattern")
    print("4. Migrate existing agents gradually")
