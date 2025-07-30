"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    ToTAgent: ToTAgent implementation.

Functions:
    get_state_value: Get State Value functionality.
    setup_workflow: Setup Workflow functionality.
"""

import logging
from typing import Any

from agents.tot.modular.branches import ToTBranch
from agents.tot.modular.config import ToTAgentConfig
from agents.tot.modular.models import Candidate, CandidateList, CandidateScore
from agents.tot.modular.state import ToTState
from haive.core.engine.agent.agent import Agent, register_agent
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.types import Command
from pydantic import BaseModel

logger = logging.getLogger(__name__)


@register_agent(ToTAgentConfig)
class ToTAgent(Agent[ToTAgentConfig]):

    def get_state_value(self, state: dict | BaseModel, key: str, default=None):
        return (
            state.get(key, default)
            if isinstance(state, dict)
            else getattr(state, key, default)
        )

    def setup_workflow(self) -> None:
        logger.debug(f"Setting up workflow for ToTAgent {self.config.name}")
        gb = DynamicGraph(state_schema=self.state_schema)

        gb.add_node(name=self.config.expand_node_name, config=self._create_expand_node)
        gb.add_node(name=self.config.score_node_name, config=self._create_score_node)
        gb.add_node(name=self.config.prune_node_name, config=self._create_prune_node)

        gb.add_edge(self.config.expand_node_name, self.config.score_node_name)
        gb.add_edge(self.config.score_node_name, self.config.prune_node_name)

        gb.add_conditional_edges(
            self.config.prune_node_name, condition_or_branch=ToTBranch(self)
        )

        gb.set_entry_point(self.config.expand_node_name)
        self.graph = gb.build()
        self.compile()

    def _create_expand_node(self, state):
        logger.debug("Running expand node")
        k = self.config.candidates_per_expansion
        seed = self.get_state_value(state, "current_seed")
        seed_str = (
            seed["content"] if isinstance(seed, dict) else getattr(seed, "content", "")
        )

        try:
            if self.config.expand_llm_config.structured_output_model is None:
                self.config.expand_llm_config.structured_output_model = CandidateList

            expand_llm = self.config.expand_llm_config.create_runnable()
            problem = self.get_state_value(state, "problem")

            result = expand_llm.invoke(
                {"problem": problem, "seed": seed_str, "candidates_per_expansion": k}
            )

            candidates = []
            if isinstance(result, CandidateList):
                candidates = [
                    Candidate(content=item.content) for item in result.candidates[:k]
                ]
            elif isinstance(result, dict):
                for item in result.get("candidates", [])[:k]:
                    content = (
                        item.get("content")
                        if isinstance(item, dict)
                        else getattr(item, "content", None)
                    )
                    if content:
                        candidates.append(Candidate(content=content))
            elif isinstance(result, str):
                candidates = [Candidate(content=result)]

            if not candidates:
                candidates = [Candidate(content="No viable candidates generated.")]

            return Command(update={"candidates": candidates})

        except Exception as e:
            logger.exception(f"Error in expand node: {e}")
            messages = self.get_state_value(state, "messages", [])
            return Command(
                update={
                    "messages": [
                        *messages,
                        AIMessage(content=f"Error generating candidates: {e}"),
                    ],
                    "candidates": [Candidate(content="Expansion failed")],
                }
            )

    def _create_score_node(self, state):
        logger.debug("Running score node")
        problem = self.get_state_value(state, "problem")
        candidates = self.get_state_value(state, "candidates", [])
        scored = []

        try:
            if self.config.score_function:
                for c in candidates:
                    content = c["content"] if isinstance(c, dict) else c.content
                    score, feedback = self.config.score_function(problem, content)
                    scored.append(
                        Candidate(content=content, score=score, feedback=feedback)
                    )

            elif self.config.score_llm_config:
                if self.config.score_llm_config.structured_output_model is None:
                    self.config.score_llm_config.structured_output_model = (
                        CandidateScore
                    )
                score_llm = self.config.score_llm_config.create_runnable()

                for c in candidates:
                    content = c["content"] if isinstance(c, dict) else c.content
                    res = score_llm.invoke({"problem": problem, "candidate": content})
                    score = getattr(res, "score", res.get("score", 0.0))
                    feedback = getattr(res, "feedback", res.get("feedback", ""))
                    scored.append(
                        Candidate(content=content, score=score, feedback=feedback)
                    )

            else:
                import random

                for c in candidates:
                    content = c["content"] if isinstance(c, dict) else c.content
                    scored.append(
                        Candidate(
                            content=content,
                            score=random.random(),
                            feedback="No scoring method.",
                        )
                    )

            return Command(update={"candidates": "clear", "scored_candidates": scored})

        except Exception as e:
            logger.exception(f"Error scoring candidates: {e}")
            messages = self.get_state_value(state, "messages", [])
            fallback = [
                Candidate(
                    content=c.get("content") if isinstance(c, dict) else c.content,
                    score=0.1,
                    feedback="Error scoring",
                )
                for c in candidates
            ]
            return Command(
                update={
                    "messages": [*messages, AIMessage(content=f"Scoring error: {e}")],
                    "candidates": "clear",
                    "scored_candidates": fallback,
                }
            )

    def _create_prune_node(self, state):
        logger.debug("Running prune node")
        scored = self.get_state_value(state, "scored_candidates", [])
        depth = self.get_state_value(state, "depth", 0)

        sorted_candidates = sorted(
            scored,
            key=lambda c: (
                c.get("score", 0.0) if isinstance(c, dict) else getattr(c, "score", 0.0)
            ),
            reverse=True,
        )

        beam_size = self.config.beam_size
        pruned = sorted_candidates[:beam_size]
        best = pruned[0] if pruned else None

        return Command(
            update={
                "scored_candidates": "clear",
                "candidates": pruned,
                "best_candidate": best,
                "depth": depth + 1,
            }
        )

    def run(self, input_data: str | dict[str, Any], **kwargs) -> dict[str, Any]:
        if isinstance(input_data, str):
            msg = HumanMessage(content=input_data)
            state = ToTState(
                problem=input_data,
                messages=[msg],
                depth=0,
                max_depth=self.config.max_depth,
            ).model_dump()
        else:
            state = input_data.copy()
            if "problem" not in state:
                for msg in state.get("messages", []):
                    if getattr(msg, "type", None) == "human":
                        state["problem"] = getattr(msg, "content", "")
                        break
            state.setdefault("depth", 0)
            state.setdefault("max_depth", self.config.max_depth)

        kwargs.setdefault("config", self.config.runnable_config)
        return super().run(state, **kwargs)
