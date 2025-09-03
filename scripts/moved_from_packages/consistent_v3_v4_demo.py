#!/usr/bin/env python3
"""Consistent V3/V4 Demo - Using the latest enhanced base agent patterns.

This demo uses:
- SimpleAgentV3 (with enhanced base agent)
- ReactAgent (standard version)
- EnhancedMultiAgentV4 (with enhanced base agent and AgentNodeV3)

All components use the consistent enhanced architecture.
"""

import asyncio
import contextlib

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent_v3 import ReactAgentV3

# Use the V3 versions that have enhanced base agent
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field


# Structured output models
class ResearchAnalysis(BaseModel):
    """Research analysis from ReactAgent."""

    topic: str = Field(description="Research topic")
    key_findings: list[str] = Field(description="Important findings")
    data_points: list[str] = Field(description="Supporting data")
    confidence_level: float = Field(
        ge=0.0, le=1.0, description="Confidence in findings"
    )


class ExecutiveReport(BaseModel):
    """Final executive report."""

    title: str = Field(description="Report title")
    executive_summary: str = Field(description="Executive summary (2-3 sentences)")
    strategic_insights: list[str] = Field(description="Key strategic insights")
    recommendations: list[str] = Field(description="Actionable recommendations")
    next_steps: list[str] = Field(description="Immediate next steps")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")


async def demo_enhanced_multi_agent_v4():
    """Demo using EnhancedMultiAgentV4 with SimpleAgentV3 and ReactAgent."""

    # Step 1: Create tools for ReactAgent
    @tool
    def market_research(query: str) -> str:
        """Perform market research on a topic."""
        return f"Research on '{query}': Market valued at $75B, growing 20% annually. Key trends: AI integration, automation, sustainability."

    @tool
    def competitive_analysis(company: str) -> str:
        """Analyze competitive landscape."""
        return f"Analysis of {company}: Leading player with 35% market share, strong in innovation, expanding globally."

    @tool
    def trend_analyzer(trend: str) -> str:
        """Analyze industry trends."""
        return f"Trend '{trend}': High growth potential, adoption rate increasing 40% YoY, significant investment flowing in."

    # Step 2: Create ReactAgentV3 for research
    research_agent = ReactAgentV3(
        name="researcher",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="You are a thorough market researcher. Use tools to gather comprehensive insights.",
            tools=[market_research, competitive_analysis, trend_analyzer],
        ),
    )

    # Step 3: Create SimpleAgentV3 for analysis with structured output
    analysis_agent = SimpleAgentV3(
        name="analyst",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="You are a strategic analyst. Transform research into structured insights.",
            structured_output_model=ResearchAnalysis,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Analyze this research data:

{research_data}

Provide structured analysis with:
- Clear topic identification
- Key findings (3-5 points)
- Supporting data points
- Confidence level assessment""",
                ),
            ]
        ),
    )

    # Step 4: Create SimpleAgentV3 for final report
    report_agent = SimpleAgentV3(
        name="report_writer",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="You are an executive report writer. Create polished, actionable reports.",
            structured_output_model=ExecutiveReport,
        ),
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "{system_message}"),
                (
                    "human",
                    """Based on this analysis:

Topic: {topic}
Key Findings: {key_findings}
Data Points: {data_points}
Confidence Level: {confidence_level}

Create an executive report with:
- Compelling title
- Brief executive summary
- Strategic insights
- Clear recommendations
- Immediate next steps""",
                ),
            ]
        ),
    )

    # Step 5: Create EnhancedMultiAgentV4 workflow
    workflow = EnhancedMultiAgentV4(
        name="research_pipeline",
        agents=[research_agent, analysis_agent, report_agent],
        execution_mode="sequential",
    )

    # Step 6: Add hooks for monitoring
    execution_trace = []

    def trace_execution(event: str, details: dict):
        """Trace execution events."""
        execution_trace.append(
            {
                "event": event,
                "agent": details.get("agent_name", "system"),
                "timestamp": asyncio.get_event_loop().time(),
            }
        )

    # Note: Hook registration would be done through the agent's hook system
    # For this demo, we'll track manually in the execution

    # Step 7: Execute the workflow

    try:
        # Initial task
        task = "Analyze the enterprise AI automation market and provide strategic recommendations"

        trace_execution("workflow_start", {"task": task})

        # Execute workflow
        result = await workflow.arun(
            {
                "messages": [{"role": "user", "content": task}],
                "research_data": "",  # Will be populated by research agent
                "topic": "",
                "key_findings": [],
                "data_points": [],
                "confidence_level": 0.0,
            }
        )

        trace_execution("workflow_complete", {"status": "success"})

        # Display results

        if isinstance(result, dict):
            # Research results
            if "researcher" in result:
                result["researcher"]

            # Analysis results
            if "analyst" in result:
                analysis = result["analyst"]
                if isinstance(analysis, dict):
                    pass

            # Final report
            if "report_writer" in result:
                report = result["report_writer"]
                if isinstance(report, dict):
                    for _i, _insight in enumerate(
                        report.get("strategic_insights", [])[:3], 1
                    ):
                        pass
                    for _i, _rec in enumerate(report.get("recommendations", [])[:3], 1):
                        pass

        # Show execution trace
        for _i, _event in enumerate(execution_trace, 1):
            pass

    except Exception as e:
        trace_execution("workflow_error", {"error": str(e)})
        import traceback

        traceback.print_exc()


async def test_individual_agents():
    """Test agents individually to ensure they work."""
    # Test SimpleAgentV3
    simple = SimpleAgentV3(
        name="test_simple",
        engine=AugLLMConfig(
            temperature=0.3, system_message="You are a helpful assistant."
        ),
    )

    with contextlib.suppress(Exception):
        await simple.arun("Hello, how are you?")

    # Test ReactAgentV3

    @tool
    def test_tool(input: str) -> str:
        """Test tool."""
        return f"Processed: {input}"

    react = ReactAgentV3(
        name="test_react",
        engine=AugLLMConfig(
            system_message="You are a helpful assistant.", tools=[test_tool]
        ),
    )

    with contextlib.suppress(Exception):
        await react.arun("Use the test tool with 'hello'")


async def main():
    """Run all demos."""
    # First test individual agents
    await test_individual_agents()

    # Then run the multi-agent demo
    await demo_enhanced_multi_agent_v4()


if __name__ == "__main__":
    asyncio.run(main())
