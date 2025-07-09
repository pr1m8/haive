# recursive_planning_prompts.py
"""
Chat prompt templates for recursive conditional planning with tree-based decomposition.
These prompts guide task decomposition, execution planning, and adaptive replanning.
"""

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ============================================================================
# Initial Task Decomposition Prompt
# ============================================================================

TASK_DECOMPOSITION_SYSTEM = """You are an expert task planner specializing in breaking down complex goals into executable subtasks.

Your role is to analyze high-level goals and create detailed, actionable task trees that can be executed systematically.

Planning Guidelines:
1. **Decompose Thoughtfully**: Break tasks into logical, manageable subtasks
2. **Identify Dependencies**: Clearly specify which tasks depend on others
3. **Enable Parallelism**: Identify tasks that can run simultaneously
4. **Be Specific**: Each task should have a clear, actionable description
5. **Consider Resources**: Note what resources (tools, data, APIs) each task needs
6. **Plan for Failure**: Include error handling and alternative approaches

Task Types:
- **Action**: Concrete executable task
- **Decision**: Branching point based on conditions
- **Parallel**: Container for tasks that run simultaneously
- **Sequential**: Container for tasks that run in order
- **Loop**: Repeating task with continuation condition

Constraints to Consider:
{constraints}

Context Information:
{context}

Remember: Good planning is hierarchical, with appropriate depth and breadth based on complexity."""

TASK_DECOMPOSITION_USER = """Create a detailed task plan for the following goal:

Goal: {goal}

Planning Strategy:
- Max Depth: {max_depth}
- Max Width: {max_width}
- Optimization Goals: {optimization_goals}

Break this down into a tree of subtasks, identifying dependencies, resources, and execution order.
Provide clear reasoning for your decomposition approach."""

task_decomposition_prompt = ChatPromptTemplate.from_messages(
    [("system", TASK_DECOMPOSITION_SYSTEM), ("human", TASK_DECOMPOSITION_USER)]
)

# ============================================================================
# Subtask Refinement Prompt
# ============================================================================

SUBTASK_REFINEMENT_SYSTEM = """You are an expert at refining and detailing subtasks within a larger plan.

Given a high-level subtask, you should:
1. Break it down further if needed (respecting depth limits)
2. Specify exact actions or decisions required
3. Identify all dependencies and resources
4. Estimate duration realistically
5. Define clear success criteria

Consider the parent task context and overall goal when refining."""

SUBTASK_REFINEMENT_USER = """Refine this subtask within the larger plan:

Parent Task: {parent_task}
Current Subtask: {subtask_name}
Description: {subtask_description}
Current Depth: {current_depth}
Max Depth: {max_depth}

Overall Goal: {goal}

Provide a detailed refinement with specific actions, dependencies, and resource requirements."""

subtask_refinement_prompt = ChatPromptTemplate.from_messages(
    [("system", SUBTASK_REFINEMENT_SYSTEM), ("human", SUBTASK_REFINEMENT_USER)]
)

# ============================================================================
# Execution Planning Prompt
# ============================================================================

EXECUTION_PLANNING_SYSTEM = """You are an expert execution planner who optimizes task execution order and parallelization.

Given a set of tasks with dependencies, create an optimal execution plan that:
1. Respects all dependencies
2. Maximizes parallelization where possible
3. Considers resource constraints
4. Minimizes total execution time
5. Handles potential bottlenecks

Resource Constraints:
{resource_constraints}

Optimization Priority: {optimization_goals}

Create execution batches that can run efficiently while maintaining correctness."""

EXECUTION_PLANNING_USER = """Create an execution plan for these tasks:

Available Tasks:
{available_tasks}

Completed Tasks: {completed_tasks}
Active Tasks: {active_tasks}
Failed Tasks: {failed_tasks}

Current Resource Usage: {resource_usage}

Determine which tasks should execute next and how they should be grouped."""

execution_planning_prompt = ChatPromptTemplate.from_messages(
    [("system", EXECUTION_PLANNING_SYSTEM), ("human", EXECUTION_PLANNING_USER)]
)

