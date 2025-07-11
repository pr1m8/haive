"""Core engine abstractions for the Haive framework.

This module provides the base classes and abstractions for all engines in the Haive framework.
Engines are the core components that provide a consistent interface for creating and using
AI components like LLMs, retrievers, vector stores, etc.

The Engine class is a configuration/factory class that produces runnable objects,
not an invokable itself. It standardizes how engines define their input and output
field requirements.
"""

from __future__ import annotations

import json
import logging
import uuid
from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar

from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel, ConfigDict, Field, create_model, field_serializer

# Import registry base
from haive.core.engine.base.protocols import AsyncInvokable, Invokable
from haive.core.engine.base.types import EngineType

logger = logging.getLogger(__name__)

# Type variables with constraints for input/output types
TIn = TypeVar("TIn", str, Dict[str, Any], BaseModel)
TOut = TypeVar("TOut", str, Dict[str, Any], BaseModel, List[Any])


class Engine(ABC, BaseModel, Generic[TIn, TOut]):
    """Abstract base class for all engine configurations.

    Engines are configuration/factory classes that create runtime objects.
    The Engine class itself is not invokable - it produces objects that may be invokable.

    All engine subclasses must implement:
    - get_input_fields() - defining required input fields
    - get_output_fields() - defining produced output fields
    - create_runnable() - creating the actual runtime object
    """

    # Core identification fields
    id: str = Field(
        default_factory=lambda: f"{uuid.uuid4().hex}",
        description="Unique identifier for this engine instance",
    )
    name: str = Field(
        default_factory=lambda: f"engine_{uuid.uuid4().hex[:8]}",
        description="Name of this engine instance",
    )
    engine_type: EngineType = Field(description="Type of engine")
    description: Optional[str] = Field(
        default=None, description="Optional description of this engine"
    )

    # Schema definitions - used only if explicitly provided
    input_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Input schema for this engine", exclude=True
    )
    output_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Output schema for this engine", exclude=True
    )

    # Metadata for serialization
    version: str = Field(
        default="1.0.0", description="Version of this engine configuration"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata for this engine"
    )

    # Configuration for model serialization
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_serializer("engine_type")
    def serialize_engine_type(self, engine_type: EngineType) -> str:
        """Ensure engine_type is serialized as its value, not string representation."""
        return engine_type.value

    @abstractmethod
    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """
        Return input field definitions as field_name -> (type, default) pairs.
        Must be implemented by all engine subclasses.

        This can represent BaseModel fields, dictionary keys, or primitive inputs.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        pass

    @abstractmethod
    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """
        Return output field definitions as field_name -> (type, default) pairs.
        Must be implemented by all engine subclasses.

        This can represent BaseModel fields, dictionary keys, or primitive outputs.

        Returns:
            Dictionary mapping field names to (type, default) tuples
        """
        pass

    @abstractmethod
    def create_runnable(self, runnable_config: Optional[RunnableConfig] = None) -> Any:
        """
        Create a runtime object from this engine config.

        The returned object may implement Invokable/AsyncInvokable,
        but the Engine itself is just a factory/configuration class.

        Args:
            runnable_config: Optional runtime configuration

        Returns:
            A runtime object (e.g., LLM, Retriever, etc.)
        """
        pass

    def get_schema_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """
        Get combined schema fields for this engine.

        Combines the input and output fields from get_input_fields() and
        get_output_fields() into a single dictionary. This is useful for
        generating a comprehensive schema for the engine.

        Returns:
            Dict[str, Tuple[Type, Any]]: Dictionary mapping field names to
                (type, default) tuples.

        Examples:
            >>> engine = MyEngine(name="test_engine", engine_type=EngineType.LLM)
            >>> fields = engine.get_schema_fields()
            >>> print(fields.keys())
            dict_keys(['prompt', 'temperature', 'completion', 'tokens_used'])
        """
        # Combine input and output fields
        fields = {}
        fields.update(self.get_input_fields())
        fields.update(self.get_output_fields())
        return fields

    def derive_input_schema(self) -> Type[BaseModel]:
        """
        Derive input schema for this engine as a Pydantic model.

        Generates a Pydantic model representing the input schema for this
        engine, based on the fields returned by get_input_fields() or
        using the explicitly provided input_schema if available.

        Returns:
            Type[BaseModel]: A Pydantic model class representing the input schema.

        Examples:
            >>> engine = MyEngine(name="test_engine", engine_type=EngineType.LLM)
            >>> InputSchema = engine.derive_input_schema()
            >>> input_data = InputSchema(prompt="Hello, world!", temperature=0.7)
            >>> print(input_data.model_dump())
            {'prompt': 'Hello, world!', 'temperature': 0.7}
        """
        # Use provided schema if available
        if self.input_schema:
            return self.input_schema

        # Get schema fields from abstract method
        fields = self.get_input_fields()

        # Create and return input schema model
        return create_model(f"{self.__class__.__name__}Input", **fields)

    def derive_output_schema(self) -> Type[BaseModel]:
        """
        Derive output schema for this engine as a Pydantic model.

        Generates a Pydantic model representing the output schema for this
        engine, based on the fields returned by get_output_fields() or
        using the explicitly provided output_schema if available.

        Returns:
            Type[BaseModel]: A Pydantic model class representing the output schema.

        Examples:
            >>> engine = MyEngine(name="test_engine", engine_type=EngineType.LLM)
            >>> OutputSchema = engine.derive_output_schema()
            >>> output_data = OutputSchema(completion="Generated text", tokens_used=15)
            >>> print(output_data.model_dump())
            {'completion': 'Generated text', 'tokens_used': 15}
        """
        # Use provided schema if available
        if self.output_schema:
            return self.output_schema

        # Get schema fields from abstract method
        fields = self.get_output_fields()

        # Create and return output schema model
        return create_model(f"{self.__class__.__name__}Output", **fields)

    def instantiate(self, runnable_config: Optional[RunnableConfig] = None) -> Any:
        """
        Instantiate the engine (alias for create_runnable).

        This is a convenience method that provides a more intuitive name for
        the create_runnable method, particularly in contexts where "instantiate"
        is more semantically appropriate than "create_runnable".

        Args:
            runnable_config (Optional[RunnableConfig]): Optional runtime configuration
                to apply when creating the runnable.

        Returns:
            Any: The instantiated runtime object.

        Examples:
            >>> engine = MyEngine(name="test_engine", engine_type=EngineType.LLM)
            >>> llm = engine.instantiate({"temperature": 0.5})
            >>> response = llm.generate("Tell me a joke")
        """
        return self.create_runnable(runnable_config)

    def register(self) -> Engine:
        """
        Register this engine in the global registry.

        Adds this engine instance to the global EngineRegistry, making it
        available for lookup by name, ID, or type. This method is typically
        called after creating an engine to make it available throughout
        the application.

        Returns:
            Engine: Self for method chaining.

        Examples:
            >>> engine = (
            ...     MyEngine(name="gpt-4", engine_type=EngineType.LLM)
            ...     .register()
            ... )
            >>> # The engine is now available in the registry
            >>> from haive.core.engine.base.registry import EngineRegistry
            >>> registry = EngineRegistry.get_instance()
            >>> same_engine = registry.get(EngineType.LLM, "gpt-4")
            >>> engine is same_engine
            True
        """
        from haive.core.engine.base.registry import EngineRegistry

        return EngineRegistry.get_instance().register(self)

    def apply_runnable_config(
        self, runnable_config: Optional[RunnableConfig] = None
    ) -> Dict[str, Any]:
        """
        Extract parameters from runnable_config relevant to this engine.

        Processes the provided runtime configuration to extract parameters
        that apply to this specific engine. The method implements a hierarchical
        lookup strategy, prioritizing more specific configurations (by ID, then name,
        then type) over general ones.

        Args:
            runnable_config (Optional[RunnableConfig]): Runtime configuration dictionary
                containing engine-specific parameters.

        Returns:
            Dict[str, Any]: Dictionary of configuration parameters that apply to this engine.

        Examples:
            >>> engine = MyEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> config = {
            ...     "configurable": {
            ...         "engine_configs": {
            ...             "gpt-4": {"temperature": 0.7},
            ...             "llm_config": {"max_tokens": 1000}
            ...         },
            ...         "temperature": 0.5
            ...     }
            ... }
            >>> params = engine.apply_runnable_config(config)
            >>> # Name-specific config takes priority over engine type config
            >>> params["temperature"]
            0.7
            >>> # Type-specific config is included
            >>> params["max_tokens"]
            1000
        """
        # Return empty dict if no config provided
        if not runnable_config or "configurable" not in runnable_config:
            return {}

        configurable = runnable_config["configurable"]
        params = {}

        # Engine identification - check for direct references using id or name
        if "engine_configs" in configurable:
            # Try by engine ID first (most specific)
            if self.id in configurable["engine_configs"]:
                params.update(configurable["engine_configs"][self.id])

            # Try by engine name if no id match
            elif self.name in configurable["engine_configs"]:
                params.update(configurable["engine_configs"][self.name])

            # Try by engine type if available (least specific)
            engine_type_key = f"{self.engine_type.value}_config"
            if engine_type_key in configurable["engine_configs"]:
                # Don't override existing params
                for k, v in configurable["engine_configs"][engine_type_key].items():
                    if k not in params:
                        params[k] = v

        # Extract parameters that match fields from this engine
        fields = self.model_fields
        for field_name in fields:
            if field_name in configurable and field_name not in params:
                params[field_name] = configurable[field_name]

        return params

    def extract_params(self) -> Dict[str, Any]:
        """
        Extract parameters from this engine for serialization.

        Collects all relevant parameters from this engine instance that should
        be included in serialization or when copying the engine configuration.
        Excludes internal fields, schema definitions, and identity fields.

        Returns:
            Dict[str, Any]: Dictionary of engine parameters suitable for serialization.

        Examples:
            >>> engine = MyLLMEngine(
            ...     name="gpt-4",
            ...     engine_type=EngineType.LLM,
            ...     temperature=0.7,
            ...     max_tokens=1000
            ... )
            >>> params = engine.extract_params()
            >>> # Contains configuration parameters
            >>> params["temperature"]
            0.7
            >>> params["max_tokens"]
            1000
            >>> # Does not contain identity fields
            >>> "name" in params
            False
            >>> "id" in params
            False
        """
        params = {}

        # Get fields from the model
        fields = self.model_fields

        # Add all relevant fields
        for field_name in fields:
            # Skip fields that shouldn't be in params
            if field_name.startswith("_") or field_name in [
                "input_schema",
                "output_schema",
                "id",
                "name",
                "engine_type",
            ]:
                continue

            # Get the value if it exists
            if hasattr(self, field_name):
                value = getattr(self, field_name)
                params[field_name] = value

        return params

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert engine to a dictionary suitable for serialization.

        Creates a complete dictionary representation of this engine that can be
        used for serialization, persistence, or reconstruction. Includes class
        information to allow proper reconstruction of the specific engine type.

        Returns:
            Dict[str, Any]: Dictionary representation of the engine with all necessary
                information for reconstruction.

        Examples:
            >>> engine = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> data = engine.to_dict()
            >>> # Contains the class information for reconstruction
            >>> data["engine_class"]
            'haive.core.engine.llm.my_llm_engine.MyLLMEngine'
            >>> # Serializable to JSON
            >>> import json
            >>> json_str = json.dumps(data)
        """
        # Convert to dictionary using Pydantic
        data = self.model_dump(exclude={"input_schema", "output_schema"})

        # Add schema information if available
        if self.input_schema:
            data["input_schema_name"] = self.input_schema.__name__

        if self.output_schema:
            data["output_schema_name"] = self.output_schema.__name__

        # Add class information for type reconstruction
        data["engine_class"] = f"{self.__class__.__module__}.{self.__class__.__name__}"

        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Engine:
        """
        Create an engine from a dictionary representation.

        Reconstructs an engine instance from its dictionary representation,
        attempting to use the original engine class if available, or falling back
        to the base class if the specific class cannot be loaded.

        Args:
            data (Dict[str, Any]): Dictionary representation of the engine, typically
                created by the to_dict method.

        Returns:
            Engine: The reconstructed engine instance.

        Raises:
            Various exceptions may be raised during dynamic class loading, but these
            are caught and logged, with a fallback to the base class.

        Examples:
            >>> # Create an engine
            >>> original = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> # Convert to dictionary
            >>> data = original.to_dict()
            >>> # Reconstruct from dictionary
            >>> reconstructed = Engine.from_dict(data)
            >>> # Verify it's the same type
            >>> type(reconstructed) == type(original)
            True
        """
        # Extract class information for dynamic loading
        engine_class_path = data.pop("engine_class", None)

        if engine_class_path:
            try:
                # Dynamically load the class
                module_name, class_name = engine_class_path.rsplit(".", 1)
                module = __import__(module_name, fromlist=[class_name])
                engine_cls = getattr(module, class_name)

                # Clean data before instantiation
                for field_name in ["input_schema_name", "output_schema_name"]:
                    if field_name in data:
                        data.pop(field_name)

                # Instantiate the correct class
                return engine_cls(**data)
            except (ImportError, AttributeError, ValueError) as e:
                logger.warning(
                    f"Could not load engine class '{engine_class_path}': {e}"
                )

        # Fallback to instantiating the base class
        return cls(**data)

    def to_json(self) -> str:
        """
        Convert engine to a JSON string representation.

        Serializes this engine to a JSON string that can be stored, transmitted,
        or persisted. The serialization process ensures that all values are
        JSON-compatible.

        Returns:
            str: JSON string representation of the engine.

        Examples:
            >>> engine = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> json_str = engine.to_json()
            >>> # Can be saved to file
            >>> with open("engine_config.json", "w") as f:
            ...     f.write(json_str)
        """
        from haive.core.utils.pydantic_utils import ensure_json_serializable

        data = self.to_dict()
        serializable_data = ensure_json_serializable(data)
        return json.dumps(serializable_data)

    @classmethod
    def from_json(cls, json_str: str) -> Engine:
        """
        Create an engine from a JSON string representation.

        Deserializes an engine from its JSON string representation, reconstructing
        the original engine instance or a compatible instance if the exact class
        is not available.

        Args:
            json_str (str): JSON string representation of the engine, typically
                created by the to_json method.

        Returns:
            Engine: The reconstructed engine instance.

        Examples:
            >>> # Create and serialize an engine
            >>> original = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> json_str = original.to_json()
            >>> # Reconstruct from JSON
            >>> reconstructed = Engine.from_json(json_str)
            >>> reconstructed.name
            'gpt-4'
            >>> reconstructed.engine_type
            <EngineType.LLM: 'llm'>
        """
        data = json.loads(json_str)
        return cls.from_dict(data)

    def with_config_overrides(self, overrides: Dict[str, Any]) -> "Engine":
        """
        Create a new engine with configuration overrides applied.

        Creates a new instance of this engine with the specified configuration
        overrides applied. This is useful for creating variations of an engine
        without modifying the original instance.

        Args:
            overrides (Dict[str, Any]): Dictionary of configuration overrides to apply.
                Only keys that exist in the engine's configuration will be applied.

        Returns:
            Engine: A new engine instance with the overrides applied.

        Examples:
            >>> original = MyLLMEngine(
            ...     name="gpt-4",
            ...     engine_type=EngineType.LLM,
            ...     temperature=0.7
            ... )
            >>> # Create a variation with different temperature
            >>> variation = original.with_config_overrides({"temperature": 0.3})
            >>> # Original is unchanged
            >>> original.temperature
            0.7
            >>> # New instance has override applied
            >>> variation.temperature
            0.3
            >>> # Other properties remain the same
            >>> variation.name
            'gpt-4'
        """
        # Create a copy of this engine
        config = self.model_dump()

        # Apply overrides
        for key, value in overrides.items():
            if key in config:
                config[key] = value

        # Create new instance
        return self.__class__.model_validate(config)


