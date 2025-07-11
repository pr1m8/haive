"""ReWOO Agent following SimpleAgent pattern with ReWOO-specific routing."""

import logging
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.node.tool_node_config_v2 import ToolNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.llm_state import LLMState
from langchain_core.messages import AIMessage
from langgraph.graph import END, START
from langgraph.types import Command
from pydantic import Field, computed_field

from haive.agents.planning.rewoo.models import EvidenceStatus, ReWOOPlan
from haive.agents.planning.rewoo.planner.prompts import REWOO_PLANNING_TEMPLATE
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class ReWOOState(LLMState):
    """ReWOO-specific state that extends LLMState with tool options.

    This state provides tools as a computed field that can be used by the agent
    but doesn't automatically sync them to all engines. This gives us more control
    over tool routing through validation nodes.
    """

    # Store available tools without auto-sync
    available_tools: list[Any] = Field(
        default_factory=list,
        description="Available tools for ReWOO planning (no auto-sync)",
    )

    # ReWOO-specific fields
    current_plan: ReWOOPlan | None = Field(
        default=None, description="Current ReWOO plan being executed"
    )

    evidence_collected: dict[str, Any] = Field(
        default_factory=dict, description="Evidence collected during execution"
    )

    @computed_field
    @property
    def tool_options(self) -> list[str]:
        """Computed field providing tool names for planning prompts."""
        return [
            tool.name if hasattr(tool, "name") else str(tool)
            for tool in self.available_tools
        ]

    @computed_field
    @property
    def planning_context(self) -> str:
        """Computed field for planning agent system message."""
        return f"""You are a ReWOO planning agent. Create evidence-based plans.

Given the user's query, create a ReWOO plan with:
1. Steps that collect evidence (#E1, #E2, etc.)
2. Tool calls for each piece of evidence
3. Evidence dependencies and references

Available tools: {self.tool_options}

Create a structured plan where each step produces evidence that later steps can reference."""


class ReWOOAgent(SimpleAgent):
    """ReWOO Agent that extends SimpleAgent with evidence-based planning.

    This agent follows the ReWOO pattern:
    1. Planning: Creates evidence-based plan
    2. Collection: Collects evidence systematically
    3. Reasoning: Uses evidence for final answer

    Uses LLMState with controlled tool routing instead of automatic sync.
    """

    # Use ReWOO-specific state schema
    state_schema: type = Field(
        default=ReWOOState,
        description="ReWOO state with LLMState base and controlled tool routing",
    )

    def setup_agent(self):
        """Setup ReWOO agent with proper engines and controlled tool routing."""
        # 1. DEFINE ENGINES FIRST with proper names matching node config
        # Format the prompt template with available tools
        tool_options = []
        if hasattr(self, "tools") and self.tools:
            tool_options = [
                tool.name if hasattr(tool, "name") else str(tool) for tool in self.tools
            ]

        # Use the ReWOO planning template

        planning_prompt = REWOO_PLANNING_TEMPLATE.format(tools=str(tool_options))

        # Define planning engine with structured output v2
        planning_engine = self.engine.model_copy(
            update={
                "name": "planning",
                "structured_output_model": ReWOOPlan,
                "structured_output_version": "v2",
                "system_message": planning_prompt,
            }
        )

        reasoning_engine = self.engine.model_copy(
            update={
                "name": "reasoning",  # Use simple name to match node config
                "system_message": """You are a ReWOO reasoning agent. Use collected evidence to answer.

Review all evidence collected and synthesize into a comprehensive response.
Reference specific evidence when making claims (e.g., "Based on #E1...").""",
            }
        )

        # 2. REGISTER ENGINES (no tool sync - we control this)
        self.engines = {
            "planning": planning_engine,
            "reasoning": reasoning_engine,
            "main": self.engine,  # Keep main engine for tool execution
        }

        # 3. CALL PARENT SETUP but skip tool sync
        super().setup_agent()

        # 4. SET AVAILABLE TOOLS in state (no auto-sync)
        if hasattr(self, "tools") and self.tools:
            # This will be set in state but won't auto-sync to engines
            pass

    def build_graph(self) -> BaseGraph:
        """Build ReWOO graph with conditional routing and validation nodes."""
        # Create ReWOO graph with proper state schema
        graph = BaseGraph(name=f"{self.name}_rewoo_graph")

        # 1. PLANNING NODE - Forces ReWOO plan generation
        planning_node = EngineNodeConfig(
            name="planning", engine_name="planning"  # Use named engine
        )

        # 2. VALIDATION NODE - Controls tool routing based on plan
        from haive.core.graph.node.validation_node_config_v2 import (
            ValidationNodeConfigV2,
        )

        validation_node = ValidationNodeConfigV2(
            name="validation",
            engine_name="main",  # Use main engine
            tool_node="tool_execution",
            parser_node="plan_parser",
            available_nodes=["planning", "tool_execution", "plan_parser", "reasoning"],
        )

        # 3. TOOL EXECUTION NODE - Executes tools based on validation
        tool_node = ToolNodeConfig(
            name="tool_execution",
            engine_name="main",
            allowed_routes=["langchain_tool", "function", "pydantic_model"],
        )

        # 4. PLAN PARSER NODE - Parses plan from structured output
        from haive.core.graph.node.parser_node_config_v2 import ParserNodeConfigV2

        parser_node = ParserNodeConfigV2(name="plan_parser", engine_name="main")

        # 5. REASONING NODE - Final answer synthesis
        reasoning_node = EngineNodeConfig(
            name="reasoning", engine_name="reasoning"  # Use reasoning engine
        )

        # Add all nodes
        graph.add_node("planning", planning_node)
        graph.add_node("validation", validation_node)
        graph.add_node("tool_execution", tool_node)
        graph.add_node("plan_parser", parser_node)
        graph.add_node("reasoning", reasoning_node)

        # ReWOO Flow: Planning → Validation → [Tool Execution OR Parser] → Reasoning
        graph.add_edge(START, "planning")
        graph.add_edge("planning", "validation")

        # Validation controls routing to tool execution or parser
        # The validation node will use Command to route appropriately
        graph.add_edge("tool_execution", "reasoning")
        graph.add_edge("plan_parser", "reasoning")
        graph.add_edge("reasoning", END)

        return graph

    def create_runnable(self, runnable_config=None) -> Any:
        """Override to set available_tools in initial state."""
        # Set available tools in state without auto-sync
        if hasattr(self, "tools") and self.tools:
            # This will be used by ReWOOState.tool_options computed field
            pass
        else:
            pass

        # Create runnable with initial state
        runnable = super().create_runnable(runnable_config)

        return runnable


# Example usage
async def example_rewoo_agent():
    """Example of using ReWOO agent with controlled tool routing."""
    from haive.tools.tools.search_tools import tavily_qna, tavily_search_tool
    from haive.tools.tools.yfinance_tool import yfinance_news_tool

    # Create agent with tools
    agent = ReWOOAgent(
        name="rewoo_agent",
        engine=AugLLMConfig(name="rewoo_main_engine", temperature=0.7),
        tools=[tavily_search_tool, tavily_qna, yfinance_news_tool],
    )

    # Run agent - should create plan, execute tools, and reason
    await agent.arun("What is the current stock price of Apple and latest news?")

    # Check state for ReWOO plan
    if hasattr(agent, "state") and hasattr(agent.state, "current_plan"):
        pass


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_rewoo_agent())
