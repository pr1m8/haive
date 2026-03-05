"""Demo 05: Parallel Multi-Agent Workflow.

Tests: Running multiple SimpleAgents in parallel with asyncio.gather
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent


def extract_text(result):
    """Extract text content from agent result."""
    if hasattr(result, "get") and "messages" in result:
        msgs = result["messages"]
        if msgs:
            return msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    elif hasattr(result, "messages"):
        msgs = result.messages
        if msgs:
            return msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    return str(result)


async def main():
    print("=" * 60)
    print("Demo 05: Parallel Multi-Agent")
    print("=" * 60)

    topic = "Should we adopt AI-powered customer service?"

    tech_analyst = SimpleAgent(
        name="tech_analyst",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You analyze technical feasibility. Give 2-3 bullet points. Be concise (max 3 sentences).",
        ),
    )

    biz_analyst = SimpleAgent(
        name="biz_analyst",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You analyze business impact. Give 2-3 bullet points. Be concise (max 3 sentences).",
        ),
    )

    risk_analyst = SimpleAgent(
        name="risk_analyst",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You identify risks and mitigations. Give 2-3 bullet points. Be concise (max 3 sentences).",
        ),
    )

    print(f"[OK] Created 3 analysts")

    print(f"\n--- Running 3 agents in parallel ---")
    results = await asyncio.gather(
        tech_analyst.arun(topic),
        biz_analyst.arun(topic),
        risk_analyst.arun(topic),
    )

    names = ["Tech Analysis", "Business Analysis", "Risk Analysis"]
    for name, result in zip(names, results):
        text = extract_text(result)
        print(f"\n{name}:\n  {text[:200]}")

    print("\n[OK] Parallel multi-agent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
