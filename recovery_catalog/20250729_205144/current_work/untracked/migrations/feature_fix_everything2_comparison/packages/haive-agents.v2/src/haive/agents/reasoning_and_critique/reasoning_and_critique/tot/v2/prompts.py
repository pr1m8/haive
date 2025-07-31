"""Prompts core module.

This module provides prompts functionality for the Haive framework.
"""

from langchain_core.prompts import ChatPromptTemplate

# Expansion prompts - all fields must exist in ToTState
expansion_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert problem solver using Tree of Thoughts methodology.
Your task is to generate diverse candidate solutions by exploring different approaches.

Current search context:
- Depth: {depth}/{max_depth}
- Strategy: {search_strategy}

Guidelines:
1. Each candidate should explore a different approach or angle
2. Build on successful patterns from parent candidates
3. Avoid repeating failed approaches
4. Consider both incremental improvements and creative leaps""",
        ),
        (
            "human",
            """Problem: {problem}

Current search progress:
{search_progress}

Parent candidates to expand from:
{candidates_for_expansion}

Generate {expansion_factor} new candidate solutions.
Each should be substantively different while building on what works.""",
        ),
    ]
)

# Scoring prompts - all fields exist in state or computed properties
scoring_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert evaluator for Tree of Thoughts search.
Evaluate candidates based on:

1. **Correctness**: Does the solution properly address the problem?
2. **Progress**: Does it move us closer to a complete solution?
3. **Feasibility**: Can this approach actually work?
4. **Innovation**: Does it offer new insights or approaches?

Scoring scale:
- 0.9-1.0: Excellent solution, likely to succeed
- 0.7-0.9: Good solution with minor issues
- 0.5-0.7: Decent approach but significant concerns
- 0.3-0.5: Flawed but has some merit
- 0.0-0.3: Poor solution, unlikely to succeed""",
        ),
        (
            "human",
            """Problem: {problem}

Candidate to evaluate:
{candidate_for_scoring}

Current best score: {best_score}
Best candidates so far:
{best_candidates_summary}

Evaluate this candidate thoroughly and provide a score with detailed reasoning.""",
        ),
    ]
)

# Control/Pruning prompts - using only state fields
control_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are the Tree of Thoughts search coordinator.
Your responsibilities:
1. Select the most promising candidates to continue exploring
2. Decide when to terminate the search
3. Adjust search strategy based on progress

Consider:
- Search efficiency (depth vs breadth)
- Convergence indicators
- Diversity vs exploitation tradeoff
- Computational budget (current depth: {depth}/{max_depth})""",
        ),
        (
            "human",
            """Problem: {problem}

All scored candidates:
{scored_candidates_summary}

Search status:
{search_progress}

Parameters:
- Beam size: {beam_size}
- Success threshold: {threshold}
- Current best score: {best_score}

Decide which candidates to keep and whether to continue searching.
If continuing, suggest the strategy for the next iteration.""",
        ),
    ]
)
