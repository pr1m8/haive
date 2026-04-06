"""Demo 51: Deep Research Agent.

5-stage pipeline: Planner → Researcher (search+RAG) → Analyzer (RAG) → FactChecker → Writer
"""

import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.agents.research.deep_research_agent import create_deep_research_agent


def main():
    print("=" * 60)
    print("Demo 51: Deep Research Agent")
    print("=" * 60)

    agent = create_deep_research_agent(
        name="demo_deep",
        max_search_iterations=5,
        include_fact_check=True,
    )
    print(f"[OK] Created: {agent.name}")
    print(f"     Pipeline: {[a.name for a in agent.agents]}")

    print("\n--- Running deep research ---")
    result = agent.run("Compare React and Vue.js frameworks for web development in 2025")

    if hasattr(result, "messages") and result.messages:
        # Show only AI responses (skip tool calls and tool messages for clean output)
        ai_msgs = [m for m in result.messages if type(m).__name__ == "AIMessage"
                    and hasattr(m, "content") and m.content and not getattr(m, "tool_calls", None)]
        for msg in ai_msgs[-2:]:  # Show last 2 AI messages (fact check + report)
            print(f"\n  [{type(msg).__name__}]: {msg.content[:500]}")

    print("\n[OK] Deep research demo complete")


if __name__ == "__main__":
    main()
