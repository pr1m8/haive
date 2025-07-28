#!/usr/bin/env python3
"""Working Sequential Demo - Shows ReactAgent → SimpleAgent with structured output."""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent_v3 import SimpleAgentV3


# Structured output model
class FinalReport(BaseModel):
    """Final structured report."""

    title: str = Field(description="Report title")
    analysis_summary: str = Field(description="Summary of the analysis")
    key_findings: List[str] = Field(description="Top 3-5 key findings")
    recommendations: List[str] = Field(description="Actionable recommendations")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")


async def main():
    """Demonstrate ReactAgent → SimpleAgent sequential flow."""
    print("=" * 60)
    print("WORKING SEQUENTIAL DEMO")
    print("ReactAgent (with tools) → SimpleAgent (structured output)")
    print("=" * 60)

    # Step 1: Create ReactAgent with tools
    @tool
    def market_analyzer(market: str) -> str:
        """Analyze market trends and data."""
        return f"Analysis of {market}: Growing at 15% annually, valued at $50B globally. Key players: TechCorp (30%), InnovateCo (25%), StartupX (15%)."

    @tool
    def competitor_research(company: str) -> str:
        """Research competitor information."""
        return f"{company} analysis: Market leader in enterprise segment, strong R&D investment, expanding to Asia-Pacific region."

    react_agent = ReactAgent(
        name="market_analyst",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are a market research analyst. Use tools to gather comprehensive market intelligence.",
        ),
    )

    # Add tools to the engine
    react_agent.engine.tools = [market_analyzer, competitor_research]

    print(
        "\n✅ ReactAgent created with tools:",
        [t.name for t in react_agent.engine.tools],
    )

    # Step 2: Create SimpleAgent with structured output
    simple_agent = SimpleAgentV3(
        name="report_writer",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are an executive report writer. Transform analysis into structured reports.",
            structured_output_model=FinalReport,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Based on this market analysis:

{analysis_content}

Create a structured executive report with:
- Clear, concise title
- Analysis summary (2-3 sentences)
- Top 3-5 key findings
- Actionable recommendations
- Confidence score based on data quality""",
                ),
            ]
        ),
    )

    print(
        "✅ SimpleAgentV3 created with structured output model:", FinalReport.__name__
    )

    # Step 3: Execute sequentially
    print("\n" + "-" * 60)
    print("EXECUTING SEQUENTIAL WORKFLOW")
    print("-" * 60)

    # Execute ReactAgent
    print("\n📊 Step 1: ReactAgent analyzing market...")
    market_task = "Analyze the enterprise AI assistant market"

    try:
        react_result = await react_agent.arun(market_task)
        print(f"\nReactAgent output:\n{react_result}")

        # Execute SimpleAgent with ReactAgent's output
        print("\n📝 Step 2: SimpleAgent creating structured report...")
        simple_result = await simple_agent.arun(
            {
                "analysis_content": str(react_result),
                "messages": [{"role": "user", "content": "Create report"}],
            }
        )

        print("\n✨ FINAL STRUCTURED OUTPUT:")
        print("-" * 40)

        if isinstance(simple_result, dict):
            print(f"Title: {simple_result.get('title', 'N/A')}")
            print(
                f"\nAnalysis Summary:\n{simple_result.get('analysis_summary', 'N/A')}"
            )
            print(f"\nKey Findings:")
            for i, finding in enumerate(simple_result.get("key_findings", []), 1):
                print(f"  {i}. {finding}")
            print(f"\nRecommendations:")
            for i, rec in enumerate(simple_result.get("recommendations", []), 1):
                print(f"  {i}. {rec}")
            print(f"\nConfidence Score: {simple_result.get('confidence_score', 0):.2f}")
        else:
            print(f"Result: {simple_result}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("DEMO COMPLETED!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
