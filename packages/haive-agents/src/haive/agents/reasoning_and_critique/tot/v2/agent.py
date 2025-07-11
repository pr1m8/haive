import logging
from typing import Any, Dict, List, Literal, Optional, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END
from langgraph.types import Send

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.simple.agent import SimpleAgent

from .models import (
    Candidate,
    CandidateEvaluation,
    CandidateGeneration,
    ScoredCandidate,
    SearchControl,
)
from .prompts import control_prompt, expansion_prompt, scoring_prompt
from .state import ExpansionState, ToTState

logger = logging.getLogger(__name__)
# In agent.py, fix the engines:

expansion_engine = AugLLMConfig(
    name="tot_expansion_engine",
    prompt_template=expansion_prompt,
    structured_output_model=CandidateGeneration,
    structured_output_model_version="v2",
    temperature=0.9,
    model_kwargs={"top_p": 0.95},
)

scoring_engine = AugLLMConfig(
    name="tot_scoring_engine",
    prompt_template=scoring_prompt,
    structured_output_model=CandidateEvaluation,
    structured_output_model_version="v2",
    temperature=0.3,
)

control_engine = AugLLMConfig(
    name="tot_control_engine",
    prompt_template=control_prompt,
    structured_output_model=SearchControl,
    structured_output_model_version="v2",
    temperature=0.2,
)

# Create the agents
expander = SimpleAgent(name="expander", engine=expansion_engine)
scorer = SimpleAgent(name="scorer", engine=scoring_engine)
controller = SimpleAgent(name="controller", engine=control_engine)


# Custom workflow nodes for ToT-specific logic
def expansion_workflow(state: ToTState) -> dict[str, Any]:
    """Process expansion results and create candidates."""
    # This is called after the expansion agent runs
    # The expansion agent's result should be in the last message
    if state.messages and hasattr(state.messages[-1], "content"):
        result = state.messages[-1].content
        if isinstance(result, dict) and "candidates" in result:
            new_candidates = []
            for i, candidate_data in enumerate(result["candidates"]):
                candidate = Candidate(
                    content=candidate_data,
                    depth=state.depth,
                    parent_id=(
                        state.seed.id if hasattr(state, "seed") and state.seed else None
                    ),
                    expansion_index=i,
                )
                new_candidates.append(candidate)

            return {
                "candidates": new_candidates,
                "all_candidates_history": new_candidates,
            }
    return {}


def scoring_workflow(state: ToTState) -> dict[str, Any]:
    """Process all candidates for scoring."""
    # Score all candidates
    scored = []
    for candidate in state.candidates:
        # Set current candidate for scoring
        state_dict = state.dict()
        state_dict["current_candidate_id"] = candidate.id
        scoring_state = ToTState(**state_dict)

        # Invoke scoring agent
        result = scorer.invoke(scoring_state)

        if hasattr(result, "messages") and result.messages:
            last_msg = result.messages[-1]
            if hasattr(last_msg, "content") and isinstance(last_msg.content, dict):
                eval_result = last_msg.content
                scored_candidate = ScoredCandidate.from_candidate(
                    candidate,
                    score=eval_result.get("score", 0.0),
                    feedback=eval_result.get("feedback", ""),
                    strengths=eval_result.get("strengths", []),
                    weaknesses=eval_result.get("weaknesses", []),
                    confidence=eval_result.get("confidence", 0.8),
                )
                scored.append(scored_candidate)

    return {
        "scored_candidates": scored,
        "candidates": "clear",  # Clear unscored candidates
    }


