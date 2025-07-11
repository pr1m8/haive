"""Generic Agent Base Class with Enhanced Typing and Auto-Configuration.

This module provides a generic agent base class that addresses key pain points:
- Type-safe generic parameters for input/output types
- Automatic schema generation using __init_subclass__ patterns
- Enhanced adaptability between different agent types
- Simplified node integration via universal adapter
- Better I/O schema handling with type hints
"""

import logging
from abc import ABC
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generic,
    Optional,
    Type,
    TypeVar,
    Union,
    get_type_hints,
)

from haive.core.engine.base import Engine, EngineType

# Import schema and typing utilities
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, Field

# Import base agent components
from .agent import Agent

logger = logging.getLogger(__name__)

# Generic type variables for input/output types
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)
TState = TypeVar("TState", bound=BaseModel)


# Default schemas for agents that don't specify types
class DefaultAgentInput(BaseModel):
    """Default input schema for generic agents."""

    messages: list[Any] = Field(default_factory=list, description="Input messages")


class DefaultAgentOutput(BaseModel):
    """Default output schema for generic agents."""

    messages: list[Any] = Field(default_factory=list, description="Output messages")


class DefaultAgentState(BaseModel):
    """Default state schema for generic agents."""

    messages: list[Any] = Field(default_factory=list, description="State messages")


