"""
Basic Sequential Multi-Agent Example

This example demonstrates a simple sequential workflow where:
1. Planner agent creates a plan
2. Executor agent executes the plan
3. Reviewer agent reviews the execution

The agents communicate through direct field updates in the shared state.
"""

from typing import Any, Dict, List

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState
from pydantic import BaseModel, Field


# Define structured outputs for each agent
class PlanningResult(BaseModel):
    """Output from the planning agent."""

    plan: List[str] = Field(description="List of planned steps")
    priority: str = Field(description="Priority level (high, medium, low)")
    estimated_time: int = Field(description="Estimated time in minutes")
    resources_needed: List[str] = Field(description="Required resources")


class ExecutionResult(BaseModel):
    """Output from the execution agent."""

    execution_status: str = Field(description="Status of execution")
    completed_steps: List[str] = Field(description="Steps that were completed")
    remaining_steps: List[str] = Field(description="Steps still to do")
    execution_notes: str = Field(description="Notes about execution")


class ReviewResult(BaseModel):
    """Output from the review agent."""

    review_score: float = Field(ge=0.0, le=10.0, description="Quality score (0-10)")
    strengths: List[str] = Field(description="Identified strengths")
    improvements: List[str] = Field(description="Suggested improvements")
    final_recommendation: str = Field(description="Overall recommendation")


# Define custom state schema with all required fields
class WorkflowState(MultiAgentState):
    """State schema for the sequential workflow."""

    # Input fields
    task_description: str = ""
    deadline: str = ""

    # Planning agent outputs
    plan: List[str] = Field(default_factory=list)
    priority: str = ""
    estimated_time: int = 0
    resources_needed: List[str] = Field(default_factory=list)

    # Execution agent outputs
    execution_status: str = ""
    completed_steps: List[str] = Field(default_factory=list)
    remaining_steps: List[str] = Field(default_factory=list)
    execution_notes: str = ""

    # Review agent outputs
    review_score: float = 0.0
    strengths: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    final_recommendation: str = ""


def create_workflow_agents():
    """Create the three agents for the workflow."""

    # Planning agent
    planner = SimpleAgent(
        name="planner",
        engine=AugLLMConfig(
            temperature=0.3,
            system_message="""You are a strategic planning agent.
            Create detailed, actionable plans for tasks.
            Consider timeline, resources, and priorities.
            Be specific and realistic in your planning.""",
        ),
        structured_output_model=PlanningResult,
    )

    # Execution agent
    executor = SimpleAgent(
        name="executor",
        engine=AugLLMConfig(
            temperature=0.5,
            system_message="""You are an execution agent.
            Review the plan and simulate execution.
            Identify what steps would be completed and any challenges.
            Provide realistic status updates.""",
        ),
        structured_output_model=ExecutionResult,
    )

    # Review agent
    reviewer = SimpleAgent(
        name="reviewer",
        engine=AugLLMConfig(
            temperature=0.4,
            system_message="""You are a quality review agent.
            Evaluate the planning and execution process.
            Provide constructive feedback and scores.
            Focus on improvement opportunities.""",
        ),
        structured_output_model=ReviewResult,
    )

    return planner, executor, reviewer


def run_sequential_workflow(task_description: str, deadline: str = "1 week"):
    """
    Run the complete sequential workflow.

    Args:
        task_description: The task to plan and execute
        deadline: When the task should be completed

    Returns:
        Final state with all results
    """

    # Create agents
    planner, executor, reviewer = create_workflow_agents()

    # Initialize state
    state = WorkflowState(
        agents=[planner, executor, reviewer],
        task_description=task_description,
        deadline=deadline,
    )

    # Create agent nodes
    plan_node = create_agent_node_v3("planner")
    exec_node = create_agent_node_v3("executor")
    review_node = create_agent_node_v3("reviewer")

    # Basic config
    config = {"configurable": {"thread_id": "workflow_1"}}

    print("🔄 Starting Sequential Workflow")
    print(f"Task: {task_description}")
    print(f"Deadline: {deadline}")
    print("-" * 50)

    # Step 1: Planning
    print("📋 Step 1: Planning...")
    result1 = plan_node(state, config)
    print(f"✅ Plan created: {len(state.plan)} steps")
    print(f"   Priority: {state.priority}")
    print(f"   Estimated time: {state.estimated_time} minutes")

    # Step 2: Execution
    print("\n⚡ Step 2: Execution...")
    result2 = exec_node(state, config)
    print(f"✅ Execution status: {state.execution_status}")
    print(f"   Completed: {len(state.completed_steps)} steps")
    print(f"   Remaining: {len(state.remaining_steps)} steps")

    # Step 3: Review
    print("\n🔍 Step 3: Review...")
    result3 = review_node(state, config)
    print(f"✅ Review score: {state.review_score}/10")
    print(f"   Strengths: {len(state.strengths)}")
    print(f"   Improvements: {len(state.improvements)}")

    print("\n" + "=" * 50)
    print("🎯 Final Results:")
    print(f"Plan: {state.plan}")
    print(f"Execution Status: {state.execution_status}")
    print(f"Review Score: {state.review_score}/10")
    print(f"Final Recommendation: {state.final_recommendation}")

    return state


if __name__ == "__main__":
    # Example usage
    result = run_sequential_workflow(
        task_description="Develop a new customer onboarding process", deadline="2 weeks"
    )

    print("\n" + "=" * 50)
    print("🔍 State Field Access Examples:")
    print(f"Direct field access - Plan: {result.plan}")
    print(f"Direct field access - Priority: {result.priority}")
    print(f"Direct field access - Review Score: {result.review_score}")

    # Compare with traditional approach
    print("\n🔄 Traditional vs Haive Approach:")
    print("Traditional (complex):")
    print(f"  plan = state.agent_outputs['planner']['plan']")
    print("Haive (direct):")
    print(f"  plan = state.plan  # {result.plan}")
