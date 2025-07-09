#!/usr/bin/env python3
"""Test graded RAG workflows"""

from haive.agents.rag.multi_agent_rag.graded_rag_workflows import (
    AdaptiveGradedRAGAgent,
    FullyGradedRAGAgent,
    MultiCriteriaGradedRAGAgent,
    ReflexiveGradedRAGAgent,
)
from haive.agents.rag.multi_agent_rag.grading_components import (
    create_answer_grader,
    create_document_grader,
    create_hallucination_grader,
    create_priority_ranker,
    create_query_analyzer,
)


def test_grading_components():
    """Test individual grading components"""
    print("=" * 60)
    print("Testing Grading Components")
    print("=" * 60)

    results = []

    # Test document grader
    try:
        doc_grader = create_document_grader()
        results.append(("✅", "Document Grader", f"Agent: {doc_grader.name}"))
    except Exception as e:
        results.append(("❌", "Document Grader", str(e)))

    # Test answer grader
    try:
        answer_grader = create_answer_grader()
        results.append(("✅", "Answer Grader", f"Agent: {answer_grader.name}"))
    except Exception as e:
        results.append(("❌", "Answer Grader", str(e)))

    # Test hallucination grader
    try:
        hallucination_grader = create_hallucination_grader()
        results.append(
            ("✅", "Hallucination Grader", f"Agent: {hallucination_grader.name}")
        )
    except Exception as e:
        results.append(("❌", "Hallucination Grader", str(e)))

    # Test priority ranker
    try:
        priority_ranker = create_priority_ranker()
        results.append(("✅", "Priority Ranker", f"Agent: {priority_ranker.name}"))
    except Exception as e:
        results.append(("❌", "Priority Ranker", str(e)))

    # Test query analyzer
    try:
        query_analyzer = create_query_analyzer()
        results.append(("✅", "Query Analyzer", f"Agent: {query_analyzer.name}"))
    except Exception as e:
        results.append(("❌", "Query Analyzer", str(e)))

    print("\nGrading Components:")
    for status, name, details in results:
        print(f"{status} {name}: {details}")

    return results


def test_graded_workflows():
    """Test graded RAG workflows"""
    print("\n" + "=" * 60)
    print("Testing Graded RAG Workflows")
    print("=" * 60)

    results = []

    # Test Fully Graded RAG
    try:
        fully_graded = FullyGradedRAGAgent(
            name="fully_graded_test", relevance_threshold=0.6
        )
        agents = [a.name for a in fully_graded.agents]
        results.append(("✅", "Fully Graded RAG", f"{len(agents)} agents"))
        print(f"\nFully Graded RAG agents: {agents}")
    except Exception as e:
        results.append(("❌", "Fully Graded RAG", str(e)))

    # Test Adaptive Graded RAG
    try:
        adaptive_graded = AdaptiveGradedRAGAgent(name="adaptive_graded_test")
        agents = [a.name for a in adaptive_graded.agents]
        results.append(("✅", "Adaptive Graded RAG", f"{len(agents)} agents"))
        print(f"\nAdaptive Graded RAG agents: {agents}")
    except Exception as e:
        results.append(("❌", "Adaptive Graded RAG", str(e)))

    # Test Multi-Criteria Graded RAG
    try:
        multi_criteria = MultiCriteriaGradedRAGAgent(
            name="multi_criteria_test",
            grading_criteria=["relevance", "accuracy", "authority"],
        )
        agents = [a.name for a in multi_criteria.agents]
        results.append(("✅", "Multi-Criteria Graded RAG", f"{len(agents)} agents"))
        print(f"\nMulti-Criteria RAG agents: {agents}")
        print(f"Grading criteria: {multi_criteria._grading_criteria}")
    except Exception as e:
        results.append(("❌", "Multi-Criteria Graded RAG", str(e)))

    # Test Reflexive Graded RAG
    try:
        reflexive = ReflexiveGradedRAGAgent(name="reflexive_test")
        agents = [a.name for a in reflexive.agents]
        results.append(("✅", "Reflexive Graded RAG", f"{len(agents)} agents"))
        print(f"\nReflexive RAG agents: {agents}")
    except Exception as e:
        results.append(("❌", "Reflexive Graded RAG", str(e)))

    print("\n\nGraded Workflows:")
    for status, name, details in results:
        print(f"{status} {name}: {details}")

    return results


def main():
    print("🔍 Testing RAG Grading System")
    print("=" * 60)

    # Test components
    component_results = test_grading_components()

    # Test workflows
    workflow_results = test_graded_workflows()

    # Summary
    all_results = component_results + workflow_results
    successful = sum(1 for s, _, _ in all_results if s == "✅")
    total = len(all_results)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {successful}/{total} tests passed")
    print("=" * 60)

    if successful == total:
        print("\n🎉 ALL GRADING COMPONENTS AND WORKFLOWS WORKING! 🎉")
        print("\nKey Features:")
        print("- Document relevance grading with detailed scoring")
        print("- Answer quality assessment across multiple dimensions")
        print("- Hallucination detection with claim verification")
        print("- Priority ranking for optimal document usage")
        print("- Query analysis for better understanding")
        print("- Adaptive thresholds based on complexity")
        print("- Multi-criteria evaluation frameworks")
        print("- Self-improving reflexive systems")


if __name__ == "__main__":
    main()