class GenericAgent(Agent, Generic[TInput, TOutput, TState]):
    """Generic agent base class with enhanced typing and auto-configuration.

    This class extends the base Agent with:
    - Generic type parameters for type-safe I/O
    - Automatic schema generation from type hints
    - __init_subclass__ patterns for auto-configuration
    - Universal adapter compatibility
    - Enhanced adaptability between agent types

    Type Parameters:
        TInput: Input data type (must be BaseModel subclass)
        TOutput: Output data type (must be BaseModel subclass)
        TState: State data type (must be BaseModel subclass)

    Example:
        # Define custom schemas
        class MyInput(BaseModel):
            query: str
            context: Optional[str] = None

        class MyOutput(BaseModel):
            answer: str
            confidence: float

        class MyState(BaseModel):
            messages: list[BaseMessage] = []
            query: str = ""
            answer: str = ""

        # Create typed agent
        class MyAgent(GenericAgent[MyInput, MyOutput, MyState]):
            def build_graph(self) -> BaseGraph:
                # Build workflow graph
                return my_graph

        # Agent automatically gets proper typing and schemas
        agent = MyAgent(name="my_agent", engine=my_llm)
        result: MyOutput = agent.invoke(MyInput(query="test"))
    """

    # Class-level type registries for subclass configuration
    _input_type: ClassVar[type[BaseModel] | None] = None
    _output_type: ClassVar[type[BaseModel] | None] = None
    _state_type: ClassVar[type[BaseModel] | None] = None
    _auto_configure: ClassVar[bool] = True

    # Enhanced type annotations for schemas
    input_schema: type[TInput] | None = Field(
        default=None, description="Typed input schema derived from generic parameters"
    )
    output_schema: type[TOutput] | None = Field(
        default=None, description="Typed output schema derived from generic parameters"
    )
    state_schema: type[TState] | None = Field(
        default=None, description="Typed state schema derived from generic parameters"
    )

    def __init_subclass__(cls, auto_configure: bool = True, **kwargs):
        """Automatic configuration of agent subclasses using __init_subclass__.

        This method:
        1. Extracts type parameters from Generic[TInput, TOutput, TState]
        2. Automatically sets schema types based on generics
        3. Configures default behaviors for the agent class
        4. Sets up universal adapter compatibility

        Args:
            auto_configure: Whether to automatically configure schemas and adapters
            **kwargs: Additional configuration options
        """
        super().__init_subclass__(**kwargs)

        if not auto_configure:
            cls._auto_configure = False
            return

        logger.debug(f"Auto-configuring agent subclass: {cls.__name__}")

        try:
            # Extract generic type parameters from class
            cls._extract_generic_types()

            # Auto-configure schemas based on type parameters
            cls._auto_configure_schemas()

            # Set up adapter compatibility
            cls._setup_adapter_compatibility()

            # Configure engine integration patterns
            cls._configure_engine_integration()

            logger.debug(f"✅ Auto-configuration complete for {cls.__name__}")

        except Exception as e:
            logger.warning(f"Auto-configuration failed for {cls.__name__}: {e}")
            # Don't fail - allow manual configuration

    @classmethod
    def _extract_generic_types(cls) -> None:
        """Extract type parameters from Generic[TInput, TOutput, TState]."""
        # Get the original bases to find Generic parameters
        for base in getattr(cls, "__orig_bases__", []):
            if hasattr(base, "__origin__") and base.__origin__ is GenericAgent:
                if hasattr(base, "__args__") and len(base.__args__) >= 3:
                    cls._input_type = base.__args__[0]
                    cls._output_type = base.__args__[1]
                    cls._state_type = base.__args__[2]

                    logger.debug(f"Extracted types for {cls.__name__}:")
                    logger.debug(
                        f"  Input: {cls._input_type.__name__ if cls._input_type else None}"
                    )
                    logger.debug(
                        f"  Output: {cls._output_type.__name__ if cls._output_type else None}"
                    )
                    logger.debug(
                        f"  State: {cls._state_type.__name__ if cls._state_type else None}"
                    )
                    return

        # Fallback to type hints on the class
        try:
            hints = get_type_hints(cls)
            cls._input_type = hints.get("input_schema")
            cls._output_type = hints.get("output_schema")
            cls._state_type = hints.get("state_schema")
        except Exception as e:
            logger.debug(f"Could not extract type hints from {cls.__name__}: {e}")

    @classmethod
    def _auto_configure_schemas(cls) -> None:
        """Automatically configure schema fields based on extracted types."""
        if cls._input_type and cls._input_type != DefaultAgentInput:
            logger.debug(f"Setting input_schema to {cls._input_type.__name__}")
            # We'll set this in the model validator

        if cls._output_type and cls._output_type != DefaultAgentOutput:
            logger.debug(f"Setting output_schema to {cls._output_type.__name__}")
            # We'll set this in the model validator

        if cls._state_type and cls._state_type != DefaultAgentState:
            logger.debug(f"Setting state_schema to {cls._state_type.__name__}")
            # We'll set this in the model validator

    @classmethod
    def _setup_adapter_compatibility(cls) -> None:
        """Set up compatibility with universal adapter system."""
        # Add methods that the universal adapter can detect
        if not hasattr(cls, "_adapter_compatible"):
            cls._adapter_compatible = True

        # Ensure the class can be detected as an agent
        if not hasattr(cls, "engine_type"):
            cls.engine_type = EngineType.AGENT

    @classmethod
    def _configure_engine_integration(cls) -> None:
        """Configure automatic engine integration patterns."""
        # Set up automatic engine discovery from type hints
        try:
            hints = get_type_hints(cls)

            # Look for engine field annotations
            for field_name, field_type in hints.items():
                if (
                    hasattr(field_type, "__origin__")
                    and field_type.__origin__ in (dict, dict)
                    and len(getattr(field_type, "__args__", [])) >= 2
                ):

                    args = field_type.__args__
                    if (
                        args[0] == str
                        and hasattr(args[1], "__bases__")
                        and any(
                            Engine in getattr(base, "__mro__", [])
                            for base in args[1].__bases__
                        )
                    ):

                        logger.debug(
                            f"Found engine field {field_name} in {cls.__name__}"
                        )

        except Exception as e:
            logger.debug(f"Engine integration setup failed for {cls.__name__}: {e}")

    def setup_agent(self) -> None:
        """Enhanced setup hook that includes generic type configuration."""
        # Call parent setup first
        super().setup_agent()

        # Apply generic type-based schema configuration
        self._apply_generic_schemas()

        # Set up type-safe adapters
        self._setup_type_adapters()

    def _apply_generic_schemas(self) -> None:
        """Apply schemas based on generic type parameters."""
        cls = self.__class__

        # Set input schema from generic type if not already set
        if not self.input_schema and cls._input_type:
            self.input_schema = cls._input_type
            logger.debug(f"Applied generic input schema: {cls._input_type.__name__}")

        # Set output schema from generic type if not already set
        if not self.output_schema and cls._output_type:
            self.output_schema = cls._output_type
            logger.debug(f"Applied generic output schema: {cls._output_type.__name__}")

        # Set state schema from generic type if not already set
        if not self.state_schema and cls._state_type:
            self.state_schema = cls._state_type
            logger.debug(f"Applied generic state schema: {cls._state_type.__name__}")

        # Apply defaults if no types were specified
        if not self.input_schema:
            self.input_schema = DefaultAgentInput

        if not self.output_schema:
            self.output_schema = DefaultAgentOutput

        if not self.state_schema:
            self.state_schema = DefaultAgentState

    def _setup_type_adapters(self) -> None:
        """Set up adapters for type-safe conversion."""
        # Add methods that adapters can use for type conversion
        self._input_adapter = self._create_input_adapter()
        self._output_adapter = self._create_output_adapter()

    def _create_input_adapter(self) -> Callable[..., Any] | None:
        """Create adapter for converting input data to typed format."""
        if not self.input_schema:
            return None

        def adapt_input(data: Any) -> TInput:
            """Adapt input data to the required input type."""
            if isinstance(data, self.input_schema):
                return data
            if isinstance(data, dict):
                return self.input_schema(**data)
            if hasattr(data, "model_dump"):
                return self.input_schema(**data.model_dump())
            else:
                # Try to wrap in a generic field
                return self.input_schema(value=data)

        return adapt_input

    def _create_output_adapter(self) -> Callable[..., Any] | None:
        """Create adapter for converting output data to typed format."""
        if not self.output_schema:
            return None

        def adapt_output(data: Any) -> TOutput:
            """Adapt output data to the required output type."""
            if isinstance(data, self.output_schema):
                return data
            if isinstance(data, dict):
                return self.output_schema(**data)
            if hasattr(data, "model_dump"):
                return self.output_schema(**data.model_dump())
            else:
                # Try to wrap in a generic field
                return self.output_schema(value=data)

        return adapt_output

    def invoke(
        self,
        input_data: TInput | dict | Any,
        config: RunnableConfig | None = None,
    ) -> TOutput:
        """Type-safe invoke method with automatic input/output conversion.

        Args:
            input_data: Input data (automatically converted to TInput type)
            config: Optional runtime configuration

        Returns:
            Typed output data (TOutput)
        """
        # Convert input to proper type
        if self._input_adapter and not isinstance(input_data, self.input_schema):
            try:
                typed_input = self._input_adapter(input_data)
            except Exception as e:
                logger.warning(f"Input adapter failed, using raw input: {e}")
                typed_input = input_data
        else:
            typed_input = input_data

        # Call parent invoke
        result = super().invoke(typed_input, config)

        # Convert output to proper type
        if self._output_adapter and not isinstance(result, self.output_schema):
            try:
                typed_output = self._output_adapter(result)
                return typed_output
            except Exception as e:
                logger.warning(f"Output adapter failed, returning raw result: {e}")

        return result

    async def ainvoke(
        self, input_data: TInput | dict | Any, config: dict | None = None
    ) -> TOutput:
        """Type-safe async invoke method with automatic input/output conversion.

        Args:
            input_data: Input data (automatically converted to TInput type)
            config: Optional runtime configuration

        Returns:
            Typed output data (TOutput)
        """
        # Convert input to proper type
        if self._input_adapter and not isinstance(input_data, self.input_schema):
            try:
                typed_input = self._input_adapter(input_data)
            except Exception as e:
                logger.warning(f"Input adapter failed, using raw input: {e}")
                typed_input = input_data
        else:
            typed_input = input_data

        # Call parent ainvoke
        result = await super().ainvoke(typed_input, config)

        # Convert output to proper type
        if self._output_adapter and not isinstance(result, self.output_schema):
            try:
                typed_output = self._output_adapter(result)
                return typed_output
            except Exception as e:
                logger.warning(f"Output adapter failed, returning raw result: {e}")

        return result

    def create_input_instance(self, **kwargs) -> TInput:
        """Create a typed input instance with the provided data.

        Args:
            **kwargs: Field values for the input schema

        Returns:
            Typed input instance
        """
        if not self.input_schema:
            raise ValueError("No input schema defined")
        return self.input_schema(**kwargs)

    def create_output_instance(self, **kwargs) -> TOutput:
        """Create a typed output instance with the provided data.

        Args:
            **kwargs: Field values for the output schema

        Returns:
            Typed output instance
        """
        if not self.output_schema:
            raise ValueError("No output schema defined")
        return self.output_schema(**kwargs)

    def create_state_instance(self, **kwargs) -> TState:
        """Create a typed state instance with the provided data.

        Args:
            **kwargs: Field values for the state schema

        Returns:
            Typed state instance
        """
        if not self.state_schema:
            raise ValueError("No state schema defined")
        return self.state_schema(**kwargs)

    def get_type_info(self) -> dict[str, Any]:
        """Get information about the agent's type parameters and schemas.

        Returns:
            Dictionary with type information
        """
        cls = self.__class__
        return {
            "agent_class": cls.__name__,
            "generic_types": {
                "input": cls._input_type.__name__ if cls._input_type else None,
                "output": cls._output_type.__name__ if cls._output_type else None,
                "state": cls._state_type.__name__ if cls._state_type else None,
            },
            "schemas": {
                "input": self.input_schema.__name__ if self.input_schema else None,
                "output": self.output_schema.__name__ if self.output_schema else None,
                "state": self.state_schema.__name__ if self.state_schema else None,
            },
            "auto_configured": cls._auto_configure,
            "adapter_compatible": getattr(cls, "_adapter_compatible", False),
        }

    def is_compatible_with(self, other: "GenericAgent") -> bool:
        """Check if this agent is compatible with another agent for chaining.

        Args:
            other: Another generic agent to check compatibility with

        Returns:
            True if agents can be chained (output -> input compatibility)
        """
        if not self.output_schema or not other.input_schema:
            return False

        # Check if output schema fields are compatible with input schema
        try:
            # Get field names and types
            output_fields = self.output_schema.model_fields
            input_fields = other.input_schema.model_fields

            # Check if all required input fields can be satisfied by output
            for field_name, field_info in input_fields.items():
                if field_info.is_required() and field_name not in output_fields:
                    return False

            return True

        except Exception as e:
            logger.debug(f"Compatibility check failed: {e}")
            return False

    def create_adapter_for(self, target: "GenericAgent") -> Callable[..., Any] | None:
        """Create an adapter function for compatibility with another agent.

        Args:
            target: Target agent to create adapter for

        Returns:
            Adapter function that converts this agent's output to target's input
        """
        if not self.is_compatible_with(target):
            return None

        def adapter(output_data: TOutput) -> Any:
            """Adapt output from source agent to input for target agent."""
            if hasattr(output_data, "model_dump"):
                output_dict = output_data.model_dump()
            else:
                output_dict = dict(output_data)

            # Filter to only include fields that target needs
            input_fields = target.input_schema.model_fields
            filtered_data = {k: v for k, v in output_dict.items() if k in input_fields}

            return target.create_input_instance(**filtered_data)

        return adapter

    def __repr__(self) -> str:
        """Enhanced string representation with type information."""
        cls = self.__class__
        type_info = ""
        if cls._input_type and cls._output_type:
            type_info = f"[{cls._input_type.__name__}, {cls._output_type.__name__}]"

        return f"{cls.__name__}{type_info}(name='{self.name}', engines={len(self.engines)})"


