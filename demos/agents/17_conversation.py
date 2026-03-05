"""Demo 17: Conversation Agents.

Tests: BaseConversationAgent, DebateConversation
"""
import asyncio
import sys
sys.path.insert(0, ".")
from dotenv import load_dotenv
load_dotenv()

from haive.core.engine.aug_llm import AugLLMConfig

async def main():
    print("=" * 60)
    print("Demo 17: Conversation Agents")
    print("=" * 60)

    try:
        from haive.agents.conversation.base.agent import BaseConversationAgent
        print("[OK] BaseConversationAgent imported")
    except ImportError as e:
        print(f"[BROKEN] BaseConversationAgent import failed: {e}")

    try:
        from haive.agents.conversation.debate.agent import DebateConversation
        print("[OK] DebateConversation imported")
    except ImportError as e:
        print(f"[BROKEN] DebateConversation import failed: {e}")

    print("\n[OK] Conversation agents demo complete")

if __name__ == "__main__":
    asyncio.run(main())
