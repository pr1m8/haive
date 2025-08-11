"""Working example of Tree of Thoughts without persistence issues."""

import asyncio
import os

# Disable persistence to avoid PostgreSQL issues
os.environ["HAIVE_PERSISTENCE_DISABLED"] = "true"

from haive.agents.reasoning_and_critique.tot.agents.candidate_generator import (
    CandidateGenerator,
)
from haive.agents.reasoning_and_critique.tot.agents.solution_scorer import (
    SolutionScorer,
)


async def demonstrate_tot():
    """Demonstrate Tree of Thoughts components working together."""
    # Initialize agents
    generator = CandidateGenerator.create(name="tot_generator", temperature=0.7)
    scorer = SolutionScorer(name="tot_scorer", temperature=0.3)

    # Example 1: Simple Math Problem

    problem1 = "Find three positive integers that sum to 15"

    # Generate candidates
    gen_result = await generator.generate_candidates(problem1, num_candidates=5)

    for _i, _candidate in enumerate(gen_result.candidates, 1):
        pass

    # Score candidates
    score_result = await scorer.score_solutions(problem1, gen_result.candidates)

    best_score = 0.0

    for scored in score_result.scored_solutions:
        best_score = max(best_score, scored.score)

    # Example 2: Game of 24

    problem2 = "Use the numbers 2, 3, 4, 6 with operations +, -, *, / to make 24. Each number must be used exactly once."

    # Iteration 1

    candidates_1 = await generator.generate_candidates(problem2, num_candidates=5)
    for _i, _c in enumerate(candidates_1.candidates, 1):
        pass

    scores_1 = await scorer.score_solutions(problem2, candidates_1.candidates)

    # Find top 3 for beam search
    scored_list = [(s.solution, s.score) for s in scores_1.scored_solutions]
    scored_list.sort(key=lambda x: x[1], reverse=True)
    top_candidates = [sol for sol, _ in scored_list[:3]]

    for _i, (_sol, _score) in enumerate(scored_list[:3], 1):
        pass

    # Iteration 2: Expand from best

    f"Based on these approaches: {', '.join(top_candidates[:2])}, generate new variations"
    candidates_2 = await generator.expand_from_seed(
        problem2, seed=top_candidates[0], num_candidates=4
    )

    for _i, _c in enumerate(candidates_2.candidates, 1):
        pass

    # Final scoring
    all_candidates = top_candidates + candidates_2.candidates
    final_scores = await scorer.score_solutions(problem2, all_candidates)

    final_best_score = 0.0

    for scored in final_scores.scored_solutions:
        final_best_score = max(final_best_score, scored.score)

    # Example 3: Creative Problem

    problem3 = "Design a simple two-player game that can be played with just a pencil and paper in under 5 minutes"

    # Generate creative solutions
    creative_gen = CandidateGenerator(name="creative_gen", temperature=0.9)
    creative_candidates = await creative_gen.generate_candidates(
        problem3, num_candidates=4
    )

    for _i, _idea in enumerate(creative_candidates.candidates, 1):
        pass

    # Score them
    creative_scores = await scorer.score_solutions(
        problem3, creative_candidates.candidates
    )

    max(creative_scores.scored_solutions, key=lambda x: x.score)


if __name__ == "__main__":
    # Run the demonstration
    asyncio.run(demonstrate_tot())
