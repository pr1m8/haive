#!/usr/bin/env python3
"""Working Sequential Demo - Shows ReactAgent → SimpleAgent with structured output."""

import asyncio

from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Structured output model
class FinalReport(BaseModel):
    """Final structured report."""

    title: str = Field(description="Report title")
    analysis_summary: str = Field(description="Summary of the analysis")
    key_findings: list[str] = Field(description="Top 3-5 key findings")
    recommendations: list[str] = Field(description="Actionable recommendations")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")


async def main():
    """Demonstrate ReactAgent → SimpleAgent sequential flow."""

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

    # Step 3: Execute sequentially

    # Execute ReactAgent
    market_task = "Analyze the enterprise AI assistant market"

    try:
        react_result = await react_agent.arun(market_task)

        # Execute SimpleAgent with ReactAgent's output
        simple_result = await simple_agent.arun(
            {
                "analysis_content": str(react_result),
                "messages": [{"role": "user", "content": "Create report"}],
            }
        )

        if isinstance(simple_result, dict):
            for _i, _finding in enumerate(simple_result.get("key_findings", []), 1):
                pass
            for _i, _rec in enumerate(simple_result.get("recommendations", []), 1):
                pass
        else:
            pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
