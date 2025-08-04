#!/usr/bin/env python3
"""
Sequential Self-Discover Pattern with AgentNodeV3

This example demonstrates how to create a sequential multi-agent workflow using
the Self-Discover methodology with AgentNodeV3 for proper state management.

The workflow follows this pattern:
1. Selector Agent: Selects relevant reasoning modules
2. Adapter Agent: Adapts modules to be task-specific
3. Structurer Agent: Creates step-by-step reasoning plan
4. Executor Agent: Executes the plan to solve the task

Each agent uses structured output and proper state transfer through AgentNodeV3.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Any
from typing import Dict

from haive.agents.simple.agent_v3 import SimpleAgentV3
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel
from pydantic import Field

# Configure logging for detailed debug output
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ==============================================================================
# Structured Output Models
# ==============================================================================


class ModuleSelectionOutput(BaseModel):
    """Output from the module selector agent."""

    selected_modules: str = Field(
        description="Selected reasoning modules formatted as numbered list"
    )


class AdaptedModulesOutput(BaseModel):
    """Output from the module adapter agent."""

    adapted_modules: str = Field(description="Task-specific adapted reasoning modules")


class ReasoningStructureOutput(BaseModel):
    """Output from the structure creator agent."""

    reasoning_structure: str = Field(
        description="Step-by-step reasoning plan using adapted modules"
    )


class FinalAnswerOutput(BaseModel):
    """Output from the executor agent."""

    final_answer: str = Field(description="The final answer to the task")


# ==============================================================================
# Self-Discover Agents
# ==============================================================================


class SelfDiscoverSelector(SimpleAgentV3):
    """Agent that selects relevant reasoning modules for a given task."""

    name: str = Field(default="selector")

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.3,
            max_tokens=1000,
            structured_output_model=ModuleSelectionOutput,
            system_message=(
                "You are an expert at selecting appropriate reasoning strategies. "
                "Given a list of reasoning modules and a task, select the 3-5 most "
                "relevant modules that would be helpful for solving the task."
            ),
        )
    )

    prompt_template: ChatPromptTemplate = Field(
        default_factory=lambda: ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an expert at selecting appropriate reasoning strategies. "
                        "Given a list of reasoning modules and a task, select the 3-5 most "
                        "relevant modules that would be helpful for solving the task."
                    ),
                ),
                ("human", "{messages}"),
            ]
        )
    )


class SelfDiscoverAdapter(SimpleAgentV3):
    """Agent that adapts selected modules to be task-specific."""

    name: str = Field(default="adapter")

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.5,
            max_tokens=1200,
            structured_output_model=AdaptedModulesOutput,
            system_message=(
                "You adapt general reasoning modules to be specific for a given task. "
                "Take the selected modules and modify them with concrete strategies "
                "that are tailored to solve the specific problem at hand."
            ),
        )
    )

    prompt_template: ChatPromptTemplate = Field(
        default_factory=lambda: ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You adapt general reasoning modules to be specific for a given task. "
                        "Take the selected modules and modify them with concrete strategies "
                        "that are tailored to solve the specific problem at hand."
                    ),
                ),
                ("human", "{messages}"),
            ]
        )
    )


class SelfDiscoverStructurer(SimpleAgentV3):
    """Agent that creates a structured reasoning plan."""

    name: str = Field(default="structurer")

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.3,
            max_tokens=1500,
            structured_output_model=ReasoningStructureOutput,
            system_message=(
                "You create detailed step-by-step reasoning plans. "
                "Take the adapted modules and organize them into a clear, "
                "sequential plan that can be followed to solve the task."
            ),
        )
    )

    prompt_template: ChatPromptTemplate = Field(
        default_factory=lambda: ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You create detailed step-by-step reasoning plans. "
                        "Take the adapted modules and organize them into a clear, "
                        "sequential plan that can be followed to solve the task."
                    ),
                ),
                ("human", "{messages}"),
            ]
        )
    )


class SelfDiscoverExecutor(SimpleAgentV3):
    """Agent that executes the reasoning plan to solve the task."""

    name: str = Field(default="executor")

    engine: AugLLMConfig = Field(
        default_factory=lambda: AugLLMConfig(
            temperature=0.7,
            max_tokens=2000,
            structured_output_model=FinalAnswerOutput,
            system_message=(
                "You execute reasoning plans to solve tasks step by step. "
                "Follow the provided reasoning structure carefully and work "
                "through each step to arrive at the final answer."
            ),
        )
    )

    prompt_template: ChatPromptTemplate = Field(
        default_factory=lambda: ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You execute reasoning plans to solve tasks step by step. "
                        "Follow the provided reasoning structure carefully and work "
                        "through each step to arrive at the final answer."
                    ),
                ),
                ("human", "{messages}"),
            ]
        )
    )


# ==============================================================================
# State Management
# ==============================================================================


class SelfDiscoverState:
    """State container for sequential Self-Discover workflow."""

    def __init__(self, initial_task: str, reasoning_modules: str):
        """Initialize state with task and available modules.

        Args:
            initial_task: The task to be solved
            reasoning_modules: Available reasoning modules as formatted string
        """
        # Initial messages with task and modules
        self.messages = [
            HumanMessage(
                content=f"""Available reasoning modules:
{reasoning_modules}

