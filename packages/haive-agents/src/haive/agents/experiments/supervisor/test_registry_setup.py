#!/usr/bin/env python3
"""Step 1: Test registry setup with real agents."""

from typing import Any, Dict, List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Step 1: Create real tools
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Returns the product of two numbers"""
    return a * b


# Planning model
class Plan(BaseModel):
    steps: List[str] = Field(description="list of steps")


# Step 2: Create real agents
def create_test_agents():
    """Create real agents for testing"""
    # Math agent with tools
    math_aug = AugLLMConfig(tools=[add, multiply])
    math_agent = ReactAgent(name="math_agent", engine=math_aug)

    # Planning agent with structured output
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    planning_agent = SimpleAgent(name="planning_agent", engine=plan_aug)

    return {"math_agent": math_agent, "planning_agent": planning_agent}


# Step 3: Simple registry
class AgentRegistry:
    def __init__(self):
        self.agents = {}

    def register(self, name: str, agent: Any, description: str):
        self.agents[name] = {"agent": agent, "description": description}
        print(f"Registered {name}: {description}")

    def get(self, name: str):
        entry = self.agents.get(name)
        return entry["agent"] if entry else None

    def list_available(self) -> Dict[str, str]:
        return {name: entry["description"] for name, entry in self.agents.items()}

    def has_agent(self, name: str) -> bool:
        return name in self.agents


# Step 4: Tests
def test_registry_basic():
    """Test 1: Registry stores and retrieves agents"""
    print("\n=== Test 1: Basic Registry ===")

    registry = AgentRegistry()

    # Create simple test agent
    test_agent = SimpleAgent(name="test_agent")
    registry.register("test_agent", test_agent, "Test agent")

    # Check it's there
    assert registry.has_agent("test_agent"), "Agent not found in registry"
    retrieved = registry.get("test_agent")
    assert retrieved.name == "test_agent", f"Expected test_agent, got {retrieved.name}"

    # Check description
    available = registry.list_available()
    assert available["test_agent"] == "Test agent", "Description mismatch"

    print("✓ Registry basic functionality works")
    return registry


def test_registry_with_real_agents():
    """Test 2: Registry with actual configured agents"""
    print("\n=== Test 2: Real Agents in Registry ===")

    registry = AgentRegistry()
    agents = create_test_agents()

    # Register real agents
    registry.register(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )
    registry.register(
        "planning_agent", agents["planning_agent"], "Creates structured plans"
    )

    # Test registry contents
    assert registry.has_agent("math_agent"), "Math agent not found"
    assert registry.has_agent("planning_agent"), "Planning agent not found"

    available = registry.list_available()
    print(f"Available agents: {available}")

    print("✓ Registry with real agents works")
    return registry


def test_individual_agents():
    """Test 3: Individual agents work correctly"""
    print("\n=== Test 3: Individual Agent Functionality ===")

    agents = create_test_agents()

    # Test math agent
    print("Testing math agent...")
    try:
        math_result = agents["math_agent"].invoke(
            {"messages": [HumanMessage("What is 5 + 3?")]}
        )
        print(f"Math result: {math_result}")
        # Look for 8 in the result
        result_str = str(math_result)
        assert "8" in result_str, f"Expected '8' in result, got: {result_str}"
        print("✓ Math agent works")
    except Exception as e:
        print(f"✗ Math agent failed: {e}")
        raise

    # Test planning agent
    print("Testing planning agent...")
    try:
        plan_result = agents["planning_agent"].invoke(
            {"messages": [HumanMessage("Plan a dinner party")]}
        )
        print(f"Plan result: {plan_result}")
        result_str = str(plan_result)
        # Look for steps or planning content
        assert (
            "steps" in result_str.lower() or "plan" in result_str.lower()
        ), f"Expected planning content, got: {result_str}"
        print("✓ Planning agent works")
    except Exception as e:
        print(f"✗ Planning agent failed: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Testing Registry Setup with Real Agents")

    # Run tests in order
    try:
        test_registry_basic()
        registry = test_registry_with_real_agents()
        test_individual_agents()

        print("\n🎉 All Step 1 tests passed!")
        print("Registry setup with real agents is working correctly.")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise
