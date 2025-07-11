from collections.abc import Callable, Sequence
from typing import Optional, Protocol, Type, Union

from haive.agents.base.agent import Agent
from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools.base import BaseToolkit
from pydantic import BaseModel

from haive.core.engine.base import Engine

# ============================================================================
# Engine Protocol
# ============================================================================


class EngineAware(Protocol):
    """Protocol for objects that have an engine attribute."""

    engine: Engine | None


class ToolAware(Protocol):
    """Protocol for objects that have a tool attribute."""

    tools: Sequence[
        type[BaseTool]
        | type[BaseModel]
        | Callable
        | StructuredTool
        | BaseModel
        | BaseToolkit
    ]


class AgentAware(Protocol):
    """Protocol for objects that have an agent attribute."""

    agent: Agent | None
