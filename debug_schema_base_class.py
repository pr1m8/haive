#!/usr/bin/env python3
"""Debug why LLMState is not being used."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer

# Create AugLLMConfig
config = AugLLMConfig(temperature=0.7)


# Check what the detection method sees
composer = SchemaComposer(name="TestSchema")

# Manually call the detection method
composer._detect_base_class_requirements([config])


# Check the value comparison
engine_type_value = getattr(config.engine_type, "value", config.engine_type)
engine_type_str = str(engine_type_value).lower()

# Check the full enum

# Check if it's an enum
if hasattr(config.engine_type, "value"):
