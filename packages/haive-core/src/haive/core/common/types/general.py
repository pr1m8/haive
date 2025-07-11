from collections.abc import Callable, Sequence
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from langchain_core.runnables import RunnableConfig
from langchain_core.tools import BaseTool, BaseToolkit, StructuredTool, Tool
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.common.types.protocols.general_protocols import Nameable
from haive.core.schema.state_schema import StateSchema

# Generic type that can be string, dict with name key, or any object with name attribute
OptionItem = TypeVar("OptionItem", str, dict[str, Any], Nameable)
ToolLike = Sequence[
    Tool | type[BaseTool] | BaseModel | Callable | StructuredTool | BaseToolkit
]

# Core type definitions
# CHECK:
NodeLike = TypeVar("NodeLike", bound=Any)
NodeOutput = TypeVar(
    "NodeOutput",
    bound=Command
    | Send
    | list[Send]
    | str
    | type[BaseModel]
    | BaseModel
    | dict[str, Any]
    | Send,
)
StateLike = TypeVar(
    "StateLike", bound=dict[str, Any] | type[BaseModel] | BaseModel | StateSchema
)
ConfigLike = TypeVar(
    "ConfigLike", bound=RunnableConfig | dict[str, Any] | type[BaseModel]
)
NodeCallable = Callable[[StateLike, ConfigLike | None], NodeOutput]
BaseEdge = Union[tuple[str, str], tuple[NodeLike, NodeLike]]
StateType = Union[dict[str, Any], BaseModel, StateSchema]
ConfigType = Union[RunnableConfig, dict[str, Any], BaseModel]