# ============================================================================
# Task Execution Prompt
# ============================================================================

TASK_EXECUTION_SYSTEM = """You are a task executor responsible for carrying out specific actions in a larger plan.

Execute the given task by:
1. Understanding the task requirements and context
2. Using available resources appropriately
3. Producing clear, structured results
4. Handling errors gracefully
5. Providing status updates

Available Resources:
{available_resources}

Previous Results from Dependencies:
{dependency_results}

Execute tasks precisely and report results in the required format."""

TASK_EXECUTION_USER = """Execute this task:

Task: {task_name}
Description: {task_description}
Action: {task_action}
Type: {task_type}

Parent Context: {parent_context}
Task Dependencies Met: {dependencies_met}

Execute this task and provide results in the structured format."""

task_execution_prompt = ChatPromptTemplate.from_messages(
    [("system", TASK_EXECUTION_SYSTEM), ("human", TASK_EXECUTION_USER)]
)

# ============================================================================
# Decision Node Prompt
# ============================================================================

DECISION_NODE_SYSTEM = """You are a decision-making component in a planning system.

Evaluate conditions and make branching decisions based on:
1. Current state and results
2. Decision criteria specified
3. Available information
4. Goal alignment

Make clear, justified decisions that advance toward the overall goal."""

DECISION_NODE_USER = """Make a decision for this branching point:

Decision Node: {node_name}
Criteria: {decision_criteria}

Current State:
- Completed Tasks: {completed_tasks}
- Recent Results: {recent_results}
- Goal Progress: {goal_progress}

Available Branches:
{branches}

Evaluate the criteria and choose the appropriate branch with justification."""

decision_node_prompt = ChatPromptTemplate.from_messages(
    [("system", DECISION_NODE_SYSTEM), ("human", DECISION_NODE_USER)]
)

# ============================================================================
# Replanning Analysis Prompt
# ============================================================================

REPLANNING_ANALYSIS_SYSTEM = """You are an expert at analyzing plan execution and determining when replanning is needed.

Analyze the current execution state and determine if replanning would be beneficial by considering:
1. Failure patterns and root causes
2. Changed assumptions or constraints
3. New information discovered during execution
4. Resource availability changes
5. Goal feasibility

Provide actionable recommendations for plan adjustments."""

REPLANNING_ANALYSIS_USER = """Analyze whether replanning is needed:

Original Goal: {goal}
Current Progress: {completion_percentage}%

Execution State:
- Completed Tasks: {completed_count}
- Failed Tasks: {failed_count}
- Active Tasks: {active_count}

Failure Details:
{failure_details}

Recent Discoveries:
{recent_discoveries}

Resource Status:
{resource_status}

Analyze the situation and recommend whether and how to replan."""

replanning_analysis_prompt = ChatPromptTemplate.from_messages(
    [("system", REPLANNING_ANALYSIS_SYSTEM), ("human", REPLANNING_ANALYSIS_USER)]
)

# ============================================================================
# Adaptive Replanning Prompt
# ============================================================================

ADAPTIVE_REPLANNING_SYSTEM = """You are an expert at adaptive replanning based on execution feedback.

Given the current state and identified issues, create an updated plan that:
1. Addresses root causes of failures
2. Incorporates lessons learned
3. Adjusts estimates based on actual performance
4. Maintains progress toward the original goal
5. Optimizes remaining work

Replanning Strategy: {replanning_strategy}

Create a revised plan that adapts to the current reality while maintaining goal focus."""

ADAPTIVE_REPLANNING_USER = """Create an updated plan based on execution feedback:

Original Goal: {goal}
Current State Summary: {state_summary}

Failed Tasks and Reasons:
{failure_analysis}

Successful Patterns:
{success_patterns}

New Constraints Discovered:
{new_constraints}

Tasks Needing Modification:
{tasks_to_modify}

Create an adapted plan that addresses these issues while maintaining progress toward the goal."""

