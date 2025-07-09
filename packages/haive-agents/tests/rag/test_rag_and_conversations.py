#!/usr/bin/env python3
"""Test RAG agents and all conversation agents with PostgreSQL persistence."""

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


def test_rag_base_agent() -> Dict[str, Any]:
    """Test RAG Base agent with persistence."""
    try:
        print("🔄 Testing RAG Base Agent...")

        from langchain_core.messages import HumanMessage

        from haive.agents.rag.base.agent import BaseRAGAgent

        timestamp = datetime.now().strftime("%H%M%S")
        agent = BaseRAGAgent(
            name=f"TestRAGBase_{timestamp}",
            system_message="You are a RAG assistant. Keep responses brief.",
            persistence=True,
        )

        agent.compile()

        thread_id = f"rag_base_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Test with simple query
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(
                        content="Hello, I need help with information retrieval."
                    )
                ]
            },
            config,
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_rag_simple_agent() -> Dict[str, Any]:
    """Test Simple RAG agent with persistence."""
    try:
        print("🔄 Testing Simple RAG Agent...")

        from langchain_core.messages import HumanMessage

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        timestamp = datetime.now().strftime("%H%M%S")
        agent = SimpleRAGAgent(
            name=f"TestRAGSimple_{timestamp}",
            system_message="You are a simple RAG assistant. Keep responses brief.",
            persistence=True,
        )

        agent.compile()

        thread_id = f"rag_simple_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        # Test with simple query
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content="What is retrieval augmented generation?")
                ]
            },
            config,
        )

        return {
            "status": "✅ PASSED",
            "agent_name": agent.name,
            "thread_id": thread_id,
            "persistence_type": type(agent.persistence).__name__,
            "app_name": (
                agent.persistence.connection_kwargs.get("application_name", "N/A")
                if hasattr(agent.persistence, "connection_kwargs")
                else "N/A"
            ),
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_collaborative_conversation() -> Dict[str, Any]:
    """Test Collaborative conversation agent."""
    try:
        print("🔄 Testing Collaborative Conversation Agent...")

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.collaberative.agent import (
            CollaborativeConversation,
        )

        timestamp = datetime.now().strftime("%H%M%S")

        participants = {
            f"PM_{timestamp}": AugLLMConfig(
                name=f"PM_{timestamp}",
                system_message="You are a product manager. Give brief responses.",
            ),
            f"Dev_{timestamp}": AugLLMConfig(
                name=f"Dev_{timestamp}",
                system_message="You are a developer. Give brief responses.",
            ),
        }

        agent = CollaborativeConversation(
            name=f"TestCollab_{timestamp}",
            participant_agents=participants,
            topic="Testing collaborative persistence",
            sections=["Issue", "Solution"],
            max_rounds=1,
            persistence=True,
        )

        agent.compile()

        thread_id = f"collab_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {
                "messages": [],
                "topic": "Testing collaborative persistence",
                "format": "outline",
            },
            config,
        )

        # Check for prepared statement errors
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
        }

    except Exception as e:
        return {"status": "❌ FAILED", "error": str(e), "error_type": type(e).__name__}


def test_debate_conversation() -> Dict[str, Any]:
    """Test Debate conversation agent."""
    try:
        print("🔄 Testing Debate Conversation Agent...")

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.debate.agent import DebateConversation

        timestamp = datetime.now().strftime("%H%M%S")

        participants = {
            f"Pro_{timestamp}": AugLLMConfig(
                name=f"Pro_{timestamp}",
                system_message="You support the topic. Give brief arguments.",
            ),
            f"Con_{timestamp}": AugLLMConfig(
                name=f"Con_{timestamp}",
                system_message="You oppose the topic. Give brief arguments.",
            ),
        }

        agent = DebateConversation(
            name=f"TestDebate_{timestamp}",
            participant_agents=participants,
            topic="AI should be regulated",
            debate_positions={
                f"Pro_{timestamp}": "For AI regulation",
                f"Con_{timestamp}": "Against AI regulation",
            },
            max_rounds=1,
            persistence=True,
        )

        agent.compile()

        thread_id = f"debate_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {"messages": [], "topic": "AI should be regulated"}, config
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


def test_directed_conversation() -> Dict[str, Any]:
    """Test Directed conversation agent."""
    try:
        print("🔄 Testing Directed Conversation Agent...")

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.directed.agent import DirectedConversation

        timestamp = datetime.now().strftime("%H%M%S")

        participants = {
            f"Lead_{timestamp}": AugLLMConfig(
                name=f"Lead_{timestamp}",
                system_message="You are the discussion leader. Guide the conversation.",
            ),
            f"Member_{timestamp}": AugLLMConfig(
                name=f"Member_{timestamp}",
                system_message="You are a team member. Respond to the leader's guidance.",
            ),
        }

        agent = DirectedConversation(
            name=f"TestDirected_{timestamp}",
            participant_agents=participants,
            topic="Planning a project sprint",
            max_rounds=1,
            persistence=True,
        )

        agent.compile()

        thread_id = f"directed_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {"messages": [], "topic": "Planning a project sprint"}, config
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


