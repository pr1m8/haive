"""Demo 50: Perplexity-style Research Agent.

Tests: QueryAnalyzer → Researcher (search + RAG) → Synthesizer
"""

import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.agents.research.perplexity_agent import create_research_agent


def main():
    print("=" * 60)
    print("Demo 50: Perplexity Research Agent")
    print("=" * 60)

    agent = create_research_agent(name="demo_research", max_search_iterations=5)
    print(f"[OK] Created: {agent.name}")
    print(f"     Sub-agents: {[a.name for a in agent.agents]}")
    tools = [t.name for t in agent.agents[1].engine.tools if hasattr(t, "name")]
    # Dedupe for display
    print(f"     Researcher tools: {list(dict.fromkeys(tools))}")

    print("\n--- Running research ---")
    result = agent.run("What are the main approaches to AI alignment and safety?")

    if hasattr(result, "messages") and result.messages:
        for msg in result.messages:
            if hasattr(msg, "content") and msg.content:
                tc = getattr(msg, "tool_calls", None)
                if tc:
                    print(f"  [{type(msg).__name__}]: tools={[c['name'] for c in tc]}")
                elif len(msg.content) > 0:
                    print(f"  [{type(msg).__name__}]: {msg.content[:300]}")

    print("\n[OK] Research agent demo complete")


if __name__ == "__main__":
    main()
