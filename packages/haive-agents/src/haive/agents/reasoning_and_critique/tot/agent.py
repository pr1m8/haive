"""Tree of Thoughts (ToT) agent implementation.

This module implements the Tree of Thoughts algorithm as a Haive agent.
"""

import logging
from typing import Generic, TypeVar

from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import END, START
from langgraph.types import Command, Send

from haive.agents.reasoning_and_critique.tot.config import TOTAgentConfig
from haive.agents.reasoning_and_critique.tot.models import (
    Candidate,
    Score,
    ScoredCandidate,
)
from haive.agents.reasoning_and_critique.tot.state import TOTState

logger = logging.getLogger(__name__)

# Type variable for content
T = TypeVar("T")


@register_agent(TOTAgentConfig)
class ToTAgent(Agent[TOTAgentConfig], Generic[T]):
    """Tree of Thoughts agent implementation.

    This agent implements the Tree of Thoughts search algorithm, which:
    1. Generates candidate solutions
    2. Scores the candidates
    3. Selects the best candidates for further exploration
    4. Repeats until a satisfactory solution is found or max depth reached

    The implementation supports parallel processing of candidates through beam search.
    """

    def __init__(self, config: TOTAgentConfig):
        """Initialize the ToT agent.

        Args:
            config: Configuration for the ToT agent
        """
        super().__init__(config)

        # Configure search parameters from config
        self.max_depth = config.max_depth
        self.beam_width = config.beam_width
        self.expansion_count = config.expansion_count
        self.threshold = config.threshold

        # Set up optional structured output models
        self.generator_output_model = config.generator_output_model
        self.evaluator_output_model = config.evaluator_output_model
        self.use_structured_output = config.use_structured_output

        # Parallelization settings
        self.parallel_evaluation = config.parallel_evaluation
        self.parallel_expansion = config.parallel_expansion

        # Set up runnables for the engines
        self._setup_runnables()

    def _setup_runnables(self):
        """Set up the generator and evaluator runnables."""
        # Get engine configurations from config
        generator_engine = self.config.get_engine("generator")
        evaluator_engine = self.config.get_engine("evaluator")

        # Apply structured output configuration if enabled
        if self.use_structured_output:
            self.generator_engine = create_generator_engine(
                generator_engine,
                use_structured_output=True,
                output_model=self.generator_output_model,
            )

            self.evaluator_engine = create_evaluator_engine(
                evaluator_engine,
                use_structured_output=True,
                output_model=self.evaluator_output_model,
            )
        else:
            self.generator_engine = generator_engine
            self.evaluator_engine = evaluator_engine

        # Create composed runnables
        self.generator_runnable = compose_generator_runnable(
            self.generator_engine, self.use_structured_output
        )

        self.evaluator_runnable = compose_evaluator_runnable(
            self.evaluator_engine, self.use_structured_output
        )

    def setup_workflow(self) -> None:
        """Set up the Tree of Thoughts workflow using the DynamicGraph builder.

        This creates a graph with nodes for:
        1. Generating candidate solutions
        2. Scoring candidates
        3. Selecting the best candidates for beam search
        4. Expanding new generations from those candidates
        """
        # Get engine configurations from config
        generator_engine = self.config.get_engine("generator")
        evaluator_engine = self.config.get_engine("evaluator")

        # Create the graph with state schema
        self.dynamic_graph = DynamicGraph(
            state_schema=self.config.state_schema,
            components=[generator_engine, evaluator_engine],
        )

        # Add nodes to the graph
        self.dynamic_graph.add_node(
            self.config.generator_node, self._generate_candidates
        )

        # Add evaluation nodes based on parallelization setting
        if self.parallel_evaluation:
            self.dynamic_graph.add_node("evaluate_candidate", self._evaluate_candidate)
            self.dynamic_graph.add_node(
                "collect_evaluations", self._collect_evaluations
            )
        else:
            self.dynamic_graph.add_node(
                self.config.evaluator_node, self._score_candidates
            )

        # Add selection node
        self.dynamic_graph.add_node(self.config.selector_node, self._select_best)

        # Define the workflow edges

        # From START to initial generation
        self.dynamic_graph.add_edge(START, self.config.generator_node)

        # From generation to evaluation
        if self.parallel_evaluation:
            # Map out to parallel evaluation
            self.dynamic_graph.add_conditional_edges(
                self.config.generator_node, self._map_candidates_to_evaluation, [END]
            )

            # From evaluation to collection
            self.dynamic_graph.add_edge("evaluate_candidate", "collect_evaluations")

            # From collection to selection
            self.dynamic_graph.add_edge(
                "collect_evaluations", self.config.selector_node
            )
        else:
            # Direct edge to sequential evaluation
            self.dynamic_graph.add_conditional_edges(
                self.config.generator_node,
                self._should_continue_search,
                [self.config.evaluator_node, END],
            )

            # From evaluation to selection
            self.dynamic_graph.add_edge(
                self.config.evaluator_node, self.config.selector_node
            )

        # From selection to either expansion or END
        if self.parallel_expansion:
            # Conditional edges for beam search expansion
            self.dynamic_graph.add_conditional_edges(
                self.config.selector_node, self._map_beam_expansion, [END]
            )
        else:
            # Simple conditional for continue/end
            self.dynamic_graph.add_conditional_edges(
                self.config.selector_node,
                self._should_expand_or_finish,
                [self.config.generator_node, END],
            )

        # Build the graph
        self.graph = self.dynamic_graph.build()

    async def _generate_candidates(self, state: TOTState) -> Command:
        """Generate candidate solutions for the problem.

        Args:
            state: Current search state

        Returns:
            Command with candidate updates
        """
        # Get generator engine
        generator = self.config.get_engine("generator")

        # Get the current seed for generation if any
        seed_info = ""
        if hasattr(state, "current_seed") and state.current_seed:
            seed_content = ""
            if hasattr(state.current_seed, "candidate") and hasattr(
                state.current_seed.candidate, "content"
            ):
                seed_content = state.current_seed.candidate.content
            elif hasattr(state.current_seed, "content"):
                seed_content = state.current_seed.content
            else:
                seed_content = str(state.current_seed)

            seed_info = f"\nUsing this as a starting point:\n{seed_content}"

        # Create the prompt
        prompt = f"Problem: {state.problem}\n{seed_info}\n\nGenerate {self.expansion_count} different candidate solutions."

        try:
            # Invoke the generator
            response = await generator.ainvoke(
                [HumanMessage(content=prompt)], {"configurable": {"temperature": 0.7}}
            )

            # Extract candidates from the response
            if hasattr(response, "to_candidates"):
                candidates = response.to_candidates()
            elif hasattr(response, "candidate_contents"):
                candidates = [Candidate(content=c) for c in response.candidate_contents]
            else:
                candidates = []
                # Fall back to extracting from response as string
                lines = (
                    response.content.split("\n")
                    if hasattr(response, "content")
                    else str(response).split("\n")
                )

                # Basic filtering for reasonable candidate lines
                for line in lines:
                    line = line.strip()
                    # Skip empty lines or very short ones
                    if line and len(line) > 10:
                        candidates.append(Candidate(content=line))

            # Ensure we have at least some candidates
            if not candidates:
                logger.warning("Failed to generate any valid candidates")
                return Command(update={"candidates": []}, goto=END)

            # Update the candidates in the state
            return Command(
                update={
                    "candidates": candidates,
                    "depth": state.depth + 1,
                    "current_seed": None,  # Clear the seed
                }
            )

        except Exception as e:
            logger.exception(f"Error generating candidates: {e}")
            return Command(update={"candidates": [], "error": str(e)}, goto=END)

    def _map_candidates_to_evaluation(self, state: TOTState) -> list[Send]:
        """Map candidates to parallel evaluation nodes.

        Args:
            state: Current search state

        Returns:
            List of Send commands for parallel evaluation
        """
        if not state.candidates:
            return [Send(END, state)]

        # Create a Send command for each candidate
        sends = []
        for candidate in state.candidates:
            # Create a new state for each evaluation with just this candidate
            candidate_state = {
                "problem": state.problem,
                "candidate": candidate,
                "depth": state.depth,
            }
            sends.append(Send("evaluate_candidate", candidate_state))

        return sends

    async def _evaluate_candidate(self, state: TOTState) -> Command:
        """Evaluate a single candidate solution.

        Args:
            state: State containing a single candidate to evaluate

        Returns:
            Command with evaluation results
        """
        candidate = state.get("candidate")
        if not candidate:
            return Command(update={"scored_candidate": None})

        try:
            # Get content from candidate
            content = candidate.get("content", str(candidate))

            # Create the prompt inputs
            prompt_inputs = {"problem": state.problem, "candidate": content}

            # Invoke the evaluator
            score = await self.evaluator_runnable.ainvoke(prompt_inputs)

            # Create scored candidate
            scored_candidate = ScoredCandidate(
                candidate=Candidate(
                    content=content, metadata=candidate.get("metadata", {})
                ),
                score=score,
            )

            return Command(update={"scored_candidate": scored_candidate})

        except Exception as e:
            logger.exception(f"Error evaluating candidate: {e}")
            # Create a zero-scored candidate as fallback
            fallback_score = Score(value=0.0, feedback=f"Error: {e}")
            scored_candidate = ScoredCandidate(
                candidate=Candidate(
                    content=candidate.get("content", str(candidate)),
                    metadata=candidate.get("metadata", {}),
                ),
                score=fallback_score,
            )
            return Command(update={"scored_candidate": scored_candidate})

    def _collect_evaluations(self, state: TOTState) -> Command:
        """Collect all the evaluated candidates.

        Args:
            state: Current state with individual evaluations

        Returns:
            Command with collected scored candidates
        """
        # Get the scored candidate from the current evaluation
        scored_candidate = state.get("scored_candidate")
        if not scored_candidate:
            return Command(update={})

        # Add to the list of scored candidates
        current_scored = state.get("scored_candidates", [])
        updated_scored = [*current_scored, scored_candidate]

        return Command(update={"scored_candidates": updated_scored})

    async def _score_candidates(self, state: TOTState) -> Command:
        """Score all candidates sequentially.

        Args:
            state: Current search state

        Returns:
            Command with scored candidate updates
        """
        scored_candidates = []

        for candidate in state.candidates:
            try:
                # Get evaluator engine
                evaluator = self.config.get_engine("evaluator")

                # Get content from candidate
                content = (
                    candidate.content
                    if hasattr(candidate, "content")
                    else str(candidate)
                )

                # Create the prompt
                prompt = f"Problem: {state.problem}\n\nCandidate Solution:\n{content}\n\nEvaluate this solution and provide a score between 0 and 1, where 1 is perfect."

                # Invoke the evaluator
                response = await evaluator.ainvoke(
                    [HumanMessage(content=prompt)],
                    {"configurable": {"temperature": 0.1}},
                )

                # Extract score from the response
                if hasattr(response, "to_score"):
                    score = response.to_score()
                elif hasattr(response, "value") and hasattr(response, "feedback"):
                    score = Score(value=response.value, feedback=response.feedback)
                else:
                    # Try to extract from text
                    import re

                    text = (
                        response.content
                        if hasattr(response, "content")
                        else str(response)
                    )
                    score_match = re.search(
                        r"(?:score:?\s*)?(\d+(?:\.\d+)?)", text.lower()
                    )

                    if score_match:
                        score_value = float(score_match.group(1))
                        # Normalize if needed
                        if score_value > 1:
                            score_value = min(score_value / 10, 1.0)
                        score = Score(value=score_value, feedback=text)
                    else:
                        score = Score(
                            value=0.5, feedback="Could not extract score: " + text
                        )

                # Create scored candidate
                metadata = candidate.metadata if hasattr(candidate, "metadata") else {}
                scored_candidate = ScoredCandidate(
                    candidate=Candidate(content=content, metadata=metadata), score=score
                )

                scored_candidates.append(scored_candidate)

            except Exception as e:
                logger.exception(f"Error scoring candidate: {e}")
                # Add a zero-scored candidate as fallback
                content = (
                    candidate.content
                    if hasattr(candidate, "content")
                    else str(candidate)
                )
                metadata = candidate.metadata if hasattr(candidate, "metadata") else {}

                fallback_score = Score(value=0.0, feedback=f"Error: {e}")
                scored_candidates.append(
                    ScoredCandidate(
                        candidate=Candidate(content=content, metadata=metadata),
                        score=fallback_score,
                    )
                )

        # Update the state with scored candidates and clear original candidates
        return Command(
            update={"scored_candidates": scored_candidates, "candidates": "clear"}
        )

    def _select_best(self, state: TOTState) -> Command:
        """Select the best candidates for the next iteration.

        Args:
            state: Current search state

        Returns:
            Command with best candidate updates
        """
        # Get scored candidates
        scored_candidates = state.scored_candidates

        if not scored_candidates:
            logger.warning("No scored candidates to select from")
            return Command(update={"best_candidate": None}, goto=END)

        # Sort by score
        sorted_candidates = sorted(
            scored_candidates,
            key=lambda c: (
                c.score.value
                if hasattr(c, "score") and hasattr(c.score, "value")
                else 0.0
            ),
            reverse=True,
        )

        # Select the best candidate
        best_candidate = sorted_candidates[0]

        # Get candidates for beam search (top k)
        beam_candidates = sorted_candidates[
            : min(self.beam_width, len(sorted_candidates))
        ]

        # Check if the best candidate exceeds the threshold
        best_score = (
            best_candidate.score.value if hasattr(best_candidate, "score") else 0.0
        )

        solved = best_score >= self.threshold

        # Update the state
        updates = {
            "best_candidate": best_candidate,
            "score": best_score,
            "beam_candidates": beam_candidates,
            "scored_candidates": "clear",
        }

        # If we've found a good solution or reached max depth, prepare the answer
        if solved or state.depth >= self.max_depth:
            best_content = (
                best_candidate.candidate.content
                if hasattr(best_candidate, "candidate")
                else str(best_candidate)
            )

            updates["answer"] = (
                f"Best solution (score: {best_score:.2f}):\n{best_content}"
            )
            updates["search_depth"] = state.depth

            return Command(update=updates, goto=END)

        # Otherwise continue the search with the beam candidates
        return Command(update=updates)

    def _should_continue_search(self, state: TOTState) -> str | END:
        """Decide whether to continue the search.

        Args:
            state: Current search state

        Returns:
            Next node to execute or END
        """
        # End if no candidates or max depth reached
        if not state.candidates or state.depth >= self.max_depth:
            return END

        # Continue to evaluation
        return self.config.evaluator_node

    def _map_beam_expansion(self, state: TOTState) -> END | list[Send]:
        """Map beam candidates to parallel expansion nodes.

        Args:
            state: Current search state

        Returns:
            List of Send commands for parallel expansion or END
        """
        # Get the best score
        best_candidate = state.best_candidate
        if not best_candidate:
            return END

        best_score = (
            best_candidate.score.value if hasattr(best_candidate, "score") else 0.0
        )

        # If we've found a solution that exceeds threshold or reached max depth, end
        if best_score >= self.threshold or state.depth >= self.max_depth:
            return END

        # Use beam search - for each candidate in the beam, create a separate path
        sends = []
        beam_candidates = (
            state.beam_candidates if hasattr(state, "beam_candidates") else []
        )

        for candidate in beam_candidates[: self.beam_width]:
            # Create a Send command for each beam candidate
            candidate_state = {
                "problem": state.problem,
                "current_seed": candidate,  # Set as seed for next generation
                "depth": state.depth,
                "scored_candidates": [],  # Clear scored candidates
                "candidates": [],  # Clear candidates
            }
            sends.append(Send(self.config.generator_node, candidate_state))

        return sends if sends else END

    def _should_expand_or_finish(self, state: TOTState) -> str | END:
        """Decide whether to expand candidates or finish.

        Args:
            state: Current search state

        Returns:
            Next node to execute or END
        """
        # Get the best score
        best_candidate = state.best_candidate
        if not best_candidate:
            return END

        best_score = getattr(
            best_candidate,
            "value",
            getattr(best_candidate.get("score", {}), "value", 0.0),
        )

        # If we've found a solution that exceeds threshold or reached max depth, end
        if best_score >= self.threshold or state.depth >= self.max_depth:
            return END

        # Continue expansion with the best candidate as seed
        return self.config.generator_node
