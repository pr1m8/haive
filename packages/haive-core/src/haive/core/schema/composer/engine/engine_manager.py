"""Engine management mixin for SchemaComposer."""

import logging
from collections import defaultdict
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class EngineComposerMixin:
    """Mixin that handles engine management in SchemaComposer.

    This mixin provides all engine-related functionality:
    - Engine tracking and registration
    - Engine type categorization
    - Engine provider updates
    - Engine field extraction
    """

    def __init__(self, *args, **kwargs):
        """Initialize engine tracking structures."""
        super().__init__(*args, **kwargs)

        # Engine tracking
        self.engines: dict[str, Any] = {}
        self.engines_by_type: dict[str, list[str]] = defaultdict(list)

        # Processing history for debugging
        if not hasattr(self, "processing_history"):
            self.processing_history: list[dict[str, Any]] = []

    def add_engine(self, engine: Any) -> "EngineComposerMixin":
        """Add an engine to the composer for tracking and later updates.

        Args:
            engine: Engine to add

        Returns:
            Self for chaining
        """
        if engine is None:
            return self

        # Get engine name and type
        engine_name = getattr(engine, "name", f"engine_{id(engine)}")
        engine_type = getattr(engine, "engine_type", None)

        # Store engine
        self.engines[engine_name] = engine

        # Track by type if available - avoid duplicates
        if engine_type:
            engine_type_str = (
                engine_type.value if hasattr(engine_type, "value") else str(engine_type)
            )
            # Only add if not already in the list (avoid duplicates)
            if engine_name not in self.engines_by_type[engine_type_str]:
                self.engines_by_type[engine_type_str].append(engine_name)
                logger.debug(
                    f"Added engine '{engine_name}' of type '{engine_type_str}'"
                )
            else:
                logger.debug(
                    f"Engine '{engine_name}' already exists in engines_by_type for type '{engine_type_str}'"
                )

        # Add tracking entry
        self.processing_history.append(
            {
                "action": "add_engine",
                "engine_name": engine_name,
                "engine_type": engine_type,
            }
        )

        return self

    def update_engine_provider(
        self, engine_type: str, updates: dict[str, Any]
    ) -> "EngineComposerMixin":
        """Update configuration for all engines of a specific type.

        Args:
            engine_type: Type of engines to update (e.g., "llm", "retriever")
            updates: Dictionary of updates to apply

        Returns:
            Self for chaining
        """
        logger.debug(f"Updating all {engine_type} engines with: {updates}")

        updated_count = 0
        for engine_name in self.engines_by_type.get(engine_type, []):
            if engine_name in self.engines:
                engine = self.engines[engine_name]

                # For LLM engines, update llm_config field
                if engine_type == "llm" and hasattr(engine, "llm_config"):
                    for key, value in updates.items():
                        if hasattr(engine.llm_config, key):
                            setattr(engine.llm_config, key, value)
                            logger.debug(
                                f"Updated {engine_name}.llm_config.{key} = {value}"
                            )
                            updated_count += 1

                # For other engine types, update directly
                else:
                    for key, value in updates.items():
                        if hasattr(engine, key):
                            setattr(engine, key, value)
                            logger.debug(f"Updated {engine_name}.{key} = {value}")
                            updated_count += 1

        logger.info(
            f"Updated {updated_count} fields across {len(self.engines_by_type.get(engine_type, []))} {engine_type} engines"
        )

        # Add tracking entry
        self.processing_history.append(
            {
                "action": "update_engine_provider",
                "engine_type": engine_type,
                "updates": updates,
                "affected_engines": updated_count,
            }
        )

        return self

    def get_engines_by_type(self, engine_type: str) -> list[Any]:
        """Get all engines of a specific type.

        Args:
            engine_type: Type of engines to retrieve

        Returns:
            List of engines of the specified type
        """
        engine_names = self.engines_by_type.get(engine_type, [])
        return [self.engines[name] for name in engine_names if name in self.engines]

    def add_engine_management(self) -> "EngineComposerMixin":
        """Add standardized engine management fields to the schema.

        This method adds the new engine management pattern to support:
        - Optional 'engine' field for primary/main engine
        - Explicit 'engines' dict field (was implicit before)
        - Automatic synchronization between the two

        Returns:
            Self for chaining
        """
        logger.debug("Adding standardized engine management fields")

        # Import engine type if available
        engine_type = Any
        try:
            from typing import Optional

            from haive.core.engine.base import Engine

            engine_type = Optional[Engine]
        except ImportError:
            logger.debug("Could not import Engine type, using Any")

        # Add optional engine field if not present
        if "engine" not in self.fields and "engine" not in self.base_class_fields:
            self.add_field(
                name="engine",
                field_type=engine_type,
                default=None,
                description="Optional main/primary engine for convenience",
                source="engine_management",
            )
            logger.debug("Added 'engine' field for primary engine")

        # Add explicit engines dict if not present
        if "engines" not in self.fields and "engines" not in self.base_class_fields:

            self.add_field(
                name="engines",
                field_type=dict[str, Any],
                default_factory=dict,
                description="Engine registry for this state (backward compatible)",
                source="engine_management",
            )
            logger.debug("Added 'engines' dict field for engine registry")

        return self
