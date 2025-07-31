"""Example core module.

This module provides example functionality for the Haive framework.

Functions:
    example_business_decision: Example Business Decision functionality.
    example_quick_reasoning: Example Quick Reasoning functionality.
"""

# src/haive/agents/reasoning/examples.py

from typing import Any

from haive.agents.reasoning_and_critique.logic.agent import ReasoningSystem
from haive.agents.reasoning_and_critique.logic.models import (
    ArgumentStrength,
    Evidence,
    EvidenceType,
)


def example_business_decision() -> Any:
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

    if report:
        for _insight in report.key_insights[:5]:
            pass

    return result


def example_quick_reasoning() -> Any:
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
                "new_offef": {
                    "salary": "$120k",
                    "commute": "1 hour",
                    "role": "similar",
                },
            },
            "constraints": ["Need work-life balance", "Have young kids"],
        }
    )

    return result


# Run examples
if __name__ == "__main__":
    # Run business example
    business_result = example_business_decision()

    # Run quick example
    quick_result = example_quick_reasoning()
