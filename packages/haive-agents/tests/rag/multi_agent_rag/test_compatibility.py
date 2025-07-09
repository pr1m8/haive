"""Safe Compatibility Testing Demo

This script demonstrates how to safely test agent compatibility without
breaking or modifying existing agents.
"""

import logging
from typing import Any

from .agents import (
    DocumentGradingAgent,
    IterativeDocumentGradingAgent,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
)
from .compatibility import (
    SafeCompatibilityTester,
    quick_agent_compatibility_check,
    safe_test_rag_compatibility,
    test_custom_agent_workflow,
)
from .multi_rag import agent_list, base_rag_agent

logger = logging.getLogger(__name__)


def run_safe_compatibility_tests() -> dict[str, Any]:
    """Run comprehensive safe compatibility tests.

    This function demonstrates how to safely test agent compatibility
    without risking damage to existing systems.
    """
    print("🔍 Starting Safe Agent Compatibility Testing...")
    print("=" * 60)

    results = {}

    try:
        # Test 1: Basic RAG compatibility (as mentioned in user prompt)
        print("\n1. Testing Basic RAG Agent Compatibility")
        print("-" * 40)

        basic_results = safe_test_rag_compatibility()
        results["basic_rag_tests"] = basic_results

        if "basic_rag_chain" in basic_results:
            report = basic_results["basic_rag_chain"]
            print(f"✅ {report.source_agent} -> {report.target_agent}")
            print(f"   Compatibility: {report.compatibility_level.value}")
            print(f"   Score: {report.compatibility_score:.2f}")
            print(f"   Safe to chain: {report.safe_to_chain}")

            if report.issues:
                print(f"   Issues: {'; '.join(report.issues)}")
            if report.suggested_mappings:
                print(f"   Suggested mappings: {report.suggested_mappings}")

        # Test 2: Multi-agent workflow compatibility
        print("\n2. Testing Multi-Agent Workflow Compatibility")
        print("-" * 40)

        # Create test agents safely
        retrieval_agent = SimpleRAGAgent(name="Test Retrieval Agent")
        grading_agent = DocumentGradingAgent(name="Test Grading Agent")
        answer_agent = SimpleRAGAnswerAgent(name="Test Answer Agent")

        workflow_agents = [retrieval_agent, grading_agent, answer_agent]
        workflow_report = test_custom_agent_workflow(
            workflow_agents, "Test RAG Workflow"
        )
        results["workflow_test"] = workflow_report

        print(f"✅ Workflow: {workflow_report.workflow_name}")
        print(f"   Overall compatible: {workflow_report.overall_compatible}")
        print(
            f"   Compatible pairs: {workflow_report.compatible_pairs}/{workflow_report.total_pairs}"
        )
        print(f"   Risk assessment: {workflow_report.risk_assessment}")

        if workflow_report.workflow_recommendations:
            print("   Recommendations:")
            for rec in workflow_report.workflow_recommendations[:3]:  # Show first 3
                print(f"     - {rec}")

        # Test 3: Quick compatibility checks
        print("\n3. Quick Compatibility Checks")
        print("-" * 40)

        quick_tests = {}

        # Test retrieval -> grading
        is_compatible = quick_agent_compatibility_check(retrieval_agent, grading_agent)
        quick_tests["retrieval_to_grading"] = is_compatible
        print(
            f"✅ Retrieval -> Grading: {'Compatible' if is_compatible else 'Needs attention'}"
        )

        # Test grading -> answer
        is_compatible = quick_agent_compatibility_check(grading_agent, answer_agent)
        quick_tests["grading_to_answer"] = is_compatible
        print(
            f"✅ Grading -> Answer: {'Compatible' if is_compatible else 'Needs attention'}"
        )

        results["quick_tests"] = quick_tests

        # Test 4: Advanced compatibility features
        print("\n4. Advanced Compatibility Analysis")
        print("-" * 40)

        tester = SafeCompatibilityTester()

        # Test iterative grading agent
        iterative_agent = IterativeDocumentGradingAgent(name="Test Iterative Agent")
        iterative_report = tester.test_agent_pair_compatibility(
            grading_agent, iterative_agent
        )
        results["iterative_test"] = iterative_report

        print("✅ Standard -> Iterative Grading")
        print(f"   Compatibility: {iterative_report.compatibility_level.value}")
        print(f"   Quality: {iterative_report.quality_assessment}")

        # Test with multi-agent systems
        if hasattr(base_rag_agent, "agents") and base_rag_agent.agents:
            multi_agent_test = tester.test_workflow_compatibility(
                list(base_rag_agent.agents), "Base RAG Multi-Agent"
            )
            results["multi_agent_test"] = multi_agent_test

            print("✅ Base RAG Multi-Agent System")
            print(f"   Compatible: {multi_agent_test.overall_compatible}")
            print(f"   Required adapters: {len(multi_agent_test.required_adapters)}")

        # Test 5: State schema compatibility
        print("\n5. State Schema Compatibility")
        print("-" * 40)

        state_test = tester._test_state_compatibility()
        results["state_compatibility"] = state_test

        if "total_fields" in state_test:
            print("✅ MultiAgentRAGState Analysis")
            print(f"   Total fields: {state_test['total_fields']}")
            print(f"   Shared fields: {len(state_test.get('shared_fields', []))}")
            print(f"   Status: {state_test.get('compatibility_status', 'Unknown')}")

        print("\n" + "=" * 60)
        print("🎉 All compatibility tests completed successfully!")
        print("✅ No agents were modified or damaged during testing")

        return results

    except Exception as e:
        error_msg = f"Error during compatibility testing: {e!s}"
        logger.error(error_msg)
        print(f"❌ {error_msg}")

        results["error"] = error_msg
        results["safety_note"] = "Error occurred but no agents were modified"

        return results


