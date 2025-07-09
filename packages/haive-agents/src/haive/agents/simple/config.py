"""Configuration for SimpleAgent with comprehensive schema handling.

This module defines the configuration class for SimpleAgent with explicit
input/output schema support, schema composition integration, and improved
mapping capabilities.
"""

import logging
import uuid
from datetime import datetime

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.state_schema import StateSchema
from langchain_core.messages import SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field, field_validator

# Setup logging
logger = logging.getLogger(__name__)


class SimpleAgentConfig(AgentConfig):
    """Configuration for a simple single-node agent with comprehensive schema handling.

    This config supports:
    - Explicit input/output schemas
    - Auto-derived state schema
    - Structured output models
    - Intelligent input/output mappings
    """

    # Required engine (must be AugLLMConfig)
    engine: AugLLMConfig = Field(
        default_factory=AugLLMConfig,
        description="The AugLLM engine to use for reasoning",
    )

    # Schema definitions
    input_schema: type[BaseModel] | type[StateSchema] | None = Field(
        default=None, description="Schema defining agent inputs (None for auto-derive)"
    )

    output_schema: type[BaseModel] | type[StateSchema] | None = Field(
        default=None, description="Schema defining agent outputs (None for auto-derive)"
    )

    state_schema: type[StateSchema] | type[BaseModel] | None = Field(
        default=None, description="Schema for the agent state (None for auto-derive)"
    )

    # Mapping configuration
    input_mapping: dict[str, str] | None = Field(
        default=None,
        description="Maps state fields to engine input fields (None for auto-derive)",
    )

    output_mapping: dict[str, str] | None = Field(
        default=None,
        description="Maps engine output fields to state fields (None for auto-derive)",
    )

    # Node configuration
    node_name: str = Field(
        default="process", description="Name for the single processing node"
    )

    # Visualization settings
    visualize: bool = Field(default=True, description="Whether to visualize the graph")

    model_config = {"arbitrary_types_allowed": True}

    @field_validator("engine")
    def validate_engine(cls, v):
        """Ensure engine is an AugLLMConfig instance"""
        if not isinstance(v, AugLLMConfig):
            raise TypeError(f"Engine must be AugLLMConfig, got {type(v)}")
        return v

    @field_validator("input_mapping", "output_mapping", mode="after")
    def validate_mappings(cls, v, info):
        """Validate mappings if provided"""
        if v is None:
            return v  # None is allowed for auto-derivation

        if not isinstance(v, dict):
            raise TypeError(f"{info.field_name} must be a dictionary")

        # Validate all keys and values are strings
        for key, value in v.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise TypeError(
                    f"All keys and values in {info.field_name} must be strings"
                )

        return v

    @classmethod
    def from_aug_llm(
        cls,
        aug_llm: AugLLMConfig,
        name: str | None = None,
        id: str | None = None,
        input_schema: type[BaseModel] | None = None,
        output_schema: type[BaseModel] | None = None,
        state_schema: type[StateSchema] | None = None,
        **kwargs,
    ) -> "SimpleAgentConfig":
        """Create a SimpleAgentConfig from an existing AugLLMConfig.

        Args:
            aug_llm: Existing AugLLMConfig to use
            name: Optional agent name
            id: Optional unique identifier
            input_schema: Optional explicit input schema
            output_schema: Optional explicit output schema
            state_schema: Optional explicit state schema
            **kwargs: Additional kwargs for the config

        Returns:
            SimpleAgentConfig instance
        """
        # Generate default name if not provided
        if name is None:
            name = f"simple_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Generate default ID if not provided
        if id is None:
            id = f"agent_{uuid.uuid4().hex[:8]}"

        return cls(
            id=id,
            name=name,
            engine=aug_llm,
            # input_schema=input_schema,
            # output_schema=output_schema,
            # state_schema=state_schema,
            **kwargs,
        )

    @classmethod
    def from_scratch(
        cls,
        system_prompt: str = "You are a helpful assistant.",
        model: str = "gpt-4o",
        temperature: float = 0.7,
        structured_output_model: type[BaseModel] | None = None,
        name: str | None = None,
        id: str | None = None,
        input_schema: type[BaseModel] | None = None,
        output_schema: type[BaseModel] | None = None,
        state_schema: type[StateSchema] | None = None,
        **kwargs,
    ) -> "SimpleAgentConfig":
        """Create a SimpleAgentConfig from scratch with a new AugLLMConfig.

        Args:
            system_prompt: System prompt for the LLM
            model: Model identifier to use
            temperature: Generation temperature
            structured_output_model: Optional model for structured outputs
            name: Optional agent name
            id: Optional unique identifier
            input_schema: Optional explicit input schema
            output_schema: Optional explicit output schema
            state_schema: Optional explicit state schema
            **kwargs: Additional kwargs for the config

        Returns:
            SimpleAgentConfig instance
        """
        # Create base LLM config
        llm_config = AzureLLMConfig(
            model=model, parameters={"temperature": temperature}
        )

        # Create messages for prompt template
        messages = [
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="messages"),
        ]
        prompt_template = ChatPromptTemplate.from_messages(messages)

        # Create AugLLMConfig
        aug_llm = AugLLMConfig(
            name=f"llm_{uuid.uuid4().hex[:6]}",
            llm_config=llm_config,
            prompt_template=prompt_template,
            system_prompt=system_prompt,
            structured_output_model=structured_output_model,
        )

        # If structured output model is provided but no output schema, use the model
        if structured_output_model is not None and output_schema is None:
            output_schema = structured_output_model

        # Create SimpleAgentConfig using from_aug_llm
        return cls.from_aug_llm(
            aug_llm=aug_llm,
            name=name,
            id=id,
            input_schema=input_schema,
            output_schema=output_schema,
            state_schema=state_schema,
            **kwargs,
        )

    @classmethod
    def with_structured_output(
        cls,
        output_model: type[BaseModel],
        system_prompt: str | None = None,
        model: str = "gpt-4o",
        temperature: float = 0.2,
        name: str | None = None,
        **kwargs,
    ) -> "SimpleAgentConfig":
        """Create a SimpleAgentConfig with structured output capabilities.

        Args:
            output_model: Pydantic model for structured output
            system_prompt: Optional system prompt (default derived from model)
            model: Model identifier
            temperature: Generation temperature (lower for structured outputs)
            name: Optional agent name
            **kwargs: Additional kwargs for the config

        Returns:
            SimpleAgentConfig with structured output capability
        """
        # Derive system prompt from model if not provided
        if system_prompt is None:
            model_name = output_model.__name__
            system_prompt = (
                f"You are a helpful assistant that provides detailed responses in a specific format. "
                f"You will analyze the user's request and provide a structured {model_name} response."
            )

        # Create from scratch with structured output model
        return cls.from_scratch(
            system_prompt=system_prompt,
            model=model,
            temperature=temperature,
            structured_output_model=output_model,
            output_schema=output_model,  # Use model as output schema directly
            name=name or f"structured_{output_model.__name__.lower()}_agent",
            **kwargs,
        )
