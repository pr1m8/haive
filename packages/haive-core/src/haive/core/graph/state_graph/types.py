# src/haive/core/graph/common/types.py

from collections.abc import Callable
from typing import Any, Dict, ForwardRef, Optional, Type, TypeVar, Union

from pydantic import BaseModel

# Type variables for generics
T = TypeVar("T", bound="BaseModel")
C = TypeVar("C", bound=Optional["BaseModel"])

# Common type aliases
StateLike = Union[type[BaseModel], BaseModel, dict[str, Any]]
ConfigLike = Union[type[BaseModel], BaseModel, dict[str, Any]]
NodeLike = Union[ForwardRef("NodeConfig"), Callable, ForwardRef("BaseGraph")]
BranchLike = Union[ForwardRef("Branch"), Callable[[dict[str, Any]], Any]]
EdgePair = tuple[str, str]
NodeColorMap = dict[str, str]
ConditionalEdge = dict[str, Any]
