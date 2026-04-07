"""Demo 47: Task Analysis Agent.

Tests: TaskAnalysisAgent - decomposes complex tasks into subtasks
"""

import asyncio
import sys
sys.path.insert(0, ".")

from dotenv import load_dotenv
load_dotenv()


async def main():
    print("=" * 60)
    print("Demo 47: Task Analysis Agent")
    print("=" * 60)

    from haive.agents.task_analysis.agent import TaskAnalysisAgent
    from haive.core.engine.aug_llm import AugLLMConfig

    agent = TaskAnalysisAgent(name="task_analyzer", engine=AugLLMConfig())
    print(f"[OK] TaskAnalysisAgent created")

    g = agent.compile()
    print(f"[OK] Compiled: {type(g).__name__}")
    print("\n[OK] Task analysis demo complete")


if __name__ == "__main__":
    asyncio.run(main())