Task to solve:
{initial_task}

Select the most relevant modules for solving this task."""
            )
        ]

        # Agent states for tracking execution
        self.agent_states = {}

        # Agents dictionary (will be populated)
        self.agents = {}

        # Sequential outputs for data transfer
        self.selected_modules = None
        self.adapted_modules = None
        self.reasoning_structure = None
        self.final_answer = None

        # Store original task for reference
        self.original_task = initial_task
        self.reasoning_modules = reasoning_modules

    def update_for_next_agent(self, step: str, previous_output: str, next_prompt: str):
        """Update state for the next agent in sequence.

        Args:
            step: Current step name for logging
            previous_output: Output from previous agent
            next_prompt: Prompt template for next agent
        """
        logger.info(f"Updating state for step: {step}")
        logger.debug(f"Previous output: {previous_output[:100]}...")

        # Update messages for next agent
        self.messages = [HumanMessage(content=next_prompt)]
        logger.debug("Updated messages for next agent")


# ==============================================================================
# Default Reasoning Modules
# ==============================================================================

DEFAULT_REASONING_MODULES = """1. Pattern Recognition - Identify patterns, shapes, and structures in data
2. Spatial Analysis - Understand spatial relationships and geometric properties
3. Logical Reasoning - Apply logical thinking and deductive reasoning
4. Mathematical Analysis - Use mathematical concepts and calculations
5. Visual Interpretation - Interpret visual information and diagrams
6. Problem Decomposition - Break complex problems into manageable parts
7. Critical Thinking - Evaluate information and assess assumptions
8. Systems Thinking - Understand systems and relationships between components
9. Comparative Analysis - Compare and contrast different options or approaches
10. Hypothesis Testing - Form and test hypotheses systematically"""


# ==============================================================================
# Sequential Workflow Implementation
# ==============================================================================


def extract_structured_output_content(result: dict[str, Any], output_field: str) -> str:
    """Extract content from structured output result.

    Args:
        result: Result from agent execution
        output_field: Name of the output field to extract

    Returns:
        Extracted content as string
    """
    if not hasattr(result, "update") or not result.update:
        return str(result)

    output_data = result.update.get(output_field, {})

    # Handle different output formats
    if isinstance(output_data, dict):
        if "content" in output_data:
            content = output_data["content"]
            # Extract from validation message if needed
            if isinstance(content, str) and "Successfully validated" in content:
                # Parse the validation message format
                import re

                match = re.search(r"{'([^']+)':\s*'([^']*)'}", content)
                if match:
                    return match.group(2).replace("\\n", "\n")
            return str(content)
        return str(output_data)

    return str(output_data)


async def run_sequential_self_discover(
    task: str, reasoning_modules: str | None = None, debug: bool = True
) -> dict[str, Any]:
    """Run the complete sequential Self-Discover workflow.

    Args:
        task: The task to be solved
        reasoning_modules: Available reasoning modules (uses default if None)
        debug: Whether to enable debug output

    Returns:
        Dictionary containing the complete workflow results
    """
    if reasoning_modules is None:
        reasoning_modules = DEFAULT_REASONING_MODULES

    logger.info("=" * 80)
    logger.info("SEQUENTIAL SELF-DISCOVER WORKFLOW")
    logger.info("=" * 80)
    logger.info(f"Task: {task}")
    logger.info(f"Debug mode: {debug}")

    # Create agents with debug enabled
    logger.info("\n1. Creating Self-Discover agents...")

    selector = SelfDiscoverSelector()
    adapter = SelfDiscoverAdapter()
    structurer = SelfDiscoverStructurer()
    executor = SelfDiscoverExecutor()

    logger.info(f"   ✅ Created {selector.name}")
    logger.info(f"   ✅ Created {adapter.name}")
    logger.info(f"   ✅ Created {structurer.name}")
    logger.info(f"   ✅ Created {executor.name}")

    # Create state and add agents
    logger.info("\n2. Setting up workflow state...")
    state = SelfDiscoverState(task, reasoning_modules)
    state.agents = {
        "selector": selector,
        "adapter": adapter,
        "structurer": structurer,
        "executor": executor,
    }
    logger.info(f"   ✅ State initialized with {len(state.agents)} agents")

    # Create agent nodes
    logger.info("\n3. Creating AgentNodeV3 nodes...")
    selector_node = create_agent_node_v3("selector", selector, "selector_node")
    adapter_node = create_agent_node_v3("adapter", adapter, "adapter_node")
    structurer_node = create_agent_node_v3("structurer", structurer, "structurer_node")
    executor_node = create_agent_node_v3("executor", executor, "executor_node")

    logger.info("   ✅ Created all AgentNodeV3 nodes"s")

    results = {}

    try:
        # Step 1: Module Selection
        logger.info("\n" + "=" * 60)
        logger.info("STEP 1: MODULE SELECTION")
        logger.info("=" * 60)

        selector_result = selector_node(state)
        selected_modules = extract_structured_output_content(
            selector_result, "module_selection_output"
        )
        results["selected_modules"] = selected_modules

        logger.info(f"✅ Selected modules: {selected_modules}")

        # Update state for adapter
        state.update_for_next_agent(
            "adapter",
            selected_modules,
            f"""Task: {task}

