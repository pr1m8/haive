from typing import (
    Any,
    Callable,
    Dict,
    Optional,
    Protocol,
    Sequence,
    Type,
    Union,
    runtime_checkable,
)

from langchain_core.tools import BaseTool, StructuredTool
from langchain_core.tools.base import BaseToolkit
from pydantic import BaseModel

from haive.core.engine.agent.agent import Agent
from haive.core.engine.base import Engine

# ============================================================================
# Group 1: Input and Output Schema Protocol
# ============================================================================


@runtime_checkable
class IOSchemaAware(Protocol):
    """Protocol for objects that have input/output schemas"""

    input_schema: Optional[Type[BaseModel]]
    output_schema: Optional[Type[BaseModel]]


# ============================================================================
# Group 2: State Schema Protocol
# ============================================================================


@runtime_checkable
class StateSchemaAware(Protocol):
    """Protocol for objects that have state schema"""

    state_schema: Optional[Type[BaseModel]]


# ============================================================================
# Group 3: Combined Schema Protocol (inherits from both)
# ============================================================================


@runtime_checkable
class FullSchemaAware(IOSchemaAware, StateSchemaAware, Protocol):
    """Protocol for objects that have all schema types"""

    # Inherits:
    # - input_schema: Optional[Type[BaseModel]]
    # - output_schema: Optional[Type[BaseModel]]
    # - state_schema: Optional[Type[BaseModel]]
    pass


# ============================================================================
# Group 4: Input and Output Fields Protocol
# ============================================================================


@runtime_checkable
class IOFieldAware(Protocol):
    """Protocol for objects that can provide input/output field definitions"""

    def get_input_fields(self) -> Dict[str, Any]:
        """Get input field definitions"""
        ...

    def get_output_fields(self) -> Dict[str, Any]:
        """Get output field definitions"""
        ...


# ============================================================================
# Group 5: Complete Protocol (combines schemas + fields)
# ============================================================================


@runtime_checkable
class CompleteSchemaAware(FullSchemaAware, IOFieldAware, Protocol):
    """Protocol for objects that have both schemas and field methods"""

    # Inherits from FullSchemaAware:
    # - input_schema: Optional[Type[BaseModel]]
    # - output_schema: Optional[Type[BaseModel]]
    # - state_schema: Optional[Type[BaseModel]]

    # Inherits from IOFieldAware:
    # - get_input_fields(self) -> Dict[str, Any]
    # - get_output_fields(self) -> Dict[str, Any]
    pass
