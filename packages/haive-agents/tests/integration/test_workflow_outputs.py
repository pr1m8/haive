#!/usr/bin/env python3
"""Test workflow outputs by examining agent structure."""


from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


def pretty_print_agent_info(agent, name):
    """Pretty print agent information."""
    for _i, sub_agent in enumerate(agent.agents, 1):
        if hasattr(sub_agent, "output_schema") and sub_agent.output_schema:
            for _key, _value in sub_agent.output_schema.items():
                pass


def test_flare():
    """Test FLARE workflow structure."""
    agent = FLAREAgent(name="flare_test")
    pretty_print_agent_info(agent, "FLARE (Forward-Looking Active REtrieval)")

    # Show FLARE workflow

    # Show state fields
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, _value in state_dict.items():
        if field.startswith("_"):
            continue


def test_dynamic_rag():
    """Test Dynamic RAG workflow structure."""
    agent = DynamicRAGAgent(name="dynamic_test")
    pretty_print_agent_info(agent, "Dynamic RAG (Add/Remove Retrievers)")

    # Show state fields
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, _value in state_dict.items():
        if field.startswith("_"):
            continue


def test_debate_rag():
    """Test Debate RAG workflow structure."""
    positions = ["Optimist", "Pessimist", "Realist"]
    agent = DebateRAGAgent(name="debate_test", debate_positions=positions)
    pretty_print_agent_info(agent, "Debate RAG (Multi-Perspective Reasoning)")

    # Show state fields
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, _value in state_dict.items():
        if field.startswith("_"):
            continue


def test_adaptive_threshold():
    """Test Adaptive Threshold workflow structure."""
    agent = AdaptiveThresholdRAGAgent(name="adaptive_test")
    pretty_print_agent_info(agent, "Adaptive Threshold RAG")

    # Show state fields (uses DynamicRAGState)
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, _value in state_dict.items():
        if field.startswith("_"):
            continue


def main():

    test_flare()
    test_dynamic_rag()
    test_debate_rag()
    test_adaptive_threshold()


if __name__ == "__main__":
    main()
