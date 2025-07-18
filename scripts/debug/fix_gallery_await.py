#!/usr/bin/env python3
"""Fix await issues in gallery.rst."""

from pathlib import Path
import re


def fix_gallery_rst():
    """Fix all await issues in gallery.rst."""
    file_path = Path("docs/source/agents/gallery.rst")
    content = file_path.read_text()

    # Fix pattern 1: Structured output example
    content = re.sub(
        r"(agent = StructuredSimpleAgent\([^)]+\)\n\s*\n\s*)(review = await agent\.arun\([^)]+\)\n\s*print\(review\.rating\))",
        r"\1async def get_review():\n       \2\n   \n   import asyncio\n   asyncio.run(get_review())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 2: Research and tool use
    content = re.sub(
        r"(agent = ReactAgent\([^)]+\)\n\s*\n\s*)(result = await agent\.arun\([^)]+\))",
        r"\1async def run_research():\n       \2\n       return result\n   \n   import asyncio\n   result = asyncio.run(run_research())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 3: Code analysis
    content = re.sub(
        r"(agent = CodeAnalysisAgent\([^)]+\)\n\s*\n\s*)(analysis = await agent\.arun\([^)]+\))",
        r"\1async def analyze_code():\n       \2\n       return analysis\n   \n   import asyncio\n   analysis = asyncio.run(analyze_code())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 4: RAG agent
    content = re.sub(
        r"(agent = BaseRAGAgent\([^)]+\)\n\s*\n\s*)(answer = await agent\.arun\([^)]+\))",
        r"\1async def get_answer():\n       \2\n       return answer\n   \n   import asyncio\n   answer = asyncio.run(get_answer())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 5: Self-RAG
    content = re.sub(
        r"(agent = SelfRAGAgent\([^)]+\)\n\s*\n\s*)(result = await agent\.arun\([^)]+\))",
        r"\1async def run_self_rag():\n       \2\n       return result\n   \n   import asyncio\n   result = asyncio.run(run_self_rag())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 6: Debate
    content = re.sub(
        r"(debate = DebateAgent\([^)]+\)\n\s*\n\s*)(result = await debate\.arun\(\))",
        r"\1async def run_debate():\n       \2\n       return result\n   \n   import asyncio\n   result = asyncio.run(run_debate())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 7: Collaborative
    content = re.sub(
        r"(collab = CollaborativeAgent\([^)]+\)\n\s*\n\s*)(solution = await collab\.arun\(\))",
        r"\1async def run_collaboration():\n       \2\n       return solution\n   \n   import asyncio\n   solution = asyncio.run(run_collaboration())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 8: Sequential pipeline
    content = re.sub(
        r"(pipeline = SequentialAgent\([^)]+\)\n\s*\n\s*)(article = await pipeline\.arun\([^)]+\))",
        r"\1async def run_pipeline():\n       \2\n       return article\n   \n   import asyncio\n   article = asyncio.run(run_pipeline())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 9: Supervisor
    content = re.sub(
        r"(supervisor = SupervisorAgent\([^)]+\)\n\s*\n\s*)(result = await supervisor\.arun\([^)]+\))",
        r"\1async def run_supervisor():\n       \2\n       return result\n   \n   import asyncio\n   result = asyncio.run(run_supervisor())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 10: PlanAndExecute
    content = re.sub(
        r"(agent = PlanAndExecuteAgent\([^)]+\)\n\s*\n\s*)(fixed_code = await agent\.arun\([^}]+\}\))",
        r"\1async def fix_code():\n       \2\n       return fixed_code\n   \n   import asyncio\n   fixed_code = asyncio.run(fix_code())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 11: ReWOO
    content = re.sub(
        r"(agent = ReWOOAgent\([^)]+\)\n\s*\n\s*)(solution = await agent\.arun\([^)]+\))",
        r"\1async def run_rewoo():\n       \2\n       return solution\n   \n   import asyncio\n   solution = asyncio.run(run_rewoo())",
        content,
        flags=re.DOTALL,
    )

    # Fix pattern 12: Error handling example
    content = re.sub(
        r'(\s+)(result = await agent\.arun\("Complex task\.\.\.")\))',
        r"\1async def run_with_error_handling():\n   \1    \2\n   \1    return result\n   \1\n   \1result = asyncio.run(run_with_error_handling())",
        content,
    )

    # Write back
    file_path.write_text(content)
    print(f"Fixed: {file_path}")


if __name__ == "__main__":
    fix_gallery_rst()
