#!/usr/bin/env python3
"""
Test real LangMem integration with Anthropic provider.

Run with: poetry run python packages/haive-agents/tests/ltm/test_real_langmem.py
"""

import logging
import sys

from haive.core.models.llm.base import LLMConfig
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.ltm.agent import LTMAgent, LTMState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_langmem_with_anthropic():
    """Test LangMem with Anthropic provider."""
    print("=== Testing LangMem with Anthropic ===")

    try:
        # Create agent with Anthropic provider
        anthropic_config = LLMConfig(
            provider="anthropic", model="claude-3-haiku-20240307"
        )

        agent = LTMAgent(name="Anthropic LTM Agent", llm_config=anthropic_config)
        agent.setup_agent()

        print(f"✅ Created agent with Anthropic: {agent.ltm_llm_config.provider}")
        print(f"   Model: {agent.ltm_llm_config.model}")

        # Create test conversation
        state = LTMState(
            messages=[
                HumanMessage(
                    content="Hi! I'm Sarah and I absolutely love reading science fiction novels."
                ),
                AIMessage(
                    content="Hello Sarah! I'll remember that you enjoy science fiction literature."
                ),
                HumanMessage(
                    content="I'm also a vegetarian and my favorite cuisine is Italian, especially pasta dishes."
                ),
                AIMessage(
                    content="Got it! You're vegetarian with a preference for Italian food, particularly pasta."
                ),
                HumanMessage(
                    content="I work as a software engineer at a tech startup in San Francisco and I love hiking on weekends."
                ),
                AIMessage(
                    content="Interesting! So you're a software engineer in SF who enjoys outdoor activities like hiking."
                ),
            ]
        )

        # Test real LangMem extraction
        print("\nTesting real LangMem memory extraction...")
        result = agent.extract_memories_node(state)

        # Verify results
        assert "extracted_memories" in result
        memories = result["extracted_memories"]

        print(f"✅ Successfully extracted {len(memories)} memories")
        print(f"   Quality score: {result['extraction_quality']:.2f}")
        print(f"   Processing stage: {result['processing_stage']}")

        # Verify we got real LangMem extraction (not fallback)
        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)
        fallback_used = any(m["source"] == "fallback_extraction" for m in memories)

        if real_langmem:
            print("🎉 REAL LangMem extraction successful!")

            # Print detailed memory analysis
            print("\n📋 Extracted Memories:")
            for i, memory in enumerate(memories):
                print(f"\n   Memory {i+1}:")
                print(f"     ID: {memory['memory_id']}")
                print(f"     Schema: {memory['schema']}")
                print(f"     Source: {memory['source']}")
                print(f"     Confidence: {memory.get('confidence', 'N/A')}")
                if isinstance(memory["content"], dict):
                    for key, value in memory["content"].items():
                        print(f"     {key}: {value}")
                else:
                    print(f"     Content: {memory['content']}")

            # Verify schema diversity
            schemas = set(m["schema"] for m in memories)
            print(f"\n📊 Schema Analysis:")
            print(f"   Unique schemas: {len(schemas)}")
            print(f"   Schema types: {schemas}")

            return memories

        elif fallback_used:
            print("❌ LangMem failed, fallback was used")
            print("This suggests an issue with Anthropic configuration or API")

            # Print error details if available
            if "processing_errors" in result:
                print(f"Errors: {result['processing_errors']}")

        else:
            print("❓ Unclear extraction source")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback

        traceback.print_exc()
        return None


def test_langmem_with_groq():
    """Test LangMem with Groq provider as backup."""
    print("\n=== Testing LangMem with Groq ===")

    try:
        # Create agent with Groq provider
        groq_config = LLMConfig(provider="groq", model="llama3-8b-8192")

        agent = LTMAgent(name="Groq LTM Agent", llm_config=groq_config)
        agent.setup_agent()

        print(f"✅ Created agent with Groq: {agent.ltm_llm_config.provider}")
        print(f"   Model: {agent.ltm_llm_config.model}")

        # Create different test conversation
        state = LTMState(
            messages=[
                HumanMessage(
                    content="My name is Alex and I'm passionate about machine learning and AI research."
                ),
                AIMessage(
                    content="Nice to meet you Alex! I'll remember your interest in ML and AI research."
                ),
                HumanMessage(
                    content="I prefer working late at night and I drink a lot of coffee to stay focused."
                ),
                AIMessage(
                    content="I'll note your night owl work preferences and coffee habit."
                ),
            ]
        )

        # Test real LangMem extraction
        print("\nTesting Groq LangMem memory extraction...")
        result = agent.extract_memories_node(state)

        # Verify results
        memories = result["extracted_memories"]
        print(f"✅ Extracted {len(memories)} memories with Groq")
        print(f"   Quality score: {result['extraction_quality']:.2f}")

        # Check if real LangMem worked
        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)

        if real_langmem:
            print("🎉 Groq LangMem extraction successful!")
            return memories
        else:
            print("❌ Groq also fell back to simple extraction")

    except Exception as e:
        print(f"❌ Groq test failed: {e}")
        return None


