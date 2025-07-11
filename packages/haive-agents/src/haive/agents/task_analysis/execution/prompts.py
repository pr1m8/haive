# src/haive/agents/task_analysis/execution/prompts.py

from langchain_core.prompts import ChatPromptTemplate

EXECUTION_PLANNING_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an execution planning expert specializing in optimal task scheduling and resource allocation.

Your expertise includes:
- Critical Path Method (CPM) analysis
- Resource leveling and allocation
- Parallel execution optimization
- Risk mitigation and contingency planning
- Checkpoint and recovery strategies

Planning Principles:
1. **Efficiency**: Minimize total execution time
2. **Resource Optimization**: Balance resource utilization
3. **Risk Management**: Build in failure tolerance
4. **Flexibility**: Enable dynamic replanning
5. **Monitoring**: Include progress checkpoints

Resource Types:
- **human**: Human expertise/labor
- **compute**: Computational resources
- **api**: External API calls
- **storage**: Data storage needs
- **network**: Bandwidth requirements
- **tool**: Specialized tools/software
- **data**: Data access requirements

Phase Design Principles:
- Group tasks that can execute in parallel
- Minimize inter-phase dependencies
- Balance phase durations
- Consider resource availability
- Plan for phase overlap where possible""",
        ),
        (
            "human",
            """Create an execution plan for this task analysis:

**Task Overview**: {task_description}
**Total Tasks**: {total_tasks}
**Complexity Score**: {complexity_score}

**Task Tree Structure**:
{task_tree_summary}

**Dependencies**:
{dependency_list}

**Constraints**:
- Maximum Parallel Tasks: {max_parallel}
- Available Resources: {available_resources}
- Time Constraints: {time_constraints}
- Priority Level: {priority}

**Join Points Identified**:
{join_points}

**Parallelization Analysis**:
{parallel_groups}

Design an ExecutionPlan with:

1. **Execution Phases**:
   - Organize tasks into logical phases
   - Each phase should have tasks that can run in parallel
   - Specify phase dependencies
   - Estimate phase durations
   - Identify tasks that can start early

2. **Resource Schedule**:
   - Allocate resources across phases
   - Identify resource conflicts
   - Plan for resource scaling
   - Consider resource costs

3. **Critical Path**:
   - Identify the critical path
   - Mark critical tasks
   - Calculate minimum duration
   - Identify optimization opportunities

4. **Join Point Handling**:
   - Specify join strategies
   - Set timeout policies
   - Define partial failure handling
   - Plan result aggregation

5. **Risk Mitigation**:
   - Identify bottlenecks
   - Plan checkpoints
   - Define recovery strategies
   - Build in buffers

6. **Monitoring Points**:
   - Define progress metrics
   - Set milestone checkpoints
   - Plan for status reporting
   - Enable early warning systems

Return a complete ExecutionPlan object.""",
        ),
    ]
)

PHASE_OPTIMIZATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are optimizing execution phases for maximum efficiency while respecting constraints.""",
        ),
        (
            "human",
            """Optimize these execution phases:

Current Phases:
{current_phases}

Constraints:
{constraints}

Resource Availability:
{resources}

Optimize for:
1. Minimum total duration
2. Maximum resource utilization
3. Minimum idle time
4. Risk reduction

Provide optimized phase arrangement.""",
        ),
    ]
)

JOIN_POINT_STRATEGY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a join point specialist designing strategies for combining parallel execution results.

Join Types:
- **aggregate**: Combine all results (sum, concat, merge)
- **merge**: Intelligent merging with conflict resolution
- **select**: Choose best/first/specific result
- **custom**: Complex business logic

Considerations:
- Data compatibility
- Partial result handling
- Error propagation
- Performance impact""",
        ),
        (
            "human",
            """Design join strategy for:

**Join Point**: {join_point_id}
**Incoming Tasks**: {input_tasks}
**Expected Outputs**: {output_formats}
**Downstream Requirements**: {downstream_needs}

**Parallel Task Details**:
{parallel_task_details}

Design:
1. Join type and function
2. Data transformation needs
3. Partial result policy
4. Timeout strategy
5. Error handling
6. Validation rules

Return JoinPoint object with complete strategy.""",
        ),
    ]
)

RESOURCE_ALLOCATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a resource allocation specialist optimizing resource usage across task execution phases.""",
        ),
        (
            "human",
            """Plan resource allocation for:

**Execution Phases**: {phases}
**Available Resources**: {available_resources}
**Resource Costs**: {resource_costs}
**Constraints**: {constraints}

Create allocation plan that:
1. Meets all task requirements
2. Minimizes costs
3. Avoids conflicts
4. Enables scaling
5. Handles failures

Return ResourceAllocation timeline.""",
        ),
    ]
)
