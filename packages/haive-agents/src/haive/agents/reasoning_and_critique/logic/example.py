# src/haive/agents/reasoning/examples.py

from haive.agents.reasoning_and_critique.logic.agent import ReasoningSystem
from haive.agents.reasoning_and_critique.logic.models import (
    ArgumentStrength,
    Evidence,
    EvidenceType,
)


def example_business_decision():
    """Example: Reasoning about a business decision."""
    # Create the reasoning system
    reasoner = ReasoningSystem()

    # Prepare the input
    input_data = {
        "question": "Should we acquire StartupX for $50M?",
        "context": {
            "our_company": {
                "revenue": "$500M",
                "cash_reserves": "$200M",
                "growth_rate": "15% YoY",
                "market_position": "3rd in market",
            },
            "startup_x": {
                "revenue": "$10M",
                "growth_rate": "100% YoY",
                "unique_technology": "AI-powered analytics",
                "team_size": 50,
                "burn_rate": "$2M/month",
            },
        },
        "evidence": [
            Evidence(
                evidence_type=EvidenceType.STATISTICAL,
                description="90% of acquisitions in our industry fail to deliver expected value",
                source="Industry Report 2023",
                strength=ArgumentStrength.STRONG,
                reliability=0.9,
                relevance=0.8,
            ),
            Evidence(
                evidence_type=EvidenceType.EMPIRICAL,
                description="Our last 2 acquisitions successfully integrated and added 30% revenue",
                source="Internal data",
                strength=ArgumentStrength.MODERATE,
                reliability=1.0,
                relevance=0.7,
            ),
        ],
        "constraints": [
            "Must maintain 6 months cash runway",
            "Cannot take on debt for acquisition",
        ],
        "reasoning_depth": 4,
        "explore_alternatives": True,
    }

    # Run the reasoning system
    result = reasoner.invoke(input_data)

    # The result contains the final synthesized report
    report = result.get("final_report") or result.get("synthesized_conclusion")

    print("REASONING REPORT: Acquisition Decision")
    print("=" * 50)

    if report:
        print(f"\nExecutive Summary:\n{report.executive_summary}")
        print(f"\nConfidence Level: {report.confidence_level}")
        print(f"\nRecommendation: {report.decision_recommendation}")

        print("\nKey Insights:")
        for insight in report.key_insights[:5]:
            print(f"- {insight}")

    return result


def example_quick_reasoning():
    """Example: Quick reasoning with minimal setup."""
    reasoner = ReasoningSystem()

    result = reasoner.invoke(
        {
            "question": "Should I take the job offer with 20% higher salary but longer commute?",
            "context": {
                "current_job": {
                    "salary": "$100k",
                    "commute": "15 min",
                    "satisfaction": "high",
                },
                "new_offer": {
                    "salary": "$120k",
                    "commute": "1 hour",
                    "role": "similar",
                },
            },
            "constraints": ["Need work-life balance", "Have young kids"],
        }
    )

    print("\nQUICK DECISION:")
    print(result.get("synthesized_conclusion", "No conclusion reached"))

    return result


# Run examples
if __name__ == "__main__":
    print("Running Reasoning System Examples...")
    print("=" * 60)

    # Run business example
    business_result = example_business_decision()

    print("\n" + "=" * 60 + "\n")

    # Run quick example
    quick_result = example_quick_reasoning()
