"""ReWOO Planner Agent - Simple agent focused on plan generation."""

import logging
from typing import Any, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig

from haive.agents.planning.rewoo.models import ReWOOPlan
from haive.agents.simple.agent import SimpleAgent

from .models import PlannerState
from .prompts import REWOO_PLANNING_TEMPLATE

logger = logging.getLogger(__name__)


class ReWOOPlannerAgent(SimpleAgent):
    """Simple agent that generates ReWOO plans using structured output.

    This agent is focused solely on creating evidence-based plans.
    It uses the planning prompt template and structured output to generate
    properly formatted ReWOO plans with tool calls and evidence references.
    """

    # Use default SimpleAgent state for now (keep it simple)

    # Override tools field to expose for planning context
    tools: List[Any] | None = None

    def __init__(
        self, name: str = "rewoo_planner", tools: List[Any] | None = None, **kwargs
    ):
        """Initialize ReWOO planner agent.

        Args:
            name: Agent name
            tools: Available tools for planning context
            **kwargs: Additional arguments passed to SimpleAgent
        """
        # Ensure structured output is configured for ReWOO plans
        if "engine" in kwargs:
            engine = kwargs["engine"]
            if hasattr(engine, "structured_output_model"):
                # Already configured
                pass
            else:
                # Configure for ReWOO planning
                engine = engine.model_copy(
                    update={
                        "structured_output_model": ReWOOPlan,
                        "structured_output_version": "v2",  # Use v2 for tool call parsing
                        "system_message": REWOO_PLANNING_TEMPLATE,  # Use planning prompt template
                    }
                )
                kwargs["engine"] = engine
        else:
            # Default engine for planning
            kwargs["engine"] = AugLLMConfig(
                name=f"{name}_engine",
                structured_output_model=ReWOOPlan,
                structured_output_version="v2",  # Use v2 for tool call parsing
                system_message=REWOO_PLANNING_TEMPLATE,  # Use planning prompt template
                temperature=0.7,
            )

        # Set tools in field (SimpleAgent pattern)
        if tools is not None:
            kwargs["tools"] = tools

        super().__init__(name=name, **kwargs)

    def setup_agent(self):
        """Setup planner agent with tools in state."""
        super().setup_agent()

        # Set available tools in state without auto-sync
        # This provides tools to the prompt context via computed field
        if hasattr(self, "tools") and self.tools:
            # Tools will be accessed via state.tool_options computed field
            pass

    async def create_plan(self, query: str) -> ReWOOPlan:
        """Create a ReWOO plan for the given query.

        Args:
            query: The user's query to plan for

        Returns:
            ReWOOPlan: The generated structured plan
        """
        # Format the prompt with available tools
        tool_options = [
            tool.name if hasattr(tool, "name") else str(tool)
            for tool in (self.tools or [])
        ]

        # Use the planning template
        prompt = REWOO_PLANNING_TEMPLATE.format(tool_options=tool_options, query=query)

        # Run the agent with structured output
        result = await self.arun(prompt)

        # The result should be a ReWOOPlan due to structured output
        if isinstance(result, ReWOOPlan):
            return result
        logger.warning(f"Expected ReWOOPlan but got {type(result)}: {result}")
        # Try to extract from result if it's wrapped
        if hasattr(result, "structured_output"):
            return result.structured_output
        elif hasattr(result, "plan"):
            return result.plan
        else:
            raise ValueError(f"Failed to generate ReWOOPlan, got: {type(result)}")

    def create_runnable(self, runnable_config=None):
        """Override to set available_tools in initial state."""
        # Set available tools in state for prompt context
        if hasattr(self, "tools") and self.tools:
            initial_state = {"available_tools": self.tools}
        else:
            pass

        # Create runnable with initial state
        runnable = super().create_runnable(runnable_config)

        return runnable


# Test function to validate the planner
async def test_rewoo_planner():
    """Test the ReWOO planner agent."""
    from haive.tools.tools.search_tools import tavily_qna, tavily_search_tool
    from haive.tools.tools.yfinance_tool import yfinance_news_tool

    # Create planner with real tools
    planner = ReWOOPlannerAgent(
        name="test_planner", tools=[tavily_search_tool, tavily_qna, yfinance_news_tool]
    )

    # Test query
    query = "What is the current stock price of Apple (AAPL) and what are the latest news about the company?"


    try:
        # Generate plan
        plan = await planner.create_plan(query)

        if plan.evidence_map:
            pass

        for i, step in enumerate(plan.steps, 1):
            if step.evidence:
                pass
            if step.tool_call:

        if plan.evidence_map:
            for eid, evidence in plan.evidence_map.items():
                pass

        return plan

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_rewoo_planner())
