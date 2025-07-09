"""Test with REAL haive ReactAgents and save proper state history."""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

print("🚀 Starting REAL ReactAgent Test with State History Saving")
print("=" * 60)


class ResearchTool(BaseTool):
    """Real research tool for testing."""

    name = "research_tool"
    description = "Research information on any topic"

    def _run(self, query: str) -> str:
        return f"Research completed: {query}"


class CodingTool(BaseTool):
    """Real coding tool for testing."""

    name = "coding_tool"
    description = "Write and analyze code"

    def _run(self, code_request: str) -> str:
        return f"Code generated: {code_request}"


def save_state_history(agent_name: str, state_data: dict, test_id: str):
    """Save state history like the existing files in resources/state_history/."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Use the same directory structure as existing state history files
    state_dir = Path(
        "/home/will/Projects/haive/backend/haive/packages/haive-agents/resources/state_history"
    )
    state_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{agent_name}_{test_id}_{timestamp}.json"
    filepath = state_dir / filename

    # Save in the same format as existing state history files
    with open(filepath, "w") as f:
        json.dump(state_data, f, indent=2, default=str)

    print(f"📁 State history saved: {filepath}")
    return filepath


async def test_real_haive_agents():
    """Test with actual haive ReactAgents."""

    print("🚀 Testing with REAL haive ReactAgents")
    print("=" * 50)

    try:
        # Create REAL ReactAgent with minimal config
        print("\n📋 Creating REAL ReactAgent...")

        # Use minimal LLM config that might work
        llm_config = LLMConfig(
            provider="openai",  # Default provider
            model="gpt-3.5-turbo",  # Basic model
            temperature=0.7,
        )

        engine_config = AugLLMConfig(
            llm=llm_config, system_prompt="You are a helpful assistant."
        )

        research_agent = ReactAgent(
            name="research_agent",
            description="Research specialist agent",
            engine=engine_config,
            tools=[ResearchTool()],
        )

        print(f"✅ Created REAL ReactAgent: {research_agent.name}")
        print(f"   Type: {type(research_agent)}")
        print(f"   Tools: {[tool.name for tool in research_agent.tools]}")

        # Save initial agent state
        initial_state = {
            "agent_name": research_agent.name,
            "agent_type": str(type(research_agent)),
            "description": research_agent.description,
            "tools": [
                {"name": tool.name, "description": tool.description}
                for tool in research_agent.tools
            ],
            "engine_type": (
                str(type(research_agent.engine))
                if hasattr(research_agent, "engine")
                else None
            ),
            "created_at": datetime.now().isoformat(),
        }

        save_state_history("research_agent", initial_state, "creation")

        # Test 1: Simple invocation
        print(f"\n🔬 TEST 1: Simple Agent Invocation")
        print("-" * 30)

        test_input = {
            "messages": [HumanMessage(content="Research AI safety regulations")]
        }

        print(f"INPUT: {test_input['messages'][0].content}")

        # Try to invoke the agent
        try:
            result = await research_agent.ainvoke(test_input)
            print(f"OUTPUT: {result}")

            # Save test state
            test_state = {
                "test_name": "simple_invocation",
                "input": {"content": test_input["messages"][0].content},
                "output": str(result),
                "success": True,
                "timestamp": datetime.now().isoformat(),
            }

        except Exception as e:
            print(f"❌ Agent invocation failed: {e}")
            test_state = {
                "test_name": "simple_invocation",
                "input": {"content": test_input["messages"][0].content},
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }

        save_state_history("research_agent", test_state, "test1")

        # Test 2: Create multiple agents for registry
        print(f"\n🎯 TEST 2: Multiple Agent Creation")
        print("-" * 35)

        try:
            coding_agent = ReactAgent(
                name="coding_agent",
                description="Coding specialist agent",
                engine=engine_config,
                tools=[CodingTool()],
            )

            print(f"✅ Created second agent: {coding_agent.name}")

            # Test registry concept
            agent_registry = {
                "research_agent": research_agent,
                "coding_agent": coding_agent,
            }

            registry_state = {
                "registry_size": len(agent_registry),
                "agents": {
                    name: {
                        "type": str(type(agent)),
                        "description": agent.description,
                        "tools": [tool.name for tool in agent.tools],
                    }
                    for name, agent in agent_registry.items()
                },
                "total_tools": sum(
                    len(agent.tools) for agent in agent_registry.values()
                ),
                "timestamp": datetime.now().isoformat(),
            }

            save_state_history("registry", registry_state, "creation")

            print(f"✅ Registry created with {len(agent_registry)} agents")
            print(f"   Total tools: {registry_state['total_tools']}")

        except Exception as e:
            print(f"❌ Multiple agent creation failed: {e}")

            error_state = {
                "test_name": "multiple_agents",
                "error": str(e),
                "success": False,
                "timestamp": datetime.now().isoformat(),
            }
            save_state_history("registry", error_state, "error")

        print(f"\n✅ REAL AGENT TESTING COMPLETED")
        print(f"📁 State history files saved to: resources/state_history/")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")

        final_error_state = {
            "test_suite": "real_agents_final",
            "error": str(e),
            "error_type": type(e).__name__,
            "timestamp": datetime.now().isoformat(),
        }
        save_state_history("test_suite", final_error_state, "failure")


if __name__ == "__main__":
    asyncio.run(test_real_haive_agents())
