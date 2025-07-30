"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    ReasoningSystemState: ReasoningSystemState implementation.
    ReasoningSystem: ReasoningSystem implementation.

Functions:
    setup_agent: Setup Agent functionality.
    build_graph: Build Graph functionality.
    should_explore_alternatives: Should Explore Alternatives functionality.
"""

# src/haive/agents/reasoning/orchestrator.py

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import BaseMessage
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.reasoning_and_critique.logic.engines import (
    Dict,
    create_bias_detector,
    create_logical_reasoner,
    create_premise_extractor,
    create_synthesis_agent,
    create_uncertainty_analyzer,
)
from haive.agents.reasoning_and_critique.logic.models import (
    Evidence,
    ReasoningAnalysis,
    ReasoningChain,
    ReasoningReport,
)


# Define the actual state we want
class ReasoningSystemState(StateSchema):
    """State for the reasoning system."""

    # Input fields
    messages: list[BaseMessage] = Field(default_factory=list)
    question: str = Field(description="Question to reason about")
    context: dict[str, Any] = Field(default_factory=dict)
    evidence: list[Evidence] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    reasoning_depth: int = Field(default=3)
    explore_alternatives: bool = Field(default=True)

    # Working fields
    initial_premises: ReasoningChain | None = None
    primary_reasoning: ReasoningChain | None = None
    alternative_reasoning: list[ReasoningChain] | None = None
    bias_analysis: ReasoningAnalysis | None = None
    uncertainty_analysis: Any | None = None

    # Output
    final_report: ReasoningReport | None = None


class ReasoningSystem(Agent):
    """Orchestrator agent for comprehensive reasoning analysis."""

    # Explicitly set our state schema
    state_schema: Any = Field(default=ReasoningSystemState)

    # Define engines
    premise_extractor: AugLLMConfig = Field(default_factory=create_premise_extractor)
    logical_reasoner: AugLLMConfig = Field(default_factory=create_logical_reasoner)
    bias_detector: AugLLMConfig = Field(default_factory=create_bias_detector)
    uncertainty_analyzer: AugLLMConfig = Field(
        default_factory=create_uncertainty_analyzer
    )
    synthesizer: AugLLMConfig = Field(default_factory=create_synthesis_agent)

    def setup_agent(self) -> None:
        """Sync engines to the engines dict."""
        self.engines = {
            "premise_extractor": self.premise_extractor,
            "logical_reasoner": self.logical_reasoner,
            "bias_detector": self.bias_detector,
            "uncertainty_analyzer": self.uncertainty_analyzer,
            "synthesizer": self.synthesizer,
        }

        # Don't auto-generate schema - we defined it explicitly
        self.set_schema = False

        super().setup_agent()

    def build_graph(self) -> BaseGraph:
        """Build the reasoning analysis workflow graph."""
        graph = BaseGraph(name="reasoning_system")

        # Add all nodes
        graph.add_node("extract_premises", self.premise_extractor)
        graph.add_node("primary_reasoning", self.logical_reasoner)
        graph.add_node("alternative_reasoning", self.logical_reasoner)
        graph.add_node("analyze_biases", self.bias_detector)
        graph.add_node("analyze_uncertainty", self.uncertainty_analyzer)
        graph.add_node("synthesize", self.synthesizer)

        # Add edges
        graph.add_edge(START, "extract_premises")
        graph.add_edge("extract_premises", "primary_reasoning")

        # Conditional edge
        def should_explore_alternatives(state: Dict[str, Any]):
            return state.explore_alternatives

        graph.add_conditional_edges(
            "primary_reasoning",
            should_explore_alternatives,
            {True: "alternative_reasoning", False: "analyze_biases"},
        )

        graph.add_edge("alternative_reasoning", "analyze_biases")
        graph.add_edge("analyze_biases", "analyze_uncertainty")
        graph.add_edge("analyze_uncertainty", "synthesize")
        graph.add_edge("synthesize", END)

        return graph
