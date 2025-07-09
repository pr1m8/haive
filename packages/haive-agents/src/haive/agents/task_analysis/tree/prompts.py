# src/haive/agents/task_analysis/tree/prompts.py

from langchain_core.prompts import ChatPromptTemplate

TREE_STRUCTURE_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a tree structure analyst specializing in hierarchical task analysis and optimization.

Your expertise includes:
- Tree balance and efficiency analysis
- Depth vs breadth trade-offs
- Dependency path analysis
- Structural pattern recognition
- Tree optimization strategies""",
        ),
        (
            "human",
            """Analyze this task tree structure:

**Tree Visualization**:
{tree_visualization}

**Tree Metrics**:
- Depth: {max_depth}
- Breadth: {max_breadth}
- Total Nodes: {total_nodes}
- Leaf Nodes: {leaf_nodes}
- Balance Factor: {balance_factor}

Analyze:
1. Structural efficiency
2. Balance issues
3. Optimization opportunities
4. Dependency bottlenecks
5. Parallelization potential

Provide structural recommendations.""",
        ),
    ]
)

CRITICAL_PATH_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are analyzing critical paths through task trees to identify optimization opportunities.""",
        ),
        (
            "human",
            """Analyze critical path for:

**Task Tree**: {task_tree}
**Dependencies**: {dependencies}
**Duration Estimates**: {durations}

Identify:
1. Primary critical path
2. Near-critical paths
3. Slack time in non-critical paths
4. Optimization opportunities
5. Risk points

Return critical path analysis with recommendations.""",
        ),
    ]
)

TREE_PATTERN_RECOGNITION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are recognizing patterns in task tree structures to identify common workflows and optimization opportunities.""",
        ),
        (
            "human",
            """Identify patterns in:

**Tree Structure**: {tree_structure}

Look for:
1. Sequential chains
2. Parallel branches
3. Fork-join patterns
4. Iterative loops
5. Conditional branches
6. Common subtree patterns

Return identified patterns and their implications.""",
        ),
    ]
)
