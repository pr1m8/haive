"""Example showing how to use the with_structured_output class method.

This demonstrates the powerful pattern of adding structured output to any agent
using the class method approach with future annotations.
"""

from __future__ import annotations

from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field


# Define various output models
class ResearchResult(BaseModel):
    """Structured output for research tasks."""

    topic: str = Field(description="Research topic")
    summary: str = Field(description="Executive summary")
    key_findings: list[str] = Field(description="Key findings")
    sources: list[str] = Field(description="Information sources")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence level")
    next_steps: list[str] = Field(default_factory=list)


class PlanningResult(BaseModel):
    """Structured output for planning tasks."""

    objective: str = Field(description="Main objective")
    strategy: str = Field(description="Overall strategy")
    phases: list[dict[str, str]] = Field(description="Implementation phases")
    timeline: str = Field(description="Expected timeline")
    resources: list[str] = Field(description="Required resources")
    risks: list[str] = Field(default_factory=list)
    success_metrics: list[str] = Field(default_factory=list)


def example_1_class_method_usage():
    """Example 1: Using with_structured_output class method."""
    # Create ReactAgent with structured output in one step
    researcher, research_structurer = ReactAgent.with_structured_output(
        output_model=ResearchResult,
        name="researcher",
        engine=AugLLMConfig(
            system_message="You are a research specialist. Provide comprehensive research on topics."
        ),
        tools=[],  # Could add research tools
    )

    # Create planning agent with structured output
    planner, plan_structurer = SimpleAgent.with_structured_output(
        output_model=PlanningResult,
        name="planner",
        custom_context="Focus on actionable strategies and clear timelines",
        engine=AugLLMConfig(
            system_message="You are a strategic planner. Create detailed implementation plans."
        ),
    )

    # Now use them in a workflow
    class ResearchPlanningState(MultiAgentState):
        # Input
        topic: str = ""

        # Research output fields
        summary: str = ""
        key_findings: list[str] = Field(default_factory=list)
        sources: list[str] = Field(default_factory=list)
        confidence: float = 0.0
        next_steps: list[str] = Field(default_factory=list)

        # Planning output fields
        objective: str = ""
        strategy: str = ""
        phases: list[dict[str, str]] = Field(default_factory=list)
        timeline: str = ""
        resources: list[str] = Field(default_factory=list)
        risks: list[str] = Field(default_factory=list)
        success_metrics: list[str] = Field(default_factory=list)

    # Initialize workflow
    state = ResearchPlanningState(
        agents=[researcher, research_structurer, planner, plan_structurer],
        topic="Implementing AI in healthcare",
    )

    config = {"configurable": {"thread_id": "research_planning"}}

    # Execute workflow
    researcher_node = create_agent_node_v3("researcher")
    researcher_node(state, config)

    research_struct_node = create_agent_node_v3("researcher_structured")
    research_struct_node(state, config)

    planner_node = create_agent_node_v3("planner")
    planner_node(state, config)

    plan_struct_node = create_agent_node_v3("planner_structured")
    plan_struct_node(state, config)


def example_2_structured_tool():
    """Example 2: Using as_structured_tool class method."""
    # Create a structured research tool
    research_tool = ReactAgent.as_structured_tool(
        output_model=ResearchResult,
        name="research_tool",
        description="Research any topic and return structured results",
        engine=AugLLMConfig(
            system_message="You are a research expert. Provide thorough research."
        ),
    )

    # Use the tool in another agent
    coordinator = SimpleAgent(
        name="research_coordinator",
        engine=AugLLMConfig(
            system_message="You coordinate research tasks using available tools."
        ),
        tools=[research_tool],
    )

    # Run coordinator
    coordinator.run("Research the latest advances in quantum computing")


