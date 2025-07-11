import logging
logging.basicConfig(level=logging.DEBUG)

from haive.core.schema.field_definition import FieldDefinition
from typing import Any

# Test a simple field creation
field_def = FieldDefinition(
    name="context",
    field_type=str,
    default="",  # Should make it optional
    description="Test context field"
)

print("🔍 Testing field definition...")
field_type, field_info = field_def.to_field_info()
print(f"Field info: default={field_info.default}, required={field_info.default is ...}")