def control_workflow(state: ToTState) -> dict[str, Any]:
    """Process control results and update state."""
    # This is called after the control agent runs
    if state.messages and hasattr(state.messages[-1], "content"):
        result = state.messages[-1].content
        if isinstance(result, dict):
            # Select candidates based on indices
            if "selected_indices" in result and state.scored_candidates:
                selected = [
                    state.scored_candidates[i]
                    for i in result["selected_indices"]
                    if i < len(state.scored_candidates)
                ]

                # Update best solution
                best = None
                for candidate in selected:
                    if not best or candidate.score > best.score:
                        best = candidate

                updates = {
                    "selected_candidates": selected,
                    "scored_candidates": "clear",
                    "candidates": "clear",
                    "should_terminate": result.get("should_terminate", False),
                    "termination_reason": result.get("termination_reason"),
                    "depth": 1,  # Increment depth
                }

                if best and (
                    not state.best_solution or best.score > state.best_solution.score
                ):
                    updates["best_solution"] = best

                return updates
    return {}


# Routing functions
def route_after_expansion(state: ToTState) -> str:
    """After expansion, go to scoring workflow."""
    return "scoring_prep"


def route_after_scoring_prep(state: ToTState) -> str:
    """After scoring prep, go to scorer."""
    return "scorer"


def route_after_scoring(state: ToTState) -> str:
    """After scoring, go to control workflow."""
    return "control_post"


def route_after_control_post(state: ToTState) -> str:
    """After control post-processing, go to controller."""
    return "controller"


def should_continue_search(state: ToTState) -> str | list[Send]:
    """After control, decide whether to continue search."""
    if state.should_terminate:
        return END

    if state.depth >= state.max_depth:
        return END

    if state.best_solution and state.best_solution.score >= state.threshold:
        return END

    # Create Send objects for parallel expansion from each selected candidate
    if state.selected_candidates:
        sends = []
        for candidate in state.selected_candidates:
            # Create expansion state with seed
            expansion_state = ExpansionState(**state.dict(), seed=candidate)
            sends.append(Send("expander", expansion_state))
        return sends

    # First iteration - no candidates yet
    return "expander"


# Create function for Tree of Thoughts
def create_tree_of_thoughts(
    name: str = "TreeOfThoughts",
    max_depth: int = 10,
    beam_size: int = 3,
    expansion_factor: int = 5,
    threshold: float = 0.9,
    **kwargs
) -> MultiAgentBase:
    """Create a Tree of Thoughts multi-agent system."""
    # Define branches for routing
    branches = [
        (expander, route_after_expansion, {"scoring_prep": "scoring_prep"}),
        ("scoring_prep", route_after_scoring_prep, {"scorer": scorer}),
        (scorer, route_after_scoring, {"control_post": "control_post"}),
        ("control_post", route_after_control_post, {"controller": controller}),
        (controller, should_continue_search, {"expander": expander, END: END}),
    ]

    # Custom workflow nodes
    workflow_nodes = {
        "expansion_post": expansion_workflow,
        "scoring_prep": scoring_workflow,
        "control_post": control_workflow,
    }

    # Create the multi-agent system
    system = MultiAgentBase(
        name=name,
        agents=[expander, scorer, controller],
        branches=branches,
        state_schema_override=ToTState,
        schema_build_mode=BuildMode.SEQUENCE,
        workflow_nodes=workflow_nodes,
        **kwargs
    )

    # Set initial state values
    system.initial_state = {
        "max_depth": max_depth,
        "beam_size": beam_size,
        "expansion_factor": expansion_factor,
        "threshold": threshold,
    }

    return system


# Convenience function for common use case
def solve_with_tot(
    problem: str,
    problem_type: str | None = None,
    max_depth: int = 5,
    beam_size: int = 3,
    **kwargs
) -> dict[str, Any]:
    """Solve a problem using Tree of Thoughts."""
    system = create_tree_of_thoughts(max_depth=max_depth, beam_size=beam_size, **kwargs)

    # Build and compile the graph
    graph = system.build_graph()
    compiled = graph.compile()

    # Create initial state
    initial_state = {
        "messages": [{"role": "user", "content": problem}],
        "problem_type": problem_type,
    }

    # Run the system
    result = compiled.invoke(initial_state)

    return result
