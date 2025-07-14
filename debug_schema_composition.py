#!/usr/bin/env python3
"""Debug schema composition issue with AugLLMConfig."""

from haive.core.engine.aug_llm.config import AugLLMConfig
from haive.core.schema.composer import SchemaComposer
from langchain_core.prompts import ChatPromptTemplate

# Create a simple prompt template
simple_prompt = ChatPromptTemplate.from_messages(
    [("system", "You are a helpful assistant"), ("human", "{query}")]
)

# Create AugLLMConfig
config = AugLLMConfig(prompt_template=simple_prompt, temperature=0.7)


# Create composer and detect base class
composer = SchemaComposer(name="TestSchema")

# Add the config to components
composer.add_fields_from_components([config])

# Check what base class was detected

# Build the schema
schema = composer.build()

for field_name, field_info in schema.__fields__.items():
    default_value = field_info.default
    if default_value is ...:
        pass")
    else:
        pass")

for cls in schema.__mro__:
    pass

# Try to instantiate the schema
try:
    instance = schema()

    # Check field values
    for field_name in schema.__fields__:
        value = getattr(instance, field_name)
        if value is ...:
            pass")
        else:
            pass")

except Exception as e:
    import traceback

    traceback.print_exc()

# Test the from_components class method
try:
    schema_class = SchemaComposer.from_components([config], name="DirectSchema")

    instance2 = schema_class()

except Exception as e:
    import traceback

    traceback.print_exc()
