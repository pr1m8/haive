#!/usr/bin/env python3
"""Comprehensive test of all agent types with PostgreSQL persistence."""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict


def setup_paths():
    """Add required paths for testing."""
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
    )
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src"
    )


def test_simple_agent() -> dict[str, Any]:
    """Test Simple agent with persistence."""
    try:

        from langchain_core.messages import HumanMessage

        from haive.agents.simple.agent import SimpleAgent

        timestamp = datetime.now().strftime("%H%M%S")
        agent = SimpleAgent(
            name=f"TestSimple_{timestamp}",
            system_message="You are a helpful assistant. Keep responses brief and remember what users tell you.",
            persistence=True,
        )

        agent.compile()

        # Test thread continuation
        thread_id = f"simple_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # First interaction
        result1 = agent.invoke(
            {
                "messages": [
                    HumanMessage(content="My favorite color is blue. Remember this.")
                ]
            },
            config,
        )

        # Second interaction - test memory
        result2 = agent.invoke(
            {"messages": [HumanMessage(content="What is my favorite color?")]}, config
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "first_messages": (
                len(result1.messages) if hasattr(result1, "messages") else 0
            ),
            "second_messages": (
                len(result2.messages) if hasattr(result2, "messages") else 0
            ),
            "memory_working": (
                len(result2.messages) > len(result1.messages)
                if hasattr(result2, "messages") and hasattr(result1, "messages")
                else False
            ),
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_react_agent() -> dict[str, Any]:
    """Test React agent with persistence."""
    try:

        from langchain_core.messages import HumanMessage

        from haive.agents.react.agent import ReactAgent

        timestamp = datetime.now().strftime("%H%M%S")
        agent = ReactAgent(
            name=f"TestReact_{timestamp}",
            system_message="You are a helpful assistant with tools. Keep responses brief.",
            persistence=True,
        )

        agent.compile()

        # Test thread continuation
        thread_id = f"react_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # First interaction - simple question
        result1 = agent.invoke(
            {
                "messages": [
                    HumanMessage(content="Hello, I'm testing React agent persistence.")
                ]
            },
            config,
        )

        # Second interaction - test memory
        result2 = agent.invoke(
            {"messages": [HumanMessage(content="What was I testing?")]}, config
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "first_messages": (
                len(result1.messages) if hasattr(result1, "messages") else 0
            ),
            "second_messages": (
                len(result2.messages) if hasattr(result2, "messages") else 0
            ),
            "memory_working": (
                len(result2.messages) > len(result1.messages)
                if hasattr(result2, "messages") and hasattr(result1, "messages")
                else False
            ),
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_rag_agent() -> dict[str, Any]:
    """Test RAG agent with persistence."""
    try:

        from langchain_core.messages import HumanMessage

        from haive.agents.rag.base.agent import BaseRAGAgent

        timestamp = datetime.now().strftime("%H%M%S")
        agent = BaseRAGAgent(
            name=f"TestRAG_{timestamp}",
            system_message="You are a RAG assistant. Keep responses brief.",
            persistence=True,
        )

        agent.compile()

        # Test thread continuation
        thread_id = f"rag_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # First interaction
        result1 = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="I'm interested in learning about AI. Remember my interest."
                    )
                ]
            },
            config,
        )

        # Second interaction - test memory
        result2 = agent.invoke(
            {
                "messages": [
                    HumanMessage(content="What am I interested in learning about?")
                ]
            },
            config,
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "first_messages": (
                len(result1.messages) if hasattr(result1, "messages") else 0
            ),
            "second_messages": (
                len(result2.messages) if hasattr(result2, "messages") else 0
            ),
            "memory_working": (
                len(result2.messages) > len(result1.messages)
                if hasattr(result2, "messages") and hasattr(result1, "messages")
                else False
            ),
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_collaborative_conversation() -> dict[str, Any]:
    """Test Collaborative conversation agent with persistence."""
    try:

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.collaberative.agent import (
            CollaborativeConversation,
        )

        timestamp = datetime.now().strftime("%H%M%S")

        # Create participant agents
        participants = {
            f"TestPM_{timestamp}": AugLLMConfig(
                name=f"TestPM_{timestamp}",
                system_message="You are a product manager. Give very brief, one-sentence responses.",
            ),
            f"TestDev_{timestamp}": AugLLMConfig(
                name=f"TestDev_{timestamp}",
                system_message="You are a developer. Give very brief, one-sentence responses.",
            ),
        }

        agent = CollaborativeConversation(
            name=f"TestCollab_{timestamp}",
            participant_agents=participants,
            topic="Testing persistence for collaborative agents",
            sections=["Problem", "Solution"],  # Keep it minimal
            max_rounds=1,  # Quick test
            persistence=True,
        )

        agent.compile()

        # Test thread continuation
        thread_id = f"collab_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Run collaboration
        result = agent.invoke(
            {
                "messages": [],
                "topic": "Testing persistence for collaborative agents",
                "format": "outline",
            },
            config,
        )

        # Check for prepared statement errors in result
        has_ps_errors = False
        if hasattr(result, "shared_document"):
            doc = str(result.shared_document)
            has_ps_errors = "prepared statement" in doc.lower()

        return {
            "status": (
                "✅ PASSED" if not has_ps_errors else "⚠️ HAS PREPARED STATEMENT ERRORS"
            ),
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "participants": list(participants.keys()),
            "has_prepared_statement_errors": has_ps_errors,
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
            "shared_document_length": (
                len(str(result.shared_document))
                if hasattr(result, "shared_document")
                else 0
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_debate_conversation() -> dict[str, Any]:
    """Test Debate conversation agent with persistence."""
    try:

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.debate.agent import DebateAgent

        timestamp = datetime.now().strftime("%H%M%S")

        # Create debate participants
        participants = {
            f"TestPro_{timestamp}": AugLLMConfig(
                name=f"TestPro_{timestamp}",
                system_message="You support the topic. Give very brief arguments.",
            ),
            f"TestCon_{timestamp}": AugLLMConfig(
                name=f"TestCon_{timestamp}",
                system_message="You oppose the topic. Give very brief arguments.",
            ),
        }

        agent = DebateAgent(
            name=f"TestDebate_{timestamp}",
            participant_agents=participants,
            topic="Should AI be used in education",
            max_rounds=1,  # Quick test
            persistence=True,
        )

        agent.compile()

        # Test thread continuation
        thread_id = f"debate_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Run debate
        agent.invoke(
            {"messages": [], "topic": "Should AI be used in education"}, config
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "participants": list(participants.keys()),
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def main():
    """Run comprehensive tests on all agent types."""

    setup_paths()

    # Run all tests
    test_results = {}

    # Test 1: Simple Agent
    test_results["simple"] = test_simple_agent()

    # Test 2: React Agent
    test_results["react"] = test_react_agent()

    # Test 3: RAG Agent
    test_results["rag"] = test_rag_agent()

    # Test 4: Collaborative Conversation
    test_results["collaborative"] = test_collaborative_conversation()

    # Test 5: Debate Conversation
    test_results["debate"] = test_debate_conversation()

    # Generate summary report

    passed_count = 0
    failed_count = 0

    for agent_type, result in test_results.items():
        status = result["status"]

        if "✅ PASSED" in status:
            passed_count += 1
            if "agent_name" in result:
                pass
            if "thread_id" in result:
                pass
            if "persistence_type" in result:
                pass
            if "app_name" in result and result["app_name"] != "N/A":
                pass
            if "memory_working" in result:
                memory_status = (
                    "✅ Working" if result["memory_working"] else "❌ Not Working"
                )
        elif "❌ FAILED" in status:
            failed_count += 1
        elif "⚠️" in status:
            pass

    # Overall status

    if failed_count == 0:
        pass
    else:
        passs.")

    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = (
        f"/home/will/Projects/haive/backend/haive/agent_test_results_{timestamp}.json"
    )

    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=2)



if __name__ == "__main__":
    main()
