from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
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
OptionItem = TypeVar("OptionItem", str, Dict[str, Any], Nameable)
ToolLike = Sequence[
    Union[Tool, Type[BaseTool], BaseModel, Callable, StructuredTool, BaseToolkit]
]
# NodeLike = Union[Callable]

# Core type definitions
# CHECK:
# NodeLike = Union[Callable[[StateLike, Optional[ConfigLike]], NodeOutput],NodeConfig]
NodeLike = TypeVar("NodeLike", bound=Any)
NodeOutput = TypeVar(
    "NodeOutput",
    bound=Union[
        Command, Send, List[Send], str, Type[BaseModel], BaseModel, Dict[str, Any], Send
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
