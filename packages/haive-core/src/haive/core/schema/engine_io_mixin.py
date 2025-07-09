"""Engine I/O Schema Mixin for State Schemas.

This module provides a mixin to handle engine-related I/O logic separately
from the core state schema functionality. This separation makes the code
more modular and allows for optional engine capabilities.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Type

from pydantic import BaseModel, Field
from rich.console import Console

if TYPE_CHECKING:
    from haive.core.engine.base import Engine

logger = logging.getLogger(__name__)
console = Console()


class EngineIOSchemaMixin(BaseModel):
    """Mixin to add engine I/O management capabilities to state schemas.

    This mixin provides:
    - Engine I/O field mappings
    - Engine validation and serialization
    - Convenience properties for engine access
    - Engine-related state operations
    """

    # Engine I/O tracking metadata
    __engine_io_mappings__: Dict[str, Dict[str, List[str]]] = {}
    __input_fields__: Dict[str, List[str]] = {}
    __output_fields__: Dict[str, List[str]] = {}
    __structured_models__: Dict[str, str] = {}
    __structured_model_fields__: Dict[str, List[str]] = {}

    # Convenience properties for accessing engines
    @property
    def llm(self) -> Optional[Any]:
        """Convenience property to access the LLM engine."""
        # First check the main engine field
        if (
            hasattr(self, "engine")
            and self.engine
            and hasattr(self.engine, "engine_type")
        ):
            engine_type_str = str(self.engine.engine_type).lower()
            if "llm" in engine_type_str:
                return self.engine

        # Then check engines dict for LLM
        if hasattr(self, "engines"):
            for name, eng in self.engines.items():
                if hasattr(eng, "engine_type"):
                    engine_type_str = str(eng.engine_type).lower()
                    if "llm" in engine_type_str:
                        return eng

        return None

    @property
    def main_engine(self) -> Optional[Any]:
        """Convenience property to access the main engine."""
        if hasattr(self, "engine") and self.engine:
            return self.engine
        if hasattr(self, "engines") and self.engines:
            return self.engines.get("main")
        return None

    def get_engine_io_mappings(self) -> Dict[str, Dict[str, List[str]]]:
        """Get engine I/O mappings for this state schema."""
        return getattr(self.__class__, "__engine_io_mappings__", {})

    def get_engine_input_fields(self, engine_name: str) -> List[str]:
        """Get input fields for a specific engine."""
        mappings = self.get_engine_io_mappings()
        return mappings.get(engine_name, {}).get("inputs", [])

    def get_engine_output_fields(self, engine_name: str) -> List[str]:
        """Get output fields for a specific engine."""
        mappings = self.get_engine_io_mappings()
        return mappings.get(engine_name, {}).get("outputs", [])

    def get_all_engine_input_fields(self) -> Set[str]:
        """Get all input fields across all engines."""
        fields = set()
        for mapping in self.get_engine_io_mappings().values():
            fields.update(mapping.get("inputs", []))
        return fields

    def get_all_engine_output_fields(self) -> Set[str]:
        """Get all output fields across all engines."""
        fields = set()
        for mapping in self.get_engine_io_mappings().values():
            fields.update(mapping.get("outputs", []))
        return fields

    def prepare_engine_input(self, engine_name: str) -> Dict[str, Any]:
        """Prepare input data for a specific engine."""
        input_fields = self.get_engine_input_fields(engine_name)
        result = {}

        for field_name in input_fields:
            if hasattr(self, field_name):
                result[field_name] = getattr(self, field_name)

        return result

    def update_from_engine_output(
        self, engine_name: str, output_data: Dict[str, Any]
    ) -> None:
        """Update state from engine output data."""
        output_fields = self.get_engine_output_fields(engine_name)

        for field_name in output_fields:
            if field_name in output_data:
                if hasattr(self, field_name):
                    setattr(self, field_name, output_data[field_name])
                else:
                    logger.warning(f"Field {field_name} not found in state schema")

    def get_engines_for_field(self, field_name: str) -> List[str]:
        """Get list of engines that use a specific field."""
        engines = []
        for engine_name, mapping in self.get_engine_io_mappings().items():
            if field_name in mapping.get("inputs", []) or field_name in mapping.get(
                "outputs", []
            ):
                engines.append(engine_name)
        return engines

    def validate_engine_compatibility(self, engine_name: str, engine: Any) -> bool:
        """Validate that an engine is compatible with expected I/O fields."""
        expected_inputs = set(self.get_engine_input_fields(engine_name))
        expected_outputs = set(self.get_engine_output_fields(engine_name))

        # Check if engine has get_input_fields and get_output_fields methods
        if hasattr(engine, "get_input_fields") and hasattr(engine, "get_output_fields"):
            try:
                actual_inputs = set(engine.get_input_fields().keys())
                actual_outputs = set(engine.get_output_fields().keys())

                # Check for compatibility (subset relationship)
                input_compatible = expected_inputs.issubset(actual_inputs)
                output_compatible = expected_outputs.issubset(actual_outputs)

                if not input_compatible:
                    logger.warning(
                        f"Engine {engine_name} missing input fields: {expected_inputs - actual_inputs}"
                    )
                if not output_compatible:
                    logger.warning(
                        f"Engine {engine_name} missing output fields: {expected_outputs - actual_outputs}"
                    )

                return input_compatible and output_compatible
            except Exception as e:
                logger.warning(f"Could not validate engine compatibility: {e}")
                return False

        return True  # Can't validate, assume compatible

    def get_schema_summary(self) -> Dict[str, Any]:
        """Get a summary of the engine I/O schema configuration."""
        return {
            "engine_io_mappings": self.get_engine_io_mappings(),
            "all_input_fields": list(self.get_all_engine_input_fields()),
            "all_output_fields": list(self.get_all_engine_output_fields()),
            "structured_models": getattr(self.__class__, "__structured_models__", {}),
            "structured_model_fields": getattr(
                self.__class__, "__structured_model_fields__", {}
            ),
        }