class InvokableEngine(Engine[TIn, TOut]):
    """
    Base class for engines that create invokable runtime objects.

    This class extends the base Engine with convenience methods for directly
    invoking the runnable objects created by the engine. While the engine itself
    is not directly invokable (it's a factory/configuration), these methods
    create the runnable and invoke it in a single operation.

    Examples of invokable engines include LLMs, Retrievers, and VectorStores,
    which all create components that can process input data and return output data.

    Type Parameters:
        TIn: The input type for the runnable.
        TOut: The output type from the runnable.

    Examples:
        >>> class MyLLMEngine(InvokableEngine[str, str]):
        ...     engine_type = EngineType.LLM
        ...     # Engine implementation...
        ...
        >>> engine = MyLLMEngine(name="gpt-4")
        >>> # Direct invocation without creating the runnable separately
        >>> response = engine.invoke("Tell me a joke")
        >>> print(response)
        'Why did the programmer go broke? Because he lost his domain in a crash!'
    """

    def invoke(
        self, input_data: TIn, runnable_config: Optional[RunnableConfig] = None
    ) -> TOut:
        """
        Convenience method to create and invoke the runnable with input data.

        Creates a runnable instance using create_runnable() and immediately invokes
        it with the provided input data. This is a shortcut that combines creation
        and invocation into a single method call.

        Args:
            input_data (TIn): Input data for the runnable to process.
            runnable_config (Optional[RunnableConfig]): Optional runtime configuration
                to apply when creating and invoking the runnable.

        Returns:
            TOut: Output from the runnable after processing the input data.

        Raises:
            NotImplementedError: If the created runnable does not support invocation.
            Various exceptions may be propagated from the runnable's invoke method.

        Examples:
            >>> engine = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> # Direct invocation with configuration
            >>> response = engine.invoke(
            ...     "Generate a poem about AI",
            ...     {"configurable": {"temperature": 0.8}}
            ... )
        """
        # Create runnable
        runnable = self.create_runnable(runnable_config)

        # Use direct invokable interface if available
        if isinstance(runnable, Invokable):
            return runnable.invoke(input_data, config=runnable_config)

        # Call with config if supported
        if callable(runnable):
            try:
                import inspect

                sig = inspect.signature(runnable)
                if "config" in sig.parameters:
                    return runnable(input_data, config=runnable_config)
                return runnable(input_data)
            except Exception as e:
                logger.error(f"Error invoking runnable: {e}")
                raise

        raise NotImplementedError(
            f"Engine {self.name} creates a runnable that does not support invoke"
        )

    async def ainvoke(
        self, input_data: TIn, runnable_config: Optional[RunnableConfig] = None
    ) -> TOut:
        """
        Convenience method to create and asynchronously invoke the runnable.

        Creates a runnable instance using create_runnable() and immediately invokes
        it asynchronously with the provided input data. If the runnable doesn't
        support asynchronous invocation natively, this method will run it in a
        separate thread.

        Args:
            input_data (TIn): Input data for the runnable to process.
            runnable_config (Optional[RunnableConfig]): Optional runtime configuration
                to apply when creating and invoking the runnable.

        Returns:
            TOut: Output from the runnable after processing the input data.

        Raises:
            NotImplementedError: If the created runnable cannot be invoked asynchronously.
            Various exceptions may be propagated from the runnable's ainvoke method.

        Examples:
            >>> engine = MyLLMEngine(name="gpt-4", engine_type=EngineType.LLM)
            >>> # Usage in an async context
            >>> async def generate():
            ...     response = await engine.ainvoke("What is the capital of France?")
            ...     print(response)
            >>> # 'The capital of France is Paris.'
        """
        # Create runnable
        runnable = self.create_runnable(runnable_config)

        # Use async invokable interface if available
        if isinstance(runnable, AsyncInvokable):
            return await runnable.ainvoke(input_data, config=runnable_config)

        # Use asyncio to run in thread if not async
        import asyncio

        if callable(runnable):
            try:
                import inspect

                sig = inspect.signature(runnable)
                if "config" in sig.parameters:
                    return await asyncio.to_thread(
                        runnable, input_data, config=runnable_config
                    )
                return await asyncio.to_thread(runnable, input_data)
            except Exception as e:
                logger.error(f"Error invoking runnable asynchronously: {e}")
                raise

        raise NotImplementedError(
            f"Engine {self.name} creates a runnable that does not support ainvoke"
        )


class NonInvokableEngine(Engine[TIn, TOut]):
    """
    Base class for engines that create non-invokable utility objects.

    This class is used for engines that create utility objects which don't
    follow the standard input-to-output invocation pattern. These engines
    typically provide specialized functionality that doesn't fit the
    Invokable/AsyncInvokable protocol.

    Examples include:
    - Embeddings engines that convert text to vectors
    - DocumentLoader engines that load documents from external sources
    - DocumentTransformer engines that transform document structure
    - DocumentSplitter engines that split documents into chunks

    Type Parameters:
        TIn: The input type for the configuration.
        TOut: The output type from the configuration.

    Examples:
        >>> class EmbeddingsEngine(NonInvokableEngine[Dict[str, Any], Any]):
        ...     engine_type = EngineType.EMBEDDINGS
        ...     # Engine implementation...
        ...
        >>> engine = EmbeddingsEngine(name="text-embedding-ada-002")
        >>> embeddings = engine.create_runnable()
        >>> # Use the embeddings object directly with its specific methods
        >>> vectors = embeddings.embed_documents(["Hello, world!"])
    """

    pass
