#!/usr/bin/env python3
"""Basic test for LTM Agent Phase 1 implementation.

This tests the basic structure and memory extraction flow.
Run with: poetry run pytest packages/haive-agents/tests/ltm/test_basic.py -v
"""

import logging

import pytest
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.ltm.agent import LTMAgent, LTMState

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_ltm_basic_structure():
    """Test basic LTM agent structure."""
    # Create agent
    agent = LTMAgent(name="Test LTM Agent")

    # Verify initialization
    assert agent.name == "Test LTM Agent"
    assert agent.enable_kg_processing
    assert agent.enable_categorization
    assert agent.enable_consolidation


def test_ltm_state_schema():
    """Test LTM state schema."""
    # Create state
    state = LTMState(
        messages=[
            HumanMessage(content="Hello, I like pizza"),
            AIMessage(content="That's interesting! I'll remember that."),
        ]
    )

    # Verify state
    assert len(state.messages) == 2
    assert state.processing_stage == "extract"
    assert not state.processing_complete
    assert len(state.extracted_memories) == 0
    assert state.extraction_quality == 0.0


def test_condition_functions():
    """Test condition functions."""
    from haive.agents.ltm.agent import (
        extraction_succeeded,
        has_processing_errors,
        needs_kg_processing,
        processing_complete,
    )

    # Test with empty state
    empty_state = LTMState()
    assert not extraction_succeeded(empty_state)
    assert not has_processing_errors(empty_state)
    assert not needs_kg_processing(empty_state)
    assert not processing_complete(empty_state)

    # Test with memories
    state_with_memories = LTMState(extracted_memories=[{"id": "1"}, {"id": "2"}])
    assert extraction_succeeded(state_with_memories)
    assert needs_kg_processing(state_with_memories)

    # Test with errors
    state_with_errors = LTMState(processing_errors=["Some error"])
    assert has_processing_errors(state_with_errors)


def test_ltm_graph_building():
    """Test LTM graph building."""
    # Create agent
    agent = LTMAgent()

    # Setup agent
    agent.setup_agent()

    # Build graph
    graph = agent.build_graph()

    # Verify graph structure
    assert graph is not None
    assert "extract_memories" in graph.nodes
    assert "complete_processing" in graph.nodes
    assert "handle_errors" in graph.nodes


def test_memory_extraction_node():
    """Test memory extraction node."""
    # Create agent and setup
    agent = LTMAgent()
    agent.setup_agent()

    # Create test state
    state = LTMState(
        messages=[
            HumanMessage(content="I love reading science fiction books"),
            AIMessage(content="Science fiction is fascinating!"),
            HumanMessage(content="My favorite author is Isaac Asimov"),
        ]
    )

    # Test extraction node
    result = agent.extract_memories_node(state)

    # Verify results
    assert "extracted_memories" in result
    assert len(result["extracted_memories"]) > 0
    assert "extraction_quality" in result
    assert result["extraction_quality"] > 0


def test_error_handling():
    """Test error handling."""
    # Create agent
    agent = LTMAgent()
    agent.setup_agent()

    # Test with empty messages
    empty_state = LTMState(messages=[])
    result = agent.extract_memories_node(empty_state)

    # Verify error handling
    assert "processing_errors" in result
    assert len(result["processing_errors"]) > 0
    assert result["processing_stage"] == "error"


def test_quality_calculation():
    """Test quality calculation logic."""
    agent = LTMAgent()

    # Test quality calculation with different scenarios
    messages = [HumanMessage(content=f"Message {i}") for i in range(5)]

    # Scenario 1: Good ratio
    memories_good = [
        {"memory_id": f"mem_{i}", "schema": "Memory", "confidence": 0.9}
        for i in range(2)
    ]
    quality_good = agent._calculate_extraction_quality(memories_good, messages)

    # Scenario 2: Poor ratio
    memories_poor = [{"memory_id": "mem_1", "schema": "Memory", "confidence": 0.5}]
    quality_poor = agent._calculate_extraction_quality(memories_poor, messages)

    # Scenario 3: Diverse schemas
    memories_diverse = [
        {"memory_id": "mem_1", "schema": "Memory", "confidence": 0.8},
        {"memory_id": "mem_2", "schema": "UserPreference", "confidence": 0.8},
        {"memory_id": "mem_3", "schema": "FactualMemory", "confidence": 0.8},
    ]
    quality_diverse = agent._calculate_extraction_quality(memories_diverse, messages)

    # Verify quality logic
    assert quality_diverse >= quality_good, "Diverse schemas should have higher quality"
    assert (
        quality_good >= quality_poor
    ), "Good ratio should have higher quality than poor ratio"
