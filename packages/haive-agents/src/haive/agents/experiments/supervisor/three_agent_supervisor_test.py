#!/usr/bin/env python3
"""Test supervisor coordinating three specialized agents for complex tasks."""

from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from haive.tools.tools.search_tools import tavily_search_tool
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Import our integrated supervisor
from haive.agents.experiments.supervisor.integrated_supervisor_with_handoff import (
    IntegratedSupervisorWithHandoff,
)
from haive.agents.experiments.supervisor.test_registry_setup import AgentRegistry
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Define Essay structure for essay writer
class Essay(BaseModel):
    title: str = Field(description="Essay title")
    introduction: str = Field(description="Introduction paragraph")
    body_paragraphs: list[str] = Field(description="Main body paragraphs")
    conclusion: str = Field(description="Conclusion paragraph")


def create_three_specialized_agents():
    """Create three agents with different specializations."""

    # 1. Research Agent - uses tavily_search tool
    research_engine = AugLLMConfig(
        name="research_engine",
        tools=[tavily_search_tool],
        system_message="""You are a research specialist. Use the tavily_search_tool to find accurate,
        up-to-date information. Always cite your sources and provide specific data when available.""",
    )
    research_agent = ReactAgent(name="research_agent", engine=research_engine)

    # 2. Math Agent - uses add/multiply tools (from previous tests)
    @tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers."""
        return a + b

    @tool
    def multiply(a: int, b: int) -> int:
        """Returns the product of two numbers."""
        return a * b

    @tool
    def calculate_roi(initial_cost: float, annual_benefit: float, years: int) -> float:
        """Calculate ROI over specified years.

        ROI = (Total Benefits - Total Costs) / Total Costs * 100
        """
        total_benefits = annual_benefit * years
        roi_percentage = ((total_benefits - initial_cost) / initial_cost) * 100
        return roi_percentage

    math_engine = AugLLMConfig(
        name="math_engine",
        tools=[add, multiply, calculate_roi],
        system_message="""You are a mathematical calculation specialist. Use the available tools to
        perform accurate calculations. Always show your work and explain the results.""",
    )
    math_agent = ReactAgent(name="math_agent", engine=math_engine)

    # 3. Essay Writer Agent - uses structured output
    essay_engine = AugLLMConfig(
        name="essay_engine",
        structured_output_model=Essay,
        structured_output_version="v2",
        system_message="""You are a professional essay writer. Create well-structured essays with:
        - A compelling title
        - Clear introduction stating the main points
        - Detailed body paragraphs with evidence
        - Strong conclusion summarizing key findings

        Base your essay on the research and calculations provided.""",
    )
    essay_writer_agent = SimpleAgent(name="essay_writer_agent", engine=essay_engine)

    return {
        "research_agent": research_agent,
        "math_agent": math_agent,
        "essay_writer_agent": essay_writer_agent,
    }


def test_three_agent_coordination():
    """Test supervisor coordinating all three agents for a complex task."""

    # Create all agents
    agents = create_three_specialized_agents()

    # Create registry and register all agents
    registry = AgentRegistry()
    registry.register(
        "research_agent",
        agents["research_agent"],
        "Searches for information using Tavily search tool",
    )
    registry.register(
        "math_agent",
        agents["math_agent"],
        "Performs mathematical calculations and ROI analysis",
    )
    registry.register(
        "essay_writer_agent",
        agents["essay_writer_agent"],
        "Writes structured essays based on research and data",
    )

    for name, desc in registry.list_available().items():
        pass

    # Create integrated supervisor with all agents
    supervisor = IntegratedSupervisorWithHandoff(
        name="three_agent_supervisor", agent_registry=registry
    )


    # Test multi-step task requiring all three agents
    complex_task = """Research the current costs of implementing AI chatbots for customer service
    in small businesses. Calculate the ROI over 5 years assuming 20% efficiency gain and
    $50,000 annual savings. Then write a brief essay about whether small businesses should
    invest in AI chatbots based on the research and calculations."""




    try:
        result = supervisor.invoke({"messages": [HumanMessage(complex_task)]})


        # Extract and display results
        if hasattr(result, "messages") and result.messages:

            # Show last few messages to see the flow
            for i, msg in enumerate(result.messages[-5:]):  # Last 5 messages
                msg_type = type(msg).__name__
                content_preview = (
                    str(msg.content)[:200] + "..."
                    if len(str(msg.content)) > 200
                    else str(msg.content)
                )


    except Exception as e:
        import traceback

        traceback.print_exc()

    return supervisor


def test_individual_agent_capabilities():
    """Test each agent individually to ensure they work before coordination."""

    agents = create_three_specialized_agents()

    # Test research agent
    try:
        research_result = agents["research_agent"].invoke(
            {
                "messages": [
                    HumanMessage("Search for average cost of AI chatbot implementation")
                ]
            }
        )
    except Exception as e:
        pass")

    # Test math agent
    try:
        math_result = agents["math_agent"].invoke(
            {
                "messages": [
                    HumanMessage(
                        "Calculate ROI: initial cost $100,000, annual benefit $50,000, over 5 years"
                    )
                ]
            }
        )
    except Exception as e:
        pass")

    # Test essay writer
    try:
        essay_result = agents["essay_writer_agent"].invoke(
            {
                "messages": [
                    HumanMessage(
                        "Write a brief essay about AI adoption in small businesses"
                    )
                ]
            }
        )
    except Exception as e:
        pass")


if __name__ == "__main__":
    # First test individual agents
    test_individual_agent_capabilities()

    # Then test full coordination
    supervisor = test_three_agent_coordination()