# Convenience functions for creating generic agents


def create_typed_agent(
    input_type: type[TInput],
    output_type: type[TOutput],
    state_type: type[TState] | None = None,
    name: str = "TypedAgent",
) -> type[GenericAgent[TInput, TOutput, TState]]:
    """Create a generic agent class with specified types.

    Args:
        input_type: Input schema type
        output_type: Output schema type
        state_type: State schema type (optional)
        name: Class name for the agent

    Returns:
        Generic agent class with specified types
    """
    if state_type is None:
        state_type = DefaultAgentState

    class TypedAgent(GenericAgent[input_type, output_type, state_type]):
        pass

    TypedAgent.__name__ = name
    TypedAgent.__qualname__ = name

    return TypedAgent


def auto_type_agent(agent_class: type) -> type[GenericAgent]:
    """Automatically add generic typing to an existing agent class.

    Args:
        agent_class: Existing agent class to enhance

    Returns:
        Generic agent class with auto-detected types
    """
    # Try to detect schemas from the class
    hints = get_type_hints(agent_class)

    input_type = hints.get("input_schema", DefaultAgentInput)
    output_type = hints.get("output_schema", DefaultAgentOutput)
    state_type = hints.get("state_schema", DefaultAgentState)

    # Create new generic class
    class AutoTypedAgent(
        GenericAgent[input_type, output_type, state_type], agent_class
    ):
        pass

    AutoTypedAgent.__name__ = f"Generic{agent_class.__name__}"
    AutoTypedAgent.__qualname__ = f"Generic{agent_class.__name__}"

    return AutoTypedAgent
