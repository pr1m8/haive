"""Self-Discover Agent using the unified MultiAgent implementation.

This implementation demonstrates how to use the new MultiAgent class to create
a sophisticated reasoning system that follows the Self-Discover methodology:
1. Select relevant reasoning modules
2. Adapt modules to the specific task
3. Structure a step-by-step plan
4. Execute the reasoning plan

This showcases sequential execution with the unified MultiAgent.
"""

import asyncio
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema import StateSchema
from langchain_core.prompts import PromptTemplate
from pydantic import Field

from haive.agents.multi.clean import MultiAgent
from haive.agents.reasoning_and_critique.self_discover.models import (
    AdaptedModule,
    ReasoningStructure,
    SelectedModule,
)
from haive.agents.simple import SimpleAgent


# State schema for self-discover workflow
class SelfDiscoverMultiAgentState(StateSchema):
    """State schema for the Self-Discover multi-agent workflow."""

    # Input
    task_description: str = Field(default="", description="The task to solve")
    reasoning_modules: list[str] = Field(
        default_factory=list, description="Available reasoning modules"
    )

    # Intermediate results
    selected_modules: list[SelectedModule] | None = Field(
        default=None, description="Modules selected for this task"
    )
    adapted_modules: list[AdaptedModule] | None = Field(
        default=None, description="Task-specific adapted modules"
    )
    reasoning_structure: ReasoningStructure | None = Field(
        default=None, description="Step-by-step reasoning plan"
    )

    # Final output
    reasoning_results: dict[str, str] = Field(
        default_factory=dict, description="Results from executing each reasoning step"
    )
    final_answer: str | None = Field(
        default=None, description="Final answer to the task"
    )


def get_default_reasoning_modules() -> list[str]:
    """Get the default set of reasoning modules."""
    return [
        "1. How could I devise an experiment to help solve that problem?",
        "2. Make a list of ideas for solving this problem, and apply them one by one.",
        "3. How could I measure progress on this problem?",
        "4. How can I simplify the problem so that it is easier to solve?",
        "5. What are the key assumptions underlying this problem?",
        "6. What are the potential risks and drawbacks of each solution?",
        "7. What are the alternative perspectives or viewpoints on this problem?",
        "8. What are the long-term implications of this problem and its solutions?",
        "9. How can I break down this problem into smaller, more manageable parts?",
        "10. Critical Thinking: Analyze from different perspectives, question assumptions.",
        "11. Try creative thinking, generate innovative and out-of-the-box ideas.",
        "12. Seek input and collaboration from others to solve the problem.",
        "13. Use systems thinking: Consider the problem as part of a larger system.",
        "14. Use Risk Analysis: Evaluate potential risks and tradeoffs.",
        "15. Use Reflective Thinking: Step back for introspection and self-reflection.",
        "16. What is the core issue or problem that needs to be addressed?",
        "17. What are the underlying causes or factors contributing to the problem?",
        "18. Are there any potential solutions that have been tried before?",
        "19. What are the potential obstacles or challenges in solving this problem?",
        "20. Are there any relevant data that can provide insights into the problem?",
        "21. Let's make a step by step plan and implement it with good explanation.",
    ]


def create_selector_agent() -> SimpleAgent:
    """Create the module selector agent."""
    select_prompt = PromptTemplate(
        template="""Select several reasoning modules that are crucial to solve the given task.

Available reasoning modules:
{reasoning_modules}

Task: {task_description}

Select 3-5 modules that are most relevant for solving this task. For each selected module:
- Identify the module by its number and brief description
- Explain why this module is relevant for the task

Return your selection in a clear, structured format.
"""
    )

    config = AugLLMConfig(
        temperature=0.1,
        system_message="You are an expert at analyzing problems and selecting appropriate reasoning strategies.",
        prompt_template=select_prompt,
    )

    return SimpleAgent(name="selector", engine=config)


def create_adapter_agent() -> SimpleAgent:
    """Create the module adapter agent."""
    adapt_prompt = PromptTemplate(
        template="""Adapt the selected reasoning modules to be more specific to the task at hand.

Selected modules:
{selected_modules}

Task: {task_description}

For each selected module, provide a task-specific adaptation that:
- Maintains the core reasoning approach
- Applies it specifically to this task
- Provides concrete guidance on how to use it

Return the adapted modules in a clear, structured format.
"""
    )

    config = AugLLMConfig(
        temperature=0.3,
        system_message="You are an expert at customizing reasoning strategies for specific problems.",
        prompt_template=adapt_prompt,
    )

    return SimpleAgent(name="adapter", engine=config)


