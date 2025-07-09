#!/usr/bin/env python3
"""Test enhanced state schemas and V2 workflows"""

from haive.agents.rag.multi_agent_rag.enhanced_state_schemas import (
    ConfigurableRAGState,
    FLAREState,
    GradedRAGState,
    create_configured_state,
)
from haive.agents.rag.multi_agent_rag.graded_rag_workflows_v2 import (
    FullyGradedRAGAgentV2,
    MultiCriteriaGradedRAGAgentV2,
    create_graded_rag_agent,
)
from haive.agents.rag.multi_agent_rag.specialized_workflows_v2 import (
    AdaptiveThresholdRAGAgentV2,
    DebateRAGAgentV2,
    DynamicRAGAgentV2,
    FLAREAgentV2,
)


def test_enhanced_states():
    """Test enhanced state schemas"""
    print("=" * 60)
    print("Testing Enhanced State Schemas")
    print("=" * 60)

    # Test ConfigurableRAGState
    print("\n1. ConfigurableRAGState:")
    state = ConfigurableRAGState(
        agent_name="test_agent",
        workflow_type="test_workflow",
        relevance_threshold=0.7,
        max_documents=5,
    )
    print(f"   Agent: {state.agent_name}")
    print(f"   Workflow: {state.workflow_type}")
    print(f"   Relevance threshold: {state.relevance_threshold}")
    print(f"   Max documents: {state.max_documents}")
    print(f"   Config: {state.config}")

    # Test GradedRAGState
    print("\n2. GradedRAGState:")
    graded_state = GradedRAGState(
        grading_criteria=["relevance", "accuracy", "completeness"],
        grading_weights={"relevance": 0.5, "accuracy": 0.3, "completeness": 0.2},
    )
    print(f"   Grading criteria: {graded_state.grading_criteria}")
    print(f"   Grading weights: {graded_state.grading_weights}")

    # Test create_configured_state
    print("\n3. create_configured_state helper:")
    flare_state = create_configured_state(
        FLAREState,
        agent_name="flare_agent",
        workflow_type="flare",
        uncertainty_threshold=0.4,
        max_retrieval_rounds=5,
        custom_param="test_value",  # Goes into config
    )
    print(f"   Uncertainty threshold: {flare_state.uncertainty_threshold}")
    print(f"   Max retrieval rounds: {flare_state.max_retrieval_rounds}")
    print(f"   Custom config: {flare_state.config}")


def test_v2_workflows():
    """Test V2 workflows with enhanced states"""
    print("\n" + "=" * 60)
    print("Testing V2 Workflows")
    print("=" * 60)

    results = []

    # Test Fully Graded RAG V2
    try:
        agent = FullyGradedRAGAgentV2(name="graded_v2", relevance_threshold=0.8)
        print("\n✓ FullyGradedRAGAgentV2 created"d")
        print(f"  State schema: {agent.state_schema.__name__}")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "FullyGradedRAGAgentV2"))
    except Exception as e:
        results.append(("❌", "FullyGradedRAGAgentV2", str(e)))

    # Test Multi-Criteria V2
    try:
        agent = MultiCriteriaGradedRAGAgentV2(
            name="multi_criteria_v2",
            grading_criteria=["relevance", "authority", "recency"],
        )
        print("\n✓ MultiCriteriaGradedRAGAgentV2 created"d")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "MultiCriteriaGradedRAGAgentV2"))
    except Exception as e:
        results.append(("❌", "MultiCriteriaGradedRAGAgentV2", str(e)))

    # Test FLARE V2
    try:
        agent = FLAREAgentV2(
            name="flare_v2", uncertainty_threshold=0.25, max_retrieval_rounds=4
        )
        print("\n✓ FLAREAgentV2 created"d")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "FLAREAgentV2"))
    except Exception as e:
        results.append(("❌", "FLAREAgentV2", str(e)))

    # Test Dynamic RAG V2
    try:
        agent = DynamicRAGAgentV2(
            name="dynamic_v2",
            min_retrievers=2,
            max_retrievers=6,
            performance_threshold=0.65,
        )
        print("\n✓ DynamicRAGAgentV2 created"d")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "DynamicRAGAgentV2"))
    except Exception as e:
        results.append(("❌", "DynamicRAGAgentV2", str(e)))

    # Test Debate RAG V2
    try:
        agent = DebateRAGAgentV2(
            name="debate_v2",
            position_names=["Pro", "Con"],
            max_debate_rounds=2,
            enable_judge=True,
        )
        print("\n✓ DebateRAGAgentV2 created"d")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "DebateRAGAgentV2"))
    except Exception as e:
        results.append(("❌", "DebateRAGAgentV2", str(e)))

    # Test Adaptive Threshold V2
    try:
        agent = AdaptiveThresholdRAGAgentV2(
            name="adaptive_v2", initial_threshold=0.6, threshold_step=0.05
        )
        print("\n✓ AdaptiveThresholdRAGAgentV2 created"d")
        print(f"  Initial config: {agent._initial_config}")
        results.append(("✅", "AdaptiveThresholdRAGAgentV2"))
    except Exception as e:
        results.append(("❌", "AdaptiveThresholdRAGAgentV2", str(e)))

    return results


def test_state_configuration_flow():
    """Test how configuration flows through the system"""
    print("\n" + "=" * 60)
    print("Testing Configuration Flow")
    print("=" * 60)

    # Create agent with configuration
    agent = create_graded_rag_agent(
        workflow_type="fully_graded", relevance_threshold=0.75, name="config_test"
    )

    print("\n1. Agent created with config:")
    print(f"   Initial config: {agent._initial_config}")

    # Simulate invocation with state
    print("\n2. Simulating invocation:")
    print("   - Configuration will be injected into state")
    print("   - State will have relevance_threshold = 0.75")
    print("   - Agents can access via state.relevance_threshold")

    # Show override capability
    print("\n3. Configuration override:")
    print("   - Can override per invocation:")
    print("     agent.invoke({'query': '...', 'relevance_threshold': 0.9})")
    print("   - State will use 0.9 instead of 0.75 for this run")


def main():
    print("🚀 Enhanced State Schemas and V2 Workflows Test")
    print("=" * 60)

    # Test state schemas
    test_enhanced_states()

    # Test V2 workflows
    results = test_v2_workflows()

    # Test configuration flow
    test_state_configuration_flow()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    successful = sum(1 for r in results if r[0] == "✅")
    total = len(results)

    print(f"\nWorkflow Tests: {successful}/{total} passed")

    if successful == total:
        print("\n✅ All V2 workflows successfully created!")
        print("\nKey Improvements:")
        print("- Configuration stored in state schemas, not agent attributes")
        print("- Clean separation of concerns")
        print("- Configuration can be overridden per invocation")
        print("- State schemas are self-documenting with Field descriptions")
        print("- Follows Pydantic best practices")


if __name__ == "__main__":
    main()
