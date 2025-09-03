"""Basic Sequential Multi-Agent Example.

This example demonstrates a simple sequential workflow where:
1. Planner agent creates a plan
2. Executor agent executes the plan
3. Reviewer agent reviews the execution

The agents communicate through direct field updates in the shared state.
"""

from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.node.agent_node_v3 import create_agent_node_v3
from haive.core.schema.prebuilt.multi_agent_state import MultiAgentState


# Define structured outputs for each agent
class PlanningResult(BaseModel):
    """Output from the planning agent."""

    plan: list[str] = Field(description="List of planned steps")
    priority: str = Field(description="Priority level (high, medium, low)")
    estimated_time: int = Field(description="Estimated time in minutes")
    resources_needed: list[str] = Field(description="Required resources")


class ExecutionResult(BaseModel):
    """Output from the execution agent."""

    execution_status: str = Field(description="Status of execution")
    completed_steps: list[str] = Field(description="Steps that were completed")
    remaining_steps: list[str] = Field(description="Steps still to do")
    execution_notes: str = Field(description="Notes about execution")


class ReviewResult(BaseModel):
    """Output from the review agent."""

    review_score: float = Field(ge=0.0, le=10.0, description="Quality score (0-10)")
    strengths: list[str] = Field(description="Identified strengths")
    improvements: list[str] = Field(description="Suggested improvements")
    final_recommendation: str = Field(description="Overall recommendation")


# Define custom state schema with all required fields
class WorkflowState(MultiAgentState):
    """State schema for the sequential workflow."""

    # Input fields
    task_description: str = ""
    deadline: str = ""

    # Planning agent outputs
    plan: list[str] = Field(default_factory=list)
    priority: str = ""
    estimated_time: int = 0
    resources_needed: list[str] = Field(default_factory=list)

    # Execution agent outputs
    execution_status: str = ""
    completed_steps: list[str] = Field(default_factory=list)
    remaining_steps: list[str] = Field(default_factory=list)
    execution_notes: str = ""

    # Review agent outputs
    review_score: float = 0.0
    strengths: list[str] = Field(default_factory=list)
    improvements: list[str] = Field(default_factory=list)
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
    """Run the complete sequential workflow.

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

    # Step 1: Planning
    plan_node(state, config)

    # Step 2: Execution
    exec_node(state, config)

    # Step 3: Review
    review_node(state, config)

    return state


if __name__ == "__main__":
    # Example usage
    result = run_sequential_workflow(
        task_description="Develop a new customer onboarding process",
        deadline="2 weeks",
    )

    # Compare with traditional approach
