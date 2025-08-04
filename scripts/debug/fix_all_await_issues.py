#!/usr/bin/env python3
"""Fix all await outside function issues in documentation."""

from __future__ import annotations

from pathlib import Path

FIXES = [
    # gallery.rst - Structured output
    {
        "file":
        "docs/source/agents/gallery.rst",
        "find":
        """   agent = StructuredSimpleAgent(
       name="reviewer",
       output_schema=MovieReview
   )

   review = await agent.arun(
       "Review the movie 'Inception' directed by Christopher Nolan"
   )
   print(review.rating)  # Structured output""",
        "replace":
        """   agent = StructuredSimpleAgent(
       name="reviewer",
       output_schema=MovieReview
   )

   import asyncio

   async def get_review():
       review = await agent.arun(
           "Review the movie 'Inception' directed by Christopher Nolan"
       )
       print(review.rating)  # Structured output
       return review

   review = asyncio.run(get_review())""",
    },
    # gallery.rst - Research with tools
    {
        "file":
        "docs/source/agents/gallery.rst",
        "find":
        """   agent = ReactAgent(
       name="researcher",
       tools=[web_search_tool, calculator_tool],
       engine=AugLLMConfig()
   )

   result = await agent.arun(
       "What's the current population of Tokyo and how much has it grown in the last decade?"
   )""",
        "replace":
        """   agent = ReactAgent(
       name="researcher",
       tools=[web_search_tool, calculator_tool],
       engine=AugLLMConfig()
   )

   import asyncio

   async def run_research():
       result = await agent.arun(
           "What's the current population of Tokyo and how much has it grown in the last decade?"
       )
       return result

   result = asyncio.run(run_research())""",
    },
    # gallery.rst - Code analysis
    {
        "file":
        "docs/source/agents/gallery.rst",
        "find":
        """   agent = CodeAnalysisAgent(
       name="code_reviewer",
       analysis_depth="comprehensive"
   )

   analysis = await agent.arun(
       code_snippet=python_code,
       focus_areas=["security", "performance", "maintainability"]
   )""",
        "replace":
        """   agent = CodeAnalysisAgent(
       name="code_reviewer",
       analysis_depth="comprehensive"
   )

   import asyncio

   async def analyze_code():
       analysis = await agent.arun(
           code_snippet=python_code,
           focus_areas=["security", "performance", "maintainability"]
       )
       return analysis

   analysis = asyncio.run(analyze_code())""",
    },
    # index.rst - Quick start
    {
        "file":
        "docs/source/agents/index.rst",
        "find":
        """result = await agent.arun("Tell me about the benefits of renewable energy")
print(result)""",
        "replace":
        """import asyncio

async def main():
    result = await agent.arun("Tell me about the benefits of renewable energy")
    print(result)

asyncio.run(main())""",
    },
    # examples/index.rst
    {
        "file":
        "docs/source/examples/index.rst",
        "find":
        """# Run the agent
result = await agent.arun("What is machine learning?")
print(result)""",
        "replace":
        """# Run the agent
import asyncio

async def run_agent():
    result = await agent.arun("What is machine learning?")
    print(result)
    return result

result = asyncio.run(run_agent())""",
    },
    # examples/index.rst - second instance
    {
        "file":
        "docs/source/examples/index.rst",
        "find":
        """# Use the agent with tools
result = await agent.arun(
    "Find the latest news about renewable energy and summarize the key points"
)""",
        "replace":
        """# Use the agent with tools
import asyncio

async def run_with_tools():
    result = await agent.arun(
        "Find the latest news about renewable energy and summarize the key points"
    )
    return result

result = asyncio.run(run_with_tools())""",
    },
    # examples/index.rst - third instance
    {
        "file":
        "docs/source/examples/index.rst",
        "find":
        """# Run multi-agent system
result = await team.arun({
    "task": "Create a marketing strategy for a new eco-friendly product",
    "requirements": ["market analysis", "competitor research", "campaign ideas"]
})""",
        "replace":
        """# Run multi-agent system
import asyncio

async def run_team():
    result = await team.arun({
        "task": "Create a marketing strategy for a new eco-friendly product",
        "requirements": ["market analysis", "competitor research", "campaign ideas"]
    })
    return result

result = asyncio.run(run_team())""",
    },
    # games/index.rst
    {
        "file":
        "docs/source/games/index.rst",
        "find":
        """# Play one move
state = game.get_state()
action = await agent.arun({
    "game_state": state,
    "legal_moves": game.get_legal_moves()
})
game.make_move(action)""",
        "replace":
        """# Play one move
import asyncio

async def play_move():
    state = game.get_state()
    action = await agent.arun({
        "game_state": state,
        "legal_moves": game.get_legal_moves()
    })
    game.make_move(action)
    return action

asyncio.run(play_move())""",
    },
]


def apply_fixes():
    """Apply all the fixes."""
    for fix in FIXES:
        file_path = Path(fix["file"])
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue

        content = file_path.read_text()

        if fix["find"] in content:
            content = content.replace(fix["find"], fix["replace"])
            file_path.write_text(content)
            print(f"Fixed: {file_path}")
        else:
            print(f"Pattern not found in: {file_path}")


if __name__ == "__main__":
    apply_fixes()
