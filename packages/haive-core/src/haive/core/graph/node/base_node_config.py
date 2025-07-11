"""Base Node Configuration for V2 Nodes.

This module provides the base configuration class for v2 nodes with
improved type safety and generic support.
"""

from typing import Generic, TypeVar

from pydantic import BaseModel

from haive.core.graph.node.base_config import NodeConfig

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class BaseNodeConfig(NodeConfig, Generic[TInput, TOutput]):
    """Base node config with generic input/output typing support for v2 nodes."""


__all__ = ["BaseNodeConfig", "TInput", "TOutput"]
