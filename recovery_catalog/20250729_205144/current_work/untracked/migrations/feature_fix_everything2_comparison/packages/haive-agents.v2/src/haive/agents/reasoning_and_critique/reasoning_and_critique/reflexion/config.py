"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    ReflexionConfig: ReflexionConfig implementation.

Functions:
    create_agent: Create Agent functionality.
"""

from collections.abc import Callable
from typing import Any

from agents.reflexion.aug_llms import initial_answer_chain_config, revision_chain_config
from agents.reflexion.models import AnswerQuestion, ReviseAnswer
from agents.reflexion.state import ReflexionState
from agents.reflexion.tools import run_queries
from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import BaseTool
from pydantic import BaseModel


class ReflexionConfig(AgentConfig):
    """Configuration for the Reflexion agent."""

    engines: dict[str, AugLLMConfig] = {
        "responder": initial_answer_chain_config,
        "revisor": revision_chain_config,
    }
    max_iterations: int = 5
    attempts: int = 3
    tools: list[BaseTool | Callable] = [run_queries]
    models: list[BaseModel] = [AnswerQuestion, ReviseAnswer]
    state_schema: BaseModel = ReflexionState

    @classmethod
    def create_agent(cls) -> Any:
        from agents.reflexion.agent import ReflexionAgent

        return ReflexionAgent(config=cls())