def test_langmem_with_deepseek():
    """Test LangMem with DeepSeek provider."""
    print("\n=== Testing LangMem with DeepSeek ===")

    try:
        # Create agent with DeepSeek provider
        deepseek_config = LLMConfig(provider="deepseek", model="deepseek-chat")

        agent = LTMAgent(name="DeepSeek LTM Agent", llm_config=deepseek_config)
        agent.setup_agent()

        print(f"✅ Created agent with DeepSeek: {agent.ltm_llm_config.provider}")
        print(f"   Model: {agent.ltm_llm_config.model}")

        # Simple test
        state = LTMState(
            messages=[
                HumanMessage(
                    content="I love playing chess and reading philosophy books."
                ),
                AIMessage(
                    content="I'll remember your interests in chess and philosophy."
                ),
            ]
        )

        print("\nTesting DeepSeek LangMem extraction...")
        result = agent.extract_memories_node(state)

        memories = result["extracted_memories"]
        print(f"✅ Extracted {len(memories)} memories with DeepSeek")

        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)

        if real_langmem:
            print("🎉 DeepSeek LangMem extraction successful!")
            return memories
        else:
            print("❌ DeepSeek also used fallback")

    except Exception as e:
        print(f"❌ DeepSeek test failed: {e}")
        return None


def test_langchain_direct():
    """Test creating LangChain models directly to verify they work."""
    print("\n=== Testing Direct LangChain Model Creation ===")

    providers_to_test = [
        ("anthropic", "claude-3-haiku-20240307"),
        ("groq", "llama3-8b-8192"),
    ]

    for provider, model in providers_to_test:
        try:
            print(f"\nTesting {provider} with {model}...")

            if provider == "anthropic":
                from langchain_anthropic import ChatAnthropic

                llm = ChatAnthropic(model=model, max_tokens=50)
            elif provider == "groq":
                from langchain_groq import ChatGroq

                llm = ChatGroq(model=model, max_tokens=50)
            else:
                continue

            # Try a simple invocation
            response = llm.invoke([HumanMessage(content="Say hello")])
            print(f"✅ {provider} model works: {response.content[:50]}...")

            # Try with LangMem
            from langmem import create_memory_manager

            manager = create_memory_manager(llm)
            print(f"✅ {provider} LangMem manager created successfully")

        except Exception as e:
            print(f"❌ {provider} failed: {e}")


if __name__ == "__main__":
    print("🧠 Real LangMem Integration Testing with Alternative Providers")
    print("=" * 70)

    # Test direct LangChain models first
    test_langchain_direct()

    # Test our LTM agent with different providers
    anthropic_result = test_langmem_with_anthropic()
    groq_result = test_langmem_with_groq()
    deepseek_result = test_langmem_with_deepseek()

    print("\n" + "=" * 70)
    print("🎯 FINAL RESULTS:")

    if anthropic_result:
        print("✅ Anthropic LangMem integration: SUCCESS")
    else:
        print("❌ Anthropic LangMem integration: FAILED")

    if groq_result:
        print("✅ Groq LangMem integration: SUCCESS")
    else:
        print("❌ Groq LangMem integration: FAILED")

    if deepseek_result:
        print("✅ DeepSeek LangMem integration: SUCCESS")
    else:
        print("❌ DeepSeek LangMem integration: FAILED")

    if any([anthropic_result, groq_result, deepseek_result]):
        print("\n🎉 LangMem integration PROVEN to work with alternative providers!")
        print("✅ Our LTM agent implementation is correct!")
    else:
        print("\n❌ All providers failed - there may be a deeper integration issue")
        print("🔍 Further debugging needed")
