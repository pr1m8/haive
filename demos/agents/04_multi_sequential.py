"""Demo 04: Sequential Multi-Agent Workflow.

Tests: Chaining SimpleAgents sequentially (agent1 output -> agent2 input)
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple.agent import SimpleAgent


async def main():
    print("=" * 60)
    print("Demo 04: Sequential Multi-Agent (Manual Chain)")
    print("=" * 60)

    researcher = SimpleAgent(
        name="researcher",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are a researcher. Given a topic, provide 3 key facts. Be concise (max 3 sentences).",
        ),
    )
    print(f"[OK] Researcher: {researcher.name}")

    writer = SimpleAgent(
        name="writer",
        engine=AugLLMConfig(
            temperature=0.7,
            system_message="You are a writer. Take the research facts provided and write a short paragraph (3-4 sentences).",
        ),
    )
    print(f"[OK] Writer: {writer.name}")

    print("\n--- Step 1: Research ---")
    research_result = await researcher.arun("Renewable energy in 2025")
    research_text = str(research_result)
    # Extract content from result
    if hasattr(research_result, "get") and "messages" in research_result:
        msgs = research_result["messages"]
        if msgs:
            research_text = msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    elif hasattr(research_result, "messages"):
        msgs = research_result.messages
        if msgs:
            research_text = msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    print(f"Research: {research_text[:200]}")

    print("\n--- Step 2: Write ---")
    write_result = await writer.arun(f"Write a paragraph based on these facts:\n{research_text}")
    write_text = str(write_result)
    if hasattr(write_result, "get") and "messages" in write_result:
        msgs = write_result["messages"]
        if msgs:
            write_text = msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    elif hasattr(write_result, "messages"):
        msgs = write_result.messages
        if msgs:
            write_text = msgs[-1].content if hasattr(msgs[-1], "content") else str(msgs[-1])
    print(f"Written: {write_text[:300]}")

    print("\n[OK] Sequential multi-agent demo complete")


if __name__ == "__main__":
    asyncio.run(main())
