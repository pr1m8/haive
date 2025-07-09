#!/usr/bin/env python3
"""Test workflow outputs by examining agent structure"""


from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


def pretty_print_agent_info(agent, name):
    """Pretty print agent information"""
    print(f"\n{'='*60}")
    print(f"{name} - Agent Structure")
    print(f"{'='*60}")

    print(f"\nAgent Name: {agent.name}")
    print(f"Execution Mode: {agent.execution_mode}")
    print(f"State Schema: {agent.state_schema.__name__}")

    print(f"\nSub-Agents ({len(agent.agents)}):")
    for i, sub_agent in enumerate(agent.agents, 1):
        print(f"\n{i}. {sub_agent.name}")
        print(f"   Instructions: {sub_agent.instructions[:100]}...")
        if hasattr(sub_agent, "output_schema") and sub_agent.output_schema:
            print("   Output Schema:")
            for key, value in sub_agent.output_schema.items():
                print(f"     - {key}: {value}")


def test_flare():
    """Test FLARE workflow structure"""
    agent = FLAREAgent(name="flare_test")
    pretty_print_agent_info(agent, "FLARE (Forward-Looking Active REtrieval)")

    # Show FLARE workflow
    print("\n📋 FLARE Workflow:")
    print("1. Monitor generation for uncertainty indicators")
    print("2. When uncertainty detected, perform targeted retrieval")
    print("3. Continue generation with retrieved information")
    print("4. Synthesize all segments into final response")

    # Show state fields
    print("\n📊 FLARE State Fields:")
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, value in state_dict.items():
        if field.startswith("_"):
            continue
        print(f"  - {field}: {type(value).__name__} = {repr(value)[:50]}")


def test_dynamic_rag():
    """Test Dynamic RAG workflow structure"""
    agent = DynamicRAGAgent(name="dynamic_test")
    pretty_print_agent_info(agent, "Dynamic RAG (Add/Remove Retrievers)")

    print("\n📋 Dynamic RAG Workflow:")
    print("1. Analyze query to determine optimal retrievers")
    print("2. Activate/deactivate retrievers based on performance")
    print("3. Coordinate parallel retrieval from multiple sources")
    print("4. Synthesize results with performance weighting")

    # Show state fields
    print("\n📊 Dynamic RAG State Fields:")
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, value in state_dict.items():
        if field.startswith("_"):
            continue
        print(f"  - {field}: {type(value).__name__} = {repr(value)[:50]}")


def test_debate_rag():
    """Test Debate RAG workflow structure"""
    positions = ["Optimist", "Pessimist", "Realist"]
    agent = DebateRAGAgent(name="debate_test", debate_positions=positions)
    pretty_print_agent_info(agent, "Debate RAG (Multi-Perspective Reasoning)")

    print("\n📋 Debate RAG Workflow:")
    print("1. Each position agent argues their perspective")
    print("2. Moderator ensures balanced discussion")
    print("3. Evidence arbiter evaluates argument quality")
    print("4. Synthesis judge combines perspectives into final answer")

    print(f"\n🎭 Debate Positions: {positions}")

    # Show state fields
    print("\n📊 Debate RAG State Fields:")
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, value in state_dict.items():
        if field.startswith("_"):
            continue
        print(f"  - {field}: {type(value).__name__} = {repr(value)[:50]}")


def test_adaptive_threshold():
    """Test Adaptive Threshold workflow structure"""
    agent = AdaptiveThresholdRAGAgent(name="adaptive_test")
    pretty_print_agent_info(agent, "Adaptive Threshold RAG")

    print("\n📋 Adaptive Threshold Workflow:")
    print("1. Analyze query complexity to set initial threshold")
    print("2. Retrieve with dynamic threshold adjustment")
    print("3. Assess confidence and adjust if needed")
    print("4. Generate answer with threshold awareness")

    # Show state fields (uses DynamicRAGState)
    print("\n📊 Adaptive Threshold State Fields:")
    state = agent.state_schema()
    state_dict = state.model_dump()
    for field, value in state_dict.items():
        if field.startswith("_"):
            continue
        print(f"  - {field}: {type(value).__name__} = {repr(value)[:50]}")


def main():
    print("🚀 Specialized RAG Workflows - Structure Analysis")
    print("=" * 60)

    test_flare()
    test_dynamic_rag()
    test_debate_rag()
    test_adaptive_threshold()

    print("\n" + "=" * 60)
    print("✅ All workflows successfully created and analyzed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
