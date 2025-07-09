"""Schema composition module.

This module provides tools for dynamically building state schemas from components,
engines, and other sources. It's organized into focused submodules:

- engine: Engine management and integration
- field: Field extraction and composition
- builder: Core schema building logic
- utils: Utility functions and helpers
"""

from haive.core.schema.composer.engine.engine_manager import EngineComposerMixin
from haive.core.schema.composer.field.field_extractor import FieldExtractorMixin
from haive.core.schema.composer.schema_composer import SchemaComposer

__all__ = [
    "SchemaComposer",
    "EngineComposerMixin",
    "FieldExtractorMixin",
]
