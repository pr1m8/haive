"""
Simple examples showing V2 SimpleAgent and ReactAgent usage.

This test demonstrates the exact usage patterns you requested:
1. SimpleAgent V2 with Plan model
2. ReactAgent with add tool
3. Both with and without safety net configurations
"""

import asyncio
import uuid
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Import agents
from haive.agents.simple.agent_v2 import SimpleAgentV2  # V2 with safety nets

# Try to import ReactAgent
try:
    from haive.agents.react.agent import ReactAgent

    REACT_AGENT_AVAILABLE = True
except ImportError:
    REACT_AGENT_AVAILABLE = False
    ReactAgent = None


# Define a simple tool
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


# Define a Plan model for structured output
class Plan(BaseModel):
    steps: List[str] = Field(description="list of steps")


async def example_simple_agent_v2_with_plan():
    """Example: SimpleAgent V2 with Plan model - your exact pattern."""
    print("\n=== SimpleAgent V2 with Plan Model Example ===")

    # Create engine configurations exactly as you specified
    plan_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="plan_engine",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
        structured_output_version="v2",
    )

    # Create agents - your exact pattern
    simple_agent = SimpleAgentV2(
        name="plan_agent_v2",
        engine=plan_aug,
        enable_persistence=False,  # For testing
        # V2 specific config
        use_parser_safety_net=True,
        parser_safety_net_mode="create",
    )

    print(f"Agent: {simple_agent}")
    print(f"Engine: {simple_agent.engine.name}")
    print(f"Structured output: {simple_agent.structured_output_model.__name__}")
    print(f"Graph nodes: {list(simple_agent.graph.nodes.keys())}")
    print(f"Safety net enabled: {simple_agent.use_parser_safety_net}")

    # Test with a simple request
    try:
        result = await simple_agent.ainvoke(
            {"messages": [HumanMessage(content="Create a plan for making coffee")]}
        )

        print("✅ Agent executed successfully!")
        print(f"Messages: {len(result.get('messages', []))} total")

        # Show any Plan results
        for key, value in result.items():
            if key != "messages" and value is not None:
                print(f"Result {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ Agent execution failed: {e}")
        return False


async def example_react_agent_with_add():
    """Example: ReactAgent with add tool - your exact pattern."""
    if not REACT_AGENT_AVAILABLE:
        print("\n=== ReactAgent Example - SKIPPED (not available) ===")
        return True

    print("\n=== ReactAgent with Add Tool Example ===")

    # Create engine configurations exactly as you specified
    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="add_engine",
        system_message="You are a helpful math assistant.",
        tools=[add],
    )

    # Create agents - your exact pattern
    react_agent = ReactAgent(
        name="math_agent", engine=add_aug, enable_persistence=False  # For testing
    )

    print(f"Agent: {react_agent}")
    print(f"Engine: {react_agent.engine.name}")
    print(f"Tools: {[t.name for t in react_agent.engine.tools]}")
    print(f"Graph nodes: {list(react_agent.graph.nodes.keys())}")

    # Test with a simple math request
    try:
        result = await react_agent.ainvoke(
            {"messages": [HumanMessage(content="What is 5 + 3?")]}
        )

        print("✅ ReactAgent executed successfully!")
        print(f"Messages: {len(result.get('messages', []))} total")

        # Show the conversation
        for i, msg in enumerate(result.get("messages", [])):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")

        return True

    except Exception as e:
        print(f"❌ ReactAgent execution failed: {e}")
        return False


async def example_simple_agent_v2_configurations():
    """Example: Different V2 configuration options."""
    print("\n=== SimpleAgent V2 Configuration Options ===")

    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="config_engine",
        system_message="You are a helpful assistant.",
        tools=[add],
    )

    # Example 1: Full V2 with all safety nets
    agent_full_v2 = SimpleAgentV2(
        name="full_v2",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=True,
        parser_safety_net_mode="create",
    )

    # Example 2: V2 with warnings only
    agent_warn_only = SimpleAgentV2(
        name="warn_only",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=True,
        parser_safety_net_mode="warn",
    )

    # Example 3: V2 with V1 parser behavior
    agent_v1_parser = SimpleAgentV2(
        name="v1_parser",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=False,
    )

    print("Configuration options:")
    print(
        f"  Full V2: safety_net={agent_full_v2.use_parser_safety_net}, mode={agent_full_v2.parser_safety_net_mode}"
    )
    print(
        f"  Warn only: safety_net={agent_warn_only.use_parser_safety_net}, mode={agent_warn_only.parser_safety_net_mode}"
    )
    print(f"  V1 parser: safety_net={agent_v1_parser.use_parser_safety_net}")

    return True


async def example_direct_usage_pattern():
    """Example: Direct usage pattern as you specified."""
    print("\n=== Direct Usage Pattern (Your Exact Code) ===")

    # Define your exact pattern
    @tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers"""
        return a + b

    class Plan(BaseModel):
        steps: List[str] = Field(description="list of steps")

    # Create engine configurations
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create agents
    simple_agent = SimpleAgentV2(engine=plan_aug)

    if REACT_AGENT_AVAILABLE:
        react_agent = ReactAgent(engine=add_aug)
        print(f"✅ ReactAgent created: {react_agent.name}")
    else:
        print("❌ ReactAgent not available")

    print(f"✅ SimpleAgent V2 created: {simple_agent.name}")
    print(f"   - Engine: {simple_agent.engine.name}")
    print(f"   - Structured output: {simple_agent.structured_output_model.__name__}")
    print(f"   - Graph: {list(simple_agent.graph.nodes.keys())}")

    return True


async def main():
    """Run all examples."""
    print("🧪 SimpleAgent V2 and ReactAgent Examples")
    print("=" * 60)

    examples = [
        ("SimpleAgent V2 + Plan", example_simple_agent_v2_with_plan),
        ("ReactAgent + Add Tool", example_react_agent_with_add),
        ("V2 Configuration Options", example_simple_agent_v2_configurations),
        ("Direct Usage Pattern", example_direct_usage_pattern),
    ]

    results = []

    for name, example_func in examples:
        try:
            print(f"\n{'='*60}")
            result = await example_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Example '{name}' failed: {e}")
            results.append((name, False))

    print(f"\n{'='*60}")
    print("📊 Example Results:")
    print("=" * 60)

    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"  {name:<30}: {status}")

    all_success = all(result for _, result in results)
    if all_success:
        print(f"\n🎉 All examples completed successfully!")
        print("✅ SimpleAgent V2 ready for use")
        print("✅ Configuration options working")
        if REACT_AGENT_AVAILABLE:
            print("✅ ReactAgent integration working")
    else:
        print(f"\n⚠️  Some examples had issues")

    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