def example_3_ensure_structured_output():
    """Example 3: Using ensure_structured_output instance method."""

    # Create a custom agent that uses ensure_structured_output
    class SmartAgent(SimpleAgent):
        """Agent that ensures its output is always structured."""

        def run(self, input_text: str) -> ResearchResult:
            # Get raw output from engine
            raw_output = super().run(input_text)

            # Ensure it's structured
            structured = self.ensure_structured_output(
                raw_output, ResearchResult, handle_errors=True
            )

            if structured is None:
                # Fallback if conversion fails
                structured = ResearchResult(
                    topic="Unknown",
                    summary="Conversion failed",
                    key_findings=[],
                    sources=[],
                    confidence=0.0,
                )

            return structured

    # Use the smart agent
    agent = SmartAgent(name="smart_researcher", engine=AugLLMConfig())

    agent.run("Tell me about machine learning")


def example_4_handling_different_formats():
    """Example 4: Handling various output formats."""
    # Create agent with structured output
    agent, structurer = SimpleAgent.with_structured_output(
        output_model=ResearchResult, name="format_handler"
    )

    # Test different output formats
    test_outputs = [
        # String output
        "Research shows that AI is advancing rapidly with key findings in NLP and computer vision.",
        # AIMessage with content
        AIMessage(
            content="The analysis reveals three key findings about quantum computing..."
        ),
        # AIMessage with tool calls
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "ResearchResult",
                    "args": {
                        "topic": "Quantum Computing",
                        "summary": "Quantum computing is advancing",
                        "key_findings": [
                            "Qubit stability improved",
                            "Error rates reduced",
                        ],
                        "sources": ["Nature", "Science"],
                        "confidence": 0.9,
                    },
                }
            ],
        ),
        # Dict output
        {
            "output": "Climate change research indicates warming trends...",
            "metadata": {"source": "IPCC"},
        },
        # Already structured
        ResearchResult(
            topic="Pre-structured",
            summary="This is already in the right format",
            key_findings=["No conversion needed"],
            sources=["Direct"],
            confidence=1.0,
        ),
    ]

    for _i, output in enumerate(test_outputs):
        # Use ensure_structured_output
        structured = agent.ensure_structured_output(
            output, ResearchResult, handle_errors=True
        )

        if structured:
            pass
        else:
            pass


def example_5_multi_agent_with_fallback():
    """Example 5: Multi-agent with structured output and fallback."""

    # Define a complex output model
    class ComplexAnalysis(BaseModel):
        executive_summary: str
        quantitative_metrics: dict[str, float]
        qualitative_insights: list[str]
        recommendations: list[dict[str, str]]
        confidence_scores: dict[str, float]
        limitations: list[str] = Field(default_factory=list)

    # Create analyzer with structured output
    analyzer, structurer = ReactAgent.with_structured_output(
        output_model=ComplexAnalysis,
        name="complex_analyzer",
        custom_context="Ensure all metrics are quantified and recommendations are actionable",
    )

    # Create state with all fields
    class AnalysisState(MultiAgentState):
        input_data: str = ""

        # Complex analysis fields
        executive_summary: str = ""
        quantitative_metrics: dict[str, float] = Field(default_factory=dict)
        qualitative_insights: list[str] = Field(default_factory=list)
        recommendations: list[dict[str, str]] = Field(default_factory=list)
        confidence_scores: dict[str, float] = Field(default_factory=dict)
        limitations: list[str] = Field(default_factory=list)

    state = AnalysisState(
        agents=[analyzer, structurer],
        input_data="Analyze the performance of our e-commerce platform in Q4",
    )

    config = {"configurable": {"thread_id": "complex_analysis"}}

    # Run analysis
    analyzer_node = create_agent_node_v3("complex_analyzer")
    structurer_node = create_agent_node_v3("complex_analyzer_structured")

    analyzer_node(state, config)
    structurer_node(state, config)


if __name__ == "__main__":
    # Run all examples
    example_1_class_method_usage()
    example_2_structured_tool()
    example_3_ensure_structured_output()
    example_4_handling_different_formats()
    example_5_multi_agent_with_fallback()
