#!/usr/bin/env python3
"""Test real LangMem integration with Anthropic provider.

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

    try:
        # Create agent with Anthropic provider
        anthropic_config = LLMConfig(
            provider="anthropic", model="claude-3-haiku-20240307"
        )

        agent = LTMAgent(name="Anthropic LTM Agent", llm_config=anthropic_config)
        agent.setup_agent()


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
        result = agent.extract_memories_node(state)

        # Verify results
        assert "extracted_memories" in result
        memories = result["extracted_memories"]


        # Verify we got real LangMem extraction (not fallback)
        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)
        fallback_used = any(m["source"] == "fallback_extraction" for m in memories)

        if real_langmem:

            # Print detailed memory analysis
            for i, memory in enumerate(memories):
                if isinstance(memory["content"], dict):
                    for key, value in memory["content"].items():
                        pass
                else:
                    pass

            # Verify schema diversity
            schemas = set(m["schema"] for m in memories}

            return memories

        if fallback_used:

            # Print error details if available
            if "processing_errors" in result:
                pass

        else:
            pass")

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


def test_langmem_with_groq():
    """Test LangMem with Groq provider as backup."""

    try:
        # Create agent with Groq provider
        groq_config = LLMConfig(provider="groq", model="llama3-8b-8192")

        agent = LTMAgent(name="Groq LTM Agent", llm_config=groq_config)
        agent.setup_agent()


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
        result = agent.extract_memories_node(state)

        # Verify results
        memories = result["extracted_memories"]

        # Check if real LangMem worked
        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)

        if real_langmem:
            return memories
        print("❌ Groq also fell back to simple extraction")")

    except Exception as e:
        return None


def test_langmem_with_deepseek():
    """Test LangMem with DeepSeek provider."""

    try:
        # Create agent with DeepSeek provider
        deepseek_config = LLMConfig(provider="deepseek", model="deepseek-chat")

        agent = LTMAgent(name="DeepSeek LTM Agent", llm_config=deepseek_config)
        agent.setup_agent()


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

        result = agent.extract_memories_node(state)

        memories = result["extracted_memories"]

        real_langmem = any(m["source"] == "langmem_extraction" for m in memories)

        if real_langmem:
            return memories
        print("❌ DeepSeek also used fallback")")

    except Exception as e:
        return None


def test_langchain_direct():
    """Test creating LangChain models directly to verify they work."""

    providers_to_test = [
        ("anthropic", "claude-3-haiku-20240307"),
        ("groq", "llama3-8b-8192"),
    ]

    for provider, model in providers_to_test:
        try:

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

            # Try with LangMem
            from langmem import create_memory_manager

            create_memory_manager(llm)

        except Exception as e:
            pass")


if __name__ == "__main__":

    # Test direct LangChain models first
    test_langchain_direct()

    # Test our LTM agent with different providers
    anthropic_result = test_langmem_with_anthropic()
    groq_result = test_langmem_with_groq()
    deepseek_result = test_langmem_with_deepseek()


    if anthropic_result:
        pass")
    else:
        pass")

    if groq_result:
        pass")
    else:
        pass")

    if deepseek_result:
        pass")
    else:
        pass")

    if any([anthropic_result, groq_result, deepseek_result]):
    else:
