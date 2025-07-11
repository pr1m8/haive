# src/haive/core/graph/StateSchema.py
from typing import Any

from pydantic import BaseModel, Field, create_model


class StateSchema:
    """Enhanced schema management system with RunnableConfig awareness."""

    def __init__(self, name: str = "State", fields: dict[str, Any] | None = None):
        self.name = name
        self.fields = fields or {}
        self.config_aware_fields = set()

    def add_field(
        self,
        name: str,
        type_hint: type,
        default: Any = None,
        config_aware: bool = False,
    ) -> "StateSchema":
        """Add a field to the schema, with optional config awareness."""
        self.fields[name] = (type_hint, Field(default=default))

        if config_aware:
            self.config_aware_fields.add(name)

        return self

    def mark_config_aware(self, field_name: str) -> "StateSchema":
        """Mark an existing field as config-aware."""
        if field_name in self.fields:
            self.config_aware_fields.add(field_name)
        return self

    def create_model(self) -> type[BaseModel]:
        """Create a Pydantic model from this schema."""
        model = create_model(self.name, **self.fields)

        # Add config awareness information
        model._config_aware_fields = self.config_aware_fields

        # Add config application method
        def apply_config(instance, config):
            """Apply configuration values to config-aware fields."""
            if not hasattr(instance, "_config_aware_fields"):
                return instance

            if not config or not hasattr(config, "configurable"):
                return instance

            # Update config-aware fields if they exist in config
            for field in instance._config_aware_fields:
                if (
                    hasattr(config.configurable, field)
                    and getattr(config.configurable, field) is not None
                ):
                    setattr(instance, field, getattr(config.configurable, field))

            return instance

        model.apply_config = apply_config

        return model

    @classmethod
    def from_models(
        cls, *models: type[BaseModel], name: str = "ComposedState"
    ) -> "StateSchema":
        """Create a schema from multiple Pydantic models."""
        schema = cls(name=name)

        for model in models:
            # Get fields from the model
            model_fields = {}

            # Handle Pydantic v2
            if hasattr(model, "model_fields"):
                for field_name, field_info in model.model_fields.items():
                    model_fields[field_name] = (field_info.annotation, field_info)
            # Handle Pydantic v1
            elif hasattr(model, "__fields__"):
                for field_name, field_info in model.__fields__.items():
                    model_fields[field_name] = (field_info.type_, field_info)

            # Add fields to schema
            for field_name, (type_hint, field_info) in model_fields.items():
                schema.add_field(field_name, type_hint, field_info.default)

            # Transfer config awareness if present
            if hasattr(model, "_config_aware_fields"):
                for field in model._config_aware_fields:
                    if field in schema.fields:
                        schema.mark_config_aware(field)

        return schema

    @classmethod
    def from_aug_llm(cls, aug_llm_config, name: str | None = None) -> "StateSchema":
        """Create schema from AugLLMConfig."""
        # Extract name from AugLLMConfig if not provided
        schema_name = name or f"{aug_llm_config.name}State"
        schema = cls(name=schema_name)

        # Add fields based on prompt template
        if (
            hasattr(aug_llm_config, "prompt_template")
            and aug_llm_config.prompt_template
        ):
            # Extract input variables
            input_vars = []
            if hasattr(aug_llm_config.prompt_template, "input_variables"):
                input_vars = aug_llm_config.prompt_template.input_variables

            # Add fields for input variables
            for var in input_vars:
                schema.add_field(var, str, default=None)

        # Add fields for structured output
        if (
            hasattr(aug_llm_config, "structured_output_model")
            and aug_llm_config.structured_output_model
        ):
            model_class = aug_llm_config.structured_output_model
            field_name = model_class.__name__.lower()

            # Add field for the structured output
            from typing import Optional as OptionalType

            schema.add_field(field_name, OptionalType[model_class], default=None)

        return schema
