"""Multi-Agent Structured Output Demo.

This example demonstrates:
1. ReactAgent with tools → SimpleAgent with structured output
2. Prompt templates with input variables
3. Hook integration for monitoring
4. Reflection patterns
"""

import asyncio

from haive.agents.base.hooks import HookContext, HookEvent
from haive.agents.base.pre_post_agent_mixin import create_reflection_agent
from haive.agents.multi.enhanced_multi_agent_v4 import EnhancedMultiAgentV4
from haive.agents.react.agent_v3 import ReactAgentV3
from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# ============================================================================
# STRUCTURED OUTPUT MODELS
# ============================================================================


class MarketAnalysis(BaseModel):
    """Structured market analysis output."""

    market_name: str = Field(description="Name of the market analyzed")
    market_size: str = Field(description="Current market size")
    growth_rate: float = Field(description="Annual growth rate percentage")
    key_players: list[str] = Field(description="Major companies in the market")
    opportunities: list[str] = Field(description="Market opportunities")
    risks: list[str] = Field(description="Market risks")
    recommendation: str = Field(description="Investment recommendation")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in analysis")


# ============================================================================
# TOOLS
# ============================================================================


@tool
def market_research(market: str) -> str:
    """Research a specific market."""
    # Simulated market data
    markets = {
        "AI": {
            "size": "$150 billion",
            "growth": 35.0,
            "players": ["OpenAI", "Google", "Microsoft", "Amazon"],
            "trends": "Generative AI, MLOps, Edge AI",
        },
        "renewable energy": {
            "size": "$1.1 trillion",
            "growth": 12.5,
            "players": ["NextEra", "Iberdrola", "Orsted", "Enel"],
            "trends": "Solar, Wind, Battery Storage",
        },
    }

    data = markets.get(
        market.lower(),
        {"size": "Unknown", "growth": 0.0, "players": [], "trends": "No data"},
    )

    return f"""Market Research for {market}:
- Market Size: {data["size"]}
- Growth Rate: {data["growth"]}% annually
- Key Players: {", ".join(data["players"])}
- Trends: {data["trends"]}"""


@tool
def financial_calculator(expression: str) -> str:
    """Calculate financial metrics."""
    try:
        result = eval(expression)
        return f"Calculation: {expression} = {result}"
    except:
        return "Calculation error"


# ============================================================================
# AGENTS
# ============================================================================


def create_market_analyst() -> ReactAgentV3:
    """Create market analysis agent with tools."""
    config = AugLLMConfig(
        temperature=0.6,
        system_message="You are a market analyst. Use tools to research markets and provide insights.",
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_message}"),
            ("human", "Analyze the {market} market. Focus on: {focus_areas}"),
        ]
    )

    return ReactAgentV3(
        name="market_analyst",
        engine=config,
        prompt_template=prompt,
        tools=[market_research, financial_calculator],
    )


def create_report_writer() -> SimpleAgentV3:
    """Create report writer with structured output."""
    config = AugLLMConfig(
        temperature=0.5,
        structured_output_model=MarketAnalysis,
        system_message="You are a professional report writer. Create structured market analysis reports.",
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "{system_message}"),
            (
                "human",
                """Create a structured market analysis report based on:

Market: {market}
Research Data:
{research_data}

Provide a comprehensive analysis with actionable recommendations.""",
            ),
        ]
    )

    return SimpleAgentV3(name="report_writer", engine=config, prompt_template=prompt)


# ============================================================================
# HOOK MONITORING
# ============================================================================


class WorkflowMonitor:
    """Monitor multi-agent workflow execution."""

    def __init__(self):
        self.events = []
        self.agent_outputs = {}

    def create_hook(self):
        def monitor(context: HookContext):
            event = {
                "event": context.event.value,
                "agent": context.agent_name,
                "timestamp": context.timestamp,
            }

            # Capture agent outputs
            if context.event == HookEvent.AFTER_RUN and hasattr(context, "result"):
                self.agent_outputs[context.agent_name] = {
                    "completed": True,
                    "has_output": bool(context.result),
                }

            self.events.append(event)

        return monitor


# ============================================================================
# DEMO FUNCTIONS
# ============================================================================


async def demo_basic_flow():
    """Demonstrate basic ReactAgent → SimpleAgent flow."""
    # Create agents
    analyst = create_market_analyst()
    writer = create_report_writer()

    # Create workflow
    workflow = EnhancedMultiAgentV4(agents=[analyst, writer], mode="sequential")

    # Input data
    initial_state = {
        "messages": [HumanMessage(content="Analyze the AI market")],
        "market": "AI",
        "focus_areas": "growth potential, key players, investment opportunities",
        "system_message": "Provide thorough analysis",
        "research_data": "",  # Will be filled by analyst
    }

    # Execute
    result = await workflow.arun(initial_state)

    # Display structured output
    if "messages" in result and len(result["messages"]) > 0:
        last_msg = result["messages"][-1]
        if hasattr(last_msg, "content"):
            try:
                import json

                data = json.loads(last_msg.content)
                for _key, _value in data.items():
                    pass
            except:
                pass

    return result


async def demo_with_hooks():
    """Demonstrate workflow with comprehensive hook monitoring."""
    # Create monitor
    monitor = WorkflowMonitor()

    # Create agents with hooks
    analyst = create_market_analyst()
    writer = create_report_writer()

    # Add hooks
    for agent in [analyst, writer]:
        agent.add_hook(HookEvent.BEFORE_RUN, monitor.create_hook())
        agent.add_hook(HookEvent.AFTER_RUN, monitor.create_hook())

    # Create workflow
    workflow = EnhancedMultiAgentV4(agents=[analyst, writer], mode="sequential")

    # Execute
    initial_state = {
        "messages": [HumanMessage(content="Analyze renewable energy market")],
        "market": "renewable energy",
        "focus_areas": "solar, wind, battery storage opportunities",
        "system_message": "Focus on investment potential",
        "research_data": "",
    }

    result = await workflow.arun(initial_state)

    # Display monitoring results
    for agent, _status in monitor.agent_outputs.items():
        pass

    return result


async def demo_with_reflection():
    """Demonstrate report writing with reflection."""
    # Create base writer
    writer = create_report_writer()

    # Enhance with reflection
    reflective_writer = create_reflection_agent(
        main_agent=writer,
        reflection_config=AugLLMConfig(
            temperature=0.4,
            system_message="You are a critical editor. Review the report and suggest improvements for clarity and impact.",
        ),
    )

    # Test data (as if from analyst)
    test_state = {
        "messages": [HumanMessage(content="Write market report")],
        "market": "Quantum Computing",
        "research_data": """Quantum Computing Market Research:
- Market Size: $500 million (2024)
- Growth Rate: 45% CAGR
- Key Players: IBM, Google, Rigetti, IonQ
- Opportunities: Drug discovery, cryptography, optimization
- Challenges: Technical complexity, high costs, talent shortage
- Recent breakthroughs in error correction
- Government investment increasing globally""",
        "system_message": "Create investment-focused report",
    }

    # Execute with reflection
    result = await reflective_writer.arun(test_state)

    if isinstance(result, dict) and "messages" in result:
        pass

    return result


# ============================================================================
# MAIN
# ============================================================================


async def main():
    """Run all demos."""
    # Demo 1: Basic flow
    await demo_basic_flow()

    # Demo 2: With hooks
    await demo_with_hooks()

    # Demo 3: With reflection
    await demo_with_reflection()


if __name__ == "__main__":
    asyncio.run(main())
