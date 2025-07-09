"""Multi-agent state schema for the Haive framework.

This module provides a specialized StateSchema for multi-agent architectures,
addressing key issues with engine handling, consolidation, and access from
engine nodes. It ensures proper engine access and visibility for sub-agents
in complex agent workflows.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional, Type, Union

from pydantic import Field, create_model, model_validator

from haive.core.logging.rich_logger import get_logger
from haive.core.schema.state_schema import StateSchema

# Get logger instance
logger = get_logger(__name__)


class MultiAgentStateSchema(StateSchema):
    """Enhanced StateSchema for multi-agent architectures.

    This class extends the base StateSchema with features specifically designed
    for multi-agent scenarios, solving common issues with engine handling and
    access in nested agent structures. It ensures that engines are properly
    accessible to EngineNodeConfig via the state.engines dictionary.

    Key Features:
    - Automatic engines field creation and population
    - Consolidation of engines from sub-agents
    - Engine visibility for engine nodes
    - Compatibility with EngineNodeConfig._get_engine()

    This schema should be used as the base class for states in multi-agent
    architectures to ensure proper engine access and visibility.
    """

    # Explicit engines field that EngineNodeConfig expects
    engines: Dict[str, Any] = Field(
        default_factory=dict, description="Dictionary of engines accessible to nodes"
    )

    @model_validator(mode="after")
    def populate_engines_dict(self) -> "MultiAgentStateSchema":
        """
        Populate the engines dictionary with all available engines.

        This validator runs after the model is created and:
        1. Collects engines from individual fields
        2. Collects engines from class-level .engines
        3. Collects engines from sub-agents if present
        4. Consolidates all engines into the state.engines dictionary
        """
        logger.debug(f"Populating engines dict for {self.__class__.__name__}")

        # Start with an empty engines dict if none exists
        if not hasattr(self, "engines"):
            self.engines = {}
        elif self.engines is None:
            self.engines = {}

        # 1. First collect engines from instance fields
        field_engines = self.get_engines()
        if field_engines:
            logger.debug(f"Found {len(field_engines)} engines in instance fields")
            self.engines.update(field_engines)

        # 2. Then add engines from class-level .engines
        class_engines = self.__class__.get_all_class_engines()
        if class_engines:
            logger.debug(f"Found {len(class_engines)} engines at class level")
            for name, engine in class_engines.items():
                if name not in self.engines:
                    self.engines[name] = engine

        # 3. Handle sub-agents in 'agents' field if present
        if hasattr(self, "agents") and isinstance(self.agents, dict):
            logger.debug(f"Found agents dictionary with {len(self.agents)} agents")

            for agent_name, agent in self.agents.items():
                # Add the agent itself as an engine
                if hasattr(agent, "engine_type"):
                    engine_name = getattr(agent, "name", agent_name)
                    if engine_name not in self.engines:
                        logger.debug(f"Adding agent '{engine_name}' to engines dict")
                        self.engines[engine_name] = agent

                # Add engines from the agent
                if hasattr(agent, "engines") and isinstance(agent.engines, dict):
                    logger.debug(
                        f"Agent '{agent_name}' has {len(agent.engines)} engines"
                    )
                    for eng_name, engine in agent.engines.items():
                        # Use qualified name to avoid collisions
                        qualified_name = f"{agent_name}.{eng_name}"
                        logger.debug(
                            f"Adding engine '{qualified_name}' from agent '{agent_name}'"
                        )
                        self.engines[qualified_name] = engine

                        # Also add with original name if not already present
                        if eng_name not in self.engines:
                            self.engines[eng_name] = engine

        logger.debug(f"Populated engines dict with {len(self.engines)} total engines")
        return self

    @classmethod
    def from_state_schema(
        cls, schema_class: Type[StateSchema], name: Optional[str] = None
    ) -> Type[MultiAgentStateSchema]:
        """
        Create a MultiAgentStateSchema from an existing StateSchema class.

        Args:
            schema_class: Original StateSchema class to convert
            name: Optional name for the new schema (defaults to original name with 'Multi' prefix)

        Returns:
            A new MultiAgentStateSchema subclass with all fields and behaviors from the original
        """
        # Generate a name if not provided
        if name is None:
            name = f"Multi{schema_class.__name__}"

        # Create field definitions from original schema
        field_defs = {}
        for field_name, field_info in schema_class.model_fields.items():
            # Skip the engines field if present (we'll add our own)
            if field_name == "engines":
                continue

            # Skip special fields
            if field_name.startswith("__"):
                continue

            # Add the field
            field_defs[field_name] = (field_info.annotation, field_info)

        # Create the new schema class
        multi_schema = create_model(name, __base__=cls, **field_defs)

        # Copy class variables from original schema
        if hasattr(schema_class, "__shared_fields__"):
            multi_schema.__shared_fields__ = list(schema_class.__shared_fields__)

        if hasattr(schema_class, "__serializable_reducers__"):
            multi_schema.__serializable_reducers__ = dict(
                schema_class.__serializable_reducers__
            )

        if hasattr(schema_class, "__reducer_fields__"):
            multi_schema.__reducer_fields__ = dict(schema_class.__reducer_fields__)

        if hasattr(schema_class, "__engine_io_mappings__"):
            multi_schema.__engine_io_mappings__ = {
                k: v.copy() for k, v in schema_class.__engine_io_mappings__.items()
            }

        if hasattr(schema_class, "__input_fields__"):
            multi_schema.__input_fields__ = {
                k: list(v) for k, v in schema_class.__input_fields__.items()
            }

        if hasattr(schema_class, "__output_fields__"):
            multi_schema.__output_fields__ = {
                k: list(v) for k, v in schema_class.__output_fields__.items()
            }

        if hasattr(schema_class, "__structured_models__"):
            multi_schema.__structured_models__ = dict(
                schema_class.__structured_models__
            )

        if hasattr(schema_class, "__structured_model_fields__"):
            multi_schema.__structured_model_fields__ = {
                k: list(v) for k, v in schema_class.__structured_model_fields__.items()
            }

        # Copy engines if present
        if hasattr(schema_class, "engines"):
            multi_schema.engines = dict(schema_class.engines)

        return multi_schema


class MultiAgentSchemaComposer:
    """Utility for creating MultiAgentStateSchema classes.

    This class provides static methods for creating MultiAgentStateSchema classes
    from existing schemas or components, ensuring proper engine handling in
    multi-agent architectures.
    """

    @staticmethod
    def from_schema(
        schema_class: Type[StateSchema], name: Optional[str] = None
    ) -> Type[MultiAgentStateSchema]:
        """
        Create a MultiAgentStateSchema from an existing StateSchema.

        Args:
            schema_class: Original StateSchema to convert
            name: Optional name for the new schema

        Returns:
            A new MultiAgentStateSchema class
        """
        return MultiAgentStateSchema.from_state_schema(schema_class, name)

    @staticmethod
    def from_components(
        components: List[Any], name: str = "MultiAgentSchema"
    ) -> Type[MultiAgentStateSchema]:
        """
        Create a MultiAgentStateSchema from components.

        Args:
            components: List of components to extract fields from
            name: Name for the schema class

        Returns:
            A new MultiAgentStateSchema class
        """
        from haive.core.schema.schema_composer import SchemaComposer

        # Use standard SchemaComposer to build from components
        composer = SchemaComposer(name=name)
        composer.add_fields_from_components(components)

        # Build the schema
        base_schema = composer.build()

        # Convert to MultiAgentStateSchema
        return MultiAgentStateSchema.from_state_schema(base_schema, name)
