"""Demo 07: DynamicSupervisor.

Tests: Supervisor that routes tasks to sub-agents via tool calls,
       with dynamic agent addition and on-the-fly agent creation.
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.dynamic_supervisor.agent import DynamicSupervisor
from langchain_core.tools import tool


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"


async def main():
    print("=" * 60)
    print("Demo 07: DynamicSupervisor")
    print("=" * 60)

    # Create supervisor
    supervisor = DynamicSupervisor(
        name="team_lead",
        engine=AugLLMConfig(temperature=0.3),
    )
    print(f"[OK] Created: {type(supervisor).__name__}")

    # Add agents dynamically
    math_agent = ReactAgent(
        name="math_expert",
        engine=AugLLMConfig(temperature=0.1, system_message="You solve math problems. Use the calculator tool."),
        tools=[calculator],
    )
    supervisor.add_agent(math_agent, "Solves math problems using calculator")
    print(f"[OK] Added math_expert")

    writer_agent = SimpleAgent(
        name="writer",
        engine=AugLLMConfig(temperature=0.8, system_message="You write short creative content."),
    )
    supervisor.add_agent(writer_agent, "Writes creative content")
    print(f"[OK] Added writer")

    # Create agent on the fly
    supervisor.create_agent(
        name="translator",
        system_message="You translate text to French.",
        description="Translates text to French",
    )
    print(f"[OK] Created translator on-the-fly")

    print(f"[OK] Agents: {list(supervisor.agents.keys())}")
    print(f"[OK] Tools: {[t.name for t in supervisor.tools]}")

    print("\n[OK] DynamicSupervisor demo complete")


if __name__ == "__main__":
    asyncio.run(main())
