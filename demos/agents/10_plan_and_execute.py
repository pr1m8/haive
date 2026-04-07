"""Demo 10: PlanAndExecuteAgent.

Tests: Plan and Execute agent (Planner → Executor → Replanner)
"""

import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool
from haive.agents.planning.plan_and_execute import PlanAndExecuteAgent


@tool
def calculator(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        return str(eval(expression, {"__builtins__": {}}))
    except Exception as e:
        return f"Error: {e}"


def main():
    print("=" * 60)
    print("Demo 10: PlanAndExecuteAgent")
    print("=" * 60)

    agent = PlanAndExecuteAgent.create(
        tools=[calculator],
        name="demo_p_and_e",
    )
    print(f"[OK] Created: {agent.name}")
    print(f"     Agents: {[a.name for a in agent.agents]}")

    result = agent.run("What is 25 * 4, then add 50 to that result?")
    print(f"[OK] Result type: {type(result).__name__}")

    if hasattr(result, "messages") and result.messages:
        for msg in result.messages:
            if hasattr(msg, "content") and msg.content:
                tc = getattr(msg, "tool_calls", None)
                if tc:
                    print(f"  [{type(msg).__name__}]: tools={[c['name'] for c in tc]}")
                else:
                    print(f"  [{type(msg).__name__}]: {msg.content[:200]}")

    print("\n[OK] PlanAndExecuteAgent demo complete")


if __name__ == "__main__":
    main()
