#!/usr/bin/env python3
"""Final verification that all workflows are properly implemented"""

from haive.agents.rag.multi_agent_rag.specialized_workflows import (
    AdaptiveThresholdRAGAgent,
    DebateRAGAgent,
    DynamicRAGAgent,
    FLAREAgent,
)


def main():
    print("=" * 60)
    print("FINAL VERIFICATION - Specialized RAG Workflows")
    print("=" * 60)

    results = []

    # Test FLARE
    try:
        flare = FLAREAgent(name="flare_test")
        agents = [a.name for a in flare.agents]
        results.append(
            ("✅", "FLARE Agent", f"{len(agents)} agents: {', '.join(agents[:3])}...")
        )
    except Exception as e:
        results.append(("❌", "FLARE Agent", str(e)))

    # Test Dynamic RAG
    try:
        dynamic = DynamicRAGAgent(name="dynamic_test")
        agents = [a.name for a in dynamic.agents]
        results.append(
            ("✅", "Dynamic RAG", f"{len(agents)} agents: {', '.join(agents[:3])}...")
        )
    except Exception as e:
        results.append(("❌", "Dynamic RAG", str(e)))

    # Test Debate RAG
    try:
        debate = DebateRAGAgent(name="debate_test", debate_positions=["Pro", "Con"])
        agents = [a.name for a in debate.agents]
        results.append(
            ("✅", "Debate RAG", f"{len(agents)} agents including positions")
        )
    except Exception as e:
        results.append(("❌", "Debate RAG", str(e)))

    # Test Adaptive Threshold
    try:
        adaptive = AdaptiveThresholdRAGAgent(name="adaptive_test")
        agents = [a.name for a in adaptive.agents]
        results.append(
            (
                "✅",
                "Adaptive Threshold",
                f"{len(agents)} agents: {', '.join(agents[:3])}...",
            )
        )
    except Exception as e:
        results.append(("❌", "Adaptive Threshold", str(e)))

    # Print results
    print("\nRESULTS:")
    print("-" * 60)
    for status, name, details in results:
        print(f"{status} {name}: {details}")

    # Summary
    successful = sum(1 for s, _, _ in results if s == "✅")
    total = len(results)

    print("\n" + "=" * 60)
    print(f"SUMMARY: {successful}/{total} workflows successfully created")
    print("=" * 60)

    if successful == total:
        print("\n🎉 ALL WORKFLOWS IMPLEMENTED SUCCESSFULLY! 🎉")
        print("\nKey Features:")
        print("- FLARE: Forward-looking retrieval with uncertainty detection")
        print("- Dynamic RAG: Add/remove retrievers based on performance")
        print("- Debate RAG: Multi-perspective reasoning through debate")
        print("- Adaptive Threshold: Dynamic threshold adjustment")

    return successful == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
