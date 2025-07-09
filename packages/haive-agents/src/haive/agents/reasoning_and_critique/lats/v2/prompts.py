from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Initial response prompt
initial_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an AI assistant with access to tools.
Analyze the user's request and decide whether to:
1. Use a tool to gather information
2. Provide a direct response

Available tools: {tools}""",
        ),
        ("human", "{input_query}"),
    ]
)

# Expansion prompt - generates candidates
expansion_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are exploring different approaches to solve a problem.
Based on the current trajectory, suggest {n_candidates} different next actions.
These should be diverse and explore different solution paths.

Available tools: {tools}""",
        ),
        (
            "human",
            """Original query: {input_query}

Current trajectory:
{current_trajectory}

Generate {n_candidates} diverse candidate next actions.""",
        ),
    ]
)

# Reflection prompt
reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are evaluating the quality of an AI assistant's response.
Consider:
1. Does it make progress toward solving the problem?
2. Is the information accurate and relevant?
3. Are there any errors or issues?
4. Has the problem been fully solved?

Score from 0-10 where:
- 0-3: Poor response, wrong direction
- 4-6: Partial progress, needs improvement
- 7-8: Good response, nearly complete
- 9-10: Excellent, problem solved""",
        ),
        (
            "human",
            """Original query: {input_query}

Response to evaluate:
{response_to_evaluate}

Provide your reflection and score.""",
        ),
    ]
)

# Selection prompt
selection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are managing a tree search to find the best solution.
Based on the current tree statistics and node values, decide:
1. Which node to expand next (using UCT scores)
2. Whether to terminate the search

Tree uses Upper Confidence Bound (UCT) scoring to balance exploration vs exploitation.""",
        ),
        (
            "human",
            """Query: {input_query}

Tree statistics:
{tree_statistics}

Current best solution score: {best_score}
Rollouts completed: {rollouts_completed}/{max_rollouts}

Should we continue searching? If so, which node should we expand?""",
        ),
    ]
)
