"""Example usage of StructuredOutputAgent in multi-agent workflows.

This script demonstrates how to use StructuredOutputAgent to convert
any agent's output into structured formats.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from pydantic import BaseModel, Field

from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent
from haive.agents.structured import GenericStructuredOutput, StructuredOutputAgent
from haive.agents.structured.agent import create_structured_agent
from haive.agents.structured.models import AnalysisOutput


def example_1_basic_usage():
    """Example 1: Basic usage with GenericStructuredOutput."""
    # Create structured output agent
    agent = create_structured_agent(
        output_model=GenericStructuredOutput, name="basic_structurer"
    )

    # Some unstructured text (could be from any agent)
    unstructured_text = """
    After reviewing the project, here are my thoughts:

    The main goal should be to improve user engagement by 25% over the next quarter.

    Key findings:
    - Current engagement rate is below industry average
    - Users drop off after 2 minutes on average
    - Mobile experience needs significant improvement

    I recommend:
    1. Redesign the mobile interface
    2. Add gamification elements
    3. Implement push notifications

    This is based on analyzing 10,000 user sessions with high confidence.
    """

    # Convert to structured output
    agent.run(unstructured_text)


def example_2_multi_agent_workflow():
    """Example 2: Multi-agent workflow with ReactAgent + StructuredOutput."""

    # Define custom output structure
    class ProjectPlan(BaseModel):
        project_name: str = Field(description="Name of the project")
        objectives: list[str] = Field(description="Project objectives")
        phases: list[str] = Field(description="Project phases")
        timeline: str = Field(description="Overall timeline")
        budget_estimate: str = Field(description="Budget estimate")
        risks: list[str] = Field(default_factory=list)

    # Create workflow state
    class PlanningWorkflowState(MultiAgentState):
        # Input
        project_request: str = ""

        # ReactAgent output (unstructured, in messages)

        # Structured output fields
        project_name: str = ""
        objectives: list[str] = Field(default_factory=list)
        phases: list[str] = Field(default_factory=list)
        timeline: str = ""
        budget_estimate: str = ""
        risks: list[str] = Field(default_factory=list)

    # Create agents
    planner = ReactAgent(
        name="project_planner",
        engine=AugLLMConfig(
            system_message="""You are a project planning expert.
            Create comprehensive project plans with objectives, phases,
            timelines, budgets, and risk assessments."""
        ),
        tools=[],  # Could add project planning tools
    )

    structurer = StructuredOutputAgent(
        name="plan_structurer",
        output_model=ProjectPlan,
        custom_context="Extract all project planning details accurately",
    )

    # Initialize workflow
    state = PlanningWorkflowState(
        agents=[planner, structurer],
        project_request="Plan a new e-commerce website development project",
    )

    config = {"configurable": {"thread_id": "planning_example"}}

    # Execute workflow
    planner_node = create_agent_node_v3("project_planner")
    planner_node(state, config)

    structurer_node = create_agent_node_v3("plan_structurer")
    structurer_node(state, config)

    # Display results


def example_3_analysis_workflow():
    """Example 3: Converting analysis to structured format."""
    # Create a simple analyst agent (no structured output)
    analyst = SimpleAgent(
        name="data_analyst",
        engine=AugLLMConfig(system_message="Analyze data and provide insights."),
        # No structured_output_model
    )

    # Create structured output agent for analysis
    analysis_structurer = create_structured_agent(
        output_model=AnalysisOutput,
        name="analysis_structurer",
        custom_context="Focus on actionable insights and evidence",
    )

    # Create workflow
    class AnalysisState(MultiAgentState):
        data_description: str = ""

        # Analysis output fields
        summary: str = ""
        findings: list[str] = Field(default_factory=list)
        evidence: list[str] = Field(default_factory=list)
        recommendations: list[str] = Field(default_factory=list)
        confidence_score: float = 0.0

    state = AnalysisState(
        agents=[analyst, analysis_structurer],
        data_description="Customer churn data showing 15% monthly loss rate",
    )

    config = {"configurable": {"thread_id": "analysis_example"}}

    # Run workflow
    analyst_node = create_agent_node_v3("data_analyst")
    structurer_node = create_agent_node_v3("analysis_structurer")

    analyst_node(state, config)
    structurer_node(state, config)


def example_4_custom_model():
    """Example 4: Using a custom output model."""

    # Define custom model for code review
    class CodeReviewOutput(BaseModel):
        overall_quality: int = Field(ge=1, le=10, description="Code quality score")
        issues_found: list[str] = Field(description="List of issues")
        suggestions: list[str] = Field(description="Improvement suggestions")
        security_concerns: list[str] = Field(default_factory=list)
        performance_notes: list[str] = Field(default_factory=list)
        approval_status: str = Field(description="approved/needs_work/rejected")

    # Create code reviewer (any agent type)
    SimpleAgent(
        name="code_reviewer",
        engine=AugLLMConfig(
            system_message="Review code for quality, security, and performance."
        ),
    )

    # Create structurer with custom model
    review_structurer = StructuredOutputAgent(
        name="review_structurer",
        output_model=CodeReviewOutput,
        custom_context="Be thorough in identifying issues and actionable suggestions",
    )

    # Example code review text
    review_text = """
    I've reviewed the authentication module. Overall, the code is well-structured
    with a quality score of 7/10.

    Issues found:
    - No input validation on email parameter
    - Password is logged in debug mode
    - Missing unit tests for edge cases

    Security concerns:
    - Passwords should be hashed with bcrypt, not MD5
    - No rate limiting on login attempts

    Performance is generally good, but the user lookup could use indexing.

    Status: Needs work before approval. Please address security issues first.
    """

    # Direct extraction (without full workflow)
    review_structurer.run(review_text)


if __name__ == "__main__":
    # Run all examples
    example_1_basic_usage()
    example_2_multi_agent_workflow()
    example_3_analysis_workflow()
    example_4_custom_model()
