"""Example: Parallel Execution and Dynamic Agent Addition with EnhancedMultiAgentV4.

This example demonstrates:
1. Parallel execution where multiple agents work simultaneously
2. Dynamic agent addition during runtime
3. Manual graph building and edge configuration
"""

import asyncio
from typing import List

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field


# Define structured output models
class MarketAnalysis(BaseModel):
    """Market analysis results."""

    market_trends: list[str] = Field(..., description="Current market trends")
    opportunities: list[str] = Field(..., description="Market opportunities")
    risks: list[str] = Field(..., description="Market risks")


class CompetitorAnalysis(BaseModel):
    """Competitor analysis results."""

    main_competitors: list[str] = Field(..., description="Main competitors")
    competitive_advantages: list[str] = Field(..., description="Our advantages")
    competitive_threats: list[str] = Field(..., description="Competitive threats")


class CustomerAnalysis(BaseModel):
    """Customer analysis results."""

    customer_segments: list[str] = Field(..., description="Customer segments")
    customer_needs: list[str] = Field(..., description="Customer needs")
    satisfaction_factors: list[str] = Field(..., description="Satisfaction factors")


class BusinessReport(BaseModel):
    """Comprehensive business report combining all analyses."""

    executive_summary: str = Field(..., description="Executive summary")
    market_insights: list[str] = Field(..., description="Key market insights")
    strategic_recommendations: list[str] = Field(
        ..., description="Strategic recommendations"
    )
    action_items: list[str] = Field(..., description="Prioritized action items")


async def parallel_execution_example():
    """Demonstrate parallel execution of multiple analysis agents."""
    print("=" * 80)
    print("Parallel Execution Example: Business Analysis Suite")
    print("=" * 80)

    # Create configuration
    config = AugLLMConfig(temperature=0.5, max_tokens=800)

    # Create specialized analysis agents
    market_analyst = SimpleAgent(
        name="market_analyst",
        engine=config,
        structured_output_model=MarketAnalysis,
        system_message=(
            "You are a market analyst. Analyze market conditions and provide insights "
            "about trends, opportunities, and risks in the technology sector."
        ),
    )

    competitor_analyst = SimpleAgent(
        name="competitor_analyst",
        engine=config,
        structured_output_model=CompetitorAnalysis,
        system_message=(
            "You are a competitor analyst. Analyze the competitive landscape and identify "
            "main competitors, our competitive advantages, and potential threats."
        ),
    )

    customer_analyst = SimpleAgent(
        name="customer_analyst",
        engine=config,
        structured_output_model=CustomerAnalysis,
        system_message=(
            "You are a customer analyst. Analyze customer segments, their needs, "
            "and factors that drive customer satisfaction."
        ),
    )

    # Create workflow with parallel execution
    workflow = EnhancedMultiAgentV4(
        name="business_analysis_suite",
        agents=[market_analyst, competitor_analyst, customer_analyst],
        execution_mode="parallel",  # All analysts work simultaneously
        build_mode="auto",
    )

    print("\nParallel Workflow Configuration:")
    workflow.display_info()

    # Execute parallel analysis
    analysis_request = {
        "messages": [
            {
                "role": "user",
                "content": (
                    "Analyze the business landscape for a new AI-powered productivity app "
                    "targeting remote workers and small businesses. Consider market conditions, "
                    "competition from existing tools like Notion and Asana, and customer needs "
                    "in the post-pandemic remote work environment."
                ),
            }
        ]
    }

    print("\nExecuting parallel analysis...")
    print("-" * 40)

    try:
        start_time = asyncio.get_event_loop().time()
        result = await workflow.arun(analysis_request)
        end_time = asyncio.get_event_loop().time()

        print(
            f"\n✅ Parallel analysis completed in {end_time - start_time:.2f} seconds"
        )

        # Display results from each analyst
        if hasattr(result, "market_analysis"):
            print("\n📈 Market Analysis:")
            analysis = result.market_analysis
            print("Trends:", ", ".join(analysis.market_trends[:3]))
            print(
                "Top Opportunity:",
                analysis.opportunities[0] if analysis.opportunities else "N/A",
            )

        if hasattr(result, "competitor_analysis"):
            print("\n🏢 Competitor Analysis:")
            analysis = result.competitor_analysis
            print("Main Competitors:", ", ".join(analysis.main_competitors[:3]))
            print(
                "Key Advantage:",
                (
                    analysis.competitive_advantages[0]
                    if analysis.competitive_advantages
                    else "N/A"
                ),
            )

        if hasattr(result, "customer_analysis"):
            print("\n👥 Customer Analysis:")
            analysis = result.customer_analysis
            print("Segments:", ", ".join(analysis.customer_segments[:3]))
            print(
                "Top Need:",
                analysis.customer_needs[0] if analysis.customer_needs else "N/A",
            )

    except Exception as e:
        print(f"\n❌ Error during parallel execution: {e}")
        import traceback

        traceback.print_exc()


