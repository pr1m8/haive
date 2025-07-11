#!/usr/bin/env python3
"""Debug why LLMState is not being used."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7)

print("=== Debugging Base Class Detection ===")
print(f"Config type: {type(config)}")
print(f"Config engine_type: {config.engine_type}")
print(f"Config engine_type value: {getattr(config.engine_type, 'value', config.engine_type)}")
print(f"String of engine_type: {str(config.engine_type)}")
print(f"Lowercase: {str(config.engine_type).lower()}")

# Check what the detection method sees
composer = SchemaComposer(name="TestSchema")

# Manually call the detection method
print("\nCalling _detect_base_class_requirements with the config...")
composer._detect_base_class_requirements([config])

print(f"\nDetected base class: {composer.detected_base_class}")
print(f"Has messages: {composer.has_messages}")
print(f"Has tools: {composer.has_tools}")

# Check the value comparison
engine_type_value = getattr(config.engine_type, "value", config.engine_type)
engine_type_str = str(engine_type_value).lower()
print(f"\nEngine type string for comparison: '{engine_type_str}'")
print(f"Is it 'llm'? {engine_type_str == 'llm'}")

# Check the full enum
print(f"\nFull engine_type enum: {config.engine_type}")
print(f"Engine type class: {type(config.engine_type)}")

# Check if it's an enum
if hasattr(config.engine_type, 'value'):
    print(f"Enum value: {config.engine_type.value}")
    print(f"Enum name: {config.engine_type.name}")