def test_round_robin_conversation() -> Dict[str, Any]:
    """Test Round Robin conversation agent."""
    try:
        print("🔄 Testing Round Robin Conversation Agent...")

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.round_robin.agent import RoundRobinConversation

        timestamp = datetime.now().strftime("%H%M%S")

        participants = {
            f"A_{timestamp}": AugLLMConfig(
                name=f"A_{timestamp}",
                system_message="You are participant A. Give brief responses.",
            ),
            f"B_{timestamp}": AugLLMConfig(
                name=f"B_{timestamp}",
                system_message="You are participant B. Give brief responses.",
            ),
        }

        agent = RoundRobinConversation(
            name=f"TestRoundRobin_{timestamp}",
            participant_agents=participants,
            topic="Round robin discussion test",
            max_rounds=1,
            persistence=True,
        )

        agent.compile()

        thread_id = f"roundrobin_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {"messages": [], "topic": "Round robin discussion test"}, config
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


def test_social_media_conversation() -> Dict[str, Any]:
    """Test Social Media conversation agent."""
    try:
        print("🔄 Testing Social Media Conversation Agent...")

        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.social_media.agent import SocialMediaConversation

        timestamp = datetime.now().strftime("%H%M%S")

        participants = {
            f"User_{timestamp}": AugLLMConfig(
                name=f"User_{timestamp}",
                system_message="You are a social media user. Give brief, casual responses.",
            ),
            f"Influencer_{timestamp}": AugLLMConfig(
                name=f"Influencer_{timestamp}",
                system_message="You are a social media influencer. Give engaging responses.",
            ),
        }

        agent = SocialMediaConversation(
            name=f"TestSocialMedia_{timestamp}",
            participant_agents=participants,
            topic="Social media conversation test",
            max_rounds=1,
            persistence=True,
        )

        agent.compile()

        thread_id = f"socialmedia_test_{timestamp}"
        config = {"configurable": {"thread_id": thread_id}}

        result = agent.invoke(
            {"messages": [], "topic": "Social media conversation test"}, config
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
    """Run tests on RAG and all conversation agents."""
    print("🧪 Testing RAG and All Conversation Agents with PostgreSQL Persistence")
    print("=" * 75)

    setup_paths()

    # Run all tests
    test_results = {}

    # RAG Agents
    test_results["rag_base"] = test_rag_base_agent()
    test_results["rag_simple"] = test_rag_simple_agent()

    # Conversation Agents
    test_results["collaborative"] = test_collaborative_conversation()
    test_results["debate"] = test_debate_conversation()
    test_results["directed"] = test_directed_conversation()
    test_results["round_robin"] = test_round_robin_conversation()
    test_results["social_media"] = test_social_media_conversation()

    # Generate summary report
    print("\n" + "=" * 75)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 75)

    passed_count = 0
    failed_count = 0

    print("\n🔍 RAG AGENTS:")
    for agent_type in ["rag_base", "rag_simple"]:
        if agent_type in test_results:
            result = test_results[agent_type]
            status = result["status"]
            print(f"   {agent_type.replace('_', ' ').title()}: {status}")
            if "✅ PASSED" in status:
                passed_count += 1
                print(f"      App Name: {result.get('app_name', 'N/A')}")
            else:
                failed_count += 1
                print(f"      Error: {result.get('error', 'Unknown')}")

    print("\n💬 CONVERSATION AGENTS:")
    for agent_type in [
        "collaborative",
        "debate",
        "directed",
        "round_robin",
        "social_media",
    ]:
        if agent_type in test_results:
            result = test_results[agent_type]
            status = result["status"]
            print(f"   {agent_type.title()}: {status}")
            if "✅ PASSED" in status:
                passed_count += 1
                print(f"      App Name: {result.get('app_name', 'N/A')}")
                if "has_prepared_statement_errors" in result:
                    ps_status = (
                        "❌ YES" if result["has_prepared_statement_errors"] else "✅ NO"
                    )
                    print(f"      Prepared Statement Errors: {ps_status}")
            else:
                failed_count += 1
                print(f"      Error: {result.get('error', 'Unknown')}")

    # Overall status
    print(f"\n🎯 OVERALL RESULTS:")
    print(f"   ✅ Passed: {passed_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📊 Total: {len(test_results)}")

    if failed_count == 0:
        print(
            f"\n🎉 ALL TESTS PASSED! All RAG and conversation agents working with PostgreSQL persistence."
        )
    else:
        print(f"\n⚠️  Some tests failed. Check the errors above for details.")

    # Save detailed results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"/home/will/Projects/haive/backend/haive/rag_conversation_test_results_{timestamp}.json"

    with open(results_file, "w") as f:
        json.dump(test_results, f, indent=2)

    print(f"\n📁 Detailed results saved: {results_file}")


if __name__ == "__main__":
    main()