Selected modules:
{selected_modules}

Adapt each selected module with specific strategies for solving this particular task.""",
        )

        # Step 2: Module Adaptation
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: MODULE ADAPTATION")
        logger.info("=" * 60)

        adapter_result = adapter_node(state)
        adapted_modules = extract_structured_output_content(
            adapter_result, "adapted_modules_output"
        )
        results["adapted_modules"] = adapted_modules

        logger.info(f"✅ Adapted modules: {adapted_modules[:100]}...")

        # Update state for structurer
        state.update_for_next_agent(
            "structurer",
            adapted_modules,
            f"""Task: {task}

Adapted modules:
{adapted_modules}

Create a step-by-step reasoning plan using these adapted modules.""",
        )

        # Step 3: Structure Creation
        logger.info("\n" + "=" * 60)
        logger.info("STEP 3: STRUCTURE CREATION")
        logger.info("=" * 60)

        structurer_result = structurer_node(state)
        reasoning_structure = extract_structured_output_content(
            structurer_result, "reasoning_structure_output"
        )
        results["reasoning_structure"] = reasoning_structure

        logger.info(f"✅ Reasoning structure: {reasoning_structure[:100]}...")

        # Update state for executor
        state.update_for_next_agent(
            "executor",
            reasoning_structure,
            f"""Task: {task}

Reasoning plan:
{reasoning_structure}

Execute this plan step by step to solve the task.""",
        )

        # Step 4: Plan Execution
        logger.info("\n" + "=" * 60)
        logger.info("STEP 4: PLAN EXECUTION")
        logger.info("=" * 60)

        executor_result = executor_node(state)
        final_answer = extract_structured_output_content(
            executor_result, "final_answer_output"
        )
        results["final_answer"] = final_answer

        logger.info(f"✅ Final answer: {final_answer}")

        # Complete workflow results
        results.update(
            {"success": True, "original_task": task, "workflow_completed": True}
        )

        logger.info("\n" + "=" * 80)
        logger.info("SEQUENTIAL SELF-DISCOVER WORKFLOW COMPLETED")
        logger.info("=" * 80)

        return results

    except Exception as e:
        logger.exception(f"❌ Workflow failed: {e}")
        import traceback

        traceback.print_exc()

        results.update({"success": False, "error": str(e), "workflow_completed": False})
        return results


# ==============================================================================
# Example Usage
# ==============================================================================


async def main():
    """Run example Self-Discover workflows with different tasks."""

    print("🚀 Self-Discover Sequential Workflow Examples")
    print("=" * 80)

    # Example 1: SVG Path Analysis
    print("\n📊 Example 1: SVG Path Analysis")
    print("-" * 50)

    svg_task = """Analyze this SVG path and determine what shape it draws:
<path d="M 10,10 L 40,10 L 40,40 L 10,40 Z"/>

The path uses these commands:
- M 10,10 (Move to point 10,10)
- L 40,10 (Line to point 40,10)
- L 40,40 (Line to point 40,40)
- L 10,40 (Line to point 10,40)
- Z (Close path back to start)

Options: circle, triangle, square, pentagon, hexagon"""

    svg_results = await run_sequential_self_discover(svg_task, debug=True)

    print("\n🎯 SVG Analysis Results:"s:")
    print(f"Final Answer: {svg_results.get('final_answer', 'No answer')}")
    print(f"Success: {svg_results.get('success', False)}")

    # Example 2: Problem Solving
    print("\n\n🧠 Example 2: Remote Work Productivity")
    print("-" * 50)

    productivity_task = "How can I improve team productivity in a remote work environment? Provide specific, actionable strategies."

    productivity_results = await run_sequential_self_discover(
        productivity_task, debug=True
    )

    print("\n🎯 Productivity Analysis Results:"s:")
    print(
        f"Final Answer: {productivity_results.get('final_answer', 'No answer')[:200]}..."
    )
    print(f"Success: {productivity_results.get('success', False)}")

    print("\n" + "=" * 80)
    print("🏁 All examples completed!")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
