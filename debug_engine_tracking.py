#!/usr/bin/env python3
"""Debug engine tracking in SchemaComposer."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7, name="test_llm")

print("=== Debugging Engine Tracking ===")

# Create composer
composer = SchemaComposer(name="TestSchema")

print(f"\nInitial state:")
print(f"  engines: {composer.engines}")
print(f"  engines_by_type: {dict(composer.engines_by_type)}")

# Add fields from the engine
print(f"\nAdding fields from AugLLMConfig...")
composer.add_fields_from_components([config])

print(f"\nAfter add_fields_from_components:")
print(f"  engines: {list(composer.engines.keys())}")
print(f"  engines_by_type: {dict(composer.engines_by_type)}")
print(f"  detected_base_class: {composer.detected_base_class.__name__ if composer.detected_base_class else 'None'}")

# Check if LLM engines are detected in the second call
print(f"\nChecking if engines_by_type has 'llm':")
print(f"  'llm' in engines_by_type: {'llm' in composer.engines_by_type}")
print(f"  engines_by_type.get('llm', []): {composer.engines_by_type.get('llm', [])}")

# Test the detection logic directly
print(f"\nTesting detection logic without components:")
has_llm_engine = False
for engine_name in composer.engines_by_type.get("llm", []):
    has_llm_engine = True
    print(f"  Found LLM engine: {engine_name}")
    break
print(f"  has_llm_engine from engines_by_type: {has_llm_engine}")

# Now call build
print(f"\nCalling build()...")
schema = composer.build()
print(f"  Schema MRO: {[cls.__name__ for cls in schema.__mro__]}")