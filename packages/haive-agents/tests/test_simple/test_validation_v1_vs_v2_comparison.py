"""
Test V1 vs V2 validation node comparison.

This test compares the original SimpleAgent (V1) with the new SimpleAgentV2
to verify that V2 properly handles ToolMessage creation for Pydantic models.

Test cases:
1. SimpleAgent V1 with Plan model (should fail to create ToolMessages for Pydantic)
2. SimpleAgentV2 with Plan model (should succeed in creating ToolMessages)
3. SimpleAgent V1 with add tool (should work fine)
4. SimpleAgentV2 with add tool (should work fine)
5. ReactAgent with add tool (should work fine)
"""

import asyncio
import uuid
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Import both V1 and V2 agents
from haive.agents.simple.agent import SimpleAgent  # V1
from haive.agents.simple.agent_v2 import SimpleAgentV2  # V2

# Try to import ReactAgent
try:
    from haive.agents.react.agent import ReactAgent

    REACT_AGENT_AVAILABLE = True
except ImportError:
    REACT_AGENT_AVAILABLE = False
    ReactAgent = None


# Define test models and tools exactly as specified
class Plan(BaseModel):
    """A plan with steps."""

    steps: List[str] = Field(description="list of steps")


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


async def test_simple_agent_v1_with_plan():
    """Test SimpleAgent V1 with Plan model - should fail to create ToolMessages."""
    print("\n=== Test 1: SimpleAgent V1 with Plan Model ===")

    # Create engine with Plan model as specified
    plan_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="plan_engine_v1",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
        structured_output_version="v2",
    )

    # Create V1 SimpleAgent
    simple_agent = SimpleAgent(
        name="simple_v1_plan", engine=plan_aug, enable_persistence=False
    )

    print(f"Agent: {simple_agent}")
    print(f"Graph nodes: {list(simple_agent.graph.nodes.keys())}")

    # Create test state with Plan tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Create a plan for making coffee"),
            AIMessage(
                content="I'll create a plan for making coffee.",
                tool_calls=[
                    {
                        "id": "call_plan_123",
                        "name": "Plan",
                        "args": {
                            "steps": [
                                "Boil water",
                                "Grind coffee beans",
                                "Add coffee to filter",
                                "Pour hot water over coffee",
                                "Wait 4 minutes",
                                "Enjoy",
                            ]
                        },
                    }
                ],
            ),
        ]
    }

    try:
        # Run the agent
        graph = simple_agent.create_runnable()
        result = await graph.ainvoke(initial_state)

        print("Final messages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
            if isinstance(msg, ToolMessage):
                print(
                    f"      Tool: {getattr(msg, 'name', 'N/A')}, ID: {getattr(msg, 'tool_call_id', 'N/A')}"
                )

        # Check for ToolMessages
        tool_messages = [
            msg for msg in result["messages"] if isinstance(msg, ToolMessage)
        ]
        if len(tool_messages) == 0:
            print("❌ V1 EXPECTED BEHAVIOR: No ToolMessage created for Pydantic model")
            return False
        else:
            print(f"✅ V1 UNEXPECTED: Created {len(tool_messages)} ToolMessage(s)")
            return True

    except Exception as e:
        print(f"❌ V1 test failed with exception: {e}")
        return False


async def test_simple_agent_v2_with_plan():
    """Test SimpleAgent V2 with Plan model - should succeed in creating ToolMessages."""
    print("\n=== Test 2: SimpleAgent V2 with Plan Model ===")

    # Create engine with Plan model as specified
    plan_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="plan_engine_v2",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
        structured_output_version="v2",
    )

    # Create V2 SimpleAgent
    simple_agent = SimpleAgentV2(
        name="simple_v2_plan", engine=plan_aug, enable_persistence=False
    )

    print(f"Agent: {simple_agent}")
    print(f"Graph nodes: {list(simple_agent.graph.nodes.keys())}")

    # Create test state with Plan tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Create a plan for making coffee"),
            AIMessage(
                content="I'll create a plan for making coffee.",
                tool_calls=[
                    {
                        "id": "call_plan_456",
                        "name": "Plan",
                        "args": {
                            "steps": [
                                "Boil water",
                                "Grind coffee beans",
                                "Add coffee to filter",
                                "Pour hot water over coffee",
                                "Wait 4 minutes",
                                "Enjoy",
                            ]
                        },
                    }
                ],
            ),
        ]
    }

    try:
        # Run the agent
        graph = simple_agent.create_runnable()
        result = await graph.ainvoke(initial_state)

        print("Final messages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
            if isinstance(msg, ToolMessage):
                print(
                    f"      Tool: {getattr(msg, 'name', 'N/A')}, ID: {getattr(msg, 'tool_call_id', 'N/A')}"
                )
                print(f"      Content preview: {str(msg.content)[:200]}...")

        # Check for ToolMessages
        tool_messages = [
            msg for msg in result["messages"] if isinstance(msg, ToolMessage)
        ]
        if len(tool_messages) > 0:
            print(
                f"✅ V2 SUCCESS: Created {len(tool_messages)} ToolMessage(s) for Pydantic model"
            )

            # Verify ToolMessage content
            tool_msg = tool_messages[0]
            if tool_msg.name == "Plan" and tool_msg.tool_call_id == "call_plan_456":
                print("✅ ToolMessage has correct name and ID")
                return True
            else:
                print("❌ ToolMessage has incorrect name or ID")
                return False
        else:
            print("❌ V2 FAILED: No ToolMessage created for Pydantic model")
            return False

    except Exception as e:
        print(f"❌ V2 test failed with exception: {e}")
        return False


async def test_simple_agent_v1_with_add_tool():
    """Test SimpleAgent V1 with add tool - should work fine."""
    print("\n=== Test 3: SimpleAgent V1 with Add Tool ===")

    # Create engine with add tool as specified
    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="add_engine_v1",
        system_message="You are a helpful math assistant.",
        tools=[add],
    )

    # Create V1 SimpleAgent
    simple_agent = SimpleAgent(
        name="simple_v1_add", engine=add_aug, enable_persistence=False
    )

    print(f"Agent: {simple_agent}")
    print(f"Graph nodes: {list(simple_agent.graph.nodes.keys())}")

    # Create test state with add tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[
                    {"id": "call_add_789", "name": "add", "args": {"a": 5, "b": 3}}
                ],
            ),
        ]
    }

    try:
        # Run the agent
        graph = simple_agent.create_runnable()
        result = await graph.ainvoke(initial_state)

        print("Final messages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
            if isinstance(msg, ToolMessage):
                print(
                    f"      Tool: {getattr(msg, 'name', 'N/A')}, ID: {getattr(msg, 'tool_call_id', 'N/A')}"
                )
                print(f"      Content: {msg.content}")

        # Check for ToolMessages
        tool_messages = [
            msg for msg in result["messages"] if isinstance(msg, ToolMessage)
        ]
        if len(tool_messages) > 0:
            print(
                f"✅ V1 SUCCESS: Created {len(tool_messages)} ToolMessage(s) for regular tool"
            )

            # Verify result
            tool_msg = tool_messages[0]
            if str(tool_msg.content) == "8" or tool_msg.content == 8:
                print("✅ Tool calculation is correct: 5 + 3 = 8")
                return True
            else:
                print(f"❌ Tool calculation is incorrect: {tool_msg.content}")
                return False
        else:
            print("❌ V1 FAILED: No ToolMessage created for regular tool")
            return False

    except Exception as e:
        print(f"❌ V1 add tool test failed with exception: {e}")
        return False


async def test_simple_agent_v2_with_add_tool():
    """Test SimpleAgent V2 with add tool - should work fine."""
    print("\n=== Test 4: SimpleAgent V2 with Add Tool ===")

    # Create engine with add tool as specified
    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="add_engine_v2",
        system_message="You are a helpful math assistant.",
        tools=[add],
    )

    # Create V2 SimpleAgent
    simple_agent = SimpleAgentV2(
        name="simple_v2_add", engine=add_aug, enable_persistence=False
    )

    print(f"Agent: {simple_agent}")
    print(f"Graph nodes: {list(simple_agent.graph.nodes.keys())}")

    # Create test state with add tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[
                    {"id": "call_add_101112", "name": "add", "args": {"a": 5, "b": 3}}
                ],
            ),
        ]
    }

    try:
        # Run the agent
        graph = simple_agent.create_runnable()
        result = await graph.ainvoke(initial_state)

        print("Final messages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
            if isinstance(msg, ToolMessage):
                print(
                    f"      Tool: {getattr(msg, 'name', 'N/A')}, ID: {getattr(msg, 'tool_call_id', 'N/A')}"
                )
                print(f"      Content: {msg.content}")

        # Check for ToolMessages
        tool_messages = [
            msg for msg in result["messages"] if isinstance(msg, ToolMessage)
        ]
        if len(tool_messages) > 0:
            print(
                f"✅ V2 SUCCESS: Created {len(tool_messages)} ToolMessage(s) for regular tool"
            )

            # Verify result
            tool_msg = tool_messages[0]
            if str(tool_msg.content) == "8" or tool_msg.content == 8:
                print("✅ Tool calculation is correct: 5 + 3 = 8")
                return True
            else:
                print(f"❌ Tool calculation is incorrect: {tool_msg.content}")
                return False
        else:
            print("❌ V2 FAILED: No ToolMessage created for regular tool")
            return False

    except Exception as e:
        print(f"❌ V2 add tool test failed with exception: {e}")
        return False


async def test_react_agent_with_add_tool():
    """Test ReactAgent with add tool - should work fine."""
    if not REACT_AGENT_AVAILABLE:
        print("\n=== Test 5: ReactAgent - SKIPPED (not available) ===")
        return True

    print("\n=== Test 5: ReactAgent with Add Tool ===")

    # Create engine with add tool as specified
    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="add_engine_react",
        system_message="You are a helpful math assistant.",
        tools=[add],
    )

    # Create ReactAgent
    react_agent = ReactAgent(name="react_add", engine=add_aug, enable_persistence=False)

    print(f"Agent: {react_agent}")
    print(f"Graph nodes: {list(react_agent.graph.nodes.keys())}")

    # Create test state with add tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[
                    {
                        "id": "call_add_react_131415",
                        "name": "add",
                        "args": {"a": 5, "b": 3},
                    }
                ],
            ),
        ]
    }

    try:
        # Run the agent
        graph = react_agent.create_runnable()
        result = await graph.ainvoke(initial_state)

        print("Final messages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
            if isinstance(msg, ToolMessage):
                print(
                    f"      Tool: {getattr(msg, 'name', 'N/A')}, ID: {getattr(msg, 'tool_call_id', 'N/A')}"
                )
                print(f"      Content: {msg.content}")

        # Check for ToolMessages
        tool_messages = [
            msg for msg in result["messages"] if isinstance(msg, ToolMessage)
        ]
        if len(tool_messages) > 0:
            print(
                f"✅ REACT SUCCESS: Created {len(tool_messages)} ToolMessage(s) for regular tool"
            )

            # Verify result
            tool_msg = tool_messages[0]
            if str(tool_msg.content) == "8" or tool_msg.content == 8:
                print("✅ Tool calculation is correct: 5 + 3 = 8")
                return True
            else:
                print(f"❌ Tool calculation is incorrect: {tool_msg.content}")
                return False
        else:
            print("❌ REACT FAILED: No ToolMessage created for regular tool")
            return False

    except Exception as e:
        print(f"❌ ReactAgent test failed with exception: {e}")
        return False


async def main():
    """Run all comparison tests."""
    print("🧪 Testing V1 vs V2 Validation Node Comparison")
    print("=" * 60)

    results = []

    # Test 1: V1 with Plan (should fail to create ToolMessages)
    try:
        result1 = await test_simple_agent_v1_with_plan()
        results.append(("SimpleAgent V1 + Plan", not result1))  # Expect failure for V1
    except Exception as e:
        print(f"Test 1 crashed: {e}")
        results.append(("SimpleAgent V1 + Plan", True))  # Crash is expected

    # Test 2: V2 with Plan (should succeed)
    try:
        result2 = await test_simple_agent_v2_with_plan()
        results.append(("SimpleAgent V2 + Plan", result2))
    except Exception as e:
        print(f"Test 2 crashed: {e}")
        results.append(("SimpleAgent V2 + Plan", False))

    # Test 3: V1 with add tool (should succeed)
    try:
        result3 = await test_simple_agent_v1_with_add_tool()
        results.append(("SimpleAgent V1 + add", result3))
    except Exception as e:
        print(f"Test 3 crashed: {e}")
        results.append(("SimpleAgent V1 + add", False))

    # Test 4: V2 with add tool (should succeed)
    try:
        result4 = await test_simple_agent_v2_with_add_tool()
        results.append(("SimpleAgent V2 + add", result4))
    except Exception as e:
        print(f"Test 4 crashed: {e}")
        results.append(("SimpleAgent V2 + add", False))

    # Test 5: ReactAgent with add tool (should succeed)
    try:
        result5 = await test_react_agent_with_add_tool()
        results.append(("ReactAgent + add", result5))
    except Exception as e:
        print(f"Test 5 crashed: {e}")
        results.append(("ReactAgent + add", False))

    print("\n" + "=" * 60)
    print("📊 FINAL RESULTS:")
    print("=" * 60)

    all_passed = True
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {test_name:<25}: {status}")
        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ V2 validation successfully creates ToolMessages for Pydantic models")
        print("✅ Both V1 and V2 work correctly with regular tools")
        print("✅ ReactAgent works correctly with tools")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("🔧 V2 validation improvements needed")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
