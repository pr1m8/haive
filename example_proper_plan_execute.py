"""Example demonstrating the Proper Plan & Execute implementation.

This example shows how to use the proper Plan & Execute agent that:
- Uses existing p_and_e models, prompts, and state
- SimpleAgent for planning with Plan structured output
- ReactAgent for execution with tools
- SimpleAgent for replanning with Act structured output
- Proper LangGraph branching following the official pattern
"""

from haive.agents.planning.proper_plan_execute import create_proper_plan_execute
from haive.tools import duckduckgo_search_tool


def example_basic_usage():
    """Example of basic Plan & Execute usage."""
    # Create the agent
    agent = create_proper_plan_execute(
        name="ExamplePlanExecute", tools=[duckduckgo_search_tool]
    )

    # Simple math problem (doesn't need tools)
    agent.run("What is 25 * 4 + 12?")

    return agent


def example_with_research():
    """Example that requires research and planning."""
    # Create agent with search capabilities
    agent = create_proper_plan_execute(
        name="ResearchPlanExecute", tools=[duckduckgo_search_tool]
    )

    # Complex research task
    research_query = """Research the latest developments in artificial intelligence in 2024 and 2025.
    Focus on major breakthroughs, new models, and industry impact.
    Provide a comprehensive summary with key findings."""

    agent.run(research_query)

    return agent


def example_step_by_step_analysis():
    """Example showing the agent's step-by-step approach."""
    agent = create_proper_plan_execute(
        name="AnalysisPlanExecute", tools=[duckduckgo_search_tool]
    )

    # Multi-step analysis task
    analysis_query = """Analyze the impact of remote work on productivity.
    I need you to:
    1. Research recent studies on remote work productivity
    2. Identify key factors that affect productivity
    3. Compare productivity metrics between remote and office work
    4. Provide actionable recommendations for improving remote work productivity"""

    agent.run(analysis_query)

    return agent


def show_agent_structure():
    """Show the internal structure of the Plan & Execute agent."""
    agent = create_proper_plan_execute()

    for _field_name in agent.state_schema.model_fields:
        pass

    for _i, sub_agent in enumerate(agent.agents):

        if (
            hasattr(sub_agent, "structured_output_model")
            and sub_agent.structured_output_model
        ):
            pass

        if hasattr(sub_agent, "tools") and sub_agent.tools:
            pass


if __name__ == "__main__":

    # Show agent structure
    show_agent_structure()

    # Run examples
    try:
        # Basic usage
        basic_agent = example_basic_usage()

        # Research example (commented out to avoid API calls in demo)

        # Analysis example (commented out to avoid API calls in demo)

    except Exception:
        import traceback

        traceback.print_exc()