def create_structurer_agent() -> SimpleAgent:
    """Create the reasoning structure agent."""
    structure_prompt = PromptTemplate(
        template="""Create a step-by-step reasoning plan using the adapted modules.

Adapted modules:
{adapted_modules}

Task: {task_description}

Create a structured plan that:
- Breaks down the problem into clear steps
- Assigns relevant adapted modules to each step
- Ensures logical flow from start to finish
- Leads to a complete solution

Format the plan as a numbered list of steps, each with:
- Step description
- Which adapted modules to apply
- Expected outcome

Note: Create the PLAN only, do not solve the problem yet.
"""
    )

    config = AugLLMConfig(
        temperature=0.2,
        system_message="You are an expert at creating structured problem-solving plans.",
        prompt_template=structure_prompt,
    )

    return SimpleAgent(name="structurer", engine=config)


def create_reasoner_agent() -> SimpleAgent:
    """Create the reasoning execution agent."""
    reasoning_prompt = PromptTemplate(
        template="""Execute the reasoning plan to solve the task.

Task: {task_description}

Reasoning Plan:
{reasoning_structure}

Previous reasoning results:
{reasoning_results}

Follow the plan step by step:
- Apply the specified reasoning modules
- Build on previous results
- Work toward the final answer

Provide detailed reasoning for each step and conclude with the final answer.
"""
    )

    config = AugLLMConfig(
        temperature=0.1,
        system_message="You are an expert problem solver who follows structured reasoning plans.",
        prompt_template=reasoning_prompt,
    )

    return SimpleAgent(name="reasoner", engine=config)


def create_self_discover_multiagent(
    name: str = "self_discover_system", reasoning_modules: list[str] | None = None
) -> MultiAgent:
    """Create a Self-Discover system using MultiAgent.

    This demonstrates sequential execution with the unified MultiAgent implementation.

    Args:
        name: Name for the multi-agent system
        reasoning_modules: Optional custom reasoning modules

    Returns:
        MultiAgent configured for Self-Discover workflow
    """
    # Create the agents for each stage
    selector = create_selector_agent()
    adapter = create_adapter_agent()
    structurer = create_structurer_agent()
    reasoner = create_reasoner_agent()

    # Create the multi-agent with sequential execution
    # The list order defines the execution sequence
    multi_agent = MultiAgent(
        name=name,
        agents=[selector, adapter, structurer, reasoner],
        state_schema=SelfDiscoverMultiAgentState,
        execution_mode="sequential",  # Explicit sequential mode
    )

    # No need for routing configuration - sequential execution is automatic
    # The agents will execute in order: selector → adapter → structurer → reasoner

    return multi_agent


async def run_self_discover_example():
    """Run an example of the Self-Discover multi-agent system."""
    # Create the system
    self_discover = create_self_discover_multiagent()

    # Example task (same as original)
    task = """This SVG path element <path d="M 55.57,80.69 L 57.38,65.80 M 57.38,65.80 L 48.90,57.46 M 48.90,57.46 L
45.58,47.78 M 45.58,47.78 L 53.25,36.07 L 66.29,48.90 L 78.69,61.09 L 55.57,80.69"/> draws a:
(A) circle (B) heptagon (C) hexagon (D) kite (E) line (F) octagon (G) pentagon(H) rectangle (I) sector (J) triangle"""

    # Prepare the initial state
    initial_state = {
        "task_description": task,
        "reasoning_modules": get_default_reasoning_modules(),
    }

    # Run the multi-agent system
    result = await self_discover.arun(initial_state)

    return result


# Alternative: Create with custom routing for more control
def create_self_discover_with_conditional_routing() -> MultiAgent:
    """Create Self-Discover with conditional routing for demonstration.

    This shows how you could add conditional logic if needed, though
    sequential execution is sufficient for Self-Discover.
    """
    # Create agents
    selector = create_selector_agent()
    adapter = create_adapter_agent()
    structurer = create_structurer_agent()
    reasoner = create_reasoner_agent()
    error_handler = SimpleAgent(
        name="error_handler",
        engine=AugLLMConfig(
            system_message="You handle errors and provide helpful feedback."
        ),
    )

    # Create multi-agent with entry point
    multi_agent = MultiAgent(
        name="self_discover_conditional",
        agents=[selector, adapter, structurer, reasoner, error_handler],
        state_schema=SelfDiscoverMultiAgentState,
        entry_point="selector",
    )

    # Add direct edges for main flow
    multi_agent.add_edge("selector", "adapter")
    multi_agent.add_edge("adapter", "structurer")
    multi_agent.add_edge("structurer", "reasoner")

    # Add conditional routing for error handling
    def check_for_errors(state: dict[str, Any]) -> str:
        """Route to error handler if any stage fails."""
        if state.get("error"):
            return "error"
        return "continue"

    # Could add error checking after each stage
    multi_agent.add_conditional_routing(
        "reasonef", check_for_errors, {"error": "error_handler", "continue": "__end__"}
    )

    return multi_agent


if __name__ == "__main__":
    # Run the example
    asyncio.run(run_self_discover_example())
