# src/haive/core/graph/common/types.py

from typing import Any, Callable, Dict, ForwardRef, Optional, Type, TypeVar, Union

from pydantic import BaseModel

# Type variables for generics
T = TypeVar("T", bound="BaseModel")
C = TypeVar("C", bound=Optional["BaseModel"])

# Common type aliases
StateLike = Union[Type[BaseModel], BaseModel, Dict[str, Any]]
ConfigLike = Union[Type[BaseModel], BaseModel, Dict[str, Any]]
NodeLike = Union[ForwardRef("NodeConfig"), Callable, ForwardRef("BaseGraph")]
BranchLike = Union[ForwardRef("Branch"), Callable[[Dict[str, Any]], Any]]
EdgePair = tuple[str, str]
NodeColorMap = Dict[str, str]
ConditionalEdge = Dict[str, Any]