async def dynamic_agent_addition_example():
    """Demonstrate dynamic agent addition and graph modification."""
    print("\n" + "=" * 80)
    print("Dynamic Agent Addition Example: Expandable Analysis Pipeline")
    print("=" * 80)

    config = AugLLMConfig(temperature=0.4)

    # Start with a basic workflow
    initial_analyzer = SimpleAgent(
        name="initial_analyzer",
        engine=config,
        system_message="Perform initial analysis and identify areas needing deeper investigation.",
    )

    workflow = EnhancedMultiAgentV4(
        name="expandable_pipeline",
        agents=[initial_analyzer],
        execution_mode="manual",  # We'll control the flow
        build_mode="auto",  # Auto-rebuild when agents are added
    )

    print("\nInitial workflow:")
    workflow.display_info()

    # Execute initial analysis
    print("\nRunning initial analysis...")
    await workflow.arun(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "Analyze the feasibility of launching a sustainable fashion e-commerce platform.",
                }
            ]
        }
    )

    print("Initial analysis complete!")

    # Based on initial analysis, dynamically add specialized agents
    print("\n🔧 Adding specialized agents based on initial findings...")

    # Add sustainability expert
    sustainability_expert = SimpleAgent(
        name="sustainability_expert",
        engine=config,
        system_message=(
            "You are a sustainability expert. Analyze environmental impact, "
            "sustainable sourcing options, and green certifications for fashion."
        ),
    )
    workflow.add_agent(sustainability_expert)
    print("✅ Added sustainability expert")

    # Add fashion industry analyst
    fashion_analyst = SimpleAgent(
        name="fashion_analyst",
        engine=config,
        system_message=(
            "You are a fashion industry analyst. Analyze fashion trends, "
            "consumer preferences, and market segmentation in sustainable fashion."
        ),
    )
    workflow.add_agent(fashion_analyst)
    print("✅ Added fashion analyst")

    # Add e-commerce specialist
    ecommerce_specialist = SimpleAgent(
        name="ecommerce_specialist",
        engine=config,
        system_message=(
            "You are an e-commerce specialist. Analyze platform requirements, "
            "payment systems, logistics, and customer experience for online fashion retail."
        ),
    )
    workflow.add_agent(ecommerce_specialist)
    print("✅ Added e-commerce specialist")

    # Add report synthesizer
    synthesizer = SimpleAgent(
        name="synthesizer",
        engine=config,
        structured_output_model=BusinessReport,
        system_message=(
            "You are a report synthesizer. Combine all analyses into a comprehensive "
            "business report with actionable recommendations."
        ),
    )
    workflow.add_agent(synthesizer)
    print("✅ Added report synthesizer")

    # Now add custom edges to create the flow
    print("\n🔗 Configuring execution flow...")

    # Initial analyzer branches to the three specialists
    workflow.add_edge("initial_analyzer", "sustainability_expert")
    workflow.add_edge("initial_analyzer", "fashion_analyst")
    workflow.add_edge("initial_analyzer", "ecommerce_specialist")

    # All specialists feed into the synthesizer
    workflow.add_edge("sustainability_expert", "synthesizer")
    workflow.add_edge("fashion_analyst", "synthesizer")
    workflow.add_edge("ecommerce_specialist", "synthesizer")

    # Rebuild the graph with new configuration
    workflow.rebuild_graph()

    print("\nExpanded workflow:")
    workflow.display_info()

    # Execute the expanded workflow
    print("\nRunning comprehensive analysis with all agents...")
    try:
        comprehensive_result = await workflow.arun(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Provide a comprehensive analysis for launching a sustainable fashion "
                            "e-commerce platform targeting millennials and Gen Z consumers."
                        ),
                    }
                ]
            }
        )

        print("\n✅ Comprehensive analysis complete!")

        if hasattr(comprehensive_result, "business_report"):
            report = comprehensive_result.business_report
            print(f"\n📋 Executive Summary:\n{report.executive_summary}")
            print(
                f"\n🎯 Top Strategic Recommendation:\n{report.strategic_recommendations[0]}"
            )
            print(f"\n✓ Priority Action Item:\n{report.action_items[0]}")

    except Exception as e:
        print(f"\n❌ Error during comprehensive analysis: {e}")
        import traceback

        traceback.print_exc()


