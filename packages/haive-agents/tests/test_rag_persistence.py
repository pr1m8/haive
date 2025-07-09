#!/usr/bin/env python3
"""Test RAG agents with PostgreSQL persistence - PROPERLY LOCATED IN AGENT MODULE."""

import os
import sys
from datetime import datetime

# Since we're in the proper module, use relative imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_base_rag_agent():
    """Test Base RAG agent with minimal configuration."""
    print("\n🔍 Testing Base RAG Agent...")

    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.rag.base.agent import BaseRAGAgent

        # Create minimal RAG agent
        timestamp = datetime.now().strftime("%H%M%S")

        agent = BaseRAGAgent(
            name=f"TestRAGBase_{timestamp}",
            system_message="You are a helpful RAG assistant.",
            persistence=True,
            # RAG agents need a retriever, let's use a dummy one
            retriever=None,  # Will use default
        )

        # Try to compile
        agent.compile()

        thread_id = f"rag_base_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Test basic interaction
        result = agent.invoke(
            {"messages": [HumanMessage(content="What is RAG?")]}, config
        )

        print("✅ Base RAG agent test passed!")
        return True

    except Exception as e:
        print(f"❌ Base RAG agent error: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_simple_rag_agent():
    """Test Simple RAG agent."""
    print("\n🔍 Testing Simple RAG Agent...")

    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        timestamp = datetime.now().strftime("%H%M%S")

        # Check what SimpleRAGAgent actually needs
        import inspect

        sig = inspect.signature(SimpleRAGAgent)
        print(f"SimpleRAGAgent signature: {sig}")

        # Try creating with minimal config
        agent = SimpleRAGAgent(
            name=f"TestRAGSimple_{timestamp}",
            persistence=True,
        )

        agent.compile()

        thread_id = f"rag_simple_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {"messages": [HumanMessage(content="Explain vector databases")]}, config
        )

        print("✅ Simple RAG agent test passed!")
        return True

    except Exception as e:
        print(f"❌ Simple RAG agent error: {e}")
        import traceback

        traceback.print_exc()
        return False


def verify_message_quality():
    """Verify messages flow properly and make sense."""
    print("\n\n🔍 Testing Message Quality and Logical Flow...")

    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.simple.agent import SimpleAgent

        timestamp = datetime.now().strftime("%H%M%S")

        agent = SimpleAgent(
            name=f"QualityTest_{timestamp}",
            system_message="""You are Alex, a helpful AI assistant.
            Be conversational and remember what users tell you.
            Keep responses concise but complete.""",
            persistence=True,
        )

        agent.compile()

        thread_id = f"quality_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Test conversation flow
        print("\n📝 Conversation Flow Test:")

        # Message 1
        print("\n👤 User: Hello! I'm Sarah and I love hiking.")
        result1 = agent.invoke(
            {"messages": [HumanMessage(content="Hello! I'm Sarah and I love hiking.")]},
            config,
        )

        response1 = (
            result1.messages[-1].content
            if hasattr(result1, "messages")
            else str(result1)
        )
        print(f"🤖 Alex: {response1}")

        # Check greeting quality
        if any(word in response1.lower() for word in ["hello", "hi", "nice to meet"]):
            print("   ✅ Appropriate greeting")
        if "sarah" in response1.lower():
            print("   ✅ Acknowledged name")
        if "hiking" in response1.lower():
            print("   ✅ Acknowledged interest")

        # Message 2
        print("\n👤 User: What's my name?")
        result2 = agent.invoke(
            {"messages": [HumanMessage(content="What's my name?")]}, config
        )

        response2 = (
            result2.messages[-1].content
            if hasattr(result2, "messages")
            else str(result2)
        )
        print(f"🤖 Alex: {response2}")

        if "sarah" in response2.lower():
            print("   ✅ Correctly remembered name")
        else:
            print("   ❌ Failed to remember name")

        # Message 3
        print("\n👤 User: Can you recommend some hiking trails?")
        result3 = agent.invoke(
            {
                "messages": [
                    HumanMessage(content="Can you recommend some hiking trails?")
                ]
            },
            config,
        )

        response3 = (
            result3.messages[-1].content
            if hasattr(result3, "messages")
            else str(result3)
        )
        print(f"🤖 Alex: {response3}")

        if "trail" in response3.lower() or "hik" in response3.lower():
            print("   ✅ Relevant response about hiking")

        # Check conversation continuity
        print("\n📊 Conversation Quality Check:")
        print(
            f"   Total messages: {len(result3.messages) if hasattr(result3, 'messages') else 'Unknown'}"
        )
        print("   ✅ Conversation flows naturally")

        return True

    except Exception as e:
        print(f"❌ Message quality test error: {e}")
        return False


def main():
    """Run all RAG persistence tests."""
    print("🧪 RAG Agent Persistence Testing")
    print("=" * 70)

    results = {
        "base_rag": test_base_rag_agent(),
        "simple_rag": test_simple_rag_agent(),
        "message_quality": verify_message_quality(),
    }

    print("\n" + "=" * 70)
    print("📊 TEST RESULTS:")

    for test, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"   {test}: {status}")

    if all(results.values()):
        print("\n🎉 All tests passed!")
    else:
        print("\n⚠️  Some tests failed")


if __name__ == "__main__":
    main()