adaptive_replanning_prompt = ChatPromptTemplate.from_messages(
    [("system", ADAPTIVE_REPLANNING_SYSTEM), ("human", ADAPTIVE_REPLANNING_USER)]
)

# ============================================================================
# Progress Monitoring Prompt
# ============================================================================

PROGRESS_MONITORING_SYSTEM = """You are a progress monitor analyzing plan execution status.

Provide insights on:
1. Overall progress toward the goal
2. Execution efficiency and bottlenecks
3. Risk factors and mitigation suggestions
4. Resource utilization patterns
5. Estimated time to completion

Be analytical and highlight both successes and areas of concern."""

PROGRESS_MONITORING_USER = """Analyze the current execution progress:

Goal: {goal}
Start Time: {start_time}
Current Time: {current_time}

Progress Metrics:
- Completion: {completion_percentage}%
- Success Rate: {success_rate}%
- Average Task Duration: {avg_duration}s
- Resource Utilization: {resource_utilization}

Task Distribution:
- Completed: {completed_count}
- In Progress: {active_count}
- Pending: {pending_count}
- Failed: {failed_count}

Critical Path Status: {critical_path_status}

Provide a comprehensive progress analysis with recommendations."""

progress_monitoring_prompt = ChatPromptTemplate.from_messages(
    [("system", PROGRESS_MONITORING_SYSTEM), ("human", PROGRESS_MONITORING_USER)]
)

# ============================================================================
# Loop Condition Evaluation Prompt
# ============================================================================

LOOP_CONDITION_SYSTEM = """You are responsible for evaluating loop continuation conditions in a planning system.

Evaluate whether a loop should continue based on:
1. The specified loop condition
2. Current iteration results
3. Overall goal progress
4. Resource constraints
5. Termination criteria

Make clear decisions with justification."""

LOOP_CONDITION_USER = """Evaluate this loop condition:

Loop Task: {loop_name}
Condition: {loop_condition}
Current Iteration: {iteration_count}

Recent Iteration Results:
{iteration_results}

Goal Progress: {goal_progress}
Resource Usage: {resource_usage}

Should the loop continue? Provide reasoning."""

loop_condition_prompt = ChatPromptTemplate.from_messages(
    [("system", LOOP_CONDITION_SYSTEM), ("human", LOOP_CONDITION_USER)]
)

# ============================================================================
# Example Usage Functions
# ============================================================================


def create_decomposition_aug_llm(llm_config):
    """Create AugLLMConfig for task decomposition."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from recursive_planning_models import TaskDecomposition

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=task_decomposition_prompt,
        structured_output_model=TaskDecomposition,
        structured_output_version="v2",
        temperature=0.4,  # Moderate temperature for creative but consistent planning
        input_variables=[
            "goal",
            "constraints",
            "context",
            "max_depth",
            "max_width",
            "optimization_goals",
        ],
    )


def create_execution_planning_aug_llm(llm_config):
    """Create AugLLMConfig for execution planning."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from recursive_planning_models import ExecutionPlan

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=execution_planning_prompt,
        structured_output_model=ExecutionPlan,
        structured_output_version="v2",
        temperature=0.2,  # Low temperature for consistent execution planning
        input_variables=[
            "available_tasks",
            "completed_tasks",
            "active_tasks",
            "failed_tasks",
            "resource_usage",
            "resource_constraints",
            "optimization_goals",
        ],
    )


def create_replanning_analysis_aug_llm(llm_config):
    """Create AugLLMConfig for replanning analysis."""
    from haive.core.engine.aug_llm import AugLLMConfig
    from recursive_planning_models import ReplanningAnalysis

    return AugLLMConfig(
        llm_config=llm_config,
        prompt_template=replanning_analysis_prompt,
        structured_output_model=ReplanningAnalysis,
        structured_output_version="v2",
        temperature=0.3,  # Balanced temperature for analysis
        input_variables=[
            "goal",
            "completion_percentage",
            "completed_count",
            "failed_count",
            "active_count",
            "failure_details",
            "recent_discoveries",
            "resource_status",
        ],
    )
