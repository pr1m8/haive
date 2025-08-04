"""Self-Discover Multi-Agent Example.

This example demonstrates the Self-Discover reasoning pattern where:
1. Selector agent selects relevant reasoning modules
2. Adapter agent adapts modules to the specific task
3. Reasoner agent creates a reasoning structure

Each agent builds on the previous agent's output through direct field access.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState


# Define structured outputs for each agent
class SelectedModules(BaseModel):
    """Output from the module selection agent."""

    selected_modules: list[str] = Field(
        description="Selected reasoning modules")
    rationale: str = Field(description="Why these modules were selected")
    confidence: float = Field(ge=0.0,
                              le=1.0,
                              description="Confidence in selection")


class AdaptedModules(BaseModel):
    """Output from the module adaptation agent."""

    adapted_modules: list[dict[str, str]] = Field(
        description="Modules adapted for the task", )
    task_context: str = Field(description="Context of the task")
    adaptation_notes: str = Field(description="Notes about adaptations made")


class ReasoningStructure(BaseModel):
    """Output from the reasoning structure agent."""

    reasoning_structure: dict[str, Any] = Field(
        description="Complete reasoning structure", )
    steps: list[str] = Field(description="Reasoning steps")
    methodology: str = Field(description="Overall methodology")
    expected_outcome: str = Field(description="What outcome is expected")


# Define custom state schema with all required fields
class SelfDiscoverState(MultiAgentState):
    """State schema for the Self-Discover workflow."""

    # Input fields
    task_description: str = ""
    available_modules: list[str] = Field(default_factory=list)
    complexity_level: str = ""

    # Selector agent outputs
    selected_modules: list[str] = Field(default_factory=list)
    rationale: str = ""
    confidence: float = 0.0

    # Adapter agent outputs
    adapted_modules: list[dict[str, str]] = Field(default_factory=list)
    task_context: str = ""
    adaptation_notes: str = ""

    # Reasoner agent outputs
    reasoning_structure: dict[str, Any] = Field(default_factory=dict)
    steps: list[str] = Field(default_factory=list)
    methodology: str = ""
    expected_outcome: str = ""


def create_self_discover_agents():
    """Create the three agents for the Self-Discover workflow."""
    # Module selector agent
    selector = SimpleAgent(
        name="selector",
        engine=AugLLMConfig(
            temperature=0.2,
            system_message="""You are a reasoning module selector.

            Your job is to select the most relevant reasoning modules
            for a given task from the available options.

            Consider:
            - Task complexity and domain
            - Module complementarity
            - Effectiveness for the specific problem type

            Be selective - choose 3-5 modules that work well together.""",
        ),
        structured_output_model=SelectedModules,
    )

    # Module adapter agent
    adapter = SimpleAgent(
        name="adapter",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="""You are a reasoning module adapter.

            Take the selected modules and adapt them specifically
            for the given task context.

            For each module:
            - Explain how it applies to this specific task
            - Provide concrete examples
            - Suggest modifications if needed

            Make the modules actionable and task-specific.""",
        ),
        structured_output_model=AdaptedModules,
    )

    # Reasoning structure agent
    reasoner = SimpleAgent(
        name="reasoner",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="""You are a reasoning structure creator.

            Take the adapted modules and create a comprehensive
            reasoning structure that combines them effectively.

            Create:
            - A step-by-step reasoning process
            - Clear methodology
            - Integration between modules
            - Expected outcomes

            Make it practical and executable.""",
        ),
        structured_output_model=ReasoningStructure,
    )

    return selector, adapter, reasoner


def run_self_discover_workflow(
    task_description: str,
    available_modules: list[str],
    complexity_level: str = "medium",
):
    """Run the complete Self-Discover workflow.

    Args:
        task_description: The task to create reasoning for
        available_modules: List of available reasoning modules
        complexity_level: Task complexity (low, medium, high)

    Returns:
        Final state with complete reasoning structure
    """
    # Create agents
    selector, adapter, reasoner = create_self_discover_agents()

    # Initialize state
    state = SelfDiscoverState(
        agents=[selector, adapter, reasoner],
        task_description=task_description,
        available_modules=available_modules,
        complexity_level=complexity_level,
    )

    # Create agent nodes
    selector_node = create_agent_node_v3("selector")
    adapter_node = create_agent_node_v3("adapter")
    reasoner_node = create_agent_node_v3("reasoner")

    # Basic config
    config = {"configurable": {"thread_id": "self_discover_1"}}

    # Step 1: Module Selection
    selector_node(state, config)
    for _module in state.selected_modules:
        pass

    # Step 2: Module Adaptation
    adapter_node(state, config)
    for _module in state.adapted_modules:
        pass

    # Step 3: Reasoning Structure Creation
    reasoner_node(state, config)

    return state


def demonstrate_field_access(state: SelfDiscoverState):
    """Demonstrate how agents access each other's outputs directly."""
    # Show how each agent can access previous outputs


if __name__ == "__main__":
    # Example reasoning modules
    reasoning_modules = [
        "systems_thinking",
        "root_cause_analysis",
        "cost_benefit_analysis",
        "stakeholder_analysis",
        "risk_assessment",
        "solution_design",
        "implementation_planning",
        "feedback_loops",
        "constraint_analysis",
        "decision_trees",
    ]

    # Example usage
    result = run_self_discover_workflow(
        task_description="How can we reduce plastic waste in oceans?",
        available_modules=reasoning_modules,
        complexity_level="high",
    )

    # Demonstrate field access
    demonstrate_field_access(result)
