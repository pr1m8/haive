"""
Self-Discover Multi-Agent Example

This example demonstrates the Self-Discover reasoning pattern where:
1. Selector agent selects relevant reasoning modules
2. Adapter agent adapts modules to the specific task
3. Reasoner agent creates a reasoning structure

Each agent builds on the previous agent's output through direct field access.
"""

from typing import Any, Dict, List

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from pydantic import BaseModel, Field


# Define structured outputs for each agent
class SelectedModules(BaseModel):
    """Output from the module selection agent."""

    selected_modules: List[str] = Field(description="Selected reasoning modules")
    rationale: str = Field(description="Why these modules were selected")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in selection")


class AdaptedModules(BaseModel):
    """Output from the module adaptation agent."""

    adapted_modules: List[Dict[str, str]] = Field(
        description="Modules adapted for the task"
    )
    task_context: str = Field(description="Context of the task")
    adaptation_notes: str = Field(description="Notes about adaptations made")


class ReasoningStructure(BaseModel):
    """Output from the reasoning structure agent."""

    reasoning_structure: Dict[str, Any] = Field(
        description="Complete reasoning structure"
    )
    steps: List[str] = Field(description="Reasoning steps")
    methodology: str = Field(description="Overall methodology")
    expected_outcome: str = Field(description="What outcome is expected")


# Define custom state schema with all required fields
class SelfDiscoverState(MultiAgentState):
    """State schema for the Self-Discover workflow."""

    # Input fields
    task_description: str = ""
    available_modules: List[str] = Field(default_factory=list)
    complexity_level: str = ""

    # Selector agent outputs
    selected_modules: List[str] = Field(default_factory=list)
    rationale: str = ""
    confidence: float = 0.0

    # Adapter agent outputs
    adapted_modules: List[Dict[str, str]] = Field(default_factory=list)
    task_context: str = ""
    adaptation_notes: str = ""

    # Reasoner agent outputs
    reasoning_structure: Dict[str, Any] = Field(default_factory=dict)
    steps: List[str] = Field(default_factory=list)
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
    available_modules: List[str],
    complexity_level: str = "medium",
):
    """
    Run the complete Self-Discover workflow.

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

    print("🧠 Starting Self-Discover Workflow")
    print(f"Task: {task_description}")
    print(f"Available modules: {len(available_modules)}")
    print(f"Complexity: {complexity_level}")
    print("-" * 60)

    # Step 1: Module Selection
    print("🎯 Step 1: Module Selection...")
    result1 = selector_node(state, config)
    print(f"✅ Selected {len(state.selected_modules)} modules:")
    for module in state.selected_modules:
        print(f"   - {module}")
    print(f"   Confidence: {state.confidence:.2f}")

    # Step 2: Module Adaptation
    print(f"\n🔧 Step 2: Module Adaptation...")
    result2 = adapter_node(state, config)
    print(f"✅ Adapted {len(state.adapted_modules)} modules:")
    for module in state.adapted_modules:
        print(
            f"   - {module.get('name', 'Unknown')}: {module.get('description', 'No description')}"
        )
    print(f"   Task context: {state.task_context}")

    # Step 3: Reasoning Structure Creation
    print(f"\n🏗️ Step 3: Reasoning Structure Creation...")
    result3 = reasoner_node(state, config)
    print(f"✅ Created reasoning structure with {len(state.steps)} steps")
    print(f"   Methodology: {state.methodology}")
    print(f"   Expected outcome: {state.expected_outcome}")

    print("\n" + "=" * 60)
    print("🎯 Final Reasoning Structure:")
    print(f"Selected Modules: {state.selected_modules}")
    print(f"Reasoning Steps: {state.steps}")
    print(f"Methodology: {state.methodology}")
    print(f"Expected Outcome: {state.expected_outcome}")

    return state


def demonstrate_field_access(state: SelfDiscoverState):
    """Demonstrate how agents access each other's outputs directly."""

    print("\n" + "=" * 60)
    print("🔍 Direct Field Access Examples:")

    # Show how each agent can access previous outputs
    print("\n1. Selector → Adapter communication:")
    print(f"   Selected modules: {state.selected_modules}")
    print(f"   Rationale: {state.rationale}")
    print(f"   Confidence: {state.confidence}")

    print("\n2. Adapter → Reasoner communication:")
    print(f"   Adapted modules: {len(state.adapted_modules)} modules")
    print(f"   Task context: {state.task_context}")
    print(f"   Adaptation notes: {state.adaptation_notes}")

    print("\n3. Final reasoning structure:")
    print(f"   Steps: {len(state.steps)} reasoning steps")
    print(f"   Methodology: {state.methodology}")
    print(f"   Expected outcome: {state.expected_outcome}")

    print("\n🔄 This demonstrates the Self-Discover pattern:")
    print("   - Each agent builds on previous outputs")
    print("   - Direct field access (no complex nested structures)")
    print("   - Type-safe state management")
    print("   - Clean agent communication")


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

    print("\n" + "=" * 60)
    print("🎯 Key Benefits of This Pattern:")
    print("1. Sequential reasoning with progressive refinement")
    print("2. Each agent specializes in one aspect")
    print("3. Direct field access for clean communication")
    print("4. Type-safe state management")
    print("5. Extensible - can add more reasoning agents")
