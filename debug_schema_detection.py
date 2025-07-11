#!/usr/bin/env python3
"""Debug the base class detection logic in detail."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7)

print("=== Tracing Base Class Detection ===")

# Create composer
composer = SchemaComposer(name="TestSchema")

# Check initial state
print(f"\nInitial state:")
print(f"  has_messages: {composer.has_messages}")
print(f"  has_tools: {composer.has_tools}")
print(f"  detected_base_class: {composer.detected_base_class}")

# Manually trace through the detection logic
print(f"\nChecking component:")
print(f"  hasattr(config, 'engine_type'): {hasattr(config, 'engine_type')}")
if hasattr(config, "engine_type"):
    engine_type_value = getattr(config.engine_type, "value", config.engine_type)
    engine_type_str = str(engine_type_value).lower()
    print(f"  engine_type_value: {engine_type_value}")
    print(f"  engine_type_str: {engine_type_str}")
    print(f"  engine_type_str == 'llm': {engine_type_str == 'llm'}")

# Call the detection method
print(f"\nCalling _detect_base_class_requirements...")
composer._detect_base_class_requirements([config])

print(f"\nAfter detection:")
print(f"  has_messages: {composer.has_messages}")
print(f"  has_tools: {composer.has_tools}")
print(f"  detected_base_class: {composer.detected_base_class}")
print(f"  detected_base_class name: {composer.detected_base_class.__name__ if composer.detected_base_class else 'None'}")

# Check if it's detecting has_llm_engine correctly
print(f"\nChecking has_llm_engine logic:")
has_llm_engine = False
if hasattr(config, "engine_type"):
    engine_type_value = getattr(config.engine_type, "value", config.engine_type)
    engine_type_str = str(engine_type_value).lower()
    if engine_type_str == "llm":
        has_llm_engine = True
        print(f"  ✓ Found LLM engine, has_llm_engine = {has_llm_engine}")

# Import the base classes to check what should be used
from haive.core.schema.prebuilt.llm_state import LLMState
from haive.core.schema.prebuilt.messages_state import MessagesState
from haive.core.schema.prebuilt.tool_state import ToolState

print(f"\nExpected base class: LLMState")
print(f"Actual base class: {composer.detected_base_class.__name__ if composer.detected_base_class else 'None'}")

# Check the MRO of each base class
print(f"\nLLMState MRO: {[cls.__name__ for cls in LLMState.__mro__]}")
print(f"MessagesState MRO: {[cls.__name__ for cls in MessagesState.__mro__]}")

# Build the schema to see the full result
schema = composer.build()
print(f"\nBuilt schema MRO: {[cls.__name__ for cls in schema.__mro__]}")