#!/usr/bin/env python3
"""Debug what happens during build method."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7)

print("=== Debugging Build Method ===")

# Create composer
composer = SchemaComposer(name="TestSchema")

# Add fields from components
print("Adding fields from components...")
composer.add_fields_from_components([config])

print(f"\nAfter add_fields_from_components:")
print(f"  detected_base_class: {composer.detected_base_class.__name__ if composer.detected_base_class else 'None'}")

# Now build
print(f"\nCalling build()...")
schema = composer.build()

print(f"\nAfter build:")
print(f"  Schema MRO: {[cls.__name__ for cls in schema.__mro__]}")

# Check if the detected_base_class was None before build
print(f"\nChecking if detected_base_class was None in build()...")
composer2 = SchemaComposer(name="TestSchema2")
print(f"  New composer detected_base_class: {composer2.detected_base_class}")

# Add fields but don't detect base class
composer2.add_fields_from_components([config])
# Manually set it to None to simulate the issue
composer2.detected_base_class = None
print(f"  Set detected_base_class to None")

# Now build and see what happens
schema2 = composer2.build()
print(f"  After build with None: {[cls.__name__ for cls in schema2.__mro__]}")