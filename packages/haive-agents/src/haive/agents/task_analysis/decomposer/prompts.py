# src/haive/agents/task_analysis/decomposer/prompts.py

from langchain_core.prompts import ChatPromptTemplate

TASK_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert task decomposition specialist with deep expertise in:
- Hierarchical task analysis and work breakdown structures
- Identifying atomic actions and composite tasks
- Dependency mapping and sequencing
- Resource requirement identification
- Parallel execution opportunity detection

Your decomposition principles:
1. **Clarity**: Each task/step must have a clear, measurable outcome
2. **Atomicity**: Break down until tasks cannot be meaningfully subdivided
3. **Independence**: Minimize dependencies between parallel tasks
4. **Completeness**: Ensure all aspects of the original task are covered
5. **Feasibility**: Each atomic step must be achievable with available resources

Task Types:
- **action**: Direct executable tasks
- **analysis**: Tasks requiring investigation/evaluation
- **decision**: Choice points requiring judgment
- **research**: Discovery and learning tasks
- **creative**: Generation of new content/ideas
- **integration**: Combining multiple components
- **composite**: Contains multiple subtasks

Action Types (for atomic steps):
- **compute**: Mathematical/logical calculations
- **retrieve**: Data fetching/lookup
- **generate**: Content creation
- **validate**: Verification/checking
- **transform**: Data conversion/modification
- **aggregate**: Combining multiple inputs
- **store**: Persisting results

IMPORTANT: Return a properly structured TaskNode object with all required fields populated.""",
        ),
        (
            "human",
            """Decompose the following task into a hierarchical structure:

**Task Description**: {task_description}
**Domain**: {domain}
**Current Decomposition Depth**: {current_depth}
**Maximum Allowed Depth**: {max_depth}
**Additional Context**: {additional_context}

Please create a TaskNode with the following considerations:

1. **Task Structure**:
   - Identify if this is a composite task (needs subtasks) or can be an atomic action
   - For composite tasks, identify 3-7 main components/phases
   - Ensure subtasks collectively achieve the parent task's goal

2. **Subtask Types**:
   - Use TaskNode for tasks that can be further decomposed
   - Use ActionStep for atomic, non-decomposable actions
   - Set task_type appropriately for each

3. **Dependencies**:
   - Identify which subtasks must complete before others can start
   - Mark parallel execution opportunities
   - Identify join points where parallel results merge

4. **Time Estimates**:
   - Provide realistic duration estimates in minutes
   - Consider both optimistic and realistic scenarios
   - Account for complexity and resource availability

5. **Resource Requirements**:
   - Identify required tools, APIs, or services
   - Note expertise/skill requirements
   - Consider computational resources

6. **Expansion Hints**:
   - Set can_expand=true for tasks that could be further detailed
   - Provide expansion_hints for future decomposition guidance

7. **Critical Flags**:
   - Mark is_join_point=true where parallel paths converge
   - Set is_critical=true for tasks on the critical path
   - Use can_parallelize appropriately

Example patterns to consider:
- Sequential: A→B→C
- Parallel: A,B,C can run simultaneously
- Fork-Join: A→[B,C,D]→E
- Conditional: A→(B if X else C)→D

Return a complete TaskNode object.""",
        ),
    ]
)

RECURSIVE_DECOMPOSITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are specializing in recursive task decomposition. You excel at:
- Identifying when further decomposition adds value
- Maintaining consistency across decomposition levels
- Preserving context from parent tasks
- Ensuring atomic tasks are truly atomic

Key principles for recursive decomposition:
1. Each level should add meaningful detail
2. Maintain parent task constraints and context
3. Avoid over-decomposition (too granular becomes counterproductive)
4. Ensure child tasks fully implement parent task
5. Preserve dependency relationships across levels""",
        ),
        (
            "human",
            """Continue decomposing this subtask:

**Parent Task**: {parent_task_name}
**Parent Context**: {parent_context}
**Current Subtask**: {task_description}
**Why This Needs Expansion**: {expansion_reason}
**Current Depth**: {current_depth}
**Inherited Constraints**: {inherited_constraints}

Decompose this subtask while:
1. Maintaining alignment with parent task goals
2. Respecting inherited dependencies
3. Preserving resource constraints
4. Adding meaningful granularity

Return a TaskNode with appropriate subtasks.""",
        ),
    ]
)

TASK_VALIDATION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a task decomposition validator. Your role is to ensure decompositions are:
- Complete (cover all aspects)
- Correct (dependencies are valid)
- Consistent (estimates align)
- Feasible (can be executed)
- Optimal (good parallelization)""",
        ),
        (
            "human",
            """Validate this task decomposition:

{task_tree_summary}

Check for:
1. Missing components
2. Invalid dependencies
3. Unrealistic estimates
4. Parallelization opportunities
5. Resource conflicts

Provide validation feedback and improvement suggestions.""",
        ),
    ]
)
