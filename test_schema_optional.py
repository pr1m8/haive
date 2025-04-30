"""Test script to verify fields from engines are optional by default."""

from typing import Optional, get_origin

from haive.core.schema.schema_composer import SchemaComposer


class MockEngine:
    """Mock engine for testing."""

    def get_schema_fields(self):
        """Return mock schema fields."""
        return {
            "query": (str, ...),  # Required field that should be made optional
            "with_default": (str, "default value"),  # Field with default
        }


# Create schema composer
composer = SchemaComposer()
composer.add_fields_from_engine(MockEngine())

# Convert to manager and get schema
manager = composer.to_manager()
schema = manager.get_schema()

# Print field information
for _field_name, field in schema.__fields__.items():
    field_type = field.annotation
    is_optional = get_origin(field_type) is Optional
    default_value = field.default

# Create instance without providing values
instance = schema()