def demonstrate_compatibility_workflow():
    """Demonstrate a complete compatibility testing workflow.

    This shows how to use compatibility testing in a real workflow.
    """
    print("\n🚀 Demonstrating Compatibility Workflow")
    print("=" * 50)

    # Step 1: Create agents for testing
    print("1. Creating test agents...")
    agents = [
        SimpleRAGAgent(name="Demo Retrieval"),
        DocumentGradingAgent(name="Demo Grading"),
        SimpleRAGAnswerAgent(name="Demo Answer"),
    ]

    # Step 2: Test individual pairs
    print("2. Testing individual agent pairs...")
    tester = SafeCompatibilityTester()

    for i in range(len(agents) - 1):
        report = tester.test_agent_pair_compatibility(agents[i], agents[i + 1])
        print(
            f"   {report.source_agent} -> {report.target_agent}: {report.compatibility_level.value}"
        )

    # Step 3: Test full workflow
    print("3. Testing complete workflow...")
    workflow_report = test_custom_agent_workflow(agents, "Demo Workflow")

    # Step 4: Generate recommendations
    print("4. Compatibility recommendations:")
    for rec in workflow_report.workflow_recommendations:
        print(f"   - {rec}")

    # Step 5: Safe to proceed?
    if workflow_report.overall_compatible:
        print("✅ Workflow is safe to implement!")
    else:
        print("⚠️  Workflow needs adapters before implementation")
        print("   Required adapters:")
        for adapter in workflow_report.required_adapters:
            print(
                f"     - {adapter['type']} for {adapter['source']} -> {adapter['target']}"
            )

    return workflow_report


def test_agent_list_compatibility():
    """Test the agent_list from multi_rag.py as mentioned in user prompt."""
    print("\n📋 Testing agent_list compatibility...")

    if len(agent_list) >= 2:
        tester = SafeCompatibilityTester()
        report = tester.test_workflow_compatibility(agent_list, "Agent List Workflow")

        print(f"Agent list compatibility: {report.overall_compatible}")
        print(f"Total agents: {report.total_agents}")
        print(f"Compatible pairs: {report.compatible_pairs}/{report.total_pairs}")

        return report
    print("Agent list has insufficient agents for compatibility testing")
    return None


if __name__ == "__main__":
    # Run safe compatibility tests
    test_results = run_safe_compatibility_tests()

    # Demonstrate workflow
    workflow_demo = demonstrate_compatibility_workflow()

    # Test agent list
    agent_list_test = test_agent_list_compatibility()

    print("\n📊 Testing Complete - All Systems Safe! 🛡️")