async def manual_graph_building_example():
    """Demonstrate manual graph building with complex routing."""
    print("\n" + "=" * 80)
    print("Manual Graph Building Example: Customer Support Router")
    print("=" * 80)

    config = AugLLMConfig(temperature=0.3)

    # Create agents for different support categories
    router = SimpleAgent(
        name="router",
        engine=config,
        system_message=(
            "You are a support ticket router. Classify tickets into categories: "
            "'technical', 'billing', 'general', or 'escalation' based on content and urgency."
        ),
    )

    tech_support = SimpleAgent(
        name="tech_support",
        engine=config,
        system_message="You are a technical support specialist. Resolve technical issues.",
    )

    billing_support = SimpleAgent(
        name="billing_support",
        engine=config,
        system_message="You are a billing specialist. Handle payment and subscription issues.",
    )

    general_support = SimpleAgent(
        name="general_support",
        engine=config,
        system_message="You are a general support agent. Handle general inquiries.",
    )

    escalation_manager = SimpleAgent(
        name="escalation_manager",
        engine=config,
        system_message="You are an escalation manager. Handle complex or urgent issues.",
    )

    # Create workflow with manual mode
    workflow = EnhancedMultiAgentV4(
        name="support_router",
        agents=[
            router,
            tech_support,
            billing_support,
            general_support,
            escalation_manager,
        ],
        execution_mode="manual",
        build_mode="manual",
    )

    # Define routing logic
    def route_ticket(state) -> str:
        """Route ticket based on classification."""
        messages = state.get("messages", [])
        if messages:
            # In real implementation, check router's output
            content = str(messages[-1].content).lower()
            if "technical" in content or "error" in content or "bug" in content:
                return "technical"
            if (
                "billing" in content
                or "payment" in content
                or "subscription" in content
            ):
                return "billing"
            elif "urgent" in content or "escalate" in content:
                return "escalation"
        return "general"

    # Add multi-way conditional routing
    workflow.add_multi_conditional_edge(
        from_agent="router",
        condition=route_ticket,
        routes={
            "technical": "tech_support",
            "billing": "billing_support",
            "escalation": "escalation_manager",
            "general": "general_support",
        },
        default="general_support",
    )

    # Build the graph
    workflow.build()

    print("\nSupport routing workflow configured!")
    workflow.display_info()

    # Test different ticket types
    test_tickets = [
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I'm getting an error when trying to upload files. The system says 'file too large' but my file is only 2MB.",
                }
            ]
        },
        {
            "messages": [
                {
                    "role": "user",
                    "content": "I was charged twice for my subscription this month. Please refund the duplicate payment.",
                }
            ]
        },
        {
            "messages": [
                {
                    "role": "user",
                    "content": "URGENT: Our entire team cannot access the platform. This is affecting our critical operations!",
                }
            ]
        },
    ]

    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n--- Processing Ticket {i} ---")
        try:
            await workflow.arun(ticket)
            print("✅ Ticket processed successfully"y")
        except Exception as e:
            print(f"❌ Error processing ticket: {e}")


async def main():
    """Run all examples."""
    # Run parallel execution example
    await parallel_execution_example()

    # Run dynamic agent addition example
    await dynamic_agent_addition_example()

    # Run manual graph building example
    await manual_graph_building_example()

    print("\n" + "=" * 80)
    print("All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
