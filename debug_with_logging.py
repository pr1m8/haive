#!/usr/bin/env python3
"""Debug with logging to see what's happening."""

import logging

# Set up logging to see debug messages
logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7)

print("=== Creating schema with logging enabled ===")

# Use from_components to see the full flow
schema_class = SchemaComposer.from_components([config], name="TestSchema")

print(f"\nResulting schema: {schema_class}")
print(f"Base classes: {[cls.__name__ for cls in schema_class.__mro__]}")

# Check if it has the required fields
print("\nChecking for required fields:")
for field in ['messages', 'token_usage', 'engine', 'engines']:
    has_field = field in schema_class.model_fields
    print(f"  {field}: {'✓' if has_field else '✗'}")

# Try to create instance
print("\nCreating instance...")
try:
    instance = schema_class()
    print("✓ Successfully created instance")
except Exception as e:
    print(f"✗ Failed: {e}")