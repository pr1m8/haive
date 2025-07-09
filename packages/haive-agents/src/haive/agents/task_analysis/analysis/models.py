# Task Decomposition Template
from langchain_core.prompts import ChatPromptTemplate

TASK_DECOMPOSITION_TEMPLATE = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert task analyst specializing in breaking down complex tasks into manageable subtasks.

Your expertise includes:
- Hierarchical task decomposition
- Identifying atomic actions vs decomposable tasks
- Recognizing parallelization opportunities
- Understanding task dependencies
- Estimating complexity and duration

Key principles:
1. Break tasks down until they become atomic actions (cannot be further decomposed)
2. Use TaskNode for decomposable tasks, ActionStep for atomic actions
3. Identify natural parallelization opportunities
4. Be explicit about dependencies between tasks
5. Consider context requirements at each level
6. Provide accurate time estimates based on task complexity

Output: Return a properly structured TaskNode object with all required fields.""",
        ),
        (
            "human",
            """Analyze and decompose this task into a hierarchical structure:

Task Description: {task_description}
Domain: {domain}
Maximum Depth: {max_depth}
Additional Context: {additional_context}

Create a TaskNode with:
1. Appropriate subtasks (mix of TaskNode and ActionStep as needed)
2. Clear dependencies between subtasks
3. Accurate complexity scoring (0-10 scale)
4. Realistic time estimates in hours
5. Context requirements for inputs and outputs
6. Parallelization opportunities identified

Remember:
- TaskNode: For tasks that can be further broken down
- ActionStep: For atomic actions that cannot be decomposed
- Use meaningful IDs and names
- Set can_expand=True for nodes that could be further decomposed
- Consider resource requirements and constraints""",
        ),
    ]
)
