# haive/core/graph/common/types.py
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, TypeVar, Union

from langchain_core.runnables import RunnableConfig
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.schema.state_schema import StateSchema

# Core type definitions
# CHECK:
NodeLike = TypeVar("NodeLike", bound=Any)
NodeOutput = TypeVar(
    "NodeOutput",
    bound=Union[
        Command, Send, List[Send], str, Type[BaseModel], BaseModel, Dict[str, Any]
    ],
)
StateLike = TypeVar(
    "StateLike", bound=Union[Dict[str, Any], Type[BaseModel], BaseModel, StateSchema]
)
ConfigLike = TypeVar(
    "ConfigLike", bound=Union[RunnableConfig, Dict[str, Any], Type[BaseModel]]
)
NodeCallable = Callable[[StateLike, Optional[ConfigLike]], NodeOutput]
BaseEdge = Union[Tuple[str, str], Tuple[NodeLike, NodeLike]]
StateType = Union[Dict[str, Any], BaseModel, StateSchema]
ConfigType = Union[RunnableConfig, Dict[str, Any], BaseModel]


# Node type enum - moved from BaseGraph to common types
class NodeType(str, Enum):
    """Types of nodes in a graph."""

    ENGINE = "engine"
    AGENT = "agent"
    CALLABLE = "callable"
    TOOL = "tool"
    VALIDATION = "validation"
    # BRANCH = "branch"
    # SEND = "send"
    CUSTOM = "custom"
    SUBGRAPH = "subgraph"
    PARSER = "parser"
