"""Demo 06: DynamicSupervisor.

Tests: DynamicSupervisor with runtime agent management
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.supervisor.dynamic.dynamic_supervisor import DynamicSupervisor


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"


async def main():
    print("=" * 60)
    print("Demo 06: DynamicSupervisor")
    print("=" * 60)

    supervisor = DynamicSupervisor(
        name="demo_supervisor",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are a supervisor that routes tasks to appropriate agents.",
        ),
    )
    print(f"[OK] Instantiated: {supervisor.name}")

    # Add sub-agents
    math_agent = ReactAgent(
        name="math_expert",
        engine=AugLLMConfig(
            temperature=0.1,
            system_message="You are a math expert. Use the calculator tool.",
        ),
        tools=[calculator],
    )

    writer_agent = SimpleAgent(
        name="writer",
        engine=AugLLMConfig(
            temperature=0.8,
            system_message="You are a creative writer. Write short, engaging responses.",
        ),
    )

    # Try to add agents dynamically
    try:
        supervisor.add_agent(math_agent)
        supervisor.add_agent(writer_agent)
        print(f"[OK] Added agents: math_expert, writer")
    except Exception as e:
        print(f"[WARN] add_agent not available: {e}")
        print("       DynamicSupervisor may need different agent registration")

    print("\n--- Running arun ---")
    try:
        result = await supervisor.arun("What is 42 * 17?")
        print(f"Result type: {type(result)}")
        print(f"Result: {str(result)[:300]}")
        print("\n[OK] DynamicSupervisor demo complete")
    except Exception as e:
        print(f"[BROKEN] arun failed: {e}")
        print("         This may need sub-agent registration to work")


if __name__ == "__main__":
    asyncio.run(main())
