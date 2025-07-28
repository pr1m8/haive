#!/usr/bin/env python3
"""Consistent V3/V4 Demo - Using the latest enhanced base agent patterns.

This demo uses:
- SimpleAgentV3 (with enhanced base agent)
- ReactAgent (standard version)
- EnhancedMultiAgentV4 (with enhanced base agent and AgentNodeV3)

All components use the consistent enhanced architecture.
"""

import asyncio
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent_v3 import ReactAgentV3

# Use the V3 versions that have enhanced base agent
from haive.agents.simple.agent_v3 import SimpleAgentV3


# Structured output models
class ResearchAnalysis(BaseModel):
    """Research analysis from ReactAgent."""

    topic: str = Field(description="Research topic")
    key_findings: List[str] = Field(description="Important findings")
    data_points: List[str] = Field(description="Supporting data")
    confidence_level: float = Field(
        ge=0.0, le=1.0, description="Confidence in findings"
    )


class ExecutiveReport(BaseModel):
    """Final executive report."""

    title: str = Field(description="Report title")
    executive_summary: str = Field(description="Executive summary (2-3 sentences)")
    strategic_insights: List[str] = Field(description="Key strategic insights")
    recommendations: List[str] = Field(description="Actionable recommendations")
    next_steps: List[str] = Field(description="Immediate next steps")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Overall confidence")


async def demo_enhanced_multi_agent_v4():
    """Demo using EnhancedMultiAgentV4 with SimpleAgentV3 and ReactAgent."""
    print("=" * 80)
    print("CONSISTENT V3/V4 ARCHITECTURE DEMO")
    print("Using Enhanced Base Agent Throughout")
    print("=" * 80)

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

    print(
        "\n✅ Created ReactAgentV3 with tools:",
        [t.name for t in research_agent.engine.tools],
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

    print(
        "✅ Created SimpleAgentV3 (analyst) with structured output:",
        ResearchAnalysis.__name__,
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

    print(
        "✅ Created SimpleAgentV3 (report_writer) with structured output:",
        ExecutiveReport.__name__,
    )

    # Step 5: Create EnhancedMultiAgentV4 workflow
    workflow = EnhancedMultiAgentV4(
        name="research_pipeline",
        agents=[research_agent, analysis_agent, report_agent],
        execution_mode="sequential",
    )

    print("\n✅ Created EnhancedMultiAgentV4 with sequential execution")
    print(f"   Agents: {workflow.get_agent_names()}")

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
        print(f"\n🔍 [{event}] {details.get('agent_name', 'system')}")

    # Note: Hook registration would be done through the agent's hook system
    # For this demo, we'll track manually in the execution

    # Step 7: Execute the workflow
    print("\n" + "-" * 80)
    print("EXECUTING MULTI-AGENT WORKFLOW")
    print("-" * 80)

    try:
        # Initial task
        task = "Analyze the enterprise AI automation market and provide strategic recommendations"
        print(f"\n📋 Task: {task}")

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
        print("\n" + "=" * 80)
        print("WORKFLOW RESULTS")
        print("=" * 80)

        if isinstance(result, dict):
            # Research results
            if "researcher" in result:
                print("\n📊 Research Phase:")
                research_output = result["researcher"]
                print(f"   Output type: {type(research_output)}")
                print(f"   Content preview: {str(research_output)[:200]}...")

            # Analysis results
            if "analyst" in result:
                print("\n🔍 Analysis Phase:")
                analysis = result["analyst"]
                if isinstance(analysis, dict):
                    print(f"   Topic: {analysis.get('topic', 'N/A')}")
                    print(
                        f"   Key Findings: {len(analysis.get('key_findings', []))} findings"
                    )
                    print(f"   Confidence: {analysis.get('confidence_level', 0):.2f}")

            # Final report
            if "report_writer" in result:
                print("\n📄 Final Report:")
                report = result["report_writer"]
                if isinstance(report, dict):
                    print(f"   Title: {report.get('title', 'N/A')}")
                    print(
                        f"   Executive Summary: {report.get('executive_summary', 'N/A')}"
                    )
                    print(f"   Strategic Insights:")
                    for i, insight in enumerate(
                        report.get("strategic_insights", [])[:3], 1
                    ):
                        print(f"      {i}. {insight}")
                    print(f"   Recommendations:")
                    for i, rec in enumerate(report.get("recommendations", [])[:3], 1):
                        print(f"      {i}. {rec}")
                    print(
                        f"   Confidence Score: {report.get('confidence_score', 0):.2f}"
                    )

        # Show execution trace
        print("\n" + "-" * 80)
        print("EXECUTION TRACE")
        print("-" * 80)
        for i, event in enumerate(execution_trace, 1):
            print(f"{i}. [{event['event']}] {event['agent']}")

    except Exception as e:
        trace_execution("workflow_error", {"error": str(e)})
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 80)
    print("DEMO COMPLETED!")
    print("=" * 80)


async def test_individual_agents():
    """Test agents individually to ensure they work."""
    print("\n" + "=" * 80)
    print("TESTING INDIVIDUAL AGENTS")
    print("=" * 80)

    # Test SimpleAgentV3
    print("\n1. Testing SimpleAgentV3...")
    simple = SimpleAgentV3(
        name="test_simple",
        engine=AugLLMConfig(
            temperature=0.3, system_message="You are a helpful assistant."
        ),
    )

    try:
        result = await simple.arun("Hello, how are you?")
        print(f"   ✅ SimpleAgentV3 works! Response: {str(result)[:100]}...")
    except Exception as e:
        print(f"   ❌ SimpleAgentV3 error: {e}")

    # Test ReactAgentV3
    print("\n2. Testing ReactAgentV3...")

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

    try:
        result = await react.arun("Use the test tool with 'hello'")
        print(f"   ✅ ReactAgentV3 works! Response: {str(result)[:100]}...")
    except Exception as e:
        print(f"   ❌ ReactAgentV3 error: {e}")


async def main():
    """Run all demos."""
    # First test individual agents
    await test_individual_agents()

    # Then run the multi-agent demo
    await demo_enhanced_multi_agent_v4()


if __name__ == "__main__":
    asyncio.run(main())
