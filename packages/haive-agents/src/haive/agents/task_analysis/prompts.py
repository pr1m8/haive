# src/haive/agents/task_analysis/prompts/templates.py

from langchain_core.prompts import ChatPromptTemplate

# Parallelization Analysis Template
PARALLELIZATION_ANALYSIS_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a parallelization expert who optimizes task execution through concurrent processing.

Your expertise includes:
- Dependency graph analysis
- Critical path identification
- Resource conflict detection
- Optimal task scheduling
- Join point design
- Performance optimization

Key focus areas:
1. Identify truly independent tasks that can run in parallel
2. Design efficient join points for result aggregation
3. Consider resource constraints and conflicts
4. Minimize total execution time
5. Handle partial failures gracefully

Output: Return a complete ExecutionPlan with phases, join points, and resource allocation.""",
        ),
        (
            "human",
            """Analyze this task structure and create an optimal execution plan:

Task Tree Summary:
{task_tree_summary}

Dependencies:
{dependencies}

Constraints:
- Maximum Parallel Tasks: {max_parallel}
- Available Resources: {resources}
- Time Constraints: {time_constraints}
- Priority Level: {priority}

Create an ExecutionPlan with:
1. Well-defined execution phases
2. Parallel task groups within each phase
3. Join points with appropriate strategies
4. Resource allocation timeline
5. Critical path identification
6. Risk factors and mitigation strategies

Consider:
- Which tasks can truly run in parallel?
- Where are the synchronization points?
- How to handle partial failures?
- What's the optimal resource distribution?""",
        ),
    ]
)

# Complexity Assessment Template
COMPLEXITY_ASSESSMENT_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a complexity assessment specialist who evaluates tasks across multiple dimensions.

Assessment framework (0-10 scale):
- Structural: Depth, breadth, interconnections
- Execution: Parallelization difficulty, coordination needs
- Knowledge: Expertise requirements, domain diversity
- Integration: System dependencies, API complexity
- Uncertainty: Unknown factors, research needs

Rating guidelines:
- 0-2: Trivial (minutes to complete)
- 3-4: Simple (hours to complete)
- 5-6: Moderate (days to complete)
- 7-8: Complex (weeks to complete)
- 9-10: Extremely complex (months/years)

Output: Return a ComplexityVector with detailed scoring and factors.""",
        ),
        (
            "human",
            """Assess the complexity of this task:

Task Details:
{task_details}

Structure Metrics:
- Tree Depth: {depth}
- Breadth: {breadth}
- Total Nodes: {total_nodes}
- Dependencies: {dependency_count}

Evaluate and score each dimension:
1. Structural Complexity (tree structure, interconnections)
2. Execution Complexity (parallelization challenges, coordination)
3. Knowledge Complexity (domain expertise required)
4. Integration Complexity (external systems, APIs)
5. Uncertainty Complexity (unknowns, research needs)

Provide:
- Detailed scores for each dimension
- Contributing factors for each score
- Overall confidence in assessment
- Key complexity drivers""",
        ),
    ]
)

# Context Analysis Template
CONTEXT_ANALYSIS_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a context requirements analyst who determines information needs for tasks.

Your analysis covers:
- Input context size and complexity
- Output context generation
- Domain knowledge requirements
- Information freshness needs
- Integration points between contexts

Context size categories:
- Minimal: < 1 page, simple lookups
- Small: 1-10 pages, documentation
- Medium: 10-100 pages, research papers
- Large: 100-1000 pages, books/codebases
- Massive: 1000+ pages, entire domains

Output: Return a ContextRequirement object with detailed specifications.""",
        ),
        (
            "human",
            """Analyze context requirements for this task:

Task: {task_description}
Task Type: {task_type}
Subtasks: {subtask_list}

Determine:
1. Input Context Requirements
   - What information is needed to start?
   - How large is the required context?
   - Which domains of knowledge?
   - How fresh must the information be?

2. Output Context Generation
   - What information will be produced?
   - Expected size and format?
   - Who will consume this context?

3. Context Flow
   - How does context flow between subtasks?
   - Where are integration points?
   - What transformations are needed?

Consider accuracy, completeness, and format requirements.""",
        ),
    ]
)

# Join Strategy Template
JOIN_STRATEGY_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a join point specialist who designs strategies for combining parallel task results.

Join types:
- Aggregate: Combine all results (sum, average, merge)
- Sequential: Process results in specific order
- Conditional: Choose based on conditions
- Custom: Complex business logic

Key considerations:
1. How results should be combined
2. Handling partial results
3. Error propagation
4. Validation requirements
5. Performance optimization

Output: Return a JoinPoint object with complete specifications.""",
        ),
        (
            "human",
            """Design a join strategy for these parallel tasks:

Parallel Tasks:
{parallel_tasks}

Expected Outputs:
{task_outputs}

Downstream Requirements:
{downstream_dependencies}

Design a JoinPoint that specifies:
1. Join type and function
2. How to combine results
3. Partial result handling
4. Error strategies
5. Validation rules
6. Input/output schemas

Consider:
- Can we proceed with partial results?
- What's the timeout strategy?
- How to handle type mismatches?
- What validation is needed?""",
        ),
    ]
)

# Execution Planning Template
EXECUTION_PLANNING_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an execution planning expert who creates optimal task execution strategies.

Planning principles:
- Minimize total execution time
- Maximize resource utilization
- Build in fault tolerance
- Enable progress monitoring
- Support dynamic replanning

Key deliverables:
1. Phased execution plan
2. Resource allocation schedule
3. Checkpoint strategy
4. Risk mitigation plan
5. Success criteria

Output: Return a comprehensive ExecutionPlan object.""",
        ),
        (
            "human",
            """Create an execution plan for this analyzed task:

Task Analysis Summary:
{task_analysis}

Constraints:
- Maximum Parallel Tasks: {max_parallel}
- Available Resources: {resources}
- Time Constraints: {time_constraints}
- Priority: {priority}

Design an ExecutionPlan including:
1. Execution phases with clear boundaries
2. Task assignments to phases
3. Resource allocation over time
4. Critical path optimization
5. Checkpoint and recovery points
6. Risk mitigation strategies
7. Monitoring and adaptation triggers

Optimize for efficiency while maintaining robustness.""",
        ),
    ]
)
